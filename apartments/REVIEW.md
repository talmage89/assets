# Form and construction review

This gate stops before look-dev. The assets are original type studies; photo
fits compare construction and rhythm, rather than claim a replica or a survey.
No reference pixels enter the meshes, colors, diagnostic image or future maps.

## Photographs, cameras and value controls

The three fitted views use the 2004 used garden-apartment photograph, a c.1978
DAHP mansard/gallery photograph, and a 2006 garage-row photograph. Crops,
authors and rights are in `refs/SOURCES.md`; DAHP's original page/crop register
is generated locally. Source and exported pairs are separate outputs.

Color review starts with assumed-neutral balancing, preserving average linear
exposure. `build/neutral-reference.json` records the exact ROIs and RGB gains:
white replacement sash (.884, 1.134, 1.013), light painted roof edge
(.910, .982, 1.133), and white garage panel (1.047, .968, .989). These are
assumptions about paint, not gray-card measurements. The photos have different
light and white balance; their JPEG values are not recovered albedos. The
shared procedural daylight stage uses AgX Medium High Contrast at −.45 EV.
The camera solver’s generic light/exposure defaults are retained in its data
but are not lighting recovery or applied stage settings.

The final measured-landmark fits give 9.59 / 9.91 / 11.95 px RMS at
25.00 / 44.78 / 54.73 mm, respectively (`build/matched-cameras.json`).
The used-garden fit reaches its lower lens bound; these corner fits do not
establish equivalent plans, fenestration or a recovered photographic camera.
The garage photo has 38 mm-equivalent EXIF; its longer fitted lens is a
consequence of comparing an original plan. Independent Blender projection
checks disagree by at most .00085 px, below the kit's .05 pixel limit.
Residual overlays remain available beside each pair.

## Pass 1 — room modules, scale and blocked openings

Witnesses: `renders/pass1/Building-301/`, `renders/pass1/Building-304/`,
`renders/pass1/Complex-301/` and `renders/pass1/matches/`. Historical pairs were
rendered retrospectively from retained procedural checkpoint scenes; they are
not substituted for current exported evidence.

**Value first:** the first exported brick building was white, despite colored
source vertices. The exporter did not recognize the first color multiply
node. Replaced it with the same supported stock texture/vertex-color node
arrangement used by the houses. White walls/rails from that rejected export
are not a color target. The two-story pair was too cold and its continuous
dark apron obscured upper gallery entrances; do not try to cure this by
brightening the light.

**Form critique:** the central-core mass and nine-foot floor rhythm read as a
small walk-up. Its broad gable is plausible for the deep double-loaded plan,
but every floor looked too diagrammatic. The gallery needed a continuous
protected route, separated end stairs and usable landing openings. Rails
initially continued across those openings. Mansard openings were cut for
windows while some doors remained behind the apron. Those are construction
failures, not material deficiencies.

**Changes:** cut real wall/roof openings, clear gallery guards at stair entries,
provide closed-riser pans/stringers/landings, reserve a side bypass in the
central hall and connect both front/rear unit pairs to it. Use front living
sliders, smaller bedroom/kitchen openings, end windows and shallow tenant
backings. Schematic unit rooms now reserve circulation and wet cores rather
than calling four exterior bays a finished interior plan.

## Pass 2 — roof intersections, approaches and site assembly

Witnesses: `renders/pass2/Complex-301/`, `renders/pass2/Row-403/`,
`renders/pass2/matches/` and `renders/pass3/Row-403/`. The second archival
source comparison was repeated after repairing its relocated relative image
paths; the magenta missing-image output was rejected.

**Value first:** dark steel and roof values now retain cavity shadow; green
foliage initially became a black silhouette because its active chart selected
an empty bark UV layer. Normalize botanical charts before joining, preserve
the original leaf mask, and strip unused wind color from this static context.
Do not raise foliage albedo to disguise an invalid chart. The blue-gray
apartment quick palette also did not support the 1970s gallery reference;
use a restrained landlord green for that profile.

