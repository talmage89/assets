# Community gardens — form and construction review

Scope: the requested checkpoint, before look-dev. All judgment renders import
external glTF. No source procedural material is substituted for a garden export.
References are comparison-only, with credits in `refs/SOURCES.md`.

## Construction preflight (not counted as a rendered critique pass)

Color/value: quick values deliberately keep soil and cavity materials dark,
with gray-brown older wood and darker steel. The new plant atlas has outline
alpha and simple constant response. None of these values is a final albedo or
weathering acceptance; the Cycles heroes and balanced pairs still decide that.

Fixed before the first review renders:

- Native shed's 9,700-triangle raw tab construction exceeded the garden brief.
  The private copy now uses full gauged lapped courses, preserving framing,
  sheathing, hinges and returns while deferring tab cuts to the normal bake.
  Native accepted files remain byte-identical.
- Gate sleeves were solid cylinders. Replaced them with bored sleeves, offset
  the frame from the pin axis and attached the sleeve with a real welded neck.
  The 5° kit sweep uses exported solids and no intended-contact exception.
- Some vegetable daughter axes used approximate trunk positions. They now
  interpolate the actual main centerline. Petioles extend into retained alpha
  so a transparent margin cannot leave a visible blade disconnected.
- Bean leaders distinguish 25mm bamboo from 2.5mm twine, and follow the
  trellis's bowed twine or the teepee's actual pole axis from planted feet.
- Row-cover hoop feet now begin in the actual plot's soil instead of a common
  arbitrary height. Cloth sags between the hoops.
- Moved negative-X standpipe hose coils away from the main route, gave the
  newer water station a firm service apron, feathered path shoulders and
  connected the gate to the neighborhood sidewalk in the presentation scene.
- Added physical sealed floors/standing seams to the watering can and barrel,
  and a curved drawn wheelbarrow tray with a rolled rim.

Evidence: `build/check.json` measures raw accessors and fresh import separately
from actual board surfaces, block cores, knee rays and routes. `build/motion.json`
records gate-neighborhood and shed sweeps. These establish their stated scopes,
not photographic realism or continuous motion certification.

Photo balance uses a white cap in Oliver, gray apartment stucco in WiseWords,
and light siding at Martin Drive. The exact neutral rectangles and linear gains
are recorded under `build/photo-references/balance.json`. All are assumed frame
neutrals, not calibrated cards. No exposure increase is used to set an albedo.
Oliver's corners are obscured by people: its inferred along-edge phases make
it a weaker framing/construction comparison. The fit reports retain that error.

## Pass 1 — exported views, site density and plant habit

Viewed every image in `renders/pass-1/` at full size: three heroes, three
overheads, all corners/bean views and the city tomato. Compared with the
original Oliver, WiseWords and Martin photographs opened in the reference cache.

Color/value first: the images retain deep soil/cavity shade and no clipped
channels. Whole-frame display-Y p5 / median / p95 is .012/.381/.771 (city),
.035/.458/.777 (park), .009/.462/.770 (newer). Green medians .217/.295/.269
include context trees as well as crops; these are diagnostics, not albedo
calibration. Uniform gray-brown timber, smooth brown chips and untextured soil
are obvious checkpoint surfaces. Do not raise exposure to hide them.

Harsh findings and corrections for the next pass:

1. The city is beds scattered on a brown pad. Four-by-eight modules are the
   right size, but the 60×70ft enclosure gives excessive bare margins. Compact
   it to 35×62ft with 3ft bed aisles and 4ft perimeter access; compact the newer
   plan around 4ft working aisles too. Keep the larger park tenant plots.
2. All heroes end in a green horizon beyond the rear fence. Extend the native
   neighborhood with a rear service alley and three houses. Side apartment
   walls alone do not establish a town when the camera looks down the lot.
3. The noticeboard blocks the garden from its gate. Move it to the side margin;
   it should serve the entrance without replacing the hero's planted foreground.
4. Tomato structure reads as a Christmas-tree rack: a bare single stem and
   horizontal tiers, with the berries too exposed. Give the mature plant three
   connected leaders, nine-leaflet compounds, broader blades and varied blade
   inclinations. Keep the 5k cap. Black wedges on some berries are hard leaf
   shadows: raw normal/winding checks find no reversed fruit faces or holes.
5. Beans are ladders of flat horizontal leaves. Increase the mature node/leaf
   population within budget and vary physical blade roll/inclination; preserve
   actual trifoliate attachments and the support-specific twining axis.
6. The two later gardens have no mature tomato stand: the care-state/crop
   modular pairing made their tomato plots fallow. Preserve a live mature stand
   of each staple while retaining all five care states. The city already has a
   mature staked row; the park will provide the caged tomato view.
7. Wet soil polygons float and cast hard shadows like black rocks in the newer
   corner view. Remove overlays; assign the quick darker value to actual soil
   faces around planted roots. Fine moisture transitions belong to look-dev.
8. The youngest peppers/herbs are miniatures with mature branching. Reduce
   their node/fork population and juvenile height while retaining blade size
   and attachment. Squash needs radial palmate lobes, not repeated side waves.

Remaining at this pass: beds and crops still look too uniform and smooth,
seedlings are sparse, labels are bright, the cone cages are absent from these
views, and the infrastructure close-ups and photo pairs have not been judged.
The layout, foliage and water fixes must show in the second-pass exports.

## Pass 2 — compact plans, fuller crops and infrastructure close-ups

Viewed every image in `renders/pass-2/`: three heroes/overheads, every crop and
corner view, all three water/compost views and the accessible-bed detail.

