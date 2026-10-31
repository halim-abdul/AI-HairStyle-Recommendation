# Optional face landmark model

Manual mode works without model downloads or MediaPipe.

1. Install the extra with `python -m pip install -e ".[vision]"`.
2. Open the [official MediaPipe Face Landmarker model page](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker#models).
3. Download the compatible Face Landmarker task bundle and save it as
   `models/face_landmarker.task`.
4. Alternatively set `FACE_LANDMARKER_MODEL` to its absolute path.
5. Run the app and select **Analyze photo**.

Review the upstream model terms before redistribution. No model weights are bundled.
The implementation uses the [MediaPipe Tasks Python API](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker/python).
Missing models, missing optional packages, no face, and multiple faces are reported in the app.
