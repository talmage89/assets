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

## Look pass 1 — first baked exports, 1100px / 20 samples

**Color/value first:** actual shipped BaseColor median linear luminance is
.2702 for cast concrete, .2542 for Ground concrete and .1407 for asphalt.
The direct sun and sky now share a direction, with exposure kept at −.45.
The guide faces read green rather than black, and bright concrete rolls off
while the underside keeps deep shade. The used-road value range is credible;
the problem in the foreground is the scale/pattern of the dark marks.

Opened every `renders/look-pass1/` image at native size: both heroes, 202 aerial,
101 terminal, underside and guide structure. Compared the same surfaces with
the balanced 2008 freeway, FHWA underside and USGS town photograph. Rejected
the wide, short crack clusters on the concrete: they read as three stretched
zigzags stamped across the lane. Narrowed them to 0.25–0.50m envelopes, with
1–3.2m runs, offset by lane; the atlas' thin crack becomes a millimeter-scale
line. Flipped placement-owned charts and dephased wear by travel direction.
The initial wheel lanes were too symmetric across opposing carriageways.

Rejected the column repairs' tar-like rectangular outline and yellow cast.
That chart belongs to sealed paving. Repairs now use the same baked concrete
manufacture with a small gray mortar-value difference and an irregular boundary
conforming to the cylinder. Strengthened joint/scupper-connected staining on
actual girder vertices; no general concrete noise wash was added. Added low
stations to the sound wall's bottom panel so splash remains below 0.5m rather
than fading over the whole 1.4m panel. No new texture set is needed.

The restored near native bodies have coherent reflections and round wheels.
Flowing traffic has unpowered daylight lamps; queues retain brake emission.
Increased arterial queue center spacing to 6.9m so the conservative lane-space
reservation keeps three stopped cars rather than dropping the middle one.

Independent fresh-import checks passed on this first look export. Freeway
counts were 264,786 / 157,618, excluding town/traffic. All 17 module UV sets had
zero degenerate triangles. Edge probes checked 3,552 / 8,256 actual skirt feet,
with no positive soil gap and at most about 25.4mm burial. Distributed bearing
probes measured −0.760…+0.755mm camber-related pad variation and zero plate-to-
pedestal gap. Three imported girder sections measured the 26/8/20in widths.
These prove construction/serialization, not photographic quality or engineering.

Still CG in this pass: overly crisp shoulders and parapets, the patch outline,
repeated house/tree silhouettes, a lawn that is much more regular than the real
town, and scalar small rubber/wood parts. The ensuing pass judges the fixes.

## Look pass 2 — native views and four photographic pairs

**Color/value first:** the corrected crack scale removes the foreground black
stamps and the gray repair no longer has a tar outline. The photo pairs expose
two lighting errors that must not be corrected with concrete color: the 2007
cloudy asphalt comparison receives blue clear-sky fill, and the bridge neutral
ROI was on stained brown concrete. Replaced it with the clean cap edge at
(1100,1410)–(1140,1470); measured gains are about .991/.991/1.019 instead of a
1.33 blue boost. The cloudy pair now desaturates its sky fill; the bridge pair
gets more ambient illumination and less direct sun, with camera exposure fixed.

Opened all six `renders/look-pass2/` native views and all four native pairs.
The pier, shoulders, lanes, signage and traffic now hold their scale. The used
bridge remains too uniform compared with the photograph, even allowing for its
different SCC beams/pile bent. Widened and strengthened only the atlas' joint,
scupper and corrosion tracks; placement remains tied to drains and bearings.
This changes the maintenance set, not the other three bakes. The palette stays
40 MiB. The cap/girder web still looks cleaner than the reference at a distance;
the final pass must disclose any remaining gap.

The 2007 fit was initially 35.85px at a 200mm bound. A landmark inspection showed
that the supposed pavement edges were inside lanes. Re-measured the inside
yellow edge and a two-lane span, ending on the photo's second divider. The fit
is now 1.49 native pixels at an estimated 163.76mm virtual crop lens. The photo
has additional outer/auxiliary lanes and no sound walls. This is a type/material
comparison, not a survey reconstruction. The other residuals remain 6.98px
(guide), 5.31px (cap) and 1.67px (diamond). Projection-transfer error is checked
separately in Blender.

Rejected the pale concrete-repair chart on Cedar Hollow's asphalt. Those repairs
now use the original asphalt texture at a darker new-paving value. Also found
that glTF clamps vertex tint gains above one: the formerly brighter replacement
rail and mortar could lose their distinction. Old rail now has a .86 tint and
replacement bays retain 1.0; repairs use a modest darker gray mortar tint.

