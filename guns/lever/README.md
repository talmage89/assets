# PD Bracken L20 lever-action carbine

An original **Propane Defense** .30-30 visual game asset, generated entirely by
Blender 5.2 scripts. A 20-inch round barrel, six-round tube, straight-grip walnut
stock, curved steel butt plate, exposed hammer and semi-buckhorn sights share
one baked 2048 PBR atlas. The finish represents a hunting gun used for many
seasons: thinning brown/plum bluing, gray contact steel, oiled walnut and local
handling/impact wear. Its contours, rollmarks, serial and ammunition headstamp
are fictional and original.

![Exported Bracken L20 with its baked 2048 atlas, Cycles](docs/hero.jpg)

The final renders load the exported GLBs with their baked maps. `make` builds
`renders/final/hero-gray.jpg`, `contact-sheet.jpg`, `turnaround.jpg`, `details.jpg`
and `action.jpg`; native Cycles stills are in `renders/final/beauty/`, Eevee in
`renders/final/eevee/`, photographic comparisons in `renders/final/pairs/`,
dense-source pairs in `renders/final/source-pairs/`, and all 37 real-duration
clip strips/WebPs in `renders/final/strips/`. Five docs JPGs are generated under
`docs/` and remain uncommitted pending the lead's acceptance.

[REVIEW.md](REVIEW.md) contains the form history, four source finish critiques,
exported bake critique, 2D wear evidence, value measurements and limitations.
[REFERENCE.md](REFERENCE.md) distinguishes published dimensions, photographic
estimates and original design decisions.

## Dimensions and construction

| Quantity | Actual evaluated geometry / design | Reference basis |
| --- | --- | --- |
| Barrel, breech face to crown | 508.00 mm / 20 in | Published carbine class; mesh bounds |
| Overall length | 965.20 mm / 38 in | Published class; Smithsonian external measurement |
| Length of pull at finger height | 340.74 mm | Actual trigger/butt surface rays; about 3 mm shorter than published 13.5-inch class |
| Closed width / height | 42.55 / 176.68 mm | Visible evaluated surfaces; shorter rear-sight ears reduce the previous height |
| Tube capacity | Six, plus one chambered | Individual representations and count states |
| Lever opening / lower bar / transverse width | 104 x 29 / 3.30 / 8.20 mm | Preserved aperture; closed-photo bar/opening ratios |
| Lever bow side depth | About 12.95 mm | Actual inner/outer surface rays; normalized photo estimate about 13 mm |
| Rear blade height / gauge / ear rise | 8.98 / 1.10 / 2.18 mm | Actual surfaces; ruler photo and seller's 9.017 mm blade |
| Rear notch width / depth | 1.60 / 1.25 mm | Requested small-notch revision; accepted shoulders/aim line retained |
| Eye behind rear sight / above actual comb | 368.00 / 39.02 mm | Authored ergonomic placement, verified on surfaces |
| Case / cartridge overall length | 51.80 / 64.77 mm | Published C.I.P. visual exterior envelope |
| Rim / body / neck diameter | 12.85 / 10.71 / 8.38 mm | C.I.P. |
| Planning mass | About 3.1 kg | Class target; not a mesh-derived mass |

The standalone headstamp planes sit 0.025 mm behind the physical case head, so
full GLB bounds include that depth. The exact Eye camera keeps 70-degree
horizontal FOV, zero shift, opaque gray surround, every gun part visible and
the bead centered at the notch shoulders. The cheek-weld photo supports the
placement qualitatively; it does not publish an eye-relief dimension.

The receiver is a hollow machined forging with rolled corners, raised rear
heel, lowered action belly, front barrel/tube ring, open top race and separate
flush bolt. Its spring-steel loading cover sits in a rounded aperture with a
real hinge/pin and rear screw. Barrel bore, chamber counterbore, crown and
hollow magazine tube are visible construction, not solid placeholder rods.
Bands are fitted to actual wood/barrel/tube section cuts with 1.3 mm steel gauge.

The stock and forend are compound subdivision cages with changing width,
comb, toe, belly and channel curvature. Dense originals remain in
`build/sculpt.blend` and supply the bake. Both tangs are inletted within the
original wood envelope, with a bored through-wrist screw and supported bearing
lands. The curved plate covers the wood across its complete crescent. Smooth
outer walnut normals come from the uncut carving; machined walls retain their
seams. The last wrist fix changes no stock vertices or triangles.

