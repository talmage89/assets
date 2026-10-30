# Relay 9 — form and final finish review

**Current round 2 status: photographic paint acceptance is unresolved.**
Studio/projection work and preservation checks are recorded at the end.
Historical passing paint fits below are superseded because they fitted the
receiver itself. The current independent calibrations are rejected.

The accepted form history below is retained. Later final-look entries supersede
the checkpoint material and delivery restrictions.

Stopped at the requested form gate, before look-dev. The lead accepted the
scale, rig/21 clips/interface 1.3, 18 contacts/clearance, magazine, stock overall,
front sight and handle/lock from round 1. Those remain the baseline. This round
rebuilds the rejected lower, trigger, rear drum, receiver and handguard, relocates
the Eye and retessellates the ammunition. The region findings below supersede
the first checkpoint's overly lenient acceptance list.

## Critique record

Round 1's nine construction/image passes remain in git history. They reduced
57,838 triangles to 38,576 and resolved the magazine/catch/handle contacts, slot,
barrel-band support, stock neck, folded magazine cavity, handguard cap web and
raw winding issues. They did not resolve the reversed trigger, soft lower,
open drum and slab-like handguard; the lead rejected those despite passing
numerical checks. Image acceptance and serialization are separate claims.

10. **Color/value first:** retained neutral dark inspection constants; the photos
    have localized gray steel and mottled polymer which remain outside this gate.
    The new lower's broad side lands and flatter molded guard replace the smooth
    bath and oval rod. A changing grip cage adds width, palm swell and backstrap
    curvature. Rejected an initial 43,380-triangle revision; recovered budget from
    redundant steel bends, marker tessellation, the old drum and minor trim.
11. **Color/value first:** the bright clamp screws identify construction; neither
    their finish nor the smooth black coat is final. Closed the drum roof, kept
    the skirt apertures, added split clamp ears and slotted screws. The first
    ears intersected the inclined skirt by about 2 mm: moved them outboard onto
    the base. The complete source/import clip sweeps now pass without a new
    contact exception. A separate 19-pose detent sweep proves indexing clearance.
12. **Color/value first:** broad gray highlights in Cycles exposed a handguard
    flank which still read flat, despite the first curved cage. Rejected it.
    Rebuilt inner and outer sections as full oval arcs with finite gauge, taper,
    a rear molded shoulder and a pin boss. The bright edge on the first corrected
    trigger exposed a flat cut toe; replaced it with a rounded tangent arc.
13. **Color/value first:** the source trigger's gray rub finish makes its face
    easier to read than our dark constant metal. Found a sharper Commons display
    photo with the entire blade exposed. Broadened the upper blade, retained
    the muzzle-facing concavity, convex back and forward lower curl, and fitted
    a new close camera to its observed blade landmarks. Fine wear remains absent.
    No source pixels or photographic outlines enter the model.

14. **Color/value first:** the dense panel's highlights exposed faint radial
    striping instead of molded pebbling. Rejected that sampling. Rebuilt only
    the dense panels on a regular surface grid; the new raking previews show
    discrete, nondirectional pebbling. The source panels are now 38.6k triangles
    each. All five exported game binary payloads remain unchanged by this repair.
15. **Color/value first:** the handguard macro showed an extra dark C behind the
    pin. Found a duplicate longitudinal shift on the surround, then replaced the
    flat ring with a 32-section band fitted to the actual curved molding. The new
    macro shows a round, seated boss at the pin. Its axes align within 0.001 mm
    and actual triangle surfaces contact the handguard on both sides. Added a
    regression check for both measurements; the final gun is 41,638 triangles.

## Current region list

A checked item means its stated form was observed in the current images, not
that the lead has accepted it or that original contours exactly copy a product.
All beauty and standalone images below use the exported GLBs. Dense polymer
comparisons are separately labeled source views. No baked normal transfer is
claimed yet.

- [x] **Trigger:** close-up (`renders/checkpoint/beauty/trigger.png`) and
  sharp photo pair (`renders/checkpoint/pairs/trigger_photo-pair.jpg`). The front
  face is concave toward the muzzle, the lower toe curls forward and has a round
  end, and the back is convex. This is a broad flat blade with radiused face
  edges, not a curved wire. The original upper blade and toe still differ in
  breadth and curvature from the photo; our toe is blunter and more rounded.
  The reference also has bright rub on the face. The pair supports direction and
  section judgment, not independent
  overall scale validation. Its camera uses observed blade landmarks.
- [x] **Lower, guard and grip:** left raking (`renders/checkpoint/beauty/lower_raking_left.png`),
  right raking (`renders/checkpoint/beauty/lower_raking_right.png`),
  lower (`renders/checkpoint/beauty/lower.png`),
  sections (`renders/checkpoint/sections.jpg`) and
  dense panel view (`renders/checkpoint/source-photos/lower.png`). Flat housing
  faces, small edge radii, front/rear pins, integrated guard roots and the
  original S/1/A arc replace the soft housing. The guard has broad molded faces,
  measured about 15.99 mm across and 6.51–7.06 mm deep at three cuts. The grip's
  actual heel/web section axis is 63.70° to the bore versus the photo estimate
  64.3° ±3°. Its width/depth change from about 36.43 ×56.07 mm low on the palm to
  31.73 ×47.70 mm at the web. Compared with the photos, our lower is still an
  original, simpler flat housing, with a broader guard and a less abrupt finger
  shelf. Panel boundaries exist in the game mesh; fine generated nondirectional
  pebbling is in the dense sources for the later normal bake, not yet in the GLB
  normal map.
- [x] **Rear drum and Eye:** drum/base (`renders/checkpoint/beauty/sights.png`) and
  exact Eye (`renders/checkpoint/beauty/aimed.png`). The top is closed, the holes
  go through the skirt and the base has split ears and slotted screws. The axis
  leans rearward 16°. Eye is 49.08 mm behind the actual near face, based on a
  close fixed-stock cheek-weld photo; pupil occlusion prevents an exact photo
  measurement. The large soft near aperture surrounds the concentric front hood,
  with its post centered against gray. Compared with the class photos, our cap
  and clamp remain simpler, the forward optical exit is larger, and the selected
  3.8-mm aperture is our own schedule. The 19-pose 0–270° sweep tests all four
  detents and intermediate travel; the accepted 21 clips are unchanged.
- [x] **Receiver and ribs:** macro (`renders/checkpoint/beauty/receiver.png`),
  raking quarter (`renders/checkpoint/beauty/raking_right.png`),
  right photo pair (`renders/checkpoint/pairs/right_photo-pair.jpg`) and
  sheet/well sections (`renders/checkpoint/sections.jpg`). Broad flat side lands,
  stepped deep press crests and tight bends replace the smooth tube/shallow
  grooves. The inside follows the presses at a visual 1.25-mm gauge; end closures,
  folded seam and spot welds remain. Rib relief is about 3.5 mm. The crests now
  cast hard shadow lines. The raking strip produces a bright reflection on the
  inspection bolt cheek; that is not final metal-response acceptance. The original
  press layout and port shape still differ from the photograph, and the weld spots
  remain more regular. Worn paint and
  stamping grain are absent at this gate.
- [x] **Handguard:** macro (`renders/checkpoint/beauty/handguard.png`),
  sections (`renders/checkpoint/sections.jpg`) and
  left pair (`renders/checkpoint/pairs/left_photo-pair.jpg`). The full-radius U
  has oval inner/outer arcs, a rounded belly, finite upper lands and taper toward
  the muzzle. Rear/middle/front cuts are about 34.01 ×43.80, 32.17 ×38.22 and
  29.81 ×32.65 mm. The rear has a molded shoulder and the pin an integral-looking
  boss. The reference has a different pin recess/texture pattern and slightly
  fuller front furniture. Ours is an original slim rounded molding; surface grain
  and the fine mold line await the bake.
- [x] **Ammunition:** mouth (`renders/checkpoint/case/case_mouth.png`),
  rim/head (`renders/checkpoint/case/case.png`),
  cartridge (`renders/checkpoint/cartridge/cartridge.png`) and
  loaded lips (`renders/checkpoint/loaded/mag_lips.png`). The standalone round and
  open fired case now each use 688 triangles, with 32-sided circumferences at
  the visible mouth, rim and extractor groove. The top display round also uses
  32 sides. Compared with the reference photographs, the exterior profile is
  still the accepted family simplification; brass is clean and the head plain.
  Small axial bevels are simplified; slight 32-sided faceting remains in the
  extreme mouth macro. Fine headstamp/soot/rub detail is absent.
- [x] **Cocking tube and charging handle:** normal (`renders/checkpoint/beauty/handle.png`),
  locked (`renders/checkpoint/beauty/locked_close.png`) and
  photo pair (`renders/checkpoint/pairs/locked_photo-pair.jpg`). Lead-accepted form
  retained; real slot, locking branch and substantial pad remain seated. The
  original pad is smoother and its locked position farther aft than the class
  photograph. Its nonreciprocating behavior is checked in every firing clip.
- [x] **Front sight and hood:** macro (`renders/checkpoint/beauty/front_sight.png`)
  and Eye (`renders/checkpoint/beauty/aimed.png`). Lead-accepted supported tower,
  band, hood and post retained. The ring surrounds the centered blade in the
  revised Eye view. Our ring/tower and weld transitions are still simpler than
  the photograph's cast/welded detail.
- [x] **Selector and controls:** lower (`renders/checkpoint/beauty/lower.png`)
  and selector strip (`renders/checkpoint/strips/Selector.jpg`). Lead-accepted
  controls retained; the added original S/1/A arc is seated on the new flat mold.
  The thumb pad remains broader than the reference's swept lever. Trigger,
  paddle, button and translating catch retain their original rigid owners.
- [x] **Stock:** macro (`renders/checkpoint/beauty/stock.png`),
  pair (`renders/checkpoint/pairs/stock_photo-pair.jpg`) and
  sections (`renders/checkpoint/sections.jpg`). Lead-accepted geometry retained,
  including the neck, changing oval section, comb and butt. Eye now sits above
  the nearer comb station, with 21.24 mm measured vertical clearance. Our belly
  and sling surround remain simpler than the museum photo; buttplate ribs and
  molding finish are deferred.
- [x] **Magazine:** loaded (`renders/checkpoint/loaded/mag_standalone.png`),
  empty (`renders/checkpoint/empty/mag_standalone.png`) and
  follower (`renders/checkpoint/empty/mag_lips.png`). Lead-accepted body, lips,
  follower and floorplate form retained; only visible cartridge tessellation
  changed. The curved body, tilted plate and lip support still read in the
  images. Our press pattern and follower remain simpler than the reference;
  paint/rub wear is absent.

## Historical form-round-2 proof and scope

The clean default command rebuilds geometry, source checks, fresh GLB imports,
all checkpoint views/pairs, sections, real-speed strips and contact sheets:

```sh
make -C guns/smg clean
make -C guns/smg
make -C guns/smg check
python3 -m compileall -q guns/smg/src guns/common/ammo9_visual.py
python3 kit/repo_check.py
```

The current gun is **41,638 triangles**, 3,062 above round 1 and 1,638 above the
original ceiling, within the authorized 42k. The pressed receiver costs 1,332
more triangles, the fuller lower 700 more and the rounded trigger 200 more.
The two new conforming pin surrounds use 768 triangles. Panel borders, clamp
screws, printed mode legend and smoother visible ammunition
also cost geometry. Recovered 1,760 triangles from the drum, 150 from the barrel
and 60 from sling trim, plus simpler small rings/markings. No accepted silhouette
was intentionally simplified to fund hidden detail. Exact per-part counts are
in `build/triangles.json`; dimensions and all GLB sizes are in the README.

All 18 actual-surface contact assertions pass in source and fresh imports. The
kit sweep reports zero violations through every clip: 1,547 source and 1,556
import samples, including quantized imported keys. Maximum depth is 0.18721 mm
against the 0.20-mm tolerance. Six original bounded contact rules remain; no
additional pair is ignored. Independent intended-state checks use 1,547
half-frame samples, 15 transitions and nine interrupted reload resumes. The rig
still has 14 bones, eight sockets, 21 clips and interface 1.3.0.

The added actual-surface tests reject reversed trigger curvature and an open
sight roof, measure Eye relief and sweep the drum through 19 poses on its real
inclined axis in source and import. Maximum detent-sweep depth is 0.01559 mm.
The imported Eye relief is 49.0828 mm. The roof ray first hits at Z=154.8297 mm.
Both pin surrounds contact the actual handguard surface and share the pin axis
within 0.001 mm; the check catches the previously duplicated Y offset. These are
exterior visual/assembly tests, not internal engineering validation.

Serialization remains separate: maximum frame translation delta is 9.22e-8 m,
linear-matrix delta 3.58e-7 and bidirectional posed-surface delta 1.08e-7 m. Raw
GLB normal direction and rigid-weight checks pass all five outputs. Source
closure is checked without a diagnostic weld; imported normal/UV attribute
splits are welded only on a diagnostic BMesh at 1e-8 m. The generator repairs a
sub-millimeter bevel/port boundary in the actual receiver mesh, rather than
relaxing the closure check. The isolated repeat build reproduces all five GLBs
byte-for-byte; hashes are in root `build/smg-r2/clean-repeat.json`. All five
retained dense-source meshes also reproduce identical vertex/topology hashes
(`build/smg-r2/high-repeat.json`).

The presentation has 330 current-source render records: 22 exported-gun views,
five exported photo views, eight dense-source views, seven standalone views and
288 clip frames. Timing/provenance is audited in `build/provenance.json`.
All current beauty/source views, pairs, sections and standalone views were
opened, together with all 16 inspection sheets covering every strip sample.
Short clips use native
60-Hz frames; longer hand motions use uniform 15-Hz samples with verified real
WebP duration. Contact sheet (`renders/checkpoint/contact-sheet.jpg`),
sections (`renders/checkpoint/sections.jpg`), photo overview (`renders/checkpoint/photo-pairs.jpg`)
and clip overview (`renders/checkpoint/clips.jpg`) collect the evidence.

Photo camera RMS remains 5.77 px right, 29.78 px left, 39.86 px locked and
18.63 px stock. The new trigger crop has about 7.79 px RMS in a 200-pixel-wide
source crop. Its lens estimate is crop-equivalent, not the original camera's
focal length. Left/locked views remain weak photographic alignments; none of
these residuals alone certifies the form. All photo authors, licenses and uses
are recorded in [refs/SOURCES.md](refs/SOURCES.md). The right photo's blue cast
is not treated as steel albedo; later hue fitting must first balance a neutral.

Kit and other guns are unchanged. The common change is confined to
`guns/common/ammo9_visual.py`: denser circumference and sparse axial stations,
688-triangle standalone round/case, and a simplified covered case-head center.
The accepted clip catalog, interface meanings, magazine construction and stock
form are retained. Final one-2048-set PBR, UV/bake checks, fine normal transfer,
issued wear, maker/model markings and final kit delivery remain closed. Nine
constant materials and zero textures are inspection aids, not final delivery.

## Final look-dev — pass 1 (exported 2048 atlas)

**Color and value first:** the first baked export is too broadly gray across
its upper receiver and tube under the neutral studio. The daylight-issued
receiver is near-black between narrow reflections. The polymer is distinct,
but the large upper highlight still makes the weapon read as clean CG.
Rejected `renders/review/pass1/{hero,receiver,lower,sights,handle}.png` after
opening all five. The exporter's default dielectric specular was higher than
the source; the next export explicitly retains a lower .28 value. Paint
roughness increases .56 → .64 while bare steel remains separately metallic.

The wear is visible, but the drum cap was incorrectly worn across its whole
roof by an axial-extremity mask. Replace it with actual radial/axial rim
distances. Clamp wear similarly needs intersections of edge distances, rather
than entire end faces. Selector dust forms a pale full circle: narrow it to
the upper recessed arc. The handle pad must receive painted steel, not the
checkpoint's polymer assignment. The grip panel shows dark specks from failed
projection. The bake reports 31,359 missed interior texels; an independent
per-part UV raster identifies both grip panels. Increase the cage and ray
range before accepting the normal transfer. No photographic acceptance is
claimed for this rejected first atlas.

## Final look-dev — pass 2 (exported 2048 atlas and four photo pairs)

