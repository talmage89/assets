# Standalone detachable mipmap delivery

Fourteen standalone sets now use the gun’s sampler, protected mip gutters and
a fully filled background. **Three magazine allocations remain pending**: the
loaded pistol magazine and both bolt-rifle magazines. The supported option remains 512/1024; **2048 is excluded**. The follow-up
shape-aware fit study reached the explicit 70% stop condition described below.
Their old compact files remain available, but are not claimed as mip-correct
deliveries.

## Sampler, gutters and fill

Rebuilt sets inherit the gun’s sampler unchanged: `minFilter=9987`
(`LINEAR_MIPMAP_LINEAR`), `magFilter=9729` (`LINEAR`), and repeat wrapping
(implicit glTF defaults). No LOD clamp or mipmap disabling is required.

The packer prefers 8 px per island. If that does not fit the requested size,
it tries the atlas-equivalent **6 px minimum**, with the same protection.
Guard rectangles align to an 8 px mip grid; right/top edges round up, giving
8–15 px guards for the preferred policy or 6–13 px for the fallback. This
contains every box/bilinear tap through mip 3. Alignment matters: an unaligned
8 px trial failed the strict mip-3 comparison. Larger required cutoffs increase
the grid and minimum guard together; the regression also tests through mip 6.

Every island’s original bilinear footprint stays byte-exact. Integer-pixel
translation and positive uniform scaling preserve density and tangent frames;
nothing is rebaked, resampled on the surface, rotated or mirrored. Guards
dilate only their own island. A masked pull-push fills all remaining texels,
with RGB in linear light and alpha/ORM as linear data. Generated normal texels
are normalized before quantization; original island texels are untouched.

## Mip error and measured outputs

`detachable_verify.mip_bleed()` builds box-filtered atlas and standalone chains.
At ten common points per triangle, each map is compared with the same island
alone, dilated without a limit. The ideal reference is aligned independently
to each actual mip grid, so intra-island filtering phase is not counted as
bleed. Error is the maximum absolute component difference in linear RGBA,
encoded tangent normal, or linear ORM. **At every point and tested level, the
new error must be no greater than the atlas error plus 1/255.**

The tiny/sliver islands make the requested two-texel cutoff mip 0 for these
items. The check deliberately extends every sampled surface through **mip 3**
instead of letting that cutoff make the test vacuous. Table values are
**new / atlas**, normalized to 0–1; values below 0.000001 round to zero.
Pointwise excess is enforced separately, not inferred from these maxima.

“Atlas bytes” are the original full-atlas GLBs; “prior bytes” are the accepted
compact, non-mipmapped GLBs. New sizes are exact embedded GLB bytes. Gutter
values are minimum pixels; the rounded right/top extents are in `layout.json`.

| Gun | Item | Map | Density ratio | Gutter | Atlas bytes | Prior bytes | New bytes | Mip 0 | Mip 1 | Mip 2 | Mip 3 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| pistol | `case` | 512 | 1.000 | 8 | 5,204,740 | 239,544 | 253,980 | 0 / 0 | 0 / 0.189946 | 0 / 0.346479 | 0 / 0.472156 |
| pistol | `magazine_empty` | 1024 | 1.000 | 6 | 5,362,360 | 945,428 | 991,512 | 0 / 0 | 0 / 0.221151 | 0 / 0.335126 | 0 / 0.644196 |
| pistol | `magazine_loaded` | 1024 — blocked | not chosen | pending | 5,396,292 | 1,105,768 | pending | — | — | — | — |
| shotgun | `hull` | 1024 | 1.000 | 8 | 8,244,008 | 345,992 | 452,248 | 0 / 0 | 0 / 0.19838 | 0 / 0.34371 | 0 / 0.47697 |
| shotgun | `shell` | 1024 | 1.000 | 8 | 8,260,472 | 362,344 | 420,528 | 0 / 0 | 0 / 0.170537 | 0 / 0.39924 | 0 / 0.600235 |
| bolt | `case` | 512 | 1.000 | 8 | 6,753,080 | 196,596 | 209,532 | 0 / 0 | 0 / 0.210254 | 0 / 0.418546 | 0 / 0.73438 |
| bolt | `magazine_empty` | 1024 — blocked | not chosen | pending | 6,928,816 | 1,151,616 | pending | — | — | — | — |
| bolt | `magazine_loaded` | 1024 — blocked | not chosen | pending | 6,997,748 | 1,373,476 | pending | — | — | — | — |
| smg | `cartridge` | 512 | 1.000 | 8 | 7,359,568 | 141,404 | 154,220 | 0 / 0 | 0 / 0.158223 | 0 / 0.382461 | 0 / 0.688034 |
| smg | `case` | 512 | 1.000 | 8 | 7,360,256 | 161,256 | 172,784 | 0 / 0 | 0 / 0.20108 | 0 / 0.418677 | 0 / 0.631851 |
| smg | `magazine_empty` | 1024 | 1.000 | 6 | 7,476,900 | 1,137,960 | 1,186,756 | 0 / 0 | 0 / 0.241367 | 0 / 0.537232 | 0 / 0.719456 |
| smg | `magazine_loaded` | 1024 | 1.000 | 6 | 7,549,888 | 1,267,700 | 1,318,624 | 0 / 0 | 0 / 0.241367 | 0 / 0.537232 | 0 / 0.719456 |
| revolver | `cartridge` | 512 | 1.000 | 8 | 6,307,544 | 58,568 | 74,972 | 0 / 0 | 0 / 0.0313176 | 0 / 0.100991 | 0 / 0.523206 |
| revolver | `case` | 512 | 1.000 | 8 | 6,304,652 | 64,264 | 75,764 | 0 / 0 | 0 / 0.0215878 | 0 / 0.111398 | 0 / 0.391379 |
| revolver | `speedloader_loaded` | 1024 | 1.000 | 8 | 6,513,196 | 548,644 | 654,268 | 0 / 0 | 0 / 0.0662934 | 0.000105483 / 0.164486 | 0.00011086 / 0.538116 |
| lever | `cartridge` | 1024 | 1.000 | 8 | 7,216,192 | 595,532 | 651,104 | 0 / 0 | 0 / 0.282336 | 0 / 0.34198 | 0 / 0.449821 |
| lever | `case` | 1024 | 1.000 | 8 | 7,197,348 | 651,064 | 713,488 | 0 / 0 | 0 / 0.20259 | 0 / 0.325882 | 0 / 0.562704 |

