# Civic buildings — form and construction checkpoint

An original civic kit for a maintained American town in 2010: a 1928 brick and limestone city hall with a 1976 police wing and 1994 accessible vestibule, and a 1974 three-bay fire station with a later exhaust retrofit. Seven building examples and two different parcels use the library's existing baked surfaces. Every vertex and texel comes from this repository's scripts.

**This stops before look-dev and final delivery.** There is no committed gallery. Full-size exported-asset evidence is in [renders/checkpoint](renders/checkpoint/), its [contact sheet](renders/checkpoint/contact.jpg), and the [photographic comparisons](renders/matches/contact.jpg). [REVIEW.md](REVIEW.md) records rejected views, construction fixes and remaining CG tells. [REFERENCE.md](REFERENCE.md) distinguishes published comparators from original dimensions; [refs/SOURCES.md](refs/SOURCES.md) records exact sources and rights.

## Program grammar

`src/plans.py::building(seed, program, style, bays, bay_width, stories, order, roof, wings)` is independent of Blender. `buildings.hall()` and `station.station()` assemble its result from common construction functions. The CLI writes custom results inside `build/custom/`, leaving the proof packages alone:

```sh
make dependencies
blender -b --factory-startup --python-exit-code 1 --python src/build.py -- \
  --program library --seed 919 --style colonial --bays 9 --bay-width 4.18 \
  --stories 2 --order pilasters --roof hip --no-wings --directory build/custom-919
```

Historic programs are `hall`, `post_office` and `library`: Classical or Colonial, 3–11 odd frontage bays, at least 3m pitch, 1–3 stories, columns/pilasters/plain, parapet/hip/cupola, and an optional later annex. The central entry occupies its own bay. Station programs have 2–4 apparatus bays at least 4.8m apart, one or two crew-wing stories, a plain modern entry, parapet or hip roof, and an optional crew/office wing. Unsupported combinations fail explicitly. The seed controls selected sash replacements and site occupancy; the two proof sites have different program-specific layouts rather than one reskinned parcel.

## Dimensions and construction

| Feature | Authored size / source comparison |
| --- | --- |
| Main hall | 29.2608 × 17.6784m / 96 × 58ft; two 3.9624m story pitches over a .9144m plinth |
| Hall entry | Four Tuscan columns, 7.3748m shaft/order height, .878m nominal diameter; molded bases, tapered shafts, necks, capitals and bearing architrave |
| Stair | Six 152.4mm risers, 330.2mm goings, 8.6m width, jointed stone treads, bearing cheeks and 42mm handrail tube |
| Historic sash | 1.3716 × 2.4384m / 4ft6in × 8ft; six-over-six glazing with masonry returns, separate frames, lintels and projecting sills |
| Police wing | 14.6304 × 12.192m / 48 × 40ft; different brick, aluminum windows and yard-facing operating entry |
| Apparatus hall | Three 5.4864m / 18ft centers; 18.288m / 60ft depth; measured clear openings 4.2672 × 4.2672m / 14 × 14ft |
| Tower | 3.6576m / 12ft masonry square, 12.8m to wall head; projecting training landings, braces, ladder and railings |
| Apron | About 26.86m from bay face to lowered sidewalk, graded to the arterial, with a transverse trench drain; wheel lanes and standing-engine drips belong to each bay |
| Later accessible links | 1.8m clear ramp skins, 7.4% and 6.73% running grades; street/lot paths reach real thresholds. These are selected geometric checks, not a whole-site code certificate |

HABS MA-995, LA-1127 and NJ-357 supply elevation, plan and molding studies. The National Register brick/limestone nomination documents civic masonry, raised bases, cornices and later additions. Fire Engineering's 1989 guide describes roughly 15ft-wide / 40ft-deep single bays and larger apparatus doors; the new design deliberately uses more width/depth. Tubac supplies a later 14×14ft cross-check. USFA and the NFPA source-capture report inform the exhaust retrofit and separation of the shallow bay from living quarters. The 2018 USFA guide recommends a taller 16ft opening; this asset represents an older 14ft station. All town names, dates, inscriptions and agency graphics are fictional.

The hall assembly including additions/portico spans 33.271 × 35.600 × 10.377m; the station including tower/landings spans 28.839 × 22.882 × 13.078m. Their parcels are 80 × 68m and 86 × 66m. These are original design envelopes, not measurements attributed to a real building.

