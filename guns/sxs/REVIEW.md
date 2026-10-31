# Covey 26 — fine walnut grain, manual unload and action presentation

This round takes over `ae64e31` on `wp/guns-sxs`. `git merge main` reported
already up to date. The accepted form, 19 complete clips, rig, checkering,
nine wear causes, nonwood finishes and oil sheen/hue are retained. No kit or
common implementation changed. The previous finish round below is archival.

## Final-round critique pass

1. **Color/value first; resolve grain in the compressed delivery.** The
   photographic neutral remains the unshadowed gray studio paper above the
   butt in `look-gray-284.jpg`. White-balance gains, full-part masks,
   calibrated cameras and physical lights are unchanged. The exact handoff
   exports, maps, pairs and docs remain in repository
   `build/grain-final/before/`. Before, the broad figure reads as brushed or
   blurred streaks in the details JPG. The photo carries finer, straighter
   dark lines over the whole stock, including its light lands.

   The corrected material overlays narrow, irregular vessel lines on that
   figure. Its source-only `GrainSection` attribute derives from the existing
   stock cage and forend sections. A seamless circular domain carries each
   strand along the corresponding section as the wood bends and tapers.
   Random cell spacing and independently varying darkness avoid a periodic stripe;
   there is no fleck mask. Neutral RGB multiplication preserves the hue.
   Stock UV/surface density is **3.230 px/mm**, forend **4.452 px/mm**. The
   line thresholds target approximately **0.3–0.6 mm** at the visible lands,
   about one to two stock texels, rather than relying on the old 60–190
   micrometer pores alone. Width varies with section shape and projection;
   these are design targets, while the density is measured from the atlas.
   Added line relief is capped at **5 micrometers**, with faint roughness variation.
   Oil-land bases remain **.40/.46** and the specular network is unchanged.

   Rejected trials are retained in `renders/grain/`: `trial-radial` stretched
   lines into broad lower-butt arcs and missed highlight red (205.08 versus
   the 205.66 lower bound); `trial-transverse` removed those arcs but still
   missed red at 205.36. `trial-fine-soft` passed its numbers but lost too
   much fine contrast in the actual compressed JPG. Wider, darker lines in
   `trial-cellular` survived JPEG but exposed cellular patches on the curved
   wrist. Section-aligned `trial-flow-low` fixed their flow, but red at
   205.09 still missed. `trial-flow-uniform` passed but kept each strand too even along its length.
   The delivered field varies individual strands gradually over centimeters
   and adds neutral 1.08 stock-only value
   compensation before the unchanged checker/wear network. Neither a light
   rig nor a tolerance was changed to accept it.

   The exported 2048 maps pass every requested wood gate, using the original
   full-part denominator at native photographic camera scale. L10/50/90 and
   H below are encoded Rec.709 luma; H is the brightest 5% mean.

| Part / stage | L10 / median / L90 | H value | H RGB |
| --- | --- | ---: | --- |
| Stock, Before | 71.67/110.94/172.45 | 185.07 | 206.75/180.18/169.59 |
| Stock, After | 64.71/106.88/168.89 | 185.18 | 207.92/180.08/168.78 |
| Stock, Balanced photo | 63.74/111.65/176.76 | 201.61 | 228.51/196.47/173.27 |
| Forend, Before | 37.45/62.08/111.28 | 125.65 | 158.05/118.56/100.45 |
| Forend, After | 37.45/62.13/106.66 | 126.47 | 159.23/119.33/100.65 |
| Forend, Balanced photo | 35.76/57.28/103.45 | 125.95 | 158.95/118.90/98.59 |

Stock relative errors, L10/median/L90/H: +1.52%/-4.27%/-4.46%/-8.15%; H RGB: -9.01%/-8.34%/-2.59%.

Forend relative errors, L10/median/L90/H: +4.73%/+8.47%/+3.10%/+0.41%; H RGB: +0.18%/+0.36%/+2.09%.

Both pass median ±10%, tails ±15%, and highlight value plus every channel
±10%. Final full pairs are
`renders/final/look-review/walnut_{stock,forend}-pair.jpg`.

The details layout and framing are retained. Native before/after butt and wrist
crops are generated from the actual compressed docs JPGs by `src/grain_review.py`:
`renders/grain/comparison/{butt,wrist}-{before,after}.jpg` and
`{butt,wrist}-before-after.jpg` (before left, after right). Source boxes are fixed
at (824,235,1290,574) and (1008,790,1475,1176). From the repository root:

```sh
python3 guns/sxs/src/grain_review.py --before build/grain-final/before
```

Preservation is independently measured in repository
`build/grain-final/preservation.json`: **559/559 accessors exact**, with exact
node/mesh/skin/animation/material/texture-view/sampler JSON. Nonwood occupied
interiors have one changed BaseColor component at one RGB8 code, 365 changed
normal components at at most one RGB16 code, and exact roughness/metallic
components. Contact AO is measured separately because wood
relief affects contact rays. `source-preservation.json` independently proves
exact ASTs for steel, ammo, plate, finish and checker substrate, plus the exact
wood checker/cut/border/pressure/wear tail. No nonwood shader or wear cause was
retuned.

## GIF: visible manual withdrawal and level action framing

The sequence now includes `Unload`: both hull mouths are visibly clear of the
chambers at its last sampled frame, before a live shell enters. The external
hand's air travel is trimmed; no hand mesh or clip was added to the game asset.
The accepted 19 complete clips and their events are unchanged.

| Phase | Source range, end exclusive | Sampled source frames | GIF indices | Frames |
| --- | --- | --- | --- | ---: |
| Open | 39–69 | 39,42,…,66 | 000–009 | 10 |
| Unload | 15–54 | 15,18,…,51 | 010–022 | 13 |
| Reload right | 30–48 | 30,33,…,45 | 023–028 | 6 |
| Reload left | 93–114 | 93,96,…,111 | 029–035 | 7 |
| Close | 18–69 | 18,21,…,66 | 036–052 | 17 |

Source clock is 60 Hz; delivery is **53 frames, 20 Hz, 720×410,
192 distinct global palette entries, 438,071 bytes**. Motion lasts 2,650 ms;
the first frame's extra 500 ms gives a **3,150-ms loop**. Decoded delays are
550 ms then 52×50 ms. The final source GLB is the same one as the JPGs.

Trimming preceded crop/quality changes: the 60-frame correction was 496,804
bytes. Shorter approach/opening excerpts and a tighter crop retained the full
manual draw, both insertions and complete close. The level 54-frame version
was 451,650 bytes; one more opening sample was removed. The accepted 20 Hz and
192-color allocation are retained, with no new palette reduction or dithering.

The camera remains slightly above the gun, with the closed bore's perspective
projection leveled. A 58-mm lens, roll 0.377407732 rad, target (0,.135,.025) m,
aspect 720/410 and vertical shift +.101388889 keep the breech, lever, receiver
underside and forend iron inside the image. Actual exported surface extrema
through the selected poses measure **23.68 px below / 33.37 px above** the
critical parts at delivery width (`build/grain-final/fit-gif-final.log`, repository
root). The complete roots, source geometry and animations compare exactly.

Opened all 53 decoded frames, in order, on the seven native-width review pages
`build/gif/review/frames-{0000,0008,0016,0024,0032,0040,0048}.jpg`. Checked the
raised rims, both hull mouths clearing, both seated handoffs, extractor return,
full barrel close, lever return, margins and loop cut. Compared gold heads,
red hulls, brown walnut, case steel and deep bluing with the unquantized frames
and docs. No objectionable contour bands at delivery width; ordinary palette
quantization remains under pixel inspection. Worst per-frame foreground mean
RGB errors are **2.694/2.024/2.827 codes**; the worst per-frame P95 of maximum
channel error is **8 codes**. Top background corners remain constant. Exact
samples, delays, provenance and fingerprint are in `build/gif/report.json`;
color measurements are in repository `build/grain-final/gif-color-error.json`.

## Action sheet and final documentation

`action.jpg` now contains only the open action: raised extractors with fired
hulls, live shells resting on the extractor, and the full 42-degree opening
in side view. The eye-socket and 1.8 m scale shots remain in
`renders/final/beauty/{aimed,scale}.png` and the contact sheets. The README's
caption names the three action views. Hero, turnaround, details layout and
Eevee cameras are retained. Details/action sheets use lossless intermediates
before their final JPEG encoding, preserving fine lines within the byte limit.

All five actual JPGs were opened at their delivered sizes. The butt and wrist
before/after crops above are from the final compressed details JPG, rather
than source shader previews. The broad, soft oil reflection is retained.
The identical whole-visible-stock mask on the two docs hero JPGs measures a
**−0.13-degree median hue change** and **−.013 saturation change**. This is a
relative audit including checkering and reflections; the same camera and exact
geometry define both masks (`build/grain-final/hero-hue.json`, repository root).

| File | Pixels | Bytes |
| --- | --- | ---: |
| `docs/hero.jpg` | 1600×572 | 42,698 |
| `docs/turnaround.jpg` | 1600×1040 | 72,026 |
| `docs/details.jpg` | 1600×1200 | 185,522 |
| `docs/action.jpg` | 1600×1200 | 160,829 |
| `docs/eevee.jpg` | 1600×572 | 43,288 |

Full Cycles views are in `renders/final/beauty/`, Eevee in
`renders/final/eevee/hero.png`. Studio-only contact:
`renders/final/docs-contact-sheet.jpg`; full studio/material/wear/family contact:
`renders/final/contact-sheet.jpg`. Image provenance is checked against the
current exported GLB before docs generation.

## Final proof and remaining limitations

The final frozen source completed the following exact commands, all exit 0:

```sh
make -C guns/sxs
make -C guns/sxs check
make -C guns/sxs gif
python3 kit/repo_check.py
```

Repository-root logs are `build/grain-final/{make,check,gif,repo}-final.log`;
`build/grain-final/proof.json` records each command and its exit code. Earlier
interrupted iterations are not counted as completed validation. The repository
check reports **1,219 source files, zero errors**. The second fresh GIF render
matches all 53 decoded candidate frames exactly, and the tool preserves the
same final bytes. Approved JPG and GIF hashes match the post-build outputs.

The gun has **38,822 / 39,000 triangles**, **54 rigid meshes**, **17 bones**,
**19 clips**, **one material** and **three 2048 maps**, baked at 4096. The GLB
is **20,358,788 bytes**; BaseColor/Normal/ORM PNGs are
**3,799,458 / 10,717,528 / 2,864,954 bytes**. The accepted RGB16 normal
exception is retained. Standalone live shell / fired hull remain **752 / 480
triangles**, one 512 set each, **624,480 / 749,380 GLB bytes**.

`build/serialization.json` passes export budgets, real-scale dimensions,
normals, UV bounds and density, part ownership and re-import. UV overlap is
**0.00012470%**, with zero outside or degenerate triangles. Its 1,715 affine
samples have a maximum position error of **0.000191 mm**: this proves export
consistency. Physical assembly is separately checked on evaluated surfaces:
source and fresh-import checks both pass topology, 929 semantic samples,
246 contact measurements and all clips at half-frame intervals. There are
1,715 source / 1,728 fresh-import motion samples; maximum measured penetration
is **0.113714 mm**, below the unchanged **0.2 mm** tolerance. The fresh-import
lever swing has **0.159160 mm** minimum clearance and zero penetration.
`build/repeat.json` passes all **104** entries without differences; the dense
action fairness audit also passes. These checks establish construction and
serialization; the photographed pairs and delivered-image review establish
the appearance.

All nine wear-site fraction bands pass. The largest change from the accepted
on/off measurements is **0.12146 percentage points**, without changing a wear
expression (`build/grain-final/wear-preservation.json`, repository root).
The actual ungraded hero foreground has luma P1/P50/P99 of
**0 / 54.57 / 214.50**, **13.537%** below value 8, zero fully clipped pixels,
and **0.0004144%** with any channel clipped. Cavities retain deep shadow and
oil/metal highlights retain their rolloff.

Remaining limitations: the previously accepted trigger low-decile mismatch
remains **17.07 versus 6.07** in the balanced photo. Ordinary 192-color GIF
quantization remains visible under pixel inspection. The grain is an original
procedural approximation, with its smallest vessels filtered by the 2048
atlas; the requested larger fine lines survive the actual JPG. No kit changes,
new tools or lead decisions are needed. This branch is committed for review;
it has not been merged or pushed.


# Previous oil-finish round at ae64e31

# Covey 26 — oil walnut and final presentation

This round begins at `6f45ac3`; `main` merged cleanly in `04a61b2`.
The accepted form, rig, all 19 clips, contacts, clearance policy, other finishes,
checker construction, nine wear causes and detachable delivery are retained.
The trigger P10 miss remains explicit. No kit or common implementation changes.
The earlier look-round journal below is archival; this section records the
walnut correction and final presentation.

## Oil-finish critique passes

1. **Color and value before sheen.** Opened the accepted stock/forend pairs
   and full hero. The neutral is the same unshadowed gray studio paper above
   the butt in `look-gray-284.jpg`, not its highlights; native rectangle,
   linear gains and untouched balanced original remain in
   `build/look-photos/white-balance.json`. The stock already passes numerical
   gates: L10/50/90/H = 72.49/109.45/175.30/192.81, photo
   63.74/111.65/176.76/201.61. Its highlight RGB is
   206.52/189.65/183.78 against 228.51/196.47/173.27.
   Forend is 37.52/62.29/107.70/122.06 against
   35.76/57.28/103.45/125.95. These do not excuse a lacquer-like white line,
   orange cast, closely repeated growth stripes and peppered butt flecks.
   The photo instead has a broad low oil reflection, darker irregular streaks
   and gradual brown drift into the wrist.

   `renders/walnut/before/{walnut_stock-pair,walnut_forend-pair,hero}.jpg`
   retains the handoff. Exact exports, maps, cameras and all original pair
   measurements were sealed in repository `build/walnut-final/before/`
   before editing. No photograph enters asset generation.

2. **Color and value on source trials; reject flat and coarse figure.**
   `renders/walnut/pass1/` removes the peppered grain and broadens the sheen,
   but its stock source median is 122.41, low tail 78.86 and H 178.63:
   too light below, too dim in the highlight, too plain. Forend source median
   66.15 also misses. The next trials add variable-width domain-warped growth,
   irregular longitudinal streaks and slow brown drift, with a separate fine
   fiber scale. Pass two still has stock low tail 77.41 and over-broad dark
   ribbons. Retain the accepted cut-wood substrate under the original checker
   field, keeping cutter normals, pitch, borders, worn tips and all cause
   masks unchanged. This isolates the planed oil lands from accepted cutter
   response. The helper is the former substrate expressions verbatim.

   Pass four source L10/50/90/H = 71.70/113.24/169.73/181.57 is closer in
   color/value but the highlight red is 202.36, outside 10% of the photo.
   Pass five adds narrower irregular fibers and reduces the wide dark waves;
   source median 108.05 and median RGB 150/99/71 approach the photo's
   155/103/71, but H red 200.60 still fails. Reject a statistical near-match.
   Increase the warm diffuse response within the varied walnut field rather
   than sharpening the white stripe or changing the photographic light rig.
   All trial source renders were opened beside the same balanced photo.
   Their diagnostics are explicitly source-only and do not establish delivery
   acceptance. Final acceptance is on the exported GLB below.

   Later source trials retain the same lighting. Pass six fixes the median
   (112.88) but barely misses the stock low-tail and highlight-red bounds.
   Increasing diffuse RGB together makes the wood browner rather than simply
   more red; slow wrist darkening supplies low-tail margin. Pass nine source
   L10/50/90/H is 71.20/110.73/172.10/184.81, H RGB
   206.24/180.00/169.30, median RGB 157/101/70 versus photo 155/103/71.
   The forend is 31.95/62.86/111.22/127.36, H RGB
   159.97/120.29/101.39. Both source gates pass. A final .01 increase in the
   stock's high-end linear red adds highlight margin before the full bake.
   Plain-stock roughness is .40 instead of .29; planed forend is .46 instead
   of .40. The accepted checker substrate and cutter/wear expressions remain
   exact. The source grain has broader, irregular dark streaks and narrower
   broken fibers, without the former regular flecks.

   One early default-build attempt was deliberately interrupted during its
   bake for this source correction. It is not counted as completed validation;
   the final unmodified default command and separate check are recorded below.



3. **Color/value and oil sheen on the shipped maps.** The independent export
   probe (`renders/walnut/export-check/`) loads `export/sxs.glb`, SHA-256
   `f688fb1c422c536fe2803e366dfd59d4802962349d4732ed93b7de05cd1f4b8b`,
   at native photographic scale with the unchanged calibrated camera/lights.
   Stock L10/50/90/H is **71.67/110.94/172.45/185.07**, H RGB
   **206.75/180.18/169.59**; forend **37.45/62.08/111.28/125.65**,
   H RGB **158.05/118.56/100.45**. Both pass every required gate, including
   the highlight's individual channels. The paper neutral and full-part
   denominators are unchanged. Opened both exported crops beside the photo:
   the reflection is broader and lower, the body is browner, and broad uneven
   streaks with fine broken fibers replace the dense pinstripes and flecks.
   The photo retains richer fine pore contrast and incidental small marks;
   those do not justify changing the accepted checkering or nine wear causes.
   Final full pairs, exact same-camera before/after hero, and their numbers
   are indexed below after the complete presentation build.

   Preservation is measured independently in repository
   `build/walnut-final/preservation.json`: **559/559 accessors exact**, with
   identical node, mesh, skin, animation, material, texture-view and sampler
   JSON. Nonwood occupied interiors have **exact BaseColor RGBA**; 354 normal
   components differ by at most one RGB16 code, and one ORM component differs
   by one RGB8 code. Contact AO is deliberately measured separately because
   changed wood microgeometry affects rays. Source AST/tail comparison also
   confirms unchanged steel/ammo/butt shaders and checker/wear expressions.


   Standalone preservation also passes the kit's original .25/255 surface
   comparison against the accepted 512 GLBs. Shell/hull BaseColor and ORM
   samples are exact; normal maxima are 0.0000078695 / 0.0000090485. Geometry,
   origins, density and tangent frames are unchanged. Encoded GLB sizes differ
   through PNG rounding/unused neighborhood data, not a subset policy change.
   Their independent current full-atlas, density and L0–L3 checks also pass.

   At the fixed butt station 35% toward the wrist, an 11-column median and
   11-row smoothing measure the reflection's contiguous half-prominence width:
   **66 → 75 px**, **22 → 25%** of the local wood height. Peak luma falls
   **197.39 → 182.03**. This is a same-camera display-profile comparison,
   not inverse roughness recovery; `build/walnut-final/highlight-profile.json`
   retains the exact station, baseline and thresholds. The full before/after
   stock, forend and hero are in `renders/walnut/comparison/`.


## Wear preservation after the oil bake

Every wear expression and the cutter/wear network remain exact; no site,
pressure footprint, selected-point hardness, impact, threshold or annotation
was retuned. The nine independent on/off pairs retain their accepted placement
and 2D structure: long carry field, narrow muzzle rims, faded flats, thumb land,
continuous inner guard rub, distinct upper-hand checker tips, and the same
small toe and upper-forend fractures. All nine full/crop/difference pairs were
opened. Whole-frame image fractions are not mathematical constants: the revised
wood affects its background response and reflected/contact light.

| Site | Handoff % | Final % | Photo % |
| --- | ---: | ---: | ---: |
| barrel_carry | 13.8220 | 13.7891 | 13.3889 |
| muzzles | 0.7395 | 0.7388 | 0.7184 |
| action_fade | 59.2379 | 59.2218 | 57.2777 |
| lever_thumb | 29.5142 | 29.6761 | 30.1996 |
| guard_fingers | 37.4095 | 37.4296 | 35.2263 |
| wrist_points | 1.6766 | 1.6877 | 1.6366 |
| forend_points | 6.0659 | 6.0578 | 5.8999 |
| stock_toe | 0.2913 | 0.2973 | 0.2673 |
| forend_edges | 0.1614 | 0.1372 | 0.1640 |

The largest before/after difference is **0.16194 percentage points** at the
lever. Every final six-code fraction remains inside its handoff's existing
four-to-eight-code sensitivity interval (`build/walnut-final/wear-preservation.json`).
This reports the existing uncertainty; it neither adds a new acceptance gate
nor replaces the rendered 2D review. The small forend fracture is 0.1372%
versus 0.1614% before, within both the accepted threshold interval and the
photograph's native boundary band. Its source cause is unchanged.

Optional snapshot comparison, from the repository root:
`python3 guns/sxs/src/finish_compare.py --before build/walnut-final/before`.
The saved handoff is local review input, never a dependency of the rebuilt asset.

## Final exported renders and documentation

The complete default build re-rendered the final GLB, embedded maps and all
source/export photographic and wear evidence. Final wood gates reproduce the
export probe above. Both complete walnut pairs, the identical-camera hero
before/after, all studio views, five delivery JPGs, nine wear pairs, standalone
shell/hull and contact sheets were opened. Color/value first: the stock now
reads browner with a lower, broader oil reflection; protected blue steel stays
dark, action recesses remain deep, and the case highlights roll off. The
photograph still has richer small pore contrast and incidental small marks.
Our broad figure remains more conspicuous than the photograph in the lower
butt; the regular peppered flecks and narrow lacquer stripe are gone.

The hero's foreground encoded luma P1/P50/P99 is **0 / 56.703 / 214.575**.
All-channel clipping is zero; any-channel values at least 254 occupy
0.0004144% of foreground, and 13.473% is below eight. These diagnose the
tonal range, not photographic equivalence. The Eevee view uses the same
textures and material extension. A presentation bug had re-enabled the
camera-hidden black reflection cards in Eevee/Workbench; they now remain
hidden there. Cycles and the calibrated photographic light rigs are unchanged.

`src/docs.py` checks render attribution against the current GLB hash before
making the five JPGs. The action sheet shows raised extractors with fired
hulls, the loaded breech from the opposite side, the exact eye and a 1.8 m
silhouette. Details cover the action, walnut, forend and controls. Each delivery
JPG was reviewed at its final dimensions, after compression.

