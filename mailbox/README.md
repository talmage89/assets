# Alder / size-1 curbside mailbox

Original black powder-coated galvanized-steel mailbox on a dressed wooden 4×4
post and half-lap mounting arm. The pine has silvered grain/checks and a darker,
road-splashed foot after a few outdoor seasons. The bent shell is hollow, with a closed rear,
pressed metal floor, returned front door, real hinge bores and an independent
red signal flag. Small pressed floor dimples and coating wear are baked detail.

![Exported mailbox](docs/hero.jpg)

The historic size-1 shell is **482.6 mm long × 165.1 mm wide × 215.9 mm high**
(19 × 6.5 × 8.5 in). The mail floor is **1066.8 mm / 42 in** above the road-height
datum. The post is **88.9 mm square** (dressed nominal 4×4); arm and mounting
board are 88.9 and 19.05 mm thick. Door returns/hinges/catch extend beyond the
nominal shell. Assembled bounds: **180.6 × 538.3 × 1269.65 mm** in the closed/rest
pose. [REFERENCE.md](REFERENCE.md) distinguishes references from authored internals.

Origin: center of the post's ground footprint, +Z up and front −Y in Blender;
glTF +Y up / +Z front. Terrain and the USPS 6–8 inch curb setback are placement
choices. There is no underground post tail or concrete block in the export.

![Turnaround of the exported GLB](docs/turnaround.jpg)

The **2,082,780-byte GLB** uses **1,264 triangles**, **one material**, and three rigid meshes:
static shell/support, door, flag. One **1024² BaseColor / OpenGL +Y Normal / ORM**
set, baked at 4096², costs approximately **4 MiB** with BC7/BC5-class compression
and mipmaps. ORM packs occlusion, roughness and metallic in R/G/B. Engine import
should treat BaseColor as sRGB and Normal/ORM as linear. `WEAR=.45` adds edge
chips, cavity drips, lower-post dampening and fiber checking; `WEAR=0` retains
the manufactured coating and wood grain only. UV coverage is 71.15%, with zero measured overlaps;
density p5 / median / p95 is approximately 595 / 744 / 1005 pixels per meter.

| Pivot | Blender position, meters | Local axis | Range |
| --- | --- | --- | --- |
| Door | (0, −0.4453, 1.0603) | +X | 0 closed → 105° outward/down |
| Flag | (0.08905, −0.33, 1.1561) | +X | 0 stowed → 90° raised |

The glTF importer converts axes; use the named node's local X for both motions.
Keep static, Door and Flag meshes separate. No armature or animation clips.
An engine controls the pivots; the retained names/extras document the ranges.

![Hardware and timber](docs/details.jpg)

```sh
make                          # references through final GLB, renders, docs and checks
make check                    # source, UV, serialization, support and motion tests
make PASS=review match        # source / photograph comparison
make PASS=review match-final  # shipped GLB / photograph comparison
make WEAR=.8                  # dirtier variant
make clean && make            # reproduce from scripts
```

`BAKE_POLICY` isolates Door and Flag high/low groups, with separate stationary
contact-AO shadows. This uses the merged kit implementation; no manual exploded
fallback was needed. `textures/bake/bake-report.json` records actual offsets and
group counts. `build/delivery-check.json` proves GLB serialization, atlas and
normal validity. `build/assembly-check.json` measures physical support surfaces.
`build/motion-game.json`, `motion-high.json` and `motion-glb.json` test the physical
source and imported meshes at one-degree steps, with 0.05 mm penetration
tolerance. Sampling is explicit; it is not a mathematical continuous sweep.
The flag's plane stays outside the shell for its entire rotation by construction.

Final Cycles hero, four-view turnaround, hardware/timber close-ups, open pose,
1.8 m human scale, and Eevee live in `renders/final/`, `renders/final-eevee/`.
The complete sheet is `renders/final/contact.jpg`. Shot metadata records the
exported GLB hash. [REVIEW.md](REVIEW.md) logs source and final GLB critique.

All geometry, shaders and address graphics are generated here. Address 1847 is
fictional; DejaVu Sans is an installed open font. Manufacturer photographs are
comparison only; rights and URLs are in [refs/SOURCES.md](refs/SOURCES.md).
Needs installed Blender 5.2, Python/Pillow/NumPy and flock. No downloaded assets,
lighting, plugins or packages. The small sheet gauge, rear seam and wood fibers
soften at street distance, and tiny baked fasteners darken more than the source; the historical shell differs from the modern reference
product's precise latch/flag construction.


Phase 2 used-object comparison: `renders/wear-pass3-glb/used_black_post-pair.jpg`
(source counterpart under `renders/wear-pass3-source/`). The fitted residual is
22.49 px at 1100×900; the photograph has a different flag/latch and does not
establish our dimensions. Pine uses `kit.materials.weathered_wood()` with
separate timber-grain and grade frames, a silver-gray tone and stronger local
road splash. Shell chips stay on manufactured folds; Door masks recover hinge
rest height and the flag excludes lower-shell deposits. The texture set is
unchanged: BaseColor / Normal / ORM 645,381 / 638,621 / 703,649 bytes at 1024².
The small fibers/checks soften at street distance; broad silvering and the dirty
foot remain visible in the full hero.

