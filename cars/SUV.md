# Alder X220 — compact crossover source form checkpoint

An original 2018–2022 two-row unibody crossover on **225/65R17** tires.
The long roof, raised package, squared separate arch moldings and rising
six-light greenhouse distinguish it from the family's sedan and pickup.
The narrow swept lamps and curved horizontal blades share Alder's fictional
family language. Every surface is scripted; photographs supply measurements
and comparisons. This checkpoint stops before optics, handles, interior,
underbody, paint, wear, UVs, baking and SUV export.

The main family index is [README.md](README.md). The manufacturer comparisons,
height definitions and construction estimates are in [REFERENCE.md](REFERENCE.md);
[refs/SOURCES.md](refs/SOURCES.md) records reference authors, URLs and licenses.
The [2020 Toyota US brochure](https://cdn.dealereprocess.org/cdn/brochures/toyota/2020-rav4.pdf)
and [2020 Honda US sheet](https://hondanews.com/en-US/honda-automobiles/releases/release-47ef5ef525f391ae783334075a01030f-2020-cr-v-specifications-features)
provide the RAV4 LE and CR-V LX FWD comparisons. No trademark, downloaded model,
photographic texture or HDRI enters the asset.

## Package and actual source measurements

| Quantity | X220 actual surfaces / pivots | Reference class |
| --- | ---: | --- |
| Overall length | 4600.1 mm | RAV4 4595 / CR-V 4625 mm, rounded |
| Body width including moldings | 1841.6 mm | Both about 1855 mm |
| Roof / rail height | 1679.0 / 1700.0 mm | Honda 1679 mm FWD; Toyota 1701 mm including antenna |
| Wheelbase | 2690.0 mm | Toyota 2690 / Honda 2662 mm |
| Front / rear track | 1600.0 / 1610.0 mm | Both 1600 / 1618 mm in the selected FWD trims |
| Front / rear overhang | 960.1 / 950.0 mm | Original front-longer allocation; see reference trim distinctions |
| Full mirror width | 2117.0 mm | Same-generation Honda UK brochure: 2117 mm |
| Hood leading center | 970.7 mm high | Brief: 900–1000 mm |
| Hood rise / windshield rake | 6.38° / 58.19° from vertical | Brief: windshield 55–60° |
| Backlight rake | 30.73° from vertical | Brief: 20–35° |
| Approach / departure | 19.45° / 20.97° | Toyota 19 / 21°; Honda FWD LX 18.1 / 25.3° |

The 1855 mm width is a design target; the measured body is slightly narrower.
Roof/rail height is separated from manufacturers' antenna-inclusive heights.
Toyota's explicitly rail/no-rail launch figures are preliminary, and Honda's
FWD/AWD height difference is not presented as a rail measurement. Those source
qualifications remain in REFERENCE.md.

The nominal tire diameter is 724.3 mm; the mean loaded circle is about 714.3 mm
across, with a light 5 mm parked deflection. Actual tire extents/hub height feed
the supporting-plane angle calculation. These are outer-form angles, not a
suspension/underbody certification. The future running-clearance allowance is
205 mm; no finished underbody exists to measure it against the manufacturers'
198/208/213 mm values. All four arch crown gaps are approximately 55 mm.

## Sections and construction

| Section | Shoulder height, mm | Upper inward lean | Lower lean | Soft die turn | Actual glass lean |
| --- | ---: | ---: | ---: | ---: | ---: |
| mid front door | 1037.0 | 16.0–16.4° | 4.6 → 15.6° | 9.0° | 19.0° |
| b pillar | 1050.0 | 16.0–16.4° | 4.6 → 14.4° | 9.2° | 19.4° |
| mid rear door | 1062.0 | 16.0–16.4° | 4.6 → 15.5° | 9.5° | 19.4° |

The low crease turns over the recorded 80 mm normal interval. A 50 mm chord
finds about 2.0–2.1 mm of inward die hollow. Glass lean uses the central 60 percent
of the actual pane's ray-hit height span. The old fixed-height chord and its
hit-object names remain in the JSON as invalid-for-glass debugging evidence.
Normal-derived paint lean and position-derived glass chords are distinguished.

Fenders swell about 34 / 29 mm beyond the same-height central door section.
Three hood sections measure roughly 13–14 mm above the actual hood boundary. The separate
lower door moldings are about 155 mm high, stand 6–7 mm proud, and tuck under.
Arch bands are about 60 mm wide with 19–23 mm sampled proud offsets and 22 mm
inward flanges. The skirt, arch and lower bumper are molded solids, not paint.

The body starts as one connected regular quad sheet. A 1900-quad section/line
net is refined twice, fitted at its **control vertices**, then Catmull–Clark
subdivided. The fitted parent has 30,400 control quads with four-valent interior
vertices. The evaluated parent is never fitted/projected after subdivision.
Feature-aligned game chart samples retain its normals. Projected panel cuts
and actual reveals come after fairness; aperture mouths retain the original
skin planes and get their own gauge rims. Wrapped lamp borders retain their
concavity in parameter space. Outside/back/rim provenance survives repeated
cuts, rather than guessing the skin from its normal angle.

Painted steel is 0.9 mm; fascia/moldings 3 mm; main glass 4.8 mm. Ten actual
front/rear door-edge samples (six left, four right) measure approximately 4.500 mm. The source checks measure
actual mesh positions, plane cuts, normals and ray hits. Neither the nominal
construction inputs nor a successful serialization test certify an assembly.

## Face and rear

The measured headlamp paths are 654–657 mm long and about 100 mm tall, wrapping
onto the fender; exact left/right measurements are retained in the source
report. Quarter/gate taillamps are split across the gate reveal, with corner
heights in the brief's 120–200 mm range. Closed optical cases have curved beds
and returns. Fine optical parts remain absent.

The grille is 61–64 mm behind its mouth, the lower intake about 55–58 mm, and
corner pockets 48–49 mm. Forty-two independent center rays through the eight
recesses and six optical blanks find no remaining painted/plastic skin over
the openings (three rays per opening; the JSON records every result).
The plate mouth measures **319.5 × 170.4 mm**, with about
25–26 mm depth and an overhead lamp. Reflector/exhaust pockets have real depth.

Backlight centerline height is **301.5 mm**, against
photo-ratio estimates of 314 mm Toyota and 275 mm Honda. Its top/base widths
are **1158.8 / 1392.5 mm**; the actual rear belt
width at its base gives a **161.6 mm** D-pillar per side. Near-rear photographs
estimate Toyota 1145 / 1464 mm glass and 196 mm pillars, and Honda 1132 / 1386 mm
and 235 mm. These photograph ratios have perspective/height/pick uncertainty,
not OEM section precision. The X220's pillar estimate remains slimmer than
these photo estimates. Local front/rear plan circles and their exact three
source samples are retained (526.4 / 487.7 mm); neither bumper is claimed constant-radius.

Mirror housings are 260 × 125 × 164 mm rounded wedges. Their bottoms sit near
the belt, on small door-mounted sails. Roof rails have three low feet per side;
the short spoiler is supported at the gate header. The temporary inner closure
is inboard of the wells and is not a drivetrain or cabin.

## Allocation and authored pivots

**58,422 game triangles**, versus a 40k–60k budget and 50k aim.
Five temporary clay materials, zero image textures, no SUV GLB. The later target
is one 2048 BaseColor/Normal/ORM set (about 16 MiB with block compression/mips),
reusing family responses where appropriate. Detail must replace/reduce this
near-cap source allocation, especially hidden backs/cases, rather than add to it.

| Part group | Triangles |
| --- | ---: |
| Pillars / fixed upper frame | 1,884 |
| Four painted door skins | 4,052 |
| Hood, gate, roof, fenders and quarters | 12,404 |
| Painted fascias | 4,828 |
| Main glazing and side panes | 2,948 |
| Arch / door / bumper moldings and skid finish | 11,026 |
| Four liners and inner closures | 1,168 |
| Lenses, optical cases, grille, intake and recesses | 8,528 |
| Temporary cavity closure | 12 |
| Mirror housings, panes and sails | 1,016 |
| Roof rails and feet | 672 |
| Gate spoiler | 268 |
| Four tires | 5,632 |
| Four wheel proxies | 3,984 |
| **Total** | **58,422** |

The following counts include each pivot's attached parts:

| Group / parent | Triangles |
| --- | ---: |
| AlderX220 | 35,658 |
| Door_FL | 2,180 |
| Door_FR | 2,156 |
| Door_RL | 1,412 |
| Door_RR | 1,432 |
| Hood | 728 |
| Liftgate | 5,240 |
| Wheel_FL | 2,404 |
| Wheel_RL | 2,404 |
| Wheel_FR | 2,404 |
| Wheel_RR | 2,404 |

`build/suv/form-check.json` additionally lists **every individual mesh**, all
measurements, samples, source hash and explicit deferred checks. These are
source triangles, not claimed exported file/draw-call counts.

Four door pivots use local Z at the lower A/B stations (left 0–72°, right
−72–0°). Hood local X is authored −65–0° at its cowl hinge; the gate local X
is 0–75° at the roof hinge. Four wheel pivots use local X ±360°. The shared
wheel generator also supplies front ±35° steering pivots with authored kingpin
inclination/caster/scrub. These are initial metadata/groupings: complete upper
frame attachment, hinge/steering sweeps, struts and clearances remain pending.
No motion or mechanically complete vehicle claim is made. Family side suffixes
follow the authored X sign; the driver is on +X, behind Door_FR.

## Rebuild and proof scope

From the clone root:

```sh
make -C cars BODY=suv
make -C cars BODY=suv check
make -C cars BODY=suv check-repeat
```

`BODY=pickup` remains the default. The SUV recipe downloads only its own ignored
image/PDF references, builds high/game sources, checks both densities, measures
the game, checks parent/game section curvature, verifies the six camera
projections, renders through the shared GPU lock and composes the evidence.
UV/texel-density, bake/normal-map, GLB/re-import, finishing and motion checks are
explicitly deferred by this form gate. The finite curvature plots retain every
raw sign crossing and annotated character/roll region; they do not certify a
global automotive Class A surface.

The independent one-thread regeneration matches all 139 meshes' geometry,
corner normals, transforms, materials and parents exactly. Pickup preservation
matches all 454 source meshes and all 150 GLB accessors, embedded maps and
delivery graph; the two freshly compared GLBs are byte-identical at 11,530,740
bytes, SHA-256 `ec70cde87fbe50fb814cc14c900ee324e254711b5bfa5d3735aef166b146de5b`.
This is a fresh before/after source build and re-export of unchanged finalized
maps, not a claim about the historical published binary or repeated GPU bakes.
The JSON is `build/suv/pickup-preservation.json`. No kit or sedan code changed;
the shared build edit is the Makefile's three-line SUV selector.

## Images and review

The final source evidence is under `renders/suv-form/`: `contact.jpg`, two
three-quarter clay views, dimensioned side/front/rear/top and paired front/rear,
raking side, seven reflection-band views including the driver's hood, parent
and game curvature plots, three actual side sections, raw and supplemental
profile overlays, rear photographic measurements, and four calibrated pairs
in **both** clay and stripes. All 24 renders carry the same source hash. The
contact contains 42 review views. No checkpoint image or rebuildable asset is
committed. [REVIEW.md](REVIEW.md) records rejected candidates and each critique.

## Camera fit and held-out profile residuals

| Fitted photograph | Native chassis-anchor RMS |
| --- | ---: |
| crv front | 7.19 px |
| rav4 front | 8.91 px |
| crv rear | 8.40 px |
| rav4 rear | 9.99 px |

These five-anchor fits calibrate the chassis, not the body shape. Independent
Blender projection checks agree with the solver within 0.003 px. Supplemental
side cameras hold an estimated 85 mm lens; their 1.21 / 0.59 px chassis RMS is
not evidence of an accurate silhouette or recovered EXIF.

Both orthographic and supplemental perspective overlays register only the two
wheel centers. The photograph retains perspective. No body outline is fitted,
deformed or used to build the geometry. Held-out photo picks have approximately
15.5 mm uncertainty before camera/trim uncertainty. Axis residuals and nearest
silhouette distances are both retained, because steep glass amplifies a
fixed-column height difference. These sparse holdouts do not certify every
point along the outline.

| Overlay / make | Worst fixed-axis residual | Worst nearest silhouette distance |
| --- | ---: | ---: |
| Orthographic / RAV4 | 128.5 mm | 83.2 mm |
| Orthographic / CRV | 110.1 mm | 81.0 mm |
| Supplemental perspective / RAV4 | 128.5 mm | 101.5 mm |
| Supplemental perspective / CRV | 244.3 mm | 102.6 mm |

**The requested approximately 40 mm agreement is not met.** The raw overlay's
largest nearest misses are the Toyota lower tail (83 mm) and Honda front
bumper (81 mm). Upper-profile nearest misses are approximately 49 / 46 mm.
Perspective overlays change the residuals, not the conclusion. Original end
styling and the photographs' uncertain projection both contribute; the result
is retained as a failed form target rather than explained away by the camera.

## Final checkpoint verification and limitations

`make -C cars BODY=suv WIDTH=1600 SAMPLES=40`, `make -C cars BODY=suv check`,
and `make -C cars BODY=suv check-repeat` completed successfully. Game/high
source audits have zero errors/warnings. Both eleven-section curvature reports
have no sign crossings outside the documented feature/roll zones; raw crossings
remain plotted. The source topology, clear-opening rays, dimensions and repeat
comparison have explicit results under `build/suv/`. These checks do not approve
the visual form, motion or any deferred delivery checks.

The game source is 1,354,146 bytes / 58,422 triangles / 139 meshes; the
high-density source is 2,793,119 bytes / 119,492 triangles / 143 meshes. These
rebuildable files are ignored. Five diagnostic materials and zero image maps
are present; delivery GLB/map sizes are inapplicable at this checkpoint.
The source SHA-256 for all 24 renders is
`1e6a4e905132772e0c87db434b516d25173cae7cbedd97631db025421263febd`.
The 42-view manifest is `renders/suv-form/review-manifest.json`.

All seven final review pages and the full-size key clay pairs were opened.
Front/rear hero foreground luminance p99 is 219 / 206 on the display-byte
scale; neither hero has a clipped 255 channel. Deep cavities remain visible.
The low-sun image is dark (median 19) and is a weaker presentation of the side
than the studio and stripe views; it does not replace them.

The candidate still needs a form round: grazing reflections pinch at the
A-pillar foot/header and rear pillar/quarter transitions; lamp-edge margins and
window/applique corners are too regular or locally uneven; the grille lands
and broad rear plastic read older/cheaper beside both makes. The measured
D-pillar estimate is slimmer than the photo ratios. The profile tolerance is
unmet, and the source allocation is near its cap before any interior. This is
an auditable form-review candidate, not accepted form or a finished asset.
No kit change was required. A future general reflection-field/section sampler
could reduce duplicated diagnostic code, but it should not hide raw reversals
or turn finite checks into a global fairness claim.
