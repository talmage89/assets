# Utility form and construction decisions

The target is maintained 1970–2010 US overhead residential distribution, seen
at pedestrian distance. The new meshes, label pixels and lighting are original.
The look checkpoint uses original physically scaled fields, a Cycles bake and shared external glTF maps.
Full source URLs, authors and rights are in [refs/SOURCES.md](refs/SOURCES.md).

## Selected construction

Use a fictional **12.47/7.2 kV grounded-wye** distribution system. WPS C01
informs wood crossarms, braces and pole pins; WPS C20/C40 informs armless
spacing and standoffs; WPS transformer/guy drawings inform mounting and bonds.
These are original assemblies informed by those drawings, not labeled copies
of a utility's approved assembly. The crossarms are 8 or 10 ft, nominal
3¾ × 4¾ in sections; two ¼ × 1¼ in steel braces support the wood arm.
The ⅝-inch through bolts have separate bearing washers and nuts.

The RUS 1728F-804 index identifies the appropriate 12.47/7.2 kV system.
Its direct PDF endpoint was inaccessible. NRECA's published Simplified
Staking Manual reproduces REA/RUS examples, their current assembly cross-reference,
staking, tension/sag and guying rules. It was read alongside WPS. We do not
claim access to the paywalled NESC or ANSI volumes or an exact RUS assembly.

WPS and Puget Sound Energy differ. WPS JU10 allows a 30-inch effectively
grounded neutral gap under stated conditions; PSE's secondary/neutral policy
uses 40 inches. This family chooses a **40-inch minimum to supply conductors**
at the pole and across spans, with a nominal 1.32 m pole separation. Grounded
supply equipment keeps a 30-inch zone; light-arm geometry stays above it.
Communication service drops and electric service drops converge toward the
house, with more than 12 inches between their mast attachments.

Geometric screens use **20 ft primary**, **18 ft neutral**, and **15½ ft
communications** above level grade. Customer triplex retains **18 ft across
the road** and **16 ft throughout private land**, using WPS Section 7's general
Type-A service criterion instead of its limited 12-ft residential-driveway
exception. Customer communications retain **15½ ft across the road** and an
authored conservative **12-ft private-yard screen**. Imported triangles are
clipped at the actual curb-back planes before measuring crossing minima.
The primary screen is the NRECA example's working criterion; WPS JU10 supplies
the local roadway communications figure. Roof overflights keep **8 ft**;
the corner attachments avoid any in the sampled current layouts. The tests evaluate
the authored self-weight/tension state and actual roof surfaces, not the
full temperature/ice/wind, strength, easement or clearance-table problem.

## Pole dimensions

Southern yellow pine, ANSI class 4, with a bare cut top. ANSI O5.1 specifies
class circumferences, not installation depth. WPS **P30** is the available
dimension table; **P25** supplies the chosen firm-soil embedment. The
Association of Southern Forestry Clubs' ANSI O5.1-2008 table agrees.

| Overall | Set depth | Above grade | Circumference 6 ft from butt | Minimum top circumference |
| --- | --- | --- | --- | --- |
| 35 ft / 10.668 m | 6 ft / 1.8288 m | 8.8392 m | 31.5 in / .8001 m | 21 in / .5334 m |
| 40 ft / 12.192 m | 6 ft / 1.8288 m | 10.3632 m | 33.5 in / .8509 m | Same |
| 45 ft / 13.716 m | 6½ ft / 1.9812 m | 11.7348 m | 35 in / .8890 m | Same |

The 45-ft reference station is six inches below grade. Linear taper passes
through that station and the cut top. The generated 20-sided shaft adjusts
its circumradius so the **actual polygon perimeter** meets the table, rather
than silently losing circumference to an inscribed polygon. Only a 120 mm
installation stub is retained below grade; the buried six feet are metadata,
not wasted hidden faces. There are no climbing steps at any height.

The dry checks are tapered mesh slits for the checkpoint. An 8½-foot protective
molding follows the taper over the #6 copper grounding path, with nails,
staples, a utility tag and a fictional 1992 birth brand. Small rooted vines
appear on selected transformer/riser seeds. Surface checks, silvering, wet ground-line absorption, removed-sign scars and
bolt rust are in the shared normal/color bake, without additional game geometry.

## Hardware dimensions and connections

| Part | Selected dimensions / source |
| --- | --- |
| Porcelain pins | Hubbell ANSI 55-3: 4.75 in / 120.65 mm maximum shed, 3.75 in / 95.25 mm porcelain height; authored pin/tie details |
| Crossarm | 2.4384 / 3.048 m; .09525 × .12065 m sawn section; published utility/RUS construction idiom |
| Conventional transformer | MPS 50 kVA: 20 in / .508 m tank diameter, 42 in / 1.0668 m bottom-to-HV-terminal height; .8128 m tank body and .254 m bushing |
| Transformer reference envelope | MPS approximate overall width/depth 26/29 in; authored lifting eyes, hangers, cutout and arrester remain separate construction, not copied vendor CAD |
| Primary conductor | Southwire Raven 1/0 6/1 ACSR, .398 in / 10.109 mm published OD; authored 10.1092 mm |
| Neutral | Southwire Sparrow #2 6/1 ACSR, .316 in / 8.026 mm published OD; authored 8.0264 mm |
| Service triplex | Classic Wire Periwinkle: two 7.6962 mm insulated hots + 6.35 mm ACSR messenger; packed triangular constituents, unresolved helical lay |
| Communication | 6.35 mm strand; 37 mm 200-pair telephone, 24.384 mm jacketed CATV; two touching 15.8 mm fiber jackets (31.6 mm bundle); optional 28 mm retained copper; two to four separately supported routes |
| Inline splice case | .68 m long × .144 m diameter; authored housing, two clamps, hanger and two supported slack loops |
| Guy | ⅜ in / 9.525 mm strand envelope; ⅝ in / 15.875 mm anchor rod; 8 ft / 2.4384 m × 52 mm faded guard; WPS guy/anchor construction |
| Street-light bracket | 2 m tip reach, .46 m rise, 60.3 mm tube; carries the original `street-light/` head at its slipfitter datum |
| House mast | 60.3 mm rigid conduit, service saddle 5.2–7.435 m above house grade, sized from each roof and crossing; downturned head, drip loops, triangulated wall brackets and roof guys |

