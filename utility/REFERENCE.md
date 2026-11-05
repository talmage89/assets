# Utility form and construction decisions

The target is maintained 1970–2010 US overhead residential distribution, seen
at pedestrian distance. The new meshes, label pixels and lighting are original.
The checkpoint deliberately uses quick materials; it is not the final asset.
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
appear on selected transformer/riser seeds. Surface checks, silvering, wet
ground-line absorption, removed-sign scars and bolt rust belong in the next
normal/color bake, not additional game geometry.

## Hardware dimensions and connections

| Part | Selected dimensions / source |
| --- | --- |
| Porcelain pins | Hubbell ANSI 55-3: 4.75 in / 120.65 mm maximum shed, 3.75 in / 95.25 mm porcelain height; authored pin/tie details |
| Crossarm | 2.4384 / 3.048 m; .09525 × .12065 m sawn section; published utility/RUS construction idiom |
| Conventional transformer | MPS 50 kVA: 20 in / .508 m tank diameter, 42 in / 1.0668 m bottom-to-HV-terminal height; .8128 m tank body and .254 m bushing |
| Transformer reference envelope | MPS approximate overall width/depth 26/29 in; authored lifting eyes, hangers, cutout and arrester remain separate construction, not copied vendor CAD |
| Primary conductor | Southwire Raven 1/0 6/1 ACSR, .398 in / 10.109 mm published OD; authored 10.1 mm |
| Neutral | Southwire Sparrow #2 6/1 ACSR, .316 in / 8.026 mm published OD; authored 8.0 mm |
| Service triplex | Two 8.5 mm insulated hots + 6.2 mm messenger; Southwire construction reference, authored strand envelopes; lay reserved for normal detail |
| Communication | 6.35 mm strand, 20 mm lashed fiber envelope, 28 mm telephone cable; authored maintained joint-use equipment, not a named vendor configuration |
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
.2158 kg/m / 550 N, neutral .1354 kg/m / 450 N, assumed supported telecom
.24 kg/m / 900 N, triplex .153 kg/m / 300 N, and small comm drop .045 kg/m /
160 N. The service mass applies to its whole triplex even though the mesh
contains three constituent tubes. These are authored self-weight cases, not
a temperature/tension chart. Different utility sag tables remain external input.

Subdivision controls chord error to 8 mm and segment length to 4 m. Four-sided
tubes carry true diameter near the camera. Their low cross-section has a
directional width compromise; a final close-view LOD may use six sides.

NVIDIA's prefiltered-line research and Pixar's minimum-width/coverage method
inform the far representation: camera-facing ribbons, **.85-pixel minimum
width**, opacity multiplied by true projected width / widened width. This
reduces broken lines without making remote wires into opaque ropes. It needs
no wire texture. The Cycles distance pair explicitly compares the original
GLB tubes with a camera-evaluated version of that policy. The supplied original
Godot shader and mesh-data generator are integration examples; no Godot binary
is installed here, so compilation, TAA/MSAA motion and engine performance are
not certified by the Cycles comparison.

## Appearance checkpoint limits

Gray-brown wood, brown porcelain, galvanized steel, gray-green can paint,
black jackets and faded yellow guards are provisional diagnostic materials.
They show construction; they do not represent the promised 15–30 years of
surface history. The next stage must prove the wood, rust runoff, chalking,
ground moisture and handling wear against used photographs after baking.
Nothing about the current images is described as final look development.

The last form pass moved the optional service masts to solid corner jambs
outside porch roofs. The mast height is the greater of 5.2 m or the measured
roof-guy anchor plus .75 m, raised only when its own tensioned crossing needs
it. This removes repetitive tall masts over the single-story houses while
retaining the roof support and actual road/driveway clearances. All house
sources/deliveries remain untouched.
