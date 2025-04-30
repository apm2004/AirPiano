import cv2
import numpy as np
import pygame
import os

class PianoKey:
    def __init__(self, x, y, width, height, is_black=False, note='C'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_black = is_black
        self.note = note
        self.is_pressed = False
        self.sound = None
        self.load_sound()

    def load_sound(self):
        try:
            self.sound = pygame.mixer.Sound(f'sounds/{self.note}.wav')
        except:
            print(f"Could not load sound for note {self.note}")

    def contains_point(self, x, y):
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def play(self):
        if self.sound and not self.is_pressed:
            self.sound.play()

class PianoUI:
    def __init__(self):
        self.keys = []
        self.setup_keys()

    def setup_keys(self):
        # White key dimensions
        white_key_width = 120
        white_key_height = 350
        num_white_keys = 7
        total_white_width = white_key_width * num_white_keys
        
        # Calculate start position - moved left by 200 pixels
        frame_width = 1920
        start_x = ((frame_width - total_white_width) // 2) - 200
        start_y = 50

        # Black key dimensions
        black_key_width = 70
        black_key_height = 200

        # Define white keys
        white_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        for i, note in enumerate(white_notes):
            x = start_x + (i * white_key_width)
            self.keys.append(PianoKey(x, start_y, white_key_width, 
                                    white_key_height, False, note))

        # Define black keys
        black_positions = [0, 1, 3, 4, 5]  # Positions after white keys
        black_notes = ['C#', 'D#', 'F#', 'G#', 'A#']
        for i, note in zip(black_positions, black_notes):
            x = start_x + (i * white_key_width) + (white_key_width * 0.7)
            self.keys.append(PianoKey(x, start_y, black_key_width,
                                    black_key_height, True, note))

    def update(self, hand_landmarks):
        pressed_keys = []
        
        # Reset all keys
        for key in self.keys:
            key.is_pressed = False

        # Check each finger tip position
        for hand in hand_landmarks:
            if len(hand) > 0:
                # Check index finger tip (landmark 8 in cvzone)
                finger_tip = hand[8]  # Index finger tip
                # cvzone gives coordinates in pixels directly
                x, y = finger_tip[0], finger_tip[1]
                
                for key in self.keys:
                    if key.contains_point(x, y):
                        key.is_pressed = True
                        key.play()
                        pressed_keys.append(key.note)

        return pressed_keys

    def draw(self, frame):
        # Draw white keys first
        for key in [k for k in self.keys if not k.is_black]:
            color = (200, 200, 200) if key.is_pressed else (255, 255, 255)
            x1, y1 = int(key.x), int(key.y)
            x2, y2 = int(key.x + key.width), int(key.y + key.height)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
            
            # Larger, better positioned note labels for white keys
            text_x = x1 + int(key.width/3)
            text_y = y2 - 30
            cv2.putText(frame, key.note, (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

        # Draw black keys on top
        for key in [k for k in self.keys if k.is_black]:
            color = (100, 100, 100) if key.is_pressed else (0, 0, 0)
            x1, y1 = int(key.x), int(key.y)
            x2, y2 = int(key.x + key.width), int(key.y + key.height)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
            # Larger, better positioned note labels for black keys
            text_x = x1 + int(key.width/4)
            text_y = y2 - 20
            cv2.putText(frame, key.note, (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return frame