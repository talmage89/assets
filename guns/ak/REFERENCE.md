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

Camera matching uses sparse landmarks, never photo contours as mesh input.
Native RMS is 7.88 px right, 13.89 px left, 0.84 px receiver, 3.19 px local
museum trigger/guard, 18.91 px sharp trigger, 8.46 px rear side, 9.83 px rear
above/behind, 3.13 px front, 13.48 px cover side, 13.25 px cover above and
0.87 px selector. The trigger/guard now uses local guard anchors instead of
out-of-crop receiver anchors. The sharp trigger reaches its 1400 mm lens
bound; cover-side reaches its 180 mm bound. These are useful
comparisons, not exact overlay acceptance. No residual certifies unmeasured
geometry between the anchors. Rear side uses independent receiver anchors;
the earlier local saddle fit falsely elevated its camera. The selector crop
includes its entire blade and uses the receiver corners. The exhibition
reference is rotated in scratch
to keep camera roll within the solver's range.

Three sparse trigger observations per photograph give projected blade heights
22.35/21.60 mm, chord bows 4.98/4.65 mm and depths about 10 mm. Scale assumes a
255 mm receiver span in the museum view and 36 mm receiver-side height in the
sharp view. Estimated uncertainty is ±20%: blur, perspective and different
surface depths dominate. `src/reference_measurements.py` records the points;
they are not a traced contour or modeling input. The actual game blade is
21.99 mm tall, 9.31 mm deep and 5.20 mm across, with a 4.79 mm section-center
bow. A side photo cannot independently resolve guard width and gauge; the
oblique references support the broad flat band. Its actual cut is
13.00 ×1.62 mm. See `renders/checkpoint/trigger-measurements.jpg`.

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
