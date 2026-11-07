# Roadside miniature golf — correction checkpoint

**Not ready for delivery.** The latest exported crops still fail the rock,
waterfall and adventure-landscape visual gate. No final gallery or `docs/`
images have been generated. [REVIEW.md](REVIEW.md) records three additional
native-size critiques, rejected candidates and the remaining faults.

Two original seeded 18-hole courses: **Bramble Putt**, an older repainted
classic, and **Cairn Creek**, a newer 1990s-style harbor/quarry adventure.
The accepted classic routing, clubhouse, themed fixtures and roadside town
remain. The correction replaces the black water with shallow painted basins,
adds cast concrete coping to the classic pond, replaces the adventure ring
with retained rows and winding links, and externalizes the shared images.
The enlarged quarry is still too blocky, its rock too smooth/uniform, and
its waterfall too regular. Passing the construction checks does not accept
those surfaces as realistic.

[Dimensions and construction sources](REFERENCE.md),
[reference credits](refs/SOURCES.md), [texture allocation](TEXTURES.md).
All geometry, graphics and material fields are scripted originals. Reference
pixels never enter the asset. Text uses installed open-license DejaVu Sans.

## Current exports and costs

| Seed / kind | Construction triangles | glTF + BIN bytes | Materials | Core image memory |
| --- | ---: | ---: | ---: | ---: |
| 71 / classic | 122,214 | 14,113,011 | 11 | 81⅓ MiB |
| 92 / adventure | 171,691 | 20,591,617 | 11 | 81⅓ MiB |

Hole construction remains **4,144–5,512 classic / 4,816–7,166 adventure**,
including the carpet, slab edge, border, tee, sign, cup and flag; fixtures are
counted separately. Both retain the accepted 2k–8k hole ceiling. Fixture
triangles remain castle **3,524**, covered bridge **988**, lighthouse **3,084**,
windmill **5,536**, shipwreck **6,428**, below the 15k ceiling.

| Optional native landscape | Placed / unique mesh triangles | glTF + BIN bytes |
| --- | ---: | ---: |
| 71 | 475,578 / 71,272 | 9,859,962 |
| 92 | 634,154 / 71,272 | 9,885,384 |

The plants retain linked native mesh instances. Complete construction plus
plants is **597,792 / 805,845 placed triangles**, and **23,972,973 /
30,477,001 geometry/JSON bytes**. These totals include the optional plants;
the construction totals above do not. The surrounding commercial road, town,
cars, poles and distant trees are presentation only.

Both complete scenes reference the same **25 canonical PNG files**:
**129⅓ MiB** at 8-bpp block compression with full mip chains, assuming an engine
caches images by normalized URI. This is one shared allocation across seeds.
**17⅓ MiB is new**; Ground, lumber and native plants reuse their existing sets.
PNG disk bytes and serialized geometry bytes are separate from GPU allocation.
`build/costs.json` records individual image sizes, bytes and placed primitives.

| Generated path | Contents |
| --- | --- |
| `export/Minigolf-{71,92}.gltf` + `.bin` | Complete construction, pivots and sockets |
| `export/Minigolf-{71,92}-landscape.gltf` + `.bin` | Co-located optional native shrubs and six perimeter trees |
| `export/MinigolfPieces.gltf` + `.bin` | 36 selectable hole roots and five standalone fixtures, coincident at the origin; 23,561,276 geometry/JSON bytes, 65⅓ MiB of shared maps |
| `textures/ship/T_Minigolf_*.png` | Shared 2048² BaseColor, OpenGL +Y Normal, ORM; 1024² graphics |
| `build/embedded/*.glb` | Embedded verification mirrors; not the delivery format |
| `build/source-construction.json`, `check.json` | Measured source construction and independent fresh-import tests |
| `build/look-check.json`, `external-check.json`, `costs.json` | UV/normal, image identity, indexed-corner equality and allocation receipts |
| `renders/fixes/*-pair.jpg` | Before/after correction panels, 1440 px per panel |

Preserve relative image URIs. They reference one copy in this family's
`textures/ship/` and the canonical `ground/`, `fences/`, `trees/` and `shrubs/`
image folders. There is no copied `export/textures/` delivery directory.
External and embedded mirrors are compared by actual indexed corner attributes
and image payloads, separately from the construction checks.

## Dimensions and construction

