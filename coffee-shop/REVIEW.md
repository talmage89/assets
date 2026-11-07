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