Windows have actual openings, glazing, blinds and dim room layers. `CivicRoomGlow` and `CivicBayDiffusers` carry `switch_kind=interior_lights`; a game can change their emission. Only the apparatus volume has a modeled inspection interior: floor, beams, racks, hanging coats/helmets/boots, 150mm exhaust hoses, ducts, lights and door tracks. There is no apparatus model or playable civic interior.

## Modules

`export/CivicPieces.gltf` is an inspection library with independent roots arranged in a grid. Replace a selected root's transform when placing it. Structural modules use construction datums: wall/window front line and sill, column foot, cornice bearing, door threshold, roof underside. Fine brick and manufactured detail remains in the shared normal maps.

| Module | Triangles | Module | Triangles |
| --- | ---: | --- | ---: |
| Wall bay with sash | 776 | Tall sash | 644 |
| Aluminum sash | 572 | Cornice run | 836 |
| Tuscan column | 756 | Pilaster | 132 |
| Operating entry/frame | 528 | Stone stair/rails | 872 |
| Complete overhead door/track | 1,856 | HVAC | 484 |
| Turnout rack/gear | 736 | Bollard | 88 |
| Scupper/downspouts | 504 | Plain fascia | 88 |
| Roof panel | 24 | Hose/training tower | 10,708 |

Small planar/simple parts remain below the nominal modular range; no triangles are added to meet a minimum. The tower uses its separate 12k allowance. Per-construction-object counts for every building are in `build/family.json`, and the complete module measurements are in `build/modules.json`.

## Proof packages and resources

| Export | Triangles | Materials | glTF + BIN bytes |
| --- | ---: | ---: | ---: |
| Civic-101, city hall + police | 84,044 | 6 | 11,691,917 |
| Civic-202, three-bay station | 39,800 | 8 | 5,276,570 |
| Civic-303, post office | 38,192 | 6 | 5,374,717 |
| Civic-404, cupola library | 54,552 | 6 | 7,810,099 |
| Civic-505, two-bay/two-story station | 43,564 | 8 | 5,845,399 |
| Civic-606, small plain hall | 36,048 | 6 | 4,936,557 |
| Civic-707, larger 11-bay hall | 87,948 | 6 | 12,467,114 |
| Site-101, including plants | 325,768 | 21 | 20,702,927 |
| Site-202, including plants | 228,810 | 22 | 14,513,140 |

Static site counts excluding vegetation are **142,300** and **69,022**, within 250k. Included trees/shrubs account for **183,468** and **159,788** placed triangles respectively. The hall has 13/19 occupied stalls and the station 6/9, with reserved route/service access kept free. Cars are presentation actors outside those packages; `build/cars-101.json` and `cars-202.json` report their actual placed/stored counts. Native vehicle geometry/maps are shared, with documented factory color decoding, parked lamps off and a separate fictional police roof upfit. The presentation car totals are 1,573,994 placed / 130,816 unique triangles for 23 hall actors and 945,752 / 129,496 for 14 station actors, with 13/11 material resources. Their two native 2048 triples add about 32 MiB shared across the actors. Context has no frame-rate guarantee; an engine needs instance batching, LODs and culling.

All packages are stock glTF + BIN with external images. Canonical relative image URIs are shared across modules and seeds. Preserve that layout or remap resolved URIs to an engine image cache. `build/review/*.glb` embeds the **same BIN and exact images** solely for fresh-import evidence. Building roots are centered on their physical footprint at grade, Blender −Y front / +Z up; glTF +Z front / +Y up. Site roots are parcel centers; `origin_offset_m` converts their construction-plan coordinates. All authored mesh scales are applied.

| Reused maps | Sizes / compressed full-mip estimate |
| --- | --- |
| Downtown masonry, mineral/roof, finish | 2048 triple + 1024 triple + 2048 triple / 36 MiB |
| Commercial painted block | 1024 triple / 4 MiB |
| Ground asphalt, concrete, lawn, trim/decals | Three 2048 triples + one 1024 triple / 52 MiB |
| Native maple and oak | Two 2048 triples / 32 MiB |
| Native boxwood/hydrangea atlas, boxwood root selected | 2048 triple / 16 MiB |
| Native chain-link | 2048 triple / 16 MiB |

