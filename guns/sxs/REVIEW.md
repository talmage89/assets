# Covey 26 — form round 5: head behind the fences

The round-four record below is retained as history. Round five keeps its
57.350 mm crowns, 51.900 mm pair width, front R13.35 arcs, 18.5 mm crown roll,
side flats and lower plate construction. The new head is being judged in
sections 3, 8 and 15 mm behind Y115 and in both bore-axis vertical planes.
Inspection material values remain unchanged; no finish work or docs JPGs.

The owner has now specified **Z55.59 mm** for the center fill. This
supersedes the former Z49.72 mm central outline; it does not preserve that
notch. The standing face now reaches the actual rib floor between the
R13.35 front arcs. The uninterrupted center surface runs level back to the
lever recess, whose R5.90 fore wall fits the original R5.60 boss. The 0–25°
lever range and all 19 clip keys remain unchanged.

## Round 5 image critique passes

25. **First Z49.72 / R6 / 3 mm join trial.** Color/value: inspected the dark
    steel and broad reflections before assessing the form; the original black
    macro backdrop has no defensible neutral, so unity white balance remains.
    The first source previews (`renders/round5/pass1`) remove the 40.64 mm
    section's two original roof facets. The 49.72 mm center datum fills the
    head behind the R13.35 front arcs, but the 3 mm join band still produces
    too narrow a reflection transition. A topology check rejects 24 boundary
    edges around the unchanged Y115 bushing cuts. These previews are rejected
    source diagnostics, not the baked delivery.
26. **6 mm signed-distance join and Y115 topology.** Color/value: the second
    preview set (`renders/round5/pass2`) retains dark steel and visible cavity
    shadows. The 6 mm join band reduces the rear reflection break, but a height
    maximum truncated at a circular patch's end still gives a derivative
    discontinuity. Replaced it with the zero of a C2 signed-distance union;
    there is no separate fence mesh. Resolved sub-0.8 mm collinear T-junctions
    on the Y115 plane by splitting the existing edges at their third vertices.
    The subsequent head source and game mesh have zero nonmanifold edges.
27. **Lever clearance and actual centerline datums.** Color/value: viewed the
    third source set (`renders/round5/pass3`), including aimed, open, breech and
    both upper rakes. The raised stock trial leaves an unnecessarily exposed
    lever cutout in the wood. Restore the accepted wood's previous head cage;
    only the action receives the 0.35 mm allowance for the original 0–25° lever
    sweep. Its first motion test identifies the stock/lever collision instead
    of adding a contact exception. Independent surface rays distinguish the
    action's 49.72 mm notch from the actual rib sighting floor, 55.59 mm, and
    the accepted boss's 50.30 mm top. Datum clarification is pending before
    choosing the delivered center fill; neither a constant nor a source
    preview constitutes acceptance of that requirement.

28. **Restored wood and measured sections.** Color/value: opened the new
    `renders/round5/datum49` and `datum55` player previews. Both retain the
    original material constants. The 49.72 mm trial retains the front notch;
    the 55.59 mm trial fills to the actual rib surface but raises its center
    outline and leaves the 50.30 mm boss in a deeper recess. Those are distinct
    outcomes, so the pending datum choice cannot be hidden by camera placement.
    Opened the Y112/Y107/Y100 and both bore-axis section drawings. The sampled
    49.72 mm head gives drops 7.63 mm just behind either return, 13.07 mm at
    either side wood line and 11.20 mm at the center wood line. Its side-return
    circle fit is R5.994 mm. The sampled bore-axis transition fits are about
    R19.4 mm rather than the initial 4–8 mm photo inference; they are not
    claimed to match that estimate. The current quick source check passes
    246 contact records and manifold topology at 38,822 triangles. The latest
    opening sweep has zero motion violations; final full source/reimport
    sweeps and the new bake are still pending the center datum choice.

29. **Z55.59 center and degree-5 rear return, both source rakes.**
    Color/value: opened both full-resolution source rakes and the top/aimed
    previews in `renders/round5/final-source`; the accepted constant steel
    remains dark, and the black-backdrop macro remains at unity balance.
    The previous signed-distance field produced small secondary folds near
    the outer returns. Replaced its rear portion with a monotone degree-5
    height excess, ending with zero height, slope and curvature; the rear
    endpoint shifts 0.68 mm per transverse mm inward. In these images the
    R6 side returns carry broad reflections from either lighting side,
    without the former wrinkles. The center fill now joins the rib at
    Z55.59 and the aimed image retains the bead. The recess lip trial is
    rejected for microscopic topology folds: a modifier bevel is replaced
    by a measured-roof-tangent circular R0.60 cutter, tapered over Y88–92.
    This is still source evidence. Baked image acceptance follows below.


# Covey 26 — form round 4: fences, flats and underside

This round judges the **baked 2048 export**, `export/sxs.glb`. The kit finalizer,
4096 GPU bake, downsampler and animated exporter supply one BaseColor / OpenGL
Normal / ORM set. The colors and roughness remain the accepted inspection
constants: finishes, grain, checkering, markings and used wear are still held.
A normal bake does not constitute finish acceptance. No docs JPGs are added.

## Current region review

- **Fences.** Replaced the oversized spheres with circular transverse sections
  continuing the measured bore axes backward, and a short longitudinal roll
  into the existing shoulder/strap. Each crown meets the tube top line; the
  pair fits inside the joined breech width. The rear boundary curves inward
  toward the strap in the top view. The photograph has a subtler, hand-finished
  shoulder junction and a differently shaped rib extension; ours retains the
  original plainer shoulders. See the [right pair](renders/checkpoint/pairs/action-pair.jpg),
  [top pair](renders/checkpoint/pairs/action_top-pair.jpg),
  [top rake](renders/checkpoint/beauty/action_rake_top.png), and fence sections.
