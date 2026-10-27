# Builder-colonial construction review

The construction and source-look checkpoints below are historical. Current
status: **baked family delivery with shared external images**. Four delivery
critiques follow the accepted construction/source records.

Historical status: **form checkpoint, placeholder materials, before look development**.
The first proof is seed 27. All current presentation views and calibrated pairs
come from a freshly reimported checkpoint GLB. This stage has no high/low bake
distinction and no material textures. Do not interpret its import audit as a
finished UV, texture, wear, or photorealism approval.

The references remain open during critique: the used `colonial-1991-oh` house,
the `colonial-rog-ri` room-over-garage house, their calibrated crops, the period steel
door sheet, and the published construction sources in `REFERENCE.md`.
The house designs differ; the comparisons are not claims that our generator
reproduces either photographed property.

## Pass 1 — first street and construction renders

Evidence: `renders/pass1/{hero,roof,window,eave}.png`; original photographs in
`refs/`. These were form previews against the photos before camera calibration.

**Color and value first.** Roof charcoal has enough value separation from the
trim; plain siding and veneer are visibly placeholder fields. Glass is a
uniform blue sheet, with too little room depth compared with both photographs.
That is an actual material-state problem, not a detail to hide with a bright
sky. Keep the roof dark, correct the glass before judging sash shadows.

The overall two-story scale and garage room are plausible, but two construction
failures dominate. Straight eave runs were split at a mathematical midpoint,
creating multiple outlets and pipes in front of windows. A main-hip plane
meeting the opposite garage slope creates a level valley. A level trough is
not a valid roof merely because the plane polygons intersect cleanly.

Reject the drainage layout. Merge straight perimeter intervals and give hip
variants a genuinely tapered cricket. Recessed window holes, projected sills,
real casings and sash offsets already read as assemblies rather than window
images on a flat wall. Keep those silhouettes; do not add siding courses or
shingle granules as thousands of polygons.

## Pass 2 — roof envelope, openings and daylight glass

Evidence: `renders/pass2/{hero,roof,window,eave,scale}.png`, with the same
photographs. The raw six-role source fell from roughly 60k triangles to the
50k range by reducing over-dense hidden curtain tessellation and duplicate
drainage runs, not by flattening visible trim.

**Color and value first.** Full transmission now shows a dim backing and some
curtains/blinds. The blue opaque-panel look is gone. Some undressed rooms are
still dark and the repeated glazing response is too uniform for a final asset.
White trim is below .70 linear reflectance; the roof remains dark. Placeholder
walls cannot yet be judged for 20-year service age.

The main/garage envelope is clipped rather than intersecting roof boxes. The
first cricket attempt still left level side segments: its independent X/Y
minimum made a flat central region. Replace it with four compound X/Y planes,
so side valleys fall all the way to their ends. The plan sweep now measures
positive fall at every retained valley segment, including the saddle.

Portico pipes must attach to columns. Routing a vertical line beside the
portico's nominal footprint leaves it floating. Move those pipe bodies to
real column faces and share corner outlets. The scale figure was hidden by a
column; move the figure/camera so the full 1.8 m aid can be assessed beside
the entry.

## Pass 3 — physical clearance and the corner detail

Evidence: `renders/pass3/{hero,roof,eave,scale}.png`, actual-source mesh audit
and `kit/motion.py` sweeps.

**Color and value first.** Cavities at window heads and under the portico are
dark without clipped trim highlights. Smooth roof and wall fields still read
as a clean model; this is an explicit form-stage limitation. Do not brighten
them to compensate for absent surface detail.

Move the eave camera below the corner so fascia, soffit and drip gauge can be
seen. Miter the soffit returns to the wall corner instead of leaving a thin
unsupported shelf. Shorten the garage upper windows to a normal 48-inch
module and align the main upper heads at 6 ft 8 in above that floor: the boxed
eave must clear the casings at 8:12 as well as 6:12.