**36 unique images / 156 MiB shared across this family, zero new civic image sets.** The resolved PNGs total 91,629,693 disk bytes. PNG disk bytes and uniform glass/emission materials are separate from that allocation. Missing Downtown/Commercial maps are rebuilt through their unchanged 4096 recipes inside civic-owned folders. No existing delivery is rewritten. Furniture and utility context use native form adapters; this is explicitly weaker than their final material deliveries.

## Pivots, sockets and paths

Custom axis/vector extras (`pivot_axis`, `points_m` and door guide vectors) retain the authored Blender frame: meters, +Z up, −Y front. For a native glTF engine, map a vector `(x,y,z)` to `(x,z,-y)` before applying the glTF node world matrix. Ordinary node transforms and mesh attributes are already converted by the exporter. Path points are local to their named path node, including its parcel-centering transform.

- Entry leaves rotate 0–90° about their physical local +Z hinges, with one shared center mullion and real clearance.
- Each overhead door has eight independently named sections with hinge origins, pitch, 420mm bend radius and nominal opening metadata. `src/door_motion.py::pose(objects, progress, rest)` preserves chord length while following the vertical/curved/horizontal track, including imported quaternion objects. Use progress 0–1 and retain its returned rest matrices. No armature is required.
- `Socket_Apparatus_*` is each apparatus center; `*_Stall_*` is each parked-car center, with occupancy/police metadata. `Path_*` nodes retain `points_m`, `path_kind` and `clear_width_m`; Blender curves become metadata-bearing glTF nodes for engine paths. The lowered apron exits, staff drive, public/police connector and service access are separate drive paths. The police aisle has a 6m vehicle opening; the hall service bay is kept unoccupied. Street crossings omit curb and raised sidewalk, with lights and trees clear of the drives.
- Flags have +Z pivots; dumpster lid is −X rotation and enclosure gates open in opposite +Z directions. Their metadata is available, but only front and sectional doors have sampled motion certification at this checkpoint.

## Rebuild and verification

```sh
make                  # refs, shared dependencies, programs/sites, checks, exports, Cycles evidence, pairs, contact
make check            # raw glTF, fresh import, UV/normal/scale, ramps, drives, parked-car/walk envelopes, door motion, repository
make repeat           # exact 56-file package/map repeat; clean Blender geometry rebuild, shared maps retained
make WIDTH=1000 SAMPLES=20 render
```

All Cycles work uses `kit/with_gpu.sh` and the inherited GPU lock, one lock per render set. `build/check.json`, `motion-check.json`, `repeat.json` and `render-check.json` retain measured evidence. Door sweeps use the existing kit BVH/edge-interval check and Downtown's oriented-solid-angle membership, including its positive/negative fixtures. Rolling guide contact is explicitly excluded; all other fixed surfaces remain. This is sampled geometry, not continuous mechanical simulation. A separate route check uses the measured native sedan box at occupied sockets, expanded by each walking path half-width: 182 + 42 segment/vehicle pairs, zero overlaps. It certifies that conservative parking-placement envelope, not full traffic motion.

The native oak has one known MikkTSpace corner that may re-encode by .0001. New civic packages restore its accepted original tangent with the kit's existing exact position/normal/UV signature guard; no other field or canonical file changes. Exact repeats are measured after that bounded preservation step. Shared GPU maps are retained during `repeat`, not claimed as a fresh byte-identical GPU rebake.

The source-surface bearing audit rays all 20 lowest foot vertices of five rooftop units against actual roof triangles: maximum measured gap is zero. Hip/cupola examples omit that rooftop unit. This proves source bearing; the separate fresh-import bounds/count audit proves serialization, and image receipts prove which exports were rendered. Neither substitutes for the photographic critique.

Remaining weaknesses: stone/roof aging is still too clean; masonry repairs and caused deposits need the look-dev pass; the lawns and repeated context parcels remain too orderly; apron oil/scuff stamps remain patterned in close view; there are no pigeon/dropping details yet. Generic gear and window-room layers are inexpensive exterior cues. The photo fits compare different original designs, including an 11-bay generator example for the larger hall photograph; they do not certify a reconstruction or every feature of the two seeded sites. Native family exports and Ground/tree/shrub maps are prerequisites supplied by the library; `make dependencies` rebuilds only the missing Downtown/Commercial recipes and local form adapters. No kit or top-level README changes.