Can lids have rolled clamping lips, lifting eyes and a relief/drain fitting.
The high side has one bushing, a mounted cutout, arrester and separate leads.
The three-can seed has an actual support rack, separate primary phases and
**three independent 120/240 V secondary circuits**. Their hots are never
paralleled. Its center A-phase circuit supplies the demonstration houses;
two named circuits remain available. This is a mechanical bank, not a supplied
three-phase delta/wye secondary interconnection diagram.

Every phase on a three-phase riser has its own sealed pothead and insulated
tail from the shared conduit. Pin and post choices are construction variants.
The communication case hangs from strand hardware and its fiber loops return
to the case. Long-span lashing and conductor strands are future normal detail.

## Catenary and distance rendering

The span API solves an unequal-support catenary. Sag means the vertical drop
below the endpoint chord at horizontal midspan. It also accepts mass and
horizontal tension via **a = H/(mass × gravity)**. Seeded examples use Raven
.2158 kg/m / 550 N, neutral .1354 kg/m / 450 N, telephone 1.771 kg/m / 6,641.25 N, CATV .43 kg/m / 1,612.5 N, fiber
bundle .36 kg/m / 1,350 N and retained copper 1.135 kg/m / 4,256.25 N;
triplex .227692 kg/m / 446.455 N, and small comm drop .045 kg/m /
160 N. The service mass applies to its whole triplex even though the mesh
contains three constituent tubes. These are authored self-weight cases, not
a temperature/tension chart. Different utility sag tables remain external input.

Subdivision controls chord error to 8 mm and segment length to 4 m. Four-sided
tubes carry true diameter near the camera. Their low cross-section has a
directional width compromise; a final close-view LOD may use six sides.

NVIDIA's prefiltered-line research and Pixar's minimum-width/coverage method
inform the far representation: camera-facing ribbons, **.85-pixel minimum
width**, opacity compensated by `(true projected width / widened width)^.55`.
The original strict exponent 1.0 preserved integrated energy but left the
120 m primary at only 2.3% displayed contrast. The .55 exponent deliberately
retains more optical contrast; it is a calibrated visibility compromise,
not a claim of conserved energy or a larger physical conductor. An engine
should transition when the true tube falls below approximately .8 px, and
retain physical tube shadows. It needs
no wire texture. The Cycles distance pair explicitly compares the original
GLB tubes with a camera-evaluated version of that policy. The supplied original
Godot shader and mesh-data generator are integration examples; no Godot binary
is installed here, so compilation, TAA/MSAA motion and engine performance are
not certified by the Cycles comparison.

## Surfaces, light and photographic limits

Original 4096 source fields are baked in Cycles, then filtered to one shared
2048 BaseColor / tangent +Y Normal / ORM set. Sixteen guarded stock charts
intentionally reuse UVs across repeated materials and hardware. These are not
a unique object unwrap: the delivery gate measures chart boundaries,
nondegenerate triangle UVs and per-role density, and reports intentional reuse.
Two round-pine charts carry grain, checks and age. Fibres warp coherently
around knots; the fir arm's grain runs along its actual length. Causal masks
put moisture at grade, end weathering at the cut top, fastener runoff below
its mounting height, chalking on exposed paint and retained dirt at the can
bottom. Zinc, gray dielectric hardware and faded guards retain their material
colors. Own fictional stamps use installed open fonts and the same atlas.

The presentation imports the external glTF and its baked maps. Neighboring
houses, original maple/pin oak, pickups, ground and light heads are rebuilt
from this library's source into utility-local scratch folders and retain
their source-look shaders. They are presentation context, not utility delivery
geometry and not a claim of re-exported neighboring final assets.

Photo cameras are estimates, not a survey. NC fits several pole/socket
landmarks; the transformer-top fit uses the shaft and both crossarm pins,
with the actual can height/position retained as a visible construction
difference. The communication camera fits the full pole base, cut top and both upper
arm pins; the telephone-height shaft point is held out. Its portrait is
rendered at the photo's native dimensions and cropped identically for review,
preserving the full camera principal point. Full portrait and calibration
overlays remain available beside the pair.
Every residual and point is recorded, and Blender independently verifies
the camera projection. Lighting is estimated separately from each photograph.
The final pairs retain original photographic colors. Separate NC/MD color
inspection copies balance on approximate achromatic cloud ROIs, recorded with
linear gains in `build/reference-balance/balance.json`. Beige concrete and a
shaded insulator were rejected as neutrals. The hardware photograph has no
accepted neutral and supports geometry/contrast comparisons only; its pole
hue is not used as an albedo target. Clouds are assumptions, not gray cards
or albedo measurements. Native photographic wire depths are unknown;
near/middle/far image profiles bracket contrast while exact 30/60/120 m
ranges apply only to our model. No photo is projected or used in an asset map.

The last form pass moved the optional service masts to solid corner jambs
outside porch roofs. The mast height is the greater of 5.2 m or the measured
roof-guy anchor plus .75 m, raised only when its own tensioned crossing needs
it. This removes repetitive tall masts over the single-story houses while
retaining the roof support and actual road/driveway clearances. All house
sources/deliveries remain untouched.
