import streamlit as st

def setup_ui():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .stButton > button {
            border-radius: 8px;
            margin: 5px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton > button:hover {
            opacity: 0.8;
        }
        .stRadio > div {
            margin-bottom: 10px;
        }
        .stFileUploader > div {
            margin-bottom: 10px;
        }
        .instruction-text {
            font-size: 16px;
            color: #555;
            margin-bottom: 20px;
        }
        .sidebar .stRadio > div, .sidebar .stFileUploader > div {
            padding: 10px;
        }
        .sidebar .st-subheader {
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Streamlit UI
    st.title("Gesture Controlled Drawing")
    st.markdown(
        '<p class="instruction-text">Use your index finger to draw, shake an open hand to clear the canvas, and hover over color buttons to select a color or eraser.</p>',
        unsafe_allow_html=True
    )

    # Sidebar for Drawing Options
    with st.sidebar:
        st.subheader("Drawing Options")
        mode = st.radio("Choose mode:", ("Blank Canvas", "Draw on Image"), horizontal=False)
        uploaded_file = None
        if mode == "Draw on Image":
            uploaded_file = st.file_uploader("Upload background image", type=["png", "jpg", "jpeg"])
        st.session_state.mode = mode
        st.session_state.uploaded_file = uploaded_file

    # Container for action buttons
    with st.container():
        st.subheader("Controls")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.start_drawing_button = st.button("Start Drawing", key="start")
        with col2:
            st.session_state.stop_drawing_button = st.button("Stop Drawing", key="stop")
        with col3:
            st.session_state.save_button = st.button("Save Image", key="save")

    # Placeholder for saved image and download button
    st.session_state.saved_image_placeholder = st.empty()
    st.session_state.download_button_placeholder = st.empty()

def initialize_session_state():
    # Initialize session state
    if 'start_drawing' not in st.session_state:
        st.session_state.start_drawing = False
    if 'saved_image_path' not in st.session_state:
        st.session_state.saved_image_path = None
    if 'canvas' not in st.session_state:
        st.session_state.canvas = None
    if 'bg_img' not in st.session_state:
        st.session_state.bg_img = None
    if 'mode' not in st.session_state:
        st.session_state.mode = "Blank Canvas"
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'save_button' not in st.session_state:
        st.session_state.save_button = False
    if 'start_drawing_button' not in st.session_state:
        st.session_state.start_drawing_button = False
    if 'stop_drawing_button' not in st.session_state:
        st.session_state.stop_drawing_button = False

    # Update start_drawing state
    if st.session_state.start_drawing_button:
        st.session_state.start_drawing = True
    if st.session_state.stop_drawing_button:
        st.session_state.start_drawing = False