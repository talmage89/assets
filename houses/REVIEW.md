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

---

## Ranch checkpoint — pass 1: first form and source fields

Evidence: `renders/ranch/pass1/{hero,roof,window,eave,entry}.png`, opened
beside the leaf-on Oklahoma and California photographs and the supplemental
Minnesota brick photograph. This is a **new source checkpoint, before bake**;
the accepted colonial delivery above remains separate and unchanged.

**Color/value first.** Reject the temporary four-region brick atlas: the first
wall changes from red to buff at a texture boundary. It is a UV/material error,
not period multicolor masonry. Use independent repeating fields with neutral
mortar. The roof remains darker than trim, and the eave shade reads at street
scale. The glass has real backing/curtain depth but lacks landscape reflections.

The low mass and picture assembly read as a ranch, but the camera hardly shows
the building's depth. Take the next hero from the garage end so a side-entry
seed does not present a seemingly unbroken wall. A common roof must be one
roof envelope, not coplanar main/garage skins. A projecting garage can reuse
the colonial's exact clipped intersection. Slender iron posts are preferable
to shrinking the colonial's bulky column/plinth assembly.

Correct corner boards that ran below grade. Wide eaves need a larger pipe
setback over brick; the original colonial pipe distance can bury the ranch's
pipe in the proud veneer. Add battens at gable accents and real carport ties,
without spending geometry on individual bricks or shingles. The very regular
roof field and uniformly clean trim remain weaker than the used-house photos.

## Ranch checkpoint — pass 2: brick, roof union and corner drainage

Evidence: all six `renders/ranch/pass2/` views and the two pairs in
`renders/ranch/matches-pass2/`, opened in full. The brick picture comparison
is spring; the broad roof comparison is leaf-on September daylight.

**Color/value first.** Independent brick fields remove the impossible red/buff
switch. Red masonry is restrained, with neutral mortar; trim stays below paper
white. The photographs have warmer direct light and richer reflections. The
source is still more regular and less nuanced in age. Do not brighten the
whole object to compensate for the dim window backings.

The whole-house pair supports the long, low roof profile. Its stone walls,
recessed entry, shallow L and wider wood picture unit intentionally differ
from our brick, small covered stoop and side-entry garage. The 8.35 px RMS
fit is a type comparison, not a surveyed match. The 7.75 px picture fit makes
the large fixed pane/flanking sashes easy to compare; our vinyl replacements
are thicker and lighter than its older wood/casement unit. Its reflected
neighbor and interior lamp are absent from our simple procedural presentation.

Reject the paired downspouts at a hip corner: the two adjoining gutter runs
need one shared outlet. Raise the ranch's roof allowance from 6 to 10 in so
30 in overhangs at 5:12 do not cut the picture-window head casing. Add an
explicit grammar check for that clearance. Move the entry/window rhythm just
enough to keep canopy posts and their pipes in solid piers, rather than over
the picture unit's edge. Preserve the actual 8 ft ceiling.

Actual roof rays initially reported the new canopy as a wrong main-roof
height. It really intersected the main overhang; unite those envelopes and
clip both at the intersection instead of giving the audit an exemption.
The carport's pipe-support miss was also real: move its end posts closer to
the slab ends, retaining bearing on the slab, and extend the straps.

## Ranch checkpoint — pass 3: six built plans and actual surfaces

Evidence: all twelve current front/rear portraits under
`renders/ranch/checkpoint/seeds/`, and the refreshed hero, rear, roof, eave,
picture, entry and scale views. Each was opened. Source geometry is separately
measured in `build/ranch/checks.json`; view provenance hashes the source and
its actual original/shared map inputs.

**Color/value first.** The four brick families remain distinct and muted.
Buff/tan do not become pale paint, and their mortar stays neutral. Roofs
remain below wall/trim value. The source's browner low masonry and deeper
entry/eave shade read, but its more regular surfaces and subtle chalk/salts
still look simpler and newer than the photographed older homes. This is a
form/source checkpoint, not an accepted final weathering look.

All six read as separate ranches: continuous gable, continuous hip, shallow
projecting garage, side entry, one/double garage, open carport, shutters,
battens, broad ridge/end chimneys, and different masonry coverage. The rear
has high bathroom windows, a sink window and patio slider, rather than the
colonial's repeated upper story. The carport posts bear on the slab and its
pipes now have actual nearby supports. Short bedroom sills leave room below
for furniture. The canopy posts no longer sit over the picture-window frame.

The six sampled meshes have no missing roof rays, blocked wall openings or
service obstructions. All door motion sweeps pass without contact exemptions.
The first weather subdivision exposed a nearly collinear roof triangle in
seed 14; dissolve the degenerate subdivision edge before triangulating, rather
than deleting a random triangle. The measured source remains 30–43k triangles.

Reject the first same-scale framing: both outside house ends are cropped.
Use a shared orthographic view wide enough to show both complete roof envelopes.
Move the optional scale figure toward the center of the stoop so a post does
not hide its torso. The initial colonial import also encountered Blender's
canonical material-settings group colliding with the source occlusion group;
rename that source-only group for presentation, retaining the imported asset.
No saved colonial or source building is modified by that fix.

## Ranch checkpoint — pass 4: current source gate and regression proof

Evidence: all 22 current Cycles views under `renders/ranch/checkpoint/` and
`renders/ranch/matches/`, the six-seed sheet, contact sheet and photo-pair
sheet. The final complete type comparison and unobscured 1.8 m figure were
opened after their framing corrections. The source-only colonial comparison
fallback was also rendered/opened, so a fresh clone does not need a new bake.
The extra-low orthographic camera originally revealed the finite presentation
plane's front edge; raising both camera and target framing removes that edge.

**Color/value first.** The hero's actual projected house silhouette has display
luminance p1 .087, p50 .326, p95 .526 and p99 .668, with zero clipped-white
pixels at the stated threshold. Those are display values under our procedural
summer lighting, not measured material albedos. The dark roof, shaded soffits,
dim window rooms and muted paints avoid the earlier pale library tendency.
Red brick is still more uniform and more saturated than the varied used-house
reference. Keep that as a specific next-stage material correction, rather than
pretend a topology or camera test certifies the look.

The final broad photographic comparison has 11.61 px RMS after increasing the
roof allowance; its roof/wall/entry proportions are deliberately different from
the photograph's stone L-plan. The picture fit remains 7.75 px RMS. Independent
Blender projection agrees within .0003 px. These are type/proportion aids,
not recovered physical cameras. The final source has a fixed large center pane,
operable flanking units, true returns/sill and real eave shade, but still lacks
the photograph's trees, neighboring reflections and furnishings. The small
covered stoop is valid within this grammar; a recessed main-roof entry would
be a worthwhile future form option, not a claimed current feature.

The default ranch `make TYPE=ranch` completes at this gate: six actual sources,
geometry/GLB repeat, authored override, 1,000 plans per type, 18 rejected invalid
controls, actual-surface and all moving-leaf checks, calibrated cameras, 22
fresh source/context/image hashes, sheets and repository check. No ranch bake,
final UV certification, final delivered texture package or docs JPG is claimed.
The single-car seed is 30,064 triangles; the most detailed is 43,072. Do not add
polygons merely to pull the smaller house up to the 35k preference.

Colonial preservation is proved twice: all six pre-change construction vertex
and full compact-GLB hashes match, and the original colonial `make check` passes.
All six delivered `.gltf`/`.bin` pairs and all fifteen shared PNGs retain their
accepted SHA-256 bytes after rebuilding that delivery. The unchanged delivered
counts remain 57,372–59,526 triangles. Existing portfolio images therefore
retain their exact asset inputs. No kit code changed.

Stop here as requested. The remaining weaknesses are source-look polish:
regular masonry/shingle fields, very simple room/glass reflections, quiet
whole-house aging, and faceted elbows/secondary fixtures at extreme close-up.
Period brick source fields are generated, but the 4096 bake/filter and the
baked-asset photo comparisons wait for the next stage. The planned new buff,
tan and red-brown 512² tiles add 3 MiB to the unchanged 38 MiB family. Aluminum
and battens reuse trim. Nothing is needed from the lead beyond this checkpoint
review; no new tool or shared-kit feature is required.

---

## Ranch revision — pass 1: masonry construction and rejected values

Evidence: `renders/ranch/revision-pass1/` (hero, roof, window, eave, entry),
`renders/ranch/revision-pairs-pass1/*-pair.jpg` and the original photographs.
All were opened. These replace the earlier checkpoint's form assessment.

**Color and value first.** The initial sunny brick patch measured Y′ .353
against .580 in the dated 1960 reference; its roof measured .366 against
.683. Reject that comparison. Y′ means Rec.709 weights on encoded sRGB,
not measured material reflectance. The photographs have different exposure;
the asset's street lighting cannot silently stand in for a calibrated photo.
State the photo camera exposure, and compare sunlit brick, shaded brick and
roof together. The new fired-unit variation and pale, recessed mortar improve
masonry, but the architectural roof's first tab table is too contrasty.
Reduce that packet variation before judging the larger roof field.

The masonry construction now has actual shell returns, a recessed frame,
individual sloping rowlocks and a thin angle above the head. It no longer
looks like white trim boxes glued over brick. The wider fireplace chimney,
concrete crown, supported stoop beam and off-corner gutter outlet are better
proportioned. Reject the first reflection scenery: large opaque crowns become
black balloons in the fixed pane. Remove their transmission-ray visibility;
replace those overscaled forms with small, perforated original leaf geometry.
No photographed scenery may be painted into glass.

The independent motion audit caught a forward-shifted entry hinge hitting a
wainscot wall at 105°. Restore its inward barrel/leaf placement while keeping
the exterior masonry frame recessed. A sequential downspout clamp also moved
one pipe out of one window and into another. Pick a solid pier against the
union of all opening intervals instead. Both are physical fixes, with the
same motion/support checks retained.

## Ranch revision — pass 2: full family, roof profile and rowlock rejection

Evidence: all 21 views in `renders/ranch/revision-pass2/`, including all twelve
front/rear portraits; the source details were opened at full resolution as
well as on `all-views.jpg`. Additional same-camera exposure diagnostics are
under `renders/ranch/exposure/`. References remain the Commons photographs.

**Color and value first.** At +.85 EV the dated-photo comparison gives sunlit
brick Y′ .552, shaded brick .247 and roof .649, versus .580/.239/.683. This is
much closer, including the shaded patch; it is not proof of physical albedo.
Set the final photo exposure explicitly to +.93 EV and slightly mute the red
body hue. Preserve the independent hero exposure at −.35 EV and the deep
upper-wall shade; do not brighten every seed to a single photograph.

The full-frame shadow band now carries the low silhouette. Most clear eaves
measure 24–27 in beyond the actual veneer; the plainest has 18 in clear, after
allowing for the veneer offset. The square columns stop at a beam underneath
the canopy. Broad ridge and end shafts read as fireplaces. All six plans still
read as plausible separate houses, including the open carport.

Reject the roof's raised-rib appearance in the overhead and chimney images.
Reduce the course height and overlap darkness, retain granule variation, and
keep the randomized course/roll addressing so a short tile does not stamp a
large repeating patch. Give the newer carport roof weathered-wood color so it
is distinct from the newer gray roof. Tired slopes keep localized north-side
algae, granule loss and a few attached curled tabs.

Reject the dark lines crossing some rowlock units. Their UVs selected the
middle of a mortar joint on odd running-bond rows. Offset those samples by
half a brick so every geometrically separate rowlock samples a solid unit.
This is a chart correction, not added geometry or decorative grime.
Rotate the two flue liners along the broad axis of the end chimney; crowding
them across its narrow axis is not credible construction.

The eave framing needs to show the bottom outlet and elbow rather than crop
the pipe at the left edge. Lower/widen that camera, retaining the actual eave
and wall. Add an iron-column/old-window detail and overheads of every seed so
period windows and roof variation can be inspected directly. Strengthen the
low masonry's irregular salt blooms and keep them within the damp/splash zone.
The next views must prove these corrections; source checks alone do not.


## Ranch revision — pass 3: contact audit and material continuity

Evidence: the complete 33-view source set and all four comparison pairs,
including six overheads, the wood/storm detail and iron-column entry.

**Color and value first.** The sunny three-quarter camera now fits the photo's
hard autumn light and processed contrast separately from the summer hero.
Brick/roof/shaded-brick Y′ differences are +.004/+.017/+.021. The dated 1960
comparison remains −.017/−.018/+.004. All are below .03, under explicitly
recorded lighting, exposure and tone curves; none is an inverse albedo claim.
The overhead sheet still gives the tired shingles too much rectangular
factory variation. Reject that checkerboard impression and reduce the tab
table to .92–1.08 while retaining causal algae and granule-loss masks.

A normal-disabled diagnostic proved the remaining diagonal rowlock colors
were a chart error: the construction source is already triangulated. Using
polygon numbers as brick IDs assigned different colors to the halves of a
unit. Use each prism's eight vertices for its ID and bounds. An independent
shared-edge chart check now covers 7,680 repeated loop samples with zero
UV discontinuity. Keep the running-bond half-unit correction as well.

Storm windows now have separate 3 mm glass, thin aluminum frames and a fixed
center picture light; only operable flank storms have meeting rails. Clear
transmission and a dim backing replace dark glass tint. The original
reflection-only leaf geometry and simple neighboring volume produce a real
roof/sky/ground reflection without photographic texels. Rooms remain simple,
and the reference still has richer scenery and furnishings.

The apron audit caught a second flashing problem: a quad crossing a hip
boundary bridged two slopes and entered the roof by up to 67 mm. Clip the
mitered apron ring against the same analytic plane envelope that builds the
roof. Its actual top now measures 12 mm above the roof, within float precision.
Counterflashing's outer skin is 1 mm proud and its back beds 2 mm into brick.
Add a concrete grade collar below the end chimney's formerly unsupported
20 mm gap. These are surface/contact checks, independent of serialization.
Localize soffit grime beneath actual gutter miters/ends rather than a periodic
noise seam. The final refresh must retain these corrections and the roof fix.

## Ranch revision — pass 4: current source checkpoint

Evidence: all 33 refreshed Cycles views in `renders/ranch/checkpoint/` and
`renders/ranch/matches/`; `family.jpg`, `roofs.jpg`, `contact.jpg` and
`photo-pairs.jpg`. Every view was inspected on the sheets; the eave, picture,
entry, iron-column/storm-window details, chimney and representative overhead
were also opened at full resolution. No ranch bake or docs JPG is produced.

**Color and value first.** Fixed patches give the following source/photo Y′:

| Comparison | Sunlit brick | Shaded brick | Roof |
| --- | ---: | ---: | ---: |
| Sunny three-quarter | .786 / .782 | .133 / .112 | .775 / .758 |
| Dated 1960 oblique | .571 / .587 | .244 / .240 | .665 / .683 |

All six absolute differences are below .03. The full JSON retains original
photo rectangles, projected source polygons, pixel counts and decoded linear
luminance as well. The three-quarter fit uses +1.95 EV, very-high-contrast AgX,
a lower sun and reduced sky/ground fill, matching its hard autumn photograph.
The dated 1960 fit uses +.93 EV with the normal studio light/tone curve. The
hero remains −.35 EV, medium-high-contrast AgX. These separate illumination/
camera fits do not establish a photographed brick's physical albedo. The
North Carolina photo's brown roof and tree shadows differ from our gray roof
and open presentation; matching values does not mean matching every hue or
reconstructing its private home.

