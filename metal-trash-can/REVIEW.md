# Galvanized garbage can review

## Construction checkpoint

Observed the manufacturer-supplied photograph at `refs/can-front.jpg`, and four 800 px Workbench views in `renders/shape/`, all individually opened. Silhouette and shallow lid read as the intended can. Failures found: initial lid was unsupported above the mouth; bracket corners floated from the curved wall; handle motion signs turned the loops inward; the interior view hid the empty rather than its descendants. Corrected the seating shoulder to meet the actual rolled-mouth profile, wrapped brackets onto the wall, added folded retaining-eye necks, reversed rotation signs, and used assembly hiding. The floor now has a flat elevated underside and an enclosing chime instead of a thick conical closure.

Final material and exported-GLB comparisons remain to be judged; Workbench is construction evidence only. Initial source count 8,888 exceeded the brief. Removed hidden subdivisions, put minor beads in the normal bake, and preserved structural cross-sections consistently between high and game sources. Revised game source is 4,896 triangles, manifold solids and valid coordinates/normals under the independent scene audit. No kit files changed.

## Material and photograph critique

Opened every image in `renders/pass1/` (hero, lid, side handle, interior): the first zinc response was too bright and chalky and blurred the flute definition. Reduced zinc albedo and roughness, constrained oxide haze, and marked the manufactured flute changes sharp enough to read as pressed sheet. Opened all four revised source images and `renders/pass2/match_front.png`, its photographic pair and calibration overlay. The revised can has a credible metal response and readable flute structure. Relative to the new reference can it has more weathered spangle, simpler rolled stiffening beads and an original bridge handle. It intentionally has no product label or patented lid shape. Camera fit is approximate: RMS 13.43 px at 600 px, estimated lens reaches the 180 mm bound; projection agreement is 0.00039 px. This is a broad proportion/construction comparison, not a camera-calibrated replica.

A floating straight rear seam was caught in the interior image and replaced by a folded strip following the actual tapered/corrugated wall. All changes remain asset-specific. The integrated motion checks pass on high and game at 61 lid positions and 49 positions per side handle: maximum seated-rim penetration 0.4575 mm at a 0.5 mm tolerance, and no handle penetration. Bearing contacts alone have named reasons. A separate source-contact check measures zero nearest lid/rim gap, a 0.6500 mm floor gauge, and 20 eye/neck triangle crossings per retaining eye. These prove construction; the export verifier separately proves serialization.

The final carrying-wire ends now include actual Y-axis stubs passing through the retained eyes, rather than ending perpendicular to their bore. Repeated the two source motion sweeps and actual-surface contact checks after this correction: all pass. Final game count is 4,928 triangles. The atlas has 56.77% coverage, no measured overlap/outside/degenerate UV triangles, and 406 / 448 / 471 px/m p5/median/p95. Final body envelope including handles is 563.784 × 533.400 × 755.650 mm. The corrected seam follows the sheet and both source qualities share the structural triangulation.

## Exported bake correction

Opened all ten first exported Cycles views. They exposed repeating black triangles at lower flute terminations even though every projected bake channel reported zero missed interior texels. Rejected these images. A 1024/8-sample small-cage probe eliminated the black areas but left an outline; opened the Eevee probe. The projection cage was larger than the 0.65 mm sheet and could cross its opposing surface at the flute transition. Removed overlapping high-only bead shells and expressed these minor pressed beads in the shared authored shader height. Final cage is 0.20 mm, ray distance 4 mm.

Because structural high/game shells match, `src/bake_normal.py` bakes the shared original manufacturing shader on the actual game shell with selected-to-active disabled. This avoids cross-wall normal projection; it does not repair or paint over bad texels. Other channels retain kit isolation and stationary contact AO. Opened the 1000 px Cycles GLB probe using this direct tangent normal: the black band and residual outlines are gone, with zinc, flutes, subtle pressed relief and dents preserved. Final normal is also baked at 4096 and delivered at 1024; an independent eroded UV mask asserts zero missing interior samples. No kit edits were needed for this asset-specific projection choice.

## Final delivery: PASS

