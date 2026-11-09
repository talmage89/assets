# Form and construction review

This is the requested checkpoint before look-dev. Images live in ignored
`renders/`; no checkpoint JPG is committed to `docs/`. All shown meshes are
fresh imports of the external glTF. Quick colors are deliberately not a claim
of baked or finished materials. The expanded signs have their own log at
`street-signs/SET_REVIEW.md`.

## Pass 1 — form, source drawings and software Workbench inspection

Opened every image in `renders/form1/`: hero, complete lineup, shelter/frame,
meter heads, the three news boxes, and speed-limit face. Also opened the used
2006 shelter, 2014 meter, 2008 street news racks and 2012 steel coin-rack
photographs at useful size. The neutral controls for the eventual pairs are
bare paving, recorded as linear RGB gains in `build/photo-calibration.json`.

Color/value first: this software Workbench lighting is too dark to judge
albedo or metal response. It does establish that black cavities, blue paint
and dark structural trim are different values; it cannot approve the final
tonal range. The flat source palette retains dark paint, dark blue and a
cream news box, without adding premature procedural weathering.

Harsh form findings and corrections:

- Bus sign, news mastheads and instrument faces were black/blank. This was
  a real export fault: print quads used PrintUV while joined solids used
  UVMap, so the export sampled a blank sheet corner. Unified the UV name
  before consolidation; the next import must show all original graphics.
- The shelter looked like two oversized sheets rather than a maintainable
  transit structure. Replaced its rear with three narrow replacement bays
  and added intermediate rails, retaining true 9.525 mm glazing, channels,
  column shoes, roof ribs/gutters and the actual slab. The period photograph
  has a flatter roof and heavier round-ended fascia; ours is an original
  shallow barrel roof, not the same maker's product.
- Meter castings were visibly faceted under raking light. The section cage
  already varies width/depth at eight stations; corrected smoothing of the
  loft rather than spending triangles on a bevelled outline. The photo's
  card conversion is deliberately absent from the mechanical dial version.
  The simple vault door still needs an actual opened-state form review.
- News boxes have credible thin walls, base hems, door returns, hinge,
  acrylic, display copy, stack, coin slot/return and small linked chains.
  The overhead coin compartment is too plain; its lock/button detail and
  seam hierarchy need the next close view. Do not use the molded free-paper
  photograph to assert steel gauge or coin-mechanism dimensions.
- Bench straps have real 6.35 × 38.1 mm section, 25.4 mm gaps and a contoured
  seat/back. The center arm and separate anchored supports read; the shelter
  bench's feet were initially below its slab and were raised to slab grade.
- Rack pipe reads as substantial 60.3 mm tube, not wire. Each flange has a
  weld collar and four heads. Row pitch is .9144 m, intentionally per rack;
  triangle allowance is reported per U, rather than calling four U's one.
- Receptacle's liner and open-centered spun lid need a Cycles close view to
  establish the cavity. The slats and welded retaining hoops are geometry;
  perforated-sheet holes are not substituted for a slat construction.
- Collection box has the correct production-size envelope and rolled roof,
  angle-stock legs, service door and a separate chute. The front mechanism
  needs its open pose checked; the lettering is TOWN POST with an original
  envelope mark, no real logo.
- The street composition cropped the near crossing sign, showed the backs
  of furniture and did not give enough room around the meter heads.
  Moved the 1.65 m / 40 mm hero farther from the curb; turned traffic signs
  toward the approaching lane; widened the head/frame shots. Added a real
  Ground intersection/corner and houses behind the near walk. The broad
  transit sidewalk leaves a separate path behind the shelter, rather than
  putting the shelter across a stock five-foot walk.

No source dimensions were inferred from an unbalanced blue-shade photograph.
Construction estimates are distinguished from published anchors in REFERENCE.
The first raw/import checks pass counts, unit normals, shared external image,
rest bounds and pivot metadata. These measure serialization, not physical
clearance or final appearance.

## Pass 2 — Cycles imports, complete lineup and three photo pairs

Opened all six `renders/pass1/` Cycles images, all fourteen `renders/form2/`
software previews, five `renders/pass2/` Cycles revisions, and all three
`renders/match2/` images and their pairs. Software Workbench uses llvmpipe
while awaiting the shared GPU lock; appearance judgments use Cycles.

Color/value first: the first Cycles ambient strength was about ten times the
established commercial presentation. It washed the furniture toward pale blue
and weakened cavities. Lowered procedural sky to .035, established a
warm-neutral raking sun, and retained dark palette values. The second hero
has deep shelter/liner/under-car shadows and a readable dark roadway.
Metallic/roughness response is still uniform: this gate cannot approve finish
color or weathering. Photo controls use bare paving, never painted surfaces.

