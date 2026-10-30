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
  `constrained(match)` retains an observed view direction and a 300 mm lens,
  fitting framing and roll while reporting all landmark residuals. A camera
  residual is not an acceptance test for the unchanged gun geometry.

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
`width` (at most 960), palette `colors`, render `samples`, RGB background bytes,
and `engine` (default `BLENDER_EEVEE`). Optional `output_width` samples a smaller
delivery from the full-size render before palette generation. Optional
`palette_quantizer: "octree"` uses Pillow's deterministic fast octree over all
RGB frames to retain small colored details at low palette counts. It still
uses one global palette, reserves transparency, and uses ffmpeg's unchanged
no-dither encoding. The default remains ffmpeg palette generation. The camera
(`location`, `target`, `lens`, `aspect`, `exposure`). Sequence
entries accept optional `start`/`end` at the manifest's source frame rate.
Trims must land on GIF sample times. Multiple clips join at the authored time
boundary, as the lever's separate Fire and Cycle require. No rig or effect
motion is added by the presentation tool.

Sampling uses time on half-open clip intervals, including fractional source
frames; each GIF tick is exactly 4 or 5 centiseconds. A lossless GIF-container
edit adds 50 centiseconds to the first frame. Decoded delays must exactly equal
the sampled motion duration plus this hold. Fixed sample settings, zero output dithering,
a flat RGB composite, one global palette, no dithering, and ffmpeg
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
engine provenance, camera and sampled time; a saved render-settings manifest
rejects stale frames after a clip/rate/studio-resolution change. Re-encoding unchanged final frames
is byte-identical; the finished guns use Eevee with one discarded first-frame warmup. Two full
Blender/render/encode runs must reproduce the GIF bytes. The warmup initializes
Eevee's light/shader cache before recording frame zero. Screen-traced lighting
is disabled to eliminate history-dependent variation; the same area lights,
PBR maps, exposure and AgX look supply direct studio illumination. These are
the studio and maps used by each gun's Eevee docs JPG. Cycles remains available as an explicit `engine='CYCLES'` choice, but GPU/denoising can move isolated pixels
by 1/255; it does not promise byte-identical fresh GIF renders.
The shared tool has no finished-gun allow-list: later members supply the same
small config, their own final studio module and the Make include.


### Exact bytes across GPU repeats

A clean checkout includes the committed signature GIF. Every `make gif` still
renders and encodes the complete clip. GPU arithmetic can move isolated output
pixels by 1/255, which can change the nearest palette entry and the compressed
bytes. The tool therefore compares a fresh `build/gif/candidate.gif` against
the existing GIF before replacing it.

Reuse requires the same complete configuration, asset source scripts, renderer
recipe and GLB geometry/UV/rig/animation/material structure. Those inputs are
fingerprinted in a GIF comment, never drawn in the frame. PNG payloads are
excluded from the geometry fingerprint because fresh GPU bakes can differ in
rounding; the actual rendered pixels must still pass the comparison. Each
frame must have the same size and delay, mean RGB byte error at most **0.02**,
maximum error **16**, and at most **0.01%** of pixels differing by more than
2 RGB byte levels. A recipe/geometry change or a substantive image change
always writes the new candidate. Nothing is copied into a texture or used as
lighting; an unchanged approved GIF is retained whole.

`report.json` records the fresh candidate hash, source hash, recipe fingerprint,
per-frame difference measurements, whether bytes were retained, and the shipped
reference's source hash. This is a documented golden-image comparison, not a
claim that GPU arithmetic itself is bit-exact. Removing the committed GIF
produces a fresh visually equivalent render, which can differ by rounding;
retaining it provides exact-byte clean-checkout rebuilds.

### Stamped receiver paint comparisons

