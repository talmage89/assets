# Main Street construction and delivery review

This log starts at the quick-material construction gate and continues through
baked export and delivery review. Early placeholder surfaces and rejected
controls are historical evidence. The last pass gives the current verdict.

## Pass 1 — first Midwest shell, Workbench (imported checkpoint GLB)

Evidence: `renders/workbench/contact.jpg`, all five constituent views inspected,
against `build/references.jpg` (three actual HABS photographs and measured plan).
Value first: the reference has deep windows and a clearly brighter trim than
masonry. The placeholder colors preserve that hierarchy; Workbench cannot
judge transmitted daylight, material albedo or the final tonal range. The two
monochrome photographs offer no hue evidence; the color photo's neutral is its
sidewalk/white sash, not blue shadow. No color was sampled into an asset.

The seven lots read as a commercial row, with a useful one-story interruption.
The tall display floor, tight window cadence, recessed sash and substantial
cornice projection work. Three form faults need correction: the transom band
collides with masonry above the storefront opening; the corner's lower return
is an implausibly long blank bank wall; the northeastern bay-window flag has
no geometry yet. Fix the band levels, add public-side display openings, and
build the bay as an actual projecting three-plane assembly with supports.
Rear platforms and stairs exist, but the flights need a closer physical check.
The repeated HVAC boxes and very consistent sash treatment remain visible CG
tells that variation/detail work must address before look-dev acceptance.

## Pass 2 — all four towns and independent motion audit

Evidence: `renders/pass2/contact.jpg` (all twelve images inspected) and the
first imported-door sweep. Color/value still uses the first pass's explicit
neutral references; Workbench is useful for form but too dark for a material
approval. The western one-story skyline, denser northeastern row with a real
bay, and southern posted galleries distinguish the towns. They share more
window detail than the photos do; that is a remaining grammar limitation.

The across/overhead/rear cameras crop the end buildings: widen those views.
The motion check found real problems that the pictures concealed: a retail
floor was 34 mm too high, the stair leaf overlapped its cast pier, and service
and corner hinges sat too far out in thick masonry reveals. Lower the shop
floor to grade, narrow/center the stair leaf within its clear opening, inset
the retail leaf behind its glazing returns, and put the other two hinges
behind their thick reveals. No collision exemptions or looser tolerances.
The repeated roof equipment is still too regular; vary its position/count and
add brick chimney masses before the next form review.

## Pass 3 — source photo pairs, regional overview and door corrections

Evidence: all twelve `renders/pass3/` views and the three Workbench preview
pairs in `renders/match-preview/`, inspected individually. The same neutral
references apply; these preview materials are darker and more uniform than
the photographed masonry and are not a look-dev result. The black and white
images constrain proportions/value only. The photographed painted window
is balanced against its pale sash and sidewalk; the low-resolution color
preview is unsuitable for a precise albedo claim.

The photographed cast front has shallower sash recesses and more shaped
cornice brackets than our first model. Italianate fronts now use 105 mm sash
inset, cream hood molds and profiled pressed-metal brackets; thick brick
Romanesque reveals remain 190 mm. The photographed upper floors have more
varied sash/hood condition; filled openings and causal weather remain next-gate
work. The bay window's supported projection reads well. The western skyline
is suitably low, while the northeastern and gallery blocks read denser.

The first whole-row cameras still clipped a corner in overhead views. They
now fit actual imported architecture bounds with explicit margins. The
Mulberry match compares the continuous street wall, not the exact landmark
building: our chamfer, roof and fire-escape location intentionally differ.
The Foster match compares one retail frontage, not the original two-store
building. The color-window crop is a weak calibration at grazing incidence;
its residual and lens bound are disclosed, not hidden by an overlay.

Further sweeps found a 4 mm threshold overlap, a dropped infill ceiling that
hit the door head, and the corner leaf opening into an interior display-room
partition. Thresholds, ceiling and corner-lobby partitions are corrected.
No tolerance change or collision exemption was used.

A further construction review of the rear found that the early diagonal
flights did not meet the next landing on three-story buildings. Replaced them
with stacked parallel flights along the rear wall, deeper end landings and a return walk and
an open stair lane. This preserves headroom over the flight, joins each flight end
to an actual lower landing, and gives the first flight feet on grade. Wall
braces now reach their anchor plates. The earlier attractive overview was
not sufficient evidence that the stairs could be used.

## Fine motion verification while the GPU queue was occupied

One-degree sampling found a 2.3 mm corner-leaf collision at 24° that five-degree
sampling missed. Moving the first side display opening farther from the
chamfer preserves a clear lobby. A separate 58° result was a ray-parity false
positive: oriented-triangle winding was −.004 in air, versus about 1 inside
the actual masonry. The downtown audit now uses that membership test while
retaining the kit's BVH/edge intervals, nearest distances and 1 mm tolerance.
Positive and negative fixtures cover abutting/overlapping members, hollow
frame air and a fully contained collision. All 89 doors pass at 101 positions
each with zero measured penetration. No shared kit behavior changes.

