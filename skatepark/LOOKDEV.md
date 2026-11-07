# Skatepark — connected terrain and baked look-dev checkpoint

The connected-form and baked look-dev checkpoint is verified. This is a review checkpoint; the remaining photographic finish gap is recorded below.

The 56 accepted modules remain, with two additional banks matching the four- and five-riser plaza heights. The accepted transition sections, coping diameter, construction grid, sockets, ride-line spawns and seeded grammar remain. The parks now use connected pours, continuous decks and an upper street terrace. No kit files, top-level README, README gallery or docs images changed. Existing checkpoint exports and renders are retained byte for byte.

## Requested corrections and views

All paths below are relative to this folder. Main views are 1440px Cycles renders of the embedded, baked GLBs. Before/after panels are 1000px each, made with identical camera and light settings. The before side uses the untouched archived external glTF from `4839a5b`, which had no embedded GLB.

The extra calibrated-pose before/after views preserve the original world placements. The revised street layout moves the stair, so the archived hubba is partly outside that narrow crop. Use the wide `101-stairs.jpg` pair for the complete construction comparison. Feature isolation selects each delivery's corresponding stair root; projection and light settings remain identical.

| Correction | Result | Evidence |
| --- | --- | --- |
| Connected municipal terrain and spacing | Adjacent quarter/bank runs, graded continuous rear deck, raised street plaza, bank/stair/rail connections, real planter walls and spectator steps. Prefab end rows tightened on their flat pad. | `renders/before-after/pairs/101-above.jpg`, `202-above.jpg`, `303-above.jpg`; each park’s `plan.png` |
| Poured ends | Placed copies lose buried end caps and receive 20° wing banks, rear retaining closures and continuous decks. Source section modules remain reusable. | `renders/before-after/pairs/101-connected_ends.jpg` |
| Hubba and stair cheeks | Concrete top remains visible between two 2in angle edges; opposite stair cheek and supported landing continuation. | `renders/before-after/pairs/101-stairs.jpg`; `renders/lookdev/101/stairs.png` |
| Pool joints | Planar radial block ends, flat cap normals, recessed 3mm radial mortar joints. | `renders/before-after/pairs/101-bowl.jpg`; `renders/lookdev/101/bowl.png` |
| Bowl types | Original tangent-circle kidney with a waist; separate three-lobed clover. Constrained floors have real drain openings and no folded plan triangles. | `renders/before-after/pairs/101-bowl_plan.jpg`, `202-bowl_plan.jpg` |
| Pad edges | Concrete thickened edges and mow strips meet lawn. Small rectangular bowl-deck corner gaps found in overhead review are infilled and ray-tested. | `renders/before-after/pairs/101-edge.jpg`; bowl plan views |
| Trees | Canonical delivered red maple and pin oak GLBs, three of each per park; MASK foliage and `_WIND` preserved, with no wind colors entering albedo. No new trees. | `renders/before-after/pairs/101-trees.jpg`; raw image/attribute receipts |
| Fence | Native-pitch six-foot fabric and taller posts/gate hardware; one low bay receives board-height deformation. | `renders/before-after/pairs/101-fence.jpg`; NCPC 2011 source in `refs/SOURCES.md` |
| Comparisons | Upright EXIF-informed kidney framing; six identified hubba corners; coping/tile lip correspondence. Full-photo and crop-projection lenses are labeled separately. | `renders/lookdev-matches/*-pair.jpg`, `*-calibration.jpg`; `renders/lookdev/matched-contact.jpg` |

## Layout measurements

The masks in `renders/research/` measure published drawings for comparison only; none is a geometry input. Feature envelopes include each feature’s local platform, and exclude surrounding circulation whose grade cannot be classified reliably from these raster plans. Ann Arbor measures the northern bowl/street program, excluding its longer street tail. These are approximate drawing reads, not CAD takeoffs.

| Published plan | Major-feature envelope | Sampled clear gaps | Reading uncertainty |
| --- | ---: | --- | --- |
| Columbia 1998–1999, PDF p10 | 26.2% | 5.37m / 6.15m / 6.83m | ±5 percentage points; ±0.4m gaps |
| Los Altos 2013-issued / 2014 record, L2 | 25.0% | 2.15m / 2.36m | ±6 percentage points; ±0.4m gaps |
| Ann Arbor 2013 as-built, PDF p18 of the 2019 RFP | 35.4% | 2.04m / 2.26m / 3.07m | ±7 percentage points; ±0.4m gaps |

