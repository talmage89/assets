# Evening 89 critique record

All source and final images are made by scripts. Reference photos appear only
in ignored comparison pairs. Main reference: Fire Sense 61436 manufacturer
photo, 89 in high, 33 in hood. The steel cabinet, hinged door, lap seams,
control graphics and external guard are original design choices.

## Pass 1 — source / proportions, construction, physical checks

Inspected individually: renders/pass1/hero_closed.png, hero_open.png,
controls.png, burner.png, casting.png, match_whole.png, and
match_whole-pair.jpg against refs/pro-full.jpeg, pro-head.jpeg, pro-base.jpeg.
24 samples, 900 px source views; photo fit 700 px. Original camera fit RMS
12.1 pixels on the 1000 px photograph, lens at the 180 mm fit cap. This is
an approximate product-proportion calibration, not an EXIF claim.

What looked CG: too much empty hero framing; uniformly copper emitter against
the reference's silver perforated sheet; insufficient blue thermal transition;
wide black upper/lower door gaps; pristine, overly even control knob.
The reflector's manufactured section and source screen detail read clearly.
The painted cabinet intentionally differs from the stainless reference.

Physical checks caught 0.5–1.0 mm hinge interference and a 0.4 mm flange/post
gap. The initial front spider leg also obstructed the useful tank access path.
The knob's solid back had no actual spindle bore. These are construction
failures even though the export would serialize them faithfully.

Changes: move hinge axis outboard, retain gauged leaves; add blind spindle bore;
join the post to its flange; move supports to sides/back; narrow door gaps;
use a silver/straw emitter with a blue upper heat zone; increase the hood's
localized underside tint; move hero camera closer. Ground/latch wear remains
restricted to physical contact and exposure masks rather than uniform dirt.

## Pass 2 — corrected source / material response and assembly

Inspected all five renders in renders/pass2 (1000 px, 40 samples), plus
match_whole.png and match_whole-pair.jpg against the same manufacturer photos.
The emitter now reads as stainless sheet with straw/blue oxidation; the hood
underside shows the actual rising plume and radial spread. Top surfaces stay
neutral aluminum. The enlarged hero framing is useful. Cabinet finish remains
subtler and more uniform than a well-used real heater, especially at the latch.
The fine slots and screen are deliberately baked detail, so bake loss is the
next critical judgment. Silver pole highlights differ from the reference's
chrome-like studio streaks, a lighting/roughness difference rather than scale.

Construction revisions after this review: hinge leaves shortened to fit between
fixed knuckles; fixed straps offset behind the door return; real drain bores
through the floor/base replace decorative shadow strips. Boolean remnants are
welded at 1 micrometer and degenerate edges removed at .1 micrometer. All
source topology audits and physical support checks pass. Both source meshes
pass 36 door poses, 28 knob poses and 25 poses per wheel with no unallowed
penetration. These are sampled sweeps, not a continuous proof. A real blind
bore removes the knob/spindle collision. Side/rear spider leaves access clear.

Proceed to the 4096 bake and 2048 GLB, then critique the delivered materials,
perforations, small labels and optional owner-tank fit before final documentation.

Extended physical support audit before final bake: the first contact list did
not cover every visible assembly. Inspection found short hood studs, guard
hoops with no radial mounts, and wheel ears that did not reach the base pan.
Extended studs through the crown, seated nuts on a washer stack, lowered the
crown screws onto its actual surface, added 16 radial guard mounts and extended
wheel brackets into the base. Added measured contact gates for these parts and
all three internal stanchions. All pass with surface intersection/contact;
these are actual evaluated-mesh checks, not copies of construction constants.
The optional external-tank checker passes on the source: minimum hose gap
16.08 mm and minimum side-stanchion gap 15.9 mm, with zero measured penetration.
The floor has actual tank contact. Lateral stops leave 7.86–10 mm slack around
the foot ring. No tank removal-path simulation is claimed.

## Pass 3 — exported GLB / bake loss, correction and delivery judgment

Inspected all 12 initial Cycles views, Eevee, and the matched GLB/reference
pair. The first export passed numerical UV, vector-length, bounds and
serialization gates but failed visual delivery: control face entirely black;
reflector and band edges showed jagged projection. Rejected it. Initial images
are retained in ignored renders/pass3-initial-glb, pass3-initial-eevee and
pass3-initial-match, rather than becoming committed docs.

