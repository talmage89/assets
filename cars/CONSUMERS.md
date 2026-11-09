# Native car consumers

Round two follows the subdivision evidence in [DETERMINISM.md](DETERMINISM.md).
The car modeling code stays unchanged. Its one-thread form builds already
repeat exactly; consumers must use the same thread count for native generation.

## Direct native source launches outside cars

| Family / entry | Native car cache | Previous launch | Current launch |
| --- | --- | --- | --- |
| `downtown/src/context.py:ensure` | Pickup, crossover, hatchback `.blend`, through `downtown/src/context_build.py` | Blender automatic threads | One thread for these three cases |
| `school/src/dependencies.py:car_cache` | The same three native `.blend` cars | Four threads | One thread |
| `school/src/dependencies.py`, car export | Hatchback's simplified school context GLB | Four threads | One thread; shrub export stays at four |
| `parking-garage/src/dependencies.py:build_context` | Native hatchback/crossover GLBs, through its adapter and downtown's source builder | Four threads | One thread; town recipes and surface audits stay at two |
| `apartments/Makefile`, `build/context/car/source.blend` | Native pickup form through `apartments/src/context_build.py` | Four threads | One thread; other context rules stay at four |
| `utility/src/context.py:prepare` | Full native pickup source in a private copy of `cars/src` | Four threads | One thread; house, tree, light and ground launches stay at four |

`utility/src/context_build.py` also exposes a manual `--role pickup` form
adapter. No repository launcher selects that role: the production context job
uses its default ground role and builds the pickup through `cars/src/build.py`.
Manual native car commands should use
`python3 kit/blender_command.py --threads 1 -- blender ...`.

The shared `kit.blender_command.with_threads` changes only Blender thread flags
before `--`. It retains the executable/wrapper, other options and script argv.
Downtown and utility car recipe signatures include the new policy. School and
garage car caches carry a one-thread marker; older caches regenerate once.
Apartments' car Make rule depends on the helper. The garage's original surface
guards and three-attempt limit remain in place.

## Canonical car Make consumers

These invoke the cars' own Makefile for missing canonical deliveries. X220,
H120 and S240 already append `-t 1`; round two adds the same override to the
pickup's command. This also overrides a caller's inherited thread flag. Their
car generation needs no second override:

- `apartments/src/dependencies.py`
- `commercial/src/context.py`
- `signals/src/context.py`
- `freeway/src/dependencies.py`
- `community-garden/Makefile`
- `coffee-shop/Makefile`
- `minigolf/Makefile` (pickup and sedan)
- `trailer-park/src/dependencies.py` (private source archive when absent)

