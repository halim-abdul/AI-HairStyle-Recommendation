"""Launch with: streamlit run app.py"""
import os
import streamlit as st
from hairstyle.geometry import SHAPES, Measurements, estimate_shape
from hairstyle.recommender import (Preferences, TEXTURES, LENGTHS, MAINTENANCE,
                                   recommend, export_recommendations)
from hairstyle.preview import make_preview
from hairstyle.vision import decode_image, analyze_image

st.set_page_config(page_title="Style Studio | Hairstyle explorer", page_icon="✂️", layout="wide")
st.caption("STYLE STUDIO / EXPLAINABLE HAIRSTYLE EXPLORER")
st.title("Find a shape. Explore a style.")
st.write("Compare haircut ideas for your texture, preferred length, and daily routine.")
st.info("Research prototype: hand-authored recommendations and schematic 3D silhouettes. "
        "Scores are ranking points, not probabilities or judgments of attractiveness.")

with st.sidebar:
    st.header("Your preferences")
    texture = st.selectbox("Hair texture", TEXTURES)
    length = st.selectbox("Preferred length", LENGTHS)
    maintenance = st.selectbox("Maximum daily maintenance", MAINTENANCE, index=2)
    color = st.color_picker("Preview hair color", "#352820")
    st.caption("Styles are available to everyone. No age or gender is inferred.")

mode = st.radio("Choose a starting point", ["Select shape", "Enter measurements", "Analyze photo"],
                horizontal=True)
shape = None
if mode == "Select shape":
    shape = st.selectbox("Face shape (your choice)", SHAPES)
elif mode == "Enter measurements":
    st.caption("Use one consistent unit. Measure face length, cheekbone width, temple width, "
               "and jaw width. This is only an approximate shape guide.")
    columns = st.columns(4)
    values = [col.number_input(label, min_value=0.1, value=value, step=0.1)
              for col, label, value in zip(columns,
                  ["Face length", "Cheekbone width", "Temple width", "Jaw width"],
                  [18.0, 14.0, 13.0, 12.0])]
    estimate = estimate_shape(Measurements(*values))
    st.caption(f"Geometric estimate: {estimate}. You can override it below.")
    shape = st.selectbox("Shape to use", SHAPES, index=SHAPES.index(estimate))
else:
    st.write("Use a front-facing JPEG or PNG with one face, even lighting, and minimal tilt.")
    st.caption("Images are processed in server memory and are not saved by this app. "
               "If hosted remotely, the upload goes to that host. Clear the file to remove it "
               "from this session; this does not promise immediate memory erasure.")
    consent = st.checkbox("I have permission to use this photo (and guardian permission for a child).")
    upload = st.file_uploader("Photo (8 MiB, at most 12 megapixels)", type=["jpg", "jpeg", "png"])
    # Recompute for the active upload: no cached photo or stale previous analysis.
    if upload and consent:
        try:
            image = decode_image(upload.getvalue())
            st.image(image, caption="Current photo", width=280)
            with st.spinner("Estimating facial proportions…"):
                measures = analyze_image(image, os.environ.get(
                    "FACE_LANDMARKER_MODEL", "models/face_landmarker.task"))
            estimate = estimate_shape(measures)
            st.caption(f"Approximate estimate: {estimate}. Camera pose and perspective affect it.")
            shape = st.selectbox("Shape to use", SHAPES, index=SHAPES.index(estimate))
        except (ValueError, RuntimeError, OSError) as exc:
            st.warning(str(exc))
            st.caption("You can continue using Select shape or Enter measurements.")
    elif upload:
        st.caption("Confirm permission before analysis.")

if shape:
    prefs = Preferences(shape, texture, length, maintenance)
    results = recommend(prefs)
    st.subheader(f"{len(results)} ideas to explore")
    if not results:
        st.warning("No catalog entries match these filters. Try any length or higher maintenance.")
    else:
        st.caption("Up to 10 matches; filters are never silently relaxed.")
        left, right = st.columns([1, 1])
        with left:
            for rank, item in enumerate(results, 1):
                with st.expander(f"{rank:02d} · {item['name']} · {item['score']} points", expanded=rank == 1):
                    st.write(item["description"])
                    st.write(" · ".join(item["reasons"]))
                    st.caption("Ask your stylist: " + item["stylist_note"])
        with right:
            chosen = st.selectbox("Explore a silhouette", [item["name"] for item in results])
            selected = next(item for item in results if item["name"] == chosen)
            st.plotly_chart(make_preview(selected, color), use_container_width=True)
            st.caption("Drag to rotate; scroll to zoom. Generic head and procedural hair envelope, "
                       "not a photorealistic haircut or a reconstruction of your face.")
        st.download_button("Download recommendations", export_recommendations(prefs, results),
                           file_name="hairstyle-recommendations.json", mime="application/json")
st.divider()
st.caption("Personal preference comes first. The catalog offers ideas, not rules about who can wear a style.")
