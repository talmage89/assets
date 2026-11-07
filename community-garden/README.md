# Community gardens — form and construction checkpoint

Three original midsummer neighborhood gardens, generated from scripts for an
American town between 1995 and 2015. **This is the requested form checkpoint:**
quick material values, outline alpha and imported-library context. No final
look-dev, baked lumber/soil atlas, final docs gallery or game-ready claim.

The native botanical toolkit supplies tapered stem sweeps, curved leaf grids,
physical normals and Wind data. Crop growth rules live in this family. Native
shed construction, fence wire fields, ground maps, trees, architecture, cars
and utility parts are reused without changing their accepted deliveries.

| Seed | Fictional place | Year | Fence footprint | Plan |
| --- | --- | --- | --- | --- |
| 117 | Bellwether Growers | 1998 | 10.668 × 18.8976 m | 16 compact beds, four banks, gravel spine between apartments |
| 229 | Meadow Commons | 2004 | 27.432 × 24.384 m | Eight 10×20 ft tenant plots, two communal beds, grass cross aisle and rear service yard |
| 341 | Alder Neighbors | 2012 | 16.4592 × 18.8976 m | 12 transverse beds, two elevated tray beds, broad front court and shared service route |

Plot states interleave tidy, lush, weedy, fallow and newly planted. Seeds also
choose plant morphology, rotations, mulch and watering positions. The three
archetypes change the plot dimensions, orientation, entry court, surface and
service organization. A different seed within an archetype varies its planting
and care, retaining that archetype's layout grammar.

| Construction dimension | Generated | Basis |
| --- | --- | --- |
| Two-sided raised bed | 4×8 ft / 1.2192×2.4384 m | OSU/ISU 4 ft reach limit; authored 8 ft length |
| Larger tenant plot | 10×20 ft / 3.048×6.096 m | Brief; internal crop rows leave access strips, not a 10 ft reach bed |
| Lumber | 38.1mm thick; 234.95 or 285.75mm high | Dressed nominal 2×10 / 2×12; 88.9mm square corner posts |
| Concrete block | 193.675mm high/thick, 396.875mm long | Angelus specified nominal 8×8×16in CMU; open cells and 25mm webs |
| Main route | 1.524m; 1.8288m in 2012 | Above ADA 36in / .9144m minimum; compacted fines, not loose chips |
| Working aisles | At least .9144m in compact grid | ISU approximately 3 ft for equipment; measured export gaps in check report |
| Accessible tray bed | 2.4384×.9144m; work surface .8636m | ADA 34in maximum work height; 18in two-sided reach |
| Tray underside | .6973m before placement | Above ADA 27in / .6858m knee height; leg openings measured separately |
| Fence | 1.2192m fabric; 3.048mm wire | Native chain-link family, 50.8335mm perpendicular clear mesh |
| Shed | 2.4384×3.048m nominal | Native 8×10ft framed shed; shingle cuts deferred to normal bake |
| Cage / trellis | 1.34m / 2.12m high | Authored home-garden hardware; 5mm cage wire, 25mm bamboo poles |
| Hose | 20.6mm outer diameter | Authored 5/8in bore class; slack coils lie on grade |

Published guides, period examples and photo credits are in
[refs/SOURCES.md](refs/SOURCES.md); the dimensional choices are expanded in
[REFERENCE.md](REFERENCE.md). These are original compositions. Unsurveyed photos
establish visual proportions rather than exact dimensions or compliance.

Plants include tomatoes, peppers, zucchini, pole beans, sweet corn, lettuce,
kale, basil-like herbs, sunflowers, marigolds and weeds, each in three stages.
Mature plants have two seeded specimens. Tomato leaves are pinnate with
serrated leaflets and suspended fruit trusses; beans have climbing axes,
trifoliate leaves and pods; corn has distichous blades, ears and tassels.
Squash has a short crown, long petioles, broad palmate blades and low fruit.
Bean variants distinguish a bamboo pole from bowed thin twine. Mature tomatoes
have three connected leaders and nine-leaflet compound leaves. Engine distance LODs/impostors
are integration work, following the existing shrub/tree convention.

| Plant | Seedling (.28) | Intermediate (.64) | Mature (1.0), triangles |
| --- | ---: | ---: | ---: |
| Tomato | 964 | 2,332 | 4,608 |
| Pepper | 206 | 552 | 1,886 |
| Zucchini / squash | 354 | 552 | 1,194 |
| Pole bean | 756 | 1,512 | 2,472 |
| Sweet corn | 278 | 398 | 858 |
| Lettuce | 260 | 420 | 620 |
| Kale | 260 | 420 | 620 |
| Herb | 336 | 712 | 1,232 |
| Sunflower | 140 | 1,124 | 1,244 |
| Marigold | 308 | 1,180 | 1,468 |
| Weed clump | 192 | 192 | 192 |

Both mature variants have the same topology count. Small seedlings and tools
intentionally use fewer triangles than the budget tier's typical range.

