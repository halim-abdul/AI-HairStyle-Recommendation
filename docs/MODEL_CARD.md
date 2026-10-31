# Prototype / model card

## Components and evidence
The shape estimator and recommendation ranker are hand-authored rules. No training
data, learned weights, experiments, or accuracy claims exist for these components.
MediaPipe is optional and supplies face landmarks only; see its upstream model
documentation for training provenance and limitations.

## Inputs and outputs
Inputs: selected shape or four positive measurements, optional consented photo,
texture, desired length, and maximum maintenance.
Outputs: up to ten catalog entries with ranking points and explanations.
No identity, age, gender, ethnicity, health, or attractiveness is inferred.

## Geometry
Distances use 2D image coordinates scaled independently by width and height.
Landmarks: 10–152 (length), 234–454 (cheeks), 103–332 (temple proxy),
172–397 (jaw). These are approximate anatomical proxies.
Rules are applied in order: length/cheeks >= 1.55 -> oblong; forehead/jaw >=
1.25 -> heart; cheeks/max(forehead,jaw) >= 1.12 -> diamond; length/cheeks <=
1.25 -> square if jaw/cheeks >= .9, otherwise round; remaining cases -> oval.
They cannot reliably distinguish all shapes; manual override is always available.

## Limitations
Pose, focal length, expression, occlusion, hair, lighting, landmark error, and
measurement choices affect results. No quality/confidence calibration is included.
Shape categories oversimplify continuous facial geometry. Catalog labels reflect
illustrative styling assumptions and may not reflect culture or personal taste.
Daily maintenance excludes initial salon time and long-term cost.
No suitability claims for children are made. The UI does not infer age.
3D envelopes are generic illustrations, not personalized reconstructions.

## Future evaluation protocol
Collect only licensed and consented data with documented provenance and deletion
procedures. Keep all photos of one person within one split; reserve a final test
set. Compare against random, popularity, and this rule baseline. Report NDCG@10,
Recall@10, coverage, and preference feedback, including uncertainty intervals.
Audit texture coverage, lighting and pose failures, and recommendation diversity.
Publish actual sample sizes, exclusions, limitations, and metrics before claiming
a trained or validated system. Do not invent results.

## Manual optional-vision acceptance
Test missing model, absent MediaPipe, blank image, one face, and two faces.
Check front-facing vs rotated photos and portrait vs landscape images.
Confirm the override changes the recommendation shape. Confirm replacing or clearing
an upload cannot reuse recommendations from the previous image.