Color/value first: city display-Y p5/median/p95 .010/.311/.739; park
.093/.447/.766; newer .007/.430/.762, with zero clipped channels. Keeping
exposure at −.35 retains the raking sun and dark recesses. The apartment-gap
view is understandably darker than the open park. Quick wood/soil surfaces
remain flat and uniform; they are not accepted as final weathered materials.

The compact city now reads as a cultivated gap between apartment walls. The
rear alley/houses close the green horizon. The newer plan has visibly smaller
working aisles and distinct front/rear accessible courts. These are meaningful
plan differences, rather than the same rectangular pad with a different seed.
Tomatoes have connected branching mass and fuller compound leaves; the park
now has mature tomatoes in cages. Beans retain visible trifoliate leaves on
twine and teepees, rather than a texture-covered volume. They still look more
orderly and open than a very vigorous July planting.

Remaining construction tells, fixed for the third pass:

- Water close-ups show a hose bent like a rigid pipe at three points. Replace
  the hanging lead and trailing tail with smooth slack curves; keep the coil
  on grade and stay below the 2k module cap.
- Compost is a set of pyramids floating above the bay floors. Replace them
  with settled irregular multi-ring heaps meeting the receiving ground. Fine
  fibers and decomposing matter remain a later material concern.
- The corner view reveals that only the long bed boards had lag heads. Add
  the missing end-board fasteners into the same internal posts. Reframe this
  view on the actual corner, rather than mainly the soil.
- Fallow beds read as empty tilled soil with a handful of sticks. Give their
  straw cover an actual 13–23mm settled bulk before the later texture pass.
- The accessible detail is blocked by the foreground fence. Move its camera
  inside the court so the legs, tray and knee opening can be judged.
- The water's dark soil no longer casts floating stone shadows. Its triangle
  value boundaries remain a deliberately coarse checkpoint approximation.
- Marigold blades are too simple. Use small serrated leaflets on a true pinnate
  rachis; keep the low specimen budget. Juvenile peppers/herbs now reduce node
  counts rather than simply shrinking the mature architecture.
- Put gardener sockets on the actual finished walking surface and independently
  ray-check their height. Source constants alone are not ground-contact proof.

One limitation of the layout stays explicit: the traditional shed retains its
raised threshold. The new garden's external water/compost/bench courts and high
beds have firm routes; the shed interior is not represented as wheelchair
accessible. No blanket ADA compliance claim is made.

## Pass 3 — exported construction and route continuity

Evidence: every PNG in `renders/pass-3/` was opened, including the three
overheads, all crop/infrastructure details, the scale view, Eevee comparison
and first complete catalogue. Same photographic neutrals as the earlier
passes: Oliver's white cap, WiseWords' gray stucco and Martin Drive's light
siding. These unsurveyed photographs constrain proportion and construction;
they do not establish exact board lengths or certified path surfaces.

Color/value first: display-luma 5th/50th/95th percentiles are
`.008/.317/.742`, `.088/.443/.769`, `.007/.425/.765` for 117/229/341.
No channel clips. City and newer-garden cavities have deep shade, and the
park remains lighter because much of the frame is sunlit lawn and siding.
The flat leaf color and uniform lumber still advertise CG. They are explicitly
provisional values, not a completed material or wear pass.

The silvered-board shape now has butted end boards, internal posts, lag heads
on both board directions and an actual narrow end check. Hollow blocks have
open cores. New seedlings are small plants rather than copied full adult
branch counts. Fallow plots have straw bulk; the mature bean leaves attach to
their petioles and climb along real poles/twine. Compared with WiseWords, the
tomatoes and beans remain more orderly and less interlocked than a vigorous
July planting. The leaf outline grids are visible at close range; normals,
veins and material variation belong to the next checkpoint.

Problems found and corrected for pass 4:

- A grass cross-aisle was coplanar with the park's gravel spine, producing an
  apparent break through the main route. Partition the firm-path union once,
  with shoulders only at exposed edges. Grass stays at the receiving grade.
- The high tray had only four corner legs under a broad floor. Add five
  galvanized transverse bearers at 16in spacing, bolted long aprons and a
  supported 19mm floor. Keep the actual lowest bearer at .6973m and re-run
  knee-corridor rays; soil depth is a shallow approximately 9cm for greens.
- The hose lead is now curved and the compost touches grade, but heap crowns
  remain too narrow and faceted. Broaden the settled crowns and smooth their
  construction normals. Decomposing fibers remain deferred.
- The rain collector was closed cylinders entering a sealed barrel lid.
  Replace it with a gauged open gutter, bored outlet, hollow downpipe and
  annular receiving lid. Bibs/taps get real outlet bores and moving handles.
- The city/newer tomato close-up selected a staked plant. Keep a front caged
  specimen in mixed-support plots and frame that specimen explicitly.
- The all-in-one catalogue makes seedlings and labels illegible. Split it
  into a full-scale plant progression sheet and a packed construction sheet,
  with legible screen-space labels. Both still render imported prototypes.
- Independent root rays expose an orientation error in transverse beds.
  Rotate the cultivation frame with the bed's long axis; keep weeds/flowers
  inside the true soil opening and fit block-bed teepees to that opening.
  Lower root caps into the soil, seat bed roots on their receiving grade and
  remeasure all 362 plot plants. This corrects both crowding and floating roots.
- Give cages a 20cm driven section and tomato stakes 30cm. Trellis/bamboo
  feet extend 20cm below their planting datum. Seal the pail floor and extend
  the pinwheel stake through its axle. Small props still need real support.
