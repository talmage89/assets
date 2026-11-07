# Form checkpoint review

These are construction critiques, before look-dev. No photograph is an asset
input. All camera fits use the kit tool and independent Blender projection
verification; the reference-neutral copies and pairs stay ignored. Concrete
patch coordinates and RGB gains are in `src/photo_matches.py` and the generated
`build/photo-balance.json`. Aggregate color and mixed light limit these neutral
assumptions. No photographic value is claimed as recovered albedo.

## Pass 1 — first mesh and period photographs

Color/value: Workbench was suitable for silhouette only; its dark grip and
uniform alloy were not finish evidence. Compare the 2010 sunlit used board,
2006 side view, 2008 mini close-up and 2005 loose truck, not a remembered toy.
The first 21,814-triangle board failed budget. The end caps were visibly angular,
the bolt seats puckered the grip, and separate rounded tower/wing seeds read
as lumps around a straight axle bar. The wheels were too spherical, with too
little flat side face around the bearing.

Changes: elliptical end-cap stations cluster near tips; a welded continuous
seven-ply shell replaces stacked buried faces; sharp countersink boundaries
stop the normal puckering. The baseplate is a flared loft fused with a bored
pivot boss; the hanger is a swept compound wing fused to its barrel, ring and
pivot arm. Hidden race/washer surfaces were reduced. The initial inspected
Workbench renders are archived under `build/skateboard-history/` after the
clean rebuild (root of the worktree).

## Pass 2 — exported geometry, matched framing, section

Color/value: preliminary Workbench pairs cannot evaluate sunlit metal or the
wheels' yellow staining. Concrete was selected as neutral before comparisons.
Kit fits against three complete boards give framing evidence; the mini is a
different deck size and wheel color. Residuals retain those differences.

Form: the first simple cylinder kingpin hole let the bushings disappear into
the casting instead of bearing on a seat. The pedestal also crowded the pivot
arm. The near-spherical wheel shoulder was especially obvious beside the
2010 used wheels and 2008 mini.

Changes: broad wheel side faces, tighter rounded shoulders, 15 mm riding band;
properly recessed bearing shields; measured 608 outer/bore/width class.
The real six-sided bolt drives use authored rings instead of boolean slivers.
A triangle-plane cut through the imported deck shows the concave and seven
veneer layers. The inspection cap derives its upper/lower limits from actual
mesh ray hits, not a replacement ideal curve.

## Pass 3 — first Cycles set and mechanical rejection

Color/value first: the original sky fill washed the concrete and turned the
black grip slate blue. It also made the alloy look chrome-plated. Reducing
sky fill kept the raking sun's deep cavities, but made the next hero too dark.
Exposure was then raised without raising shadow fill. The quick alloy was
roughened; its finish is still unapproved.

Construction: the initial kingpin direction was wrong. Correcting it exposed
an axle/kingpin clash. The initial 50° virtual-axis estimate was abandoned.
The corrected cast pedestal, pivot cup and bushing-seat positions define an
actual 35.94° hanger axis. This is original geometry, not a manufacturer angle
claim. The kingpin inclines 20° from vertical toward its axle; the two axes
are distinct. Broad flared counterbores leave an annular bushing seat and
clear the fixed kingpin, nut and washers. A tapered cast arm replaces the
long uniform pivot rod. The measured rigid-metal failures were fixed rather
than added to an allow-list. Only bushing compliance and the retained rubber
pivot interface remain exceptions.

The first reduced yoke had four coincident unjoined edges. Welding those and
removing degenerate edges restored a closed solid. Dense casting normals now
transfer to the reduced castings; the retained high source includes the same
machined bores and seats. Dense/game triangle-plane sections expose all three
stations in each casting, so a bevelled side extrusion cannot pass unnoticed.

## Pass 4 — veneer, hardware and all seeds

Color/value: seven equal alternating dark/light stripes overstated the plywood.
The quick layers now distinguish the two cross bands from five long-grain plies;
grain, glue, filed grit and surface response remain for look-dev.

Construction review against Roarockit's published 1/16 inch stock caught the
original 7 mm deck gauge. It is now 10.5 mm pressed/sanded maple plus 0.55 mm
grip, with L/L/C/L/C/L/L layup. Press compression/sanding to this finished gauge
is an estimate. Mounting hardware now has 3/8 inch wrench flats and one-inch
countersunk bolts. Four machined nut lands remove actual nut/pedestal overlap;
those static contacts are checked separately from moving-root tests.

