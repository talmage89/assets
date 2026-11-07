# School form / construction review

This gate stops before school look-dev. There are no final documentation JPGs,
new school tiling bakes or weathering acceptance claims. All review renders
import the exported external-image glTF. Period photographs and the National
Register's reproduced plans were inspected directly.

## Pass 1 — plan graphs, room bay, export tint and exposed construction

**Color and value first.** The raw export initially dropped the source vertex
tint, leaving white materials despite a colored source. The exported COLOR_0
attributes now carry the quick colors explicitly. The nine inspected 900 px
views in `renders/pass1/` retain darker asphalt, deep canopy/window shadow and
unclipped coping. The brick and buff CMU remain intentionally uniform proxies;
they are not accepted brick albedos or a material match to the photographs.
Walls' concrete curb, McDowell's white spandrel and Emerald's pale fascia are the
neutral assumptions for the later photographic comparisons. The two 1973
transparencies carry a pronounced warm/magenta cast, so raw hue is not a target.

The three plan views prove different graphs: three fingers and a later cross
wing; independent four-room pods and covered courtyard links; an internally
organized compact core with a later rear classroom row. They are not one plan
with seed-specific dressing. The published Orchard and Fairview diagrams
support the classroom/spine and addition logic. Cheltenham supports a common
core distinct from teaching cells. Clear classrooms are 30 × 32 ft; wall pitch
includes the six-inch partition rather than consuming it from the room.

Rejected tells and fixes selected for pass 2:

- The tall gym had a visible open side above an adjoining low office roof.
  A 2D adjacency test incorrectly suppressed the whole wall. Exposed wall
  sections now begin at the neighbor's roof and extend to the gym's roof;
  coping/counterflashing follows the resulting step.
- The first two window cameras entered the next wing and rendered glass or
  darkness. The new cameras approach the outer west finger and the open north
  side of the east cluster, with the normal and tangent derived from that face.
- Court lines were one millimeter beneath the asphalt and disappeared. They
  move above the actual blacktop surface. The hoop construction rotates as an
  entire assembly to face the long court axis.
- The raised loop walk showed an unsupported black slot against grade. A
  two-meter lawn verge meets its edge and slopes into the field. Drive entries
  interrupt the curb and walk; a complete closed curb is not a valid entrance.
- All three heroes reused tree/vehicle positions relative to the door. Mature
  library trees now have different seeded positions, and the second car has a
  different uniform form paint. No new tree shapes or pixels are introduced.
- The portable's old ramp met a high lower landing and its windows lay against
  solid walls. Both are construction failures: real openings, a hinged door,
  continuous top landing, a 1:12 ramp and a lower grade landing replace them.
- Site 102 exceeded 300k. Local parked-car copies omit small brake/lug internals,
  retaining their authored body/wheels/glass, and the bike pad uses two racks.
  Existing library deliveries remain byte-identical.

The three school counts in this first tinted export were 61,720 / 65,344 /
60,828 triangles; whole sites 296,327 / 300,999 / 295,040. The middle site is a
rejected budget result, not a delivered exception. The photographs also show
that the early pods need broader glazing and a stronger spandrel/eave rhythm;
that comparison is retained for the next pass.

## Pass 2 — exported construction, camera visibility and real paths

**Color and value first.** All 27 exported views in `renders/pass2/` and the
three `renders/matches-pass2/*-pair.jpg` images were opened. The matched Walls
gym is much darker and less orange than the quick gym. Its neutral is the
sunlit concrete curb; brick is not a white-balance target. Seed 103's gym
proxy changes from the classroom ochre to a darker brown. This is a rough
value correction, not acceptance of final masonry. McDowell is balanced on
white spandrels; Emerald on the pale fascia. The scans' original lighting and
film response still prevent a numeric albedo claim.

