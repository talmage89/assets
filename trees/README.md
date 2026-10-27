# Trees / red maple

An original scripted summer **red maple (*Acer rubrum*)**, about 12.5 m tall,
with a 9.8 m crown and a 36 cm trunk. The specimen represents an open-grown
front-yard tree around twenty years old; age is an authored brief, not inferred
from a surveyed reference tree.

![Red maple, Cycles](docs/hero.jpg)

![Front, side, back and top](docs/turnaround.jpg)

![Bark close and at two meters, branchlet, roots, scale and Eevee](docs/details.jpg)

All presentation images use the **exported GLB and its embedded baked texture
set**. The foliage renderer implements the documented thin-leaf response from
those maps. Lighting is procedural daylight; no HDRI or reference pixels enter
the asset.

[Full contact](renders/final/contact.jpg) ·
[Penn State pair](renders/final/match_psu-measured-pair.jpg) ·
[Oregon State pair](renders/final/match_osu-measured-pair.jpg) ·
[Bark value crops](renders/final/bark-value-pair.jpg) ·
[Critique history](REVIEW.md) · [Species evidence](REFERENCE.md).
The full-resolution files are local rebuild outputs; the three docs JPGs are
tracked.

## Scale and construction

| Measured source surface | Result |
| --- | ---: |
| Complete mesh, including transparent card corners | 10.074 × 9.111 × 12.535 m |
| Retained foliage X / Y width | 9.801 / 8.857 m |
| Retained foliage base / top | 2.086 / 12.432 m |
| Fitted trunk diameter at 1.35 m | 0.361 m |
| Grade section, area-equivalent diameter at 0.01 m | 0.620 m; 1.72× DBH |
| Flare section at 0.70 m | 0.373 m; 1.03× DBH |
| Root reach below 8 cm height | 0.378 m |
| Conservative whole-card walking clearance within 1 m of bole | 2.826 m |
| Four co-dominant emergence heights | 2.193–2.726 m |

Meters; Blender +Z up and −Y front, glTF +Y up and +Z forward. Origin is at the
bole's footprint center on grade. Two static meshes, no armature or moving parts.
The scale silhouette is the toolkit's unchanged 1.8 m human.

Four curved co-dominants support 23 asymmetric scaffold masses, 69 secondary
limbs and 276 fine fourth-order forks. The last order continues in branchlet
cards. Overlapping leafy growth partly fills the deepest mass windows, broadens
the upper sides and preserves the low skirt. Branch load determines nominal
pipe radii; collars swell at attachments. The actual wood is one connected,
sealed triangulated surface. Opposing microscopic union slivers are removed
before acceptance rather than left for the exporter to discard.

Five broad buttresses merge into a smooth lower-bole flare and disappear into
grade. Section measurements use actual triangle/plane intersections; pipe
conservation checks concern authored profiles, not exact fused-surface areas.

## Budget and texture split

| Allocation | Delivered cost |
| --- | ---: |
| Wood | 8,080 triangles |
| Foliage | 15,600 triangles; 7,800 cards |
| Total / cap | **23,680 / 25,000 triangles** |
| Materials / static meshes | **2 / 2** |
| GLB, including embedded maps | **7,876,080 bytes** |
| Shared BaseColor-alpha / OpenGL +Y Normal / ORM | **2048² each**, from 4096² source/bake |

Delivered PNG sizes are 1,398,132 bytes BaseColor-alpha, 2,411,144 bytes Normal
and 1,388,810 bytes ORM. The GLB embeds those same images once.

Both materials share the same three images. The lower atlas half holds eight
repeated branchlet variants; the upper half holds unique bark islands. Bark is
GPU Cycles baked; the original analytic leaf albedo, alpha, cup/rib normals and
roughness are composited at 4096 before filtering. Photographs are never read
by either generator.

