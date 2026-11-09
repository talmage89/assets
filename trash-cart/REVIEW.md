# Trash cart visual review

References were opened individually: manufacturer front, rear and blue cart
photographs plus brochure feature/dimension pages. Workbench closed, open,
lift-channel detail, front and side images were opened and inspected before
material rendering. All comparison pixels stay in ignored folders.

## Pass 1 — measured photo pairs

`renders/pass1/match_front-pair.jpg` and `match_back-pair.jpg`, with both original
Cycles renders, were opened. Front/rear photographs are credited in SOURCES.md.
Camera fitting is a measurement aid; this original cart is not a pixel-identical
replica. Initial landmark RMS was 37.04 px front / 29.30 px rear.

Visible CG cues and corrections:

- Lid catches too much pale diffuse/specular light. Darken the black resin and
  separate its finish from the sun-faded body; add a stepped perimeter sealing bead.
- Wheel webs are solid disks with decorative spokes. Replace with open annular
  rims, real radial webs and distinct axle caps. Carry tread relief in the bake.
- A visible rectangular stamp backing looks pasted on. Apply original hot-stamp
  text directly in the body material using physical coordinates, with no sheet.
- Body is too smooth and clean. Increase molded resin grain, introduce restrained
  recycled-resin color variation, and strengthen low drag/truck-contact scuffs.
  Grime remains anchored to the splash line, lid lip and cavities; drips begin at
  the upper shoulder. No reference image enters these masks.
- Rear wall lacks molded stiffening/journal construction. Add integral rear
  channels and load-bearing journal gussets; keep both wheel pivots on the axle.
- Lid underside was initially a closed slab. Rebuild as a true thin crowned skin,
  skirt and returned edge, so opening shows wall thickness and the hollow body.
- Open hero camera cropped the lid. Reframe around the complete open assembly.

## Pass 2 — corrected construction and causal wear

`renders/pass2/match_front-pair.jpg` and `match_back-pair.jpg` were opened with the
same photos. Open wheel webs, borderless municipal markings, localized heel
scrapes and the molded rear channels now read. The source is deliberately solid
charcoal resin rather than an exact copy of the reference's granite color blend.

Remaining cues: the low-resolution atlas will soften molded grain and the serial
number; the lid still reflects a broader studio card than the product photograph;
the authored rear well profile is simpler and less organically blended. These
are proportionate limitations for a repeated standard prop. The broad taper,
shoulder, recessed lift bar, 10-inch wheels and overall size establish the object.
The final source adds the sealing bead identified in pass 1. Further delivery
inspection will check that the blue symbol survives in the normal map.

The initial floor/handle camera anchors were uncertain photo estimates. Remove
those anchors and retain visible rim, wheel and lift-bar points; final residuals
and independent Blender projection agreement are recorded after the last match.
No camera fit changes the modeled dimensions or deforms a mesh.

## Delivery corrections and reduced-resolution proof

The refreshed `renders/final-photo/` pairs were opened after the sealing bead
and hinge-local hand-wear corrections. Camera RMS is **27.22 / 17.28 px**
(front / rear). The front lens estimate reaches the fitter's 180 mm bound;
treat that view as a rough photographic comparison, not known EXIF or an exact
replica. Independent Blender projection agrees within **0.00069 / 0.00019 px**.

The first exported images revealed black normal-bake patches near the wheel
wells despite passing geometry, UV and re-import checks. Source and game used
different diagonals through nonplanar structural quads. The body now triangulates
explicitly before both paths. Independent comparison finds **zero different body
triangles** between high source and finalized low. Reduced-resolution GLB side
and wheel renders in `renders/probe/` confirmed the patches were removed.

The scale-shot configuration initially omitted its human flag; the corrected
probe includes the complete 1.8 m silhouette. The required recycling mark did not
read reliably as a fine projected relief. It now retains **220 triangles** in
the recycling lid, with a footprint about 16 cm across. It is part of the lid's
existing mesh and shared material. This functional identification detail fits the
6,000-triangle budget without another draw call or texture set. The source uses
our generated crown to conform the installed-font geometry; no reference image
is projected or traced. Its converted mesh is welded and passes the solid audit.
The final reduced-resolution recycling top render was opened and the complete
mark reads clearly. Source/probe diagnostic images remain ignored.

The municipal stamp is restricted by both positive-X location and outward
orientation, preventing a repeat on the opposite inner wall. Hand wear uses the
front grip's hinge-local position. The source retains caused splash/heel grime,
shoulder runoff, sun fade and contact scuffs; no uniform dirt overlay is used.

