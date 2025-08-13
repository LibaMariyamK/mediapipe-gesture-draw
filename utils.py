import cv2
import streamlit as st
import tempfile
import os
import numpy as np  # Added import for numpy

def save_image(canvas, bg_img):
    try:
        # Combine canvas and background (if exists)
        if bg_img is not None:
            saved_image = cv2.add(bg_img, canvas)
        else:
            saved_image = canvas.copy()

        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        cv2.imwrite(temp_file.name, saved_image)
        st.session_state.saved_image_path = temp_file.name

        # Display saved image
        saved_image_rgb = cv2.cvtColor(saved_image, cv2.COLOR_BGR2RGB)
        st.session_state.saved_image_placeholder.image(saved_image_rgb, caption="Saved Image")

        # Provide download button
        with open(st.session_state.saved_image_path, "rb") as file:
            st.session_state.download_button_placeholder.download_button(
                label="Download Saved Image",
                data=file,
                file_name="drawing.png",
                mime="image/png"
            )
        return True
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return False

def load_background_image(uploaded_file, screen_width, screen_height):
    if uploaded_file is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        bg_img = cv2.imread(temp_file.name)
        if bg_img is not None:
            # Get image dimensions
            img_height, img_width = bg_img.shape[:2]
            img_aspect = img_width / img_height
            canvas_aspect = screen_width / screen_height

            # Calculate new dimensions to preserve aspect ratio
            if img_aspect > canvas_aspect:
                new_width = screen_width
                new_height = int(screen_width / img_aspect)
            else:
                new_height = screen_height
                new_width = int(screen_height * img_aspect)

            # Resize image
            bg_img = cv2.resize(bg_img, (new_width, new_height))

            # Create a blank canvas
            canvas_bg = np.zeros((screen_height, screen_width, 3), np.uint8)

            # Calculate offsets to center the image
            x_offset = (screen_width - new_width) // 2
            y_offset = (screen_height - new_height) // 2

            # Place the resized image on the canvas
            canvas_bg[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = bg_img
            return canvas_bg
    return None