AK and SMG own their complete receiver outlines in `src/paint_review.json` and
physical photographic card recipes in `src/paint_lights.json`. `make paint-review`
uses the existing independently checked delivery surfaces to rasterize complete
visible receivers, including accepted wear. It checks V P10/median/P90 against
15%/10%/15%, and brightest-luminance-decile RGB, value and normalized color
against 10%. Zero reference tails require exact zero. References are balanced
by each member's existing neutral script before sampling; no photograph enters
a material, UV, bake or export. Round 2 gives both members the Harrow studio; their cameras and GIF clips stay fixed.

The SMG additionally compares broad upper and lower lands, preventing a
whole-part statistical fit from placing the reflection on the wrong land.
These spatial observations remain explicit rather than substituting a patch
for the whole receiver. `src/paint_review.py --renders <folder> --out <folder>`
also audits archived before exports, and `--preview` labels dense-source work.

Optional refitting uses installed OpenImageIO/PyOpenColorIO and NumPy:

```sh
kit/with_gpu.sh blender -b --factory-startup --python-exit-code 1 \
  --python guns/common/paint_light_response.py -- --member smg \
  --sets paint_studio_photo,locked_photo --source guns/smg/export/smg.glb \
  --out guns/smg/build/paint-light-response --width 1100 --samples 32
python3 guns/common/paint_fit_lights.py smg
```

Unit-energy scene-linear EXRs guide nonnegative area-card energy fitting.
The objective samples ONLY the member-owned `anchors`: neutral backing and
unchanged finishes. No receiver pixel, statistic, height guard or highlight
enters it. Every basis render audits its active fixtures; the world-only
response has no area light. Numerical energy units are conditioned by measured
nonpaint response, then converted back to physical watts. White-balanced color
gains default to .95–1.05. The optional `--mixed-light` fit has two physical
color groups, above and below .25 m: R .5–2.5, G .65–2, B 1. The used Rill
test constrains this broader range with three white cloth regions in the same
photograph. It supplies no per-part color adjustment. Final acceptance requires a fresh GLB render and
rejects failed independent anchors before testing the unchanged paint bounds.
The SMG also samples narrow cards along measured crown reflection directions.
Each photograph gets one physical rig illuminating the entire gun; there is
no light linking, per-part gain or image correction. Review the fitted light
placement and rerender at full resolution before copying a reviewed recipe
into `src/`. Optional fitting dependencies are not needed for normal builds.

`--broad-only` uses the world and sixteen fixed broad cards.
`--nonpaint-studio` adds reflection cards inferred only from visible nonpaint
geometry, .35 m from the surfaces. It excludes close cards and all
receiver-derived cards. `--append` and `--indices` support audited batches;
source hashes and the existing basis order must agree. Both smaller bases
were tested after the unrestricted diagnostic basis failed. All round 2
recipes currently committed in the members are explicitly **rejected**
calibrations. Their fresh pairs expose the disagreement; they do not verify
new paint parameters, and the default builds stop at the photographic gate.

`paint_light_response.py --paint-roughness <value>` or `--paint-albedo <value>`
creates an explicitly labeled shader diagnostic for material selection. The
fitter records those overrides. Such a render cannot pass the final paint
acceptance audit: chosen inputs must first be authored, rebaked, exported and
rendered from the unmodified shipping GLB.

The receiver audit can also report broad height regions and unchanged-finish
lighting anchors. These retain independent spatial evidence: a whole-part
histogram pass does not imply that either diagnostic matches. Both the failed
spatial observations and the main requested bounds remain in the JSON.

`paint_trials.py` renders fixed-light roughness/specular grids, labeled
`REVIEW ONLY`. Its partial-film estimate is diagnostic. It cannot accept a
material or replace the required authored, baked and exported comparison.

`paint_projection.py` splits each existing rigid/named bake group by enamel
ownership and delegates baking to the kit. Nonpaint stays in its original
group; assembled ghosts preserve contact AO. No mesh or UV is modified. A
paint-only control bake tests nonpaint source attribution separately from
old/new map differences. No shared kit code changed in this round.