- Re-exporting native context without material-driven vertex colors loses
  the original railing/siding tints. Preserve native `COLOR_0` while checking
  that garden `_WIND` never becomes color. The failed serialization views
  remain in `renders/serialization-review/` as evidence, not final views.

The gardens now have distinct spatial programs and visible street neighbors.
The newer garden's wide court earns its space; the park's large lawn alleys
are less intimate than the photographed chip-path garden. This is a deliberate
tenant-plot archetype, not a reproduction of Martin Drive's plan. The front
gate, usable working strips, common water point, shared tools and service end
make a coherent place rather than a set of pieces spread over a pad.

## Pass 4 — final exported scenes and three photographic pairs

Evidence: all 24 garden PNGs, the two catalogues and three photo pairs in
`renders/checkpoint/` were opened. These views use freshly re-imported scene
packages; the mature-bed pair relocates the unchanged exported Plot10, and
the installation pair assembles unchanged exported bed/seedling prototypes.
No source photo is an asset input. Neutral assumptions remain Oliver's white
cap, WiseWords' gray stucco and Martin Drive's light siding. The last two are
assumed neutrals, not measured gray cards.

Color/value first: final hero display-luma 5th/50th/95th percentiles are
`.008/.318/.742`, `.090/.446/.769`, `.006/.464/.765`. No channel clips.
The newer garden has more bright firm surface, but its leaves and underside
retain deep values. Native railing/siding tints survive scene serialization.
The first WiseWords pair was too dark and used a sparse display assembly;
the corrected pair uses actual Plot10 and a brighter soft comparison light.
Its grass and boards are now readable. The gray unpainted bed intentionally
differs from the photo's colorful painted boards; material matching is not
claimed before look-dev.

Photographic findings, without treating good camera residuals as good art:

- **WiseWords, July 2010:** the 4×8 framing and reaching scale read, and the
  three tomatoes now carry compound foliage, fruit trusses and driven
  supports. The mixed-crop photograph is much denser, with foliage interlocked
  across the whole bed. Our pruning, bare leader tips and regular silhouettes
  still read too orderly. Different crop identities prevent a direct species
  calibration, but the missing midsummer mass remains a real weakness. The
  fitted lens is 41.2mm, weighted RMS approximately 14.7px at 1024px width.
- **Oliver installation, August 2008/2009:** the soil-filled board enclosure,
  butted corner and transplant scale are credible. The photograph has fresh
  lumber, rough granular soil and much incidental human/tool activity. The
  model is smoother and emptier. People hide most corners; the 37.8mm fit has
  27.6px RMS and should only support broad construction/framing comparisons.
- **Martin Drive, July 2009:** sign/post proportions fit strongly (38.6mm,
  5.8px RMS). This does not make the compositions equivalent. The reference
  has dense flowers, informal twine and a narrow chip entrance; Meadow
  Commons has wide grass tenant alleys and chain-link. Our park garden is
  particularly regular and underplanted. Keep that weakness visible rather
  than calling the different layout a photographic match.

Construction now holds up better: bed roots sit on actual grade, all 357 plot
plant roots meet the soil, cages have measured driven feet, and the exposed
CMU cells are real voids. The accessible detail shows a supported tray and
firm approach. Its approximately 9cm growing medium is deliberately shallow;
this is a greens/herb tray, not a deep-rooted crop bed. The traditional shed's
raised threshold remains outside the accessible-interior claim.

Remaining visible tells are the regular crop spacing, open herb/tomato
silhouettes, simple tool shells, smooth compost masses, angular path-shoulder
corners and hard coarse wet-soil boundaries. Flat leaf response, grain, rust,
soil/chip/straw microstructure and wear are not developed yet. The catalogues
are legible at full resolution but small seedlings require zooming. There is
no claim that these quick-material views are finished product photography.

Checks prove budgets, scale/contact, sampled clearance and serialization;
they do not erase the differences above. Stop here at the requested form
checkpoint. Before a finished-asset claim, foliage needs a stronger organic
mass pass, secondary ground construction needs softening, and look-dev/bakes
must be judged again from the exports against used-garden photographs.

The final care-state audit found that the park's mature-crop safeguard had
eliminated its only fallow plot. Its small donated herb bed is now mulched and
fallow, and all five states are asserted on the imported gardens. A pure plan
audit also retains all five across 300 seeds. This reduces the park garden to
214,898 triangles without removing its mature staple crops. The changed
exports and all checkpoint views are rebuilt before handoff.

## Look-dev pass 1 — recover the midsummer mass before polishing

Color/value first: opened the 1000px exported heroes, overheads and tomato,
bean and squash details in `renders/lookdev-pass-1/`, against the Martin Drive,
WiseWords and additional July 2010 City Hall photographs. Also opened UMN's
indeterminate tomato, zucchini and bean photographs, the corn tassel close-up
and NC Extension's marigold planting. Martin's light siding and WiseWords'
gray stucco remain the assumed neutrals. The new City Hall comparator uses the
near bed's gray cap; plant-photo neutrals and their limitations are recorded
with the next comparison set. No reference pixels enter an asset texture.

The first new export has real foliage overlap, a much taller corn stand, closed
bean foliage on the teepee, a wider squash mound and dense lettuce rows. The
same plot sizes, positions, care states, pivots and accessible clearances stay.
Density now comes from planted rows reaching the plot edges, not enlarged
plot geometry. High specimens keep curved leaf grids; ordinary field plants
retain their leaves with fewer hidden petiole/fruit sections. First park count
259,508 exceeded the cap: reduced field sections, then got 223,148. Further
mulch simplification is required to retain the previously accepted budget.

Harsh findings, fixed for pass 2:

- Shade in the tomato and bean is nearly black, hiding the material range.
  Double the procedural sky fill without raising exposure or the sun. Keep
  soil/cavity contact shadows, and check the next exported images numerically.
- Zucchini is a clean dark scalloped cutout. Strengthen silver mottling along
  the primary vein axils, with broken patches, and restore the high specimen's
  finer curved grid. The single 1K plant set remains unchanged in allocation.
- Fallow beds are visibly still brown soil: the soil-to-straw material change
  left their UVs pointing at the soil tile. Reproject those faces to straw.
- The shed roof shows wood knots. Native low roof courses had a default wood
  material; classify the upward roof-course faces and assign roofing.
- All shed variants became blue because instance material edits shared mesh
  data. Copy that private mesh before changing site finishes. City gets the
  painted mural shed/reclaimed painted bins, park weathered unpainted wood,
  newer site green paint and newer bin boards. Native deliveries stay read-only.
- The gravel reads like tiny dunes. Reduce its macro height and color wave;
  keep fine granular normals. Wood knots also need a quieter relief signal.
- Park framing loses its adjacent building and exposes an empty horizon.
  Move the existing side neighbor nearer the lot edge and add native trees at
  the park boundary; re-aim from the open gate. No plots or routes move.
- Bean and squash detail cameras crop away too much construction. Pull back
  to show the full support and plant mound, maintaining the real scale.

This pass is a diagnostic, not accepted look-dev. The foliage is fuller but
still regularly spaced and the first opaque palette has too many materials.
Consolidate identical atlas swatches into one stock glTF PBR material before
the next export; the botanical color/alpha atlas remains a separate material.

## Look-dev pass 2 — inspect the baked charts and the photographic pairs

Color/value first: viewed the second exported batch, its three midsummer pairs,
and the five plant specimens. Fallow straw is now golden-gray instead of brown
soil; roofing is dark; faded blue/wood/green finishes distinguish the sites.
The three new opaque maps share one 2K atlas, rather than multiplying memory
by swatch. Direct garden allocations are 24 MiB city / 40 MiB other sites,
including the unchanged 4 MiB plant set, 4 MiB wire field and existing lawn.
The leaf values remain too dark under the raking sun relative to UMN's tomato
photograph. Lettuce is too yellow. Correct species albedos, keeping the existing
sun/exposure and actual shaded cavities. The squash's silver marks are obvious
but repeat as stripes; replace the sinusoidal breakup with seeded small patches
beside its five primary veins. Healthy blades should not all carry identical
bites: put those on the sparse older lower blades only.

WiseWords still exposes too much of the soil beneath a regular crown. Each
mature tomato now receives supported daughter branchlet cards, with nine
script-generated leaflets apiece, overlapping the modeled compounds; this
adds mass in the shrub/tree manner without paying for hundreds more petioles.
Close the bare growing tips with small terminal leaves. Keep each plant below
the accepted 4.6k ceiling. Add compact marigold borders among low crops, using
original alpha flower heads on field specimens and geometry on the hero plant;
these use spare cells in the same plant atlas. The photograph has mixed crops
and colorful painted beds; this is a growth/coverage comparison, not a replica.

The third pair (City Hall, July 2010) exposed a bad camera constraint: its bed
ends are out of frame. The first fit's RMS is 107.8px and its roll is implausible.
Do not call it a strong photo match. Retain that failed image in this pass and
replace the framing constraints before the final comparison. Martin's sign
fit remains 5.8px and WiseWords' bed fit 14.7px, but the regular tenant plots,
chain-link and large lawn alleys intentionally differ from Martin's intimate
flower garden. The additional border flowers address some of the missing
midsummer presence without changing the accepted plan.

The raw UV audit also rejects collapsed charts on elevated boards, marker
caps and imported shed parts. The ground-height clamp was flattening some
charts above .38m. Repair each collapsed chart in the face's geometric plane;
verify exported triangles, not only the source layer. The chips are still too
large and uniformly warm, and the compost heap reads as an undifferentiated
mound. Reduce chip sizes, mix weathered gray fragments, preserve their normal
relief and rejudge the final infrastructure details. Move the mural to the
fixed side siding so it cannot float in front of a moving door.

The plant maps are analytic at 4K and filtered to 1K; the opaque swatches are
Cycles-baked at 4K and filtered to 2K. The prototype high mesh is not substituted
for the exported field geometry in garden renders. The three camera-matched
old-view comparisons remain required in addition to the new open-gate heroes.

## Look-dev pass 3 — reject the small export losses

Color/value first: inspected the 1200px third-pass city set and the park hero,
overhead, old camera, corner, tomato, bean, compost and water views, against the
same balanced photographs. The additional fill and species changes recover green
variation without lifting the deep soil and under-canopy shadows. Silvered boards
and darker ground-contact posts now separate from replacement tan slats; golden
fallow straw, dark watering basins and chip paths read from the garden frame.
The park now has a full stand of beans on five supports rather than a tiny
isolated trellis in a largely empty tenant plot. Its adjacent house and edge trees
also replace the repeated central house backdrop. The city blue shed/mural, chips
and brick walls read differently from the park's wood shed, grass and large plots.

The foliage comparison still catches artificial construction. Some tomato
leaflets floated a few centimetres off the rachis after fine petiole removal.
Seat the retained blade bases directly on the rachis; do the same for the three
bean leaflets. Add the missing secondary pod pedicels on the detailed bean. This
costs 72 triangles per garden and keeps the park below 215k. Independent rays
now measure the actual exported stem-foot vertices against the receiving soil,
in addition to the existing root-origin test. Neither this nor the export
comparison proves photographic plant anatomy; the photographs remain the judge.