- **Side and knuckle.** One ground side plane now continues from head to bar.
  The rounded lower edge sweeps upward into the original hinge axis, and the
  pin end is a thin flush circle in the same blued inspection steel. The
  photograph's shallow decorative panel line is not a geometric step and has
  not been copied. Our plain lower neck is broader through its flat belly;
  the reference has a slightly narrower sculpted throat. See the
  [right rake](renders/checkpoint/beauty/action_rake_right.png), left rake,
  right/left pairs and the bar/knuckle sections.
- **Underside and plate.** The plate seats into the forging and shares its
  rounded lower skin. Its curved front joint is a narrow seam. Rounded-end
  blade slots replace the broad rectangular openings. The guard and its rear
  wrist tang retain their accepted form. Our joint remains simpler than the
  photograph's curved plate border, and the forward hook pocket remains more
  open than the photograph's shallow visible joint. See the
  [bottom rake](renders/checkpoint/beauty/action_rake_bottom.png),
  [bottom pair](renders/checkpoint/pairs/action_bottom-pair.jpg), and the new
  plate and two slot sections. Baked raking light is the appearance evidence;
  geometry probes alone do not approve the highlight.
- **Aimed view.** The accepted eye frame, cheek station, drops, lever and safety
  are retained. The rib is visible between the fences toward the bead, with
  the crown below the bead line. Its short apparent length is strongly
  foreshortened by the cited fitted sight picture. The inspection rib is not
  yet matted. See the exact [Socket_Eye view](renders/checkpoint/beauty/aimed.png).
  Required sight rays now cover six rib stations from Y=140 to 740 mm as well
  as the bead, independently against all occupied skins.
- **Accepted remainder.** Trigger blades, guard band/tang, lever, safety,
  barrels/ribs/bead, splinter/iron, ammunition, rig, sockets and all 19 clip
  keys are preserved. Only the action, its pin/cross-pin placement, plate and
  stock head/inlets change. The stock head is refitted to the continuous side
  plane; the shortened upper head and wood beside the strap remain. A fresh
  build of `8a6ff08` confirms 96 of 104 native geometry/normal/rig/socket/clip
  entries are identical. See `build/preservation.json`. The larger historical
  region review below remains a record, not current acceptance.

## Round 4 critique passes

19. **Reference relation and first rebuild.** Color/value: retained dark steel
    and deep cavities; the black-backed macros cannot support a quantitative
    hue match. At full resolution the old spherical fences clearly stood
    above and outside the tubes, and the head/bar junction had a side ledge.
    Replaced them with concentric transverse arcs and an 18.5 mm axial roll;
    carried one side plane through the forging and extended the flush pin
    ends to that plane. Checked the first side/top/aimed previews against the
    native reference crops. The underside still had a raised plate boundary.
20. **Shared lower construction.** Color/value: judged the broad lower steel
    highlight before detail. The first plate-seat subtraction left a thin
    exterior skin and an oversized dark seam. Extended the seat cutter below
    the outer skin, made the plate and bar share the same 8 mm arris, and
    made their forward stations follow the curved seam monotonically. Narrow
    6 mm slots now surround the unchanged 5.4 mm blade roots. Cleared the
    wood inlets slightly beyond the plate slots to avoid coincident cut walls.
    Rechecked topology and contacts; no collision allow-list was added.
21. **Baked export and highlight continuity.** Color/value: the first 4096→2048
    export retained deep shadows without pale pin disks. Its bottom rake
    exposed a highlight mismatch at the plate joint and small polygonal
    transitions. Gave both sides of the seam the same original lower-skin
    normal field, retaining flat side normals, then rebaked. The fences also
    follow the actual tubes' slight axis convergence rather than assuming
    perfectly parallel bore centers. Circle/roll fits are measured from the
    export; neither the radius nor the center result is echoed from a model
    constant. Rejected UV charts that folded across the stock's hidden routed
    inlets; isolated its atlas region and tightened its projection partitions.

22. **Projection loss in the matched export.** Color/value: the top and
    underside pairs exposed a serrated steel-colored strip on the wood inlet,
    absent from the intended inspection color. Zero missed texels had only
    proved that rays hit something, not that they hit the intended part.
    Rejected the bake. Isolated the stock, action, plate and tang surfaces
    during material/normal projection, then combined those channels with a
    separate assembled-contact AO pass through the same kit baker. No
    geometry, accepted controls or triangle allocation changed. Rechecked the
    macro pairs and rakes from the new baked export before accepting the bake.

23. **All-part projection ownership.** Color/value: the new forend view still
    showed a serrated steel-colored fringe at the latch, even after isolating
    the action/stock joint. Extended projection isolation to all 54 actual
    named parts, independent of their shared animation bones. The accepted
    forend, controls and ammunition geometry remain unchanged. Added an
    independent constant-albedo audit of 48 single-material parts: 5,133,244
    eroded interior texels pass with zero wrong-color texels at a 0.01 linear
    RGB tolerance. As a negative control, the same audit rejects the assembled
    material projection (400,286 wrong-color texels), whose AO channel alone
    is retained. Reviewed new forend, control, underside and exact-eye previews;
    the neighboring-material fringes are gone. Tiny facets in the accepted
    routed latch lip remain geometry, rather than being hidden with a texture.

24. **Final baked-export review.** Color/value: reopened all eleven current
    photo pairs, the six full-size review pages, exact-eye image, three raw
    and annotated action rakes, sections and contact sheets. The inspection
    steel retains dark cavities and a broad rolled underside highlight; the
    hero has 20.71% deep-shadow pixels and no all-channel clipping. The black
    macro backgrounds provide no defensible neutral, so their unity balance
    and form-only comparison remain explicit. The whole-gun pairs retain the
    white-backdrop balance. Material boundaries at the head, strap and latch
    are clean in the delivered atlas. The side has no ledge, the pin reads as
    a flush same-steel circle, the bottom plate is seated, and the narrow slots
    follow the unchanged blades. Both rear fence edges curve toward the strap;
    the rib and bead are visible from the unchanged eye frame. The plainer
    shoulder junction, broader lower throat, simpler plate border and open
    forward hook pocket remain visible differences from the photographs.
    Reopened the clip and wide-opening strips and ammunition views; the
    accepted controls, extraction and manual loading sequence remain intact.

