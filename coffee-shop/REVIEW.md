# Coffee shop / form and look-dev critique

The first three passes below record the accepted form gate with quick materials.
The new look-dev passes use exported external-image glTFs, baked manufacture
and placed wear. This round stops before the docs gallery.
Every rendered image in passes 1–3 was opened, including failed views.
The period photographs remain in ignored `refs/`; their credits are in SOURCES.

## Pass 1 — storefront and first exported views

**Color/value first.** The exterior was too blue and dim compared with the
neutral painted trim and sunlit walks in the 2008 references. Black steel
remained dark, but cool illumination obscured its construction. The interior
had large artificial white disks from presentation area lights. Kept exposure
fixed, reduced sky saturation/strength and increased the raking sun. Hidden
light-source disks while retaining actual pendant geometry and illumination.
This is a checkpoint lighting correction, not material calibration.

Evidence: `renders/pass1/{117,228,339}/{hero,counter,above}.png`, pad
`walkup.png`, and `pieces.png`. Comparison: Annie's old shopfront/awning,
PJ's 2008 end cap, Lakeview's converted building and Rose Nicaud's counter.

- Downtown's projecting molding cut straight through FOLIO. Advanced its
  sign carrier beyond the molding and centered it in the old fascia.
- Host glazing roughness smeared menus and group heads. Reduced quick glass
  roughness to a plausible polished-pane value, preserving physical panes.
- Cloned glTF roots retained quaternion mode, so a requested Euler yaw did
  not rotate the strip counter. Corrected the local-frame conversion.
- The walk-up opening was on the wrong side-wall station; its interior
  backing also needed a matching hole. Corrected both actual apertures.
- Finite paving ended against black ground, and the isolated old building
  lacked party neighbors. Added continuous procedural ground and adjacent
  host context. The pad stays separated from its neighboring buildings.
- Furniture scale read correctly, but the sparse first piece sheet had a
  black background and poor small-part legibility. It needed a floor/labels.

**Verdict:** recognizable cafe types, unsuitable checkpoint presentation.
The room was too schematic and the strip fit-out was functionally wrong.

## Pass 2 — legibility, real construction and measured circulation

**Color/value first.** The steel and timber retained deep values under the
more neutral sky; bright surfaces stopped reading pale blue. Compared with
balanced neutral assumptions in the period photos, the common wooden room
was still overly clean and regular. Detailed wear remains for the requested
later gate; do not add random smears to disguise missing construction.

Evidence: all `renders/pass2/` images. Rose Nicaud shows the missing spatial
hierarchy: customer counter, working aisle and equipment/back bar. Coffea's
photo shows rounded stock and fine expanded metal rather than a coarse cage.

- Added a separate supported back bar and a **.96 m** working aisle. The
  espresso machine's operating face now looks into the working area.
- Corrected the strip counter to face into its room and aligned its menus
  behind it in the same frame. The first revised camera still hit a pier.
- Replaced oversized chair wires with a crowned steel sheet and original
  diamond coverage. Mesh edges and bent frame remain physical geometry.
- Rounded the arm bends; kept their real **22 mm** diameter. Added lower
  support/plinth geometry beneath the customer counter.
- Actual triangle clipping, not center tests, found umbrella eaves entering
  the public walk, foliage in an entry, and a fence across the pad entrance.
  Made an umbrella table with four legs and a **52 mm** guide around the
  stock pole/base. Opened the fence at the entry and moved/trimmed plantings.
- Enlarged the accessible table's approach width; checked the actual legs
  and apron with rays, rather than quoting the socket's intended dimensions.
- Added actual cutout window vinyl, then reduced it and raised it after the
  close-up showed it obscuring the equipment.

**Verdict:** form substantially improved. Remaining problems were furniture
contacts, final framing, and route connections beyond the obvious rectangles.

## Pass 3 — exported construction, context and photographic framing

**Color/value first.** At native 1200 px the dark frames and room cavities
remain dark, cream signs roll off, and metal highlights retain headroom.
The quick shaded paving is still simpler and cleaner than Annie's used walk.
The three shop identities read green, wine and teal; their age-specific
fading/scuffs/deposits are specified but deliberately not baked at this gate.

