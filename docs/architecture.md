# Architecture

## System Diagram

```
Webcam
  ↓
MediaPipe Hand Tracking
  ↓
Gesture Classifier
  ↓
FastAPI Gesture Server
  ↓  HTTP JSON  GET /gesture
Unity XR Client
  ↓
XR Object Interaction
```

## Modules

### `ai_engine/gesture_detector.py`
Opens the webcam, runs MediaPipe Hands, and returns 21 normalized landmark coordinates per frame. Target latency: < 30ms per frame.

### `ai_engine/gesture_classifier.py`
Applies geometric rules to the 21 landmarks to classify one of four gestures: `open_hand`, `grab`, `pinch`, `point`. Returns gesture name and confidence score.

### `gesture_api/server/main.py`
FastAPI server that runs the detector + classifier in a background thread and exposes the latest result at `GET /gesture`. Stateless — Unity polls at 500ms intervals.

### `unity_plugin/Scripts/GestureClient.cs`
Polls `GET /gesture` every 500ms, parses the JSON response, and fires the static `OnGestureReceived` event.

### `unity_plugin/Scripts/ObjectInteractor.cs`
Subscribes to `OnGestureReceived` and maps gestures to object actions: grab attaches the object to the hand anchor, open_hand releases it, pinch selects, point highlights.

---

## Future Extensions

- **Deep learning model** — swap rule-based classifier for a trained ONNX model
- **Multi-hand tracking** — extend MediaPipe config and API schema
- **OpenXR native plugin** — replace HTTP polling with a native XR extension
- **Cloud inference** — offload model to a cloud endpoint for mobile/AR devices
- **AR device support** — integrate ARCore / ARKit hand tracking APIs
