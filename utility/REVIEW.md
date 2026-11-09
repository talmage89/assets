# Utility construction review

This is a form checkpoint, not a final look-development sign-off. The user
asked for at least two form passes and then a stop. Photos are local inspection
only. The final reconstruction renders the exported quick-material GLBs.

## Pass 1 — first Cycles hero, transformer and house service

Color/value first: the provisional pole is too smooth and dark to reproduce
silvered treated timber in the residential photographs. Steel/can paint is
uniform and cold; the tree source and quick context are also darker than the
photographs. No wood/rust/chalk look-dev is claimed. The photographs' sidewalk
cement is the assumed neutral for the later balance measurement; no gray card
or inverse albedo claim is available.

The 40-ft pole height against one/two-story houses reads correctly, and the
native six-foot planting allowance gives sensible curb/walk placement. The
first hero clipped the top and made the line hierarchy harder to read.
The first transformer frame exposed an arrester consisting of floating sheds,
deadend eyes floating at tangent-pin height, a wrong-direction light bracket,
and insufficient support above the low house eave. Those are construction
errors, not material problems.

Fixed: add the arrester core and supported mounting bars; put deadend eyes on
the arm/pole bearing datum; face the bracket into the road and mount the
library head; roof-guy the mast at actual roof hits. Pull back to a 35 mm,
sidewalk-height hero. The three-can rack initially exceeded 11k triangles;
lower radial/cable resolution on that rare bank recovered its budget while
retaining the same can/fixture construction. Keep fixed parts consolidated.

## Pass 2 — all four streets, hardware, base and distance

Color/value first: cavity and under-hardware shadow are deep and legible.
There is no pale white clipping problem. The pole still lacks the photograph's
gray/brown fiber variation; the yellow guard is too uniformly manufactured.
These are documented next-stage surfaces. The quick label planes are useful
construction tags, not final burned/embossed graphics.

The full set exposed important errors that the hero alone concealed. The
house yaw convention faced the rows away from the street. Roof-ray checks
caught drops crossing those roofs, prompting the yaw correction rather than
relaxing the geometry test. A front-wall mast outside the overhang replaces
the first side-eave guess. Its lower elbow enters the wall; a second meter is
removed. A roof-guy query measures source roof triangles for every attachment.

Other rejected details: the anchor frame cropped away the actual ground eye;
the base frame did not show the base; a distance frame exposed the presentation
road's artificial end. Reframe the first two and extend the native roadway
well behind the viewing positions. Secondary spools originally had their axes
along the wire and the socket inside the porcelain. Reorient the spools,
give them a real vertical rack and put the neutral on its outer bearing line.
The ground-wire molding now follows the measured taper.

The three-can assembly now has separate primary phases, a supported steel rack
and three **independent** secondary circuits. Its outer hots must not terminate
on the central circuit. Three-phase risers now carry three sealed terminations
and tails rather than a single phase's cable. These were construction fixes.

The distant exported four-sided tubes show intermittent breakup, especially
against bright sky. A camera-facing .85-pixel ribbon with compensated coverage
preserves their integrated darkness better. Use that as the runtime direction,
retain true tubes near the player, and keep the comparison explicitly labeled.
An opaque width floor would make the remote wires visibly too heavy.

## Pass 3 — physical gates and final checkpoint replay

Color/value first: neutral balance is based on a bare sidewalk ROI in the NC
photo and concrete driveway/sidewalk in the MD photo. `build/reference-balance.json`
records native rectangles, linear medians and gains; balanced inspection copies
stay in build/. Photo pairs retain original colors, not baked replacement pixels.
The source wood is still deliberately flat. The exported hero's lower-image
Y′ percentiles and clipping fraction are recorded in `build/hero-tones.json`;
that region includes context and is not a utility-only albedo mask.

The mathematical tests verify unequal endpoint heights, sag definition,
catenary differential identity, tension conversion, polyline error and
coverage compensation; invalid inputs are rejected. The independent raw GLB
gate caught degenerate check-tip faces; those tips are now actual triangles
with single end vertices. Every final raw mesh has zero degenerate triangles
and unit normals. Fresh import verifies the real socket transforms and counts.

The earlier uniform-height version passed the 20/18/15½-ft geometric screens. Minimum sampled
neutral/comm surface gap is 1.205 m, above 1.016 m; the nominal 1.32 m pole gap
alone was not used as proof. Ground clearances are measured on imported wire
vertices. Roof rays sample the actual placed house roof surfaces under the
service curves. A 100 mm mast increase recovers the conservative eight-foot
roof screen for the low communication drop near a porch. Minimum sampled
roof clearance is 2.493 m; higher masts remain supported by roof guys.

The photo fits keep their errors visible. NC uses several pole heights and
run positions; MD is a weaker type comparison, with the two space landmarks
held out because they differ from our selected utility layout. Lens estimates
are not EXIF. The MD image was made in 2015, after the modeled equipment period.
Both comparisons judge existing residential infrastructure, not an attempt to
copy a real neighborhood. Full residuals live beside the paired images.

No final look-dev, atlas, UV, bake, engine shader compilation or game
performance result is implied by these form checks.

## Pass 4 — reject repetitive antenna-like service masts

Color/value first: the replay's lower-image Y′ range has deep cavity/context
shadow and rolled highlights without clipped white. Its flat wood and guard
still cannot reproduce the aged-photo surfaces; this remains an explicit
look-dev stop, not a material approval.

The replay made the uniform 6.6 m masts conspicuous over the one-story roofs.
Applying a road-height criterion to the entire yard was visually and
constructionally unhelpful. Review WPS Section 7's actual distinctions:
the general Type-A service criterion is 16 ft, with a conditional lower
residential-driveway exception that this family does not use.

Move supports to solid corner jambs outside porch roofs. Measure roof anchors
again and size the mast to those anchors and its own service/communication
crossing. The current 5.2–7.435 m attachments follow one/two-story roof heights.
The 5.2 m ranch masts replace the old 6.6 m version. Keep a conservative 18-ft
service screen over the road and 16 ft over all private land; comm drops use
15½ ft over the road and an authored 12-ft private-yard screen.