The hero's projected house silhouette measures p1 .079, p50 .346, p95 .510,
p99 .669 and zero clipped-white pixels. Its broad eave shadow survives the
whole frame. The reduced tired-tab contrast removes the checkerboard read;
newer gray and weathered-wood architectural roofs stay distinct from the
older three-tab roofs. No short repeated roof patch stands out on the six
current overheads. Age remains strongest below the shaded ridge, at damp
masonry, sill runoff, gutter ends and walking surfaces. Fine aging is still
more legible in the close-ups than the hero.

The corrected rowlocks have continuous unit colors, real gaps and sloping
tops. Frame setback measures 97.5 mm / 3.84 in, sill slope 8.67°, angle gauge
4 mm. Three map courses average .203222 m / 8.001 in across fourteen spans;
the observed .203067–.203344 m range includes 512-map sampling. Clear front
eaves measure 18 in on seed 11, 24.165 in on 13/16 and 27.165 in on 12/14/15.
The square and iron posts bear on their stoops and stop at their beams.
All four fireplace shafts measure 4 × 2 ft. Their aprons measure 12 mm above
the actual roof surfaces, and their counterflashing skins/backs measure
+1/−2 mm relative to the brick. The end shaft's collar reaches grade.

The sunny three-quarter camera has a 33.79 px residual on a 2,641 px crop;
planting hides its ground anchors. The dated 1960 fit is 17.64 px, the summer
type comparison 11.61 px and the picture unit 7.75 px. These remain comparison
aids with different plans/window systems, not survey-grade recovered cameras.
The window now reflects an original neighboring roof, sky and grade while
retaining curtains/blinds. Its simple rooms and sparse reflection environment
still lack the photograph's layered landscaping and furnishings. Secondary
elbows and fittings remain less nuanced at extreme close-up.

`make TYPE=ranch WIDTH=1440 SAMPLES=48` passes at this source gate: six meshes,
1,000 plans per type, eighteen invalid controls, real roof/opening/support/
flashing probes, all moving-leaf sweeps, deterministic form GLB repeat,
calibrated cameras, 33 fresh source/material hashes and repository rules.
There are 28,122 roof probes with no misses and maximum error below 4.3 μm.
The six source counts are 48,674 / 36,010 / 45,236 / 31,192 / 36,668 / 40,262.
At most six material roles are used. The explicit 31-image source manifest
plans at 47⅓ MiB compressed with full mips; sixteen new source PNGs total
6,108,099 bytes before the final filtering/bake stage.

All six colonial construction/full-GLB byte comparisons remain exact. The
separate colonial `make check` passes, and its six delivered glTF/BIN pairs
plus fifteen PNGs retain all 27 pre-revision SHA-256 values. No kit code or
existing portfolio image changed. No new tool is needed.

Stop before the bake. The source roof's course/roll atlas addressing must be
converted to ordinary split UV charts for delivery; final bake/filter loss,
stock glTF/Eevee appearance and the final family package still need their
normal next-stage checks. The current source checkpoint makes no claims for
those unfinished delivery steps.

---

## Ranch delivery — pass 1: physical bake and ordinary roof charts

Evidence: all twelve `renders/ranch/delivery-pass1/` views, opened on their
contact sheet; hero, roof/top and all four details also opened at full size.
The original photographs remain the comparators. These views load the exported
glTF and shared baked maps, rather than the source blend.

**Color and value first.** The front has a continuous deep eave band under
lower, more frontal sunlight and reduced sky fill; the brick keeps its warm
body color, with the roof clearly darker than the trim. The new hero light is
presentation only. The entry stays dark without losing the green door. Mortar,
rowlock joints, soot-free crown, soffit holes and room backing survive baking.
The roof's fine grain is softer after filtering than in the source, and brick
still has a more regular manufacture than a real fifty-year-old wall. Preserve
the accepted look rather than adding a new age treatment during delivery.

Reject the first roof/top framing: an outside roof corner and the rear patio
are too close to or beyond the frame. Widen those cameras. The first source
checker also rejected an indexing failure in the conversion: every mesh had
all family material slots, so testing slots alone rebuilt non-roof meshes.
Restrict conversion to faces actually using the roof. Keep non-roof vertex
ordering so independent rowlock/flashing construction probes remain meaningful.
The exported doors then pass their sampled sweeps. Reject sub-texel UV slivers
at course boundaries that collapse in float32; snap coordinates within .0000002
UV of a chart boundary before clipping, without moving the surface.

The original native procedural fields are interpolated periodically to 4096
before the actual Cycles GPU bake. This deliberately preserves the accepted
512/1024 random unit tables; it does not invent or claim 4K source detail.
Physical height evaluates in meters, normals retain 16 bits until filtering,
and only the sixteen new ranch maps are published beside the untouched maps.

## Ranch delivery — pass 2: baked photographic comparisons and first street

Evidence: all four `renders/ranch/delivery-pairs-pass1/*-pair.jpg`, opened
beside the source pairs and original photos; first street render opened.

**Color and value first.** Exported sunny three-quarter brick/shade/roof Y′
differences are +.013/.027/.018; the dated oblique is −.009/+.011/−.018.
All remain below .03 under the unchanged photo-camera lighting, tone curve
and exposure. The increased diffuse mortar contribution after the physical
normal bake slightly lifts masonry relative to the analytic source normals.
That small loss stays inside the accepted value bounds. These are processed
photograph/display comparisons, not inverse measurements of physical albedo.
The real three-quarter roof is brown and receives tree shadows; our gray
replacement roof and open lighting remain different authored choices.

The picture comparison retains the sill, deep frame recess and layered sashes.
The neighboring procedural reflection is far simpler than the photographed
roof, garden and lamp, and its clear pane remains overly uniform. This is the
same accepted source limitation, not missing textures. The full facade's low
salts/runoff remain restrained; their strongest evidence is in the details.

The street genuinely imports both ranches, the colonial and the ground/maple/
shrub/pickup families' own exports. The first view has too much empty sky and
foreground and clips the second maple's crown. Tighten the image aspect and
move that presentation instance inward. Keep the houses at real meter scale.
No other-family mesh or texture is edited, joined or re-exported. The scene is
a neighborhood presentation, without a new claim of measured pavement socket
contacts; that separate construction evidence remains in the house checks.

## Ranch delivery — pass 3: complete imports, roof certification and Eevee rejection

Evidence: twelve full-size final Cycles views, all six front/rear/roof imports,
period-11 details, four photographic pairs, the tighter street and Eevee hero.
The initial finals are archived under `build/ranch/delivery/pass3/`; their main,
family, roof and period sheets were opened. The main four details, scale and
top were also opened individually. The next pass replaces these initial finals.

**Color and value first.** The full family keeps tan/buff/red/brown brick and
wood/gray/brown roofs distinct without pale trim. The tired north planes retain
localized darker aging; the newer gray and weathered-wood fields are separate.
The shaded rears are darker and cooler than sunny facades, without losing
windows or rear fixtures. The source photographs have much richer landscape
reflections and less uniform mortar/manufacture. Those remain specific visible
limitations rather than reasons to raise albedo or alter the accepted weather.
The revised top and roof cameras now include the complete attachments/corners.

The independent source check samples 146k roof triangle centers across six
houses. Float32 BVH nearest points on long thin gauges initially report
millimeter errors; float64 triangle/edge distances resolve them below 2 μm.
The saved source shader graph is evaluated separately from the converter.
At coincident miter/gauge surfaces, either source chart within 2 μm is valid;
source-triangle and wrap boundaries are counted separately where chart identity
is ambiguous. Interior addressing error stays below .000016 UV. This is a
source-preservation proof, independent of raw glTF and importer fidelity.

Float32 UV slivers are resolved by welding compatible coincident cuts,
dissolving degenerate edges into adjacent faces, and retriangulating only the
affected meshes. Normals and per-loop UV seams are retained. No triangles are
arbitrarily deleted. All six raw deliveries now have zero degenerate UVs;
all physical rays and moving-leaf sweeps pass. Named image URIs are chosen
before content-hash fallback so equal brick normals cannot select a different
color's filename through directory traversal order. Both types plus a repeat
hold exactly 31 canonical image objects in the stock importer.

Reject the Eevee dish: its single open surface disappears from the front when
backface culling is honored. Give that original paraboloid a 3 mm closed metal
shell, retaining its front position. This is a delivery construction correction,
not a new seed choice. Actual front/back rays measure 2.99978 mm, with zero
boundary/nonmanifold edges. Refresh the affected sources, exports, final views
and photo pairs; the change adds 216 triangles only to the dish-bearing seed.
The colonial's 27 delivered geometry/image files and five docs JPGs still
match every pre-delivery hash. Its separate `make check` also passes.

## Ranch delivery — pass 4: final shipped family and portfolio gate

Evidence: all current views in `renders/ranch/final/`, `final-seeds/`,
`final-eevee/`, `final-matches/` and `street/`. The full contact, six-seed and
roof sheets, five docs JPGs and all four final photographic pairs were opened.
The details, scale, top and corrected Eevee were inspected at full resolution.
All 38 view records resolve the current delivered geometry and shared maps.

**Color and value first.** Final exported/photo Y′, in the fixed patches:

| Pair | Sunlit brick | Shaded brick | Roof |
| --- | ---: | ---: | ---: |
| Sunny three-quarter | .795217 / .781535 | .139806 / .111734 | .774975 / .757727 |
| Dated 1960 oblique | .578165 / .587388 | .250692 / .239522 | .664671 / .682928 |

The maximum absolute difference is .028072. The photo illumination, exposures
(+1.95 / +.93 EV), tone curves and camera residuals remain stated; these are
not physical albedo measurements. Decoded linear values and patch counts are
retained in `build/ranch/delivery/values.json`. Three map courses measure
.2032224 m / 8.001 in, unchanged from the accepted native field.

The hero has a clear continuous eave-shadow band, warm brick, a darker roof,
deep entry shade and unclipped trim. Its projected-silhouette display Y′ is
p1 .0462, p50 .3782, p95 .5524 and p99 .6935, with zero clipped-white pixels.
The broad low mass remains the main read. Glazing keeps the accepted sky/
neighbor/grade reflection and shallow room layers. The corrected dish is now
present in Eevee as well as Cycles; measured gauge is 2.99978 mm and closed
sheet topology has zero boundary/nonmanifold edges. Nothing else in the
accepted construction, window/roof choices or weather was redesigned.

All six roofs retain their seeded styles and course/roll variation through
ordinary UV charts. No short repeated roof patch stands out on the overhead
sheet. The two original-window and iron-column details retain their thinner,
darker frames and storms, distinct from replacement vinyl. Rowlocks, brick
returns, gutter outlet/offset, supported columns and broad chimney remain
legible. The revised roof/top framing includes the complete geometry. The
street contains two ranches and the colonial on imported ground-family lawns,
with native-scale maple, both shrub types and the pickup; no context geometry
or texture is edited, joined into the house or re-exported.

`make TYPE=ranch WIDTH=1440 SAMPLES=48` completes, including checks and final
sheets/docs. `make TYPE=ranch check` passes the ranch and separate colonial
gates. Construction, motions and pivots remain measured independently from
serialization. All six game deliveries have zero degenerate UV triangles,
unit normals and normalized RGBA8 weather tint. Source-preservation checks
cover 146,237 roof centers, with maximum surface disagreement below 2 μm and
interior UV error below .000016. The 31-image importer reuse test holds the
same image identities across both types and a repeat.

Delivered triangles are 69,940 / 58,915 / 68,873 / 50,624 / 56,030 / 62,715.
There are six used materials at most and four meshes (three for the carport).
Several exceed the preferred 35–55k range: exact course/roll and wrap charts
must cut the accepted weather-sampled roof while the texture allocation stays
fixed. All remain below 80k. The sixteen new maps join the fifteen untouched
colonial maps, totaling 21,823,467 PNG bytes and 47⅓ MiB under the stated BC7/
BC5/full-mip estimate. The actual stock importer retains all 31 resources.

A second export reproduces all eighteen ranch glTF/BIN/optional-metadata files
byte-for-byte. The independent 4K GPU rebake stays within the kit's tolerance:
maximum one-byte channel delta, largest byte-domain RMS .001953125. The six
colonial glTF/BIN pairs, fifteen PNGs and five original docs JPGs match all 32
pre-delivery hashes. The colonial construction baseline also remains exact.
No kit file changed. Repository/source/privacy rules pass; no reference photo,
private-home identifier, source listing or generated binary is added to git.

Still visibly CG: mortar and manufacture are unusually regular; the glaze/
room layers and reflected scenery are much simpler than furnished homes with
mature gardens; fine normal response softens after filtering; service age is
more restrained at full frame than in the details; and the lawn, trees and
empty neighborhood context remain procedural. The street is an integration
presentation, not a complete neighborhood. These limitations are explicit in
the README. No tool, approval or new kit feature is needed to finish delivery.

## Ranch delivery — pass 5: triangle ceiling, measured eave and sidewalk view

**Color and value first.** Reopen all four photograph pairs and source/export
sheets for changed seeds 11, 12, 13, 15 and 16, then the two old/new hero and
north-roof close-up sheets. The broad roof discoloration, north-side algae,
low wall splash and eave grime remain visible. No loss is apparent at hero
distance; the close-up keeps the same granule pattern, dark patches and causal
variation. Small color interpolation differences exist, so do not call the
reduced weather field byte-identical. Roof area-weighted mean linear weather
luminance and two-way centroid maximum-channel errors measure:

| Seed | Roof factor Y, before / after | Mean RGB error | Worst local RGB error |
| --- | ---: | ---: | ---: |
| 11 | .499620 / .499587 | .000439493 | .031224 |
| 12 | .918191 / .918191 | .000108407 | .019166 |
| 13 | .671863 / .671844 | .000298597 | .023484 |
| 15 | .681022 / .681022 | .000000332 | .005995 |
| 16 | .670175 / .670172 | .000392350 | .023042 |

These are linear `COLOR_0` factors, not display Y′ or physical albedo. The
independent comparison samples both triangulations' centers, area weighted;
coincident trim/gauge facets are matched within 20 μm, retaining raw nearest
errors in the report. Shared texture bytes are unchanged. Evidence is
`build/ranch/revision2/weather-comparison.json` and
`renders/ranch/revision2/compare/{11,13}/before-after.jpg`.

The repeated photo-camera renders retain warmer sunlit masonry and deep eave
shade. Current seed 12 exported/photo Y′ patches remain .795/.782 sunlit
brick, .140/.112 shade, .775/.758 roof in the sunny three-quarter; dated
oblique values remain .578/.587, .251/.240, .665/.683. Maximum fixed-patch
error is .0281. All five changed seeds were rendered from both the native
source and current export in all four cameras. Asset-silhouette mean absolute
source/export Y′ errors range .00257–.00582; largest per-view p95 .0244.
Isolated feature/reflection differences reach .269, so these means do not
promise every pixel within .03. The five source/export and photo sheets were
opened; none shows lost weather regions, reversed normals or a chart seam.
The roof close-ups still show the previously accepted filtering of very fine
granules. Calibration is a type comparison, with differing house plans and
photographic illumination, not a survey or an exact photographic reconstruction.

