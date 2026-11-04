# Alder X220 — detail and look development

Original compact crossover, generated entirely by Blender 5.2 scripts. This is
an **unbaked source checkpoint**, with the accepted form, exterior detail,
five-seat cabin/cargo area, AWD underbody and functional hinges. It stops before
SUV UV allocation, baking and GLB delivery. The C150 export is untouched.
[Critiques](REVIEW.md), [reference measurements](REFERENCE.md) and
[credits](refs/SOURCES.md) distinguish observations from construction estimates.

## Images

All images here are ignored build products; checkpoint images are not committed
as final portfolio photographs.

- [Complete contact sheet](renders/suv-detail/contact.jpg)
- [Five factory colors, front and rear](renders/suv-detail/five-colors.jpg)
- [Face, optics, wheel, cladding, cabin and underneath](renders/suv-detail/details.jpg)
- [Opened parts and sampled trajectories](renders/suv-detail/motion.jpg)
- [Gloss clay](renders/suv-detail/gloss-clay.jpg) and [four stock-camera pairs](renders/suv-detail/gloss-pairs.jpg)
- [Front curvature / matching bands](renders/suv-detail/curvature-front_three_quarter.jpg), [rear](renders/suv-detail/curvature-rear_three_quarter.jpg), [side](renders/suv-detail/curvature-side.jpg), [front elevation](renders/suv-detail/curvature-front.jpg), [rear elevation](renders/suv-detail/curvature-rear.jpg)
- [Used front pair](renders/suv-detail/used_front-pair.jpg) and [used rear pair](renders/suv-detail/used_rear-pair.jpg)
- [White-balanced measurement picks, front](renders/suv-detail/used_front-measurement-picks.jpg) and [rear](renders/suv-detail/used_rear-measurement-picks.jpg)

## Form fixes and accepted package

The cowl's hard hood/canopy branch introduced a height/derivative discontinuity.
A continuous blend removes that break. The fascia had a second fault: aperture
vertices sampled a different tessellation than their neighboring retained faces,
and the folded polar chart concentrated sliver triangles at the pocket/outer
lamp ends. New points now interpolate the same physical source triangles; a
constrained fascia chart redistributes samples without changing the aperture
outlines. The source density is master(3), independently triangulated once.

In the exposed front-corner diagnostic region, valid signed mean-curvature
samples below −5/m drop from five to zero (587 versus 347 eligible samples;
this is not a vertex-for-vertex count). The A-foot still has a coherent concave
draw rather than a flat patch; some thin cut-edge curvature noise remains. The
maps show actual game triangles; the bands use matching cameras. No normal-map
substitute or smoothed display mesh conceals them.

The mid-gray clearcoated clay uses a procedural sky and actual dark ground.
The shoulder now breaks from a bright upper reflection to a darker lower band,
the lower crease changes reflected value, and the fender crowns carry curved
highlights. Their accepted fields remain: approximately 16° across 30 mm at the
shoulder, the rising lower die crease and the two broad wheel crowns. The
accepted package, profile camera fits and original styling are retained. The
arch return joints and rear sash/header are split for actual movement.

| Quantity | Measured source / accepted nominal |
| --- | ---: |
| Length / body width | 4598.8 / 1842.0 mm, accepted form |
| Roof / rails / antenna maximum | 1679.0 / 1700.0 / 1735.0 mm |
| Width including mirrors | 2117.0 mm |
| Wheelbase / front and rear tracks | 2690.0 / 1600.0 and 1610.0 mm |
| Tires | 225/65R17; 724.3 mm unloaded nominal diameter |
| Lowest underbody surface | 205.0 mm, actual rear differential |
| Front / rear approach | 17.88 / 20.63°, accepted outer form |

The published class sources are Toyota's 2020 US brochure and Honda's 2020 US
specifications; Honda's UK brochure supplies the 2117 mm mirror-span cross-check.
They are linked with authors/licenses in the reference ledger. The antenna is
additional to the accepted roof/rail heights. Actual post-detail vertex bounds,
not transformed local bounding boxes, are measured by `suv_detail_check.py`.

## Construction, pivots and ranges

Meters; +Z up, front −Y, origin at ground footprint center. Side suffix L is −X,
R is +X; driver controls are at +X as in the family. Angles below use each named
node's **local** axis. No armature.

| Node | Closed pivot in vehicle coordinates (m) | Axis | Authored range |
| --- | --- | --- | --- |
| Door_FL / Door_FR | (−/+0.840, −1.035, 0.780) | local Z, inclined 5.71° outward; vehicle direction normalize((−/+0.10,0,1)) | L 0…60°, R −60…0° |
| Door_RL / Door_RR | (−/+0.820, 0.150, 0.780) | same inclined local Z | L 0…60°, R −60…0° |
| Hood | (0, −1.070, 1.120) | local X | −65…0° |
| Liftgate | (0, 1.620, 1.670) | local X | 0…75° |
| Wheel_FL / FR | (−/+0.800, −1.340, 0.35715) | local X | continuous; sweep 0…360° |
| Wheel_RL / RR | (−/+0.805, 1.350, 0.35715) | local X | continuous; sweep 0…360° |
| Steer_FL / FR | (−/+0.68409, −1.34431, 0.35715) | local Z, true 12° SAI / 6.5° caster | −35…35° |
| FuelDoor | (−0.91055, 1.47854, 1.04016) | local Z along its forward edge, vehicle axis (−.03070,.00006,.99953) | 0…85° |

Wheel centers are measured again from their actual node matrices in the reports.
Door pins and sleeves share a measured inclined bearing line; formed C-shaped
leaves reach the inner door carriers without sweeping through the fender. The
hood and gate each have two telescoping gas struts. A cut filler cup and cap sit behind the hinged fuel flap. Their attachment distances
are measured at 76 poses: hood 507–790 mm, gate 524–851 mm. Minimum rod engagement
is 110 / 89 mm respectively. The roof/header, rear sash, D-pillar upper return,
plate bed, lamps and spoiler are allocated to the correct moving or fixed group.

`kit.motion` tests evaluated solid crossings, parity and penetration at ≤2°
steps for doors/hood/gate/steering/fuel flap, and 15° for wheel spin. The tolerance
is 0.5 mm. Reconstructed collision gauges use the retained outer faces and
specified actual thickness where concealed back faces were removed. Allowed
contacts are listed explicitly: strut ball seats and the knuckle's CV/control-arm
joints. Tires, glazing, fenders, roof and spoiler have no blanket exemption.
The orange lines in the motion images are actual sampled vertex trajectories,
not a claim to be swept-volume boundaries. Individual-motion sweeps do not prove
that arbitrary combinations of open parts clear each other.

Exterior detail includes curved grille ribs/web, projector/reflector/guide optics
with lit state, original ALDER/X220 AWD badges, supported curved handle seats,
wipers, fin, fuel flap, side markers, trims/appliques, rail caps, seated washer
nozzles, and normal-relief cladding rivets. The plate is a fictional ALDER studio
label. The cabin uses the pickup's lofted-seat/dash method: five seats/headrests,
cluster, screen, console/shifter, wheel, conformed door cards, headliner, floor,
cargo floor and cover. Pressed rails, cradles, suspension, halfshafts, driveshaft,
rear differential, tank/straps, exhaust/hangers, muffler and transverse engine
fill low-angle and open-hood views at deliberately low detail.