| Original park | Active paving | Major-feature envelope | All terrain including shared raised circulation | Measured approach gaps |
| --- | ---: | ---: | ---: | --- |
| 101, Alder Glen 2011 | 1404.1m² | 25.0% | 44.0% | 4.57m / 4.21m / 5.65m / 5.52m / 5.51m |
| 202, Cedar Junction 2004 | 927.5m² | 32.2% | 46.5% | 4.57m / 1.78m / 2.77m / 4.11m |
| 303, Mill Creek 1999 | 1004.7m² | 22.5% | 22.5% | 5.30m |

The feature envelopes fall within the approximate published ranges. The poured parks have additional connected raised circulation, explicitly reported rather than mixed into the obstacle comparison. Gap samples use actual exported surface endpoints along the named approaches; diagonal ride routes can be longer. The large park’s former 7.95–8.09m bowl approach was reduced to 5.51–5.65m. The compact park’s 1.78m ledge-to-bank interval is deliberately tight. Full endpoints and masks are in `build/plan-measurements.json`.

## Dimensions retained and construction added

| Item | Meters / construction | Basis |
| --- | --- | --- |
| Quarter sections | 1.2192m high / 2.1336m radius; 1.524m high / 2.4384m radius | Accepted 4/5ft heights, 7/8ft circular sections; Columbia construction details |
| Bowl | 1.2192–2.1336m depth, 2.4384m transition radius | Accepted 4/7ft pockets and 8ft section; independent exported circle fits |
| Steel coping | 0.060325m OD | Nominal 2in Schedule 40 / 2⅜in OD; Los Altos L5 |
| Banks / stairs | 20° banks; 0.1524m risers, 0.3048m treads | Accepted construction sections; 4- and 5-riser upper grades 0.6096 / 0.762m |
| Hubba / cheek | 0.5588m concrete top; 0.0508m angle legs, 0.0047625m gauge; opposite 0.32m cheek | Original proportions checked against Burnham; width is an inferred comparator, not a published 22in dimension |
| Pool coping | 0.30475m full radial profile width, 0.0635m bullnose height, radial end planes | Accepted profile, Federal Stone SBN comparator |
| Prefab | 0.006m riding sheets; 0.003m toe plate; one fixing lifted 0.0018m | Accepted framed construction and maker installation comparators |
| Fence / guard | 1.8288m fence; 1.0668m deck guard, 50.8mm posts, 19.05mm pickets | 2011 NCPC municipal fence description and original welded guard construction |

Sources, authors, licenses and exact reference URLs are recorded in `refs/SOURCES.md`. The native library’s moving pivots and source sockets are retained. Source flange/mark contacts and fresh GLB surface probes distinguish physical construction checks from serialization checks. The drain check compares actual floor vertices with its imported drain datum; it is not a hydraulic simulation.

## Triangle, material and file budgets

| Park | Skating triangles | Whole site triangles | Material definitions in GLB | GLB bytes | Compressed image estimate, full mips |
| --- | ---: | ---: | ---: | ---: | ---: |
| 101 | 48,694 | 286,380 | 17 | 78,078,672 | 100 MiB |
| 202 | 45,451 | 271,757 | 17 | 77,040,480 | 100 MiB |
| 303 | 44,367 | 271,069 | 18 | 79,845,084 | 104 MiB |

All 58 base modules are below 4,000 triangles; the maximum is 3,304. The library GLB is 19,906,864 bytes and uses three material definitions total, at most two per base piece. Placed skating pieces use up to three states when wear/wax is present. Whole-site counts include the six canonical trees, native fence hardware and site fixtures; distant houses/roads are render context only.

| New shared set | Shipped resolution | BaseColor bytes | Normal bytes | ORM bytes | Compressed estimate |
| --- | --- | ---: | ---: | ---: | ---: |
| SkateTrim | 2048² × 3 | 3,462,372 | 2,427,493 | 399,967 | 16 MiB |
| Prefab | 1024² × 3 | 180,731 | 319,383 | 630,860 | 4 MiB |

**20 MiB new, 48 MiB unchanged Ground sets reused.** Canonical maple/oak and chain-link add 36 MiB already belonging to those families. Every opaque/cutout/wax trim state shares the same three images. Bakes are 4096; trim ships at 2048 and prefab at 1024. These GPU figures assume 8bpp block compression and full mips, and are distinct from PNG/GLB disk sizes. See `TEXTURES.md` and `build/delivery-audit.json`.

