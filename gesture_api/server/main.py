"""
FastAPI Gesture Service
Runs webcam + detection + classification in a background thread.
Exposes GET /gesture.
"""

import threading
import cv2
from fastapi import FastAPI
from pydantic import BaseModel

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ai_engine.gesture_detector import detect_hand
from ai_engine.gesture_classifier import classify_gesture

app = FastAPI(title="ARMAX Gesture API")

_state = {"gesture": "none", "confidence": 0.0}
_lock = threading.Lock()


def _detection_loop():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        result = detect_hand(frame)
        if result["hand_detected"]:
            classified = classify_gesture(result["landmarks"])
        else:
            classified = {"gesture": "none", "confidence": 0.0}
        with _lock:
            _state.update(classified)
    cap.release()


@app.on_event("startup")
def startup():
    threading.Thread(target=_detection_loop, daemon=True).start()


class GestureResponse(BaseModel):
    gesture: str
    confidence: float


@app.get("/gesture", response_model=GestureResponse)
def get_gesture():
    with _lock:
        return GestureResponse(**_state)