Reject the previous faint hero band. Raise the front-directed sun to about
36° and reduce sky/grade fill, keeping the accepted materials and geometry.
In the final 1440 px render, three clear front-wall profiles cross the
lit/shaded threshold at a median band height **.643633 m / 25.34 in**, or
**43.88 px**. Mean band Y′ **.046942** compares with shaded side masonry
**.038384**; difference .008558. Yellow and cyan patches on
`renders/ranch/final/hero-band-measurement.jpg` show the actual sample areas.
The height comes from rendered threshold crossings projected onto the
imported masonry, not an overhang constant. Sun-projected vertex bounds and
visual inspection keep the whole ground shadow in frame. Hero silhouette
p1/p50/p95/p99 is .0154/.3482/.5187/.6677, with zero white clipping. The band
now reads at full frame; the facade still has warm brick, readable mortar and
unclipped trim. The dark side and entry remain intentionally deep.

The prior triangle justification was insufficient. Dissolve redundant planar
weather samples after ordinary UV chart resolution, using affine UV/color
tests, collinear boundary tests and unchanged hard-normal splits. Preserve
front walls and low wall weather. On the three densest sources, omit random
course phase cuts only from concealed roof gauges and 24 mm eave lips; exposed
roof planes retain full seeded course/roll addressing. Do not remove physical
edges, penetrations, valleys, moving leaves or fittings. Actual source-surface
checks remain below 2 μm disagreement. The delivered result is:

| Seed | Before triangles | After triangles | After glTF + BIN bytes |
| --- | ---: | ---: | ---: |
| 11 | 69,940 | 59,795 | 5,597,923 |
| 12 | 58,915 | 55,228 | 4,906,874 |
| 13 | 68,873 | 59,576 | 5,693,608 |
| 14 | 50,624 | 50,624 | 4,633,617 |
| 15 | 56,030 | 54,998 | 4,991,063 |
| 16 | 62,715 | 53,037 | 4,722,440 |

Every seed is below 60k; median **55,113**, down from 60,815. Total reduction
is 33,839 triangles / 9.22%, without another texture or material. Geometry
bytes total 30,545,525. Family GPU estimate stays **47⅓ MiB**. The repeat
export matches all eighteen ranch geometry/metadata files. All 31 image files,
all 32 colonial geometry/map/docs hashes, and seed 14's glTF/BIN remain exact.

Reject the original distant street composition and an intermediate preview
whose distant lawn plane covered the depressed road. Lower that presentation
plane and use the native ground family's asphalt, curbs, sidewalks, lawns and
driveway pours. Place the camera on the opposite sidewalk, measured 1.68 m
above its actual surface. The nearest ranch spans **37.54%** of frame width;
the colonial spans 20.20% and the farther ranch 12.99%. The road now has a
readable crown and curb edge, the lawns form bands, and the houses recede in
three-quarter front views. PinOak from current main stands behind the first
house beside the RedMaple farther along. Both species, shrubs, pickup, ground
and houses load their own deliveries, with hashes recorded. All instances are
presentation only; no foreign mesh/material is edited or re-exported, and no
street socket-contact claim is made. The composition is stronger, although
the sparse horizon and lack of a full neighborhood remain conspicuously CG.

Validation: `git merge main` was already up to date. The full
`make TYPE=ranch WIDTH=1440 SAMPLES=48` completes. A subsequent
`make TYPE=ranch check` passes ranch construction, motion, delivery, UV/chart,
import/image-reuse and repository gates, then runs and passes the separate
colonial `make check`. All 38 final views use current bundle/map hashes.
The changed-seed photo cameras also pass independent Blender projection
verification. Refresh all five ranch docs JPGs after opening the contact,
details, seed/roof sheets, Eevee, scale, hero, street and comparison sheets;
colonial docs stay unchanged. The new optional `bake-loss-pairs` target
reproduces the five changed seeds' photographic proof. No kit file changed.

Remaining CG tells: overly regular manufacture in masonry and roofs, shallow
room layers and simple reflections, filtered fine granules, sparse landscape
and a flat distant horizon. They are existing limitations, not hidden by the
triangle reduction. Nothing is needed from the lead to finish this revision.

---

## Cape form — pass 1: first roof and dormer assembly

Evidence: `renders/cape/pass1/hero.png`, opened beside the New York spring
and New Jersey leaf-on photographs, the Massachusetts summer renovation
views and the Illinois preservation photographs. This is a **source form
checkpoint**, not a new baked delivery or a replacement for either accepted
type above.

**Color and value first.** The roof remains dark relative to the trim and
walls; the raw photographs have different white balances and much richer
landscape reflections. Do not infer albedo from them. The inherited lap and
roof fields are enough to judge volume, not an accepted 75-year material look.
White casing is the neutral to use for later color comparisons. Keep real
paint factors below the accepted family ceiling rather than brightening the
whole scene to hide the missing age.

Reject the exposed stair-step fins behind the dormers. Step flashing continued
past the actual cheek/parent-roof intersection. End each course where the cheek
ends, so its top beds into siding instead of standing in the air. The early
sill also fell into the parent roof. Place the window and its header in the
actual dormer wall space and add an upward interior roof ray, rather than
calling a hole in the roof a usable room. The principal side gable is steep
and dominant; the tight rake is already a different construction from the
ranch's broad boxed overhang.

## Cape form — pass 2: complete six-house set and contact rejection

Evidence: all seven main views, twelve front/rear seed portraits, same-scale
three-type comparison and the contact/family sheets under `renders/cape/pass2/`.
Every view was opened on the sheets; dormer, eave, entry, roof, rear and scale
were also inspected at full size against the photographs.

**Color and value first.** White/gray/yellow/sage/blue/red remain restrained,
with deep roof/entry shadows and no paper-white trim. The quick cement and
cedar fields are still too regular and the shared roof is too clean. This is
not evidence of finished material age. The upper shadowed rooms remain simple
and gray-blue compared with real foliage/interior reflections.

Reject the narrow black open strip around the dormer bases. The envelope had
cut the parent roofing to the dormer **roof** footprint, including its overhang,
leaving no roof below the projecting trim skirts. Cut to the cheek-wall
footprint and retain parent roofing beneath the skirts. A separate actual
surface ray must find that roof there; this is not a check exemption.

The entry hood also exposed its interior intersection and unsupported-looking
triangle. Close its front with a painted-board pediment and supported ceiling,
then close the remaining face-band/beam slot. The brackets and portico posts
must bear into a beam and landing. Preserve the small stoop and equal rises;
do not turn a modest starter-house entrance into a full-width porch.

Six plans read as separate homes: two/three/no front dormers, rear shed
additions, low wings/enclosed-porch additions, detached and breezeway garages,
newer glazing and retained storms. Parking and wings stay on opposite sides.
Four-window fronts need enough width for real half-sash shutters. Very small
sash bevels on the most complex three-dormer assemblies are deferred to the
normal map, keeping casing silhouettes and all measured dimensions. This
brings every quick-field source into the preferred 30–45k range.

## Cape form — pass 3: photographic dormer proportion correction

Evidence: `renders/cape/matches/cape_dormers-pair.jpg` and
`cape_plain-pair.jpg`, first before the final dormer reduction, then refreshed.
Comparison photographs remain inspection-only. Summer regional context and
the dated spring supplemental view are distinguished in SOURCES.

**Color and value first.** Normalize the review copies on white-painted
exterior casing/door stiles. The spring photograph's linear RGB gains are
1.070/.988/.950; the leaf-on photograph's are 1.000/.962/1.041. Preserve their
mean linear RGB and exposure. The asset has a different authored palette;
these corrections do not establish physical reflectance. Its siding/roof
are smoother and its reflections much simpler than either real house.

Reject the overly tall dormer fronts in the first pair. They stand too high
above the low eave, making the half story resemble an applied second facade.
Lower the dormer bearing by 430 mm, move its face 100 mm toward the eave and
use a 28 × 40 in hung window. Keep a 4 ft 6 in body, real wedge cheeks and a
steep independent roof. This leaves the main roof as the dominant front mass,
with smaller punctures sitting below its ridge. The two-dormer centers align
with the side bays. The three-dormer rhythm is exactly centered on the entry
and the paired window-group centers, with equal spacing.

The unpierced variant's large plain roof and low wall compare credibly with
the New Jersey type. Its offset entry and picture window are later alterations;
its raised basement and hood differ from the photographed low floor and bare
entry. Those are authored variants. The dormer photograph has projecting bays,
shutters upstairs, an altered porch and an end chimney; the hero keeps simpler
windows, a stoop hood and central chimney. Do not stretch the model into a
copy of the private photographed home. Fits remain approximate: 18.25 / 19.26
px RMS, estimated 83.5 / 100 mm lenses, the second at its upper bound.
Independent Blender projection differs by less than .0008 px.

## Cape form — pass 4: current checkpoint and preservation gate

Evidence: current `renders/cape/checkpoint/hero.png`, rear, overhead, dormer,
eave/rake, entry and 1.8 m scale views; all twelve independent seed portraits;
`comparison/types.png`; both current pairs and the contact/family/pair sheets.
All were reopened, with the main details, rear, scale and type comparison at
full size. No docs JPG is published at this gate.

**Color and value first.** Current hero silhouette display Y′ is p1 .056,
p50 .339, p95 .684, p99 .692, with zero clipped-white pixels. The roof remains
substantially darker than the trim, with deep shade in cheeks, eaves and the
entry. The six paints retain their individual colors. The back is deliberately
in shade; simple reflection scenery is still much poorer than a real yard.
These are rendered display statistics, not albedo measurements or final
weathering approval.

The reduced dormers now sit within the roof rather than dominating it. Their
cheeks are wedges cut by the parent plane, with metal terminating at actual
intersections. Roofing under the skirt is continuous. The zero-rake hero's
edge is nearly flush, and the six proofs include 0, 3, 4 and 6 in rakes with
6–10 in eaves. The eave sits just above first-floor heads: actual source
casing/soffit clearances measure 58.7–143.4 mm. The entry pediment, brackets,
posts, face band and landing now read as a supported assembly. The rear shed
looks like a later addition, with a strip of original roof above and below it;
its transverse pitch break drains across the joint, unlike a level valley.
Basement windows now have actual holes and open wells even at the lower floor
height. Service stand-offs and line connections have physical wall supports.

Source tests measure 31,517 roof probes across the six houses with zero
misses, maximum height disagreement below 4.5 μm, plus 945 wall-opening/service
probes. Dormer-skirt contact, actual roof pitch, eave/rake extent, window-head
clearance, downspout support and equal stair rises are measured on the mesh.
Both moving leaves pass all sampled solid-clearance poses, without exemptions.
Separate raw-GLB/fresh-import checks prove serialization and pivot/socket
retention; they do not certify construction or baked materials. The repeated
first seed gives identical complete compact diagnostic GLB bytes. An authored
JSON-equivalent override is also built and audited.

The 1,000-plan sweep covers all three types, with nine new invalid Cape
controls rejected. All twelve accepted colonial/ranch construction digests
and full compact GLB hashes match the pre-Cape fixture. Their 77 existing
export/map/docs files retain their exact bytes. The small opt-in family
changes preserve the legacy RNG and default geometry path; no kit file changes.

Current sources use at most six roles and stay in the 30–45k preference.
Cedar/cement preview addressing still needs ordinary split charts and a real
4K bake/filter during delivery. One shared 512-square two-region triple is
planned, adding 1 MiB to 47⅓ MiB, for 48⅓ MiB with BC7/BC5/full mips. The
accepted shared maps are untouched and no new map is published to `export/`.

Stop before the bake as requested. Remaining weaknesses: very regular source
shingles/siding, overly clean and unworn trim, simplified original/replacement
frame differences, shallow window rooms and sparse reflections. Cedar grain,
cement joints, paint chalk/peeling, storm oxidation and stronger cause-driven
75-year wear need the next look-dev stage. There is no finished Cape texture
or UV certification, baked-asset photographic comparison, playable interior or
final game delivery claim. No tool or kit feature is needed for this checkpoint.

## Cape look-development, before bake

### Pass 1 — exposed structure and first age fields

Color and value first: compared the source white paint and gray-green roof
against used Cape photographs, balancing the white-painted door casing in the
white Cape and the attic casing in the cedar Cape. The initial source is too
uniform at street distance. Its siding retains the vinyl normal scale, and
the first peeling field wrongly affects interior fabric. The storm glazing
also needs a darker room behind its reflected sky. Images:
`renders/cape/lookdev/pass1/` (hero, entry, foundation and sill).

Raised the exposed concrete datum to 15–24 inches across these proofs, below
the floor framing and water table. Rear basement glazing/wells remain real
openings; the crawlspace has four framed louvered vent openings. The initial landing
was 28 mm below the threshold; the final contact correction is recorded below. Both connectors now have posts, roof beams,
a sided waist wall and a diagonally framed lattice back. Accepted roof and
opening geometry stays in the shared construction path. Deepened the window
backs to 1.15 m, with dark return walls. Fixed the interior/exterior paint mask
and gave wood its own 101.6 mm course period and staggered board-end joints.

### Pass 2 — inspect all elevations and diagnose the flat shingle fields

Color and value first: the first six-seed front/rear sheet distinguishes the
paint palettes, but the brown cedar and sage cement read as flat panels.
That is a failure, regardless of the dimensions in a report. Pixel inspection
found a preview-map encoding error: integer 0–255 input to the toolkit's
0–1 PNG writer clamped every map to white, including metallic. Corrected the
writer inputs and the opposite image-row/UV-V orientation of the half atlas.
Neither correction touches an accepted colonial/ranch map. Images:
`renders/cape/lookdev/pass2/`, including the initial family sheet.

The isolated sill now has dark room depth and sky reflection, but the paint
loss is too finely stippled and the room fabric has little construction detail.
Enlarged the peeling islands, limited them by the actual sill datum and added
sparse lifted film edges. Added a few curled asphalt tabs, attached uphill to
the original continuous roof. Their first placement is too regular in places;
the final pass must judge their value against the surrounding shingles.

### Pass 3 — distinct manufacture, exposure and comparison patches

Color and value first: the corrected cedar is too warm and too even beside
the neutral-balanced used cedar photograph. Increased silvering on exposed
upper/sunny areas while retaining brown under eaves. Strengthened actual
course/keyway contrast, retaining individual unit color rather than overlaying
a gray wash. Painted wood needs darker narrow course breaks to match the
photograph's low tail. Cement now shows the large, straight-butt units and
fine vertical face striations. Images: `renders/cape/lookdev/pass3/` and
`pass3b/` (including the encoding/orientation correction).

The shaded roof view is too dark to judge moss. Increased procedural sky fill
from .055 to .12 for every checkpoint view, retaining the same sun and EV.
The north-plane algae follows gravity; moss is confined to low courses and
dormer-cheek drainage. Added east-facing shade to the wall mildew mask where
the review sun leaves that wall in shade. Fixed physical patch cameras and
photographic ROIs before the numerical comparison; exposure and any auxiliary
paint control are recorded separately from the six proof palettes.

### Pass 4 — reject the striped roof, compare complete material ranges

Color and value first: the first fixed-patch render matches wood and cement
medians, but cedar lacks the photograph's dark-butts/light-faces range. The
initial roof has too little granular variation. A large full-house render
then exposes the opposite error in the first correction: too many narrow,
uniform, full-length dark stripes. That roof reads as a synthetic striped
sheet. Replaced it with broader, irregular gravity paths, reduced front-plane
granule-depletion contrast, and separated fine mineral variation from organic
algae. Strong algae remains on shaded planes; the sunlit face keeps shingle
color. The intermediate rejected view is retained locally in the render log.

