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

The pickup override is checked against an independent native one-thread
source build: all 472 objects / 454 meshes match the accepted source exactly
in transforms, hierarchy, vertices, faces, split normals and material names.
Its accepted GLB stays at 59,838 triangles with receipt
`f3efff732a4edc3d9353bf2bf7b583b49f3a0a5f9be7932f1041c5729f965c65`.
The source comparison is `round2/utility-1/pickup-preservation.json` under
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

Complete-site car exceptions, including the garage's embedded repeat guard,
need each site's car caches/immutable input receipts refreshed, its owned site
baseline rebuilt, and its full repeat check run before becoming exact. The
same applies to churches, civic, river and the other families' accepted site
receipts. No whole sites are rebuilt here. On their next build, site counts
may move by the few triangles contributed by the corrected native car caches.

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