The aerial pair exposes a remaining town error beyond the freeway: a local
street passes through the strip parcel. Reserved the complete parcel, routed
that street behind the center, moved the gas parcels between public streets,
and joined the arterial to the actual native driveway apertures with graded
aprons. Removed the houses conflicting with the rear cross street. Added true
left-turn glyphs to the arterial center lane and corrected the through arrows'
heading. A closer controls view and rail-replacement view supplement the
unchanged checkpoint cameras.

Still CG: the repeated house prototypes and regular lot rhythm, sparse small
brush, broad Ground asphalt variation, idealized crisp concrete edges, low
parallax of the fine rib/wire surfaces, and less complex bridge patina than the
photograph. The final export set is judged after these corrections.

## Look pass 3 — native export, zinc rejected

**Color and value first.** Opened all seventeen 1400px views preserved in
`renders/look-pass3/`. Concrete and asphalt retain their .270/.254/.141 median
linear map luminances and the raking heroes have deep bridge/wall shade. The
rail and post close-ups expose a different error: high local contrast between
rough oxide and reflective zinc makes the steel read as crumpled foil. Against
the daily-freeway photographs this is stronger and more broken than real aged
galvanizing. The shipped normal's 5–95% X range is only ±1/255, so geometry or a
large normal amplitude is not the principal cause. Its roughness and metallic
islands vary far too strongly.

Rejected that zinc response. Narrowed crystalline color variation, raised the
old coating's base roughness from .53 to .72, reduced oxide/metal contrast and
reduced the already small manufacture height variation. Kept the actual dents
and replacement-bay placement, the 1024 triple and every triangle budget. A
new bake and two original-camera rail/sign inspections precede the final set.

The first final aerial still exposed an empty town fringe. Extended Alder
Junction to seven parallel streets per side and 663 native-plan house shells,
with additional garden trees. Cedar Hollow has 216 houses after removing the
previous outer-row length cutoff. Its actual imported house/fence envelope
clearance is now at least 2.502m. The places read differently; the regular lots,
repeated two house types and limited canopy still read as generated context.

The girder web/flanges, cap chamfers and contact construction now read from the
original hero and bearing cameras. The apron no longer floats; the close
controls view shows arrows, stop bars and wrong-way controls. Caused joint and
scupper deposits survive the bake, while the broad barrier faces and concrete
edges remain cleaner and more ideal than the used photograph. Those remain
appearance weaknesses, not claims disproved by the geometry checks.

Also rejected the distance car meshes where the sign/gore/terminal cameras
approach them closely. The original origin-only detail zone was inappropriate
for these other views of a 1.6km scene. Actors within 36m of those fixed cameras
now use the complete native vehicles. The positions, colors, speeds and random
stream remain unchanged; the separately reported 101 traffic cost increases
to 3,702,680 triangles. No freeway triangle or texture allocation changes.

## Look pass 4 — paint transfer and comparison illumination

**Color and value first.** The 2007 pair's mostly pale fleet prompted a
numerical check rather than another lighting adjustment. The traffic adapter
had treated a byte-image pixel buffer as shader-linear color. Against the
native PNG's documented linear reference-plus-coverage transfer, the Carbon
variants were wrong by 40–59 sRGB bytes on average. That was my adapter error,
not a pale freeway material or a reason to darken the road.

Opened all 19 scene views, 17 module views, the scale view, four shipped pairs
and four source-field pairs preserved under `renders/look-pass4/`. Replaced the
adapter with explicit decoding of the original native GLBs' embedded RGBA PNGs,
linear factory-color adjustment and filtering, and a single sRGB encoding.
Source/recipe hashes guard the twelve local color maps. An independent inverse
check on actual exported material image bindings subtracts the coverage-scaled
factory delta and recovers the filtered original reference. It excludes clamped
filter boundaries and passes all twelve variants within 8-bit quantization.
No native delivery, body geometry, traffic pose or triangle budget changes.

The balanced bridge photo still makes the isolated module's sky fill look too
blue and dim; the photograph has broad diffuse fill and ground bounce. Raised
that comparison's sky strength .30 to .70 and desaturated it to .08, with
exposure and concrete maps fixed. The guide's photographed front faces receive
more sun than the old near-vertical test sun: changed only that comparison's
direction to (.2,.45,-1), energy 5.4, preserving approximately the horizontal
pavement's direct illumination. The raking hero lighting is unchanged.

