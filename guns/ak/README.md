# Propane Defense Rill 39 — form checkpoint

An original **stamped-receiver 7.62×39 rifle** visual game prop, generated in
Blender 5.2 from scripts. Fixed wooden furniture, a curved 30-round steel
magazine, reciprocating handle and three-position selector use the family's
grip frame. The fictional maker/model is **Propane Defense Rill 39**.

This is the requested **checkpoint before look-dev**. Constant inspection
materials, separate named meshes, rig, clips and five inspection GLBs are
provided. UVs, sculpt baking, final wear, the canonical 2048 set and final
kit atlas delivery remain behind the checkpoint. No documentation JPGs are
committed at this stage. Generated images below are deliberately plain paths.

`renders/checkpoint/contact-sheet.jpg` collects the form evidence.
`renders/checkpoint/beauty/` contains exported-GLB Cycles views, including
side/top/front, both raking quarters, receiver, controls, trigger, sights,
furniture, open action and exact Eye. Actual triangle cuts are in
`renders/checkpoint/sections.jpg`; dimensions in `dimensions.jpg`.
Photo comparisons are in `pairs/`, source comparisons in `source-pairs/`.
Real-duration playback and strips live in `strips/`; `clips.jpg` and numbered
`clip-inspection-*.jpg` pages expose every rendered sample.

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
separate rivet heads. The cover has shallow pressed ribs, a rolled shoulder,
rear closure and retaining button. Visible inserts, barrel bands, gas tube,
inclined gas-block neck, bayonet lug and supported cleaning rod describe the
exterior construction. The brake has a slanted hollow sleeve silhouette.

Stock, handguards and molded grip use supported subdivision cages with
changing rounded sections. Dense originals are retained in `High_Sources` for
the later bake. The handguards have a real U channel and finite rounded lands.
The magazine has hollow formed sheet, integral ribs, folded spines, a tilted
floorplate, display catches, curled lips and separate follower/round owners.
The trigger's concave face faces the muzzle and its rounded tip curls forward.

Hidden bolt, piston and hammer shapes are **nonfunctional animation proxies**.
The barrel has an oversized inert display void; it has no chamber or rifling.
No pressure-bearing locking, working sear, feed mechanism, tolerance or
manufacturing model is supplied or certified. Assembly checks describe visual
fit and sampled animation clearance. The regional differences and unfulfilled
functional-contact requests are explicit in [REVIEW.md](REVIEW.md).

## Frame, rig and clips

Meters, palm origin; Blender +Y forward/+Z up/+X right, glTF −Z forward/+Y up.
Root remains identity. Consumer stance/recoil transforms the complete instance.
The [1.6.0 supplement](INTERFACE.md) reuses the existing occupancy/select-fire
states and adds `magazine_rocks_in`. No last-round hold-open. The full manifest
is [src/interface.py](src/interface.py); generated values are in
`build/interface.json`.

The carrier slides, the bolt proxy rotates, and the handle follows the
carrier's full frame. Trigger, hammer, selector, paddle, catch and magazine
have separate owners. The magazine pivots around its front hook during the
initial/final rocking phase. Its socket supplies the complete detached spawn
transform. Rounds use STEP occupancy; feeding is a visibility handoff.

Twenty clips: Idle, IdleEmpty, IdleSafe, IdleAutoReady, IdleAuto; Fire,
FireSemi, FireAuto, FireLast; Reload, ReloadEmpty, Charge, Inspect; Selector,
SelectorSafe, SelectorSemi, SelectorAuto, SelectorAutoSemi; AutoStart, AutoStop.
FireLast closes empty. Reload retains the chamber; ReloadEmpty racks after the
exchange. FireAuto is a .10-second visual loop. Pause/resume retains the same
clip and frame, including magazine absence. All event frames and durations are
documented by the supplement and executable manifest.

Six base sockets remain at scene root. Socket_Magazine follows Magazine;
Socket_ChargingHandle follows ChargingHandle. Socket_Eye is an actual aiming
frame, without presentation offsets. The aimed render looks through the notch
at the post against the gray procedural studio. The cheek-weld source's
obscured pupil and perspective make its estimate uncertain; this is not an
ergonomics certification.

## Checkpoint budgets and rebuild

The gun is budgeted at **30k–40k triangles**, including every animated display
representation. `build/triangles.json` records each actual part, total and
detached variant. The checkpoint uses eight constant material types and no
texture images; that is inspection data, not final draw-call acceptance.
The final target is one canonical 2048 atlas, approximately 16 MiB compressed
with mipmaps and consumer texture reuse.

| Inspection GLB | Triangles | Materials | Bytes |
| --- | ---: | ---: | ---: |
| Gun | 39,524 | 8 | 1,943,468 |
| Loaded magazine | 6,400 | 4 | 143,360 |
| Empty magazine | 4,240 | 2 | 93,932 |
| Cartridge | 960 | 2 | 23,452 |
| Fired case | 704 | 1 | 18,752 |

All five contain zero texture images. The gun has 17 rigid bones, eight sockets
and 20 clips. A second factory-startup model build produced five byte-identical
GLBs. These sizes describe the unbaked inspection outputs.

`make` and `make check` passed. The checks evaluated 1,556 source clip poses,
1,568 imported clearance samples and eleven visual contact/optical assertions.
The import's maximum posed-surface difference was 0.0000894 mm. Ordinary
cross-owner clearance uses 0.2 mm tolerance; five named visual joints have
separate finite overlap bounds, fully reported in `build/check.json`.
These checks establish visual assembly and serialization, with the functional
limitations documented below and in the review.

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
maker markings, generated wood grain, molded texture and caused wear belong
to the subsequent source-normal/look-dev stage, pending form acceptance.

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
asset geometry or materials. This asset adds only two new common modules,
`ammo762_visual.py` and `interface_v1_6.py`; existing common/kit/other guns are
unchanged.