**Color and value first:** the corrected right-side paint patch measures 44.0
at this pass, versus 46.47 in the neutral-balanced edited side photo and 41.14
in the outdoor issued reference. Its ratio is 1:1:1. The broad upper reflection
remains lighter because of its normal/light angle; do not increase black albedo
to match that highlight. Opened hero, receiver, lower, drum, handle and all four
photo pairs. Polymer and steel now remain separate blacks, but both still look
too smooth. Increase resolved phosphate relief at ~1.7 cycles/mm; the original
5.8/mm microtexture filtered away at this atlas density.

The drum roof is black again, with a rim, and clamp wear follows the edges.
Selector dust no longer forms a conspicuous circle. The handle's extremity
mask still exposes an entire small face; replace it with intersecting edge
distances. The longitudinal support-hand rub remains only a lighter black;
replace it with opaque gray phosphate in a narrow, tapered strip between the
receiver ribs. This is a real flat rubbing location, not a noise blotch.

The larger cage reduced misses to 9,933, but rays on the grip's backing and
horizontal return faces still point away from the retained dense front skin.
Add the accepted low backing/returns to the dense bake source and use a 3-mm
cage / 12-mm ray. The next bake has zero missed interior texels in every channel.
The actual game mesh, rig and clips remain unchanged by that source correction.
The locked pair's removed magazine is visible below the gun; hide it only in
that presentation frame to match the reference's empty scene. This does not
change the reload clip or detachable delivery.

## Final look-dev — pass 3 (zero-miss exported atlas)

**Color and value first:** the third hero retains neutral black paint and the
slightly greener polymer. Opened all five 1200-pixel review stills and the four
new photo pairs. Broad upper highlights still differ from the photograph's
light, while the flat receiver patch is close in value. The photographic
polymer spans 34.40 in direct outdoor light to 67.77 on the shaded display
stock; our flat right lower is 56.0, left lower 20.72 under its different normal.
These are display values, not an albedo inversion or proof of identical light.

The grip's black projection specks are gone. All six bake channels report zero
missed interiors. The full atlas round trip passes all 1,547 affine samples,
posed surfaces, UVs, normal direction, 21 clips and identical embedded maps in
all five outputs. The delivery's 41,540 triangles differ from the accepted
41,638 only by collapsed microscopic Boolean/panel-pole triangles removed for
valid UVs; the independent final construction sweep passes.

The finish still needs a stronger, physically localized flat rub. The next
pass replaces the left-flank muted patina with exposed phosphate in a long,
narrow track, and narrows the handle's face rub to its corners. The floorplate
also needs rim distances in its actual tilted frame. Add fine weld bead relief
and smooth the dense grip's pebbled peaks where hands polish them. Keep these
in the normal map. Do not add triangles or broad random damage to hide the
remaining original geometric simplifications.

## Final look-dev — pass 4 (native-size hero, detail and exact Eye)

**Color and value first:** opened all seven 1400-pixel stills, including the
exact Eye and locked-handle view. The blacks remain neutral and separate;
the hero's upper rolled surface has a broad gray reflection, but its flat
lands stay dark. The native hero now clearly shows phosphate rub without a
contrast stretch. Rejected the first long flat-rub mask: it reads as an even
horizontal gray bar. Shorten it to the actual forward support-hand area and
taper it as a soft, irregular contact patch. The small boundary perturbation
must stay below a shipping texel, not form periodic scallops.

The handle's whole-face silver patch is gone; the pad is black painted steel
with corner rub. Keep the separate shaft bright. The fired/loaded ammunition
and the hood still need their final macro review, and no docs are committed.
The Eye view has the accepted large soft aperture, concentric hood and centered
post on gray, without moving its socket. Finish the phosphate's resolved
microtexture, fine weld relief and the dense panel's polished peaks. Final
floorplate wear follows its tilted frame rather than a uniform silver band.
These refinements use the same one-atlas delivery and add no game geometry.

## Final look-dev — pass 5 (all finals and macro rejection)

**Color and value first:** the native hero has display luma p1 / median / p99
of 1.00 / 35.72 / 190.57, with 28.73% below 24 and no clipped object pixels.
Intact paint stays black, phosphate is gray and the sharpest rubs are metallic.
An independent shipping-UV raster finds 8,053 bright-steel and 14,789 phosphate
texels on 198,000 exterior receiver samples. Their median BaseColor RGB is
160/164/166 and 77/80/78 respectively; intact exterior median is 13/14/13.
The four rib bands span 0.52–0.70 mm between bright texel sample centers, about
one to two texels at their measured density. This is actual-map evidence, not
a source-mask screenshot or an opacity claim.

Opened every Cycles still in four inspection sheets, the native hero on both
sides, Eevee, all seven detached/ammunition stills, and the exact Eye. The
shortened forward-flank patch no longer looks like a long painted gray bar.
The hood macro still exposes too much of its flat annular face: restrict wear
to the inner/outer sharp rims. The cartridge tips look crumpled in the normal
bake although their accepted geometry is unchanged. The 3-mm projection cage
is excessive relative to their radius. The new grip backing/returns now permit
a 0.65-mm cage / 4-mm ray without holes; test that smaller cage before shipping.
The first reduced-cage emission passes retain zero missed interior texels.

The final measurement audit also rejected the outdoor rear-cap patch as a
polymer sample. Use the clearly visible polymer lower in `navy2.jpg` instead,
retain the fixed-stock sample separately, and retain the outdoor photo for its
visible steel and magazine. This region correction changes the comparison
report, not the shader inputs. All source pixel polygons and neutral selections
are explicit in `src/white_balance.py`.

The scale image initially clipped the cyclorama at the shared renderer's
20-m far plane. Rotate its seamless behind the camera's view and use a 200-m
scale-only clipping distance. The gun and human keep their real dimensions;
no camera shift or per-object size adjustment enters delivery.

## Final look-dev — pass 6 (projection and macro checkpoint)

**Color and value first:** black paint, polymer and the ammunition's brass/copper
remain separate materials after the reduced-cage bake. The hood now retains
black paint between narrow inner/outer rim rubs. Opened the new hero, hood,
scale, loaded lips and both case views. All six reduced-cage channels have zero
missed interior texels; the grip-return repair remains effective.

The smaller cage cleans up the rim's transfer but does not remove the jacket's
lumpy highlight. The remaining issue is the triangulated game mesh being used
as its own dense normal source. Rebuild only the ammunition bake source as
regular 128-segment quad revolutions of the already accepted visual profiles.
The game vertices, 688-triangle standalone budgets, rig and ammunition exterior
anchors stay unchanged. The new `guns/common/ammo9_bake.py` calls the existing
profile builder read-only; no existing common module or other gun changes.
This normal-source correction requires another bake and review, rather than
calling the remaining distortion physical dents.

## Final look-dev — pass 7 (dense source and reflection diagnosis)

**Color and value first:** the dense-source export preserves the distinct
black finishes, brass cases and copper jackets. Opened all three new macro
views, then a matte diffuse diagnostic with the baked normal retained and a
metallic diagnostic with the normal disconnected. The diffuse jackets have
smooth gradients; the normal-off metallic view retains the same broken bright
patterns. Those remaining patterns are reflections of adjacent rounds/feed
lips, rather than evidence of dents. The earlier cage hypothesis did not
explain them. Keep the regular dense source for cleaner rim/primer transfer,
without claiming it removes physically valid neighboring reflections.

All six bake channels remain at zero missed interiors. The source-only dense
ammunition's measured bounds match every finalized counterpart within 1 µm
(`build/delivery/high-ammo-check.json`); the case/template bound delta is below
1 nm. The delivered game geometry is unchanged. A 0.65-mm cage and 4-mm ray
now work because the grip's real backing/returns are present. The hood's flat
face retains a black center between narrow worn rims. The corrected scale-only
200-m far plane removes the cyclorama's circular clipping boundary. Regenerate
all final stills, source/export pairs, clip frames, contact sheets and docs from
this canonical export before committing imagery.

## Final white balance and photographic measurements

All values below use corrected native reference pixels. Linear RGB gains preserve
the neutral patch's Rec.709 luminance; they correct chromaticity, not exposure.
These are estimated scene neutrals, with mixed light and photographic editing
remaining uncontrolled. Display luma is on 0–255; ratios use median RGB with G=1.

| Photo | Neutral / native rectangle | Linear RGB gains |
| --- | --- | --- |
| `left.jpg` | white safe-selector S legend, brightest paint pixels; edited image, auxiliary; [596, 224, 605, 237] | 2.116103 / 0.897424 / 0.703810 |
| `right.jpg` | unclipped pale gray studio backdrop; auxiliary; [1300, 100, 1500, 350] | 1.000000 / 1.000000 / 1.000000 |
| `navy2.jpg` | white selector legend on upper gun; brightest paint pixels, estimated neutral; [2270, 535, 2330, 565] | 0.995370 / 0.995370 / 1.063568 |
| `trigger-ref.jpg` | white selector safe legend; brightest paint pixels, estimated neutral; [2280, 882, 2340, 922] | 0.989718 / 0.998704 / 1.045416 |
| `daylight.jpg` | gray painted ship bulkhead in daylight, estimated neutral; [1700, 950, 1800, 1100] | 1.242894 / 0.941005 / 1.047759 |

The display photographs are daylight views of issued guns at an exhibition.
The outdoor ship photograph independently constrains the visible steel and
magazine. The edited side and studio quarter remain auxiliary comparisons.
The stock is retained separately from the clearly identified polymer lower.

| Corrected photograph | Surface | Median luma | R:G:B, G=1 |
| --- | --- | ---: | --- |
| `left.jpg` | paint | 46.71 | 1.0435:1.0000:1.0217 |
| `left.jpg` | polymer | 67.22 | 1.0455:1.0000:1.1212 |
| `left.jpg` | magazine | 61.69 | 1.2203:1.0000:1.0000 |
| `right.jpg` | paint | 35.28 | 1.0278:1.0000:0.7778 |
| `right.jpg` | polymer | 68.93 | 0.9143:1.0000:1.0429 |
| `right.jpg` | magazine | 69.79 | 1.0145:1.0000:1.0580 |
| `navy2.jpg` | paint | 35.07 | 1.0571:1.0000:0.9429 |
| `navy2.jpg` | polymer | 30.93 | 0.8438:1.0000:1.0312 |
| `navy2.jpg` | polymer stock | 67.77 | 1.0294:1.0000:0.9265 |
| `navy2.jpg` | worn phosphate | 81.95 | 1.0370:1.0000:0.9753 |
| `trigger-ref.jpg` | paint | 110.85 | 1.0545:1.0000:0.9364 |
| `trigger-ref.jpg` | polymer | 114.78 | 1.0000:1.0000:0.9739 |
| `daylight.jpg` | paint | 41.14 | 1.1250:1.0000:1.0000 |
| `daylight.jpg` | magazine | 41.34 | 1.1750:1.0000:1.0000 |

Native polygons, neutral masks and overlays rebuild from `src/white_balance.py`
in `build/white-balanced/`. Source reference pixels never enter the asset.
The initial rear-cap “polymer” selection in the outdoor image was rejected
during region review and is excluded from this final table.

## Final look-dev — pass 8 (first finish submission; subsequently rejected)

**Color and value first:** the final exported gun keeps a neutral near-black
paint and a deeper, slightly greener polymer. Broad reflections still depend
on the surface normal and lighting. The right paint sample is 44.00, between
the corrected outdoor 41.14 and edited auxiliary 46.71. The display photograph
gives paint 35.07 and lower polymer 30.93. Our opposite sides bracket those
shaded values; this is a useful value-range comparison, not exposure matching.
The hero's object-mask luma p1/median/p99 is 1.00 / 35.72 / 190.57, with 28.90%
below 24 and no clipped pixels. Receiver cavities, the slot and grip underside
retain deep shadow. The broad upper reflection does not turn the paint albedo
gray or blue.

| Exported photo view | Actual surface sample | Median luma | R:G:B, G=1 |
| --- | --- | ---: | --- |
| Right | paint | 44.00 | 1.0000:1.0000:1.0000 |
| Right | polymer | 56.00 | 1.0000:1.0000:1.0000 |
| Right | magazine | 38.72 | 0.9744:1.0000:0.9744 |
| Left | paint | 27.72 | 0.9643:1.0000:0.9643 |
| Left | polymer | 20.72 | 0.9524:1.0000:0.9524 |
| Left | magazine | 26.00 | 1.0000:1.0000:1.0000 |

Opened all 19 final gun views, the Eevee hero and all seven standalone views,
the four exported photo pairs and four dense-source pairs, the native-scale
wear pair, all 16 inspection pages covering every one of the 288 strip samples,
the contact sheet and all five final documentation JPGs. The hood face keeps
black between worn rims. The drum roof stays black, its rim and clamp edges
rubbed. The handle shaft and port steel remain distinct from paint. The flat
left receiver rub tapers between crests. The feed lips and floorplate show
localized metal rather than a washed-out gray magazine. The grip relief is
softer in the shipping normal than in the dense source; smooth contact areas
still polish differently from textured areas. No black ray-miss specks remain.

The native wear comparison preserves the hero pixels, resizing only the
reference to the measured receiver span; it is neither a contrast boost nor
an enlarged asset crop. Its 230-mm receiver-length assumption is stated in
`renders/final/pairs/native-wear-values.json`. A separate barycentric UV audit
reads actual shipping pixel centers on exterior receiver triangles. Of 198,000
audited texels, 8,060 classify as bright steel (median BC 160/164/165, metallic
234/255) and 14,818 as phosphate (BC 77/80/78, metallic 183/255). Overall median
BC remains 13/14/13. Bright rib samples span 0.52–0.70 mm across their crests,
about one to two shipping texels. These measurements concern the baked maps,
not the source shader masks or their padding.

The final complete `make -C guns/smg` passes, including `check`, with the
canonical exports below. The earlier explicit `make -C guns/smg check` also
passed. Source, finalized and reconstructed imported triangles all pass their
18 contact assertions and independent state checks. Motion sweeps use 1,547
finalized and 1,556 imported samples: zero violations, maximum measured depths
0.187198 / 0.187210 mm against the existing 0.20-mm tolerance. The inclined drum
also retains its independent 19-pose sweep. Intended-state checks cover 1,547
half-frame samples, 15 transitions and nine reload resumes. Round-trip affine
translation differs by at most 9.22e-8 m and linear terms by 3.58e-7. This proves
serialization separately from the contact/clearance assertions.

The gun is 41,540 triangles, one mesh/material, 14 bones, eight sockets and
21 clips. Standalones are 5,792 loaded / 4,048 empty / 688 cartridge / 688 case.
The one 2048 BaseColor/Normal/ORM set comes from a 4096, 32-sample GPU bake:
zero missed interior texels in all six channels, each auditing 5,658,237 texels.
All five outputs embed the same three image hashes. Imported-gun atlas
coverage is 36.87%; density p5/p50/p95 is 1,313.65 / 2,382.22 / 2,637.90 px/m.
One microscopic intersection has overlap fraction 8.11e-8; no outside or
degenerate UV triangles remain. Full source-atlas coverage, including separate
ammunition, is 39.36%. GLB sizes and PNG bytes are listed in the README.

The final gun SHA-256 is
`69b059e5f90678c10a25c9607f479762a7341cc5afd881402a300f2764c1ebfe`.
`src/final_review.py` verifies 323 current-source render records: 319 from the
five baked GLBs and four explicitly labeled dense-source comparisons. It also
decodes WebP durations at real speed: short clips use 60-Hz samples; longer
motions use 15-Hz samples. Inspection sheets supplement the animated strips,
not replace their timing check. All requested images are collected at
`renders/final/contact-sheet.jpg`; originals, pairs and strips remain beneath
`renders/final/`. Only the five finished, <=1600-pixel / 200-KB `docs/*.jpg`
images are committed.

Remaining weaknesses: the lighting is estimated, the left/locked camera fits
have 29.78/39.86-pixel RMS residuals (right 5.77; trigger crop 7.79), and the
display photo's individual scratch history is more irregular and severe than
our continuous edge rubs. Very fine grain, stamps and weld relief soften in
2048 delivery. Extreme case-mouth close-ups reveal the accepted 32-sided
silhouette. The loaded/empty magazines retain held-gun detail for reuse rather
than supplying a separate reduced dropped-prop mesh. These are documented
limits; no exact photographic identity or internal engineering is claimed.