| Module | Triangles |
| --- | ---: |
| Bank_3ft | 68 |
| Bank_Rail | 288 |
| Bowl_Floor | 1,093 |
| Bowl_Floor_1 | 674 |
| Bowl_Floor_2 | 485 |
| Bowl_Floor_3 | 638 |
| Bowl_Sector_00 | 2,200 |
| Bowl_Sector_01 | 2,200 |
| Bowl_Sector_02 | 2,201 |
| Bowl_Sector_03 | 2,200 |
| Bowl_Sector_04 | 2,200 |
| Bowl_Sector_05 | 2,200 |
| Bowl_Sector_06 | 2,201 |
| Bowl_Sector_07 | 2,200 |
| Bowl_Sector_08 | 2,200 |
| Bowl_Sector_09 | 2,201 |
| Bowl_Sector_10 | 2,200 |
| Bowl_Sector_11 | 2,200 |
| Bowl_Sector_12 | 2,200 |
| Bowl_Sector_13 | 2,201 |
| Bowl_Sector_14 | 2,200 |
| Bowl_Sector_15 | 2,204 |
| FlatBar | 324 |
| Hip_90 | 1,170 |
| Ledge_18in | 180 |
| ManualPad | 84 |
| PlazaBank_4 | 288 |
| PlazaBank_5 | 288 |
| Prefab_Funbox | 262 |
| Prefab_GrindBox | 244 |
| Prefab_Launch | 3,280 |
| Prefab_Quarter | 3,304 |
| Pyramid | 34 |
| Quarter_4ft | 252 |
| Quarter_5ft | 252 |
| Spine_5ft | 408 |
| Stairs_4 | 456 |
| Stairs_5 | 464 |
| SteelBowl_Floor_0 | 1,210 |
| SteelBowl_Floor_1 | 435 |
| SteelBowl_Floor_2 | 695 |
| SteelBowl_Floor_3 | 432 |
| SteelBowl_Sector_00 | 2,112 |
| SteelBowl_Sector_01 | 2,109 |
| SteelBowl_Sector_02 | 2,108 |
| SteelBowl_Sector_03 | 2,108 |
| SteelBowl_Sector_04 | 2,108 |
| SteelBowl_Sector_05 | 2,108 |
| SteelBowl_Sector_06 | 2,109 |
| SteelBowl_Sector_07 | 2,110 |
| SteelBowl_Sector_08 | 2,110 |
| SteelBowl_Sector_09 | 2,109 |
| SteelBowl_Sector_10 | 2,108 |
| SteelBowl_Sector_11 | 2,108 |
| SteelBowl_Sector_12 | 2,108 |
| SteelBowl_Sector_13 | 2,108 |
| SteelBowl_Sector_14 | 2,109 |
| SteelBowl_Sector_15 | 2,112 |

These placed terrain assemblies are additional to the reusable modules; their counts include their welded guards where present and are already included in the park totals.

| Terrain assembly | 101 triangles | 202 triangles |
| --- | ---: | ---: |
| Plaza entry returns | 40 | 40 |
| North west run closures/deck | 1,936 | 1,372 |
| North east run closures/deck | 1,372 | 796 |
| South bank closures/deck | 48 | 48 |
| Graded north connection | 1,198 | 1,570 |
| Upper street plaza | 168 | 156 |

## Age, value and comparison evidence

1999 uses the hard-worn composite/steel prefab program: lighter riding lanes, worn plate surfaces, lifted fixing, grind-box wax and more exposed paint damage. 2004 has the stronger concrete pumping/contact paths and middle steel-age lane. 2011 keeps a newer concrete value, narrower service marks and pool blocks/tile. Their age controls are 1.0 / .68 / .38. Crack starts, repairs, lip scrapes, wax, salts, sparse missing tiles, fictional tags and upstream drain deposits are tied to construction and use locations.

The sunlit concrete control moved from about .57 to .76 display Y, against balanced photo patches .794 / .776 / .859. Canonical Ground pixels stay byte-identical. This calibrates the estimated camera exposure, not an inferred physical reflectance. The assumed neutral is the photo’s unpainted sunlit concrete coping/deck; the linear RGB gains and actual sun/camera-clear surface probes are in `renders/values-final/concrete-value.json`.

| Pair | Native photo crop width | RMS / maximum error | Lens and limit |
| --- | ---: | --- | --- |
| Alondra kidney | 866px | 28.33 / 69.17px | Upright, EXIF-informed 27mm full-photo equivalent. Inferred nearest-outline phases; different original plan, 3m comparator camera height. A type/wear comparison, not dimensional identity. |
| Burnham hubba | 400px | 1.84px RMS | Six identified concrete corners; about 48.6mm full-photo equivalent, 372.9mm crop projection. |
| Memorial coping/tile | 580px | 6.78px RMS | Inferred lip/scale anchors, approximately 17mm full-photo equivalent; no retained EXIF. |

