Gesture Controlled Drawing App
This is a Streamlit-based application that allows users to draw on a canvas using hand gestures captured via a webcam. The app uses MediaPipe for hand tracking and OpenCV for image processing.
Features

Draw with your index finger using different colors.
Clear the canvas by shaking an open hand.
Select colors or eraser by hovering over buttons.
Draw on a blank canvas or a custom background image.
Save and download your drawings as PNG files.

Installation

Clone the repository:git clone <repository-url>
cd gesture_drawing_app


Install dependencies:pip install -r requirements.txt


Run the app:streamlit run app.py



Requirements

Python 3.8+
Webcam for gesture detection

Usage

Select a mode ("Blank Canvas" or "Draw on Image") from the sidebar.
Upload an image if "Draw on Image" mode is selected.
Click "Start Drawing" to begin using hand gestures.
Use your index finger to draw, shake an open hand to clear, or hover over color buttons to change colors.
Click "Save Image" to save your drawing and download it.

Project Structure

app.py: Main entry point for the Streamlit app.
drawing_logic.py: Core logic for hand tracking and drawing.
ui_components.py: UI components and session state management.
utils.py: Utility functions for image handling.
requirements.txt: Project dependencies.