Measured diagnosis: the control print plane's source normal was +Y, facing
into its backing. The closed-solid normal operator had reversed this elevated
open sheet. Its actual GLB texels were unit vectors pointing inward (blue 0)
and AO 0, despite correct BaseColor labels. The badge normal was already −Y.
Fixed kit plane_uv to honor the authored front before assigning corner UVs;
the regression uses this elevated-panel case and passes. Added a delivery
surface-ray/UV check; it correctly rejects the old GLB at 222 panel samples.

For the thin reflector, match macro radial stations between high and game,
then use a .5 mm cage / 3 mm ray distance below its .9 mm gauge. Fine source
bevels, screw drives, print, vents and shader relief still transfer. This
avoids trying to bridge high/low chord differences with a cage wider than the
sheet. Increased the visible knob's radial segments within the 15k budget.
Rebuilt and rebaked the full 4096 set. No atlas repair or texture filling.

Corrected GLB review: inspected every rebuilt Cycles view, Eevee and the photo
pair. Labels return with a front-facing normal (panel blue P5 255, AO median
241, byte contrast 134; all 222 sampled hits pass). Main heat colors and screen
pattern survive the bake. The owner cylinder is seated and the door clears it
in the fit view; it remains absent from the exported asset. The lit-state
material gives a warm orange screen without changing off-state steel color.
The reference has a shinier stainless cabinet and a lift cover by design;
our painted hinged cabinet is not claimed as a copy of its silhouette.

Accepted limits: the thin reflector/crown edge still has some atlas-edge
sparkle at extreme close-up, and small control lettering is softer than the
source at 2K. Screen holes are opaque normal/albedo recesses, not see-through
mesh. This reads correctly at ordinary player distance and avoids an extra
alpha material/texture set. Paint weathering is restrained rather than a
heavily neglected appliance. Retain these honest limitations in the README.
No collision check claims a continuous sweep or a tank extraction proof.

Build-path validation: full `make TANK_REFERENCE= WIDTH=96 SAMPLES=1` passes,
including docs, source audits, UV/re-import checks, physical motion, support
and printed-face gates. The optional tank render/check are explicitly skipped;
no external-file dependency reaches modeling, baking or export. The tiny
validation renders are retained under build/no-tank-renders and were reviewed
as a contact sheet. Restoring default `make` regenerates the 1400 px / 72-sample
final set and the tank fit view. No low-resolution validation JPG is committed.

The final game source was rebuilt into a second clean scene; its geometry hash
matches exactly: f0252f0349ab62d33aa9643063244c875db209c22350ca36396aca1087d73c18.
Texture repeatability was not separately rebaked/tested. Shared kit changes:
optional emission tint without another image, plus authored-front preservation
for open print sheets; composed export / alpha / optical / variant / studio
fixture passes with the new print regression.

Final close-up construction correction: the crown's .155 m radius had two
collinear overlapping vertical faces in its folded skirt. Topology/manifold
checks did not detect that self-overlap. Give the inside skirt its proper
.1541 m radius and a distinct bottom thickness face. This removes the double
surface rather than treating the dark stitch pattern as mere texture loss.
Rebuild the full delivery again; prior exported images remain ignored.

Crown correction accepted after inspecting rebuilt hero, controls, burner and
reflector close-ups: the crown skirt is now a continuous clean band rather
than a dark stitch. The outer .9 mm reflector hem still has subpixel glints at
extreme magnification; keep that smaller limitation and the softened tiny text.
The final export is 14,536 triangles / two materials / three shared 2048 maps /
6,832,488 bytes. UV coverage 50.996%, density P5/median/P95
451.64 / 602.95 / 1122.24 px/m, measured overlap zero. Panel sample check now
reports blue P5 255, AO median 241, BaseColor contrast 116 after repacking.

Completion: default make and explicit make check pass. Reviewed the final
12-view Cycles sheet, final Eevee hero, photo pair and regenerated docs; all
render metadata matches GLB SHA-256
7632597fc6932c61883cfdeb8fe92ee243276d0299f9375439c0c4e848004e63.
Final docs are three JPGs: hero 71,432 bytes, turnaround 96,245 bytes, details
193,490 bytes; all at most 1600 px wide. They are committed only at completion.
Suggested kit follow-up: detect self-overlap in folded profiles as well as
manifold topology. Nothing needed from the lead; stop before the mower.


## Acceptance follow-up: visible patio wear

The owner accepted the construction but rejected the default finish: the old
wear masks did not read at hero distance. This revision changes procedural
materials and the used-photo review camera only. No modeling parameters,
vertices, pivots, UV islands, budgets or delivered texture slots are added.
Default WEAR=.35 now represents visible ordinary outdoor service rather than
requiring the owner to turn the value up.

