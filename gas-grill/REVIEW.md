# Image review record

Every render in each set below was opened and inspected. References were viewed
as a source sheet and individually where dimensions/construction required it.
Intermediate images remain ignored local outputs, not committed documentation.

| Pass | Images and critique | Changes before the next pass |
| --- | --- | --- |
| Workbench | Closed/open, controls, front, side. Wheels edge-on from front; feet separated from leg ends; excessive front lid gap. | Correct wheel axle from X to Y, connect feet, add sealing lips, model hose barb. |
| Cycles 1 | All five requested views. Coated parts too silver, graphics washed out, badge and gauge float; tank 5812 triangles, thin plates have zero-area slivers. | Darker dielectrics, calmer exposure, surface-tangent mounts, safe thin bevel radii, remove small tank game bevels. |
| Cycles 2 | All five requested views. Wheel rims hide spokes; depth short by 14.8 mm; tank still 4100 triangles. | Open spoke rims, adjust handle bow, reduce cylinder radial count, increase high hood tessellation; generated game counts 19376 / 3876 pass. |
| Cycles 3 | Five required views plus interior, tank, construction, scale. Tank close-up reveals hose entering shoulder and weld cutting through label. Controls expose intersecting handle curves. Shelf anisotropy makes a radial star. | Shared analytic handle curve, regulator extension and exterior hose route, label conformed over bead, explicit brushing tangent, coated grime reduces metallic response. Tank rises to 3948 with conformed label. |
| Checkpoint refinement | All nine views. Inner lid stiffeners protrude through the steep front hood where a vertical offset gives too little surface clearance. | Offset ribs along the actual profile normal. Rebase asset origin to the full ground footprint center; repeat the complete build, audits and nine-view render. |

The checkpoint is intentionally a source-scene review. Game topology is generated
for a defensible budget, but no bake/export/final pipeline claim is made.

Remaining weaknesses: sparse asymmetric use marks, overly regular carbon and
grease variation, simplified regulator construction, and side/rear proportions
supported by manufacturer diagrams rather than matched orthophotography. The
hood profile and open clearance are original, so its open envelope is not an
exact duplicate of the dimensional reference.

## Validation at handoff

- `make -C gas-grill PASS=checkpoint`: passed; full source build, two scene audits,
  repository rules, nine locked OptiX Cycles renders at 1400 px / 80 samples,
  reference plates, contact sheets and four documentation JPGs.
- `make -C gas-grill check`: passed. Grill 19,376 triangles; tank 3,948.
  Finite geometry/normals, no zero-area triangles, manifold closed solids,
  positive signed volumes, and measured bounds pass. Printed label/marking
  sheets are explicitly allowed open boundaries.
- `make -C gas-grill preview`: Workbench completed; the initial five views
  were inspected. A final preview was also regenerated after geometry fixes.
- Studio Eevee smoke check: `hero_closed`, 1000 px / 64 samples, passed and
  inspected. Eevee grain remains at this preview quality; this is not delivery proof.
- Worktree-local pre-commit hook installed and invoked by commits. Four docs
  JPGs are 1600 px wide, each under 200 KB; no downloaded reference pixels
  are included in those committed images. Reference comparisons stay ignored.
- Independent repeated game builds produce identical geometry SHA-256 values
  for both sets (`6e9a85ba…` grill, `7e3ee6fe…` tank). Regenerating all four
  marking images produces byte-identical PNGs.

The UV, bake, export, texture/material delivery budgets and GLB re-import gates
are listed as pending in every audit. The look-dev scene is 838,692 bytes locally;
its source finishes are 18 grill material slots and 6 tank material sources, not
the final two atlases. No blend, PNG, GLB or reference files enter Git.

# Checkpoint 2 / photo-directed review

Checkpoint 1 was not an acceptable realism result. The four committed JPGs were
removed in commit `5387347`; checkpoint images now stay in ignored `renders/`.
No bake or export is authorized for this review round.

Selected pairs: manufacturer front three-quarter (`grill-three-quarter.jpeg`),
Future/Monib Zahdeh's open cooking area (`open-photo.png`), and Weber/John Burns'
connected cylinder (`tank-connected.jpg`). `kit/photo_match.py` fits cameras from
measured dimensional landmarks using a pinhole model and writes its pixel errors.
The photographs never enter a material. No source camera EXIF is available;
focal lengths are estimates, not claimed measurements. The interior reference
has a regional GBS insert; this asset retains the US two-section straight grates.

