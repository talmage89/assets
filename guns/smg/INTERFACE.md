# Guns Interface 1.3.0 — manually locking charging handle

Additive to [1.0.0](../INTERFACE.md) and the [1.1.0 supplement](../shotgun/INTERFACE.md).
The bolt rifle reserves 1.2.0; this member neither edits it nor changes an existing
meaning. This is a visual game-asset binding, not a mechanical simulation.

`src/interface.py` owns the capability/state/event manifest; `src/clips.py` owns
its complete 60-Hz poses. New capabilities are `closed_bolt`, `select_fire`,
`full_automatic`, `manual_handle_lock` and `charging_handle_reciprocates=False`.
The detachable magazine holds the class's 30 rounds; only three staggered display
rounds are modeled. Last-round hold-open is **false**. The empty bolt closes.

Seven existing sockets retain their paths, basis and purpose. The new
`Socket_ChargingHandle` rides the handle's complete frame for hand IK, without
being collapsed by a visibility state. `Socket_Magazine` rides the magazine.
Six attachment/effect references remain at scene root. +Y forward / +Z up / +X
right in Blender, −Z forward / +Y up in glTF; meters and palm origin. Root is
identity throughout. Consumers move the entire loaded scene for stance/recoil.

| Clip | Seconds | Start → end | Significant 60-Hz frames |
| --- | ---: | --- | --- |
| Idle | 1/60 | ready → ready | semi, closed, chamber occupied |
| Fire / FireSemi | .20 | ready → ready | shot 2, eject 4, chamber 7, reset 12 |
| FireAuto | 5/60 | auto_held → auto_held | shot 0, eject 2, chamber 5; handle stationary |
| FireLast | .20 | last_ready → empty_closed | shot 2, eject 4, closes 7, resets 12; no lock |
| Reload | 2.20 | ready → ready | chamber retained; out 34, replacement 56, seat 104, catch 110 |
| ReloadEmpty | 3.50 | empty_closed → ready | draw 30, lock 42, out 78, replacement 100, seat 148, catch 154, slap 171, release 175, chamber 181 |
| Charge | 1.00 | empty_closed → empty_open | draws 30, locks by hand 42, holds open |
| Inspect | 2.00 | ready → ready | safe 18, semi 54, partial check 82, closed 104 |
| Selector | 1/3 | safe_ready → auto_ready | seek safe 0, semi 10, auto 20 |
| SelectorSafe / SelectorSemi | .20 | ready ↔ safe_ready | committed mode at 10 |
| SelectorAuto / SelectorAutoSemi | .20 | ready ↔ auto_ready | committed mode at 10 |
| AutoStart / AutoStop | 2/60 / .10 | auto_ready ↔ auto_held | trigger held 2 / reset 6 |
| IdleAuto / IdleAutoReady / IdleSafe | 1/60 | exact state holds | no implied firing |
| IdleEmpty / IdleOpen | 1.00 | exact empty state holds | open means manually locked handle |

The 5-frame auto loop is an authored **720 rpm visual estimate**, versus the
published class's approximately 800 rpm. Consumers can scale it with their shot
rate. It keeps the trigger held; `AutoStart` and `AutoStop` connect the loop to
an auto-selected, reset trigger. `Fire` is explicitly the semi alias here, not
an assumed universal automatic clip. Last-round bookkeeping supplies `last_ready`
with an empty magazine; `FireLast → ReloadEmpty → Idle` is a tested transition.

ReloadEmpty starts **closed**, pulls and raises the nonreciprocating handle,
changes magazines while both handle and bolt hold back, then slaps the handle
down before the bolt closes. This differs legitimately from the C9's automatic
hold-open start. `Charge` deliberately demonstrates an empty rack ending manually
locked, not loaded feeding. `IdleOpen` exposes that state separately.

Ammunition ownership changes discretely with STEP keys. Ejection is a spawn event
for the separate fired case; feeding is a visibility handoff, not a cartridge-path
or spring simulation. The offscreen replacement occurs after magazine-out. Spawn
the empty detached GLB for the departing empty magazine; loaded and empty variants
share the full inverse magazine-bone frame.

Interruptions retain `{version, clip, frame}` and pause/resume that **same** clip
at that time. There is no safe jump to Idle while a magazine is absent or the
handle is locked. Reload state transitions commit at completion. Effects consume
the manifest's event times, not fixed family durations. Current checkpoint GLBs
have inspection constants; final delivery will use the existing kit atlas,
animation and DETACHABLES path, with one shared 2048 set and imported PBR slots.