Source-field versus shipped comparisons retain the large repairs, joint/drain
tracks, sign legends and lane history. Fine manufacture grain is softer after
shipping reduction. Both versions remain more uniform than the photographs:
the broad barrier/cap surfaces, smooth mowing, regular lots and repeated house
types remain the largest CG cues. The final set is regenerated after the paint
and comparison-light corrections; these images are a rejected intermediate.

## Look pass 5 — corrected exports and native before/after views

**Color and value first.** The guide pair now has a clearly green sunlit face,
rather than the old nearly black face. Compared with its pavement-balanced
2008 photograph, the new concrete still has less broken lane history and a
more uniform surface. The 2007 asphalt pair is balanced on the same gray-road
ROI recorded in LOOKDEV; the corrected native paint now separates Carbon and
Graphite from the white/silver fleet, although this seed and the five native
colors still put many light vehicles near the camera. The asphalt's broad
cloudy variation remains too regular relative to the photograph.

The source-bearing comparison uses the clean-cap neutral and revised diffuse
fill, with material albedo and exposure fixed. Its gray concrete no longer
inherits the earlier blue sky cast. The photographed cap and beams have much
more irregular brown/olive contamination, casting variation and accumulated
streaking. Two placed bearing tracks cannot substitute for that richer history.
Broad cap, barrier and wall faces remain too clean, and concrete edges too crisp.
The deep hero shade and sunlit surfaces have usable range; the full-frame
display measurements and object ROIs are in `build/tones-look.json`.

The native before/after views show the town grids and terminal parcels,
queues and through traffic, seated pavement, I-girder lines, mowing/drainage
construction and long shadows. The source and shipped photo views preserve
the large repair, joint, tire and drain causes. The delivery reduction softens
fine concrete/zinc grain and some chart edges; it does not lose the main
construction or original legends. This inspection compares the four new
4096 source fields on exported geometry, not an unexported high-detail scene.

The aerial is still conspicuously procedural: repeated white house envelopes,
regular roofs/lots, sparse and repeated native canopy, smooth cut slopes and
hard mowing boundaries. The gore and repair close-ups also contradict a
favorable reading of the shaded rail view: zinc is duller than pass 3 but its
crystalline pattern is still exaggerated and can read as crumpled metal.
The selected rail bend is shallow and more regular than real impact damage.
These remain appearance defects, alongside limited alpha rib/wire parallax
and the expensive optional town/traffic packages.

The final receipts exposed a stale shipped bearing image: source/bundle hashes
were current, but the cached shot retained sky strength .30 while its camera
file requested .70 and saturation .08. The cache now compares the complete
shot record, and the independent review rejects mismatched camera/light data.
A regression check rejected just that image and retained the other three
current shipped comparisons. The interrupted set is recorded in the ignored
`build/rejected-stale-camera.log`; it is not a passing final receipt.

The corrected shipped bearing was then regenerated and opened against the
same balanced photograph and source-field view. Both retain the neutral fill;
shipping softens fine grain but preserves the bearing tracks and I section.
The final `make` exits successfully with all eight matched shot records current.
Opened all 45 raw rendered views: 19 scene views, 17 modules, the scale view,
four shipped photo views and four source-field views, plus the labeled sheet,
photo pairs, before/after evidence and contacts. The reviewed remaining defects
above still apply. This round stops before a README gallery or docs images.
## Delivery critique 6 — first dense town, rejected hero and lost assembly tint

**Color and value first.** Opened all nine native 1200 px views in
`renders/final-pass1/`: both 101 compositions, both 202 compositions, both
aerials, pier/girders, bearings and sign structure. The clear low sun now
produces a blue sky, deep under-bridge shadow and unclipped surfaces. The
sky is too cyan, the aerial foliage too black, and native house facades are
still white. Read the actual staged GLB's CORNER colors: gray/sage/cream
siding and colored roof factors are present there. Read the town's actual
accessors: the second import renames the layer Color, while assembly exports
only Tint. The native tint is lost at that boundary. The adapter now retains
that layer only when the material actually reads color, leaving Wind data
independent. A new raw-export assertion rejects a missing COLOR_0 on a material
that declares tiling_vertex_tint.

The 101 hero is rejected: its dominant foreground fence still hides the freeway.
Move it to the arterial's east-terminal walk, looking west across the bridge
and down into the cut, with the west gas canopy, strip signs and queues in frame.
The aerial has the requested small lots and substantial canopy, but wholesale
reserved blocks still leave a 256 m empty band along the arterial. Reserve only
the actual commercial/apartment parcels and fill the rest with houses, yards and
alley segments. In 202 the front tree belt still hides every roof and wire. Thin
that belt, plant the first houses' trees toward their street frontage and retain
actual Telephone/primary sockets and sag. The Telephone key had been wrong.