The cedar comparison now uses an unobstructed lower-gable patch; the earlier
patch included foreground twigs. Measurements read native photo pixels rather
than a 1200-pixel reduction. The neutral and both coordinate frames are saved.
The updated-lap comparator is now a photograph explicitly catalogued as vinyl,
not an uncertain substrate inferred from the blue Cape. Auxiliary white/pale
gray paint controls and independent photographic exposure fits are explicit.

Expanded inspection to the family's concrete, trim, masonry and glazing.
The plinth comparison needs cloudy neutral light, rather than a hard blue
water-table shadow. The first brick crop incorrectly includes lettering and
the first glass crop includes a muntin: both are rejected as material-only
ROIs. The source brick is too orange for the aged chimney photograph; desaturate
its fired face toward the older brown-gray, retaining the mortar. The dark room
back still receives too much light, so deepen its value as well as its distance.

### Pass 5 — construction contact, manufacture bounds and glazing context

Color and value first: all five siding finishes, the asphalt, trim and brick
now meet the fixed-patch tolerances. The concrete crop initially included a
foreground dark post/well; replaced it with bare concrete. The glass crop now
excludes a muntin. These are material-only crops, with their native-resolution
coordinates, not dark fixture pixels counted as a material's low tail.

The glass comparison exposes a context bug: reflection scenery hidden from
transmission rays disappears behind the storm/sash interfaces and leaves an
implausibly uniform sky. Added original low leafy reflection proxies visible
through those optical paths. They are procedural modeled lighting cards, never
exported or baked into the glass. Their prescribed neighboring-crown radiance
is separate from the house material. The comparison uses stated diffuse
daylight and neutral camera balance; window values remain view-dependent.

Corrected periodic cedar partitioning so every complete unit really remains
3–10 inches wide, including units crossing the tile seam. The five courses
have staggered keyways and slightly uneven butts; manufacture metadata records
the actual generated widths. Storm oxide reduces metallic response rather
than merely lightening a metallic surface. Dormer window wear uses its own
block's sill/eave context, rather than the main wall's datums.

The threshold close-up also exposed an 18 mm unsupported gap below the metal
threshold. Raised the landing to its actual flat underside (10 mm below the
threshold top), retained equal safe rises, and added an independent upward
surface probe inside the threshold's rounded edge. Both front and rear stoops
use the corrected landing datum. Six proof roofs and building footprints keep
the accepted geometry; only the requested foundation/landing and connector
fixes, room depth and sparse age relief differ from the form checkpoint.

### Pass 6 — reject statistical success when the elevation fails

Color and value first: the first complete 1600-pixel round exposes a serious
cedar failure. Its patch passes the histogram tolerances, but nearly black
whole shingles alternate with pale units across the house. That is a
checkerboard, not the photographed wall. Rejected it. Restricted unit-to-unit
absorption variation and moved the dark range into each course's sheltered
upper end, below the next course's butt. Retained exposed lower faces and
exposure-driven brown-to-silver color. The revised elevation is visibly cedar
without the mosaic. Evidence: `renders/cape/lookdev/cedar-correction/` and
`correction2/` through `correction4/`. Its rejected material pair and measurements
remain in `renders/cape/lookdev/rejected-mosaic/`; they are not acceptance evidence.

The initial asphalt pair also compares a granule macro with many photographic
courses. Replaced the source ROI with a wide clear upper-roof strip, above the
dormers. A stronger continuous overlap shadow passes its histogram, but the
whole roof then reads as ribbed sheet material. Rejected that correction too.
Reuse the family's existing ranch roof atlas/addressing: three-tab on old roofs,
architectural on new ones. Confine exposed dark asphalt to fine granule-loss
paths inside the broader runoff field, with separate north-plane algae and low
moss. This adds no roof texture allocation. The accepted shared images remain
unchanged; the source atlas copy is generated in the Cape's ignored build folder.

Opened the hero, entry, scale, foundation, peeling sill, dormer, rake, rear,
first two seeds' front/rear/material views and seed 32's dedicated connector
view individually. The exposed plinth reads below the water table, the stoop
supports the threshold, and the connector has a visible slab, posts, beams,
rear waist wall and diagonal lattice. It no longer reads as a blank rectangle.
The following pass judges the regenerated complete set, not these superseded
frames. Fine cement texture, perfectly straight trim and sparse room contents
remain weaker than the photographs.

### Pass 7 — whole-sheet wear must retain its cause

Color and value first: the regenerated 36-view set and all ten material
comparisons pass their median, tail and hue checks. Nevertheless the bare
front roof of seed 33 reveals broad blotches, and the red wood house has
too even a low peeling band. Numerical success does not accept either pattern.
Stretch roof loss/algae masks much farther along the slope's runoff direction,
retaining irregular cross-slope paths. Reduce low peeling away from actual
stoop and downspout wet sites; preserve the sill-specific water damage.
The upper wall paint and every material's own color stay intact.

All 34 house views, both connector close-ups and the same-scale three-type
comparison were opened individually. Cedar/cement/wood/lap construction reads
at elevation size; the authored painted-cedar close-up is distinct as well.
The roof and low-course changes require another complete source/provenance
refresh before the acceptance images and final measurement table are reported.

### Pass 8 — current checkpoint, source evidence only

Color and value first: reopened the current hero, complete family/material/contact
sheets, detail images and ten neutral-balanced pairs. All ten fixed-ROI tests
pass: maximum absolute median error 9.29%, p10/p90 error 13.88%, and hue-ratio
error 7.61%. The README records every source/photo median and R:G:B pair.
The hero's silhouette Y′ is p1 .0934, p50 .3920, p95 .7261, p99 .7339;
no white clipping. Roof, shaded cheeks, entry and room backs retain deep values.
These are conditional display measurements; neutral paint controls and glass
reflection lighting are stated separately from the six proof palettes.

The bare roof now carries long irregular runoff paths. Granule loss stays
asphalt-colored; shaded-plane algae and lower-course/cheek moss remain separate.
Low red/white paint loss is strongest beside stoops and drains, with gray wood
and lifted surviving film at sills. It no longer makes the same white band
across every lower course. Cedar has narrow staggered keyways, sheltered upper
ends and exposed faces, without alternating black whole units. The large cement
courses, finer wood clapboard and smoother updated lap are distinguishable at
the family sheet's size.

Both 32/35 connectors are open passages with supported roofs, slab floors,
sided waist back walls and diagonal lattice. The hero, entry, foundation and
1.8 m scale view show an exposed concrete plinth below the sill trim. Actual
source exposure is 24/21/24/21/15/15 inches. Upward threshold-contact probes
have maximum numerical residual below 0.001 mm; the landing bears on the
threshold underside rather than leaving the previous gap. Basement openings
and wells, or the crawlspace's four louvered openings, remain real holes.

`make TYPE=cape WIDTH=1600 SAMPLES=48` finishes with 36 current Cycles house/type
camera views plus ten material renders, current source/map/recipe hashes, six
source/motion/import audits and the repeated construction bytes. Triangles are
35,092 / 42,016 / 34,518 / 40,768 / 39,602 / 43,330; the painted-cedar authored
control is 43,790. The family remains 47⅓ MiB delivered, with a planned +1 MiB
512-square cedar/cement triple. The reused roof source triple is byte-identical
to the ranch's. No existing export, shared delivery image or portfolio JPG changed.

Remaining CG tells: perfectly straight trim and large roof planes; very regular
grain/face striations at close range; a few obviously planar lifted paint flakes
and curled tabs; simple repeated curtains and sparse room dressing. Street glass
is much improved, but its reflection scenery remains a presentation proxy rather
than a complete neighborhood. The new fine wear has not yet survived a 4K
bake/filter or engine import, so this is not final game-asset acceptance. Stop
before the bake. No kit change or additional tool is needed for this checkpoint.


## Cape delivery — pass 1: reject fine-color aliasing and concealed sill wear

Color and value first. Inspected the first delivered-PBR hero, sill and
foundation in `renders/cape/finish/export-pass1/`, together with the ten
neutral-balanced source material crops. The concrete hue correction reaches
R:G:B .956:1:.985, versus .964:1:.989; the revised chimney is .370 versus
.377 Y-prime, with R:G:B 1.270:1:1.034 versus 1.222:1:1.047. These are
conditional display values, not albedos. Retain the stated casing neutrals.
The broad concrete statistical crop includes trim and a cast shadow; reject
it as a material-only ROI and restore the small bare-plinth measurement.
Use a separate wide construction view for form lines and plugs.

The first exported roof has broad polygonal patches: per-granule and per-tab
source noise evaluated at isolated vertices has aliased into macro color.
Reject that transfer. Evaluate fine manufacturing at its mean for vertex
baking and retain the actual shared roof tile's granules and unit variation.
Keep the long runoff, shaded algae and drainage-site moss as macro fields.
The exported sill has lost the fine source peeling. Surface inspection also
finds that the flat supporting sill block conceals its sloping weather face
and the lifted-film geometry. Lower the supporting block below that face,
then put long bare-gray patches and curled surviving film on the actual
nose and sash-joint surface. No floating paint rectangles are accepted.

## Cape delivery — pass 2: compare equivalent scales; reject seam overhead

Color and value first. The first corrected cedar retains the photograph's
median (.217 versus .214) but has much too little range: its 10th percentile
is 51% too high and its 90th is 40% too low. Reject this statistical result.
The new units need their own browner/grayer absorption and a few lighter
silver faces, with sheltered dark upper ends. Re-author that distribution,
without using photographic pixels as a material input. The cement comparison
now uses the used straight-butt striated photograph; the dimensioned 12 × 24
in replacement photograph separately establishes manufacture. Paint statistics
exclude the used photograph's localized lower biological deposit; the full
comparison retains that deposit and its course/joint construction.

Photographic derivative autocorrelation measures 2.941 wood courses,
7.944 vinyl courses and 6.211 aluminum courses in the fixed native crops.
Set the rendered crops to those same physical course counts before judging
shadow width/darkness. Move the paint samples clear of the window shadow.
The new geometry has 14 mm wood, 10.5 mm updated-lap and 4.37 mm cement
projection; independent surface rays will measure the delivered result.

The packed two-region wall atlas creates thousands of chart-cut triangles:
the first cedar export is 53,731 and remains 51,469 after cautious reduction.
Reject it. Split the already baked/filterered pixels into two 512 × 256
periodic triples. This keeps the same combined 1 MiB allocation and texel
density, avoids mixed cedar/cement deep mips, and removes the atlas seam
cuts without reducing construction or adding materials. Original colonial
and ranch images are unchanged. Foundation interval unions remove redundant
overlapping solids; the six actual source surface and motion sweeps still pass.

## Cape delivery — pass 3: reject scratches and open dormer corners

Color and value first. The source material suite now meets the stated median,
tail and hue limits, including the wider per-unit cedar distribution. Aluminum
passes after removing the cloud field: the exposed faces are evenly dulled,
window-corner runoff is cleaner, and dirt is trapped immediately under each lap.
The pale white aluminum comparison is a separately baked paint control; it does
not replace the accepted blue seed. The roof export no longer has aliased broad
polygonal blotches after transferring macro weather separately from granules.

Inspect the exported hero and the dormer, sill, plinth and chimney close-ups.
The sill still looks scratched: too many thin gray slivers, with angular white
chips. Widen the long water-site losses to 6–14 mm, roll the surviving film
across five smooth cross-sections, and retain bare gray grain underneath.
The dormer cheek tips are exposed at the front corners: the original corner
skip incorrectly treats the parent main block as an adjoining wall. Restore
the actual two-leg corner boards. Do not hide these defects by changing cameras.
The entry view proves the stoop but not the shallow foundation's construction;
add a dedicated low, wide plinth view for form seams and tie plugs. Remove
sub-70 mm rear aluminum casing bevels to fund the course dirt sampling within
45k; keep the front casing profiles and both door leaves. Keep the roof's
granule loss and omit the unconvincing isolated curled tabs, as authorized.

## Cape delivery — pass 4: inspect filtered detail, not only its statistics

Color and value first. On the fresh 5.2.3 export, nine material comparisons
pass. The aged roof median is .3641 versus .4050, just outside 10%; its low
and high tails pass. The source roof is .376. Retain the controlled roof
palette and the existing causal weather, apply the bounded chart-interpolation
contrast correction, and record a .02 EV comparison adjustment for both source
and export. The material controls and primary palettes remain explicit.
Reject trial maps with exaggerated tab values or coarse black stippling:
their manufactured pattern is less convincing, irrespective of histogram fit.
No trial map is published, and no image allocation is added.

The revised cement face now carries resolved striation, but its joints and
face nails are still too easily confused with the face grooves. Deepen the
joint's occlusion and nail-head contrast, keeping physical width, 4.37 mm butt
projection and half-unit stagger unchanged. In the exported sill close-up,
straight four-point gray losses still look cut with a knife. Replace them
with ragged eight-point grain-long losses. Curl three films per nine losses,
using compound curved film surfaces; the saved repeated films fund the richer
outlines without adding triangles. Check the water sites and grain direction
again against the used sill photograph. The dedicated plinth view shows a
vertical form seam and a tie plug; it also honestly exposes the remaining
low-resolution, smooth concrete response.

The full old-type rebuild has twelve byte-exact BIN payloads. The Blender
patch update changes only twelve exporter labels, six form-provenance hashes,
and one-byte samples in eight independently rebaked maps. Preserve the accepted
canonical files and record every difference in the rebuild audit. Historical
construction comparisons normalize only that exporter label, with the raw
hash retained; no changed geometry or material payload is ignored.


## Cape delivery — pass 5: final masonry, sill and bake loss

Color and value first. All ten freshly exported material pairs pass the
stated median (10%), p10/p90 (15%) and hue-ratio (10%) limits, after balancing
the photographs on their documented assumed neutrals. The delivered concrete
is .5322 versus .5456 Y-prime, R:G:B .964:1:.978 versus .964:1:.989;
brick is .3629 versus .3775, 1.253:1:1.034 versus 1.222:1:1.047.
The first extra concrete aggregate field was too contrasty in the wide
foundation view, resembling exposed stone. Halve that color modulation;
retain the original form seams, plugs, pores and low mineral/splash masks.
The corrected hero has a neutral gray plinth and restrained aggregate.

The final sill replaces the pass-4 trial with five twenty-point ragged,
grain-long bare losses and two compound-curved films per window. The actual
support-surface measurements put bare wood about .149 mm above the sloped
sill, and lifted film .111–1.991 mm above it. The nose and sash-joint losses
read as worn wood instead of scattered gray spots. The thin white film edges
catch light; repeated manufacture is still visible at extreme close range.
The old isolated roof boxes remain omitted.

Inspect all ten source/export image pairs. Absolute median bake changes
range from zero to .0152 Y-prime. The roof's .0146 median loss understates
its visible loss of fine granule contrast and the coarser vertex-interpolated
weather; retain that limitation explicitly. Cement striation, two face nails,
half-unit joints and 4.37 mm butts survive the filter. Cedar keeps per-unit
brown/gray absorption, splits and uneven butts; its grain is still more
regular than the photographic fibers. Shipping lower-face CV is .247,
compared with the limited nine-unit photographic CV .204.

