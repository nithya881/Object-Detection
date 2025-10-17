# HSV-Based Object Tracking from Video Stream Using OpenCV

This project uses OpenCV and the HSV color space to detect and track objects of a specific color in real time via a webcam feed.

The user can click on any part of the video frame to pick a color. The program captures the average HSV value in a 10×10 region around the click, then uses that color range to detect and track matching objects live.

---

## 📁 Project Structure

```

ObjectDetect/
├── objectdetect.py       # Main script for detection
├── requirements.txt      # List of Python packages
├── venv/                 # Virtual environment (not shared)
└── **pycache**/          # Python cache (can be ignored)

````

---

## 💻 Requirements

- Python 3.10+
- OpenCV (`opencv-python`)
- NumPy

---

## ⚙️ Setup Instructions

1. Open terminal and go to project folder:

```bash
cd /home/nithya/PycharmProjects/ObjectDetect
````

2. Create & activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
python3 objectdetect.py
```

---

## 🧠 How It Works

* Converts frame from BGR to HSV color space.
* Captures average HSV in a 10×10 region on mouse click.
* Calculates HSV range with delta tolerance.
* Applies mask and detects contours.
* Draws bounding boxes around matched areas.

---

## 🖱️ Interactive Features

* Click on the video to select the target color.
* Live tracking based on HSV range.
* Supports hue wrapping logic (e.g., for red colors).

---

## 📸 Results

Below are some sample output frames showing object detection and tracking:

	Object detected and highlighted with bounding box
  <img width="1282" height="577" alt="Image" src="https://github.com/user-attachments/assets/8f938c13-7568-41ee-af32-9f10454233d4" />
 

	Tracking the same color in motion

	

	HSV mask used for color filtering

---


## 📌 Notes

* Make sure your webcam is working.
* Tested on Ubuntu 22.04 with Python 3.10.
* Don’t share the `venv/` folder — it's machine-specific.

---


## 📦 To Share

Include only:

* `objectdetect.py`
* `requirements.txt`
* `README.md`

You can zip the folder like this:

```bash
zip -r ObjectDetect.zip ObjectDetect -x "ObjectDetect/venv/*"
