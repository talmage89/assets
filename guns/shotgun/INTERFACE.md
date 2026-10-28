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

Feeding is a visual representation: chamber/carrier ownership changes discretely;
the opaque tube hides slot reindexing. There is no growing ammunition. Tube counts
and follower positions are explicit. The separate fired hull spawns at Ejection;
it is not the live shell. Animation is not an internal ballistics or mechanical
simulation. Fresh-import checks establish intended holds, counts, socket frames,
support contacts and sampled surface clearance separately.