The actual door sweep failed at 105 degrees with the hinge too near the
exterior plane. A door that can serialize cannot necessarily open. Recess the
44 mm leaf and place its barrel at the room-side jamb. A later closed-position
failure identified 4 mm of leaf/threshold penetration; set the threshold top
to the documented finished-floor elevation. The final 36-sample sweep has no
violations or contact exemptions.

The first six-mesh sweep also caught collinear clipping points generating
zero-area faces in a gable wall. Clean polygon boundaries before extruding
their thickness, rather than deleting arbitrary triangles after export.

## Pass 4 — calibrated photographic comparisons

Evidence: `renders/matches/colonial_rog_ri-pair.jpg` and
`renders/matches/colonial_1991_oh-pair.jpg`; residual overlays alongside them.

**Color and value first.** Compared with the actual photographs, our placeholder
fields are smoother and cooler in this daylight, with none of the roof's
granular range or siding's repeated small shadows. The palette is an authored
sand/forest/oxblood option; the photos show different colors. Preserve the
dark shingle albedo, but the future maps must create manufacturing and age
variation instead of using one flat gray sheet. Smooth brick-colored bands
are not yet convincing masonry.

The colonial-1991-oh facade fit supports the two-floor width/height and entrance scale
(3.34 px RMS on the picked anchors). Our hip roof, single windows, portico
and front veneer differ from its side gable, paired windows and bare stoop.
Those are explicit builder choices, not residuals to eliminate by distorting
the authored plan. The colonial-rog-ri garage fit is 4.12 px RMS; its crop-camera lens
hits the 100 mm upper bound. Treat that front-plane fit as a proportion aid,
not an independently recovered physical camera or measured building.

The original half-window-width shutters are correctly large enough to cover
the opening, as requested; paneled shutters differ from the photo's louvers.
Head flashing, jamb recess, separate meeting rails and a sill are legible.
The long plain garage wall is still visually sterile; adding texture and
correctly localized aging is necessary before any final acceptance.

The dimensioned side elevation catches an actual construction error that the
opening-only audit missed: the electric meter occupied the bottom of a window.
Move it into the pier between windows. Add service-to-opening rays so this
cannot recur in a different depth variant.

## Pass 5 — support and exported checkpoint gate

**Color and value first.** The final daylight setup retains the dark roof and
door, strong recess shadows and roll-off on the trim. The recorded tonal
statistic is an approximate image-region check, not a measured albedo or an
object-only mask. No region should be made pale to conceal the missing maps.

The pipe-body check originally proved only that the tubes were outside the
walls. It did not prove support: a roof-corner endpoint also needs to be
clamped along the gutter run back onto the wall's span. Correct both axes,
then measure distance to actual wall/column triangles. The largest measured
body-to-support distance is about 54 mm, with straps reaching the surface.
Set splash blocks on grade, rather than 20 mm above it. Inspect the final
corner and full hero after the shared GPU render refresh. The refreshed views
show the corrected supported pipe runs. Add the missing head-jamb lining
above each upper sash: an unlined black slot was too broad compared with the
photographs. That closure costs 12 triangles per window and keeps the proof
inside the 40–60k target.

The last join audit extends the garage sill to the actual apron-socket edge,
removing a 30 mm discrepancy. Fixture backplates meet the siding; vent-boot
flashing follows the roof plane instead of projecting horizontally above the
downhill edge. Actual mount gaps are below .24 μm, boot tops are about 6 mm
above the roof, and socket-to-sill distance is .71 mm at the 1 mm bevel. Thin
shutter backs now touch the wall and retain visible recessed infill; compound
pipe sections remain perpendicular to their centerline. These changes reduce
the final proof to 51,160 triangles rather than spending geometry on fine
surface effects.

The fixed house is consolidated separately from its front leaf. Raw GLB
accessors confirm triangle counts, unit normals and palette retention;
reimport checks world surface positions and hinge/socket transforms. Source
rays prove the roof has no sampled holes and that opening cores are actually
empty. These checks have different scopes and are reported separately.

