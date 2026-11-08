# Manufactured communities — look-dev handoff

This is the requested checkpoint before docs. The accepted home dimensions,
chassis/pier installation, utility pedestal, hinges, sockets, drive paths
and separate context accounting remain. No kit code, top-level README,
existing delivery or docs image changes are included.

The final evidence lives under `renders/checkpoint/look5/`. The source
packages are external-image glTF/BIN; every render freshly imports a
losslessly embedded GLB containing those exact meshes and shipping maps.
`sources/`, `provenance.json` and `source-verification.json` retain the
container/image hashes, real cameras, lighting and presentation counts.

## Form corrections and views

| Request | Change and reason | Checkpoint views |
| --- | --- | --- |
| Dense parks | Four end-on rows, 36 older / 33 newer homes; eight seeded profiles per park, linked home meshes and repeated add-ons | Both `Park-*/hero.png` and `above.png` |
| Era construction | Bowed metal roofs/drip rails, awnings/bands/end banks; shallow later gables with end overhangs; shingled double-wide eaves, shutters, paired windows and supported entry covers; proud storm frames; front and rear steps | `HomeForms/detail.png`; both inspection-home turnarounds, heroes and entry details |
| Occupied lots | Seeded sheds, fences/gates, carts, chairs, grills, pots/toys, dishes/tanks, replacement panels, leaning tools, supported covers and slack hoses; mature old-park trees inside rows | Both `Park-*/row.png`; `matches/Park-101/single-2009.png` and `aerial-2015.png` |
| Lane/pad separation | Measured 20 ft older asphalt core, fine broken edge, distinct concrete/gravel pads and unpaved throats; compacted walks on selected older lots | Both older street views and the aerial pair |
| Town surroundings | Varied native single-story ranch blocks, realistic compact lots/backyards/privacy lines, entrance gas station/strip; newer public road, field margin and tree line | Both `above.png` and `entrance.png`; heroes check the eye-level horizon |
| Useful pairs | Cameras fit actual existing subjects within populated exported parks; neutral-balanced photos and landmark/visibility receipts | `matches/*-pair.jpg`, `matched-contact.jpg`, `matches/comparison-cameras.json` |

`renders/fixes/` contains eight before/after sheets: both park heroes and
obliques, the single-wide/double-wide heroes, deck and carport. Each panel
is 1440 pixels wide. The old six delivery packages and their legacy town
context are frozen from the original checkpoint cache. Both sides are
rerendered with equal camera matrices, lens, resolution and physical light;
`renders/fixes/cameras.json` checks equality to float32 tolerance, 1e−6.
This preserves a useful common view despite the changed park footprint.
The original pass-4 images also remain available unchanged.

## Lots and cost

| Park | Homes | Lot ft / sq ft | Gross acres | Homes/acre | Measured home-envelope gap |
| --- | ---: | --- | ---: | ---: | --- |
| 101 / Alder Court | 36 | 32 × 110 / 3,520 | 3.9765 | 9.0532 | 4.2464–4.6159 m |
| 202 / Meadow Bend | 33 | 56 × 95 / 5,320 | 5.7255 | 5.7637 | 6.1724–10.4178 m |

The narrow older lots use the compact end of the cited HUD builder-guide
survey, Appendix D pp. 63–66. These are original fictional layouts, with
no claim of civil approval. Density includes common land. The newer plan
reserves three lots for shared facilities and keeps its connected loop.

The complete measured tables are in `build/metrics.md` / `.json`: all six
inspection homes, all 69 lots, every inspection module and both parks.
Home rows include both steps. Lot rows include native fixed props, local
flatwork, resident storage and small edge plants. Cars, large vegetation,
town architecture and public streets have their own placed/unique rows.
Unique means distinct exported mesh data; placed counts every node instance.
Local per-lot unique totals are not incremental allocations to sum together.
Unbatched primitive counts remain explicit; instancing alone does not merge
draw calls. A game should cull the socket population and batch static props.
Additional placements beyond one copy of each unique mesh contribute
1,471,948 / 1,290,912 triangles in the older/newer park. Their unbatched
primitive counts are 2,203 / 1,941, before presentation actors.