`make -C metal-trash-can` and `make -C metal-trash-can check` exit 0 with the corrected production bake. Both topology/scale audits, independent UV/normal checks, fresh GLB re-import, camera projection, repository rules, high/game motion sweeps and actual-surface contacts pass. The delivered GLB has 4,928 triangles, one material, four mesh objects and 2,795,164 bytes. SHA-256: `2bae221354fd6f5b24ecae91ce69f3799c40cf67af6478b077fc444bbda23582`. All three textures are 1024²: BaseColor 947,574 bytes, Normal 333,714, ORM 1,257,198; approximately 4 MB block-compressed residency including mipmaps. Re-imported geometry and pivot errors measure 0; raw vertex-normal unit error is 1.1921e-7. UV coverage 56.77%, overlap/outside/degenerate counts 0, density 406/448/471 px/m p5/median/p95.

Baked at 4096/32 samples, OptiX. Projected channels and the separate direct-normal pass have zero missed interior samples over 9,239,613 independently checked texels; BaseColor also has zero black interior samples. The direct normal took 184.60 seconds. Moving-part isolation has four groups and ten stationary AO occluders; source masks remain in each part's rest coordinates.

Individually opened all ten corrected final Cycles images (closed hero, lifted lid, four orthographic views, lid detail, wire/eye detail, interior, 1.8 m scale), the Eevee hero, the final exported photo render and pair, the refreshed source photo render/pair/overlay, all three docs and the contact sheet. All 12 final metadata records identify the current GLB hash. No black projection band remains. The first Eevee image lacked environment capture and made bare metal almost black; `src/eevee.py` adds an original procedural studio SPHERE capture. Opened the corrected Eevee image: zinc now reads consistently with Cycles without changing any delivered surface or texture.

Final contact sheet: `renders/final/contact.jpg`; exported photo pair: `renders/photo-final/match_front-pair.jpg`. Docs: hero 1600×809 / 67,041 bytes; turnaround 1600×1700 / 194,163; details 1600×2911 / 186,696. The exported comparison preserves proportions, corrugation and weathered zinc but loses some micrograin and pressed-bead sharpness at 1024. Dents and hems remain simpler than a close-up battered real can. Orthographic transparent views lose the bright floor reflections and look darker than the perspective hero; this is lighting, not a material swap. Camera match remains approximate as disclosed above. These are the weakest areas; no unresolved construction or budget failure remains. No lead input needed.


## Phase 2 combined-kit regression

The initial clean `make` failed in the existing Eevee reflection-capture wrapper:
`captured_studio() got an unexpected keyword argument 'backdrop_height'`.
The shared studio had begun forwarding an absent backdrop override as `None`.
Kit commit `1c93019` omits that absent keyword, retaining explicit height/scale
settings and the existing zero-argument hook. The focused main-entry fixture
checks both paths with rendering mocked and asserts that it creates no image.

Resumed `make` and `make check` both passed after the kit correction (logs
`../build/polish/metal-regression-repair-{make,check}.log`). The clean baseline
remains 4,928 triangles / one material / 2,795,168 bytes, versus 2,795,164 in the
README. Opened the committed/new hero comparison, full final contact including
the repaired reflected Eevee view, and the original construction photo pair.
Metal response, lid/handle poses and framing agree; no visual regression remains.
The requested stronger use-weathering is a separate material-only correction.

First used-weather checkpoint: opened source and exported pairs
`renders/wear-pass1-{source,glb}/used_estate-pair.jpg`, the full hero and all
six side/detail probes. The oxide survives the 1024 bake, but rejected its
excess coverage: the lid and body read almost white and uniformly mottled,
unlike the used outdoor reference's dull zinc, broken white deposits and
localized wet-joint rust. Reduced the oxide layer and sparse-spot coverage;
required retained-rain exposure for cavity oxidation instead of whitening
every flute. Kept the cause-located rim/seam rust and made handling/low skirt
dirt darker. The first check passed (4,928 triangles / one material /
3,678,356 bytes); this is not yet the accepted finish. The used-reference
camera residual is 18.01 px; its lid/handle construction differs intentionally.

Second used-weather checkpoint: opened both source/exported used-estate pairs,
the full hero, four orthographic views and lid/handle details. Accepted the
reduced oxide coverage: zinc still reads gray metallic sheet, with broken
white deposits, dull exposure response, early orange rim/seam corrosion and
dark low/handling dirt visible at hero distance. The brighter studio highlights
and original lid/handle shape differ from the shaded reference; this is not
a battered replica. All wear stays in the existing 1024 atlas.

`make export check` passes: 4,928 triangles, one material, four movable/static
mesh parts, 3,485,008 bytes; maps 1,274,044 / 327,667 / 1,626,619 bytes. Final
full studio/Eevee regeneration follows this accepted material checkpoint.