Transparent imports now show the original labels, papers, timetable, flags
and poster. Three narrow rear glazing bays and rails read as maintainable
construction; the missing pane is an actual absent mesh. The weekly cabinet
has one impact-shaped sheet dent with an interior surface. Bench arm ends
now meet the actual straps, and its feet sit on the slab. Rack pipe/flanges
read at their measured diameter. The collection roof was faceted and its
schedule floated because local coordinates were treated as world coordinates:
corrected both, closed the small chute shoulders, and retained the moving leaf.

The meter resembled a tall thermometer. Widened its compound casting and
replaced the pill aperture with a broad arch; cut the vault opening and made
its separate leaf rounded. The next close view exposed bright triangular cut
edges at the dome. Added a physical retaining bezel; the next imported view
must establish whether this solves them. Counts stay under 3k per meter.

Separated regulatory rows to remove occlusion, and added the related two-blank
time/day parking assembly. Moved the foreground warning down the curb because
it cropped against the hero edge. The bike row is partly hidden by cans in the
wide hero, so its dedicated close view remains necessary.

Rejected the first black shelter/photo pair: its fit chose a below-ground
mirror solution. Corrected rear-view landmark handedness and stated an
estimated 8 m height prior. Current fit is above grade, RMS 21.36 px in the
800 px crop; its ad case is at the opposite end from the photo. The different
meter/card mechanism gives a weak 74.40 px fit. The free pedestal rack differs
from our coin cabinet; constrain its comparison to an estimated 1.3 m eye
instead of accepting a .267 m camera. Its larger residual is disclosed. These
are construction comparisons, not surveyed reconstructions or color approval.

The clean replay exposed an eagerly expanded Make command before BP was
defined. Deferred its expansion so a failed Blender check cannot accidentally
be interpreted as an ignored shell command. Raw/import tests remain distinct
from the separate form and physical clearance judgments.

## Pass 3 — full checkpoint replay, staging and coordinate audit

Opened all fourteen images from the first complete `renders/checkpoint/`
replay, then their revised street view. Color/value first: the darker sky
leaves strong roof/bench/liner cavities, and the blue/cream/red cabinet values
remain distinct. The cream paint and aluminum still look like uniform plastic;
this is a material-stage weakness, not approval of their albedo or response.
The balanced photographs show the mottled contact dirt and worn edges that
the later bake must preserve. Their neutral is bare paving.

Rejected the context's dark empty strips below the near houses. Added native
Ground lawn modules and carried the sidewalk's cross-slope into adjacent
panels. The rack was hidden by receptacles: moved it beyond them, retaining
separate flanges and a route behind the furnishing zone. The next hero exposed
the first meter but the pickup still hid the row: move the parked pickup
farther down the block and turn the near meter faces toward the camera.

The frame, bench, newspaper shells/chains, collection box, rack and receptacle
close-ups now expose their construction. The spun lids retain visibly hollow
deposit openings and the bench has convincing strap thickness. The meter
bezel leaves bright shoulder triangles and the vault leaf is still too simply
rounded; those are explicit remaining weaknesses for the next form refinement.
The instrument face cannot rescue an unfinished casting under close raking
light. A denser mesh alone would not address the cut/shading problem.

An independent inspection found that the bent-post metadata had not bent the
mesh: its joined origin was a fastener, rather than the footprint. Corrected
the deformation into the module frame and added a fresh-import fit to the
exposed post perforations. This is an actual physical geometry check, separate
from source/import equality. Added a band/rail close-up around a procedural
host cylinder; the host is presentation only. Make and image validation now
require every listed view, including the rack and band, rather than silently
omitting a missing image.

## Pass 4 — reject disconnected band, refine dome and freeze presentation

Opened the revised street, both sign lineups, module lineup and new bracket
close-up. Color/value first: neutral white sign faces, black shadows and the
dark green frame are retained. The flat palette still cannot stand in for
galvanizing, sheeting or the used photos' chalked paint. The white meter
shoulder spots are particularly distracting under raking light.

The band view exposed a real construction error: individual chord boxes
were partly inside the host and looked like disconnected tabs. Replaced them
with continuous closed 19 × 1 mm strips, with radial chord clearance around
the .320 m host. The new bracket is 712 triangles, fewer than the original.
It remains an authored rail/tensioner, not a particular supplier's buckle.

The meter's glass was an arched but flat sheet. Replaced it with a shallow
compound dome fan and reset housing sharp edges after the Boolean cuts.
This adds only two triangles per head. Single/twin remain below 3k. The
coin mechanism/vault still need a higher-detail source and motion review.