The full-size squash photo has pointed palmate lobes, whereas the current
scalloped outline reads like pumpkin. Sharpen those five lobes in the analytic
alpha without adding geometry. Restrict old lettuce blades to the outer basal
whorl so its young heart stays green. Vein-adjacent squash silvering is more
credible than the previous stripes, but repeated texture outlines remain visible.
The bean's regular vertical tiers and the marigold's neat flower rings are also
still CG tells. Keep them explicit in the checkpoint assessment.

The raw audit found that 4K-to-1K filtering erased the fine bird-net alpha below
the .45 cutout threshold. Conservatively cover the source pixels: 23.44% of the
net cell now survives the shipping threshold, rather than silently losing the
net. Compost clippings also lost their chart when a BakeUV layer was joined to
UVMap; normalize that layer name before the join. Every shipped geometric UV
triangle is now noncollapsed and opaque vertices stay within their reserved
swatches. Shared tiling/card overlap is intentional, not a unique atlas unwrap.

Replaced the unreliable City Hall bed-end constraints with the visible cage hoop.
The new fit uses an inferred cage size, not surveyed dimensions: about 2.9px RMS
at 1024px and a 28mm lens. It is useful for foliage coverage and construction,
not proof that the fictional bed is the photographed bed. WiseWords and Martin
remain approximately 14.7px and 5.8px respectively. All three are July garden
photographs of the requested period; Oliver's installation view is retained only
as earlier construction evidence. The final set repeats the old hero cameras
for the before/after evidence, alongside unobstructed 35mm eye-height heroes.

## Look-dev pass 4 — the garden must belong to a block

Color/value first: opened all nine completed city views in the 1200px/40-sample
batch (`renders/lookdev-pass-4/`). Straw, silver/tan lumber, pale blue paint and
dark soil retain separate values under the same raking sun. Deep foliage shadows
persist without a pale overall lift. The tomato detail now has overlapping
compound blades and green/turning/red fruit with connected leaf bases. The
exported marigold border is legible beside the bed corner. Chip fragments remain
too graphic at very close range, and the compost still reads as a simple mound
under its clippings. These are remaining material/form limitations, not resolved
by the passing numerical checks.

The open-gate city hero and repeated old camera exposed a larger composition
failure: removing the shared central house left an empty straight green horizon
behind the rear fence. Stop this intermediate batch and correct that context.
Instance the existing brick apartment across the rear service alley, preserving
the alley clearance, accepted garden plan and all native delivery bytes. This
closes an urban block rather than reintroducing the same suburban house behind
every garden. It adds presentation-context instances, not garden triangles or
new image memory. Repackage and repeat the scene before rerendering the full set;
no intermediate image is promoted into the final evidence folder.

## Look-dev pass 5 — isolated specimens expose the remaining form errors

Color/value first: opened the complete 1200px/40-sample set in
`renders/lookdev-pass-5/`, including every garden view, both catalogues, the five
isolated specimens and the three photographic pairs. The same assumed neutrals
apply: WiseWords gray stucco, Martin's light siding and City Hall's gray board
cap. The city/park/newer heroes have display-luma 5th/median/95th percentiles
.013/.305/.690, .003/.302/.826 and .013/.321/.638 respectively, with zero clipped
channels. These numbers demonstrate preserved shadows and highlight range, not
photographic realism. The city now belongs to a brick block; the park has grass
and broad stands beside trees/building; the later garden foreground shows an
elevated tray and actual knee space. Before/after panes retain the old cameras.

Reject the following remaining form problems before the next set:

- The weedy squash detail reveals only one of the two intended plants. The old
  random 20% crop omission could empty half a compact bed. Neglect must add weeds
  around the planted vegetables, not randomly erase them. Keep the full crop
  grid in weedy plots. Preserve all five care states and all accepted bed centers.
- Pay for that density by replacing the six fine cylindrical axes of repeated
  field herbs with tapered ribbons of their true width. Retain every leaf and
  the hero prototype's modeled stems. Field herbs fall from 200 to 164 triangles;
  the intermediate park count is 213,663 rather than exceeding 215k.
- Tomato leaflets and daughter compounds are mostly edge-on at eye height. Their
  nominal leaf count overstates visible coverage. Add droop, varied branchlet
  pitch and roll, while limiting the lowest compounds' fall above soil. This
  changes visible canopy area without adding triangles or changing real scale.
- The squash alpha revision still has broad rounded tips. Deepen the clefts and
  give the five lobes steeper points. Keep the 24 curved blades and their actual
  dimensions; the next photograph pair must judge the resulting silhouette.
- Isolated marigold heads are almost flat saucers. Dome their existing curved
  grids in proportion to head radius. The original alpha petals stay, with no
  geometry or map allocation increase. This supersedes pass 2's proposed
  geometry petals: both high and field flower heads use curved alpha grids.
- Corn has random whole-blade roll but insufficient twist along each blade.
  Rotate its cross section progressively along the existing grid, preserving
  its joint spacing, leaf count, ears, silk and tassel.
- The first wet-soil assignment covered the entire tended bed. Restore watered
  patches around actual planted root locations, with broken edges, leaving dry
  crust between irrigated rows. The same shared dry/wet swatches supply both.

WiseWords still has more irregular mixed growth and incidental objects than the
fictional tomato bed. City Hall's crops and wooden walls differ from our Plot10;
its cage hoop fit supports framing, not a reconstruction of the whole garden.
Martin is flower-rich and intimate while the accepted park plan is spacious and
rectilinear. Those composition differences remain visible and are not excused by
small landmark residuals. The plant photos remain morphology checks where no
reliable neutral exists. No photograph enters a material or mesh.