Equal-course lap comparisons show wood shadow fractions .156 export / .167
photo, vinyl .125 / .211, aluminum .188 / .263. Dark/lit ratios are .559 / .689,
.723 / .798, and .934 / .682 respectively. Thus vinyl's shadow is narrower,
and aluminum's lighter than these photographs, despite actual measured
14 mm wood and 10.5 mm updated-lap projections. Record the illumination and
profile differences; do not claim a statistical paint match proves identical
shadow appearance. These profiles are measured at the same physical scale.

Constant dielectric shingle roughness channels free one third MiB for two
256-square Cape-only masonry color/normal pairs. The original 31 shared PNGs
remain byte exact. The whole family has 39 PNGs and stays at 48⅓ MiB, with
no extra masonry geometry. Final geometry is 36,383–44,716 triangles: the
added true lap surfaces and water-site paint construction spend the earlier
checkpoint's spare triangles while staying within the delivery's 30–45k.


## Cape delivery — pass 6: all six seeds and final studio views

Color and value first. Inspect all fifteen final Cycles views, the Eevee hero,
and all twenty-three seed views from the current exports. The hero's masked
Y-prime p1/median/p95 are .089/.372/.741, with no white clipping. Eaves,
entries, roof intersections and open connectors retain deep shade. Rear views
are deliberately shaded but still show the raised foundations and openings.
The main six palettes remain vinyl gray, brown/gray cedar, green cement,
blue aluminum, red clapboard and warm-white clapboard. The white paint
material comparisons are labeled controls, not replacements for those seeds.

On the six-seed front/rear sheet, cement courses and half-unit vertical joints
are visible; the close-up resolves striation and paired face nails. Cedar now
reads as separate units at street distance, with occasional irregular butts
and cuts, although its small periodic field remains apparent at close range.
Aluminum has exposed-face dulling, vertical washing at window sites and lap
dirt; there is no cloud-noise chalk field. Wood/vinyl carry real lap relief.
The sill close-up shows long gray wood losses at the nose and sash joint,
with thin lifted surviving paint. Concrete is still softer and more periodic
than a detailed photograph, especially on the wide stoop.

Dormer cheeks have complete corner boards and cast clear shadows onto the
parent roof. The eave/rake view shows their construction; entry includes the
stoop and exposed plinth, chimney includes irregular shallow masonry joints,
cap, flue tiles and supported rain cover. The 1.8 m scale figure has its feet
at grade. The 32/35 connector views retain open supported passages rather
than filled-in addition walls. No isolated curled roof-tab boxes remain.
Eevee preserves the form and shade but loses some Cycles reflection/interior
response in the glass; record that renderer difference.

All six exports have three meshes and five or six PBR materials. Actual
source/game surface displacement remains below 2 micrometers after chart
conversion and reduction. The raw-accessor and fresh-import checks report
zero position mismatch; this proves serialization separately from the
construction rays and 342 clearance poses. All 77 accepted older-type files
remain byte-identical. The full rebuild audit separately explains the
Blender patch's exporter-label and one-byte bake differences.


## Cape delivery — pass 7: fitted pairs and street composition

Color and value first. Inspect the two fitted export/photo comparisons and
their source renders, retaining the photographs' documented casing neutrals
and the six original paint choices. The primary roof is darker and its fine
granules less raised than the photograph; the material crop passes its stated
conditional value limits, which does not make the full roof photographic.
Large roof planes and periodic manufacture remain visible CG tells. The
photographic porch, additions and landscaping differ from the original asset;
the camera-fit residuals remain explicit rather than claiming a surveyed copy.

The street uses four different delivered Capes at sidewalk eye height, with
the nearest spanning 35.2% of frame width and the others receding. Lawn stays
in low bands around the sidewalk and lots; the camera looks along the road
and three-quarter to the fronts. Ground, RedMaple, PinOak, Shrubs and AlderC150
are loaded from their own immutable exports, with hashes checked before and
after rendering. Their geometry/maps are never re-exported or baked into a
house. The pickup bears on its delivered driveway instances. The lawn and
foliage retain a visibly procedural presentation character; these are reused
family assets, and this task makes no claim to improve them.

Inspect the supplemental crawlspace close-up as well as the poured-plinth
view: the former shows 8 × 16 in coursing through the parging and a louvered
vent, the latter form seams and tie plugs. Both retain cool-neutral concrete,
low deposits and splash dirt. The relief is intentionally shallow; the
256-square field's softness remains a close-view limitation. All required
views import delivered maps, with source renders used only for the separate
bake-loss comparisons. Five final Cape JPGs pass the current-source/map/camera provenance gates,
with the older ten docs unchanged. Whole-house mean absolute Y-prime bake
loss is .0107 / .0168 (dormered / plain), with p95 .0429 / .0650 on the
common opaque asset mask; ground/context pixels are excluded.


---

## Split-level form — pass 1: levels, foundation and first shared finishes

Evidence: `renders/split/pass1/{hero,entry,eave}.png` and all twelve
`renders/split/pass1/family/seeds/*/{front,rear}.png`, inspected together on
`renders/split/pass1/family.jpg`, beside the Pennsylvania side-split photos,
the western survey examples, the Connecticut July view and the Illinois
July 1964 street. This is a new form checkpoint, before any split bake.

**Color and value first.** The roof is below siding/trim value, the entry and
soffits have deep shade, and the poured plinth is neutral gray rather than
Cape's rejected tan. The red-brown brick retains a warm fired body; the buff
variant is too regular. White paint is authored at .53/.51/.45 on the hero,
not inferred from a JPEG. Quick common maps and source age are insufficient
for a final sixty-year surface. Reject any claim that their cleanliness is
accepted look-development. The reference whites have different white balances;
use their actual sash/casing neutrals before quantitative hue comparisons.

The living threshold, bedroom windows and lower garage/daylight windows give
three genuinely staggered heights. The living foundation is exposed below its
floor; it does not run siding nearly to grade. The integral garage needs a
real descending drive, a level apron and retaining cheeks; a buried door on a
flat lawn is unacceptable. The source includes all three. Two garage seeds,
two attached garages, a posted carport and side parking provide different
parking arrangements, not six garage recolors. The foyer is a single box with
the entrance between floors, rather than a two-story colonial entry.

Reject the first orthographic elevations: below-grade faces form a black
strip because the horizontal camera sees under the ground surface. Tilt the
orthographic rays slightly downward and cut the presentation ground at drives
and window wells. This changes presentation, not floor heights. Keep the
wide eaves and their boxed/vented undersides. The opening and cap profiles are
real geometry, with half-sash shutters only on ordinary hung windows.

## Split-level form — pass 2: roofs and working garage construction

Evidence: every main view and twelve seed portraits in `renders/split/pass2/`,
with entry, eave, veneer, rear, roof and side opened at full resolution.
The same-scale four-type image is `pass2/comparison/types.png`.

**Color and value first.** The refreshed ground hides the underground skins.
Roof, trim and deep recesses remain separated; the hero does not wash out.
The underside vent strip reads in the close-up. However the glass still has
simple sky and room backings, brick remains regularly manufactured, and
source age is too restrained at whole-house distance for final acceptance.
Do not fix those shortcomings by raising albedo. The source's muted colors
are deliberate variants of the photograph's red/green contemporary paint.

Reject the black wedge behind the tall wing in the rear. Analytic roof union
cut the living roof at the tall roof's projecting eave, leaving no roofing
under that skirt. Use a split-only wall-footprint occlusion boundary, retain
the living roof under the high eave, add roof/wall step flashing and probe the
lower roof separately there. The original top-down maximum-height roof audit
could not see that gap; extend it rather than exempting the location.

A clipped hip soffit also collapsed a miter in float storage. Dissolve its
sub-micrometer degenerate edges and redundant coincident caps before export;
never remove arbitrary triangles from a roof. Raw source/export counts must
agree after that correction. There is no change to any accepted type's path.

The first sectional-door sweep fails: a 40 mm foundation band enters the
bottom section, and the top panel enters the header. Lower the foundation
edge below the sill and recess the common stamped sections 180 mm behind the
frame. Solve each successive section's path from the preceding rigid chord,
so joints remain connected around the bend. The corrected four-section
mechanism clears every fixed solid and neighboring section over 41 samples,
without allowed-contact exemptions. The separate front/rear leaf sweeps also
pass. A serialized hinge alone would not prove any of this.

## Split-level form — pass 3: calibrated photographic comparisons

Evidence: `renders/split/matches-pass2/{split_side,split_foyer}-pair.jpg`, both
opened against their native PDF photographs. White upper sash stile is the
side neutral; white entry/screen-wall mullion is the foyer neutral. The
linear RGB gains are 1.0142/.9861/1.0000 and 1.0061/.9970/.9970, preserving
mean linear value and photographic exposure. ROIs and crop coordinates are
in `build/split/reference-preparation.json`. These are assumed whites, not
gray cards or inverse albedo measurements.

**Color and value first.** The photo's stained red wood and green metal roof
differ from our ochre boards and brown asphalt. Preserve that authored palette;
this is a form pair, not a completed material-value match. Our paint faces are
too smooth and the manufacture too regular. The foyer photo has richer window
curtains/reflections and much denser vegetation. Those are future look limits,
not proof that brighter paint would help.

The side pair supports the low living roof / higher bedroom roof / lower
recreation arrangement. The photo has three shorter bedroom units, an end
carport and original screening; our seed has two windows, a shallow later bay
and side parking. The roof is at the brief's 4:12–6:12 range; do not force it
into the photograph's much shallower contemporary roof. The bay's faceted
sashes, seat and knee brackets distinguish it from a pasted-on flat picture.
The living stoop is taller than that photograph, within the authored floor
range. Retain the exposed foundation and report the difference honestly.

The split-entry door lands between the lower daylight windows and upper
floor. Its small hood and attached side garage are different original choices
from the photograph's large glazed stair facade. The basic level relationship
reads, without pretending these are the same plan. Fits are approximate:
27.57 px RMS at a 25 mm lower lens bound for the side pair, 23.40 px at
56.43 mm for the foyer. The weak lens-bound side fit is explicitly a type
comparison, not a recovered survey camera. Independent Blender projection is
checked separately. The next refreshed gate must show the roof-skirt fix and
all current sources, not these superseded renders.

## Split-level form — pass 4: current form gate and construction closure

Evidence: every current main view in `renders/split/checkpoint/`, all twelve
seed front/rear images, `comparison/types.png`, `side-levels.jpg`, both
refreshed photographs in `renders/split/matches/`, and the half/open garage
views in `renders/split/motion/`. The contact, family and detail sheets were
opened again after the final rebuild. Provenance checks bind 25 required
Cycles views to their current source, metadata, maps and render recipe.

**Color and value first.** The same neutral-balanced photographs from pass 3
remain the comparison. Brick keeps its red/buff body, concrete stays neutral,
and the hero has dark soffit, window and garage recesses without clipping the
white trim. Display luminance percentiles are .125 / .509 / .715 / .722 at
p1 / p50 / p95 / p99; clipped-white fraction is zero. These are image-tone
observations, not inferred material albedos. The exposed painted faces and
regular brick still look cleaner and more uniform than the used photographs.
The low/shaded/drainage masks are a starting point: whole-frame age remains
too weak. Do not call the source finish accepted or solve it with a noise wash.

The five side-splits read from the street through living thresholds, lower
openings or descending garages, and bedroom windows half a story higher.
The foyer reads through its between-floor entry and low daylight windows.
The annotated side view labels authored floor datums, not surveyed surfaces.
The 4:12–6:12 masses, gable/hip combinations and parallel/perpendicular ridges
produce distinct low/high eave lines; the same-scale Cape/ranch/colonial view
confirms their type and scale. The three-quarter source remains more useful
than the side photographic fit, which still reaches its lower lens bound.

Wide boxed soffits, vent strips, friezes and rake hems survive the close-up.
The lower roofing now reaches the higher wall beneath its skirt. Pixel-ray
inspection of the remaining dark triangular junction hits roofing and step
flashing: it is shadow, not the rejected opening. Independent lower-roof probes
also pass. The plumbing vent was shifted clear of the adjoining eave and
chimney apron; its actual tip is about .400 m above the highest roof surface
below it on every proof seed.

The veneer cap and upper cantilever/material break are visible construction,
not paint stripes. Dogleg downpipes follow the recessed lower wall. Picture
units and the faceted bay occupy the living frontage without picture-window
shutters; ordinary shutters remain half-opening width. The double garage is
deliberately dominant on 51, while a single garage, attached garages, carport
and side parking vary that share across the family. The bay, taller entry
stoops and window counts differ from the photographic houses and are original
plan choices, not claimed matches. The carport remains open on posts, rather
than closing its negative space into a breezeway box.

Reject the first optional open-garage render's green strip: the review ground
crossed the sunken room. Cut the ground back inside the garage and retain a
simple concrete floor backing. The refreshed open view has a continuous
floor/apron. Lower the overhead track 50 mm so the handles and actual panel
bounds clear the authored ceiling plane by at least 15.3 mm. That last test
is explicitly against a plan plane; the separate collision test uses actual
tagged closed construction and neighboring sections. Neither claims complete
interior construction or continuous collision proof between sampled poses.

The final `make TYPE=split WIDTH=1440 SAMPLES=40` and standalone
`make TYPE=split check` pass. Evidence includes 4,000 plans across four types,
eleven split negative controls, six proof sources plus an authored override,
24,195 actual roof rays and 936 opening rays on the six source seeds, raw
GLB/import checks, repeat geometry/full GLB bytes and 506 sampled door/garage
poses. Roof error is below .005 mm; import position and pivot error are zero.
All eighteen pre-change raw GLBs/geometry digests match, and all 111 captured
accepted delivery/map/docs files keep their bytes. The source-context fallback
was also built and rendered without relying on previous deliveries.

No shared map or kit file changes. Existing 39 maps remain an estimated
48⅓ MiB with full mips under the documented block-compression assumption;
planned split addition is zero. Six-material sources span 31,460–38,384
triangles. Stop here: no split bake, final UV/density certification, exported
baked-look comparison, delivered game package or committed portfolio image.
The next gate must address visible age, repetitive manufacture and simple
glass/room backings before calling this a finished sixty-year-old house.

## Split source look development — pass 1: reject overstatement

Evidence: `renders/split/lookdev/pass1/` hero, back, entry, eave, veneer,
garage, tired-roof and drive close-ups, and all six front/rear portraits.
These are source Cycles views; no split bake has run.

**Color and value first.** Compared with the new Pennsylvania and Ohio used
builder photographs, the veneers have become too similar, pink and chalky.
The fieldstone is too bright and flat in the family sheet. Concrete is too
blue under the current daylight and must be checked against the accepted
Cape neutral recipe and an actual used-house patch. Reject these as calibrated
finishes. Restrict efflorescence to broken runoff/base sites, reduce its
coverage, and measure the complete body/mortar distribution before tuning.

Roof aging is visible at full frame but is now exaggerated: dark stripes on
sunny slopes read as a procedural overlay. Reduce granule-depletion amplitude,
preserve the material's own granules and courses, and keep the deepest algae
on shaded slopes. Do not replace the stripes with a whole-plane noise wash.
The source has proper dark rooms and clearer glazing, but needs more varied
visible curtain/blind response. The sunken drives have useful parked-car marks;
their new control-joint and edge deposits need a closer value/scale comparison.