## Pass 4 — Cycles form review of exported quick-material blocks

Evidence: `renders/pass1/contact.jpg`, the 35 mm hero review and all twenty
first complete Cycles gallery views. Color/value first: untextured brick is
much more even than the photographs, as expected at this gate. The pale trim
is separated from red/buff masonry, storefront cavities stay deep, and the
hero's highlights do not clip. The photo's pale sash/sidewalk are the color
comparison neutrals; no photographic pixel has become an asset texture.
Final material/albedo and wear calibration is expressly deferred.

The full row and parked pickup/crossover/hatchback read at eye height. The
first 40 mm composition lost too much of the near row; the 35 mm camera stays
on the opposite walk and shows the corner and the row beyond. The four
skyline rhythms remain distinct; the southern gallery's deck, posts and rails
read as supported construction. The new fire escape has real end landings and
readable flights. Rear shots retain deep shade rather than a pale wash.

The close-ups caught two presentation/construction mistakes: a date stone was
behind brick corbels, and the ghost-sign view cropped its lettering. Reserve a central frieze field
for the date panel, clear of brackets/corbels and aim the side view at the actual sign center.
Show the profiled metal cornice in its close-up, with the brick cornices still
visible in the block elevations. A support pass also corrects furniture feet,
chair columns and roof curbs after the shop floor was lowered to grade.

Remaining form limits are deliberate but visible: the sashes and rear service
layout share too much vocabulary, cornice ornament is coarse, room dressing is
boxy, and the street ends use simple right-angle curbs. The sign is a form
placeholder, not a convincing painted-brick ghost yet. The source vehicle
forms are context, not the accepted baked car deliveries. The final texture,
weather, window vinyl and night-light work belongs to the next gate.


## Pass 5 — taller sash proportions and construction contacts

Evidence: all twenty window-revision Cycles views and all three matched pairs
inspected. Value first: the archival pale sash and sidewalk remain the stated
color neutral; the monochrome pairs constrain value and proportions only.
The quick masonry is still much more uniform than the photographed brick.
Material approval is deferred; the render does preserve dark entrances,
shaded undersides and separated light trim.

The Foster pair exposed overly short upper windows. Increase Italianate
openings to 2.20 m and Romanesque to 2.14 m; keep plain commercial openings at
1.96 m. These fit the existing 11–12 ft floor modules and distinguish styles
without adding window silhouette segments. Re-rendered pairs show a better
tall-sash rhythm. The surveyed facade still has more elaborate hoods and
cornice relief; those differences remain visible and belong in the shared
ornament source rather than extra repeated game-mesh faces.

The corrected side camera exposed a more serious mistake: the old ghost-sign
rectangle crossed a display-window opening. Move it and the demolished-neighbor
outline onto uninterrupted masonry, and assert the sign field clears every
opening. The new close-up verifies the placement. Its opaque painted rectangle
still reads as a printed panel; this is a quick-material placeholder that must
become worn paint integrated with brick at look-dev.

A contact review also found gallery feet above grade, a flat skylight curb
below sloping glazing, and missing short blade-sign hangers. Correct the feet
and canopy column caps, build a four-sided inclined hollow curb whose flashing
intersects the falling roof, add the hangers and seat the masonry tie plates.
Independent rays on the actual exported surfaces now measure gallery feet at
grade, 20 mm curb-base overlap into the roof, and glazing-to-side-rail gaps
below 1 micrometer of mesh precision. Those numbers establish geometric
contact; they do not certify structural capacity or field construction tolerances.


## Pass 6 — final exported checkpoint, Cycles

Evidence: every view in `renders/checkpoint/contact.jpg`, all three pairs in
`renders/matches/contact.jpg`, and the full-resolution final hero inspected.
The audit confirms all 23 views use the current exported GLB hashes, the
Cycles engine and the recorded camera/context. The 35 mm hero is at 1.68 m on
the opposite sidewalk with the pickup, crossover, hatchback, trees and lights.

Value first: the final hero has deep storefront/awning cavities and bright
trim with smooth highlight roll-off. No RGB channel reaches 255; display-luma
5th/50th/95th percentiles are 4.93/68.19/192.90 on the 0–255 PNG scale. These
are display diagnostics, not measured albedo or a final material approval.
The photographic neutral remains the pale sash/sidewalk; monochrome pairs
remain form/value evidence only.

The Midwest infill interrupts an otherwise two-story cadence, the western
row stays low, the northeast has a denser three-story street wall and a bay,
and the southern gallery reads as a supported continuous sidewalk frontage.
Store entries, transoms, separate stair doors, upper openings and cornices
read clearly in their close-ups. The ghost field clears the display windows;
the revised date panel is legible. Rear service volumes and usable escape
landings are visible, though the shaded rear close-up remains deliberately dark.