The street now exposes rack and separate meter heads, with parked cars
farther down the block, rather than concealing the new forms. Supported
house foundations, curb/sidewalk construction and human-height perspective
give an appropriate town scale. It is still a sparse presentation block;
the flat world horizon and repeated context houses are not a finished scene.
Sorted imported root names so sign lineup placement is deterministic.

## Pass 5 — reviewed checkpoint and remaining form issues

Opened every final checkpoint view (15), all three individual calibrated
renders and their side-by-side pairs. Color/value first: the street hero
retains deep cavities and distinct paint values without clipped white faces.
The shaded pairs remain too blue/flat for material approval; the photos were
balanced on bare pavement, but these quick shaders have no final albedo or
roughness calibration. No color-finish approval is claimed at this form gate.

The band is now a continuous strip around the illustrated host. The damaged
post visibly leans and its separate import measurement is 2.9996°. The rows,
complete variants, foot/base hardware, signs and fictional graphics are
visible in the lineup/detail set. Native library houses, road, walk and parked
cars are presentation only and retain their delivery bytes.

The meter still fails a close form/shading review: Boolean shoulders pinch,
the upper casting facets, the vault is too simple, and its retaining bezel
needs a proper support-loop high source. The shallow dome does not fix that
housing. This should be corrected before look-dev approval, rather than hidden
by metal response or grime. The sign pedestrian/school figures similarly
remain an approximation to refine. Other constructions are adequate to expose
the design choices for the owner's checkpoint, not finished game assets.
The bus route plate's 2.1257 m bottom is 7.9 mm below TARC's seven-foot
clearance target; raise that plate before treating its placement as compliant.

The used shelter comparison has 21.36 px landmark RMS; it shows our higher
barrel roof, thinner fascia, different ad-end placement and a lack of the
photo's contact dirt. Meter RMS is 74.40 px at the 140 mm lens bound and the
free-paper pedestal RMS is 152.24 px at that bound. Their different mechanisms
and support proportions are obvious; these two fits are weak comparisons,
not evidence of dimensional agreement. Do not infer manufacturing dimensions
or final color from them. Published anchors remain the dimension authority.

`make` completed the imported Cycles checkpoint, three matches and receipt
validation. Both module checks pass. `make repeat` rebuilt both additions:
**86 glTF/BIN/PNG files, 8,015,914 bytes, all byte-identical**. Re-import/image
checks were rerun afterward, and all **459 existing delivery files** preserve
their baseline hashes. Final UV overlap/density, final materials, wear/bakes
and sampled motion clearances are expressly deferred. No kit code changed.

Stop here for the requested form/construction review; no look-dev started.

The first two finish-pass intermediates were retained locally in
`../build/furniture-before/finish-audit/` before the clean build. Their
`renders/look*` names below describe those historical images; final evidence
is regenerated under `renders/final/` and `renders/match/`.

## Finish pass 1 — neutral controls, cast housing and causal finishes

Color and value first: opened the checkpoint hero, meter and warning lineup
at native size. The cream paint is uniformly pale, zinc and alloy look like
one gray plastic, and the empty dark horizon makes their shadows look staged.
The later card-meter and free-paper pedestal photos cannot establish our
mechanisms. Replaced those studies with Jonathunder's used mechanical
coin/crank meter and Twzink's standalone coin cabinet. Controls are bare paving;
the blue meter's paint is expressly not an alloy color target.

Rebuilt the meter from a subdivided compound cage, cut die openings, and
relaxed a 1.5 mm voxel cast source. The game skin is reduced from that source;
the dome is a separate three-ring glazed surface seated in a real bezel.
Raised the route plate 7.9 mm to a 2.1336 m lower edge. Removed one duplicate
rack-path station that generated zero-area tube triangles, without changing
its silhouette. Meter single/twin are 1,477 / 2,976 triangles.

The first shared unwrap was rejected: native packing left overlapping thin
returns. Kept kit finalization, split the one folded chart and repacked chart
rectangles with guarded bounds. Independent kit intersection measurement now
finds zero overlap, zero outside and zero degenerate triangles. The family
has 109 px/m median opaque density; high-priority heads get more, and printed
legends retain their independent sheet. Fine chips may soften at delivery;
judge the actual bake rather than assuming source detail survives.

Authored finish reflectances distinguish dark powder coating, blue/red/cream
paint, galvanized pipe, bare alloy and concrete. Chalking follows upward
exposure, chips actual edges and lower impacts, runoff actual seams, splash
low height, and hand polish the door pull/bench contact zone. These are source
masks awaiting the exported render. What still reads as CG: source panes lack
accumulated edge dirt; the dome needs an export close-up; native packing's
thin-chart density is modest. No final look approval yet.

## Finish pass 2 — exported full-frame failures and corrections

