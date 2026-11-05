# Rill / wood utility poles and overhead lines

**Form and construction checkpoint.** Original scripted US residential
distribution, maintained equipment of the 1970–2010 period. Quick materials,
exported checkpoint GLBs, four street layouts, mathematical and surface checks.
The requested stop is before look development, final UVs, baking and shipment.

After `make`, open [the hero](renders/checkpoint/101/hero.png),
[all views](renders/checkpoint/contact.jpg),
[four streets](renders/checkpoint/four-streets.jpg),
[hardware](renders/checkpoint/construction.jpg),
[photographic pairs](renders/checkpoint/matched-pairs.jpg), and
[distance-wire comparison](renders/checkpoint/wire-distance.jpg).
These are local rebuilt outputs, deliberately not committed docs images.

[REFERENCE.md](REFERENCE.md) separates published dimensions from authored
choices; [REVIEW.md](REVIEW.md) records the form critiques and limits;
[refs/SOURCES.md](refs/SOURCES.md) records authors, rights and citations.

## Construction and scale

Southern yellow pine, **ANSI class 4**, linear taper, bare cut top. WPS P25/P30
supplies the accessible depth and circumference tables, cross-checked against
the published ANSI O5.1-2008 table. Overall lengths / installation depths /
exposed heights are **35/6/29 ft**, **40/6/34 ft**, **45/6½/38½ ft**.
The six-foot-from-butt circumferences are **31½ / 33½ / 35 in**; all have
**21-in minimum tops**. Actual mesh section perimeters are measured after import.
The full buried length is recorded as metadata; only a 120 mm insertion stub
is modeled. Origins on poles are at their grade/shaft center.

A fictional **12.47/7.2 kV grounded-wye** system uses WPS-informed framing:
8/10-ft wood crossarms with flat steel braces, through bolts, pin insulators,
or seeded armless polymer posts. The brown porcelain is ANSI 55-3, **120.65 mm
shed × 95.25 mm high**. The MPS-informed 50 kVA can has a **508 mm tank** and
**1,066.8 mm bottom-to-HV-terminal height**, with formed hangers, lid clamp,
lifting eyes, cutout, arrester, bushings, secondary leads and bonds.

The three-can pole has three distinct primary phases and three independent
120/240 V secondary circuits. Center A supplies this sample's houses; B/C have
separate service sockets. No out-of-phase hots are paralleled. This is a
mechanical bank; a three-phase secondary interconnection is outside this build.
Every phase on a three-phase riser has a sealed pothead and insulated tail.

The lower space has a 6.35 mm strand, a 20 mm fiber envelope, a 28 mm telephone
cable, a .68 × .144 m inline case, hanger, clamps and returning slack loops.
Dead ends and the angle location have guy/strain/anchor assemblies with
9.525 mm guys, 15.875 mm anchor rods and 2.4384 m hollow yellow guards with
2.5 mm walls. Pole tags,
birth brands, old staples, checks and selected base vines establish the
construction; their final appearance and causal surface wear remain next-stage work.

Named light sockets mount a 60.3 mm bracket and the `street-light/` family's
head. The original head is staged from its script in the checkpoint images;
it is not joined into or re-exported with a pole. Its daytime shader is the
family's original procedural source material, not a new baked utility map.

## Four runs and cost

Each run has five poles and twelve library houses on both sides. Poles stand
in the native ground family's six-foot planting allowance, one side of the
street. Houses face the street. Native road/curb/walk geometry, maple trees,
pickup forms and the light head are presentation context only, built under
`utility/build/context/`. No neighboring asset is rebuilt in its own folder.

| Seed | Character | Pole / phases | Framing / nominal spacing |
| --- | --- | --- | --- |
| 101 | Older northern grid, Cape/ranch/split | 40 ft / 3 | 8-ft crossarm, communications, 140 ft |
| 102 | Low postwar feeder, ranch/Cape | 35 ft / 1 | Armless, communications, 110 ft |
| 103 | Small commercial edge, colonial/split | 45 ft / 3 | 10-ft crossarm, three-can rack, no comm, 185 ft |
| 104 | Later suburban rebuild, split/colonial/ranch | 40 ft / 3 | Armless polymer, communications, shallow angle, 160 ft |

Spacing jitters by ±4% from the seed. The bounded grammar is in `src/plan.py`;
the conductor API is independent of these four demonstration layouts.