The remaining CG tells are the flat/unworn masonry, simplified cornice relief,
repeated rear equipment and sash detailing, simple room furniture, and the
printed-looking ghost sign. Source vehicle forms are presentation context.
Archival matches are approximate original-family comparisons: RMS residuals
are 6.85/10.56/5.46 pixels, and the grazing window crop reaches its 100 mm lens
bound. They are not exact reproductions of the pictured facades. Stop here,
before brick/trim look-dev, wear, final UV/bakes and night lighting.

## Pass 7 — inherited checkpoint rejected for ornament, before look-dev

Color and value first: inspected the native hero, storefront, corner, cornice
and pair sheet from 889d811. The plain red walls have no kiln range or mortar;
the green storefront and pale trim have almost no manufacturing response.
The HABS Foster and Mulberry photographs cannot constrain hue. For the new
color comparisons the stated neutrals are Auburn's sunlit pale concrete curb
and Galena's distant white painted facade. Both are assumptions rather than
calibrated gray cards, and their channel gains will be recorded with the fits.
The winter Galena photograph also has wet/snowy paving; it will not calibrate
a dry downtown street.

The inherited cornice has too little depth and only single coarse brackets;
the hoods are shallow bands, the piers rectangular, and the awning's 65 mm
sag over tiny panels reads rigid. The bank chamfer technically exists, but its
unframed door makes it read as an accidental side opening. Repeated rear
service blocks and identical sash undermine the alley. The cropped reference
pair is especially blunt: Foster's keys, ears and paired scrolls are missing.
The accepted proportions and street rhythm remain useful and are retained.
The inherited hero's horizon and opposite side are visibly empty. These are
rejections to fix, not claims that texture alone will rescue the silhouette.

## Pass 8 — first baked exported surfaces and town, Cycles

Color and value first: opened all nine native `renders/pass8/` images (eight
Midwest views and the northeastern iron storefront) against the Foster,
Auburn and Galena photographs. The brick is too orange and the mortar too
bright/clean. The buff brick is also too yellow. Trim keeps deep underside
shadows, but the bank's entire lower return has become a smooth pale mineral
wall, including the ghost-sign substrate; that is the wrong construction.
The dusk sky and unlit surfaces are too dark to read. The stated photographic
neutrals remain the unpainted Auburn apron and Galena white facade; HABS is
form/value evidence only. No quantitative color approval is claimed yet.

The new hoods/keys and paired cornice brackets read in silhouette and throw
useful raking shadows. The scrolls still look faceted, and the date panel is
crowded by brackets. Canvas is unacceptable: excessive panel sag plus dark
striping/normal response creates triangular black folds. Reduce the sag and
cloth normal amplitude, then judge the connected smooth surface. Close-up
windows still reflect a bare horizon because context was removed for those
cameras. Retain the town in glossy rays for close-ups. The ghost field loses
paint, but its rectangular cadence and masonry mismatch remain obvious.

Both sides of the hero's street now exist, with a continuing junction, cars
and lamps. The near opposite tree dominates the center, the foreground walk
is oversized and the principal row's cornice is cropped at the left. Raise the
aim slightly and thin the nearest opposing canopy. The dusk needs a brighter
blue-hour environment and more readable shop/window light. Wear is still too
weak at full-frame hero scale: improve located sill/drain/low-wall effects
rather than putting a global gray film over these already saturated bricks.

The independent checks also found a UV issue on almost-horizontal arch filler
faces: mixed Python/float mesh precision made a nominally horizontal face use
a vertical chart. Classify those faces by normal as well as height range.
The first motion audit found a raised-lobby/stair-door conflict and an ell
membership result. The landing notch and shared per-solid vertices are now
implemented; rerun the same checks without exemptions or relaxed limits.

## Pass 9 — second exported bake and comparison-camera rejection

Color and value first: opened all ten native `renders/pass9/` views, and all
six `renders/pass9-matches/*-pair.jpg` files. Reducing orange chroma and mortar
value removes much of the pale toy-brick effect. The bank's exposed return is
brick again; ashlar remains confined to its public ground floor. Deep cornice
cavities survive the bake, and the reserved center panel separates the date
from the paired brackets. The dusk now reveals architecture, but is still too
gray and daylight-like. Use a blue-hour sky balance with warm room lights.

The first Galena display-value statistic is withdrawn: the inspected native
crop crosses the hanging candy sign. Correcting that ROI also exposed wrongly
identified window-head landmarks in the low-resolution image. The Auburn
storefront-only fit had put the effective camera above its awning. Neither
fit is retained in active calibration or used to tune material albedo. Add the
much sharper Paul Sableman Louisiana color photograph, balance its pale hood
fascia (native pixels 836,1222–849,1233), and compare its actual glass corners.
This cropped-detail fit has unknown original lens shift/perspective correction;
its estimated camera is a framing device, not a recovered survey position.
Auburn's wide street comparison retains the sunlit concrete neutral. HABS
continues to judge form, not hue. The authored facades differ from the pictured
ones; report residuals rather than claiming a reconstruction.

