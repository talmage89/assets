# Guns interface — bolt/optic supplement 1.2.0

Additive to [the accepted 1.0.0 contract](../INTERFACE.md). The C9 binding and its
meanings remain unchanged. Version 1.2 reserves a separate minor binding from
the pump shotgun's parallel 1.1 supplement. `src/interface.py` retains
`VERSION=1.0.0` for base checks and declares `SUPPLEMENT_VERSION=1.2.0`.

Capabilities: bolt action, five-round detachable magazine, **no last-round
hold-open**, folding/extending bipod, magnified optic. Keep Root identity and
apply stance/recoil to the complete loaded instance. Blender +Y forward, +Z up,
+X right; glTF −Z forward, +Y up. Every public socket retains its base meaning.

| Clip | Seconds | Start → end | Events at 60 Hz frames |
| --- | ---: | --- | --- |
| Idle | 1/60 | ready → ready | — |
| IdleEmpty | 1 | empty_closed → empty_closed | — |
| Fire | 2.2 | ready → ready | shot 3, unlock 42, eject 64, chamber 104, lock 122, reset 132 |
| FireLast | 2.2 | last_ready → empty_closed | shot 3, unlock 42, eject 64, lock 122, reset 132 |
| Reload | 3 | ready → ready | magazine out 48, offscreen replacement 78, magazine in 142 |
| ReloadEmpty | 4.2 | empty_closed → ready | unlock 25, open 48, magazine out 86, replacement 116, magazine in 180, chamber 219, lock 242 |
| Inspect | 3 | ready → ready | safe 25, optic adjustments 80, reset 170 |
| BipodDeploy | 1.3 | ready/folded → ready/deployed | unfolded 42, extended 72 |
| BipodFold | 1.3 | ready/deployed → ready/folded | retracted 32, folded 72 |

`FireLast` deliberately cycles and closes on an empty chamber: there is no
automatic hold-open and no chamber event. `ReloadEmpty` is supplied despite the
base contract only requiring it for hold-open guns. It starts closed/empty,
opens manually, exchanges the magazine, then closes and locks. Chambered Reload
holds the bolt locked and retains the chamber occupancy throughout. Feeding is
a STEP visibility representation; no cartridge-path physics is claimed.

All movement has explicit hold boundaries. Save `{version, clip, frame, state}`
to pause and resume at exactly that clip/time. Drop the empty magazine at the
magazine-out event, before offscreen replacement. Both standalone variants share
the complete `Socket_Magazine` spawn frame. Bipod state is orthogonal to ammo:
the supplied clips start from the illustrated canonical bipod pose; a consumer
that preserves deployed legs through firing/reload should mask these clips to
the action/ammunition bones and retain its bipod layer.

Optional optic capability:

- `Socket_Eye` lies on axis 88.9 mm behind the ocular's rear rim. Its orientation
  is the actual aimed camera. The comb is below the optical ray, with a cheek
  height chosen from the class's illustrated cheek weld.
- `Socket_OpticObjective` is a new scene-root node on the same axis at the
  objective front. A game can render a secondary camera there at its chosen
  4–16× FOV and composite into the lens aperture. The mesh itself does not
  magnify the world or implement a physical optical solver.
- `Reticle` owns the original centered split-post pattern. Hide that bone's
  geometry when drawing an engine/UI reticle. No real product reticle is copied.
- `PowerRing`, `Diopter`, `Elevation`, `Windage`, `Parallax` are optional visual
  controls. They do not change gameplay zero or optical power automatically.

Final delivery uses the established kit atlas exporter, one 2048 texture set
and a second glass material. Standalone magazines now carry their own 1024 sets;
the fired case carries 512, all extracted from the gun's baked atlas at its
original density. See [delivery sampling details](../DETACHABLES.md).
The direct mesh remains unmagnified;
the objective-camera capability above is optional consumer integration.

The Blender demonstration is rebuilt as `renders/final/beauty/aimed.png` by
[src/scope_integration.py](src/scope_integration.py), after importing the final
GLB. A secondary camera uses the complete `Socket_OpticObjective` frame, at
**8×**, viewing a procedural daylight range and **1.8 m silhouette 100 m** from
the objective. Its scene-linear render target is
`renders/final/beauty/aimed-range.exr`; a display preview is `aimed-range.png`.
The aimed camera is the exact `Socket_Eye` frame with a 70° horizontal field.

Engine assignment: mesh **`VesperB24`**, zero-based **material slot 1**,
**`VesperB24 Glass`** (the glass glTF primitive). Both lenses share that slot.
Select only the ocular with optical-axis distance from `Socket_Eye` **<0.15 m**;
leave the objective's glass response in the other branch. In the socket frame,
ocular image UV is `(0.5 + x/0.0376, 0.5 + z/0.0376)`. Here x/z are
Blender right/up components; glTF consumers use the equivalent right/up basis
(X/Y in the family frame, with −Z forward). The existing circular
lens geometry crops the target; no additional exported mesh or material slot
is required. The ocular center is 91.9 mm from Eye; the rear-rim eye relief is
88.9 mm. Preserve that viewpoint to avoid changing the aperture's apparent size.

The integration composites a **procedural reticle texture in the lens shader**,
over the render target. It reproduces our original centered split-post pattern.
The GLB also retains its original internal `Reticle` geometry; the opaque target
occludes it here. Engines using this composite should hide the Reticle bone's
geometry as already specified above. No reticle bitmap or extra canonical atlas
is shipped. The generated render target is a runtime demonstration, not static
world imagery baked into the asset.

Magnification uses the actual aperture at Eye: radius **18.8 mm**, axial
distance **91.9 mm**, angular diameter **23.1230°**. For power M, use
`horizontal FOV = 2 atan(0.0188 / (0.0919 * M))`, square render target.
The player's 70° FOV controls framing; it does not determine the optic power.
This gives the stated angular magnification through the physical eyepiece.

| Power | Horizontal / vertical FOV |
| --- | ---: |
| 4× | 5.8554° |
| 5× | 4.6858° |
| 6× | 3.9055° |
| 7× | 3.3479° |
| 8× | 2.9296° |
| 9× | 2.6042° |
| 10× | 2.3439° |
| 11× | 2.1308° |
| 12× | 1.9533° |
| 13× | 1.8031° |
| 14× | 1.6743° |
| 15× | 1.5627° |
| 16× | 1.4650° |

These fields implement the original asset's aperture and eye-relief convention;
they are not a real product's optical specification. PowerRing animation
remains visual; the consumer updates the secondary camera field. `scope-integration.json` records the actual socket
positions, power, field, range dimensions and receiving slot for each render.