Turf is warmer/yellower, with original Ground blade grain and dry-height color
stations, but long bands still read smooth; bring rooted seed stems to the
upper cut and sound-wall mowing edges, instead of hiding them at the ROW fence.
Runoff no longer has rectangular stamp boundaries and reads in the original
cut hero. Its cap channels are too strong and too regular; lower their opacity,
retain the damp shelf film, and improve the bearing close-up's neutral fill and
pad framing. Restore the tree family's documented thin-leaf response from the
exported images and reduce sky saturation. These are rejected intermediates,
not final docs. The render set was interrupted after nine views (exit 143),
before its four photo views; none of those missing views is claimed reviewed.

## Delivery critique 7 — native tint survives, but the hero and runoff still fail

**Color and value first.** Opened all thirteen 1200 px frames in
`renders/final-pass2/`, including its four photographic-camera views. The
concrete-balanced 2002 aerial now has gray, sage and cream house facades,
narrow parcels and a substantial broken canopy. The sky is less cyan and the
native thin-leaf response opens the excessively black tree masses. Summer turf
is muted yellow/olive with dry variation, rather than the original saturated
green. The 2007 road-balanced traffic photograph still has a darker fleet than
this seed's near view. Its exported paint bindings and independently decoded
pixels are correct; the metallic factors were still the imported Atlantic
factor. Apply the actual factory factors and put more weight on Carbon, blue
and red, retaining silver/gray/white. This is a color/value correction, not a
claim that a histogram alone proves the appearance.

The 101 east-terminal hero is rejected again: grass dominates and the freeway
is a sliver. Opened the two ramp-shoulder candidate views at native size. The
70 m station gives the freeway, bridge, signal queue, west gas canopy, strip
front and roof/tree/pole skyline together. Tighten that framing and aim lower
to remove surplus sky. The 115 m view loses the bridge and has a dominant
light pole; reject it. The 202 new hero shows roofs and utility conductors above
the wall, with varied trees behind them. The aerials still show regular block
repetition and only four native house silhouettes; those remain context limits.

The full-scene bearing photo view has real road/landscape surroundings now,
but the close inspection camera is much too dark. Opened the wider bearing
candidate: the actual pads, pedestals, cap and passing traffic are readable.
Use that view and neutral sky fill. The cap's overlapping equal-length drips
still form a curtain unlike the concrete-balanced 2008 photo. Move their
concentrations under the actual seven bearing lines, vary width, strength and
run length, and break the girder drip-line repetition. Preserve the broad damp
shelf film and actual scupper/joint concentrations.

The verge stems can intersect an elevated ramp because roots were sampled only
on earth. Reject roots under real paving. Open the ROW fence across the arterial
and audit that clearance explicitly; the accepted bridge, plan, controls and
paving remain geometrically identical. This is still an intermediate set:
the warmer concrete has usable highlight range and deep cavities, but the
repeated vehicle types, smooth slopes and regular native tree silhouettes
continue to read as CG. No gallery images are approved by this pass.

## Delivery critique 8 — new traffic and town framing, rejected sparse crowns and clean cap

**Color and value first.** Opened all thirteen native 1200 px pass-3 frames,
the four kit-composed photographic pairs, both newly rendered historical
reframed views and all nine native before/after panels. The traffic now reads
blue, black, gray, silver, white, red and green at full frame. The factory
metallic values survive actual serialization; the inverse image audit checks
all 21 derived RGB maps. The guide's green and the heroes' clear blue upper sky
retain color, with deep bridge shade and no clipped concrete. The low horizon
in the ramp hero is naturally lighter than the high sky in the cut view.

The matched 2002 aerial is decisive: narrow lots, drives, alleys, paved commercial
parcels and much more foliage are present, but individual small crowns still
look like dots beside the photograph's connected mature canopy. Increase yard
and apartment crown scale 1.4×, street crowns 1.2×, with more broad red maples.
Use instance transforms, adding no triangles. Keep the closest 202 roof/wire
zone at its current scale so that canopy does not hide it again. Record species,
yaw and actual scale in the placement manifest for engine replacement/batching.

The new 101 ramp hero finally includes the strip front, gas canopy, signal queue
and passing freeway below. The 202 view has gables, different trees and utility
conductors above the wall. The sign/traffic views confirm the busier seeded
snapshot; the models still repeat three vehicle types and four house envelopes.

