"""
Gesture Detector Module
Detects hand landmarks via MediaPipe and classifies gestures using rule-based logic.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional

# Supported gestures
GESTURES = ["open_hand", "grab", "pinch", "point"]

mp_hands = mp.solutions.hands


def _finger_extended(landmarks, tip_id: int, pip_id: int) -> bool:
    """Return True if the finger tip is above its PIP joint (extended)."""
    return landmarks[tip_id].y < landmarks[pip_id].y


def classify_gesture(landmarks) -> tuple[str, float]:
    """
    Rule-based gesture classifier using 21 MediaPipe hand landmarks.
    Returns (gesture_name, confidence).
    """
    lm = landmarks.landmark

    # Finger tip / pip landmark indices
    fingers = {
        "index": (8, 6),
        "middle": (12, 10),
        "ring": (16, 14),
        "pinky": (20, 18),
    }
    extended = {name: _finger_extended(lm, tip, pip) for name, (tip, pip) in fingers.items()}

    # Thumb: compare tip x to IP joint x (mirrored for left/right)
    thumb_extended = lm[4].x < lm[3].x  # works for right hand facing camera

    # Pinch: thumb tip close to index tip
    thumb_tip = np.array([lm[4].x, lm[4].y])
    index_tip = np.array([lm[8].x, lm[8].y])
    pinch_dist = float(np.linalg.norm(thumb_tip - index_tip))

    if pinch_dist < 0.05:
        return "pinch", 0.90

    num_extended = sum(extended.values())

    if num_extended == 4 and thumb_extended:
        return "open_hand", 0.92
    if num_extended == 0:
        return "grab", 0.88
    if extended["index"] and not extended["middle"] and not extended["ring"] and not extended["pinky"]:
        return "point", 0.85

    return "open_hand", 0.60  # fallback


def run_detector(on_gesture=None):
    """
    Main detection loop. Opens webcam, detects landmarks, classifies gestures.
    Calls on_gesture(result) with {"gesture": str, "confidence": float} each frame.
    """
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            result: Optional[dict] = None
            if results.multi_hand_landmarks:
                gesture, confidence = classify_gesture(results.multi_hand_landmarks[0])
                result = {"gesture": gesture, "confidence": confidence}
            else:
                result = {"gesture": "none", "confidence": 0.0}

            if on_gesture:
                on_gesture(result)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_detector(on_gesture=print)
