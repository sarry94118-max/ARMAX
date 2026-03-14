# Architecture

## System Components

### AI Engine (`ai_engine/`)
Python module that opens the webcam, runs MediaPipe hand landmark detection, and classifies gestures using a rule-based classifier. Outputs a gesture name and confidence score.

### Gesture API (`gesture_api/`)
FastAPI server that runs the AI engine in a background thread and exposes the latest gesture result over HTTP. Unity polls this endpoint.

### Unity XR Client (`unity_plugin/`)
C# scripts that poll the Gesture API and map gesture events to XR object interactions using Unity's transform system and OpenXR.

---

## ASCII Architecture Diagram

```
Webcam
   │
   ▼
Gesture Detector (Python / MediaPipe)
   │  ai_engine/inference/gesture_detector.py
   ▼
FastAPI Gesture Server
   │  gesture_api/server/main.py
   │  GET /gesture → {"gesture": "grab", "confidence": 0.91}
   │
HTTP JSON (polling ~20 Hz)
   │
   ▼
Unity XR Client
   │  GestureClient.cs  →  OnGestureReceived event
   ▼
ObjectInteractor.cs
   │
   ▼
Virtual Object Interaction (grab / release / select / highlight)
```

---

## Future Extensions

- **Deep learning model** — replace rule-based classifier with a trained ONNX model
- **Multi-hand tracking** — extend MediaPipe config and API schema
- **OpenXR native plugin** — replace HTTP polling with a native XR extension
- **Cloud inference** — offload model inference to a cloud endpoint for mobile/AR devices
- **AR device support** — integrate with ARCore / ARKit hand tracking APIs