The merge preserved every family index entry and interface supplement. No kit,
other gun or pre-existing common module changed during look-dev. The sole new
common helper, `guns/common/ammo9_bake.py`, builds dense source revolutions from
the accepted family profiles without changing their game meshes. Nothing is
needed from the lead to rebuild or inspect delivery. A future general kit
feature could record shipping-pixel material classifications and merge partial
render provenance, but this task keeps both wrappers local as instructed.

## Finish round 2 — pass A: remeasure before changing wear

**Color and value first:** the lead correctly rejected the first finish's
one-sample rationale for a deeper polymer. The four comparisons with lighter
polymer govern the revision: edited side 46.71/67.22, studio 35.28/68.93,
issued display paint/stock 35.07/67.77, trigger display 110.85/114.78. The
shaded lower at 30.93 remains a real sample, but does not determine the material
ordering. The previous finish acceptance language above is superseded; its
delivery/assembly evidence remains valid and was accepted by the lead.

Before changing the masks, measured `navy2.jpg` at native resolution after
white-balancing on the upper gun's white selector legend. The ribbon is
[1900,294,2600,316], directly below the crest, excluding its thin rim glint.
The approximate 1090-pixel / 230-mm receiver envelope gives 4.739 px/mm, so
the sample spans 147.71 ×4.64 mm. Observed wear is luma >65; gray is 65–180,
bright >=180. Area classification is on native pixels. Half-mm longitudinal
bins count as worn above 25% ribbon occupancy; isolated half-mm holes/specks
are removed for run lengths only. Boundary-clipped runs do not supply a
complete chip/gap length. `src/wear_metrics.py` reproduces all selections and
the overlay/classification, without putting source pixels into the asset.

The photo has **55.93% worn length**, median chip **2.0 mm** (IQR 1.0–4.5),
median gap **2.5 mm** (IQR 1.25–8.0), **44.0% worn area**, and **98.94% gray /
1.06% bright** among the worn pixels. Thresholds 60/70 give 56.95/55.59% length,
1.5/1.5-mm chip medians and 2.25/2.5-mm gaps. This supports the length scale,
but is not a precision paint-chemistry measurement: perspective, reflection,
threshold choice and estimated scale remain limitations.

The first rebake raises paint roughness .64 → .83, polymer .48 → .84 with
handled areas .27 → .65, and phosphate .57 → .88. Phosphate metallic .75 →
.08; rare steel remains separate. Paint linear base becomes
.0034/.0035/.0034 and polymer .012/.013/.012. Under the unchanged studio,
the left hero's actual paint/lower samples read 36.21/53.72, right 23.00/41.00;
stock 54.72/41.72. Opened all five pass-A GLB views. Reflections are softer
and the ordering reads, but the rib patterns still cover 64–73% of the test
length, too much, and have no resolved bright flecks. Reject that wear pass.

## Finish round 2 — pass B: spacing and pressure

**Color and value first:** retain the corrected deep paint and grayer polymer;
the same lights now produce a broad, gentle rolloff instead of the old bright
reflection boundaries. Opened both heroes, receiver, lower, drum and all four
matched GLB views. Gray conversion coating is diffuse rather than chrome.
Reduce longitudinal coverage and retain only tiny steel flecks at sharp
contact points. The four sampled crests now cover 43.7–56.3% of their lengths,
but their median gaps are still 4.0–7.25 mm. Fine irregular chip contours read
better than the original trim; the spacing is still wrong. Reject for another
pattern pass, keeping the material/value correction.

## Finish round 2 — pass C: reject barcode-shaped chips

**Color and value first:** matte phosphate and the two blacks retain the new
ordering. The close receiver view reveals that explicitly seeded longitudinal
runs have square ends spanning too much of each crest's width. They read as
short bars, despite plausible run-length numbers. Opened both heroes, receiver,
lower, drum and all four matched views; do not let statistics certify that
appearance. Reject the interval shader. Replace it with fully two-dimensional,
independently generated fracture contours, with small resolved ragged edges
and pressure-driven width/coverage. The intermediate masks remain original
script output, are independent of the reference image, and bake into the
same one-2048-set delivery. Geometry and accepted ammunition remain unchanged.

## Finish round 2 — passes D–F: two-dimensional fractures and shipping calibration

**Color and value first:** retain paint .0034/.0035/.0034 and grayer polymer
.012/.013/.012. The unchanged studio now gives diffuse upper-body gradients
and a readable lighter lower/stock, rather than sharp bright reflection bands.
Compared the fixed-light checkpoints and the matched daylight views against
the neutral-balanced photographs. The display stock/lower's broader, flatter
reflection is the relevant polymer guide; its single shaded lower sample is
not a universal material value. No light, exposure or camera was changed to
create the finish difference.

Opened each nine-view D/E/F checkpoint, including both full heroes and native
receiver/lower close-ups. D's fractures remove the barcode ends, but the
actual upper-crest audit still gives 64.4% worn length. E reduces this to 55.6%,
but its small-chip/gap distribution is 3.0/1.5 mm. F shifts the independent
two-dimensional field's longitudinal wavelength and concentrates coverage more
strongly at the physical well/end contact stations. Its shipping upper-crest
result is **54.58% / 1.5-mm chips / 2.5-mm gaps**. The photo is
**55.93% / 2.0-mm chips / 2.5-mm gaps**. The half-mm chip difference is one
measurement bin; changing the photo threshold by ±5 already moves its median
to 1.5 mm. This matches the statistical scale without reproducing chip outlines.

| Left exterior crest, Z | Worn length | Median chip | Median gap | Gray / bright worn texels |
| --- | ---: | ---: | ---: | --- |
| 86.1 mm | 57.63% | 1.5 mm | 4.25 mm | 99.50% / 0.50% |
| 89.1 mm | 59.32% | 1.5 mm | 3.00 mm | 97.53% / 2.47% |
| **102.7 mm, preselected comparison** | **54.58%** | **1.5 mm** | **2.50 mm** | **98.35% / 1.65%** |
| 105.9 mm | 62.03% | 2.0 mm | 3.50 mm | 98.71% / 1.29% |
| Photograph | 55.93% | 2.0 mm | 2.50 mm | 98.94% / 1.06% |

Each shipping ribbon has the photo's approximate 147.7-mm span and 4.6-mm
depth. Sampling is barycentric at actual 2048 UV-pixel centers on exterior
receiver triangles, not the high shader's masks. All 295 longitudinal bins
have samples. The other crests retain natural variation rather than identical
patterns. Their pooled medians are 1.5-mm chips and 3.0-mm gaps; the photo's
IQRs are broad. Photographic gray/bright are observable luma bins, while the
shipping distinction uses actual BaseColor and metallic pixels; neither is a
recovered measurement of the photograph's coating chemistry.

Across all 198,000 audited exterior receiver texels, 31,777 classify as gray
phosphate and 481 as bright steel: **98.51% gray / 1.49% bright** among those
worn texels. Intact paint's actual median BaseColor is 11/11/11 and ORM
239/212/0. Phosphate's median is BC 65/67/65 and ORM 243/221/18: measured
roughness **0.867**, metallic **0.071**, versus the authored **0.88 / 0.08**.
Boundary filtering accounts for that modest reduction. This replaces the
rejected conversion coating's metallic 183/255. Bright steel is authored at
metallic 1, roughness .58, restricted to small sharp-point flecks.

Paint roughness is authored .83 and measures **212/255 = 0.831** in intact
shipping pixels. Polymer is authored .84 on untouched surfaces, .65 at hand/
cheek contact. Actual lower and stock medians are **214/255 = 0.839**; their
p5–p95 ranges are .682–.843 and .749–.843. The heavily handled handguard's
median is .667, range .651–.843. It remains faintly satin rather than the
previous .27 mirror-like handling polish. The grip's accepted pebbled geometry
and its dense source are unchanged.

`src/paint_masks.py` reads no references: it generates original rest-frame
fractures from independently seeded multiscale fields and causal bands.
Small boundaries resolve below a shipping texel, with opaque phosphate inside
the chips. Intermediate mask previews are calibrated below final apparent
coverage because linear-color mixing and atlas filtering expand their visible
edges. Only the final UV audit supplies the numbers above. Receiver-end/well
patches, broken flank rubbing, top edges, caps and floorplate no longer use
continuous bright cores. The final complete export/GLB-render rebuild follows
this F checkpoint; its photographic review and checks are recorded below.

## Finish round 2 — pass G: secondary rims and final hero values

**Color and value first:** the final 64-sample heroes preserve the corrected
material ordering under the same lights. These are projected actual triangle-
ray regions on the opaque rendered surfaces, with no per-material exposure
adjustment. The left paint/stock contrast is 36.21/54.72 and the right is
23.00/41.72. The polymer is visibly grayer at full frame; the paint stays deeper.

| Actual final hero region | Left median luma | Right median luma |
| --- | ---: | ---: |
| Intact receiver paint | 36.21 | 23.00 |
| Polymer lower | 53.72 | 40.86 |
| Polymer stock | 54.72 | 41.72 |
| Polymer handguard | 42.82 | 30.72 |
| Magazine body | 33.00 | 24.00 |

The full-resolution F stills exposed soft, spotty generic wear on the hood and
tube, despite the main receiver's improved fractures. Narrowed generic rim
phosphate to a 0.50–0.78-mm distance transition, left the hood's center paint
intact, and used smaller resolved chips with firmer boundaries. Tube-top rubs
now expose opaque, rough phosphate in broken fragments. Opened the G hero,
native handle, hood and drum checkpoints: the shapes are finer and the slot's
deep shadow remains. The receiver's independently generated fields, its four
measured ribbons, material values, geometry, rig and delivery layout do not
change in this refinement.

The current receiver exterior audit has 31,437 gray and 475 bright texels:
98.51% gray / 1.49% bright among exposed texels. Its median phosphate ORM is
243/221/18 (roughness .867 / metallic .071). Intact paint is BC 11/11/11,
ORM 241/212/0. All four ribbon statistics in the preceding table are unchanged.
The hero's object-mask luma p1/median/p99 is **6.0 / 48.0 / 124.5**, with
9.60% below 24 and no clipped whites. The lower overall contrast follows the
matte finish and grayer furniture; cavities and the slot retain deep shadow.

The G checks and final media regeneration use the same canonical
five exports. The accepted position/normal/UV/skin/animation buffers and
node/accessor layout match the acceptance hashes; exporter-derived tangent
frames are regenerated. No kit, common module, other gun, geometry generator,
rig, clip, camera or studio-light configuration changes in this finish round.


### G final media review and proof

**Color and value first:** reviewed both complete G heroes at full frame and
the native receiver/magazine crop. The lighter lower, comb and handguard read
separately from the deeper painted shell. Receiver highlights now spread into
soft, low-contrast gradients instead of bounded glossy panels. Compared the
white-balanced display and side pairs again: the photographs still have mixed
light and different reflection angles, so their brightness is a range rather
than an exact rendered exposure target. The rough phosphate chips remain
visible without turning the crest into a polished line.

Opened all 19 final beauty views, the Eevee hero, seven standalone views, all
four shipping and four dense-source photo pairs, the native wear pair, and
all 16 clip inspection sheets (288 frames). Also opened all five replacement
docs JPGs and the final contact sheet. Caps and floorplate now carry broken
coating loss; the hood retains central paint between smaller rim chips. The
left flank's exposed gray is interrupted and matte. Fine chip boundaries,
stamps and the smallest sight-rim chips still soften at 2048; the sight close-up
is the weakest finish view. The receiver remains more orderly overall than
the issued photo because wear follows our original pressed ribs. No photograph
was traced or used as a texture. Photographic millimeter scale and gray/bright
classification remain estimates, with the threshold sensitivity above.

The final command `make -C guns/smg check docs` completed successfully. All
five round trips passed; all accepted geometry/UV/normal/weight/rig/clip/layout
fingerprints match. The source, finalized and imported construction checks
pass all 18 contacts with zero clearance violations; the imported sweep has
1,556 samples and maximum penetration 0.18721 mm against 0.2-mm tolerance.
All 21 clips, 15 transitions, nine resume checks and the 19-pose drum sweep
pass. All six 4096 bake channels cover 5,658,237 audited interior texels with
zero missed rays. UV, normals, material, texture, scale and budget checks pass.
No geometry, rig, clip, eye, delivery-layout or studio-light change accompanies
this finish revision.

Final gun SHA-256:
`a7e543919a79ec5672a492e71914ce3ced7994942d69f8e62574ffc12d6a9b41`.
The gun remains 41,540 triangles; the other exports remain 5,792 / 4,048 /
688 / 688. All five share one material and the same three 2048 images.
The gun GLB is 10,537,280 bytes; the canonical PNG set totals 6,975,170 bytes.
The final provenance check verifies 323 render records (319 from shipping
GLBs and four labeled dense-source comparisons).

Generated review paths:
`renders/final/contact-sheet.jpg`, `renders/final/pairs/native-wear-pair.jpg`,
`renders/final/finish-values.json`, and
`renders/final/beauty/hero-receiver-magazine-native.png`. The last is a
592×673 crop of the 1600×800 hero, rectangle (441,94)–(1033,767), without
resampling or contrast changes. The five final docs JPGs replace the first
submission's images. No new toolkit feature or lead input is required.

## Finish round 3 — pass A: contour replacement and satin response

**Color and value first:** keep the accepted paint .0034/.0035/.0034 and
polymer .012/.013/.012. The lead's round-3 rejection supersedes round 2 G's
visual acceptance language: its numbers did not certify convincing chip shapes
or sheen. The full-resolution original hero and receiver/magazine crop showed
tiny square fragments between straight ribbon margins. The phosphate remains
.060/.064/.061, roughness .88, metallic .08; bright steel remains a separate,
rare finish. Neither the game geometry nor the atlas packing changes.

Replace the receiver's bicubic resized random grids and independent clipped
bands with continuous quintic noise, warped coordinates, mixed physical scales
and a threshold that rises with distance from the rubbing crest or area center.
Coverage AA uses the signed field's local gradient at the generated mask's own
resolution. Density falls at margins, with opaque interiors, rounded islands,
merging neighbors and irregular outlines. The source generator reads no photos.

Opened both 1600-pixel A heroes, receiver, handle, hood, drum and stock, and the
nearest-neighbor 4x chip crop. Shapes are better, but reject the first field's
3.0-mm median runs / 9.75-mm gaps on the shipping comparison crest (50.17% worn
length). Also reject the nearly continuous restored crown line and overly broad
secondary rim loss. Corrected the tube's front distance (actual game surface
332 mm, previously tested at 344.5 mm), explicitly followed its through-slot,
and included the cap. A distance-biased threshold replaces the secondary
binary width cutoff. End-cap roof abrasion follows the actual ellipse rather
than stripping an entire end face.

## Finish round 3 — pass B: contact distribution and sheen sweep

**Color and value first:** retain the two accepted base colors. Tested paint
roughness .64/.70/.76/.83 in explicitly labeled GLB shader diagnostics, under
the same key/fill/rim setup and exposure. Opened every diagnostic hero and crown
view. .83 loses the satin response; .64 makes the light region more conspicuous.
Selected central paint roughness .68, untouched textured polymer .78, handled
polymer .48. Phosphate .88/.08 and steel .58/1 remain unchanged. Source paint
specular is aligned to the existing .28 delivery override; no exported IOR or
studio light changes.

Opened both B heroes and all five close views. The top track is now sparse
between pressure stations and stronger at corners/end and well stations;
secondary rims break into thin chips. Shorter fracture wavelengths give
57.29% / 3.0-mm chips / 2.0-mm gaps on the shipping upper ribbon, with 98.42%
gray / 1.58% bright. Reject the remaining long median chip size. The next
field's dominant longitudinal wavelength is 1.10 mm, with coarser cluster
variation, smaller outline variation and the same continuously falling density.

The initial attempt to measure a full highlight through the 3/4 hero was
rejected: the far half runs into the silhouette, and wear can contaminate the
peak. Added an explicitly supplemental crown camera under the unchanged studio
lights, keeping all accepted final cameras intact. Width and value selections
are scripted in `src/highlight_review.py`; estimated photographic scale and
unknown source dimensions remain limitations. The two neutrals remain the
issued display's selector legend and the studio quarter's gray backdrop.

## Finish round 3 — passes C–F: shipping calibration and complete comparisons

**Color and value first:** unchanged black-paint and grayer-polymer albedos keep
the accepted ordering. Opened every D/E 1600-pixel hero and close-up, including
hood, slot, drum and stock, and both forward and aft native hero chip crops at
4× beside the white-balanced photo. There is no per-image contrast enhancement.
The forward pressure station forms larger merged patches, while the middle and
aft crests retain separate smaller chips. Boundaries are curved and irregular;
there is no per-texel random threshold or independent straight band cutoff.
The actual 2048 maps inevitably limit subpixel outlines.

