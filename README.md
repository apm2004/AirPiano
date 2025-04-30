# Air Piano

A virtual piano that can be played using hand gestures, powered by computer vision and hand tracking.

## Features

- Play piano keys using hand gestures in the air
- Visual feedback with on-screen piano interface
- Hand tracking with gesture recognition
- Real-time sound feedback
- Support for both black and white keys
- Two-hand support for complex pieces

## Requirements

- Python 3.8 (for mediapipe)
- Webcam
- Required Python packages (listed in requirements.txt):
  - opencv-python >= 4.5.0
  - cvzone >= 1.5.6
  - pygame >= 2.1.0
  - numpy >= 1.19.0

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Create a 'sounds' directory and add piano note sound files (WAV format)
   - Required sound files: C.wav, D.wav, E.wav, F.wav, G.wav, A.wav, B.wav, C#.wav, D#.wav, F#.wav, G#.wav, A#.wav

## Usage

1. Run the program:
```bash
python main.py
```
2. Place your hands in view of the camera
3. Use your index finger to "press" the piano keys
4. Press ESC to quit

## How It Works

- The application uses OpenCV and the CVZone HandTrackingModule for real-time hand tracking
- Piano keys are displayed on screen with proper visual feedback
- When an index finger intersects with a key's position, the corresponding note is played
- Pygame handles the audio playback of piano notes

## Project Structure

- `main.py`: Main application entry point and camera handling
- `piano_ui.py`: Piano interface and key management
- `hand_tracker.py`: Hand tracking and gesture recognition
- `requirements.txt`: List of required Python packages
- `sounds/`: Directory containing piano note sound files