The lever is a continuous forging. Its fuller lower rail grows outward from
the accepted aperture; a concealed 2.2 mm upper relief preserves tang/wood
clearance. The S and opening remain in the gun's mid-plane throughout the
stroke. The hammer has a compound curved body, returning spur and crowned
1 mm checkering. The trigger is a 6 mm wide, 3.7 mm deep radiused blade, with
muzzle-facing concavity and a forward-returning toe. The rear sight is one
filled, coin-gauge sheet with a shallow crescent, short ears and center notch,
supported by its spring leaf, dovetail and stepped elevator.

Visible bolt, forked lock, cradle carrier, sear supports and ammunition
handoffs establish supported poses and game animation. Concealed engineering,
springs and fire-control internals are deliberately incomplete. This is a
visual asset, not a functioning reproduction. Every reference/credit is in
[refs/SOURCES.md](refs/SOURCES.md).

![Front, side, rear and top of the exported GLB](docs/turnaround.jpg)

## Materials and years of use

Intact blue steel uses linear `.021/.022/.023`, metallic 1 and central
roughness `.36`. A contact/exposure field thins the receiver flats toward
brown/plum oxide, with authored limiting color `.130/.064/.032`. That oxide
remains distinct from the bare gray steel, linear `.56/.60/.63`, roughness
`.34`. Axial manufacturing striae and fine surface relief break reflections.
The shipping dielectric specular level is `.16` (glTF specular factor `.32`);
fully metallic surfaces retain their conductor response. Consumers must retain
the imported PBR material and support `KHR_materials_specular`.

Walnut comes from curved longitudinal growth layers, narrow latewood, separate
fiber bundles and individual elongated vessels. Grain follows the stock and
forend's long axes. Its original diffuse endpoints are `.012/.0039/.0015` and
`.085/.034/.015`, with central roughness `.48`; hand-ridden areas are darker
and slightly smoother. No stretched photograph or downloaded texture is used.
Brass, copper jacket, lead cap and separate primer response share the atlas.
The fired case retains its struck primer, open mouth and localized mouth soot.
Original **PROPANE DEFENSE / BRACKEN L20**, **CAL. 30-30 / PD L20** and
**PD-L20-082147** rollmarks use installed Noto Sans. The ammunition's
**PD / 30-30** lettering uses installed DejaVu Sans.

| Wear site | Finished appearance and cause |
| --- | --- |
| Receiver lower edges and bottom | Bright gray core following the actual lower forging contour; narrower broken shoulder/rear rubs, brown oxide retained on flats |
| Lever loop | Polished gray inner lower rail where fingers ride; bow/web remain predominantly blue |
| Loading cover | Narrow gray contact at the rounded perimeter, dark central spring plate |
| Barrel bands | Rubbed gray rim edges and small exposed high points; broad bands remain blue |
| Muzzle | Gray outer crown contact, dark bore/soot retained inside |
| Stock toe and heel | Local compressed dark fibers with small pale broken-finish lips |
| Forend margins | Isolated handling/impact dings near its exposed ends and lower edges |
| Wrist | Dark brown hand-oil region confined to the grip, with a restrained satin response |

![Receiver, wrist, forend, rear sight, butt plate and muzzle details](docs/details.jpg)

White balance precedes every photo measurement. The primary used right/top
photograph uses its broad exposed bolt flat; the full right profile uses
unclipped white paper. The other action views use silver pin/screw facets, the
sight photos their gray backdrops, and the ammunition photo its exposed gray
lead. Native rectangles, gains and marked neutrals are rebuilt in
`build/white-balanced/`. These reflected neutrals are estimates, not gray cards.

| Used-photo surface | Photo median RGB / luma (0–255) | Exported comparison RGB / luma |
| --- | --- | --- |
| Receiver flat | 81/54/39 / 58.73 | 83/53/32 / 57.86 |
| Handled wrist | 44/23/11 / 26.75 | 39/27/22 / 29.12 |
| Forend | 86/51/32 / 57.29 | 84/50/31 / 55.79 |

These are observed display values under estimated comparable views and neutral
studio light, not recovered albedos. Full sampling polygons, channel ratios and
distributions rebuild as `renders/final/photos/value-patches.jpg` and
`values.json`. The wrist remains less red/yellow than the photograph. The flash-lit whole-stock
photo patch is much brighter (140.38 versus 64.79 luma); its strong reflected
highlight is not reproduced by this oil-finish studio setup. It remains a
lighting/material-response limitation, retained in the full measurement JSON.

