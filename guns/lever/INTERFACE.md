# Guns interface 1.5.0 — lever action and top ejection

Additive to [1.0.0](../INTERFACE.md), reusing the
[1.1.0 tube-loading meanings](../shotgun/INTERFACE.md). The bolt rifle's 1.2.0,
SMG's reserved 1.3.0 and revolver's reserved 1.4.0 are unchanged. The executable
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

The insertion pushes the existing stack and follower continuously. Opaque tube
slots reindex at commits; their display meshes are hidden for the preceding
single frame. The same mask protects manual feeding at f27–28. Occupancy uses
STEP sampling. This is a declared visual handoff, not cartridge-path physics.
CarrierGuide and FiredGuide retain motion on nonscaling bones; their display
children alone have STEP visibility. This avoids losing rotation during a
zero-scale GLB sample. The carrier round is separately controlled during the bolt push, so it remains
on the chamber line while the tray lowers. The exported clips include the
fired-case demonstration trajectory through the top opening.

At eject f24, `Socket_Ejection` is the case **head** frame, matching the standalone
case's origin and orientation. A physics consumer spawns `case.glb` there and
hides the FiredCase display from that event onward, avoiding two simultaneous
representations. The demo retains the scripted case until f34 for visual review.
The live `cartridge.glb` has the same head-centered +Y-to-mouth convention.

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
and canonical identical maps in the gun, cartridge and case GLBs. No final atlas
or consolidated draw-call claim is made before that stage.