C's first build was discarded after a duplicate Make invocation removed its
intermediate color map; D rebuilt all six channels cleanly. D gave 58.31%
upper-ribbon coverage / 2.0-mm median chips / 2.0-mm gaps. E reduced coverage too
far, to 51.86% / 1.5 mm / 2.5 mm. F uses the midpoint density threshold and
extends the secondary abrasion around the raised branch of the actual handle
slot. End-cap wear follows both side rims and the rolled roof's actual ellipse.
All these are finish-only changes; accepted mesh/rig/clip/layout bytes stay fixed.

The new `chips-4x-pair.png` compares both the forward/well pressure region and
the middle/aft crest, using native hero pixels replicated 4×. Only the reference
is first resized to a common receiver scale. Counts and percentages in the
<2 / 2–<4 / 4–<8 / >=8-mm bins are **complete longitudinal ribbon runs** under
the existing half-mm occupancy method, not falsely claimed 2-D component areas.
The photo pattern is never used as a source mask.

The controlled roughness sweep retains .68 paint / .78 untouched textured
polymer / .48 handled polymer. The accepted studio lights, exposure, hero and
photo cameras remain unchanged. A supplemental top/crown view makes the whole
highlight visible, avoiding the silhouette-censored 3/4 measurements. Width is
measured at half the peak's excess above each fixed intact-crown profile's
median; the older flat-land photo medians remain separate fields. These baselines
must not be conflated. Both photos keep their original white-balance neutrals
and gains from the preceding tables.

### F shipping measurements

**Color and value first:** intact paint's shipping BC remains 11/11/11; the
polymer lower/stock remains 29/30/29. The worn gray median is 64/67/65,
roughness 216/255 = .847 and metallic 18/255 = .071 after filtering. Authored
phosphate remains .88/.08. There are 27,009 gray and 328 bright exterior
receiver texels: 98.80% gray / 1.20% bright among the exposed texels.

| Exterior left crest Z | Worn length | Median chip | Median gap | Gray / bright worn area |
| --- | ---: | ---: | ---: | --- |
| 86.1 mm | 60.00% | 4.25 mm | 2.50 mm | 98.99% / 1.01% |
| 89.1 mm | 51.53% | 2.75 mm | 2.25 mm | 99.39% / 0.61% |
| **102.7 mm, same preselected comparison** | **54.92%** | **2.00 mm** | **2.50 mm** | **99.20% / 0.80%** |
| 105.9 mm | 51.86% | 2.00 mm | 1.50 mm | 98.11% / 1.89% |
| Photograph | 55.93% | 2.00 mm | 2.50 mm | 98.94% / 1.06% |

The selected shipping ribbon's complete-run distribution is 9 / 9 / 2 / 2
runs in <2 / 2–<4 / 4–<8 / >=8 mm (40.91 / 40.91 / 9.09 / 9.09%). The photo
has 5 / 3 / 2 / 1 (45.45 / 27.27 / 18.18 / 9.09%). Shipping IQR is
1.5–3.0 mm, p90 4.9 mm, maximum 19 mm; photo IQR 1.0–4.5, p90 6.5, maximum
12 mm. Source/atlas filtering, perspective and clipped boundary runs limit
this comparison. The shipping pattern has more complete small/medium runs,
and its longest merged patch is longer. Statistical similarity is not a claim
of identical individual wear history or contours.

Actual intact-paint roughness is 174/255 = **.682**. Lower/stock interior
medians are 199/255 = **.780**; their p5–p95 ranges are .533–.784 and
.635–.780. The heavily handled handguard has median **.506**, p5–p95
**.478–.780**, reflecting the authored .48 handled endpoint. No polymer
albedo was darkened to obtain sheen. The reproducibility rerun compares both
complete final 4096×1172×3 mask arrays byte for byte; both pass, with 80,030 /
69,145 coverage-AA texels. Its hashes/report are in
`build/finish-round3/f-mask-reproducibility.json` at the worktree root.

| Intact crown under fixed profile method | Local median | Peak | Peak / median | Half-excess width, native px | Approximate projected width |
| --- | ---: | ---: | ---: | ---: | ---: |
| White-balanced `navy2.jpg` | 80.36 | 109.39 | 1.36 | 20.85 | 4.40 mm |
| White-balanced `right.jpg` | 26.14 | 42.93 | 1.64 | 10.07 | 5.65 mm |
| Shipping GLB, supplemental studio crown | 68.27 | 86.96 | 1.27 | 169.01 | 17.87 mm |

None of these three widths is boundary-censored. The photographs' separate
flat-land paint medians are 35.07 and 35.28; peak / flat-land ratios are 3.12
and 1.22. All luma values are display 0–255. The local profile is a spatial
median across the fixed intact-crown strip; the peak uses a three-sample box.
The white-balance neutrals remain the issued display's white selector legend
and the quarter-view studio's unclipped gray backdrop, with the earlier gains
unchanged. The measurement rectangles and complete sampled profiles rebuild
in `renders/final/pairs/highlight-values.json`; their visual plot is
`renders/final/pairs/paint-highlight-pair.jpg`, including the shipped roughness
values beside the references.

**Remaining visual weakness:** .68 restores the soft satin peak on paint and
the stock comb reads under the key, but the supplemental studio reflection
remains broader and lower in local peak contrast than the selected photographs.
Do not call this an exact highlight match. Uncontrolled source lighting,
perspective, the projected scale estimate and different crown cross-sections
prevent treating these measurements as a recovered BRDF. No lighting change
or per-image grading was used to hide the difference. At 2048, the finest
chip boundaries also soften; the shipping IQR is narrower and the largest
merged run longer than the photograph's. The native and 4× pairs expose those
limits rather than claiming all differences are gone.

| Actual triangle-ray hero patch | Left median luma | Right median luma |
| --- | ---: | ---: |
| Intact paint | 42.00 | 23.00 |
| Polymer lower | 55.72 | 41.72 |
| Polymer stock | 56.72 | 41.72 |
| Handled handguard | 36.72 | 24.72 |
| Magazine | 35.00 | 23.00 |

The final left hero's subject luma p1 / p50 / p99 is 5.00 / 50.00 / 134.72;
10.73% falls below 24, and no subject pixels clip white. Cavities, the trigger
space and the underside retain deep shadows. The native receiver/magazine
crop is 592×673 pixels, rectangle (441,94)–(1033,767) of the 1600×800 hero,
composited onto gray without resampling or contrast changes. The full gray
hero is also saved as `renders/final/beauty/hero-gray.png`.

### F final proof and media review

`make -C guns/smg check docs` completed with exit 0. This rebuilt the maps and
five exports, verified the asset and regenerated all final media. All six
4096 / 32-sample bake channels have zero missed interior rays across 5,658,237
audited pixels each. UV overlap/density, normals, dimensions, materials,
texture identity and budgets pass. The accepted position/normal/UV/weight,
rig, clip and delivery-layout fingerprints are byte-identical in all five
exports; derived export tangents are excluded as in the earlier finish checks.

Source/finalized/imported construction and all 18 contact checks pass. The
imported motion check measures 1,556 samples with zero clearance violations;
maximum penetration is 0.18721 mm against the accepted 0.2-mm tolerance.
These actual-surface checks establish clearance/contact within that tolerance.
The separate serialization check compares 1,547 affine samples, with maximum
position error 0.0000000922 m and linear error 0.0000003576. All 21 clips,
15 transitions, nine resume checks and 19 drum poses pass. Serialization
agreement alone is not treated as construction proof.

The gun remains 41,540 triangles, one material, one skinned mesh, 14 bones,
eight sockets and 21 clips. Standalone triangle counts remain 5,792 / 4,048 /
688 / 688. Gun / loaded magazine / empty magazine / cartridge / case GLBs
are 10,751,580 / 7,422,192 / 7,349,204 / 7,231,896 / 7,232,584 bytes.
All share the exact canonical 2048 BaseColor / Normal / ORM images totaling
7,189,471 PNG bytes (996,308 / 2,420,180 / 3,772,983), about 16 MiB with
8-bpp block compression and full mip chains.

Final gun SHA-256:
`5d33e553be911e07b4a17fdbd9fbbb240760114c03d6245e0971a941d487e117`.
Provenance verifies 324 render records: 320 shipping-GLB records, including
288 clip frames, and four clearly labeled dense-source photo comparisons.
Opened all 19 beauty stills, Eevee, the seven standalone/ammunition views,
four shipping photo pairs, four source pairs, the supplemental crown, all
16 clip inspection sheets, the contact sheet and all five final docs JPGs.
Reviewed the gray hero and receiver/magazine crop, native wear pair, common-span
4× chips, own-native-pixel 4× chips and the highlight comparison at full size.
The secondary abrasion is visible at the receiver crown and cap rims, well
lips, tube front and handle slot branch, hood/drum rims, and magazine spine,
lips and floor plate. Coverage falls into separate chips away from contact
stations rather than stopping at a straight mask boundary.

Final review artifacts: `renders/final/contact-sheet.jpg`,
`renders/final/beauty/hero-receiver-magazine-native.png`,
`renders/final/pairs/native-wear-pair.jpg`,
`renders/final/pairs/chips-4x-pair.png`,
`renders/final/pairs/chips-native-4x-pair.png`, and
`renders/final/pairs/paint-highlight-pair.jpg`. Numerical reports sit beside
the pairs, plus `renders/final/finish-values.json` and the delivery check
reports in `build/delivery/`. Final docs are five JPGs, at most 1600 pixels
wide and under 200 KB each. No kit changes or additional lead input are
required. A future photo-calibration helper could separate light-source
angular width from material roughness; the present comparison keeps that
uncertainty explicit.

Final lightweight verification after documentation: `python3 kit/repo_check.py`
reports 811 source files and zero errors; `python3 -m compileall -q guns/smg/src`
and `git diff --check` exit 0. `python3 guns/smg/src/finish_review.py --layout-only`
again confirms the accepted immutable data in all five exports. No kit files
were changed, so no kit regression suite is triggered by this pass.

## Paint value follow-up — diagnosis, before final calibration

**Color and value first:** the lead correctly rejected round 3's charcoal
upper flank. The earlier paint table sampled a lower flat strip between the
ribs, missing this reflection. Added actual upper-flank and grip triangle-ray
patches, plus an independent perspective-correct triangle z-buffer that measures
whole visible regions: receiver above Z112 mm with exposed-chip texels excluded,
the stock mold, and the grip plus texture panels below Z25 mm / behind Y40 mm. One-pixel erosion
excludes antialiased region boundaries. This reads finalized triangles whose
identity to the shipping triangles is independently checked; it does not use
sampled constants as measurements. The prior final hero measures upper paint
69.21, stock 53.72, grip 43.72, agreeing with the lead's full-frame diagnosis.

Review-only GLB sweeps keep all geometry, textures, lights and cameras fixed.
They override intact paint roughness and albedo in the shader without writing
an export. At albedo .002, roughness .52 / .44 / .36 / .28 / .20 gives the
fixed upper-flank patch medians 82 / 92 / 103 / 114 / 124, respectively.
The unchanged intact-crown method gives widths 10.15 / 9.81 / 9.79 / 9.81 /
9.55 mm. Even roughness .04 and albedo .0003 gives 8.81 mm, a 4.97 local
peak ratio and a sharp, recognizably rectangular reflection: reject it.
Thus lower roughness narrows the reflection but raises its peak over the
specific flank that sees the large fill card. Albedo cannot remove the
dielectric reflection. This is a measured limitation of the fixed studio
lighting, not evidence for another small roughness/albedo adjustment.

Additional review-only tests reduce only the intact paint's reflection strength;
the polymer, exposed phosphate and steel keep their prior inputs. At .42
roughness / .0015 albedo / .08 Principled specular level, whole upper paint
is 40.00 against stock 53.72 and grip 43.72 at 1400 pixels. This solves the
black-value ordering but does not establish a 4–6-mm highlight. A disposable
export probe verifies that a per-surface specular factor could share the opaque
BaseColor image's unused alpha via KHR_materials_specular, retaining one
material and three canonical images. No such extension or paint calibration
has yet been applied to delivery. The lead has been asked whether unchanged
studio lighting or the numerical 4–6-mm width takes precedence before
committing the final calibration. Raw diagnostics, masks and measurements
are in the worktree root's `build/paint-value/`.

## Paint value follow-up — paint-only exported candidate

**Color and value first:** preserve the studio lights and every camera. The
rebaked/re-imported candidate's whole visible upper receiver is **40.00**,
stock **53.72**, grip including textured panels **43.72**, against the prior
69.21 / 53.72 / 43.72. The lower intact-paint strip is 13.00, the upper-flank
triangle patch 42.00, stock patch 56.72 and grip patch 46.72. Thus both the
broad region and the off-highlight flat strip read deeper than polymer.
The other hero's upper-flank patch is 21.00 against stock 41.72 and grip
33.72. Opened the bolt rifle hero extracted read-only from `main`; this
receiver now reads black beside it and below the lead's approximately 47-luma
receiver benchmark. That benchmark is the lead's measurement, not a newly
measured constant in our check.

Paint is authored at linear RGB **.0015/.00154/.0015**, roughness **.42**
with the existing .06 microvariation, and Principled specular level **.08**.
Shipping intact medians are BC **5/5/5**, roughness **107/255 = .420**, and
glTF specular factor **41/255 = .161**, equivalent to Principled **.0804**.
Reducing reflection strength is essential here: a darker diffuse color alone
did not remove the reflected card. Lower roughness by itself brightened the
flank and eventually produced a mirror-like rectangle. This candidate retains
a soft peak, visible falloff and a black flank in both studio quarters.

The extra factor is baked using the kit's existing arbitrary BaseColor-alpha
channel, then filtered independently of RGB. The asset-local export wrapper
links it through Blender's inverse glTF factor conversion. It shares the
canonical opaque BaseColor image through `KHR_materials_specular`: still one
material, three images and the same delivery geometry/rig/animation layout.
No opacity, blend mode, extra texture image or extra material is introduced.
The verifier checks OPAQUE mode, a shared BaseColor/specular image, the image
hashes and the actual factor values. Consumers need texture support for the
existing specular extension. No toolkit code changes accompany this work.

Polymer authored roughness remains .78 / .48; its shipping lower/stock medians
remain .780 and the handled handguard .506, reaching .478. All polymer RGB,
roughness and touch fields are unchanged. The whole-part lower-mold UV audit
also includes painted details, so its raw p5 is .420 after this paint change;
that number must not be mislabeled as a new polymer endpoint. Polymer and
fully exposed phosphate/steel retain the previous glTF specular factor .56.
Mixed paint/chip boundaries interpolate their factors and roughness, as they
already interpolate color.

The source wear generator, its masks, all contact-distance fields and seeds
are unchanged. The complete shipping metallic map is byte-identical to the
accepted map, preserving the exposed-metal response pattern. Fresh bake
roundoff changes 15 normal components by one byte; AO differs at 1,559 texels
(maximum 19/255), so neither entire map is falsely claimed byte-identical.
The accepted vertex normals and all other immutable delivery data still pass
their original fingerprints. With darker paint mixed at boundary texels, the
existing color-threshold audit now reports upper-crest **54.58%**, **2.0-mm
chips / 2.5-mm gaps**, **99.18% gray / 0.82% bright**. This is a classification
change at filtered boundaries, not another wear-density calibration.

**Unresolved requirement:** the unchanged top-crown profile remains wider than
the photographs' requested 4–6 mm. The paint's value fault is corrected, but
this is not acceptance of an exact highlight-width match. The optional
lighting choice was posted to the lead; no lighting change has been made
without that direction. The numerical profiles below keep the original
method, strips, white-balance neutrals and gains, rather than changing the
measurement to manufacture a passing width.

| Fixed intact-crown method | Local median / peak, 0–255 | Peak / median | Half-excess width |
| --- | --- | ---: | ---: |
| White-balanced issued display | 80.36 / 109.39 | 1.36 | 4.40 mm |
| White-balanced studio quarter | 26.14 / 42.93 | 1.64 | 5.65 mm |
| Final shipping GLB, original top-crown view | 32.19 / 62.06 | 1.93 | 9.32 mm |