Ammunition uses linear brass `.49/.29/.085`, copper `.43/.16/.062` and lead
`.14/.145/.15`, all metallic. Brass/copper roughness is approximately `.32`;
lead is `.55`. The lead-cap neutral is an estimate. The original photographed
rounded soft point and our accepted flat nose reflect different light angles:

| Ammunition surface | Photo display luma | Exported display luma |
| --- | ---: | ---: |
| Brass body | 207.04 | 206.07 |
| Copper jacket | 68.57 | 96.92 |
| Lead cap | 104.14 | 72.16 |

The copper/lead display differences remain a limitation of this comparison;
neither their albedos nor identical illumination are recovered. Native patches
are shown in `renders/final/pairs/ammunition-values-pair.jpg` and its JSON.

Receiver wear is judged in two dimensions at a common physical grid:
`renders/final/pairs/wear-2d-pair.jpg` shows color, the actual shipped gray-steel mask beside an independent
photographic fillet annotation, and worn share along length and across height. `wear-2d-values.json` includes connected
areas, bounding dimensions, boundary-clipping flags and threshold sensitivity.
Actual surface rays sample the canonical BaseColor/ORM separately from the
lighting-dependent hero/photo masks. The photo's approximate class envelope,
different forging/camera/light and atlas filtering are explicit limitations;
matching a one-dimensional line is never treated as visual acceptance.

## Frame, rig and consumer binding

The [1.5.0 additive supplement](INTERFACE.md) preserves the family 1.0.0 contract
and reuses 1.1.0 tube-loading/interruption meanings. Meters, grip origin,
Blender +Y forward / +Z up / +X right; glTF −Z forward / +Y up. Internal Root
remains identity. Whole-instance stance/recoil and hand IK belong to the
consumer. All 26 bones, 37 clips and ten complete socket frames are retained.

| Part | Rest pivot or travel, Blender mm | Visual range |
| --- | --- | --- |
| Lever | X at (0,124,−1), riding Link | 0–80 degrees global |
| Lower link | X at (0,195,5) | 0–20 degrees |
| Bolt | Y translation | 90 mm rearward |
| Locking block | Z translation | 30 mm down |
| Carrier | X at (0,85,7) | 0–20 degrees |
| Hammer | X at (0,70,30) | Fired 0, half-cock 12, cocked 44, overtravel 90 degrees |
| Trigger | X at (0,83,0) | 0 to −12 degrees |
| Loading cover | Z at (15.2,122,20) | 0–28 degrees inward |
| Tube rounds/follower | Y translation | 64.77 mm pitch, count-dependent |

These are authored visual motion estimates, not published mechanism dimensions.
Fire and manual Cycle are separate clips. Count-specific holds, single/multiple
insertions, empty reload, empty cycling and hammer safe/cock states retain their
explicit events and STEP occupancy. Save `{version, clip, frame, state}` to
pause/resume an insertion; exit only in declared hand-clear windows. The
executable binding is [src/interface.py](src/interface.py).

The gun exports as one rigidly weighted skin/material primitive. Cartridge and
case export unskinned at their head-centered origins, +Y toward the mouth.
At eject, the ejection socket equals the case head frame; consumers can spawn
the standalone case and hide the demonstration representation. Feeding remains
a declared visual ownership handoff rather than cartridge-path physics.

![Open action, exact aimed view, live cartridge and fired case](docs/action.jpg)

## Budget and delivery

| Output | Triangles | Materials | GLB bytes |
| --- | ---: | ---: | ---: |
| Carbine, including all ammunition displays | 39,950 | 1 | 11,804,068 |
| Live cartridge | 1,598 | 1 | 6,786,108 |
| Fired case | 1,326 | 1 | 6,767,264 |

The inspection source has 39,968 triangles; only microscopic Boolean cleanup
removes 18 for delivery. The final asset stays below 40k. One 4096/32-sample
source bake is filtered to a single **2048 BaseColor / OpenGL +Y Normal / ORM**
set. ORM is R occlusion, G roughness, B metallic. All three GLBs embed identical
canonical maps. An engine must reuse them by atlas ID/content hash to share
approximately **16 MiB compressed memory with mipmaps**; separate GLB imports
do not automatically share GPU texture allocation.

