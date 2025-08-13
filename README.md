# Gesture Controlled Drawing App

A **Streamlit-based application** that allows users to draw on a canvas using **hand gestures** captured via a webcam or from uploaded media.  
The app uses **MediaPipe** for **hand tracking** and **OpenCV** for **image processing**, enabling intuitive, touch-free drawing.

---

## 📌 Introduction to Technologies

- **[Streamlit](https://streamlit.io/)**  
  A Python framework for building interactive web applications with minimal code.  
  Used here for creating the web-based UI.

- **[OpenCV](https://opencv.org/)** (Open Source Computer Vision Library)  
  A powerful library for computer vision and image processing.  
  Used for:
  - Capturing frames from webcam or uploaded video
  - Processing images (drawing lines, detecting positions)

- **[MediaPipe](https://developers.google.com/mediapipe)**  
  A Google framework for building machine learning pipelines for processing video, audio, and sensor data.  
  Used here for **real-time hand landmark detection**.

- **[NumPy](https://numpy.org/)**  
  A fundamental Python library for numerical computing.  
  Used for handling image arrays and calculations.

- **[Pillow (PIL)](https://python-pillow.org/)**  
  Python Imaging Library fork for opening, manipulating, and saving many image file formats.  
  Used for saving the final drawing as a PNG.

---
## 📂 Project Structure

```
gesture_drawing_app/
│── app.py                # Main entry point for the Streamlit app
│── drawing_logic.py       # Core logic for hand tracking and drawing
│── ui_components.py       # UI components and session state management
│── utils.py               # Utility functions for image handling
│── requirements.txt       # Project dependencies
│── README.md              # Project documentation
│── .gitignore             # Ignored files/folders
```

---
## ✨ Features

- ✍ **Draw with your index finger** using different colors.  
- 🖐 **Clear the canvas** by shaking an open hand.  
- 🎨 **Select colors or eraser** by hovering over buttons.  
- 🖼 **Draw on a blank canvas** or a custom background image.  
- 💾 **Save and download** your drawings as PNG files.  

---

## 🛠 Installation

```bash
# Clone the repository
git clone <repository-url>
cd gesture_drawing_app

# Install dependencies
pip install -r requirements.txt
````

---

## ▶ Usage (Local Webcam Version)

```bash
streamlit run app.py
```

### Steps:

1. Select a mode (**"Blank Canvas"** or **"Draw on Image"**) from the sidebar.
2. Upload an image if "Draw on Image" mode is selected.
3. Click **"Start Drawing"** to begin using hand gestures.
4. Use your **index finger to draw**, shake an open hand to clear, or hover over color buttons to change colors.
5. Click **"Save Image"** to save your drawing and download it.

---