The independent audit clips imported triangles at the curb-back planes, so
a crossing minimum between centerline stations cannot escape the test.
Current measured minima: service private 5.193 m / road 5.975 m; comm private
4.397 m / road 4.866 m. Sampled roof rays now find no overflights. The previous
2.493 m porch separation is a superseded layout measurement, not a current claim.
The guy guard is also a real hollow 2.5 mm wall with open end rings, exposing
the wire/anchor rather than passing it through a solid yellow cap.

## Pass 5 — reject the misleading imported context pose

Color/value first: the quick-material limitation remains unchanged. This
pass addresses a construction presentation error that the source-space roof
checks could not establish.

Imported house roots use quaternion rotation. Writing their Euler yaw left
the visible houses unrotated, even though the layout, source roof queries
and service mast transforms faced the street. The resulting pictures showed
apparently floating masts. This was a renderer bug and invalidated those
pictures as evidence of a working assembly.

Compose the instance's world matrix explicitly, preserving the imported glTF
axis conversion. Add a second check against the actual posed visible GLB
house triangles: every roof-guy endpoint must meet that house within 0.2 mm.
Run it for all 48 house instances, and include its measured errors in each
render receipt. All 96 anchors pass; the maximum measured surface miss is
0.00811 mm. The service camera now follows the house's front frame.
Regenerate every street, detail, distance frame and photographic pair from
the corrected presentation. Current-source recipe hashes reject stale images.

## Pass 6 — keep the line jog out of the travel lane

Color/value first: the corrected-pose hero has deep under-eave and hardware
shadow, a broad midrange and no clipped white. Wood remains dark and smooth
against the balanced used-pole photographs; surface age is still deferred.

Opening every street and aerial exposed a layout error in seed 104: the
original 1.05 m-per-span lateral offset crossed the curb and placed two poles
in the road. The straight native ground context did not follow a road bend.
Reject that arrangement. Reduce the line jog to .15 m per span, staying in
the planting strip, with the guy opposing its lateral pull. This is a small
utility alignment jog, not a claim of a curved street. The independent import
gate now records the actual shaft's world-space section bounds and requires
its entire ground footprint between curb back and sidewalk front.

The close-up review also finds polygonal short-jumper bends, a simplified
splice-case end and temporary nameplate orientation. Those need closer-range
polish at the next stage. Widen and lower the service detail framing to include
the eave/supports with the head and drip loops. The final replay regenerates
all frames and both matches; stale receipts cannot pass the review script.

Final inspection: opened all 20 regenerated native frames, both photographic
pairs, the contact sheets and neutral-balanced reference copies. The corrected
104 aerial keeps every pole on grass; its nearest shaft edge is 0.347 m behind
the curb back. The service frame now includes the two wall supports, wall-entry
elbow, roof edge and upper attachment. Long wires remain thin in the distance;
the filtered still improves continuity without the opaque-rope silhouette,
but cannot establish moving-camera temporal stability.

Final hero lower-56% encoded Y′ p1/p50/p95/p99 is
0.0255 / 0.3668 / 0.8550 / 0.8701, with zero all-channel white clipping.
The final NC/MD calibration RMS is 6.513 / 18.117 native pixels; MD's held-out
neutral/comm residuals are 36.93 / 81.88 pixels. These expose the real spacing
differences rather than hide them. The three-can close-up reads as supported
separate cans; the source still needs the finer connections/normal detail
described below and is not a three-phase secondary wiring diagram.

Proof: `make clean && make` completed the clean checkpoint replay;
after the planting-strip correction, `make` regenerated the models, checks,
20 Cycles images, two pairs and sheets. Final `make check`, `make review`,
`python3 kit/repo_check.py` and `git diff --check` pass. The five pure math tests,
raw/fresh-import gates, road clipping, shaft footprints and visible house fits
all pass. Repository check reports 1,539 source files and zero errors.
No kit regression suite is required because kit/ is unchanged.

## Remaining work, deliberately outside this checkpoint

- Prove real aged wood, silvering/check depth, wet ground-line absorption,
  bolt rust/runoff, transformer chalking, hand contact and faded guards against
  used photographs, first in source and then on the baked export.
- Put fine triplex strand lay, long-span fiber lashing, conductor strands,
  threads, manufacturing texture and scars into the shared normal/color maps.
  Current service constituent tubes are smooth, not a geometric helix.
- Complete the shared 2048 atlas and at-most-three-material delivery; current
  diagnostic material/label counts are temporary. Run final UV/density/bake gates.
- Validate the supplied original ribbon shader in a real engine, moving the
  camera under its AA modes and testing transitions, culling and performance.
- Town staging is intentionally sparse and repeats one source seed per house
  type, with quick ground/pickup materials. It demonstrates utility scale and
  connections rather than a finished town environment. House internal meter
  routing and a three-phase secondary bank connection are not modeled.

No shared kit file or neighboring asset source is modified. Existing generated
deliveries were absent from this worktree; context generation writes only
utility/build. Their absence is stated rather than claimed as a comparison of
hundreds of delivered files that were not present.

## Surface round, pass 1 — exported 2048 atlas and cable hierarchy

Color and value first: opened the original NC/MD photographs and the old hero
and distance sheet, then the first baked export's hero, ground line, transformer
and communication views at native 1280. Jacketed routes are now much darker
against sky. The pine is neutral gray-brown rather than the old smooth dark
cylinder; the pale gray dielectric sheds and can keep distinct responses.
Assumed neutral for the MD comparison remains its bare driveway cement; NC
uses its bare sidewalk. Their explicit linear gains are retained for the next
matched-light measurements. No photographed pixel is an input to a material.

Reject the first images as finals: 24 un-denoised samples leave conspicuous
noise in tree crowns and shadowed timber; the base camera clips the number
tag; and a source-field update made during an earlier bake left that bake's
crossarm grain perpendicular to the arm. The actual current source field has
horizontal growth bands and checks. Rebuild the complete atlas serially from
stable fields, reframe the base to show grade and tags, and preserve actual
wire coverage when denoising the scene. The current top close-up also exposes
a flat green horizon between the trees; fill the distant residential yards
with the library tree species as well as the nearby planting strips.

