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
