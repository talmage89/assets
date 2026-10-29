# Propane Defense Rill 39 — form checkpoint

An original **stamped-receiver 7.62×39 rifle** visual game prop, generated in
Blender 5.2 from scripts. Fixed wooden furniture, a curved 30-round steel
magazine, reciprocating handle and three-position selector use the family's
grip frame. The fictional maker/model is **Propane Defense Rill 39**.

This is **form round 3, before look-dev**. Constant inspection finish, separate
named meshes, rig, clips and five inspection GLBs are provided. Original fine
geometry is baked to one shared 2048 normal for receiver stampings, grip
checkering, sight graduations, button knurl and smooth forging surfaces. Final
UV packing, furniture bake, finish, wear and canonical atlas delivery remain
behind the checkpoint. No
documentation JPGs are committed at this stage.

`renders/checkpoint/contact-sheet.jpg` collects the form evidence.
`renders/checkpoint/beauty/` contains exported-GLB Cycles views, including
side/top/front, both raking quarters, receiver, controls, trigger, sights,
furniture, open action and exact Eye. Actual triangle cuts are in
`renders/checkpoint/sections.jpg`; dimensions in `dimensions.jpg`.
Photo comparisons are in `pairs/`, source comparisons in `source-pairs/`.
Real-duration playback and strips live in `strips/`; `clips.jpg` and numbered
`clip-inspection-*.jpg` pages expose every rendered sample.

`contacts.jpg` shows isolated source/export seating diagnostics.
`trigger-measurements.jpg` records sparse photographic observations separately
from actual mesh measurements. `form-observations.jpg` adds the sight estimates,
with explicit scale assumptions and uncertainty. Fifteen local orthographic
side/top/front diagnostic views isolate the sights, gas block, cover and grip
with their seating parts, independently of photo camera fits.
[REVIEW.md](REVIEW.md) links every revised region and records the remaining
differences from its photograph.

## Exterior dimensions and construction

| Measure | Design basis |
| --- | --- |
| Overall length | 881.38 mm measured; about 880 mm class target, including rounded end fasteners/brake |
| Barrel exterior span | 415.00 mm measured |
| Intended unloaded class mass | About 3.1 kg; reference target, not a mesh mass measurement |
| Magazine capacity | 30; three staggered display rounds |
| Receiver visual gauge | About 1 mm, with magazine well and trigger opening |
| Sight spacing | About 360 mm; original visual layout |
| Eye behind rear notch | About 295 mm; photo estimate 268 ±35 mm, subject to pupil/perspective uncertainty |
| Texture reservation | One 2048 BaseColor/OpenGL Normal/ORM set after acceptance |

The U receiver has both skins, bottom bends, deformed guide dimples and
separate rivet heads. The cover has flat flanks, a low rear longitudinal bead,
shallow roof-only transverse ribs, a downturned rear closure and retaining
button. Visible inserts, gas tube, a curved forged gas-block neck/collar,
bayonet lug and supported cleaning rod describe the
exterior construction. The brake has a slanted hollow sleeve silhouette.

Stock, handguards and molded grip use supported subdivision cages with
changing rounded sections. Dense originals are retained in `High_Sources` for
the later bake. The handguards have a real U channel and finite rounded lands.
The magazine has hollow formed sheet, integral ribs, folded spines, a tilted
floorplate, display catches, curled lips and separate follower/round owners.
The trigger's concave face faces the muzzle and its rounded tip curls forward.

The rear sight has a low saddle with raised front hinge cheeks, an open spring
channel, a narrow graduated leaf, a wider U-notch crosspiece and a sleeve with
two knurled cylindrical buttons. The front forging has a rectangular window,
flush round drum ends and a thin open sheet hood with broad side ears.
The lower handguard front has a fitted retaining cap; its left-side wire loop
is the sling attachment. It replaces the former rectangular wire approximation
of the retainer. The grip has flat checkered side panels and smooth rounded
front/back straps. All checkering is in the normal map. Original smooth cages
supply the retained high-detail forgings.

The actual trigger envelope is **21.99 mm tall, 8.43 mm deep and 5.16 mm across**;
its measured section-center bow is 4.92 mm. Its toe is only 2.61 mm forward of
the pivot. Sparse photo estimates give heights of 22.35/21.60 mm and bows of
4.98/4.65 mm, with about 20% uncertainty. The guard's actual flat-band section
is 13.00 ×1.65 mm at the documented cut, with a straight bottom, tight bends
and vertical front. Its front forms a folded housing, and the release has a
curved stamped finger tab.

