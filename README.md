# hand_gesture
# 🎮 Hand Gesture Game Controller

A Python-based project that allows users to control PC games using **hand gestures** instead of a keyboard.  
The system uses **computer vision and real-time hand tracking** to convert finger gestures into game actions.

---

## 🚀 Features

- Real-time hand gesture recognition
- Smooth & accurate finger detection
- No keyboard or mouse required
- Works with offline / PC-installed games
- Flicker-free control using smoothing & debounce logic
- Easy to customize gesture mappings

---

## 🧠 Technologies Used

- **Python** – Core programming language  
- **OpenCV** – Webcam access & image processing  
- **MediaPipe** – Hand tracking & finger landmark detection  
- **PyAutoGUI** – Keyboard input simulation  

---

## 🖐️ Gesture Mapping

| Fingers | Action | Keyboard Key |
|-------|--------|--------------|
| 1 | Move Right | Right Arrow |
| 2 | Move Left | Left Arrow |
| 3 | Jump | Space |
| 4 | Crunch / Duck | Down Arrow |
| 5 | Action / Special | Ctrl |

---

## ⚙️ How It Works

1. Webcam captures live video frames  
2. OpenCV processes each frame  
3. MediaPipe detects hand landmarks  
4. Finger count is calculated  
5. Gesture smoothing improves accuracy  
6. PyAutoGUI triggers keyboard actions  
7. Game responds like real key presses  

---

## 🖥️ System Requirements

- Windows OS  
- Python 3.10 or higher  
- Webcam  

---

## 📦 Installation

```bash
pip install mediapipe opencv-python pyautogui
