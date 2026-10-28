# Guns Interface 1.6.0 — rocking magazine and reciprocating handle

Additive to [1.0.0](../INTERFACE.md), the [1.2.0](../bolt/INTERFACE.md) and
[1.3.0](../smg/INTERFACE.md) supplements. Versions 1.4/1.5 remain reserved by
other family members. This visual binding changes no existing meaning.

`src/interface.py` supplies capabilities, states, 60-Hz durations and events.
Reuse `ready`, `last_ready`, `empty_closed`, `safe_ready`, `auto_ready` and
`auto_held` with their existing occupancy/selection meanings. The new capability
is `magazine_rocks_in=True`. `charging_handle_reciprocates=True` reverses the
SMG's optional capability value, without changing its semantics. No hold-open:
`FireLast` and empty `Charge` both end closed. No manually locked-open state.

Meters, grip origin, Blender +Y forward/+Z up/+X right; glTF −Z forward/+Y up.
Root remains identity. Whole-instance stance, recoil and inspection rotation
belong to the consumer. Six base sockets remain scene-root references.
`Socket_ChargingHandle` rides the carrier-fixed handle's full frame;
`Socket_Magazine` rides the magazine's full frame. Never use translation alone
to spawn the departing loaded/empty magazine.

## Driving the rock-in path

Play the supplied Reload or ReloadEmpty animation. The magazine bone's origin
is the front visual hook, so its initial/final rock is rotation about that
point. At `front_hook` the front is engaged; the seated pose arrives at
`magazine_in`, then the release returns at `catch_engaged`. Do not linearly
interpolate from a detached transform directly to the seated socket. A game
with procedural hand IK samples the same animated magazine socket, including
rotation. The authored path is an exterior animation estimate, not a mechanical
or ergonomic specification.

Both reload clips use these frames: release 16, unhook 40, out 56, offscreen
replacement 72, front hook 112, seated 132, catch 138. Reload finishes at 150
(2.50 s), retaining its chambered round. ReloadEmpty starts empty and closed,
then draws the handle at 174 and chambers at 188, finishing at 210 (3.50 s).
Drop/spawn the departing variant at `magazine_out`, before substitution. Loaded
and empty GLBs share the inverse full magazine frame.

Fire/FireSemi last .20 s: shot 2, eject 4, chamber 8, reset 12. FireAuto is a
.10 s loop (600 rpm visual cadence), with shot 0, eject 2 and chamber 6; the
trigger stays held. AutoStart/AutoStop join that loop to auto-ready. FireLast
closes empty at 8, resets at 12. Selector seeks safe/automatic/semi at 0/18/36;
individual selection clips and state holds are also supplied. Inspect is
2.50 s; Charge is a 1.00 s empty rack returning empty and closed.

Ammunition visibility is STEP. Feeding is a discrete occupancy handoff, without
a feed-path or spring simulation. A fired-case display starts just outside the
port; the eject event supplies the separate case GLB for game effects. Pause
retains `{version, clip, frame}` and resumes that same clip and time. Do not
jump to Idle with the magazine absent. State commits occur at clip completion.

The checkpoint has inspection constants and no UV/texture acceptance. Final
delivery is reserved for the existing kit atlas exporter, rigid-bone isolation,
named clips and DETACHABLES, with one canonical 2048 set.