| Final docs file | Pixels | Bytes |
| --- | --- | ---: |
| `docs/hero.jpg` | 1600 × 572 | 39,508 |
| `docs/turnaround.jpg` | 1600 × 1040 | 70,331 |
| `docs/action.jpg` | 1600 × 1300 | 166,297 |
| `docs/details.jpg` | 1600 × 1200 | 194,009 |
| `docs/eevee.jpg` | 1600 × 572 | 40,191 |
| `docs/motion.gif` | 720 × 320 | 447,475 |

Full Cycles stills: `renders/final/beauty/`; Eevee:
`renders/final/eevee/hero.png`. `renders/final/contact-sheet.jpg` contains
all 51 studio, ammunition, material, wear and family panels;
`renders/final/docs-contact-sheet.jpg` contains the 20 main-gun studio/Eevee
views. Before/after evidence is
`renders/walnut/comparison/{walnut_stock,walnut_forend}-before-after.jpg`
and `hero-before-after.jpg`, with exact measurements in `values.json`.

The rewritten README leads with the hero and captioned motion, then the four
remaining JPGs. It documents sourced real dimensions and their limits,
construction, measured materials, nine wear causes, the rig and 14 sockets,
all 19 clips, detachable subsets, triangle/map/file budgets, RGB16 normals,
rebuild steps, evidence paths, credits and remaining limits. Family README
and GIF tables now include the ninth finished gun.

## Signature GIF: trim, crop, then palette

The unmodified shared tool loads the same exported GLB. The slightly elevated
camera levels the closed gun and spends the crop on the breech, extractor
and shells. Background is flat gray, with no text or dithering. Source clip
ranges are half-open 60-Hz frames:

| Clip | Source range | Decoded GIF indices | What remains |
| --- | --- | --- | --- |
| Open | 24–69 | 0–14 | Lever already swung; barrel drop and complete extractor lift |
| Reload | 27–48 | 15–21 | Right shell insertion and seating |
| Reload | 90–114 | 22–29 | Left shell insertion and seated handoff |
| Close | 0–69 | 30–52 | Extractor return, barrel closure and lever locking |

The manual Unload phase and the reload's air approach/hand-clear gap are cuts
between excerpts, explicitly described in the README. The full 19 clips and
their boundary states remain untouched. Both insertion strokes and the
closing stroke remain at real speed. Source samples advance by three frames.
The loop has **53 frames, 20 fps, 192 global octree colors**, **447,475 bytes**,
and **3,150 ms** total duration: 550 ms first frame and 52 × 50 ms afterward.
The first delay includes the shared tool's extra 500 ms hold.

The first 108-frame 25-fps, 256-color 960-wide loop was 1,369,312 bytes.
Trimming the static reload tail and cropping to 720 × 400 came first
(1,005,920 bytes). Only then were lower palettes and 20 fps tried. The
80-frame 96-color trial was still 565,165 bytes; removing the reload's air
intervals retained both seatings in 53 frames. A further vertical crop to
720 × 320 left the 128-color ffmpeg trial at 473,099 bytes. Its 112-color
444,678-byte version fit but shifted shaded brass toward pink: reject.
Low 48/64-color trials also showed visible wood contour steps. Octree better
preserved the rare gold tones; 112/128/144/176-color trials fit, but **192**
retained smoother walnut/bluing gradients within the limit. These prototypes
remain ignored build files; only the final loop is committed.

All 53 decoded frames were opened in order on the seven native-width pages
`build/gif/review/frames-{0000,0008,0016,0024,0032,0040,0048}.jpg`.
Checked rim/extractor lift, both shell insertions, seating visibility changes,
extractor return, barrel and lever closure, crop clearance and the loop cut.
Compared the wood, blue-black barrels, case steel, red hulls and brass against
the final JPGs and unquantized frames. No objectionable contour bands remain
at delivery width; ordinary GIF quantization remains visible under pixel
inspection. Against the unquantized foreground, the worst frame's mean
absolute RGB errors are **2.7045 / 1.9329 / 2.6211 codes**, and the worst
per-frame 95th percentile of maximum-channel error is **8 codes**. The decoded
surround is a constant **107/110/113**, one code below its 108/111/114 input.
Repository `build/walnut-final/gif-color-error.json` retains the counts.

The final fresh `make gif` reproduced the accepted bytes and all 53 decoded
reference frames exactly. `build/gif/report.json` records source attribution,
samples, delays and palette. Final GIF SHA-256:
`d2cfec4b0fa53ef213534a91d178fb1812429daa7228a20ed026388ed008e7f1`.

## Final build proof and limits

All requested commands completed with exit status zero:

```sh
make -C guns/sxs
make -C guns/sxs check
make -C guns/sxs gif
python3 kit/repo_check.py
```

The full default build used 4096/32-sample GPU bakes and 4000-wide/48-sample
Cycles finals through the kit lock. Logs are in repository
`build/walnut-final/{make-final,check-final,gif-final-octree,repo-check}.log`.
The repository check reports **1,218 source files, zero errors**. Source and
fresh-import assembly/contact and half-frame clearance probes, the independent
51-angle lever sweep, deterministic rebuild, fairness gauges, attribution,
and standalone surface/density/L0–L3 checks all pass. Serialization separately
passes **1,715 affine samples**, maximum position error **0.000000190828 m**.
UV overlap is **0.00012470%**, with zero outside/degenerate UV triangles;
median density is **3,226.50 px/m**. These are measurements, not substitutes
for the appearance review above.

Gun: **38,822 triangles, one material, three 2048 maps, 19,369,020 GLB bytes**.
BaseColor RGBA8 / Normal RGB16 / ORM RGB8 PNG bytes are
**3,236,682 / 10,542,965 / 2,612,523**. RGB16 avoids the eight-bit reflection
steps previously observed across the rounded hollow action head; its size
cost and importer requirements are explicit in the README. Shell/hull remain
**752 / 480 triangles**, each one material and three 512 maps, at
**624,492 / 742,316 GLB bytes**. Rig, clips and sockets remain **17 / 19 / 14**.

Remaining limits are disclosed rather than silently redesigned: accepted
trigger P10 miss, different-maker camera/wood-line residuals, inferred visual
eye fit rather than measured human anatomy, and fine pore/safety/headstamp
detail softened by the 2048 bake. No kit/common file changed and no tool or
approval is needed from the lead. No contract change is proposed.

---

# Covey 26 — look round one delivery

The owner accepted round seven's form, cameras and 38,822-triangle allocation
for this look brief. The archival failed form gates below remain measurements;
they are no longer requests to redesign that accepted geometry. Main merged
cleanly at the start. No vertex, clip, pivot or contact policy has changed.

## Look critique passes

1. **Rejected first source finishes. Color and value:** the 1200-pixel Cycles
   source hero and action/wrist/forend close-ups in `renders/look1/pass1/source/`
   showed walnut too light and case oxide chalky straw. Native studio photographs
   `look-field.jpg` and `look-field-13.jpg` show a darker oil-finished brown and
   subdued case colors. Their clipped white background cannot supply a white
   balance; these first observations are qualitative, not a numeric match.
   Reduce walnut diffuse values and specular (.28 to .16, matching the lever),
   mute blue/straw/brown oxide, and lower the smooth dent bowls from .40 to .18 mm.
   Break their edges procedurally and reduce their pale lips: the first forend
   dents looked punched. The accepted silhouette geometry is untouched.

2. **Rejected first baked export. Color and value:** the white-balanced gray-paper
   whole-gun and macro references supersede the clipped-cutout color guess.
   Neutral rectangles and linear gains are in `build/look-photos/white-balance.json`.
   `renders/look1/pass2c/look-review/` measures whole parts on the actual export:
   barrel median 20.9 versus 59.3, case 58.9 versus 118.5, stock 57.6 versus
   111.7. These are substantial misses. The first free macro fit also crossed
   the gun and hid the controls: reject its lower RMS. Lock the observed rearward,
   above hemisphere and disclose the remaining 33-pixel inter-maker residual.
   The carry mask was too far ahead of the balance; move it toward the forend.
   Checkering retains a 1.27-mm perpendicular pitch (20 LPI), but its hand-polished
   points need actual exported on/off evidence. The first isolated material
   projection was audited with constants; replace that dependent color test with
   an independent 54-part ownership witness, removed from the shipped color map.

3. **Rejected light and surface trial. Color and value:** the pass-three front
   fill made the action's whole-side median 225.9 instead of the photo's 118.5.
   That is a reflected softbox, not evidence to lower steel albedo arbitrarily.
   Remove the frontal macro fill, aim the lights at each photographed region,
   and retain the paper as a diffuse lighting check. In `renders/look1/pass3b/`,
   paper agrees approximately but the flat remains too bright (141.7), the
   stock too matte/dark (64.4 versus 111.7) and the forend too even (P90 66.8
   versus 103.5). The upper case oxide still reads like clean blue/straw
   camouflage and the walnut's annual rings look drawn. Reject both. Reduce
   ring contrast, restore the pump's .33 dielectric specular level and a .34
   stock oil roughness, retain open pores, and add fine oxide freckles only
   where case oxide survives handling. Use a darker oxidized gray on faded
   flats. Let the thumb-pressure mask reach the lever's rounded rim instead of
   stopping on its top plane. No accepted geometry changes. This pass's exact
   GLB/high source and hashes are retained under repository `build/look1/pass3/`.


4. **Rejected 2048 wear visibility and small-surface bake. Color and value:**
   the long softbox now runs along the gun, restoring a plausible oil highlight.
   Whole-stock P10 is 65.1 against 63.7, but median/P90 remain 86.9/120.4
   against 111.7/176.8; case flats are too uniform and bright at 162.9 against
   118.5. The forend stays too pale/even (75.4/80.4/84.4 versus
   35.8/57.3/103.5). Do not accept these as a match. Source and baked hero,
   open/aimed/shooter views, turnaround and all close-ups were opened.
   The safety's fine cuts alias to cloudy bumps at only 1.695 texels/mm;
   forend cutters have only 2.034 texels/mm. Increase their UV priority within
   the same atlas, without adding a triangle. Broaden the forend's developed
   checker panel up its outer cheeks; the old panel sat too low in the accepted
   section to read from the hero. Add an original, font-generated shell
   headstamp and more ammunition texels: the unmarked head looked unfinished.

   The actual site-off exports preserve **every GLB accessor**. Full-frame
   image-difference masks expose failures the node masks could not: wrist and
   forend point wear both measure **0%** above six RGB levels. Reject. The
   carry field measures 17.22% versus 13.39%, action fade 72.74% versus 57.28%,
   thumb 10.34% versus 30.20%, guard 46.47% versus 66.08%, toe 0.15% versus
   0.57%, forend impacts 1.49% versus 3.45%. Narrow the carry field, retain
   oxide islands between handled action fields, extend thumb and finger
   pressure through their rounded contact surfaces, polish the flattened
   checker tops more visibly, and enlarge the local shallow impacts. The
   reference annotations and reflection uncertainty remain visible; masks are
   measurements for review, never inputs to textures. Correct the review's
   profile axes for the macro's rigid image rotation and enlarge native crops
   explicitly for display. Original native masks and counts remain saved.
   Pass-four artifacts and source snapshot are retained in `renders/look1/pass4/`
   and repository `build/look1/pass4/` respectively. No form or rig changes.


5. **Rejected excessive polish fields; correct the photographic denominator.
   Color and value:** stock median 112.3 versus 111.7 is close, but its low/high
   spread is still too narrow; the paper is now 183 rather than the photo's
   approximately 154. Match that exposure before making finer color claims.
   The forend's 107.8/116.7/129.2 versus 35.8/57.3/103.5 is a clear miss.
   Source/photo/export pairs show nearly identical source and export values
   (forend mean absolute RGB difference only 1.58/1.76/1.79), so this is **not**
   further bake loss to excuse. The hand-pressure roughness override polished
   almost the whole forend. Remove that continuous gloss field, leave rough
   grime in grooves, and polish flattened tips only. Narrow the peak pressure
   footprints at wrist and forend: actual exported differences reached 5.40%
   and 40.56%, versus 1.64% and 5.90%. Dings remain too small/faint at full frame;
   brighten only the fractured bare-wood lips, not the surrounding wood.

   The new rearward hero exposes the long narrow accepted lever and the wrist;
   the accepted aimed/open cameras are untouched. Its thumb field is now too
   broad (44.03% versus 30.20%), so narrow it along the leaf. The barrel carry
   patch is still high/broad (17.79% versus 13.39%); lower it onto the carrying
   flank and reduce its length. Extend muzzle thinning slightly along the tube
   so it remains visible from this whole-gun angle. The source field finishes
   use a physical .45 dielectric specular level for oil, with one shared atlas;
   no per-part exposure or image grading is allowed. The same-studio three-gun
   view shows bluing consistent with the pump and warm walnut within the lever's
   range; our case action remains a distinct used silver-gray finish.

   A native-pixel inspection found a real annotation error: the previous guard
   polygon included some cast shadow and missed the brightest inner edge.
   The steel/shadow transition is visible in repository
   `build/look1/guard-mask-boundary.jpg` and the native scan profiles. Replace
   it with the measured inner-edge path plus the visible 8-pixel steel width;
   the rubbed inner gray/bright field is about 3 pixels wide. Its reference
   worn fraction changes from the invalid 66.08% to approximately 35%, and its
   whole-part highlight from 199 to approximately 239. This forces a **smaller**
   guard rub, not an acceptance of the 76.38% export. Retain the one-native-pixel
   boundary sensitivity and the warning that a highlight is not uniquely wear.
   Original and revised evidence remain archived. No geometry changed.

   The denser layout raised the measured global UV median to 3056 texels/m;
   the former arbitrary `<3000` assertion rejected an improvement. Replace
   that cap with a measured minimum of three texels per designed cutter pitch
   on stock, forend and safety. All scale, UV overlap, normals, rig, contacts,
   serialization and exact-precision detachable audits pass. Seven boundary
   texels on hook/lump UV boundaries differ between clean and used color bakes
   after filtering; source interiors remain unchanged. They are recorded as
   bounded one-pixel UV-edge differences, not counted as physical weather.
   Site-off outputs retain every untouched used texel exactly. Pass-five
   artifacts/source are archived under `renders/look1/pass5/` and repository
   `build/look1/pass5/`.


6. **Resolve reflection visibility, then remeasure. Color and value:** the
   pass-six source and export both made the checkered forend too pale
   (median 85.0 versus 57.3). A source-only zero-specular diagnostic changed
   that to 41.0; it isolated reflected visibility in the grooves rather than
   a missing dark base color or lost bake detail. Preserve oil sheen on flat
   wood and point tops, suppress reflected visibility in cut grooves and
   vessels, and bake this scalar into the existing opaque BaseColor alpha.
   The kit exporter explicitly opts into KHR_materials_specular with the same
   BaseColor image/sampler. No extra image, material or texture resolution is
   introduced. A clean fresh archive ran all 24 kit modules sequentially:
   `build/kit-specular-suite/build/results/results.json`, 24 passed.
   Pass-six hero retains deep cavity shadow and no clipped surface highlights;
   its foreground median is approximately 75, P99 199, and about 9% below 8/255.
   That tonal range is useful, but does not prove the photographic match.

7. **Reject repeated impacts and compressed control highlights. Color and
   value:** pass-seven export medians are barrel 42.6/59.3, case 135.6/118.5,
   lever 72.9/55.3, safety 65.3/75.4, triggers 29.7/24.5, guard 27.8/51.3,
   stock 103.3/111.7 and forend 58.7/57.3 (ours/photo). The forend's median
   improvement is real, but P10 53.2/35.8 still misses: the native/source/export
   pair shows the photo's deeper grooves. Small source/export RGB differences
   (about 1 code value in wood) show this is mainly source response. The
   safety's diamonds read after the new scalar map and larger UV allocation;
   their source/export difference remains about 16 codes because subpixel
   facets filter at 2048. Do not claim a lossless material bake.

   Trigger and guard highlights remain too subdued compared with the native
   photograph. Darken intact bluing on their broad flats, polish the contact
   edges, and allocate more UV area to the blades and lever. The guard's
   original normal-direction pressure gate did not narrow its broad inner
   land; use a physical X strip on that land. Actual pass-seven worn fractions
   are carry 12.08/13.39%, muzzle .40/.72%, case 66.69/57.28%, lever
   33.58/30.20%, guard 48.34/35.23%, wrist 2.79/1.64%, forend points
   10.55/5.90%, toe .48/.57%, and forend edges 3.93/3.45%. Narrow the latter
   pressure fields, reduce case fade, and lengthen only the muzzle end field.

   The toe and forend dings have repeated pale upper crescents: this is a CG
   tell despite their approximately correct area. Replace the toe's ten bowls
   with three impacts and break each thin raised lip into one torn quadrant,
   interrupted along fibers. Keep shallow compressed wood and unbroken finish
   around it. This changes normal/color only; accepted geometry is untouched.

   Eighteen BaseColor and seventeen roughness/metallic chart-boundary texels
   differ between the independent used/clean bakes. BaseColor/roughness/metallic
   **interiors outside the site domains are identical**; normal interior delta
   is at most one 16-bit code value. Remove the arbitrary global edge-count
   cap and instead retain all boundary coordinates/counts/amplitudes, with
   exceptions restricted to the measured one-pixel boundary. The strict
   interior assertion remains. Every untouched site-off texel remains exactly
   the used texel. These edges are not counted as physical wear.

   Quick lighting probes initially reused calibration-file light settings,
   which override the module defaults. Correct the probe camera copies and
   regenerate the calibration through Make before final comparisons; do not
   infer material behavior from a light change that was never applied.


8. **Keep the action; reject matching by washed-out fill. Color and value:**
   pass eight's action passes every requested gate: P10/median/P90/highlight
   67.8/113.7/147.0/203.7, versus 61.1/118.5/157.9/205.2. The newly resolved
   source/export control edges are visible. The remaining photographic misses
   are still real. Native-scale side diagnosis (5977 pixels, matching the
   reference width) changes forend P10 from 54.5 to 45.6 and median from 58.9
   to 63.2: filtering was part of the earlier compression, but does not explain
   the entire miss. Use native-scale finish comparisons, retain the delivered
   2048 maps, and retain the ordinary 1600-pixel game-frame hero.

   Checkering needs both form and response: freshly cut grain absorbs more oil
   stain than planed lands; its grooves lose reflected visibility. Increase
   warm flat-land walnut response only within a real walnut range, darken the
   absorbing cut field, and retain individual worn point tops. Keep all of
   that original; no image supplies a texel. The safety's upper facets need a
   slightly brighter polished response, with dark oxide in the cuts.

   Pass-eight visible wear fractions are carry 13.37/13.39%, muzzle .69/.72%,
   case 63.68/57.28%, lever 33.58/30.20%, guard 49.67/35.23%, wrist
   1.41/1.64%, forend points 6.19/5.90%, toe .29/.57% and forend edges
   .87/3.45%. Fractions alone conceal the checker problem: the forend's actual
   image change is one merged field, whereas bright tips in the photograph
   remain separate. Oil changes in connected grooves were being counted as
   point wear. Retain oil finishing in both used and unused counterparts;
   remove the broad pressure-dependent oil roughness override. Change only
   flattened tips in the wear counterfactual, then inspect native 2D masks as
   well as the filtered game frame. Add a native 4000-pixel hero proof at the
   same camera/lights, with common 800-pixel part rasters, connected worn and
   surviving regions, and both profiles. This supplements the full 1600-frame
   proof rather than replacing it.

   A physical X strip still reaches the guard's entire outer side face. Add a
   normal gate that rejects that protected broad side while retaining the
   inner land and its rounded contact edge. The three toe impacts look less
   manufactured, but the forend's short torn lips lost too much full-frame
   contrast. Increase shallow compressed-wood contrast and modestly enlarge
   the impact footprints; do not restore the repeated pale crescents.

   Several side-light trials are rejected explicitly: stronger uniform room
   light raises the barrel median but also lifts its P10 and washes the wood;
   broad low frontal fill improves the median at the expense of excessive P90
   and pale walnut. Keep all three finishes in the same light-fitting objective
   and include the photographed neutral paper. A fixed-material, neutral-light
   coordinate search in `build/look1/fit-side-lights.py` tests key power/height,
   fill and world strength together. This is camera/studio estimation only;
   it never changes material pixels, asset geometry or per-part exposure.


9. **Reject a statistical polish stripe. Color and value:** pass nine keeps the
   case steel inside every photographic tolerance, but stock/forend low tails
   and the lever's median still miss. Increasing annual-ring contrast produced
   exhibition-like zebra bands in the source; reject that trial and retain
   moderate plain-walnut figure with longitudinal open vessels. The old narrow
   hand ovals approximately matched worn fractions while creating connected
   polished stripes. Broaden each oval to the actual hand footprint, select
   individual cutter tips with deterministic per-diamond hardness, and keep
   permanent oil and cavity response identical in used/unused counterparts.
   These changes affect shader height and material response only.

10. **Resolve the delivered cutter pitch. Color and value:** keep the oil-walnut
    lands warm and the freshly cut field darker; brighter diffuse walnut alone
    cannot recover a filtered groove. Stock unwrap angle trials at 30/40/55
    degrees and assembly trials at 40/55/66 identify a denser valid layout.
    Keep 40-degree stock / 55-degree assembly, 1,396 islands, 45.08% occupied
    coverage and 0.000144% measured overlap. Concave packing adds negligible
    coverage and is rejected. Measured median shipped texels per perpendicular
    cutter pitch are 4.10 stock, 6.27 forend and 10.06 safety. No triangle or
    accepted vertex moves. Rebuild the used and unused 4096 bakes on these same
    UVs before judging them.

    The macro guard reflects a dark field on its broad accepted inner land.
    A small low studio strip can match the guard's quantiles, but washes out
    the neighboring trigger edges. Two physical black baffles still fail the
    joint fit; reject all these control-light trials, rather than calling an
    isolated guard improvement a matched action. Guard normals and signed
    volume were checked independently and are outward: this is not a reversed
    face repair. The extra retained-blue barrel photograph uses a narrow
    neutral key, fill and matte reflection card, identically for source and
    exported comparisons; it supplements the sharper gray-paper whole gun.
    Its original unscaled WordPress upload is unavailable (404), so retain
    the downloaded 2560-pixel photo and disclose its limited cross-section
    resolution. No imagined higher-resolution source is claimed.


