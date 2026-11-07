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
