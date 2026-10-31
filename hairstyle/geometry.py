"""Illustrative geometric rules; these are not a validated classifier."""
from dataclasses import dataclass
from math import hypot, isfinite

SHAPES = ("oval", "round", "square", "oblong", "heart", "diamond")

@dataclass(frozen=True)
class Measurements:
    length: float
    cheek: float
    forehead: float
    jaw: float

    def __post_init__(self):
        for value in (self.length, self.cheek, self.forehead, self.jaw):
            if not isfinite(value) or value <= 0:
                raise ValueError("All four measurements must be finite and positive.")

def estimate_shape(m: Measurements) -> str:
    """Use scale-invariant ratios. Thresholds are hand-authored, not learned."""
    elongation = m.length / m.cheek
    if elongation >= 1.55:
        return "oblong"
    if m.forehead / m.jaw >= 1.25:
        return "heart"
    if m.cheek / max(m.forehead, m.jaw) >= 1.12:
        return "diamond"
    if elongation <= 1.25:
        return "square" if m.jaw / m.cheek >= 0.9 else "round"
    return "oval"

def measure_landmarks(points, width: int, height: int) -> Measurements:
    """MediaPipe normalized landmarks -> 2D pixel distances.

    Forehead is a temple-width proxy, not the true hairline.
    Separate image width/height scaling avoids aspect-ratio distortion.
    """
    if len(points) < 455 or width <= 0 or height <= 0:
        raise ValueError("Need at least 455 landmarks and positive image dimensions.")
    def distance(a, b):
        return hypot((points[a].x - points[b].x) * width,
                     (points[a].y - points[b].y) * height)
    return Measurements(length=distance(10, 152), cheek=distance(234, 454),
                        forehead=distance(103, 332), jaw=distance(172, 397))
