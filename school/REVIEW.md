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

## Pass 7 — first look export rejected: value, camera and site cost

**Color and value first.** Opened all six 1000 px native Cycles views in
`renders/look-pass1/`. Ground and brick now have readable manufacture, but
using the red commercial brick for all three districts clipped the intended
buff/tan channel multipliers. The result was three red schools. Rejected that
binding: 102/103 now use the houses' already-authored buff/tan bricks, baked at
4096 and shipped at their native 512. No new school texture set. Exposure is
fixed; albedo changes, rather than exposure raises, distinguish the palettes.
Walls' concrete curb and McDowell's white spandrel remain the balancing
neutrals; Emerald's monochrome fascia is the third comparison neutral.

The large tree trunk hides 101's entry. Planting moves off that camera ray and
the hero moves to its actual loading approach. The compact hero gives too much
of the gym's near wall: the next view approaches from the parent lane instead.
102's communal/service block moves to the other side of its office; the
four-room pods and exact room reservations stay intact. The entry headings
are south, east and north in the campus frame. In the first above views the
new neighborhood houses still floated on lawn: continuing streets, curb/walks
and native utility-pole sockets now connect them. The park-backed site keeps
its rear woodland instead of another row of houses.

The first full sites were 381–409k, rejected. Native fence alpha charts stay
unchanged, but continuous run rails and eight-sided posts replace repeatedly
modeled bay ties. Weather samples are restricted to the wall runoff locations
and short column-base stations, rather than cutting the whole canopy deck.
Lettering is painted, so it has no invisible extruded sidewalls. These changes
bring the subsequent 101/102 buildings back to about 72k; whole-site budgets
are checked on serialized placed instances, not unique mesh data.

The open bus and parent routes also receive a physical review. Bus direction
is westbound along the school-side north curb so the actual right-side doors
would face the walk. Two preliminary drive crossings are removed; subsequent
checks intersect the actual exported-source paving polygons. Staff accesses
have curb openings. The loading positions are empty sockets, not cars used as
bus substitutes. Native cars are unmodified source instances in presentation.

Still CG in this pass: blank surrounding ground, regular small glass backings,
sparse foundation planting, identical red palettes, and site color wear too
subtle at full frame. Those are rejected issues, not acceptance claims.

## Pass 8 — second aerial and loading-lane review

**Color and value first.** Opened all six 1200 px native views in
`renders/look-pass2/`. The neutral-balanced McDowell spandrel and Walls curb
remain the comparison neutrals. The buff court school was too light under
the same exposure; its brick tint is reduced from (.36,.285,.19) to
(.29,.225,.135) in linear RGB. The compact school's brown brick and narrow
original slots now separate it from the earlier schools at full frame.
Window shadows, dark door recesses and deep canopy shadows survive the bake.

The mid-block loading curb now reaches the entry walk and the two drives
have separate street aprons. The corner school's gym is on the opposite
side of its office from 101; the park-backed compact school has its staff
lot and bus loading on opposite approaches. Above views show three distinct
parcels rather than two identical rings. Blacktop paint reads as school
games, with the playground reservation and practice field beyond.

Rejected four remaining visible issues: the compact school's entry tree
still blocked its canopy, the compact blacktop touched too little classroom
wall, the courtyard glazing retained an unnecessarily high sill, and the
east horizon was empty. Move the tree out of the approach ray, extend the
yard across the 1991 addition, lower the original courtyard window wall and
add the missing native house/street row and distant trees. The replacement
upper panels remain distinguishable from the original steel sash.

Construction review also found an incorrectly oriented finger-wing ridge
and HVAC curbs whose flat bottoms did not seat on pitched roofs. The ridge
now follows the long wing; curbs have four independently checked sloping
bottom corners. Eave and monitor end closures are actual surfaces. A new
classroom yard door exposes a downspout conflict: choose a clear masonry
pier from the actual opening intervals, then align its weather mask to the
same station. Entry paving now grades from the loading curb down to the
floor instead of touching the operating leaves. These changes require a
fresh export and independent clearance checks, not just another picture.

Still weak: grass is a broad shared tiling surface, roof ballast is coarse,
the native houses and vehicles have a different level of finish, and the
small mineral repairs need the close-up photo pairs to judge their scale.

## Pass 9 — exported detail review, before photographic acceptance