## Round 4 measured proof

`make -C guns/sxs` and the separately invoked `make -C guns/sxs check` both
complete with exit status 0. The final review audit accepts 294 render records
from the current exports and 19 correctly timed clip WebPs. Gun stills, rakes
and photo pairs use the baked `export/sxs.glb`; standalone ammunition retains
its accepted diagnostic export. No kit or common module changes this round.

| Check | Current result |
| --- | --- |
| Gun budget, including hidden ammunition alternatives | 37,822 / 38,000 triangles; 178 spare |
| Delivery | 6,175,024-byte GLB; one material; three 2048 images, from a 4096 GPU bake |
| PNG bytes: BaseColor / Normal / ORM | 260,530 / 1,078,947 / 1,596,544 |
| Geometry and intended states | source and reimport pass; 929 state samples each |
| Actual surface contact checks | 246 / 246 pass in both source and reimport |
| Half-frame motion sweep, all 19 clips | 1,715 source / 1,728 imported samples; zero violations; no allowed-contact exceptions |
| Largest measured motion penetration | 0.113714 mm imported, within the 0.20 mm tolerance |
| Independent native rebuild | 104 entries identical: positions at 1 nm, normals at five decimal components, exact clip keys/interpolation |
| Accepted baseline preservation | 96 / 104 native entries identical to a fresh build of `8a6ff08`; changed entries belong to the requested action/head/plate/pin work |
| UV atlas | no outside or degenerate UV triangles; overlap fraction 0.000001028, within the kit's 0.00001 tolerance |
| Texel density at 2048, p5 / median / p95 | 1,344 / 2,394 / 2,996 px/m |
| Projection | zero missed interior texels in all five channels; independent ownership audit and negative control described in pass 23 |
| Reimport serialization | maximum affine-position error 0.000191 mm; maximum sampled posed-surface error 0.000253 mm |

The exterior gauges in `build/serialization.json` are measured on actual
exported triangles. Both fence crowns are Z=57.350 mm against the barrels'
57.350 mm top line. Pair and breech widths are both 51.900 mm. Fitted arc
centers differ from the measured bore axes by at most 0.009 mm right and
0.019 mm left. The fitted rolls are 18.475 mm against the photograph's
18–20 mm estimate. The largest sampled head/bar side step is 0.00001 mm;
the largest plate/bar step is 0.004 mm. Lower-edge section fits give
7.96 mm radius against the photograph's 7–9 mm estimate. Each slot is
6.000 mm around a 5.400 mm blade, giving 0.300 mm on either side. The photo
scale estimates carry about ±2 mm uncertainty, as recorded in `refs/SOURCES.md`.
They are visual estimates, not published part dimensions.

The action/right, action/top and action/bottom landmark RMS residuals remain
61.57 / 41.00 / 81.00 px respectively. These are disclosed camera/form
comparison residuals, not a dimensional acceptance test; the three-landmark
bottom fit is particularly limited. Named meshes remain separate for form
diagnostics. Finish work and eventual skin consolidation remain held, and
no docs JPGs have been generated or committed.

## Earlier rounds — archival record

The following round-three and earlier claims describe their old unbaked outputs.
Round four above supersedes them; they are not current delivery claims.

# Covey 26 — form round 3: action

This is a form review, before finish/look-dev. The current inspection GLB has
constant materials and no texture images. Fine edge-radius/checkering normal
bakes and used finishes are still held; vertex-normal transfer from our own
dense sources is not described as a texture bake. No final docs JPGs are committed.
The accepted stock drops, cheek station, overall/barrel length, trigger blades,
rig, 19 clip schedules, 1.7.0 meanings and ammunition are retained.

## Current region review

Each entry names what still differs from the photograph. Passing geometry or
camera checks does not approve the look. Native pairs include unobscured panels,
a review-only photo outline over the render, and numbered residual arrows.
Black-background macros have no defensible neutral: unity gains remain explicit.
The white dealer backdrop supplies the whole-gun comparison balance. Neither
case color nor bluing is assumed to be neutral, and no finish match is claimed.

- **Fences and standing breech.** Replaced the flat-topped shoulders and melted
  crown with genuine round dome patches joined into one closed action skin.
  The barrel ends meet the standing-breech plane, without the former rectangular
  shoulder under them. The photo's fence roll is less proud and has a more
  delicate transition into its strap channel. Ours retains about 1.45 mm of
  fence crown above the tube crown and a broader central land; the reference's
  exact exterior radius is not independently calibrated. Inspect
  [right action pair](renders/checkpoint/pairs/action-pair.jpg),
  [left action pair](renders/checkpoint/pairs/action_left-pair.jpg),
  [loaded breech](renders/checkpoint/beauty/breech.png), the fence and standing
  breech sections, and both action raking sides.
- **Ground faces, bar and knuckle.** The sides and upper shoulders are explicit
  planes. The bar's lower edge sweeps up, its underside rolls into a narrower
  neck, and the concentric knuckle continues the same skin. Its cross-pin ends
  are flush circles. The photo has a more uniform, softer lower neck and more
  subtle arrises; ours has a stronger shoulder-to-side break and a small front
  hook pocket. The long underside opening is covered. No render or check
  relabels that remaining pocket as the photo's shallow plate joint. Inspect
  [underside pair](renders/checkpoint/pairs/action_bottom-pair.jpg),
  [right rake](renders/checkpoint/beauty/action_rake_right.png),
  [left rake](renders/checkpoint/beauty/action_rake_left.png),
  [bottom rake](renders/checkpoint/beauty/action_rake_bottom.png), and the bar,
  knuckle, knuckle-side and floor/lump sections.
- **Short upper body and wood head.** The upper head ends just behind the
  fences; wood comes forward beside the strap. The strap continues alone
  along the wrist. The photo has deeper rounded fingers and a less diagonal
  side seam. Ours uses simpler ground shoulders and a more pronounced diagonal
  inletting line. Inspect
  [top pair](renders/checkpoint/pairs/action_top-pair.jpg),
  [top rake](renders/checkpoint/beauty/action_rake_top.png),
  [controls](renders/checkpoint/beauty/top_controls.png), and the shoulder/head
  section. The accepted straight hand, pull and comb/heel drops remain.
