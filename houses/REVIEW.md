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
