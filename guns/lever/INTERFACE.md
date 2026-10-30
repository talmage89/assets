# Guns interface 1.5.0 — lever action and top ejection

Additive to [1.0.0](../INTERFACE.md), reusing the
[1.1.0 tube-loading meanings](../shotgun/INTERFACE.md). The bolt rifle's 1.2.0,
the SMG's 1.3.0 and the revolver's 1.4.0 supplements are unchanged. The executable
binding is [src/interface.py](src/interface.py): base version 1.0.0, supplement
1.5.0, 60 Hz. This is a visual game-asset interface, not a working mechanism.

Capabilities: manual lever action, six-round tube, individual loading through a
right-side spring gate, exposed hammer with a half-cock display, and top ejection.
There is no detachable magazine or automatic last-round hold-open. Consumers
read the capability/event manifest instead of inferring semantics from bone names.

Meters; grip origin; Blender +Y forward / +Z up / +X right; glTF −Z forward /
+Y up. Root remains identity. Whole-instance recoil/stance belongs to the consumer.
All seven base sockets retain their meanings. Magazine is a fixed tube-mouth
frame; it is not a dropped-magazine spawn. Foregrip remains a scene-root reference.
SupportHand retains 1.1.0's complete hand frame, riding the stationary Root here.
Shell retains the insertion guide meaning; it rides the nonscaling InsertGuide,
while InsertRound alone controls display visibility. It stays nonsingular.

The additive `Socket_LeverHand` rides LeverHand, a child of Lever, and provides
the operating-hand frame through the entire compound motion. The lever pivots
on the dropping Link, rather than rotating about a pin floating in the receiver.
Consumers supply their own hand mesh/IK. Checkpoint clearance uses explicit palm
and finger envelopes; it does not deliver an anatomical hand animation.

| Clip or family | Duration | Start → end and events |
| --- | ---: | --- |
| Idle | 1/60 s | Six in tube, one chambered, hammer cocked |
| Fire / Fire1–5 | .30 s | Shot at f3; live chamber becomes a fired case; hammer stays down; tube count unchanged |
| FireLast | .30 s | Last chambered round fires; empty tube, fired case still in chamber |
| Cycle / Cycle1–5 | 1.00 s | Unlock f6, open f22, eject f24, release f28, carrier up f36, chamber f50, lock f58; tube count falls by one |
| CycleLast | 1.00 s | Ejects the last case and closes empty, without hold-open |
| CycleEmpty | 1.00 s | Empty manual cycle; no eject/chamber event |
| Chamber | 1.00 s | One in tube / empty chamber → chambered / empty tube; no eject event |
| Reload / Reload1–5 | 1.20 s | One insertion, counts 5→6 / 0→1 through 4→5; commit f58, hand-clear f66–72 |
| ReloadSeveral | 3.60 s | Three insertions, counts 3→6; commits f58/130/202; hand-clear f66–72/138–144/210–216 |
| ReloadEmpty | 9.40 s | Insert one into empty tube, cycle it into chamber, then six insertions; chamber f122, final commit f550 |
| HammerSafe / HammerCock | .80 / .50 s | Canonical full-load cocked ↔ half-cock presentation |
| Inspect | 2.00 s | Canonical full-load inspection, returns to same state |
| IdleTube0–5 | 1.00 s | Count-specific chambered holds |
| IdleEmpty / IdleOpen / IdleUnchambered1 | 1.00 s | Explicit empty closed/open and loaded-tube/empty-chamber holds |

Initialize the display with the appropriate Idle hold before first drawing the
gun. The inspection GLB bind pose is a modeling rest pose, not an ammunition
state. Fire and Cycle are deliberately separate. For example:
`ready → Fire → spent6 → Cycle → ready5 → Fire5 → spent5`.
FireLast goes from `last_ready` to `spent0`, then CycleLast reaches
`empty_closed`. The base `last_ready` meaning remains one chambered live round
and an empty magazine. A fired case is an additional explicit state, not a live
cartridge. All exact schedules and count/state names live in the manifest.