The lower roof profiles and wider eaves improve the massing, especially 53.
The foyer lower sashes now read as room windows. The first trial kept its accepted floor
datums with a local grade at −.3048 m. Pass 2 replaces that trial with the
smaller −.1524 m adjustment and a .1524 m sill clearance. This is a declared site adjustment,
not an unreported change to accepted levels. The bay now has a folded hood,
angled sashes and stepped masonry corbels following the used bay photograph.

Four new camera fits are being evaluated. Corresponding facade corners fit
under 10 native pixels, but held-out entry locations expose major plan
differences in the first foyer candidates. Do not use a four-corner residual
to imply a complete house match. Search for better centered-entry photographs,
retain all diagnostics, and keep the accepted six plans rather than distorting
their widths or landing heights to chase an image.


## Split source look development — pass 2: scale and distributions

Evidence: `renders/split/lookdev/pass2/` hero/back and eight close-ups, all
six front/rear portraits; `values-pass4/` seventeen fixed surface pairs.

**Color and value first.** Reject the pink appearance of 52 in direct sun
even though its overcast redwood crop passes. Lower the coating's linear
albedo and use a red-brown rather than mauve body. Brick 51 needs a warmer
red/yellow balance; the Chicago mix lacks the photograph's near-black fired
units. Perlin interpolation between brick IDs suppressed those extremes: use
a deterministic independent kiln-tone assignment per brick. Retain neutral
mortar. Buff 55 is still 13% low in its photographed shaded appearance.

The fixed tests now include brick 56 and the drive balanced on sunlit
unpainted concrete, assumed neutral gray; the cream soffit and shaded vehicle
plate were rejected as unreliable whites. This assumption is disclosed: these
are appearance comparisons, not inverse albedo measurements. All patches use
first-hit material masks; none use displayed brightness to select pixels.

The horizontal aluminum photo has wide courses. Model 53 with eight-inch
exposure while preserving the same original shared map; halve its V scale and
keep the trapped lip dirt at its physical width. Compare its blue appearance
separately from the accepted Cape's white four-inch aluminum control. Match
physical patch spans to the photographed course counts rather than enlarging
a few clean brick faces. Stone still looks too like a smooth polygon diagram:
retain its deep joints but increase fine relief on the actual rock faces.

The roof no longer looks covered by black painted stripes. The driveway's
parked-engine mark, tire paths and joint cracks read at full frame, but its
calibration crop is too dark. Garage 51 needs a clearer replacement bottom
section and aged upper sections, rather than uniformly white stamped panels.
Its low road film remains localized to the seal. Glazing is clear in the hero,
but the small measured room patch is almost uniformly black: investigate the
reflection context without tinting the material or painting a reflection.

Form: 53's 3.5:12 hip is lower and the 24-inch bearing eaves read convincingly.
Foyer 55 uses grade −.1524 m, giving a four-foot lower-floor depth, six-inch
sill clearance and full 36-inch sashes. Move stoops, condenser, meter mounts
and splash blocks to that grade, and extend rail feet to actual tread tops.
The bay's masonry corbels alone cannot support a cantilevered frame: add
visible bolted steel wall plates and square-tube triangular knees beneath
the seat, with a three-plane folded sheet hood and its wall flashing.

Four true-type camera pairs fit corresponding facade features at
8.46/6.51/3.63/9.29 native pixels. Do not hide their held-out differences.
The first side pair's living width, the Ohio side pair's plan and the Ohio
foyer's garage/window arrangement differ from our protected original plans.
The Pennsylvania foyer's added gable also differs. Roof/eave recovery is
limited by foliage, frontal angles and missing ridge views; report those
limits instead of substituting authored numbers for photographic measurements.

## Split source look development — pass 3: reject diagrammatic stone

Evidence: first complete `lookdev/checkpoint` gate, including four clay/look
pairs, all seed portraits, veneers/siding and bay/lower-window details.
Historical copies of selected rejected views remain in `lookdev/pass3/`.

**Color and value first.** Sixteen of seventeen fixed tests pass. The vertical
red coating remains 15% low in its measured shaded median, with a 20% low
upper tail: correct that test's disclosed exposure without lightening the
actual street palette. The darker body coat prevents the first pale pink
appearance; it follows the used redwood photograph, rather than inventing a
pastel. The independent fired-unit assignment now gives 54 the required dark,
brown and buff mix. Keep its calibrated mortar and body distribution.

Reject the stone despite its passing median. At full frame it looks like a
polygon diagram, and the close-up shows smooth slabs outlined by an even
black line. Increase face cleavage and irregularity at actual rock scales,
vary the individual stone tones, and break the straight joints. Keep the
18 mm recess and original meter scale. Generate the periodic stone field
before packing it into its guarded chart so the chart boundary does not
introduce a manufactured seam. Keep the same two 512 maps and scalar ORM.

The new bay has actual angled side lights, a folded hipped hood, seat and
visible triangular bolted steel support. Its glass now shows room depth and
hood/sky reflection. The lower foyer sashes are full windows above local
soil, not slits. The original roof masses and all floor datums remain, with
53's lowered broad roof and wider eaves. The photo pairs still show protected
plan differences; the small camera fit errors do not erase them. Record
those, including the PA foyer's different added cross-gable and the Ohio
foyer's integral rather than attached parking.

Weaknesses carried into the last pass: regular mortar/course manufacture,
limited stone repeat, clean replacement trims and simplified curtain/room
backings. Peeling is correctly at old wet sill noses but is weaker at street
size than the driveway oil, bottom-seal dirt and roof algae. These images
are source look-dev evidence, not proof of how fine wear survives a bake.


## Split source look development — pass 4: actual surfaces over appearance

Evidence: `stone-pass4b/`, `common-pass4/`, `values-pass8/` focused pairs,
and the complete checkpoint's new `peeling.png`, hero, bay and foyer details.

**Color and value first.** The focused stone, red board and common-brick
rechecks pass the unchanged 10% median / 15% tail / 10% hue thresholds. The
common brick now varies continuously between fired tones rather than switching
three flat colors. Stone's measured physical scale is reduced to a 1.3716 m
repeat with twenty stones; its calibration patch spans 1.70 m, corresponding
to about 1.29 m in the central measured area. The photograph's apparent scale
is estimated from a nominal nine-foot garage opening, not a measured home.
The base color distribution is close, but reject the broad rounded bumps:
they read as molded pillows. Replace them with shallow intersected cleavage
planes and much smaller pores, within the same 512 color/normal pair.

The independent surface audit also contradicts pass 3's visual assumption
that every inherited paint loss sits correctly on its sill. The shared helper
was placing wood losses on brick rowlocks and the bay's different seat. Some
were buried beneath a flat supporting block and the storm-frame rail. Remove
the incompatible sites, lower the supporting block 16 mm beneath the sloped
weather surface, and give the helper that actual profile. Limit the retained
losses to exposed outer wood noses. The revised close-up shows thin cupped
film over grain-long gray wood, without floating slabs or scattered specks.
Actual tests now measure all 600 retained vertices: maximum surface distance
1.986 mm and minimum outward gap .079 mm; none float or lie buried. The
Cape's default geometry, attributes, shader inputs/links and referenced fields
remain exactly equal to the accepted version in the separate reuse witness.

Do not promote the camera numbers into a whole-house fit claim. Native
corresponding-feature RMS is 8.46 / 6.51 / 3.63 / 9.29 px; at 1100 px it is
12.74 / 10.77 / 6.65 / 14.60 px. Held-out native differences remain
60.51 / 41.10 / 12.51 / 44.22 px because protected living widths, parking,
window locations and the added PA foyer gable differ. The foyers' main ridges
and three physical soffit depths are not recovered by these frontal images.
Only the Ohio side photograph yields a usable bearing-eave estimate,
24.5 ±4 in. These are limits of the comparisons, not measurements to invent.


## Split source look development — pass 5: checkpoint before bake

Evidence: all 63 current Cycles views in `renders/split/lookdev/checkpoint/`,
with current source, metadata, map, recipe and rendered-PNG hashes. All views
were opened, including the complete front/rear, veneer, siding, clay/look and
material sheets, the sill and bay, and the scale/type-comparison views.

**Color and value first.** Seventeen fixed used-surface comparisons pass.
Maximum absolute median error is 8.24%, p10/p90 tail error 14.84%
and R/G or B/G ratio error 9.74%. The tired roof
upper tail is the closest to its limit; preserve that result as a pre-bake
measurement, not a guarantee of the next bake.

The table reports encoded Rec.709 Y-prime medians and median-channel R:G:B,
with G normalized to one. Photographic white balance preserves exposure;
render lighting/exposure and physical patch spans are disclosed in the JSON.
No rendered pixels are edited or selected by brightness. Source masks use
independent first-hit triangle/material IDs. These are appearance comparisons,
not inverse-rendered albedos. Aluminum white paint and glass are explicitly
unchanged Cape controls; the split's wide blue lap and street/bay glazing are
separate evidence. The blue photograph's substrate is unverified. The gray
concrete neutral is an assumption, not a measured gray card.

| Surface | Y source / photo | R:G:B source | R:G:B photo | Worst tail error | Photo neutral |
| --- | --- | --- | --- | ---: | --- |
| Red brick / 51 | 0.560 / 0.560 | 1.336:1:0.754 | 1.431:1:0.688 | 3.87% | white upper sash casing |
| Red-brown brick / 53 | 0.338 / 0.317 | 1.346:1:0.802 | 1.451:1:0.781 | 2.92% | white living-window casing |
| Common mix / 54 | 0.285 / 0.287 | 1.214:1:0.800 | 1.201:1:0.749 | 4.15% | white entry casing |
| Buff brick / 55 | 0.681 / 0.742 | 1.140:1:0.849 | 1.209:1:0.784 | 11.33% | white upper sash casing |
| Tan brick / 56 | 0.626 / 0.640 | 1.095:1:0.880 | 1.147:1:0.804 | 2.85% | unpainted sunlit concrete at the lower-left drive, assumed neutral gray |
| Fieldstone / 52 | 0.365 / 0.373 | 1.154:1:0.791 | 1.102:1:0.846 | 3.53% | white upper window bottom casing |
| Red wood battens / 52 | 0.248 / 0.253 | 2.118:1:1.020 | 2.101:1:1.096 | 7.41% | white upper sash stile |
| Blue wide lap / 53 | 0.324 / 0.336 | 0.800:1:1.188 | 0.832:1:1.212 | 12.44% | white upper window casing |
| Vinyl / 55 | 0.813 / 0.839 | 0.981:1:1.014 | 1.031:1:0.924 | 11.16% | white upper sash casing |
| Steel garage / 51 | 0.745 / 0.715 | 0.974:1:1.010 | 1.001:1:1.046 | 13.90% | white upper window casing |
| Tired charcoal / 51 | 0.174 / 0.181 | 0.911:1:1.089 | 0.986:1:1.166 | 14.84% | white living-window casing |
| Drive / 51 | 0.770 / 0.839 | 0.949:1:1.040 | 1.009:1:0.980 | 9.73% | unpainted sunlit concrete at the lower-left drive, assumed neutral gray |
| Wood lap / 51 | 0.651 / 0.630 | 0.964:1:1.018 | 1.031:1:0.969 | 1.48% | white-painted left door casing, in the same facade light |
| White aluminum / Cape control | 0.884 / 0.939 | 0.987:1:1.009 | 0.966:1:0.988 | 12.60% | white-painted right corner board in front-wall daylight |
| Concrete / 51 | 0.508 / 0.546 | 0.962:1:0.969 | 0.964:1:0.989 | 7.32% | white-painted window casing |
| Trim / 51 | 0.599 / 0.649 | 0.955:1:1.013 | 1.000:1:1.000 | 11.11% | white-painted door casing, same neutral used for wall paint |
| Glass / Cape control | 0.075 / 0.070 | 1.000:1:1.000 | 1.024:1:1.046 | 14.19% | white-painted door casing |

The hero's asset-mask Y-prime p1/median/p99 is
0.112/0.472/0.722, with 0% clipped-white pixels. Window
rooms retain deep values, with sky/eave and modeled neighboring-crown
reflections. The bay is clear rather than pale/frosted. Newer roof and vinyl
parts remain cleaner; old garage seals, engine/tire zones, shaded lower
roof/wall sites and water paths carry the strongest visible use. Fine sill
peeling and fascia overflow remain weaker at street size than oil/algae.

Stone now uses shallow intersected fracture planes, smaller pores and broken
edges; its joint scale and cap differ from modular brick. It still has a
detectable repeated cell vocabulary. Mortar and shingle manufacture are too
regular at close range, and interior backings/curtain folds remain simplified.
These are the clearest remaining CG tells. The causal fields preserve each
material's body color; no additional whole-wall chalk/noise wash was added.

Form remains the accepted six-house grammar. The taller lower foyer sashes,
reduced 53 roof, wide cornices, rowlock boundaries and supported shallow bay
read correctly. Their photo-pair limits are recorded in pass 4 and
`REFERENCE.md`; the unchanged original plans do not globally fit four
different real houses within ten pixels. Three soffit depths and both foyer
main pitches remain unmeasured because the necessary geometry is hidden.

`make TYPE=split WIDTH=1440 SAMPLES=40` and `make TYPE=split check` pass.
Proof comprises 4,000 plans, fourteen split negative controls, six source
seeds plus an authored override, 24,171 roof rays and 936 opening rays,
506 sampled door/garage poses, actual ground/rail/paint contact, raw GLB
import and repeat bytes. All eighteen previous construction payloads and all
111 protected existing files retain their bytes. The separate Cape-36 default
age/profile/surface witness matches exact geometry, every mesh attribute,
shader inputs/links and referenced field bytes. No kit files changed.

Source triangle counts for 51–56 are 34,036 / 32,926 / 33,228 / 33,756 /
33,064 / 37,242; every house uses six materials. Raw construction GLBs are
2.62–3.23 MB and are serialization proofs, not textured deliveries. Existing
39 shared maps remain 48⅓ MiB. The only planned addition is the 512 color/
normal fieldstone pair with packed brick coping: ⅔ MiB, hence a planned
49 MiB family allocation under BC7/BC5 plus full mips. Scalar roughness/metal
avoids an ORM map. No canonical shared map changed.

Stop here. No split bake, final UV/density or deep-mip certification,
textured-game export, exported-look comparison or portfolio image is claimed.
Thin film and the stone/coping chart must be judged after the eventual bake;
source Cycles does not prove their game-distance stability. No tools or kit
features are needed from the lead for this checkpoint.

## Split delivery — pass 1: reject aliased factory color

Color and value first. The first exported brick crops fail despite mostly
close medians: red 51 loses red chroma, and 54 loses the common brick's near
black fired units (p10 error +88.8%, p90 −23.2%). The stone median is 5.2%
low and passes. These are actual imported glTF patches with unchanged fixed
cameras, exposure and material-ID masks in `renders/split/delivery-pass1/`.
The fitted source measurements cannot stand in for export measurements.

The first hero, cap and peeling views were opened. Form, low garage and
wide soffits survive, but fine factory color has become broad vertex patches;
the drive's parked-car stains are also lost between coarse samples. Reject
this transfer. Put kiln variation into guarded texture regions within the
same planned pair, leave the older shared maps immutable, and add physical
samples at driveway and drainage wear sites. The thin sill film survives its
close-up, but needs stronger wet wood contrast at street size. Keep its actual
surface contact rather than enlarging flakes into floating geometry.