| Reusable module | Measured triangles |
| --- | ---: |
| Tangent / angle | 3,592 / 3,592 |
| Dead end | 3,016 |
| Transformer pole | 6,622 |
| Riser pole, 3-phase | 4,376 |
| Street-light bracket pole, excluding separate head | 3,984 |
| Crossarm, braces, two pins/insulators | 1,248 |
| Standalone 50 kVA transformer and protective equipment | 3,030 |
| Guy / guard / anchor | 280 |
| Three-can pole, seed 103 | 8,404 |

The riser exceeds the tangent's 4k cap by 376 triangles for its conduit,
three sealed terminations and tails. It is a separately placed specialty
pole. The guy falls below the broad prop guidance because extra geometry
would not change its silhouette. No baked microdetail is modeled as filler.

| Whole utility block, including optional house masts | Triangles | GLB bytes | Individual conductor meshes before consolidation |
| --- | ---: | ---: | ---: |
| 101 | 47,916 | 2,020,424 | 76 |
| 102 | 40,692 | 1,640,636 | 68 |
| 103 | 44,242 | 1,997,964 | 52 |
| 104 | 48,824 | 2,054,700 | 76 |

`build/checks.json` is authoritative. The parts library is 29,740 triangles /
1,729,184 bytes, with 24 diagnostic material states and eight 256² label images;
the street files use 23–24 states and seven label images. These are provisional
construction counts, not the final one-atlas delivery. Whole-block counts exclude presentation houses/trees/cars/
ground/light heads. Each conductor uses **32–128 triangles** in these examples,
depending on curve length/sag. Tube systems consolidate into five static meshes
(three when there are no communications); poles and house masts remain reusable
assemblies. There is no armature or moving mechanism.

**Planned texture allocation:** one shared **2048² BaseColor / OpenGL +Y Normal /
ORM** set, baked at 4096. With BC7/BC5-class 8-bpp maps and full mipmaps this
costs **16 MiB**, reused by every family part/seed. An optional shipped light
head can be remapped from the original scripted head into this atlas in the
next stage, preserving the original street-light delivery. A 1024 set would halve the
already limited heightwise wood/tag density at pedestrian range; the tall
wood grain and near-ground marks justify 2048. Current diagnostic materials
and tiny label images are explicitly temporary and exceed final material/image
counts. No final shared atlas or final UV/bake claim is made at this checkpoint.

## Sockets, parts and game use

Meters, Blender +Z up, street run +Y, asset front −Y; glTF maps `(x,y,z)` to
`(x,z,-y)`. The parts library is `build/utility.glb`; replace a part root's
inspection-layout transform. Pole grade remains local zero. Crossarm origins
are their central mounting-bolt datum; transformer origins are the pole-line
mount frame at tank-bottom height; guy origins use the pole grade datum.
Those mounted modules intentionally use installation frames rather than
standalone ground-prop centers.

Every pole carries `<root>__Socket_<name>` empties with `socket_kind`:

| Socket | Role |
| --- | --- |
| `Primary_A`, optional `Primary_B/C` | Actual tangent saddles or deadend clamps |
| `Neutral` | Neutral spool's outside bearing line |
| `Service` | Central triplex strain clamp; optional bank `Service_A/B/C` are distinct circuits |
| `CommStrand`, `LashedFiber`, `Telephone`, `CommDrop` | Each long conductor and the house drop |
| `GuyUpper` | Upper guy eye |
| `CrossarmMount`, `TransformerMount` | Installation frames for reusable equipment |
| `Riser_Primary_A/B/C`, `RiserUnderground` | Sealed phase terminations and underground entry |
| `LightBracket`, optional `LightHead` | Bracket pad and head slipfitter; local −Y points toward the street after a +90° Z rotation |

`build/street-<seed>.json` records complete Blender world coordinates and
construction parameters. House mast roots carry `ServiceDrop` and
`CommunicationDrop`. `build/house-attachments-<seed>.json` is the optional
sidecar: local coordinates, instance transform, house type/seed and ray-measured
roof-guy anchor points. The mast's lower elbow enters the wall; an internal
route to the original meter is reserved, not modeled in the exterior shell.
No second meter, altered house mesh, house export or changed house script.
The render-context check also ray-tests the anchors against the actual posed
imported GLB house meshes, catching presentation rotations as well as modeling
errors. It does not substitute an intended transform for the visible geometry.