## Materials and wear

The source uses the family's neutral paint coverage/contamination channels and
factory factors. Porcelain, Carbon, Graphite, Aluminum and Atlantic have authored
spawn weights 30/25/22/16/7%; these are artistic proportions, not sales statistics.
Colors use one material graph and no per-color texture copies. A clearcoat,
faint orange peel and metallic flakes distinguish paint from primer. Textured
cladding, gloss-black appliques, dark chrome, rubber, dusty alloy, turned discs,
cloth and clear tinted glazing have separate manufacturing responses.

Road film follows height and the tire wakes, stronger than on the sedan. Upward
cladding fades, loading surfaces and sills scuff, exposed door edges/hood front
chip, wash swirls alter clearcoat roughness, and actual measured skin-edge
distance drives gap dirt. Glass sediment stays at its lower edge. Masks use
rest-space positions and normals so opening parts does not slide their wear.
Fine grain, sipes, fictional sidewall text and rivets remain shader height for
the future bake. The original generated marking images are build products.

**Delivery plan:** one neutral 2048 BaseColor/Normal/ORM set, baked at 4096,
about **16 MiB** with block compression and a complete mip chain. Compatible
family materials use the same decode method. No SUV atlas has been baked, so
this is a budget, not measured delivered memory; bake loss and draw-call
consolidation remain later gates. The 35 source manufacturing materials and six original marking/display images are not
the final shipping material/texture count.

## Triangle allocation

| Part group | Game triangles |
| --- | ---: |
| doors | 2,322 |
| body | 10,385 |
| fascia | 5,011 |
| glass | 1,858 |
| cladding | 8,666 |
| liners | 1,168 |
| openings | 6,304 |
| mirrors | 2,716 |
| rails | 744 |
| spoiler | 1,710 |
| tires | 4,608 |
| wheels | 3,600 |
| brakes | 1,360 |
| interior | 3,736 |
| underbody | 1,668 |
| lamps | 2,032 |
| trim | 2,500 |
| mechanisms | 1,688 |
| pillars | 2,920 |
| **Total** | **64,996 / 65,000** |

The form source is 62,668 triangles before the detail allocation. Concealed
reverse skin faces are removed while retaining visible gauge/rims. Six nearly
planar side panes are reduced only when the measured chord error is ≤1.3 mm
and the solid remains closed; windshield/backlight reduction proposals are
rejected. The two glass layers share one exterior normal field; a hemisphere check alone
is insufficient. Independent laminate rays measure entrance/exit normal mismatch
on both densities: below 0.56° on rear/quarter panes and up to 3.65° at the
tightly curved lower front corner, against a disclosed 5° limit. The rejected
transfer produced a 47.7° optical prism. No glass thickness or IOR is disabled
in checkpoint views.
Hidden floor bevels and lower barrel/lug segment counts fund visible construction.
No pickup geometry or shared generator is changed.

<details>
<summary>Every game-source mesh, measured from its actual loop triangles</summary>