| Round 3 exterior form | Photo estimate | Actual game triangles |
| --- | ---: | ---: |
| Rear saddle above barrel, rear/middle | 18 ±4 mm | 14.99 / 16.60 mm |
| Rear hinge cheek above barrel | 26 ±6 mm | 29.32 mm |
| Leaf width | 12.9 ±2.1 mm | 13.40 mm |
| Notch crosspiece width | 27.3 ±4.4 mm | 25.99 mm |
| Front hood sheet gauge | 1.3 ±0.5 mm | 1.01 mm |
| Front hood band depth | 12.6 ±2.0 mm | 14.00 mm |

Photo estimates use the [museum side](refs/SOURCES.md), Erik Gregg's Commons
rear macro and the sharp AKOptions front side/rear photos. They depend on
explicit visual-scale assumptions; the barrel datum is occluded in the side
photo. They are not independent caliper measurements. Native points, ratios,
scale and limitations are in [REFERENCE.md](REFERENCE.md) and
`build/round3-photo-observations.json`. Actual dimensions come from triangle
intersections/bounds in `build/form-measurements.json`, including three rear
saddle stations and a two-surface hood gauge ray.

The dark receiver-side rectangle above the magazine front was the outer end
of the front-lug cradle bridge, coplanar with the exterior skin. It was an
exposed interior support, not a marking. Its end now seats within the inner
receiver wall; the hook/contact surfaces and magazine path are retained.

The hidden bolt-lug and hammer/sear surfaces have **zero render geometry**.
Their accepted Bolt/Hammer transform bones and timing remain. The source and
fresh GLB inventory assert this absence, so those surfaces cannot appear in
any clip or camera. The visible carrier/piston are inert display geometry.
The barrel has an oversized display void, without chamber or rifling. Contact
checks establish exterior visual seating, coverage and sampled clearance;
they do not supply an operative internal mechanism.

## Frame, rig and clips

Meters, palm origin; Blender +Y forward/+Z up/+X right, glTF −Z forward/+Y up.
Root remains identity. Consumer stance/recoil transforms the complete instance.
The [1.6.0 supplement](INTERFACE.md) reuses the existing occupancy/select-fire
states and adds `magazine_rocks_in`. No last-round hold-open. The full manifest
is [src/interface.py](src/interface.py); generated values are in
`build/interface.json`.

The carrier slides, the retained Bolt transform rotates, and the handle follows
the carrier's full frame. Trigger, selector, paddle, catch and magazine have
separate visible owners. The magazine pivots around its front hook during the
initial/final rocking phase. Its socket supplies the complete detached spawn
transform. Rounds use STEP occupancy; feeding is a visibility handoff.

Twenty clips: Idle, IdleEmpty, IdleSafe, IdleAutoReady, IdleAuto; Fire,
FireSemi, FireAuto, FireLast; Reload, ReloadEmpty, Charge, Inspect; Selector,
SelectorSafe, SelectorSemi, SelectorAuto, SelectorAutoSemi; AutoStart, AutoStop.
FireLast closes empty. Reload retains the chamber; ReloadEmpty racks after the
exchange. FireAuto is a .10-second visual loop. Pause/resume retains the same
clip and frame, including magazine absence. All event frames and durations are
documented by the supplement and executable manifest.

The revised selector's poses are safe 0°, automatic −10°, semi −15° about its
unchanged X axis. These angles clear the wider stamped blade through firing;
the 20 clip names, schedules, events and 1.6.0 meanings are unchanged. Sight
adjustments and the buttplate trap remain static display settings.

Six base sockets remain at scene root. Socket_Magazine follows Magazine;
Socket_ChargingHandle follows ChargingHandle. Socket_Eye is an actual aiming
frame, without presentation offsets. The aimed render looks through the notch
at the post against the gray procedural studio. The cheek-weld source's
obscured pupil and perspective make its estimate uncertain; this is not an
ergonomics certification.

## Checkpoint budgets and rebuild

The gun is budgeted at **30k–40k triangles**, including every animated display
representation. `build/triangles.json` records each actual part, total and
detached variant. The checkpoint uses eight inspection material types and one
geometry-only normal image; that is not final material/draw-call acceptance.
The final target is one canonical 2048 atlas, approximately 16 MiB compressed
with mipmaps and consumer texture reuse.

