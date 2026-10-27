# Foundation shrubs / boxwood look-dev checkpoint

These are source look-dev renders, using original 4096 analytic fields filtered
to the proposed shared 2048 set. No final GLB/bake or delivery acceptance is
claimed. Photographs are local ignored comparison evidence, credited in refs.

## Pass 1 — reject color, perched ball and lost basal stems

Evidence: all seven `renders/pass1/*.png` presentation/diagnostic images opened,
plus both `match_*-pair.jpg` comparisons and preview front/side.

**Color and value first:** the leaves are visibly blue/cyan and too dark beside
both photos. Selected green display luminance p5/median/p95 is
.045/.167/.381 in the Green Velvet camera, versus .100/.321/.539 in the
photo's interior patch. The clipped comparison reads .049/.170/.387 versus
.131/.260/.413. These are different populations/specimens/lighting, not albedo
calibrations. Zero selected-green clipping does not excuse the hue error.
The procedural sky also turns neutral grade/wood blue, so correct illumination
before pushing leaf albedo. Glossy reflections should be local, not a cyan wash.

The candidate reads as a small topiary tree: tapering lower sphere, one visible
pole, and a conspicuous gray polygonal soil plate. The rooted union discarded
six independent basal stems because they were not actually connected. Fine
branches from those discarded parents remain visibly unsupported in structure.
Reject this construction; make all basal stems share a real connected stock,
measure attachments, and preserve the seven leaders. Broaden the lower skirt
and compress its underside into a mound while retaining bare low forks.

Long ladder-like shoots are too obvious. The outer silhouette has sparse fern
spikes with overly regular leaf pairs. Keep opposite botany but vary projection,
axis length, internode spacing and shear-tip foliage. The 1 m camera is too
close for its focal length and clips the object; show a true 1 m near-surface
leaf detail with a deliberately documented field, not a whole shrub close view.
The clipped photo render clips the root patch at the bottom; its framing is
invalid evidence until padded/reframed. Initial 4,131 triangles are within budget;
counts do not compensate for these failures.

## Pass 2 — reject open shell; connected stock and hue improve

Evidence: all seven views on `renders/pass2/contact.jpg`, full-size leaf/base/
structure images and both padded pairs opened. The new neutral margins retain
fit projections and reveal the complete model; both references remain unchanged
inside their canvases.

**Color and value first:** desaturating the procedural sky removes the cyan
wash from leaves, wood and ground. The foliage is now plausible muted green,
but the main reference is warmer and has a brighter middle population. Do not
brighten the whole scene or add emission: increase the blade's green modestly,
keep brown shaded leaves local and preserve the darker underside. Gloss is
still overly broad/matte in the 1 m view; refine after coverage is correct.

The seven basal leaders now join through real stock and the structure diagnostic
has no missing parents. Measured visible foliage spans .993 × .941 m, top .898 m,
with its lowest retained leaf at .138 m. The complete mesh is 1.042 × .987 × .905 m.
However, the shell is visibly too open: large bright see-through holes near
its center and a round lower taper still suggest a decorative topiary. Reject.
Concentrate more of the existing shoot sites at the outer shell, use three
orthogonal planes per shoot instead of two, and make denser short lateral sprays.
A modest triangle increase is justified by coverage at street distance.

The basal soil still looks like a smooth stone plate. Give it original granular
soil/mulch response and an irregular feathered edge inside the same opaque
material. New shoots need their UV V axis aligned to growth instead of relying
on the global up projection. Leaf cards repeat at close range; their size is
within the brief, but projection and shorter varied branch axes need to break
the repeated ladders. At 4,079 triangles this source is a useful rejected stage,
not a look acceptance.

## Pass 3 — hue and mound improve; reject remaining bright windows

Evidence: all seven images on `renders/pass3/contact.jpg`, full-size leaf/base,
three-quarter and both padded pairs opened.

