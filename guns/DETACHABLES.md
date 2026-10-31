# Standalone detachable mipmap delivery

All twenty-one standalone items across seven guns now fit **512 or 1024 at
density ratio 1.000**. The previously oversized magazines and the Rill 39
magazines fit losslessly by moving atlas neighborhoods;
no 2048, reduced-density export, rebake, rotation, mirroring or resampling is
needed. The original subset-only exports kept main gun GLBs byte-identical. The later
[Vesper feed correction](bolt/README.md#feed-geometry-correction) intentionally
changes its geometry, clips and baked atlas; its subsets retain full density.

## Sampler, atlas clusters, gutters and fill

Every standalone set matches its gun: `minFilter=9987`
(`LINEAR_MIPMAP_LINEAR`), `magFilter=9729` (`LINEAR`), and repeat wrapping
(implicit glTF defaults). Retain these imported material samplers.

`texture_clusters=True` / static `EXPORT_TEXTURE_CLUSTERS=True` selects the
kit’s atlas-neighborhood path. Connected components join islands whose
**6 px guarded sampling masks touch or overlap** in the original 2048 atlas.
Internal texels, including the atlas’s existing margins and nonmember texels,
are **kept exactly as copied**, rather than separately dilating every island.
Each source region receives one complete protected mip block of original atlas
halo: **8 px minimum through mip 3**, rounded outward to that grid. Source and
destination borders share the grid; integer translations preserve mip phase.
Destination regions and their outer guards are disjoint.

Oversized components split around whole islands, along the atlas’s empty
margins. A band accepts an island only when its complete vertical extent fits;
the seam detours around islands crossing the nominal band boundary. Each part
copies its bounding rectangle and halo. **Source crops can overlap**, retaining
duplicate nonmember atlas texels at their borders; UVs reference each island
only in its assigned part. No rectangle edge clips a moved island. Measured
minimum cross-region island bounding-box separation is 2.45752 px for the loaded
pistol and 1.47449 px for both bolt magazines, confirming empty margins between
the assigned islands. `build/clusters/split-audit.json` records the measurements.
In that original subset-only delivery, pistol loaded had one source cluster
→ two regions; bolt empty five → six and bolt loaded one → two. The later
Vesper geometry revision uses the updated counts in the table below.

A masked pull-push fills every texel outside the copied regions. RGB averages
in linear light; alpha/ORM are linear data. Generated normal texels normalize
before quantization. All copied texels, including original atlas normals in
margins, remain byte-exact. At deeper unprotected levels the retained atlas
neighbors and the new set’s tail can still mix, as in the source atlas.

The same path was evaluated for the fourteen accepted items. Eight produce
smaller files and use it. Six cluster candidates are larger: pistol empty,
SMG empty/loaded and all three revolver items keep their accepted PNGs and UVs
exactly. Their existing isolated-island guards remain 6 px for magazines or
8 px for the revolver, aligned to the mip grid and dilated from their own
islands; pull-push fills outside. The full pistol export changes only the empty
magazine’s mesh/material names versus its earlier single-entry staging export
(+4 JSON padding bytes); its binary payload and all three PNGs are identical.
`build/clusters/candidate-bytes.json` and `retained.log` record this selection.
No candidate reduces an accepted 1024 allocation to 512 at full density.

## Per-item results

One material / three maps per item. Geometry, normals and origins were unchanged
by the subset optimization; the later Vesper correction updates its magazine
construction and spawn frame as documented in its own README.
“Atlas clusters” counts connected guarded neighborhoods in the source atlas.
“Packed regions” counts delivered guarded regions: an accepted island-packed
map uses one per island, marked **i**. Other region counts are copied atlas
neighborhoods after any split. “Old bytes” means the original full-atlas GLB; new bytes are
exact final embedded GLB bytes. Gutter values are minimum outer pixels.

The test builds box-filtered mip chains for the atlas, the new set and the same
island alone, dilated without limit. At ten common points per triangle it
measures maximum absolute component error in linear RGBA / encoded normal /
linear ORM. **Every point, map and level must satisfy new error ≤ atlas error
+ 1/255** (0.00392157). “Excess” below is the worst pointwise new-minus-atlas
error at each level, rather than a difference of aggregate maxima. Values below
1e-12 round to zero. The smallest-island two-texel cutoff is mip 0 here; all
items are deliberately tested through mip 3. The kit’s larger-island fixture
also tests through mip 6. Base-level surface copying uses 0.25/255 tolerance;
float UV storage is separately bounded to 0.001 delivered pixels and tangent
direction to 0.5°. No scaled-item tolerance/test is needed: nothing scales.

| Gun / item | Map | Atlas clusters | Packed regions | Density ratio | Gutter | Old bytes | New bytes | Excess L0 | Excess L1 | Excess L2 | Excess L3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pistol/case | 512 | 1 | 1 | 1.000 | 8 | 5,204,740 | 235,932 | 0 | 0 | 0 | 0 |
| pistol/magazine_empty | 1024 | 5 | 207 i | 1.000 | 6 | 5,362,360 | 991,516 | 0 | 0 | 0 | 0 |
| pistol/magazine_loaded | 1024 | 1 | 2 | 1.000 | 8 | 5,396,292 | 1,318,548 | 0 | 0 | 0 | 0 |
| shotgun/hull | 1024 | 1 | 1 | 1.000 | 8 | 8,244,008 | 404,136 | 0 | 0 | 0 | 0 |
| shotgun/shell | 1024 | 1 | 1 | 1.000 | 8 | 8,260,472 | 364,784 | 0 | 0 | 0 | 0 |
| bolt/case | 512 | 1 | 1 | 1.000 | 8 | 6,753,080 | 201,536 | 0 | 0 | 0 | 0 |
| bolt/magazine_empty | 1024 | 7 | 7 | 1.000 | 8 | 6,928,816 | 1,165,896 | 0 | 0 | 0 | 0 |
| bolt/magazine_loaded | 1024 | 2 | 2 | 1.000 | 8 | 6,997,748 | 1,134,900 | 0 | 0 | 0 | 0 |
| smg/cartridge | 512 | 1 | 1 | 1.000 | 8 | 7,359,568 | 151,444 | 0 | 0 | 0 | 0 |
| smg/case | 512 | 1 | 1 | 1.000 | 8 | 7,360,256 | 154,940 | 0 | 0 | 0 | 0 |
| smg/magazine_empty | 1024 | 7 | 373 i | 1.000 | 6 | 7,476,900 | 1,186,756 | 0 | 0 | 0 | 0 |
| smg/magazine_loaded | 1024 | 1 | 531 i | 1.000 | 6 | 7,549,888 | 1,318,624 | 0 | 0 | 0 | 0 |
| revolver/cartridge | 512 | 32 | 36 i | 1.000 | 8 | 6,307,544 | 74,972 | 0 | 0 | 0 | 0 |
| revolver/case | 512 | 18 | 27 i | 1.000 | 8 | 6,304,652 | 75,764 | 0 | 0 | 0 | 0 |
| revolver/speedloader_loaded | 1024 | 45 | 392 i | 1.000 | 8 | 6,513,196 | 654,268 | 0 | 0 | 3.3361024e-05 | 0 |
| lever/cartridge | 1024 | 1 | 1 | 1.000 | 8 | 7,216,192 | 492,544 | 0 | 0 | 0 | 0 |
| lever/case | 1024 | 1 | 1 | 1.000 | 8 | 7,197,348 | 516,876 | 0 | 0 | 0 | 0 |
| ak/magazine_loaded | 1024 | 1 | 2 | 1.000 | 8 | 7,704,908 | 1,534,300 | 0 | 0 | 0 | 0 |
| ak/magazine_empty | 1024 | 4 | 5 | 1.000 | 8 | 7,616,752 | 1,462,396 | 0 | 0 | 0 | 0 |
| ak/cartridge | 512 | 1 | 1 | 1.000 | 8 | 7,496,472 | 164,864 | 0 | 0 | 0 | 0 |
| ak/case | 512 | 1 | 1 | 1.000 | 8 | 7,484,152 | 149,668 | 0 | 0 | 0 | 0 |

Final total for all twenty-one: **146,735,344 → 13,754,664 bytes**,
**90.63% smaller**. The Rill 39 contributes **30,302,284 → 3,311,228 bytes**
(89.07% smaller); the other seventeen now total 10,443,436 bytes.
The current geometric total is **54,064 triangles**, with **540,640** base
surface samples. The Vesper revision adds twelve triangles per magazine; its
historical full-atlas byte baseline is retained in the Old bytes column. Eight sets are 512 and
thirteen 1024: about **60 MiB total** at 8-bpp block compression with full mip
chains, versus about 336 MiB for twenty-one separate 2048 sets. Each magazine
costs about 4 MiB; no inter-file texture deduplication is assumed.

Full density percentiles, per-channel/base errors, per-level atlas/new errors,
pointwise excesses and sampler records for the first seventeen:
`build/clusters/proof.json`; the four Rill 39 entries are in
`guns/ak/build/delivery/verify.json` and `build/ak-detach/proof.json`.
The largest excess is **0.0000333610** at mip 2 on the unchanged revolver
speedloader, below 1/255. Cluster-copy excesses are numerical noise below 3e-14.

## Render pairs

All seventeen full-size, native distant and magnified distant comparisons were
opened and reviewed. Gallery: `build/clusters/pairs/index.html`; contact sheets:
`distant-contact-1.png`, `distant-contact-2.png`, and `magazines-distant.png` in
that directory. The three requested magazines are under:

- `pistol/magazine_loaded/full-pair.png`, `distant-pair.png`, `distant-texels.png`
- `bolt/magazine_empty/full-pair.png`, `distant-pair.png`, `distant-texels.png`
- `bolt/magazine_loaded/full-pair.png`, `distant-pair.png`, `distant-texels.png`

Left is the original gun atlas; right is the final exported standalone GLB.
`guns/common/detachable_mip_review.py` uses actual raw GLB triangles, explicit
linear-light box mip chains, derivative-selected trilinear LOD and repeat
wrapping. Full coverage is about 570 px; distant coverage about 40 px, rendered
natively rather than reduced from the full shot. Nearest magnification exposes
those same distant texels. Per-item provenance includes input/renderer SHA-256,
LOD range and coverage; `build/clusters/render-provenance.json` was checked
against the final GLBs.

The magazines retain sidewalls, ribs, witness holes, feed-lip/follower cavities,
base lips and ammunition response. Deep tail differences are small. Original
faceting, soft headstamps and the SMG’s strong wear remain. Review notes:
`build/clusters/visual-review.md`. These are analytic-GGX sampling diagnostics,
not new photographic studio renders or a temporal/runtime-engine integration
test. No docs JPG was regenerated or changed.

## Checks and preservation

Every `kit/test_*.py` passed: **23/23** from clean fixture outputs, Blender for
bpy fixtures, unittest for Python fixtures, and `kit/with_gpu.sh` for the three
bake fixtures. Commands/results: `build/clusters/kit-tests.json`; logs:
`build/clusters/kit-logs/`. The extended detachable fixture proves connected
neighborhoods, an oversized split around intact islands, full atlas-region
byte copying, overlapping source halos, deterministic maps, main identity,
base sampling and per-island mip bleed. Prior sampler/background negative
cases, the dense 6 px fallback and mip-6 fixture still pass.

All six guns passed their complete `make check`: pistol, shotgun, bolt, SMG,
revolver and lever. Commands/results are in `build/clusters/checks.json`; logs
are `<gun>-check-final.log` (pistol: `pistol-check.log`). Interrupted intermediate
bolt/shotgun attempts were repeated to completion. All six `make export` paths
completed and all six main hashes match the original
baseline; `build/clusters/exports.json` records the final hashes. The shotgun
needed one additional exact-signature tangent anchor for a 0.0001 rounding
change; the existing kit correction guards position/normal/UV/tangent signature
and rejects a larger delta. No source geometry or canonical map was changed.

The final preservation manifest is `build/clusters/checkpoint.json`: main GLBs,
canonical PNGs/finalized sources, all 111 tracked docs JPGs, retained maps,
independent proof, render provenance and check results.

## Rill 39 completion

All four Rill 39 items use the same atlas-region path. The loaded magazine has
one original cluster split into two packed regions; the empty has four split
into five. Both fail 512 with either clustered or 8 px island packing, and
island packing also fails 1024 with 8 px guards. Existing long islands prevent
the smaller allocation; no island was cut or scaled. The cartridge and fired
case fit one 512 region each. Their cluster GLBs are smaller than their 8 px
island candidates: 164,864 versus 184,124 bytes, and 149,668 versus 172,076.
Packing evidence: `build/ak-detach/packing.json`; candidate exports:
`build/ak-detach/islands/`. Internal atlas margins and nonmember texels are
kept byte-exact; only the outside uses pull-push. Guards are 8 px on the mip-3
grid. Sampling and opaque specular-alpha data are inherited from the gun.

Old/new raw-GLB comparisons match oriented geometry, normals, nodes and
material factors/extensions, including alpha. Across 130,160 surface samples,
the maximum base-level component error is 0.00003498 (below 0.25/255).
The largest UV storage discrepancy is 0.000122071 delivered pixels;
maximum triangle tangent-direction delta is 0.012822° (below 0.5°).
Extraction density ratios are exactly 1.000; independent raw-GLB area ratios
include the expected float-storage noise on thin triangles, with resolved
minimum 0.999852. `build/ak-detach/comparison.json` records the measurements.
Pointwise mip bleed is checked at L0–L3 against independently aligned isolated
island references, with the same 1/255 tolerance as the other seventeen.

All four full-size, native distant and nearest-magnified distant pairs were
opened and reviewed. Gallery: `build/ak-detach/pairs/index.html`; contact
sheets: `full-contact.png` and `distant-contact.png` in that directory.
Each of `magazine_loaded/`, `magazine_empty/`, `cartridge/` and `case/` contains
`full-pair.png`, `distant-pair.png` and `distant-texels.png`. The unchanged
`guns/common/detachable_mip_review.py` renders the old full-atlas GLB left and
the final subset GLB right, at about 570 px and native 40 px. Color/value,
rib wear, lips/follower cavities, lacquer and jacket response remain consistent.
Small tail-filter differences become visible under nearest magnification:
maximum 22/255 in these diagnostic images, beyond the protected mip range.
Existing faceting and soft normal-only headstamps remain. These are mipmapped
sampling diagnostics, not new photographic finals or a runtime-engine test.
`build/ak-detach/render-provenance.json` matches every final GLB hash;
`render-differences.json` records the image differences.

The export uses `make -C guns/ak export`, keeping finals and look renders out
of this round. The extended `make -C guns/ak check` covers inherited source,
finalized and imported construction/motion, fresh GLB import, density, atlas
samples, aligned guards, sampler and per-level bleed. The accepted main GLB
from `main` at `2b6ac0e` stays byte-identical:
`0fecef4cfc1b77fa9c485272d787cb276625781745a6893fe67ba190b60355a0`.
Three exact-signature tangent anchors use the existing kit correction for one
0.0001 exporter rounding step. The existing main geometry/UV/rig fingerprint
is retained; a separate baseline from the original main detachables preserves
oriented non-UV attributes and node frames after UV remapping. Canonical maps
and all docs JPGs remain unchanged. No kit code changed, so the conditional
full kit-suite rerun was unnecessary. Evidence and logs: `build/ak-detach/`;
`checkpoint.json` records final preservation and check results.

## Prior accepted evidence retained

The original non-mipmapped compact delivery remains documented in
`build/detachables/`: **116,433,060 → 10,347,156 bytes (91.11% smaller)**, its
31 old/new Cycles pairs, surface comparison, six gun checks and 23 kit tests.
Those historical numbers are retained rather than substituted for the final
mipmapped totals above. The fourteen accepted mipmap proofs and pairs remain
under `build/mipmaps/`; their six retained sets are unchanged. The earlier
per-island 70% obstruction remains reproducible in `build/magazine-fit/` and
was correctly conditional on separate guards per island. Clusters remove that
cost without weakening the density floor or using a 2048 magazine.

## Vesper visible-feed update

The Vesper’s corrected magazine uses two separated atlas panels so every
source neighborhood fits 1024 at density **1.000**. Its loaded variant has two
clusters/regions; empty has seven, with no splits. Both retain 8 px guarded
regions, mipmapped samplers and exact source-atlas copying. The fired case
remains one 512 region. Repeated base/mip-0–3 proofs are in
`guns/bolt/build/delivery/verify.json`; excesses are below 3e-14.
The source gun now depicts extraction, ejection and feeding, with updated
final/docs images. Earlier preservation manifests and rendered comparisons
above describe the subset-only delivery before that intentional revision.

## Rill 39 and Relay 9 reviewed paint refresh

Both canonical sets were freshly baked at 4096 and shipped at 2048 after
raising intact receiver enamel to linear RGB .022/.023/.024. The kit's existing
subset path regenerated all four detachables per gun. Every output still uses
one material and three maps; geometry, UV layout, rig, sockets and clips retain
their original exact baselines. Density remains 1.000, with the same mipmapped
samplers and guarded regions. Earlier subset-only preservation claims above
describe that historical handoff, before this intentional receiver-paint bake.

| Family | Main GLB bytes / triangles | Loaded / empty magazine bytes (1024) | Cartridge / case bytes (512) |
| --- | --- | --- | --- |
| Rill 39 | 10,839,212 / 40,000 | 1,534,304 / 1,462,400 | 164,864 / 149,672 |
| Relay 9 | 10,984,144 / 41,540 | 1,318,624 / 1,186,756 | 151,444 / 154,940 |

The member reviews record the deliberate look-baseline changes, accepted GPU
rounding, unchanged authored wear/other finishes, and existing projection
contacts where neighboring low surfaces receive changed receiver paint. These
are not claims of byte-identical nonpaint atlases. Fresh export/import, copied
atlas samples, geometry/layout identity and per-mip bleed remain checked. No kit
code changed. Final presentation and GIFs were regenerated from the exports.