11. **Reject a material-projection leak and excessive point density. Color and
    value:** the pass-eleven exported action and lever meet every requested
    histogram/color tolerance. Safety low tail 43.9/35.9, stock 76.9/63.7,
    forend median 66.2/57.3 and guard median 27.9/51.3 still miss (ours/photo).
    Source/export pairs show these are mostly source response, with measurable
    filtering loss in the safety and forend. Source-tested corrections retain
    plain warm walnut, deepen longitudinal grain, reduce checker-field response
    and lower the safety's polished steel response. A .31 brass-bead roughness
    improves its shadowed lower tail without raising its median beyond 10%.
    A .24 barrel polish produces a crisper reflected strip. The taller .18-m
    reflection card blocked the blue-view key: reject it and keep the .10-m
    card, with the direct key path clear. A slight warm side key is fitted to
    barrel, stock and forend highlights together; all parts share it and the
    paper's measured color is retained. No per-part grading.

    The used/unused audit correctly rejects 48/255 reflection-factor leakage
    onto the forend latch, iron and web. Their RGB, normals, roughness and
    metallic are unchanged. The assembled scalar projection had selected
    neighboring wooden cutter tips. Capture reflection in the kit's already
    isolated named-part scene instead, retaining the independent first-pass
    owner witness. Only AO comes from assembled contact groups. The strict
    outside-site material assertion is retained, including alpha.

    A clearly marked interim calibration under repository
    `build/look1/interim-wear/` uses the actual site-off GLBs and preserves all
    their accessors; it is not accepted delivery evidence while that audit
    fails. Its nine visible fractions are 12.45/13.39 carry, .68/.72 muzzle,
    63.06/57.28 case, 32.84/30.20 thumb, 47.90/35.23 guard,
    4.82/1.64 wrist, 33.45/5.90 forend points, .46/.57 toe and
    3.04/3.45 forend edges. The broad hand fields now cover plausible contact
    areas, but far too many diamond tips flatten and their filtered changes
    still merge. Reduce per-point hardness selection, not the hand footprint,
    then inspect both final native 2D fields. Narrow the guard's physical inner
    contact strip, reduce case fade/lever pressure extent and adjust the toe
    and edge impact sizes modestly. All accepted geometry remains unchanged.


12. **Correct the area measurement and the bow's contact path. Color and
    value:** pass twelve's retained-blue barrel pair, safety, top lever and
    brass bead pass every requested gate. Walnut reaches its main value ranges,
    with small highlight residuals; shared side key 33.8 W improves the forend's
    entire histogram without changing its albedo. The action remains slightly
    low after reducing the faded area. Increase only the handled gray response
    within a realistic oxidized-steel range. Keep the macro's common neutral
    three-light setup; its 6% light trial pushed the lever median to the upper
    tolerance without quite matching the action. Do not accept that joint fit.

    The corrected isolated scalar capture passes all 10,642,945 owner-covered
    texels with zero misses. The nine used/site-off exports preserve every
    accessor. Outside-site interiors measure RGB/alpha 0, normal one 16-bit
    code and roughness/metallic one 8-bit code, with zero boundary outliers.
    `make -C guns/sxs` completes successfully in `build/look1/make-pass12.log`.
    That build success does not establish wear acceptance.

    The native 2D pair exposes a measurement error: one-pixel erosion removes
    much of the thin guard from the 1600-pixel denominator. Use **complete
    visible-part masks without erosion** for area, retaining the former
    erosion result only as a diagnostic. The sealed pass-twelve 4000-pixel
    fractions with complete masks are carry 11.36/13.39%, muzzle .87/.72%,
    case 57.69/57.28%, thumb 27.13/30.20%, guard 14.68/35.23%,
    wrist .99/1.64%, forend points 3.04/5.90%, toe .55/.57% and
    forend edges 3.57/3.45%. Archive the earlier 1600 measurements rather than
    presenting their different denominators as matching area.

    The bow's rub is also visibly a short bottom strip. Its former rear normal
    gate faces the wrong way, the front curve lies outside the intervals, and
    a fixed X strip misses the narrower rear band. Follow the actual formed
    width, select the rear +Y / floor +Z / front -Y inner surfaces and retain
    the dark outer face. Match a continuous C-shaped rub, not a brighter bottom
    line. Increase individual worn-tip selection within the unchanged hand
    footprints; native masks already resolve separate tips, but too few of
    them. Adjust carry/muzzle extent and thumb contact length against complete
    part area. No accepted vertex, pivot or clip changes.

    The primary hero and wear proof now use 4000 pixels so that the guard and
    checker tips are resolved for photographic acceptance. The old 1600 outputs
    remain archived as filtering diagnostics. The shipped maps remain 2048,
    and source/export pairs still expose their actual filtering loss. Reuse
    byte-identical 4000-pixel on/off images for the native 2D layout, checking
    source SHA, renderer signature, camera, sample count and resolution; never
    upscale an image to manufacture native evidence.


13. **Reject closed pore cells in grazing light. Color and value:** the new
    4000-pixel exported close-ups retain deep blue-black tubes, warm walnut
    and silver-gray handled case fields, without a pale overall wash. The
    guard's continuous inner C-shaped rub is now visible around both curves;
    area acceptance awaits its complete-part exported on/off proof.
    The walnut fails a closer photographic comparison: on front-facing wood
    and the comb, the elongated Voronoi boundary network closes into coarse
    cells and reads like embossed leather. `look-field-13.jpg` instead shows
    fine open pores and longitudinal dark streaks. The gray-paper wrist macro
    confirms the direction; its neutral balance is unchanged. Reject the
    closed network. Test longitudinal soft fiber bundles and smaller vessel
    apertures, retaining annual growth, oil response, cutter pitch/borders and
    all original contact wear. Published walnut vessel measurements in the
    reference register constrain the new pore diameter; they do not supply
    texture pixels. No geometry is changed. This source-only trial is not
    delivery acceptance; its baked export must be judged again.


    The sealed pass-thirteen build completes with exit 0. Complete visible-part
    wear fractions, ours/photo: carry 13.42/13.39%, muzzle .74/.72%,
    action 58.07/57.28%, thumb 29.47/30.20%, guard 24.74/35.23%,
    wrist 1.65/1.64%, forend points 5.06/5.90%, toe .54/.57%,
    forend edges 3.57/3.45%. These counts do not override the 2D sheets:
    the carry field is too oval and short; the forend's bright tips sit too
    far down the cheek, whereas the photo concentrates them on the upper,
    rear gripping flank. The guard is now one continuous C, but too narrow.
    Its largest connected worn region occupies about 24% of the part, against
    the photo's 35%; the native boundary uncertainty remains 19–51%.
    Keep the original pressure causes, revise their footprints, and do not
    accept matching area alone. Exact source/export and all render evidence
    are preserved under repository `build/look1/pass13/` and
    `renders/look1/pass13/`.

14. **Repair filtering and cutter construction before the next bake. Color
    and value:** pass thirteen passes all requested gates for walnut, safety,
    lever and bead. The action median is still 104.9/118.5, the guard
    34.8/51.3, and the retained-blue barrel P90 is 100.0/86.4 (ours/photo).
    Source tests increase handled case gray within an oxidized-steel range;
    median reaches 108.2 while its protected oxide and highlights stay in
    range. A slightly warmer, lower-value barrel rub reduces its cool upper
    tail without changing the intact blue shared with the pump. The revised
    longitudinal wood source reaches stock 71.7/111.3/175.1/193.0 and
    forend 33.7/62.6/108.5/122.5 (P10/median/P90/highlight). These are
    source diagnostics, not accepted exported measurements.

    The source/export macro also exposes a bright zipper at the action's
    constant-X land boundary. Turning off the normal map removes it. At 26
    affected ground-side samples, the delivered filtered normal deviates as
    much as 37.18 degrees; separating the original ground-side UV charts and
    projecting the same dense source reduces that to .00966 degrees. The
    preview removes the vertical zipper. Repack at unchanged texture size,
    retain all vertices/triangles and normal fans, and verify the rebaked
    export again. This is a UV/filtering repair, not a head-form change.

    Native photographic checker crops show elongated diamonds along the
    grain, approximately 3:1, not the current nearly square 1.33:1 cuts.
    Change the original cutter normals to (.32, ±sqrt(1−.32²)); they remain
    unit length, so perpendicular pitch remains exactly 1.27 mm / 20 LPI.
    Move forend pressure toward the upper cheeks and rear grip while retaining
    individual point hardness and dark unhandled grooves. Keep stock-toe and
    forend impact sites local. The open view's headstamp is too soft: increase
    ammunition UV priority from 1.2 to 2.0 and use heavier original open-font
    lettering. Trial ammunition density rises from 1708 to 2545 texels/m;
    the forend retains 5.66 texels per cutter pitch and stock keeps its own
    unchanged region. Each final detachable must still pass the lossless
    512-subset audit.

    Reflection trials remain diagnostics. A physically placed opposite-side
    strip can brighten the inner guard without washing out the triggers or
    lever, but a broad strip overlights too much of its land. Narrow its
    angular footprint and inspect all controls together; no selective image
    grading or per-part exposure is allowed. Final light settings and any
    remaining miss will be recorded with the actual exported pairs.


    The useful guard correction is its intact surface, not more fill. The
    former .285 roughness spread the reflected slit over too much of the
    broad inner land. Uniform .18 polished blue gives source P10/median/P90/
    highlight 7.1/55.9/170.1/237.0, versus 11.0/51.3/170.0/238.6 in
    the photograph. A .17 inner polish with .25 on the narrow filed outer
    faces gives 8.1/54.4/161.8/237.6; only P10 still misses. Preserve the
    inner polish and test .34 on the filed edges in the actual next export.
    Base blue stays .035/.037/.039 linear; pressure maxima reach bare steel,
    with cubic progressive thinning in the surrounding rub. The 0.26 W,
    140 × 1 mm reflected slit and its upper barn door are explicit camera
    metadata, identically present in source and export. Lowering the door's
    bottom to −13.5 mm stops the unwanted trigger reflection. The rejected
    extra front card brightens the triggers and is not retained.

    Source triggers reach 16.1/23.9/64.2/109.9 against photo
    6.1/24.5/61.1/110.9: their low-decile mismatch remains clearly localized
    to broad protected blade faces in the cyan overlay. The other values
    match. Do not force their real blued-steel color toward zero to imitate
    a different maker's thin, partly shadowed profiles. The lever's slightly
    darker protected blue gives source 18.6/57.7/187.6/227.4 with its
    bright pressure field retained. All of these are pre-bake source results.

    The carry field now merges three overlapping carrying positions into a
    long, thin rub rather than one oval; a source on/off pair confirms that
    structure. Reduce its vertical half-width from 9 to 8.1 mm after the
    source total barrel-use fraction measures 15.64% including the muzzle.
    Worn forend points move to the upper/rear gripping cheeks, and the
    original 3:1 diamonds now read as short longitudinal tips rather than
    round sparkles. Final worn fractions still require the independent
    4096 bakes and actual 2048 site-off exports. No accepted vertex, pivot,
    clip, original form camera or contact tolerance changes.


15. **Reject fraction-only guard and forend matches. Color and value:** the
    pass-fourteen exported case action, lever, safety, guard, stock and forend
    meet every requested value and highlight-color gate. The retained-blue
    barrel still misses its median (35.6/29.0), and the bead its low decile
    (55.4/68.5). A camera check reveals that the barrel photograph is almost
    side-on; the old above-side camera exposes too much of the second tube.
    A near-level comparison improves rigid-landmark RMS from 7.01 to 5.74
    pixels. With neutral room strength .98, the actual export measures
    15.6/28.9/94.4/145.9 versus 17.0/29.0/86.4/153.5, and its highlight
    RGB 142.7/146.7/146.9 versus 155.3/153.3/149.8. Every gate passes.
    This is a review camera/light correction; original accepted form cameras
    and the shared studio are unchanged. The alternative 5.47-pixel camera
    retains a larger upper-tail miss and is rejected.

    A small physical fill ahead of the muzzles, below the bead center, lifts
    its shadowed lower hemisphere without changing brass color. At .04 W the
    actual export reaches 58.6/176.6/222.5/242.6 versus
    68.5/160.8/246.7/254.0, highlight RGB 247.7/242.2/230.8 versus
    254.9/253.7/254.1. These all meet the stated tolerances, though median
    and low tail remain near their limits. Larger fill overlights the median;
    a below-barrel fill is blocked and has little effect. Keep the accepted
    raised foot and round bead. Correct a review annotation: the measured
    Front_Bead mask contains the round bead only; its separate foot appears
    in context but was never part of that denominator.

    The three camera-side trigger-shade trials lower P10 only to roughly
    13–14 against 6.1 while losing the matching median/highlight and the
    guard low tail. Reject them. The original broad blade faces remain
    fully measured; no near-zero steel color or selectively omitted dark
    pixels are justified. The source/export pair localizes this remaining
    low-tail mismatch. A passing median alone does not accept that finish.

    Complete-part on/off export fractions are carry 13.81/13.39%, muzzle
    .74/.72%, case 59.13/57.28%, thumb 29.51/30.20%, guard
    23.05/35.23%, wrist 1.68/1.64%, forend points 5.49/5.90%, toe
    .55/.57% and forend edges 3.69/3.45%. The carry now reads as one
    long thin field, with a similar length and one connected worn region;
    accept its placement rather than only its area. Muzzle thinning remains
    confined to the end rim. Toe and forend impacts remain a few local,
    original compressed bowls and broken lips, with intact surrounding oil.

    Reject the guard and forend pressure distribution. The inner bow has
    too little actual material change along its rear curve, despite a bright
    reflection already present in the unused polished blue. Broaden the
    physical contact field and test rear/front pressure through the bends.
    The source baseline independently measures 22.37%, close to the exported
    23.05%; this is a source pressure problem. The forend tips spread too
    far down the cheek even though their area nearly matches. Concentrate
    contact in a narrower upper hand field and increase the selected-tip
    density there, retaining dark grooves and unhandled borders. The first
    narrow-field source trial measures 5.26%; its more concentrated 2D
    structure is useful, but only the next baked export can establish the
    final area, visibility and filtered shape.


    The wider guard trial reaches source 33.95% against photo 35.23%,
    but its P10/median rise to 19.1/59.4 against 11.0/51.3. Reject the
    finish despite improved area. A deeper protected blue, .020/.022/.024
    linear, with a 1.3-mm contact core and stronger pressure around the two
    bends, gives 33.23% and 12.9/53.6/167.0/233.6. Keep its complete C
    structure and lower protected blue modestly to .016/.018/.020 for the
    next full bake; no pure-black color is introduced. The bright core stays
    real steel. The forend's 10-mm vertical hand-field trial at .55 point
    selection reaches 6.24%; use .52 between the measured .48 and .55
    trials, retaining separate elongated tips and the intact cut valleys.
    These are source diagnoses. Final acceptance requires fresh exported
    values and all nine actual on/off images after the next bake.


    The completed fresh kit archive ran every one of its 24 test modules
    successfully. Current kit source hashes still equal that archive. The
    GPU-selection fixture requires Blender indirectly through `kit.gpu`;
    an additional system-Python invocation fails at the missing `bpy` import,
    before running a test. Its correct Blender invocation in the clean suite
    ran all four cases successfully. No package installation or kit change
    is needed. Full commands and results are retained in
    `build/kit-specular-suite/build/results/results.json` at repository root.


16. **Color and value, then audit what is actually damage:** pass fifteen's
    exported retained bluing, case, lever, safety, guard, stock, forend and
    bead meet every requested finish gate. The triggers retain their
    disclosed P10 miss; other trigger values still match. The more complete
    guard contact field measures 37.41/35.23%, with a continuous inner bow;
    the forend tips measure 6.39/5.90%, now concentrated higher on the cheek.
    These improvements do not excuse erroneous photographic annotations.

    The native lower-stock crop exposes a fitted metal inlay, mistakenly
    included in the former toe-damage mask. Exclude it. Actual chipped and
    compressed heel/toe edges occupy **0.2673%**, not 0.5728%, of the full
    visible stock (1,787 of 668,631 native pixels). Cross-view inspection
    also identifies a slotted forend screw in a former ding polygon; the
    other polygons select intact grain rather than clear impact damage.
    Reject that entire 3.45% forend-edge target. Keep the old masks and their
    failed interpretation in the archived rounds; never call hardware wear.

    The existing sharper `look-gray-used.jpg` shows a definite fractured
    barrel-facing wood rim beside the forward checker point. The complete
    visible wooden forend, excluding its fitted latch, supplies the new
    denominator. Only the unambiguous fracture is counted: **0.1640%**,
    384 of 234,155 native pixels. Balance its upper-left neutral gray
    studio paper, native rectangle (40,40)–(500,300), linear gains
    (.94134,1.01711,1.01711). No photographic pixel enters a material.

    Rebuild the original impacts at these lower densities: reduce the large
    toe bowl; replace oversized end bowls with small original fractures at
    the barrel-facing rim and ends. The first source trial puts them so high
    the barrel hides every changed pixel: 0% is rejected. Move the impacts
    slightly onto the visible upper cheek, retaining their edge cause.

    A proposed height partition would require an artificial unhandled gap
    in the hand field. Reject it. The fracture and point fields can physically
    overlap. Two additional 4096 kit bakes disable just one forend cause each;
    use that whole-part counterfactual for its evidence export, keeping the
    other cause active. The other seven fields retain disjoint all-clean
    regions. Integer atlas copying preserves every untouched used texel;
    every GLB accessor must still match. These extra textures are evidence
    only; one 2048 set ships. Preserve every accepted vertex, original rig,
    clip, pivot, form camera and triangle. Both source trials and the fresh
    baked export require inspection; the old area agreement is withdrawn.

    The revised 4000-pixel source on/off trial measures 0.15336% visible
    forend impacts, 0.29089% toe impacts and 5.42820% forend point wear.
    The fractures now interrupt a few upper-edge fibers instead of forming
    broad pale bowls; the toe has three small local compressed/chipped sites.
    Opened all three side-by-side crops and their difference fields. This
    is still source evidence; the shipped-map footprint must be measured
    independently after the 4096-to-2048 reduction.


17. **Color and value on the fresh export:** eight of nine primary finishes
    satisfy all requested whole-part luma and highlight-RGB gates. The stock
    is 72.49/109.45/175.30/192.81 versus 63.74/111.65/176.76/201.61;
    the forend is 37.52/62.29/107.70/122.06 versus
    35.76/57.28/103.45/125.95 (P10/median/P90/highlight, 0–255).
    The trigger P10 remains 17.07 versus 6.07; its median, upper tail and
    highlight agree. The cyan quantile overlay locates the miss on our broad
    accepted blade faces versus the photograph's thin shadowed profiles.
    Source and export both miss: mean source/export RGB difference is only
    about 1.1 levels. Keep the actual low-tail failure visible; do not claim
    a ninth pass or lower real steel reflectivity to pure black.

    Opened every fresh studio view, including both heroes, turnaround,
    shooter, aimed, open, breech, wood/metal details and scale, plus Eevee
    and both ammunition renders. On gray the barrels remain deep blue-black,
    the underside and bow retain dark cavities, and highlights roll across
    the turned fences and oil wood. Original 20-LPI cuts, borders, flattened
    tops and dark valleys survive. The macro source/photo/export pairs show
    the real limits: our walnut's fine grain is stronger and more regular
    than the photographed stock, case mottle has different placement and
    stronger blue islands, and the safety cuts/headstamp soften at delivery
    resolution. Passing histograms do not erase those visual differences.
    The bead/safety/deep-blue metallic neutrals are estimates; their lighting
    and small photographic cross-sections make them weaker evidence than the
    gray-paper action and whole-stock pairs. The older gray-barrel pair
    remains an explicit contextual miss, not a match for retained rust blue.

    The complete 4096 used bake and separate `make check` passed. Final
    causal wear evidence is still being rebuilt at this journal checkpoint;
    its final fractions and 2D review are recorded below when complete.


18. **Color and value, then final causal wear review:** the complete build
    retains the eight primary finish passes and the disclosed trigger P10
    failure. The actual foreground hero has P1/P50/P99 luma
    0.00/57.40/214.84, 13.43% below eight, zero all-channel clipping and
    0.000414% with any channel at 254 or above. Dark cavities remain deep;
    neither this tonal check nor successful delivery checks substitutes for
    the photograph pairs.

    Opened all nine full-frame/crop/difference pairs and all nine native 2D
    pairs. The carry field is one elongated gray area around the balance,
    with protected blue along the rest of the tubes. Muzzle wear is confined
    to narrow gray end rims. Handled action flats form a broad faded field,
    leaving oxide around the returns; the accepted head and the photo's
    separate plates/fences divide that field differently. The lever has a
    merged bright thumb-contact land and a dark neck. The guard now has one
    continuous rubbed inner bow, with small separate edge fragments; its
    accepted broad flat land projects a thicker lower strip than the photo's
    thin rounded band. The intact outside margins stay dark. These are 2D
    structural observations, not acceptance by equal region counts.

    The wrist and upper forend hand fields contain distinct polished cutter
    tops, not uniform pale overlays, with their grooves and borders intact.
    Their connected-region counts differ from the native photographs, whose
    projected tip sizes and stock forms also differ. Forend point wear is
    6.07/5.90%; the broad-hand field survives the bake without being replaced
    by a few isolated bright dots. Toe/heel damage is three small localized
    compressed/chipped edge sites, 0.29132/0.26726%. Forend edge damage is
    three small original fiber fractures, largest near the upper rim,
    0.16143/0.16399%; the photo's single clear rim chip remains the independent
    reference. Neither fitted hardware nor intact grain is counted. These
    impacts are minor in the 4000-pixel whole-gun hero, as their very small
    photographic area requires; do not imply they are conspicuous in a
    contact-sheet thumbnail. Native boundaries and RGB thresholds remain
    sensitivity bands, not precise physical surface-area measurements.

    Both overlapping forend causes use their own single-cause-off 4096 kit
    bake, preserving the other cause. Source flags and projection hashes are
    checked. All nine evidence GLBs preserve every geometry, UV, skin and
    animation accessor. Independent other-part interior comparisons stay
    within one 8-bit color/roughness/metallic code and approximately one RGB16
    normal code. Every untouched pixel in the actual evidence exports is
    copied exactly from the used maps. The all-clean/used comparison retains
    five color and two ORM chart-boundary outliers, with coordinates and
    maxima in `build/wear/variants.json`; no occupied interior exception is
    hidden. Contact AO is assembled and can legitimately differ outside use.

    Opened the current 51-panel contact sheet and three-gun studio comparison.
    The exact same lights, camera, exposure and scale show compatible deep
    black bluing across Covey, Hearth and Bracken. Covey's walnut is warmer,
    more amber and more strongly grained than Hearth's muted stock, closer
    to Bracken's brown wood. It is not an exact family walnut color match;
    the balanced used-stock pair remains its finish target. All three actual
    export hashes and unchanged studio settings are retained.

