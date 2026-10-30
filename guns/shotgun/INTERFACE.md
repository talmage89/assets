# Guns Interface 1.1.0 — additive tube-magazine binding

This supplement preserves every meaning in [1.0.0](../INTERFACE.md). Its added
capabilities are `pump_action`, `tube_magazine`, `shell_by_shell_loading` and
`tube_capacity`. Detachable magazines and last-round hold-open are false here.
`src/interface.py` owns this member's exact states, events and 60-Hz timings.

All seven existing sockets remain. `Socket_Foregrip` stays a scene-root rest
reference. The **new `Socket_SupportHand` rides Forend** with its complete frame,
so hand IK follows the pump through its full stroke. `Socket_Shell` rides the
insertion shell's always-visible guide frame. Its display bone alone changes
visibility, so the socket remains nonsingular. `Socket_Magazine` remains at the fixed tube
mouth; a tube-fed gun does not offer a dropped magazine. +Y faces the muzzle,
+Z faces up; the origin is the wrist's palm center. Root stays identity. Whole
instance recoil, stance and inspect presentation belong to the consumer.

The ordinary Fire is 1.10 s, including the hand-driven pump: ready (four in tube)
to ready3. Fire3/2/1 continue the count down. FireLast cycles and closes empty;
this gun has no automatic hold-open. IdleTube0–3 provide matching exact holds.
`last_ready` is chambered with an empty tube, as defined in 1.0.0.

Reload is one 1.20 s insertion from three to four. Reload1/2/3 insert into counts
zero/one/two. ReloadEmpty takes 6.30 s: load the carrier, close, then insert four
shells. Each insertion has an approach, tube entry, discrete shell-commit event
and hand-clear interval. These intervals are listed as `interruptible` phases.
During approach/insertion, pause and resume **the same clip and frame**. At a
hand-clear interval the token also supplies the matching Idle clip and count.
Never jump to the four-shell Idle in the middle of an insertion. An early exit
from ReloadEmpty can retain its chambered shell and any committed tube count.

### Visible feeding, additive correction

All existing events, states, clip names/durations and socket bind frames remain.
`visible_cartridge_feed` advertises the revised demonstration. Four added
bones are CarrierGuide, FiredGuide, FiredHull and
TubeFeedGuide. CarrierShell now rides CarrierGuide, and the tube displays ride
TubeFeedGuide. Existing bone names remain. There is no unload clip in this
member; Fire cycles a fired hull, not a live-round unload.

In Fire/Fire1–3 the same shell begins retained at the left latch, leaves the
tube f26–30 and settles on the depressed carrier. The right latch intercepts
the following shell 3.4 mm ahead of the left latch. The forward stroke raises
the carrier to 16° by f40; the bolt picks up the rim and seats the shell by the
unchanged chamber event f44. The carrier drops from the bolt's path. The right
latch releases its following shell to the left latch f42–43. FireLast has the
same empty carrier stroke without creating a shell. The terminal rear stroke
now reaches its stop by f24 and holds through the open event f26. The forward
stroke starts with the carrier lift; its small initial pickup travel precedes
the brisk f40–44 closing stroke. These phases refine interpolation while
retaining the event meanings.

ReloadEmpty brings its first shell through the open port using CarrierGuide
f20–36, lifts it f36–44, and feeds it f46–50. It then performs the original four
tube insertions. Ordinary reloads show the inserted shell pushing the existing
stack, without blanking the tube. TubeFeedGuide provides continuous travel;
STEP child offsets reassign display slots at coincident positions. The pitch
is the actual loaded shell length, 57.5 mm, replacing 59 mm and its 1.5 mm gaps.
The low tray now shares the tube's axis instead of sitting 3 mm above it.
Counts change only at the original commit events. STEP scale marks coincident
ownership changes, initial/final occupancy and the live/fired change at shot f2.
The incoming-hand display starts at each unchanged insertion_begin f12;
without the consumer’s hand mesh this appears as a shell below the receiver.
Socket_Shell supplies that insertion frame. CarrierGuide supplies the first
port-loaded shell’s frame in ReloadEmpty.

The fired hull is a distinct, open 69.8 mm representation. The right extractor
draws its rim with the bolt; the left receiver ejector turns its nose out first.
A small rim roll clears the existing rounded port. At unchanged eject f24 the
whole hull is outside the receiver. The new capability
`case_handoff_bone=FiredGuide` identifies the physics continuation frame:

```text
case_world = gun_world * armature_world * pose(FiredGuide)
             * inverse(bind(FiredGuide)) * translate(0, .2411, .049)
```

This is the full Blender asset-frame matrix; convert it once to the consumer's
glTF basis. Spawn head-centered `hull.glb` there and hide FiredHull from f24.
The demonstration alone continues to f32. Socket_Ejection retains its original
effect/reference frame; it is not the moving hull's spawn frame. Measured pose
and asset-frame linear/angular velocity are in `build/feed-audit.json`.

These are authored visual paths rather than spring/friction or internal
ballistics simulation. Independent source and fresh-import surface checks
establish support, bolt contact and clearance; affine comparisons separately
establish serialization fidelity.