The low classroom/tall gym proportion is plausible. The cluster ribbon needed
near-full-bay glazing, low white spandrels and deeper eaves: those now read in
the McDowell pair. The new sash is still too mechanically regular, with broad
uniform blinds and no occupied interior. That is explicit next-stage work.
The roof equipment has real curbs and intake/exhaust geometry, but identical
unit size and clean uniform membranes remain obvious proxies.

Construction failures found in this pass and corrected for pass 3:

- Adjacent visible facade intervals were split by unrelated block coordinates.
  This silently suppressed the entire main entry of seed 102 and some ribbon
  bays. Contiguous exposed spans now merge; every generated plan must contain
  exactly one main entry. This is not merely a camera repair.
- All door leaves omitted the floor elevation before rebasing at the hinge.
  They penetrated the threshold and left a large head gap. Leaf geometry now
  includes its real floor and 18 mm undercut; actual leaf/casing sweeps reject
  intersections. A gym pilaster also overlapped a door and now skips openings.
- The school name was hidden behind the canopy. It moves onto the front fascia
  where its construction and legibility can be judged. The fascia gains the
  depth visible in the covered-walk photograph.
- Rear exits, blacktops and playground gates opened onto isolated turf. An
  original walk network connects actual door approaches, the rear spine,
  playground gate, court, portable landings and field. The portable gains
  intermediate ramp supports; one seed-102 portable moves away from the fence.
- Two staff-lot rows and a drive through stalls were not credible circulation.
  The lot now has a side entry to its aisle, 9 × 18 ft stalls and a reserved
  11 ft van bay / 5 ft access aisle. The service lane shifts away from loops.
- Exported trees used their Wind attribute as a visible vertex color. It
  darkened and fragmented their crowns. Export now names Tint explicitly,
  preserves _WIND and strips color from untinted canonical materials. The
  shrub adapter now retains the original analytic alpha-mask atlas instead
  of rendering opaque leaf rectangles.
- The west-walk photo camera was fitted to columns hidden behind an addition.
  The final Emerald pair fits the exposed front canopy's actual columns.
  Seed 101's window camera moves inside the portable's sightline obstruction;
  seed 102's gym camera moves ahead of the parked car.

The library light is added at the staff lot. Car context uses a local decimated
copy and shared uniform form materials; the source family and its deliveries
remain unchanged. These savings pay for the school, doors and circulation.
All placed instance triangles, including foliage cards, count against the site.

## Pass 3 — full export review and supported circulation

**Color and value first.** All 27 images now retained in `renders/pass3/` were
opened at their rendered size. The darker seed-103 gym separates from its
ochre classrooms. Entry cavities, canopy undersides and sash pockets retain
shadow rather than a pale ambient wash; coping highlights retain shape. Flat
school colors remain proxies. The undifferentiated masonry, broad glass
response and repeated HVAC boxes still announce CG and are not accepted as
look-dev. The public-face silhouettes and relative floor/roof datums are the
subject of this gate.

The fingers, courtyard and compact core remain different in both full-site
and close plan views. The early classroom ribbon / low-roof relationship is
readable; smaller later replacement sash and the raised compact media core
give a different decade. The relocated names are legible in all entry details.
Doors no longer pass beneath thresholds or leave an open strip at the head.
The second gym detail is no longer hidden by a car. Tree alpha and Wind now
survive export without the old blocky color multiplication.

The extended source-surface sweep found one additional physical failure:
seed 102's courtyard-link end column stood in an addition doorway. That end
now bears on a steel seat against the addition's masonry above its door,
with no column through the opening. Twenty-one sampled poses test each leaf
against its casing and all neighboring source geometry, including other
leaves at rest and canopy columns. Portable doors are also tested on campus.
Cylindrical jamb knuckles have intentional attachment contact and are kept
separate from the moving leaf test.

Two unsupported-surface tells remained in these renders: the thin sloping
door aprons had black open edges; seed 102's foreground loop walk exposed a
raised open end at its drive. Aprons now have concrete side closures to grade.
The loop's walk/curb ends and adjacent verge descend into the crossing instead
of cutting off at full height. A final fourth visual pass checks those changes.
The overhead courtyard review also exposed a program error: the east pod's
cross link met its classroom side rather than its central corridor exit. That
link moves to the actual eight-foot hall centerline and stops at the pod's
outer wall instead of penetrating a meter into it.

