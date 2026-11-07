# Form and construction review

This is the requested pre-look-dev gate. Quick concrete/steel colors, existing
Ground tiles, original sign graphics and native-library context are exported
before rendering. No final bake, game-ready material pass or documentation
gallery is claimed. Photographs are comparison inputs only.

## Pass 1 — cross-section and the two places

Viewed every `renders/pass1/{101,202}/{hero,above}.png` Eevee preview against the
2008 freeway photo and 2002 USGS diamond aerial.

**Color/value first:** paving is darker than the quick barrier concrete, with
readable under-bridge shade. The gray sky is a procedural lighting background,
not evidence of calibrated albedo. No exposure correction was used to force a
photo value match. Surface finish remains deliberately incomplete.

Rejected reversed winding on the mirrored carriageway/earthwork; large areas
disappeared from the aerials. Corrected exposed-skin winding independently of
closed manufactured sections. The first overview was so distant that terminals
could not be judged. Added closer aerials and kept a full-corridor view for the
speed-change lanes. The curved, raised, asphalt corridor with wide cable median
and sound walls is a genuinely different civil section from the depressed,
concrete-paved diamond; it is not another dressing of the same plan.

## Pass 2 — bridge structure, signs, context budgets

Viewed the Cycles `renders/pass2/101/{hero,above,pier_girders}.png` and
`202/{hero,above}.png`, plus the closer terminal previews. Compared cap, girder
and bearing construction with FHWA's 2008 photo. Its pile bent is a different
design; it does not authorize inventing dimensions for our columns.

**Color/value first:** the concrete is sufficiently dark to model under the
bridge, but uniformly colored and unworn. This reads as a form model, as expected
at this gate. Increased sun-to-sky ratio for the inspection views so bearings,
webs and slope paving can be judged under raking light; kept fixed exposure.

Rejected abutment seats extending through the girder ends. Lowered the actual
seats and separated the backwalls. Corrected plate/bearing/cap stack and matched
pad heights to actual camber. Split the girders and bent into reusable assembly
parts; end diaphragms remain real geometry. Replaced a second wide F rail with
a thin pedestrian parapet to recover a true 1.524 m clear sidewalk. Moved outer
girders to 3.048 m centers for a plausible deck cantilever.

Rejected a guide panel over opposing lanes and structures downstream of the
exits. Both faces now sit above their own carriageway, upstream in the auxiliary
lane; arrows align with through-lane centers. The generic cantilever is a module,
not claimed to be an engineered support calculation. State marker and legends
are fictional; the DejaVu substitute is visibly less like FHWA lettering.

## Pass 3 — gores, terminals and failed context reductions

Viewed the 1400 px construction close-ups and the `final-form-preview`,
`roof-proof` and `envelope-proof` images at full size.

**Color/value first:** opaque, coherent silhouettes matter before weather.
The first collapsed car had crumpled reflections, and the reduced houses had
literal missing/spiked roof patches. Those were geometry failures, not a reason
to disguise them with a brighter exposure or noisy dirt.

Rejected the collapsed nearest car; the closest vehicle now retains the original
full H120 geometry. More distant traffic uses explicitly local context LODs.
Generic collapse could not preserve the houses' disconnected weather-grid
boundaries. The context adapter now uses the house family's exact delivered
roof planes, clipped wall outlines and opening plans, with canonical surface
maps and simple distance fixtures/foundations. These are disclosed plan-derived
context proxies, not unchanged house deliveries. The arterial commercial parcel
uses the full native convenience-store exterior and an original Ground-tiled parking parcel, omitting the
gas canopy/pumps instead of displaying a broken collapsed version.

Cut the sidewalk through the branch mouths; added 40 ft curb returns and
separate arterial/off-ramp stop bars. Fixed the two-way turn-lane pattern.
Aligned the ramp path with the auxiliary-lane center, followed the mainline crossfall plane
through the throat, and placed gore paint on a real interpolated paving wedge.
The attenuator is beside the diverging lane rather than on its driving path.
Rail, blockout, post, cable and terminal remain constructed parts. ROW fabric
uses the fence family's actual analytic wire field, not opaque cards.

## Pass 4 — rejected distant earthwork

