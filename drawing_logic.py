import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import streamlit as st
import tempfile
import time
import os
from utils import load_background_image

def start_drawing_loop():
    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils

    # Open Webcam
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = 1280, 720
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    canvas = np.zeros((screen_height, screen_width, 3), np.uint8)

    # Load background if provided
    bg_img = load_background_image(st.session_state.uploaded_file, screen_width, screen_height)
    st.session_state.bg_img = bg_img

    # Drawing settings
    draw_color = (255, 255, 255)
    prev_pos = None
    pos_buffer = deque(maxlen=4)
    wrist_buffer = deque(maxlen=60)
    hover_zone = 35
    hover_time_required = 15
    hover_counter = 0
    hovered_color = None

    frame_placeholder = st.empty()

    try:
        while st.session_state.start_drawing:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture webcam feed. Check if the webcam is connected.")
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (screen_width, screen_height))
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Background logic
            if bg_img is not None:
                faint_bg = cv2.addWeighted(bg_img, 1, np.zeros_like(bg_img), 0.7, 0)
                frame = faint_bg.copy()

            results = hands.process(rgb_frame)

            # Draw buttons
            button_y = int(screen_height * 0.05)
            button_positions = [
                (0.05, (0, 0, 255)),
                (0.12, (0, 255, 0)),
                (0.19, (255, 0, 0)),
                (0.26, (0, 255, 255)),
                (0.33, (255, 255, 255)),
            ]
            for pos_x, color in button_positions:
                cv2.circle(frame, (int(screen_width * pos_x), button_y), 30, color, cv2.FILLED)
                if color == (255, 255, 255):
                    cv2.circle(frame, (int(screen_width * pos_x), button_y), 30, (0, 0, 0), 2)

            # Eraser button
            eraser_center_x = int(screen_width * 0.40)
            eraser_center_y = button_y
            cv2.rectangle(frame,
                          (eraser_center_x - 35, eraser_center_y - 25),
                          (eraser_center_x + 35, eraser_center_y + 25),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(frame,
                          (eraser_center_x - 35, eraser_center_y - 25),
                          (eraser_center_x + 35, eraser_center_y + 25),
                          (0, 0, 0), 2)

            # Hand tracking
            if results.multi_hand_landmarks:
                for hand_lm in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

                    lm_list = [(int(lm.x * screen_width), int(lm.y * screen_height))
                               for lm in hand_lm.landmark]

                    if len(lm_list) > 20:
                        index_tip = lm_list[8]
                        wrist = lm_list[0]

                        # Draw tip
                        if draw_color == (0, 0, 0):
                            cv2.rectangle(frame, (index_tip[0] - 17, index_tip[1] - 12),
                                          (index_tip[0] + 17, index_tip[1] + 12),
                                          (255, 255, 255), cv2.FILLED)
                            cv2.rectangle(frame, (index_tip[0] - 17, index_tip[1] - 12),
                                          (index_tip[0] + 17, index_tip[1] + 12),
                                          (0, 0, 0), 1)
                        else:
                            cv2.circle(frame, index_tip, 15, draw_color, cv2.FILLED)

                        # Smooth wrist position to reduce noise
                        wrist_buffer.append(wrist)
                        if len(wrist_buffer) >= 30:
                            smoothed_wrist_x = np.mean([p[0] for p in wrist_buffer])
                            changes = 0
                            min_amplitude = 20
                            for i in range(1, len(wrist_buffer) - 1):
                                if (wrist_buffer[i][0] > wrist_buffer[i-1][0] + min_amplitude and
                                    wrist_buffer[i][0] > wrist_buffer[i+1][0] + min_amplitude) or \
                                   (wrist_buffer[i][0] < wrist_buffer[i-1][0] - min_amplitude and
                                    wrist_buffer[i][0] < wrist_buffer[i+1][0] - min_amplitude):
                                    changes += 1

                            # Check for open-hand gesture
                            is_open_hand = (
                                lm_list[8][1] < lm_list[6][1] and
                                lm_list[12][1] < lm_list[10][1] and
                                lm_list[16][1] < lm_list[14][1] and
                                lm_list[20][1] < lm_list[18][1]
                            )

                            # Clear canvas if shake is detected and hand is open
                            if changes >= 3 and is_open_hand:
                                canvas = np.zeros((screen_height, screen_width, 3), np.uint8)
                                prev_pos = None
                                pos_buffer.clear()
                                wrist_buffer.clear()
                                continue

                        # Hover color select
                        color_buttons = [
                            (int(screen_width * 0.05), button_y, (0, 0, 255)),
                            (int(screen_width * 0.12), button_y, (0, 255, 0)),
                            (int(screen_width * 0.19), button_y, (255, 0, 0)),
                            (int(screen_width * 0.26), button_y, (0, 255, 255)),
                            (int(screen_width * 0.33), button_y, (255, 255, 255)),
                            (int(screen_width * 0.40), button_y, (0, 0, 0)),
                        ]
                        current_hover = None
                        for (bx, by, color) in color_buttons:
                            if abs(index_tip[0] - bx) < hover_zone and abs(index_tip[1] - by) < hover_zone:
                                current_hover = color
                                break
                        if current_hover == hovered_color:
                            hover_counter += 1
                        else:
                            hovered_color = current_hover
                            hover_counter = 0
                        if hovered_color is not None and hover_counter >= hover_time_required:
                            draw_color = hovered_color
                            hover_counter = 0
                            prev_pos = None
                            pos_buffer.clear()

                        # Drawing
                        if lm_list[8][1] < lm_list[5][1] and lm_list[12][1] > lm_list[9][1]:
                            pos_buffer.append(index_tip)
                            if len(pos_buffer) > 1:
                                avg_x = int(np.mean([p[0] for p in pos_buffer]))
                                avg_y = int(np.mean([p[1] for p in pos_buffer]))
                                smoothed_pos = (avg_x, avg_y)
                                if prev_pos is None:
                                    prev_pos = smoothed_pos
                                thickness = 30 if draw_color == (0, 0, 0) else 5
                                cv2.line(canvas, prev_pos, smoothed_pos, draw_color, thickness)
                                prev_pos = smoothed_pos
                        else:
                            prev_pos = None
                            pos_buffer.clear()

            frame = cv2.add(frame, canvas)
            frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            st.session_state.canvas = canvas.copy()

            # Small sleep to prevent excessive CPU usage
            time.sleep(0.01)

    except Exception as e:
        st.error(f"Error in drawing loop: {e}")
    finally:
        cap.release()
        hands.close()
        # Clean up any temporary saved image file
        if st.session_state.saved_image_path and os.path.exists(st.session_state.saved_image_path):
            os.unlink(st.session_state.saved_image_path)