Final refreshed hero, elevations, top/roof, eave/window/valley details, scale,
door pose, six seed portraits and both photographic pairs were opened. The
remaining CG tells are the deliberately smooth material fields and uniform
age, together with elbow/fixture finish that belongs to the trim look-dev.
The clean rebuild reproduces the same GLB bytes; all 19 raw views record the
hash of their current reimported source. The image-region luminance proxy has
zero clipped-white pixels at its stated threshold.

Final gate commands and numeric details are recorded in the README and ignored
JSON reports. The six-seed strip must show six independently exported houses,
not translations or recolors of a single mesh. An authored JSON-equivalent
override is also built and checked. A repeated seed reproduces the complete
placeholder GLB bytes.

## Still weak / next stage

- Roof courses, siding laps, mortar and the fine fixture/soffit structure are
  intentionally absent. No normal map or service-age wear is present. The
  render is not a product photograph and is not claimed to be one.
- Some window rooms remain too uniformly dim. Keep the current real recess,
  then tune neutral glass, blind/curtain variation and room backing against
  the used-house photos during look development.
- Ridge caps, valley metal, long gutters and elbow bends need their final map
  response and a closer end/miter review; the placeholder accents look too
  smooth. Corrugations/perforations belong in the trim normal.
- Buried mating faces and fine panel geometry can be culled after the trim
  bake. Opaque placeholder states are currently double-sided. Final material
  policy and culling need to be checked after shared UV/material assignment.
- The grammar currently proves one room-over-garage house type. Other garage
  story counts, arbitrary footprints, dormers and alternate architectural
  types have no validation and are rejected or outside the API.
- The house has no interior or rear entry/terrace. It is an exterior shell
  with a small amount of window depth. Hidden framing, permit compliance and
  load calculations are outside the delivered construction evidence.

Stop here for the requested form checkpoint. The shared texture plan is in
the README: five sets, six materials including glass, about 38 MiB compressed
with mipmaps. Final tiled UV density/seams, used-object masks, texture bake,
source-versus-baked photo pairs and portfolio docs remain to be built after
the form review.

---

## Accepted construction revision — one form pass

The lead accepted the massing, roof intersections, trim, openings, drainage
and seed grammar. Preserve them. The revision changes the room story at the
rear/sides: a 6 ft kitchen slider and landing, high short sink window, a true
between-floor stair window in a reserved stairwell, garage service door,
patio/deck seed choice and occasional low direct-vent fireplace chase.
The foyer is a shallow floor/wall/ceiling enclosure, not a full interior.
An octagonal garage vent is cheap enough to add. Keep the accepted portico
rather than introduce a new full-width porch roof in this pass.

The form audit now measures the foyer and rear steps as actual surfaces.
Ordinary openings still clear floors and plates; the stair window is an
explicit exception inside the reserved stairwell. All six built/imported
forms pass, as do 1,000 plan seeds. The slider and service leaf have real
origins, with independent sampled motion checks alongside the front leaf.

The 8.9 MB placeholder file was largely attribute overhead. A same-geometry
repack is 4,992,424 bytes, retaining positions, hard normals and UV0. Remove
the unused tangent channel and text-conversion UV1; pack POINT tint as
normalized u8 RGBA. Exact tuple comparison finds just 1.1% strict duplicates,
so indiscriminate welding would sacrifice profiles for little benefit.
The new form itself is 47,750 triangles and 4,643,868 untextured GLB bytes.
The count reduction includes fewer rear window assemblies, not a claim that
attribute packing removed triangles.

## Look pass 1 — original fields, first source Cycles review

Evidence: all six views in `renders/lookdev-pass1/`, open beside the colonial-1991-oh,
colonial-rog-ri and summer colonial-2003-nh photos. These are source renders, as requested.