**Color/value first:** the first complete exported aerial had near-black,
blade-shaped areas across otherwise flat grass. These were folded construction
surfaces and their shadows, not convincing soil variation. Changing exposure
would have hidden the diagnostic.

The ramp and ordinary terrain sections used different breakpoint meanings.
At their boundary the generator joined a ramp edge to a far-field break; the
initial branch edge could also cross its neighbor. Rebuilt the sections with
the same ordered ditch/branch/crest/field stations. The far continuation now
keeps the cut profile, instead of jumping from the depressed road directly to
high ground. It samples the curved continuation rather than drawing a single
long chord. The curved scene's far field is planar, avoiding offsets beyond
the alignment radius. The fresh-import check now inspects geometric winding
of every earthwork triangle. The aerial render remains the visual proof.

The repeat audit also rejected a single unstable imported-tree tangent value.
Optional stored tangents were omitted; importers reconstruct them from UVs and
the preserved normals. The following repeat matched all 20 geometry buffers.
An empty native-store selection was caught and changed to the actual delivered
mesh names; native selection now asserts nonempty output. One background tree
was removed to keep the intact store and remain under the scene budget.

## Pass 5 — approach support, traffic shading and guide placement

**Color/value first:** the terminal view still had a large black void below
the road, while the distant SUV had crushed reflections. Neither was weather.
The first was missing approach fill; the second included normals pointing
through thin body panels. Houses now have complete outward-facing roofs in
the exported terminal view.

Raised the arterial approach fill behind the abutments, widening its plateau
at the ramp terminals with 1:4 side slopes. Added the arterial pavement's base
and side section. Eight independent soil/pavement rays now measure zero gap.
The original normal-transfer method put 2,714 of 8,301 inspected SUV corners
opposite their triangle normals. The local LOD now has a coherent weighted
field with a face-normal cone limit. It keeps native BaseColor/ORM; the full
mesh's normal bake is removed from distant derivatives because it belongs to
a different tangent field. The nearest car retains the full native mesh and
all maps. Actual exported normal hemispheres are checked.

Opposing guides now say SOUTH / Cedar Hollow and NORTH / Alder Junction.
The curved stretch has one through panel over its own carriageway, rather
than an exit panel implying an absent ramp. Level trusses have unequal legs
and embedded concrete footings sampled against their actual graded earth.
Fresh-import rays measure concrete-base burial, rather than trusting a common
placement elevation. Both guide directions receive inspection views.

## Pass 6 — exported inspection and period comparisons

Inspected all 15 exported scene views, 17 individually framed modules, the
human/car scale shot, the module sheet, the three matched views and their
side-by-side pairs. The final set contains 36 individual Cycles renders.
`renders/checkpoint/contact.jpg` and `renders/matches/contact.jpg` collect them.
These files remain ignored at this checkpoint; no `docs/` images are committed.

**Color/value first:** the diamond hero's display-luminance 1/50/99 percentiles
are .0109/.5288/.7513; the curved hero's are .1003/.4916/.7546. Clipped RGB
samples are .0165% and .0022%, mostly small vehicle-light highlights. These are
whole-image display values, including sky, not measured surface albedos.
Under-bridge cavities retain deep shade without a pale hero exposure. The
barrier, cap and wall are still uniformly colored quick materials: they do
not yet reproduce used concrete. The sign green is darker and less cyan than
the photograph, and DejaVu's condensed lettering differs visibly from FHWA's
alphabet. Pavement lacks the photograph's polished wheel paths, longitudinal
repair history and grime. These are explicit look-dev debts.

The first matched bridge image was unusably dark. A directional-light change
made its cap visible, then a temporary neutral inspection floor supplied the
ground bounce absent from an isolated bridge over empty sky. Camera exposure
was kept fixed. This improves inspection, not the asset's materials; the
floor is absent from every export.

The camera fits use a guide-panel plane, a cap plane and central interchange
landmarks. They are feature comparisons, not surveys of the photographed sites.
The freeway photograph has more lanes, the bridge uses different beams/bent,
and the photographed diamond curves on its west approach. Those differences
remain visible. Fit residuals are 6.975 px for the guide, 5.312 px for the cap
and 1.669 px for the diamond, in original-photo pixels. Independent Blender
projection disagreement is at most .00837 px; that proves camera transfer,
not agreement with a surveyed site.