**Form critique:** intersecting front-gable solids left abrupt roof ends. The
row's raised floors lacked foundation fill and its flat drives missed garage
thresholds. An entry camera looked at a truck instead of the door. Rear slabs,
carts and stoops needed ground-level placement despite stepped unit floors.
The reference's mansard end fins flank an open gallery: a continuous low strip
across the door faces is the wrong construction. The courtyard was too much
unbroken grass and wide unaccounted parking depth.

**Changes:** use the houses' analytic roof-plane clipping for the cross gables;
fill exposed foundations; vary stoop riser count with actual floor elevation;
slope garage drives and parked vehicles together; correct entry framing.
Open the gallery canopy between mansard fins. Split shared balcony posts at
each slab, give chairs four feet, and fit the bicycle/grill to their patio
surfaces. Add actual AC sleeves and one pad per split-system unit, with meter
count independent from HVAC type. Condensers sit along end-wall service runs,
outside occupied patios. Pool coping is an open ring, with an actual water
opening. Clip native turf around slabs/walks and add curbed islands and a drive.

**Assembly/optimization critique:** joining independently placed copies that
shared mutable mesh data multiplied context geometry. Consolidate each native
module once before instancing; independently count every raw glTF node's
triangles. Preserve separate moving architectural parts. Apply scaled terrain
placements into copied mesh data and leave exported frames at unit scale.

## Pass 3 — physical checks and current exported judgment

Current witnesses: all 52 images in `renders/checkpoint/`, three pairs in
`renders/matches/`, and three independent source pairs in
`renders/source-matches/`. `renders/review/` gathers the full set, plans and
heroes. Historical source images above do not certify the current export.

**Checks that changed the model:** sampled door surfaces caught threshold
penetration at rest and hinge binding at 100°. Raise the leaf bottom clear of
the threshold and put the offset hinge behind the casing return. Curved-guide
checks caught adjacent rectangular garage sections binding; tapered end noses
now clear while rigid section chords retain their length. The measured minimum
garage ceiling gap is 140.20 mm. Poses are sampled, not a continuous collision
proof. These checks cover leaves/casings and garage sections/guides/ceiling;
they are not a whole-site collision or egress certificate.

Wall-grid coordinates that differed only by floating arithmetic generated
zero-area slivers. Merge grid lines at a micrometer and reject zero spans.
Temporary text and constant-color source context also carried empty charts;
replace those with finite metric charts while retaining actual leaf-mask UVs.
The gate rejects zero-area geometry and UVs. This cleanup does not masquerade
as final atlas packing, density calibration or baked normal detail.

Building roots are centered on their actual wall-footprint bounds. Their
footprint polygons/corners, module walk sockets and townhouse party-wall
centers/endpoints remain explicit. Recentered site placement preserves the
designed world layout. Color and numbering vary by unit while belonging to
the same architectural module on both faces.

The additional passage/site pass below follows the close-up inspection.

## Pass 4 — service access, amenity routes and final frame review

**Value first:** flat quick colors remain visibly synthetic against the balanced
photographs. The green gallery profile now belongs to the period; it still
needs the reference’s material breakup and worn lower concrete at look-dev.
Shadowed rear patios and the core retain dark recesses. The first dark meter
views concealed the construction, so service/core inspection frames now use a
120 W temporary area fill, disclosed in camera provenance. That fill is absent
from the heroes and photo comparisons.

**Construction critique and corrections:** the linked wings’ original five-foot
wall gap was not five feet of working space. A neighboring balcony or condenser
consumed it, and canopy posts crowded the meters. Widen the walls to ten feet
and bear the low canopy on wall ledgers/cross beams. Actual opposing mesh bounds
now leave at least 1.295 m in the L and 1.564 m in the offset building through
2.1 m height, exceeding the authored 1.2192 m reservation. This does not certify
an electrical installation. Broad site views also cropped the amenity corner;
pull back those cameras. Connect pool/playground walks to the main path and
open the pool’s north fence with a separately hinged, outward-opening gate.

**Slider correction:** the first nine-position sash sweep failed at rest: the
outer moving extrusion intersected the fixed center stile, and the handle
belonged to the fixed window. Move the moving track 35 mm farther outward
and put the handle on that sash. The revised sweep tests actual fixed/moving
surfaces, separate from pivot serialization and the door-leaf tests. No
triangles were added by transferring that handle.