- **Top lever and safety.** The lever is long, narrow and tapered, lying close
  above the strap on a round boss, below the fence crowns. Its closed tail
  follows the strap instead of swinging across it. The photo's tail is more
  pointed and its boss sits a little farther behind the fences. The accepted
  lever pivot and 25-degree clip travel remain. The safety stays farther back
  in its original guide/detents; its checkering remains a later normal field.
  Inspect the top pair, controls, aimed view, and Safety/SafetyOn/Open strips.
- **Guard and triggers.** The bow is a broad flat band with a swept front
  return and a rear wrist tang. The photo's rear return curls more sharply
  and its lower bow is less shallow. Both accepted trigger blades keep their
  forward-facing concavity, forward toes, pivots, pull direction and barrel
  assignment. The photo's front blade is longer/more delicate; it was not
  changed to conceal a framing residual. Inspect
  [trigger pair](renders/checkpoint/pairs/trigger-pair.jpg),
  [three-quarter blades](renders/checkpoint/beauty/trigger_quarter.png),
  underside pair and Fire/FireLeft strips.
- **Aimed view and rib.** The cited sporting sight picture now derives the eye
  height from the actual rib and bead, preserving the cheek station and stock
  drops. A short forward rib leads to the bead between the fences, with the
  lever/action below. The original dip after the chambers hid that surface;
  the sighting surface now follows the straight line between its accepted
  breech/muzzle endpoint heights. Joined flats and the seated valley filler
  remain. The rib is still broad at the rear; matting is held. Inspect the
  exact [socket view](renders/checkpoint/beauty/aimed.png), both barrel sections
  and the top orthographic view. No raised presentation eye substitutes for
  the socket, and no human mesh/personal fit is certified.
- **Forend and iron.** Kept the accepted 34.4 × 24.2 × 173 mm envelope. Replaced
  the sausage side with a flat land, defined lower edge, nearly straight taper
  and a supported slanted nose. Dense sculpt normals carry the carved surface
  without increasing the wood budget. Our plan-view nose is more squared off than the photo, the lower profile
  remains deeper forward of the latch, and the iron wraps less far up the
  wood. The original inset latch and two bearing cups remain simpler. Inspect
  [side pair](renders/checkpoint/pairs/forend_side-pair.jpg),
  [underside pair](renders/checkpoint/pairs/forend-pair.jpg),
  [forend](renders/checkpoint/beauty/forend.png), both forend sections and reload
  strips. There is no hand mesh; guide/shell clearance does not prove hand fit.
- **Open breech, extractor and ammunition.** Loaded above/behind views show
  the accepted shells in the extractor. The open photographic pose remains
  an empty, 30-degree comparison; canonical clips still open 42 degrees.
  The reference's broad upper extension differs from our narrower under-lug
  construction and cannot be used as a shared camera landmark. Our chamber
  backs/extractor and its exterior flats remain visibly different construction.
  Inspect [open pair](renders/checkpoint/pairs/open-pair.jpg),
  [detached flats](renders/checkpoint/pairs/barrel_flats-pair.jpg), loaded breech,
  lumps, opening strip and all reload/unload strips. The calibrated open
  camera is explicitly constrained to the muzzle-side hemisphere; a low-RMS
  chamber-facing fit was rejected. No clip or ammunition dimension changed.

## Round 3 critique log

12. **Planes and domes.** Color/value: retained dark inspection steel and checked
    unclipped raking highlights; the black reference has no neutral for a hue
    claim. The old crown and rounded-box shoulders were visibly melted. The
    first replacement still produced a curtain at the height-field boundary.
    Rejected it and rebuilt the domes as real closed spherical patches joined
    to explicit ground planes, without a smooth union.
13. **Head, controls and guard.** Color/value: made the underside readable with
    the existing procedural inspection softbox, without claiming the photo's
    case-color response. The full-width upper head still extended too far back
    because its seam depended only on height. Brought its outer upper corners
    forward, fitted the wood head, lowered/lengthened the narrow lever, added
    its round boss and refitted the broad guard's front return. The accepted
    trigger geometry and rig schedules remain.
14. **Fitted eye and forend.** Color/value: compared the exact socket picture
    against gray, judging bead and rib visibility. The old vertical offset
    was unsupported; the primary sporting coin rule supplies a reproducible
    sight-picture construction. It exposed the rib's longitudinal dip, which
    was corrected while retaining endpoint sections and valley seats. The
    forend's round side and nose were replaced by supported flat lands and a
    defined slanted tip within the accepted envelope.
15. **Photographic framing.** Color/value: black-backed macros remain form-only;
    white whole-gun backdrops retain their recorded balance. Re-observed shared
    breech corners, hinge, lever boss, visible trigger root and guard seats.
    Held all macro review lenses at 150 mm, bounded the observed view within
    20 degrees, and rejected an open fit on the wrong side of the breech.
    Added native-pixel arrows and a separate silhouette overlay to every pair.
    Sparse low residuals are not form acceptance. The underside remains the
    least certain comparison; its seat/length differences cannot be explained
    by one global translation or scale.
16. **Final raking and reproducibility.** Color/value: checked the actual export's
    side lands, dark cavities and rolling dome highlights. The underside's
    lower-radius transition still broke abruptly, so rolled the exposed neck
    across its section and eased it into the unchanged front bearing. Before
    reduction, conditioned the constructive seams with the same 6 µm weld
    used on the game mesh and a 1 µm coordinate grid. Canonical face/corner
    order makes both reduction and dense-source normal transfer reproducible.
    Independent builds retain the original strict 1 nm position/five-decimal
    normal comparison, rather than loosening it to hide variation.