The first new 104 block was 50,164 triangles, above the retained 49k target.
Recover oversampling in the repeated optional mast curves and tiny roof guys,
retaining their diameters, sockets and supports. Long-span uniform stations
already retain the API's 8 mm chord-error and 4 m step screens without the
old power-of-two excess. All five existing mathematical controls pass.

## Surface round, pass 2 — reject machined-looking wood and floating ink

Color and value first: opened all six 1600-pixel pass-2 exports at native
size: hero, base, transformer, crossarm, communications and dusk. Compared
with the neutral-balanced MD pole/can and NC street photographs. The gray
paint, shaded jacket black and porcelain are separated without pale clipping.
The hero's raking shadows and continuing residential horizon read much more
convincingly than the original field; the remaining run stays visible between
crowns. The strip/yard trees no longer obscure the whole line corridor.

Reject the wood's normal strength: the long ridges make pine and fir read
like corrugated plastic. Lower the physical growth-band relief from .33 mm
to .085 mm on fir / .11 mm on round pine; keep localized drying splits.
Raise the uneven capillary wetting reach slightly so the ground line has a
visible material change. The can's broad lower stain is plausible, but the
one sinuous front streak looks arbitrary. Start runoff at the actual lift-eye
weld roots and lid seam, reduce its wandering and make bottom retention uneven.
No pasted speckle or uniform rust wash is added.

The base camera now reaches grade and the birth mark, but the tag lettering
has the atlas rectangle's distorted aspect. The birth/rating quads also bridge
their cylinders. Author lettering at physical aspect, use shared glyphs for
seeded tag numbers, and conform the stamped mark and foil nameplate to the
actual polygon surfaces. Keep these in the same atlas and draw call. Turn
some existing vine growth toward the base view; do not add a vegetation mesh
budget. Correct the triplex's constituent packing; the old separated row was
wider than a real #4 assembly even though its constituent diameters were right.

Dusk has a blue sky above a darker street, lit heads and window glow, but the
pickup's glass incorrectly receives the house-window emission state. Exclude
vehicle glazing and give the night wire samples 128 samples to reduce bright
specular sampling noise. Retain native sky-line samples when denoising the
surrounding surfaces. Three original factory paint colors reduce the parked
pickup repetition without changing any car source or delivery.

The raw delivery gate now passes every package: nondegenerate UVs, retained
stock-chart boundaries, unit normals/tangents and the same three image
**datablocks** when all five external glTFs are imported together. The gate
previously caught a collapsed UV strip on the buried insertion stub and a
folded central riser breakout; the stub now has nonzero UV height, and that
straight central connection no longer folds back over itself. Physical
clearance tests remain separate and pass at this authored tension state.


## Surface pass 3 — exported atlas, native 1600 px, photo fits and exact wire ranges

Color and value first: the exported wood retains gray-brown albedo, but the
strong blue fill and an overly regular annual-band pattern made the upper
shaft look like fluted metal. The can is substantially lighter than the used
Maryland can in soft backlight; its fitting layout is also different. The
Maryland concrete and NC concrete were separately balanced as assumed
neutrals (not gray cards); native photographic line profiles are saved beside
the raw model probes. They have no surveyed distances.

Opened all six pass-3 close views, all three paired sheets, and the native
wire comparison. Reject the old local can-only 2.4 px fit: it concealed the
wrong crossarm direction. Add both arm pins and the cut top as independent
controls. The communication fit's shaft roll was visibly wrong; add a second
shaft station and start the camera on the physically correct side of the
cable direction. Keep the residual visible instead of reporting the local
can fit as full-assembly agreement. Accepted equipment heights stay fixed.

The corrected telephone and coax remain dark at 120 m (23.7/23.8% displayed
contrast); the true 10.109 mm primary falls to 2.6%. Strict energy-preserving
.85 px ribbons also fall to 2.3%, so merely widening and reducing alpha in
exact proportion fails this requirement. Retain true diameters nearby; give
the documented far policy an explicit calibrated optical exponent .55,
with 1.0 available for strict integrated coverage. This is a deliberate
visibility compromise, never a changed physical cable diameter. Re-measure
the result against native photo profiles and report both versions.

Change the grain coordinate with coherent anisotropic fibre waviness and
vary each band's strength; enlarge fir knots to their physical section.
Reduce molding relief independently. Reframe ground-line and identification
views separately, so neither the wet base nor the full tag is cropped.
The actual exported-label contact check also found a 6.8 mm bank-only gap;
conform its plate to the bank's 14 facets and require <1 mm measured contact.


## Surface pass 4 — native close views and eye-height street

Color and value first: opened the four complete pass-4 1600 px renders
(crossarm, base, tags, hero). The warm-gray wood separates from blue-gray
steel and the black communication jackets now hold the street perspective.
The pine still looks too smooth at an extreme close-up, and capillary
darkening is too weak. Add millimetre-scale longitudinal fibre variation
under the existing warped growth bands; strengthen only wet/shaded wood at
grade, with its irregular upper reach. The fir grain direction and the
reduced relief are now correct, without the previous regular flutes.

Reject the tag view: the camera still cuts the upper digits, and the real
ground molding occludes the birth brand. Turn the complete tag/brand group
exactly two shaft facets (36 degrees) clear of the molding; this preserves
the conformed contact and geometry budget. Increase camera distance and
frame the actual world-height datums. The vine's sparse kite leaves and the
close view's enlarged texture are weaker than the real plant/wood; retain
this as a limitation rather than claiming a photograph at macro distance.

The sunlit street is populated and continues to the horizon. Repeated house
setbacks, lawn planes and pickup type still reveal procedural presentation.
Keep the utility audit separate from that context. The resumed four-view
render completed with 4,522,972 KiB peak resident memory; all following jobs
run serially with four CPU threads. No other delivery was involved.

The new transformer-top fit includes both arm pins and the cut top (6.19 px
RMS); the can mount remains a visible construction difference from the
Maryland installation. The communications fit has 15.10 px residual against
its estimated shaft stations/cable points. That is a weaker comparison,
not a precise equipment survey. Balance NC/MD on stated concrete ROIs and
the communications photo on an assumed gray porcelain shed before color
comparison. Reverse the NC sun direction to match the right-side tree
shadows; desaturate the soft MD sky fill instead of accepting a blue pole.


