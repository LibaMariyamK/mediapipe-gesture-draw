import streamlit as st
from ui_components import setup_ui, initialize_session_state
from drawing_logic import start_drawing_loop
from utils import save_image

def main():
    # Setup UI
    setup_ui()

    # Initialize session state
    initialize_session_state()

    # Handle save button
    if st.session_state.save_button and st.session_state.canvas is not None:
        if not save_image(st.session_state.canvas, st.session_state.bg_img):
            st.error("Failed to save image. Ensure you have drawn something or try again.")

    # Start drawing loop if enabled
    if st.session_state.start_drawing:
        start_drawing_loop()

if __name__ == "__main__":
    main()