**Color and value first.** Roof albedo now averages about .10 linear; veneer
is real red-brown brick instead of the orange placeholder band. The facade
still looks too smooth at street scale. The first clear-glass region is too
rough: it reads frosted and hides the room depth. Reject that glazing response.

The rear reads as a kitchen/family-room wall rather than a repeated grid;
the slider, high sink window, patio and stair window explain circulation.
The open entry reveals a shaded wall and floor instead of unbounded black.
Keep those additions. The roof's initial repeated tab widths resemble neat
masonry blocks. Give every course independent widths/staggering and reduce
whole-tab color contrast; granules should blend a roof, not make a checkerboard.

## Look pass 2 — glass, laps and the three photo pairs

Evidence: `renders/lookdev-pass2/` and all three pairs under
`renders/lookdev-matches-pass2/`. The unchanged first two calibrations retain
their original residuals. The summer comparison is a weaker type fit.

**Color and value first.** The source house is cooler than the landscaped
listing photographs, especially in shadow. Its sand/forest palette differs
from their gray/green vinyl; do not infer physical reflectance from processed
photos. Keep white below paper-white, the roof dark and brick muted. The
`colonial-1991-oh` reference's course shadows are still much stronger at a whole-facade view. Strengthen the
overlap shadow/profile instead of making the wall brighter.

Clear upper panes now reveal curtain depth and variable blind heights. Lower
screens soften transmission without an oversized woven grid. Reflection lacks
the photos' trees; procedural sky/clouds give a controlled environment but
cannot recreate a mature yard. Do not disguise that limitation as an asset
match. The main roof reads as staggered shingles rather than a flat sheet;
the extra 20 m view must target the main roof, not a garage gable obscuring it.

The first weather field is too faint in the street hero. Increase irregular
base splash and localized drainage staining; sample those regions explicitly.
Avoid a uniform dark band. North roof/eave aging belongs on +Y exposure, not
all roof planes. Porch shade should remain deep while the foyer receives
natural indirect light from its opening.

## Look pass 3 — weather samples and trim-atlas rejection

Evidence: all six `renders/lookdev-pass3/` views, followed by the refreshed
source details. Inspect the front window at full size, not just the contact.

**Color and value first.** The revised butt shadow is readable on the full
facade without raising vinyl albedo. Roof grain and brick joints survive the
street view; darker base and runoff regions retain their material colors.
The closed door needs its own entry detail so faded red paint can be judged
outside the open-door silhouette.

Reject a UV implementation error: an incorrectly parenthesized atlas span
lets part of the shutter sample soffit perforations and adds spurious bands
to glass. Correct the span and assert that each face stays inside its chosen
V strip. Restrict louver normals to recessed shutter infill; frame members
need plain paint. Map long stock along U instead of stretching a whole strip
over six-meter posts. Painted gutters must sample dielectric paint, not bare
metal. The soffit's own underside should show the perforation region.

Weather subdivision was also spending triangles on hidden roof undersides and
inner wall skins. Limit dense samples to exposed surfaces, retain causal cuts
near grade/drains, and dissolve zero-area triangulation edges into neighbors.
Do not delete arbitrary triangles. Actual roof/hole rays and topology checks
must still pass after that cleanup. The result is 56,396 triangles, including
8,646 additional weather-sampling triangles, within the original target.

## Look pass 4 — current source gate and stock export proof

Evidence: all ten current `renders/lookdev/` views, twelve independent front/
rear seed portraits, and the three current photographic pairs. The contact
and six-seed sheet are ignored review artifacts, not final portfolio images.

**Color and value first.** The asset-silhouette display luminance is p1 .137,
p50 .483, p95 .712 and p99 .725, with zero clipped-white pixels at the stated
threshold. These are display values under this daylight, not physical albedo.
The roof remains substantially darker than trim/siding. The source has clear
butt shadows, muted red-brown masonry, dim window rooms and deep entry shade.
Base splash and north roof/eave discoloration are visible at whole-house
scale, with finer overflow and nosing wear more apparent in the details.