The kit bake report now records uncovered alpha samples inside an independently
rasterized, eroded UV mask, separately from atlas padding. No automatic texture
painting or fabricated repair is used. Experimental cage changes were discarded;
the approved grill's projection defaults remain unchanged.

## Final source and reproducibility proof

The final high source has **20,856 triangles**. The shared game bake layout has
**6,816 triangles**, including both lids and the recycling mark. The per-export
limit remains **6,000**, enforced independently on each GLB. All source solids
are manifold with positive volume, finite coordinates and valid normals; no
zero-area triangles remain.

An independent clean-scene repeat generated the same game geometry SHA-256:
`558ff2c286cccb9b7d51e5b1347a51d2e2d44a90306bfa7884bb5dec4d53b97b`.
The packed union covers **51.81%**, with zero measured overlaps, outside or
degenerate UV triangles. The final 4096 bake and exported-GLB evidence follow.

## Final delivery evidence

`make -C trash-cart` completed successfully after the interrupted session was
resumed. `make -C trash-cart check` also completed successfully. The final bake
uses 4096² / 32 samples on OptiX through the shared GPU flock. All five channels
report **zero uncovered samples** across **8,327,739 checked interior texels**;
BaseColor also reports zero black interior texels. Channel bake times are about
48 / 46 / 22 / 96 / 94 seconds for BaseColor, roughness, metallic, AO and normals.

| Export | Triangles | GLB bytes | UV coverage |
| --- | --- | --- | --- |
| Trash | 5,556 | 2,387,496 | 42.41% |
| Recycling | 5,776 | 2,409,616 | 42.52% |

Both exports contain four mesh objects, one material and three **1024²** images.
BaseColor / Normal / ORM PNG sizes are **736,541 / 486,758 / 825,586 bytes**.
Both GLBs embed byte-identical images, validated independently; approximately
**4 MB** of block-compressed GPU memory with mipmaps when shared by the engine.
The normal intermediate is 16-bit at 4096; delivery uses linear color filtering,
vector-normal renormalization and RMS roughness filtering.

Both imported atlases have **zero** measured overlapping, outside or degenerate
UV triangles. UV-area-weighted density p5 / median / p95 is approximately
**200 / 236 / 238 px/m** at 1024. Raw vertex-normal unit error is at most
**1.19e-7**. Independent re-import finds zero measured world-vertex or pivot-
matrix error relative to the export expectations. No staging lid leaks into
an export. The actual ground-contact footprint midpoint is centered within
**0.000015 mm**; wheel radii match 127 mm within **0.000019 mm**. The −100° lid
exercise moves an extreme vertex **1.227 m** with hinge-radius change below
**0.000086 mm**. Wheels are exercised around their X axes.

Every final render was opened individually: ten trash-cart Cycles views, two
recycling Cycles views and one Eevee view, all 1400 px wide. This includes both
lid poses, front/side/back/top, lift-channel/hinge/wheel close-ups, a complete
1.8 m human scale view, the blue lid and its complete molded symbol. All final
metadata has `stage=final` and a GLB source, with these matching checksums:

- Trash: `10c6174ea36ccbabbd442ee55115a3bb4f32b822c8841d2e4a28db895ef5081e`
- Recycling: `e3ab4135c6e6eefd664998a2a2a8c803a1348383b3e1f25724dd41071251dbed`

The contact sheet and all three documentation sheets were opened as well:

- `renders/final/contact.jpg`: all 13 final images, Eevee last.
- `renders/final/variants-contact.jpg`: both variants.
- `renders/final/turnaround-contact.jpg`: four measured views.
- `renders/final/details-contact.jpg`: open body, lifting interface, hinge,
  wheel, recycling relief and scale.
- `docs/variants.jpg`: 1600 × 843, **75,904 bytes**.
- `docs/turnaround.jpg`: 1600 × 1700, **132,012 bytes**.
- `docs/details.jpg`: 1600 × 2303, **186,887 bytes**.

Final visual limitations: serial lettering, tread and manufacturing grain soften
in the shared 1024 atlas. Extreme hinge and lid close-ups show coarse bevels and
baked-normal waviness. The authored wheel-well and shoulder blends are simpler
than the photographed molding. Eevee reflections/occlusion differ from Cycles.
The black wheel-well bake patches are corrected; no failed numerical gates are
waived. This is an original measured standard prop, not a manufacturing replica.

Python compilation, repository source/type/size checks, staged-blob checks and
`git diff --check` pass. No rebuilt assets or references enter Git. Kit additions
are optional configuration or reporting: ship size and invalidation, shared-atlas
variant selection, separate source/delivery budgets, imported delivery bounds,
optional UV density bands, WebP reference retrieval and bake-coverage statistics.
The grill's existing defaults remain unchanged; its make graph was checked,
without performing another full grill bake.

