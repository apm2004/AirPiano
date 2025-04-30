import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

class HandTracker:
    def __init__(self):
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)

    def detect_hands(self, frame):
        hands, frame = self.detector.findHands(frame, draw=True)
        landmarks = []

        if hands:
            for hand in hands:
                # Convert landmarks to numpy array
                landmarks.append(np.array(hand['lmList']))

        return landmarks