| Reusable piece | Triangles, including moving children |
| --- | ---: |
| Lumber 4×8 bed, either height | 1,012 |
| Hollow block 4×8 bed | 1,104 |
| Accessible 8×3 tray and supports | 1,016 |
| Ground 10×20 plot, board / bare | 324 / 144 |
| Tomato cage | 864 |
| Bean twine trellis / bamboo teepee | 322 / 584 |
| Three-bay compost | 1,140 |
| Standpipe, handles and hose | 1,976 |
| Rain barrel, lid and tap | 1,396 |
| Shade bench / bulletin board | 316 / 508 |
| Bucket / watering can | 476 / 702 |
| Wheelbarrow / row cover / pinwheel | 636 / 570 / 52 |
| Native framed shed, private checkpoint simplification | 4,468 |

`build/pieces.json` contains every reusable piece and plant count.
`build/check.json` contains raw accessor counts, normal lengths, external image
identities, geometry/file bytes, fresh-import comparison and measured widths.
`build/garden-<seed>.json` is the complete plan/planting manifest. Gardens stay
under 250k triangles; plants under 5k, shed under 8k, other modules under 2k.

| Garden | Triangles | Quick material slots | glTF / BIN bytes | Direct texture memory |
| --- | ---: | ---: | ---: | ---: |
| 117 | 144,189 | 33 | 487,598 / 7,315,300 | 8 MiB |
| 229 | 214,898 | 34 | 502,739 / 5,826,348 | 24 MiB |
| 341 | 137,582 | 34 | 510,626 / 6,910,468 | 24 MiB |

Fence bays are 492–508 triangles, the 5ft/6ft gate assemblies 612/620 and
the open gutter/downpipe 636. These are placed modular pieces, counted from
the exports. Broad scene totals count every plant instance; BIN sizes benefit
from shared meshes. Material slots are provisional for construction review
and exceed the final atlas/draw-call target.

Measured main-spine minima are 1.524 / 1.524 / 1.8288m, sampled at intervals
no greater than six inches. Actual gate hardware leaves 1.43884 / 1.43884 /
1.74364m clear. Minimum measured edge-to-edge gaps are .91440 / 1.15840 /
1.05451m; the third figure includes planter/post geometry rather than only the
nominal board rectangles. Gardener socket heights agree with actual imported
walking surfaces within 0.001mm. Nine rays through the high bed's knee corridor
are clear through 27in height; an upward ray measures .69730m to its bearer.
These checks prove the modeled construction; triangle/bounds re-import checks
separately prove serialization. Motion checks sample gate and placed shed doors
every 5°, omitting open alpha sheets and allowing no solid penetration.

Actual soil rays check 116 / 135 / 106 planted roots, with 4.8–18.4mm of root
penetration rather than floating caps. Cage feet reach approximately 19–20cm
below the local soil; timber tomato stakes reach 30cm, trellis/bamboo feet 20cm.
The latter dimensions are authored construction lengths; cage/plant contact
ranges are measured from the imported mesh. Crop layouts follow a bed's long
axis even when the frame is transverse; flowers/weeds stay within its actual
soil opening. Teepee radii contract to fit narrow block-bed soil openings.

Delivery is `export/checkpoint/Garden_<seed>.gltf` plus its BIN;
`CommunityGardenPieces.gltf` is the overlapping-root reusable library. Select
and instance a named library root; the inspection sheet lays roots out only
for presentation. The three garden files reference the same external image
identities. Canonical images remain outside `export/`; preserve the relative
directory layout or remap URIs when packaging an engine scene.

`Site_<seed>.gltf` packages that garden with the native street, buildings,
trees, cars and utility context. The renderer exports this assembly and
re-imports it before drawing the checkpoint views. Existing maps remain
external where their file identity is available; packed native maps are
losslessly externalized into one shared `textures/context/` cache by content
hash. That cache contains native image copies, not a new authored texture set.
Native context costs are recorded separately in `build/context/costs-*.json`,
and scene/package identities in `build/context/site-*.json`. The 250k limit
applies to the garden, not the surrounding town already present in the library.

| Packaged scene | Total triangles | Native context triangles | Unique image memory | glTF / BIN bytes |
| --- | ---: | ---: | ---: | ---: |
| Site 117 | 914,132 | 769,943 | 148.02 MiB | 864,911 / 34,301,148 |
| Site 229 | 1,179,900 | 965,002 | 142.00 MiB | 784,766 / 28,978,184 |
| Site 341 | 1,102,584 | 965,002 | 142.00 MiB | 792,983 / 30,090,568 |

Native vertex tints are preserved as material-driven `COLOR_0`; garden wind
remains `_WIND` and is never exported as base-color modulation. Scene checks
verify that separation and every garden image's original byte identity.
Memory assumes 8bpp block compression and full mips per unique map, excluding
geometry/engine overhead. External PNG storage is 86.37MB for Site 117 and
82.52MB for each other scene; all seeds share canonical files.