The fourteen completed items total **97,110,204 → 7,329,780 bytes**
(92.45% smaller than their original full-atlas deliveries).
Each has one material, three maps, unchanged triangles and unchanged origins.
Full per-channel/per-level errors, density and geometry comparisons are in
`build/mipmaps/proof-partial.json`.

## Shape-aware fit study: stopped at the 70% floor

The fourteen accepted sets are unchanged. The three remaining sets must stay
at 1024; the earlier 2048 proposal is rejected and no such export was made.

A prototype packs guarded island masks, rather than rectangles, with integer
translations only. It considers all 64 integer phases of the 8-pixel mip grid
and tries height-, occupied-area-, and longest-extent placement orders. Guard
masks use the exact bilinear footprint plus the accepted 6 px minimum. They
also reserve the complete mip blocks touched by those guards.

| Item | Islands | Full-density guarded pixels, before grid rounding | Minimum phase-aware mip-mask pixels | Full-density result |
| --- | ---: | ---: | ---: | --- |
| Pistol loaded magazine | 282 | 879,512 | 1,015,360 | Three placement orders failed; this is not an impossibility proof |
| Bolt empty magazine | 1,223 | 1,287,175 | 1,493,888 | Mask area exceeds 1,048,576 |
| Bolt loaded magazine | 1,560 | 1,604,189 | 1,875,712 | Mask area exceeds 1,048,576 |

At a 0.70 density ratio, the loaded bolt magazine's rasterized 6 px guards
still occupy **1,147,971 pixels**, before grid rounding or packing waste.
An independent read of the original finalized Blender UVs confirms a stronger,
placement- and pixel-phase-independent obstruction:

| Loaded bolt magazine, at 70% density | Pixels |
| --- | ---: |
| Conservative minimum for disjoint 6 px guarded bilinear footprints | **1,049,203** |
| 1024 map capacity | **1,048,576** |
| Unavoidable excess before packing waste | **627** |

The resulting necessary density upper bound is **0.6995305503**. This is an
upper bound, not a fitted solution; an actual arrangement could require less.
It is below the permitted 0.70, so work stopped under the brief's explicit rule.
No scaled images were generated, and the three magazines were not exported.

The bound is computed from the original source's 1,560 islands / 4,976 triangles.
For each island, triangle area minus all pairwise intersections gives a
conservative union-area lower bound. Successive horizontal/vertical dilation
then gives a lower bound on the area expanded by a 6.5 px square. A bilinear
footprint plus six pixels of dilation covers that region with unit texel cells;
taking each island's integer ceiling before summing gives the bound above.
Axis-projection lengths are measured as unions of intervals, so disconnected
projections do not inflate the result. A small numerical safety deduction is
applied before each ceiling. Every coefficient increases monotonically with
density; this rules out all ratios at or above 0.70, rather than just one raster
phase or one placement heuristic.