## Pass 1: new construction, compared directly with the three photographs

Images: `renders/cp2-pass1/*-pair.jpg`, plus hero closed/open, construction,
tank and control close-ups. All were opened and inspected.

Differences that still say CG:

- Whole object too bright; coated casting reads pale plastic beside the source's dark gray casting.
- Enamel front has broad silver reflections and a mottled heat band. The reference has a controlled dark finish and crisp rectangular reflection.
- Cap wrapping and overlapping skirt are now real, but their contours are too softly lit to read.
- Gray control knobs, excessive bezel glints and razor-clean fascia lack the source's restrained contrast.
- Three brass valve bodies protrude through the fascia; the ignition lead makes an impossible diagonal line on its face.
- Several high screw recesses are topologically broken, leaving bright fragments. This is a source audit failure, not acceptable tiny detail.
- Hook rail and shelf hems now exist, but the metal remains too uniformly clean and bright.
- Cooking bars still read gray; gaps expose too much white steel below. Source bars are satin black, closer together, with dark depth beneath them.
- Warming rack wires run fore-aft. The actual photographed rack uses long transverse wires with sparse longitudinal ties.
- Heat tents have correct V construction/count, but their material still reads reflective silver. They must be dark oxidized/enameled steel.
- New inner carbon is gray-black rather than brown, but its cloud pattern is too broad and regular.
- Added carbon flake geometry reads as scattered dots from this distance; reduce large fake-looking flakes and keep the crack layer restrained.
- The regulator is connected to the correct nut now, but the inlet stub sticks through the dome and its outlet barb is too long.
- The valve/outlet points straight at the fitted tank camera. The photograph shows its brass side and a diagonal regulator.
- Coupling plastic is too light; regulator casing lacks the source's subdued zinc contrast and stamped detail.
- Tank paint is too white/sterile; lower ring/seam patina is too weak to read.
- Our scale appears on the opposite image side because this grill hangs its tank outside the right cart; the photo shows a different cart arrangement. Keep the correct mechanical spring/hook construction and label the configuration difference.
- The lower retention saddle looks like a floating black rod. It needs attachment to the frame and contact against the cylinder.
- The rear left fixed foot is what looked like an unexplained central block at checkpoint 1. It is a real second fixed foot; its new push-on shoe and leg connection make its role visible.

Changes for pass 2: darker calibrated dielectrics and exposure, narrow photographic
rim/negative-fill cards, less enamel heat roughness, more/closer satin-black grate
bars, transverse warming wires, dull dark heat channels, valve/lead clearance,
clean radial screw recess topology, shorter compact regulator inlet/outlet,
valve yaw within a wider collar opening, and an attached lower cylinder saddle.

## Pass 2: controlled lighting and corrected assemblies

Images: `renders/cp2-pass2/*-pair.jpg` and all five standalone hero/detail
renders. Each was opened and inspected. The parts now read as manufactured
assemblies, but this is still too pristine beside the photographs.

Differences that still say CG:

- The tank hose disappears into the shoulder immediately after its ferrule. The visible black hose farther left disguises a real routing error. The ferrule must clear the spun shoulder before the bend.
- The lower saddle is attached to the cart now, but its rubber end still floats clear of the lower dome. Move the contact to the cylindrical wall.
- The tank's coating, equator weld and ring lack visible localized oxidation. The paint is too smooth at close range.
- The regulator still resembles a smooth generic disc. Add pressed ribs, vent and stamped identification; use darker zinc with irregular oxidation in creases.
- Handwheel sits too high on a long exposed spindle. The source has a compact forged valve and a lower handwheel.
- The grate spacing/cross-sections are credible now, but identical gray faces have no food contact patches, cooked oil or irregular carbon. The exact GBS center insert is deliberately absent for the selected US configuration.
- Rack wires are correctly transverse now; the fitted open camera still has about 22 px residual and cannot reproduce the reference's slight roll.
- Construction view leaves the grate's empty perimeter and cross ribs floating above the tents. Hide the whole removable grate assembly for this diagnostic view.
- Heat tents are dull now but their mottling is broad; deposits should concentrate near the ridge and low edges rather than become uniform camouflage.
- Powder coating has virtually no readable contact scuffs/chips at feet or joints. White tank edges remain immaculate.
- Stainless worktops and fascia are too even. Fingerprints are too weak, and their current envelope would be too large if strengthened.
- Enamel is substantially better, but still lacks convincing localized handling scratches near the saddles. Inner carbon remains too cloudy and evenly distributed.
- Small screw recesses render better but still produce zero-area cap triangulation in the high source audit. Correct topology before accepting the source.
- The main hero's silver front reflection is slightly broad; dark rims and grounded contact shadows now establish the silhouette, but lighting alone cannot supply missing material detail.