The 7.75, 8, 8.25 and 8.5 inch seeds use matching axle widths; the widest gets
1/8 inch risers. The riser supports are measured as deck → pad → plate rather
than incorrectly requiring the plate to touch the deck through its pad.
The coordinated motion uses front +angle / rear −angle: the two axles steer
oppositely under a shared deck lean, rather than twisting their banks apart.

## Remaining look gate

The silhouette and physical assembly are the only approval requested by this
checkpoint. Temporary material factors, unchamfered tiny nuts, planar 28-sided
wheel silhouettes in macro views, small residual low-poly casting shading and
the approximate mini camera fit are visible limitations. Fine bevels, grit,
cast grain, machining, graphics, foot dirt, scrape-through, chips/delamination,
razor-tail geometry, coning and the three age states are not delivered yet.
No UV packing, texture bake, one-material consolidation or final docs image
is claimed. No existing asset or toolkit file was changed.

## Pass 5 — full-size checkpoint audit, then stop

Color/value: the final hero's display-referred full-frame luma percentiles
p1/p5/p50/p95/p99 are **39.88 / 47.09 / 148.59 / 153.73 / 154.73** (byte scale,
concrete included). No pixels have all channels ≥250; under-deck/bolt cavities
reach near black. These are image values, not albedos. The sun/sky balance now
keeps the grip dark and the cast shadow distinct without a pale concrete field.
The 2010 pair uses hard sun, the 2008 close-up hard sun and the 2006 side view
a camera-position flash; their reference concrete is neutral-balanced first.

Full-size inspection rejected the dense-normal transfer: nearest-face changes
made sharp reflection streaks around the yoke and pedestal. It was removed.
Welded game geometry now uses sharper machined boundaries and area-weighted
normals; this removes the streaks while retaining visible low-poly facets.
Those remaining facets are a real macro limitation, not proof of photorealism.
All requested Cycles views, both truck angles, the three complete-board pairs,
wall rest and alternate-seed images were opened after the correction.

The deck measures **203.200 × 815.975 mm**, with **11.050 mm** maple-plus-grip
center thickness and **7.471 mm** rise measured 1 mm inside the rail. Measured
straight-kick ray gauges give **17.954° nose / 18.000° tail**. The actual bushing
web measures **7.800 / 7.801 mm**. All four through bores per truck are open;
the one-inch bolt tips pass their nylon inserts. Static nut/pedestal overlap
was removed at four machined bearing lands per plate and independently checked.

Final source/game clearance checks pass: 25 samples per hanger (±12° in 1°
steps), 25 spin samples per wheel (0…360° in 15° steps), no rigid-metal
exceptions, and **18.890 mm** minimum sampled wheel-vertex/deck distance.
The surface-derived wall socket seats the actual tail on the floor and the
front wheels on the wall: minimum Z **0.000093 mm**, minimum Y **−0.000004 mm**.
Its target contact height is **595.542 mm**. These are triangle/vertex-surface
measurements, separate from fresh-import preservation.

The default is **11,662 triangles**, **397,852 GLB bytes**, **16 temporary factor
materials**, **95 inspection meshes**, **zero images**. Alternative 7.75/8.25/
8.5 inch seeds pass at **11,602 / 11,582 / 11,940 triangles**; widest seed includes
the risers. Clean `make` passed. `make variant-renders` passed all three geometry
checks and rendered the alternatives. `make repeat` produced exact matching GLB
SHA-256 **0abcb924767553a6d74e36e3184beb4da1196fd1fb888de19f3134124477d4a7**.
Repository check passed with zero errors. No kit or existing delivery changed.

Camera-fit RMS is **14.369 px** on the 1285 px horizontal crop, **22.602 px** on
the 3072 px used-board crop and **76.808 px** on the 2550 px mini crop. Independent
Blender projection disagreement is below **0.002 px**. The mini's nose/size is
not our full street shape: that pair judges its casting and wheel profile only.
The fitted lenses are estimates, including the mini, not recovered EXIF.