**Color and value first:** warmer blade green is much closer to the primary
photograph than the cyan first pass, and the underside is dark. The close-up
still reads too matte and too uniformly lit, with insufficient waxy roll-off
on individual blades. Restore a stronger dielectric highlight and modestly
lower roughness under the neutralized daylight, then judge highlights rather
than assuming the brighter green alone solved realism.

The denser sprays and three directions improve the clipped mass. Large bright
windows still cross the middle; the photos show dense, dark interior foliage
rather than background. Add a small inner population, plus short lateral sprays
in unused tile space, instead of adding more outer shell sites. No opaque
ball is allowed as an occluder. Preserve shallow pruning lobes and the low
shaded thinning. All added coverage must stay within 6k triangles.

The soil normal field looks quilted in the macro and the low stem UVs enter
its dark strip, creating a sharp brown band. Separate their UV ranges and use
fine low-amplitude granular normals on soil. The basal stock now has seven
visible leaders but needs an independent attachment/closed-wood audit; the
combined soil sheet's allow-boundary flag is too broad a check exemption.
Move the soil sheet to its own source mesh so the woody solids are audited.
Reframe the 1 m camera at an exact 1 m target distance, with a downward angle
that removes the staging horizon. The second photo is lower quality and a
different cultivar; use it for the clipped mass, not detailed blade identity.

## Pass 4 — corrected source checkpoint and stop

Evidence: every current PNG under `renders/checkpoint/` opened, both full photo
pairs, `contact.jpg` and `review-sheet.jpg`. Nine GPU Cycles renders at 1200 px /
40 samples. The 1 m view has an actual camera-to-target distance of 1.000 m.
The scale view uses the unchanged kit 1.8 m silhouette. No docs JPGs committed.

**Color and value first:** primary-camera selected green display luminance
p5/median/p95 is **.073/.310/.561**, versus **.100/.321/.539** in the photo's
interior patch. Median hue **103.28° / 103.53°**. No selected-green channel clips;
**.52%** lies below .02 display luminance. The original cyan wash is gone and
individual waxy highlights now roll off. Model shadows are deeper and highlights
slightly brighter than the primary photo. The second comparison is **.076/.319/
.564**, photo **.131/.260/.413**, with hue **103.02° / 94.74°**: that model view
is brighter and less yellow than this other cultivar's low-resolution photo.
Do not claim both lighting situations or cultivars are exact matches. Statistics
compare different display-image populations, not calibrated albedo.

The inner leafy population and denser short lateral sprays close the largest
bright central windows without adding an opaque ball. Shallow lobes and uneven
shoots interrupt the clipped mound, and low +Y leaves include brown/olive older
growth with less coverage. The lower skirt is broad rather than perched on one
stem. Some small gaps survive, particularly from the shaded side. The silhouette
is still more regular and the leaf sprays less upright/interlocked than the
Green Velvet photo; the 1 m view exposes repeated planar leaves. Those remain
limitations for lead review, not passed photorealism claims.

The first stricter wood audit rejected the core's **negative signed volume**.
Normal recalculation after the tiny grade cap had selected its inner orientation.
The source now measures volume after capping and flips inward faces before
saving. Both independent builds pass zero nonmanifold edges and positive
**0.00085624 m³** total wood volume. All **35 actual four-vertex daughter-base
centers** lie inside the actual primary surface by all three ray tests, with
nearest primary surface **1.47–6.23 mm** inward. This proves embedded bases,
not that all fine attachment caps are Boolean-unioned. The economical closed
fine sweeps still have hidden internal cap faces. No per-sprite twig-continuity
proof is claimed.

Soil has its own source mesh and no longer exempts the wood from manifold
checks. Its granular field is less quilted and the stem UVs no longer enter its
dark strip. The thin polygonal patch edge is still conspicuous in the base macro;
a softer bed transition is needed for final delivery. Basal wood remains angular
at this close distance. Shading and form, rather than pass counts or budgets,
remain the review decision.

### Proof of this checkpoint