The corrected window has plain shutter frames and louvered infill, no false
perforations or atlas-crossing bands. Clear and screened panes retain curtain
depth. The foyer's wall/floor enclosure is legible but naturally dim. Garage
and rear service circulation is readable in the side/back views. The six
sources retain believable builder variation and show both patio and low-deck
options; the chase does not pass through an upper window or roof.

The source-PBR GLB proof initially exposed a sixteenth image: disconnecting
glass's metallic input made Blender repack its ORM. Keep the shared ORM link
and select glass regions whose metallic channel is zero. The proof now has
six materials and fifteen images, four meshes, one UV channel and POINT tint.
Normalized tint is compared to source colors at matching world positions;
its maximum per-channel difference stays within .5/255. A fresh import also
retains the three moving pivots. No custom weather shader
or compression extension is present. This proves serialization, not final
bake fidelity or an engine's shared-resource allocation.

The portability audit rejected tightly packed RGB8: vertex elements must be
four-byte aligned. Use RGBA8 with alpha fixed at one and check every exported
attribute's effective stride. This adds about .12 MB and preserves the large
reduction from removing unused channels and float color storage.

The fifteen original source PNGs total 17,599,598 bytes; their planned BC7/
BC5/BC7 allocation is 38 MiB with mipmaps. The self-contained diagnostic GLB
is 22,656,636 bytes. Final family packaging must share those images externally
or within a multi-house GLB rather than embedding copies in every house.

Still weaker than the photos: sparse reflection scenery makes some panes
too uniform; undressed rooms remain simple shallow backings; roof granule
and fine weather response still need the final bake/filter comparison. The
summer fit is 8.48 px RMS and reaches the lens bound, so it cannot certify
survey-accurate massing. No claim of full interiors, hidden structural framing,
permit compliance or a finished photoreal delivery follows from these checks.

Stop here, before the Cycles bake. Final delivered texture filtering, exported
GLB photo comparisons, engine image reuse, Eevee and portfolio docs are the
next stage. No requested checkpoint work is deferred to those delivery checks.

The final aligned-export gate was run from `make clean` (including all source
maps), followed by `make SAMPLES=48`. Both prototype and source-PBR GLBs and
all fifteen PNGs reproduce their pre-clean bytes. All 25 source views reference
the rebuilt files. `make check` and the repository check pass. No kit API was
changed and no generated binaries or review JPGs are committed.

---

## Delivery pass 1 — 4K bake, stock glTF, and rejected subtle age

Evidence: `renders/delivery-pass1-fixed-uv/` (five full-size views) and all
three `renders/delivery-pairs-pass1/*-pair.jpg`. These import the exported
glTF and its shared PNG directory. The earlier `delivery-pass1/` preview
was superseded during a rebuild and failed its provenance guard; its images
are diagnostic only. It is not final evidence.

**Color and value first.** The three photographs still show warmer roof
aggregate and stronger separation between directly lit trim and cavities.
The dark roof has appropriate value, but the sky's diffuse blue dominates its
neutral granules. Preserve the accepted facade palettes; warm the charcoal
factor and rebalance daylight toward direct neutral-warm sun. Clear sky has
already removed the previous smoky noise. No photographic lighting is baked.

The exported siding's lap profile, brick mortar and varied room depths
survive the bake. Fine normal responses differ slightly after physical bump
baking/filtering: the stored-map check records mean errors separately from
worst texels, rather than claiming a lossless bake. The window remains simpler
than real tree reflections. Keep that honest; do not paint scenery into glass.

Reject the still-clean garage bottom panel and step edges. Increase dirt there
and at downspout feet. The corner runoff has a placement error: a roof's
305 mm overhang puts an endpoint outside the supporting wall, beyond a narrow
stain. Project the stain and its vertex samples onto the actual wall span.
The first two or three siding courses now receive splash at their own start
height (including above a veneer water table), rather than only near grade.
North-exposure normals must come from the outer surface, not an arbitrary
thin edge or inner face sharing its vertices. Correct those assignments.

