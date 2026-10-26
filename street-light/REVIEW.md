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

Final GLB review follows bake, export and reimport.