Local review paths: `renders/checkpoint/contact.jpg`, `matched-pairs.jpg`,
`cast-sections.jpg`, `steering.jpg`, `rest_wall.png`; alternate heroes under
`renders/seeds/`. All are ignored, rebuilt outputs. No final `docs/` image is
committed. Stop here: surface aging, original marks, normal-map detail, bake,
atlas and delivery consolidation remain the next gate.

## Form correction / pass 6 — rounded press and visible construction

Color and value: these comparison renders still use the accepted quick palette.
They judge silhouette, rail section and hardware exposure. The pale ivory wheels
and untextured black grip are not a look approval. Concrete in the photographs
is the neutral assumption; the loose 2005 truck uses its zinc cup washer.

The lead correctly rejected the straight knees, five-chord concave, square rail,
faceted outlines and wheel rims, blobby yoke and hidden bushing stack. The new
press integrates a smooth slope over an 80 mm transition, with slight continuing
curvature in the kick. On `period-horizontal.jpg`, the visible rear transition
occupies roughly X=980…1100 of a roughly 1210 px deck span: normalized to this
815.975 mm class, about 81 mm. Perspective, concave and unknown photographic
board dimensions limit this to roughly ±20 mm; it is not a recovered mold.
The authored minimum transition radius is about 164 mm (6.45 in), rather than
a hinge between two planes. Mesh rays independently measure the kick slope.

The transverse curve is flatter in the center and rises progressively at the
rails. The full 5.25 mm half-gauge roundover carries all seven veneer bands;
there are no square veneer strips or buried stacked faces. Actual imported-mesh
sections at Y=0, −200 and −320 mm are rendered with ray-derived inspection caps.
The end contour has 64 arc samples; wheels have 64 radial sides. Mounting drive
recesses move into the bake source, while the actual eight bores/countersinks
remain. Entirely buried spacer bodies and bearing backs are omitted.

A narrower, drafted annular hanger seat opens the bushing view; cup washers
have raised lips. The baseplate now has side pockets and raised ribs beside the
kingpin pedestal. Dense original voxel-fused sculpted sources retain all bores.
The game castings still show reduction shading in quick-material macro views;
their dense normal bake must be judged separately. The bearing shield starts
outside the steel inner race, exposing a narrow race beside the nut flats.

An actual modeling failure was caught before look-dev: Exact Boolean inverted
the new curved deck shell and added cutter-shaped protrusions. The asset uses
Manifold for those machined cuts. Positive volume, all eight open-hole rays,
closed structural topology, actual bushing support and sampled metal clearance
are independently checked. No generic kit Boolean behavior was changed.

Same-camera native-resolution comparisons are rebuilt in
`renders/form-fixes/`: `side-before-after.jpg`, `hero-before-after.jpg`,
`tail_plies-before-after.jpg`, `truck-before-after.jpg`,
`truck_inner-before-after.jpg`, `wheel_bearing-before-after.jpg`, and the three
`section_*-before-after.jpg` panels. Each panel is 1440 px wide; these are local
review images, not final docs. The preceding checkpoint is reconstructed from
its tracked scripts at `8cc0710`, without another checkout or worktree.

## Look pass 1 — first baked GLB, rejected macro response

Color and value first: the new grip stays black at full frame and the fictional
teal/orange print retains its dark ink. New urethane is a warm cream, not white.
The exposed wood in the initial scrape source was too orange beside the
neutral-balanced 2010 used board; its scratch substrate was shifted to lighter
maple tan before the used-state review. These are material decisions, not a
claim to recover albedo from a photograph.

Opened all six 1200 px images in `renders/look-pass1/new/`, rendered from
`build/new/pass1.glb` with the first baked maps. The bottom print is readable,
but the truck has broken reflection patches at the washer/bushing interfaces.
The bearing and wheel lettering blur in the macro, and the eight flat bolt
heads lose their normal-only drive recesses. The first grip has useful broad
value but reads too fine/smooth in macro. Clean/new is not an excuse for these
projection and density defects.

Corrections: per-part temporary projection owners prevent high rays crossing
small adjacent washer/bushing/deck gaps. Those helpers are removed by final
assembly consolidation; they are not additional engine controls or draw calls.
Bolt heads, bearing faces and wheel prints receive more atlas area. The source
keeps their hex drives and 64-sided axles; tiny manufacturing detail remains in
normal maps. Source UV overlap is corrected through narrower projections and
convex island packing, rather than accepting an overlap tolerance failure.