Foster's principal hoods remain arched where the photograph has pediments.
Give the original Italianate iron fronts peaked hoods and omit the conflicting
arched headlight. The remaining canvas defect is geometric: longitudinal sag
passes below straight ribs at the panel boundaries. Retain cross-bay sag but
seat those edges on their ribs. At full-frame scale the sill runoff is still
too weak: add color vertices around the actual sill edges and darken narrow
runoff below those edges, preserving the painted/masonry substrate's hue.
No global noise overlay is warranted. Next pass must include every town's
fronts and rears, the parked cars with their original exterior construction,
and all revised matched-light views.

## Pass 10 — complete town/export set, camera and lighting corrections

Color and value first: opened all 24 native 1440 px Cycles views in
`renders/pass10/`, all five active exported photo pairs, and both 1000 px
overcast lighting controls. The Louisiana pair exposed an unacceptable blue
cast from using a clear sky with its sun disabled. Replaced that environment
with neutral diffuse procedural overcast light, then adjusted its exposure.
On the stated painted-brick pier the first blue result was Y′ .604 versus the
balanced photograph's .529. The neutral-light control was .317; increasing
exposure gave .575. The final exposure interpolates between those controls,
with a small correction to the authored putty paint's yellow bias. These are
display diagnostics, not inferred reflectance. Recheck the actual cold export.
The Auburn photo needs the higher summer sun indicated by its short shadows;
its earlier low sun put the comparison pavement in the opposite row's shadow.

The new pediments, iron supports, washed sills and paired cornice brackets
survive the exported textures. Canvas now lies on its frame and shows sag
and a hanging valance without the protruding black ribs. The corner's two
risers, framed diagonal leaf, heavier base and mineral name panel read as an
entry rather than a stray side door. Ghost paint exposes the coursing and has
lost the printed solid field; its single-line fictional typography remains
simpler than many real multi-layer ghost advertisements. Sill weather remains
too weak down the street; broaden the narrow runoff slightly. Add localized
oxide runoff from the actual fire-escape plate fixings, not random rust spots.

The roofs, ells, parapet steps, changing rear sash and stairs now give different
alley silhouettes. Identical rooftop units and backings remain economical CG
tells. The rear views expose the edge of the presentation neighborhood: extend
its grades, house row and background trees. The hatchback's apparent white
scabs were overlapping fitting-cage geometry, not intentional rust: the source
exterior builder retained an unparented cage. Exclude source helpers and retain
only the actual vehicle assembly. No car source or delivery is changed.

The southern across view is obstructed by the opposite gallery's railing.
For these diagnostic elevations use an explicitly recorded foreground cutaway
of the opposing row/lamps/trees; preserve the complete town in hero, dusk,
overhead and rear views. Add a three-quarter cornice-profile view and a whole
peaked-hood close-up; the old close-ups cannot show both ends of those parts.
The dusk reads as blue hour with lit shops and selected upper rooms, but the
street emitters/pools are weak. Raise their presentation emission and power.
The current raw/imported/motion audit passes all 28 buildings and 107 leaves;
32 building/street glTFs really share eleven imported image datablocks. These
checks prove construction/resources, not photographic appearance.

## Pass 11 — first complete cold build, full-resolution judgment

Color and value first: opened all 26 native checkpoint views, all five active
pairs, five original-4096-field comparison renders, the Eevee view and all
seven native before/after panels. Louisiana's balanced brick patch now reads
Y′ .52883 in the photograph and .52855 in the exported render; median RGB is
(.533,.529,.514) versus (.533,.529,.506). This agreement applies to that stated
patch and assumed neutral, not every facade or a physical albedo measurement.
The blue-clear-sky error is gone. The hero keeps dark cavities and controlled
highlights (p05/p50/p95/p99 3.9/76.7/210.7/217.8 in 8-bit display values;
four pixels with a channel at 255). Dusk has visible warm lamp pools, selected
upper rooms and shops. No pale-overcast hero is substituted for the raking sun.

The constructed hood, entry, iron support, washed sill, canvas and alley changes
are clear beside 889d811. The added whole-hood and three-quarter cornice views
resolve the earlier cropped detail evidence. Remaining frieze relief is too
shallow: both the original source fields and baked export show nearly blank
panels. This is an authored-height miss, not bake loss. Deepen the stamped
rosette field from 1.8 mm to a 12 mm relief with a small central boss, retaining
all game-mesh triangles and the same finish allocation. Raking light must then
show it in the delivered map. Fine brick pores are softer in the downsampled
normal, as expected; profiles, courses and guards remain intact.

The first complete build/check passed. All 32 building/street glTFs share eleven
actual imported images; 107 leaves clear their 101 sampled positions without
exemptions. The bank risers measure .14999992/.15000010 m. The town's houses,
trees and continuing street improve the hero, but the high rear views still
expose an empty strip behind the neighborhood. Add instanced commercial rows
on the next parallel streets and move the houses beyond them, preserving
street/sidewalk interfaces and keeping these meshes outside delivery. The
Eevee comparison exposes opaque white transmission fallbacks; enable actual
Eevee ray-traced refraction/fast GI before judging that engine. A second cold
build will verify these last material/presentation corrections. No docs images
are committed.