Still weaker: sparse grounds, geometric rectangular path runs, identical roof
units, dark shallow room witnesses and regular blinds. The service volumes
and small practice field are schematic, not full school facilities. Exterior
routes now exist; no claim of complete historical accessibility or a certified
bus swept path follows from that fact. Fine construction normals and all
cause-driven school aging remain deliberately deferred to look-dev.
The reused library cars are also late-2010s designs, later than this town's
1995–2015 brief. Their quick context reuse does not resolve that period mismatch;
final school scenes need a period vehicle variant from the car family.

The three updated pairs in `renders/matches-pass3/` were also opened. Emerald
now shows the exposed front canopy rather than an addition occluding the fitted
columns. Its long fascia and slim column gauge are plausible; the original
school's lower office proportions differ intentionally. Walls confirms the
gym/office height step, but even the darkened proxy remains lighter and flatter
than its weathered brick. McDowell confirms the near-full-width ribbon and
low spandrel, while the repeated blinds/glass response remain too uniform.
Camera estimates are 42.09 / 43.96 / 59.77 mm with native-image landmark RMS
18.19 / 17.58 / 8.15 px; these are type fits, not identical-building matches.
Independent Blender projection verification is below 0.05 px for all three.

## Pass 4 — complete review, parcel conflicts and exact drive cuts

**Color and value first.** All 27 views in `renders/pass4/` and its three
`renders/matches-pass4/*-pair.jpg` images were opened. Full-frame display-luma
p1 / median / p99 was 0.050 / 0.356 / 0.898, 0.084 / 0.468 / 0.898 and
0.189 / 0.511 / 0.895. All-channel clipping was zero. Those include sky and
ground; they are exposure facts, not measured school albedos. The Walls pair
still rejects final approval of the flat gym color. The form gate does not
turn those quick colors into finished materials.

The corrected courtyard cross link meets the central hall exit. The apron
side closures remove the previous floating wedge below the gym doors. However,
the foreground drive still had a real hole: whole curved walk/verge segments
were removed when their centers fell inside a wider gateway threshold. That
left uncovered slivers outside the narrower paved drive. The fix now clips
each source triangle against the exact drive rectangle and lifts the result
back to its own surface plane. This preserves the adjoining curb/walk/verge
instead of dropping a whole segment.

The parcel audit found three other failures worth recording plainly:

- Seed 101's oak trunk was inside the kitchen footprint. The crown obscured
  the mistake in some views. It moves to clear lawn northeast of the service
  block. Actual low trunk-vertex bounds now reject building overlaps.
- The added rear walk crossed the first and third playground reservations.
  Those pads move behind the rear spine; the field approach skirts both the
  playground and court. Actual walk polygons are checked against the authored
  reservation, allowing only a 2 × 1 m gate apron. Portable wall footprints
  are measured separately and also reject walk penetration.
- Portable landings ended at the school floor datum, leaving a six-inch step
  to general site grade. A separate 2.7432 m gentle approach now descends from
  the lower landing to 0.018 m grade. The first portable moves north, its route
  passes east of its ramp instead of crossing the parent loop, and the second
  connects from below its landing. North gym exits gain actual connections;
  the courtyard connection rises gently into the covered walk.

The full clean rebuild exposed a single oak-trunk MikkTSpace tangent component
alternating by 0.0001 between exports. The kit's existing guarded tangent repair
now preserves the accepted canonical oak corner, with exact position/normal/UV
guards and a one-rounding-step bound. This is not geometry rounding or a
previous-school binary dependency. An independent repeat passed all 34 files
before the parcel fixes; the final repeat is rerun after those fixes.

## Pass 5 — all views, circulation at grade and one rejected field route

