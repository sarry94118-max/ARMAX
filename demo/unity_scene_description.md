# Unity Demo Scene — Description

## Scene Contents

| Object       | Type        | Position       |
|--------------|-------------|----------------|
| XR Camera    | XR Rig      | (0, 1.6, 0)    |
| Cube         | Mesh        | (0.3, 1.0, 1.5)|
| Sphere       | Mesh        | (-0.3, 1.0, 1.5)|

## Setup Steps

1. Create a new Unity 2022 LTS project with the **XR Interaction Toolkit** package installed.
2. Add the **OpenXR** plugin via *Edit → Project Settings → XR Plug-in Management*.
3. Import the `unity_plugin/Scripts/` folder into `Assets/OpenGestureXR/Scripts/`.
4. Add an empty GameObject named **GestureManager** to the scene and attach `GestureClient.cs`.
   - Set `handAnchor` to the XR camera's right-hand anchor transform.
5. Attach `ObjectInteractor.cs` to the **Cube**.
   - Set `handAnchor` to the same hand anchor.

## Interactions

| Gesture      | Result                        |
|--------------|-------------------------------|
| `grab`       | Cube attaches to hand anchor  |
| `open_hand`  | Cube detaches and stays in place |
| `pinch`      | Logs "Selected: Cube"         |
| `point`      | Logs "Highlighted: Cube"      |
