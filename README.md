# AI HairStyle Recommendation

An explainable Python prototype for exploring hairstyles using facial proportions,
hair texture, desired length, and maintenance preferences.

**Status:** runnable heuristic baseline. No social-media dataset, trained hairstyle
ranking model, measured accuracy, or photorealistic virtual try-on is included.
The optional computer-vision component uses a separately downloaded pretrained
MediaPipe face landmark model. Haircut scores come from transparent catalog rules.

## Features

- Manual face-shape selection works without a model or photo.
- Approximate shape estimation from measurements or a single-face photo.
- Up to 10 ranked ideas with explanations and strict preference filters.
- 20 hand-authored, gender-neutral style entries spanning four hair textures.
- Interactive, rotatable 3D silhouettes on a generic head.
- JSON export, input validation, automated tests, and GitHub Actions CI.

## Quick start

Use Python 3.11 or 3.12.

```bash
git clone https://github.com/halim-abdul/AI-HairStyle-Recommendation.git
cd AI-HairStyle-Recommendation
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
streamlit run app.py
```

Open the local URL printed by Streamlit. Choose a shape, set hair texture and
maintenance in the sidebar, then expand recommendations or rotate a silhouette.
For example, oval + straight + any length + high maintenance returns 10 ideas.
More restrictive preferences can return fewer or zero results.

For photo analysis, follow [models/README.md](models/README.md). Use a clear,
front-facing JPEG or PNG with exactly one face. Manual mode remains available
if MediaPipe or its model is unavailable.

## How it works

1. Obtain a user-selected shape or estimate one using pixel-distance ratios.
2. Filter the catalog by texture, length, and maximum daily maintenance.
3. Award 60 baseline points, 30 for a catalog shape pairing, and 5 for low maintenance.
4. Sort by score, then stable style ID; return at most 10.
5. Render a procedural hair envelope controlled by volume, drop, and texture.

Scores are **not probabilities**. The shape thresholds, catalog pairings, and
weights are illustrative assumptions, not scientifically validated beauty rules.
The 3D view is a rough silhouette, not a faithful representation of every named
haircut. Styles sharing similar parameters can look similar.

## Project layout

| Path | Purpose |
| --- | --- |
| `app.py` | Streamlit interface |
| `hairstyle/geometry.py` | Measurements and geometric shape rules |
| `hairstyle/vision.py` | Safe image decoding and optional MediaPipe adapter |
| `hairstyle/recommender.py` | Filtering, scoring, and export |
| `hairstyle/preview.py` | Plotly procedural 3D preview |
| `hairstyle/data/styles.json` | Editable hairstyle catalog |
| `tests/` | Core, image, preview, and UI smoke tests |
| `docs/MODEL_CARD.md` | Assumptions, limitations, and evaluation plan |

## Tests

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

CI tests the baseline on Python 3.11 and 3.12. The optional detector requires its
external model and a consented photo, so real-image inference is a separate manual
integration check. Do not interpret baseline test success as validation of visual
recommendation quality.

## Privacy and data

The app does not save uploaded photos, train on them, or send them to third-party
AI services. Streamlit transfers uploads to the machine hosting the app; use a local
instance if you want processing on your own computer. Photos may remain in server
memory for the session. No face recognition, age prediction, or gender prediction
is performed. Only use photos with permission; for children obtain guardian
permission. No social-media scraping or dataset is provided.

## Development roadmap

- Collect licensed, explicitly consented examples and stylist preference labels.
- Evaluate by person-disjoint splits, texture groups, and camera conditions.
- Compare a learned ranker against this baseline using NDCG@10 and user feedback.
- Replace silhouettes with licensed hairstyle meshes and validated alignment.
- Add deployment-specific authentication, retention controls, and load testing.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidance.
Licensed under [Apache 2.0](LICENSE); external model terms apply separately.