The pickup override is checked against three independent native one-thread
source builds: all 472 objects / 454 meshes match the accepted source exactly
in transforms, hierarchy, vertices, faces, split normals and material names.
Its accepted GLB stays at 59,838 triangles with receipt
`f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
The comparisons are `round2/utility-{1,2,3}/pickup-preservation.json` under
`build/cars-determinism/`.

Church, civic and other presentation adapters import existing canonical car
deliveries rather than generating native car source. River's school-context
dependency reaches the corrected school cache path. Its native town adapter
builds buildings, not another car generator. Downtown's building-only adapters
in church, civic and coffee shop likewise need no thread change.

## Proof scope

Cold cache verification uses separate empty folders and serial Blender
processes. Blend-only consumers are compared through a common stock glTF
export of their native cache, with identical export settings and extras.
Their procedural source finishes differ from the cars' baked deliveries;
those formats are not interchangeable hash references. Downtown and school
use the same native source format and can be compared directly.

Raw `.blend` container receipts remain audit provenance. An exact guard for
a blend-only consumer should compare its GLB or mesh arrays; one thread does
not promise identical serialized viewport state or container bytes.

`python3 cars/src/test_consumers.py` checks launch arguments, old-cache
invalidation, new-cache reuse and preservation of non-car thread counts.
`python3 -m unittest kit.test_blender_command` checks the shared override,
including wrappers and script arguments that themselves contain thread flags.

## Downstream exact guards

The garage's native car cache hashes and `context_repeat.py` could require
exact bytes after accepting the new fixed-recipe hashes and replacing older
four-thread caches. Its immutable accepted surface baselines remain useful
independent preservation checks.

The garage's `context_embedded.py` / `embedded_repeat.py` car exception also
needs refreshed fixed car caches, rebuilt owned form/look-dev site baselines,
and the full `make repeat` proof before requiring exact car payloads.

Church and civic already compare their own packages exactly while keeping
canonical native cars immutable; river also has an exact package repeat and
reuses school's car cache. Their guards need no new tolerance rule. Adopting
changed car inputs still needs their input receipts/owned caches refreshed
and their full repeat checks run. No whole sites are rebuilt here. On the
next build, site counts may move by the few triangles contributed by the
corrected native car caches.

## H120 metadata proof

The source of the varying metadata is `hatch_detail.py`, which used to copy
the SHA-256 of its form `.blend` into Scene `form_source_sha256`. This is not
an exporter timestamp. The compressed containers differ even with identical
mesh arrays: unpacking their own SDNA locates the first difference in one pair
at Mesh offset 1560, `face_sets_color_seed`. Three cold forms hold
−413440761 / −1424484633 / 1491297234 there. Viewport color state cannot identify
a delivery. Other container differences also exist; their hashes remain useful
as audit provenance, rather than as stable mesh identifiers.

The detail script now records that receipt in its counts JSON and removes
any inherited Scene value. `src/hatch_metadata_repeat.py` exercises that actual
function with three different cold form receipts, then performs three stock
kit exports of the accepted finalized mesh/UVs and accepted maps. All three
give **59,852 triangles**, **7,892,160 bytes**, SHA-256
`4cdbafe2a1436f031eb58caf8fbd3a80b6a4e2eed65842fe0c293e2ff62baeb9`.
The complete BIN chunk is byte-identical to the accepted H120. The complete
JSON is identical after removing only Scene `form_source_sha256`. This
replaces `86104add5c3aaa7bf909af12fc666f9a0ef87f635df2b0e7ce7639c247f1136e`
(7,892,248 bytes); no geometry, UV, map or docs image changes.

Proof receipt: `build/cars-determinism/round2/hatch-metadata/repeat.json`.
This isolates the metadata fix and reuses accepted finalized geometry/maps;
it does not claim three fresh GPU bakes. The three independent one-thread
form builds are the round-one builds documented in `DETERMINISM.md`.
The regression also passes against the already-corrected delivery baseline,
with the same three GLB receipts (`hatch-metadata-current-baseline/repeat.json`).

## Three-cold native cache proof

Every row has three separate factory-empty native builds per consumer and
byte-identical GLBs in all three. Downtown and school each build all three
bodies independently; their corresponding source-cache projections also
match each other. School's simplified cache uses its actual export adapter.
Blend-only cache projections use the same stock glTF settings in every run.

The projection worker opens the native cache in a fresh one-thread Blender
process and calls:

```python
bpy.ops.export_scene.gltf(
    filepath=str(target), export_format='GLB', export_extras=True,
    export_animations=False, export_apply=True, export_tangents=False)
