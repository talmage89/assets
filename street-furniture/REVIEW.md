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