One interrupted CPU build briefly overlapped a second attempted build. Both were
stopped in this worktree, and the updated family is rebuilt serially before the
next checks and image set. GPU bakes/renders remain under the shared lock. The
next set is judged from fresh exported files, not patched historical receipts.

## Look-dev pass 6 — keep the growth and audit its supports

Color/value first: inspected all 40 PNG renders in `renders/lookdev-pass-6/`.
Hero display-luma 5th/median/95th percentiles are .014/.301/.690 (city),
.003/.302/.826 (park) and .013/.321/.638 (newer); no channel clips. The plant
comparison neutrals remain concrete for tomato and weed cloth for squash;
bean/corn/marigold comparisons remain morphology-only. Squash is dark with
broken silvering; lettuce is pale with green hearts; kale is distinctly blue-gray.
Old lower blades differ from healthy upper growth without a uniform yellow wash.

The weedy squash bed now has both plants, and the herb/corn/kale/pepper stands
retain their full planting grids. The overheads show tended crowns reaching bed
edges, with bare areas concentrated in fresh and fallow plots and working strips.
The revised tomato view reads as a mass of drooping compound foliage around its
cage instead of rows of edge-on cards. Fruit is partly hidden inside that mass,
as expected. Pointed squash lobes, actual corn twist and domed marigold heads are
visible in their exported close-ups and isolated specimens. The photo comparisons
still expose regular tiering, repeated blade outlines and simplified leaf response;
this is a substantial form improvement, not photographic equivalence.

The attachment audit catches a new error in the flower dome: raising its central
vertex above the authored head position leaves a gap above the stalk. Define the
head's highest center at its stalk attachment and lower the rim. Extend the
existing marigold branch to the upper floret layer, and give the separate spent
head a short connected branch. Squash flowers and fruit also need explicit
pedicels/peduncles from the crown rather than relying on the leaves to hide their
supports. These are real stem meshes, within the same atlas and budgets. The
resulting rebuild measures 122,144 / 214,223 / 109,632 garden triangles; the
largest plant remains 4,488. Re-render and repeat after these connections change.

Visible limitations to carry into the checkpoint report: field grass has no
individual blades; chip relief is shallow and its fragments graphic close up;
the compacted fines have too-even shoulders; compost is still a smooth mound
under sparse clippings. Botanical veins, silhouettes and fine branching repeat.
The three photographic scenes contain more incidental mixed growth and objects
than the fictional sites. Do not describe these as finished product photographs,
and do not add gallery/docs images at this checkpoint.

## Look-dev pass 7 — exported checkpoint handoff

Color/value first: reviewed all 40 final exported renders in readable inspection
groups, then opened the five botanical pairs, three period-garden pairs and three
before/after pairs at full size. Final hero luma ranges are .014/.301/.690,
.003/.302/.826 and .013/.320/.638 (5th/median/95th); clipped-channel share is zero.
Concrete and weed cloth remain the assumed botanical neutrals; period-photo
neutrals are unchanged. Comparisons do not claim equal exposure or surveyed plant
scale. Isolated squash remains cooler/teal and its silvering cleaner than the
balanced photograph; the hero's warmer illumination does not prove an exact match.

The caps now meet their stalks, existing branches reach the upper floret layer,
the spent head has a branch, and squash fruit/flowers have peduncles/pedicels.
This is explicit construction, not a claim from the serialization test. Separate
soil/root/cage checks measure actual exported surfaces. All 40 render receipts
match current export bundles.

Final botanical judgement:

- Tomato fills the cage with drooping, overlapping compounds, but the photograph
  has finer branches, less repetitive serration and more irregular lower growth.
- Squash fills the compact bed with overlapping pointed palmate blades and a
  shaded crown. Veins, mottling and lobe profiles still repeat too visibly.
- Bean groups fill the teepees and park supports. An isolated vine remains airy,
  with regular tiers and straighter pods than the close-up photograph; that photo
  is not a whole-plant density survey.
- Corn stands interlocked with arched/twisted leaves, ears, silk and tassels.
  Anther/silk detail is sparse and the blade response lacks the photo's texture.
  The modern close-up supports morphology, not period-site evidence.
- Marigolds form visible pinnate flowering borders with curved heads. Ray patterns
  and stiff outlines repeat; the genus-level photo is not a replica cultivar.

The sites read differently: city chips/blue mural shed/painted bins/brick block;
park grass/broad in-ground stands/old wood/edge trees and building; newer raised
trays/firm granular court/newer boards. Accepted plans, dimensions, sockets and
moving construction stay. Old-camera pairs are 2400x818 with 1200px panes;
pose/lens/aspect equality is asserted.

Validation completed:

- `make -C community-garden WIDTH=1200 SAMPLES=40`: passed model, refs, repository,
  budgets, normals, fresh import, actual surface contact/clearance, motion, raw UV,
  packaged-scene and render-provenance checks; complete rendered/reviewed set.
- `make -C community-garden repeat`: passed seven independently rebuilt glTF/BIN
  files, three regenerated plant maps and byte-identical authored surface fields.
  Native inputs and baked swatches are retained; exact GPU bake/render bytes are
  outside this repeat check's scope.
- Gardens: 122,144 / 214,223 / 109,632 triangles, 3 / 4 / 4 materials,
  24 / 40 / 40 MiB direct compressed full-mip image allocation. The fourth material
  preserves native lawn. Plants remain one shared 1K/4 MiB set; opaque swatches
  share one 2K/16 MiB set. README lists all modules and measured file sizes.