The full-size crop of the 2010 truck also rejects the remaining rod-like pivot
bridge. A continuous compound triangular outer web now connects the axle
housing to the pivot nose, while the annular bushing seat remains behind it.
This is a new sculpted loft/union, not a side-profile extrusion. The casting
still needs a same-light source/export comparison after this change.

## Look pass 2 — full three-state bake, material and photo-light rejection

Color and value first: neutral concrete in the 2006 flash photograph makes the
rendered grip visibly too dark, including its shoe patches. The 2010 used
board's exposed maple is lighter than the first warm scrape substrate. In the
2005 loose-truck pair the rendered alloy is overexposed against the neutral
zinc washer; that cannot be excused as silver metal. The full-frame sun heroes
retain deep under-deck shadow, but old urethane is too uniform and mustard.

Opened all eight views for each of the three ages in the preserved
`build/look-pass2/renders/`, plus the three photographic comparisons. The real
hex mouths now survive the bake, and the annular bushing stack is visible. The
belly-slide loss is visible at full frame and has the right contact direction,
but repeated narrow scratches still look authored. The rail grain, wheel
lettering and smallest grip grains soften in the single 2048 atlas. Beat's
lifted veneers read as simple flakes in macro rather than torn fibers.

Rejected the bright, crumpled-foil grind normals and pillow-shaped outer web.
The third pass makes the web thin with drafted broad faces and rounded corners,
reduces grind relief, increases alloy roughness and puts grime into cavities.
The four visible axle stubs replace buried steel, gain UV priority and carry
stronger thread relief. A blue coated bearing shield and its two stamped rings
separate it from the steel inner race. More localized wheel shoulder dirt and
bearing grease break up the old urethane; torn rail losses are deeper.

The loose-truck GLB presentation also clipped the fixed baseplate because its
inverted transform had not updated before selection. This is a render bug,
not missing exported geometry. The third pass isolates connected imported
surfaces in root space, preserving their split normals, and seats the actual
visible truck on a procedural wooden table. Source and GLB use the same indoor
area light and exposure. This comparison remains a class/form/light estimate:
the photograph has no recovered real-world truck measurements or calibrated
photometry. Its full-size camera fit is 13.65 px RMS on the 600 px photograph.

## Look pass 3 — improved bearing/threads, rejected boss slivers

Color and value first: the neutral-balanced flash comparison is closer in grip
value after raising the grit source and exposure. The warm indoor truck pair
now has a warm bounce and visible alloy highlights rather than a white void.
Old wheel shoulders are darker than their faces, with local bore grease; they
still lack the strongly oxidized brown road band in the 2010 photograph.

Opened all 24 state images at their native 1440 px width, all three GLB/photo
pairs, and their three dense-source equivalents. Threads now resolve on the
actual steel stubs, the blue coated shield separates from the inner race, and
both amber bushings/cup washers are exposed. The thinner drafted outer web
holds its broad triangular face. The source has finer grit, casting scratches,
wood fibers and type than the atlas: these are real bake losses in macro.
The full-size loose truck replaces the rejected miniature; a crop of the
constrained 2010 full board provides the complete truck/wheel comparison.

Rejected a construction defect exposed by the new loose-truck camera: vertex
flattening around each nut land stretched the baseplate boss into thin slivers.
They exist in the dense source and become black tears in the normal bake.
Neither the motion checks nor serialization caught that appearance defect.
The next correction replaces that deformation with actual cylindrical
machining cuts, keeping the same 6 mm mounting bearing plane. Earlier pass
images and GLBs are retained locally under `build/look-pass3/`.

Remaining CG tells: scrape islands share a too-consistent substrate color,
the rail's smallest wood fibers blur, extremely close grip resembles a rough
sheet rather than individually resolved carbide grains, and the beat veneer
flakes remain simple. These are not hidden by the numerical gates.

## Look pass 4 — machined lands, final atlas and tone audit