## Surface pass 5 — reject the remaining pale street lighting

Color and value first: opened native final/101 hero and street before stopping the batch. The street has actual
raking cast shadows, but the nearly white procedural sky fill, neutral sun
and .20 linear pine base combine into a cold, pale pole. Against the
neutral-balanced used wood, its reflectance is too high. Lower treated pine
to .132/.113/.084 linear and fir to .145/.111/.073; preserve gray-brown hue
and all localized age masks. Add fine fibre relief to the fine fibre field,
not to the low-frequency growth bands that previously looked corrugated.

The separate sun lamp was white even when the procedural sky described a
lower afternoon sun. Give the ordinary sun its warm low-angle color, lower
its elevation to about 23 degrees and reduce sky fill. Keep the photo-pair
lighting independent and neutral for their own conditions. This is a
lighting correction plus measured material-value correction, not a uniform
color-grade wash. Make removed the incomplete grouped render targets on termination; retain
the inspection receipt and recheck a complete hero/base/tag group before
producing the remaining views.

The moved markings now clear the molding and measured surface contact
remains within .401 mm. All physical and external-delivery checks passed
from the clean build before this deliberate visual rejection.


## Surface pass 6 — value-corrected export, 1600 px hero/base/tags

Color and value first: opened all three native value-pass images. The pole
now reads brown-gray in the warm sun and substantially darker in shade;
the light has long raking shadows instead of the earlier cold flatness.
Black communication jackets remain distinct across the sky. The atlas
retains measured dark wet/green pixels at grade (about 70–86 sRGB bytes
versus 97–108 higher up); those are material samples, not a claim about
displayed brightness under different lighting. Fine wood remains limited
by reused atlas density at a macro crop; the small vine's silhouette is
still angular. At street distance the pole is the intended material.

The complete RV number and birth mark now fit and clear the ground molding.
Reject the birth mark's pale rectangle: change its backing to wood of the
same mean reflectance with its own fibres, retaining dark burned/stamped
letters. This should read as a marked patch of wood, not a foil label.
The transformer's actual foil plate stays gray. Correct the guard UVs to
lathe-local cylindrical coordinates: its dirt belongs at the anchor end,
not across a tube face selected by an arbitrary projection. Neither fix
adds geometry, materials or images. Add independent native jacketed-line
profiles in the Maryland and communications photographs alongside the
existing bare-line probes. Then rebuild from nothing and inspect all views.


## Surface pass 7 — reject inferred local shaft stations as camera controls

Color and value first: retain the corrected warm gray-brown material values
and the separate neutral-balanced reference lighting; do not use a blue
cast to make a pole look dark. The communications framing still needs a
stronger geometric basis. The local fit used arbitrary estimated stations
on an unmarked shaft and reached its lens bound. Reject that fit.

Fit the complete reference pole from base, cut top and both upper arm pins,
using the actual exported 40-ft angle pole. These controls span its full
height and width. Independently hold out the shaft centre at telephone
strand height. Render the verified whole portrait at its native 749 × 1640
pixels, then take the same native 570 × 370 review crop from both images.
This preserves the actual full-frame lens and principal point, rather than
refitting an assumed centred lens to an off-centre crop. Record the control
residual, held-out residual, full portrait and crop separately. Equipment
placement differences (case position, extra route) remain visible.

The guard unwrap gate caught the riser's yellow formed channel sharing the
Guard role. Cylindrical mapping belongs only on the round guy guard; the
channel keeps a longitudinal planar chart and separate cap mapping. Retain
the zero-degenerate-UV gate; do not loosen it to get the build through.

The full-street ribbon inspection also needs the same raw-wire preservation
mask as physical tubes. Assign its temporary ribbon mesh to that object
index and include transparent coverage in the pass; otherwise the surface
denoiser can erase the very far-wire policy being reviewed. The controlled
30/60/120 m measurements remain completely undenoised.


## Surface pass 8 — distinct routes, not an aliased merged line

Color and value first: the raw distance profiles had suspiciously identical
telephone/coax minima at 120 m. Their dark value was correct, but their
different authored tension/mass ratios let the telephone sag toward the
coax and merge at midspan. The longest seed actually crossed their analytic
envelopes. Reject this. The new actual-triangle section gate independently
fails the old export at only 105.46 mm free separation near the start of
seed 101; it samples 84 planes per street and also checks the observed
number of separately hung route envelopes.

Restore the accepted communication catenary constant from .24 kg/m / 900 N
for each supported route. Scale force with supported mass: telephone
6,641.25 N, coax 1,612.5 N, paired fiber 1,350 N and retained copper
4,256.25 N. These remain authored supported self-weight cases, not vendor
stringing tables. This keeps the new accurate diameters and route count
while retaining the accepted sag shape and vertical spacing. It adds no
geometry. Keep an independent 60 m span regression and the actual imported
triangle-plane gap gate. Rebuild the blocks and all affected render evidence.


## Surface pass 9 — native final review and rejected color assumptions

Color and value first: reopened the current hero, base and transformer,
three final pairs, full communications portrait and held-out overlay at
native resolution. Also opened every final Cycles seed/detail/dusk image,
the nine raw 30/60/120 m wire controls, ten historical renders and all eleven
native before/after sheets. The brown-gray shaft, warm fir, neutral can and
zinc, gray dielectric sheds, faded yellow guard and near-black jackets keep
their own colors. The hero's lower-image p10 / median / p95 are .065 / .227 /
.821 displayed Y′, with .001% white clipping; this measures the whole street
foreground, not a segmented utility albedo. Raking shadows keep deep values.

Reject the previous beige-concrete and shaded-insulator neutral assumptions.
The latter produced a false orange reference; neither is an acceptable color
target. Final pairs retain original photographed colors. Separate inspection
copies balance NC on cloud ROI (20,95)–(55,120), gains 1.143/1.031/.866, and
Maryland on cloud ROI (2150,330)–(2220,380), gains .988/.988/1.026 in linear
light. These are approximate achromatic-cloud assumptions, not gray cards.
No neutral is accepted in the hardware photograph; use it for geometry and
contrast only. Do not calibrate the wood's hue to that photo's blue cast.