**Color and value first.** Opened all 27 native 1200 px Cycles views in
`renders/look-pass3/`: nine per school, including the heroes, aerials, rear,
window, canopy, gym, hardware, roof and blacktop. The reduced buff brick
retains a warmer light value without the previous pale facade. Deep canopy
and glass shadows remain, but the west-facing finger window view is too
dark to assess sash paint. Give each detail its exposed-side sun direction;
do not lift the whole scene's exposure. The gym-door view of 103 also needs
its own face-facing sun. The balance assumptions remain the concrete curb,
painted spandrel and monochrome fascia recorded in `reference-balance.json`.

The lowered court glazing now reads as a window wall, and the 1970s slots
read as a different design. The compact entry is clear after the tree move,
but the hero is too distant: move farther along its actual parent approach
to put more of the building in frame. The separate bus curb, pedestrian
plaza, staff connections and real street aprons read in all three aerials.
The compact blacktop now abuts its later classroom wing. Games, tetherballs,
hoops and the neighboring playground reservation replace the former small
futsal enclosure.

Rejected the roof's broad repeating checker: the shared asphalt's four-cell
low-frequency manufacture is too large at the provisional .8m roof repeat.
Use a .2032m repeat for its fine roof aggregate and reduce the normal strength
to .65. This changes physical scale, not the canonical maps. Roof vent bases
also now follow the actual pitched plane. The rear cameras formerly hid the
kitchen behind the gym: move to the service side and raise the eye so both
the yard and service compound can be inspected together. The repeated single
colonial house is a distracting tell; vary the context with the unchanged
native ranch and cape generators and setbacks. Keep native cars intact.

Remaining CG tells: regular interior blinds/backings, very even lawns, crisp
door-paint chips, repeated native foliage, simple HVAC forms and a shared
brick tile whose repetition is visible in long close-up walls. These are
look limitations to judge against the forthcoming photo pairs, not facts
which a serialization check can approve. No final documentation image is
written or committed in this pass.

## Pass 10 — full-size roof rejection and final binding change

**Color and value first.** Opened all fifteen 1400 px views produced for 101
in the interrupted `renders/lookdev/` run. The red brick retains its color
in raking light; the canopy cavities stay dark, and the front concrete and
steel highlights roll off without a white wash. The same-camera views also
show why that older, cooler light is unsuitable as the new hero lighting.
The human scale view seats its feet on the plaza slope.

The .2032m roof repeat still produces a visible grid at full size. Rejected
it and stopped the render batch. Roof cover now uses the already-baked
CommercialConcrete mineral grain at a coarser 4.8768m repeat and stronger
normal response, rather than Ground's four-cell binder clouds. Roof and
sill materials share their images. A building now loads twelve images / 25
MiB instead of fifteen / 41 MiB; the campus already loads the Ground maps,
so its shared allocation remains unchanged. This is a material-scale reuse,
not a new school bake or a claim that cement and roofing are the same finish.

The raised rear camera reveals the kitchen but clips part of its enclosure
at the left edge. Widen the lens to 35mm and aim toward the service side.
The new window-side light makes the steel sash and its small lower chips
read; the glass remains too uniformly reflective and the simple room
backings are visible. Roof refinement must be inspected again before the
full batch resumes. No image from this interrupted run is final evidence.

## Pass 11 — photographic visibility and color/value corrections

**Color and value first.** Opened the three native exported views and all
three 2200 px pairs in `renders/pairs-pass5/`, then both corrected pairs in
`renders/pairs-pass6/`. Walls' neutral-balanced curb exposes a gym wall too
warm/light in direct front sun. Match the photograph's shaded front instead
of raising exposure, then reduce the compact gym's red component and albedo
to (.14,.09,.055). McDowell's balanced white spandrel exposes our panel at
roughly half its relative height. Keep the low rough opening, increase the
panel from .22 to .45m, and give it maintained warm-white paint. The glazing
still occupies most of the facade, nearly to the ceiling. Emerald's neutral
monochrome fascia comparison keeps the column/deck heights credible; its
different district paint and massing are not reproduced as a replica.

