import json
from types import SimpleNamespace
import pytest
from hairstyle.geometry import Measurements, estimate_shape, measure_landmarks, SHAPES
from hairstyle.recommender import Preferences, recommend, load_catalog, export_recommendations

@pytest.mark.parametrize("values, expected", [
    ((18, 14, 13, 12), "oval"), ((16, 14, 13, 12), "round"),
    ((16, 14, 13, 13), "square"), ((23, 14, 13, 12), "oblong"),
    ((18, 14, 14, 10), "heart"), ((18, 14, 12, 11), "diamond")])
def test_shapes_and_scale_invariance(values, expected):
    assert estimate_shape(Measurements(*values)) == expected
    assert estimate_shape(Measurements(*(x*10 for x in values))) == expected

@pytest.mark.parametrize("bad", [0, -1, float("nan"), float("inf")])
def test_invalid_measurements(bad):
    with pytest.raises(ValueError):
        Measurements(bad, 1, 1, 1)

def test_pixel_aspect_ratio():
    points = [SimpleNamespace(x=.5, y=.5) for _ in range(478)]
    for a, b in [(10,152),(234,454),(103,332),(172,397)]:
        points[a] = SimpleNamespace(x=.2, y=.2)
        points[b] = SimpleNamespace(x=.8, y=.8)
    m = measure_landmarks(points, 200, 100)
    assert m.cheek == pytest.approx((120**2+60**2)**.5)

def test_bad_landmarks():
    with pytest.raises(ValueError):
        measure_landmarks([], 100, 100)

def test_catalog():
    catalog = load_catalog()
    assert len(catalog) == 20
    assert len({s["id"] for s in catalog}) == len(catalog)
    for s in catalog:
        assert set(s["shapes"]) <= set(SHAPES)
        assert s["length"] in {"short", "medium", "long"}
        assert s["maintenance"] in {"low", "medium", "high"}
        assert set(s["textures"]) <= {"straight","wavy","curly","coily"}
        assert s["textures"] and s["shapes"]
        assert s["description"] and s["stylist_note"]
        assert 0 <= s["preview"]["volume"] <= 1
        assert 0 <= s["preview"]["drop"] <= 2

def test_default_top_ten_deterministic():
    p = Preferences(texture="straight")
    first = recommend(p)
    assert len(first) == 10
    assert first == recommend(p)
    assert first == sorted(first, key=lambda s: (-s["score"], s["id"]))

def test_filters_are_hard_constraints():
    p = Preferences(texture="curly", length="short", maintenance="low")
    results = recommend(p)
    assert results
    assert all(s["length"] == "short" and s["maintenance"] == "low"
               and "curly" in s["textures"] for s in results)

def test_no_match_is_not_silently_relaxed():
    assert recommend(Preferences(texture="coily", length="long", maintenance="low")) == []

def test_shape_bonus():
    oval = {s["id"]:s["score"] for s in recommend(Preferences(), 20)}
    oblong = {s["id"]:s["score"] for s in recommend(Preferences(shape="oblong"), 20)}
    assert oval["crew-cut"] - oblong["crew-cut"] == 30

@pytest.mark.parametrize("kwargs", [{"shape":"unknown"},{"texture":"unknown"},
                                    {"length":"unknown"},{"maintenance":"unknown"}])
def test_invalid_preferences(kwargs):
    with pytest.raises(ValueError):
        Preferences(**kwargs)

@pytest.mark.parametrize("k", [0, -1, 21, 2.5, True])
def test_invalid_top_k(k):
    with pytest.raises(ValueError):
        recommend(Preferences(), k)

def test_export():
    p = Preferences()
    data = json.loads(export_recommendations(p, recommend(p)))
    assert data["preferences"]["shape"] == "oval"
    assert len(data["recommendations"]) <= 10
    assert "heuristic" in data["method"]