The final fitted RMS residuals are 6.51 px street, 6.19 px transformer upper
shaft/arm and 9.74 px full communications pole. The latter's native dimensions
are 749 × 1640 (correcting the initial 1644-pixel transcription); its telephone-height shaft centre is held out and misses by
2.17 px. The case and the passing span have different installation positions
and azimuths; the Maryland can is lower than this accepted mounting. Keep
those differences visible rather than claiming that a shaft/arm fit also
proves every item of equipment. House slopes no longer drive this camera.

The true primary's 30/60/120 m displayed contrast is 33.2/10.5/3.8%; the
far option reaches 37.7/15.5/7.6%. Telephone reaches 87.8/51.1/21.3% as tube,
99.4/53.8/23.9% as ribbon; coax 79.6/34.1/14.9% and 90.3/34.7/20.5%.
Against native photographic bare-line contrasts (NC 11.0/9.7/6.8%, Maryland
23.1/23.6/24.7%), the far primary is readable at 120 m, but the tube alone
remains too weak. Photo depths are unknown. Retain tubes near and recommend
the .85 px / exponent .55 option below .8 projected pixels; this deliberately
boosts optical contrast rather than preserving strict integrated energy.
The hardware jacket annotation was five pixels below its centre at one end;
reject its 32.4% result. Correct centreline controls clear of the case give
83.7% median, p10 81.8%; the Maryland jacket independently measures 60.1%.

The street has mature maple/oak, both-sided houses, continuing roads and
walks, parked pickups and populated far ground. At full frame, softened wood
and wet base read better than the old flat material, but fine bolt streaks
and sign scars remain subtle. Close wood still looks filtered; vine leaves
are angular, and repeated pickups/setbacks, lawn planes and cloudless sky
remain procedural tells. The can keeps its paint rather than a pasted rust
wash. Dusk has powered lamp pools and warm house windows; isolated bare-wire
specular samples remain noisy. These limitations are not covered by the
construction checks.

The separate Eevee shot initially exposed a house-context compiler failure
(pink trim despite Blender exiting zero). Reject it. Prune only unreachable
branches, combine identical reads and pack six existing scalar masks into
two FLOAT_COLOR RGBA corner attributes. Exact field roundtrip error is zero.
The final shader log passes an explicit compilation-error gate and the
reopened hero has no pink material. Eevee's context glazing stays flatter
than Cycles; the delivered utility retains the exact same baked PBR maps.


Final verification after pass 9: the uninterrupted serial sequence
`make clean`, `make`, `make check`, `make repeat`, then the repository check
completed with exit zero. The root-worktree log is
`build/utility-clean-final-validation.log`. All seven span tests pass;
all five fresh geometry packages and 48 source fields reproduce byte for
byte. The final independent GPU rebake has exact BaseColor/ORM and one
Normal channel sample different by one 8-bit level (RMSE .000282/255).
A prior rebake instead had two one-level ORM differences; retain the
explicit floating-point bake tolerance rather than claim universal byte
identity. No rebake replaces the canonical delivery maps.

Reopened the final 22 Cycles views, three matched pairs, Eevee checkpoint,
nine raw range controls, ten regenerated historical images and all eleven
regenerated before/after sheets at native size. The smallest crop panel is
1,152 pixels wide; no before/after panel is upsampled. Rechecked the current
contact sheets and exposed photographic profile selections. Color and value
remain as judged above; the listed close-wood, fine-age, context, vine and
dusk-sample limitations remain. No kit, neighboring delivery, top-level
README or docs image is changed. Suggested kit improvement: treat Eevee
shader compilation errors as failure even when Blender exits zero.

## Delivery pass 10 — reject the first revised framing and shaded color

Color and value first: opened all five native `renders/pass10/101` images.
The silvered base hue is closer to the photographs and the tank now holds
mid gray with fitting runoff. Reject the strongly blue shadow fill: it
obscures the tag-side checks and rust. Desaturate the physical sky fill and
raise its strength, retaining the separate raking sun and closed cavities.
The first camera-sky gradient is still too uniformly muted: increase the
horizon radiance and darken/saturate the upper sky independently of fill.

The closer hero clips the upper crossarm. Reject it; use a 35 mm portrait
from eight metres, framing the actual base and top together. The ground
ring is present, but the evenly spaced straight grass blades read as
bristles. Replace them with overlapping tufts of curved, tapered blades.
The ground-line wetting still reads too weakly on the visible face; broaden
its azimuthal exposure and place green damp growth on that shaded front.
Vine removal is accepted; there are no foliage quads left on the delivered
pole. Fine wood texture remains visibly filtered at a macro distance.

## Delivery pass 11 — neutral fill accepted; reject the remaining presentation artifacts

Color and value first: opened native hero/base/tags/transformer/dusk, both
local equipment fits and the full communications portrait. The neutralized
fill preserves silvered wood instead of blue-black shadow; the tank body in
the MD fit samples about 111/123/130 sRGB against 110/118/130 in the balanced
photo. This is displayed appearance under estimated light, not reflectance.
The clear hero's upper sky samples 6/78/137: its red channel is too low.
Reject that over-saturated field and retain a continuous, lighter blue
zenith-to-horizon gradient. The bottom edge of the transformer remains deep.

The soil outline reads as a hard disk and its aggregate as pyramids. Feather
the installation's disturbed boundary into existing turf and use rounded
pebbles. Trimmer damage reads as soft pale spots: replace the mask with thin
horizontal impacts. The bark macro grain is still stretched at this atlas
density; long checks and fastener runoff carry the larger-scale information.
The full-height portrait frames both base and equipment correctly and keeps
the street running away beside it. The dusk pool reads on pavement; the
large blue sky still needs azimuthal warmth from the sunset side.

Reject the first NC corner: bending isolated modules leaves broken curb
joins and the crossing surface looks pasted over them. Build one coherent
presentation corner instead. Two additional image candidates were inspected
and rejected as replacement street fits (slope/curve, or different parallel
feeder construction). Preserve the accepted exported street geometry.

## Delivery pass 12 — final preparation at native 1600 pixels