The independent final checker also rejected 567 zero-area UV triangles on
roof gauges/caps. Give those vertical sides ordinary side charts while
keeping true slope-distance charts on the roof faces. All six then pass:
56,716–59,084 triangles, zero degenerate UV triangles, standard normalized
RGBA8 color, six or five used materials, fifteen or twelve referenced images.
A no-veneer house correctly omits the unused brick material and three maps;
the family still has just fifteen shared files.

## Delivery pass 2 — warm roof and localized service age

Evidence: the twelve full-size Cycles views in `renders/final/` (subsequently
retained as finals) and the repeated three photographic pairs in
`renders/final-matches/`; source comparisons use `renders/lookdev-matches/`.

**Color and value first.** The hero roof is now warm charcoal instead of
blue-gray, below the facade's value, while north-facing planes remain darker.
The source PNG remains a neutral aggregate; three seeded warm/wood/brown
linear tints multiply it without new materials or images. Lower sky fill and
a neutral-warm direct sun restore the deep eave/entry recesses and preserve
trim highlight roll-off. The summer roof comparison supports the value range;
its photographed roof is brighter in different sunlight, not a reflectance
sample to copy. The scene uses a clean procedural sky, no cloud noise.

Base splash stays attached to the first exposed courses, with an irregular
height boundary and brown rather than blue/gray soil attenuation. Foundation
concrete darkens toward grade. The garage's bottom panel is visibly dirtier
than those above it; the step nosings have localized brown grime and cleaner
worn lips. The faded entry retains its original paint family. Projected gutter
corners and the downspout shoes produce localized dark water marks, rather
than a whole-wall noise wash. North algae is gray-green and ridge-weighted;
it is more evident from the back/top than on the sunlit hero's south roof.

All details were opened at full size. The normal bake preserves the lap butt,
mortar and soffit response. Its fine granular variation loses some high-frequency
contrast after filtering, which is appropriate at 420 px/m. The close window
still reveals plain sky in its reflection: the sparse isolated presentation
cannot resemble a fully landscaped photograph there. The entry's shallow
wall and floor are present but intentionally dim, not a complete room.

The scale silhouette is a neutral 1.8 m aid and stands on the landing. The
front/side/rear/top views expose the real plan and drainage. Keep the accepted
construction and triangle target; the revised seed 27 is 58,232 triangles.
Next inspect the six independent imports, Eevee and actual ground connections.

## Delivery pass 3 — six imports, stock image reuse, Eevee and street rejection

Evidence: all twelve `renders/final-seeds/<seed>/{hero,back}.png`, the first
Eevee hero, and the first `renders/street/street.png` (replaced by pass 4).
The final/source calibrated pairs were opened side by side again.

**Color and value first.** All six retain muted builder palettes and dark,
warm roof choices. The photo-pair bake loss is small at facade scale: the
source/export lap, mortar and room backing values track each other. The real
summer photograph has much more complex dappled light and landscape reflection.
Those differences should remain listed as limitations, not silently attributed
to camera fit or hidden behind altered albedo.

Reject the initial Eevee glazing: without transmission ray tracing it becomes
opaque white and erases the room depth. Enable the engine's tracing and slab
refraction while retaining the original imported PBR nodes and textures.
Cycles' correct glass does not prove Eevee's renderer is configured correctly.

The street's initial actual-surface check caught a misplaced walk before any
render was accepted. Imported roots used quaternion rotation mode, so assigning
Euler yaw alone had not rotated the paving. Explicitly set instance rotation
mode, orient the sidewalk along its own longitudinal panel direction, and
match its gentle grade to both the road and bottom stair. The driveway's
sawn edge is placed at the sill surface rather than its nominal slab plane.
Contacts are independently measured on the imported paving triangles.