## Final build proof and scope

`make -C guns/sxs` completed with exit 0, including all renders and evidence.
The separately invoked `make -C guns/sxs check` also completed with exit 0.
Root-local transcripts: `build/look1/make-pass16.log` and
`build/look1/check-pass16.log`, with their corresponding `*-result.json` files.
The source and fresh-import checks cover topology, dimensions, UVs, normals,
19 clips, actual-surface contacts, motion clearances, sight visibility and the
51-angle lever sweep. Deterministic rebuild agrees on all 104 recorded entries.
The 1,715 affine samples separately establish serialization fidelity.
`python3 kit/repo_check.py` reports 1,111 source files and zero errors.

No accepted form vertex, pivot, clip or original form camera changed. The
bake-revealed repair separates 103 ground-side UV faces from the curved
returns: 44 joined ground boundaries become zero, with the geometry hash
unchanged. Correct named-part projection prevents neighboring steel/wood from
contaminating one another, including the reflection scalar. RGB16 shipped
normals retain continuous forging reflections. Higher ammunition UV priority
and a bolder installed-font headstamp improve the small delivery maps; these
are UV, shader and marking changes, not alterations to the accepted shell.
The open 2.469-mm and top wood-line 3.293-mm residuals remain as accepted.

Shell: 752 triangles, 624,480 bytes, three lossless 512 PNG subsets.
Fired hull: 480 triangles, 744,848 bytes, the same layout and RGB16 normal
precision. `texture_size=512` and `texture_clusters=True` use the kit path.
Independent oriented-geometry, tangent-frame, material, density and L0–L3
pointwise mip audits pass against full-atlas snapshots. Exact copied texels
are lossless; the hull's float32 UV serialization still has a maximum
3.05176e-5-pixel transform roundoff and about 1.20e-6 sampled normal difference.
That roundoff is disclosed, not labeled literally zero surface error.

Shared kit work, in separate commits: preserve RGB16 precision through
lossless detachable clustering and its comparison; optionally carry opaque
`KHR_materials_specular` data in existing BaseColor alpha, reusing the same
image and sampler. Previous defaults remain. Every `kit/test_*.py` module ran
sequentially from a fresh build, all 24 exit 0; GPU fixtures used
`kit/with_gpu.sh`. The runner and exact commands/results are at repository
`build/kit-specular-suite/run-tests.py` and
`build/kit-specular-suite/build/results/results.json`. Current kit source
hashes equal that tested archive. No shared gun modeling file changed.

No docs JPGs or GIF were generated or committed. Render outputs, bakes, GLBs
and downloaded references remain ignored. Nothing is pushed. No additional
tool is needed. A future general kit API for multiple isolated scalar captures
would remove this asset's dependence on the existing bake scene/node names.
The primary remaining weaknesses are the trigger low tail, stronger original
wood/case texture character, small-photo metallic neutral uncertainty, and
normal/headstamp filtering at the fixed delivery resolutions. Importers must
support `KHR_materials_specular` and should check their own normal compression.


## Whole-part finish values

Generated local pairs are in `renders/final/look-review/`; artifacts are rebuilt, not committed.

Actual exported GLB SHA256: `97d981c13569411e1c3a72fc299a4aa28699af082fbcefd4ba01dc273f8b4d5b`. Values are Rec.709 display luma in 0–255; the highlight is the mean of the brightest 5%. Every row is ours / balanced native photograph. One-pixel AA boundaries are excluded from rendered finish samples; complete visible-part denominators are retained for wear. No per-part exposure, normalization or grading.

| Finish and pair | P10 | Median | P90 | Highlight | Highlight RGB | Gates |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Retained rust blue (`barrels_deep_blue-pair.jpg`) | 15.6 / 17.0 | 28.9 / 29.0 | 94.4 / 86.4 | 145.9 / 153.5 | (142.7,146.7,146.9) / (155.3,153.3,149.8) | all |
| Faded case action (`case_action-pair.jpg`) | 66.6 / 61.1 | 108.6 / 118.5 | 144.6 / 157.9 | 203.5 / 205.2 | (205.2,203.5,199.1) / (210.8,204.4,196.9) | all |
| Blued top lever (`top_lever-pair.jpg`) | 18.8 / 20.1 | 60.6 / 55.3 | 187.6 / 188.1 | 229.6 / 246.2 | (228.3,229.8,230.8) / (244.6,246.9,243.9) | all |
| Safety steel (`safety-pair.jpg`) | 39.0 / 35.9 | 68.8 / 75.4 | 152.1 / 147.3 | 206.8 / 200.6 | (208.2,206.8,202.1) / (206.0,199.8,192.5) | all |
| Blued triggers (`triggers-pair.jpg`) | 17.1 / 6.1 | 25.7 / 24.5 | 65.0 / 61.1 | 111.9 / 110.9 | (112.6,111.4,114.8) / (115.6,109.6,110.2) | p10 +181.3% |
| Blued guard (`guard-pair.jpg`) | 10.4 / 11.0 | 52.9 / 51.3 | 173.5 / 170.0 | 232.0 / 238.6 | (230.8,232.3,233.5) / (240.5,238.4,234.9) | all |
| Walnut stock (`walnut_stock-pair.jpg`) | 72.5 / 63.7 | 109.5 / 111.7 | 175.3 / 176.8 | 192.8 / 201.6 | (206.5,189.6,183.8) / (228.5,196.5,173.3) | all |
| Walnut forend (`walnut_forend-pair.jpg`) | 37.5 / 35.8 | 62.3 / 57.3 | 107.7 / 103.5 | 122.1 / 125.9 | (159.6,113.7,94.4) / (158.9,118.9,98.6) | all |
| Brass bead (`brass_bead-pair.jpg`) | 58.6 / 68.5 | 176.6 / 160.8 | 222.5 / 246.7 | 242.6 / 254.0 | (247.7,242.2,230.8) / (254.9,253.7,254.1) | all |
| Older gray-barrel context (`barrels-pair.jpg`) | 7.0 / 14.1 | 35.4 / 59.3 | 174.8 / 132.4 | 194.2 / 203.1 | (193.6,194.4,194.4) / (206.4,202.8,197.3) | p10 -50.5%; median -40.3%; p90 +32.1% |

## Visible wear fractions and 2D evidence

Full-frame and cropped on/off pairs: `renders/final/wear/<site>-on-off-pair.jpg`. Native 2D pairs: `renders/final/wear-native/`.

Complete projected named-part area; worn pixels change by at least 6 RGB levels between the actual used and site-off GLBs. Every site-off export preserves all accessors. The photographs use independent native annotations; reflection/threshold and one-pixel boundary uncertainty remain in each pair. Counts describe 8-connected worn and remaining regions at a common 800-pixel longest-part scale; they are evidence, never an acceptance gate.

| Site and full-frame on/off pair | Ours % | Photo % | Delta pp | Native 2D pair | Worn regions ours/photo | Remaining regions ours/photo |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| `barrel_carry` | 13.82 | 13.39 | +0.43 | `barrel_carry-native-2d-pair.jpg` | 1/1 | 8/1 |
| `muzzles` | 0.74 | 0.72 | +0.02 | `muzzles-native-2d-pair.jpg` | 3/1 | 2/2 |
| `action_fade` | 59.24 | 57.28 | +1.96 | `action_fade-native-2d-pair.jpg` | 14/5 | 29/1 |
| `lever_thumb` | 29.51 | 30.20 | -0.69 | `lever_thumb-native-2d-pair.jpg` | 1/2 | 1/11 |
| `guard_fingers` | 37.41 | 35.23 | +2.18 | `guard_fingers-native-2d-pair.jpg` | 10/1 | 5/74 |
| `wrist_points` | 1.68 | 1.64 | +0.04 | `wrist_points-native-2d-pair.jpg` | 159/555 | 8/1 |
| `forend_points` | 6.07 | 5.90 | +0.17 | `forend_points-native-2d-pair.jpg` | 99/219 | 1/4 |
| `stock_toe` | 0.29 | 0.27 | +0.02 | `stock_toe-native-2d-pair.jpg` | 3/2 | 9/2 |
| `forend_edges` | 0.16 | 0.16 | -0.00 | `forend_edges-native-2d-pair.jpg` | 3/1 | 1/1 |

## Actual delivered files

| File | Bytes |
| --- | ---: |
| `export/shell.glb` | 624,480 |
| `export/hull.glb` | 744,848 |
| `export/sxs.glb` | 19,674,244 |
| `textures/T_Covey26_BaseColor.png` | 3,450,993 |
| `textures/T_Covey26_Normal.png` | 10,590,347 |
| `textures/T_Covey26_ORM.png` | 2,656,055 |

38,822 triangles; 54 named parts, 17 bones, 19 clips, 14 sockets; 1 atlas material; three 2048 images, PNG channel precision [8, 16, 8].
Fresh imported UV coverage is 43.4285%; overlap fraction is 0.0000012470,
with no degenerate or out-of-bounds triangles. Measured density P5/50/P95 is
1,034.4 / 3,226.5 / 4,561.8 texels per meter. Median delivered texels per
construction pitch: wrist 4.102, forend 5.693, safety 9.067. The checker cutter
pitch is the original 1.27 mm (20 LPI).

The 1,715 serialization samples have a maximum position error of
1.90828e-7 m; this is export fidelity, separate from the actual assembly checks.



---

# Covey 26 — form round 7: turned and milled head

Round six's favorable fairness judgments are superseded by the owner's round-seven
review. Its complete source, export and image baseline is preserved locally in
`build/round7/before/` at repository root. Main merged cleanly before changes.
No finish work or docs images are authorized in this round.

## Round 7 critique passes

43. **Baseline and first distance-union source, rejected.** Color/value: the
    dark inspection constants are unchanged. The black-backed dealer photos
    have no defensible neutral, so unity balance remains; no hue acceptance.
    Opened both full-resolution source/export stripe sheets, the ordinary
    open-head comparison and both requested photo pairs. Longitudinal bands
    expose small closed islands and saddles; transverse bands expose the
    two rear-centered cushions. These are present in the source. The old
    adjacent-face-angle results cannot establish fairness at this wavelength.
    Replaced all free height controls with original turned fence primitives,
    ground-side/roof planes, a circular center land and compact distance
    blends. Opened all ten first source stripe crops. The small cage waves
    are reduced, but the transverse loops still center behind the breech:
    reject. The base roof and union flatten the fence's rear fall. The next
    trial uses one concave turned meridian whose axial slope never returns
    to zero behind its crown, and a narrower blend support. First actual
    sections also show the extra inflections; these remain visible in the
    diagnostics and are not excused by topology or a normal-angle percentile.

44. **Turned fall, center datum and front circles.** Color/value: same held
    dark-steel constants and unity-balanced black-background references.
    Opened both band directions from the top and open cameras in source
    trials 2–4. Trial 2's closed transverse loops still center behind the
    face. Trial 3 carries the turned meridian to the wood but keeps the
    level center land; that land rises above the falling fences and adds
    an unphotographed central ridge. Reject the level rear datum. Trial 4
    keeps Z55.59 at the front and inclines the cylindrical land rearward
    at 0.32 mm/mm. Its measured uninterrupted rear land is Z50.982 at
    Y100.6, a 4.608 mm change from round six. The native top reference shows
    the strongest fence highlights beside the barrels and a broad fall
    toward the lever; it does not show the old raised land surrounded by
    lower cushions. This is photographic form evidence, with uncalibrated
    light and the camera/outline gate still pending, not a metric height scan.

    That trial's turned meridian is `r(d)=13.35 - 0.5*(sqrt(d*d+12.8*12.8)-12.8)`.
    Its axial slope and curvature have no secondary reversal. Transverse
    sections remain circles about the continued bore axes. Restored the
    constant front roof envelope: the inclined trial roof had intruded into
    the accepted circular sectors. Independent game-triangle arc fits now
    put their centers within 0.022 mm of the bores in that trial. Side return remains R6;
    the unchanged lower construction, bushings, controls and rig remain.
    All 246 source contact probes and the complete half-frame/lever sweeps
    pass without adding any contact exception. The source has 38,822 tris.

    The old 18.7 mm finite endpoint/degree-five fit and R7.18 at Y96.5–102
    describe the rejected leveling-off construction. The new continuing
    turn fits an equivalent front ellipse length about 20.3–21.2 mm and an
    equivalent local circle about R124 there. These are observations of
    different profiles, not new fillet constants. A 0.10 mm rise above a
    level rear baseline no longer identifies the return on an inclined
    surface; retain it only as a clearly labeled legacy observation. The
    actual rear wood boundary is measured from rear-facing triangles.
    Adjacent-face angles remain a tessellation check, never fairness proof.


45. **Export control, reproducibility and blend rejection.** Color/value:
    unchanged inspection constants; black-background photo comparisons remain
    form-only. Opened the first baked top/open camera previews and all ten
    source stripe crops. The continuing front-to-rear turn removes the old
    small cage islands, but the 1 mm distance support makes the inner valley
    too tight. Its source triangles turn by about 25 degrees across one
    coarse transverse interval; the visible narrow converging bands, not
    that angle by itself, reject the shape. The hard side-envelope clip also
    leaves a small roof/ground-face crease. Widen the constructive blends.

    A complete independent rebuild initially fails only Action_Body. The
    dense sources differ at 59 vertices, up to 0.0057 mm: the 0.006 mm weld
    chooses either of two crown samples 0.0056 mm apart. Retain one fixed
    coordinate owner with bounded deterministic radius groups. Two fresh
    builds then match all 104 entries at the unchanged 1 nm position and
    five-decimal corner-normal tolerances. No test tolerance is relaxed.

    Opened every broad-blend trial-5 stripe crop. A rearward-varying central
    support introduces extra longitudinal islands, so reject it and keep one
    constant 3 mm central support. The ordinary rounded intersection also
    rounds coincident side planes inward: its envelope has no zero on those
    rays, folds the remesh and breaks the stock Boolean. The 35,023-triangle
    trial is rejected despite being manifold. The corrected side operation
    makes its support vanish as the transverse normals become parallel;
    the same 0.6 mm scale varies continuously along that return. The next
    source/export, image and contact gates must pass before this is accepted.

    Corrected a separate camera error: comparison crops had been treated as
    centered optical frames. Retain the original image center through crop
    shifts and verify it independently in Blender (maximum 0.0042 px
    disagreement in the two-camera trial). Rigid-only top RMS is 7.989 px,
    0.488 mm at head depth. The physically valid open fit remains 35.198 px,
    3.877 mm. Reversed-hemisphere low-error fits, alternate side labels,
    free-principal-point fits and exterior-rim/joint-pose trials are not
    acceptance. The open gate and independent outlines remain unresolved;
    additional verified rigid correspondences remain necessary. Outline
    observations never influence the camera solve or modeling.


46. **Constant joins, tangent sampling and section rejection.** Color/value:
    held inspection constants, procedural bands only; unity-balanced dealer
    macros remain form-only. Opened all ten source stripe crops from trials
    6, 7 and 9, both actual height/curvature plot sheets, and native top/open
    reference crops with observation grids. The outer union's rearward-varying
    width creates shallow millimeter waves; reject it and retain constant
    center/outer supports of 3/1 mm. Uniform-X interpolation flattens the
    vertical side tangent; replace it with 1,281 transverse-angle samples and
    0.05 mm Y spacing. This is numerical evaluation of the same zero field,
    not a height cage. Rebuilt source passes the unchanged strict 104-entry
    repeat comparison. Its topology is closed and consistently oriented.

    Sections expose a second flaw: the circular center cap makes two shallow
    troughs beside a center hump. Replace it with a milled inclined land,
    12 mm flat width, with R2 shoulders buried in the turned fences. The
    central valley now has one flat bottom. The R6 side/roof return's level
    rear roof also stops the fence fall before the wood. A shallow 0.10 slope
    in that roof continues the fall and keeps the old drop observations within
    their recorded photo uncertainty. Direct field comparisons at 0.10,
    0.15, 0.20, 0.25 and 0.32 distinguish this effect from lighting.

    The source trial still has broad rear-weighted transverse bands. Reject
    the long 12.8 mm axial crown scale. A 2 mm crown scale with asymptotic
    slope 0.30 concentrates the axial turn beside the breech and carries a
    near-conical fall to the wood. Its behind-return height is close to the
    previous trial; its equivalent front ellipse length deliberately changes.
    The photo's strongest front highlight and steady rear darkening motivate
    the localized crown. This is form evidence, not recovery of a 3D section
    from specular brightness. Increase transverse source sampling for the
    tighter manufactured joins; do not loosen the 12-degree mesh regression.


47. **Near-conical export rejected; front crown and hollow fall.** Color/value:
    unchanged inspection constants; black-backed photographs remain at unity
    balance and supply form evidence only. Opened the complete first 4096/2048
    source/export stripe sheets and native open before/after crop. That build
    passes its mechanical checks, but its near-conical fences remain as two
    raised rails behind the front. Reject it. Preserve that trial locally in
    `build/round7/near-cone/`. The new turned meridian has zero slope at the
    face, a short 1.2 mm crown scale, then an eased 2.5 mm hollow fall over a
    7 mm scale into a 0.30 rear slope. The actual maximum axial slope is now
    near Y111.35, close to the front highlight in the top photograph. This is
    a turned profile, not a set of independently placed roof heights.

48. **Buried milled edges and actual sections.** Color/value: same procedural
    reflection bands and steel constants. A narrow 12 mm flat central land
    exposes its R2 edges in the valley. A widening wedge also exposes them;
    actual transverse cuts show extra troughs. Reject both. The final central
    land is 25.2 mm wide, inclined 0.32 rearward, with its R2 edges buried under
    the turned crowns. Constant 1.5 mm central and 1 mm outer union supports
    replace the earlier varying widths. Opened all ten broad-land source
    stripe crops, both every-5-mm height/curvature sheets, and native photo
    grids. There are no former small cage islands on the central plane.
    Nested crown bands concentrate at the front. Long rake bands wrap the
    outer crown/return; this broad outer blend still needs the photographic
    registration rather than an automatic fairness claim. Curvature sign
    reversals remain fully recorded, including intervals spanning a planar
    land. A midpoint of such an interval is not a localized dent.

    The original recess outline, floor and R0.60 lip remain. No recess-floor
    lowering was used to accommodate a bad land. The independent build now
    matches all 104 strict entries. A round-six preservation audit also matches
    102/104 entries exactly: only Action_Body and its Stock_Walnut inlet differ.
    Rig, controls, barrels, other furniture, sockets and clips match exactly.

49. **Native camera observations and rejected low-error fit.** Color/value:
    no neutral or finish claim added. Inspected native top/open crops, observed
    grids, full pairs, projected curves and independent Workbench camera
    previews. The top fit uses the actual lever-tip and safety upper surfaces,
    rather than bone pivots, plus two breech corners and the rigid rib line.
    Its four-point RMS is 12.392 px / 0.825 mm; rib-line RMS 9.926 px / 0.661 mm.
    No guessed barrel highlight or head form is fitted.

    Open-rim observations were inspected at native resolution. A seven-point
    arc, rigid lines, controls and a lower breech corner produce a 4.131 px /
    0.492 mm free-principal-point trial. Independent projection agrees below
    0.001 px, but its rendered view shows the chambers and does not establish
    the photo's exterior-side correspondence. Reject that numerical result as
    camera acceptance. Refit with an explicit muzzle-side prior, both real
    safety detents, multiple focal starts and multiple initial view directions.
    Also inspect the true rounded lever tip and the safety's upper center,
    rather than points inside their pads. The constrained trials still exceed
    1 mm. Extending the partial rim down to its bottom roll does not fix this.
    Do not move accepted parts or fit head landmarks into the camera to hide it.

    Recover actual cap-boundary segments from the triangles for the wood joint.
    The former fixed-X/photo point pairs and 0.10 mm height departures were
    not valid outline correspondences. The native joint observations remain
    separate from rigid fitting. Some exceed 2 mm. The centerline is covered
    by the reference's different barrel extension, and the old return markers
    fall on engraving/highlight departures rather than an identifiable edge.
    These registration gates remain unresolved, not silently waived.


## Every-5-mm section audit, round 7

Opened both current plot sheets. Teal is the dense triangle surface; brown is
the game triangles. Curvature is measured over 0.8 mm at 0.05 mm sample spacing;
the sign floor stays 0.002/mm. Counts include a sign carried across a nearly
planar stretch. The JSON retains both ends of that bracket; its midpoint is
not necessarily a localized inflection. Abrupt recess/floor or rear-cap edges
are not smoothed away. No source/export count is suppressed.