17. **Head-section fit.** Color/value: reviewed the bright wood/metal seam in
    the top pair before grain or finish could hide it. The stock cage still
    sampled the narrower unwarped station after the action seam moved forward.
    Matched the head section at its actual warped station and returned the
    seam around the strap root. Cleared a small unsupported wood feather at
    the front well rim instead of filling its resulting boundary triangle.
    Retested the actual contacts, topology and all clips after rebuilding.

18. **Latch-land normals.** Color/value: the flat underside pair exposed
    star-shaped dark highlights around the routed latch. The transferred corner
    normals were choosing an inlet wall for some corners on the exterior land.
    Preserved the dense lower-land polygon normals and kept the reduced land's
    own surface normals at the route. The clean underside preview removes the
    stars without moving vertices, changing the accepted envelope or spending
    more triangles. The surrounding carved corners retain smooth normals.

## Photographic fit limits

The 150 mm macro lens is a review-camera choice, not recovered EXIF. The
observed hemisphere and 20-degree view cone prevent arbitrary orbiting, but
three-point comparisons remain sparse. The left-action fit in particular
cannot certify the rest of the shape. The open photo's differing extension is
excluded from calibration. The photo outline is extracted only in the review
compositor: no contour or image is read by modeling or shaders. Threshold
lighting holes remain in some outlines; the unobscured photo panels are the
authoritative visual comparison.

The companion diagnostic fits a 2D similarity correction to the residuals.
A large remainder demonstrates nonuniform disagreement; it cannot, by itself,
distinguish a form difference from an uncertain landmark or perspective.
The region critiques above supply that visual judgment. The underside's
remaining disagreement is explicitly retained rather than minimized by fitting
an unshared contour.

## Measured form and source limits

| Quantity | Actual exported surface | Reference basis |
| --- | ---: | --- |
| Lever length / thumb width | 78.45 / 7.09 mm | plain top photograph; estimated target 76–82 / 6.5–8 mm |
| Round lever boss | 11.20 mm | plain top photograph; estimated target 10–12 mm |
| Lever thickness | 1.89–1.93 mm | plain side photograph; about 1.5–2.1 mm |
| Lever height above strap, underside gap | 0.67–1.33 mm | plain side photograph; about 0.5–1.5 mm |
| Guard band width × thickness | 12.40 × 1.63 mm | plain underside/side; about 12–14 × 1.5–2.1 mm |
| Eye above actual comb | 42.811 mm | CPSA sporting coin-rule construction; see below |
| Eye above extended actual rib | 3.612 mm | same construction |
| Forend overall W × D × L | 34.40 × 24.20 × 172.99 mm | accepted nominal 34.4 × 24.2 × 173 mm |
| Forend rear, Y=211 mm | 34.16 × 22.54 mm | actual triangle-plane intersection |
| Forend front, Y=320 mm | 28.24 × 16.16 mm | actual triangle-plane intersection |
| Wrist, Y=-15 mm | 32.17 × 37.88 mm | actual triangle-plane intersection |

Lever and guard reference sizes are explicitly photo-scale estimates, about
10% uncertain, not published dimensions. Preview pixels, assumed exterior
scale, native sources and licenses are recorded in [SOURCES.md](refs/SOURCES.md).
Thickness is measured vertically through the actual lever at three stations;
the gap is from its underside to the actual strap. Width excludes the boss
where labeled thumbpiece. These are mesh measurements, not parameter echoes.