The 2008 cap comparison still fails the age test. Rectangular stamps are gone,
and the seven concentrations follow actual bearings and the cap chamfers, but
too much cap stays uniform and clean. Broaden and strengthen those variable
top-connected concentrations, clip them at the real cap ends, slightly warm the
concrete tint, and increase base spray/road film on barriers. The comparison
also needs broad environmental bounce like the photograph's bright surrounding
site; add one recorded soft area fill to that photographic shot only. Keep the
heroes' deep shade. No source photograph supplies any material pixel.

The turf has distinct dry/mown/unmown treatment and rooted stems, but the right
sign-view slope is shaded and is a poor crop for the requested sunlit value
comparison. Use the same reframed ramp camera's sunlit slope and mowing edge,
at native pixel size, and strengthen the exposed dry grass's straw pigment.
Long slopes, straight bristly clumps and broad repeating asphalt variation still
read as CG. These frames are rejected intermediates; no gallery is approved.

The expanded tire audit initially made an incorrect diagnosis: SUV rubber uses
separate tiled Tire meshes while atlas Wheel meshes contain rims/markings.
Requiring both to touch paving falsely implicated simplification. Restored the
original distance reduction and check four actual tire surfaces per actor.
The audit did find a real 57 mm parked-car gap; flat-road actor heights now use
actual paving and native tire minima. Fresh exports measure 1,656 tire surfaces
between −12.04 and +13.27 mm. The gate is now ±20 mm. A separate correction
starts support rays beside the tire so overhead bridge decks are excluded.

## Delivery critique 9 — connected canopy and runoff; reject overlapping turf

**Color and value first.** Opened all thirteen native pass-4 frames, all four
photographic pairs, and all nine native before/after panels. The concrete-neutral
2002 comparison has much narrower, occupied parcels and linked mature crowns;
the oblique aerial reads as a wooded neighborhood rather than isolated white
houses. The concrete-neutral 2008 comparison now shows warm cap runoff beginning
at the actual bearing lines, varying in length and strength. Its real road,
trees and slope replace the isolated white background. A recorded broad bounce
opens this photographic view; the heroes retain deep bridge shade. These are
different lighting situations and neither is an albedo measurement.

The 2007 road-neutral pair confirms denser daily traffic with dark blue, black,
gray, silver, red, green and white finishes. The new ramp hero includes the gas
canopy, strip signs, signal queue and freeway below. The curved hero includes
house gables, mixed crowns and the pole/conductor line. Upper skies are clear
blue and concrete highlights retain texture. The dark maple masses still repeat
two native silhouettes, and the aerial street/parcel grid is more regular than
the photograph. Four house envelopes and three vehicle types remain visible
repetitions; report them as context limitations.

Reject the grass crop. Its yellow/olive pigment is closer to the reference,
but angular green patches persist on the far sunlit slope. Actual pixel rays
hit overlapping opaque mowing skins with different tint from the graded soil.
Remove those cosmetic skins, carry mowing tint on the existing terrain instead,
and retain all drainage geometry and volunteer leaves. The final comparison
must show that this fixes the patches. Preserve the native yard color while
moving dry red pigment into the texture: normalized glTF vertex colors cannot
carry a multiplier above one. Replace straight triangular stems with bent,
three-triangle blades rooted individually on the measured soil. No new texture
allocation or civil surface change is needed.

The broad asphalt variation, regular tire bands and smooth distant slopes still
read as CG. Final raw frames and crops are pending the clean rebuild; this pass
does not approve docs.

## Delivery critique 10 — cold exported finals and native fix panels

**Color and value first.** Opened all 49 current raw frames at native size:
22 scene views, 17 individual modules, human/car scale, Eevee, four shipped-PBR
photo cameras and four source-field cameras. Also opened the labeled sheet
and all five native row crops, eight composed photo pairs, nine before/after
panels and all three contact sheets. Photo balance still uses the recorded
concrete patches in the 2002 aerial and 2008 bridge/guide views, and roadway in
the 2007 traffic view. The gains make an approximate field neutral, with no
exposure adjustment or calibrated-reflectance claim.

Warm concrete is retained after shipping: actual bridge BaseColor median is
(.2462, .2270, .1946) linear RGB before placed age and illumination. The heroes'
99th-percentile display luminance is .777/.770; clipped RGB samples are
.001513%/.000333%. The bridge shade sample has median .0396 versus .4160 on
sunlit pavement. A tighter wall-only sample in 202 has median .1063 versus
.3175 on pavement; the earlier sample included the adjacent road. These are
measured display samples with stored ROI coordinates, not albedo measurements.
The low horizon is lighter than the upper sky, and the underpass retains deep
shade without clipping the sunlit concrete.

