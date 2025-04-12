# Rock Paper Scissors – Gesture Recognition Game (OpenCV + Python)

This project is a real-time Rock-Paper-Scissors game built using **OpenCV** in **Python**, where you play by showing hand gestures to your webcam. The game detects your hand shape, compares it with a randomly generated AI move, and tracks the score — all live!

## 🎮 Features

- Hand gesture recognition using **contour and convexity defects**
- Game logic for Rock, Paper, and Scissors
- Countdown animation before each round
- Real-time feedback like:
  - "Too far"
  - "Too close"
  - "Hand not centered"
  - "No hand detected"
- Score tracking and 5-round game limit (or first to 3 wins)
- Clean UI with OpenCV windows

## 🛠 Requirements

Install with Anaconda or pip:

```bash
pip install opencv-python numpy