## LOD rollout checkpoint: rejected motion

No mailbox chain is adopted. The measured trial below passes generic image,
geometry and normal checks, but `make check-lod LOD_THREADS=4` returns 2 on
the added imported-surface motion check. The reduced door penetrates the shell
by .248/.894 mm at LOD1/2, versus the original zero and .05 mm tolerance.
Separate Door/Flag meshes and unchanged pivots do not prove physical clearance.
See [both LOD critiques](REVIEW.md). `make lod` reproduces the rejected trial;
do not deploy it. Target misses remain 766/506 and 202/190, without claiming
an accepted target exception. Comparisons are `renders/lod/`; complete configs,
payload hashes, checks and images are archived in
`build/lod-rollout/mailbox/pass1/` and `pass2/`.

The reporter's generic PASS labels below cover its own image/raw/field gates;
they do not include or overrule the failed physical sweep. Its measured stored
cost is 2232 triangles, one canonical material, nine primitive placements,
4155897 physical bytes and 4.160 MiB resident. All three original 1024 maps
remain one 4.000 MiB allocation; added mesh buffers .07352 MiB, new images 0.
An instance would draw one level (1264/766/202 triangles and three draws),
not all nine stored placements. Both original `make check` runs pass.

<!-- LOD checkpoint: begin -->
## Additional LODs

`make lod` builds additional core glTF/BIN files and a manifest under `export/lod/`; `make check-lod` checks them. The existing delivery is immutable LOD0. Default `make` and `make check` retain their original build graph.

| Level | Triangles / target | Materials / draw calls | Geometry bytes | PNG bytes | Total load bytes | GPU unique textures + mesh, MiB | Switch height / distance |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| LOD0 | 1,264 / — | 1 / 3 | 95,129 | 1,987,651 | 2,082,780 | 4.000 + 0.0864 | near |
| LOD1 | 766 / 506 | 1 / 3 | 63,756 | 1,987,651 | 2,051,407 | 4.000 + 0.0568 | 25.0% / 4.40 m |
| LOD2 | 202 / 190 | 1 / 3 | 21,710 | 1,987,651 | 2,009,361 | 4.000 + 0.0167 | 9.0% / 12.22 m |

Chain check: True; image check: True; normal check: True.


Whole-chain resident GPU estimate: **4.160 MiB**, versus LOD0 alone **4.087 MiB**. Unique textures 4.000 MiB = 4.000 MiB original + 0.000 MiB proxy/impostor; all meshes 0.1599 MiB. Increase over LOD0 0.074 MiB = 0.000 MiB far maps + 0.0735 MiB additional mesh buffers. Intermediate new images: 0. Bind intermediate primitives to the canonical LOD0 material resources; the manifest records full image hashes and source image indices. Identical embedded/external PNG bytes require this resource binding to share GPU allocations, including duplicate original image entries. GPU columns deduplicate complete image hashes within each row; PNG/dependency bytes retain physical payload copies. Optional camera-facing impostor is a separate alternative; engine overhead is excluded.

Distances are to the bound center at 60° vertical FOV / 1080p. GPU figures estimate 8-bpp block-compressed textures with full mips plus raw accessor mesh bytes, before engine overhead. Per-level map bytes describe dependencies, including reused originals. The whole-chain estimate deduplicates canonical image resources. Targets and achieved counts are reported separately; a count alone does not establish visual acceptance.

Load these files as alternatives and configure Godot visibility ranges, Unity LODGroup renderers, or Unreal mesh/component LODs. Keep matching near pivots in the same pose during switching. [Engine sources, pixel thresholds and texture policy](../kit/LOD.md).

Near levels consolidate static parts by material and simplify moving parts while retaining names, pivots, sockets and animation data. Intermediate levels preserve original charts, attributes and LOD0 materials. Only the proxy receives new charts baked from the immutable delivered maps and shaders. Intermediate levels allocate no additional images.

Native-pixel LOD0/adjacent strips, amplified differences, close views and measured image status: `renders/lod/` (`contact.jpg`, `metrics.json`). Raw checks: `export/lod/check.json` and `export/lod/normals-vs-lod0.json`; per-level construction/pruning decisions: `build/lod/<source stem>/simplification.json` and manifest assembly receipts. [Critique, target misses and known failures](../kit/LOD_REVIEW.md).

Shipped PNG dimensions: LOD0: 3 × 1024×1024; LOD1: 3 × 1024×1024; LOD2: 3 × 1024×1024.

LOD1 separate moving meshes: `DoorMesh`, `FlagMesh`.

LOD2 separate moving meshes: `DoorMesh`, `FlagMesh`.

Whole default chain:

| Stored mesh triangles | Material resources | Stored primitive placements | Distinct payload bytes | Resident GPU, MiB |
| ---: | ---: | ---: | ---: | ---: |
| 2,232 | 1 | 9 | 4,155,897 | 4.1600 |

Stored counts include the full immutable source container once and every default level; optional impostor alternatives are excluded. Near materials use their canonical source bindings. Physical payload files are counted once by path. Only one level is drawn per instance: active draw calls range from 3 to 3 across these kinds/levels. Stored primitive placements are not simultaneous runtime draw calls.

<!-- LOD checkpoint: end -->
