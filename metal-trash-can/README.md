# Galvanized garbage can

An original, weathered 31-gallon steel garbage can: corrugated tapered sheet,
folded rear seam, rolled mouth, elevated floor and lower chime, removable
pressed lid and three carrying handles. The lid and the two side wire loops
remain independently movable. Every vertex and texel comes from the scripts.

![Cycles and Eevee views of the exported GLB](docs/hero.jpg)
![Exported front, side, back and top](docs/turnaround.jpg)
![Lid, handle, interior, scale and removable lid](docs/details.jpg)

The [manufacturer's 2021 catalog](https://www.behrens.com/wp-content/uploads/Behrens-Catalog-2021.pdf)
gives the 31-gallon class a 21-inch diameter and 29¾-inch overall height. The
current product page contains conflicting widths, so the dated catalog controls
this design. [REFERENCE.md](REFERENCE.md) distinguishes published dimensions
from authored construction estimates; [sources](refs/SOURCES.md) identify all
photographs and their rights. Photos are measurement/review only.

| Measurement | Modeled value |
| --- | --- |
| Lid diameter | 533.400 mm / 21 in |
| Overall height, including bridge handle | 755.650 mm / 29¾ in |
| Lower chime diameter | 457.200 mm / 18 in |
| Width including hanging side handles | 563.784 mm |
| Sheet / lid gauge | 0.65 / 0.80 mm, authored estimates |
| Elevated floor, actual inside / underside | 17.000 / 16.350 mm above ground |

Capacity is the nominal 31-gallon class; internal volume is not certified.
The original lid and bridge are a classic construction rather than a copy of
the reference manufacturer's patented lid. There are no commercial markings.

One material and one **1024²** BaseColor (sRGB), OpenGL +Y Normal and ORM
(R occlusion, G roughness, B metallic) atlas serve the complete assembly.
The exported asset is **4,928 triangles**, inside the 2,000–5,000 budget, in
four mesh objects. The GLB is **3,485,008 bytes**. Budgeted texture residency is approximately **4 MB** with
block compression and mipmaps. Engines may generate distance LODs on import.

The source uses angular zinc crystals, exposure dulling, broken white oxide
where rain and folded joints retain water, early rim/seam rust, and dark
handling and low-skirt grime. Restrained handling dents remain unchanged. `WEAR` controls use-related layers.
Small pressed beads and grain reside in shader microrelief. Other channels
use the kit's isolated high-to-low projection and stationary contact AO; the
normal is baked directly on the matching game shell to avoid projection
across the 0.65 mm wall. All maps are baked at 4096 before delivery filtering.
No texture repair, reference projection, downloaded material or HDRI is used.
Delivered PNG bytes are BaseColor 1,274,044; Normal 327,667; ORM 1,626,619.
The imported atlas covers 56.77%, with zero measured overlap/outside/degenerate
triangles and density p5/median/p95 of 406/448/471 px/m.

| Part | Pivot in Blender meters | Motion |
| --- | --- | --- |
| `MetalTrashCan` | (0, 0, 0) | Ground-footprint center; +Z up, front −Y |
| `Lid` | (0, 0, 0.714) | Removable; demonstrated +Z travel 0–0.600 m |
| `Handle_Left` | (−0.262, 0, 0.644) | Local Y, 0–95° outward |
| `Handle_Right` | (0.262, 0, 0.644) | Local Y, 0 to −95° outward |

The eye bores retain actual axle portions of the wire. The construction check
measures the lid/rim contact, floor gauge and retaining-eye support on source
surfaces. The kit sweeps high and game meshes at 10 mm lid steps and 2° handle
steps. The closed rim permits a declared 0.5 mm seating tolerance; each handle
uses 0.4 mm and only its intended eye-bearing contact is allowed. These are
sampled checks, not a claim of continuous collision certification. GLB
verification separately checks that serialization preserves geometry and pivots.

```sh
make                        # references through final renders/docs and checks
make check                  # geometry, UVs, normals, GLB, motion and actual contacts
make WEAR=.65               # a more weathered version
make match PASS=source-review WIDTH=1000 SAMPLES=24
make clean && make          # rebuild generated delivery from scripts
```

Requires Blender 5.2, Python/Pillow/NumPy and `flock`. Cycles uses the kit's GPU
lock and OptiX/CUDA. Eevee adds a procedural studio sphere reflection capture
for the bare metal; it uses the same exported material and textures. The Makefile includes the unified kit rules and declares
1024 delivery size; asset-specific code handles the thin-sheet normal pass.

The GLB is `export/MetalTrashCan.glb`, textures are in `textures/ship/`, and
source/UV/export/check JSON evidence lives in `build/`. Final Cycles views are
in `renders/final/`, Eevee in `renders/final-eevee/`; all are imported GLB views
with source SHA-256 metadata. `renders/final/contact.jpg` contains the complete
set. `renders/photo-final/match_front-pair.jpg` compares the delivered GLB
against the reference photo. [REVIEW.md](REVIEW.md) records failures, corrections
and final delivery evidence.

The weakest areas are the thin pressed beads and zinc grain at close range:
the shared 1024 atlas softens them, and the restrained dents are simpler than a
heavily battered real can. The construction photograph shows a newer, more reflective can. Outdoor-use
calibration uses `renders/wear-pass2-glb/used_estate-pair.jpg` and the matching
source pair; landmark RMS is 18.01 px. Its original lid and handle construction
differs from the estate photograph, and studio illumination is brighter than
the shaded outdoor reference.