All widths are uncensored; photographic scale remains estimated. The original
white-balance neutrals remain the issued display's white selector legend and
the studio quarter's unclipped gray backdrop. The script retains the old
flat-land baselines separately. The numerical width target remains unmet,
and the local peak ratio is higher than the photos'. A narrower fill-height
diagnostic alone also failed to solve this: other studio cards still reflect
in the crown. Any lighting revision needs evaluation of the full setup rather
than a promise that one card's size will fix every view. The actual hero's
paint-value correction, by contrast, is measured on the final exported asset.

`make -C guns/smg check` exits **0**. All seven 4096 / 32-sample bake channels
cover 5,658,237 audited interior texels each with zero missed rays. Canonical
images, specular packing and opaque mode, UV overlap/density, normals, scale,
budgets, skinning and animation checks pass. Source/finalized/imported
construction/contact/clearance checks pass. The prior 18 contacts, 21 clips,
15 transitions, nine resume checks and 19 drum poses remain fixed. Imported
clearance uses 1,556 samples and retains maximum penetration 0.18721 mm against
the accepted 0.2-mm tolerance. The independent serialization comparison and
the immutable-data fingerprints pass for all five exports; those checks prove
round-trip agreement, while the actual-surface checks prove the assembly.

The first final-review attempt exposed a hard-coded overlay-color lookup that
did not recognize the new upper-flank region. Fixed the reporter's prefix
handling; also corrected an indentation error in that edit before the successful
rerun. No renderer or bake artifact was substituted. After all media generation,
`python3 src/final_review.py --docs` from this folder exits **0**, verifying
**324 current-source render records and all 288 clip frames**, and regenerating
the pairs, contact sheet and five compact docs JPGs. The generation and check
logs remain at the worktree root in `build/paint-value/`.

Budgets remain **41,540 triangles / one material / three 2048 images** for the
gun. The loaded/empty magazine and cartridge/case triangle counts remain
5,792 / 4,048 / 688 / 688. Gun GLB **11,033,396 bytes**; loaded magazine
7,704,032, empty 7,631,044, cartridge 7,513,712, case 7,514,400. Canonical
PNGs total **7,471,287 bytes**: BaseColor RGBA 1,208,055, Normal RGB 2,420,186,
ORM RGB 3,843,046. The existing 8-bpp compressed allocation remains about
16 MiB with mipmaps; alpha carries data rather than another allocation.
Gun SHA-256:
`629bda9ddda8aa0ffdbf3beb9eefe8a48272fffdf3e1b93d1b2c3d7d52bbf1d5`.

Final hero luma p1 / p50 / p99 is **1.00 / 40.72 / 130.00**, with **32.65%**
below 24 and no clipped white pixels. Deep cavities and the magazine's shaded
face remain dark; the stock and grip retain their accepted roughness response.
Review artifacts remain `renders/final/beauty/hero-gray.png`,
`renders/final/paint-value-regions.jpg`, `renders/final/paint-value-values.json`,
`renders/final/pairs/paint-highlight-pair.jpg`, the native and 4× wear pairs,
and `renders/final/contact-sheet.jpg`. No kit changes or new tools are needed.
The lead's remaining decision is whether the corrected black value and wider
highlight are acceptable under unchanged lighting, or whether to authorize
studio-light calibration toward the 4–6-mm width.

Completed full-size visual inspection of all 19 beauty stills, Eevee, all seven
standalone/ammunition views, four exported photo pairs and four source pairs,
the crown comparison, native hero crop, both 4× chip plates, wear pair, semantic
sampling overlay, all 16 clip sheets covering the 288 frames, contact sheet
and all five docs JPGs. No alpha/transparency or material-packing artifact was
found. The source, rig, clips, contacts and construction remain accepted; the
width/peak mismatch above is the unresolved finish requirement. Per the
repository's "Docs JPGs only when final" rule, the regenerated five JPGs remain
uncommitted pending that decision; scripts and the measured candidate are
recorded separately. Final docs sizes are 155,962 / 199,649 / 70,543 / 69,372 /
84,082 bytes for action / details / Eevee / hero / turnaround, all within limits.

Final lightweight checks: `python3 -m compileall -q guns/smg/src` and
`git diff --check` exit 0; `python3 kit/repo_check.py` reports 813 source files,
zero errors. No kit files changed, so this pass does not trigger kit tests.

## Receiver wear in two dimensions — diagnosis and rejected checkpoints

**Color and value first:** the lead accepts paint roughness .42, linear albedo
.0015/.00154/.0015 and shipping specular factor .161, plus the polymer values
and response. Those remain fixed. The former 4–6-mm highlight-width target is
withdrawn; the historical width tables above are diagnostic rather than an
outstanding acceptance requirement. No geometry, rig, clip, contact, camera,
light, ammunition or delivery-layout change is part of this pass.

Reopened the full gray hero, native and 4× wear pairs, `navy2.jpg` and its
(1645,245)–(2735,450) receiver crop. White balance retains the upper gun's white
selector legend: brightest 15% of (2270,535)–(2330,565), linear RGB gains
.995370/.995370/1.063568. This is an estimated neutral, not a color chart.
The continuous forward worn patch (1910,290)–(1990,323), excluding pixels below
65 luma, measures median RGB **129/119/106**, luma **120.05**. It remains warm
gray after balancing. The previous .060/.064/.061 phosphate reads too green
there. Only the new upper-land phosphate receives .058/.049/.0375; the other
accepted edge finishes retain their colors, roughness, metallic and masks.

The previous mask generated broad fractures around five crests and calibrated
one ribbon's run lengths. The new independently selected upper-land region
contained only **0.8%** visible wear in that hero, versus **40.3%** in the
photo; the conspicuous wear was elsewhere. A 2-mm median run did not establish
its location, topology or field/island relationship. Historical ribbon reports
are retained explicitly as diagnostics. They neither fit nor accept this mask.

- **A, rejected:** move broad abrasion above the upper side rib; retain thin
  lower-crest nicks and the existing secondary edge shaders. The exported hero
  now reads as one strip, but the field is too solid: 66.3% worn area,
  forward/middle/aft 100/54/44%, and one component contains all the wear. The
  initial warm phosphate is also too light: rectified worn median luma 131.92
  versus the photo's 117.64. The forward boundary is blunt. Opened the native
  hero and the 2D pair; reject despite the improved location.
- **B–C, rejected:** shorten the support-hand pressure range, fray the threshold
  with finer domain warping and taper the forward termination. C gives 39.6%
  worn area but forward/middle/aft 79/15/24%: the middle is too empty. Its main
  worn component is 59.5 ×14 mm, 593.5 mm². The photograph's is 48.5 ×14 mm,
  517 mm². Opened the full hero, binary masks and both profiles. Similar total
  coverage alone does not accept the distribution.
- **D–E, rejected:** add a weaker, broader hand-pressure falloff through the
  middle; reduce and warm the upper-land phosphate. D's observed RGB is
  127/118/104 versus 125/117/105 in the rectified photograph, with median luma
  118.97/117.64. Its coverage is still too heavy at 46.1%. E reduces this to
  43.0%, but a thin gray bridge joins 102.5 mm into one component, containing
  87.7% of the wear. Reject that connectivity, visible in the 2D classification.
- **F–G, rejected at the final 4× review:** add secondary fractures entering from
  the upper margin and large intact lobes which interrupt gray bridges. G's
  main field is 51.5 ×14 mm, about 603 mm², with 42.2% total wear. The hero's
  black lower flats and single rubbed strip now read correctly. However, the
  secondary 12-mm noise correlation produces several long wormlike marks,
  and the continuous forward phosphate is too smooth. In an independently
  fixed forward 2D patch, adjacent-pixel median absolute luma differences are
  0 versus 4 in the photo. Do not let the improved component sizes certify
  those remaining visual faults. Opened every 64-sample beauty view, Eevee,
  the native/4× pair and shipping photo pairs before this last correction.

**H, final refinement:** shorten the secondary fracture correlation to
2.2 ×4.8 mm, retaining the coarse 17 ×10-mm paint structure, independently
warped smaller scales, causal hand/well pressure and distance below the upper
crest. Keep sparse thin nicks below the rib. Add intrinsic porous-coating color
grain only inside this exposed field, with a nominal unit-mean multiplier;
this is manufactured substrate variation, not extra randomly scattered wear.
Its hue, central value, metallic .08, roughness .88 and rare steel treatment
remain controlled separately. The source generator reads no photograph.

The early diagnostic render commands incorrectly overrode the inherited GPU
lock with a worktree-local path. Corrected that before the final bake/media
commands; subsequent GPU work uses the inherited shared lock. All bakes use
the Makefile's shared-lock wrapper. Scratch comparisons and command logs are
under the worktree's ignored `build/smg-wear2d/`.

### H final 2D evidence and color

The final comparison uses a **311 ×28 grid at 0.5 mm per cell**, spanning
155.5 ×14 mm, forward at left. Hero sample points intersect the actual accepted
receiver triangles, then project through the unchanged hero camera into the
exported GLB's 64-sample render. The photo is independently rectified with a
projective homography through (1900,284), (2638,271), (2638,332), (1900,350).
Its front edge is 66 pixels / (1090 pixels /230 mm) = **13.93 mm**, rounded to
14 mm within reference-scale uncertainty; the homography corrects the receding
61-pixel aft edge. Its four corner projections agree within 1e-8 pixels.
This assumes a planar rectangular photographic land and an approximate 230-mm
receiver envelope. It is an explicit scale estimate, not recovered engineering.
The earlier checkpoint numbers used bilinear quadrilateral sampling; this
projective correction changes the photo's measured area from 40.3% to 38.9%.

Both color images are sampled bilinearly onto that same physical grid, then
classified at display luma >65. There is no closing, speck removal, run filter
or contrast change. Worn components use eight neighbors; paint uses four.
Every component retains its area, bounding length/height and boundary-censoring
flags. A clipped region is not reported as a complete island. The full lists,
area histograms and threshold sensitivity are in `wear-2d-values.json`.

| 2D observed worn area | Exported hero | White-balanced photo |
| --- | ---: | ---: |
| Entire selected upper land | 40.16% | 38.91% |
| Forward third | 83.21% | 74.11% |
| Middle third | 26.55% | 24.48% |
| Aft third | 10.44% | 17.93% |
| Top height quarter | 69.55% | 54.71% |
| Second quarter | 40.70% | 44.10% |
| Third quarter | 31.10% | 28.07% |
| Bottom quarter | 19.29% | 28.76% |

| Connected region, area / bounding length ×height | Exported hero | Photo |
| --- | --- | --- |
| Largest worn field, boundary-clipped | 603.75 mm² / 51.5 ×14 mm | 487.00 mm² / 46.0 ×14 mm |
| Second worn region, boundary-clipped | 79.25 mm² / 23.5 ×7.5 mm | 156.25 mm² / 44.5 ×12.5 mm |
| Third worn region | 55.25 mm² / 15.5 ×6.5 mm, clipped | 29.50 mm² / 11.5 ×6.0 mm, complete |
| Largest intact paint region, boundary-clipped | 1,285.50 mm² / 128.5 ×14 mm | 1,292.00 mm² / 128.5 ×14 mm |
| Second paint region, boundary-clipped | 11.25 mm² / 6.0 ×4.5 mm | 12.50 mm² / 1.0 ×14 mm |
| Third paint region, boundary-clipped | 2.50 mm² / 4.0 ×1.0 mm | 4.50 mm² / 3.0 ×2.5 mm |

The hero has 25 worn components, ten complete; the photo 89, 43 complete.
The largest contains **69.06% /57.50%** of each image's wear. Paint has
11 /36 connected regions, including **4 /29 enclosed islands**. Most intact
paint belongs to a large region connected along the lower margin in both
images; visible 5–30-mm lobes must not be falsely counted as separate closed
islands. The component tables expose the distinction the previous 1D check
could not. At thresholds 55/60/70/75, hero worn shares are
43.35/41.66/38.77/37.62%; photo 42.34/40.61/36.92/35.16%.

Observed worn medians are **RGB 126.31/117.01/104.51**, luma **118.11**, versus
**124.98/116.59/105.15**, luma **117.59**, in the rectified photo. Their hues
remain warm gray under the stated neutral. A fixed continuous forward patch
has adjacent-pixel median absolute luma differences **2.68 /3.49**, standard
deviations **6.07 /10.13**. This is a separate coating-grain diagnostic, not
a wear-pattern acceptance profile or an albedo inversion. Source light,
photographic noise, editing and atlas filtering remain confounders.

The full-height receiver comparison measures **1.54%** visible worn area below
Z109 mm; the broad lower flats are black, with thin crest nicks. The final
hero on gray reads as black paint with one rubbed upper strip. Its independently
segmented intact upper receiver is **39.00** luma, stock **53.72**, grip
**43.72**. The old upper-flank four-point patch now includes the rubbed field
and measures 86.13; it is not an intact-paint value. No material or lighting
adjustment was used to darken the black region in this pass.

**Remaining photographic differences:** the forward field is fuller, the aft
bites are sparser, and small enclosed islands are fewer than in the photo.
The smaller secondary gray regions do not reproduce its largest lacy network.
The finest lace and grain soften at 2048. The photo's upper seam/glints and
our curved original land also differ in projection. Similar total area is not
claimed as proof of identical morphology, and these differences remain visible
in the masks, height profile and native/4× pairs. The delivered structure has
changed from three uniform speckled bands to one forward merged field, large
intact middle lobes and edge-entering aft bites; it does not copy an individual
photograph's scratch history.

### H preservation and delivery checks

`make -C guns/smg check` completed with exit 0 on the final export. All five
accepted position/normal/UV/weight, rig/clip and node/accessor-layout
fingerprints match; exporter-derived tangent frames remain excluded as in the
accepted baseline. Source, finalized and re-imported construction pass all
18 actual-surface contact assertions. The imported motion sweep has 1,556
samples, zero violations and maximum penetration **0.18721 mm** against the
existing 0.20-mm tolerance. All 21 clips, 15 transitions, nine resume checks
and the 19-pose inclined drum sweep pass. The independent serialization check
has 1,547 affine samples, maximum position delta 9.216e-8 m and linear delta
3.576e-7. Serialization agreement is separate from construction correctness.

All seven 4096 /32-sample bake channels audit 5,658,237 interior texels each
with zero missed rays. UV overlap/density, winding/normals, scale, skin weights,
materials, texture identity and budgets pass. Actual intact paint is BC
**5/5/5**, roughness **107/255 = .420**, specular **41/255 = .161**. Lower/stock
polymer medians remain BC 29/30/29, roughness .780 and specular .561; handled
handguard roughness .506 reaches .478. The raw lower-mold UV audit still
includes painted details in its .420 lower tail; that is not a polymer change.
Classified gray phosphate has median BC 65/61/54, roughness .859, metallic
.078 after filtering. Exterior worn texels are **98.95% gray /1.05% bright**
(16,928 /180); rare filtered steel cores are not mislabeled as pure-metal texels.

No accepted secondary edge shader or polymer input changed. An independent
shipping-pixel comparison with the handed-off maps finds only 141 nonreceiver
interior texels changing by more than one byte: three at the handguard's rear
Y189.92–190.14 mm join, 42 at the lower's Z73.88–73.91 mm rim, and 96 at the
well/receiver Z73.94–74.67 mm contact. These are receiver-source projection
changes at touching surfaces, not new well-lip or polymer wear. The well lip at
Z38.6 mm and specified tube, hood, drum and magazine edge shader inputs remain
unchanged. Do not claim the complete nonreceiver images are byte-identical.
Actual barycentric position ranges are in the ignored preservation report.

Both complete 4096 ×1172 ×3 source mask arrays were regenerated independently
and compare byte for byte. Array SHA-256:
left `4c619f326c84ac88bef2f2e4d70fd90cf5f088baca61b4c0b32d13e7758ee289`,
right `d83a14f4c54fc98734b157e2f1027177d09535ba0f8854e24a72f545c94ae7cf`.
The reproducibility, preservation and command logs are under root
`build/smg-wear2d/`; the primary rebuildable image/data evidence is under the
asset's `renders/final/pairs/`.