Reproducible working evidence is under `build/magazine-fit/`:
`mask_pack.py`, `mask-pack.log`, `capture_source.py`, `floor_bound.py`,
`floor-bound.json`, `exact_source.py`, and `exact-source-area.json`.
All 23 existing gun/detachable GLBs and all 111 docs JPG hashes were rechecked
unchanged. Kit source and exporter code were not modified in this fit study.
The scaled-item comparison, pistol/bolt re-export/checks and three new render
pairs were therefore not run; the stop condition precedes those steps.

The existing fourteen-item bytes and error table above remains valid. There is
no completed corrected delivery total for all seventeen. The current mixed
filesystem total is 10,960,640 bytes, which includes the three unresolved legacy
files; it must not be reported as a completed mip-correct total.

The fired shotgun hull remains 1024; every other accepted size is unchanged.
At 8-bpp block compression, three maps with full mips cost about 1 MiB at 512
or 4 MiB at 1024. No 2048 magazine is proposed or supported.

## New render proof

Gallery: `build/mipmaps/pairs/index.html`. Each completed item has
`<gun>/<item>/full-pair.png`, `distant-pair.png` and `distant-texels.png`.
Contacts: `build/mipmaps/pairs/contact-*.png`.

`guns/common/detachable_mip_review.py` rasterizes the actual raw GLB triangles
with explicit box mip chains and derivative-selected trilinear LOD. Full
coverage is about 570 px; distant coverage is measured at about 40 px, rendered
directly at that scale. The nearest-magnified view exposes those same distant
texels. This is an analytic-GGX **sampling diagnostic**, not a replacement for
the accepted Cycles studio photographs or a three.js/Unity/Unreal integration
test. Per-item provenance records source and renderer SHA-256, coverage and LOD.

All completed full/distant pairs and distant texel views were opened. Close
views retain color/value and normal response; the coarse tail has small
expected changes from averaging own-surface colors. Existing faceting, soft
headstamps and the SMG’s strong wear remain. Notes:
`build/mipmaps/visual-review.md`. No docs JPG was regenerated or revised.

## Checks and preservation

All 23 `kit/test_*.py` pass from clean fixture outputs, with Blender for bpy
fixtures, unittest for Python fixtures and the shared GPU lock for bake tests.
`build/mipmaps/kit-tests-six.json` records commands/results; logs are in
`build/mipmaps/kit-logs-six/`. The detachable test includes sampler and black
background negative cases, a dense 400-island 512 fallback and a mip-6 fixture.

The shotgun, revolver and lever were re-exported through their ordinary
`make export` and passed `make check`. The SMG check is recorded separately in
`build/mipmaps/gun-checks-final.json` and also passed. Pistol/bolt full export/check remain
blocked by the three allocations above. Their unaffected ammunition recipes
were invoked through make with review-only make fragments under each `build/`;
`build/mipmaps/ammo-exports.json` records exact commands. The empty pistol
magazine was exported with a review-only entry subset, independently verified,
then installed; its main GLB was not replaced by that staging export.

All six raw main GLBs match the preserved branch-point baseline byte-for-byte;
`build/mipmaps/checkpoint.json` records hashes, sizes and the four successful
gun checks. The fourteen completed items retain 27,076 triangles and one
material each, with 270,760 independent base-level surface samples. The worst
pointwise mip-error excess is 0.0000333611, below the 1/255 tolerance.
The revolver needed two additional exact-signature MikkTSpace anchors
for one last-decimal tangent component each; the existing kit utility bounds
each correction to one 0.0001 step. All other main bytes remain untouched.
An interrupted intermediate revolver check was repeated after the final guards.
Canonical PNGs, finalized sources and all 111 tracked docs JPGs are hash-checked.

## Accepted prior delivery retained

The previous compact delivery measured **116,433,060 → 10,347,156 bytes**,
a **91.11% reduction**, before this mipmap correction. Its per-item prior sizes
are retained in the table above. Its original 31 old/new Cycles pairs remain in
`build/detachables/pairs/`, with their original provenance and visual notes.
The accepted independent surface comparison covered 410,240 samples across
all seventeen items, with its six gun checks and 23 kit tests. Those historical
records remain in `build/detachables/`; they are not substituted for this
follow-up’s new mip checks. The original density choices and no-rebake policy
are preserved. Only the explicitly documented hull promotion and pending
allocation exceptions differ from those choices.

This follow-up stopped at the explicit 70% floor. Completing the remaining
three items requires a change beyond the present fitting constraints; no
2048, sub-70% density or unapproved guard reduction was used.