Color and value first: opened all five `renders/look1/` images at their native
1440 px: meter, hero, boxes, speed face and warning lineup. The blue/red/cream
paint values stay distinct and white signs remain neutral. The meter alloy is
too glossy and reads machined/chromed rather than used die casting. Most wear
vanishes at the wide hero's scale. The new extended lawn accidentally sits
above much of the roadway, making a green street: rejected this hero outright.

Lowered that presentation plane below the actual road. Reduced the tree
population to alternating species at approximately 31 m instead of a 15 m
canopy wall, retaining houses on both sides and the library utility poles and
catenaries. The raking sun and 1.65 m / 40 mm camera are unchanged. Those
corrections still require the next actual Cycles image.

The cabinet close-up proves that source-only bevel chips were subpixel at
shared-atlas density. Added a physical 10 mm edge-distance envelope, confined
to the actual part edges, with stronger low splash and gravity tracks under
folds. Kept each paint's own color. Added one small original F9 adhesive tag.
Separated the shelter's anodized extrusions from its powder-coated steel bench.
Raised alloy roughness and confined oxidation to ledges/cavities. Glass now
has authored UVs for edge deposits and rougher retaining margins, shared by
all panes rather than allocating another map. The meter crown gets 100 more
triangles funded by its hidden bezel rear and lens tessellation; single/twin
are now 1,449 / 2,916. The vault leaf was recentered over its actual opening.

The independent source motion sweep found preexisting interference, not a
serialization error: approximately 6 mm in cabinet returns/caps, 9.1 mm at the
collection door jamb, 5.7 mm at the chute/roof and 5 mm at the receptacle rear
rim. Meter leaves meet the reduced casting by up to 1.44 mm at rest. These are
not hidden by a blanket contact exception. The owner was asked whether to
extend scope because accepted forms/pivots were explicitly to be retained.
No unapproved hinge change has been made. The numeric sweep is separate from
the passing raw/import/UV/channel/preservation gates; no physical-clearance
pass is claimed here.

Remaining CG tells: the printed newspapers are original stylized press art,
small corners and circles can facet at macro distance, and the shared atlas
softens very fine wear. The corrected cast/dome and stronger wear need the
next exported close-up and matched-light comparisons before final approval.


## Finish pass 3 — final imported delivery, values and limits

Color and value first: inspected the 1600 px exported hero, all module and
sign lineups, every detail, the four turnarounds, Eevee, four full-size pairs
and the ROI overlay. Blue/red/cream paint remains colored under sun; black
cavities and undersides stay deep. Chips and fold grime survive on the nearest
news cabinets at full hero frame. The bench's pale handling stripe was rejected:
powder roughness is now higher and hand polish stays around the actual arms.
Galvanized low pipe gets zinc-colored oxide rather than painted-steel rust.
The roof/frame, bench and glass now have distinct responses.

Neutral controls are bare paving/concrete, with the exact original-photo ROI
and RGB gains in `build/photo-calibration.json`. Sunshine shelter/meter pairs
have directional light; the cabinet and shaded sign use diffuse sky. Camera
exposure is calibrated on comparable surfaces, not presented as recovered
camera metadata. The ROI audit caught the first cabinet photo measurement on
the side skin; it was moved to the front red stile, excluding rivets, and the
comparison exposure was corrected. The sign's first concrete control had
accidentally selected sky and was rejected before final calibration. The final
numeric receipt is tabulated below. Our charcoal anodizing is intentionally
darker than the reference's blue finish; that pair is not exact color agreement.

The source cast cage/voxel body and separate dome were checked again on the
baked export. The larger straight die opening removes the narrowing vault
mouth without changing the accepted pivot. Single/twin remain 1,449/2,916
triangles. A sampled source-surface sweep is separate from the successful
raw/import serialization gate. Accepted cabinet/collection returns and lid
rims still have interference; no clearance pass or new hinge location is
claimed while permission to alter the accepted mechanisms remains pending.

The road continues into town with library houses on both sides, alternating
street trees, parked cars and utility construction/catenaries. No other
family delivery was written. The front orthographic camera was moved back
along its existing view to remove a narrow below-floor strip. The hero is
still 40 mm / 1.65 m, with a raking sun. Every image is made from the external
glTF and its actual maps, with dependency hashes in its JSON receipt.

Eevee initially lost print behind the combined transmission state. Its
presentation adapter now assigns opaque print faces an equivalent opaque
state for per-material refraction sorting; all vertices, UVs, image bytes and
PBR values come from the import. It does not rewrite the glTF. Screen-space
refraction still loses detail through stacked panes. Cycles is the reference
for these layers. The shipped material limit and shared memory are unchanged.

