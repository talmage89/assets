# Guns interface — belt-feed supplement 1.8.0

Additive to [1.0.0](../INTERFACE.md); changes no existing socket or state
meaning. Reuses [1.2 bipod layering](../bolt/INTERFACE.md),
[1.3 nonreciprocating handle](../smg/INTERFACE.md) and
[1.6 complete detachable spawn frames](../ak/INTERFACE.md).
Version 1.7 belongs to the parallel side-by-side asset.

This is a visual game binding. External animation timings and inert display
meshes do not simulate or validate an operative firearm.

Meters, palm origin, Blender +Y forward/+Z up/+X right, glTF −Z forward/+Y
up. Root stays identity. Apply stance, recoil and inspection movement to the
whole imported instance. Six existing fixed references remain scene roots.
Socket_Magazine rides Magazine and Socket_ChargingHandle rides the handle's
complete frame. The legacy magazine socket is the box's spawn here; it never
spawns a magazine for the inactive covered side well.

Capabilities: belt_feed, detachable_box, open_bolt, full_automatic, bipod;
semi_automatic=false, select_fire=false, last_round_hold_open=false,
charging_handle_reciprocates=false. The box's gameplay capacity is 200.

The new `belt_ready` state has the action displayed at the rear and chamber
occupancy **zero**. `belt_last_ready` has one display round remaining on the tray,
not a chambered round. These are new state names. The existing `ready` and `last_ready` meanings
remain unchanged in the base binding; this asset does not reuse them for
an empty open chamber. `belt_auto_held`, `belt_safe_ready` and
`belt_tail_ready` describe the other open-bolt feed displays. `empty_closed` means forward/empty.
`FireLast` ends there; no automatic empty hold-open. `CeaseFire` ends rearward
with trigger reset. A game owns ammunition bookkeeping and shot effects.

Nineteen clips, 60 Hz. Exact durations/events are executable in
[src/interface.py](src/interface.py) and generated `build/interface.json`.
Idle, IdleEmpty, IdleSafe, Fire, Burst, CeaseFire, FireLast, Reload,
ReloadEmpty, Charge, BipodDeploy, BipodFold, SafetyOn, SafetyOff,
CarryRaise, CarryFold, BoxOpen, Inspect and BeltEnd. Fire is an authored
one-shot automatic presentation, not a semiautomatic capability. Burst shows
three cycles. Reload retains remaining rounds; ReloadEmpty starts forward,
exchanges the box and then draws/returns the independent handle. Feed-cover
and box states commit at the manifest events, not guessed clip fractions.

Bipod state is orthogonal to ammunition. Mask action clips to action/feed
owners to retain deployed legs, as 1.2 describes. Carry handle and shoulder
rest are optional presentation owners. The supplied BoxOpen clip withdraws
the box before opening its lid.

## Driving the cosmetic belt

Persist `{version, clip, frame, remaining, phase}`. Pause/resume at precisely
the saved time. Never jump to Idle while the cover is open or box is absent.
`remaining` is the count on the incoming display train. `phase` is continuous
advance in display spacings. `src/belt.py` provides a pure-Python solver and
count masking; apply its poses to BeltRoot, BeltLink00…18 and BeltRound00…18.
Every round is a child of its link owner. The underlying round and link mesh
data are reused. Seventeen round meshes and sixteen link meshes are retained;
the last two round owners and last three link owners have no geometry. The
64-bone rig and 19-clip contract stay intact. All cartridge axes remain parallel to +Y. Equal chord
lengths keep the rig's center spacing constant at solved frames; interpolation
error is measured separately. The curve is an authored hanging guide, not a
physical chain solver or a measured link engineering specification.

At each consumed round, advance phase continuously and decrement remaining
at the shot event. Do not wrap phase to zero while the belt is visible. When
remaining drops below the visible count, the far tail owners use STEP zero
scale, revealing a real end. `BeltEnd` illustrates the last three slots.
For an indefinitely long gameplay belt, consumers may recycle an owner only
when occluded inside the box or after it has left the tray; preserve its full
pose before reuse. The supplied `game_pose(completed_shots, advance, remaining)` helper cycles
owner identity at the ends: commit completed_shots after advance reaches 1,
then reset advance to 0. Visible identical slots retain their positions. The
consumer must occlude the box-end recycling region. The authored clips remain
a finite demonstration; this helper is not a runtime-engine integration test. Source/import spacing evidence records
its practical limits.

A cartridge/chamber display handoff and ejection event are visual effects.
Two inert rectangular ready witnesses now prove the rearward animation seat
on evaluated surfaces at every ready clip endpoint. They are not a working
sear; no bolt lugs, firing pin or operative feed cam is provided. Cover/box seating and visible
motion are checked separately from export serialization.

## Baked delivery

The main GLB now carries one canonical 2048 BaseColor / OpenGL +Y Normal /
ORM set, baked at 4096. Its opaque BaseColor alpha retains the per-surface
specular factor through KHR_materials_specular. Keep that extension and each
imported material/sampler. The accepted 64 bones, twelve sockets, nineteen
clips and complete box spawn frame remain.

Loaded/empty boxes embed lossless 1024 subsets; cartridge, fired case and
link use 512. The kit's texture-size path moves original atlas neighborhoods
without reducing density or resampling. All retain the main gun's trilinear
mipmapped sampler. See the local README and family DETACHABLES contract.
The finished README shows exported-GLB docs JPGs and the real-speed Reload GIF;
the generated comparison and validation evidence remains local and ignored.