Changes for pass 3: shoulder-clearing regulator/hose route, tank saddle contact,
lower OPD handwheel, pressed/marked regulator cover, explicit screw recess floor
fans, camera roll fitting and corrected rack landmarks, localized cooking/oil
patches, stronger sparse seam/foot rust, manufactured coating microstructure,
small finger-pad ridges, contact-gated abrasion, and a combustion diagnostic view
with selected heat tents removed. No source photo is used in any shader.

## Pass 3: localized use, camera roll and clearance inspection

Images: all nine `renders/cp2-pass3/*.png` and the three recomposed pairs were
opened. The tank seam/ring patina finally reads, the saddle contacts the cylinder,
and the source audit is clean. However, this pass exposed further failures:

- New pointiness-based chips pepper the cap strips and broad leg faces. This is procedural decoration, not credible abrasion. Remove that curvature fallback and require authored contact regions.
- The ferrule clears the shoulder now, but the hose's return curve still cuts through the vessel. Use a polar route outside the measured vessel radius, and assert clearance for every path sample.
- The outlet has too much exposed brass between the regulator and ferrule. Shorten it to a compact barb.
- The fascia's top black stripe is not a graphic: the heat shield intersects the inclined panel and hides the brand silkscreen. Move the shield behind the panel.
- Heat tent noise is still camouflage across each whole face. Narrow heat exposure to the ridges, place cooked deposits only under the grate's food zones, and darken their dry carbon response.
- The combustion view removes the two channels BETWEEN burners, leaving the burner tubes covered. Remove channels 1/3/5 for that diagnostic instead, and raise the camera.
- The bowl floor/drain has real construction but is too spotless. Add localized grease tracks on the sloped front, using surface direction to prevent identical tracks on the back.
- Grate contact zones are visible only weakly in roughness. Their carbon should suppress specular response as well as diffuse color.
- Seven raised lid flakes read as evenly scattered black dots. Keep fewer, smaller lifted edges; put the fine cracking into the shader and restrict buildup to heat plumes/cavities.
- Wheel tread is almost smooth at this framing. Add circumferential molded grooves in the high source; preserve the game silhouette/count.
- The control knobs look slightly small against the measured fascia. Increase their diameter to about 60 mm while retaining the shaft pivots.
- The shared rubber shader applies its wheel-radius scuff to the entire hose. Split wheel-local radial wear into a tire-specific instance; keep ordinary hose rubber free of that mask.
- The stainless worktops still have a faint cloudy appearance because height alone exposes the whole top to heat. Gate tint to their inner edges; the final review should emphasize fine brushing and localized touch marks rather than broad dirt.

Changes for the confirmation render: all of the above, plus a higher-resolution
1600 px / 112-sample Cycles set. This is a fourth image set following three
critique/fix passes, with no bake/export. The camera mismatch caused by regional
grates and the opposite-side scale in the tank photo remains explicitly labeled.

## Pass 4: full-size confirmation, then final polish

Archived as `renders/cp2-pass4/`. All 13 rendered views were inspected, including
the three pairs. The hose loop clears the cylinder (3.94 mm minimum sampled
surface clearance), the cap speckling is gone, and the fascia graphics are exposed.
Further differences found at full size:

- Cooked regions on the channels/grates are pale, sponge-like patches. A separate locked Cycles diagnostic with the channel bump disconnected (`renders/diagnostic-no-bump/construction.png`, also inspected) leaves the artifact intact: reflectance/mask scale is responsible. Replace broad channel patches with small food-drip spots, reduce the roughness contrast, and use gentler grayscale breakup on the grate cooking zones.
- The exposed-burner camera reveals heat-channel support tabs floating under the empty center of each V. Replace them with two continuous cast ledges, connected to the bowl walls, that meet the feet of all five channels.
- Burner tubes are too pristine/shiny for a used combustion chamber. Give their upper flame-port regions restrained heat tint and cavity residue.
- The original regulator reinforcing ribs are buried in the pressed dome. Place them on the actual piecewise cover profile; use a less diffuse zinc response so the rolled/crimped construction reads.
- The printed fascia loses its substrate's anisotropy when the print shader is created. Preserve coat, anisotropy and dielectric specular settings in the reusable print helper.
- Larger knobs partly hide OFF and the arc. Redraw the scale with correct physical X/Y print aspect and more clearance, and reduce the top wordmark size.
- Label-edge aging and corner lift were fixed at one intensity. Pass WEAR through original graphic generation and scale the lifted corner, so cleaner/dirtier variants remain one parameter.