What still reads as CG: low-cost bezel/cap silhouettes facet at macro distance;
the shared atlas softens fine wear; the newspapers remain stylized original
press art; the meter's dial/crank internals are authored estimates. Repeated
context trees/houses and very clean broad pavement reveal the staged street.
The meter/cabinet camera fits compare different original designs and retain
large landmark residuals (170.85/116.67 source pixels); they prove mechanism
class and guide surface response, not exact replicas. The shelter fit is
21.36 px; the R2-1 is 2.34 px. The independent Blender projection check proves
camera serialization only, not these geometric agreements.


### Final measurement and command receipt

Display-referred median luminance on the explicit surface ROIs (render /
neutral-balanced photograph), not linear albedo:

| Surface | Render | Photo |
| --- | ---: | ---: |
| rear frame; different original design, compare value not exact hue | 0.081 | 0.182 |
| unpainted bezel; exclude blue housing as an alloy target | 0.487 | 0.439 |
| red front door stile, exposed painted steel; excludes side skin and rivets | 0.258 | 0.256 |
| white sheeting away from text and border | 0.434 | 0.436 |

Hero display luminance p5 / median / p95 is .026 / .338 / .608; 7.47% of the
frame is below .05, and .0132% has any channel at least 254/255. This describes
the whole image, not a proof of material reflectance. The darkest cavities and
under-roof seating were also inspected directly.

Commands: `make -C street-signs set-clean`, `make clean`, `make`, then the
render-adapter refresh through `make`; `make repeat` passes all 89 added files
byte-for-byte (20,706,651 bytes), retaining accepted baked maps. `make check`
passes 15 furniture modules plus 25 sign modules, 722 prior-delivery hashes,
actual imported normals/bounds, material channels, budgets and zero opaque
UV overlap. Final atlas density p5 / median / p95 is 73.84 / 109.16 / 189.60
px/m, coverage 33.15%. The separate `make check-motion` intentionally fails:
6.000 mm cabinet contacts, 9.054 mm service-door contact, 5.736 mm chute/roof,
and 4.976 mm receptacle rear-rim contact. All three meter leaves report no
penetration over the 0.5 mm threshold at the sampled angles. No pair is skipped.

The repeated GPU bake is not bit-identical: a few encoded map bytes can change
at quantization boundaries. Geometry/UV/graphics/export repeat is byte-tested
with accepted maps retained; no bit-identical GPU rebake is claimed. The final
renders were refreshed against the current canonical images and all 25 receipts
pass their actual dependency hashes. Repeat now preserves dependency timestamps
after proven byte identity, avoiding an unintended unchanged bake on `make check`.

Final crops are `renders/comparison/{meter,symbols,route-plate,setting}-pair.jpg`;
each constituent crop is at least 800 px wide and normalized to the same scale.
The replaced mechanism pairs are `reference-{meter,news}-{before,after}.jpg`
in that directory. The route's actual imported lower edge measures
2.125699997 m before / 2.133599997 m after, against 2.1336 m. Book comparisons
remain local in root build/. No downloaded image enters docs or a texture.

## LOD rollout — 2026-11-09

Merged current main (already up to date). Frozen revision `6bea63c` and 103
literal tool hashes are in `build/lod-rollout/street-furniture/freeze*`.
The original `make check` passes before adoption. Its full command in
`original-before.json` explicitly freezes the three accepted source blends,
manifest, all 32 furniture glTF/BIN files and the nested RoadSigns/Signs inputs;
the dry run confirms no original generator runs. Start with one static bench
chain at the standard .4 / .25 switch. Other kinds, especially glazing and
moving cabinets, need independent config/build/review/check proof; no bench
result approves them. Original source/map/docs bytes remain immutable.

### LOD critique 1: reject the bench near row

Opened all three wide native strips, both construction views and contact,
then all six unscaled original/LOD/difference pages in `bench-native-pass1/`.
Color/value stays consistent, with dark painted straps and shaded underside.
The 2448/3436 candidate retains 71.25%, above 1374, and changes repeated
slat-tip highlights. Side local error .08465 fails .08; the front/rear pass.
`check-lod` exits 2 for that image gate; independent UV/normal/tangent/raw
checks pass. Close views expose sharp slat toes and flatter support response.
Full config, payload hashes, checks and every image are archived in
`build/lod-rollout/street-furniture/bench-pass1/`. No gate is relaxed.

Omit this costly, failed near row and try the standard farther starting point
at .09 with a .15 request. A changed candidate must also be tested at the old
.25 distance before its farther switch can be selected; no switch approval
is inferred from the earlier different mesh. Bench is static; all slats,
arm rails, supports and feet must retain coarse geometry and contact.

### LOD critique 2: retain the failed far coverage control