| Canonical 2048 PNG | Bytes |
| --- | ---: |
| `T_BrackenL20_BaseColor.png` | 1,659,560 |
| `T_BrackenL20_Normal.png` | 2,286,588 |
| `T_BrackenL20_ORM.png` | 2,718,359 |

The prepared gun covers about 27.73% of the atlas. Separate regions protect
stock and forend UV tips and padding from nearby metal, while the same single
set still serves the gun and ammunition. Median regional shipping densities
are approximately 2,312 px/m for metal, 2,441 for stock and 1,934 for forend.
Escaped and degenerate UV triangles are zero; microscopic clipped overlap
fraction is approximately 3.11e−7, below the unchanged 1e−5 limit. All six bake
channels miss zero of 4,143,388 checked interior texels. The complete wood
regions, including subpixel tips and padding, contain zero metallic texels.
The generated delivery audit retains full distributions, hashes and sizes.

![Exported GLB in Eevee with the same atlas](docs/eevee.jpg)

## Rebuild and proof

Requires installed Blender 5.2, Python/Pillow/NumPy, fontconfig, Noto/DejaVu,
GNU make and flock. No downloaded code, models, materials or lighting are used.

```sh
make -C guns/lever                    # refs through bake, exports, checks and finals
make -C guns/lever check              # source/finalized/imported construction and motion
make -C guns/lever form-review        # final sight/lever pairs, wrist rake and stroke
make -C guns/lever render match       # exported GLB stills and photographic pairs
make -C guns/lever source-match       # separately labeled dense-source comparisons
make -C guns/lever wear-review        # 2D receiver wear evidence and actual-map samples
make -C guns/lever strips extra       # all clips and standalone ammunition macros
make -C guns/lever repeat             # independent deterministic geometry/rig rebuild
make -C guns/lever WEAR=.45            # cleaner use layers, same forms and rig
make -C guns/lever clean              # generated outputs only; references retained
```

Defaults: `BAKE_SIZE=4096`, `BAKE_SAMPLES=32`, `SHIP_SIZE=2048`, `WIDTH=1600`,
`SAMPLES=64`, `WEAR=1`. Parameter stamps invalidate affected stages. Every
Cycles bake/render uses the shared kit GPU lock; the Eevee clip batch holds one
shared lease while its per-clip guards use a nested local lock. Scratch stays
under `build/`.
`checkpoint.mk` retains the earlier untextured inspection graph.

The 67 actual-surface contacts, tang bearing lands, through-wrist bore,
plate/wood cover, sight rays and trigger direction establish construction.
All 37 clips are swept at half frames, with fixed hand envelopes and the same
bounded contact policy. The lever's mid-plane is tested at each sampled pose.
The final consolidated GLB is decomposed only for auditing: every imported
triangle must match one named finalized surface by rigid owner, centroid and
all oriented vertices, corner normals and UVs before construction and clearance
are independently repeated.

Full affine bone/socket frames, intended states/counts, event/end surfaces,
rigid weights, normal direction and standalone origins separately establish
serialization. Raw texture hashes and a final provenance audit associate every
still/strip with the current exported GLB; WebP durations are decoded and checked.
Raw GLB corner normals agree within 0.0049 degrees, with exact positions and
UV error below 0.000061 shipping pixels. Blender's imported custom-normal fan
encoding reaches 0.584 degrees at one narrow inletting cut; that importer loss
is measured separately from the raw delivered normals.
See `build/check.json`, `serialization.json`, `delivery/construction.json`,
`delivery/verify.json`, `final-provenance.json` and `determinism.json`.

## Remaining limits and credits

Our short sight tips are more angular than the reference insert; the accepted
long lever opening, larger hammer mortise and broader thumb table still differ
from the photographed guns. Wood figure is more regular than real walnut,
small pores/lettering soften at 2048, and the wrist hue remains less warm.
Reflected neutrals, approximate cameras and different illumination limit exact
photographic matching. The rig demonstrates supported visual poses and declared
handoffs; it supplies neither functional internals nor an anatomical hand.

All geometry, relief, masks, graphics and texels are original script output.
Reference authors, licenses and URLs are in [refs/SOURCES.md](refs/SOURCES.md).
Noto Sans uses the SIL Open Font License; DejaVu Sans uses its open font license.
No kit or existing common/gun module changes are required by this asset.