These corrections are rebuilt for the final checkpoint-2 set. Remaining artistic
limitations are the stronger enamel hero reflection, very restrained fine
stainless scratches/fingerprints, and cleaner zinc/brass than the connected-tank
photograph. The source images are not identical lighting/configuration captures;
measured camera residuals and regional differences remain visible in the pairs.

## Final checkpoint 2 / handoff validation

The four polish previews in `renders/cp2-polish-preview/` were inspected before
regenerating the complete final checkpoint set. All 13 final Cycles views,
photo pairs and both requested contact sheets were opened. The small spots on
the channels change reflectance with viewing angle; the former large pale
camouflage regions are gone. The remaining limitations below are artistic,
not waived geometry audit failures.

- `make -C gas-grill WIDTH=1600 SAMPLES=112 PASS=checkpoint2`: passed. Thirteen 1600 px Cycles renders, OptiX on the GTX 1660, inside the shared GPU flock; reference fetch, source/game builds, audits, camera verification, comparisons and sheets completed.
- `make -C gas-grill check`: passed after the final render. Both source and game have finite geometry/normals, no zero-area slivers, manifold positive-volume solids (declared print/etched sheets excepted), correct bounds and documented pivots. UV/bake/export gates are explicitly pending.
- High source: grill **162,658** triangles / **27** used material sources; tank **38,134** / **8**. There are **32 unique** used materials across the two sets because some finishes are shared. All expose BaseColor, roughness, metallic and meter-height bake channels; the printed fascia retains its substrate anisotropy.
- Planned game geometry: grill **19,596** / 20,000; tank **3,876** / 4,000. Independent clean-scene repeats have identical geometry SHA-256 values: grill `c83eecb3fd3d…`, tank `a7a05b472072…`. All six generated markings also repeat byte-for-byte.
- Grill bounds: **1320.0 × 685.8 × 1130.3 mm**, against **1320.8 × 685.8 × 1130.3 mm**. Bare tank body diameter **312.42 mm**; full tank bounds **314.02 × 314.52 × 437.10 mm** including label/weld/rolled collar. Table-width comparison excludes the removable tank's approximately 4 mm side overhang.
- Camera fitter vs Blender API projection: maximum disagreement **0.00094 px**. Actual photo landmark RMS is **6.48 / 18.05 / 15.66 px** (closed / interior / tank). Estimated crop-camera lenses **104.9 / 30.7 / 127.3 mm** are not known source EXIF values.
- Workbench inspection caught reflection flags showing/casting shadows because that engine ignores Cycles ray visibility. Hide the flags for Workbench and use neutral clay with brighter exposure for readable geometry; Cycles/Eevee remain unchanged. Re-render and inspect both preview poses.
- Eevee hero smoke render at 1000 px / 64 samples and Workbench closed/open at 1000 px passed and were inspected. Eevee is grainier at this preview setting; it is not final delivery proof.
- Original look-dev blend: **2,939,230 bytes**; game source: **1,236,674 bytes**, both ignored. Two planned atlas materials, 2048 grill / 1024 tank, with BaseColor / Normal / ORM. No baked textures or GLB exist at this checkpoint.
- Pre-commit checks ran on the implementation commits. Repository checks pass with 34 source files and zero errors. There are no tracked images. Forced ignored output paths and JPGs outside final docs are now rejected by the shared checker.

Review outputs (all local/ignored):

| Path | Contents |
| --- | --- |
| `renders/checkpoint2/contact.jpg` | 2400 × 4656, 1,441,747 bytes; both heroes and all three photographed pairs |
| `renders/checkpoint2/construction-contact.jpg` | 2400 × 2215, 485,111 bytes; heat channels, exposed burner/igniter/drain, controls and connected cylinder |
| `renders/checkpoint2/dimensions-contact.jpg` | Published-envelope front/side review |
| `renders/checkpoint2/` | 13 original PNG renders, three pairs, calibration overlays, camera JSON and shot metadata |
| `renders/checkpoint2-eevee/`, `renders/checkpoint2-workbench/` | Engine smoke checks |