**Color and value first.** All 27 exports in `renders/pass5/`, its three
`renders/matches-pass5/*-pair.jpg` images and the extra eye-level gateway preview
were opened. The exact driveway cut removes the black void. Entry and sash
shadows remain deep; the proxy colors and material limitations from pass 4
remain. No lighting/exposure change is used to disguise the construction fix.

The relocated oak is visibly on lawn rather than through the kitchen roof.
The playgrounds now sit beyond the rear walks. Portable approaches reach site
grade and their paths pass outside the actual portable walls. North gym exits
connect into the site's paths, with the courtyard path rising into its covered
walk. Source placement checks and the 3,750 downward entrance probes pass;
fresh import checks separately preserve the resulting frames and bounds.

One route was still wrong: seed 102's field connection skirted the blacktop by
passing north of it, then cut across the practice infield. That is rejected.
The rear spine now extends west and the field branch follows the west side
of the backstop. Checks now also reject walk overlap with the entire authored
practice-field envelope and blacktop play area (except its shallow entry
apron). This last parcel change is reviewed in pass 6.

The independent repeat passes 34 geometry/image files with the canonical oak
tangent guard. The source checks measure 35 classrooms, test 42 exterior
leaves through 882 poses and preserve all 772 existing delivery files. Those
facts prove construction and serialization within their stated scope; they
do not accept the school materials, aging or final UV/bake quality.

## Pass 6 — final exported form checkpoint

**Color and value first.** Every final view in `renders/checkpoint/101/`,
`102/` and `103/`, all three final photographic pairs, and both final contact
sheets were opened. The hero display-luma 1st / 50th / 99th percentiles are
0.0506 / 0.3590 / 0.8975, 0.1082 / 0.4709 / 0.8981, and
0.1885 / 0.5111 / 0.8947. No pixel clips in all three channels. Those are
full-frame diagnostics, including sky and ground, not measured albedos or
material acceptance. The quick gym surface is still lighter and flatter than
the neutral-balanced Walls photograph. The covered-walk and ribbon pairs
retain the structural depth while making the regular blinds, uniform walls
and sparse surroundings obvious. These remain look-dev work.

The final courtyard above/rear views confirm that its field approach now
runs west of the backstop rather than through the infield. Source walk
polygons have zero area overlap with the authored field envelope, court
play area, portable wall footprints and playground reservations beyond the
explicit entrance aprons. All three campuses have connected exterior routes;
the different circulation graphs, classroom window rhythms, roof-height
steps and later additions read as three places rather than recolored copies.
The 1950s fingers, 1960s court and 1970s compact core remain deliberately
original interpretations of the cited types, not replicas of the photographs.

The final `make` completes references, construction, checks, 27 exported
Cycles views, three calibrated pairs and both sheets. A separate `make repeat`
passes all 34 external geometry/image files. Source checks measure 35 rooms,
42 exterior leaves through 882 poses, and 3,750 downward surface probes at
the loop entrances. The grammar checks 300 seeds. Fresh imports preserve
counts, bounds, pivots and sockets; these serialization checks are separate
from the physical source checks. All 772 existing delivery files remain
byte-identical. Package hashes, including referenced images, match all 30
final Cycles views. Buildings use six materials; sites remain under 300k
placed triangles. Final budgets and shared image costs are in README.md and
`build/check.json`.

The remaining weaknesses are explicit: proxy masonry/roof response, repeated
HVAC and blind arrangements, shallow room witnesses rather than complete
interiors, sparse grounds and schematic program/mechanical systems. There is
no causal school aging yet. Final UV density, collapsed staging charts,
lightmap charts, bakes and normal-map fidelity still need their own acceptance.
The reused late-2010s cars are period-inappropriate context stand-ins. Neither
the checks nor the photographs certify a complete school program, structural
design, continuous collisions, vehicle swept paths or occupancy/egress code
compliance. The form/construction evidence is ready for the lead's checkpoint
review. Work stops here, before school look-dev.