One native-car MikkTSpace corner can straddle a four-decimal tangent rounding
boundary on re-export. The packager preserves that corner's original native
tangent, guarded by exact position/normal/UV signatures and a maximum one-step
change. The native input stays untouched; no general quantization is applied.

The new temporary plant set is 1024² BaseColor-alpha / +Y Normal / ORM:
**4 MiB compressed with full mips**, shared across every crop/stage/seed. Its
unused leaf tile also holds bird netting. Normal/ORM are deliberately simple
checkpoint maps. The fence field is the native 1024 analytic wire set rebuilt
in this family's private cache: **4 MiB**, intended to point at the canonical
fence atlas during look-dev. Garden lawn reuses Ground's 2048 set: **16 MiB**.
Lumber, soil and equipment use uniform checkpoint values, allocating no maps.
Presentation-only context additionally reuses native ground, tree, building,
car and utility maps; this is separately costed from the garden itself.
No new final lumber/soil set is allocated at this checkpoint.

Garden root: centre of fence footprint at grade, metres, Blender +Z up and −Y
front. glTF converts to +Y up and +Z front. `GateLeaf` pivots about its left
hinge, Z −110°…0°; checkpoint is open at −85°. The native shed keeps both
hinged door pivots and their authored ranges. `BarrowWheel` is X ±360°;
`PinwheelRotor` is Y ±360°. `BibWheel_Left/Right` are Z 0°…720°;
`BarrelTapLever` is Z 0°…90°; `BarrelLid` slides Z 0…0.30m. Plot sockets sit 470mm outside the front edge,
facing the plot; `Socket_Standpipe` stands at its bibs. These are gardener
placement sockets, not animation or reach certification.

```sh
make -C community-garden                    # checkpoint only
make -C community-garden check
make -C community-garden match              # three local photo comparisons
make -C community-garden repeat             # deterministic geometry/image proof
make -C community-garden render WIDTH=1440 SAMPLES=40
make -C community-garden model SEEDS=118 ARCHETYPE=city # alternate plan instance
```

`src/plan.py` owns footprints, plot banks, bed dimensions, court/aisle widths
and service positions. `SEEDS` chooses integer garden seeds; `ARCHETYPE`
optionally overrides the seed-modulo-three archetype. Seeds choose five care
states, two mature specimens, plant rotation, skipped plants, weeds, straw and
watered root zones. `plants.build(species, stage, seed, support_radius)` exposes
botanical generation separately; the shared catalogue starts at seed 713,
with .28/.64/1.0 stages. The default check/render suite covers the three
curated seeds; alternate-seed `model` builds do not imply that suite has
certified an arbitrary new layout.

Native context exports live in the same clone (trees, houses, apartments, cars,
utility and Ground textures). `make` builds a missing prerequisite; existing
deliveries are read-only inputs. `make clean` removes only this family's build/render cache. Requires
Blender 5.2, Python/Pillow/NumPy, fontconfig/Noto Sans and flock. All Cycles work
holds the shared kit GPU lock. No kit or top-level index change.

Renders and contact sheets stay under `renders/`; no checkpoint JPG enters
git history. Form critique and remaining weaknesses are in [REVIEW.md](REVIEW.md).

The checkpoint views are `renders/checkpoint/<seed>/{hero,above,corner,compost,
water,tomato,bean}.png`, with `above-annotated.jpg` for plot/path dimensions.
Seed 341 also has `accessible.png`; 117 has `scale.png` and `eevee.png`.
`plants.png` shows every stage/variant; `pieces.png` shows construction modules.
The three period photo comparisons and calibration overlays are in
`renders/checkpoint/matches/`. `contact.jpg`, `heroes.jpg`, `details.jpg` and
`matched-contact.jpg` collect them. Render receipts record the actual imported
glTF/BIN/image bundle hash; review rejects stale exports or camera recipes.

Remaining limits: uniform checkpoint materials and provisional UVs; coarse
wet-soil value boundaries; vegetation less tangled than the mature photo;
an approximate Oliver camera fit with occluded landmarks; a traditional raised
shed threshold. The firm routes and measured knee opening support the design,
but this is not a blanket ADA compliance claim. Later look-dev must consolidate
material slots, bake construction detail/wear, develop leaf response and
recheck the exported result. No final lumber/soil atlas or material approval is
implied by this checkpoint.

The park plan remains especially regular and underplanted; path-shoulder
corners also need a finishing pass. Every curated garden retains all five
care states, including a visibly mulched fallow plot.

Validation: `make`, `make check`, `make scenes check-scenes` and `make repeat`
pass. Repeat compares all seven glTF/BIN deliveries and regenerates the three
analytic plant maps byte-for-byte. Render provenance checks 29 source-bundle
receipts. A separate preservation audit found all 312 pre-existing delivery,
texture and docs files unchanged. `REVIEW.md` records four critique passes.
No kit or top-level README change, and no preview image is committed.