Still weakest: the source's extremely fine stainless grain/scratches and handling
marks remain restrained at this framing; zinc/brass look newer than the used
connection photograph; exterior grease tracks could be more individually
characterized; and the hero enamel reflection is broader/brighter than the
catalog source. Regional grate and opposite-side scale differences are deliberate
configuration differences, not exact photo matches. The source has substantially
more real construction now, but I am not claiming a finished photographic/game
asset before the lead's image review and bake/export validation.

No additional tools or installations are needed. The lead's next input is visual
review of these two sheets. Keep photo comparisons/residuals and image-free
checkpoints as a standing workflow for subsequent assets; larger future assets
can extend the same studio rig with scale/placement controls when first needed.

# Final scope / post-checkpoint-2 photo critique

Owner decisions #7/#9 remove the procedural cylinder and add a six-bone hose.
The canonical tank is an external, read-only fit reference. It is never loaded
by modeling, UV, bake or export scripts. Its measured foot-ring origin, 312.2 mm
body, 468.0 mm height, 175 mm collar, 210 mm foot ring and valve face at
(0, −41.9, 423.5) mm control the new socket and hardware.

Compared `renders/pre-bake-final/match_closed-pair.jpg` and
`match_interior-pair.jpg` with the same photographs/cameras used at checkpoint 2.
Also inspected the closed/open heroes, controls, exposed construction, canonical
fit and free-hose close-up in the pre-bake iterations.

Differences and corrections:

- No cylinder/valve/label geometry or tank material set remains. The hanger's J-hook now supports the canonical collar lip from below, and its lower cradle contacts the actual foot ring.
- The old straight black tether was a valve dust-cap tether. It belongs to the excluded cylinder, so both cap and tether are removed.
- The hood interior and bowl were too uniformly clean. Heat plumes now spread with height; carbon and flaking follow those plumes/cavities. Bowl buildup follows burner lanes, slope, gravity tracks and the drain pool.
- Round noise spots on heat tents looked artificial. Carbon now follows apexes and the three burner lanes; oil tracks descend the V faces. Tents 1/3/5 are directly above the burners. The combustion diagnostic intentionally removes them and is labeled accordingly.
- Burners still caught broad silver highlights. Their source is now hollow thin-wall tubing with real ports and air shutters; port-indexed soot blooms and a duller heat-tinted finish make the holes readable in the bake.
- Initial strengthened brushing was excessive and looked like broad stripes; its scale/contrast were reduced, and smooth chrome was separated from the brushed finish. Grain direction and the real hems remain visible.
- Moving the key and reducing the overhead card narrowed the enamel reflection substantially. The hood reads dark porcelain again rather than a silver front panel.
- Dust at the lower frame/feet, wheel shoulders and shelf, handled grip scuffs, front-lip and tray grease were strengthened with the existing wear scalar.
- A near-vertical pose exposed frame twisting in the hose chain. Rest/posed frames now use parallel transport. The manifold is pinned, fitting rigid on bone 6, and smooth two-bone weights blend the hose rings. Rest-frame metadata preserves the demonstration across glTF bone-frame conversion.

UV layout uses a single atlas with explicit importance weights. Structural and
hidden surfaces get less space than the hood, fascia, shelves, markings and
fitting. Original low print overlays are removed and projected onto their solid
backing during the high-to-low bake. Source print planes remain intact.

The final two calibrated pairs were opened again after the changes. The grate
layout still intentionally differs from the regional circular-insert photograph.
The interior now reads as carbon rather than flat gray; the used photograph has
more wet exterior grease than this lightly used configuration. Fine burner holes
are side-facing and remain a close-up/normal-map detail, rather than conspicuous
black top dots. The right shelf has a real hem and finer directional grain; the
remaining limitation is how much of that microstructure survives one 2048 atlas.
The final hanger inspection caught a floating scale backplate and a cradle bolt
inside the leg channel: two formed bridge straps now connect the scale to the
upright, and the cradle plate/bolt sit on the upright's outer face.