Opened all three native far strips, both construction views and contact.
Color/value remains consistent at .09 / 7.75m, but reduced slat curvature and
thin boundaries alter coverage. The 1768-triangle candidate misses 515;
side/rear silhouette loss .06083/.05559 fails .05. Front coverage passes.
All local RGB, mean/p95 and alpha gates pass; the failure is not relabeled as
a color error. Independent raw UV/normal/tangent audits pass, while full
`check-lod` exits 2 on images. The close view exposes angular front strap tips.
Config, payloads, checks, every image and hashes are archived in `bench-pass2/`.
Next test more coarse geometry at this same far switch, keeping the original
515 goal and all image limits. No bench or other furniture chain is accepted yet.

### LOD critique 3: the small density change still fails

Opened every new native strip, both construction views and contact after the
GPU queue released. The .3 request yields 1808 triangles. Color/value and all
local RGB checks pass, but side/rear coverage .05505/.05091 still fails .05;
front .03535 passes. The close slat tips remain angular. Full `check-lod`
returns 2 on images; the independent field audit passes. Archive: `bench-pass3/`.
Try .5 at the same far switch, preserving the 515 goal. Select the canonical
Bench root explicitly so consolidated geometry stays under its placement
frame alongside its sidewalk/anchor sockets; no original placement is changed.

### LOD critique 4: coverage requires tighter surface preservation

Opened all three fresh native strips, both construction views and contact.
The .5 request gives 1908 triangles with the canonical Bench placement root.
Hue/value and RGB checks hold; side/rear silhouette loss .05479/.05038 still
fails .05. No complete feature was removed according to the pruning receipt;
the thin strap boundaries and curvature shift. `check-lod` returns 2 for
images, with raw/normal/UV audit passing. Archive: `bench-pass4/`.
One final trial tightens the geometry surface allowance from .75 to .25 switch
pixels; it does not alter the image gate, target or switch. The other furniture
kinds remain unbuilt and receive no approval from these bench trials.

### LOD critique 5: select the tighter far bench

The .25-pixel geometry allowance yields 2360/3436 triangles at .09 / 7.75m,
against the unchanged 515 goal. Opened all three native strips, both construction
views and contact. Dark paint values, strap gaps, arm rails, supports and feet
hold. Worst mean .004133, p95 .019608, local .017097, alpha .022631 and
silhouette loss .031105 pass unchanged gates; independent raw/field audits pass.
Close slat tips and support curvature remain coarser than LOD0. The 1908
same-distance control remains a cheaper native visible/coverage failure.
Keep `target_met: false`: 2360 is the lowest reviewed passing count, not a
global geometric minimum.

Rendered this exact export at the old .25 / 2.79m switch without editing its
geometry. Opened all three wide controls and all six unscaled pages in
`bench-native-old/`. Side local error .08603 fails .08, with repeated strap-tip
highlight changes; front/rear pass. `bench-original-switch/receipt.json`
hashes that unchanged candidate. These failed old-distance comparisons and
passing new-distance strips justify the farther switch, rather than the earlier
different meshes or a lowered limit.

Independent `bench-contact.json` measures actual vertices around all four
source anchor regions: source and selected foot minima are each 0m at grade.
Every mesh node belongs to the canonical Bench subtree. Moving that root by
1m moves every measured mesh vertex by 1m with maximum error 0m. This proves
placement/contact on actual surfaces, separate from serialization. Bench has
no moving mechanisms. Stop this long-session checkpoint after the bench;
the other fourteen delivered kinds stay unbuilt/L0, without a minimality claim
or inherited approval. Their existing motion/glazing limitations are unchanged.

Final receipts: `bench-pass5-check.json` records `check-lod` exit 0, including
the independent field audit; original before/after checks both exit 0 with
their complete frozen-input commands recorded. All 103 literal tool hashes
match revision `6bea63c`. `lod_report.py --write-readmes` generated the measured
bench table and `report/contact.jpg`, which was opened. Full-container costs
include all sixteen original containers plus this level: 89434 stored triangles,
29 source-specific materials, 115 primitive placements, 17622047 physical bytes,
24.8369 MiB resident; added images 0, added mesh .1990 MiB. Active draw range
is 1–57 across these alternatives; a bench draws one primitive. Repository
check: 2603 files, zero errors; diff check passes. No kit, accepted delivery,
map or original docs image changed.
## LOD round 2 — independent kinds and original motion preflight

Merged current main (already up to date). Existing standalones match every
recorded triangle count and glTF/BIN size exactly. The original make check
passes with accepted scenes, exports and the original sign-set inputs explicitly
frozen; complete commands and costs are in build/lod-round2/street-furniture/.
Freeze revision 8ca54fc and 103 tool hashes precede these trials. The source
receipt includes original packages/maps and the accepted bench LOD payloads;
another kind's proof cannot alter or approve the bench.