| Element | Dimensions / basis |
| --- | --- |
| Construction parcels | Classic 49 × 56 m; adventure 64 × 65 m, including parking and clubhouse |
| Holes | 5.2–8.6 m centerline; 2.0–3.6576 m nominal width; original seeded necks, heads and bends |
| Base / carpet | .1016 m slab edge and .0048 m nominal carpet offset; Harris sections / Wittek comparator |
| Cup | .10795 m clear opening, .1016 m liner depth, 2 mm wall, open 20 mm drain; Wittek/TNT comparator |
| Tee | .9144 × .6096 × .003175 m rubber pad with drilled start pocket, number/par, scorecard shelf and pencil; Wittek stock class |
| Borders | .1524 m painted curb, brick, .0889/.1397 m timber, carved rock banks; original arrangement |
| Water | Main surface -.17 m, main painted floor -.36 m; shallow stream with 35/45 mm downstream riffle drops |
| Waterfall | Original three-level pumped cascade, irregular carved crowns, separate liquid tongues, impact fragments, service vault and routed 63 mm return; still visually rejected |
| Footbridge | 3.6 m span, 1.524 m nominal path, 2×6 joists, .0381 m boards, 1.067 m guard |
| Fixtures | Windmill 3.20 m, lighthouse 4.73 m, castle keep 6.00 m / front turrets 4.20 m, covered ball bridge 2.30 m, wreck 2.40 m |
| Clubhouse | 6.8 × 4.6 m, sided walls, framed service sash/counter, awning, price/menu boards, stock and putter rack |
| Parking | 7.3152 m aisle, 5.4864 m stalls, 2.7432 m pitch and two 6.096 m driveways |
| Circulation | 1.524 m walks, retained grades, ten quarry risers, 1.18 m three-rail fence and twin-head night lights |

The independently measured fenced play enclosures remain **1,948.55 /
2,033.50 m²**: **9.24 / 8.85 holes per 1,000 m²**. Middletown's 22,000 sq ft
and Oak Island's approximately 18,590 sq ft plans are density comparators,
not copied layouts. The source now measures landscape-to-carpet clearance
and rock intersections against actual playing/walking triangles. Contacts,
serialization and sampled motion have separate scopes in their receipts.

## Generator, placement and moving parts

`src/plan.py::generate(seed, kind=None)` chooses dimensions, feature order,
par, bend, rise, carpet and fixture assignment. An omitted kind uses seed
parity. The documented proofs explicitly use `generate(71, 'classic')` and
`generate(92, 'adventure')`. The grammar checks 250 seeds per kind. It is a
bounded course grammar, not arbitrary parcel packing or a ball simulation.

Import a construction scene and its optional landscape companion with the
same root transform. Meters, Blender +Z up / -Y front; glTF coordinates are
`(x,z,-y)`. Course origins use the parcel center and low-grade datum. Reserve
the imported scene bounds, including native crowns beyond the construction
parcel. The course includes its own ground; surrounding game terrain must
leave its pond/stream excavation open.

For assembly, select individual roots from `MinigolfPieces`; its coincident
unplaced library is not one visible course. Each hole retains Tee/Cup sockets,
number, feature and footprint extras. Fixed parts consolidate by owner;
moving members retain independent origins. No armature or animation clips.

| Part | Blender local axis / range |
| --- | --- |
| Windmill rotor | Y, 0–360°, bored hub on its shaft |
| Castle portcullis | Z translation, 0–.40 m from raised rest |
| Clubhouse door | Z, -90–0°, hinge at the jamb |
| Service sash | X translation, -2.04–0 m; inspection poses open it 1.40 m |
| Cup-marker flags | Z, -30–30°, authored sagging cloth around the pole |

## Rebuild and inspect

Needs installed Blender 5.2, Python/NumPy/Pillow, fontconfig and flock. All
Blender work is serialized through the shared kit lock; Cycles uses the GPU.
Existing library deliveries remain read-only. No downloaded code, model,
material, texture or HDRI is used.

```sh
make -C minigolf model plants
make -C minigolf check
make -C minigolf before-after
make -C minigolf match
```

The current correction's `make check` passes. The lighthouse photo comparison
is rejected because the enlarged quarry obstructs its fitted landmarks;
`make match` consequently fails that visibility gate. The classic-green
comparison uses a course-facing refit, rather than the old lawn-dominated
camera. The geometry checks do not override the visual rejection.

The initial before images and exports are saved under
`build/revision-before/`; `before-after` uses that local accepted snapshot.
Tee/border cameras follow the relocated hole in its own frame; site views keep
exact world cameras. The framing correction intentionally refits its camera.
A final clean `make`, exact replay/GPU-tolerance proof, complete final render
inventory, final README gallery and docs commit remain outstanding. Prepared
repeat checks are not claimed to have passed this correction.
