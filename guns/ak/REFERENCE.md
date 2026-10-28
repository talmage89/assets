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

Camera matching uses sparse landmarks, never photo contours as mesh input.
Native RMS is 7.88 px right, 13.89 px left, 0.84 px receiver, 0.44 px museum
trigger and 11.66 px sharp trigger. The museum trigger's anchors extend beyond
its crop; its low residual is not a blade-form measurement. The sharp trigger
fit reaches its 100 mm lens bound, so that pair supports direction and broad
curvature judgment, not an exact overlay acceptance. No residual certifies
unmeasured geometry between the anchors.

The anonymous cheek-weld crop gives an estimated eye-to-notch distance of
268 ±35 mm using an assumed 255 mm receiver exterior baseline. The pupil is
shadowed and the photograph is perspective, so this is a coarse visual
estimate. Our measured Eye-to-notch distance is 295.00 mm; the eye is 42.87 mm
above the actual comb surface. See `renders/checkpoint/cheek-weld.jpg`.

## Color and finish gate

`src/reference.py` records native neutral rectangles and linear gains.
The museum comparison uses its unshadowed gray upper-left backdrop; the early
view uses unprinted white cloth; the sharper trigger uses white display
paper; ammunition uses bright paper-grid cells excluding printed lines.
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
has our own contours and press layout. The sights use an original closed hood
variant rather than the museum example's protective ears.

Internal bolt, piston and hammer shapes are inert display proxies. There is
no chamber, rifling, pressure-bearing lock, working sear or manufactured feed
mechanism. No internal parts drawing or operational manual is implemented as
a mechanism. The requested functional contacts cannot be certified by this
visual checkpoint; the review records that limitation explicitly.