| Mesh | Triangles |
| --- | ---: |
| Door F_L | 614 |
| Door F_R | 617 |
| Door R_L | 544 |
| Door R_R | 547 |
| Front fender_L | 1130 |
| Front fender_R | 1151 |
| Front molded fascia | 2819 |
| Hood outer | 1410 |
| Liftgate outer | 1798 |
| Rear molded fascia | 2192 |
| Windshield | 620 |
| Front lower bumper cladding | 1528 |
| Rear lower bumper cladding | 3110 |
| Wheelwell_FL | 196 |
| Wheelwell inboard_FL | 96 |
| Wheelwell_RL | 196 |
| Wheelwell inboard_RL | 96 |
| Wheelwell_FR | 196 |
| Wheelwell inboard_FR | 96 |
| Wheelwell_RR | 196 |
| Wheelwell inboard_RR | 96 |
| Upper grille opening | 88 |
| Upper grille opening molded return | 256 |
| Grille folded surround | 512 |
| Lower intake opening | 108 |
| Lower intake opening molded return | 256 |
| Corner pocket L opening | 40 |
| Corner pocket L opening molded return | 160 |
| Corner pocket R opening | 40 |
| Corner pocket R opening molded return | 160 |
| Headlamp opening-1 | 296 |
| Headlamp opening1 | 296 |
| Headlamp opening-1 optical cassette | 472 |
| Headlamp opening1 optical cassette | 472 |
| Plate pocket opening | 136 |
| Plate pocket opening molded return | 160 |
| Plate lamp | 108 |
| Reflector L opening | 40 |
| Reflector L opening molded return | 160 |
| Reflector R opening | 40 |
| Reflector R opening molded return | 160 |
| Exhaust cutout opening | 40 |
| Exhaust cutout opening molded return | 160 |
| Taillamp opening-1 gate | 200 |
| Taillamp opening-1 quarter | 152 |
| Taillamp opening1 gate | 200 |
| Taillamp opening1 quarter | 152 |
| Taillamp opening-1 gate optical cassette | 320 |
| Taillamp opening-1 quarter optical cassette | 264 |
| Taillamp opening1 gate optical cassette | 320 |
| Taillamp opening1 quarter optical cassette | 264 |
| Liftgate sculpted garnish | 196 |
| Liftgate badge mounting land | 76 |
| Front side glazing_L | 136 |
| Rear side glazing_L | 96 |
| Quarter side glazing_L | 114 |
| Front side glazing_R | 138 |
| Rear side glazing_R | 96 |
| Quarter side glazing_R | 130 |
| Backlight | 528 |
| Mirror housing_L | 1246 |
| Mirror pane_L | 92 |
| Mirror sail_L | 20 |
| Mirror housing_R | 1246 |
| Mirror pane_R | 92 |
| Mirror sail_R | 20 |
| Lower door cladding_FL | 172 |
| Lower door cladding_RL | 200 |
| Roof rail_L | 268 |
| Rail foot_L0 | 52 |
| Rail foot_L1 | 52 |
| Lower door cladding_FR | 172 |
| Lower door cladding_RR | 200 |
| Roof rail_R | 268 |
| Rail foot_R0 | 52 |
| Rail foot_R1 | 52 |
| Chin skid finish | 268 |
| Rear skid finish | 268 |
| Liftgate spoiler | 1514 |
| Spoiler brake lamp | 196 |
| Tire_FL | 768 |
| Shoulder tread_FL | 384 |
| Wheel barrel_FL | 288 |
| Wheel center_FL | 120 |
| Cast spoke_FL_0 | 62 |
| Wheel lug_FL0 | 36 |
| Cast spoke_FL_1 | 62 |
| Wheel lug_FL1 | 36 |
| Cast spoke_FL_2 | 62 |
| Wheel lug_FL2 | 36 |
| Cast spoke_FL_3 | 62 |
| Wheel lug_FL3 | 36 |
| Cast spoke_FL_4 | 62 |
| Wheel lug_FL4 | 36 |
| Alder center cap_FL | 2 |
| Brake rotor_FL | 240 |
| Brake caliper_FL | 100 |
| Tire_RL | 768 |
| Shoulder tread_RL | 384 |
| Wheel barrel_RL | 288 |
| Wheel center_RL | 120 |
| Cast spoke_RL_0 | 62 |
| Wheel lug_RL0 | 36 |
| Cast spoke_RL_1 | 62 |
| Wheel lug_RL1 | 36 |
| Cast spoke_RL_2 | 62 |
| Wheel lug_RL2 | 36 |
| Cast spoke_RL_3 | 62 |
| Wheel lug_RL3 | 36 |
| Cast spoke_RL_4 | 62 |
| Wheel lug_RL4 | 36 |
| Alder center cap_RL | 2 |
| Brake rotor_RL | 240 |
| Brake caliper_RL | 100 |
| Tire_FR | 768 |
| Shoulder tread_FR | 384 |
| Wheel barrel_FR | 288 |
| Wheel center_FR | 120 |
| Cast spoke_FR_0 | 62 |
| Wheel lug_FR0 | 36 |
| Cast spoke_FR_1 | 62 |
| Wheel lug_FR1 | 36 |
| Cast spoke_FR_2 | 62 |
| Wheel lug_FR2 | 36 |
| Cast spoke_FR_3 | 62 |
| Wheel lug_FR3 | 36 |
| Cast spoke_FR_4 | 62 |
| Wheel lug_FR4 | 36 |
| Alder center cap_FR | 2 |
| Brake rotor_FR | 240 |
| Brake caliper_FR | 100 |
| Tire_RR | 768 |
| Shoulder tread_RR | 384 |
| Wheel barrel_RR | 288 |
| Wheel center_RR | 120 |
| Cast spoke_RR_0 | 62 |
| Wheel lug_RR0 | 36 |
| Cast spoke_RR_1 | 62 |
| Wheel lug_RR1 | 36 |
| Cast spoke_RR_2 | 62 |
| Wheel lug_RR2 | 36 |
| Cast spoke_RR_3 | 62 |
| Wheel lug_RR3 | 36 |
| Cast spoke_RR_4 | 62 |
| Wheel lug_RR4 | 36 |
| Alder center cap_RR | 2 |
| Brake rotor_RR | 240 |
| Brake caliper_RR | 100 |
| Seat rail L-0.15 | 12 |
| Seat rail L0.15 | 12 |
| Front cushion L | 68 |
| Front backrest L | 92 |
| Headrest stem L-0.063 | 16 |
| Headrest stem L0.063 | 16 |
| Front headrest L | 68 |
| Bolster seam L-1 | 20 |
| Bolster seam L1 | 20 |
| Seat rail R-0.15 | 12 |
| Seat rail R0.15 | 12 |
| Front cushion R | 68 |
| Front backrest R | 92 |
| Headrest stem R-0.063 | 16 |
| Headrest stem R0.063 | 16 |
| Front headrest R | 68 |
| Bolster seam R-1 | 20 |
| Bolster seam R1 | 20 |
| Rear bench cushion | 68 |
| Rear bench back | 68 |
| Rear headrest stem 0-0.05 | 16 |
| Rear headrest stem 00.05 | 16 |
| Rear headrest 0 | 68 |
| Rear headrest stem 1-0.05 | 16 |
| Rear headrest stem 10.05 | 16 |
| Rear headrest 1 | 68 |
| Rear headrest stem 2-0.05 | 16 |
| Rear headrest stem 20.05 | 16 |
| Rear headrest 2 | 68 |
| Dashboard shell | 64 |
| Center stack | 44 |
| Center display | 2 |
| Cluster binnacle | 44 |
| Cluster face | 2 |
| Dash vent -0.67 | 44 |
| Vent vane -0.670.983 | 12 |
| Vent vane -0.671.001 | 12 |
| Vent vane -0.671.019 | 12 |
| Dash vent -0.2 | 44 |
| Vent vane -0.20.983 | 12 |
| Vent vane -0.21.001 | 12 |
| Vent vane -0.21.019 | 12 |
| Dash vent 0.2 | 44 |
| Vent vane 0.20.983 | 12 |
| Vent vane 0.21.001 | 12 |
| Vent vane 0.21.019 | 12 |
| Dash vent 0.67 | 44 |
| Vent vane 0.670.983 | 12 |
| Vent vane 0.671.001 | 12 |
| Vent vane 0.671.019 | 12 |
| Center console | 44 |
| Console arm pad | 44 |
| Cup holder -0.15 | 96 |
| Cup holder -0.27 | 96 |
| Shifter | 20 |
| Shifter knob | 44 |
| Steering rim | 240 |
| Steering column | 28 |
| Steering airbag | 44 |
| Steering spoke 0 | 12 |
| Steering spoke 3.141592653589793 | 12 |
| Steering spoke 4.71238898038469 | 12 |
| Door card FL | 44 |
| Door inner carrier FL | 32 |
| Door armrest FL | 44 |
| Inside latch FL | 44 |
| Door pocket FL | 44 |
| Door card RL | 56 |
| Door inner carrier RL | 48 |
| Door armrest RL | 44 |
| Inside latch RL | 44 |
| Door pocket RL | 44 |
| Door card FR | 44 |
| Door inner carrier FR | 32 |
| Door armrest FR | 44 |
| Inside latch FR | 44 |
| Door pocket FR | 44 |
| Door card RR | 56 |
| Door inner carrier RR | 48 |
| Door armrest RR | 44 |
| Inside latch RR | 44 |
| Door pocket RR | 44 |
| Cabin floor | 28 |
| Cargo floor | 12 |
| Cargo wheelhouse trim -1 | 44 |
| Cargo cover ledge -1 | 44 |
| Cargo wheelhouse trim 1 | 44 |
| Cargo cover ledge 1 | 44 |
| Cargo cover | 20 |
| Headliner | 44 |
| Sun visor -0.4 | 44 |
| Sun visor 0.4 | 44 |
| Cab mirror case | 44 |
| Cab mirror pane | 44 |
| Liftgate inner trim | 140 |
| Unibody rail -1 | 52 |
| Unibody rail 1 | 52 |
| Subframe crossmember F-0.22 | 44 |
| Subframe crossmember F0.22 | 44 |
| Subframe side F-1 | 32 |
| Control arm F-1 | 32 |
| Halfshaft F-1 | 20 |
| Strut F-1 | 28 |
| Hub spindle F-1 | 20 |
| Subframe side F1 | 32 |
| Control arm F1 | 32 |
| Halfshaft F1 | 20 |
| Strut F1 | 28 |
| Hub spindle F1 | 20 |
| Subframe crossmember R-0.22 | 44 |
| Subframe crossmember R0.22 | 44 |
| Subframe side R-1 | 32 |
| Control arm R-1 | 32 |
| Halfshaft R-1 | 20 |
| Strut R-1 | 28 |
| Hub spindle R-1 | 20 |
| Subframe side R1 | 32 |
| Control arm R1 | 32 |
| Halfshaft R1 | 20 |
| Strut R1 | 28 |
| Hub spindle R1 | 20 |
| AWD rear differential | 128 |
| AWD propshaft | 44 |
| Transverse engine | 44 |
| Engine cover | 44 |
| Transaxle | 44 |
| Front sump | 44 |
| Radiator | 44 |
| Fuel tank | 44 |
| Tank strap 0.3 | 12 |
| Tank strap 0.76 | 12 |
| Exhaust | 92 |
| Muffler | 44 |
| Exhaust hanger -0.77 | 16 |
| Exhaust hanger 0.55 | 16 |
| Exhaust hanger 1.68 | 16 |
| Exhaust rolled tip | 128 |
| Front crash beam | 44 |
| Rear crash beam | 44 |
| Running guide Headlamp opening-1 | 196 |
| Reflector Headlamp opening-10 | 160 |
| Projector Headlamp opening-10 | 64 |
| LED source Headlamp opening-10 | 48 |
| Reflector Headlamp opening-11 | 160 |
| Projector Headlamp opening-11 | 64 |
| LED source Headlamp opening-11 | 48 |
| Amber side optic Headlamp opening-1 | 44 |
| Running guide Headlamp opening1 | 196 |
| Reflector Headlamp opening10 | 160 |
| Projector Headlamp opening10 | 64 |
| LED source Headlamp opening10 | 48 |
| Reflector Headlamp opening11 | 160 |
| Projector Headlamp opening11 | 64 |
| LED source Headlamp opening11 | 48 |
| Amber side optic Headlamp opening1 | 44 |
| Rear guide Taillamp opening-1 gate | 132 |
| Rear guide Taillamp opening-1 quarter | 100 |
| Rear guide Taillamp opening1 gate | 132 |
| Rear guide Taillamp opening1 quarter | 100 |
| Upper grille opening recessed rib 1 | 44 |
| Upper grille opening recessed rib 2 | 44 |
| Upper grille opening recessed rib 3 | 44 |
| Upper grille opening recessed rib 4 | 44 |
| Upper grille opening recessed rib 5 | 44 |
| Upper grille opening back web 2 | 12 |
| Upper grille opening back web 4 | 12 |
| Upper grille opening back web 6 | 12 |
| Upper grille opening back web 8 | 12 |
| Upper grille opening back web 10 | 12 |
| Lower intake opening recessed rib 1 | 44 |
| Lower intake opening recessed rib 2 | 44 |
| Lower intake opening recessed rib 3 | 44 |
| Lower intake opening recessed rib 4 | 44 |
| Lower intake opening recessed rib 5 | 44 |
| Lower intake opening back web 2 | 12 |
| Lower intake opening back web 4 | 12 |
| Lower intake opening back web 6 | 12 |
| Lower intake opening back web 8 | 12 |
| Lower intake opening back web 10 | 12 |
| Rear ALDER badge | 2 |
| Front badge land | 44 |
| Front ALDER badge | 2 |
| Handle escutcheon FL | 28 |
| Pull handle FL | 44 |
| Handle escutcheon RL | 28 |
| Pull handle RL | 44 |
| Window seal FrontL | 128 |
| Window belt FrontL | 36 |
| Window seal RearL | 128 |
| Window belt RearL | 36 |
| Window seal QuarterL | 128 |
| Window belt QuarterL | 36 |
| Rail end cap L0 | 44 |
| Rail end cap L1 | 44 |
| Handle escutcheon FR | 28 |
| Pull handle FR | 44 |
| Handle escutcheon RR | 28 |
| Pull handle RR | 44 |
| Window seal FrontR | 128 |
| Window belt FrontR | 36 |
| Window seal RearR | 128 |
| Window belt RearR | 36 |
| Window seal QuarterR | 128 |
| Window belt QuarterR | 36 |
| Rail end cap R0 | 44 |
| Rail end cap R1 | 44 |
| Fuel filler cup | 60 |
| Fuel flap | 28 |
| Fuel filler cap | 24 |
| Rear plate | 12 |
| Rear plate face | 2 |
| X220 AWD model badge | 2 |
| Front wiper blade 0 | 36 |
| Front wiper arm 0 | 12 |
| Washer nozzle 0 | 44 |
| Front wiper blade 1 | 36 |
| Front wiper arm 1 | 12 |
| Washer nozzle 1 | 44 |
| Rear wiper blade | 28 |
| Rear wiper arm | 12 |
| Shark fin antenna | 92 |
| Door hinge FL0.73 pin | 24 |
| Door hinge FL0.73 sleeve | 48 |
| Door hinge FL0.73 fixed bracket | 8 |
| Door hinge FL0.73 door leaf | 28 |
| Door hinge FL1.04 pin | 24 |
| Door hinge FL1.04 sleeve | 48 |
| Door hinge FL1.04 fixed bracket | 8 |
| Door hinge FL1.04 door leaf | 28 |
| Door hinge RL0.63 pin | 24 |
| Door hinge RL0.63 sleeve | 48 |
| Door hinge RL0.63 fixed bracket | 8 |
| Door hinge RL0.63 door leaf | 28 |
| Door hinge RL1.01 pin | 24 |
| Door hinge RL1.01 sleeve | 48 |
| Door hinge RL1.01 fixed bracket | 8 |
| Door hinge RL1.01 door leaf | 28 |
| Door hinge FR0.73 pin | 24 |
| Door hinge FR0.73 sleeve | 48 |
| Door hinge FR0.73 fixed bracket | 8 |
| Door hinge FR0.73 door leaf | 28 |
| Door hinge FR1.04 pin | 24 |
| Door hinge FR1.04 sleeve | 48 |
| Door hinge FR1.04 fixed bracket | 8 |
| Door hinge FR1.04 door leaf | 28 |
| Door hinge RR0.63 pin | 24 |
| Door hinge RR0.63 sleeve | 48 |
| Door hinge RR0.63 fixed bracket | 8 |
| Door hinge RR0.63 door leaf | 28 |
| Door hinge RR1.01 pin | 24 |
| Door hinge RR1.01 sleeve | 48 |
| Door hinge RR1.01 fixed bracket | 8 |
| Door hinge RR1.01 door leaf | 28 |
| Roof fixed | 314 |
| Gate upper header | 208 |
| Hood hinge -1 | 12 |
| Liftgate hinge -1 | 12 |
| Hood strut -1 barrel | 64 |
| Hood strut -1 rod | 32 |
| Hood strut -1 body ball seat | 44 |
| Hood strut -1 gate ball seat | 44 |
| Hood strut body return -1 | 8 |
| Gate strut -1 barrel | 64 |
| Gate strut -1 rod | 32 |
| Gate strut -1 body ball seat | 44 |
| Gate strut -1 gate ball seat | 44 |
| Gate strut body return -1 | 12 |
| Hood hinge 1 | 12 |
| Liftgate hinge 1 | 12 |
| Hood strut 1 barrel | 64 |
| Hood strut 1 rod | 32 |
| Hood strut 1 body ball seat | 44 |
| Hood strut 1 gate ball seat | 44 |
| Hood strut body return 1 | 8 |
| Gate strut 1 barrel | 64 |
| Gate strut 1 rod | 32 |
| Gate strut 1 body ball seat | 44 |
| Gate strut 1 gate ball seat | 44 |
| Gate strut body return 1 | 12 |
| Greenhouse_L A return | 345 |
| Greenhouse_L front sash | 270 |
| Greenhouse_L rear sash | 130 |
| Greenhouse_L quarter | 144 |
| Window surround_L A return | 38 |
| Window surround_L front sash | 148 |
| Window surround_L quarter | 88 |
| B applique_L front door | 60 |
| B applique_L rear door | 92 |
| C divider_L door | 92 |
| C divider_L quarter | 80 |
| Greenhouse_L gate header fixed base | 65 |
| Greenhouse_L gate header moving top | 176 |
| Arch cladding_FL fender | 342 |
| Arch cladding_FL door | 128 |
| Arch cladding_RL door | 220 |
| Arch cladding_RL quarter | 236 |
| Arch flange_FL fender | 172 |
| Arch flange_FL door | 52 |
| Arch flange_RL door | 108 |
| Arch flange_RL quarter | 116 |
| Rear quarter_L lower | 1773 |
| Rear quarter_L upper aft gate return | 156 |
| Rear quarter_L upper aft fixed side | 26 |
| Greenhouse_R A return | 345 |
| Greenhouse_R front sash | 278 |
| Greenhouse_R rear sash | 122 |
| Greenhouse_R quarter | 141 |
| Window surround_R A return | 38 |
| Window surround_R front sash | 140 |
| Window surround_R quarter | 88 |
| B applique_R front door | 56 |
| B applique_R rear door | 100 |
| C divider_R door | 96 |
| C divider_R quarter | 85 |
| Greenhouse_R gate header fixed base | 65 |
| Greenhouse_R gate header moving top | 178 |
| Arch cladding_FR fender | 342 |
| Arch cladding_FR door | 128 |
| Arch cladding_RR door | 220 |
| Arch cladding_RR quarter | 236 |
| Arch flange_FR fender | 172 |
| Arch flange_FR door | 52 |
| Arch flange_RR door | 108 |
| Arch flange_RR quarter | 116 |
| Rear quarter_R lower | 1689 |
| Rear quarter_R upper aft gate return | 160 |
| Rear quarter_R upper aft fixed side | 30 |