Evidence: every `renders/pass3/` image, including scale and the failed strip
counter/chair views. Photo camera studies use named glazing/umbrella features
and assumed neutral trim/table patches. The geometry is an original design;
the pad is not a copy of Lakeview's roof/canopy.

- Repaired the chair rear-panel edge/support contacts and arm termination;
  fine holes now reveal the ground without a thick wire silhouette.
- Chairs had been facing away from tables. Corrected their actual local yaw.
- The umbrella intersected the laptop screen after being centered properly.
  Moved the setting within the tabletop's remaining radius.
- The strip counter camera was behind its masonry pier. Reframed through
  a real pane. Isolated the placed chair from the actual shop export for its
  construction close-up, since rail/column occlusion spoiled the site views.
- Moved the pad's front row inside the canopy clearance, away from its public
  route, and moved receptacles away from the side-route connection.
- Added and tested explicit public-to-cafe connectors. The A-frame moves
  outside the strip connector; the route does not terminate at a fence.
- The generator now varies two/three outdoor pairs, counter position,
  identity/palette, settings and placements within each type. The three proof
  sites retain different topologies: curbside band, covered-walk patio,
  and front/side court with a walk-up window.
- Kept the street context within the requested period; current library cars
  are late-2010s, so the final coffee presentation omits them.

**Verdict:** ready for a final checkpoint review of current export images
and all three photographic pairs. Final finishes, cause-driven age and unique
bake UVs remain the next gate, rather than being claimed complete here.

## Pass 4 — native construction close-ups and resource audit

**Color/value first.** Opened every 1600 px `renders/pass4/` image and all
eight completed `renders/pass5/` images. Dark mesh/frame values remain deep;
the tabletop rim, espresso rails and lettering keep highlight headroom.
Cream walls and canvas still have too little local material variation against
the photographs. The floor and joinery are too glossy and regular. These are
quick-material weaknesses, not evidence of finished look-dev.

- The revised strip counter camera clears its pier and shows the two work
  surfaces, grinders, machine and case. Glass reflections still cover menu
  rows. Keep them in the critique: hiding panes would evade the requirement.
- Table settings clear the pole and fit the small tops. The pastries are
  conspicuously rectangular, and all equipment/cups are too evenly arranged.
  Those forms deserve another focused pass at the next gate.
- The isolated placed-chair views show rounded arm bends, actual feet,
  lower bracing and a supported curved back. At close range the alpha holes
  are too flat and regular; manufacturing relief belongs in the normal bake.
- The pad's walk-up view confirms the real wall opening, sliding-pane frame,
  bracketed shelf and visible counter, rather than a window over an opaque
  backing. Its large blank side wall still reads as a schematic conversion.
- The pad roof, neighbor storefronts and identical stock green umbrellas are
  overly orderly. A distinct plan is present; an individual history is still
  absent. Apply fading, repairs and hand/drag wear by cause at the next gate.
- Found duplicate material records after image compaction. Merged exact
  exported states locally: the shops now have **12 / 17 / 15** total material
  records, including host and reused resources, rather than claiming the
  whole sites meet the new fit-out's three-state allocation. The **67 / 95 /
  53** primitives remain a significant batching opportunity for final delivery.

**Verdict:** construction and circulation are reviewable. This is still visibly
a form checkpoint. Preserve the useful dark tonal range when adding finishes;
do not compensate for flat surfaces by raising exposure or adding noise.

## Pass 5 — current exports and drawn layouts

**Color/value first.** Opened all **23** current 1600 px Cycles PNGs. The
architectural framing's display-luminance medians are **.304 / .373 / .394**;
99th percentiles **.713 / .837 / .825**. No sampled channel clips white.
The first percentile is **.000 / .007 / .004**: deep cavities remain present.
These are display-image measurements including reflections and some sky,
not measured albedos or proof of matching a photographic material.

The downtown reads as an old storefront with a fresh coffee tenancy. The
strip is visibly an end cap with a long covered walk and a separate patio;
its equipment is less legible from the distant hero because of the columns
and counter orientation, but the through-glass detail resolves it. The pad's
front and side courts and walk-up aperture make it a third place/plan. It
still looks newly assembled; faded conversion surfaces remain unimplemented.