| Export | Placed triangles | Unique triangles | Materials | glTF + BIN bytes |
| --- | ---: | ---: | ---: | ---: |
| SingleWide-120 | 26,735 | 26,735 | 3 | 2,419,255 |
| SingleWide-147 | 23,407 | 23,407 | 4 | 1,986,085 |
| SingleWide-168 | 26,791 | 26,791 | 4 | 2,302,518 |
| DoubleWide-245 | 26,834 | 26,834 | 5 | 2,353,612 |
| DoubleWide-228 | 29,297 | 29,297 | 5 | 2,554,393 |
| DoubleWide-326 | 31,420 | 31,420 | 5 | 2,761,838 |
| Park-101 | 2,135,310 | 663,362 | 29 | 54,554,107 |
| Park-202 | 1,963,684 | 672,772 | 33 | 53,820,722 |

Individual occupied lots range from 43,716–74,371 placed triangles in Alder
Court and 39,561–74,778 in Meadow Bend. Their local unique ranges are
42,336–74,371 and 39,561–74,778. The office/laundry are 25,900/21,564;
the clubhouse/laundry are 27,061/21,868. The native framed shed is 9,700,
above the standard-prop tier because its working doors and framed interior
are inherited intact. The other new add-ons remain within their budgets.

| Presentation only | Category | Placed triangles | Unique triangles |
| --- | --- | ---: | ---: |
| Park-101 | Cars | 4,430,966 | 184,623 |
| Park-101 | Large vegetation | 3,467,216 | 71,168 |
| Park-101 | Town architecture | 3,245,805 | 529,796 |
| Park-101 | Public streets | 39,868 | 214 |
| Park-202 | Cars | 4,306,153 | 184,623 |
| Park-202 | Large vegetation | 3,242,084 | 59,992 |
| Park-202 | Town architecture | 781,090 | 333,258 |
| Park-202 | Public streets | 28,592 | 214 |

## Materials, photo comparisons and limits

One new `Manufactured` BaseColor / OpenGL +Y Normal / ORM set is baked at
4096 and shipped at 2048: 5,670,523 PNG bytes, approximately 16 MiB with
8bpp compression and full mip chains. It serves metal siding/roofing,
skirting, steel chassis, concrete piers and carport manufacture. Existing
house siding/shingle/trim, Ground and native prop images are reused, with
canonical external references. Complete static and presentation unions are
content-deduplicated in the metrics; memory is not multiplied per house.
The static parks bind 160.00 / 176.0417 MiB; their combined image union is
176.0417 MiB. Including all presentation actors raises the respective totals
to 298.6667 / 280.7083 MiB; both full presentations together use 314.7083 MiB.
These are compressed full-mip estimates, not measured driver allocations.

Exposure and upkeep use seeded corner colors: sunny chalk, north/eave
algae, roof-seam runoff, low skirt splash/cracks, differing roof coatings,
grayed cupped timber and corrosion at painted-steel carport feet. Native
Ground supplies summer turf, edge tufts, cracked/repair/oil surfaces and
compacted paths. These are authored manufacture and cause masks, with no
photographic projection, imported texture or HDRI.

| Pair | Native-pixel anchor RMS | Lens | Interpretation |
| --- | ---: | ---: | --- |
| Used 1980s lot, 2009 | 18.431 | 43.73 mm | Three outer-fascia and two wall/skirt anchors; low camera inferred without an eye-height prior |
| Older addition row, 2007 | 16.954 | 25.93 mm | Six corners on the actual exported lot-36 addition |
| Occupied park aerial, 2015 | 16.652 | 100.00 mm | Nine visible corners on two adjacent carports; occluded left post foot excluded; reaches the cropped-lens bound |
| Newer lane, 2024 | 8.528 | 23.50 mm | Supplementary coplanar road fit; longitudinal stations inferred from our plan |

The comparison neutrals are respectively a white storm-door frame, white
addition fascia, sunlit aluminum pan and white PVC fence post. Gains are
calculated in linear RGB. RMS applies to the selected anchors, not every
building or the whole photograph. The fictional layouts, climate/planting,
vehicles and maintenance histories are not replicas of those photographs.
The 2024 photo illustrates older construction types, not a 2024 asset era.

Before rendering, imported-triangle sightline checks clear 5/5, 6/6 and
9/9 construction anchors; the newer lane clears 4/4. The renderer rejects
any required fit with an occluded anchor. Blender's independent camera
projection cross-check has a maximum disagreement of 0.00674 native pixels.
The archived visibility receipt explains the conservative triangle rays
and their final 0.50 m surface/trim exclusion.

