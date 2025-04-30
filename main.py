import cv2
from cvzone.HandTrackingModule import HandDetector
import pygame
import numpy as np
from piano_ui import PianoUI
import os

class VirtualPiano:
    def __init__(self):
        # Initialize camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Try DirectShow backend
        if not self.cap.isOpened():
            print("Failed with DSHOW, trying default backend")
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise ValueError("Could not open camera. Please check if camera is connected.")

        # Set camera properties to higher resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        # Read a test frame to verify camera works
        ret, test_frame = self.cap.read()
        if not ret or test_frame is None:
            raise ValueError("Camera opened but cannot read frames")

        pygame.mixer.init()
        self.piano_ui = PianoUI()
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.running = True
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
        sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C#', 'D#', 'F#', 'G#', 'A#']
        
        if not os.path.exists(sound_dir):
            os.makedirs(sound_dir)
            print(f"Created sounds directory at {sound_dir}")
            print("Please add piano note sound files (WAV format) to this directory")
            return

        for note in notes:
            sound_file = os.path.join(sound_dir, f'{note}.wav')
            try:
                if os.path.exists(sound_file):
                    self.sounds[note] = pygame.mixer.Sound(sound_file)
                    print(f"Loaded sound for note {note}")
                else:
                    print(f"Missing sound file: {sound_file}")
            except Exception as e:
                print(f"Error loading sound for note {note}: {str(e)}")

    def play_note(self, note):
        if note in self.sounds:
            self.sounds[note].play()

    def run(self):
        cv2.namedWindow('Virtual Piano', cv2.WINDOW_NORMAL)
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print("Failed to grab frame")
                continue

            # Check frame is not empty
            if frame.size == 0:
                print("Empty frame received")
                continue

            frame = cv2.flip(frame, 1)
            
            try:
                hands, frame = self.detector.findHands(frame, draw=True)
                landmarks = []
                
                if hands:
                    for hand in hands:
                        landmarks.append(hand['lmList'])
                
                # Update piano UI and check for key presses
                pressed_keys = self.piano_ui.update(landmarks)
                
                # Play sounds for pressed keys
                for key in pressed_keys:
                    self.play_note(key)
                
                # Draw piano UI on frame
                frame = self.piano_ui.draw(frame)
                
                # Display frame
                cv2.imshow('Virtual Piano', frame)
            except Exception as e:
                print(f"Error processing frame: {str(e)}")
                continue

            key = cv2.waitKey(1)
            if key & 0xFF == 27:  # ESC to quit
                self.running = False
            
        self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    piano = VirtualPiano()
    piano.run()