Prototype 512 atlas bake/export was used to exercise the entire path first.
Re-import found Blender's generated 80-triangle bone-display shape; checks and
final studio now exclude that display helper explicitly. Raw glTF inverse-bind
matrices are verified in glTF's world bind coordinates, independently of
Blender's bone-display orientation. All 49 hose cross-sections were exercised
using ordinary linear skinning; minimum radius 4.44 mm versus 5.20 mm rest.

Delivery polish inspection corrected two pipeline details before the clean
rebuild: imported lid pivots use quaternion mode, so the studio now explicitly
converts the lid to Euler mode before its hinge pose; and the moving grease
tray's heat/drip masks were rebased to its new local coordinates. The prototype
also exposed the generic tube helper's 40° smoothing threshold: eight-sided
round hose sections have 45° face angles and were being treated as hard facets.
Tube smoothing now accounts for radial tessellation while retaining hard end
caps. This improves coarse round sections without adding triangles.

The final GLB detail review caught one last real construction bug: the regulator
vent disk was 0.1 mm below its cover's flat label land. It now starts at 12.2 mm
in the cover frame, above the 12.0 mm land, rather than 11.5 mm. This restores
the visible dark vent in both source and game geometry without adding triangles.
The source/photo pairs are refreshed in `renders/final-photo/`; exported-GLB
images remain the only inputs to the final documentation sheets.

# Final delivery review and proof

All final GLB views and the refreshed source/photo pairs were opened. The last
polish pass fixed the buried regulator vent, round-tube smoothing, moving-tray
mask coordinates and imported-lid rotation mode. The fascia gained atlas space;
the free-hose pose distributes its untwist along the chain. Eevee now enables
screen-space ray tracing and higher shadow quality; it still differs visibly
from Cycles in metallic reflections. The combustion sheet explicitly labels
that all five tents are removed from the grouped GLB diagnostic.

Remaining artistic weaknesses: fine burner ports, fingerprints, small graphics
and regulator stamp relief soften in one 2048 atlas. Extreme control/handle
close-ups reveal coarse silhouettes and some baked-normal waviness. Carbon
breakup is still more regular than the incidental buildup in the used reference.
The hose is a checked demonstration pose, not a physics simulation. These are
reported limitations; no failed geometry, UV, texture or rig gates are waived.

Commands and results:

- `make -C gas-grill clean && make -C gas-grill`: passed, including the final vent correction; high/game generation, UVs, 4096 GPU bake, 2048 filtering, skinned GLB, imported-GLB studio, documentation and all checks. Subsequent `make -C gas-grill` regenerated the final studio after the Eevee quality/metadata update and passed again.
- `make -C gas-grill check`: passed. Real bounds, positive/manifold source solids, no slivers/invalid normals, budgets, camera projection, independent raw GLB + Blender re-import, UVs, textures, rig and canonical fit.
- `make -C gas-grill check TANK_REFERENCE=`: passed with the explicit optional-fit skip. A separate final-mode `studio.py --shots fit_check` with an absent reference also skipped clearly and produced no image. The default canonical fit report was then regenerated by `make`.
- `make -C gas-grill match PASS=final-photo WIDTH=1400 SAMPLES=48`: passed; both refreshed photo pairs inspected. Comparison pixels remain ignored and never enter material/bake inputs.
- `python3 kit/repo_check.py`, Python compilation and `git diff --check`: passed. The worktree-local pre-commit hook checks staged blobs; five final JPGs only, each 1600 px wide and below 200,000 bytes.

Delivery: **19,992 triangles**, one material and three 2048² PNGs; high source
**170,242 triangles**. Source game tessellation is 19,996 before the four
coplanar print-sheet triangles are removed. GLB **11,016,792 bytes**; BaseColor
**1,740,046**, Normal **2,922,246**, ORM **4,765,286 bytes**. No cylinder/valve,
cylinder marking or cylinder texture set is included.

UV coverage **49.62%**; UV-area-weighted density p5/median/p95 **294/559/1176
px/m**. No outside/degenerate UV triangles. Three numerical contacts total
**0.36 shipped texel²**, overlap fraction **1.73e-7**. Re-imported vertex normals
are unit within **1.2e-7**; authored weights return with **zero measured error**,
normalized sums and at most two influences. Bone names/hierarchy and raw inverse
binds pass; maximum bind residual **3.13e-7**, world rest-vertex error **0.000246
mm**, socket-matrix residual **3.87e-7**.