The guide pair supports the panel scale and overhead construction, while
showing that our four-lane rural-edge corridor is much less dense than the
photographed urban freeway. The diamond pair supports the long, separated
branches and terminal arrangement; it also makes our straight mainline and
sparse, orderly town context conspicuous. The bridge pair compares cap,
bearing seat and girder layering only: the photographed SCC beams/pile bent
are different construction from our Type IV-envelope girders/round columns.
The ordinary inspection underside view shows the complete two-span load path.

The final module/scale views preserve the F profile, W-beam folds and blockouts,
real post pitch, rail anchor form, panel-in-post sound-wall construction,
three-column bent and individual girders. The two seeded plans read as distinct
places at shoulder height, with town streets and houses beyond the ROW; the
context remains sparse and repetitive in aerials. No more form changes were
made after this inspection.

White balance uses concrete paving for the freeway, the unpainted cap for the
bridge and a gray industrial roof for the aerial. These are approximate field
neutrals, not gray cards; gain values, original RGBs and rectangles are in
`build/reference-balance.json`. Exposure is unchanged during balance. The
calibrator and independent Blender projection check have separate reports.

Remaining form limits to carry to the lead: the generic barrier end/attenuator
and sign members are not reproductions of certified products; ramp terminal
sweeps are plausible geometry rather than a full vehicle swept-path design;
the source excerpt begins/ends within a constant-radius bank, with a separate
partial bank-transition module for chaining. Context proxies are intentionally
simple at street distance. Guardrail splices/bolts, pavement edge distress,
bridge repairs and drain staining, shoulder debris, weeds and wear remain for
look-dev. No random weather wash has been substituted for that work.


## Revision pass 1 — form, town and the first lighting rejection

**Color/value first:** the retained checkpoint had pale, uniform concrete and a
neutral sky. The first revised sun lit the pavement but put the bridge fascia
and near cap into excessive shade. Rejected that direction after opening the
1200px hero and underside at native size; moved the low sun to the visible
fascia side and increased physical sky fill. The resumed curved/terminal views
show long shadows and retain dark wall bases without clipping the concrete.
This is a form review; it does not certify the later baked finish.

Opened all nine `renders/form-corrected/` images at native resolution: 101 hero,
aerial, sign, underside, gore and terminal; 202 hero, aerial and sound wall.
Compared the aerial to the 2002 USGS photo, the underside to FHWA's 2008 image,
and traffic to the 2008 and newly retrieved 2007 road photographs. The two
unchanged civil alignments now have towns: commercial parcels at the diamond,
residential grids either side, and backyards/dead-end cross streets beyond the
curved corridor's sound walls. Original house-plan distance shells remain
recognizable and repeated; this is context, not a new house family.

Rejected the old open black ramp-terminal edge. Added measured-to-soil shoulder
returns and curb backs. The first revised image exposed small unclosed corner
wedges; added triangular corner closures. Extended the context arterial beyond
the civil excerpt rather than leaving its cut end visible in the aerial.

Verified the girder profile against TxDOT report 0-4751-1 vol.2, Figure A.1.4.1
(page 18 of the PDF): 54in depth, 20/26in top/bottom flanges and 8in web, with
8/9/23/6/8in vertical divisions. Added haunches, intermediate/end diaphragms,
a 50mm cap chamfer and the deck drip groove. The first plinths were buried in
the cap; lowered the cap body/abutment seats while preserving pad and girder
contacts, so actual bearing pedestals can read. Closed a missing underside
strip beside the outer girder. These corrections are judged again in look-dev.

The 5k traffic derivatives look too angular close to the shoulder. Restored
full native bodies in the near zone, keeping the native hatchback at its
accepted anchor. All three original bodies and five native factory colors are
seeded. The color derivatives decode the cars' own baked coverage into ordinary
local RGB maps; no reference image enters a shader. Added queue priority and
lane-space reservations to prevent a flowing car occupying a queued position.

Form exports measured 223,232 and 127,170 freeway triangles before the final
edge/plinth corrections and age geometry. Context and actors are separate
external glTF packages, so the 400k freeway ceiling is checked independently.
No existing library delivery was regenerated in place.
