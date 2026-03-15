# OpenGestureXR

Open-source prototype SDK for AI-powered hand gesture interaction in XR (AR/VR) applications.

## Project Overview

OpenGestureXR connects a webcam-based hand gesture recognizer to a Unity XR scene. Gestures detected in real time are streamed via a FastAPI server and consumed by a Unity client to drive virtual object interactions.

## Architecture

```
Webcam
  ↓
MediaPipe Hand Tracking  (ai_engine/gesture_detector.py)
  ↓
Gesture Classifier       (ai_engine/gesture_classifier.py)
  ↓
FastAPI Gesture Server   (gesture_api/server/main.py)
  ↓  GET /gesture — HTTP JSON polling
Unity XR Client          (GestureClient.cs)
  ↓
XR Object Interaction    (ObjectInteractor.cs)
```

## Installation

```bash
git clone https://github.com/sarry94118-max/ARMAX.git
cd ARMAX
pip install -r ai_engine/requirements.txt
```

## Quick Start

```bash
# 1. Start the gesture API server
cd gesture_api
uvicorn server.main:app --reload

# 2. Verify
curl http://localhost:8000/gesture
# {"gesture":"open_hand","confidence":0.92}
```

Then open the Unity demo project and press **Play**.

## Unity Demo

See [`demo/unity_scene_description.md`](demo/unity_scene_description.md) for full scene setup.

| Gesture      | Action                  |
|--------------|-------------------------|
| `grab`       | Move cube with hand     |
| `open_hand`  | Release cube            |
| `pinch`      | Select sphere           |
| `point`      | Highlight sphere        |

## Future Work

- Deep learning ONNX gesture model
- Multi-hand tracking
- OpenXR native plugin (replace HTTP polling)
- Cloud inference support
- ARCore / ARKit integration