Opened all three annotated layouts. The first annotation placed accessible
labels over entry dimensions; separated those labels and added a gold-key
footer. Every drawn corridor has been tested against actual imported
triangles from 25 mm to 2.03 m above grade. An inserted negative obstruction
must be detected. This establishes the shown corridor boxes, not occupied
chair motion, door sweeps, slab slopes or a jurisdiction's permit approval.

Measured accessible-table width/underside are **.775 / .732 m**, with **195**
clear forward rays. Public walks are **1.870 / 1.880 / 1.900 m**. The visible
room and shop totals stay under **60k / 200k**; all furniture stays under
**3k**, except the allowed stock umbrellas at **3,920 / 3,908** triangles.

The isolated stock/host/shop repeat reproduces **46 delivery files /
16,711,476 bytes** after normalizing relative canonical image URIs. Each
host is independently rebuilt and byte-compared too. All **140** preexisting
delivery/map inputs retain their starting hashes. Importing the three sites,
a duplicate site, the stock sheet and a standalone chair holds **14 / 14**
decoded images. No kit or other-family file was changed.

**Remaining form weaknesses:** upholstery is blocky; case pastries are too
uniform; room dressing is sparse compared with Rose Nicaud; frame/hardware
joinery lacks fine weld/fastener relief; canvas has insufficient fold variety;
all businesses share the same green stock umbrella finish. Full door-closer
linkage motion and swept clearance remain uncertified. The current material
and primitive counts also need deliberate final batching. None is hidden by
the geometric pass result.

Possible kit follow-up: exact-state material compaction after image/texture
index compaction would remove the need for this family's local final pass.
It was kept local to preserve all existing deliveries.

## Pass 6 — photographic pairs and final contact

**Color/value first.** Inspected the three completed pairs, their residual
overlays and the final matched contact. Annie's neutral is pale door trim;
Coffea's is the unpainted table edge; Lakeview's is pale window/base trim.
These assumed neutrals have unknown photographic processing. Coffea needs
the largest balance correction (linear RGB gains **1.391 / 1.008 / .775**),
so its shaded blue fabric is particularly unsuitable as an albedo sample.
The final heroes retain medians **.303 / .373 / .394**, 99th percentiles
**.713 / .837 / .825**, and zero sampled white clipping. Deep cavities remain.

- **Annie's / storefront:** the framing reads the projecting cover, recessed
  entry, pane depth and shaded room. Our fresh dark-green shopfront differs
  deliberately from its pale old construction. The photograph's irregular
  signage, layered hardware and lived-in walk make our parallel rails, clean
  pavement and sparse window dressing look overly manufactured. The awning
  still lacks the reference's varied edge folds and attachment character.
- **Coffea / furniture:** frame gauges, compact chair/table scale, pole,
  canopy span, ribs and weighted support read as construction. The stock
  canopy's scalloped sag and vent differ from the photographed type; its
  cloth is too regular. Our dark paint differs from the photo's silver frame.
  The expanded steel needs baked thickness/wear cues; chair drag/contact
  wear and tabletop use are still absent. These finishes remain the next gate.
- **Lakeview / pad:** the original flat-roof pad is not a reconstruction of
  the large former service-station canopy. The fitted comparison uses its
  long glazed plane; it cannot establish the return wall or overall roof
  proportions. Our blank return and plain roof are particularly weak in this
  angle. More credible infill/repair material transitions and visible age will
  be needed for the converted-building story.

Landmark RMS is **4.52 / 16.26 / 12.43 px** in the 1000 px photographic studies;
estimated lenses **35.69 / 70 / 70 mm**. The latter two reach the lens bound.
Independent Blender projection disagreement is **.00024 / .00022 / .00115 px**.
That verifies the camera math, while the larger residuals and different
construction limit photographic comparison. It does not prove form identity.

