# Coffee shop / form and construction critique

This gate uses quick materials and exported external-image glTFs. No final
manufactured-material bake, wear pass or docs gallery is approved here.
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