No tool installations or lead input are needed. Keep a reduced-resolution GLB
probe before a full bake, and align structural triangulation through the source
and game paths. Stop after this asset, as required by the phase brief.

## Unified-kit regression, resumed batch

Merged `main`'s `wp/integrate` at 3e8dc84. Main's `policy.py`, canonical density dictionary and SHIP_SIZE path control UVs, bake/downsample/export verification and invalidation. Ported only variant selection/staging, source budgets, delivery-envelope verification, WebP references and interior bake diagnostics; no competing density resolver remains. Fixed the pre-existing Blender Vector-minus-float fallback in finalize separately (55a0585). `python3 -m unittest kit.test_delivery`, Python compilation and Blender `kit/test_policy.py` pass.

Ran `make -C trash-cart clean`, then `make -C trash-cart` and `make -C trash-cart check` to successful exit 0, resuming incomplete bakes after transient server interruptions. All five 4096 bake channels have zero missed interior samples across 8,327,739 checked texels; BaseColor has zero black interior samples. Rebuilt all 13 exported-GLB shots, opened each individually and the contact sheet, and found no visual regression. Both delivery checks, atlas byte-identity, four moving/static mesh objects, footprint and pivot checks pass. Triangles remain 5,556 / 5,776. The unified exporter preserves the asset tag correctly, adding eight bytes to each GLB: 2,387,504 / 2,409,624. Shared 1024 texture sizes and measured dimensions remain unchanged. Updated final docs from the rebuilt exports.

## LOD rollout — 2026-11-09

Merged current main (already up to date). Freeze revision `7e266d5` and 103
literal tool hashes: `build/lod-rollout/trash-cart/freeze*`. The original check
passes before adoption with explicit `-o build/lookdev.blend`,
`-o build/game-audit.blend`, `-o build/finalized.blend`,
`-o export/TrashCart.glb`, `-o export/TrashCartRecycling.glb` inputs;
`original-before.{json,log}` records the complete command. Variant preflight
`variant-routing.json` measures identical original image hashes but different
lid UV/vertex data, so each gets its own config/proof. Near chains retain
Lid/Wheel_Left/Wheel_Right frames and use one canonical texture pool. No
accepted source/map/docs image is changed. No result yet approves either kind.

### LOD critique 1: trash rest and close construction

Opened every native strip, all three construction views and contact for the
trash kind. Charcoal body/lid values, hot stamps, grip and wheel coverage hold
at .25 / 3.81m and .09 / 10.57m. The far construction view exposes a distorted
lid skirt/reveal and angular wheel/shoulder forms. Counts 3130/2178 miss
2222/833; this pass does not establish an accepted target exception. Generic
`check-lod` exits 0, including independent raw UV/tangent/normal checks.
The blue-lid kind is not built or approved by this proof.

### LOD critique 2: open pose and unresolved joint clearance

Opened both native same-pose strips in
`build/lod-rollout/trash-cart/motion-views/` (55/145 degrees, lid -71 degrees).
All three exported levels are imported independently with unchanged shaders.
Color/value and independent lid/wheels hold; the far rim, corner and skirt
deformation is obvious in this deliberately closer construction control.
It is not substituted for the far switch-distance acceptance images.

No cart chain is adopted. The independent actual-surface diagnostic
`motion-proof.json` samples the lid at one-degree intervals and a full wheel
turn at five-degree intervals, against all three fixed meshes with no exemptions.
It reports source contacts too: worst lid depths 16.625/18.917/21.665mm for
source/LOD1/LOD2; wheel depths source 15.559mm, LOD1 16.024/16.477mm,
LOD2 14.813/12.760mm. These are measured BVH/solid-parity diagnostic depths,
not established unintended interference: the test does not distinguish intended
coaxial pin/hub contacts. Its process exit 0 means the diagnostic finished,
not clearance passed. Its JSON records all three clearance results false.
The increased lid depths and deformed skirt remain unresolved without a
joint-specific fixture. No broad mesh-pair exemption is introduced to hide them.

The original cart check exercises pivot/radius/origin and shared atlas data;
it is serialization/kinematic evidence, not a sampled clearance certificate.
Likewise a generic `check-lod` pass cannot certify motion. Target misses also
lack a reviewed cheaper visible-failure witness, so no target exception is
claimed. Stop this family before spending its time box on fixture/tool work.
Recycling stays unbuilt/L0 pending its own proof, rather than inheriting the
trash result. Complete trash payload/config/hash/check/render archive:
`build/lod-rollout/trash-cart/trash-pass1/`.