</details>

## Build and evidence

```sh
make -C cars BODY=suv WIDTH=1600 SAMPLES=48
make -C cars BODY=suv check
make -C cars BODY=suv check-detail-repeat
make -C cars BODY=suv check-repeat
```

`make` builds form and detail source densities, original markings, camera fits,
solid/scale/budget/construction audits, full sampled sweeps and checkpoint images.
All Cycles work uses the kit GPU lock. `make refs` fetches registered image/PDF
references only. No UV/bake/export is invoked by `BODY=suv` at this checkpoint.

Reports are in `build/suv/` and `build/suv-detail/`: form-check, curvature,
game/high audit, game/high construction, motion-game/high, repeat-check,
used-cameras and pickup-preservation. `renders/suv-detail/` holds the source
hashes/recipes, tone masks, tonal-ranges, pair-measurements and checkpoint report.
The repeat check compares independent positions, polygons, corner normals,
matrices, parents and material names; binary Blend identity is not expected.
Final game/high Blend build products are 2,769,427 / 6,097,867 bytes; they are
ignored and are not delivery-file budgets. The preserved pickup GLB is 11,530,740 bytes with SHA256
`ec70cde87fbe50fb814cc14c900ee324e254711b5bfa5d3735aef166b146de5b`.

## Photo comparison and remaining weaknesses