- No collapsed exported UV triangles or escaped swatches. Density is measured;
  intentional tiling/card overlap is not a unique-island claim.
- All 479 recorded other-family deliveries remain byte-identical. No kit change,
  authored top-level README change, gallery or docs images.

Stop at the requested look-dev checkpoint. Remaining CG tells are regular
spacing/branching, repeating analytic leaf surfaces, approximate transmission,
flat field grass, shallow graphic chips, even gravel shoulders and simple compost.
Period pairs retain crop/context differences; City Hall's hoop scale is inferred.
Passing measurements do not resolve those visual weaknesses. Nothing is needed
from the lead to reproduce this state.

## Delivery pass 8 — first correction crops, rejected for final use

Color and value first: opened all 15 new 1200 px exported views, the rebuilt
historical corn-ear close-up and all three full photographic pairs. The grass
is still too brown and low in value: a sunlit park patch is RGB 86/95/54,
display Y .354, versus 105/138/79 and Y .498 in the Wise grass after balancing
on its gray apartment stucco. Martin's house-siding balance gives much brighter
dry July turf (Y .724). Exposure and illumination differ, so these are visual
constraints, not measured albedos. Keep the hero exposure and accepted surface
sets; raise the private summer lawn's healthy green value, retain localized dry
patches and strengthen the fine blade silhouettes at bed edges. The Wise and
City Hall foliage also sits too dark against the balanced photos; soften the
Wise comparison's light and lift the City Hall comparison's sky fill before
judging fine form. Hero eaves, underside shade and sunlit lumber already retain
useful depth without clipped highlights.

What improved: the tomato is now a closed, cage-overflowing mass at 4,200
triangles. The foreground heads have different sizes, rotations, leaf counts,
colors, intermediate stages and failed gaps. The park plots are cut from turf;
the recreation hall, houses and edge grove replace the gray horizon. The white
foreground object was a clipped row cover; moving it onto the rear seedling bed
removes it without changing the accepted city camera. Upright husked ears now
leave the actual corn leaf joints; their measured opaque surface is about
.237 m long at 29 degrees from vertical. The fixed-camera close-up proves the
old pendant pod shape is gone.

Still CG / corrections owed: the lawn remains a flat thatch-like field between
its sparse edge blades; clover needs rooted petioles. The granular court now has
angular grain but its print sampler misses part of its compacted swatch, and
many loose stones are buried in the feathered shoulder. Deformed earth needs
terrain stations on the rows and updated smooth normals. The complete Wise
site comparison now has neighboring crops, chips and apartments in frame.
City Hall still reads as one edge bed beside empty lawn despite importing the
whole accessible site: move that garden's tomato stand to an interior plot and
fit to that actual cage, with neighboring squash/greens in the foreground.
Martin has its real park and new entry planting, but its mounds are too small
behind the fence. Enlarge only those entrance marigolds within the same genus
and triangle count. Leaf silhouettes, regular branching, smooth fruit and the
very even granular microstructure remain obvious close up. No docs approved.

## Delivery pass 9 — whole-site pairs and summer turf, before final corrections

Color and value first: opened all 15 native 1200 px pass-2 PNGs and all three
full photographic pairs, then reopened the three original garden photographs.
In the same park-hero lawn region (x950–1150, y550–680), median RGB changes
from 73/90/65 to 103/128/65; display Y rises from .332 to .463. The assumed
neutrals remain Wise's gray stucco, Martin's pale house siding and City Hall's
weathered gray board cap. Different exposure/light prevents an albedo claim.
The body grass now has visible blade/thatch normals and muted yellow-green
variation. The upright edge cards are still too bright and tall, reading as a
lime fringe. Shorten them to a clipped 25–45 mm visible height, lower their
albedo and reduce the yellow bias. Put an actual brown dry patch in the
visible exposed southern shoulder, instead of leaving its strongest mask
outside the hero's field of view. Keep the low sun, unclipped lumber and deep
canopy/eave shade.

The park is now clearly cultivated earth cut into turf, with different head
sizes, leaf counts, colors and stages, and failed gaps. Its hall and grove
close the hero. The tomato comparison is a closed mass extending beyond its
cage; individual leaflet silhouettes and tiers still repeat too much. Ears
are upward at leaf joints and have a brown tip, but the crossed spent-flower
cards read as a star-shaped cap in the ear close-up. Replace that cap with
curved individual silk ribbons at essentially the same field triangle cost.
The granular court now has angular grain, loose edge stones, steel edging,
sole prints and wheel tracks. Its aggregate distribution remains too even.
The city row cover is smoother and farther back, but still clips the right
frame edge as a gray blob; remove the city instance outright. Keep the reusable
piece and the other gardens' covers.

Wise now frames neighboring corn, beans, herb margins, chips, apartments and
the actual tomato stand. City Hall frames the interior stand and foreground
squash, but still exposes a featureless horizon behind the shed. Add rear
neighbors and mature rear canopies without moving its accepted houses/trays;
fit to the stand's opposite actual cage to improve the foreground overlap.
Martin frames the service beds rather than the park's dense tenant plots;
its left flower margin is outside the fitted field of view. Place the park
sign on the cultivated side of the entrance and flank it with the two public
flower margins, keeping the gate approach clear. Refit that actual sign.
These are corrections in the delivered sites, not replacement fixtures.

Still CG: analytic leaf veins and serrations, regular vine tiers, star-like
marigold florets, shallow graphic chips, even aggregate and repeated native
tree crowns. Squash still runs cool/teal in its isolated comparison. The
first batch was interrupted after five saved views; the remaining set resumed
from disk and completed with exit 0. No gallery images have been generated.