The first new original-sash ribbon fit rendered black. Its mathematically
projected landmarks passed the kit solver, but the camera lay inside the
later row. Reject it. Fit the unobstructed original south window in the
courtyard gap with a tighter reference crop and a bounded 22–25mm lens.
The new independent plan check rejects cameras inside any building block.
This is a feature/type fit with explicit residuals, not lens recovery.
The corrected pair is readable and shows the remaining lack of interior
activity and varied glass response. The gym's foreground tree also moves
out of that comparison ray while remaining a real planted parcel tree.

Opened the two `renders/look-pass5/101/` views: the mineral roof binding has
lost the rejected regular grid and the widened rear includes both the
service compound and blacktop. Its aggregate is still subdued; it does not
yet provide a convincing macro photograph of loose ballast. Do not spend
thousands of geometry pebbles to conceal that shared-map limitation.

The original checkpoint is now rebuildable in an isolated archive from
`1fd7b37`, without another worktree. Its six original binaries reproduce
byte for byte and all original counts/bounds agree. This makes the literal
before/after evidence reproducible after a clean, rather than relying only
on copied PNGs. No reference pixels enter either material pipeline.

## Pass 12 — final exported batch and source/export loss check

**Color and value first.** Opened all 45 final 1400px Cycles views, the three
exported photo pairs and the three source pairs at native size. Hero display
luminance p1/p50/p99 is .006/.420/.793 (101), .056/.487/.762 (102) and
.000/.408/.796 (103). No hero clips all three highlight channels. These
whole-frame image statistics describe exposure, not measured surface albedo.
Walls' concrete curb, McDowell's painted spandrel and Emerald's monochrome
fascia remain the balancing neutrals. The gym comparison's front is shaded:
reducing sky fill from .16 to .08 brings it nearer the photograph without
changing hero exposure or raising the masonry albedo.

The final pairs have landmark RMS 18.19 / 35.73 / 8.15 native pixels for
gym / ribbon / walk. The 25mm ribbon lens sits on its explicit bound; it
is an estimated planar feature fit, not a recovered photographic lens.
Projection agreement below .005px verifies the solver-to-Blender transfer,
not photographic likeness. Comparing source/export image RGB gives mean
absolute display differences .029% / .064% / .531%. These include sampling
and representation differences and are diagnostics, not a physical accuracy
score. Neither pair has the earlier black/occluded sash failure.

The three aerials read as distinct parcels with entry loading attached to
the walks, different frontage counts, gyms, yards and fields. The wider
rear views retain both service compounds and school games. Opened the
literal old-camera hero/aerial pairs as well: the unchanged camera now
looks at a different facade after 102/103 turn. Those are honest world-camera
comparisons; the new targeted windows and heroes are the useful look views.
Twelve before/after pairs each retain 1400px panels and zero camera residual.

The rotated scale views initially carried the kit figure's offset in world
space, placing it against the wall. Parent the complete silhouette under
the campus heading, then rerender 102/103. Opened both corrected views; the
figure stands on the graded plaza beside the entry. The first Eevee preview
had opaque white glass: apply the library renderer's ray-traced slab
refraction and sky/bounce cache. Opened the corrected preview. Glass now
reads correctly; foliage and its shadows remain less faithful than Cycles.

Remaining CG: overly even lawn, abrupt shortcut edges, repeated native
context/foliage, sparse room backings and regular blinds, crisp paint chips,
repeating brick in close-ups, simple HVAC and subdued loose-grain roof detail.
The small mineral repairs remain too weak in distant hero framing to claim
photographic aging. This is review evidence, not portfolio-photograph
acceptance. No gallery or `docs/` images are produced.

The occupied-parcel cost must remain explicit: static campuses are
275,916 / 281,641 / 258,005 triangles, but two unmodified native car actors
add 116,064. Including those actors gives 391,980 / 397,705 / 374,069,
above 300k if moving vehicles are charged to the site ceiling. That is a
budget exception for review, not an assertion that a different mesh count
made the same scene cheaper. No car reshaping or school-specific LOD is used.

`make` completes the full graph; `make repeat` passes all 49 external
geometry/image files; `make check` and the shared-image audit pass. The
final render audit finds 45 current exported views and three current export
pairs, plus source pairs, all with the expected package hashes. Physical
checks measure 35 rooms, 43 exterior leaves through 903 sampled poses and
22 equipment-curb seats; serialization checks preserve counts, bounds and
pivots independently. All 772 prior non-school delivery files are unchanged.
The report is `LOOKDEV.md`; work stops at the requested look-dev checkpoint.