Used-photo front and rear camera RMS errors are approximately 12.66 and 6.39
pixels at native widths 5265 and 4809. Wheel/hub/contact anchors plus a disclosed
1.50 ±0.20 m height prior constrain the cameras; lenses are solved estimates,
not EXIF. The rear also uses a weighted far-wheel contact. Photos never enter
the geometry or material graphs.

Balance the front on the lower-left asphalt and the rear on the unprinted white
parking-sign patch. The front neutral is aged pavement, not a calibrated gray
card. Recorded linear RGB gains are front .883/.991/1.165 and rear
1.017/1.017/.967. Measurements are display values under different reflection
environments, not albedo measurements. The front six-year vehicle is explicitly
an older wear cross-check; the rear is five years old.

| Balanced comparison patch | Render luma | Photo luma |
| --- | ---: | ---: |
| Front mid-door | 82.1 | 88.1 |
| Front low door | 77.1 | 76.6 |
| Rear mid-door | 139.2 | 135.3 |
| Rear quarter | 146.4 | 152.6 |
| Front cladding | 32.7 | 37.4 |
| Rear cladding | 39.9 | 27.4 |

Final measured patch values and the final image critique are recorded in
[REVIEW.md](REVIEW.md); the JSON files preserve exact picks and values. Remaining
risks include the small cut-border curvature noise, idealized procedural roadside
reflections, less irregular wheels/tires and low-detail cabin/underbody. The
reference rear cladding is darker, and the front glass reflection is brighter,
than the source comparison. No claim of a finished photoreal delivery or baked
material equivalence follows from the source checks.

## Interrupted session audit

Kept the useful SUV-specific decomposition, exterior/cabin/underbody scaffold,
family shader reuse and proposed reference sources. Finished or replaced the
unproven portions: wrong-side rear camera and wheel picks, unstable glass normal
transfer, floor/card intrusion, unsupported fixtures, unmeasured hinge clearances,
self-intersecting early hinge leaves, impossible strut stroke, and surplus source
geometry. `main` was merged first (already up to date). The source and render
pipelines remain in `suv_*.py`; no kit feature or pickup export was changed.

<details>
<summary>Historical accepted form-round-three measurements (superseded budgets/stage)</summary>

# Alder X220 — form round 3

Original compact crossover generated by scripts in Blender 5.2. This checkpoint
fairs the parent surface, cuts a planar plate recess, strengthens the side lines,
and rebuilds the mirror shells and molded spoiler. The accepted package, face,
lamp language, door-mounted mirrors and low rails remain. It stops before the
interior, underbody, finishing detail, UVs, baking and SUV export.
[Reference comparisons](REFERENCE.md), [credits](refs/SOURCES.md) and
[regional critiques](REVIEW.md) accompany the measurements below.

## Accepted package, measured again

| Quantity | Actual game source |
| --- | ---: |
| Length / body width | 4598.8 / 1842.0 mm |
| Roof / rails | 1679.0 / 1700.0 mm |
| Wheelbase / front and rear tracks | 2690.0 / 1600.0 and 1610.0 mm |
| Width across mirrors | 2117.0 mm |
| Windshield / backlight rake from vertical | 58.19 / 30.73° |
| Backlight top / base width; height | 1158.8 / 1394.7; 301.4 mm |
| Approach / departure | 17.88 / 20.63° |
| Tire package | 225/65R17; nominal diameter 724.3 mm |