The low pad view exposed a **presentation** subgrade gap below the finite
exported slab. A first correction raised the whole terrain and covered the
road; that gallery was rejected (`renders/checkpoint-grade-rejected/`).
Restricted raised fill to the parcel behind the curb and rerendered all
23 views and all three pairs through the shared GPU lock. Actual imported
triangle rays versus terrain vertices measure **4 mm** overlap beneath the
front pours and **14 mm** beneath the pad side court (`build/context-contact.json`).
The street stays visible. No exported asset geometry or other delivery changed.

Inspected every final view in six review grids, the corrected hero/pad pair,
the drawn layouts, the piece sheet and the final contacts; earlier passes
also inspected the close-ups at native resolution. No additional form change
is hidden behind the final material critique.

Proof commands completed: the empty coffee `build/` + `export/` build via
`make WIDTH=1600 SAMPLES=48`; `make check`; `make repeat`; independent kit camera
verification; the final two `src/render.py` invocations at **1600 px / 48 samples**
inside one `kit/with_gpu.sh` lock, followed by pair composition and `src/review.py`.
The latter validates **23** current gallery PNG receipts plus the matched PNGs
and requires **three** completed pairs. Repository and whitespace checks pass.

**Checkpoint verdict:** three distinct businesses, working visible-room
hierarchy and reviewable furniture/layout construction. Stop here as requested.
Material realism, causal age, finer food/upholstery forms, unique bake UVs,
final batching and complete motion certification remain unfinished.

## Look-dev pass 1 (pass4) — reject foreground obstructions and hidden wear

**Color/value first.** The neutral-balanced Annie's and Fair Grinds pavement
has bright lit areas, deep canopy shade and an irregular history of use.
The first revised Folio remained almost entirely in shade; Morrow's walk
looked new. Counter oak was too yellow/orange against the neutral plaster
and older wood in Rose Nicaud. Rejected these looks: darkened/desaturated the
oak input, added ground-tied wear samples beneath actual customer/table
locations, and adjusted the daylight's balance without lifting black steel.

Opened every newly rendered image in `renders/pass4`: the three heroes and
overheads, each table/counter/awning and the pad walk-up (16 images). The
folder also contains old chair/scale images from the previous gate; those
are not evidence of this new pass. Native revised images are 1000 px wide.

- Folio's fixed hero camera was inside the opposite awning. Increased Main
  Street to 14 m and set the opposing front behind its public walk, leaving
  the 40 mm / 1.65 m camera fixed. Party-wall neighbors are correctly joined
  and their dressed rooms now render; their practical light needs review.
- Switchyard's fixed camera was inside the east island tree. Moved that
  island back on the lot; the new hip roof only read in the overhead.
- Every car's canonical lamps were on, producing red streaks in glazing.
  Parked instances now use zero lamp emission, with local scalar paint
  variants. Canonical car files and geometry are unchanged.
- Awning front creases left a small mismatch at the valance attachment;
  closed that seam and made each cloth chart continuous across its rib bay.
- Croissants stopped being boxes, but repeated crust charts read like
  ridges on a molded chip. Corrected their section orientation, softened the
  broad rolls and mapped one continuous crust chart around each roll.
- Shared paving had too few samples for customer-local history. Added only
  exposed-top samples; side gauges stay large faces and buried bottoms are
  omitted. This adds no image, material family or per-seed map.
- Removed vinyl is gone, and the three backed menu boards have single,
  distinct coffee/espresso/bakery listings. The new wood grain reads, but
  the room is still too orderly compared with the equipment photograph.

The four photographic fits remain explicit estimates: 4.52 / 16.26 / 12.43 /
25.83 px RMS. The last matches two actual canopy ribs, not an invented full
roof reconstruction; the reference has a deep metal gallery and ours has
fabric. It is a canopy-shade/use comparator, weaker as construction evidence.
No person or photographic texture is reproduced.

## Look-dev pass 2 (pass5) — connected sites, native material read

**Color/value first.** The counter wood is now a deeper brown rather than
yellow plastic; black steel stays black and the cream tops retain highlight
headroom. Compared with neutral-balanced Fair Grinds, the walks still show
too little accumulated contact history at the hero distance. Source fields
and shipping pixels agree closely, so the remaining weakness is authored
macro wear, not a bake/color-space correction. Added floor-owned queue
darkening and retained localized outdoor spills/drag wear.