**Architectural judgment:** the central-core block has a legible nine-foot
floor rhythm, deep roof and paired unit/balcony bays. The open-core offset
version belongs to a later landlord-built phase. The two gallery variants
read as economy walk-ups with separated end flights and usable upper access;
they should not acquire a continuous mansard apron across their doors. The
six-unit mansard and brick/gable rows differ convincingly in period; the
four-unit green row is a smaller related place. The garage row’s clipped
cross-gables, filled raised foundations and sloped approaches resolve its
previous construction failures. Rear patios remain too repetitive and bare,
and the site’s sparse trees and identical pickups expose the staging. Those
are explicit next-gate weaknesses, not evidence of photographic realism.

The two final heroes’ encoded display-luma percentiles (whole frame, including
sky/ground) are .002805 / .310426 / .842056 and .069755 / .558953 / .845144
for p1 / median / p99, respectively. Neither has any channel above .99.
These are exposure/clipping checks, not linear photometry, surface albedos or
a substitute for matching materials to photographs. `tonal-range.json` records
the complete figures. The current physical gate passes 2,530 hinged leaf
poses, 1,998 sliding-sash poses and 504 garage-section poses. Complex point
correspondence is explicitly unmeasured; its counts and pivot/socket frames
are checked, while the building forms are compared as standalone exports.

**Final pair judgment and gate evidence:** opened all 52 current exported
views, all three exported photo pairs and all three independent source pairs.
The green economy gallery differs substantially from the used 2004 building’s
brick skin, recessed private balconies and continuous mansard. It is a
comparison of related period types, not a replica. Against 1978, the open
access rhythm and fin profile read correctly, while this authored version’s
stair flights project farther forward and its kitchen windows are taller.
The garage row has the period’s repeated private entries and front gables,
but fewer facade projections and no arched stair windows. Those choices and
the explicitly simple room backings limit the comparisons; low corner-fit
residuals do not erase them. Source/export pairs show the same form and quick
material response. No bake-loss conclusion is possible before look-dev.

`make WIDTH=1200 SAMPLES=32` completed with exit 0 after the staged rebuild;
`make check` also passed. The final repository check has 1,672 tracked/staged
source files and zero errors. `renders/review/evidence-audit.json` verifies
all 58 current frame hashes, Cycles provenance and the hero/ground eye/lens
settings. All twelve exports pass, with zero degenerate geometry or metric
UV triangles, and 197 pre-existing delivery/docs hashes unchanged. Images
remain local rebuildable evidence; no checkpoint JPEG is committed as final
documentation. The work stops at this gate, before look-dev.
The staging lawn also exposes native patch boundaries under raking light;
continuous ground treatment belongs with the site material pass.

## Limits deliberately retained for the look-dev gate

- Brick, wood, shingles, stone and steel are flat quick-color reservations.
  Surface manufacture, meaningful shared trim mapping, causal fading/rust/dirt,
  roughness variation and final maps are absent. These are not product photos.
- Repeated window backings remain simple; unit room reservations are schematic.
  Full interiors, fire-resistance assemblies and local accessibility/egress
  certification are not delivered.
- The original plan differs from each photograph. In particular the economy
  gallery has a continuous access route rather than the 2004 photograph's
  recessed private balcony rhythm; the garage row lacks its arched stair bays.
  The comparison exposes those differences instead of treating a low fit error
  as proof of architectural equivalence.
- Context uses original library source geometry and simplified materials. Parked
  pickups repeat; a final complex should use several accepted car types and the
  canonical landscape/ground maps. Landscape density and tenant dressing are
  still sparse. No claim of a finished photorealistic site is made.
- Linked wings provide L/offset assemblies. Arbitrary continuous L-roof plans,
  sunken-floor circulation, final collision/navigation, LODs and dusk window
  emission remain future work.

No kit or accepted family delivery was changed. This checkpoint's extra rigor
went into openings, construction, circulation, mechanics and independent
serialization checks; it did not add a new material atlas.
