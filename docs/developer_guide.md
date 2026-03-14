# Developer Guide

## Prerequisites

- Python 3.10+
- A webcam
- Unity 2022 LTS with XR Interaction Toolkit and OpenXR plugin

---

## Running the AI Gesture Server

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn gesture_api.server.main:app --reload
```

The server starts on `http://localhost:8000`.  
Test it: `curl http://localhost:8000/gesture`

The gesture detector starts automatically in a background thread and begins reading from your webcam.

---

## Connecting the Unity Client

1. Open your Unity 2022 LTS project.
2. Copy `unity_plugin/Scripts/` into `Assets/OpenGestureXR/Scripts/`.
3. Follow the scene setup steps in `demo/unity_scene_description.md`.
4. Ensure the `apiUrl` field on `GestureClient` matches your server address (default: `http://localhost:8000/gesture`).
5. Press **Play** — the client will begin polling the API and firing gesture events.

---

## Project Layout

```
ai_engine/inference/gesture_detector.py   # Webcam + MediaPipe + classifier
gesture_api/server/main.py                # FastAPI server
unity_plugin/Scripts/GestureClient.cs     # HTTP polling
unity_plugin/Scripts/ObjectInteractor.cs  # Gesture → object action mapping
```