Six bones `Hose_01`…`Hose_06`, root fixed at the manifold; fittings rigid on the
last bone. All **49** hose rings tested in the free pose, minimum radius **3.86
mm** versus **5.20 mm** rest. Attachment travel **771.05 mm**; manifold error
**0.000030 mm**. `regulator_attach` is the authoritative mating frame.

Canonical fit: **312.2 × 312.2 × 468.0 mm**, collar **175 mm**, foot ring **210
mm**; origin at foot-ring bottom, +Z up, outlet −Y. Socket world **(451.5, 13,
198) mm**, yaw **50°**. Outlet local **(0, −41.9, 423.5) mm**, transformed world
**(483.597, −13.933, 621.5) mm**, outward axis **(0.766044, −0.642788, 0)**.
Coupling face error **0.000124 mm**, axes opposed on axis. Collar-hook contact
gap **0.0063 mm**; foot cradle/pads tangent to the 105 mm ring radius. Minimum
connected-hose clearance **25.44 mm**. The external file checksum is unchanged:
`27955562131121505d15234088412d64a250b5feaaf96314558454a1ba9f3a39`.

Final render records: **14 Cycles + 1 Eevee**, all 1600 px wide, all from GLB
SHA-256 `efbd8c056c09a99699fe7790c2f06bfdd67b253a06bdd950b70f3bec1b36c2a1`.
Every Cycles operation used OptiX on the GTX 1660 inside the shared flock.

- `renders/final/contact.jpg`: all views, including scale, canonical fit, free hose and Eevee.
- `renders/final/details-contact.jpg`: controls, open cookbox, construction and regulator.
- `renders/final/rig-contact.jpg`: free-hose pose and optional canonical fit.
- `renders/final/turnaround-contact.jpg`: front/side/back/top.
- `renders/final/*.png`, `renders/final-eevee/hero_closed.png`: original final renders.
- `docs/`: five bounded final JPGs; no source/reference comparison JPGs are committed.

No tools, installations or approvals are needed from the lead. For future
assets, keep the explicit source/game/delivery gates, photo residuals and final
GLB checksums. Extend tiling/alpha policies when those assets actually need them.

## Final targeted touch-up — 2026-10-26

The owner approved the pilot and asked for proportionate effort. This pass fixes
only the requested construction, reusable kit and documentation issues from
`.foundry/runs/grill-review.md`; the earlier delivery measurements above are
historical and are superseded here. Weathering, stainless, burner representation,
knob shading and the demonstration hose pose remain known limitations in README.

- The thermometer and badge now stack on the lid centerline. Orthographic front
  measurement: badge X error 0.0000037 mm, thermometer 0.0000009 mm; projected
  vertical gap 65.99 mm. `front-centering.jpg` overlays the measured axis on the
  exported-GLB front render. The composition reads as a coherent product header.
- Wheels move to Y ±290 mm with a longer axle, inboard mounting ears and thrust
  spacers. Their minimum axial gaps to the legs are 17.50 / 18.50 mm. Y rotation
  preserves those coordinates, proving leg separation at every angle, beyond
  the sampled 5° sweep. Only the intended hub/axle bore contact is allowed.
- The catch cup now has two folded hangers: 0.00 mm sampled tray gap and
  0.0288 mm cup gap. The hollow pan has a real 30 × 40 mm drain. Underfloor
  runners clear the drawer through its full 200 mm travel. The pulled-out GLB
  render exposes the pan floor; its former projected cookbox outline is gone.
- The hinge axis moves to world (−55.5, 294, 912) mm, with revised fork ears,
  connecting webs, relieved cap rear corners and cleared lower lips. Both high
  and game scenes pass 53 lid angles, every 2° from −104° to closed, at 0.5 mm
  penetration tolerance. No non-allowed penetration is reported. This is a
  sampled sweep, not continuous collision detection. Wheel, knob and drawer
  sweeps also pass. Knobs have a 3 mm bezel gap and coherent OFF 0°, HI −25°,
  LO −140° graphics/range. The obsolete colliding opening-stop cubes are gone.
- Actual closed envelope is 1320.0 × 715.8 × 1130.3 mm: the clearance changes add
  30 mm depth relative to the catalog. Fully open at −104°, connected rest hose,
  excluding the external tank: height 1570.2 mm, depth 916.7 mm. These authored
  open dimensions exceed the reference open-height callout; README says so.
  The open hero camera was pulled back to retain the raised handle in frame.