Color and value first: concrete remains the neutral in both used-board photos;
the loose truck uses the zinc washer. On the horizontal crop, front-grip
patch (200,70)…(280,105) measures median RGB 35/35/36 in the balanced photo
and 42/42/40 in the render. Rear-grip patch (850,65)…(930,100) is 41/37/39
versus 43/43/41. These display values include estimated flash/ambient light,
not recovered material albedo. Neutralizing the flash fill removes the earlier
blue grip. The sun heroes retain black cavities and dark ink. The upside-down
heroes use the same lower exposure across all three ages: a first tone audit
found 96 white-clipped pixels on beat's small tail/glue glints; the correction
leaves 8 (about 0.0006% of the frame), still an honest minor limitation.
New/season underside p1/p99 luma is 15.75/150.35 and 15.73/143.38; beat is
15.66/151.52. Top-side hero p1 is 36.58…37.44 and p99 154.80…154.95, with no
white-clipped pixels. Full-frame values include concrete and are not albedos.

The real cylindrical nut-land cuts remove the source's stretched strips and
the baked black tears. The final loose truck comparison shows the same clean
boss, thin drafted web and open bushing stack in source and export. The small
notches beside the boss are now actual machined wrench clearances. Independent
construction and dense-source sweeps pass with no rigid-metal exceptions.
The final panels preserve 1440 pixels per before/after image, including the
kit's outer margins; the three-station sheet also retains 1440 per section.
The 1140 px truck/wheel crops preserve the full-board camera and source pixels.

Reviewed the final exported new, season and beat heroes, tail, both truck
angles, wheel/bearing and grip views at full size, plus the source/export photo
pairs and the correction panels. New has satin ivory urethane, fresh black grit
and clear-coated ink. Season/beat retain distinct belly loss, foot dirt/polish,
tail dragging/chips and brighter hanger contact faces at full frame. Coning
preserves ground contact. Beat includes the compressed razor tail, two attached
veneer flakes, torn nose grip and ribbed repair. The three original graphic
panels are distinct and legible; only the default Ditchlight board has all
three baked age-state reviews in this checkpoint.

The delivered allocation is 13,888 triangles new/season and 13,928 beat.
Relative to the original 11,662: deck +2,204; wheels +960; bushings +160;
visible axle ends +80; baseplates +24; hangers +22; mounting assemblies −448;
bearings −256; spacers/speed rings −304; kingpin/cup/washer hardware −72;
axle nuts −144. All three alternate widths pass at 13,870 / 13,860 / 13,914.
Three shared-image response materials form seven meshes and twelve primitives.
Each age embeds one 2048 BaseColor/Normal/ORM set after a 4096 bake. Estimated
BC-class memory with full mips is 16 MiB per resident state, 48 MiB for all
three; this is a compression estimate, not measured engine residency. Actual
GLBs are 7,960,356 / 8,815,616 / 9,130,536 bytes. PNG sets total
7,016,261 / 7,880,744 / 8,205,419 bytes, respectively.

All three final GLB audits pass: zero UV overlap/outside/degenerate triangles,
valid normals, preserved sockets/pivots and three embedded 2048 images. UV
coverage is 42.51 / 43.86 / 42.16%, median density 2,032 / 2,067 / 2,027 px/m.
All bake channels report zero missed interior texels; BaseColor reports zero
black interior texels. Raw form regeneration and final serialization from the
accepted maps are byte-identical. Independent generation of all 24 source PNGs
also matches byte-for-byte; no repeated independent GPU bake is claimed.
`make all`, `make check`, `make check-variants`, `make repeat-form` and
`make repeat` pass. Repository check reports 1,818 source files, zero errors.
No kit file or top-level README was edited; all 780 other delivery hashes match.

Remaining CG: the 2048 atlas softens individual carbide grains, small rail
fibers, bearing stamping and thin wheel lettering. The two veneer flakes are
simple in extreme macro. Scrape substrate is too even and scratch edges too
similarly sharp, old wheel oxidation is weaker than the 2010 photograph's
brown tread, and cast transitions retain some reduction shading. The indoor
light/camera and unknown reference truck measurements limit exact matching.
The eight residual hot glint pixels are recorded above. These are checkpoint
limitations; no final docs/gallery or photorealism approval is claimed.

Final local review: `renders/lookdev/contact.jpg`, `matched-pairs.jpg`,
`graphics-sheet.jpg`, `pairs/fullsize-wheel-pair.jpg`, all correction panels
under `renders/form-fixes/`, and the four `*-finished-before-after.jpg` panels
under `renders/lookdev/`. All remain ignored rebuildable outputs. No lead tool
or approval is needed; no shared-kit change was required.
