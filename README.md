# OpenGestureXR

Open-source prototype SDK for AI-based hand gesture recognition in XR (AR/VR) applications.

## Features

- Real-time hand gesture detection via MediaPipe (< 30ms per frame target)
- Rule-based gesture classifier: `open_hand`, `grab`, `pinch`, `point`
- FastAPI server exposing gesture state over HTTP
- Unity XR client that maps gestures to virtual object interactions (OpenXR)

## Installation

```bash
git clone https://github.com/example/OpenGestureXR
cd OpenGestureXR
pip install -r requirements.txt
```

## Quick Start

### 1. Start the gesture server

```bash
uvicorn gesture_api.server.main:app --reload
```

### 2. Verify the API

```bash
curl http://localhost:8000/gesture
# {"gesture":"open_hand","confidence":0.92}
```

### 3. Open Unity demo

Follow the setup steps in `demo/unity_scene_description.md` to configure the Unity scene, then press **Play**.

## Documentation

- [Architecture](docs/architecture.md)
- [Developer Guide](docs/developer_guide.md)
- [Demo Scene](demo/unity_scene_description.md)

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| AI Engine   | Python 3.10, MediaPipe, OpenCV      |
| API Server  | FastAPI, Uvicorn                    |
| XR Client   | Unity 2022 LTS, C#, OpenXR         |