Opened all 19 new 1000 px views in `renders/pass5`: hero, above, table, counter,
awning and full site for each, plus the walk-up. The fixed Folio and pad
cameras are clear. Dressed neighbors, foreground parking, the pad hip and
the strip's other tenants are actual exported geometry. Canonical vehicles
are now parked with lamps off and locally varied paint, removing red glass
ghosts. The street/lot widths and door/table layout are distinct places.

- Folio's curbside cars were just outside its fixed hero. Moved two into
  the camera's edge while retaining the public walk and curb buffer.
- The awning's rectangular dark tabs were its front frame showing through
  the displaced cloth. Recessed the front carrier and rib noses behind the
  valance. Cloth charts and normals now stay continuous across a rib bay.
- The croissant was smooth like a small bread roll. Increased its crescent
  and tapered horns, with broad rolled dough lobes, using the same triangles.
- The pad's side wall was all shade and too blank. Chose its own raking sun
  direction, added a cause-local repaint patch/cracks at that repair and
  completed the side hip seams. The walk-up sill mark now sits 0.35 mm
  above the actual shelf top.
- The queue's five isolated dark stamps looked like dots. Removed them and
  sampled continuous traffic/handoff darkening on the exposed floor. The
  room's construction and arrangements are unchanged.

Still weak: the block's repeating neighbors, orderly smallware and case
contents, broad plain stucco, sparse planting, and similar clean umbrellas.
The patio marks should remain restrained, but the ages must read without
zooming into individual scratches. Final native-size views and photographic
pairs are the next acceptance test, not these counts alone.

## Look-dev pass 3 — native PBR, reject obstructed photo comparisons

**Color/value first.** Opened all 26 first full-size 1280 px views and the
four newly composed photographic pairs. Compared with the assumed-neutral
Annie's pavement, our sidewalk is too even, especially under customers' feet;
the black steel is suitably dark but remains too uniformly coated at the
glides. Broadened the customer-local concrete stains, keeping their centers
at seats and handoff/entry locations. Remapped existing lower leg faces to a
height-driven coating-loss chart; chair geometry remains exactly 2,156 tris.

The warm rooms retain ceiling/pendant gradients and shadow under the counter.
The three business signs used too similar a serif treatment; Morrow now uses
its own titlecase sans, Switchyard a heavier sans, and
Folio keeps its bookish serif. They use the same atlas allocation.

Rejected two photo comparisons: Lakeview's landmarks had been assigned to
the receding side instead of the front, putting an island tree in the
comparison. Reidentified front glazing/eave landmarks and moved only the pad's
east landscape island toward the walk approach, away from that sight line.
Fair Grinds' shallow canopy-only fit invented a 13.8 degree camera roll. Added
explicitly estimated wall/ground junctions behind the gate/patrons; the new
fit is near level, but has a larger, honestly reported residual. Its deeper
metal gallery is not proof of matching our fabric construction.

Scale silhouettes were hidden by foreground parked cars; dedicated scale
views now omit only those context vehicles and record that omission. Enlarged
the isolated-piece studio ground to remove its black edge. The underlying
site exports retain all vehicles. Fixed the independent parking checker to
apply homogeneous raw glTF matrices, then convert measured NumPy scalars for
its JSON receipt. These are checker corrections, not geometry changes.

The final rerun must verify these fixes on the export, all new photo framing,
and the actual atlas bake. Remaining tells are orderly smallware, smooth
pastry crusts, repeated block architecture/trees and broad plain wall areas.

## Look-dev pass 4 — reject the dark gap at the town edge

**Color/value first.** Native PBR heroes retain neutral gray concrete, dark
steel/canopy cavities and warm rooms, without lifting the whole façade to
make its shaded furniture readable. Against the balanced used-café photos,
the broad walks remain cleaner than the strongest photographed mildew; our
stains stay tied to customer locations rather than copying that entire age.