Five new image critiques follow the earlier form critiques in `REVIEW.md`.
Earlier passes were rejected for lighting, mapping, comparison and culled
pavement-wear errors. All 44 native 1440px frames, four full-size pairs,
eight historical sheets and both contacts were inspected. The last critique
records the remaining visual weaknesses. No final README gallery or docs
images are produced at this gate.

## Validation and handoff

Run from this folder; the final pipeline uses the existing native inputs:

| Command / receipt | Result and scope |
| --- | --- |
| `make` (`build/look5-make.log`) | PASS: references, models, repository/export/resource/construction checks, one locked Cycles render batch, pairs and contacts |
| Check stage / `build/check.json` | PASS: 21 exports, finite/noncollapsed geometry and UVs, unit normals, fresh re-import, 1,000 deterministic plan seeds; 1,365 static assembly comparisons |
| Motion stage / `build/motion.json` | PASS: 18 home hinges, 936 poses sampled at 2 degrees, zero violations; not a full-site sweep of every native gate or car |
| Resource stage / `build/look-check.json` | PASS: budgets, atlas-cell containment and reported texel density; repeat UVs intentionally overlap, not a unique lightmap pack |
| `make repeat` (`build/repeat.json`) | PASS: 64 glTF/BIN/JSON/local PNG files byte-identical, cached native inputs; no independent GPU rebake |
| Procedural source repeat / `build/texture-repeat.json` | PASS: four 4096 source/layout files byte-identical; separate from GPU bake determinism |
| `make check-preservation` | PASS: 1,202 prior delivery/image files unchanged, including all 492 files protected at the original checkpoint |
| `renders/checkpoint/look5/source-verification.json` | PASS: 44 archived GLB and referenced-image SHA-256 receipts |
| `renders/fixes/cameras.json` | PASS: eight equal camera/lens/resolution/physical-light comparisons; maximum measured matrix delta 1.20e-7, tolerance 1e-6 |
| `build/final-projection.log`, `build/final-visibility.json` | PASS: independent Blender projection within .00674px; required construction sightlines 5/5, 6/6, 9/9, supplementary road 4/4 |

The new flat atlas was actually GPU-baked at 4096 and downsampled to 2048.
The bake receipt in `textures/4k/Manufactured-bake.json` records mean
BaseColor error .000386; the shipping normal's maximum unit-length error
is .005227. All Cycles work used the shared GPU lock, held once per render
set and separately for the bake. No tools or packages were installed.

Construction checks sample the actual imported surfaces. For example,
canopy post bottoms engage their deck tops by 4.97–6.12 mm; those are ray
measurements, distinct from a serialization comparison. The final terrain
audit checks both raw winding and positive-up normals on 22,436/31,482
tagged open-surface triangles. This repairs the earlier volume-normal
recalculation error without increasing the park triangle counts.

Both lane heroes use an eye height of 1.68 m, a 40 mm lens and a clear
procedural sky with an 18-degree raking sun. Their p5/p95 display values
are .0706/.7843 and .1451/.8039; near clipping is .000944%/.000258%.
Both obliques have zero near-clipping. This supports the exposure review,
not a claim that the surfaces have achieved photographic appearance.

The principal remaining weakness is the older lot's apron: cracks and
repairs remain too weak at the paired framing beside the battered photo.
Broad turf remains planar, foliage silhouettes and pots repeat, the three
native vehicle bodies recur, and the grayed deck remains too uniform.
Some adapted secondary objects are simpler than the homes. The final
winding correction has only a small visible effect in Cycles. Surface
history is strongest at skirt feet, roof coatings and carport bases;
sunny walls and pads still need more convincing irregular maintenance.
These are unresolved look-dev issues, not waived by the passing checks.

Nothing is needed from the lead to reproduce or inspect this checkpoint.
No kit files changed. A useful general kit follow-up would be an explicit
open-surface winding contract: volume-normal recalculation is inappropriate
for one-sided terrain skins, and unit-length normal checks cannot catch it.
The local regression now covers that case. Stop here before docs and final
art acceptance; prioritize repair history and ground relief in further
appearance work.