BC7 BaseColor-alpha, BC5 normal and 8-bpp ORM with full mip chains total about
**16 MiB** of texture memory. Vertex/index buffers add about **2.5 MiB**, for
about **18.55 MiB** total before engine overhead. The two extra bole UV seams
add 5,760 bytes of vertex data (0.0055 MiB) over the previous delivery; texture
allocation is unchanged. PNG/GLB storage and uncompressed runtime textures
have different sizes. The independent delivery report records
exact file and accessor sizes.

Unique bark UVs have no overlaps. Two bole seams isolate the eye-height band;
unwrap/packing uses the delivery region’s aspect, with roughly **460 px/m in
every tangent direction** there. Bark occupies about 23% of the whole atlas,
with half the atlas reserved separately for foliage. Leaf-card density is
727–812 px/m at 2048. Alpha reuse is intentional only inside the declared leaf region.

## Materials and engine integration

The branchlet variants carry 24–30 opposite leaves each. Blade length is
6.6–9.4 cm before 0.94–1.05 card scale variation: approximately **6.2–9.9 cm**
delivered. Broad shallow three-lobed outlines, occasional five-lobed blades,
serrated margins, palmate veins and small cup/tilt changes are generated
mathematically. Red petioles, red-brown current-year shoots, sparse insect bites
and a few older leaves provide species detail.

The leaf shader has no emission. It mixes 40% diffuse transmission with the
reflective leaf surface, gives below-view backs a desaturated gray-green
response and rejects glancing cards using their true geometric normal.
Lighting normals bend 90% toward a radial field blended **40% crown / 60%
branch mass**. Orthogonal companion cards maintain coverage from every view.
Bark has original seeded 2–4 cm longitudinal ridges divided into 10–30 cm
shallow plates. Independent wandering ridge edges, torn lips and fine granular
relief bake into the normal map; physical cavity visibility multiplies the
geometric ORM occlusion. Bark maturity follows both height and stem radius:
limbs below 10 cm diameter stay smooth and lighter. Rain tracks darken the
lower bole below the crotch; north-side lichen stays sparse. The matte response
uses exported KHR_materials_specular/ior constants, without another texture.
Honor those extensions, or port specularFactor .24 and IOR 1.45 into the engine
material; discarding them restores the excessive blue sky reflection.

The GLB supplies ordinary double-sided **MASK PBR** foliage. Stock glTF cannot
fully describe this thin-leaf/backface/glancing response. For the demonstrated
appearance, port `src/leaf_material.py` to the engine's foliage material: true
normal/view coverage fades over cosine 0.13–0.32, alpha cutoff 0.45. The final
renderer restores that response using **only the imported embedded maps**.
It loads no procedural bark or source geometry.

All source vertices carry floating-point RGBA `Wind`. Export preserves those
linear channels as the custom vertex-color attribute **`_WIND`**, avoiding the
standard `COLOR_0` albedo multiplier. The engine importer must retain it or copy
it into its wind-data vertex-color channel.

| Channel | Meaning |
| --- | --- |
| R | Height-based sway; wood up to .65, leaves up to 1; zero at grade |
| G | Branch hierarchy / 4; bole/roots 0, co .25, scaffold .5, secondary .75, leaf 1 |
| B | Seeded branch-family phase in [0,1] |
| A | Leaf flutter .65–1; wood 0 |

The engine adds the wind shader, instance variation, distance LODs and impostors
or billboards. Keep authored bent normals on foliage; automatic normal
recalculation loses the mass shading. Wind is not animation baked into the GLB.

## Rebuild and checks

```sh
make -C trees                  # refs → source → UV → bake → GLB → final renders/docs/checks
make -C trees check            # source, camera, bake, GLB/PBR/UV and botanical serialization checks
make -C trees tree-render PASS=study WIDTH=1200 SAMPLES=32
make -C trees tree-match PASS=study WIDTH=1200 SAMPLES=32
make -C trees tree-contact PASS=study
```

Requires installed Blender 5.2, Python/NumPy/Pillow, fontconfig/Noto Sans and
`flock`. Every Cycles bake/render uses the shared GPU lock. Defaults are 4096
bakes, 2048 delivery maps and 1600 px / 72-sample final renders. No downloaded
code, 3D assets, textures or lighting are needed.