## Split delivery — pass 2: preserve manufacture without excess seams

Color and value first. Opened all seventeen exported material pairs and the
hero/eave/drive/sill sheet. Factory palettes in the first guarded two-axis
atlas restore distinct brick colors; sixteen rows improve, but common brick
still loses its dark tail. The blue lap's p10 and roof's p90 also miss. Reject
promoting these images on the strength of their medians. Restore the common
mix's fired spread and compensate the measured lap/roof filtering loss.

Two-axis atlas seams and indiscriminate wear cuts also exceed 45k. Replace
square brick regions by full-width color bands, retaining the existing Cape
brick normal at full density through standard texture transforms. Stone's
full-density normal is retained; its color occupies the lower half of the
same planned 512 pair. No older shared pixel changes and no added allocation.
Remove only redundant coplanar color samples within a stated residual bound.
The regular factory repeat remains an honest limitation.

The opened drive is too clean and its control-joint cracks disappear. Add
samples at the actual joint lips, retain the parked engine/tire sites and
restore their attenuated contrast. The sill's measured film stays attached;
darken its already exposed wet wood, and strengthen runoff only at real low
gutter outlets. These should be judged in the next whole-house and street
views, not asserted from the close-up. A source-to-game surface audit found a
4.6 mm folded-return change: freeze original tessellation before planar cuts.
A fresh six-seed surface audit must prove that repair.

## Split delivery — pass 3: retain the field, audit precision and placement

Color and value first. Sixteen fixed exported surface rows now pass. Opened
the full material sheet and roof-control contact. Red brick's lost chroma is
corrected in manufacture; the blue lap and common mix retain their colors.
The roof still misses its low tail by about two tenths of a percent. Do not
round that into a pass or change the accepted camera/EV. Uniform gain controls
show plateaus from dark normalized vertex colors and eight-bit display pixels;
they cannot restore the lost spread. Retain a bounded fraction of the source's
actual granule-loss field, and use the available COLOR_0 range by moving a
common uniform factor into the stock material. The latter must preserve the
physical color and be checked in the actual glTF, with no added map or material.

All six surface comparisons now measure less than 2 micrometers difference.
The earlier folded-return losses came from changing a nonplanar ngon's
triangulation: preserve its original tessellation before cuts, and retain those
folds through chart conversion. Actual moving-leaf and sectional sweeps pass;
serialization checks separately preserve pivots and sockets. All six exports
are below 45k. The three earlier types pass their checks; only exporter labels
and original-form file hashes drifted on rebuilding. Every other JSON value,
BIN, image and old docs byte matched, and accepted canonical files were restored.

The CPU-only street framing preview was opened to judge composition, not
materials. Four delivered seeds recede down a native ground-family street;
closest projected width is 35%, eye height 1.68 m over the actual sidewalk.
Add real exported curb cuts and tapered aprons, retaining the sunken drives'
open ground slots. This avoids an uninterrupted curb across driveways. Its
pavement dominates the foreground and the sky remains broad; the final Cycles
view must judge whether this reads as a street photograph. The fine sill losses
remain smaller than the roof and parking wear at this distance. Keep their
contact and localized water causes while strengthening their wet-wood contrast.

## Split delivery — pass 4: current export, full-frame wear and street rejection

Color and value first. All seventeen actual exported material rows pass with
the same source cameras, light and EV. Maximum median error is 8.24%, maximum
p10/p90 error 14.84%, and maximum hue-ratio error 9.74%. The roof's final fix
retains uniform .925 roughness, within .005 of the accepted .93 source, rather
than silently using the different shared ORM roughness. Its original shared
ORM bytes remain available for AO. The dark-color material/vertex factor
preserves physical color and improves quantization without another texture.

Opened the current hero, driveway, all required main views and the new street.
The living/bedroom/lower levels, sunken garage, driveway and complete ground
shadow read. Engine/tire zones and control-joint lips now survive at full
frame, although their finest cracks and oil breakup remain softer than the
source. Low gutter-end contrast and wet sill wood are stronger at their actual
causes; fine peeling still reads mainly in the close-up. Do not invent large
floating flakes to make subpixel film conspicuous. The white siding keeps its
body value, the garage replacement section remains distinct, and window rooms
remain dark with glass/eave reflections.

Reject the street's blue horizon: finite lawn ends expose the procedural sky's
lower hemisphere like water. Extend only the distant presentation lawn with
the already imported ground material. The native cut curbs, aprons, sidewalks,
road and open sunken-drive slots remain. The scene still has too much empty
background around four houses; add untouched back-lot maple/pin-oak instances
to break the line while retaining the front silhouettes. This changes only
presentation. Actual camera height is 1.68 m over the sidewalk and nearest
projected width is 35%. Re-render and inspect the final street before docs.

Fresh complete publication repeats all eighteen split glTF/BIN/metadata files
byte-for-byte. All 111 accepted older files also retain their bytes. Independent
whole-house source/export losses on common opaque asset pixels are .01347 /
.00965 / .00590 / .00583 mean absolute Y′ for the two sides and two foyers;
maximum per-view p95 is .04596. These statistics include filtering and coarse
weather interpolation; they do not certify a photographic look or full interiors.

## Split delivery — pass 5: inspect and retain the shipped set

Color and value first. Opened the final hero at full size, all six front/rear
portraits, all eleven veneer/siding close-ups, the entry/eave/cap/garage/bay
and wet-sill sheet, scale and both lifted garage poses, Eevee, all seventeen
material pairs and source/export pairs, all four whole-house photo pairs and
their source/export comparisons. All seventeen fixed material rows pass.
The hero's actual asset-mask Y′ p1/median/p99 is .10814/.46987/.72189, with
zero clipped-white pixels. The white siding stays below the highlights'
shoulder and the garage/room cavities stay dark. No pale material wash is
used to hide the softened fine color.

Opened the revised street at full size: the false water horizon is gone, and
additional exported mature maple/oak crowns break the back-lot line without
covering the stepped fronts. Four different exported houses, including the
foyer, recede behind the nearest side-split; native ground curbs, cut aprons,
sidewalks and road connect the drives. The pickup and shrubs remain untouched
exports. Measured eye height is 1.68 m over the sidewalk and nearest-house
width is 35% of the frame. The spare empty far lots, straight horizon, wide
pavement and repeated tree vocabulary still make this a procedural scene.
This is the presentation's weakest image, not proof of photoreal landscaping.

The roof's macro use, parked engine/tire sites and old garage bottom seals
read at full frame. Gutter-end runoff and wet wood are stronger only at their
existing physical causes. Fine peeling remains mainly a close-up effect; it
is subpixel in the street. Regular mortar, very orderly shingles, softened
stone color and simple dark room/curtain backings remain visible CG tells.
Do not misreport statistical agreement as the absence of those weaknesses.
The accepted six plans, levels, roofs and material families are retained.

The final complete make passes, including 47 current export views, seventeen
passing exported/photo material pairs, independent source/export masks and
measured tone. Fresh publication of all six seeds repeats all eighteen
glTF/BIN/metadata payloads exactly. Every seed uses six materials and
40,998–44,223 triangles; the whole family remains 49 MiB. Existing accepted
files are all byte-identical. Only these five final split JPGs enter docs;
no earlier-type image is replaced. No kit file changed.

## Split delivery — street framing correction

Color and value first. The accepted house/map colors, sun and sky are unchanged.
Opened the final street beside the registered real split-level street photograph
in `refs/split-midwest-summer.jpg`, using `renders/split/street/photo-pair.jpg`.
The 1964 photograph is monochrome and elevated: it informs roof/eave shadow,
setback and row rhythm, not hue, pedestrian camera calibration or an exposure
match. The exported image retains dark roof/cavity values and bright trim. Its
full-image Y′ p1/median/p99 is .01010/.54771/.86305; three clipped-white pixels
are .000305% of the image. The separate accepted hero-mask tonal check is
unchanged and passes.

The lead rejected the previous street as a horizon band. Its reported 35%
width included the driveway and did not measure the visible house. Retire that
framing claim from passes 4–5. The new fixed 35 mm full-frame camera stands on
the houses' own Sidewalk_A, at (-20, -7, 1.594948) m, measured 1.60 m above its
actual surface. It aims at (80, 11, 8) m with a 36 mm sensor; a 2.6:1 vertical
crop leaves the road at the right and the lawn in a low foreground band.

Opened the new full-size render and compressed docs JPG. The nearest side-split
occupies the left 34.3% of the frame in visible architecture, with the living
wing continuing beyond the left edge. Three other seeds recede behind it; the
foyer, carport, pickup and native curb/apron connections remain visible. Raw
unclipped building bounds and frame-clipped bounds are recorded separately,
with concrete driveway/retaining faces excluded. This is an intentional crop,
not a claim that the complete nearest house fits inside one third. No house,
context placement, mesh, map, material, sun or sky changed. The far horizon,
regular paving/lawn and repeated tree vocabulary remain procedural.

The new `docs/split-street.jpg` is 1600 × 615 and 141,670 bytes. It replaces the
previous image in the original portfolio commit, so only one street JPG blob
remains in this branch's history. All other accepted docs, delivered split
files and shared maps retain their bytes. All four types' make checks and
the repository/privacy checks pass again for this correction. No kit changes.

## LOD adoption — ranch immutable original, 2026-11-09

The LOD reference is the accepted delivery, not a new source look. Main was
merged before work (already current at `1c38664`). The tool/recipe freeze is
`build/lod-freeze-revision.txt` and `build/lod-freeze.sha256`. No kit code is
changed. `build/houses-lod/originals.json` protects all 136 existing house
delivery, image and docs files; no digest is refreshed during adoption.

To avoid publishing a newer exporter label over the accepted original, copied
the family scripts, generated inputs and maps to the ignored
`build/houses-lod/original-build/houses/`, with the current kit read-only.
Ran `make TYPE=ranch export -W src/ranch_sweep.py` there: exit 0, 81.13 s.
This freshly rebuilds the six procedural sources and deliveries. All six BINs
and metadata files match exactly. Each glTF differs only in its generator
label v5.2.40 to v5.2.41; after removing that single field its entire JSON
matches. The scratch build did not publish to the accepted directory. Counts and
geometry sizes match the existing six-seed README table. Full commands, hashes
and comparisons: `build/houses-lod/ranch-original-{build,comparison}.json`.

One representative chain is attempted for seed 12: the ranch is an unbounded
seeded generator, not six cosmetic copies with identical routing. Seed 12
includes the broad eave, picture glazing, chimney, garage, front/service leaves
and rear slider. No result is inferred for another seed or roof/material
choice. Source glTF SHA-256:
`0beefce72801255d7209147d098f0935fb414e1bdb84592c1c902227fcea237c`;
BIN: `af84399a8d1698badd2ac59b0772be75ef4dc5c41099e6e7a4a2af6c9f2f3b25`.
The LOD builder additionally freezes every canonical source-image dependency.

The first original-check attempt exposed a GNU make trap: `-o` is not inherited
by recursive make. The ranch check passed, but its recursive colonial check
began rebuilding/republication. Stopped it and restored all sixteen changed
original files from verified exact backups; the 136-file ledger then passed.
No digest was refreshed. `interrupted-original-check.json` lists those files.
The corrected command passes the same explicit frozen-input list through
`MAKE` as well as the outer invocation; its full argv is retained in the
original-check receipt. This is an interrupted validation, not a passing one.

The corrected `make TYPE=ranch check` returns 0 in 69.64 s, including the
recursive colonial check. Construction, motion, imported surfaces/frames,
shared maps and original delivery checks pass; the 136-file ledger is exact.

### Ranch fixed-region cost probe

The first public-tool trial requests .4/.15 at .30/.12 screen height, with
`preserve_uv_regions: true`, original materials and explicitly protected
`FrontDoor`, `PatioDoor`, `ServiceDoor`. Its serialized near counts are
53,990 / 53,926 of 55,228: savings only 2.24% / 2.36%, against the colonial's
55% / 25% ceilings (30,375 / 13,807). These are not adopted on count alone.

An ordinary-Python inventory of the original accessors, using the frozen
region classifier, measures all 10,618 geometric static-trim vertices fixed;
16,113 of 16,294 roof vertices fixed; and all 228 / 120 / 96 trim vertices
fixed in the three moving leaves. Counts are per material primitive and may
overlap physically. Normal-only splits do not create these regions. The roof
and trim retain 23,486 / 18,438 source triangles. Inventory:
`build/houses-lod/ranch-region-inventory.json`. This explains the cost of the
conservative domain policy; it does not establish a minimum over other tools
or approve removing the UV guard. Proxy bake and native review follow.

### Ranch LOD critique pass 1 — exported values and construction

Opened all nine native four-panel strips through unscaled raw-PNG pages
(`build/houses-lod/inspection/ranch/`), their original/preceding comparisons
and x6 differences, all four 960-square construction views and the contact.
Color/value first: the near brick, gray shingles, dark room backings and
green entry door match the immutable original under identical procedural
light; no photographic white balance is inferred. Neither near level gains
the colonial's dark window-to-wall streaks. Normal-map phase, gutter/drop
coverage, chimney/dish outline and the separate doors remain consistent.

The 1,800-triangle proxy blurs masonry and roof granules and has a dark
crease beside the entry hood in the elevated construction view. It is not
suited to that closer view. At 4.5% / 48.6 nominal pixels / 110.18 m, the
three native comparisons retain the roof/wall values, picture opening,
entry supports and broad footprint. Maximum reference mean/p95/local are
.012453/.053376/.078411; alpha/IoU maxima .016807/.018141. Every original
and adjacent gate passes at its default, with no phase exception.

`make lod LOD_CONFIG=src/lod-ranch.json LOD_THREADS=4` returns 0 (1,820 s
including two GPU queues). `make check-lod` with the same override returns
0 (19.32 s), including source charts/regions, normals, fresh re-import,
pivots/sockets, original hashes and image residency. These rest/data checks
are separate from the original family's sampled motion check and do not
establish engine performance. The trial remains unwired pending the cost
decision: its near mesh buffers are 4,967,832 / 4,961,820 bytes versus the
original's 4,892,352, for only 2.24% / 2.36% triangle savings. They retain
ten draws and allocate more geometry memory than LOD0.

The complete trial is preserved as `src/lod-ranch-trial.json`, wired to no
Make target. Its contents and payloads are unchanged by that filename move;
`build/houses-lod/ranch-trial-report/` was generated from the current passing
manifest without a failure waiver. This is a cost rejection, not a claim that
an unsafe cheaper mesh visibly failed or that these counts are minimal.

| Trial level | Triangles / target | Draws | Geometry bytes | Texture / mesh MiB | Switch |
| --- | ---: | ---: | ---: | ---: | --- |
| Original | 55,228 / — | 10 | 4,906,874 | 27.3337 / 4.6657 | near |
| Near | 53,990 / 30,375 | 10 | 4,981,701 | 27.3337 / 4.7377 | 30% / 16.53 m |
| Middle | 53,926 / 13,807 | 10 | 4,975,687 | 27.3337 / 4.7320 | 12% / 41.32 m |
| Proxy | 1,800 / 1,800 | 1 | 97,954 | 1.3334 / .0900 | 4.5% / 110.18 m |