Light direction, sun softness, sky contribution and exposure are estimated per reference. The Alondra key is behind the far lip so the far wall is shaded, as in the photo. Burnham and Memorial depict active daily use; the additional sunny Venice value reference is also in use. All photographs are comparison inputs only. No photographic pixels enter a material.

## Rebuild and proof receipts

```sh
make -C skatepark WIDTH=1440 SAMPLES=32
make -C skatepark check
make -C skatepark before-after WIDTH=1000 SAMPLES=20
make -C skatepark repeat
make -C skatepark values SAMPLES=32
```

All commands passed. The final fresh `make check` includes repository rules, library/park GLB re-import, section measurements, actual surface contacts, exported UV/density/tangent checks and drawing/layout measurements. There are zero degenerate skating UV triangles, zero geometric degenerate triangles, and zero below-grade bowl plan overlaps above 1e-6m². Actual deck flange contact error is at most 1.2e-7m across 88 / 76 underside samples; all eight bowl deck corner probes hit concrete at grade. The 1,000 seeded numeric plan checks pass; this is distinct from geometric verification of the three delivered parks.

The isolated `make repeat` passes **40 byte-identical files**, using shared read-only texture/context inputs. It does not repeat the Cycles bakes. One oak trunk tangent straddled MikkTSpace's four-decimal rounding boundary; the existing kit stabilizer now guards its exact position/normal/UV and limits the correction to one rounding step. Missing/invalid tangent repairs remain separate. No canonical tree file changes. Unreferenced iteration images are removed from the new export folder.

All **24 main views and three matched views** have source SHA-256 values equal to the final GLBs, recorded in `build/render-audit.json`. All **17 before/after pairs** pass projection, lighting, native panel size and source-hash checks in `build/before-after-check.json`; the two reframed details were refreshed separately after the full run. All 1,041 protected existing delivery files, 15 archived skatepark export files, 26 checkpoint render files and 13 original match files remain byte-identical. Three final concrete probes measure .759384 / .760218 / .760501 display Y. Final hero white clipping is zero in each park; whole-image tone receipts include sky/context and are not albedo measurements.

`make` rebuilds the current deliveries and renders from scripts, including native dependencies. `before-after` additionally uses this session’s preserved checkpoint archive in `build/before/`. No baseline archive is needed for the current asset build. All Cycles bakes/renders use the shared GPU lock, with Blender processes run serially. No kit files changed.

Important evidence paths:

- `renders/lookdev/contact.jpg` and `matched-contact.jpg`: main and comparison contact sheets.
- `renders/lookdev/{101,202,303}/hero.png`, `above.png`, `plan.png`: eye-height 35/35/40mm heroes and layout views.
- `renders/lookdev/{101,202}/bowl_plan.png`: close overhead shape checks.
- `renders/lookdev/101/{bowl,ledge,stairs,deep_end,edge,fence,trees}.png`; `202/steel_coping.png`; `303/{prefab,plate}.png`: requested detail evidence.
- `renders/before-after/{before,after}/` and `pairs/`: identical cameras, native individual panels and paired JPGs.
- `renders/lookdev-matches/`: three native pairs and landmark overlays.
- `renders/values-final/`: balanced sunlit-photo patches, actual render patches and value receipt.
- `renders/research/`: three annotated city-plan reads and actual exported footprint masks.
- `build/checks.json`, `delivery-audit.json`, `plan-measurements.json`, `repeat-check.json`, `before-after-check.json`, `render-audit.json`: measurements, image provenance and determinism receipts.

## What remains weaker

The concrete remains more orderly and uniform than the daily-use photographs: Burnham has stronger irregular armor drips, Memorial a darker ground-in coping nose, and Alondra broader pumping abrasion. Some wear still has regular procedural rhythm. The 1999 prefab reads as hard-used at full frame; the 2004/2011 age difference is subtler than intended, especially on the street terraces. Fine leaf/grit silhouettes are economical. The native lawn has a flat silhouette, some reused fixture finishes are still constant-color, and repeated houses remain obvious presentation context. The upright kidney fit is materially weaker than the hubba fit; its error is disclosed on the pair. These are look-dev limits, not claims of final photographic equivalence.

No additional input is needed from the lead for this checkpoint. Useful kit follow-ups are an explicit authored-winding option for open skins, initialization of the complete Blender glTF metadata group before native re-import, and guarded zero-tangent handling for normal-mapped exports. Those changes were kept local here; promoting them to kit should include the full clean kit test suite.