| Direction / station mm | Dense / export changes | Dense event coordinates mm | Construction interpretation to review |
| --- | ---: | --- | --- |
| transverse 85 | 2 / 2 | -10.52, 10.53 | Wood line on either side of the strap. |
| transverse 90 | 6 / 6 | -10.75, -7.60, -6.37, 8.08, 8.88, 10.75 | Rear land/wood return and recess lip/floor; outer ±10.75 still unregistered. |
| transverse 95 | 10 / 10 | -19.12, -16.42, -10.32, -7.02, -5.87, 5.88, 7.03, 10.33, 16.43, 19.13 | Outer returns, valley, recess lip; wood-line endpoints. |
| transverse 100 | 10 / 12 | -19.92, -18.12, -9.95, -4.45, -0.92, 0.93, 4.45, 9.95, 18.13, 19.93 | Outer returns and valley; short recess-front lip. Long central brackets span the plane. |
| transverse 105 | 6 / 10 | -21.52, -19.95, -9.35, 9.35, 19.95, 21.53 | Outer return pairs and two valley shoulders; no recess intersection. |
| transverse 110 | 6 / 8 | -23.77, -22.52, -8.25, 8.25, 22.53, 23.78 | Outer return pairs and valley shoulders beside the front turn. |
| transverse 115 | 2 / 2 | -7.15, 7.15 | Only the two valley shoulders at the front crowns (actual Y114.8). |
| longitudinal -25 | 2 / 2 | 102.82, 113.55 | Rear wood-edge/plane bracket and front crown roll. |
| longitudinal -20 | 4 / 16 | 97.70, 105.30, 108.22, 110.52 | Wood/outer-return departure, outer blend and front crown; intermediate reversals remain unregistered. |
| longitudinal -15 | 4 / 20 | 90.62, 92.70, 95.57, 111.50 | Wood return, outer-blend/plane brackets, front crown roll. |
| longitudinal -10 | 2 / 4 | 87.82, 111.62 | Wood-line blend and front-crown transition across a nearly planar meridian. |
| longitudinal -5 | 6 / 10 | 86.77, 90.42, 95.55, 97.17, 103.47, 112.80 | Recess heel, floor/lip, plane-to-crown brackets; long zero-curvature intervals retain both feature ends. |
| longitudinal 0 | 1 / 1 | 86.27 | Recess rear heel; center land stays planar ahead of the lip. |
| longitudinal 5 | 6 / 8 | 86.47, 90.27, 95.55, 97.17, 103.45, 112.77 | Recess heel, floor/lip, plane-to-crown brackets; long zero-curvature intervals retain both feature ends. |
| longitudinal 10 | 2 / 8 | 87.82, 111.62 | Wood-line blend and front-crown transition across a nearly planar meridian. |
| longitudinal 15 | 4 / 13 | 90.62, 92.70, 95.57, 111.50 | Wood return, outer-blend/plane brackets, front crown roll. |
| longitudinal 20 | 4 / 12 | 97.70, 105.35, 108.17, 110.57 | Wood/outer-return departure, outer blend and front crown; intermediate reversals remain unregistered. |
| longitudinal 25 | 2 / 2 | 102.80, 113.55 | Rear wood-edge/plane bracket and front crown roll. |

55 dense events remain without verified photographic attribution in the raw
report. The interpretation column names the constructive surfaces, not a
waiver of the requested photo-feature criterion. In particular the outer
fence/base fillets have additional convex/concave transitions. They cannot be
certified from an unsolved open pair. Additional game-mesh reversals on the
nearly planar intervals are triangulation error; that explanation does not
turn them into photographed features or erase them from the count. **The
strict section/fairness acceptance is incomplete.**

Plots: [transverse height and curvature](renders/checkpoint/curvature/transverse.png),
[longitudinal height and curvature](renders/checkpoint/curvature/longitudinal.png).
Every sample, feature distance and reversal bracket is in the adjacent
`sections.json`. Source geometric face-angle maxima and monotone bore rays
remain regression checks only; they are not a replacement for these plots.

## Round-five observations retained or deliberately changed

The README lists the complete current measurements and photographic uncertainty.
This table makes the departures from the delivered round-six evaluation explicit.
Values are millimeters except the separately recorded center-plane slope.

| Observation | Before | Current | Change |
| --- | ---: | ---: | ---: |
| behind right return drop | 7.60332 | 7.33083 | -0.27249 |
| behind left return drop | 7.60284 | 7.32887 | -0.27397 |
| right side wood line drop | 12.95792 | 15.02363 | +2.06571 |
| left side wood line drop | 12.95019 | 15.02647 | +2.07627 |
| center wood line drop | 10.96043 | 11.12744 | +0.16701 |
| center Z at Y100.6 | 55.58974 | 50.98153 | -4.60821 |
| center Z at Y114.8 | 55.59004 | 55.52625 | -0.06380 |
| side-return R fit  side -1 | 5.89599 | 6.00426 | +0.10826 |
| side-return R fit  side 1 | 5.89312 | 6.00462 | +0.11150 |
| local profile R fit fence to head side -1 | 7.18216 | 233.09967 | +225.91751 |
| local profile R fit head to strap side -1 | 6.97641 | 4408.21873 | +4401.24232 |
| local profile R fit fence to head side 1 | 7.18246 | 216.96420 | +209.78174 |
| local profile R fit head to strap side 1 | 7.01659 | 10232.89378 | +10225.87719 |
| degree-five length equivalent  side -1 | 18.70000 | 23.11000 | +4.41000 |
| degree-five length equivalent  side 1 | 18.71000 | 23.14000 | +4.43000 |
| recess-lip R fit | 0.57552 | 0.58310 | +0.00758 |

The center-plane slope changes from zero to +0.32001 in forward Y. Its front
face stays Z55.58707 beside the actual Z55.58494 rib floor. A rear level
Z55.59 land would stand above the falling turned fences; this is the specific
number that forced the former rear cushions. The top photograph shows a front
crown highlight and a fall toward the strap, not that raised rear level.

The old R7.18 and R6.98/R7.02 local circles and finite degree-five/ellipse
endpoints describe the rejected tight leveling-off profile. The new meridian
has no finite flat rear endpoint. The local strap interval is now nearly a
plane, making a large circle fit ill-conditioned. The legacy ellipse extrapolates
its front beyond Y220/231 and its lengths to 122.75/134.00 mm; these are not
physical roll extents. The old first-0.10-mm departure offsets, 8.8/9.0 mm,
become 2.7/2.6 mm on the inclined roof and no longer identify the rear outline.
These obsolete numerical interpretations cannot certify a photographic match.

The front circular radius, crowns, side planes, R6 side construction and R0.60
lip construction are retained. Small changes in fitted R values and boss gaps
reflect the changed neighboring surface and reduction. No lever, boss, recess
outline, floor, moving pivot or canonical sweep was changed. The native
preservation comparison is explicit. Photograph-based approval of the changed
profile remains incomplete because its camera/outline gates fail; the
highlight comparison is the stated form evidence, not an invented metric scan.

## Current rigid calibration and independent outline residuals

Four top points plus the rigid rib line, and seven open arc points plus three
rigid points and two lines, are fitted. No head or wood-joint observation enters
the objective. All residuals below are in native reference pixels and image-plane
millimeters at the measured head or individual point depth, not recovered 3D error.

| Camera | Point RMS px | mm at head | Line RMS px / mm | Free lens mm |
| --- | ---: | ---: | ---: | ---: |
| action_top | 12.39206 | 0.82461 | 9.92622 / 0.66052 | 162.081 |
| open | 24.13641 | 2.46865 | 7.30875 / 0.74753 | 717.381 |

The open solution presses against the 1 mm muzzle-side prior and its fitted
principal point is far off the published crop. The small opposite-side trial
remains rejected. This is not a unique calibrated photographic camera; the
open <1 mm requirement is **not met**. The original-image-center assumption
for the top view and broad principal-point bounds for the cropped open image
are recorded explicitly. Neither a lens prior nor head landmarks were used
to force the reported residual downward.

| View / actual wood joint observation | Native photo x,y | Error px | Error mm | <=2 mm |
| --- | --- | ---: | ---: | --- |
| action_top / wood joint curve 1 | 610, 2873 | 34.715 | 2.356 | **no** |
| action_top / wood joint curve 2 | 650, 2870 | 0.642 | 0.044 | yes |
| action_top / wood joint curve 3 | 675, 2880 | 13.773 | 0.932 | yes |
| action_top / wood joint curve 4 | 690, 2915 | 3.439 | 0.233 | yes |
| action_top / wood joint curve 5 | 702, 2960 | 20.992 | 1.422 | yes |
| action_top / wood joint curve 6 | 712, 3000 | 48.363 | 3.278 | **no** |
| action_top / wood joint curve 7 | 1030, 2970 | 12.673 | 0.844 | yes |
| action_top / wood joint curve 8 | 1033, 2925 | 16.593 | 1.101 | yes |
| action_top / wood joint curve 9 | 1035, 2890 | 37.028 | 2.450 | **no** |
| action_top / wood joint curve 10 | 1050, 2868 | 39.170 | 2.590 | **no** |
| action_top / wood joint curve 11 | 1080, 2852 | 26.988 | 1.784 | yes |
| action_top / wood joint curve 12 | 1110, 2849 | 7.710 | 0.510 | yes |
| action_top / wood joint curve 13 | 1150, 2851 | 17.643 | 1.164 | yes |
| action_top / wood joint curve 14 | 1200, 2870 | 38.791 | 2.556 | **no** |
| action_top / wood joint curve 15 | 1232, 2901 | 48.316 | 3.293 | **no** |
| open / wood joint curve 1 | 2258, 865 | 8.999 | 0.919 | yes |
| open / wood joint curve 2 | 2259, 825 | 19.322 | 1.968 | yes |
| open / wood joint curve 3 | 2261, 785 | 24.414 | 2.485 | **no** |
| open / wood joint curve 4 | 2266, 750 | 17.641 | 1.854 | yes |
| open / wood joint curve 5 | 2277, 724 | 8.540 | 0.897 | yes |
| open / wood joint curve 6 | 2300, 706 | 9.081 | 0.932 | yes |

Distances are to the projected actual rear-cap segments. No guessed fixed-X
photo correspondence is assumed. Visibility and the open camera remain limits;
the table does not silently certify an occluded segment. Smooth returns have
no identified photographic edge, and the top centerline is partly covered by
the different barrel extension. Their old engraved/highlight markers cannot
certify <=2 mm. **The complete outline gate is not met.**


50. **Independent projection catches the outline interpolation error.**
    Color/value: unchanged. Opened the corrected native top/open pairs and all
    23 current ordinary inspection renders (individual required player views
    plus five review sheets). The new central plane removes the earlier
    small islands and the crown highlight is concentrated toward the face.
    The outer shoulder still carries a broad return highlight; it must not
    be pronounced fair solely because the source is C2 or the export agrees.
    The top wood joint differs by as much as 3.29 mm and the open camera still
    fails. The source/export height curves are close; the game curvature has
    additional small facet reversals, retained in the count. No look change.

    The fresh Blender projection check found up to 4.68 pixels disagreement
    for new joint markers. Rigid camera points still agreed. The overlay had
    interpolated world coordinates with a screen-space segment fraction.
    Correct it to the perspective-correct fraction using the endpoint depths.
    The independent check now agrees within 0.004 pixels, including the joint
    points. No landmark observation, fit target or pass threshold was moved.
    Re-run the full build after this correction; retain the earlier failed
    build log rather than calling that run successful. Also remove stale
    18.5 mm roll and level-center callouts from the construction section sheet.



51. **Broader constructive outer joins rejected numerically.** Color/value:
    unchanged; this was a direct field/section study, not a new look pass.
    Reorder the union so the central plane is added after the turned fences
    and outer milled envelope, then test constant supports 1–24 mm and smooth
    rearward-growing supports. The wider joins can remove the two outer
    convex/concave reversals in each transverse half. A support of
    `1 + 0.95*(115-Y)` removes them at Y95–114.8 while keeping monotone axial
    heights and a front crown. It does so by burying the turned sectors:
    the Y108 fitted-circle center departs from the bore by 3.377 mm, Y110 by
    1.513 mm, and the side-window circle fit becomes R10.932 rather than R6.
    The face remains approximately R13.350, but that alone is insufficient
    to excuse replacing the accepted exposed fences. Reject this candidate
    rather than trading a sign-count pass for the wrong main surfaces.
    The retained narrow outer blend, its remaining reflections and its
    photographic attribution remain an explicit weakness. A body/control-only
    open camera trial also fails (best about 3.22 mm); discarding the rim
    observations is not a route to a validated <1 mm camera.


52. **Final source/export stripe set and current delivery, not form acceptance.**
    Color/value: inspection constants remain held. The current hero has luma
    percentiles 1.07 / 47.22 / 207.00, 21.13% below luma 15 and no all-channel
    clipping. These are tonal sanity checks, not a finish match. Opened all
    ten native source/export head panels, both full before/after export sheets,
    the native ordinary open crop, current player views, all 23 ordinary views,
    all 12 photo comparisons, both source/export side rakes, all construction
    sections, both curvature plots, ammunition, clip and final contact sheets.
    The small round-six central islands and folded-looking ordinary highlights
    are greatly reduced. The broad outer-return loops remain a form weakness.
    The bake reproduces the source; that does not certify the source's fairness.

| Image, both source and export | Dense source observation | Baked 2048 observation |
| --- | --- | --- |
| Open / longitudinal | Long front-crown bands; central land has no former small islands. Extra oval/S-turn structure remains on the outer return. | Same course; small jagged band edges on the outer return. No new central island. |
| Top / longitudinal | Front-crown ends turn near the face; long straightening runs flank the plane. Outer return creates secondary converging bands. | Central land stays quiet. Outer bands have small filtering/triangulation deviations; secondary structure remains. |
| Aimed / longitudinal | Crown loops sit on the front rolls. Outer shoulders and the recess make sharp course changes; the outer feature needs photo registration. | Same crown and shoulder structure, with fine band-edge filtering. |
| Right rake / longitudinal | Nested closed loops extend along the outer fence/base join, away from the front crown. Not accepted without a matching photographic feature. | Loops are retained; the ground side stays broad and flat. A few boundary artifacts remain at the forward edge. |
| Left rake / longitudinal | Mirrored extra closed-loop structure at the outer join. Not accepted as automatically fair. | Retains that structure; no return to the round-six small wave field. |
| Open / transverse | The large loops have moved toward the front crowns. Broad central plane is quiet; lower outer-return course change remains. | Same crown placement and lower return; narrow lip fringe is the real recess edge. |
| Top / transverse | Front-weighted triangular crown loops, with a flat central band response. Bright short band at recess heel is the cut lip. | Same locations; lip edge is slightly coarser. No rear-centered central cushion loop. |
| Aimed / transverse | Upper front crown arcs are simple. Lower shoulder/outer-return lobes remain separate reflected features. | Those lobes survive the bake; they require the same photo explanation as the source. |
| Right rake / transverse | Closed loops are concentrated at the front roll; the outer return fans into the broad side band. | Same paths with slightly softer edges; no new isolated island on the plane. |
| Left rake / transverse | Front roll carries the nested loops; outer return changes course before the side plane. | Matches the source, including that unregistered return feature. |

The recess lip is photographed and intentionally retained; its narrow bright
edge is not a fabricated fairness exception. The outer return is a known
constructive blend, but naming it does not prove the photograph has this exact
course. The longitudinal outer loops and 55 unregistered dense section events
remain explicitly unaccepted. **Round seven is incomplete.**

## Current build proof and handoff limits

- `make -C guns/sxs`: exit 0 after correcting the independent outline marker
  projection; full log `build/round7/make-final-current.log` at repository root.
- `make -C guns/sxs check`: exit 0; full log
  `build/round7/check-current.log`. The earlier failed full-build log remains
  `build/round7/make-current.log`; it is not presented as passing.
- The final review rerun passes current-source provenance for 317 render records,
  19 clips and every source/export band image. `build/round7-acceptance.json`
  remains `full_form_passed: false`, with separate camera, outline and section
  attribution results. The audit's `passed` covers provenance/mechanical checks.
- Native and imported checks each pass 246 actual contact probes. All 19 clips
  are swept at half-frame intervals over 1,161 cross-bone pairs, with no allowed-
  contact exceptions: 8,672 native and 9,862 imported unique solid tests. Largest
  measured general penetration is 0.11371 mm native / 0.11371 mm imported, inside
  the unchanged 0.2 mm tolerance. This is not a zero-intersection claim.
- Lever sweep: 51 angles from 0 to 25 degrees in 0.5-degree increments; actual
  triangle vertex/face and interior edge/edge distances. Minimum gap is
  0.15916034 mm native / 0.15915975 mm imported; maximum penetration 0, no triangle
  crossings. This is a sampled sweep, not a continuous-angle certificate.
- Strict repeat comparison: 104/104 entries match at 1 nm positions, five-decimal
  normal components and exact animation values/interpolation. Preservation
  against round six: 102/104 entries unchanged; only the head and stock inlet differ.
- 1,715 affine serialization samples pass. Dense head has zero nonmanifold edges
  and zero zero-area faces. Adjacent geometric face angles are regression data,
  not proof of fairness. The normal map projects the dense source through the
  actual game Mikk basis, with maximum roof/lip/floor/rear distances
  0.09227 / 0.01469 / 0.01093 / 0.03290 mm. All five bake channels report zero
  missed interior texels among 5,272,084 tested interior texels per channel.
- Current import UVs: no outside or degenerate triangles; overlap fraction
  0.0000013127, median density 2,375.43 px/m over all parts. The separately packed
  unique region has its own recorded UV report and lower overlap. No UV test
  threshold was relaxed. The former exact 99-ground-triangle assertion is now
  a nonzero-coverage check; the new forging has 103 such triangles, with both
  fitted plane and texel-coverage checks retained.
- Gun: 38,822 triangles, 54 named meshes, 17 bones, 19 clips, 14 sockets,
  one material, three 2048 maps. GLB 12,477,444 bytes. BaseColor 262,792 bytes
  (RGB8), Normal 7,287,012 bytes (RGB16), ORM 1,613,267 bytes (RGB8).
  Source bake is 4096 / 32 samples on the locked GPU. Shell/hull remain
  752 / 480 triangles. No kit/common changes, look work, docs JPGs or push.

Current evidence is under `renders/checkpoint/`: `contact-sheet.jpg`,
`reflections/source-export-{longitudinal,transverse}.jpg`,
`reflections/before-after-{source,export}-{longitudinal,transverse}.jpg`,
`reflections/open-head-before-after.jpg`, `beauty/{open,aimed,top,breech}.png`,
`pairs/{action_top,open,open-player}-pair.jpg`, `head-raking-comparison.jpg`,
`sections/sections.jpg`, and `curvature/{longitudinal,transverse}.png`.

What remains is substantive: the open camera does not meet 1 mm; actual top
wood-joint observations reach 3.29 mm; returns and the covered centerline have
no accepted registration; outer-loop/section attribution is incomplete. Verified
rigid correspondences for the open photograph are needed before that pair can
safely drive further head changes. The different raised barrel extension and
uncertain visible rim must not be used as if they were a shared calibrated part.
The two free-camera fits are useful diagnostics, not a claim of recovered EXIF.
No kit feature is needed to hide or waive these failures.


# Covey 26 — form round 6: upper forging fairness

Round five's favorable surface judgments are superseded. The accepted
layout, controls, material constants and rig are retained. Before evidence
is preserved under `build/round6/before/`; no final docs images are added.

## Round 6 critique passes

33. **Baseline and first shared cage.** Color/value: original dark-steel
    inspection constants; the black-background dealer macros contain no
    neutral, so unity balance remains and no finish match is claimed.
    Opened the original open view, its exact 450 × 300 head crop, the top
    and open player pairs and both dense/export rakes. The open view plainly
    has diagonal ridges from both inner fences, wrinkled rear corners and a
    wavering lip. The side rakes do not reveal them adequately. Added five
    matched stripe cameras in two perpendicular band orientations. An initial
    longitude/atan2 environment pinched its stripes at its own poles; rejected
    that lighting and used parallel latitude bands, without a pole singularity.
    The first 35 × 18 shared subdivision control net removes the large diagonal
    ridges but retains small curvature changes near the inner shoulders.
    Its `pass1` source images are rejected; it also misses the accepted local
    radii and leaves small Boolean boundary failures. No bake made from it.

34. **One net with curvature regularization.** Color/value: bands are a
    diagnostic shader; the ordinary inspection values remain unchanged.
    Opened all ten `pass2/stripes-source` images. The transverse top bands now
    form continuous wide curves across both fences and the center, without the
    original diagonal folds. The longitudinal bands reveal extra curvature
    near the central shoulder departure and the rear corners; the lip still
    has small tessellation/shading disturbances. Reject for further work.
    Strengthened the measured front-circle, center-height and profile
    constraints without adding separate surface patches. Found that the old
    per-corner roof-normal classification also flattened the last 0.10 mm of
    the lip before an abrupt shading change. It now classifies entire roof
    faces, leaving the arc's own normals intact. Increased source resolution
    and removed tangent-intersection slivers before considering a bake.


35. **Physical curvature, integral lip and all five source cameras.**
    Color/value: retained the accepted inspection constants. The neutral
    black/white bands test form only; the dealer macro has no defensible
    white-balance neutral. Opened all ten `pass10/stripes-source` images:
    open, top, exact aimed and both side rakes, each with two perpendicular
    band directions. The top's bands form continuous curves through the
    inner shoulders; the open camera no longer shows the long diagonal
    folds. The right/left rear returns carry continuous bands to the wood
    boundary. Bands turn at the standing face and external wood joint,
    which are intentional boundaries. The small fore recess lip no longer
    ripples. Tight but continuous closed bands around the compound crowns
    are reflections of continuous curvature, not a separate fence seam.

    A merely C2 control net still permitted secondary humps. Added monotone
    physical slopes and a penalty on physical curvature variation, retaining
    the measured profile/radius constraints. Removed the tangent recess
    Boolean entirely. A constrained triangulation joins the one roof to
    circular R0.60 lip rows using shared boundary vertices; the rear relief
    is below the original lever. Source remains manifold with no zero-area
    polygons. A 1 µm action-coordinate grid distorted the shortest boundary
    intervals; retaining those intervals at 10 nm removes that quantization.
    The other parts retain their original precision policy.

    Dense geometric adjacent-face maxima are 3.27/2.94 degrees on the
    right/left fences, 3.86 at the center, 5.49/5.54 on the right/left rear
    returns and 7.57 on the lip. These are actual triangulated face normals,
    not the derivative or transferred shading normals. Intentional breech,
    wood-joint, recess-floor, bushing and internal spindle-seat edges are
    separately listed with exact locations; their sharpness is not counted
    as a smooth blend. This sampling audit supports but does not replace
    the images. The export/bake-loss comparison remains the next gate.


36. **First 2048 bake: rejected rear-return projection.** Color/value:
    the held dark steel and wood constants survive the 4096-to-2048 bake,
    with no missed interior texels in the five channels. The ordinary open
    player's image and its native crop expose several black stripes along
    the rear returns, absent from the dense source. Reject this export.
    A passing coverage/constant-color audit cannot detect a wrong normal
    projected from an adjacent surface of the same steel part.

    The old nearest-source normal transfer did not distinguish the roof from
    its adjacent end cap after reduction. Added integer face ownership to
    the constructed roof, lip and floor, and retain it through canonical
    ordering and triangulation. Roof corners now retain the subdivision
    limit's normal, including boundary corners; the end cap and lip retain
    their own normals. The bake and every exported evidence view must be
    regenerated after this correction. No pixels are manually repaired.