- The fit checker now samples actual cradle/pad triangles against the canonical
  tank, instead of subtracting nominal maximum radii. Measured minimum gaps:
  cradle 3.144 mm; pads 3.400 / 3.505 mm. These restrain swing and do not carry
  the tank's weight; the collar hook does. The owner GLB remains unchanged.

Kit additions are opt-in/backward compatible: `BAKE_POLICY` separates matching
high/low moving roots for projection and retains stationary contact AO with
independent rest-position shadow meshes; `MOTIONS` declares ranges, sample
spacing, tolerances and intended-contact reasons; naming, skin pose/radius,
texel-density bands, combustion dimensions and studio node/axis are parameters.
`kit/README.md` gives the next author examples. A source-consolidation test found
that Blender joins mutate shared mesh data; AO shadows now own independent mesh
copies, guarded by an assertion. Two development bakes made before that fix were
discarded. The fit checker also needed copied names before switching scenes;
that verification error was fixed before the passing build.

The generic solid checker fails the old audited scene for the reported wheel,
lid and drawer collisions (`build/motion-regression.json`). Small checked-in
fixtures pass for penetration, tangency, containment, a hollow cavity, legacy
asset tags and a non-grill three-bone rig (`kit/test_policy.py`). New declaration
options retain the original defaults, so existing asset callers do not need edits.

Final game delivery: **19,912 triangles**, **171,390 high-source triangles**,
one material and one 2048² BaseColor/Normal/ORM set baked at 4096² on OptiX under
the shared lock. Packed coverage **46.45%**; density p5/median/p95
**279/549/1140 px/m**. Three numerical contacts total **0.34 shipped texel²**;
no outside or degenerate UV triangles. Re-import verifies names, hierarchy,
weights, rest vertices, sockets, normals and the six-bone hose pose.

Reviewed the exported heroes, all views on the contact sheet, orthographic
centering overlay, withdrawn pan and underside support close-ups. The header,
axle separation and supported cup fixes are visible. Remaining weaknesses:
procedural carbon mottling, pale/granular stainless, subtexel burner ports,
coarse/wavy controls and the hose's stiff twisted demonstration pose. These
are retained deliberately within the owner's final scope.

Numerical repeat proof on two current 4096→2048 isolated bakes:
`python3 kit/compare_textures.py --reference build/touchup-repeat-reference
--candidate gas-grill/textures/ship --out gas-grill/build/texture-repeat.json`
passes. BaseColor/Normal/ORM changed 8/27/18 channel values, maximum delta 1,
worst byte-domain RMSE 0.001465. Accepted limits are delta 2 and RMSE 0.02;
byte identity is not promised. Final GLB **10,439,228 bytes**, delivered PNGs
**1,645,778 / 2,693,421 / 4,489,710 bytes**.

Accepted build commands and results:

- `make -C gas-grill` — PASS (`build/touchup-camera-make.log`): affected source,
  packed low mesh, 4096 GPU bake, downsample, GLB, 16 Cycles views, Eevee,
  contacts/docs and all checks. The open hero now includes the full handle.
- `make -C gas-grill check` — PASS (`build/touchup-last-check.log`): budgets,
  bounds, topology/normals, UVs/density, camera calibration, GLB re-import,
  six-bone skin/weights/pose/sockets, external fit, both motion sweeps,
  construction measurements and repository rules.
- `blender -b --factory-startup --python-exit-code 1 --python kit/test_policy.py`
  — PASS. Numerical repeat comparison — PASS as recorded above.
- `python3 kit/repo_check.py` and `git diff --check` — PASS. Five final docs JPGs
  are 1600 px wide and 118–190 KB each; no generated asset/reference is tracked.

All 17 final render records match current GLB SHA-256
`0bde8373c76eb6fa32504f6be29136f8cebe909475b2428d4b51464fdd92c4f8`.
Images: `renders/final/contact.jpg` (all), `details-contact.jpg`,
`rig-contact.jpg`, `turnaround-contact.jpg`, `front-centering.jpg`, individual
`renders/final/*.png`, and `renders/final-eevee/hero_closed.png`. Final committed
JPGs: `docs/hero-closed.jpg`, `hero-open.jpg`, `details.jpg`, `rig-fit.jpg`,
`turnaround.jpg`. No further tools or lead action are needed for this touch-up.
