"""
Gesture API Server
Runs the gesture detection loop in a background thread and exposes the latest result via REST.
"""

import threading
from fastapi import FastAPI
from pydantic import BaseModel

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from ai_engine.inference.gesture_detector import run_detector

app = FastAPI(title="OpenGestureXR API")

# Shared state
_latest: dict = {"gesture": "none", "confidence": 0.0}
_lock = threading.Lock()


def _update(result: dict):
    with _lock:
        _latest.update(result)


# Start detector in background thread on startup
@app.on_event("startup")
def start_detector():
    t = threading.Thread(target=run_detector, args=(_update,), daemon=True)
    t.start()


class GestureResponse(BaseModel):
    gesture: str
    confidence: float


@app.get("/gesture", response_model=GestureResponse)
def get_gesture():
    """Return the latest detected gesture."""
    with _lock:
        return GestureResponse(**_latest)
