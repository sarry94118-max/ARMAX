"""
Rule-based gesture classifier using 21 MediaPipe hand landmarks.
"""

import numpy as np


def classify_gesture(landmarks: list[list[float]]) -> dict:
    """
    Classify gesture from 21 landmark points [[x,y,z], ...].

    Returns:
        {"gesture": str, "confidence": float}
    """
    lm = landmarks  # shorthand

    def extended(tip: int, pip: int) -> bool:
        """Finger is extended when tip is above (lower y) its PIP joint."""
        return lm[tip][1] < lm[pip][1]

    # Pinch: thumb tip (4) close to index tip (8)
    dist = float(np.linalg.norm(np.array(lm[4][:2]) - np.array(lm[8][:2])))
    if dist < 0.05:
        return {"gesture": "pinch", "confidence": 0.90}

    fingers_extended = [
        extended(8, 6),   # index
        extended(12, 10), # middle
        extended(16, 14), # ring
        extended(20, 18), # pinky
    ]
    n = sum(fingers_extended)

    if n == 4:
        return {"gesture": "open_hand", "confidence": 0.92}
    if n == 0:
        return {"gesture": "grab", "confidence": 0.88}
    if fingers_extended[0] and not any(fingers_extended[1:]):
        return {"gesture": "point", "confidence": 0.85}

    return {"gesture": "open_hand", "confidence": 0.60}