The gun remains **41,540 triangles**, one material, 14 bones, eight sockets
and 21 clips. Loaded/empty magazine and cartridge/case remain
**5,792 /4,048 /688 /688** triangles. Gun GLB **10,879,252 bytes**; loaded
7,549,888, empty 7,476,900, cartridge 7,359,568, case 7,360,256. All embed the
same three **2048** images, totaling **7,317,144 PNG bytes**: BaseColor
1,140,711, Normal 2,413,887, ORM 3,762,546. Compressed allocation remains about
16 MiB with full mip chains and canonical texture reuse. Final gun SHA-256:
`11e9649956b6b2e16d608bcc60e10d38c729b8b0afb4808201f143207656242a`.

No kit or common files changed. No tool or lead input is needed. A future
part-aware projection option could prevent the tiny shared-coordinate contact
texel swaps; the current task keeps the accepted delivery pipeline intact.

### H final media and documentation

`make -C guns/smg docs` completed with exit 0 after resuming an interrupted
media batch. Final review verifies **324 source-verified renders**, including
all **288 clip frames**, and audits the 21 animated WebPs against their actual
clip durations. Finals, shipping/source photo pairs, common-scale and native
4× wear comparisons, native wear pair, standalone ammunition views and the
contact sheet were regenerated and visually inspected. The exported hero's
subject luma p1/median/p99 is **1.00 /39.72 /133.56**; **35.25%** is below 24,
with no white clipping. Cavities remain dark and the worn field remains matte.

The old crown highlight probe crosses the new rubbed strip. It is explicitly
marked **mixed paint and wear**, with intact-paint width unavailable, rather
than reporting its mixed-surface width as a paint measurement. The owner
withdrew the width target; no material value was adjusted to fit this probe.
`python3 guns/smg/src/final_review.py --docs` then completed with exit 0 and
regenerated the corrected charts, contact sheet and five final documentation
JPGs. Their byte sizes are hero **67,296**, turnaround **83,992**, details
**192,704**, action **154,713**, Eevee **68,758**, all within 1600 px and 200 KB.

Primary evidence is `renders/final/beauty/hero-gray.png`,
`renders/final/pairs/wear-2d-pair.jpg` (binary masks, connected regions,
physical sizes and both profiles), `wear-2d-values.json` (complete tables),
`wear-2d-height-context.jpg`, `chips-4x-pair.jpg`,
`chips-native-4x-pair.png`, `native-wear-pair.jpg`, and
`renders/final/contact-sheet.jpg`. The scripts rebuild this evidence; generated
PNGs, JSON, GLBs and textures remain ignored. Final repository and Python
syntax checks pass; only scripts, README/review text and final docs JPGs are
committed.

## README signature GIF — 2026-10-30

Color/value first: compared with `docs/hero.jpg` and `docs/eevee.jpg`.
Painted steel remains black, the polymer is a quieter gray-black, and the
warm worn strip across the receiver keeps its accepted color. Broad highlights
roll off without making the gun pale. Direct Eevee has less indirect cavity
light than the Cycles hero; baked maps, studio and AgX response are retained.

Chose **ReloadEmpty** for the nonreciprocating charging handle's draw/lock,
magazine exchange and final release/slap. Fire would show much less external
motion. The left-side quarter keeps the handle visible and leaves room under
the mag well, with the complete silhouette recognizable. Inspected every
decoded frame and the native handle/magazine pages: the handle locks before
the exchange, the replacement magazine seats, then the handle releases near
the end. Brass is small at the magazine top but distinct before insertion;
this reload contains no fired-case ejection. The final 960-pixel version fits
without trimming, a frame-rate reduction or a palette reduction.

Camera in meters: location **(-0.92, 0.48, 0.35)**, target
**(0, 0.08, -0.02)**, **50 mm**, aspect **1.85**,
roll **0 rad**, exposure **-0.15**. Flat background
RGB **(108, 111, 114)**. Final studio, embedded GLB maps, 64-sample
Eevee and one discarded initialization render; screen raytracing is disabled.

Frame/palette review: **70 decoded frames**, numbered
**000–069**, checked in the complete contact sheet and native
frame pages. No objectionable palette flicker, steel banding or dither noise
appeared in the sequence. One global palette and no dithering keep the
background corner exactly constant in every frame. Quantization audit:
**0.051/255** mean RGB error; worst full-frame 99th
percentile **1/255**. This measures palette loss,
not mechanism correctness.

Timing audit: **960×519**, **20 Hz**,
**249 distinct palette entries** (allocation 256),
**300,968 bytes**. Source samples at 60 Hz: **ReloadEmpty 0, 3, …, 207**.
Motion samples have **50 ms** delays, with **500 ms** added only
to the first delay; decoded loop duration is **4,000 ms**.
Two complete `make gif` runs returned identical shipped bytes. The documented
recipe fingerprint and per-frame numeric comparison retain the approved GIF
only for negligible GPU rounding; fresh candidates are retained for inspection.

Evidence stays under `build/gif/`: `report.json`, `palette-audit.json`,
`contact-sheet.jpg`, `review/frames-*.jpg`, full PNGs and `candidate.gif`.
`playback.html` provides the continuous authored-speed loop. This headless
review inspected decoded frames and audited real-speed delays; continuous
visual playback was unavailable in this session. The committed image is
`docs/motion.gif`; the README names the clip below it.


## Family paint correction — pass 1: accepted export and reference audit

**Color and value first:** opened the accepted exported locked view, issued
photograph and existing studio quarter reference. The inherited issued target
is V10/50/90 **4/8/64 against 0/15/143**, highlight RGB
**90/84/75 against 174/168/160**. It is an exhibition photograph, not studio
lighting. Retain it as an explicit diagnostic and use `right.jpg` as the primary
studio receiver comparison. The latter's unclipped pale-gray backdrop
(1300,100)–(1500,350) is neutral; the issued comparison retains the brightest
15% of the upper gun's white selector legend (2270,535)–(2330,565).
The independent complete receiver polygon excludes the polymer/tube; it is
fixed before fitting. Its studio target is V **2/21/42**, highlight
**52.63/54.46/49.62**. Different wear histories remain visible in the pair.
Accepted exports/maps were archived in root `build/family-paint/before/smg/`.

## Family paint correction — pass 2: reject old-light material compensation

**Color and value first:** opened the whole-receiver studio crop and both
reference photos. The initial LMG paint (.022/.023/.024, factor .8, roughness
.42) under the old photo lights gives V **37/57/82**, highlight **94/89/82**.
A .20-factor/.32-roughness diagnostic remains **30/46/71**, highlight
**93/87/79**. Neither matches the dark studio distribution; the accepted warm
phosphate patch is also more extensive than on the studio specimen. Keep
that wear rather than changing its area to fit a histogram. Restore physical
dielectric reflection and calibrate one whole-scene light rig per photograph.
The subsequent paint keeps 2.2–2.4% diffuse reflectance and tries .29 roughness
for the studio's tighter satin reflection. Magazine oxide keeps its old inputs;
all substrate, steel, polymer and ammunition mixes and every wear field stay.


### Pass 3 spatial audit — reject the first numerical match

**Color and value first:** the first fresh exported whole-part fit passed its
percentile/highlight bounds, but opening the pairs exposed a reflection on the
wrong flat. Do not accept numerical agreement alone. The studio observation
also mistakenly omitted the receiver's rolled roof behind the cocking tube.
Corrected the complete visible-part outline, including that roof and excluding
the occluding rear-sight base, before refitting. The studio target is now
V **2/24/46**, highlight RGB **59.77/61.03/57.93**. The previous 2/21/42
selection above is retained as rejected evidence, not the final target.

Added broad upper/lower value guards, divided at physical Z109 mm and located
on the reference with the existing calibrated projection. Narrow physical
cards are sampled along the actual crown reflection directions. There is still
one whole-scene physical rig for each photograph; no image grading, per-part
light linking or changed paint/wear is involved. The issued comparison retains
the inherited full-part polygon and method so its original numbers remain
comparable. Model and photographic pressings differ; spatial guards are
reported separately from the required complete-part distribution.


### Paint-role scope correction

**Color and value first:** the .29/.42/.55 roughness and 3.5%-albedo diagnostics
were inspected as physical-light response studies. The broader and lighter
alternatives did not improve the complete-part/spatial fit; retain 2.2–2.4%
diffuse enamel, .29 central roughness and .8 specular factor for the next actual
bake. The current full-part .29 GLB measures V **2/23/40** against **2/24/46**,
highlight **64.12/62.50/62.87** against **59.77/61.03/57.93**. The retained
issued diagnostic is **0/15/150** against **0/15/143**, highlight
**170.86/166.72/162.06** against **173.68/167.95/159.84**. All requested full-part
bounds pass; the broad upper/lower spatial medians remain a weaker match and
are not certified by that pass. The original pressing/camera alignment and
accepted wear differ from this cleaner studio specimen.

The role audit caught a separate scope fault in the prototypes: `steel()` also
serves `darksteel` slots. Restrict the new BRDF to the explicit inspection
`paint` role (plus the already-painted handle pad), still excluding Magazine_*
parts. Barrel, post, rear sight hardware, releases and other dark steel retain
their old inputs. Bright steel, magazine oxide, polymer, ammunition, every wear
field and the entire rig/layout stay fixed. Repeat the actual bake/export and
photographic gates after this correction; the prototype figures above are not
the final delivery proof. Pure-alpha pixel cohorts alone could not establish
this scope because old paint and old dark steel shared the same alpha factor.


### Reviewed paint baseline and first clean build

The actual role-corrected export is
`168665169a6df2961cfc3d1442f6dc6b656a7e05c7cf2a9e22257496c4a2f3b5`,
replacing the handed-off fresh bake
`55ec8e8ec04f2d7503db7822d9ef409fd7c57266a9a71aeeefa569b278e843ce`.
The older historical acceptance was
`11e9649956b6b2e16d608bcc60e10d38c729b8b0afb4808201f143207656242a`.
`src/accepted_paint.json` deliberately records the reviewed change and its
old/new identities. The old specular interval .14–.19 moves to .775–.825:
its width stays .05. The new intact-paint RGB median is pinned at 41/42/43
with a one-byte component bound. Geometry/layout/detachable baselines and
all motion/contact tolerances remain unchanged.

Both original receiver fracture arrays remain byte-identical after clean
regeneration: left
`4c619f326c84ac88bef2f2e4d70fd90cf5f088baca61b4c0b32d13e7758ee289`, right
`d83a14f4c54fc98734b157e2f1027177d09535ba0f8854e24a72f545c94ae7cf`.
The source-role correction changes only the intact enamel path; polymer,
ammunition and all weathering functions remain identical. The first empty
build's `make export` and separate `make check` both pass; full command/status
records are root `build/family-paint/smg-clean1-*.json`.

### Whole-photo lighting anchor and limits

The final optional fit also observes the complete unchanged studio handguard
as an illumination anchor. This prevents claiming that a favorable paint
histogram alone recovers the photograph's light. With the original handguard
material frozen, the best sampled estimate remains roughly 17 median V against
71 in that edited studio photo. Upper/lower receiver medians also remain a
weaker spatial match than the whole-part values. The final recipe retains the
best constrained whole-part fit, not a claim that these secondary observations
pass. The photographic pressing, camera residual and accepted wear differ;
no polymer, wear or geometry input is changed to hide that mismatch. These
limits remain in the final audit's `height_guards` and
`unchanged_finish_anchors` fields. Whole-receiver acceptance is tested again on
the second clean, role-corrected export; there is no image-space correction.

### Final GIF review — unchanged signature motion

**Color and value first:** opened all nine decoded GIF pages in
`build/gif/review/frames-*.jpg`, every frame **000–069** in order. The intact
paint remains charcoal under the unchanged studio, with a tighter satin line;
the accepted warm phosphate ribbon, black polymer and dark oxide magazine stay
distinct. Frames 000–023 retract and lock the handle; 024–033 withdraw the
magazine, 034–048 return/seat it, and 049–069 release and settle the action.
The magazine briefly crosses the lower image edge at maximum withdrawal,
as in the original accepted camera/clip. No new flash, missing part or paint
palette jump appears. Fine surface detail is softer in the GIF than the JPGs.
The review uses decoded frames and measured delays, not interactive playback.

`make gif` passes: **960×519**, **70 frames**, **20 Hz**, **249 palette colors**,
**306,046 bytes**, **4,000 ms** including the unchanged 500-ms first-frame hold.
The `ReloadEmpty` samples 0,3,…,207 and `src/gif.json` remain identical.
GIF SHA-256: `2cf5d434e60a71f67c1288d834195e3ec5c8b372c3a3dba0b1d4a271cf8c739f`.

### Final exported paint and docs critique

**Color and value first:** opened the two full histogram pairs, controlled
before/after triptychs and native final hero. The actual second clean export
measures studio V10/50/90 **2/23/40** against **2/24/46**, highlight RGB
**65.27/64.32/63.26** against **59.77/61.03/57.93**. The issued diagnostic is
**0/15/150** against **0/15/143**, highlight **170.81/166.67/162.00** against
**173.68/167.95/159.84**. All requested full-part bounds pass, including
highlight value, every RGB channel and normalized color. Source preview
measures studio **2/22/40**, **65.27/64.34/63.27**, and issued **0/15/149**,
**171.05/166.95/162.28**: broad response survives baking.

Holding the final physical lights/camera fixed, the old GLB measures studio
**0/2/18**, **31.83/30.52/28.81**, and issued **0/4/91**,
**112.83/107.72/101.81**. This is distinct from the inherited old-light result
4/8/64, 90/84/75. Complete polygons include the accepted wear; neither a paint
threshold nor an altered wear field selects a favorable subset.

The spatial weakness remains clear in the pair: upper/lower receiver medians
are **11/27** versus **30/16**. The unchanged handguard anchor is **16** versus
**71**. These are failed secondary observations, not a fully recovered studio
or spatial photo match. Different accepted pressing geometry, camera residual,
wear and other frozen finishes limit the fit. The physical rig is an estimated
comparison condition; no image grading or local light linking is used.

Opened every final docs JPG at native size. `hero.jpg` has charcoal paint,
a distinct warm worn ribbon and deep handle/port shadows; the reflection
remains smoother than the photograph. `turnaround.jpg` retains the original
rolled profile, deep muzzle and black magazine. `details.jpg` preserves the
accepted ribbon lobes, exposed edges and molded lower; the drum/hood faceting
and softened microtexture remain existing limits. `action.jpg` retains the
locked handle and sight channel, black oxide magazine and brass/copper
separation; the soft normal-only headstamp remains weak. `eevee.jpg` agrees
with the Cycles finish order and keeps cavity depth.

Hero luma P1/50/99 is **2.79/53.72/185.07**, with **18.49%** below 24;
reverse is **1.00/39.72/185.79**, **23.75%** below 24. Neither clips white.
The new .29 paint reflects a narrower satin line than the Rill's .42; both
read in the same charcoal family beside the unchanged Harrow in
`../lmg/renders/final/hero-beside-ak-smg.jpg`, opened for this review.

### Final artifact inventory

| Docs file | Pixels | Bytes |
| --- | --- | ---: |
| `docs/action.jpg` | 1244×1400 | 154,477 |
| `docs/details.jpg` | 1204×1400 | 193,527 |
| `docs/eevee.jpg` | 1600×800 | 67,268 |
| `docs/hero.jpg` | 1600×800 | 65,523 |
| `docs/motion.gif` | 960×519 | 306,046 |
| `docs/turnaround.jpg` | 1600×1300 | 82,697 |

All five JPGs and all seventy GIF frames were opened; the observations above
refer to these final files. The generated final contact sheet is
`renders/final/contact-sheet.jpg`, with Cycles/Eevee stills, exported/photo
pairs and motion strips. Current full GLB SHA-256: `290b044c70d6319bbf4418d4f7f21e633ddb12741d1609aa03040b2ddec2b074`.

Opened all 36 non-clip final renders on six indexed pages, all sixteen clip
pages (`inspection/clips-00.jpg`–`clips-15.jpg`, 288 samples), all four final
photo pairs and four source companions, and the contact sheet. Paint stays
stable across the motion samples. Also opened the rejected broad-roughness and
lighter-albedo response sheets, and both final unit-card response sheets;
these +4 EV unit-card diagnostics are labeled and never accept the shipping
BRDF. The whole-part match and the failed spatial/handguard anchors remain
visible together rather than silently dropping the unfavorable observations.