## Pass 12 — final visual set and independent GPU-repeat failure

Color and value first: inspected all 26 new native checkpoint renders and all
five exported pairs after the deeper relief and expanded setting. The neutral
Louisiana paint comparison remains close in hue/value; the HABS photographs
remain form-only evidence. Cornice rosettes now respond to the raking sun,
without adding triangles. The high views contain surrounding commercial rows
and houses beyond them. These repeated background seeds and repeated roof units
still reveal the procedural presentation at aerial distances. Sill runoff,
low-wall deposits, fixing-plate oxidation and ghost losses are localized;
the town remains maintained rather than uniformly derelict.

Opened all five original-field renders and the Eevee comparison. Fine source
pores are softened after shipping; course/joint response and larger relief
survive. Eevee still showed pale fallback panes. Blender's documented default
thickness comes from the smallest dimension of the *object*, which here is a
joined building. A presentation-only explicit 4 mm slab thickness now prevents
it skipping the room; inspected the 1000 px control. Its approximate glass
remains more reflective and less convincing than Cycles.

The independent repeat exposed real GPU numerical nondeterminism in the
8-sample flat data bake: all nine original field PNGs and geometry buffers are
byte-identical, but six shipped maps differ at 136 pixels by at most one 8-bit
code. Embedded diagnostic GLBs consequently differ too. The strict byte test
was not relaxed. Two independent 4096 single-sample bakes and ship filters are
now byte-identical for all ten generated ship PNGs. Emission/tangent data need
no stochastic lighting integration; the original 4096 raster plus the
channel-aware ship filter supplies the footprint antialiasing. Use one sample
and rerun the full cold pipeline and strict independent bake/export repeat.
The one-sample BaseColor mean source errors are .0000144 / .0000835 / .0000125;
mean channel biases stay below 2.4e-8. This is a precision correction, not a
texture-budget change.

## Pass 13 — cold delivery and final native-size review

Color and value first: opened the final 26 native Cycles views, all five fitted
export/photo pairs, the focused Foster storefront pair, five original-field
renders, all seven native before/after panels, Eevee and both contact sheets.
Louisiana's assumed neutral remains the pale hood fascia. Inspection of the
measurement overlay caught the old tall brick rectangle crossing a wall anchor;
the earlier .52883 photo median is superseded. The clear brick rectangle is now
(1006,1490)–(1050,1590), above that hardware. Balanced photo / exported render
Y′ medians are **.53108 / .52574**, RGB (.533,.529,.518) / (.533,.525,.506).
The painted brick is close in value and slightly warmer in the render; its local
contrast remains narrower than the photograph. These are display diagnostics
under the stated neutral and light assumptions, not measured physical albedos.
The Auburn cream wall does not calibrate our original red-brick facade.
Hero p05/p50/p95/p99 are 3.86/75.80/210.75/217.81 in 8-bit display values,
with four pixels having a channel at 255. Cavities and shop recesses stay deep.

The seven panels in `renders/fixes/` retain 1440 native pixels on each side:
cornice, cast-hood, washed-sill, iron-piers, canvas, corner-entry and alley.
The dated source is rebuilt from 889d811. The scroll pairs, cyma/bead profiles,
modillions/dentils, ears/keys/consoles, washed/dripped sills, iron bases/capitals,
canvas bay sag/valance and bank's diagonal framed entry are clear improvements.
The bank's two risers independently measure .14999992/.15000010 m. Rear ells,
additions, porches, sash changes and parapet steps give differing silhouettes;
the retained escape assemblies and all 107 leaves clear their sampled ranges.

Low splash, sill/scupper runoff, fixing-plate oxide, folded-paint losses and
ghost lettering's broken coursing have identifiable causes. They remain
restrained on maintained buildings; the hero's sill streaks and masonry repair
variation are visible, while the narrow fixing streaks need the close-up.
Ghost typography is still simpler than a real wall carrying several generations
of advertising. The two-sided street, parked family vehicles, pit trees, lamps,
tenant belongings and next crossing improve the eye-height setting. The high
views still show repeated neighboring seeds and unfinished-looking open grades
at the edge of the presentation district.

The five source-field comparisons expose real shipping loss: fine pores and
floral-normal contrast soften, especially under the overcast light. Larger
profiles and coursing survive, and the relief reads under the raking sun, but
the normal-map frieze is weaker than its 4096 bump-field source. The faceted
bracket cages, blank hood fields, simple capitals, regular pavement/roof units
and repeated shallow room backings remain CG tells. Eevee's explicit pane gauge
removes the white fallback, but its glass still hides more of the rooms than
Cycles. This checkpoint is not a claim that those close-ups are photographic.