Reran the family's independent source-part make check-motion with its accepted
motion-parts scene frozen. It exits 2, reproducing the documented failures:

| Original kind | Measured worst penetration | Outcome before LOD work |
| --- | ---: | --- |
| Litter | 4.976 mm | Lid/rear rim; no verified animatable hold |
| Recycling | 4.976 mm | Own lid/rear rim proof; no verified animatable hold |
| NewsDaily | 6.000 mm | Coin lid and lower door both interfere |
| NewsPedestal | 6.000 mm | Own coin lid and door both interfere |
| NewsWeekly | 6.000 mm | Own coin lid and door both interfere |
| CollectionBox | 9.054 mm | Service leaf; chute also 5.736 mm |
| MeterSingle | 0 mm | Source coin-door sweep passes |
| MeterTwin | 0 mm | Both source coin-door sweeps pass |

These use actual solid source surfaces, the unchanged .5 mm tolerance and
documented sampled ranges, without whole-pair exceptions. Original export
serialization is independently checked. Holding LOD0 during interaction cannot
repair a collision already in that original. Preserve those accepted deliveries;
do not create a pretend passing chain or count old pictures as new LOD critiques.
The receptacle and news/collection kinds stop before LOD trials. NewsRow retains
its members' original limitations. Their evidence is original-motion.json, not
an adopted delivery. Racks remain minimal LOD0: 1020 per U, 4080 for four.

Prepare separate, unwired meter and shelter configs. Meters start with .4/.15
at .25/.09; their own actual permitted poses must pass. Shelters start with one
far .09 level and .05-pixel surface preservation, retaining coarse rails/posts.
Each shelter variant needs its own native view, root and material/UV proof.
The Makefile still exposes only the previously accepted bench by default.

### Single meter critique 1 — reject far coverage and head change

Opened all six native strips and three construction views. Color/value first:
galvanized post, cast housing and dial retain their palette, but the far head's
top highlight breaks and its outline changes. Counts 1449 -> 921 -> 552,
goals 580/217, at .25/.09 (5.26/14.62 m). Near images pass. Far front p95
.08392 exceeds .08; silhouette loss .06435 exceeds .05. Reject that level,
without widening either limit. The supplied normal-field audit passes; the
generic check fails only its image gate, not topology or UVs.

The new independent check_lod_parts.py passes placement, grade and permitted
motion: original coin door sampled at 5 degrees; reduced levels at rest only.
It uses actual opaque surfaces, matching the original's solid tags. Original
open graphics/lens sheets are non-solid; material faces are separated for this
temporary audit when static consolidation combines them. No moving/fixed pair
is exempted. Every mesh, including graphics, must follow its placement root.
Hold LOD0 while the coin door is open. Archive exact trial inputs, payloads,
images and checks in meter-single-pass1/. Try a .2 near request against the
same 580 goal, and tighten far surface_pixels from .75 to .15.

### Single meter critique 2 — one near level and a native goal witness

Opened the second trial's six strips and three close views. Color/value holds;
the near head remains rounded at its switch. The tighter far head restores
coverage, but costs 1026 triangles versus near 911. Its image/normal checks
pass; the raw check correctly rejects increasing triangles down the chain.
Archive that trial and omit its unhelpful far switch, rather than waive a gate.

Re-rendered the frozen first trial's 552-triangle far mesh at the *near*
5.264 m switch, alongside original and chosen meshes. This is a negative witness
at/below the 580 goal, never a delivery or substitute tool. Opened all three
native strips in meter-single-near-goal/. The cheap housing's pointed crown,
floating-looking lens seat, faceted vault leaf and changed highlights are clear.
Front p95 .12549, local mean .10958 and silhouette loss .06433 fail; 55-degree
p95 .09020 / local .16155 and rear local .12072 also fail the unchanged limits.
Only local dependency symlinks resolve the archived candidate's unchanged maps;
payload hashes and the complete script/command are retained with the witness.

Adopt the separately rebuilt 911-triangle level at .25 / 5.264 m, goal 580
still target_met:false. Opened every final strip, close view and contact again.
Galvanized post width/coverage, dial routing, rounded crown and footing hold at
native size. The close view shows some existing cast-skin waviness and reduced
vault faceting; this is not a new close-range replacement for LOD0.
Raw/UV/frame/topology, normal-field and permitted-pose/placement checks pass.
The original coin-door sweep is sampled at 5 degrees, reduced door at rest;
all measured penetration is zero. Hold original LOD0 during coin-door use.
The Makefile lists only bench plus this adopted meter; both receive the
placement/grade check, with physical opaque-surface motion where applicable.