The first completed street render still failed visually: tiled lawn slopes
reset at each cell and left visible dark seams, the tree was excessively
cropped, and the finite lot ended against an empty blue horizon. Level the
imported lawn modules by their instance transforms, widen the street camera,
and add a low distant presentation plane using the imported lawn material.
Turn and tilt the pickup as a parked instance, retaining its real tires.
No ground, tree or truck source/export is edited, joined into the house, or
re-exported. Scene staging is separate from the house's delivery.

A real multi-import test loads different seeds and a repeat. It retains the
same fifteen external-image datablocks, by identity and canonical path, rather
than merely observing equal PNG hashes. Compression remains an engine import
choice; the 38 MiB figure is not Blender's uncompressed pixel allocation.

## Delivery pass 4 — final baked package, repeat build and portfolio gate

Evidence: the current `renders/final/` hero, turnaround, details, scale and
shingle view; `renders/final-eevee/hero.png`; all twelve independent seed
portraits and their six-seed sheet; final/source photographic pairs; and
`renders/street/street.png`. The full-size images and all five small JPGs
were opened, including the contact sheet. Earlier delivery critique frames
are archived locally under the worktree's ignored `build/` during clean builds.

**Color and value first.** Warm charcoal now reads neutral-to-warm in direct
sun; the north plane stays darker with restrained gray-green biological
shading. The full hero retains brown base-course/foundation dirt, a visibly
dirtier garage bottom and localized runoff. The shaded door is desaturated
within its own paint family. The rebuilt hero has deep recesses and zero
clipped-white pixels in its actual projected silhouette. Source/export pairs
retain siding, brick, glazing depth and roof values after baking/filtering;
the photographs' different landscaping and light are not claimed as a match.

Eevee's remaining failure had a precise cause. With an unconnected Thickness
input it derives an approximation from the whole joined building, skipping
the shallow window rooms. An explicit linked 4 mm pane gauge plus slab/screen
tracing restores those rooms while retaining the imported PBR factors and
maps. This is an Eevee renderer setting, not an altered game shader or a
replacement glass texture. Screen tracing still softens or ghosts fine grilles
more than Cycles; it is a documented real-time presentation limitation.

The street now shows the maple crown, the parked pickup, ground-family lawn,
walk and driveway, with no empty blue horizon gap. Imported pavement triangles
meet the two sockets within float precision (under 1 micrometer in this build).
The near driveway edge meets the measured garage sill within the house's
existing bevel tolerance. The pickup is turned toward the garage and tilted
to the drive grade; imported model/texture files retain their hashes.

The final checker proves all six surfaces and fresh imports, zero degenerate
UVs, correct normal/tint data, pivots and relative shared image URIs. All six
plus a repeat hold fifteen image objects by identity in one stock importer.
A separate fresh selection containing only no-veneer seeds still ships the
whole canonical family; replacing a stale generated map and removing an old
seed are exercised without a manual clean.

The clean rebuild repeats all twelve geometry/glTF files byte-for-byte. GPU
bakes agree within the kit's 2-byte maximum / .02-byte RMS policy: the observed
largest channel delta is one byte and largest RMS is below .0036 byte. This
is not a claim of bit-identical GPU rendering. Current-view provenance hashes
include the shared PNGs as well as each glTF and binary. The final review gate
checks 29 exported views plus source photo evidence, and five docs JPGs remain
at most 1600 px and 200 KB each. Repository rules and `make check` pass.

Still visibly CG: the isolated reflections and shallow room treatments are
simpler than a furnished, landscaped home; asphalt granules lose very fine
contrast at the family density; straight construction edges are unusually
regular; the lawn/tree context and distant plane remain procedural. The street
is a house integration proof rather than a fully populated neighborhood.
There are no full interiors, collision meshes or delivered distance LODs.
Those limitations are explicit in the README and are not hidden by the checks.