Reuse 1.1.0 interruption rules: store `{version, clip, frame, state}` and resume
the same clip/frame during an insertion. At declared hand-clear windows, an
exit token names the matching count-specific Idle. ReloadEmpty can first exit
to IdleUnchambered1, followed by Chamber; after chambering it can exit to
IdleTube0 and continue with individual insertions. Never jump to full-load Idle
before the corresponding commits. HammerSafe/Cock and Inspect demonstrate the
canonical full-load state; consumers retaining other counts mask their ammunition
channels and keep their own count layer.

### Visible feeding, additive correction

All event frames, state meanings, clip names/durations and socket bind frames
remain. `visible_cartridge_feed` and `feed_type=tube_carrier` identify the
continuous demonstration. No unload clip existed in this member; none is implied
by Cycle, whose start state contains a fired case.

The first cartridge uses CarrierRound from the retained tube position, through
the stop (release motion f14–28), onto the horizontal tray, and through its
16° lift f28–36. TubeStop retracts only for that first rim; TubeCutoff catches
the following rim before the stop returns. The bolt picks up the inclined rear
rim after f37 and pushes it against the chamber lead-in through f49. The tray
drops as the bolt takes control. CarrierRound changes ownership to ChamberRound
at f50 at the same position and orientation. ReloadEmpty uses the same sequence
offset by 72 frames. Tube insertion moves the whole existing stack continuously.
TubeFeedGuide carries travel; STEP child offsets rename occupied slots at a
commit without a blank frame or physical position jump. STEP scale is used only
for coincident ownership changes and initial/final occupancy.

`open` f22 still means the bolt is fully rearward. The lever's remaining carrier
cam travel finishes at f36 (80°); its return now accompanies the bolt's f37–49
stroke, then seats by f58. This is an additive refinement of the old pose
interpolation, which held the lever open while the bolt moved home. Loading
clearance uses 16° rather than the former 20°. The static IdleOpen reference
retains its legacy 20° presentation; feed/cycle motion uses 16°. TubeStop, TubeCutoff and
TubeFeedGuide are three added bones; all previous names remain. FiredGuide now
rides Root, with explicit extraction motion, rather than inheriting Bolt.

The upper claw retains the fired rim during withdrawal. The lower ejector
tips the case nose upward f19–22, before free flight. At unchanged eject f24,
the whole case is outside the top opening. Use the added capability
`case_handoff_bone=FiredGuide`, not the legacy effect socket, for physics:

```text
case_world = gun_world * armature_world * pose(FiredGuide)
             * inverse(bind(FiredGuide)) * translate(0, .200, .048)
```

Those coordinates and the formula are Blender asset coordinates. Convert the
whole matrix once to the consumer's glTF basis; do not add a second axis flip.
The head-centered standalone `case.glb` uses that complete frame. Spawn it and
hide FiredCase from f24 onward. The review-only display continues to f30.
`Socket_Ejection` retains its legacy effect/reference frame and original bind
orientation; its former case-head promise is superseded by this explicit
additive handoff. `build/feed-audit.json` records the measured pose, linear and
angular velocities in the asset frame. The live cartridge has the same
head-centered +Y-to-mouth convention. This is authored visual motion, not a
spring, friction or cartridge-path physics solver.

Eye is the exact aimed camera, on the line through the buckhorn notch and front
bead. The checkpoint uses 70° horizontal FOV, zero shift and a gray surround;
no gun part is hidden. Rear-sight/bead alignment and eye/comb height are measured
from actual surfaces separately from serialization checks.

Form round two retains every bone frame, clip key, event and socket orientation.
`Socket_Butt` alone follows the revised curved steel shoulder surface:
Blender **(0, −249.2064, −50) mm**, 4.2936 mm forward of its previous seat.
Its meaning remains the shoulder-contact reference. The operating-hand frame
and exact Eye frame are unchanged. The lever stays in the gun's mid-plane;
half-frame source/import sweeps also assert its transformed X normal and center.

The checkpoint GLB preserves named rigid parts for independent imported-surface
audits. Final delivery, after form acceptance, uses the kit's atlas finalizer,
baker and animated skin exporter, one 2048 BaseColor / OpenGL Normal / ORM set,
with the gun retaining that atlas. Standalone cartridge and case now carry their
own 1024 subsets at the original density; see [delivery sampling details](../DETACHABLES.md).
No final atlas or consolidated draw-call claim is made before that stage.