`make clean` followed by the complete `make` finished with exit 0; it resumed
the same cold build after two command-session SIGTERMs during context creation.
The subsequent separate `make check` passed raw/import/construction, 10,807 door
positions, charts, normals, 4,000 deterministic plans and actual eleven-image
reuse across 32 deliveries. `make repeat` independently regenerated the fields,
4096 GPU bakes, delivery filters and geometry: **79 files byte-identical**, no
tolerance or copied maps. The repository check reports **1598 source files,
zero errors**. Logs and exit receipts are under the worktree's ignored `build/`.
Family delivery is 77,991,841 bytes, including 17,475,265 shared-image bytes;
the compressed mip allocation remains 42⅔ MiB. All class budgets pass.
No kit changes, docs-image commits, or changes to other families' deliveries.

## Pass 14 — accepted look reopened; first exported corrections

Color and value first: inspected the seven handoff images at native resolution,
Foster's larger HABS photograph, both original color photographs, and all six
1440 px `renders/pass14/midwest/` exports. The assumed color neutrals remain
Auburn's sunlit concrete apron and Louisiana's pale hood fascia; the HABS and
NPS ghost-sign photographs constrain form/value only. The sidewalk is darker
and has joints on the opposite side too, but its broad regularity still reads
as CG. The brick's runoff is still insufficient in the hero. No quantitative
color acceptance is claimed for this pass.

The corner bay is now 1.80 m on each street edge, with a narrower hinged leaf,
a real separate transom and stone piers within the diagonal, plus ashlar on the
public return and a continuous base/water table. Its actual corner planes still
need independent measurements. The new scrolled modillion profiles are visible
under the crown, although the leaf normal must be finished. The pier's paneled
shaft, molded base/capital and original maker plate need their focused crop.

Rejected: the ghost wall's remaining parging appeared as evenly distributed
polygon patches, with an unintended buff chart and an ashlar boundary crossing
the old roof scar. Remove the isolated patches, retain the softer old interior
brick and flush slope stains, force the original red chart, and stop the stone
return before this former neighbor. The shop light's broad area appeared as a
white rectangle in specular rays; hide that presentation emitter from glossy
rays while retaining the actual fixture. Reduce pane roughness to recover a
legible street reflection. The raised street-light power was too broad and
washed out dusk. Move emitters clear of their housings and use a downward spot
with a soft pool. These are failed controls, not final evidence.

All edits remain in downtown. Main was not actually an ancestor at handoff;
merged its utility/signal deliveries without conflict. No other family's
export existed in this worktree, and none has been generated or edited here.

## Pass 15 — same-camera export controls, form still short of the gate