Each requested correction now shows in its identical-camera panel. `town`
has occupied narrow lots, garages/drives, alleys, fences, apartments and linked
mature canopy. `hero-town` includes the gas canopy, strip signs, signal queue
and freeway below; `backyards` has roofs, varied trees and utility conductors
over the wall. `traffic` has denser daily traffic and dark/color finishes
instead of the pale fleet. `grass` has dry straw/olive variation and rooted
seed stems, and the overlapping green polygon patches are gone. `concrete`
and `bearing-surroundings` show variable top-connected runoff without the old
rectangular stamps, with actual road/landscape surroundings. Both sky panels
replace the white haze with clear upper sky. Native widths are 980, 1120 or
1400 pixels per side; no panel is enlarged.

Compared with the photos, the repeated four house envelopes, two crown types,
three vehicle types and regular block rhythm remain CG cues. Long turf is
smoother than real grass, verge clumps still repeat, lane polish is too regular,
and concrete manufacture grain is more uniform than the bridge photograph.
Raking foreground rail views make the zinc/spangle response look coarse.
Rumble and fence alpha detail has limited parallax. The supplementary wall
close-up is strongly backlit, limiting its material read; keep it in the raw
inspection set and use the clearer cable-median image in the bounded gallery.
Eevee has flatter bridge shade and foliage than Cycles. None of these limits
is hidden by the contact sheet or replaced with a source-scene final.

The cold `make checkpoint` passed after current generation products were
removed. Historical handoff comparisons and preservation hashes were retained
only as evidence. All 49 current-frame provenance checks passed, together with
raw PBR/UV/normal/resource budgets, fresh imports, actual edge/bearing/tire
contacts, measured parcels and accepted-construction comparison. The town's
expanded tree count remains expensive despite shared meshes; it needs engine
parcel culling and foliage LODs/impostors. No whole-town frame-rate claim is
made. The six-fix visual gate passes; the gallery may now be assembled.
Full repeat, tolerant GPU rebake and the final gallery checks remain separate.

## Delivery critique 11 — gallery and completed verification

**Color and value first.** Opened all five bounded gallery JPGs at native size
after the full-size source-frame review. Their warm concrete, dark bridge
shade, clear skies, native paint colors and dry turf survive JPEG compression.
Captions and the two aerial plans remain readable. The gallery deliberately
uses the cable-median view in place of the very dark supplementary wall view.
The concrete grain, regular lane polish, smooth distant turf, coarse raking
zinc and repeated native silhouettes remain the limits described in pass 10.

The clean checkpoint and subsequent `make` and `make check` passed. Full
`make repeat` regenerated 175 files byte for byte: 69 CPU field/calibration
files, 73 native-cache/export/manifest files and 33 CPU photo/crop/contact/gallery
products. `make check-texture-repeat` independently rebaked all twelve shipped
maps: maximum difference one byte, worst RMS .002473744 byte, with exact
maintenance coverage alpha. No blend-container or stochastic raw-render byte
claim is made. Current-frame provenance still passed after the regenerated
exports, and the gallery/pair/contact bytes remained identical.

The final repository check reports 2,116 source files and zero errors. Actual
freeway triangles are 263,504 / 160,534; town/traffic expanded counts, instances,
unique meshes, geometry/PNG bytes and deduplicated image memory are listed
separately in the README. All 1,094 other-delivery files remain hash-identical.
Five JPGs are 184,392; 183,427; 199,904; 194,695; and 190,665 bytes, with widths
1400/1400/1600/1600/1600. No kit or top-level README change was made. Gallery
images are ready for the final, separate commit.
# Round 4, pass 1: exported turf, age and framing (rejected)

Color and value: the 1000 px exported views in renders/round4-pass1 make the
miss clear. The native lawn's soil/weed RGB, normalized independently and
amplified, becomes yellow camouflage rather than a continuous grass bed.
Against the concrete-neutral 2002 aerial and 2008 bridge photo, the large
yellow/green value breaks are the first CG tell. The 202 median shows sparse
card islands above that base. Near 101 grass has volume but reads as an overly
upright seed curtain. The pavement wheel paths now read; the column shafts
still look almost new and their old repair skin becomes a pale rectangle.
The barrier has a smooth low gradient, with too little irregular spray history.

