# 🖐️ Computer Vision with Python

## Author : Priyanshu Kumar [YiralcrafT]

A collection of real-time **Computer Vision** projects built using **Python**, **OpenCV**, and **MediaPipe**. This repository demonstrates how hand tracking can be used to create natural Human-Computer Interaction (HCI) applications such as controlling the system volume and moving the mouse with simple hand gestures.

---

## 📌 Features

- ✋ Real-time hand detection and tracking
- 🎯 21 hand landmark detection using MediaPipe
- 🖱️ Virtual Mouse Control
- 🔊 Hand Gesture Volume Control
- 📈 Live FPS display
- ♻️ Reusable Hand Tracking Module

---

## 📂 Project Structure

```text
ComputerVision/
│
├── HandTrakingModule.py      # Custom reusable hand tracking module
├── VirtualMouseControl.py    # Control mouse using hand gestures
├── VolumeHandControl.py      # Control Windows volume using finger distance
├── ex.py                     # Testing / experimental file
│
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
├── LICENSE                   # License
├── .gitignore                # Ignored files
```

---

# 🚀 Projects

## 🔊 Hand Gesture Volume Controller

Control your Windows system volume using only your hand.

### Features

- Detects thumb and index finger
- Calculates the distance between fingertips
- Maps the distance to Windows master volume
- Displays volume percentage
- Smooth real-time interaction

### Technologies

- Python
- OpenCV
- MediaPipe
- NumPy
- PyCAW

---

## 🖱️ Virtual Mouse Controller

Control the mouse cursor using hand gestures captured through the webcam.

### Features

- Move mouse cursor
- Gesture-based clicking
- Smooth cursor movement
- Real-time hand tracking

### Technologies

- Python
- OpenCV
- MediaPipe
- PyAutoGUI

---

# 🛠️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/ComputerVision.git
```

Go into the project folder

```bash
cd ComputerVision
```

Install the required packages

```bash
pip install -r requirements.txt
```

---

# ▶️ Run

### Volume Controller

```bash
python VolumeHandControl.py
```

### Virtual Mouse

```bash
python VirtualMouseControl.py
```

---

# 📦 Dependencies

- OpenCV
- MediaPipe
- NumPy
- PyCAW
- PyAutoGUI
- Comtypes

Install everything with

```bash
pip install -r requirements.txt
```

---

# 📖 What I Learned

While building these projects I learned:

- Computer Vision fundamentals
- Image processing with OpenCV
- Hand tracking using MediaPipe
- Gesture recognition
- Human-Computer Interaction (HCI)
- Windows Audio API integration
- Real-time application development

---

# 🎯 Future Improvements

- Brightness control
- Gesture-based media player
- AI virtual painter
- Air keyboard
- Hand gesture presentation controller
- Multi-hand gesture recognition

---

## 🤝 Contributing

Contributions, ideas, and suggestions are always welcome.

Feel free to fork the repository and submit a pull request.

---

## ⭐ Support

If you found this project helpful, consider giving it a **Star ⭐** on GitHub.

---

## 📄 License

This project is licensed under the MIT License.
