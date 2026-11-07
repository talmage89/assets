# Civil form and construction basis

The setting is 2012 maintenance on a 1970s four-lane freeway. These are
original, plausible configurations for a game asset, with measured exported
sections. They are not construction documents or a load/crash-rated design.
The source register distinguishes period publications from later explanations
of the same conventions. The full copyrighted AASHTO books were unavailable;
their recommendations were researched through the official AASHTO excerpt,
FHWA explanations and the period state-DOT material, not claimed as read.

## Cross-section, plan and vertical geometry

| Feature | Model | Basis |
| --- | --- | --- |
| Through lanes | 2 each direction, 3.6576 m / 12 ft | AASHTO Green Book recommendations reproduced in FHWA freeway primer table 4 and AASHTO §8.2.4 excerpt |
| Right / left paved shoulder | 3.048 / 1.2192 m; 10 / 4 ft | Same, four total lanes and moderate truck volume |
| Tangent crossfall | 2%, away from median | AASHTO cross-section excerpt; independently measured on exported road triangles |
| Curve | 1,400 m centerline radius, 4% bank toward circle center | Authored design choice; constant-bank excerpt, with a separate bank-transition module |
| Diamond median | 2.4384 m / 8 ft between paving edges | Authored pier reservation, 4 ft shoulder in addition on each carriageway |
| Wide median | 9.144 m / 30 ft between paving edges | Authored cable-barrier installation; no claim that a universal clear-zone width applies |
| Diamond / curved stretch | 1,600 / 1,000 m modeled length, plus far continuations | Full acceleration lanes fit inside the diamond, not compressed to fit a picture |
| Diamond terminal axes | X ±78 m on the arterial | Authored spacing, distinct from ramp length; USGS 2002 photo supplies plan comparison |
| Ramp | 16 ft travel width, 4/6 ft inner/outer shoulder | Authored generous single-ramp envelope; terminal branches flare for turning |
| Ramp vertical profile | −.28 m freeway throat to +7.35 m terminal, first 10% held at low grade, then cubic vertical curve | Original grade profile; actual path gradient and plan radii are measured in `build/check.json` |
| Speed-change lane | 3.6576 m, 366 m parallel length + 91.44 m taper | TxDOT acceleration/gap-acceptance discussion; generous authored length, not a traffic-volume calculation |
| Recoverable cut slopes | Approximately 1:4 outside the ditch where space allows | FHWA explanation of AASHTO Roadside Design Guide; the ramp wedges and paved abutment slopes have different geometry |
| Shoulder ditch / inlets | .36 m nominal depression, 600 × 900 mm inlet | Authored construction choices; grates have actual open bars |

Station is Blender +Y. East (+X) traffic moves toward +Y; west traffic moves
toward −Y. The curved seed uses the exact circular alignment and its normal,
rather than rotating a row of straight road boxes. Earthwork is cut around
the ramps and the freeway. The arterial crosses on +X at station 0.

## Pavement, barriers and equipment

The [2003 MUTCD](refs/SOURCES.md) §3A.05 and 2009 §3A.06 support 4–6 in normal
lines and 10 ft broken segments with 30 ft gaps. This family chooses **6 in**
freeway lines, **10/40 ft** dash/cycle, yellow left and white right edges,
3/12 ft dotted auxiliary boundaries and raised markers after the dashes.
The arterial's two-way turn lane has solid outer and broken inner yellow
lines. The 2009 freeway guide-sign chapter informs the green/white hierarchy,
exit tabs, arrows and nominal overhead clearance. Lettering uses installed
DejaVu Sans Condensed Bold, an explicitly approximate alphabet. LARK / 47 is
an original plain state marker. No Interstate shield appears in an asset.

| Construction | Dimensions and limits |
| --- | --- |
| Jointed concrete | 4.572 m / 15 ft transverse spacing; 12 mm visible joint, longitudinal joints on lane boundaries; placement-owned retrofit patch groups |
| Milled shoulder strip | .4064 × .1778 m / 16 × 7 in envelopes at .3048 m / 12 in pitch, .3048 m off travel edge; represented by cards at this form gate |
| F barrier | .8128 m / 32 in high; .6096 m / 24 in base, .1524 m / 6 in top; 3 in toe / 10 in slope break; 6.096 m bay, actual .3048 m drainage opening |
| W-beam | 2.66 mm sheet, 311.15 mm face envelope, 83 mm depth; 31 in steel top, 1.905 m post centers; rail has two shells and edge returns |
| Blockout | 203.2 × 152.4 × 355.6 mm; top slightly above steel top, as a separate timber component |
| Generic end treatment | 7.62 m inspection module; energy-absorbing head, weakened-post form, ground strut and tension cable; no named proprietary terminal copied or certification implied |
| Cable | Three 19 mm envelopes at .53 / .68 / .83 m, 6.096 m bay; attachment clips and small self-weight sag |
| Sound panels | 6.096 m span, 4.2672 m / 14 ft high, 152.4 mm gauge, three horizontal panels in H posts; authored dimensions informed by GDOT's period post/panel construction |
| ROW fence | 1.83 m, 3.048 m posts; original chain-link family's analytic 3.048 mm wire / nominal 2 in mesh field; two tension wires |
| Sign truss | 34 m span, 1.52 m truss depth, four chords and triangulated side/top/bottom webs; .46 m posts, anchored footings and rear service walk |
| Replaceable signs | 7 × 2.74 m through, 5.49 × 2.74 m exit, 2.43 × .61 m tab; .0032 m aluminum back with stiffeners |
| Davit | 12 m mounting height, 2.4 m reach, curved tube and separate luminaire socket |

WSDOT's 1999 bridge-rail memo supports the 32 in F-shape type; its 2015
barrier material supports the maintained Type 31 installation. The truss,
terminal and attenuator are original generic constructions: their member
sizes and mechanical arrangement remain illustrative, not agency-approved
hardware. Retroreflection, small bolts, grate casting marks and wear belong
to look-dev, rather than additional silhouette triangles.

## Bridge load path

The arterial is a five-lane 11 ft / 3.3528 m street. Two 24 m spans carry
the **21.336 m / 70 ft** deck, with sidewalks, inner parapets and an outer
safety fence. Deck crown is 2%; the center is +7.35 m and nominal soffit is
+7.10 m. Seven girders per span sit at 2.74 m centers. The traditional
54 in / 1.3716 m AASHTO IV envelope uses .6604 m flanges and a .2032 m web;
this is not the newer Tx54 profile.

Each 23.49 m girder is a reusable object with end sockets, modest 18 mm camber,
and an elastomeric bearing at each end. Steel plates meet the bent/abutment
seats. The three **1.2 m** round columns carry a **19.8 × 2 × 1.1 m** cap.
End diaphragms brace the webs. Abutment backwalls rise behind the ends; wing
walls retain approach fill and approximately 1:1.6 slope paving protects it.
Six-meter approach slabs, expansion joints, scupper throats and connected
downpipes complete the visible construction. Hidden piles, prestressing
strands and reinforcing cages are omitted. Final bridge weather will originate
at joints and drains, not random stains.

The independent audit samples actual road-to-girder rays and pad-top-to-girder
gaps after fresh import. These prove geometry, not structural capacity. The
FHWA 2008 photograph is a useful period bearing/cap comparison but shows a
different pile bent and precast beam design; its camera fit is explicitly a
feature comparison, not a reconstruction of that bridge.