## Delivery pass 10 — third correction set, final two framing issues

Color and value first: all 15 native pass-3 PNGs and all three complete photo
pairs were opened at original size. The shorter, darker blade fringe now
belongs to the lawn instead of glowing lime. Sunlit boards retain grain and
canopy shadows remain deep. The same assumed photo neutrals apply. The main
lawn is lighter/yellower with visible blade normals, but the authored dry
station still misses the park camera: ray projection places the visible lower
right shoulder around x0/y−5, rather than x2.4/y−8. Move that localized mask
there and put forty small crossed tufts along the path shoulders, leaving its
worn centre clear. This uses 320 triangles within the original garden limit.

The city white edge object is gone. Ears rise from their actual joints; the
close-up now shows separate brown curled strands instead of a flower cap.
The silk is still angular and sparse, and the husks very smooth, but the
pendant-pepper construction is gone. Tomato mass and varied leafy heads hold.
The accessible hero keeps its trays and original houses; its pair now shows
neighboring beds, foreground squash, canopies and houses instead of an empty
horizon. Foreground grass still occupies more of that composition than in the
photograph; the real crop mix and bed proportions are different.

The park pair still looks diagonally through a broad lawn toward the service
area, despite moving the sign left. Move/angle the actual sign on the cultivated
frontage, clear of the fence, then apply the same rigid transform to its photo
landmarks and initial camera. That directs the full-site view toward the corn
and tomato plots without changing the hero camera or staging an isolated bed.
Use matte dark painted letters instead of reflective metal on the old boards.
No change to the camera-fit residual can prove surrounding density: judge the
new exported picture. Leaf repetition, clean analytic fruit, regular trellis
tiers, shallow chips, even aggregate and cloned native crowns remain CG tells.
No gallery images approved yet.

## Delivery pass 11 — fourth set and a serialization failure caught visually

Color and value first: all 15 native pass-4 PNGs and three complete photographic
pairs were opened at original size. The park's newly positioned/angled sign
now frames corn, leafy plots, flowers, the hall and the neighborhood. The assumed
neutrals are unchanged. Yet the lawn still lacked the designed mowing, dry and
traffic variation. Raw garden COLOR_0 carried it (green down to .523), while
that same lawn primitive in the full-site export was entirely white. Moving
the dry mask could never correct that loss. The presence/count of a color
attribute was an inadequate serialization check.

The full-site exporter now explicitly resolves imported color layers, exports
the active color stream and strips it from materials that do not consume it,
so Wind remains separate. A new independent raw-stream audit compares actual
local position/RGB records, collapsing only duplicate seam samples. Measured
maximum linear RGB differences are .004148 / .004504 / .004498 for 117 / 229 /
341, within the .0046 limit for Blender's BYTE_COLOR import and U16 re-export.
This proves color serialization; the next native exported images must prove
the lawn's appearance. The street-side turf verge also carries mowing and
curb/sign-side dry variation, rather than leaving the photographic foreground
as the untinted presentation plane. No texture allocation was added.

The new hall received pull-handle standoffs and door-bottom clearance above
its threshold. Its added exported-solid sweep caught a 5 mm glazing/jamb clash
at 90 degrees. Reducing the jamb's projection to 200 mm gives both leaves their
full ±90 degree travel with zero reported penetration at 5 degree samples.
Garden gate/shed sweeps, actual surface contacts, UVs, budgets, fresh imports,
all three color-transfer audits and the 479 protected deliveries now pass.
These checks prove construction/serialization, not photographic realism.
The fifth correction set is pending; no gallery images have been generated.

## Delivery pass 12 — native correction crops accepted for final rendering

Color and value first: all 15 pass-5 native PNGs, all three complete garden
pairs, and all thirteen native before/after crop comparisons were opened at
original size. Photo balance still uses Wise's gray stucco, Martin's pale
siding and City Hall's weathered gray board cap as assumed neutrals. The
exported park lawn now carries the lighter yellow-green blade grain, mowing
variation, worn shoulders and localized brown dry patch. Dark leaf interiors
and the shed eaves stay deep; sunlit boards retain tone and grain. All three
heroes use the same clear low sun, and the city edge blob is absent. Native
full-quality finals remain to be judged for foliage noise.

The park's cut-earth plots, real hilled rows, municipal hall, rear houses and
canopies close the view. Leafy heads vary in size, stage, hue and rotation,
with failures rather than a uniform filled grid. The tomato closes into an
overflowing canopy. Corn ears rise from leaf joints with husk leaves and
curved brown silk. The accessible court has angular grain, steel edging,
loose shoulder stones and compressed sole/wheel marks. Accepted tray and
house construction, city composition and shared texture allocations remain.

Wise and Martin now show neighboring beds, paths and populated surroundings.
The City Hall comparison's first interior accessible-site fit still exposed
too much open lawn. Its final fit uses the actual city plot-10 cage from the
clear central path, with foreground corn, neighboring herbs, beds, wood chips
and apartments. Only camera/landmark placement changes; no plants or cage
move for the comparison. The circular cage permits a free azimuth phase; the
measured reprojection RMS is 3.53 px. These are inferred landmark matches,
not a claim that either fictional site duplicates the photographed garden.

Still CG: repeated analytic leaflet serrations/veins, regular vine tiers,
smooth fruit and husks, sparse angular silk, cool squash leaves, star-like
marigold florets, shallow graphic chips, even aggregate and repeated native
tree crowns. All requested corrections show in their crops; proceed to the
clean final build. No docs images have been generated or approved.