Final receipts: the exact original commands above pass both before and after;
`trash-pass1-check.json` records the trash generic check exit 0. No recycling
`check-lod` result is asserted. Tool freeze: all 103 hashes match. The reporter
ran `--write-readmes --allow-failed` for the trash trial only; its complete
contact was inspected. Its PASS describes its own generic gates, not motion
or a target exception. Full-family costs include both immutable source
containers and their shared maps once. Repository check: 2555 files, zero
errors. No accepted source/map/docs or kit code changed.

## Archived rejected LOD reports — round 1

These reports are rejected evidence, not delivered chains.

## LOD rollout checkpoint: unresolved clearance

Neither cart kind has an adopted chain. The table below describes the trash
trial only. Its generic `check-lod` passes, but the independent joint-clearance
diagnostic remains unresolved and 3130/2178 triangles miss 2222/833 without a
reviewed cheaper visible-failure witness. See [both LOD critiques](REVIEW.md).
The diagnostic also finds source pin/hub contacts, so it is not reported as
proven unintended interference or as a tool regression. More precise joint
fixtures are needed. The recycling config is staged but unbuilt; it has no
LOD comparison, check or approval. Its unchanged LOD0 costs 5776 triangles,
one material and four draws, sharing the original 1024 atlas.

`make lod LOD_CONFIG=src/lod-trash.json LOD_THREADS=4` reproduces the trash
trial; `src/lod-recycling.json` selects the unproved blue-lid trial. Images are
`renders/lod/trash/` and `build/lod-rollout/trash-cart/motion-views/`.
The reporter's generic PASS label does not cover physical clearance.

Full-container accounting (both original variants plus the trash trial) is
`build/lod-rollout/trash-cart/full-family-costs.{json,md}`: 16640 stored triangles,
two source-specific material resources, sixteen primitive placements,
7268239 physical bytes and 5.0478 MiB resident. Original images occupy
4.0001 MiB once; new images 0, added meshes .3921 MiB. Only one level draws
per instance: trash 5556/3130/2178 triangles with four draws, recycling 5776
with four. Both original family checks pass with accepted generated inputs frozen.

<!-- LOD checkpoint trash: begin -->
## Trash cart LODs

`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/trash/`; `make check-lod` checks them. The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.

| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 5,556 / — | 1 / 4 | 338,624 | 2,048,880 | 2,387,504 | 4.000 + 0.3173 | near |
| LOD1 | 3,130 / 2,222 | 1 / 4 | 237,423 | 2,048,880 | 2,286,303 | 4.000 + 0.2211 | 25.0% / 3.81 m |
| LOD2 | 2,178 / 833 | 1 / 4 | 184,808 | 2,048,880 | 2,233,688 | 4.000 + 0.1709 | 9.0% / 10.57 m |

Chain check: True; image check: True; normal check: True.


Whole-chain resident GPU estimate: **4.709 MiB**, versus LOD0 alone **4.317 MiB**. Unique textures 4.000 MiB = 4.000 MiB original + 0.000 MiB proxy/impostor; all meshes 0.7094 MiB. Increase over LOD0 0.392 MiB = 0.000 MiB far maps + 0.3921 MiB additional mesh buffers. Intermediate new images: 0. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.

Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.

Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. [Engine sources, pixel thresholds and texture policy](../kit/LOD.md).

Near levels consolidate static parts by material and simplify moving parts while retaining names, pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. Only the proxy receives new charts baked from the immutable delivered maps and shaders. Intermediate levels allocate no additional images.

Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: `renders/lod/trash/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/trash/check.json` and `export/lod/trash/normals-vs-lod0.json`; per-level construction/pruning decisions: `build/lod/<source stem>/simplification.json` and manifest assembly receipts. [Critique, target misses and known failures](../kit/LOD_REVIEW.md).

Shipped PNG dimensions: LOD0: 3 × 1024×1024; LOD1: 3 × 1024×1024; LOD2: 3 × 1024×1024.

LOD1 separate moving meshes: `LidMesh`, `Wheel_LeftMesh`, `Wheel_RightMesh`.

LOD2 separate moving meshes: `LidMesh`, `Wheel_LeftMesh`, `Wheel_RightMesh`.

Whole default chain:

| Stored mesh triangles | Material resources | Stored primitive placements | Distinct payload bytes | Resident GPU, MiB |
| ---: | ---: | ---: | ---: | ---: |
| 10,864 | 1 | 12 | 4,858,615 | 4.7094 |

Stored counts include the full immutable source container once and every default level; optional impostor alternatives are excluded. Near materials use their canonical source bindings. Physical payload files are counted once by path. Only one level is drawn per instance: active draw calls range from 4 to 4 across these kinds/levels. Stored primitive placements are not simultaneous runtime draw calls.

<!-- LOD checkpoint trash: end -->
