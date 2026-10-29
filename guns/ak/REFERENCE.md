# Rill 39 — exterior reference plan

The reference class is a fixed-stock stamped-receiver 7.62×39 rifle. This is
an original visual game asset, not a product replica or a manufacturing model.
The fictional maker is Propane Defense and the model is Rill 39. All vertices
come from the scripts; photographs only inform visual judgments and camera
placement. Sources, direct downloads, authors and licenses are recorded in
[refs/SOURCES.md](refs/SOURCES.md).

## Scale and uncertainty

Published class specifications give approximately 880 mm overall length,
415 mm barrel and a 30-round magazine. The museum catalog independently gives
415 mm for the barrel. The identification-sheet mirror gives 3.06 kg unloaded
but uses different length conventions (896/436 mm); those values are recorded
as a discrepancy. The asset uses the 880/415 convention, with a measured
881.38 mm exterior envelope including end fasteners and brake. About 3.1 kg
is an intended reference mass; the mesh has no density-derived mass proof.

The museum's paired exterior views are the primary form reference: receiver
and cover, furniture proportions, stamped magazine, controls and trigger.
The earlier photograph cross-checks variation. The muzzle photograph shows
the slanted sleeve silhouette and surrounding exterior parts. The sharper
wet display photograph gives a larger trigger blade, while its modern stock
is excluded from furniture comparisons. The ammunition photograph informs
the inert exterior silhouette and the choice of lacquered steel appearance.
The sharp rear-sight macro supplies the leaf, slider/buttons and graduated
top. It depicts an earlier receiver variant, so its receiver is excluded.
The oblique exhibition photograph supplies cover pressing and open front
ears; reflections, display wires and unrelated furniture are excluded.

Round 3 replaces the small muzzle crop with sharp component photographs:
AKOptions' side/rear tower views, Walter Gurske's installed sight macros,
Arms of America's side saddle, gas forging, molded grip and sharp cover. Their primary
parts span at least 600 native pixels, generally 1,300–2,500. The two large
Commons museum photos cross-check installed construction; glass and small
local crops keep them auxiliary. The old Commons rear macro independently
checks leaf/crosspiece relationships. See the native dimensions and credits
in SOURCES.md. The sharp cover is a modern replacement; it checks pressing and rear/flank
construction while the accepted cover span stays fixed. Its camera residual
is retained rather than treated as exact contour acceptance. No image is
upscaled and then described as sharp evidence.

Camera matching uses sparse landmarks, never contours as a mesh input.
`src/calibrate.py` retains the kit's projection/verification and fixes yaw and
elevation for true side/rear component views. Only translation and roll fit
at a fixed 300 mm lens. The old 3.1 px front fit was not a valid view match:
a side plate was compared with two separated ears from behind. Round 3's
constrained side and rear fits have honest residuals of 91.25 and 99.22
native pixels. Fifteen local orthographic views independently expose width,
height and section relationships. Residual is framing evidence, never form
approval.

Other native RMS values are 7.88 px right, 13.89 left, 0.84 receiver, 3.19
museum trigger/guard, 18.91 sharp trigger, 87.57 isolated rear side, 9.80
Commons rear macro, 32.64 new rear macro, 13.92 installed front, 46.20 gas
side, 75.20 grip side, 13.48 cover side, 13.25 old cover above, 88.64 new sharp cover above and 0.87 selector.
Rear-side reference has its leaf raised; the asset's static leaf is lower.
That setting difference is retained visibly rather than fitted away by an
elevated camera. Trigger reaches its 1400 mm lens bound; cover side reaches
180 mm. Selector is posed at frame 9 of Selector for the lower photographed
lever position; its safe/auto/semi settings and coverage are unchanged.

Round 3 sparse observations are reproducible in `src/form_observations.py`:

| Region / source | Native observation | Conditional exterior estimate |
| --- | --- | --- |
| Saddle rear shoulder / museum.jpg | 39.5 px above inferred barrel top | 18.0 ±4 mm |
| Hinge cheek / museum.jpg | 57.5 px above inferred barrel top | 26.2 ±6 mm |
| Leaf / rear-sight.jpg | 205.2 px against 525.6 px saddle baseline | 12.9 ±2.1 mm |
| Crosspiece / rear-sight.jpg | 435.6 px against same baseline | 27.3 ±4.4 mm |
| Hood edge / front-behind.jpg | 26 px against 451 px collar width | 1.3 ±0.5 mm |
| Hood depth / front-side.jpg | 374 px against 267 px drum end | 12.6 ±2.0 mm |