| Inspection GLB | Triangles | Materials | Bytes |
| --- | ---: | ---: | ---: |
| Gun | 39,956 | 8 | 6,422,792 |
| Loaded magazine | 6,756 | 4 | 4,373,224 |
| Empty magazine | 4,596 | 2 | 4,311,876 |
| Cartridge | 960 | 2 | 23,452 |
| Fired case | 704 | 1 | 18,752 |

The gun and both magazines embed the same 2048 normal payload (4,184,091 bytes);
the cartridge and case contain no images. The normal was baked at 4096 and
vector-filtered to 2048. Its inspection UV regions reserve space for the eight
projected parts; other surfaces sample a flat normal. This is not a final UV
overlap/texel-density acceptance. A consumer-compressed BC5 normal with mipmaps
would use about 5.3 MiB, shared across the three instances. The gun retains
17 rigid bones, eight sockets and 20 clips.

`make -C guns/ak model` and `make -C guns/ak check` passed. The checks evaluated 1,556 source clip poses,
1,568 imported clearance samples and 44 visual contact/visibility groups.
The import's maximum posed-surface difference was 0.0000894 mm. Ordinary
cross-owner clearance uses 0.2 mm tolerance; four named visual joints have
separate finite overlap bounds, fully reported in `build/check.json`.
These checks establish visual assembly and serialization, with the functional
limitations documented below and in the review.

Nine additional fixed-surface seating checks cover the new sling/retainer,
gas forging and rear spring in source and fresh GLB
(`build/form-measurements.json`).
The current outer envelope is 881.38 ×65.29 ×246.74 mm; the width includes
the added left-side sling loop, and the revised hood sets the upper extent.

The front lug's contact is measured throughout the engaged rock-out and rock-in
phases. The rear catch seats at the holds and is deliberately released during
extraction. Safe coverage uses 71 rays over the handle neck's actual swept
cross-section: 68 hit the selector and three hit the closed handle at the front
end. Each selector detent is checked on surfaces. Every clip finishes with the
carrier against its front shoulder. Both top cases lie under their lips, and
all visible-round transforms remain fixed relative to the magazine through
every sampled pose, before and after GLB import.

```sh
make -C guns/ak                 # references, model, source/import checks, media
make -C guns/ak check           # construction, states, swept clips and round trip
make -C guns/ak model           # five inspection GLBs and retained source
make -C guns/ak render match    # exported stills and source/export photo pairs
make -C guns/ak sections strips extra review
```

Requires installed Blender 5.2, Python/Pillow/NumPy, Noto Sans, make and flock.
GPU Cycles uses the inherited shared kit lock. Scratch stays inside `build/`.
No downloaded code, meshes, materials, textures or lighting are used.

| Generated output | Purpose |
| --- | --- |
| `build/ak.blend`, `build/ak.glb` | Separate game parts, retained dense molds, rigid rig and clips |
| `build/magazine_loaded.glb`, `magazine_empty.glb` | Full-frame detachable variants |
| `build/cartridge.glb`, `case.glb` | Inert exterior ammunition silhouettes |
| `build/check.json`, `serialization.json` | Independent construction/state/sweep and serialization evidence |
| `renders/checkpoint/` | Form evidence, pairs, sections and real-duration clips |

The ammunition uses a muted olive lacquered-steel appearance as an issued-era
visual choice. It is an inert exterior approximation. Fictional headstamps,
maker markings, generated wood grain, fine molded surface texture and caused
wear belong to the subsequent look-dev stage, pending form acceptance.

The planned issued wear stays at named causes: gray phosphate at receiver
edges/rivets and cover crests; narrow polished selector edges; bright carrier
rails and handle contact; matte carbon at the brake and gas block; worn varnish
and quieter raw wood at the handguard and wrist; compressed fiber dings at the
stock's toe and heel. Every site must survive the single 2048 atlas and remain
visible in the full-frame hero before finish acceptance.

References, authors, licenses, specification discrepancies and direct URLs are
in [refs/SOURCES.md](refs/SOURCES.md); the measurement plan and uncertainty are
in [REFERENCE.md](REFERENCE.md). White balance uses documented neutral
patches in `build/white-balanced/corrections.json`; no reference pixels enter
asset geometry or materials. Round 3 changes no kit or common module. The
initial checkpoint added only two new common modules,
`ammo762_visual.py` and `interface_v1_6.py`; existing common/kit/other guns are
unchanged.
