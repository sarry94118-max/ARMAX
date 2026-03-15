"""
Gesture detector — captures a webcam frame and returns hand landmarks via MediaPipe.
"""

import cv2
import mediapipe as mp
import numpy as np

_hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)


def detect_hand(frame: np.ndarray) -> dict:
    """
    Detect hand landmarks in a BGR frame.

    Returns:
        {"hand_detected": True,  "landmarks": [[x,y,z], ...]}  # 21 points
        {"hand_detected": False}
    """
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = _hands.process(rgb)

    if not results.multi_hand_landmarks:
        return {"hand_detected": False}

    lm = results.multi_hand_landmarks[0].landmark
    return {
        "hand_detected": True,
        "landmarks": [[p.x, p.y, p.z] for p in lm],
    }