Opened the complete second native set through Morrow and the pad's hero,
overhead, table, counter and awning. The pad's distant black horizontal slit
is not acceptable as an artistic shadow: the district soil was 240 mm below
the road top, leaving an air gap below the finite paving boxes. Interrupted
only our queued photo-match job, raised the context terrain to 5 mm below
the actual roadway surface (including Main Street's lower road grade), and
reran all sites/views. The new independent receipt measures raw exported
terrain/paving heights, requiring support intersection while leaving the
paving surface exposed. No café/furniture/layout dimension changes.

The scale views now expose the 1.8 m figure; opaque cars remain in actual
site exports and normal views. Morrow's titlecase sans and Switchyard's bold
sans distinguish them from Folio's serif without another texture set.
Smooth pastry crusts and orderly room contents are still weaker than the
period counter photograph; they no longer have box silhouettes. Fine rail
chips and foot abrasion need the detail views more than the widest hero.

## Correction evidence index

All paths are local rebuildable evidence, outside `docs/`. The 16 before/after
pairs assert identical saved camera recipes; each side is 1,024 px wide.

| Requested correction | Exported evidence |
| --- | --- |
| Shops connected to streets/lots | `renders/fixes/117-hero.jpg`, `228-hero.jpg`, `339-hero.jpg`; all three `renders/lookdev/<seed>/site.png` |
| Dressed Main Street neighbors | `renders/lookdev/117/hero.png`, `117/scale.png`, `117/site.png` |
| Pad silhouette and walk-up | `renders/fixes/339-hero.jpg`, `339-above.jpg`, `339-walkup.jpg` |
| Fabric frame, sag and valance | `renders/fixes/117-awning.jpg`, `228-awning.jpg`, `339-awning.jpg`; overheads expose cloth bays |
| Offset duplicate lettering | `renders/fixes/117-counter.jpg`; the reflective promotional vinyl was removed; hours, signs and menus reviewed in all counter/awning views |
| Pastry forms and real size | `renders/fixes/228-table.jpg`, `339-table.jpg`, each counter; `export/pieces/PastryCase.gltf` |
| Raking sunlight, warm room, cars | Three `renders/lookdev/<seed>/hero.png` at 40 / 45 / 42 mm and eye height |
| Cause-local age and baked response | Table, chair, counter, awning and walk-up details; baked/source period photo pairs |

`renders/fixes/contact.jpg` indexes every fixed-camera pair. Full normal
presentation is `renders/lookdev/contact.jpg`; layout annotations remain in
`renders/lookdev/layouts.jpg`. Shared-chart audit and photographic judgment
are separate receipts, as are serialization, route geometry and physical
terrain support.

## Look-dev pass 5 — final exported PBR and source comparison

**Color/value first.** Compared all four assumed-neutral period photos with
both the source-finish and baked exports. Cream trim and tops retain highlight
headroom; painted steel remains dark, with deep canopy/under-counter shade.
Folio's fitted wood stays brown instead of the first pass's orange/yellow.
Switchyard's older canvas is lighter on its exposed roof than its shaded
valance, while the window sill's abrasion remains on its contact surface.
The photographic sidewalks have more irregular accumulated use than ours,
especially the damp/mildewed Annie's walk: our used pavement remains a
weaker match, even after broadening the seat-local stains.

Opened every final 1280 px presentation render (26), all eight native
source/baked matched renders, all eight composed pairs, and the three native
fixed-camera hero comparisons. The terrain correction removes the distant
road slit; actual exported heights establish support separately from the
images. Front glazing, all three identities/menus, cloth bays, table settings,
scale silhouettes, the walk-up and the whole sites were inspected.

Display-space luminance in the architectural framing rectangle, including
glazing and reflections (not an albedo measurement):

| Seed | p1 | p50 | p95 | p99 | Any-channel clipped pixels |
| --- | ---: | ---: | ---: | ---: | ---: |
| 117 | 0.0000 | 0.2312 | 0.5876 | 0.6969 | 0.000000% |
| 228 | 0.0081 | 0.3390 | 0.7877 | 0.7953 | 0.000000% |
| 339 | 0.0429 | 0.3891 | 0.9202 | 0.9529 | 0.000540% |

The source-finish pairs use the same game geometry with original manufacture
charts and meter-valued height, before normal-map baking/filtering; they do
not claim a high-sculpt projection comparison. The 4096-to-2048 bake slightly
softens fine grain/print edges but preserves the broad hue/value and menu
legibility. The remaining plainness is mostly authored detail/use history.

Final landmark fits are **4.52 / 16.26 / 17.04 / 58.49 px RMS**. The pad
comparison now uses the correct front glazing/eave plane; an island still
partially overlaps the side patio, but the front and hip are readable. The
Fair Grinds view is close to level and includes seating, but its 45.7 mm fit
is the weakest: the reference has a deeper gallery, denser planting and
people using a narrower shaded walk. The two hidden ground junctions are
estimates. Neither that fit nor the camera implementation check proves
matching photographed architecture or albedo. The umbrella/pad estimates
reach their 70 mm bound; no original EXIF or surveyed photo footprint exists.

Remaining CG tells, recorded for the lead: repeated neighboring façades and
trees; an orderly room/case and sparse smallware; smooth pastry crusts;
broad stucco/concrete age that is cleaner and less irregular than the used
photographs. Glass reflections veil some menus; fine rail chips and chair
foot abrasion mostly need the detail views. No final docs/gallery is made.

## Reproducibility corrections

Strict byte tests exposed MikkTSpace rounding at three imported car corners
and one-bit UV interpolation on the private Commercial neighbor slabs. No
position, normal, index or layout discrepancy was accepted. Production and
repeat now both use one CPU worker, as the vehicle pipelines do. Private
Commercial-host UVs round to six decimals after evaluated bevels; measured
maximum change is 9.536744e-7, below 0.002 shipping texel. Original canonical
family files remain unchanged. Three asset-owned tangent anchors per proof
site use `kit.gltf.stabilize_tangents`: exact position/normal/UV signatures
and at most one 0.0001 rounding step are required; this cannot conceal a
changed source corner. The source anchors are in `src/context_tangents.json`.

The clean rebuild subsequently passed all 53 delivery files (121,942,723
bytes) and all seven private host GLBs byte for byte. New final views are
rendered after that reproducible source path; the GPU rebake is checked
separately with the kit's RGB pixel tolerances and exact coverage alpha.

## Final checkpoint receipts

- `make check repeat WIDTH=1280 SAMPLES=40`: PASS. Fresh scene imports,
  counts/scale/normals/chart bounds/density, actual route surfaces and knee
  rays, measured parking gaps and terrain support; 53 delivery files /
  121,942,723 bytes plus seven private host GLBs reproduced byte for byte.
- `make all texture-repeat WIDTH=1280 SAMPLES=40`: the complete `all` goal
  finished (26 presentation renders, eight matched renders, four photo pairs
  in each finish stage, and 16 fixed-camera comparisons). The additional
  rebake check initially rejected its alpha reader because Pillow-generated
  BaseColor uses legal PNG filters unsupported by `kit.image_io.read_png`.
  Switched only that coverage reader to Pillow; kept kit RGB comparison.
- `make texture-repeat check-repo`: PASS. Independent real 4096 GPU rebake
  filtered to 2048: BaseColor / Normal / ORM each have maximum byte delta 0
  and RGB byte RMSE 0; coverage alpha is exact and accepted maps unchanged.
  Repository: 1,979 source files, zero errors.
- Final CPU receipt audit: all 34 native PNGs identify the current actual
  exported bundle and match their recorded pixel-file hash. All 53 current
  export files still match the repeat receipt. Existing delivery hashes:
  140 / 140 unchanged. No kit, top-level README, docs or gallery authored.

Opened the regenerated native views and matched renders after the numerical
reproducibility changes; the visual conclusions of pass 5 hold. The final
new set is 3,447,041 PNG bytes / 16 MiB with 8-bpp compression and full mips.
The three complete shop allocations are 108 / 86.67 / 86.67 MiB; the union
of all context images is 262.17 MiB. Shared-chart reuse remains explicit.
No tool installation or other lead action is needed. A gravity/roll bound
for poorly constrained photographic fits would be a useful future kit
option; no shared helper changed in this round.