Scale is explicit, not an independent part specification: museum uses the
accepted 255 mm receiver span /559 px; rear macro assumes a 33 mm saddle
within the accepted 35 mm receiver; front views assume 23 mm exterior collar
and 9 mm drum. The installed barrel top is occluded: its line is inferred
from the accepted barrel/receiver datum. Surface depth, obliquity, paint and
edge blur limit these estimates. The standalone sharp side photo confirms
the low stepped shoulder and hinge hump but cannot independently measure a
height above an absent barrel. These qualifications prevent a model constant
from being presented as a photo measurement.

Actual triangle measurements are separate: saddle above barrel 14.99/16.60 mm
at Y195/Y220 and 29.32 mm at the front hinge Y246; leaf 13.40 mm; crosspiece
25.99 mm; hood depth 14.00 mm; sheet gauge 1.01 mm from two surface-ray hits.
The gas center section shows one continuous collar/curved neck. The cover
sections show vertical flanks and roof-only beads. Grip cuts show flat side
lands and rounded straps; its fine diamond panels are authored high geometry
projected into the normal. `form-observations.jpg` and `sections.jpg` show the
two distinct kinds of evidence.

Three sparse trigger observations per photograph give projected blade heights
22.35/21.60 mm, chord bows 4.98/4.65 mm and depths about 10 mm. Scale assumes a
255 mm receiver span in the museum view and 36 mm receiver-side height in the
sharp view. Estimated uncertainty is ±20%: blur, perspective and different
surface depths dominate. `src/reference_measurements.py` records the points;
they are not a traced contour or modeling input. The actual game blade is
21.99 mm tall, 8.43 mm deep and 5.16 mm across, with a 4.92 mm section-center
bow. A side photo cannot independently resolve guard width and gauge; the
oblique references support the broad flat band. Its actual cut is
13.00 ×1.65 mm. See `renders/checkpoint/trigger-measurements.jpg`.

The anonymous cheek-weld crop gives an estimated eye-to-notch distance of
268 ±35 mm using an assumed 255 mm receiver exterior baseline. The pupil is
shadowed and the photograph is perspective, so this is a coarse visual
estimate. Our measured Eye-to-notch distance is 295.00 mm; the eye is 42.87 mm
above the actual comb surface. See `renders/checkpoint/cheek-weld.jpg`.

## Color and finish gate

`src/reference.py` records native neutral rectangles and linear gains.
The museum comparison uses its unshadowed gray upper-left backdrop; the early
view uses unprinted white cloth; the sharper trigger uses white display
paper; ammunition uses bright paper-grid cells excluding printed lines. The
rear-sight macro uses concrete behind the rifle and the exhibition view uses
its gray display backing, both estimated neutrals.
Round 3's installed macros use estimated gray weathered wood; the grip uses
light gray concrete; gas side and the sharp cover use a white backdrop. Tan cardboard in the
isolated front views and the colored rear-side work surface have no reliable
neutral, retain identity gains and are form-only.
These are estimates, not controlled color cards. The muzzle photograph's sky
and the cheek-weld photograph's garment are not reliable neutrals: they retain
identity correction and are forbidden for color measurements.

Inspection materials are constants and are visibly too pale/regular in some
views. No wood, paint or wear color has been accepted. The finish stage must
white-balance its used-object reference before measuring albedo and judge the
exported baked asset in two dimensions. No reference pixels enter a texture.

## Construction scope

Actual surface cuts demonstrate a folded open U receiver, finite handguard
walls, compound furniture sections and hollow ribbed magazine. The exterior
has our own contours and press layout. The front sight now has open protective
ears, a tapered rounded forging, collar and drum sections. The rear sight has
a smooth forged saddle, long front-hinged leaf, slider/buttons and underlying
spring. The retained dense originals and geometric normal are our own scripts.

The carrier/piston are inert display shapes. Bolt-lug and hammer/sear surfaces
have zero render geometry in source and fresh GLB; their transform bones and
clip timing remain. This proves those hidden surfaces cannot appear in any
clip or camera by absence. Actual evaluated surfaces prove visible front-lug,
rear-catch, detent, feed-lip and carrier seating; a two-dimensional ray grid
tests safe-slot coverage. These are exterior visual assembly checks. There is
no chamber, rifling, pressure-bearing lock or working sear. No internal parts
drawing or operational manual is implemented as a mechanism.