I opened all seven raw exported views at native size: old 101 camera, barrier,
pier/girders, 202 hero, and three 101 framing candidates. The ramp candidates
retain the accepted gas canopy/storefronts/signals but too much foreground;
the mainline view gives the pavement and bridge weight but loses the town.
Centered 2.4/2.6 aspect studies of the ramp-shoulder view retain town/bridge/road
and reduce foreground turf to a band. The selected 50mm, 2.6 composition will
be rendered again, not used as a cropped final. Its actual exported shoulder
surface is Z 6.8302619m, with the camera 1.65m above it. A separate 35mm roadway
view will keep pavement age legible at player eye height.

Corrections: compress native blade luminance instead of amplifying separate
RGB channels; lower large-clump contrast; increase blade coverage and clump
density while retaining eight linked meshes and the same atlas allocation;
soften mown contrast and reduce the leaf normal's effective relief to .8mm.
Strengthen head-connected column streams and low spray, weather the repair
skin continuously with its shaft, and vary barrier spray height along station.
No docs are accepted at this pass.

Construction gate: rejected bilinear ground resampling moved supports/flumes.
It was removed before the first images above; the actual old earth triangles
remain, with smooth grass normals. Mowing contrast moves to the cards. Civil
101 drops from the rejected grid's 357,538 to 287,616 triangles; 202 is 162,966.
Both traffic glTF/BIN pairs remain byte-identical, and cap-runoff chart bytes
remain exact. A later edge-return merge also retains the original diagonals
around new lane-center samples. The first oriented-surface audit exposed
ambiguous coincident internal tube caps; it now selects the matching oriented
chart rather than the first nearest cap. Final physical checks remain pending.

# Round 4: rejected grass and surface age / baseline

Color and value: at native size the aaf099e 101 hero has a dark olive ground
sheet with too little local contrast, while its sun-facing slope jumps to a
flat yellow triangle. The 202 median is similarly smooth with broad brown
patches. I inspected grass.jpg, concrete.jpg, backyards.jpg and both final
heroes before editing. The comparison photographs are the existing concrete-
balanced freeway/bridge/traffic images; their neutral ROIs and gains remain in
build/reference-balance.json. The 2002 aerial has summer green ROW; the 2007
traffic photograph has dormant turf, so season limits a literal hue match.

CG tells: isolated tall stems emphasize the flat base, triangulated slope
normals expose the terrain grid, the 101 foreground overwhelms the freeway,
the column bodies have almost no age and the median faces read as new castings.
The road's narrow oil field misses the lane center at its mesh sample points;
the replacement panel reads as an atlas stamp. Accepted canopy, houses,
traffic paint/density, clear-sky light and cap runoff are retained.

Implementation checkpoint: clumped seasonal color over the native baked blade
normal/ORM, shared crossed-card tiles with a spatial density falloff, smooth
earth normals, closer candidate hero, head-connected column streams and low
splash, dark barrier toes/joints, sampled lane centers and native-textured
replacement slabs. Full-size exported visual checkpoints remain pending here;
syntax and texture-field checks alone do not accept these fixes.

## Round 4 construction and determinism checkpoint

The clean rebuild removed the freeway's generated context cache, working
blends, exports and all four source/bake/shipped texture sets. It regenerated
4096 bakes and 2048/1024 deliveries from scripts. `make check` passes:
287,600 / 162,518 civil triangles, raw PBR/UV/normal checks, fresh imports,
retained context and 1,099 other-delivery hashes. All 21 paint transfers pass;
both traffic glTF/BIN pairs remain byte-identical to aaf099e.

The independent construction comparison passes 343 retessellated mesh
surfaces, plus strict oriented corner data for unchanged civil meshes. Actual
edge/soil contact passes 11,808 probes with zero exposed gap; 168 bearing
probes have at most .760mm pad/girder discrepancy. These are surface checks;
the separate source/import equality checks establish serialization only.
All 69 CPU manufacture/calibration products independently repeat byte for byte.
This checkpoint does not approve the appearance or the gallery.

## Round 4, pass 2: six exported views (rejected)

Color and value: opened all six native 1000px pass-2 renders: the new 101
hero, retained hero camera, road view, pier/girders and barrier, plus 202 hero.
Against the same concrete-neutral 2002 aerial and 2008 bridge, the grass cards
are still too yellow and bright relative to their base. Dense opaque fans
make cabbage-like patches; random tile/root positions leave dark islands.
The compressed base loses too much of the native blade contrast. The 202
median has a particularly clear smooth strip beside its clumps. This is still
CG grass, even though the old faceted lighting is gone. No gallery approval.

