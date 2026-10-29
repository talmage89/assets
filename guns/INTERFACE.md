# Guns interface 1.0.0

A visual game-asset interface. Consumers read capabilities and events; they do
not infer semantics from rifle bone names, animation lengths or material names.
Each family member supplies its own event/state manifest; this table is the C9
binding, not a universal timing table. The current implementation is
`pistol/src/interface.py`; times below are 60-Hz frames
from zero, divided by 60 for seconds. Clip endpoints are inclusive.

| Clip | Required | Duration | Start → end | Events (frame) |
| --- | --- | --- | --- | --- |
| Idle | yes | 1/60 s | ready → ready | — |
| Fire | yes | .20 s | ready → ready | shot 2, eject 4, chamber 8, reset 12 |
| FireLast | yes | .25 s | last_ready → empty_open | shot 2, eject 4, lock 7, reset 12 |
| Reload | yes for detachable magazines | 2.00 s | ready → ready | magazine out 28, magazine in 91 |
| ReloadEmpty | yes for hold-open magazines | 2.40 s | empty_open → ready | magazine out 28, magazine in 91, slide release 112, chamber 118 |
| FireSemi | optional alias of Fire | .20 s | ready → ready | identical to Fire |
| Inspect | optional press check | 1.50 s | ready → ready | open 30, closed 65 |
| Charge | optional empty-magazine rack | .60 s | empty_closed → empty_open | lock 30 |
| IdleOpen | optional state hold | 1.00 s | empty_open → empty_open | — |
| IdleEmpty | optional state hold | 1.00 s | empty_closed → empty_closed | — |

`ready` = closed, chamber occupied, loaded magazine; `last_ready` = closed,
chamber occupied, empty magazine. `empty_open` and `empty_closed` have an empty
chamber and empty magazine. The C9 capabilities are semiautomatic, detachable
magazine, last-round hold-open. `Charge` deliberately racks an **empty** gun and
finishes locked open. A loaded charging animation is not supplied.

Shot/eject/chamber are effect and occupancy events. Cartridge visibility changes
use STEP sampling; all movement uses explicit hold boundaries. Feeding is a
visibility representation, not a cartridge-path simulation. At frame 47 of an
empty reload, the replacement magazine becomes loaded offscreen. Drop the empty
standalone at magazine-out, before this substitution. Do not replace the dropped
magazine with the loaded variant. Loaded/empty exports use the same local origin
and canonical atlas coordinates.

Transitions commit at clip completion: normal Fire → Idle/Fire/Reload; last-round
FireLast → ReloadEmpty → Idle; IdleEmpty → Charge → IdleOpen. Supply `last_ready`
when ammunition bookkeeping reaches one chambered round. This occupancy change
is a discrete consumer state, not a hidden animation reset. An interrupted reload
retains `{version, clip, frame, state}` and resumes that same clip/time. Hold the
pose while paused. Do not enter Idle or restart Reload while the magazine is
absent. Future shell-by-shell guns must declare their own interruptible insertion
phases and events; they may add clips without changing these meanings. Breaking
state/socket changes require a major interface version.

Meters; grip origin; Blender +Y forward, +Z up, +X right. glTF +Y up, −Z forward.
The seven public nodes are `Socket_Muzzle`, `Socket_Foregrip`, `Socket_Butt`,
`Socket_Eye`, `Socket_Ejection`, `Socket_MagWell`, `Socket_Magazine`. `Butt` is a
pistol grip-seat reference. `Eye` is the optical sightline, not an elevated product
camera. Every socket's +Y is forward and +Z up in the Blender source frame.

**Whole-weapon motion belongs to the external instance transform.** Internal
`Root` stays identity in every clip. This preserves the rifle's six scene-root
socket paths and bone-riding magazine socket. The rifle's helper also makes these
six scene-root references; its public paths are retained. A game applies stance,
recoil and inspect-hand movement to the common loaded-scene instance, including
all roots. Do not transform only the armature. The six static references describe
the grip/aim/effect frame, not the silent moving slide at every subframe. Muzzle
is valid at shot (slide in battery); ejection is inside the actual moving port at
the eject event. `Socket_Magazine` follows the full magazine bone transform and
is the spawn transform for either detached variant. Position **and orientation**
are round-trip tested. Effect sockets are not used as moving-part constraints.

Every member retains Root and Trigger. Detachable-magazine members also retain
Magazine and MagRelease. Action-specific C9 bones:
Slide, Barrel, SlideStop; additional visual children remain implementation detail.
Optional features are discovered through capabilities, never demanded from a
shotgun/bolt-action gun. Preserve imported PBR materials by index; no `Rifle` or
`RifleLens` name override. The final delivery contract is one 2048 BaseColor /
OpenGL Normal / ORM atlas; separate GLBs repeat identical embedded payloads.
An engine must reuse textures by canonical atlas ID/content hash to share GPU
memory: identical GLBs do not make runtime caching automatic.

## Additive 1.1.0 tube-loading supplement

The [Hearth 12 supplement](shotgun/INTERFACE.md) adds tube-magazine capabilities,
count-specific states, interruptible shell insertion, `Socket_SupportHand` and
`Socket_Shell`. Existing 1.0.0 meanings and the C9 binding above remain valid.
`common/interface_v1_1.py` checks the added schema; each gun supplies its own
event schedule and independent intended-state/contact tests.

## Additive 1.2.0 bolt/optic supplement

The [Vesper B24 supplement](bolt/INTERFACE.md) adds manual bolt cycling,
no-hold-open detachable-magazine states, folding/extending bipod clips and
`Socket_OpticObjective` for optional magnified rendering. Both the 1.0.0 binding
and the 1.1.0 tube-loading supplement retain their existing meanings.

## Additive 1.3.0 manual charging-handle supplement

The [Relay 9 supplement](smg/INTERFACE.md) adds a manually locking,
nonreciprocating charging handle, its full-frame hand socket, select-fire
states and no-hold-open reload schedules. The 1.0.0 binding and the 1.1.0
and 1.2.0 supplements retain their existing meanings.

## Additive 1.4.0 swing-out revolver supplement

The [Meridian Six supplement](revolver/INTERFACE.md) adds a six-chamber
cylinder with per-chamber `loaded`, `fired` and `empty` state, double and
single action, a manual swing-out reload and a speedloader. It has no
magazine; its magazine sockets are declared inactive. The 1.0.0 binding and the
1.1.0 to 1.3.0 supplements retain their existing meanings.

## Additive 1.6.0 rocking-magazine supplement

The [Rill 39 supplement](ak/INTERFACE.md) adds `magazine_rocks_in`, the authored
front-hook/rock/seat path and a reciprocating charging-handle binding. Existing
occupancy, socket, effect and select-fire meanings remain unchanged. Version
1.5.0 is reserved by another family member.