The pure-Python API works without Blender; add `utility/src` to the import path.
It uses +Z up. Convert imported engine coordinates `(x,y,z)` to `(x,-z,y)`
before calling it, then convert the result back with `(x,z,-y)`:

```python
from span import sample, sag_from_tension

# Transform imported socket positions into one common world frame first.
points, report = sample(start_socket, end_socket, sag=0.8)
# Or calculate a self-weight case from horizontal tension:
sag = sag_from_tension(start_socket, end_socket,
                       mass_kg_m=0.2158, horizontal_tension_n=550)
```

`sample` handles unequal supports, solves the actual catenary, and adaptively
subdivides to 8 mm chord error / 4 m maximum steps. Its arc length and minimum
height are included in the report. `construction.conductor` creates the Blender
tube. For an engine, sweep a four/six-sided section along the points, or use
`ribbon.data(points, diameter)` for the far mesh. Sag is below the chord at
horizontal midspan; it is not the absolute elevation of the lowest point.

At distance use the supplied original `src/wire.gdshader`: camera-facing ribbon,
.85-pixel floor, coverage reduced by `true_width / widened_width`. Apply object
scale; convert positions and tangent normals into the engine frame. Use UV.x
for 0/1 side, UV2.x for physical diameter. Expand the runtime AABB to contain
the widened vertices. Keep physical tubes nearby and for shadows; cross-fade
representations over a chosen pixel-width range without drawing both at full
opacity. The shader needs no extra map. Godot compilation, moving-camera AA
and performance still need engine validation; the Cycles filtered view is an
explicit geometric equivalent, not proof of a tested game shader.

## Rebuilding and evidence

```sh
make -C utility                 # references, own-context staging, parts, four runs,
                                # checks, 20 Cycles images, two photo pairs, sheets
make -C utility check           # pure math, raw GLB, fresh import and actual surfaces
make -C utility clean
make -C utility                 # full checkpoint rebuild; reference cache retained
python3 utility/src/span.py --start 0 0 10 --end 0 45 11 --sag .8 --out build/span.json
```

Uses installed Blender 5.2, Python/Pillow/NumPy, open fonts and the kit's shared
GPU lock. No kit change. Existing generated neighboring deliveries were absent
in this worktree; no neighboring output path is written. Tracked neighboring
sources remain unchanged. `build/context.json` records that scope and hashes
the scratch context files. The USDA RUS PDF endpoint was inaccessible;
the optional Howard brochure's TLS chain also fails in this environment, so
it is excluded from automatic reference fetching. Required dimensions come
from the retrievable MPS/WPS/NRECA publications.

`build/checks.json` distinguishes serialization from geometry: raw GLB counts,
finite positions, unit normals and zero degenerate triangles; fresh-import
counts and sockets; actual shaft sections and wire minima; sampled interspace
clearance; actual roof rays beneath service drops. Every imported shaft's
full ground footprint also has to fit between the curb back and sidewalk.
Minimum neutral/comm gap
is **1.205 m**. Lowest checkpoint service surface is **5.193 m** above grade;
lowest comm drop is **4.397 m** on private land. Actual triangle-clipped road
minima are **5.975 m service / 4.866 m comm drop**, above the chosen
18 / 15½-ft road screens. The whole private service stays above the WPS
general 16-ft Type-A driveway screen; private comm retains an authored 12-ft
screen. Corner attachments avoid all roof overflights in the sampled rays.
These are the authored tension case on level terrain, not a structural or
all-weather certification. Final UV overlap/density and bake gates are deferred.

Photo fits use the kit's calibrated camera tool and independent Blender
projection verification. NC is a 2009 photograph; the MD photograph is 2015
and documents older maintained equipment, so it is not period dating proof.
Fits compare construction types rather than surveyed copies; residuals remain
visible in the calibration overlays. Neutral concrete ROIs and white-balance
gains are recorded before color critique. The two MD space landmarks are held
out because the reference's attachment heights differ from our selected standard.

The weakest parts are the provisional surfaces, unmodeled triplex/lashing lay,
simple town staging and repeated context houses, the specialty riser's cost,
and the untested runtime shader. The next stage must establish real aged wood,
rust, chalking and ground moisture, then prove those effects on the baked export.
This checkpoint stops here as requested; no final docs JPGs are committed.