Single-meter closing proof: public check-lod for bench plus meter and original
make check pass. The reporter writes both measured README sections and their
shared-resource union under report-single/; only surrounding prose is shortened.
The meter alone stores 2360 triangles, two material resources, six primitive
placements and 9716845 distinct payload bytes; it draws 1449 or 911 triangles
in three calls. Original maps remain 17.333 MiB with no new images; whole-chain
residency is 17.5030 MiB. All 38 original/accepted-bench payload hashes and all
103 tool hashes match. Repository and whitespace checks pass.

### Twin meter critique 1 — two heads require their own coverage proof

Opened all six native strips and three close views. Color/value first: both
cast housings, zinc post/yoke and distinct paid/expired dial states retain their
palette. The near 1935-triangle level keeps both crowns, lens seats and vaults
at .25 / 5.39 m; its image gates pass. The 1156-triangle far level has obvious
angular crowns in the close view and front silhouette loss .06251 at .09,
above .05. Reject that level. Its raw check fails only the image comparison;
normal/UV/topology and permitted-pose/placement checks pass independently.
Both original coin doors are sampled at 5 degrees; reduced doors at rest only.

Archive all first-trial payloads, config, native images, checks and hashes in
meter-twin-pass1/. Test that 1156-triangle mesh against the original at the
near switch as a witness to the 1166 near goal. A first witness-driver run
stopped at its dependency-symlink assertion; no picture or passing claim was
produced. Correct only the ignored driver's lexical-path handling, preserving
the delivered maps and archived payloads, then rerun. Tighten the far trial's
surface allowance to .35 rather than borrow the single meter's .15 result.

### Twin meter critique 2 — own near witness and accepted far retune

Opened all three near-goal strips. The 1156-triangle witness, just below the
1166 near goal, visibly flattens both crowns and separates the lens seats and
vault silhouettes; every near view fails the unchanged image limits. Its exact
driver, candidate, maps, chosen payload hashes and metrics remain in
meter-twin-near-goal/. This is this twin's evidence, not the single's witness.

The .35-pixel far retune measures 1935/1363 triangles, goals 1166/437, at
.25/.09 (5.387/14.963 m). Opened all six native strips and all three construction
views. Color/value and both dial states hold; both heads, yoke, post and footing
keep their coverage. Far construction views remain faceted, but the native
97-pixel comparisons no longer show the cheaper level's broken outlines.
All original RGB/alpha/local gates pass, without a new atlas or changed limits.

The first retune's runner was observed exiting 143 without a closing receipt,
although its child had finished writing the images. Verified that no own job
remained, recorded that run as interrupted, and repeated the exact command
under foreground monitoring. The retry exits 0. Its native JPGs are byte-
identical to those inspected; PNG file hashes include changing render metadata.
Reopened the final close views and complete contact. Final public check-lod
passes for bench and both meters, including actual permitted-pose/placement
audits. The two source coin doors each receive 20 samples; reduced doors draw
only at rest, all measured penetration zero. Hold LOD0 for either open door.
Normal, UV, frame and topology audits pass independently. Original make check,
immutable-source and frozen-tool checks close this kind before shelter work.

Twin closing results: original make check and public check-lod pass; source
receipt and all 103 frozen tool hashes match. The reporter-generated table
stores 6214 triangles, two material resources, twelve primitive placements,
10058175 distinct payload bytes and 17.8195 MiB resident. One instance draws
2916, 1935 or 1363 triangles in four calls. Texture residency remains the
original shared 17.333 MiB; new images zero, added mesh buffers 288444 bytes.
No existing package, accepted bench/meter geometry, map or docs JPG changed.

### Intact shelter critique 1 — thin structure preserved, weak savings

The original passes the new actual construction audit: six independent pads,
six columns, slab and a rear-right pane ray. Every pad-bottom sample meets the
actual slab within .000030 mm, and every column enters its own measured pad.
The .05-pixel LOD trial measures 7730 -> 5958 triangles, goal 1160, at .09 /
26.385 m. Its raw/UV/frame/normal, native-image, placement and support checks
all pass; rear pane hit is unchanged on the actual geometry.

Opened all three native strips, both close views and contact. Color/value first:
roof and slab highlights, dark frame and cloudy glazing stay consistent. The
roof ribs, columns, knee rails, bench straps and feet remain, without a detached
or faded thin member. The close view reveals the original economical glazing
and roof segmentation; this is not new look development. But 23% savings is a
weak extra level. Archive this complete proof in shelter-pass1/ and try a
cheaper .05 request with the normal .75-pixel allowance, retaining the 1160
goal, original maps, original switches and all physical/image gates.