- **`make -C shrubs`: passed**, complete source checkpoint, source/game audits,
  botanical checks, camera projection verification, nine Cycles views, pairs,
  contact and value/provenance reports. Every Cycles operation held the shared
  GPU lock. **`make -C shrubs check`: passed** explicitly afterward.
- **4,893 triangles**: **3,794 leaf / 1,082 wood / 17 soil**; **1,897 alpha cards**,
  **two materials**, **three source meshes**. Opaque wood/soil consolidation is
  final-delivery work. No moving parts or armature.
- Actual retained foliage **1.02109 × .98092 m**, bottom **.11181 m**, top
  **.88021 m**. Complete card-corner envelope **1.10102 × 1.03837 × .90659 m**.
  Origin on grade; numerical lowest Z is −3.4e−9 m. Bounds use actual alpha
  texel-center support on actual quads, not authored envelope constants.
- Original 4096 fields filtered to shared **2048² BaseColor-alpha / +Y Normal /
  ORM**. PNG bytes **654,733 / 1,290,223 / 134,896**; packed source
  **2,276,380 bytes**. Planned full-mip BC7/BC5/8-bpp ORM allocation **16 MiB**
  for both shrubs together, excluding geometry/engine overhead. Upper-right
  atlas space remains reserved for hydrangea.
- Independent source/game geometry SHA-256 agrees:
  `7d5127eb3d2dd31104c5947175ec89e1e459e094283c978a509957dc073ec55c`.
  Wind values finite/normalized and zero-sway at grade; actual normals unit;
  alpha UVs remain in their declared lower-half tiles. Card density
  **3,701–3,910 px/m** at the proposed delivery size. Unique final stem UVs,
  final bake and GLB checks are deliberately pending.
- Both anatomical fits retain their estimated-lens RMS **16.11 / 18.78 px**;
  independent Blender projections agree to **.00011 / .00029 px** after framing.
  Different living specimens and uncertain anatomical anchors limit the fit.
- All nine image metadata hashes match current source SHA-256
  `b7ac0d897901d097cc2430d5af3aac3227d227e62e879d0b90925e3d79413e65`.
  `renders/checkpoint/render-check.json` certifies source provenance only.
- Current images: `renders/checkpoint/{three_quarter,side,close_1m,scale,base,
  shaded_side,structure}.png`, `match_{green_velvet,clipped}-pair.jpg`,
  `contact.jpg`, `review-sheet.jpg`, `tonal-check.json`, `shots.json`.

### Shared kit changes and compatibility

- `7458a56`: move the maple thin-leaf material into `kit/foliage.py`, with
  optional species gloss/transmission/back-color controls. The original maple
  default graph's nodes, links, values and properties have an identical golden
  byte snapshot; `kit/test_foliage.py` passes.
- `2aded7e`: move the maple comparison framer to `kit/photo_frame.py`. Its
  original default JSON and generated PNGs compare byte-identical; optional
  vertical margins preserve camera projection. The maple's wrappers retain
  existing entry points. **No change to `kit/rules.mk`.**
- Full maple source rebuilt twice, with pre-extraction and current material.
  Exact positions, triangle indices, corner normals, UVs and Wind share digest
  `01a3f2577af1c5635cf2796aa3916ca2fc8ae9dc5819fa7fdc3aeee0490a2967`;
  all three analytic atlas PNG SHA-256 values also agree. Evidence:
  `../build/maple-extraction-regression.json`. This is full source/content
  compatibility; GPU rebake/export was not repeated and is not claimed byte-identical.
- `kit/test_botany.py`: passed both union component policies and optional normal
  defaults. `python3 -m unittest kit.test_delivery`: **six tests pass**.
  Repository rules and `git diff --check` pass.

Stop here as requested. Hydrangea botany/reference photos are researched but no
hydrangea geometry is built. Final unique UVs, GPU stem bake, GLB/re-import,
wind serialization and exported-GLB renders remain held. No tool or permission
is needed; the lead's review of this boxwood checkpoint is the next decision.
