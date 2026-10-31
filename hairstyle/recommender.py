"""Deterministic content-based ranking with explicit preference constraints."""
from dataclasses import asdict, dataclass
from importlib.resources import files
import json
from .geometry import SHAPES

TEXTURES = ("straight", "wavy", "curly", "coily")
LENGTHS = ("any", "short", "medium", "long")
MAINTENANCE = ("low", "medium", "high")

@dataclass(frozen=True)
class Preferences:
    shape: str = "oval"
    texture: str = "wavy"
    length: str = "any"
    maintenance: str = "high"

    def __post_init__(self):
        for value, allowed, name in (
            (self.shape, SHAPES, "shape"), (self.texture, TEXTURES, "texture"),
            (self.length, LENGTHS, "length"), (self.maintenance, MAINTENANCE, "maintenance"),
        ):
            if value not in allowed:
                raise ValueError(f"Unsupported {name}: {value}")

def load_catalog() -> list[dict]:
    return json.loads(files("hairstyle").joinpath("data/styles.json").read_text(encoding="utf-8"))

def recommend(preferences: Preferences, top_k: int = 10) -> list[dict]:
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 20:
        raise ValueError("top_k must be an integer between 1 and 20.")
    results = []
    for style in load_catalog():
        if preferences.texture not in style["textures"]:
            continue
        if preferences.length != "any" and preferences.length != style["length"]:
            continue
        if MAINTENANCE.index(style["maintenance"]) > MAINTENANCE.index(preferences.maintenance):
            continue
        shape_match = preferences.shape in style["shapes"]
        score = 60 + 30 * shape_match + 5 * (style["maintenance"] == "low")
        reasons = [f"Supports {preferences.texture} texture",
                   f"{style['maintenance'].capitalize()} daily maintenance"]
        reasons.append(f"Catalog pairing for {preferences.shape} shape" if shape_match
                       else "Alternative outside this shape's catalog pairings")
        results.append({**style, "score": score, "reasons": reasons})
    return sorted(results, key=lambda item: (-item["score"], item["id"]))[:top_k]

def export_recommendations(preferences: Preferences, results: list[dict]) -> str:
    return json.dumps({"method": "hand-authored heuristic v0.1",
                       "preferences": asdict(preferences), "recommendations": results}, indent=2)