```

It checks the declared GLB and BIN lengths before the direct worker exit.

| Consumer / native car | Triangles, each run | SHA-256, each run |
| --- | ---: | --- |
| Garage H120 | 58,020 | `60b25083a8e6c8c0fde7f3624517ef326827e1b5e7bca5c1204ffc0d09ecb079` |
| Garage X220 | 73,382 | `8c2230440ab2ca3fdec2255a03ef71672203a19d4194b222569827bd09247b1f` |
| Downtown and school C150 | 50,434 | `8f9f85bbbdd6c15c48f0f1a0ce9e19534ed4e4027ed56ef434f3065b6bab72b3` |
| Downtown and school X220 | 73,382 | `7ebf13799ec6b70e6c6732358a654e5e1039c9210e8e460d2445ba3c6db58c6f` |
| Downtown and school H120 | 58,020 | `f6f9b59db0ce3478c5947e19c22f5f5d9e18cf7a4679b2685c0d6d5accb9209a` |
| School simplified H120 | 43,179 | `421b26f8fecbdb3156f6791a9b8508f9b1369407e40bdee62c695594cc0b2139` |
| Apartments C150 form | 38,226 | `d38d0d93fb261ba9e8b1eba00d43624a9c9ced80cf5ddd66b810a0c9d94d62f1` |
| Utility C150 full source | 59,838 | `4683c56869223b2b177ea97088f4a80c2254e21de6a64b3ceb445b164b322037` |

Combined receipts: `build/cars-determinism/round2/garage-proof.json` and
`build/cars-determinism/round2/consumer-proof.json`, with the separate build
folders, generation/export logs and pickup source comparisons beside them.
The real consumer functions/command constructors generate only their car
caches; no complete site builder runs. The diagnostic stock exporter follows
the garage's existing complete-container validation/direct-exit pattern for
Blender's native-node teardown crash. Its initial failed diagnostic log is
retained. No native generator failure was ignored.

Only the garage's two expected native cache hashes change in source; its
immutable accepted surface baselines remain intact. All six new caches pass
the old guards. H120 is 12 triangles lower than 58,032 (0.02068%), with a
maximum sampled distance of 0.832915 mm over 7,020 points. X220 is 44 lower
than 73,426 (0.05993%), maximum 0.855972 mm over 8,250 points. These are
sampled preservation measurements, not whole-surface maxima.

Each direct consumer family's REVIEW records its receipts and warns that
site counts may move by these few car triangles on the next site build.
Existing family deliveries and docs remain accepted; whole-site repeat
proofs and any change to tolerance guards are deferred.

## Corresponding form geometry

The native source adapter adds exterior construction to the cars' form stage.
`suv_exterior.fuel_pocket` cuts the left rear quarter; `hatch_exterior.py`
partitions front side glazing into fixed and moving panes. These documented
stage changes explain the differing form/detail meshes in the array probe.

All other shared skins match the cars' original one-thread cold forms exactly:
**44 X220 meshes / 38,856 triangles**, **27 H120 meshes / 28,521 triangles**,
including positions, corner indices/polygon topology, split normals, transforms
and UV layers. The receipt is
`build/cars-determinism/round2/form-cache-match.json`, which records the
expected detail operations and zero unexpected changes. The modified detail
objects remain included in every complete native GLB repeat above. Utility's
three full C150 sources also match the accepted source, as recorded earlier.

## Validation and preservation

- `python3 cars/src/test_consumers.py`: six launch/cache tests pass.
- Every `kit/test_*.py`: **38 files pass**, from fresh fixture folders,
  separate Blender processes, serial GPU locking; results and logs are in
  `build/cars-determinism/round2/kit-tests/`.
- Pickup and H120 `make check`: pass with accepted model/map/export stages
  frozen and check receipts forced. Exact `-B` / `-o` argument lists are in
  `round2/{pickup,hatch}-check-argv.json`; this checks accepted geometry,
  normals, UVs, motions, repeat arrays and re-import without a GPU rebake.
- S240 and X220: direct `kit/verify.py` delivery checks pass.
- Repository check: **2,647 source files, zero errors**; `git diff --check`
  passes. Full-site `make check` / `make repeat` were not run in this session.

The final 819-file delivery/map/docs snapshot differs only at
`cars/export/AlderH120.glb`. All 35 existing car texture PNGs and 19 car docs
images retain their bytes. No committed docs image, `houses/`, `kit/lod*` or
top-level README changed. No asset render was made. Preservation receipts are
in `build/cars-determinism/round2/preservation-final.json`.

| Accepted delivery | Triangles | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| C150, unchanged | 59,838 | 11,530,736 | `f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65` |
| S240, unchanged | 69,658 | 10,140,724 | `3b907074594759b4247e379b1535a4700f3ecdbcfcd67cd1b967390c2fe1ebfa` |
| X220, unchanged | 64,933 | 9,061,700 | `75fc9507347fbc96ae0af8204a59168f63098eeee8a9dd43362ad350a75c1e82` |
| H120, metadata only | 59,852 | 7,892,160 | `4cdbafe2a1436f031eb58caf8fbd3a80b6a4e2eed65842fe0c293e2ff62baeb9` |

Each retains four materials and three embedded 2048-square PNG maps. The
accepted geometry and texture budgets are unchanged.