37. **Precision and the actual high source's ground flats.** Color/value:
    no inspection constant changed. Opened the corrected ordinary open,
    aimed, top, breech and both side rakes, then every other beauty view on
    six review sheets. The false black stripes on the rear end caps are
    gone. The normal's 8-bit shipping quantization still steps very narrow
    mirror bands. A 2048 RGB16 trial retains the continuous gradients, so
    keep the original 4096 bake precision through the same normalized
    two-by-two vector filter. BaseColor/ORM remain RGB8; it is still one
    2048 three-map atlas. This costs disk space, not additional triangles
    or texels, and requires consumer precision/compression validation later.

    The dense source also had a distinct shading error on the genuinely
    ground constant-X side faces. Actual corner normals departed from the
    plane by as much as 4.10375 degrees. Give only those planar corners
    their measured face normal; preserve all roof, lip and end-cap normals.
    The saved preparation report now reads the corrected normals back and
    measures 0.30710 degrees after custom-normal storage, rather than reporting
    the assigned ideal as a measurement. Dense
    diagnostic preparation applies exactly the same policy as the bake.
    The narrow-band test remains at roughness 0.045, without denoising;
    a softer 0.10 trial is not the final fairness evidence.



38. **Final narrow-band comparison rejects the flat-side bake.**
    Color/value: identical neutral diagnostic bands at roughness 0.045;
    no denoising or material-value adjustment. The complete make passed
    317 current evidence records, but that is provenance, not visual approval.
    Opened both all-five-view source/export stripe sheets. In both
    directions the upper crown, center, rear returns and recess follow the
    dense source closely. The exported ground side flats have speckled
    interruptions at narrow transverse bands, especially in both rakes.
    Reject this bake despite the much improved ordinary open view.

    A saved-source read-back confirms the assigned flat normals still
    depart by 0.307 degrees at corners encoded in a smooth fan shared
    with neighboring curved faces. A scripted flat-face trial isolates
    those loop-normal spaces and removes that directional error. Apply
    this only to actual constant-X ground faces in both the UV target and
    dense source, preserving the roof, lip and end-cap normals. Use atan2
    of cross length and dot to measure the tiny residual: acos of a
    float32 dot alone falsely reports about 0.02 degrees for a parallel
    vector whose length rounded below one. Re-bake and regenerate the
    full evidence; no pixel or shader repair is used.

    The first flat-fan trial still fails the transverse rakes. Actual target
    triangles span a breech-edge-break vertex 1.3 microns inside the ground
    plane, outside the initial 0.3-micron coordinate bound. Use the model's
    existing 15-micron ground-side tolerance with its strict face-normal
    criterion, and include the continuation into the hinge cheek. This
    selects 3,274 dense and 297 target corners. Read-back maxima are now
    0.00356 and 0.01577 degrees respectively, over the full selected region.
    A separate direct PNG/import test confirms the exported RGB16 normal
    decodes into a float image with maximum channel difference 5.96e-8;
    bit-depth conversion is not the remaining cause. These checks support
    the revised projection; the rendered bands must still pass.


39. **Connected-map control and precise ground-plane projection.**
    Color/value: same neutral bands, roughness 0.045 and no denoising.
    Opened the right transverse control with its normal map disconnected:
    the side band is clean. The diagnostic is not a delivery image. Then
    opened all four `math-projection/reflections` rakes with the test normal
    map connected. Both transverse ground bands are now continuous, and
    both longitudinal sets retain the smooth upper forging and returns.
    The former broad speckled breaks are gone. Tiny filtered UV-edge signals
    remain at the boundaries of the curved bake, not as geometric folds.

    The saved Cycles map deviates up to 0.26 degrees at sampled ground-side
    texels despite the corrected source/target normals. Decode preserves
    RGB16, and the kit's temporary mesh join changes selected ground normals
    by 0.0 degrees. Use an exact geometric projection for these planes:
    fit each to the original dense source by SVD, evaluate its normal through
    the actual game mesh's interpolated Mikk tangent basis at each 4096 UV
    texel, and extend only into unoccupied gutter. This is a scripted bake
    of our original geometry, with no painted pixels, photo input or shader
    change. The compound head, recess, returns and every other normal region
    retain their GPU Cycles bake. The kit still filters and exports the set.

    The two measured plane fits have RMS residuals 0.000318/0.000290 mm;
    largest residual 0.003410 mm. Projection covers 99 triangles, 89,208
    interior texels and 15,971 gutter texels. The standalone prototype's 22
    sampled side texels now deviate at most 0.0155 degrees. Its normal map
    remains connected. Integrate the fitted-source version, retain the
    original GPU map for comparison and regenerate every final view.

40. **Reject residual curved-strip projection noise.** Color/value: same
    narrow neutral bands and unchanged ordinary inspection constants. The
    plane-only projection cleans the middle of the ground faces, but final
    full-resolution right/left transverse rakes still show ragged band edges
    in the curved strip immediately beside them. The earlier pass's favorable
    ground-plane judgment does not accept that adjacent strip. Reject it.

    Project the complete forging directly from its original dense triangles,
    interpolating their saved corner normals at the nearest source point
    within each construction region. Roof, lip, floor and rear cap cannot
    select each other's normals. Evaluate each result through the target's
    actual interpolated Mikk basis at 4096, retain RGB16 at 2048 and keep the
    normal map connected. The SVD-fitted planes remain for the ground sides;
    all other parts retain their original GPU bake. Opened both prototype
    transverse rakes: the formerly ragged curved-strip bands are continuous
    and follow the dense source. This changes no vertex or material value.
    Projection covers 555,222 interior and 385,031 gutter texels. Worst
    source distances for roof/lip/floor/rear cap are 0.09731 / 0.02282 /
    0.00530 / 0.02687 mm; the remaining reduced forging reaches 0.53739 mm.
    Two independent projections reproduce all three 4096 PNGs and their
    report byte for byte. Full-camera and ordinary-view regeneration remains
    the final gate.

41. **Top-view atlas-border audit.** Color/value: unchanged constants and
    narrow neutral bands. Opened all twenty source/export stripe crops at
    native resolution. Both side rakes in both directions now retain clean
    continuous bands. The top view still has small export-only marks near
    the lip, especially longitudinally, and slight band-edge filtering at
    the outer rolls. The source is clean there. A passing make and 317
    current render records do not resolve this last projection defect.

    The gutter blocker used a conservative polygon fill for the action as
    well as the other parts. It incorrectly protected some pixels outside
    the action's actual pixel-center occupancy, retaining the original GPU
    bake inside the shipping filter's footprint. Use the exact action
    occupancy already computed by the projection; keep conservative
    protection for every other part. Opened the trial top and open views,
    both band directions. The distinct export-only spots beside the lip
    disappear; curved bands remain continuous. Finite 2048 filtering still
    softens some band edges, and must not be described as pixel-identical
    to the dense source. The revised gutter covers 436,266 texels, without
    changing the 555,222 interior texels or any vertex.

42. **Final source, delivery and photographic gate.** Color/value: the
    original dark-steel and walnut inspection constants remain unchanged.
    The dealer action macros have no defensible neutral; unity balance is
    retained and no finish match is claimed. Diagnostic bands remain neutral,
    roughness 0.045, 32 samples, without denoising. Opened all twenty final
    stripe images as native head crops, the four complete before/after
    sheets, and the ordinary open view's native 450 × 300 before/after crop.
    The old diagonal fence-to-boss folds, rear corner wrinkles and rippled
    lip are absent. The following records each source and delivery image;
    transverse/longitudinal names match the PNG filenames.

| View / bands | Dense source observation | Baked 2048 export observation |
| --- | --- | --- |
| Open / transverse | Crown loops flow into the shoulders; center and lip have no pinched fold. | Same continuous paths; rear returns have no former black projection stripes. |
| Open / longitudinal | Bands sweep through the inner shoulders and around the recess without the former diagonal ridge. | Sweep retained; lip and both rear corners remain continuous. |
| Top / transverse | Nested crown bands widen smoothly into the head; outer returns have no secondary wrinkles. | Bands remain connected; some edges on the outer rolls are softened by 2048 filtering. |
| Top / longitudinal | Inner-return bands bend continuously into the recess; rim has no ripple. | The isolated lip-border marks from pass 41 are gone; small band-edge filtering remains. |
| Aimed / transverse | Both crown loops and central recessed-wall bands are continuous; no surrounding fence crease. | Same shoulder and recess pattern; the original bead remains visible. |
| Aimed / longitudinal | Curved shoulder bands flow toward the recess and down both returns. | Paths retained without a new center seam or abrupt upper-surface turn. |
| Right rake / transverse | Continuous crown/return loops and a clean broad ground-side band. | Both retained; the ragged curved-strip interruptions from pass 40 are gone. |
| Right rake / longitudinal | Bands run continuously from the front roll through the rear return. | Same flowing bands through the side radius and rear corner. |
| Left rake / transverse | Continuous crown/return loops; broad side band has no wrinkle. | Matches the source's continuity; no former speckled break beside the ground plane. |
| Left rake / longitudinal | Bands run continuously across the return and into the side radius. | Same course, with no rear-corner kink. |

Sharp changes are confined to the standing face, actual wood joint and
recess boundaries; their separately measured edges are listed below.
Finite texture filtering is visible at close zoom, so the export is not
claimed to be pixel-identical to the dense source. It no longer reproduces
the old cloth folds. Both ordinary rakes, all six beauty-review pages,
twelve photographic pairs, the exact aimed/open pairs, all 24 sections,
the clip/opening sheets, ammunition views and contact sheet were inspected.
The head reads as one forging and the standing face remains one face with
its bushings. Published-class interpretation and estimated photographic
cameras remain limitations; these are not precision scan comparisons.

The final `make -C guns/sxs` and subsequent `make -C guns/sxs check` both
exit 0. The check leaves the GLB's SHA-256 and timestamp unchanged.
The presentation audit has 317 current render records, all 19 real-duration
clips, twenty current stripe images and twenty matching baseline
camera/light comparisons. All ten export stripe images retain their normal
map. The final GLB SHA-256 is
`bf3aab8b13e529c7bf6739d19d57cb2c696180308ce4d9e4095eca116106436b`.
The isolated padding trial and production projection have byte-identical
BaseColor/Normal/ORM 4096 PNGs. Repository-root `build/round6/` retains the
before evidence, diagnostic trials, comparison hashes and final build logs.
No look work, docs JPGs, kit changes or shared/common changes were made.

### Dense geometric normal audit

`build/fairness.json` measures the largest angle between adjacent triangle
face normals, after triangulating the actual dense action. It records the
worst edge and both face centers, not just a percentile. No shading normals
or fitted derivatives enter these numbers.

| Continuous region | Largest angle |
| --- | ---: |
| Right / left fence into head | 3.2707° / 2.9363° |
| Center fill | 3.8643° |
| Right / left rear return | 5.4898° / 5.5421° |
| Upper recess lip | 7.5739° |

The intentionally retained boundaries are measured separately: breech arris
90.7554°, rear wood joint 87.7588°, recess floor/wall 111.8014°, bushing
counterbore 90.0002°, and the internal lower spindle seat 143.0237°.
The last is a microscopic internal triangulation edge, not an upper blend;
it is explicitly retained in the report rather than silently filtered out.
The dense action has zero nonmanifold edges, zero zero-area faces and positive
signed volume. The 12° smooth-region test is a tessellation regression bound;
only the reflection images establish whether the surface looks fair.


### Round 6 measured build proof

- `make -C guns/sxs` and `make -C guns/sxs check`: both exit 0 against
  the final RGB16-normal export.
- 38,822 total triangles, including staged ammunition; action allocation
  7,750. One atlas material, three 2048 images; BaseColor/ORM RGB8 and
  OpenGL normal RGB16. GLB 12,495,908 bytes. Delivered PNGs: BaseColor
  263,623, Normal 7,289,858, ORM 1,623,793 bytes.
- Source and imported contacts: 246 actual surface probes each, all pass.
  All 19 clips at half-frame spacing: 1,715 source and 1,728 imported
  samples, zero violations, no allowed-contact exceptions. Largest sampled
  penetration is 0.113714 mm, below the existing 0.20 mm visual tolerance;
  this is not a claim of zero intersection throughout every assembly.
- Strict lever sweep: 51 angles, 0–25° at 0.5°, 306 moving/fixed pairs.
  Minimum actual gap 0.156732 mm source / 0.156731 mm import, zero
  penetration and triangle crossings. This proves clearance of the unchanged
  lever and spindle against the new head, original strap and revised inlet.
- UVs: no outside or degenerate triangles; overlap fraction 0.000001015
  against the 0.00001 bound. Median density 2,383.4 px/m at 2048.
  The five 4096 bake channels have zero missed interior texels.
- Re-import serialization: 1,715 affine samples; maximum position error
  0.000191 mm and maximum of 100 surface-pose errors 0.000253 mm. These
  prove serialization, separately from the contact/clearance measurements.
- Independent native rebuild: 104/104 entries identical. Preservation
  against round five: 102/104 identical; only the action and its wood inlet
  change. Moving meshes, strap, rig, sockets and exact clip keys are retained.
- Repository check: 1,050 sources, zero errors. No kit/common changes.

The README repeats every accepted exterior gauge against its original
photographic uncertainty. Those uncertainties remain material: this is an
original measured interpretation, not a scan of a specific gun. The narrow
mirror response also exposes the delivered texture's finite spatial resolution
and custom-normal storage; engine compression must be judged again at the
finish gate. Keeping RGB16 here is a disk/consumer tradeoff, not evidence that
an arbitrary game importer preserves it. A general optional RGB16 mode in
the kit downsampler would avoid the local precision-preserving wrapper.

---

# Covey 26 — form round 5: head behind the fences

The round-four record below is retained as history. Round five keeps its
57.350 mm crowns, 51.900 mm pair width, front R13.35 arcs, 18.5 mm crown roll,
side flats and lower plate construction. The new head is judged in
sections 3, 8 and 15 mm behind Y115 and in both bore-axis vertical planes.
Inspection material values remain unchanged; no finish work or docs JPGs.

The owner has now specified **Z55.59 mm** for the center fill. This
supersedes the former Z49.72 mm central outline; it does not preserve that
notch. The standing face now reaches the actual rib floor between the
R13.35 front arcs. The uninterrupted center surface runs level back to the
lever recess, whose R5.90 fore wall fits the original R5.60 boss. The 0–25°
lever range and all 19 clip keys remain unchanged.

## Round 5 image critique passes

25. **First Z49.72 / R6 / 3 mm join trial.** Color/value: inspected the dark
    steel and broad reflections before assessing the form; the original black
    macro backdrop has no defensible neutral, so unity white balance remains.
    The first source previews (`renders/round5/pass1`) remove the 40.64 mm
    section's two original roof facets. The 49.72 mm center datum fills the
    head behind the R13.35 front arcs, but the 3 mm join band still produces
    too narrow a reflection transition. A topology check rejects 24 boundary
    edges around the unchanged Y115 bushing cuts. These previews are rejected
    source diagnostics, not the baked delivery.
26. **6 mm signed-distance join and Y115 topology.** Color/value: the second
    preview set (`renders/round5/pass2`) retains dark steel and visible cavity
    shadows. The 6 mm join band reduces the rear reflection break, but a height
    maximum truncated at a circular patch's end still gives a derivative
    discontinuity. Replaced it with the zero of a C2 signed-distance union;
    there is no separate fence mesh. Resolved sub-0.8 mm collinear T-junctions
    on the Y115 plane by splitting the existing edges at their third vertices.
    The subsequent head source and game mesh have zero nonmanifold edges.
27. **Lever clearance and actual centerline datums.** Color/value: viewed the
    third source set (`renders/round5/pass3`), including aimed, open, breech and
    both upper rakes. The raised stock trial leaves an unnecessarily exposed
    lever cutout in the wood. Restore the accepted wood's previous head cage;
    only the action receives the 0.35 mm allowance for the original 0–25° lever
    sweep. Its first motion test identifies the stock/lever collision instead
    of adding a contact exception. Independent surface rays distinguish the
    action's 49.72 mm notch from the actual rib sighting floor, 55.59 mm, and
    the accepted boss's 50.30 mm top. At this trial, datum clarification was pending before
    choosing the delivered center fill; neither a constant nor a source
    preview constitutes acceptance of that requirement.

28. **Restored wood and measured sections.** Color/value: opened the new
    `renders/round5/datum49` and `datum55` player previews. Both retain the
    original material constants. The 49.72 mm trial retains the front notch;
    the 55.59 mm trial fills to the actual rib surface but raises its center
    outline and leaves the 50.30 mm boss in a deeper recess. Those are distinct
    outcomes, so the then-pending datum choice cannot be hidden by camera placement.
    Opened the Y112/Y107/Y100 and both bore-axis section drawings. The sampled
    49.72 mm head gives drops 7.63 mm just behind either return, 13.07 mm at
    either side wood line and 11.20 mm at the center wood line. Its side-return
    circle fit is R5.994 mm. The sampled bore-axis transition fits are about
    R19.4 mm rather than the initial 4–8 mm photo inference; they are not
    claimed to match that estimate. The current quick source check passes
    246 contact records and manifold topology at 38,822 triangles. The latest
    opening sweep has zero motion violations; final full source/reimport
    sweeps and the new bake were pending the center datum choice at this pass.

29. **Z55.59 center and degree-5 rear return, both source rakes.**
    Color/value: opened both full-resolution source rakes and the top/aimed
    previews in `renders/round5/final-source`; the accepted constant steel
    remains dark, and the black-backdrop macro remains at unity balance.
    The previous signed-distance field produced small secondary folds near
    the outer returns. Replaced its rear portion with a monotone degree-5
    height excess, ending with zero height, slope and curvature; the rear
    endpoint shifts 0.68 mm per transverse mm inward. In these images the
    R6 side returns carry broad reflections from either lighting side,
    without the former wrinkles. The center fill now joins the rib at
    Z55.59 and the aimed image retains the bead. The recess lip trial is
    rejected for microscopic topology folds: a modifier bevel is replaced
    by a measured-roof-tangent circular R0.60 cutter, tapered over Y88–92.
    This is still source evidence. Baked image acceptance follows below.


30. **Both baked rakes and the 0.999 Y corner-normal failure.** Color/value:
    the 2048 export retains the constant dark steel and unaltered wood values.
    The right rake carries the R6/degree-5 return without the former small
    folds. The left rake exposes a dark diagonal absent from the dense left
    image (`head-raking-comparison.jpg`, trial GLB `38344c7572b5`). Reject
    that bake. UV probes find green as low as 2/255 on the side-flat normal
    map, while AO is 255/255 there. One reduced triangle inherited a corner
    normal approximately (−0.036, +0.999, 0) from the orthogonal standing
    face. Classify the actual planar face before nearest-source transfer
    and give its corners the ±X normal. A temporary sharp-edge projection
    split did not solve this error and is discarded. Add an independent
    side-flat shading-normal check with a 0.25° bound, then rebake and
    re-render every exported view. No texture pixels are hand repaired.


31. **R6 / degree-5 source and 2048 export, both lighting sides.**
    Color/value: reopened the two dense rakes and both new exported rakes at
    full resolution. The accepted dark steel keeps cavity shadow and broad
    highlights; no white balance or material constant changes. The R6 side
    return and degree-5 fence/head return now carry those highlights without
    the former small folds. The left side's false diagonal is gone after the
    planar normal correction; its map probes are approximately (127,128,255).
    The remaining dark horizontal line under the barrels is the real table
    recess and its occlusion. The source and imported side-flat normal checks
    pass the 0.25° bound. The R0.60 construction lip fits R0.583 mm on the source and
    R0.591 mm on the export, with 0.002 mm maximum profile error. Review the unannotated
    right/left rakes and `head-raking-comparison.jpg`; the final comparison
    sheet is regenerated from these same cameras and the current GLB.


32. **Z55.59 player pairs, 9.20/9.40 mm returns and five head cuts.**
    Color/value: opened the new aimed pair, both open player pairs and top
    pair at full resolution. Constant dark steel has less color variation
    than the case-colored reference; materials remain held. The macros and
    rear film frame have no reliable neutral, so unity balance is retained.
    The exact Eye view now has a Z55.59 head surface between and behind the
    R13.35 crowns, with the rib/bead still visible. Its photographic comparison
    is explicitly elevated and oblique; the fitted camera does not replace
    Socket_Eye. The two open pairs retain the actual player frame. The empty
    macro comparison exposes one standing face from the table to the crowns;
    the two small pin bushings remain in that plane. The Commons comparison
    is labelled for its different camera, opening angle and sidelock exterior.
    Neither ammunition head in the loaded player frame is being presented as
    the standing face.

    The top pair includes all four return ends and three centerline markers.
    Inner-behind-outer offsets are 9.20/9.40 mm, against 11.5±3 mm in the
    photograph. The added arrows are review-only and do not improve the
    camera fit; the complete top RMS is about 69 native pixels. The outlines
    are tangent-return observations at a 0.10 mm height departure, not seams.
    The image comparison remains less exact than a scan or calibrated part
    drawing; the photo's lever also hides the center wood-line station.

    Opened the cuts at Y112, Y107 and Y100, both bore-axis cuts and the
    Y94–115 center cut. The R6 side return and degree-5 axial return meet
    without the former designed corner. The center cut confines the lower
    surface to the lever recess; measured uninterrupted head from Y100.6 to
    the face is Z55.589–55.590. Drops behind each return are 7.63 mm (photo
    5.6±3), side wood-line drops 13.07 mm (12.5±3), and center wood-line drop
    11.29 mm (8.5±3.5, occluded). Equivalent local radii are R5.994 at the
    side, R6.63–6.65 at the fence/head and R5.72–5.92 at the upper strap
    departure; fitted intervals and errors remain explicit in the gauges.
    Minor one-to-three-pixel seam signals at the wood inlets remain visible
    at 1440-pixel magnification. They are outside the fence/head return and
    are not claimed as finish acceptance.


## Round 5 delivered proof