Near goals both miss; the proxy goal meets. Original/near dependency PNGs are
7,277,844 bytes; the four 512-square proxy PNGs total 403,560. Stored costs:
164,944 triangles, seven canonical materials, 31 primitive placements,
22,643,620 distinct payload bytes and 42.8926 MiB, versus 31.9995 MiB for
LOD0 alone. Only one level draws: ten submissions near, one at the proxy.
No intermediate image is added. The two near buffers would cost 9.4697 MiB
for negligible benefit. The useful far replacement will be proved separately;
an engine must hold LOD0 while any door/slider differs from rest.

The scratch rebuild driver initially replaced the inherited GPU lock with a
worktree-local fallback. That affected only its first ignored material rebake;
the accepted maps were not published. Corrected it to retain the supplied
shared lock, and queued a fresh source/4096-map rebuild. The adoption bake and
all switch renders used the supplied shared lock. The recorded descriptor
audit confirms the corrected scratch wrapper uses that same lock; it has no
leftover own holder.

The original-check wrapper was also extended before Cape adoption: its legacy
check invokes `make` directly from Python, in addition to `$(MAKE)` recursion.
A local PATH wrapper appends the explicit `-o` list to both forms and logs
every full nested argv. Dry checks of the family check graph and a direct
nested ranch export return 0 with no publication scheduled. This changes no
Makefile or kit file. The wrapper, complete inputs, commands and dry output
remain in `build/houses-lod/`; the original 136 digests still match.

The corrected fresh source rebuild returns 0: `make TYPE=ranch export
-W src/ranch_sweep.py -W src/ranch_bake.py`, 1,676.95 s including the shared
GPU queue. All six BINs and all six metadata files match accepted bytes;
the six glTFs still differ only in the exporter label. The accepted 136-file
ledger remains exact. This complete run supersedes the initial scratch bake.

The sixteen fresh ranch PNGs have maximum independent channel drift 1/255
against the accepted maps, within the family's documented GPU repeat bound.
Per-map maximum and RMS code errors are in
`build/houses-lod/ranch-rebaked-maps.json`. All accepted source PNG hashes are
unchanged; the source-repeat variation is not baked into a replacement LOD0.

### Ranch LOD critique pass 2 — direct far switch and final adoption

The optional cost question received no answer during continued work. Proceeded
with the stated economical choice: omit the near buffers, retain LOD0 for
interaction, and prove the same far construction as the sole additional level.
This is a partial adoption of the requested four-level chain; the near targets
remain blocked by cost, not approved through an exception or lower image gate.

Fresh `make lod LOD_CONFIG=src/lod-ranch.json LOD_THREADS=4` returns 0 in
310.10 s; `make check-lod` with that override returns 0 in 4.21 s. Opened all
three fresh native source/new/preceding strips and differences through six
unscaled raw-PNG pages, both construction views and the contact. Color/value,
entry posts, window rhythm, hip outline and deep eave shading remain consistent
at 4.5%. The rear service/room highlights change slightly but do not become
large bright blocks. Masonry blur and the close-view hood/roof crease remain
visible weaknesses. No near-view equivalence is claimed for this shell.

The fresh proxy's position/normal/UV/index arrays match the earlier reviewed
proxy exactly. Three rebaked image hashes differ, so acceptance uses the fresh
images, not a file-identity claim. Native reference mean/p95/local maxima are
.012447/.053304/.078390, alpha/IoU .016807/.018141; all unchanged gates pass.
The final proxy is 1,800/1,800 triangles, one material/draw, 97,954 geometry
bytes and 403,132 PNG bytes (four 512-square maps). Its cold load is 501,086
bytes. Whole storage: 57,028 triangles, seven material resources, eleven
primitive placements and 12,685,804 distinct payload bytes; active draws are
ten or one. Resident cost is 33.4229 MiB versus 31.9995 MiB for LOD0: only
1.3334 MiB maps and .0900 MiB mesh are added. The two wasteful near meshes
are absent from this manifest and the Make hooks.

The post-build frozen `make TYPE=ranch check` returns 0 in 70.41 s, including
the recursive colonial check. All 136 original files and every literal kit/
recipe freeze entry match. Current evidence is
`renders/lod/ranch-12-proxy/`, `export/lod/ranch-12-proxy/`, and
`build/houses-lod/ranch-final-report/`; the original/trial receipts remain
alongside. The README table is generated from this final serialized manifest.

## LOD adoption — Cape Cod immutable original, 2026-11-09

Merged current main before this type (already current). Tool/recipe freeze:
`build/houses-lod/cape-freeze-revision.txt` and `cape-freeze.sha256`, revision
`d1c4f13`; the later ranch prose correction changes no tool bytes.
`make TYPE=cape export -W src/cape_sweep.py` in the same ignored original-build
copy returns 0 in 1,021.66 s, including the shared GPU queue. All twenty-one
glTF/BIN/metadata files for seeds 31–36 and the existing 34 paint control
match accepted bytes exactly. Counts and sizes match the original README.
The 136-file original ledger remains exact. Full receipt and per-file hashes:
`build/houses-lod/cape-original-{build,comparison}.json`.

The representative is seed 36, the accepted portfolio hero: its steep roof,
two front dormers, short eaves, entry hood and chimney test this generator's
distinctive construction. Front/service leaves are the source's two moving
roots; this seed has no garage. An unbounded generator is not a set of cosmetic
variants, so no chain is inferred for the other seeds, additions or sash/skin
choices. Immutable glTF SHA-256:
`1127ddc65eec070e7110a62fc57151916def0e3e6a8d66d1d30a47bc3701ef9e`;
BIN: `748b85fdfd534d260796b3c4c7b3dfa5dc3ef3b8d8a5ddf0527e35d65122294b`.
The builder additionally freezes every canonical image dependency.
The frozen original `make TYPE=cape check` returns 0 in 161.69 s, including
both older types, physical construction/motion, actual delivery surfaces,
UVs/normals, imported frames and canonical images. Nested direct/recursive
make arguments are recorded in `build/houses-lod/cape-nested-make.jsonl`;
the 136-file preservation check also passes.

### Cape near trial — raw failure before native comparisons

The full frozen-tool request produces 34,721 / 34,397 / 1,798 triangles,
against goals 20,010 / 9,095 / 1,800. Near levels keep original materials,
`preserve_uv_regions: true`, and separate front/service roots. The two near
mesh allocations are 3,603,078 / 3,575,502 bytes versus 3,231,894 original:
only 4.57% / 5.46% triangle savings, larger buffers and the same eight draws.
All 13,298 geometric static-trim vertices are region-fixed; the per-material
source inventory is `build/houses-lod/cape-region-inventory.json`.

The build/bake finishes, but `make lod` returns 2 after the comparison renderer
refuses `Imported LOD triangle/corner order changed` on LOD1. Opened the only
completed render, `renders/lod/cape-36/close-LOD0.png`; no near switch image
was produced, so no near visual pass is claimed. Color/value in that source
view retains the white lap, dark roof/rooms and red entry; it is the immutable
appearance reference, not a photo-white-balance measurement.

Full `check-lod` returns 2. Each near level has two new degenerate/sliver
triangles; Blender re-import drops nine triangles (34,712 / 34,388 imported).
The independent UV/normal field audit passes, which does not waive those raw
failures. The proxy separately re-imports all 1,798 triangles, with zero
open/nonmanifold/degenerate/sliver faces and positive volume on all sixteen
shells. It still needs its own native image proof.

Preserved `src/lod-cape-trial.json`, complete payload dependencies/hashes,
full checks, failed render log and simplification report before replacing
the active config. Evidence: `build/houses-lod/cape-trial-*` and
`export/lod/cape-36/`. The trial is wired to no target. No importer/shading,
topology or image check is disabled; no kit edit is attempted. These near
levels are blocked by both serialization/topology and cost. A separate direct
far configuration is being proved from the original, not from this trial.

The failed full chain would store 107,299 triangles, seven material resources,
25 primitive placements and 17,088,230 distinct payload bytes, with eight or
one active draws. Resident estimate: 35.689 MiB versus 27.416 MiB original;
1.333 MiB new proxy maps and 6.9394 MiB additional mesh buffers. Original/near
PNGs total 6,155,272 bytes per dependency set; the four 512-square proxy maps
total 384,900. Geometry bytes are 3,244,354 / 3,614,991 / 3,587,402 / 101,311.
These measured costs do not approve the failed near levels or the unreviewed
far appearance. Complete dimensions and resources remain in the saved manifest.

### Cape LOD critique pass 1 — reject the 4.5% proxy

Built the direct far-only config independently from immutable LOD0. Opened
all three native four-panel strips, source/new/preceding raw-PNG pages and
x6 differences, both construction views and contact. Color/value first:
the front windows/trim become brighter, the lap and shingles blur, and the
close view exposes pale triangular window fields. At the intended 48.6-pixel
height this changes the frontal appearance; it is not approved as mere loss
of subpixel granules. Coverage and the main gable/dormer silhouette pass.

The 1,798/1,800-triangle proxy meets its count and is one material/draw.
Front mean/p95/local are .034095/.133333/.117586; side
.023323/.101961/.096181. Both fail the unchanged .02/.08/.08 gates;
rear .015240/.054902/.039542 passes. Alpha/IoU maxima .025770/.027926 pass.
`check-lod` returns 2 solely for rendered differences; geometry, source bytes,
re-import, pivots and normal-map audit pass. There is no image-limit override.

Preserved the exact config as `src/lod-cape-proxy045-trial.json`, all payloads,
maps, manifest, raw checks, metrics and native images in
`build/houses-lod/cape-proxy045/` before tuning. The measured failed report is
`build/houses-lod/cape-proxy045-report/`, explicitly using `--allow-failed`
without updating the README. A 3% / 32.4-pixel switch is tested next with
the same triangle goal, 512 maps, shader policy and original image limits.

### Cape LOD critique pass 2 — farther switch does not fix color

Opened all three new 3% native strips and all six unscaled source/new/
preceding/difference pages, both close views and contact. Color/value first:
the front openings/trim remain too bright; the close view still has false
pale triangular window fields and blurred roof manufacture. At 32.4 nominal
pixels / 225.16 m, front mean/p95/local are .033532/.125490/.087503;
side .022318/.094966/.076320; rear .014211/.047059/.029571. Coverage
passes (maximum alpha .029686, IoU .033172). The front and side still fail
the original color gates. Moving farther alone has not solved the appearance.

The count is 1,800/1,800, one material/draw. The full check returns 2 only for
image differences; geometry, fresh import, fields and source bytes pass.
Archived the exact config as `src/lod-cape-proxy030-trial.json` and the
complete package/evidence under `build/houses-lod/cape-proxy030/`; the failed
measured report is alongside. No README table or Make hook is added.
The next control keeps 3% and changes only the public
`min_projected_coverage` option to .97, testing whether envelope merging
fills small window recesses. This is a geometry-control hypothesis, not a
claim that the cause has been isolated or permission to change any image gate.

### Cape LOD critique pass 3 — opening coverage is insufficient

Opened the .97-coverage control's three native strips, six raw-PNG inspection
pages, both construction views and contact. Color/value still fails at the
front window/trim fields; the close view retains false pale window triangles.
Front mean/p95/local are .033172/.133333/.089777; side
.022863/.097093/.084838; rear .013498/.043137/.028039. Coverage improves
slightly (maximum alpha .026345, IoU .029586), but that does not fix color.
The count remains 1,800/1,800 and the complete check returns 2 only for images.

Archived `src/lod-cape-coverage030-trial.json`, package, metrics, checks,
maps and raw/native images under `build/houses-lod/cape-coverage030/`.
Its failed measured report is `cape-coverage030-report/` alongside. No chain
is adopted and no limit changes. The last bounded trial moves to 2% / 21.6px,
keeps .97 coverage and uses a finer quarter-pixel grid with .15-pixel inflation.
It tests a smaller far silhouette with less envelope expansion; a failure
will end this type's attempt rather than authorize a general tool edit.

### Cape LOD critique pass 4 — final far rejection and hold

Opened every final 2% native strip, all six unscaled comparison/difference
pages, both construction views and the contact. Color/value remains wrong
at the front window/trim fields; the closer view also exposes dark triangular
dormer-apex artifacts, coarse steps and lost roof/lap detail. At 21.6 nominal
pixels / 337.75 m, front mean/p95/local are .029275/.118235/.055592;
side .019967/.082353/.047376; rear .011807/.039216/.024422. Alpha/IoU
maxima .015886/.018900 pass. Front color still fails strongly, and side p95
still exceeds .08; no tolerance is relaxed for the smaller excess.

The final full check returns 2 only for images; topology, normals, re-import,
pivots and immutable inputs pass. The 1,800/1,800-triangle shell has one
material/draw, 100,041 geometry bytes and four 512-square PNGs / 414,704 bytes,
514,745 cold-load bytes altogether. This rejected two-level package would
store 38,183 triangles, seven material resources and nine placements, with
28.8414 MiB resident versus the original's 27.4158 MiB. No intermediate
image is added. Its saved recipe is `src/lod-cape-proxy020-trial.json`;
current payload/native evidence is `export/lod/cape-36-proxy/` and
`renders/lod/cape-36-proxy/`, with measured failed tables/contact in
`build/houses-lod/cape-final-failed-report/`.

No passing proxy was found at 4.5%, 3% or 2%, including the opening/finer-grid
controls. Both near levels are raw failures and poor cost reductions, so
ending at LOD2 would also be invalid. Cape stays LOD0-only. All rejected
configs remain unwired; the README gets three plain lines and no failed
tables. General near serialization and far appearance fixes are deferred,
as required by this adoption scope. The post-build original check follows.

The post-build frozen `make TYPE=cape check` returns 0 in 172.83 s, including
both older types. All 136 accepted files and all literal Cape tool/recipe
freeze entries match. `repo_check.py` and `git diff --check` pass. There is no
Cape LOD hook or active `lod-cape.json`; only explicitly named rejected trials
remain in `src/`. Default family LOD hooks still select adopted chains only.

## LOD adoption — split-level immutable original, 2026-11-09

Merged `main` before starting this type: merge `6ae1ac0` adds an unrelated
Blender-command helper/test and its README paragraph; no existing LOD source
changed. All prior literal freeze entries still match. A fresh split freeze
is `build/houses-lod/split-freeze.sha256`, revision recorded alongside it.

Rebuilt all six originals in the isolated scratch mirror using
`make TYPE=split export -W src/split_sweep.py`: exit 0 in 116.15 s.
All 18 glTF/BIN/metadata files are byte-identical to accepted deliveries.
The exporter repeats its existing tangent warning on static geometry;
it changes no delivery bytes. The immutable ledger still matches all 136
accepted files. Comparison and command receipts are
`build/houses-lod/split-original-{build,comparison}.json`.

Representative seed 51 is the accepted core side-split: stepped roof,
sunken integral two-car garage, both entry doors and all four sectional
garage panels. Those six moving nodes are held in near reductions. A rest
proxy must hold LOD0 whenever any door/panel moves. This proof makes no
claim for the other five seeds' foyer, carport or bay configurations.

The original `make TYPE=split check` with generated inputs frozen through
every recursive/direct make returns 0 in 124.06 s. Phony mesh, motion,
delivery and older-type checks execute; only rebuilding accepted deliveries
is suppressed. Its archived precheck is `split-pre-original-check.{json,log}`.
The first bounded trial keeps UV regions and original materials near, and
uses the colonial's default 4.5% one-draw far recipe without limit changes.