Color and value first: opened hero, base, tags and dusk at native resolution,
the two equipment fits/full communications portrait, and the NC street.
The wood is gray rather than warm brown, the damp green/dark foot occupies
the lower .6 m, and the tank has a darker underside and fitting stains.
Retain the neutral fill. The upper camera sky still needs more saturation;
move its blue transition to a lower elevation and brighten the horizon,
using measured NC/VT clear patches separately from the brighter MD sky.

The softened soil boundary and rounded aggregate no longer have the hard
outline/pyramids of pass 11. Horizontal trimmer cuts, long grass tufts and
pole wetting are visible at pedestrian distance. Their small relief and
wood fibres remain filtered in a close crop. Give the long grain and checks
a gentle common spiral instead of the remaining evenly vertical bands.
The hero contains the actual base and all equipment, with a real sidewalk
viewpoint. Dusk now varies toward the sun's side, the can stays dark, and
the light pool reads on the paving. Isolated bare-wire sparkle remains.

The NC approach now curves into a T corner and the near pickup is gone.
Reject its black gaps: flat curb ribbons lack the vertical cast-concrete
faces. Add those faces and restore the asphalt's actual 6.096 m source
coverage (the draft used the concrete's 3.048 m scale). House types/setbacks
still differ from the photograph; this is an original layout comparison,
not a survey. The exported street/clearance geometry is untouched.

Opened every tangent/dead-end gallery direction in native 800-pixel strips
and the 1.8 m scale view. Their studio exposure is too bright for silvered
wood; lower it .6 stop before finals. Gallery selections preserve each
retained exported triangle's coordinates, UVs and split normals; the
sections are explicitly documented, rather than claimed standalone crops.

## Delivery pass 13 — reject a measured sky-value undershoot

Color and value first: opened all twelve completed native frames from the
first clean final batch (hero, street, above, transformer, crossarm,
communication, dead end, anchor, service, tags, both distance versions; base
was cancelled). The upper hero sky measures 58/107/156, Y prime .393,
against balanced NC 79/124/167, .460. Reject the undershoot. Empty-world
Cycles/AgX probes recover the latter exactly at the hero exposure and the
horizon at 184/198/200. Expose photographic camera skies independently of
their surface-light exposure; retain actual hemispherical fill and raking
sun, and the accepted wire controls. The brighter MD sky has its own
measured radiance field. It is sky radiance, not a reflectance/albedo value.

The MD shaded shaft in pass 11/12 remains about 110/118/123 against
96/98/105; reduce only the silvered dry-wood base to .170/.158/.150 linear,
retaining the tank (already close), damp absorption and localized scuffs.
The source wood stays neutral gray rather than the original warm brown.
Macro fibres remain soft, and the context's repeated pickups and setbacks
remain visible. The deep tank underside and warm dusk pool are retained.

SIGINT cancelled a frame without stopping Blender's Python shot loop.
Reject a cancelled render as a success: the family now requires FINISHED
and an actual output before writing provenance. The remaining batch was
terminated and is not delivery evidence. Rebuild cleanly again with this
last measured correction; review every replacement at native size.

## Delivery pass 14 — native export final audit

Color and value first: opened all 22 replacement Cycles street/detail frames
at native size. The clear-day upper sky now measures 79/124/167 against
balanced NC 79/124/167. A lower unobscured patch just above the roofs reads
167/185/191 against the photograph's thin-cloud 184/198/200; it remains
.052 darker in displayed Y prime. These are image zones, not surveyed sky
angles. Keep that residual explicit. The intermediate sky patch is retained
in the measurement record, rather than silently calling it the horizon.
The earlier linear gradient looked overcast in horizontal street views;
clear-day saturation now develops lower in the sky while the fitted photo
views retain their own gradients.

Sunlit upper-shaft wood measures 149/144/139 against the balanced VT
149/142/132 (.568 versus .559 Y prime): slightly cooler, within .009 in
value. The ground-line view is wetter and darker and is not substituted for
that dry upper-shaft comparison. The MD shaded wood and tank comparison is
measured separately after its final photographic render. Neutral assumptions
and every measurement rectangle remain visible in `build/color-review/`.

The hero contains the near pole's entire base and top, with checks visible
along the shaft, wetting/scuffs and backfill at its foot, and the street
receding beside it. The tank holds gray with localized runoff and a dark
underside. Dusk has a warmer sunset side, a blue gradient, a dark tank and
a pavement light pool. The sparse vine is gone. All four streets and their
above views were opened individually, as were every construction detail
and both range-policy views.

What still reads as CG: fine shaft grain and small scars are filtered at
this shared atlas density; some long checks are stronger than their fine
branching; grass tufts and rounded aggregate remain economical presentation
geometry. The accepted context repeats houses and pickups, particularly
from above. Dusk retains isolated specular samples on bare wires. These
limits are not hidden by the contact sheet.

The shared machine interrupted an earlier make batch. Completed views now
survive subsequent interrupted jobs, and matching source/recipe/context
receipts allow a serial batch to resume without accepting old images. The
final 18 remaining frames were rendered together under one GPU lock; `make`
then resumes the same clean build for the remaining evidence and gates.

## Delivery pass 15 — matched-light values accepted; reject the curb joins

Color and value first: opened all three photographic renders at native size,
including the uncropped 749 × 1640 communications portrait. MD wood now
measures 100/106/113 against balanced 96/98/105 (+.0265 Y prime); the tank
111/123/130 against 110/118/130 (+.0142). The MD sky is 198/206/228 against
196/206/229 (+.0020). Retain the material/light correction: silvered wood
and gray paint are close in both value and hue without lifting cavities.
The sunlit upper shaft comparison in pass 14 covers the second balanced
wood photograph. The warmer, wet ground-line wood is not a dry-wood target.

The NC T corner has the intended approach bend and right-hand houses, but
the final reveals black seams at the curve joins. Reject it. The old return
started at the un-offset centreline and its walk continuation ignored the
walk's radial offset. Finite chord normals also pulled the first/last walk
edges apart. Solve the return from the actual bent-ribbon endpoint/tangent,
end both curves on the crossing curb line, continue the walk at its true
offset, and use exact endpoint tangents. Measure all eight actual built
curb/walk edge joins, not just their intended coordinates.

The other 22 views retain their appearance; source-recipe provenance is
refreshed by a serial export render batch under the shared GPU lock. Native
image hashes are compared to the inspected pre-join finals, and any differing
image is reopened. The small shared-atlas fibre/scar filtering, economical
ground vegetation and repeated context remain the principal CG tells.

## Delivery pass 16 — remove the crossing's false asphalt patch

Color and value first: the native before/after sheets retain the measured
gray shaft/tank and clear sky. The wider NC crop exposes a sharp dark
rectangle at the crossing. Reject it. A separate construction inspection
finds the actual main/crossing road normals already point upward, despite
the input ribbon winding; the toolkit recalculates them. Do not infer
shipped normals from an assumed vertex order. Two crossing-walk sheets do
face down and are explicitly reoriented upward.

The asphalt sheets overlapped coplanarly. End the approach precisely on the
crossing edge instead, using actual mesh Y extrema to prove their domains
meet without overlapping area. Curb/walk endpoint checks remain separate.
The final NC pair must be reopened after this correction. This changes only
the photographic setting, not a pole, map, line or accepted block.

All 32 gallery directions, the 1.8 m scale, Eevee and the pedestrian-range
study have now been opened at native size. Gallery top sections intentionally
show the cut shaft's open plane; they are documented inspection selections,
not hollow shipped poles. The 10 m study ray measures 9.87345 m to the actual
shaft surface and 10.00000 m to its axis. Larger checks read; fibre/scar
filtering still limits the macro surface. All nine wire control images were
opened at native size, and `contrast.json` is byte-identical to the accepted
f824685 control. No line appearance recalibration was introduced.

`make` and the explicit `make check` passed; `make repeat` passed after an
interrupted attempt: five geometry packages and 48 fields repeat byte for
byte. The independent rebake is identical for BaseColor/ORM; Normal differs
by at most 1/255, RMSE .000282/255, within the existing tolerance. The root
repository check reports zero errors. The later paving correction changes
none of those geometry/map inputs.

## Delivery pass 17 — final acceptance and image delivery

Color and value first: the final measurement table is unchanged by the
paving-only correction. Hero foreground Y prime p1/p10/p50/p95/p99 is
.0157/.1539/.4822/.6224/.7046; the near-white clipping fraction is .00000771.
This is the lower 56% of the displayed hero including context, not a
segmented utility albedo audit. The can underside and closed cavities retain
deep shade, and highlight rolloff is preserved.

Opened the corrected NC comparison again: the coplanar rectangular patch is
gone. Actual approach minimum and crossing maximum Y both measure
−23.076200485 m; their domains meet at an edge. The eight curb/walk endpoint
gaps remain below .000002 m. All 22 refreshed street/detail images differ
from the previously inspected native finals by at most one encoded channel
level; decoded-image comparison is in the worktree's
`build/utility-paving-image-equality.json`. No shape/material change was
introduced outside the NC comparison.

Opened all nine native before/after sheets, all five final docs JPGs, the
matched-light sheet and the complete 69-view contact sheet. Every fix panel
is at least 800 pixels wide without enlargement. The JPGs remain under
1600 pixels wide and 200,000 bytes, and the last pure review run reproduces
the inspected docs byte for byte. Docs are committed only after this audit.

Remaining CG tells: filtered fine wood fibres/scars, economical grass and
aggregate, repeated house/tree/pickup forms, a more even and lighter NC
pavement/turf response than the photograph, estimated camera/light and
equipment-placement differences, and isolated dusk bare-wire sparkle. The
upper/lower photo sky zones have no surveyed elevations; the lower clear
hero remains .052 Y prime below the thin-cloud comparator. Gallery section
cuts and the uncompiled engine far-shader example are documented limits.
The utility itself remains within its accepted geometry/material/texture
budgets. No kit or neighboring source/delivery was changed.

## LOD rollout preflight — blocked, 2026-11-09

Merged current main (already up to date), read the family construction, wire
policy and original check graph. `build/lod-rollout/utility/preflight.json`
records all fifteen expected glTF/BIN/JSON paths absent and zero generated
build files. There is no accepted geometry/map input for an immutable-source
receipt, native comparison or original `make check`. That check depends on
`export` and would rebuild missing accepted deliveries, so it is not run.
No config, LOD render, adoption or LOD0-only minimality claim is made. Two
render critique passes and `check-lod` are not possible without those inputs.
No kit/source delivery/docs image changes. The lead needs to stage the accepted
packages, maps and generated check inputs before this family can be adopted.
The tool hashes were recorded without invoking the builder at revision
`b132747`; `build/lod-rollout/utility/freeze.sha256` remains checkable.

## LOD round 2 — rebuild the originals

Round 1's absent ignored products are not an asset defect or a reason to ask
for staged deliveries. `make -C utility export check` rebuilt them here from
empty build/texture/export directories, exiting 0. It runs the family's complete
original geometry, bake, external delivery and checks, leaving existing docs
JPGs unchanged. Context construction stays inside utility/build and verifies
neighboring exports/textures unchanged. No car source or delivery was edited.

All five glTF+BIN sizes match the README exactly: Parts 2268943 bytes; streets
101/102/103/104 2905687/2412537/2780181/3004135. Street triangle counts also
match exactly: 45804/37628/41734/48116. The parts library measures 29932
triangles in nine primitives, with the documented individual module counts.
Shared PNGs total 10052349 bytes, one byte below the recorded trio; geometry
package sizes and counts match exactly. The original GPU rebake policy permits
small encoded-map variation; absent old maps, no pixel-equality claim is made.
Actual confirmation,
full command/exit/resource log and the new 18-file immutable export receipt are
in build/lod-round2/utility/{original-confirmation.json,original-build.json,
source-frozen.json}. Source UV/chart, normals, socket and physical checks pass.

Tool revision e375b58 and literal hashes were frozen before use. Start with an
unwired Tangent config: .4 at .25 with .05-pixel surface preservation for the
thin shaft. Experimental builds explicitly add kit/lod_rules.mk on the command
line; no public Makefile exposes a candidate before it passes its own proof.

### Tangent critique 1 — native switch and close views

Opened all three native strips, both 960-pixel construction views and the
contact sheet in renders/lod/tangent. Color/value first: the original's dark
treated timber and gray hardware retain their values; the difference panes
show no broad wash or missing silhouette. Braces, porcelain, shaft taper,
ground molding and the lower cable loop remain. The construction views expose
the original's small polygonal bends, without a new coarse break at the switch.
This is a comparison to the accepted export, not a new photo-realism approval.

The .05-pixel trial measures 3632 -> 2592 triangles at .25 / 36.315 m,
above the 1453 goal. Generic check-lod and the independent guarded-atlas test
both pass; zero triangles leave their stock charts. Brand support gaps are
.345–.436 mm, below the original's 1 mm maximum. Preserve that trial's config,
payload and images in build/lod-round2/utility/tangent-pass1 before testing
.5-pixel surface preservation for a cheaper witness. No delivery claim yet.

### Tangent critique 2 — stop on guarded-chart regression

Opened the three new native strips and both construction views. Color/value
first: no broad pole-color change appears; the difference is concentrated at
hardware and the loop. Thin braces remain rather than disappear. The cheaper
trial measures 1620 triangles against 1453; all native image limits and both
generic check-lod stages pass. Those passes do not approve the delivery.

The independent family audit finds **34 new guarded-chart crossings**, versus
zero in LOD0 and the first trial. Brand support still passes. A triangle that
crosses a stock boundary can interpolate unrelated material even when these
three views hide it. This is the frozen simplifier's chart defect, not a reason
to relax the original chart limits. The utility family stops here, as required;
no other pole, transformer, crossarm or street-wire kind inherits an approval.
No general tool change is in scope. The 280-triangle GuyAssembly remains
LOD0-only: its thin guard, guy and anchor already use coarse geometry.

Both trials' exact configs, payloads, native images and hashes stay in
build/lod-round2/utility/tangent-pass{1,2}/. The final chart failure is
tangent-pass2/atlas.json; rejected measured cost reports are in
build/lod-round2/utility/rejected-report/. The live rejected mesh is removed
from export/lod. The src config is evidence, wired to no Makefile target.
No README trial table or public LOD hook is added. The original check is
rerun with accepted generated inputs frozen explicitly; its complete command
is in original-check-command.json. Receipt and freeze outcomes are recorded
in the closing entry below.

Closing result: original make check exits 0, including seven unit tests,
physical construction, raw/imported delivery and render-input validation.
All 103 frozen tool hashes match; all 18 newly built source files and all
1206 pre-existing delivery/texture/docs files retain their hashes. Repository
check and diff whitespace check pass. Utility has no lod/check-lod targets.

## Fixed-region adoption — Tangent, 2026-11-09

Tool freeze `cc6cfee`; literal source/recipe hashes are in
`build/lod-uv/freeze.sha256`. The originals are already built here and match
the recorded package counts; the original frozen-input `make check` passes
before adoption (`build/lod-uv/utility-original-before.json`). Source, map and
docs bytes are covered by `build/lod-uv/originals.json`.

### Tangent critique 1 — region fix, support failure

Opened all three native strips, both construction views and contact. Color
and value agree with the dark source timber; shaft, braces, porcelain and
cable loop retain coverage. The new .5-pixel trial has 2828 triangles versus
the old 1620, a 1208-triangle cost. Its guarded-chart crossings fall from 34
to zero. Generic checks and images pass, but the independently measured brand
support gap reaches 2.204 mm, above 1 mm. Reject it. Exact config, payload,
images and hashes: `build/lod-uv/archive/utility/tangent-support-failure/`.

### Tangent critique 2 — retain support at the original switch

Restored the previously successful .05-pixel surface bound. Opened all three
new native strips, both construction views and contact, then revisited the
shaft and small label at native size. Values, taper and dark underside agree;
the cable loop and braces remain. The close view still exposes original
low-sided fittings and coarse timber detail, not close-view equivalence.
The level is 2852/3632 triangles at .25 / 36.315 m, missing 1453. It costs
260 triangles over the old safe 2592 trial, and 1232 over the rejected 1620
chart-crossing trial. The cheaper new 2828 trial is a support failure, not a
visual waiver or a claimed mathematical minimum. Maximum measured brand gap
is .4331 mm and crossings are zero. All original RGB/alpha/local/IoU gates,
re-import, source-field and tangent checks pass. The achieved saving is modest
(21.5%); it allocates .2243 MiB of mesh and no image. Actual per-level and
stored costs are in the measured README table. No material or map changes.

The post-build original `make check` passes, including all seven unit tests,
physical construction and source/import checks. `make check-lod` now includes
the independent atlas/support audit and passes. All 30 utility delivery/map/docs
files match the immutable receipt; all frozen tool hashes match. Final per-kind
payloads, images and simplification receipt are archived in
`build/lod-uv/archive/utility/tangent-final/`. The report contact is
`build/lod-uv/utility-report/contact.jpg`; native judgment uses
`renders/lod/tangent/`, not its reduced index. This is rest/source-field and
actual support-gap proof, not an engine timing or continuous-motion claim.

### Crossarm critique 1 — native field and coverage

Opened all three native .09 / 9.228 m strips and their difference panes.
Color/value, wood grain, porcelain and zinc agree; both thin braces and their
lower joint remain. The trial is 1172/1248 triangles against 187. All image,
field, topology, re-import and guarded-atlas checks pass; no new crossings.
Worst mean .0000335, local .00104 and IoU loss .000123.

### Crossarm critique 2 — reject an uneconomic extra row

Opened both construction views and contact, then revisited native end hardware
and the brace joint. No new unsupported piece or missing thin member appears;
the old low-sided sheds and tiny bolt geometry remain coarse. The row retains
93.91% of LOD0, saving only 76 triangles while adding 101592 mesh bytes.
Keep the 1248-triangle original instead of another almost-complete buffer.
This is a cost decision under the recipe's already-compact module rule, not a
tool or image failure. Config stays unwired; payload/images/checks are archived
in `build/lod-uv/archive/utility/crossarm-cost-rejected/`, removed from live
export/lod. It has no runtime switch recommendation or residency increment.
Its two rejected trials have no runtime residency or placement recommendation.
