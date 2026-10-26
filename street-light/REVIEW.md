# Street-light review

Pass 1: opened all four source renders (overall, optics, base and lit optics),
and compared the casting/optics with the publisher's photograph and dimension
sheet. The assembly reads as a tapered cobra-head pole, but overall framing was
too loose, the upward camera saw the studio wall edge, and the zinc looked like
large round spots. Changed zinc to low-contrast angular spangles at millimeter
scale, raised the procedural wall and tightened the overall view. The control
was only a short cap; changed it to the height of a real twist-lock housing.

Physical review found a 1 mm tray gap and a nominal pipe passing into a solid
receiver. Seated the tray, cut the actual receiver bore, made the last arm segment
straight and added a clamp jaw. Glass/reflector inspection also prompted a real
compression gasket, retaining rails and ceramic LED boards, with declared
surface-contact checks. The source shaft retains 11-gauge walls and its handhole;
the game shaft is sealed behind the closed covers to avoid invisible interior
faces. No operating motion is needed for the assembled light.

Pass 2 and source refinement: opened the revised overall, optics, base, lit
optics and calibrated pair. Zinc no longer reads as large dots; the backdrop
is continuous and the control has plausible scale. Added shallow tray ribs and
anchor threads in normals, softened the driver/nose casting transition and
reduced fin height after comparison with the photograph. A neutral alpha
background keeps the camera-facing world from making the pair artificially
black. The five sparse visible-edge anchors fit at 18.9 px RMS in a 987 px
photograph; the estimated 28 mm lens is uncertain, not EXIF. Independent Blender
projection agrees within 0.002 px. Our original reflector and bolted cover
layout intentionally differ from the reference.

Packing initially covered only 25.7%. Reduced the long shaft's relative UV
priority; fixed the kit's Blender-5.2 vector arithmetic in density clamping.
Finalized coverage is 37.93%, zero overlaps, median 600 px/m. The 3064 triangles
include real transparent optics and necessary support geometry. The source lit
view was too subdued under studio lights; increased the authored glow multiplier
to 16 for the shipped material, with daytime/photo emission explicitly off.

First GLB inspection: the lit tiles, glass and shared atlas exported correctly,
but the base close-up exposed black projection patches at the handhole. The
cover had been capped with a nonplanar ngon, giving inconsistent triangulation
across a curved surface. Rebuilt it as an actual curved sheet grid, and isolated
its bake group from the shaft while retaining rest-position contact AO shadows.
The grid adds 116 silhouette/support triangles.

The exporter also emitted ten identical texture views referencing three images.
Added optional compaction for material-override exports, preserving BIN/image
bytes and remapping all material texture indices. A temporary delivery retained
byte-identical BIN data and passed reimport/material checks after 10→3 compaction.
Final corrected GLB review follows the new bake.

Corrected-grid delivery: the handhole is now clean in the exported base close-up.
The first complete turnaround exposed missed projection strips on the top of
the arm. Its eight game bend intervals approximate a smooth parabolic source;
the source rises roughly 2.3 mm above the longest chord before radial faceting,
exceeding the 1.5 mm cage. Restored the kit's 6 mm cage / 18 mm ray reach.
The handhole remains isolated so that widening the cage cannot reintroduce
neighbor projection there. Rebuild and exported top-view review follow.

Widening the cage removed the arm misses but projected nearby optics onto the
glass. Rejected that delivery. The source and game arm now share eight bend
intervals plus the straight-end knot; the source adds radial subdivisions but
keeps its centerline chords aligned. Restored the tight 1.5 mm cage / 6 mm rays.
This retains 3180 triangles and smooth interpolated pipe normals while keeping
the close-packed optics free of cross-projection. The exported photo filter
also now includes the joined StreetLightMesh; source-only part prefixes had
hidden the entire joined mesh in the first comparison.

Final Cycles review (aligned source, review7): opened the hero, front, side,
back, top, optics, base, scale and lit views from the new exported GLB. The
arm's top is continuous zinc, the handhole has no black projection patches,
and the reflector/glass edges are clean again. The visible bend faceting is
proportionate to a fixture nearly eight meters above the ground. Tiny anchor
threads and fasteners are softer than the source at 1024; the shaft's low texel
density and sparse camera calibration remain the main compromises.

Delivery complete: `make -C street-light all match-final PASS=review7` passed,
including audits, repository policy, UV/density, normals, independent GLB
reimport, camera calibration, physical supports and actual optical-material
checks. Opened the final Eevee, contact sheet, documentation composites and
exported photograph pair as well. The pair now shows the joined fixture; its
support arm continues out of frame. The original casting has a more angular
driver hump and simpler reflector layout than the reference, while retaining
the measured envelope and plausible construction.

All 11 final-shot metadata records (nine Cycles, one Eevee, one photo match)
match GLB SHA256 `521d3a1663aa1204e002bcc711ef98f2c52a9711221143b4c25b74370e13a0b5`.
Delivery is 3180 triangles, three materials, three shared 1024-square images,
1472732 GLB bytes. UV coverage 37.9366%, zero overlaps, density p5/median/p95
128/600/775 px/m. All 19 physical support pairs pass on actual
game surfaces; maximum sampled vertex-to-triangle gap is
4.76837158e-07 m (an upper bound, not an exact distance).
Serialization checks prove delivery fidelity separately. No in-use motion.
The three final JPGs are at most 1600 px wide and 67657 bytes.