Species and specimen choices live in `src/settings.py`: dimensions, leaders,
scaffold destinations, overlap controls, flare, leaf profiles/colors and bark
parameters. `growth.py`, `wood.py`, `wood_uv.py` and `leaves.py` implement the
family algorithms. The common toolkit handles UV packing, baking, filtering,
export and independent GLB verification.

`build/structure-check.json` measures actual source form and topology.
`build/delivery-check.json` independently checks the GLB's geometry, dimensions,
PBR images, material/alpha state, UV overlap and density.
`build/botanical-delivery-check.json` compares actual positions, split normals
and linear wind values through raw accessors and fresh import. Final image
metadata records the GLB hash; `renders/final/render-check.json` rejects stale
or source-scene presentation images. These checks prove their stated scopes;
only the photo pairs and close-ups establish appearance.

## Final photo and build evidence

The bark correction rebuilt the source scenes, UVs, 4096 bake, filtered maps,
GLB and full presentation with `make -C trees`; `make -C trees check` passes.
Twenty-one Cycles views (19 presentation/diagnostic views plus two photo cameras) and one Eevee
hero all match the current GLB hash. The kit and botanical delivery checks
find zero position/Wind errors, split-normal vector difference below 8.6e-5,
zero UV overlaps and zero missed/black interior bake texels of 3,511,566 checked.
Six finishing critique passes, including the lead’s bark correction and
rejected candidates, are logged in REVIEW.

| Final comparison | Model | Photo |
| --- | ---: | ---: |
| Penn State crown W/H | .961 | 1.256 |
| Oregon State crown W/H | .952 | .960 |
| Penn State green display luminance p5 / median / p95 | .037 / .218 / .543 | .073 / .260 / .564 |
| Penn State brightest-fifth median | .488 | .495 |
| Penn State shaded-fifth hue | 123.2° | 124.9° |

The crown median is lower than the lime round-3 checkpoint (.244). Shaded
recesses remain darker than the photograph: 1.84% of selected green pixels fall
below .02 display luminance, versus .38% in the photo; none clip a channel.
Oregon State is judged for form only. These are display-image comparisons
across different lighting and individuals, not calibrated reflectance.

Bark display-value patches are measured in `bark-evidence.json`, with their
rectangles shown in the [bark comparison](renders/final/bark-value-pair.jpg).
Penn State lower bole is **.119 model / .124 photo** median display luminance;
upper shade is **.041 / .077**. The lower surface is now dark gray-brown rather
than pale blue-gray. The model’s shade remains darker and cooler than the photo.
Both photo patches sit beneath the crown; they are not equal-lighting albedo
calibrations. OSU slide values are recorded but are not a color target.

The shipped eye-height band measures **458–462 px/m by area**, and **457–464
px/m in every tangent direction**. Uniform surface-area samples from the
embedded maps find median / p90 tangent-normal deviations **4.27° / 14.75°**;
ORM occlusion p10 is **.608**. These verify retained normal/occlusion variation;
the bark and two-meter images establish whether it reads. Plate lips remain
flat at grazing angles, with some procedural regularity in macro views.

## Limits and credits

The crown is more compact and its masses more distinct than Penn State's broad
individual. Some isolated upper wood remains angular. Close branchlet views
expose flat-card construction and soften the smallest teeth/scars at this
texture budget. The bark retains a low-poly silhouette and cannot show
displaced plate edges at grazing angles.
The engine foliage shader and distance impostors remain integration work.

The Penn State photograph is the color/value reference; the Oregon State slide
is used for form only. Neither supplies surveyed dimensions or age. Camera
fits compare different individuals and retain their residuals. Reference
credits, URLs and rights are in [refs/SOURCES.md](refs/SOURCES.md); comparison
photographs stay local and are never committed in docs. Every asset vertex and
texel is generated by our scripts.