Color and value first: inspected every native `renders/proof/` image, including
Foster's full-height iron front, against the same original photographs. The
brick and pale trim remain too even beside Louisiana's handled, repainted
surface. The stated photographic neutrals have not changed. The corrected
ghost sign's contrast is now much closer to the barely surviving paint in
NPS Brief 25, page 7 (Thomas C. Jester's Baltimore photograph); this monochrome
comparison does not calibrate hue. The new lower sidewalk value avoids the
near-white slab, but must be measured under Auburn's matched sun.

The filled old openings were still effectively invisible because the standard
masonry path discarded their intended tint. Explicitly preserve the old-wall
chart/tint, break the flashing stain and darken the filled joist pockets. The
paneled iron shafts now have rails, molded bases/capitals, flange bolts and
original foundry plates. They remain dark in the Foster camera's awning shade;
a close view will be needed to judge their construction honestly. The stock
aluminum replacements keep their plain sections.

The lower glass roughness restores cars and the opposite facade in reflections,
with actual shelves visible behind. A broad presentation light still appeared
through the panes: camera/glossy flags alone were insufficient. Disable its
transmission visibility and transmission/specular contribution. The first
118-degree lamp spots spread their energy over too much ground. Narrow to
84 degrees and judge the actual pools; do not brighten the entire dusk world.

## Pass 16 — native Cycles controls and independent corner construction

Color and value first: inspected all six 1440 px `renders/pass16/midwest/`
views. The neutral references remain Auburn's sunlit apron and Louisiana's
hood fascia. The glass now carries two legible depth layers: muted street/car
reflections and warm shelves/room light. The oversized white light rectangles
are gone. Dusk retains a blue ambient shadow with local warm pools; its road
and walks are no longer uniformly lit. The hero still needs a stronger visible
maintenance history: add small mortar-only bed-joint repairs, lower-rail
abrasion and roof membrane repair overlaps, keeping each material's color.

The model audit independently measures the actual diagonal ashlar cut plane,
the return stone face, landing and risers; it does not simply echo the plan.
The 1.80 m edge setbacks fit the requested 4–6 ft range. All door sweeps and
resource/chart checks pass. This proves assembly/serialization, not appearance.

The three-quarter cornice view caught a substantive construction miss: the
modillion's rolled outline and the large bracket's head were buried inside
the horizontal crown profile. Expose both beneath and forward of the shelf.
Keep the stamped acanthus in the existing finish normal strip. Regular brick,
spare hood fields, dark simple iron capitals and repeated room goods still
read as CG; these controls do not yet authorize docs.

## Pass 17 — exposed scrolls and measurement-patch rejection

Color and value first: inspected all seven native `renders/pass17/` exports,
the dry Auburn paving crop with outlined measurement candidates, and the NPS
sign photograph. The assumed neutrals remain the unpainted sunlit apron and
the pale Louisiana hood fascia. A purported sunlit concrete measurement fell
under a parked pickup; discard it. Clear ground candidates show that asphalt
was too dark relative to concrete. Use the aged wearing-course value, retain
darker fresh utility patches, and validate both camera and sun rays through
the actual assembled town. Do not infer physical albedo from those display
values or use the wet Louisiana pavement as a dry-road target.

The newly exposed rolled modillions and bracket heads finally cast their own
shadows under the crown. They are no longer just buried cages with a visible
stem. Their economical profiles remain visibly faceted close up, and fine
leaf detail is weaker than real cast ornament. Ghost paint has lost its field
and most letters, with a broken flush flashing stain instead of a raised rod.
Joist infill and protected interior-brick differences remain too weak. Add
actual local infill tint and remnant lime parging along the scar, without the
rejected regular isolated patches.

## Pass 18 — iron close-up catches an embedded casting

Color and value first: inspected all eight 1440 px `renders/pass18/` images,
including the native full-height iron close-up. Lower-rail scuffing and the
localized dark brick/sill weather are clearer; the maintained block still has
more regular surfaces than the photographs. The paving calibration remains
pending a current render: a SIGTERM stopped the Auburn run, so its old PNG
must not be measured as the new surface. No stale measurement is accepted.

The iron close-up is a rejection. It shows a maker plate and thin panel rails
against masonry because the intended shaft is embedded behind the wall face.
The original 140 mm placement put almost all of its oval section inside the
brick. Move the casting forward to a real exposed pilaster; add an independent
mid-shaft projection ray so a decorated masonry face cannot pass as iron.
Retain the original replacement aluminum fronts. This fixes a construction
mistake without adding triangles. The corner transom also needs a continuous
head rail and jamb linings, with its height responding to the bank landing.

The blue-hour pools now read on both road and walk, with deep intervals and
blue ambient shadow between them. Glass shows warm goods and street/car
reflections without the broad white presentation-light rectangles. The lower
painted rails show localized abrasion, although the goods and their layout
remain simplified. Roof patches, drains and copings must be judged again in
the complete cold exported gallery. Docs remain withheld at this pass.

## Pass 19 — exposed iron, eroded wall scar and clear pavement rays

Color and value first: inspected the native `renders/gate/` iron, ghost and
hero, `renders/gate2/midwest/ghost.png`, the current Auburn render, and both
outlined paving images. The photographic neutrals remain the sunlit unpainted
Auburn apron and Louisiana hood fascia. Clear sample centers pass camera rays
bounded at the lens and unobstructed sun rays through the assembled scene.
The earlier lamp-shadow concrete patch is discarded. Display Y′ is .479
concrete versus .744 in the chosen sunlit photo slab, and .437 asphalt versus
.553/.563/.557 in three photo patches. The render's used paving remains darker;
these exposure diagnostics do not establish physical reflectance. Concrete
actual base color stays mineral gray, with slab changes and located deposits.

The exposed cast shaft now reads as a paneled pilaster over its molded base,
with a cap carrying the beam and a foundry plate at the foot. It is still too
dark in the awning's shade to show fine casting detail as well as the brightly
painted Foster front, and the capital remains simplified. This is disclosed;
the shaft is no longer masonry masquerading as an iron panel. The bank's
actual 45-degree cut, separate transom, landing and return stone remain clear.

The opaque parging control failed: its hard polygon boundary looked freshly
applied. Replaced its coverage with original eroded alpha in a vacant band of
the existing sign sheet, retaining material/image counts and triangles. The
final ghost view now has a soft partial parging/tar remnant following the old
slope, warmer protected interior brick, dark filled joist pockets and mostly
lost field/letters. It reads as a wall's history rather than a new roof rod.
The scroll/modillion silhouettes, glass depth layers, local paving repairs
and dusk pools all show in the native controls. The full cold gallery and
its roof/rear views still require review before any docs commit.

## Pass 20 — cold exported gallery and delivery verdict

Color and value first: opened every final checkpoint PNG at original size:
14 Midwest, five western, seven northeastern and six southern views, plus
the Eevee hero. Opened the five source-look and five exported photographic
renders and their pairs, the native Foster storefront pair, all seven native
accepted/fixed panels, the accepted Foster control, both contact sheets and
the five final docs JPGs. The earlier required handoff images and photographic
originals were also reviewed at native size. Auburn is balanced on its
unpainted sunlit apron; Louisiana on its pale hood fascia, with the same
explicit neutral assumptions used in the fitted pairs.

The cold result's painted-brick median display Y′ is .513 versus .531 in
the balanced Louisiana patch. Concrete is .475 versus .744 in the sunlit
Auburn slab; asphalt .435 versus .563/.553/.557. These supersede the preview
numbers in pass 19. The rendered paving is visibly darker, particularly the
concrete; differing weather, light and unknown photo processing prevent a
reflectance claim. Neither a car nor a lamp shadow covers the rendered sample
centers: bounded camera rays and sun rays are clear. The outlined photo/render
patches were opened again. No wet pavement is used as a dry value target.

| Town hero | Display Y′ p05 / p50 / p95, 0–255 | Pixels with any channel at 255 |
| --- | --- | ---: |
| Midwest | 3.86 / 81.97 / 210.75 | 1 |
| Western | 3.36 / 87.16 / 215.82 | 175 |
| Northeast | 3.36 / 79.39 / 207.26 | 0 |
| Southern | 1.86 / 82.90 / 210.54 | 130 |

Each hero has 1,152,000 pixels. Tiny vehicle/glass highlights reach the display
limit; the building trim rolls off below clipping. Recesses, under-awning
iron and alleys keep deep shade. The roofs stay charcoal rather than pale
gray. Eevee loses the Cycles glass depth and makes the shops milky; it remains
an explicitly labeled renderer comparison.

The four form controls now show their changes at native 1440 px per panel:

- [Corner](renders/fixes/corner-entry.jpg): actual 45° opening, door/transom,
  two steps and continuous stone on front, diagonal and public return. Rays
  on the export measure 1.799999–1.800001 m edge setbacks and return-stone
  face error below 0.000001 m. The upper corner bears on the stone piers.
- [Iron](renders/fixes/iron-piers.jpg): exposed paneled shaft, molded base,
  sill plate, seated maker plate/bolts and capital below the girder. The shared
  diagnostic exposure is one stop above the overview in both panels. An
  independent mid-shaft ray measures 159.723 mm projection from masonry on
  all four original iron fronts. Actual opposed triangle planes measure
  zero capital-to-girder gap; the source correction closed a 15 mm gap and
  connected the core through its collars. Replacement aluminum stays plain.
- [Scrolls](renders/fixes/scrolls.jpg): the rolled modillion noses and bracket
  heads now project below/forward of the crown and cast distinct shadows in
  the three-quarter raking view. The leaf occupies existing normal-map space.
  Its fine ribs are clearer in the source-look pair than after downsampling;
  the exported leaf remains weak and the silhouettes visibly faceted close up.
- [Ghost](renders/fixes/ghost-sign.jpg): mostly lost lettering and field,
  softened broken lime/tar along the old roof slope, warmer protected brick
  and filled joist pockets. The hard opaque parging control was rejected.
  No raised rod remains. The old slope is deliberately faint, visible at this
  distance rather than a new outlined roof shape.

[Hero wear](renders/fixes/hero-wear.jpg) shows darker upper courses, soot and
runoff under cornices/sills, while buff and red masonry keep their own colors.
The close-ups show mortar repairs between openings, handling scuffs on lower
painted rails and thresholds, and low salts/damp/splash at walls and drains.
These are localized causes; fine salt/abrasion marks remain easier to see in
the close-ups than in the overview. Above/rear finals show membrane patches,
drains, copings, stepped rears and hollow additions. Roof equipment and repair
placement still repeat too regularly across the presentation town.
[Glass](renders/fixes/store-glass.jpg) shows lit goods behind street/car
reflections. [Dusk](renders/fixes/dusk-pools.jpg) shows soft warm pools on road
and walks separated by cool blue shadow, without the old broad white shop
light rectangles. Goods are still simple blocks and the rooms shallow.

The construction/visual gate passes for these fixes. Remaining CG tells are
regular coursing and mortar, simplified cast capitals and normal relief,
faceted scroll edges at extreme close range, the repeated roof equipment,
sparse street activity and the empty grades beyond the staged town. The
accepted street setting, triangle envelope and eleven-image allocation are
retained. No claim of photographic equivalence is made.

Cold proof: `make clean`, `make`, separate `make check`, `make repeat` and
`make check-repo` completed successfully. The clean run was resumed after the
capital correction in the same emptied build tree; fields, GPU bakes and
context had already been rebuilt there. The isolated repeat then generated
its own fields/bakes/model from empty workspace and reproduced all 79 delivery
files byte-for-byte. Checks cover 28 buildings, 107 leaves/10,807 sampled door
positions, physical construction, scale, normals, actual UV charts and 32
deliveries plus a repeated import reusing exactly eleven images. No collision
exemptions. Serialization and construction results are separately labeled.
Repository check: 1,696 source files, zero errors before final commits.

Final buildings are 4,788–29,526 triangles; block totals are 95,272 / 69,584 /
135,162 / 121,614. Buildings cost 58,719,324 bytes, streets 5,034,993 and shared
images 17,201,057: 80,955,374 bytes total, excluding diagnostic/context files.
Five/six material states and the existing 42⅔ MiB compressed mip allocation
remain. All 32 Cycles finals and the Eevee view appear in
`renders/checkpoint/contact.jpg`; five fitted pairs plus storefront detail
appear in `renders/matches/contact.jpg`. Five reviewed final JPGs are
192,573 / 198,731 / 195,633 / 199,731 / 199,144 bytes, at most 1600 px wide;
they are committed last, separately from source and prose. No kit change.
