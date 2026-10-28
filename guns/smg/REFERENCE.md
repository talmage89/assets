# Form plan

Original fictional maker/model: Propane Defense **Relay 9**. A fixed-stock,
roller-delayed-class 9 mm visual game asset, not a product replica or working
firearm design. Frame: family grip origin, +Y forward, +Z up, +X right, meters.

Published exterior anchors: overall 680 mm; barrel 225 mm; sight radius about
340 mm; loaded-envelope height about 260 mm; maximum width about 50 mm.
Unloaded mass is the 2.54 kg lightweight class target, not simulated mesh mass.
The 2008 manufacturer catalog's 2.71 kg is a configuration discrepancy retained
in the source register. Thicknesses, pivots, hidden cavities and animation paths
are authored visual estimates; they are not manufacturing specifications.

Build the stamped receiver as a changing hollow section with integral rib crests,
folds, port returns, seams and local weld marks. Upper tube, front hood and rear
drum get first-person silhouette geometry. The polymer lower/grip, fixed stock
and slim handguard must have dense compound sculpt sources with a reduced game
mesh; show their changing triangle-plane sections. Contacts and visual state
checks are independent of GLB serialization and unwanted-penetration sweeps.

The original checkpoint used constant inspection materials only. Form and rig
were subsequently accepted after round 2. Final look-dev uses original marking
relief, causal issued wear and one 2048 atlas, as documented in README.md and
the later REVIEW.md entries. The historical checkpoint images make no claim
of finished photographic realism.


## Round 2 exterior observations

- **Grip axis:** in `left.jpg`, approximate web/heel center observations are
  (565,250) and (500,382) px. The receiver-axis proxy parallel to the hidden bore
  runs from (427,82) to (857,86) px. Their angle is 64.3°, with roughly ±3°
  uncertainty from the selected surface landmarks and perspective. The game
  angle is measured separately from actual section extents at Z=25 and −52 mm
  in `build/sections.json`, not repeated from these authored observations.
- **Guard:** its lower band is approximately 9–13 pixels thick in the same side
  photograph. The 430-pixel / 230-mm receiver baseline gives a local estimate
  of 4.8–7.0 mm; perspective and edge highlights limit precision. The oblique
  `right.jpg` view shows a broad transverse face, approximately 14–18 mm wide
  relative to the nearby magazine. This second width is an estimate, not a
  uniquely recoverable dimension. The new molded section is about 16 × 6.5 mm,
  measured on the actual guard cuts rather than treated as a circular rod.
- **Rear sight / eye:** `shooter-sd.jpg` shows a fixed-stock cheek weld close
  behind the drum; the pupil is partly obscured by glasses and the view is
  oblique, so it cannot establish an exact millimeter distance. Adopted a
  40–60-mm exterior placement range; the revised Eye is measured about 49 mm
  behind the actual near drum face. The separate `eye-reference.jpg` establishes
  the concentric rings and soft near aperture edge, not a simulated camera FOV.
  The aimed presentation uses an 85-mm lens with a 36-mm horizontal sensor
  (about 24° field), 1-mm entrance pupil and focus on the front post. The socket
  itself has no presentation-only offset. The existing stock shape is retained.
- **Drum axis:** 16° rearward from vertical follows the side photographs. The
  original closed skirt has three small circumferential aperture sizes and a
  larger concealed forward optical exit. Its selected 3.8-mm setting replaces
  the previous enlarged 6.6-mm hole. This is our visual design, not a measured
  reproduction of a manufacturer's aperture schedule.
- **Pressed receiver:** use 1.25-mm visual sheet gauge with a following inside
  profile, tight bends, broad flat lands and roughly 3.5-mm rib relief. Oblique
  photographs and the resulting hard shadow lines guide the relief; no exact
  rib-depth specification is claimed from a flat photograph.

The new sharp trigger pair uses four observed blade landmarks for camera
framing. It supports direction/curvature/edge comparison, not independent
validation of the gun's overall scale. All references remain comparison-only;
no image is projected or traced into mesh or texture data.
