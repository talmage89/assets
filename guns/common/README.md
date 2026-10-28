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