At the accepted Y=−123 mm cheek station, the actual comb is Z=17.689 mm.
The [CPSA handbook](https://www.cpsa.co.uk/userfiles/files/CTSH.pdf), printed p. 4-2,
sets the sporting sight picture by a pound coin 200 mm ahead of the breech.
Using the [Royal Mint historical 3.15 mm thickness](https://www.royalmint.com/collect/collector-resources/designs-and-specifications/one-pound-coin-designs/)
and the actual rib Z=54.492 mm at Y=315 mm, the line to the
bead center extends back to eye Z=60.500 mm. The local comb drop
39.199 plus eye-above-rib 3.612 gives
42.811 mm above the comb. The measured coin-ray error is
0.000004 mm. This is a cited sight-picture fit, not an anatomical
claim. The original Brownells cheek station and cited 38/63 mm drops remain.

## Native photographic residuals

| Pair | RMS px | Remainder after 2D similarity px | Interpretation |
| --- | ---: | ---: | --- |
| [right](renders/checkpoint/pairs/right-pair.jpg) | 4.11 | 3.89 | accepted whole silhouette; local form |
| [left](renders/checkpoint/pairs/left-pair.jpg) | 5.60 | 5.30 | class stock/gauge differences; local form |
| [action](renders/checkpoint/pairs/action-pair.jpg) | 55.73 | 55.03 | fence/breech proportions and original head seam; form |
| [action_left](renders/checkpoint/pairs/action_left-pair.jpg) | 0.25 | 0.25 | three-point fit only; sparse evidence, not form acceptance |
| [action_top](renders/checkpoint/pairs/action_top-pair.jpg) | 40.89 | 39.41 | boss station, head corners and tail; form |
| [action_bottom](renders/checkpoint/pairs/action_bottom-pair.jpg) | 77.20 | 77.02 | guard seats/length; form plus perspective/landmark uncertainty |
| [open](renders/checkpoint/pairs/open-pair.jpg) | 39.75 | 39.74 | different exterior extension/lug construction; form |
| [barrel_flats](renders/checkpoint/pairs/barrel_flats-pair.jpg) | 12.51 | 12.49 | original lug/flats dimensions; form |
| [forend](renders/checkpoint/pairs/forend-pair.jpg) | 2.87 | 2.84 | nose/iron proportions; local form |
| [forend_side](renders/checkpoint/pairs/forend_side-pair.jpg) | 2.48 | 2.41 | lower profile/nose; local form |
| [trigger](renders/checkpoint/pairs/trigger-pair.jpg) | 26.14 | 25.41 | guard return and accepted blade differences; form |

No pair has a dominant residual that one additional global translation, scale
or roll removes. This does not rule out perspective or observation uncertainty,
especially in the underside. The open pair now crops out the guard and fits
barrel rim corners and the hinge rather than the unshared extension.

## Current verification

`make -C guns/sxs` passes the complete form build and evidence audit.
`make -C guns/sxs check` also passes a separate assembly/serialization run.
The form GLB has **37,728 triangles**, 54 named rigid meshes,
17 bones, 19 clips and 14 sockets. It is 1,765,484 bytes, with
9 inspection materials and zero texture images. The source retains dense
geometry for later normal baking. Normal-map radii/checkering, UV/atlas checks,
finishes, wear and bake-loss assessment remain outside this form gate.

The separate source/import checks pass topology, intended states, required
surface contacts and all 19 half-frame sweeps, with no contact allow-list.
They cover 1,715 / 1,728 samples, with 246 contact records each and
0.11371 mm maximum penetration against a 0.20 mm visual tolerance. No mesh has
nonmanifold edges, zero-area triangles or reversed volume. The joined tube
separating-plane measurement remains a distinct check on the same-bone skins.

Ground-side/shoulder plane probes measure at most 0.000118 mm departure from a
best-fit plane over their sampled patches. Those measurements establish the
geometric flats; the raking renders establish the highlight behavior.

Independent fresh builds agree on all 104 geometry/normal/rig/socket/clip
entries at the original 1 nm position and five-decimal normal comparison.
Serialization separately compares 1,715 affine samples and event surfaces. Maximum
affine position error is 0.000191 mm; event-surface displacement is at most
0.000253 mm. This does not substitute for the contact sweeps.

All current evidence is under `renders/checkpoint/`: `contact-sheet.jpg`,
`photo-pairs.jpg`, `source-photo-pairs.jpg`, `sections/sections.jpg`,
`clips.jpg`, `opening.jpg`, `strips/`, `ammunition.jpg`, and the individual
beauty views linked above. The provenance/timing audit checks hashes and real
clip durations. The audit confirms 305 current render records and 19 real-duration
WebPs. Hero luma p1/p50/p99 is 1.07 / 47.87 / 205.59; deep shadows occupy 21.08%
of the visible hero, with zero all-channel clipping. This is inspection tone,
not albedo or finish acceptance.

No kit or shared/common source changed. Main was merged before modeling; the
family interface conflict retained all additive supplements. A general kit
candidate is deterministic mesh/corner canonicalization before reduction,
with explicit precision policy and regression fixtures. Nothing is needed
from the lead beyond reviewing this form gate. No final docs images are added.

## Round 2 record, superseded by the current region review

# Covey 26 — form round 2

Look-dev remains held. All current views are constant-material inspection
renders. No normal-map edge transfer, checkering, finish, wear or final atlas
is being passed off as complete. The previous checked region list was too
lenient and is superseded below. This document requests review; it does not
approve its own remaining form and measurement limitations.

## References and photographic framing

Commons was searched first. Its plain American whole-side photograph is sharp
as a whole gun but does not resolve the action at 600 pixels. The new primary
plain 12-gauge dealer set supplies native 1876–4767 px originals: both action
sides, top, underside, splinter underside and assembled open action. The
registered smaller-gauge dealer set supplies complete left/right views with
the entire gun over 800 native pixels. The primary wide 12-gauge sides clip
the muzzle and are never labeled whole-gun references. The old decorated
sideplate action and loaded sidelock are excluded from current acceptance.

See [SOURCES.md](refs/SOURCES.md) for every original, dimensions, attribution,
license and use. The tile-pyramid fetcher assembles the dealer's original
pixels without tracing or changing a contour. It downloads images only.
No photo or measured outline is consumed by the geometry generator.

The white backdrop in the whole-gun pair is balanced in linear light. The
black-background macros contain no reliable neutral; they are form-only
comparisons, with unity gains explicitly recorded. No bluing or case-color
patch is assumed gray. Each critique begins with value; these materials are
inspection constants and cannot establish photographic finish or wear.

`build/cameras.json` retains native observations, fitted cameras, residuals
and view constraints. Blender independently verifies the projections. Eleven
pairs cover right, left, both action sides, top, bottom, open action, detached
barrel flats, bottom and side of the forend, and triggers. RMS is not form
acceptance. The whole-gun fits are about 4–6 native pixels. Eight macro view directions
are locked after visual inspection; translation, focal estimate and roll
fit the framing. They retain up to 132 px native residuals because original
contours and landmarks differ. This limitation is visible in every pair.

An early open pair fitted circles while viewing the wrong side of the breech.
It was rejected despite its smaller RMS. The corrected comparison fixes a shallow view from above and forward of
the breech, with an empty 30-degree photographic presentation and its
extractor pressed home. The 42-degree canonical clips and extractor travel
are unchanged. The open reference also has a raised top extension with a rectangular cut,
which our original under-lug construction does not share. It must not be
misidentified as our barrel flats. The detached flats reference has no action or forend: only the
visible barrel region can be compared; it cannot establish an assembled fit.
The matched flats shot omits the action and forend to match the detached
photograph; the full exported gun and canonical clips are unchanged.

## Round 2 critique passes

7. **Photographs and sections.** Color/value: black backgrounds have no
   defensible neutral, so no quantitative finish match is claimed. The old
   action reference was the wrong construction class. The old breech outer
   walls overlapped, the rib was a post, and the forend was too round/full.
   Replaced the acceptance set, cut joined breech flats, filled the top valley
   with a seated tapered rib, and built a slim, flat-sided splinter with its
   channels, iron pocket and bottom latch. Added separate wood dimensions to
   the section labels so barrel width cannot be mistaken for wood width.
8. **Forging and furniture.** Color/value: checked the roll-off on dark steel
   and the head's shaded seam before detail. The first union left a slab-like
   bar/receiver transition, long rear body and an oval wood head that made
   wings beside the metal. Rebuilt the forging's changing sections, rounded
   belly, bowed rear seam, tapered bar and concentric knuckle; matched the
   wood head to its inlet section. Replaced the proud slotted hinge heads
   with the ends of a small flush cross pin. The source forging is retained.
9. **Lever, guard and actual assembly.** Color/value: underside views were
   unreadably black, so added a procedural inspection softbox below them.
   The lever was a thin plate; the first thicker sweep collided at the crown
   and stock. Lowered the central rear crown, seated the thick shank and
   swept thumbpiece, and opened the stock inlet. Refitted the guard bow and
   wrist tang, and moved the rear blade's root back 12 mm while retaining
   direction, angle and assignment. Corrected actual collisions instead of
   adding clearance exceptions. A tiny folded Boolean flap at the guard-tang
   inlet was removed by its topology, not filled into a nonmanifold patch.
10. **Stock drop and exact eye.** Color/value: judged the bead and rib against
    the neutral gray card. A bead hit alone did not prove visibility. The
    source/import checks now test every occupied skin along that ray and rays
    to three forward rib stations. Lowered the comb to the published drop
    and located the cheek station 35 mm behind its nose. The exact socket
    view shows a short rib length and the bead, with the action below. The
    vertical human cheek-to-eye citation remains missing: see measurement
    limits below. A 45 mm inspection lens makes the actual sight picture
    readable; it does not alter the socket or imply a physiological FOV.
11. **Exported shading and final evidence.** Color/value: checked deep
    cavities, unclipped bright regions and the crown's moving highlights.
    The roof's inherited Boolean face labels were unsafe after reduction;
    use actual surface location to identify the analytic roof field. A dense
    normal-transfer experiment was rejected. The bar now shares continuous
    surface strips with the body; its former overlapping table union was
    removed, and the fence shoulders were made more proud of the tubes. Keep
    the raking views and dense-source comparisons visible: smoothness and
    photographic form still require the lead's judgment, not a passing mesh
    check. The final sheet review also rejected a low-RMS forend side camera that
    had drifted below the wood. Locked that view and isolated the barrel
    assembly for the detached flats reference, where the action had occluded
    the part under review. Rebuilt all current evidence against the final
    output hash.

## Region review and remaining differences

- **Action, fences, top lever and safety.** The forging now has bowed rear
  inletting, rounded top/bottom shoulders, a tapering bar and circular knuckle
  bearing. The primary photo's fences have a more cylindrical rear roll;
  its rear head has deeper scalloped fingers around the tang. Ours remains
  fuller through the central crown, with a plainer rear seam and a more
  exposed spindle. The bar/receiver transition and crown highlights are the
  weakest form cues and must not be called fixed by future texturing.
  Inspect `beauty/action.png`, `action_left.png`, `top_controls.png`,
  `rake_right.png`, `rake_left.png`; `pairs/action-pair.jpg`,
  `action_left-pair.jpg`, `action_top-pair.jpg`, `action_bottom-pair.jpg`;
  and the standing-breech, bar and knuckle side sections.
- **Triggers and guard.** Both faces retain their forward concavity, forward
  tips and barrel assignment. The guard is a swept flat band with a rear tang
  following the wrist. The photo has a longer, more delicate front blade and
  a flatter lower bow. Ours is thicker through the lower corners and has
  more front clearance. Inspect `beauty/triggers.png`, `trigger_quarter.png`,
  `pairs/trigger-pair.jpg`, `strips/Fire.jpg` and `FireLeft.jpg`.
- **Barrels, rib, bead and muzzles.** Joined outer flats replace overlapping
  skins at the breech. The rib fills the valley, follows the barrel seats and
  tapers to the muzzle. The photo has a narrower, more visibly raised rib at
  the rear; ours has a broad shallow-concave face there. Matting is held for
  the normal map. Inspect side/top/front orthos, `beauty/muzzle.png`,
  `aimed.png`, both whole-side pairs and both barrel sections. The exact eye
  sees the bead and a short forward rib; most rear rib remains foreshortened.
- **Breech, extractor and lumps.** Our joined-tube construction has a narrower
  web and stepped central lumps. The reference has broader continuous flats
  and a different single lug profile. No detached photograph proves hinge
  engagement. Actual hook/pin, breech, rim/extractor and bite/shoe probes do.
  Inspect `beauty/breech.png` (loaded from above/behind), `open.png`,
  `lumps.png`, `pairs/open-pair.jpg`, `barrel_flats-pair.jpg`, floor/lump
  section, `opening.jpg` and the Open strips. Shell dimensions are unchanged.
- **Forend and iron.** The splinter is narrower than the barrels, with nearly
  flat tapering sides, rounded bottom and two top channels. The photo's nose
  is squarer and rises more sharply; ours is rounder and more pointed. Its
  iron wraps farther up the rear wood; ours uses two separate bearing cups
  and a simpler inset latch. The bottom photo alone cannot validate that
  latch design. Inspect `beauty/forend.png`, `pairs/forend-pair.jpg`,
  `forend_side-pair.jpg`, two dimensioned wood sections and the reload strips.
  No hand mesh is present, so hand contact is not proven; socket and shell
  paths clear the revised furniture through all clips.
- **Stock, wrist and butt.** Kept the straight hand, length and front-trigger
  pull. Widened the wrist and fitted the head to the bowed forging seam.
  Actual rib/wood rays now measure published-class comb/heel drops. The
  whole-gun reference has a different grip and butt treatment; its geometry
  cannot establish our exact straight-hand contours. Our head is plainer and
  its tang inlet seam broader. Inspect `beauty/stock.png`, both whole-side
  pairs, both butt sections, wrist and tang-inlet sections.
- **Ammunition.** Accepted dimensions and shared module are unchanged. Our
  unmarked red hull and primer are simplified original exterior forms.
  Inspect `ammunition.jpg`, `beauty/breech.png` and reload/unload strips.
  Markings, head finish and hull wear remain held.

## Measured dimensions and evidence limits

The imported GLB measures 1079.95 mm overall, 660.40 mm barrels and 369.63 mm
front-trigger pull. Stock drop, measured against a straightedge reconstructed from actual points on
the rib centerline, is 38.05 mm at the authored comb nose and 63.05 mm at the heel,
against published 38/63 mm. This centerline datum approximates a
straightedge: the concave rib edges rise about 0.22 mm above it. The cheek station is 35.00 mm behind that nose,
within the primary fitting source's 31.75–38.10 mm range.

**The human vertical fit is not sourced.** The socket is (0,−123,67) mm,
49.31 mm above the actual comb at its station. That is a measured model offset
and an authored vertical fit, not a measured human cheek weld. The original
45 mm justification is withdrawn. A reproducible mounted-person measurement
with scale is still needed to satisfy that part of the brief.

Wood-only wrist at Y = −15 mm is 32.23 × 37.74 mm. The forend's overall wood
bounds are 34.40 × 24.19 × 173.01 mm; its sections at Y = 211 / 320 mm are
34.39 × 22.53 / 25.90 × 18.68 mm. These are actual triangle intersections.
The photos constrain proportions, but their absolute wrist/forend dimensions
were not independently calibrated in millimeters. Do not label these numbers
as published specifications or precise photo measurements. This reference
measurement requirement remains weaker than requested.

## Verification scope

`make check` runs separate source and fresh-import topology/contact sweeps
through all 19 clips at half-frame intervals, with a 0.20 mm visual tolerance
and no contact allow-list. Actual-surface probes cover hinge, knuckle, breech,
chambers, rim support, locking bites, lever seat, safety and sight visibility.
A separate global-X surface-extrema check proves that the two joined tube
skins do not overlap; their shared bone would exclude them from the normal
cross-bone sweep. A second independent build checks deterministic geometry, normals, bones,
sockets and animation. Source/import affine samples and event surfaces prove
serialization separately from assembly correctness. Timed WebPs are decoded
and summed at their real durations. `audit.json` checks current source hashes.

Current proof: `make -C guns/sxs` and `make -C guns/sxs check` pass.
The staged gun is 34,638 triangles, 54 rigid meshes, nine inspection materials,
zero images and 1,630,020 GLB bytes. Source/import sweeps cover 1,715 / 1,728
samples across 19 clips, with 246 measured contact records each and 0.17201 mm
maximum penetration. Rebuild comparison passes all 104 entries at 1 nm position
rounding and five decimal normal components. The presentation audit confirms
301 current render records and all 19 real-duration WebPs. Hero luma p1/p50/p99
is 1.07 / 46.21 / 204.27, with zero all-channel clipping; this is a tonal-range
check on inspection materials, not finish acceptance.

No kit or shared/common file changed in this round. There are no final UVs,
textures or bake-loss claims. No hand mesh or ergonomic fit test is supplied.

## Prior checkpoint history, not current acceptance

The following log records the first session's investigations. The owner's
round-2 rejection supersedes its favorable judgments and reference choices.

## Critique log

1. **Blockout, both sides and sections.** Color/value: constant dark steel and
   brown wood make no finish claim; pale Workbench illumination is unsuitable
   for color acceptance. The first allocation was too expensive, the tang
   floated over the wrist, and the safety lacked a convincing seat. Rebuilt
   tang inlets and fitted the controls; reduced hidden bevel and cage costs.
   Preserved the stock's changing comb/cheeks and the splinter's barrel
   channels instead of flattening either into an extruded profile.
2. **Raking form and trigger photograph.** Color/value: retained dark material
   values and inspected the light roll-off, without matching the colored
   floor's hue. The action looked like a rounded cap on a separate plank.
   Rebuilt a changing-section body with continuous fences and a unioned water
   table. Broad guard band, blade thickness and forward-concave trigger faces
   were checked in side and underside views. Narrow wires and backwards
   hooks were rejected. Hero framing was enlarged to retain the whole butt.
3. **Open assembly and actual contacts.** Color/value: dark cavities must stay
   legible under the breech. The extractor bridge/stem, rim seats, lock shoes
   and lever spindle exposed real interpenetrations during motion. Cut their
   actual passages and reset the movement sequence; no clearance allow-list
   hides them. The lower tang/safety support and forend iron were fitted to
   their actual surfaces. Shell skins were made closed without overlapping
   disconnected head/hull components.
4. **Cycles exported close-ups.** Color/value: no all-channel white clipping
   is accepted in the hero; black metal must retain deep cavities and rolling
   highlights. The shell heads had a false concave reflection after export;
   restored planar head normals. The exact aimed view hid too much rib;
   raised the eye and remeasured the comb offset. The roof showed triangular
   highlight boundaries, and some cross-pin heads were buried or reversed.
   Rebuilt longitudinal curvature and normal fields, seated both pin pairs,
   and added a recessed steel floor/rails under the safety.
5. **Sharp breech photo and section recheck.** Color/value: white-balanced the
   new sheet-backed macro; no sampled finish is accepted yet. Replaced the
   undersized open-action target. A section exposed a floating bottom rib;
   rebuilt it to join both lower barrel skins. Coincident extractor-relief
   cuts left hatch-like sliver faces; moved the cutter into empty bore space.
   The remaining roof sawtooth came from a hard minimum in the fence/land
   surface, not lighting. A continuous radius removed it under the same
   raking camera (`renders/crown-review/action.png`). Final reduction also
   exposed a microscopic folded corner at the lever bore. Welding within
   0.0001 mm after reduction repairs it; both topology checks must pass.
6. **Whole photographic framing.** Color/value: retained the declared neutral
   patches; finishes remain held. Chamber-only fitting concealed an incorrect
   whole-assembly comparison. Inspecting the full sharp original and the
   neighboring photographs showed its barrels were detached. Reclassified
   that pair as barrel detail, rather than forcing a false hinge fit. Corrected
   the left/right shell identification and removed an arbitrary camera-height
   prior in the assembled loaded photograph; its fit improved from 120.3 to
   26.7 native pixels. Both action and shells now share the photographed
   framing. Fixed a presentation-only extractor press that an active animation
   had overwritten. The pose is frozen before applying it, then asserted.
   Restored smooth sculpt shading on the dense controls in their comparison
   scene; inherited flat cage faces had produced bands absent from the game
   normals. Enlarged the stock/lump framing and gave trigger/safety clips
   their own close cameras so their real travel can be judged.
