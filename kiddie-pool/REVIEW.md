# Minnow Petal 60 review

## Source pass

Opened the manufacturer's smaller-pool construction image, the retailer's real
60-inch shell photo and all first source renders. The first source was too
perfectly circular and its height-only dirt mask covered the whole floor in
cloudy noise, concealing the original molded relief. Restricted ground grime
to outward normals and real floor-wall cavities. Strengthened the raised
1.25 mm petal/ring/pinwheel relief and added crest polish from contact. This is
not a painted or photo-derived pattern. The fresh floor remains clear of
uniform weather noise. The source is the same 1,936-triangle physical shell as
the game model; submillimeter surface structure is procedural shading.

Added 5.5 mm maximum downward rim warp and small inward waviness to the
unsupported upper wall, preserving the nominal cardinal diameter and flat
floor. The twelve broad wall flutes are original geometry. The curled rim has
an actual free return. Five thin grass strips use downward ray hits to follow
the real lip across their widths; source/game contact checks measure actual
intersections. Wet arcs follow the grass/splash locations. Water is horizontal
at 140 mm with measured 1.05–5.48 mm side clearance and 137.6 mm floor gap.
Measured wall gauge is 1.80 mm over 24 crest/valley rays. Ground origin error is
zero. The source and game are triangulated identically before baking.

The first circle camera fit used lateral silhouette extrema as cardinal points,
which is wrong under perspective, and poorly placed foot landmarks (42.7 px
RMS). Corrected the lateral azimuth and used actual ground-edge positions.
Retailer framing now fits at 8.21 px RMS, estimated 123.2 mm lens. Its exact
camera is unknown; this is a framing comparison, not a traced product replica.
The original unprinted relief differs intentionally from the photo's graphics.

## Used-object calibration

Main's new wear contract was merged before final docs. Catalog framing remains
only a dimensional/construction aid. Added an estate-auction photograph of
actual used round pools, plus an auxiliary used-oblong-pool
reference for cause placement. The round estate pool's dimensions and age are
unknown; four rim landmarks fit at 2.39 px RMS, estimated 68.8 mm lens. It is a
used-object weather comparison, not an age measurement or exact product match.
No catalog photo is used to claim used-object wear calibration.

The newer source has visibly sun-softened upper plastic against protected blue,
waterline deposits, wet grass and worn upper edges. Broke the previous perfectly
uniform pale waterline into irregular mineral residue at the physical prior
fill level. The original floor relief reads in the full source frame; the
baked comparison must still retain it. No reference image is ever in a shader.

## Exported pass

Opened both exported construction and estate-used pairs. The baked floor
relief is softer than the source, especially in the bright comparison camera,
but the medallion and rings remain legible. The mineral line is broken, its
height follows prior fill, and the upper plastic is visibly faded against the
protected lower wall. Grass survives as narrow green clippings; individual
blade grain is below atlas resolution. No black projection patches are visible.
Both delivered materials share the same three embedded 1024 images; the water
material retains transmission and IOR 1.333. The estate pool is a different
original molding and still more saturated than our deliberately sun-faded blue.
Its unknown age is not presented as a measured weathering duration.

Opened all ten final Cycles views and the full contact sheet. Fading and the
broken waterline remain visible at full hero framing. Fine grass grain is lost
and the floor relief has slight atlas stair-stepping up close. The first
Eevee water preview rendered black despite ray tracing; the required Eevee
preview now shows the dry pool and the engine-specific water limitation is
explicit in the README. No false successful-water claim is made.

`make` and `make check` pass; delivery is 1,936 triangles, two materials sharing
three 1024 images, 974,256-byte GLB. All physical checks, UV overlap/density,
normals and fresh import pass. Final dry Eevee/contact images were opened after the
preview correction; no black water is included in the published contact sheet.