The UV-interior scope audit is root
`build/family-paint/smg-scope-part-deltas.json`. Original same-bone projection
contacts carry changed paint onto nominally nonpaint low surfaces: chamber
seat 41 texels, barrel 2,298, handle hinge 10, front post 25, rear base 448,
clamp ears 35/34, rear bearing 183, handguard 281 and lower molding 21,084
BaseColor texels change by more than one byte. These are not proof of a source
polymer/darksteel change; the source role audit preserves those shader inputs.
They are an existing projection limitation, so this report does not claim
pixel-identical other-finish atlases. Geometry, UVs and the bake isolation
layout were not changed to conceal it.

### Two clean-build checks and preservation proof

Cycle 1: `make -C guns/smg clean`, `make -C guns/smg export` (**0**, 319.52 s),
then `make -C guns/smg check` (**0**, 360.50 s). Passing reports, actual export,
textures and comparison evidence are archived in root
`build/family-paint/smg-clean1/`; command/status records are
`smg-clean1-*.json`. Cycle 2 independently removed all generated asset outputs,
then ran the requested default `make -C guns/smg` (**0**, 1,315.71 s) and
separate `make -C guns/smg check` (**0**, 236.70 s). Both cycles bake **4096 /
32 samples**, ship **2048**, and report zero missed interior bake texels.
All Cycles work used the shared GPU lock. `make gif` also returns zero.

The original geometry/layout signatures and every geometry/motion/contact
bound remain unchanged. Source, finalized and freshly imported construction,
actual-surface clearances, gun UV/weights/rig/clips identity, standalone
oriented geometry/normals/origins, inverse atlas samples, full density and
protected-mip bleed all pass. Identity proves preservation; construction and
clearance tests independently prove assembly behavior. The two clean bakes
have identical BaseColor; only **13 Normal and 8 ORM texels** differ, by at
most one byte/channel. The final gun stays **41,540 triangles / one material /
three 2048 maps / 10,984,144 bytes**. The accepted fracture-array hashes are
also enforced exactly by `wear_audit.py`. No kit code changed.

The deliberate paint acceptance uses the same .05-wide specular interval at
its new center, plus the new one-byte RGB-median pin. Neither a geometry
signature nor a tolerance was relaxed. Final `python3 kit/repo_check.py`
passes with zero errors; `git diff --check` passes. Shared photographic-bound
unit tests pass (three), as do the rifle's bake/rebaseline tests (18).


## Paint round 2 — pass 1: reject the circular light fit

**Color and value first:** the f95dac1 docs hero is gray rather than black.
Opened the original docs heroes, the Harrow hero, both neutral-balanced studio
photos, the anchor outlines and all four initial Harrow-lit previews per gun
in root `build/paint-round2/studio-smg/`. The five area fixtures now use
the Harrow locations, sizes and energies (18/4/13/5/5 W), and its .045 world
strength. Camera, exposure, backdrop color and GIF camera are retained.
The inherited studio's 35/15 W key/fill is rejected.

The photographic light objective now contains only independently selected
unchanged finishes and a physically illuminated neutral backing. Receiver
pixels, tails, median, highlight and height guards never enter that objective.
The first independent fit fails multiple anchors; its old paint-only match
is not material evidence. Expanded card bases, surface-matched region checks
and fresh Cycles comparisons are required before accepting any sheen.

The source-attribution control now perturbs only the enamel's diffuse RGB,
using the same 4096/32-sample kit bake and 2048 downsample. The corrected
projection gives **zero** changed BaseColor interior texels on the nominal
nonpaint surfaces (including the Relay lower/barrel and Rill rear insert).
The full per-part control deltas are in root `build/paint-round2/smg-projection-control-deltas.json`. Repaired texels can differ from the old
contaminated bake; that repair delta is reported separately from paint leakage.

Inspecting the unit-world basis found an unintended default area light at
the origin on its first frame. That basis is rejected and rerendered with
zero area-light energy. Every subsequent response render asserts its exact
active fixture set and records the world strength. The older lighting fits
are investigation evidence only, never accepted material measurements.

## Round 2 reviewed projection baseline

Reason (explicit reviewed command): Round 2: isolate enamel projection from adjacent accepted finishes; no geometry, UV, rig, clip, wear-mask or authored finish change.

The actual `f95dac1` GLB SHA-256 is `290b044c70d6319bbf4418d4f7f21e633ddb12741d1609aa03040b2ddec2b074`. Its tracked acceptance journal records `168665169a6df2961cfc3d1442f6dc6b656a7e05c7cf2a9e22257496c4a2f3b5` (the earlier reviewed bake, with bounded sparse GPU rounding accepted at handoff). The old manifest SHA-256 is `82afa5c72949d9b4e7037534bf2f88c643f6c658f90463532bd5d8ce917bcab6`. The reviewed projection-corrected GLB is `2c2643de76361b88319d5a42429be5ad7bd93fddc02b34a247649dd41a28744b`. The actual handoff and the earlier journal hash are separate facts.

This acceptance records the projection correction only. It does **not** approve the unresolved photographic paint fit. The SMG’s exact accepted geometry/layout signatures, wear-mask hashes,
specular interval and 1-byte median BaseColor bound are unchanged. The
1-byte / 128-texel full-image rounding journal belongs to the AK; this SMG
manifest does not claim that full-image test.

### Reference and basis investigation

The old gray-background quarter image is digitally isolated. Its original
Commons upload retains the real gray table and colored cloth, so the physical
neutral is now the table `(1300,970)–(1480,1080)`. The inherited form camera is
preserved; a separate paint shot uses the original photo's same pixel geometry.
A candidate fixed-stock studio image was rejected because its clipped/possibly
isolated white backing cannot constrain illumination.

The table/cloth in both selected views lies behind a gun laid on its side.
Correcting the backing plane substantially improves the issued handguard fit,
but does not produce a complete accepted calibration. The red cloth is not
treated as a neutral; the issued white-balance constraint remains the brightest
selector-legend pixels. Original source-array wear and all other finishes are
retained. Outside-surface anchor masks exclude the handguard's inner channel;
all eight studio and all six issued anchors remain in the objective. The grip
photo polygon was inset to remove yellow flag slivers, rather than treating
those pixels as polymer color.

All light cards affect the whole scene. No receiver observation enters the
light objective. The fits are explicitly **rejected**; no new sheen is claimed.
Fixed-light trials (.02–.58 roughness, .2–.8 glTF specular factors) do not pass
the complete receiver tests. The clean studio specimen also lacks the accepted
asset's broad worn upper field, leaving a large upper-tail/highlight difference.
Round 2 therefore retains the authored .022/.023/.024, .29 and .8 inputs.

### Actual handoff and current shipping-map hashes

These are hashes of the actual `f95dac1` files, not the older reviewed journal. The current files include the reviewed projection repair. PNG byte hashes describe compression; decoded hashes describe texels.

| Map | f95dac1 PNG SHA-256 | f95dac1 decoded SHA-256 | Current decoded SHA-256 |
| --- | --- | --- | --- |
| T_Relay9_BaseColor | `7628aeffb8294fb274c3e91fd95ecac4b9019df3777ec8b8eca13bda1b717b4d` | `783183861ed890c8601fc00870d0339966448dcb92e3230ec0252f6157e33569` | `ad9a7bb32edbd58c1a17002871e77363fd70ebd564c6f63434bf8fb1fdbc40a5` |
| T_Relay9_Normal | `b00a609eb439bea711e55e9480cab42c574704a98fdda66a396bbe1220e6ee95` | `a31fb7d79488ed2d53f70556cff7879ac6f71364ddb105e6572ad71c89650536` | `1e688581e3c6a9d094fd93f3217935b00bf5829f7a2e9f5cd5edc656bfb81fba` |
| T_Relay9_ORM | `df322ebfb23b8dc5881d69223b6daf461640f27fcf643dca58e6870be531138d` | `84acf8aacf8c1d27237222aba2e304d05da0657b685bbca321acc448fe534bf8` | `3be771e61c6aee4fc467674bb8ff27d9b604f7a9563b335b27128059ce5ec196` |

Current actual GLB SHA-256: `c5dfb18ab711c8315163bbb2ee3f0a01e536386807fbc9d5c560c7fe817b0582`. Sparse bounded GPU rounding can make this differ from the explicitly reviewed bake; the original byte/texel limits remain unchanged.


<!-- ROUND2_PAIRS_START -->
## Paint round 2 — pass 2: independent pairs remain rejected

**Color and value first:** the fresh GLB/photo pairs fail visibly. The held-out
receiver measurements below are observations, never light-fitting inputs.
No new sheen is accepted. Authored enamel remains linear .022/.023/.024,
roughness .29, Principled specular .4 / glTF factor .8, dielectric.
The source shaders, all other finishes and all wear masks retain the handoff inputs.

In `pairs/paint_studio_photo-pair.jpg`, handguard median is much closer
than in the circular handoff fit, but bright polymer highlights remain wrong;
the receiver and muzzle still look silver beside the black photographed gun.
The clean specimen lacks the accepted broad worn upper field. Whole-receiver
tails retain that wear; an intact dark patch cannot stand in for the assembly.
Both issued comparisons remain: the inherited `locked_photo` camera, and the
new `paint_issued_photo` observed-direction test (60.4 px landmark RMS).
The latter shows more of the grip but is still a camera hypothesis, not
form approval. Both retain all six nonpaint anchors. Their fresh images are
severely overlit, while the reference receiver has black paint between wear.
The accepted barrel is very dark dielectric oxide (linear approximately
.0015, roughness .42, glTF specular factor .16 plus carbon), while the
photographed muzzle is bright. The tested rigs cannot raise it sufficiently
without bleaching other surfaces. This diagnoses an unresolved reference /
accepted-finish / illumination conflict; it does not prove a new paint BRDF.
No barrel or polymer input is changed.

Studio WB uses actual gray table `(1300,970)–(1480,1080)`, observed RGB
152/155/159, gains 1.038932/.995225/.940897. Issued WB uses the brightest
white selector-legend pixels `(2270,535)–(2330,565)`, RGB 243/243/236,
gains .995370/.995370/1.063568. The red cloth is not a neutral or exposure
anchor. Its albedo and backing plane are explicit comparison assumptions.

The light objective contains only unchanged-finish anchors and neutral
constraints. All active card energies are nonnegative; every card illuminates
the whole scene. There is no light linking, per-part gain or image grading.
The broad-only basis (world + 16 cards), nonpaint-derived reflection cards,
corrected backing plane and native 1600-pixel responses were also tested.
The last observed-direction native basis has 27 entries.
All these fits remain rejected. Unit responses were opened in normalized
contact pages; the normalization is for inspecting those diagnostics only.
The actual pairs below are fresh Cycles renders at 1600 px / 64 samples.
Their values, rather than lower-resolution optimizer predictions, govern review.

The same strict full comparison bands are applied to nonpaint anchors as a
conservative calibration gate. Paint bounds remain median ±10%, P10/P90 ±15%,
and highlight value, RGB and normalized color ±10%. Zero photo tails require
zero. The failed independent gate stops `make paint-review` before any claim
of paint acceptance. No tolerance or geometry check has been weakened.

### studio_receiver — `paint_studio_photo`

GLB source SHA-256: `c5dfb18ab711c8315163bbb2ee3f0a01e536386807fbc9d5c560c7fe817b0582`. Independent light accepted: **no**.
Pair: `renders/final/pairs/paint_studio_photo-pair.jpg`; full paint and every anchor’s
error/color data: `renders/final/paint-review/finish-values.json`.
Histogram: `renders/final/paint-review/studio_receiver-histograms.jpg`.

| Held-out paint | Render | Balanced photo |
| --- | --- | --- |
| V P10/median/P90 | 21.0/44.0/113.0 | 8.0/14.0/24.0 |
| Brightest-decile RGB | 160.6/164.7/161.6 | 32.3/32.1/27.5 |
| Highlight V | 164.7 | 32.3 |
| Highlight normalized RGB | 0.975/1.000/0.981 | 1.000/0.993/0.849 |

| Independent anchor | Render V P10/median/P90 | Photo V P10/median/P90 | Render highlight RGB | Photo highlight RGB | All bounds pass |
| --- | --- | --- | --- | --- | --- |
| handguard | 27.0/35.0/70.0 | 25.0/38.0/53.0 | 142.0/145.4/143.9 | 68.6/70.4/65.7 | no |
| lower | 20.0/25.0/41.0 | 15.0/23.0/30.0 | 39.7/43.3/41.3 | 40.6/42.3/38.2 | no |
| grip | 26.0/29.0/37.0 | 23.0/27.0/35.0 | 52.6/56.1/54.9 | 32.9/38.0/39.0 | no |
| magazine | 18.0/37.0/255.0 | 25.0/34.0/211.0 | 255.0/255.0/255.0 | 198.8/209.1/204.1 | no |
| barrel | 22.0/44.0/113.0 | 31.0/47.0/107.0 | 113.3/119.2/116.5 | 134.4/123.4/104.1 | no |
| neutral_backdrop | 151.0/165.0/176.0 | 156.0/161.0/171.0 | 175.1/178.9/176.0 | 172.2/168.5/162.6 | yes |
| handguard_upper | 33.0/47.0/67.0 | 37.0/43.0/54.0 | 65.1/70.4/67.4 | 67.8/78.3/81.6 | no |
| handguard_lower | 26.0/29.0/37.0 | 24.0/30.0/39.0 | 66.7/69.9/70.0 | 38.2/41.1/40.9 | no |

### issued_diagnostic — `locked_photo`

GLB source SHA-256: `c5dfb18ab711c8315163bbb2ee3f0a01e536386807fbc9d5c560c7fe817b0582`. Independent light accepted: **no**.
Pair: `renders/final/pairs/locked_photo-pair.jpg`; full paint and every anchor’s
error/color data: `renders/final/paint-review/finish-values.json`.
Histogram: `renders/final/paint-review/issued_diagnostic-histograms.jpg`.

| Held-out paint | Render | Balanced photo |
| --- | --- | --- |
| V P10/median/P90 | 46.0/216.0/243.0 | 0.0/15.0/143.0 |
| Brightest-decile RGB | 245.7/246.7/245.8 | 173.7/168.0/159.8 |
| Highlight V | 246.7 | 173.7 |
| Highlight normalized RGB | 0.996/1.000/0.996 | 1.000/0.967/0.920 |

| Independent anchor | Render V P10/median/P90 | Photo V P10/median/P90 | Render highlight RGB | Photo highlight RGB | All bounds pass |
| --- | --- | --- | --- | --- | --- |
| handguard | 24.0/129.0/219.0 | 18.0/146.0/188.0 | 234.2/236.6/235.0 | 194.3/202.0/203.7 | no |
| handguard_upper | 81.0/157.0/192.0 | 140.0/161.0/191.0 | 193.6/198.3/195.0 | 189.7/196.4/196.9 | no |
| handguard_lower | 24.0/53.0/117.0 | 12.0/47.0/137.0 | 153.6/153.5/150.2 | 147.1/147.5/145.2 | no |
| lower_cheek | 69.0/75.0/82.0 | 56.0/72.0/88.0 | 77.3/83.1/80.0 | 91.7/93.4/96.1 | no |
| grip | 81.0/134.0/170.0 | 90.0/140.0/181.0 | 167.1/172.6/169.2 | 167.2/182.2/185.7 | yes |
| barrel | 122.0/192.0/233.0 | 199.0/212.0/237.0 | 237.6/238.2/237.2 | 240.2/237.0/232.9 | no |

### issued_observed_camera — `paint_issued_photo`

GLB source SHA-256: `c5dfb18ab711c8315163bbb2ee3f0a01e536386807fbc9d5c560c7fe817b0582`. Independent light accepted: **no**.
Pair: `renders/final/pairs/paint_issued_photo-pair.jpg`; full paint and every anchor’s
error/color data: `renders/final/paint-review/finish-values.json`.
Histogram: `renders/final/paint-review/issued_observed_camera-histograms.jpg`.

| Held-out paint | Render | Balanced photo |
| --- | --- | --- |
| V P10/median/P90 | 2.0/159.0/251.0 | 0.0/15.0/143.0 |
| Brightest-decile RGB | 253.5/252.6/252.4 | 173.7/168.0/159.8 |
| Highlight V | 253.5 | 173.7 |
| Highlight normalized RGB | 1.000/0.997/0.996 | 1.000/0.967/0.920 |