The new 50mm/2.6 101 composition does reduce the foreground to a band and
retains the signal queue, gas canopy, storefronts, bridge and freeway. Keep
that camera. Wheel paths, lane-center oil and panel joints read in the road
view, with the native-grain replacement slab. Column shafts remain broad,
nearly clean gradients below the accepted cap streams. The barrier toe is
darker, but its end-joint deposit is too faint. Their vertex masks alone do
not supply the fine connected flow visible in the bridge photograph.

Corrections: thinner 90-blade fans, closer pigment to the base, 64 stratified
roots per tile, restrained tile jitter and upward blade normals; restore more
native blade luminance contrast. Shrink paving exclusion to the actual card
footprint. Add the existing runoff chart continuously around each real column
ring, beginning under the cap, and deepen end-joint grime. The new column skin
follows the original 32-sided shaft, offset .6mm; it allocates no new image.
Town/car repetition, broad road-field regularity and uniform concrete grain
remain other CG cues. Final-size inspection and new crops are still pending.

## Round 4, pass 3: native comparisons (rejected)

Color and value: opened all six new 1400px exports, all eight native
before/after panels and three newly rendered before-camera images. The
concrete-balanced references remain the 2002 aerial and 2008 bridge. The
yellow clump camouflage is gone; 101's foreground now reads as a dark dense
stand of grass, with textured mown slopes and no hard lighting triangle.
The 202 median gains sward texture, but its card exclusion leaves an abrupt
smooth strip beside paving. Tile rhythm and overly even mowing remain CG cues.

The 101 composition passes: town, bridge and lanes remain, foreground is a
band. Lane-center darkening, wheel response, joints and native-grain replacement
slabs survive at the hero camera's distance; the road-camera pair makes the
changes clearer. Barrier feet and end joints now show road film. Fine runoff
finally continues down the columns. It also exposes the inherited opaque
repair skins as pale pasted cutouts: they sit outside the runoff skin. This
fails the no-stamps requirement. Do not generate docs or continue the finals.

Corrections: remove only the 48 cosmetic column-repair triangles, retaining
the actual shafts, collars and cap. The construction audit records that
narrow cosmetic exclusion and still tests the supporting surfaces. Fill the
median's card-exclusion margin with two narrower shared tile rows, shorter
toward the pavement. Expose a narrow irregular soil edge sampled from the
actual terrain. Reuse Ground's original mineral normal/color/ORM for brown
soil/gravel instead of a smooth scalar strip. No new map is needed. Keep the
rest of pass 3: hue, dense near grass, smooth grading, framing and lane wear.
Regular joint staining, lane bands, manufacture grain and native silhouettes
remain CG tells to assess again after this correction.

## Round 4, pass 4: native fix gate passes

Color and value: inspected all six 1400px key exports and all eight native
before/after panels. The concrete-neutral 2002 aerial and 2008 bridge remain
the summer-green and concrete comparisons; the March traffic reference has
dormant grass and only an asphalt neutral, so it cannot set summer turf hue.
The new grass is muted green rather than yellow camouflage, with a darker
dense stand on the shaded near slope and shorter mown cover near pavement.
The 202 transition now has short linked sward and a narrow exposed mineral
edge. Blade/clump texture replaces the former sheet and isolated toothpicks;
the lit slope no longer breaks into lighting triangles. These are visible
changes at the retained cameras, without enlarging a crop.

The new 101 hero reduces foreground turf to a band while retaining the town,
bridge and lanes. That panel explicitly labels the changed composition; the
seven physical-change panels retain identical cameras and 1400 native pixels
per side. Column channels now continue below the accepted cap without pale
opaque cutouts. Low road film and joint staining read on the barriers.
Wheel response, lane-center darkening, joints and native-grain replacement
panels survive at the hero distance; the road-camera panel is the clearest
pavement comparison. Soil/gravel uses the existing mineral images, not a new
texture allocation. Accepted town, traffic, sky and cap flow remain.

Still CG: the eight clump patterns and mowing rows have more rhythm than the
photographs, lane bands and barrier-joint staining are regular, and concrete
manufacture grain is more even. Native house/tree/car silhouettes repeat.
The photographic fits also differ in season, lane count and bridge type.
The requested fix gate passes; the remaining final views may render under
the current GPU lease. Gallery approval still requires every final, photo
pair and contact sheet to be inspected, and the complete checks/repeats.