Sources are the [2020 Toyota US brochure](https://cdn.dealereprocess.org/cdn/brochures/toyota/2020-rav4.pdf),
[2020 Honda US specifications](https://hondanews.com/en-US/honda-automobiles/releases/release-47ef5ef525f391ae783334075a01030f-2020-cr-v-specifications-features)
and [Honda UK brochure](https://www.kingswood-honda.com/wp-content/uploads/2019/01/CR-V_Brochure.pdf).
Toyota publishes 19/21° approach/departure; Honda LX FWD 18.1/25.3°.
The revised front follows Honda's approximately 18° approach, and the rear
follows Toyota's approximately 21° departure. These are static outer-form
measurements, not suspension, loaded clearance or underbody certification.
The future underbody target remains 205 mm. The roof is not the antenna height.

## Causes and corrections

The baseline game mesh and an independently rebuilt **uncut round-two parent**
were compared before editing. The dents were already in that parent. Cutting
and low-resolution sampling added smaller local error; changing normals alone
could not repair the source shape.

| Region | Cause found | Correction |
| --- | --- | --- |
| Plate surround | A 22 mm displacement field pushed a broad recess into the parent | Delete the displacement; retain one convex gate, cut only the mouth, construct a planar bed and sharp return |
| Hood front corners | A narrow 26 mm fender crown collided with the leading roll and draw banks | Broaden and reduce the local crown, fair the leading roll, fade the two draw banks before the nose |
| D-pillar base / rear quarter | Abrupt plan-power transitions and bunched control quads at the folded chart transition | Smooth the height-dependent plan blend; use one radial projection center and tangentially relax control spacing before subdivision |
| Rear bumper corner | Lower-door die hollow and lean transition continued around the bumper; corner-reaching bumper crease compounded it | Terminate the die feature into the rear arch; use a simple progressive bumper section and fade the central crease before the corner |
| Mirror facets | Irregular polygon loft and reduction left long fans on a curved housing | Replace with evenly distributed rounded sections, 48 samples around and 12 along the nose, without QEM collapse |

The control cage remains one connected quad sheet; the relaxation acts on its
control vertices **before** Catmull–Clark evaluation. It does not fit evaluated
vertices or soften the game mesh to conceal defects. Early smoothing-only trials
were rejected: they did not remove the bumper's repeated reflection teeth.

The parent diagnostic found 1,247 radially reversed triangles in round two.
The revised parent has two tiny radially reversed triangles at the concealed
lower rear return, Z314 mm, each approximately 0.075 mm². None is in the four
reviewed exposed regions; both generated source densities pass the solid audit.
This is a radial orientation diagnostic, not a complete self-intersection test.
No claim of a globally perfect parent follows from that count.

Independent game-to-parent rays retain all samples and aperture exclusions in
`build/suv-round3/diagnosis.json`. At the gate, rear bumper and D-pillar, the
95th-percentile shading-normal mismatch falls respectively from 3.58 / 2.67 /
2.86° to **0.51 / 0.36 / 0.54°**. Corresponding positional errors are now
**1.12 / 0.64 / 2.17 mm**. The hood corner remains the least uniform sampled
region: 95th-percentile error **2.72 mm / 3.48°**. These numbers measure sampling
agreement; the stripes and curvature maps judge the shape itself.

## Gate, hood and spoiler

The gate is one convex cross-car surface. At Z770 / 810 / 1035 mm its center
stands **24.4 / 28.5 / 45.6 mm** behind the X600 mm samples. Its upper panel
turns inward below the lamps; a separate broad garnish follows that plan over
the plate. The garnish is **1201 × 44 mm** in rear projection, with a flat lower
return and an unmarked badge land above. Its 60 mm total fore-aft extent includes
the gate's curvature; that number is not its stand-off from the panel.

The accepted **320 × 170 × 25 mm nominal pocket** now has a planar bottom.
Forty-nine actual bed ray hits fit a plane with maximum residual **0.0002 mm**.
The actual cut rim including assembly clearance is **323 × 176 mm**. Perpendicular
rim-to-bed depths are **20.8–24.9 mm**, because a flat bed meets a convex/sloping
mouth. The 25 mm design setting is not reported as a uniform measured depth.
The old optical-guide depth rays start 4 mm proud of the skin; they remain labeled
as guide measurements in the raw report and are superseded here by actual shared
skin/rim vertices. No surrounding vertices are displaced to make the recess.
The supported plate lamp remains above it.

Two raised hood draw banks carry back toward the cowl and fade before the lamp
corners. Actual center-to-X600 mm drops are **34.1 / 30.1 / 17.9 mm** at
Y−2000 / −1700 / −1400 mm. Both reflection directions show the raised center and
fairer outer roll. This is not a flat lid with a separate ridge pasted on.

The spoiler is a closed molded section continuing the roof, **1510 mm** wide.
At the aft chord, 20 mm ahead of its trailing extremity, measured main-section
thickness is **65–76 mm**. Outboard return sections are intentionally thicker;
the end drops are **159–191 mm** beside the upper backlight corners. The underside
curves forward into the gate/roof seat. Twenty-nine measured root samples sit
**5.4–8.0 mm inside** the roof surface, so it has a supported closed root rather
than an open slot. The integrated third-lamp blank remains in the aft face.
The part group costs **1710 triangles**, including the lamp. Low rails retain
39–47 mm local stand-off and their 1700 mm absolute maximum.

## Side lines and mirrors

| Actual side station | Shoulder height | Shoulder normal turn / vertical span | Shoulder 10–90% transition width | Lower normal turn / vertical span | Lower 10–90% width |
| --- | ---: | ---: | ---: | ---: | ---: |
| Y-390 mm | 1038 mm | 16.09° / 30 mm | 31.0 mm | 9.04° / 80 mm | 43.5 mm |
| Y+215 mm | 1052 mm | 16.29° / 30 mm | 30.5 mm | 9.19° / 80 mm | 40.0 mm |
| Y+720 mm | 1062 mm | 16.06° / 30 mm | 30.5 mm | 9.49° / 80 mm | 37.0 mm |

Normal turns use independently interpolated actual game corner normals, not
prescribed section slopes. Full raw ray profiles are in `form-check.json`.
The shoulder crosses the fenders and doors from the front lamp to the rear lamp;
its close-spaced reflection bands and narrow curvature strip are continuous.
The lower crease rises from **561 to 587 mm**, with a **2.05–2.10 mm** hollow over
a 50 mm chord. Fender swells at Z900 mm remain **32.3 mm front / 29.6 mm rear**
beyond the door. The low sun runs along the body; the lower break and rear swell
read more strongly than the front swell in that one view. Upper side lean remains
15.9–16.4°, initial lower lean 4.3°, low-door lean 15.6–16.0°.

Each mirror housing remains **260 mm outboard × 160 mm high × 130 mm deep**,
centered at **X±928.5 / Y−649 / Z1215 mm**, bottom **1135 mm**. The upper-door
sail starts at Y−890 mm behind the A-foot. The rear glass is planar; the nose,
cap and outboard end are rounded. Each shell is **1246 triangles**; both complete
assemblies total **2716**. The overall span remains 2117 mm and the side view
places no mirror bump on the hood/cowl silhouette.

## Accepted ends and overlays

| Measured feature | Round-three game source | Toyota / Honda reference estimate |
| --- | ---: | ---: |
| Front setback at X800 mm | 254.7 mm | 271 / 258 mm |
| Rear setback at X800 mm | 213.6 mm | 252 / 197 mm |
| Headlamp / rear lamp maximum height | 157.3 / 182.9 mm | 161 / 167 front; 178 / 197 rear |
| Grille depth | 65.7–67.1 mm | Brief: 40–80 mm |
| Lamp–grille mouth gap | 18.4 mm | No broad painted separator |
| Front black center height / share | 331 mm / 34.5% | 391 / 303 mm; 43.4 / 37.2% |
| Front black height at X700 mm | 152 mm | Descending painted corners |
| Rear lip, center through X700 mm | 223–248 mm | Main lower lip 229 / 233 mm |

The sparse rescue-plan picks are independently scaled from the cited envelopes:
[Toyota RAV4 sheet](https://global.toyota/pages/global_toyota/your-vehicle/RAV4_50_1.pdf),
[Honda RW sheet](https://w3.techinfo.honda-eu.com/sites/default/files/2023-11/cr-v_rw-_en.pdf).
Allow approximately ±20 mm plan / ±30 mm photographic feature-height uncertainty.
The rear follows Honda's fuller gate plan; Toyota sets its corners farther back.
The lower-lip reference figures exclude the extra black band above the lip.

All original cameras are unchanged. Four chassis camera RMS values remain
7.19 / 8.91 / 8.40 / 9.99 native pixels. Those checks prove camera projection,
not surface correspondence. The perspective overlay picks have approximately
±15.5 mm selection uncertainty before trim and camera uncertainty. Both raw
fixed-axis and nearest-silhouette residuals are retained.

| Perspective holdout region | RAV4 nearest miss | CR-V nearest miss |
| --- | ---: | ---: |
| Hood / cowl | 16 mm | 56 mm |
| Header / main roof | 22 mm | 13 mm |
| Upper/front bumper | 42 mm | 34 mm |
| Front lower chin | 7 mm | 2 mm |
| Upper tail | 16 mm | 38 mm |
| Rear bumper | 33 mm | 40 mm |
| Lower rear | 18 mm | 29 mm |
| Spoiler | 24 mm | 22 mm |
| D-pillar | 23 mm | 106 mm |

The lower bumper holdouts remain within approximately 40 mm of both makes.
The spoiler now falls within 25 mm of both sparse picks. The upper front bumper
still misses Toyota by 42 mm, and the accepted Honda cowl / D-pillar differences
remain 56 / 106 mm. The Honda D-pillar fixed-column vertical residual is 231 mm;
the nearest-silhouette distance is reported separately, not substituted silently.
This is not a whole-outline 40 mm match.

## Triangles and finishing allocation

**61,374 game triangles, 142 meshes / 155 objects, five diagnostic materials,
zero image textures.** The increase from round two is 1732 triangles. This pays
for the molded spoiler, smooth mirror shells and fair surface samples.
The source counts are not shipping draw calls; final consolidation remains later.
No SUV GLB exists at this gate.

| Part group | Actual triangles |
| --- | ---: |
| Pillars / upper frame | 1,932 |
| Four painted door skins | 3,546 |
| Hood, roof, gate, fenders, quarters | 14,592 |
| Painted fascias | 7,524 |
| Glazing | 2,728 |
| Arch, door and bumper moldings / skid finish | 9,880 |
| Wheelwell liners and closures | 1,168 |
| Optics, cases, grille, wells, garnish and badge | 6,614 |
| Temporary cavity closure | 12 |
| Mirror shells, panes and sails | 2,716 |
| Rails and feet | 744 |
| Spoiler and brake lamp | 1,710 |
| Four tires | 4,224 |
| Four wheel proxies | 3,984 |
| **Total** | **61,374** |

The actual concealed-gauge reduction already removes **2262 triangles** from the
current raw shells, including **1514** from the new local reduction. Each accepted
patch retains the complete exterior triangle soup exactly and passes closed-edge
and inside-surface probes. Rejected proposals restore their original geometry.
These achieved savings are already included in 61,374; they are not counted twice
in the following **future** allocation.

| Finishing allocation | Triangles |
| --- | ---: |
| Current clay | 61,374 |
| Further concealed fascia/gauge and optical cassette backs | −3,000 target |
| Flat glazing/inboard panels and redundant cage samples | −1,500 target |
| Tire cross-sections and concealed wheel backs | −1,000 target |
| Cabin: seats, dash, cards and floor | +5,000 ceiling |
| Underbody / running gear | +2,500 ceiling |
| Optics, seals, handles, wipers and brake detail | +1,500 ceiling |
| **Planned finished total / reserve below 65k** | **64,874 / 126** |

The former 64,142 plan allowed 10,000 triangles of additions. This revision
allows 9000, assigning more detail to the normal map, to fund the form fixes.
The 5500 future savings remain an implementation requirement, not an achieved
result. There is only 3626 spare capacity at the present count; adding the whole
finishing allocation without those reductions would fail. The final texture
target remains one 2048 BaseColor / Normal / ORM set, approximately 16 MiB with
block compression and mipmaps.

<details><summary>Actual triangles for every current mesh</summary>

| Mesh | Triangles |
| --- | ---: |
| Arch cladding_FL | 396 |
| Arch cladding_FR | 396 |
| Arch cladding_RL | 396 |
| Arch cladding_RR | 396 |
| Arch flange_FL | 196 |
| Arch flange_FR | 196 |
| Arch flange_RL | 196 |
| Arch flange_RR | 196 |
| B applique_L | 98 |
| B applique_R | 68 |
| Backlight | 528 |
| C divider_L | 68 |
| C divider_R | 64 |
| Cast spoke_FL_0 | 62 |
| Cast spoke_FL_1 | 62 |
| Cast spoke_FL_2 | 62 |
| Cast spoke_FL_3 | 62 |
| Cast spoke_FL_4 | 62 |
| Cast spoke_FL_5 | 62 |
| Cast spoke_FR_0 | 62 |
| Cast spoke_FR_1 | 62 |
| Cast spoke_FR_2 | 62 |
| Cast spoke_FR_3 | 62 |
| Cast spoke_FR_4 | 62 |
| Cast spoke_FR_5 | 62 |
| Cast spoke_RL_0 | 62 |
| Cast spoke_RL_1 | 62 |
| Cast spoke_RL_2 | 62 |
| Cast spoke_RL_3 | 62 |
| Cast spoke_RL_4 | 62 |
| Cast spoke_RL_5 | 62 |
| Cast spoke_RR_0 | 62 |
| Cast spoke_RR_1 | 62 |
| Cast spoke_RR_2 | 62 |
| Cast spoke_RR_3 | 62 |
| Cast spoke_RR_4 | 62 |
| Cast spoke_RR_5 | 62 |
| Chin skid finish | 268 |
| Corner pocket L opening | 40 |
| Corner pocket L opening molded return | 160 |
| Corner pocket R opening | 40 |
| Corner pocket R opening molded return | 160 |
| Door F_L | 980 |
| Door F_R | 978 |
| Door R_L | 792 |
| Door R_R | 796 |
| Exhaust cutout opening | 40 |
| Exhaust cutout opening molded return | 160 |
| Form cavity closure | 12 |
| Front fender_L | 1,908 |
| Front fender_R | 1,948 |
| Front lower bumper cladding | 1,672 |
| Front molded fascia | 4,362 |
| Front side glazing_L | 256 |
| Front side glazing_R | 256 |
| Greenhouse_L | 820 |
| Greenhouse_R | 814 |
| Grille folded surround | 512 |
| Headlamp opening-1 | 296 |
| Headlamp opening-1 optical cassette | 472 |
| Headlamp opening1 | 296 |
| Headlamp opening1 optical cassette | 472 |
| Hood outer | 1,042 |
| Liftgate badge mounting land | 76 |
| Liftgate outer | 2,844 |
| Liftgate sculpted garnish | 196 |
| Liftgate spoiler | 1,514 |
| Lower door cladding_FL | 172 |
| Lower door cladding_FR | 172 |
| Lower door cladding_RL | 200 |
| Lower door cladding_RR | 200 |
| Lower intake opening | 108 |
| Lower intake opening blade 1 | 52 |
| Lower intake opening blade 2 | 52 |
| Lower intake opening blade 3 | 52 |
| Lower intake opening molded return | 256 |
| Mirror housing_L | 1,246 |
| Mirror housing_R | 1,246 |
| Mirror pane_L | 92 |
| Mirror pane_R | 92 |
| Mirror sail_L | 20 |
| Mirror sail_R | 20 |
| Plate lamp | 108 |
| Plate pocket opening | 134 |
| Plate pocket opening molded return | 160 |
| Quarter side glazing_L | 256 |
| Quarter side glazing_R | 256 |
| Rail foot_L0 | 52 |
| Rail foot_L1 | 52 |
| Rail foot_R0 | 52 |
| Rail foot_R1 | 52 |
| Rear lower bumper cladding | 4,560 |
| Rear molded fascia | 3,162 |
| Rear quarter_L | 2,862 |
| Rear quarter_R | 2,860 |
| Rear side glazing_L | 256 |
| Rear side glazing_R | 256 |
| Rear skid finish | 268 |
| Reflector L opening | 40 |
| Reflector L opening molded return | 160 |
| Reflector R opening | 40 |
| Reflector R opening molded return | 160 |
| Roof | 568 |
| Roof rail_L | 268 |
| Roof rail_R | 268 |
| Spoiler brake lamp | 196 |
| Taillamp opening-1 gate | 200 |
| Taillamp opening-1 gate optical cassette | 320 |
| Taillamp opening-1 quarter | 152 |
| Taillamp opening-1 quarter optical cassette | 264 |
| Taillamp opening1 gate | 200 |
| Taillamp opening1 gate optical cassette | 320 |
| Taillamp opening1 quarter | 152 |
| Taillamp opening1 quarter optical cassette | 264 |
| Tire_FL | 1,056 |
| Tire_FR | 1,056 |
| Tire_RL | 1,056 |
| Tire_RR | 1,056 |
| Upper grille opening | 88 |
| Upper grille opening blade 1 | 52 |
| Upper grille opening blade 2 | 52 |
| Upper grille opening blade 3 | 52 |
| Upper grille opening molded return | 256 |
| Wheel barrel_FL | 480 |
| Wheel barrel_FR | 480 |
| Wheel barrel_RL | 480 |
| Wheel barrel_RR | 480 |
| Wheel center_FL | 144 |
| Wheel center_FR | 144 |
| Wheel center_RL | 144 |
| Wheel center_RR | 144 |
| Wheelwell inboard_FL | 96 |
| Wheelwell inboard_FR | 96 |
| Wheelwell inboard_RL | 96 |
| Wheelwell inboard_RR | 96 |
| Wheelwell_FL | 196 |
| Wheelwell_FR | 196 |
| Wheelwell_RL | 196 |
| Wheelwell_RR | 196 |
| Window surround_L | 280 |
| Window surround_R | 280 |
| Windshield | 664 |

</details>

Door pivots remain local Z (left 0–72°, right −72–0°), hood local X −65–0°,
gate local X 0–75°, wheels local X ±360°, front steering ±35°. These are authored
groupings, not successful mechanical sweeps. Attachments, seals and articulation
clearance remain later work.

## Rebuild and proof

```sh
make -C cars BODY=suv WIDTH=1600 SAMPLES=40
make -C cars BODY=suv check
make -C cars BODY=suv check-repeat
```

`BODY=pickup` remains the default. The isolated SUV pipeline rebuilds both source
densities, runs dimensional and topology audits, verifies six calibrated cameras,
renders through the shared GPU lock and composes the review. No kit or shared
family generator changed this round. No downloaded model, texture or executable
was used.

Current evidence is `renders/suv-round3/`: **34 source renders** comprising the
same 24 cameras/modes as round two plus five geometric mean-curvature maps and
five matching stripe views. `round3-curvature-*.jpg` puts those five pairs beside
each other with a common color scale. `round2-round3-ends-raking.jpg`, both
`round2-round3-*-rear.jpg` pages, and `round3-raking-measured.jpg` expose the old/new
changes. Both makes have calibrated clay and striped photo pairs. The full
`contact.jpg` also includes dimensions, side sections, reference picks, overlays
and independent sectional-curvature plots. Round two remains in `renders/suv-round2/`.
No checkpoint image or rebuild artifact is committed.

The new map computes signed mean **H=(k1+k2)/2**, convex positive, from the actual
game triangles with cotangent weights and mixed Voronoi areas. It uses no authored
normal field, smoothing or parent substitution. Only open boundary vertices are
gray; unmeasured parts are dark. All five views share nonlinear scale anchors
−20, −5, −1, 0, +1, +5, +20 per meter. This exposes triangulation noise near cuts
as well as physical curvature, so speckles are evidence to inspect, not automatic
dents. Plane, radius-2 sphere and cylinder analytic checks pass. Method citation
and use are in `refs/SOURCES.md`.

The older eleven-section normal-derivative checks retain every raw reversal.
Feature attribution now includes the actual ±3-sample stencil support, and names
the continuous waist-to-upper-plan transition at the rear. These are limited
section checks, not a global fairness certificate; the unsmoothed whole-mesh maps
remain alongside them.

The full SUV `make`, `make check` and `make check-repeat` recipes pass.
Both game/high source audits pass with zero errors and warnings. Both eleven-section
reports pass their documented feature zones, all six camera implementations pass
projection checks, and the repository check passes. The independent repeat matches
**155 objects / 142 meshes** exactly: positions, polygons, corner normals,
transforms, parents and material names. This proves determinism, not appearance.

Game source: **1,448,654 bytes / 61,374 triangles**. High source: **2,929,100 bytes /
130,086 triangles**. The 34 render metadata records identify game SHA-256
`a9e45a08f7edbf2ea086e4284c6f08c00bae38008ae9394614855bf833cdcb4a`;
curvature views additionally record their separate diagnostic-scene hash.
Hero foreground p99 is approximately **231 / 219**, without clipped channels.
Raking foreground median/p99 is approximately **39 / 199**. No final paint,
texture, UV, motion or GLB validation is implied by those source values.

Logs are in the clone's `build/suv-round3/`: `final-all.log`, `final-check-verified.log`,
`final-render.log`, `final-repeat.log`, `diagnosis.json` and
`analytic-curvature.log`. The latter's maximum sphere error is 0.0000753 per
meter; cylinder error is below 2e-14 and the plane is exact.

The pickup delivery remains byte-identical to the accepted round-two export:
**11,530,740 bytes**, SHA-256
`ec70cde87fbe50fb814cc14c900ee324e254711b5bfa5d3735aef166b146de5b`.
`build/suv/pickup-round3-preservation.json` records this existing-delivery comparison;
it is not a claim of a new pickup bake. Its 150 accessor arrays and embedded data
are therefore unchanged.

## Remaining weaknesses

The broad gate dents and rear-corner reflection teeth are removed. Small cut-edge
reflection disturbances and geometric-curvature noise remain, especially around
the end-corner triangulation and front arch. The mirrors are smoother but a little
oval; the spoiler end caps meet the pillars abruptly. The garnish is still more
generic than Honda’s, and untrimmed window edges, opaque optical blanks and wheel
proxies keep the car looking unfinished. The accepted Honda D-pillar/cowl mismatch
remains. These are form-review limitations, not a finished-asset claim.

</details>
