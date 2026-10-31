"""Optional MediaPipe Tasks integration; no image files are persisted."""
from io import BytesIO
from pathlib import Path
import warnings
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 12_000_000

def decode_image(data: bytes) -> Image.Image:
    if not data or len(data) > MAX_BYTES:
        raise ValueError("Choose a non-empty JPEG or PNG smaller than 8 MiB.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data)) as image:
                if image.format not in {"JPEG", "PNG"}:
                    raise ValueError("Only JPEG and PNG images are supported.")
                if image.width * image.height > MAX_PIXELS:
                    raise ValueError("Image is too large; resize to at most 12 megapixels.")
                image.load()
                result = ImageOps.exif_transpose(image).convert("RGB")
                result.thumbnail((1600, 1600))
                return result
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError,
            Image.DecompressionBombWarning) as exc:
        raise ValueError("The image is invalid, damaged, or too large.") from exc

def analyze_image(image: Image.Image, model_path: str):
    from .geometry import measure_landmarks
    if not Path(model_path).is_file():
        raise ValueError("Face model missing. Follow models/README.md, or use manual mode.")
    try:
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision
        import numpy as np
    except ImportError as exc:
        raise ValueError("Install the vision extra: pip install -e '.[vision]'") from exc
    options = vision.FaceLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=model_path),
        running_mode=vision.RunningMode.IMAGE,
        num_faces=2,
    )
    with vision.FaceLandmarker.create_from_options(options) as detector:
        result = detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB,
                                          data=np.asarray(image)))
    if len(result.face_landmarks) != 1:
        raise ValueError("Use a clear front-facing photo containing exactly one face.")
    return measure_landmarks(result.face_landmarks[0], image.width, image.height)