`make -C guns/sxs` and `make -C guns/sxs check` both finish with exit 0.
The current GLB is **38,822 / 39,000 triangles**, 6,299,240 bytes, one material,
and three 2048 maps from the 4096 / 32-sample GPU bake. The delivered map files
are 264,423 / 1,077,331 / 1,612,273 bytes (BaseColor / Normal / ORM).
All 54 rigid meshes have closed manifold topology and positive volume, with
no zero-area faces. UV outside/degenerate counts are zero; overlap fraction
is 0.000000965 and median density about 2,345 px/m. Projection ownership and
interior-texel coverage pass. No kit or common module changed.

Source/import each pass 246 actual contact probes. Their 19-clip half-frame
sweeps contain 1,715 / 1,728 samples and no violation at the accepted 0.20 mm
motion tolerance; maximum penetration is 0.11371 mm. The additional lever
sweep is stricter: 51 angles at 0.5° spacing through 0–25°, 306 moving/fixed
pair records, **minimum gap 0.15673 mm**, at 0° between lever and stock, and
zero penetration. It samples the actual triangle surfaces, including interior
edge/edge distances; it is not a continuous-angle certificate.

Independent rebuild matches all 104 entries. Preservation against `f4842bc`
retains 101 entries; only Action_Body, Stock_Walnut and Top_Strap differ.
Moving geometry, bone rest frames, sockets and exact clip keys are retained.
Baked export serialization passes 1,715 affine samples plus its actual-surface
poses. The current presentation audit passes **297 render records** and all
19 real-duration WebPs, tied to GLB hash `1895379528879f03…`. All gun pairs,
rakes and player views use this GLB. Dense-source and standalone ammunition
images are labelled exceptions. The final contact, clip and ammunition sheets
have been opened. Hero luma p1/p50/p99 is 1.07 / 47.08 / 205.67, with 21.06%
deep shadow and zero all-channel clipping; this is a range check on the held
inspection values, not look acceptance.

The photo uncertainty, elevated rear reference, 1–3 px wood-inlet seam signals,
and right crown's +0.004 mm reduction deviation are disclosed limits. All
requested dimensions are independently measured in `build/serialization.json`
and tabulated against the photos in README. No docs JPGs or finish work.


# Covey 26 — form round 4: fences, flats and underside

This round judges the **baked 2048 export**, `export/sxs.glb`. The kit finalizer,
4096 GPU bake, downsampler and animated exporter supply one BaseColor / OpenGL
Normal / ORM set. The colors and roughness remain the accepted inspection
constants: finishes, grain, checkering, markings and used wear are still held.
A normal bake does not constitute finish acceptance. No docs JPGs are added.

## Current region review

- **Fences.** Replaced the oversized spheres with circular transverse sections
  continuing the measured bore axes backward, and a short longitudinal roll
  into the existing shoulder/strap. Each crown meets the tube top line; the
  pair fits inside the joined breech width. The rear boundary curves inward
  toward the strap in the top view. The photograph has a subtler, hand-finished
  shoulder junction and a differently shaped rib extension; ours retains the
  original plainer shoulders. See the [right pair](renders/checkpoint/pairs/action-pair.jpg),
  [top pair](renders/checkpoint/pairs/action_top-pair.jpg),
  [top rake](renders/checkpoint/beauty/action_rake_top.png), and fence sections.
- **Side and knuckle.** One ground side plane now continues from head to bar.
  The rounded lower edge sweeps upward into the original hinge axis, and the
  pin end is a thin flush circle in the same blued inspection steel. The
  photograph's shallow decorative panel line is not a geometric step and has
  not been copied. Our plain lower neck is broader through its flat belly;
  the reference has a slightly narrower sculpted throat. See the
  [right rake](renders/checkpoint/beauty/action_rake_right.png), left rake,
  right/left pairs and the bar/knuckle sections.
- **Underside and plate.** The plate seats into the forging and shares its
  rounded lower skin. Its curved front joint is a narrow seam. Rounded-end
  blade slots replace the broad rectangular openings. The guard and its rear
  wrist tang retain their accepted form. Our joint remains simpler than the
  photograph's curved plate border, and the forward hook pocket remains more
  open than the photograph's shallow visible joint. See the
  [bottom rake](renders/checkpoint/beauty/action_rake_bottom.png),
  [bottom pair](renders/checkpoint/pairs/action_bottom-pair.jpg), and the new
  plate and two slot sections. Baked raking light is the appearance evidence;
  geometry probes alone do not approve the highlight.
- **Aimed view.** The accepted eye frame, cheek station, drops, lever and safety
  are retained. The rib is visible between the fences toward the bead, with
  the crown below the bead line. Its short apparent length is strongly
  foreshortened by the cited fitted sight picture. The inspection rib is not
  yet matted. See the exact [Socket_Eye view](renders/checkpoint/beauty/aimed.png).
  Required sight rays now cover six rib stations from Y=140 to 740 mm as well
  as the bead, independently against all occupied skins.
- **Accepted remainder.** Trigger blades, guard band/tang, lever, safety,
  barrels/ribs/bead, splinter/iron, ammunition, rig, sockets and all 19 clip
  keys are preserved. Only the action, its pin/cross-pin placement, plate and
  stock head/inlets change. The stock head is refitted to the continuous side
  plane; the shortened upper head and wood beside the strap remain. A fresh
  build of `8a6ff08` confirms 96 of 104 native geometry/normal/rig/socket/clip
  entries are identical. See `build/preservation.json`. The larger historical
  region review below remains a record, not current acceptance.

## Round 4 critique passes

19. **Reference relation and first rebuild.** Color/value: retained dark steel
    and deep cavities; the black-backed macros cannot support a quantitative
    hue match. At full resolution the old spherical fences clearly stood
    above and outside the tubes, and the head/bar junction had a side ledge.
    Replaced them with concentric transverse arcs and an 18.5 mm axial roll;
    carried one side plane through the forging and extended the flush pin
    ends to that plane. Checked the first side/top/aimed previews against the
    native reference crops. The underside still had a raised plate boundary.
20. **Shared lower construction.** Color/value: judged the broad lower steel
    highlight before detail. The first plate-seat subtraction left a thin
    exterior skin and an oversized dark seam. Extended the seat cutter below
    the outer skin, made the plate and bar share the same 8 mm arris, and
    made their forward stations follow the curved seam monotonically. Narrow
    6 mm slots now surround the unchanged 5.4 mm blade roots. Cleared the
    wood inlets slightly beyond the plate slots to avoid coincident cut walls.
    Rechecked topology and contacts; no collision allow-list was added.
21. **Baked export and highlight continuity.** Color/value: the first 4096→2048
    export retained deep shadows without pale pin disks. Its bottom rake
    exposed a highlight mismatch at the plate joint and small polygonal
    transitions. Gave both sides of the seam the same original lower-skin
    normal field, retaining flat side normals, then rebaked. The fences also
    follow the actual tubes' slight axis convergence rather than assuming
    perfectly parallel bore centers. Circle/roll fits are measured from the
    export; neither the radius nor the center result is echoed from a model
    constant. Rejected UV charts that folded across the stock's hidden routed
    inlets; isolated its atlas region and tightened its projection partitions.

22. **Projection loss in the matched export.** Color/value: the top and
    underside pairs exposed a serrated steel-colored strip on the wood inlet,
    absent from the intended inspection color. Zero missed texels had only
    proved that rays hit something, not that they hit the intended part.
    Rejected the bake. Isolated the stock, action, plate and tang surfaces
    during material/normal projection, then combined those channels with a
    separate assembled-contact AO pass through the same kit baker. No
    geometry, accepted controls or triangle allocation changed. Rechecked the
    macro pairs and rakes from the new baked export before accepting the bake.

23. **All-part projection ownership.** Color/value: the new forend view still
    showed a serrated steel-colored fringe at the latch, even after isolating
    the action/stock joint. Extended projection isolation to all 54 actual
    named parts, independent of their shared animation bones. The accepted
    forend, controls and ammunition geometry remain unchanged. Added an
    independent constant-albedo audit of 48 single-material parts: 5,133,244
    eroded interior texels pass with zero wrong-color texels at a 0.01 linear
    RGB tolerance. As a negative control, the same audit rejects the assembled
    material projection (400,286 wrong-color texels), whose AO channel alone
    is retained. Reviewed new forend, control, underside and exact-eye previews;
    the neighboring-material fringes are gone. Tiny facets in the accepted
    routed latch lip remain geometry, rather than being hidden with a texture.

24. **Final baked-export review.** Color/value: reopened all eleven current
    photo pairs, the six full-size review pages, exact-eye image, three raw
    and annotated action rakes, sections and contact sheets. The inspection
    steel retains dark cavities and a broad rolled underside highlight; the
    hero has 20.71% deep-shadow pixels and no all-channel clipping. The black
    macro backgrounds provide no defensible neutral, so their unity balance
    and form-only comparison remain explicit. The whole-gun pairs retain the
    white-backdrop balance. Material boundaries at the head, strap and latch
    are clean in the delivered atlas. The side has no ledge, the pin reads as
    a flush same-steel circle, the bottom plate is seated, and the narrow slots
    follow the unchanged blades. Both rear fence edges curve toward the strap;
    the rib and bead are visible from the unchanged eye frame. The plainer
    shoulder junction, broader lower throat, simpler plate border and open
    forward hook pocket remain visible differences from the photographs.
    Reopened the clip and wide-opening strips and ammunition views; the
    accepted controls, extraction and manual loading sequence remain intact.

## Round 4 measured proof

`make -C guns/sxs` and the separately invoked `make -C guns/sxs check` both
complete with exit status 0. The final review audit accepts 294 render records
from the current exports and 19 correctly timed clip WebPs. Gun stills, rakes
and photo pairs use the baked `export/sxs.glb`; standalone ammunition retains
its accepted diagnostic export. No kit or common module changes this round.

| Check | Current result |
| --- | --- |
| Gun budget, including hidden ammunition alternatives | 37,822 / 38,000 triangles; 178 spare |
| Delivery | 6,175,024-byte GLB; one material; three 2048 images, from a 4096 GPU bake |
| PNG bytes: BaseColor / Normal / ORM | 260,530 / 1,078,947 / 1,596,544 |
| Geometry and intended states | source and reimport pass; 929 state samples each |
| Actual surface contact checks | 246 / 246 pass in both source and reimport |
| Half-frame motion sweep, all 19 clips | 1,715 source / 1,728 imported samples; zero violations; no allowed-contact exceptions |
| Largest measured motion penetration | 0.113714 mm imported, within the 0.20 mm tolerance |
| Independent native rebuild | 104 entries identical: positions at 1 nm, normals at five decimal components, exact clip keys/interpolation |
| Accepted baseline preservation | 96 / 104 native entries identical to a fresh build of `8a6ff08`; changed entries belong to the requested action/head/plate/pin work |
| UV atlas | no outside or degenerate UV triangles; overlap fraction 0.000001028, within the kit's 0.00001 tolerance |
| Texel density at 2048, p5 / median / p95 | 1,344 / 2,394 / 2,996 px/m |
| Projection | zero missed interior texels in all five channels; independent ownership audit and negative control described in pass 23 |
| Reimport serialization | maximum affine-position error 0.000191 mm; maximum sampled posed-surface error 0.000253 mm |

The exterior gauges in `build/serialization.json` are measured on actual
exported triangles. Both fence crowns are Z=57.350 mm against the barrels'
57.350 mm top line. Pair and breech widths are both 51.900 mm. Fitted arc
centers differ from the measured bore axes by at most 0.009 mm right and
0.019 mm left. The fitted rolls are 18.475 mm against the photograph's
18–20 mm estimate. The largest sampled head/bar side step is 0.00001 mm;
the largest plate/bar step is 0.004 mm. Lower-edge section fits give
7.96 mm radius against the photograph's 7–9 mm estimate. Each slot is
6.000 mm around a 5.400 mm blade, giving 0.300 mm on either side. The photo
scale estimates carry about ±2 mm uncertainty, as recorded in `refs/SOURCES.md`.
They are visual estimates, not published part dimensions.

The action/right, action/top and action/bottom landmark RMS residuals remain
61.57 / 41.00 / 81.00 px respectively. These are disclosed camera/form
comparison residuals, not a dimensional acceptance test; the three-landmark
bottom fit is particularly limited. Named meshes remain separate for form
diagnostics. Finish work and eventual skin consolidation remain held, and
no docs JPGs have been generated or committed.

## Earlier rounds — archival record

The following round-three and earlier claims describe their old unbaked outputs.
Round four above supersedes them; they are not current delivery claims.

# Covey 26 — form round 3: action

This is a form review, before finish/look-dev. The current inspection GLB has
constant materials and no texture images. Fine edge-radius/checkering normal
bakes and used finishes are still held; vertex-normal transfer from our own
dense sources is not described as a texture bake. No final docs JPGs are committed.
The accepted stock drops, cheek station, overall/barrel length, trigger blades,
rig, 19 clip schedules, 1.7.0 meanings and ammunition are retained.

## Current region review

Each entry names what still differs from the photograph. Passing geometry or
camera checks does not approve the look. Native pairs include unobscured panels,
a review-only photo outline over the render, and numbered residual arrows.
Black-background macros have no defensible neutral: unity gains remain explicit.
The white dealer backdrop supplies the whole-gun comparison balance. Neither
case color nor bluing is assumed to be neutral, and no finish match is claimed.

- **Fences and standing breech.** Replaced the flat-topped shoulders and melted
  crown with genuine round dome patches joined into one closed action skin.
  The barrel ends meet the standing-breech plane, without the former rectangular
  shoulder under them. The photo's fence roll is less proud and has a more
  delicate transition into its strap channel. Ours retains about 1.45 mm of
  fence crown above the tube crown and a broader central land; the reference's
  exact exterior radius is not independently calibrated. Inspect
  [right action pair](renders/checkpoint/pairs/action-pair.jpg),
  [left action pair](renders/checkpoint/pairs/action_left-pair.jpg),
  [loaded breech](renders/checkpoint/beauty/breech.png), the fence and standing
  breech sections, and both action raking sides.
- **Ground faces, bar and knuckle.** The sides and upper shoulders are explicit
  planes. The bar's lower edge sweeps up, its underside rolls into a narrower
  neck, and the concentric knuckle continues the same skin. Its cross-pin ends
  are flush circles. The photo has a more uniform, softer lower neck and more
  subtle arrises; ours has a stronger shoulder-to-side break and a small front
  hook pocket. The long underside opening is covered. No render or check
  relabels that remaining pocket as the photo's shallow plate joint. Inspect
  [underside pair](renders/checkpoint/pairs/action_bottom-pair.jpg),
  [right rake](renders/checkpoint/beauty/action_rake_right.png),
  [left rake](renders/checkpoint/beauty/action_rake_left.png),
  [bottom rake](renders/checkpoint/beauty/action_rake_bottom.png), and the bar,
  knuckle, knuckle-side and floor/lump sections.
- **Short upper body and wood head.** The upper head ends just behind the
  fences; wood comes forward beside the strap. The strap continues alone
  along the wrist. The photo has deeper rounded fingers and a less diagonal
  side seam. Ours uses simpler ground shoulders and a more pronounced diagonal
  inletting line. Inspect
  [top pair](renders/checkpoint/pairs/action_top-pair.jpg),
  [top rake](renders/checkpoint/beauty/action_rake_top.png),
  [controls](renders/checkpoint/beauty/top_controls.png), and the shoulder/head
  section. The accepted straight hand, pull and comb/heel drops remain.
- **Top lever and safety.** The lever is long, narrow and tapered, lying close
  above the strap on a round boss, below the fence crowns. Its closed tail
  follows the strap instead of swinging across it. The photo's tail is more
  pointed and its boss sits a little farther behind the fences. The accepted
  lever pivot and 25-degree clip travel remain. The safety stays farther back
  in its original guide/detents; its checkering remains a later normal field.
  Inspect the top pair, controls, aimed view, and Safety/SafetyOn/Open strips.
- **Guard and triggers.** The bow is a broad flat band with a swept front
  return and a rear wrist tang. The photo's rear return curls more sharply
  and its lower bow is less shallow. Both accepted trigger blades keep their
  forward-facing concavity, forward toes, pivots, pull direction and barrel
  assignment. The photo's front blade is longer/more delicate; it was not
  changed to conceal a framing residual. Inspect
  [trigger pair](renders/checkpoint/pairs/trigger-pair.jpg),
  [three-quarter blades](renders/checkpoint/beauty/trigger_quarter.png),
  underside pair and Fire/FireLeft strips.
- **Aimed view and rib.** The cited sporting sight picture now derives the eye
  height from the actual rib and bead, preserving the cheek station and stock
  drops. A short forward rib leads to the bead between the fences, with the
  lever/action below. The original dip after the chambers hid that surface;
  the sighting surface now follows the straight line between its accepted
  breech/muzzle endpoint heights. Joined flats and the seated valley filler
  remain. The rib is still broad at the rear; matting is held. Inspect the
  exact [socket view](renders/checkpoint/beauty/aimed.png), both barrel sections
  and the top orthographic view. No raised presentation eye substitutes for
  the socket, and no human mesh/personal fit is certified.
- **Forend and iron.** Kept the accepted 34.4 × 24.2 × 173 mm envelope. Replaced
  the sausage side with a flat land, defined lower edge, nearly straight taper
  and a supported slanted nose. Dense sculpt normals carry the carved surface
  without increasing the wood budget. Our plan-view nose is more squared off than the photo, the lower profile
  remains deeper forward of the latch, and the iron wraps less far up the
  wood. The original inset latch and two bearing cups remain simpler. Inspect
  [side pair](renders/checkpoint/pairs/forend_side-pair.jpg),
  [underside pair](renders/checkpoint/pairs/forend-pair.jpg),
  [forend](renders/checkpoint/beauty/forend.png), both forend sections and reload
  strips. There is no hand mesh; guide/shell clearance does not prove hand fit.
- **Open breech, extractor and ammunition.** Loaded above/behind views show
  the accepted shells in the extractor. The open photographic pose remains
  an empty, 30-degree comparison; canonical clips still open 42 degrees.
  The reference's broad upper extension differs from our narrower under-lug
  construction and cannot be used as a shared camera landmark. Our chamber
  backs/extractor and its exterior flats remain visibly different construction.
  Inspect [open pair](renders/checkpoint/pairs/open-pair.jpg),
  [detached flats](renders/checkpoint/pairs/barrel_flats-pair.jpg), loaded breech,
  lumps, opening strip and all reload/unload strips. The calibrated open
  camera is explicitly constrained to the muzzle-side hemisphere; a low-RMS
  chamber-facing fit was rejected. No clip or ammunition dimension changed.

## Round 3 critique log

12. **Planes and domes.** Color/value: retained dark inspection steel and checked
    unclipped raking highlights; the black reference has no neutral for a hue
    claim. The old crown and rounded-box shoulders were visibly melted. The
    first replacement still produced a curtain at the height-field boundary.
    Rejected it and rebuilt the domes as real closed spherical patches joined
    to explicit ground planes, without a smooth union.
13. **Head, controls and guard.** Color/value: made the underside readable with
    the existing procedural inspection softbox, without claiming the photo's
    case-color response. The full-width upper head still extended too far back
    because its seam depended only on height. Brought its outer upper corners
    forward, fitted the wood head, lowered/lengthened the narrow lever, added
    its round boss and refitted the broad guard's front return. The accepted
    trigger geometry and rig schedules remain.
14. **Fitted eye and forend.** Color/value: compared the exact socket picture
    against gray, judging bead and rib visibility. The old vertical offset
    was unsupported; the primary sporting coin rule supplies a reproducible
    sight-picture construction. It exposed the rib's longitudinal dip, which
    was corrected while retaining endpoint sections and valley seats. The
    forend's round side and nose were replaced by supported flat lands and a
    defined slanted tip within the accepted envelope.
15. **Photographic framing.** Color/value: black-backed macros remain form-only;
    white whole-gun backdrops retain their recorded balance. Re-observed shared
    breech corners, hinge, lever boss, visible trigger root and guard seats.
    Held all macro review lenses at 150 mm, bounded the observed view within
    20 degrees, and rejected an open fit on the wrong side of the breech.
    Added native-pixel arrows and a separate silhouette overlay to every pair.
    Sparse low residuals are not form acceptance. The underside remains the
    least certain comparison; its seat/length differences cannot be explained
    by one global translation or scale.
16. **Final raking and reproducibility.** Color/value: checked the actual export's
    side lands, dark cavities and rolling dome highlights. The underside's
    lower-radius transition still broke abruptly, so rolled the exposed neck
    across its section and eased it into the unchanged front bearing. Before
    reduction, conditioned the constructive seams with the same 6 µm weld
    used on the game mesh and a 1 µm coordinate grid. Canonical face/corner
    order makes both reduction and dense-source normal transfer reproducible.
    Independent builds retain the original strict 1 nm position/five-decimal
    normal comparison, rather than loosening it to hide variation.

17. **Head-section fit.** Color/value: reviewed the bright wood/metal seam in
    the top pair before grain or finish could hide it. The stock cage still
    sampled the narrower unwarped station after the action seam moved forward.
    Matched the head section at its actual warped station and returned the
    seam around the strap root. Cleared a small unsupported wood feather at
    the front well rim instead of filling its resulting boundary triangle.
    Retested the actual contacts, topology and all clips after rebuilding.

18. **Latch-land normals.** Color/value: the flat underside pair exposed
    star-shaped dark highlights around the routed latch. The transferred corner
    normals were choosing an inlet wall for some corners on the exterior land.
    Preserved the dense lower-land polygon normals and kept the reduced land's
    own surface normals at the route. The clean underside preview removes the
    stars without moving vertices, changing the accepted envelope or spending
    more triangles. The surrounding carved corners retain smooth normals.

## Photographic fit limits

The 150 mm macro lens is a review-camera choice, not recovered EXIF. The
observed hemisphere and 20-degree view cone prevent arbitrary orbiting, but
three-point comparisons remain sparse. The left-action fit in particular
cannot certify the rest of the shape. The open photo's differing extension is
excluded from calibration. The photo outline is extracted only in the review
compositor: no contour or image is read by modeling or shaders. Threshold
lighting holes remain in some outlines; the unobscured photo panels are the
authoritative visual comparison.