Cause placement: surface-normal exposure fades/chalks the up-facing cabinet
shoulder and base pan, with only a small diffuse-sky contribution on sides.
The dragged base lip and tipping-wheel neighborhoods carry interrupted,
elongated 3–15 mm chips. A fragmented turning arc and handling polish sit at
the actual latch bezel, with edge scratches on its ABS handle. Trapped moisture
locates oxide at the door hem; actual floor drain angles and flange fasteners
anchor short runoff marks. Fastener recesses and edges receive crevice oxide.
Dust settles on the upward reflector, especially behind the crown and real
petal laps; sparse broken mineral rings represent dried rain. The accepted
underside/emitter heat tint is retained. Masks modify color, roughness,
metallic response and micrometer-scale relief and bake into the same atlas.

Reference: 3268zauber's 2009 Terrassenstrahler photo shows restaurant heaters
in service, with scuffed bases, stained metal and corroded shoulders. It is
not a catalog photo; exact service age is unknown. The foreground appliance
is stainless and uses a lift cover, so its color and detailed cabinet shape
are not asserted as our target. Cropping and inspected landmarks fit the
review camera only. Its 68.95 px RMS over a 2956 px-high reference crop records
proportional differences honestly. CC BY-SA 3.0 attribution, modifications
and composite license accompany the pair. No photograph enters any material.

Wear pass 1 (exported GLB, 700 px used-photo comparison and 1000 px previews):
chalking, chips and door hem wear finally read at whole-object scale. Reject
the evenly orange drain tracks, round latch abrasion blob and excessive bright
rain rings: they resemble procedural decoration. Break the drain stains with
located fine-scale noise, use a fragmented latch-turn arc, and reduce mineral
ring coverage and contrast.

Wear pass 2 (same exported-GLB views): exposed shoulders are visibly lighter
than sheltered sides; base chips and modest rust read without overtaking the
paint; latch wear is localized. The used-photo pair shows plausible service
at the same framing distance. The top close-up still shows seam dust crossing
the seamless crown: restrict the angular mask to radii beyond the actual
crown edge. This last correction changes only the dust mask.

Geometry preservation is independently checked against the accepted GLB:
POSITION, NORMAL, TEXCOORD_0 and index buffers match byte-for-byte across all
five meshes, and node matrices match. One exporter tangent component differs
by 0.00009999; all other tangent components match. This is tangent rounding,
not a mesh/UV edit. Both high/game source geometry hashes and the complete
UV report match the accepted build. These comparisons establish unchanged
geometry and packing, separately from the kit's serialization/physical checks.
The local report is build/texture-only-check.json.


Wear pass 3: inspected the corrected exported hero, reflector close-up and
used-photo pair. The crown is continuous again; dust follows actual petal laps
and rain spots remain uneven. Chalking separates the exposed shoulders from
the cabinet wall. Latch abrasion, door-hem rust and base drag chips survive at
whole-heater distance, including the final scale view. The used reference has
more irregular stainless staining and a different head profile; matching those
literally would change the accepted original construction/material choice.
The final 12 Cycles views are from the same revised exported GLB, with the
owner cylinder appearing only in the authorized fit-check render. Existing
close-crop rim glints and soft tiny labels remain as documented; no new kit
changes or geometry changes are part of this correction.


Final delivery: `make -C patio-heater` completed with the full 1400 px,
72-sample Cycles batch, Eevee hero and one docs regeneration. Reviewed every
final view, contact sheet and all three bounded JPGs. All render metadata,
including the used-photo pair, identifies revised GLB SHA-256
`df58170f8e747790b37e79c876f200cfb6fea401da1f45c4a737b58aeadffc06`.
Export: 14,536 triangles, two materials, three shared 2048 maps; 6,967,140 bytes.
BaseColor / Normal / ORM PNGs are 1,414,879 / 1,559,859 / 3,111,233 bytes.
UV overlap remains zero; coverage 50.996%; density P5 / median / P95 remains
451.64 / 602.95 / 1122.24 px/m. Re-import vertex/socket errors remain zero.
Docs: hero 71,599 bytes, turnaround 88,858 bytes, details 192,995 bytes; maximum
width 1600 px. Pair: renders/wear-review-glb/match_used-pair.jpg; GLB-only view:
renders/wear-review-glb/match_used.png; credit sidecar in the same directory.
Final contact sheet: renders/final/contact.jpg. No kit changes or requests
for the lead. The mower is left for a separate session.

`make -C patio-heater check` also passes explicitly after final docs generation:
source topology/scale audits, UV and GLB re-import gates, camera projection,
sampled motion, owner-tank fit, construction support and printed-face bake
checks all pass. Repository rules and `git diff --check` pass.
