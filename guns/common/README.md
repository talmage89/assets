# Guns-only helpers

- `render.main(config, manifest)` imports a blend/GLB, poses it with the kit,
  renders `config.SHOTS`, and writes source hashes and pose/camera metadata.
  Config supplies `floor_height(source)`, `DEFAULT_SHOTS`, `PHOTO_POSES`,
  and `STRIP_SHOT`. Optional `configure_scene(scene, source)` and
  `prepare_shot(scene, shot)` hooks supply asset lighting/inspection setup. Manifest supplies `CLIPS` and `FPS`.
  `FINAL_STAGE=True` restricts input to an exported GLB; optional `RENDER_STAGE`
  labels final metadata. Existing checkpoint defaults are unchanged.
- `strips.main(base, manifest, source=..., output=...)` calls that gun's
  `src/render.py` and makes uniformly sampled strips and real-duration WebP loops.
  Optional keyword `engine` defaults to Workbench; final assets can request
  Eevee/Cycles with `samples`. GPU engines use the kit lock wrapper.
  Static holds retain an explicit one-frame WebP duration when the encoder
  would otherwise discard timing; every decoded clip duration is checked.
- `interface_checks.manifest(binding)` checks the versioned event/state schema;
  `scene_frame(arm, clip, frame)` checks identity Root and scene-root socket axes.
  Each gun independently asserts intended states and physical contacts.
- `photo_matches.L(world_mm, pixel, weight)` defines measured landmarks;
  `camera_shots(path)` loads the kit's solved photo configurations. Each gun owns
  landmarks and photographic action selection. Photographs never enter modeling.

These are stable entry points for subsequent guns. Mechanical schedules, anatomy
and dimensions never belong in the shared renderer or schema checker.

## One signature-motion GIF

`make -C guns/<gun> gif` imports the exported GLB, uses that gun's
`src/final_shots.py` studio/lights/AgX settings, and writes `docs/motion.gif`.
Requires the already installed ffmpeg, Blender and Python/Pillow. The render
runs through the kit GPU lock. Nothing is installed or downloaded.

`gif.py` is the shared driver and Blender worker; `gif.mk` adds the opt-in
Make target after a gun defines `EXPORTS`. Each member owns `src/gif.json`:
source/output paths relative to its folder, a clip `sequence`, `fps` (20 or 25),
`width` (at most 960), `colors` (256), Cycles `samples`, RGB background bytes,
and its camera (`location`, `target`, `lens`, `aspect`, `exposure`). Sequence
entries accept optional `start`/`end` at the manifest's source frame rate.
Trims must land on GIF sample times. Multiple clips join at the authored time
boundary, as the lever's separate Fire and Cycle require. No rig or effect
motion is added by the presentation tool.

Sampling uses time on half-open clip intervals, including fractional source
frames; each GIF tick is exactly 4 or 5 centiseconds. A lossless GIF-container
edit adds 50 centiseconds to the first frame. Decoded delays must exactly equal
the sampled motion duration plus this hold. Fixed Cycles seed and sample count,
a flat RGB composite, one global ffmpeg palette, no dithering, and ffmpeg
palette-use rectangle differencing / transparent unchanged pixels avoid
background noise and local-palette flicker. Output over 450,000 bytes fails;
tighten the crop or trim a static span before reducing rate or palette.

`build/gif/` retains raw PNGs, composited frames, palette, render provenance,
`timeline.json`, `report.json` (decoded size/rate/colors/bytes/delays/hash), a
complete contact sheet, native-width numbered frame pages, and `playback.html`
for continuous 1× browser playback. These stay ignored. The worker uses a
byte-identical GLB copy so member diagnostic part-attribution hooks cannot load
source geometry. Every rendered triangle, texture and animation comes from the
export; only the existing procedural studio is added.

```sh
python3 guns/common/gif.py --asset guns/bolt --preview # six quick clay framing views
make -C guns/bolt gif                                # full final and GIF
python3 guns/common/gif.py --asset guns/bolt --encode-only # re-encode current final frames
python3 -m unittest guns.common.test_gif              # timing, delay, palette and repeat fixture
```

Preview frames cannot be encoded. Encoding checks every frame's GLB hash,
Cycles provenance, camera and sampled time. Re-encoding unchanged final frames
is byte-identical; a full render uses the same deterministic seed and settings.
The shared tool has no finished-gun allow-list: later members supply the same
small config, their own final studio module and the Make include.