The companion diagnostic fits a 2D similarity correction to the residuals.
A large remainder demonstrates nonuniform disagreement; it cannot, by itself,
distinguish a form difference from an uncertain landmark or perspective.
The region critiques above supply that visual judgment. The underside's
remaining disagreement is explicitly retained rather than minimized by fitting
an unshared contour.

## Measured form and source limits

| Quantity | Actual exported surface | Reference basis |
| --- | ---: | --- |
| Lever length / thumb width | 78.45 / 7.09 mm | plain top photograph; estimated target 76–82 / 6.5–8 mm |
| Round lever boss | 11.20 mm | plain top photograph; estimated target 10–12 mm |
| Lever thickness | 1.89–1.93 mm | plain side photograph; about 1.5–2.1 mm |
| Lever height above strap, underside gap | 0.67–1.33 mm | plain side photograph; about 0.5–1.5 mm |
| Guard band width × thickness | 12.40 × 1.63 mm | plain underside/side; about 12–14 × 1.5–2.1 mm |
| Eye above actual comb | 42.811 mm | CPSA sporting coin-rule construction; see below |
| Eye above extended actual rib | 3.612 mm | same construction |
| Forend overall W × D × L | 34.40 × 24.20 × 172.99 mm | accepted nominal 34.4 × 24.2 × 173 mm |
| Forend rear, Y=211 mm | 34.16 × 22.54 mm | actual triangle-plane intersection |
| Forend front, Y=320 mm | 28.24 × 16.16 mm | actual triangle-plane intersection |
| Wrist, Y=-15 mm | 32.17 × 37.88 mm | actual triangle-plane intersection |

Lever and guard reference sizes are explicitly photo-scale estimates, about
10% uncertain, not published dimensions. Preview pixels, assumed exterior
scale, native sources and licenses are recorded in [SOURCES.md](refs/SOURCES.md).
Thickness is measured vertically through the actual lever at three stations;
the gap is from its underside to the actual strap. Width excludes the boss
where labeled thumbpiece. These are mesh measurements, not parameter echoes.

At the accepted Y=−123 mm cheek station, the actual comb is Z=17.689 mm.
The [CPSA handbook](https://www.cpsa.co.uk/userfiles/files/CTSH.pdf), printed p. 4-2,
sets the sporting sight picture by a pound coin 200 mm ahead of the breech.
Using the [Royal Mint historical 3.15 mm thickness](https://www.royalmint.com/collect/collector-resources/designs-and-specifications/one-pound-coin-designs/)
and the actual rib Z=54.492 mm at Y=315 mm, the line to the
bead center extends back to eye Z=60.500 mm. The local comb drop
39.199 plus eye-above-rib 3.612 gives
42.811 mm above the comb. The measured coin-ray error is
0.000004 mm. This is a cited sight-picture fit, not an anatomical
claim. The original Brownells cheek station and cited 38/63 mm drops remain.

## Native photographic residuals

| Pair | RMS px | Remainder after 2D similarity px | Interpretation |
| --- | ---: | ---: | --- |
| [right](renders/checkpoint/pairs/right-pair.jpg) | 4.11 | 3.89 | accepted whole silhouette; local form |
| [left](renders/checkpoint/pairs/left-pair.jpg) | 5.60 | 5.30 | class stock/gauge differences; local form |
| [action](renders/checkpoint/pairs/action-pair.jpg) | 55.73 | 55.03 | fence/breech proportions and original head seam; form |
| [action_left](renders/checkpoint/pairs/action_left-pair.jpg) | 0.25 | 0.25 | three-point fit only; sparse evidence, not form acceptance |
| [action_top](renders/checkpoint/pairs/action_top-pair.jpg) | 40.89 | 39.41 | boss station, head corners and tail; form |
| [action_bottom](renders/checkpoint/pairs/action_bottom-pair.jpg) | 77.20 | 77.02 | guard seats/length; form plus perspective/landmark uncertainty |
| [open](renders/checkpoint/pairs/open-pair.jpg) | 39.75 | 39.74 | different exterior extension/lug construction; form |
| [barrel_flats](renders/checkpoint/pairs/barrel_flats-pair.jpg) | 12.51 | 12.49 | original lug/flats dimensions; form |
| [forend](renders/checkpoint/pairs/forend-pair.jpg) | 2.87 | 2.84 | nose/iron proportions; local form |
| [forend_side](renders/checkpoint/pairs/forend_side-pair.jpg) | 2.48 | 2.41 | lower profile/nose; local form |
| [trigger](renders/checkpoint/pairs/trigger-pair.jpg) | 26.14 | 25.41 | guard return and accepted blade differences; form |

No pair has a dominant residual that one additional global translation, scale
or roll removes. This does not rule out perspective or observation uncertainty,
especially in the underside. The open pair now crops out the guard and fits
barrel rim corners and the hinge rather than the unshared extension.

## Current verification

`make -C guns/sxs` passes the complete form build and evidence audit.
`make -C guns/sxs check` also passes a separate assembly/serialization run.
The form GLB has **37,728 triangles**, 54 named rigid meshes,
17 bones, 19 clips and 14 sockets. It is 1,765,484 bytes, with
9 inspection materials and zero texture images. The source retains dense
geometry for later normal baking. Normal-map radii/checkering, UV/atlas checks,
finishes, wear and bake-loss assessment remain outside this form gate.

The separate source/import checks pass topology, intended states, required
surface contacts and all 19 half-frame sweeps, with no contact allow-list.
They cover 1,715 / 1,728 samples, with 246 contact records each and
0.11371 mm maximum penetration against a 0.20 mm visual tolerance. No mesh has
nonmanifold edges, zero-area triangles or reversed volume. The joined tube
separating-plane measurement remains a distinct check on the same-bone skins.

Ground-side/shoulder plane probes measure at most 0.000118 mm departure from a
best-fit plane over their sampled patches. Those measurements establish the
geometric flats; the raking renders establish the highlight behavior.

Independent fresh builds agree on all 104 geometry/normal/rig/socket/clip
entries at the original 1 nm position and five-decimal normal comparison.
Serialization separately compares 1,715 affine samples and event surfaces. Maximum
affine position error is 0.000191 mm; event-surface displacement is at most
0.000253 mm. This does not substitute for the contact sweeps.

All current evidence is under `renders/checkpoint/`: `contact-sheet.jpg`,
`photo-pairs.jpg`, `source-photo-pairs.jpg`, `sections/sections.jpg`,
`clips.jpg`, `opening.jpg`, `strips/`, `ammunition.jpg`, and the individual
beauty views linked above. The provenance/timing audit checks hashes and real
clip durations. The audit confirms 305 current render records and 19 real-duration
WebPs. Hero luma p1/p50/p99 is 1.07 / 47.87 / 205.59; deep shadows occupy 21.08%
of the visible hero, with zero all-channel clipping. This is inspection tone,
not albedo or finish acceptance.

No kit or shared/common source changed. Main was merged before modeling; the
family interface conflict retained all additive supplements. A general kit
candidate is deterministic mesh/corner canonicalization before reduction,
with explicit precision policy and regression fixtures. Nothing is needed
from the lead beyond reviewing this form gate. No final docs images are added.

## Round 2 record, superseded by the current region review

# Covey 26 — form round 2

Look-dev remains held. All current views are constant-material inspection
renders. No normal-map edge transfer, checkering, finish, wear or final atlas
is being passed off as complete. The previous checked region list was too
lenient and is superseded below. This document requests review; it does not
approve its own remaining form and measurement limitations.

## References and photographic framing

Commons was searched first. Its plain American whole-side photograph is sharp
as a whole gun but does not resolve the action at 600 pixels. The new primary
plain 12-gauge dealer set supplies native 1876–4767 px originals: both action
sides, top, underside, splinter underside and assembled open action. The
registered smaller-gauge dealer set supplies complete left/right views with
the entire gun over 800 native pixels. The primary wide 12-gauge sides clip
the muzzle and are never labeled whole-gun references. The old decorated
sideplate action and loaded sidelock are excluded from current acceptance.

See [SOURCES.md](refs/SOURCES.md) for every original, dimensions, attribution,
license and use. The tile-pyramid fetcher assembles the dealer's original
pixels without tracing or changing a contour. It downloads images only.
No photo or measured outline is consumed by the geometry generator.

The white backdrop in the whole-gun pair is balanced in linear light. The
black-background macros contain no reliable neutral; they are form-only
comparisons, with unity gains explicitly recorded. No bluing or case-color
patch is assumed gray. Each critique begins with value; these materials are
inspection constants and cannot establish photographic finish or wear.

`build/cameras.json` retains native observations, fitted cameras, residuals
and view constraints. Blender independently verifies the projections. Eleven
pairs cover right, left, both action sides, top, bottom, open action, detached
barrel flats, bottom and side of the forend, and triggers. RMS is not form
acceptance. The whole-gun fits are about 4–6 native pixels. Eight macro view directions
are locked after visual inspection; translation, focal estimate and roll
fit the framing. They retain up to 132 px native residuals because original
contours and landmarks differ. This limitation is visible in every pair.

An early open pair fitted circles while viewing the wrong side of the breech.
It was rejected despite its smaller RMS. The corrected comparison fixes a shallow view from above and forward of
the breech, with an empty 30-degree photographic presentation and its
extractor pressed home. The 42-degree canonical clips and extractor travel
are unchanged. The open reference also has a raised top extension with a rectangular cut,
which our original under-lug construction does not share. It must not be
misidentified as our barrel flats. The detached flats reference has no action or forend: only the
visible barrel region can be compared; it cannot establish an assembled fit.
The matched flats shot omits the action and forend to match the detached
photograph; the full exported gun and canonical clips are unchanged.

## Round 2 critique passes

7. **Photographs and sections.** Color/value: black backgrounds have no
   defensible neutral, so no quantitative finish match is claimed. The old
   action reference was the wrong construction class. The old breech outer
   walls overlapped, the rib was a post, and the forend was too round/full.
   Replaced the acceptance set, cut joined breech flats, filled the top valley
   with a seated tapered rib, and built a slim, flat-sided splinter with its
   channels, iron pocket and bottom latch. Added separate wood dimensions to
   the section labels so barrel width cannot be mistaken for wood width.
8. **Forging and furniture.** Color/value: checked the roll-off on dark steel
   and the head's shaded seam before detail. The first union left a slab-like
   bar/receiver transition, long rear body and an oval wood head that made
   wings beside the metal. Rebuilt the forging's changing sections, rounded
   belly, bowed rear seam, tapered bar and concentric knuckle; matched the
   wood head to its inlet section. Replaced the proud slotted hinge heads
   with the ends of a small flush cross pin. The source forging is retained.
9. **Lever, guard and actual assembly.** Color/value: underside views were
   unreadably black, so added a procedural inspection softbox below them.
   The lever was a thin plate; the first thicker sweep collided at the crown
   and stock. Lowered the central rear crown, seated the thick shank and
   swept thumbpiece, and opened the stock inlet. Refitted the guard bow and
   wrist tang, and moved the rear blade's root back 12 mm while retaining
   direction, angle and assignment. Corrected actual collisions instead of
   adding clearance exceptions. A tiny folded Boolean flap at the guard-tang
   inlet was removed by its topology, not filled into a nonmanifold patch.
10. **Stock drop and exact eye.** Color/value: judged the bead and rib against
    the neutral gray card. A bead hit alone did not prove visibility. The
    source/import checks now test every occupied skin along that ray and rays
    to three forward rib stations. Lowered the comb to the published drop
    and located the cheek station 35 mm behind its nose. The exact socket
    view shows a short rib length and the bead, with the action below. The
    vertical human cheek-to-eye citation remains missing: see measurement
    limits below. A 45 mm inspection lens makes the actual sight picture
    readable; it does not alter the socket or imply a physiological FOV.
11. **Exported shading and final evidence.** Color/value: checked deep
    cavities, unclipped bright regions and the crown's moving highlights.
    The roof's inherited Boolean face labels were unsafe after reduction;
    use actual surface location to identify the analytic roof field. A dense
    normal-transfer experiment was rejected. The bar now shares continuous
    surface strips with the body; its former overlapping table union was
    removed, and the fence shoulders were made more proud of the tubes. Keep
    the raking views and dense-source comparisons visible: smoothness and
    photographic form still require the lead's judgment, not a passing mesh
    check. The final sheet review also rejected a low-RMS forend side camera that
    had drifted below the wood. Locked that view and isolated the barrel
    assembly for the detached flats reference, where the action had occluded
    the part under review. Rebuilt all current evidence against the final
    output hash.

## Region review and remaining differences

- **Action, fences, top lever and safety.** The forging now has bowed rear
  inletting, rounded top/bottom shoulders, a tapering bar and circular knuckle
  bearing. The primary photo's fences have a more cylindrical rear roll;
  its rear head has deeper scalloped fingers around the tang. Ours remains
  fuller through the central crown, with a plainer rear seam and a more
  exposed spindle. The bar/receiver transition and crown highlights are the
  weakest form cues and must not be called fixed by future texturing.
  Inspect `beauty/action.png`, `action_left.png`, `top_controls.png`,
  `rake_right.png`, `rake_left.png`; `pairs/action-pair.jpg`,
  `action_left-pair.jpg`, `action_top-pair.jpg`, `action_bottom-pair.jpg`;
  and the standing-breech, bar and knuckle side sections.
- **Triggers and guard.** Both faces retain their forward concavity, forward
  tips and barrel assignment. The guard is a swept flat band with a rear tang
  following the wrist. The photo has a longer, more delicate front blade and
  a flatter lower bow. Ours is thicker through the lower corners and has
  more front clearance. Inspect `beauty/triggers.png`, `trigger_quarter.png`,
  `pairs/trigger-pair.jpg`, `strips/Fire.jpg` and `FireLeft.jpg`.
- **Barrels, rib, bead and muzzles.** Joined outer flats replace overlapping
  skins at the breech. The rib fills the valley, follows the barrel seats and
  tapers to the muzzle. The photo has a narrower, more visibly raised rib at
  the rear; ours has a broad shallow-concave face there. Matting is held for
  the normal map. Inspect side/top/front orthos, `beauty/muzzle.png`,
  `aimed.png`, both whole-side pairs and both barrel sections. The exact eye
  sees the bead and a short forward rib; most rear rib remains foreshortened.
- **Breech, extractor and lumps.** Our joined-tube construction has a narrower
  web and stepped central lumps. The reference has broader continuous flats
  and a different single lug profile. No detached photograph proves hinge
  engagement. Actual hook/pin, breech, rim/extractor and bite/shoe probes do.
  Inspect `beauty/breech.png` (loaded from above/behind), `open.png`,
  `lumps.png`, `pairs/open-pair.jpg`, `barrel_flats-pair.jpg`, floor/lump
  section, `opening.jpg` and the Open strips. Shell dimensions are unchanged.
- **Forend and iron.** The splinter is narrower than the barrels, with nearly
  flat tapering sides, rounded bottom and two top channels. The photo's nose
  is squarer and rises more sharply; ours is rounder and more pointed. Its
  iron wraps farther up the rear wood; ours uses two separate bearing cups
  and a simpler inset latch. The bottom photo alone cannot validate that
  latch design. Inspect `beauty/forend.png`, `pairs/forend-pair.jpg`,
  `forend_side-pair.jpg`, two dimensioned wood sections and the reload strips.
  No hand mesh is present, so hand contact is not proven; socket and shell
  paths clear the revised furniture through all clips.
- **Stock, wrist and butt.** Kept the straight hand, length and front-trigger
  pull. Widened the wrist and fitted the head to the bowed forging seam.
  Actual rib/wood rays now measure published-class comb/heel drops. The
  whole-gun reference has a different grip and butt treatment; its geometry
  cannot establish our exact straight-hand contours. Our head is plainer and
  its tang inlet seam broader. Inspect `beauty/stock.png`, both whole-side
  pairs, both butt sections, wrist and tang-inlet sections.
- **Ammunition.** Accepted dimensions and shared module are unchanged. Our
  unmarked red hull and primer are simplified original exterior forms.
  Inspect `ammunition.jpg`, `beauty/breech.png` and reload/unload strips.
  Markings, head finish and hull wear remain held.

## Measured dimensions and evidence limits

The imported GLB measures 1079.95 mm overall, 660.40 mm barrels and 369.63 mm
front-trigger pull. Stock drop, measured against a straightedge reconstructed from actual points on
the rib centerline, is 38.05 mm at the authored comb nose and 63.05 mm at the heel,
against published 38/63 mm. This centerline datum approximates a
straightedge: the concave rib edges rise about 0.22 mm above it. The cheek station is 35.00 mm behind that nose,
within the primary fitting source's 31.75–38.10 mm range.

**The human vertical fit is not sourced.** The socket is (0,−123,67) mm,
49.31 mm above the actual comb at its station. That is a measured model offset
and an authored vertical fit, not a measured human cheek weld. The original
45 mm justification is withdrawn. A reproducible mounted-person measurement
with scale is still needed to satisfy that part of the brief.

Wood-only wrist at Y = −15 mm is 32.23 × 37.74 mm. The forend's overall wood
bounds are 34.40 × 24.19 × 173.01 mm; its sections at Y = 211 / 320 mm are
34.39 × 22.53 / 25.90 × 18.68 mm. These are actual triangle intersections.
The photos constrain proportions, but their absolute wrist/forend dimensions
were not independently calibrated in millimeters. Do not label these numbers
as published specifications or precise photo measurements. This reference
measurement requirement remains weaker than requested.

## Verification scope

`make check` runs separate source and fresh-import topology/contact sweeps
through all 19 clips at half-frame intervals, with a 0.20 mm visual tolerance
and no contact allow-list. Actual-surface probes cover hinge, knuckle, breech,
chambers, rim support, locking bites, lever seat, safety and sight visibility.
A separate global-X surface-extrema check proves that the two joined tube
skins do not overlap; their shared bone would exclude them from the normal
cross-bone sweep. A second independent build checks deterministic geometry, normals, bones,
sockets and animation. Source/import affine samples and event surfaces prove
serialization separately from assembly correctness. Timed WebPs are decoded
and summed at their real durations. `audit.json` checks current source hashes.

Current proof: `make -C guns/sxs` and `make -C guns/sxs check` pass.
The staged gun is 34,638 triangles, 54 rigid meshes, nine inspection materials,
zero images and 1,630,020 GLB bytes. Source/import sweeps cover 1,715 / 1,728
samples across 19 clips, with 246 measured contact records each and 0.17201 mm
maximum penetration. Rebuild comparison passes all 104 entries at 1 nm position
rounding and five decimal normal components. The presentation audit confirms
301 current render records and all 19 real-duration WebPs. Hero luma p1/p50/p99
is 1.07 / 46.21 / 204.27, with zero all-channel clipping; this is a tonal-range
check on inspection materials, not finish acceptance.

No kit or shared/common file changed in this round. There are no final UVs,
textures or bake-loss claims. No hand mesh or ergonomic fit test is supplied.

## Prior checkpoint history, not current acceptance

The following log records the first session's investigations. The owner's
round-2 rejection supersedes its favorable judgments and reference choices.

## Critique log

1. **Blockout, both sides and sections.** Color/value: constant dark steel and
   brown wood make no finish claim; pale Workbench illumination is unsuitable
   for color acceptance. The first allocation was too expensive, the tang
   floated over the wrist, and the safety lacked a convincing seat. Rebuilt
   tang inlets and fitted the controls; reduced hidden bevel and cage costs.
   Preserved the stock's changing comb/cheeks and the splinter's barrel
   channels instead of flattening either into an extruded profile.
2. **Raking form and trigger photograph.** Color/value: retained dark material
   values and inspected the light roll-off, without matching the colored
   floor's hue. The action looked like a rounded cap on a separate plank.
   Rebuilt a changing-section body with continuous fences and a unioned water
   table. Broad guard band, blade thickness and forward-concave trigger faces
   were checked in side and underside views. Narrow wires and backwards
   hooks were rejected. Hero framing was enlarged to retain the whole butt.
3. **Open assembly and actual contacts.** Color/value: dark cavities must stay
   legible under the breech. The extractor bridge/stem, rim seats, lock shoes
   and lever spindle exposed real interpenetrations during motion. Cut their
   actual passages and reset the movement sequence; no clearance allow-list
   hides them. The lower tang/safety support and forend iron were fitted to
   their actual surfaces. Shell skins were made closed without overlapping
   disconnected head/hull components.
4. **Cycles exported close-ups.** Color/value: no all-channel white clipping
   is accepted in the hero; black metal must retain deep cavities and rolling
   highlights. The shell heads had a false concave reflection after export;
   restored planar head normals. The exact aimed view hid too much rib;
   raised the eye and remeasured the comb offset. The roof showed triangular
   highlight boundaries, and some cross-pin heads were buried or reversed.
   Rebuilt longitudinal curvature and normal fields, seated both pin pairs,
   and added a recessed steel floor/rails under the safety.
5. **Sharp breech photo and section recheck.** Color/value: white-balanced the
   new sheet-backed macro; no sampled finish is accepted yet. Replaced the
   undersized open-action target. A section exposed a floating bottom rib;
   rebuilt it to join both lower barrel skins. Coincident extractor-relief
   cuts left hatch-like sliver faces; moved the cutter into empty bore space.
   The remaining roof sawtooth came from a hard minimum in the fence/land
   surface, not lighting. A continuous radius removed it under the same
   raking camera (`renders/crown-review/action.png`). Final reduction also
   exposed a microscopic folded corner at the lever bore. Welding within
   0.0001 mm after reduction repairs it; both topology checks must pass.
6. **Whole photographic framing.** Color/value: retained the declared neutral
   patches; finishes remain held. Chamber-only fitting concealed an incorrect
   whole-assembly comparison. Inspecting the full sharp original and the
   neighboring photographs showed its barrels were detached. Reclassified
   that pair as barrel detail, rather than forcing a false hinge fit. Corrected
   the left/right shell identification and removed an arbitrary camera-height
   prior in the assembled loaded photograph; its fit improved from 120.3 to
   26.7 native pixels. Both action and shells now share the photographed
   framing. Fixed a presentation-only extractor press that an active animation
   had overwritten. The pose is frozen before applying it, then asserted.
   Restored smooth sculpt shading on the dense controls in their comparison
   scene; inherited flat cage faces had produced bands absent from the game
   normals. Enlarged the stock/lump framing and gave trigger/safety clips
   their own close cameras so their real travel can be judged.