| Independent anchor | Render V P10/median/P90 | Photo V P10/median/P90 | Render highlight RGB | Photo highlight RGB | All bounds pass |
| --- | --- | --- | --- | --- | --- |
| handguard | 33.0/102.0/230.0 | 18.0/146.0/188.0 | 243.2/243.0/243.0 | 194.3/202.0/203.7 | no |
| handguard_upper | 157.0/203.0/231.0 | 140.0/161.0/191.0 | 237.7/237.5/237.5 | 189.7/196.4/196.9 | no |
| handguard_lower | 29.0/61.0/80.0 | 12.0/47.0/137.0 | 80.3/70.4/71.6 | 147.1/147.5/145.2 | no |
| lower_cheek | 81.2/95.0/104.0 | 56.0/72.0/88.0 | 104.9/104.9/105.0 | 91.7/93.4/96.1 | no |
| grip | 55.0/86.0/115.0 | 90.0/140.0/181.0 | 118.2/118.3/118.2 | 167.2/182.2/185.7 | no |
| barrel | 17.0/154.0/249.0 | 199.0/212.0/237.0 | 251.6/250.8/251.1 | 240.2/237.0/232.9 | no |

The dense-source pairs are also rendered separately in `source-pairs/`
and labeled source audits are written to `source-paint-review/`. The source
is not substituted for the shipped GLB. Roughness/specular trial grids are
explicit shader diagnostics, not rebaked acceptance evidence. None establishes
a valid new sheen under an accepted independent light. A better confirmed
coating reference or a resolved physical calibration is still needed.
<!-- ROUND2_PAIRS_END -->


<!-- ROUND2_NOTES_START -->
### Component-region correction and final failed refits

A final outline audit found that the studio lower-polymer photo region
included the selector lever, push pin and red control ink, while the
render object-ID mask excluded separate components. Explicit holes now
exclude those different materials. The handguard photo mask likewise
excludes its metal fastener, consistently in both studio and issued views.
All eight studio and all six issued anchor roles are retained; the
magazine’s real bright stripe remains unchanged. No RGB-based selection
or tolerance change is involved. Outlines were opened at native scale in
root `build/paint-round2/smg-lower-exclusions.jpg` and the full anchor view.
The lower mask loses 8,429 audited pixels belonging to those components:
its median stays 23; P90 changes 33 → 30, and highlight V
50.8 → 42.3. That is a material-region correction, not a passing fit.

All three current rigs were refitted with those corrected regions and
remain rejected. An additional native 1600 px / 32 sample basis uses the
world, 16 broad fixtures and 20 reflection cards derived only from visible
nonpaint geometry, at .35 m. Its magazine P90 prediction is
20.7 versus 211; its independent anchors still fail.
Its normalized unit-response sheet was opened, and it was not copied as an
accepted rig. Full refit predictions are root
`build/paint-round2/smg-component-refits.json` and this gun’s
`build/paint-components-*.json`. The tables above use fresh full-resolution
renders of the refitted, rejected rigs, not those optimizer predictions.

### Dense source and exported GLB both retain the failed look

| Pair | Source V P10/median/P90 | GLB V P10/median/P90 | Source highlight RGB | GLB highlight RGB |
| --- | --- | --- | --- | --- |
| studio_receiver | 21.0/44.0/111.0 | 21.0/44.0/113.0 | 157.7/161.8/158.6 | 160.6/164.7/161.6 |
| issued_diagnostic | 45.0/216.0/243.0 | 46.0/216.0/243.0 | 245.9/246.8/245.9 | 245.7/246.7/245.8 |
| issued_observed_camera | 2.0/158.0/251.0 | 2.0/159.0/251.0 | 253.4/252.5/252.3 | 253.5/252.6/252.4 |

These labeled source previews use the same held, rejected whole-scene
photo rig. They are not substituted for game delivery. Their failure already
exists before baking; it cannot be attributed solely to lost bake detail.

### Hero tonal range

Measured on nontransparent gun pixels in the actual PNGs. This is an overall
tonal audit, separate from receiver-only photographic/family masks.

| Hero | Luma P1/median/P99 | Fraction below 24 | Fraction all RGB ≥254 |
| --- | --- | ---: | ---: |
| hero | 0.0/36.7/160.0 | 27.78% | 0.0000% |
| hero_right | 0.0/22.0/155.8 | 59.43% | 0.0000% |

The visible cavity shadows remain deep and hero highlights do not clip.
That does not waive the unresolved receiver value or photographic fit.
<!-- ROUND2_NOTES_END -->

<!-- ROUND2_DELIVERY_START -->
## Paint round 2 — pass 3: studio, projection and delivery review

**Color and value first:** this is a review build, with a failed photographic
calibration gate. No new paint sheen is verified. The studio matches the
Harrow’s five fixtures exactly: key 18 W, fill 4 W, rims 13/5 W and overhead
card 5 W, including positions, dimensions, white color and directions.
Neutral world is .25/.25/.25 at strength .045. Existing exposure, backdrop,
all existing cameras and GIF camera/clip stay exact. A prepared-scene check
also proves that a colored photo rig cannot tint a subsequent ordinary shot.
Both configurations already initialized neutral world color; the new reset
repairs photo-order carryover, not an ordinary hero’s initial color. The
hero value change comes from 35/15 → 18/4 W and world .18 → .045.

Opened all 22 beauty/Eevee stills, including lower and barrel close-ups.
`docs/hero.jpg` remains unacceptable as a black-painted family gun: the
rolled upper field is conspicuously silver above a dark flat and black
polymer. `docs/turnaround.jpg` confirms that this is broad upper response,
not one isolated specular pixel. `docs/details.jpg` shows the same gray
upper, retained phosphate/steel wear, and deep ejection/slot cavities.
The stock, lower and handguard retain a dry black polymer appearance.
`docs/action.jpg` keeps the oxide magazine black with edge glints; the
existing 9 mm brass/copper remains bright. `docs/eevee.jpg` repeats the
silver upper problem. All five actual docs JPGs were opened. None of those
other accepted finish inputs was changed.

`beauty/projection_lower.png`, `beauty/projection_barrel.png`, ordinary
details and the hero were inspected. The lower stays black through the
receiver joint and grip transition; the exposed barrel is oxide-dark with
separate brighter crown/ring detail. No pale enamel patch was visible on
the polymer or barrel. The barrel’s disagreement with the bright issued
photo remains in the failed photographic pairs; this is not called a
successful barrel calibration.

Every decoded GIF frame 0–69 was opened at native delivery width. Handle
draw/lock/release and the magazine handoff retain their timing; the detached
magazine intentionally crosses the frame edge. Black polymer and magazine
remain stable, but the receiver upper stays silver throughout. No palette
flashing was seen. After the final rerun, 68 frames were byte-identical in
RGB to the viewed frames; changed frames 19/25 were reopened in pages
0016/0024. All 288 additional strip thumbnails were opened in inspection pages.

### Family measurements: explicit fixed surface regions

V means the maximum sRGB channel, 0–255. Masks are projected from actual
imported triangles and eroded one pixel, not chosen by pixel brightness.
The named bounds below are in the accepted Blender frame, in millimeters.
Visible mask overlays and all statistics are in root
`build/paint-round2/family-values/`; the three-gun image is
`guns/lmg/renders/final/hero-beside-ak-smg.jpg`. Its per-gun PNG metadata
pins the actual current GLB hashes. The Harrow export/source is unchanged.

| Region | Y bounds (mm) | Z bounds (mm) |
| --- | --- | --- |
| flat / Receiver_Shell | -20.0 to 170.0 | 92.5 to 99.5 |
| upper_land / Receiver_Shell | 10.0 to 140.0 | 114.0 to 124.0 |
| whole_receiver / Receiver_Shell | all to all | all to all |

| Image and region | f95dac1 V P10/median/P90 | Round 2 V P10/median/P90 |
| --- | --- | --- |
| docs / flat | 59/66/73 | 38/45/55 |
| docs / upper_land | 126/141/161 | 95/116/154 |
| docs / whole_receiver | 54/89/148 | 34/66/132 |
| family / flat | 36/44/54 | 36/44/54 |
| family / upper_land | 96/116/154 | 96/116/154 |
| family / whole_receiver | 34/65/132 | 33/65/132 |

The supplied handoff crops use different, unspecified pixel regions:
Relay docs **66/117/155**, family **49/94/143**.
Those observations are retained; they are not silently substituted for the
fixed geometry masks above. The supplied Harrow targets are median **58**
in its own hero and **66** in the family image. My annotated Harrow flat
(`Receiver_Sheet`, Y −20…210, Z 80…91 mm) measures **17/53/57**, before
and now. That region difference is reported rather than used to waive the
supplied 66 target.

Own-docs flat median **45** is **-22.4%** from 58; family
flat **44** is **-33.3%** from 66. The ±20% family requirement
is therefore not claimed as met.
The upper land’s **116** median is an additional visible failure, despite
the lower narrow flat being within 20% of my darker Harrow mask. A whole
receiver median of 65/66 does not excuse that upper field or the supplied
flat-side target.

### Projection and preservation

The wrapper partitions each original rigid/named projection owner into
enamel and non-enamel sources and delegates to the unchanged kit bake.
Target geometry, UVs and source shapes stay fixed. Assembled ghosts retain
contact AO. A second 4096/32-sample bake changes only enamel diffuse RGB;
the delivered 2048 interior masks then measure causal leakage.

| Nonpaint region | Changed BaseColor texels before | After control bake | Maximum channel delta after |
| --- | ---: | ---: | ---: |
| Lower_Mold | 21,084 | 0 | 0 |
| Barrel | 2,298 | 0 | 0 |
| Handguard_Mold | not supplied | 0 | 0 |
| Handle_Hinge | not supplied | 0 | 0 |

All **73** non-enamel named interior regions on this gun have exactly
zero BaseColor channel change. Reports are root
`build/paint-round2/smg-projection-control-deltas.json`.
The old/new texture repair delta is a different quantity from this causal
enamel-only perturbation; repairing an old wrong projection can change
a nonpaint texel without continuing to project paint onto it.

Direct comparison with the actual f95dac1 exports proves exact positions,
normals, UVs, weights and oriented triangle corners for this gun and all
four detachables. The gun’s original rig/clip/layout checks remain exact;
the SMG retains its existing tangent-rounding convention. Both existing
photo-camera sets (20 Rill / 4 Relay), all existing final shot definitions
(57 / 31), strip cameras and both GIF configurations remain exact.
Reports: root `exact-uv-identity.json`, `preservation-proof.json` and
`presentation-identity.json` under `build/paint-round2/`. Those prove
preservation/serialization. The unchanged actual-surface construction and
motion-clearance checks separately test assembly correctness.

### Build/check results and file inventory

Two independent clean builds removed this gun’s build, textures, exports
and renders. Each rebaked 4096 at 32 samples and regenerated all detachable
subsets through the kit path. Each separate `check` returned **0**:

| Clean cycle | Export/build | Separate check |
| --- | --- | --- |
| 1 | `make export`: 0 | `make check`: 0 |
| 2 | default `make`: 2, newly added diagnostic PNG absent from its already parsed shot list | `make check`: 0 |

The stable full default build was then rerun and returned **2 at the strict
independent nonpaint photographic gate**. All preceding construction, UV,
budget, atlas, rig, motion and re-import checks passed. The missing-view
dependency issue was resolved; it is not confused with the later material
calibration rejection. Logs and command/status JSON are root
`build/paint-round2/smg-clean-checks.json`, `smg-final-make.log` and
`smg-final-presentation.json`. The direct final photographic gate returns 1.
The normal baseline replacement refusal still fails closed and leaves its
manifest unchanged. No geometry check or tolerance was weakened.

All seven bake channels report zero missed interior rays. The 18 AK
baseline/rebaseline tests and three shared paint-bound tests pass.
No kit code changed. All Cycles bakes/renders and GPU motion renders used
the shared kit GPU lock. `python3 kit/repo_check.py` reports zero errors;
`git diff --check` passes.

Current gun: **41,540 triangles, one material, three 2048 maps,
10,670,292 GLB bytes**. Map PNG bytes: BaseColor.png 1,106,978, Normal.png 2,321,064, ORM.png 3,680,142.
Standalone budgets, every decoded texture hash and actual source hashes
are in root `build/paint-round2/inventory.json`. The reviewed projection
baseline and actual f95dac1 old hashes are recorded above; this presentation
work does not approve the paint.

| Docs file | Pixels | Bytes |
| --- | --- | ---: |
| `docs/action.jpg` | 1244×1400 | 155,265 |
| `docs/details.jpg` | 1204×1400 | 184,640 |
| `docs/eevee.jpg` | 1600×800 | 65,028 |
| `docs/hero.jpg` | 1600×800 | 63,750 |
| `docs/motion.gif` | 960×519 | 277,016 |
| `docs/turnaround.jpg` | 1600×1300 | 81,237 |

GIF SHA-256: `2d2fb1c68903a29cf9642616ea701b1a2cc7a843988c52a638a177f0e50d642a`. `make gif` returned **0**.
Each signature has 70 frames at 20 fps, unchanged ReloadEmpty/camera,
a 500 ms first-frame hold and 4000 ms decoded duration. All five JPGs and
all final decoded GIF frames were reviewed; repeat-rounding frames were
explicitly reopened and the remaining RGB hashes proved unchanged.

Final contact sheet: `renders/final/contact-sheet.jpg`. 330 render records
are verified against their actual source files in `build/provenance.json`.
All six contact-sheet inspection pages were opened. The bright rolled roof,
broad inherited wear and failed issued-photo reflections remain visible;
the contact sheet does not establish paint acceptance.
Photo pairs are in `pairs/`, source pairs in `source-pairs/`, stills in
`beauty/` and `eevee/`, and motion inspection sheets in `inspection/`, all
under `renders/final/`. The explicit `python3 src/final_review.py --docs`
step prepared these review JPGs after the failed gate; it does not turn
that failure into acceptance.

**Still unresolved:** a valid independent light calibration and verified
paint sheen. The dark flat and brighter upper response are both reported.
Further parameter changes need an explainable photo/accepted-finish
calibration. No new software is needed. A shared neutral-clipping audit
and explicit component-aware photo masks would help future family reviews.
<!-- ROUND2_DELIVERY_END -->

## Round 3 — family paint ruling and build separation

The owner's ruling supersedes the unresolved photographic approval above.
The five anchored light fits (1/11, 0/8, 1/8, 1/6 and 0/6 passing anchors)
cannot calibrate these guns' light. The accepted finish is the Harrow 56's
family paint in its same five-fixture studio. The failed fits, masks, pairs
and their original bounds remain diagnostic; they do not choose the paint.

`paint-review` is now a separate opt-in diagnostic that writes its JSON and
images without `--check`. It is no longer a prerequisite of `review`, `docs`
or `all`. The explicit Python `--check` retains the original anchor and paint
assertions. No other anchored-fit gate was in either default graph. All
construction, motion, geometry, rig, clip, UV, atlas, detachable and preservation
checks retain their bounds. `check` additionally verifies the accepted enamel
projection owner partition and exact delivered RGBA on all 73 non-enamel
interior regions, using `src/accepted_projection.json` recorded from the
actual `ab206c5` files. This verifies delivered preservation; the round-two
enamel perturbation pairs remain the causal projection experiment.

The Relay changes only intact enamel central roughness, .29 → .42. Its
linear base .022/.023/.024 and glTF specular factor .8 (Principled .4)
already equal the Harrow's. Non-enamel finishes, wear masks, studio, cameras,
geometry, UVs, rig, clips and detachable geometry remain fixed.

### Reviewed round-three paint baseline

Reason: Round 3: use the Harrow family's .42 enamel roughness instead of the rejected self-fitted .29; retain base color, specular, wear, all non-enamel finishes and exact geometry/UV/rig/clips/detachables.

Old `ab206c5` manifest SHA-256: `fe779730af1428a7576c4cfb30312d15c3f05189dd9268ac1b3d9b26c3b08963`. Its reviewed journal GLB
SHA-256 is `2c2643de76361b88319d5a42429be5ad7bd93fddc02b34a247649dd41a28744b`. The actual `ab206c5` exported GLB SHA-256 is
`c5dfb18ab711c8315163bbb2ee3f0a01e536386807fbc9d5c560c7fe817b0582`. The new reviewed GLB SHA-256 is `ebef6a42250e04de592ca4657a3c6522afd5d8d5ecd74de00ebcc23d38aa041e`.

The explicit `src/reviewed_rebaseline.py` step verifies those hashes, their
prior recording here, the handoff geometry/UV/rig/clip signature and all
accepted gun/detachable layout checks before updating the paint journal.
All specular/color/wear bounds and geometry baselines remain unchanged.
