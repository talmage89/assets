# Privacy fence image and construction review

Only the privacy system is in this stop point. Reference images remain local;
see refs/SOURCES.md. Observations below distinguish photographed construction,
authored aging, physical measurements and serialization checks.

## Pass 1 — source, Eevee, 1000 px / 16 samples

Opened all six images in `renders/pass1/contact.jpg`: good side, rail side,
grain, post saddle, gate front and gate back. Compared directly with both
Denver construction photos and Classic Fence Co PDF p36 (weathered dog-ear).

- Picket dog-ears, three rails and the gate's lower-hinge-to-upper-latch brace
  direction read correctly. Two source sections need different board rhythms.
- Growth bands are too regular; identical fiber phase makes the boards look
  machined. Knots are too soft and wide in comparison with the sharp dark cores
  and disturbed surrounding fibers visible in the photographs.
- Very pale source light washes away the gray/tan wood. Back views are unusable:
  the seamless backdrop sits between the reverse camera and the product.
- Source audit also caught a latch pivot/frame update error. The corrected game
  assembly measures 2068 triangles before the small latch stand-off addition.
- Solid motion checks caught the latch bar entering the post and strike backing
  during release. Moved the bar in front of the post plane, with a real pivot
  stand-off; no collision exception is used to excuse that interference.

Changes: independently phase each board's fine fibers, reduce broad stripe
contrast, tighten knot cores, introduce more tan/gray variation; rotate the
studio for rear views. Keep silhouette geometry lean and leave the boards'
end checks and fasteners in the bake. The 4096 bake is downsampled to one 2048
atlas; measured initial packing has zero overlaps, 50.2% coverage and 233 px/m
median, with extra density on hardware and the gate.

The daylight cedar photo calibrates joinery/camera, not pine hue. Its inferred
8 ft bay and rail positions have photographic uncertainty: the initial fit RMS
is 5.60 px over a 475×420 crop. Classic Fence p36 supplies a separate direct
weathering comparison; the watermarked PDF is not used as a texture or docs.

## Pass 2 — source and exported GLB

Reviewed the four source Cycles views in `renders/pass2-final/contact.jpg`
and its calibrated rail-side photographic pair, then every exported studio
view in groups covering heroes, turnaround, grain, joinery, hinge hardware,
gate front/back, exploded modules, posts and human scale. Also opened the
assembled corner pair, Eevee view and exported photo-match pair.

- Increasing irregular earlywood erosion and drying checks made the gray/tan
  boards read as aged timber at gameplay distance. The source remains finer
  than the delivered atlas: at 233 px/m, the closest grain and bracket views
  show filtering softness. That is a real delivery limit, not source quality
  presented as a game result. Macro grain is still more regular than the photos.
- Source/end-grain review separated timber axes from height above grade: splash
  now stays near the ground on horizontal rails, and cut faces expose growth
  rings. The two section seeds retain coherent gray/tan hues instead of green
  or pink random board colors.
- Export review exposed a modular projection error: neighboring rail brackets
  had baked metallic marks onto bare post faces. Changed the bake to eight
  isolated module/moving groups and preserved 65 explicit wood coordinate
  frames. The imported ORM now measures **0.0 metallic** at 96 post-body sample
  points. The isolated post render visibly confirms the correction.
- Corrected the cropped post inventory camera. The reverse corner view needed
  a lower aim and a wider seamless: independent vertex projection now frames
  all complete post/assembly geometry; corner rays hit the backdrop in all
  four image corners. View settings are separated from delivery policy.
- The gate's bent straps initially crossed the pin bore; trimmed their necks
  around it. Both high/game released-gate sweeps now pass at 111 poses over
  −110°…0°, and both latch sweeps pass at 34 poses over −65°…0°. No collision
  exceptions are used. Physical hinge-axis error measures zero at stored float
  precision.
- Twenty-eight evaluated triangle-surface support checks per quality pass.
  Maximum sampled contact bound: 0.00013 mm game, 0.00005 mm high. The measured
  clear opening is 914.4001 mm, leaf 888.9999 mm, with 12.7001 mm side gaps;
  brace bearing-plane errors are below 0.00012 mm.
- Actual imported post-center sockets coincide for the straight run and the
  assembly proof. The imported 90° corner check measures zero penetration at
  its 0.3 mm acceptance tolerance. These are construction tests, distinct from
  the kit's independent GLB serialization/texture/UV verification.

The final calibrated rail-side camera is approximately 71.4 mm, with a
5.64 px photographic RMS on the 475×420 crop. Blender's independent projection
agrees within 0.00028 px. The reference is unsurveyed new cedar, so remaining
rail/camera residuals and its warmer hue are not hidden or called an exact
pine material match. Classic Fence p36 remains the direct aging reference.

Final acceptance: preserve the lean geometry and shared texture memory; accept
close-up filtering and some procedural grain regularity at this repeatable
fence's intended viewing distance. No white picket or chain-link work is started.


## Accepted privacy follow-up — knot population only

The lead accepted construction, sockets and lean geometry, and rejected the
repeated soft dark ovals. Changed only the shared pine material: approximately
half of timber draws are clear, remaining branches occur in one or two whorls,
with strongly skewed sizes, tilted axes, a narrow resin ring and occasional axial
check. Continuous grain diversion replaces blending a broad oval into the grain.
UV aging desaturates knots along with their board. All geometry, pivots and
installation choices are unchanged.

Opened `renders/knots-glb/match_rails-pair.jpg`, rendered from the freshly baked
export at the existing calibrated camera, beside the Denver construction photo.
The dots no longer march across every board: Section A has 12 clear pickets and
8 branch cuts on the other five, with radii 2.0–21.0 mm, some clipped by board
edges. The wide variation, quiet branches and local grain deflection read as
wood rather than a spotted decoration. The cedar photo remains warmer and more
knotty than this aged pine; that material/age distinction was already accepted.
Fine resin lines and pin knots soften at the unchanged 233 px/m atlas density.
Source and GLB checks pass with the original 664-triangle section meshes.
Final studio images are regenerated from the revised exported textures; family
docs JPGs are deferred until picket and chain-link are also complete.


## Picket pass 1 — construction and source photo match

Opened all four source studio views (`picket/renders/pass1/contact.jpg`) and
`picket/renders/pass1/match_pickets-pair.jpg` beside the installed white-timber
photo. Gothic shoulders, pinched throats, spaced-board rhythm and two rails read
correctly. The authored 42 in stock and adjusted 8 ft center spacing differ from
the unsurveyed nominal 4 ft photo, so the camera has a 20.8 px RMS and reaches its
180 mm fitted-lens limit; this is a visual comparison, not a surveyed dimension
claim. Manufacturer stock dimensions remain the dimensional authority.

Critique: white-on-light-gray studio lost silhouette and looked like plastic;
paint lacked broad timber relief, and ground mildew was too faint. Adjusted the
picket studio's seamless to darker neutral gray (a new optional kit parameter),
added subtle longitudinal raised wood beneath opaque paint, and increased only
the caused lower wet/splash mask. Kept paint overwhelmingly intact. Increased
atlas density from the first 160 px/m layout to use the available 1024 set more
efficiently; stopped that early bake before the change. No additional texture
memory. Hinges now place both mounting screws over actual gate boards rather
than the open spaces between them.

Physical preflight measures 80 support contacts per quality, brace bearing,
914.4 mm clear opening, 12.7 mm side gaps and coaxial hinge pins; released gate
sweeps through 111 poses without collisions. These are surface measurements,
separate from GLB serialization. Finalized/exported checks repeat them after bake.


## Picket pass 2 — delivered GLB and complete run

Opened the freshly exported photo pair at
`picket/renders/pass2-glb/match_pickets-pair.jpg`, every final studio view in
`build/picket-export-review.jpg`, both assembled corner views, and the Eevee
hero. The darker studio separates white timber without changing its paint;
subtle ground discoloration now reads in the hero, and bare end chips remain
restrained. Rear rails, compression brace, black hinge straps and capped post
silhouettes read as real backyard construction. The gate clears its strike
with the latch raised. No further art iteration is warranted for this repeated
street asset.

Weakest: close-up painted grain, screw heads and chips filter softer than the
photo/source at the 208 px/m shared 1024 atlas. French Gothic shoulders retain
some angular simplification in the game silhouette. The source photo's larger
height and unsurveyed spacing leave the explicitly reported 20.8 px camera-fit
residual; no pixel/color tracing was used. At backyard distance these losses
are acceptable in exchange for one shared 4 MiB set.

Delivery: 996 triangles per section, 32 per capped post, 848 for the complete
gate bay (including both posts), 2936 total library. One material, three 1024²
maps; GLB 2,484,636 bytes. UV coverage 52.48%, zero overlap pairs, density
p5/median/p95 about 208.34 px/m. Both high/game checks pass **83 distinct support
contacts** per quality (max sampled distance bound 0.000229 mm), 111 released
gate poses and 34 latch poses, with no allowances. Imported straight sockets
coincide and a 90° corner measures zero penetration at 0.3 mm tolerance.
Serialization verifies zero rest-vertex error and required socket matrices.
Final per-type contacts remain ignored; family JPG composition is deferred to
batch completion.


## Chain-link — careful construction/material pass

Opened every first source preview, the Denver-independent New Orleans mesh
close-up and its calibrated pair. The initial source preview was black because
its material looked for UVMap while source cards used BakeUV. Corrected both
image UV and tangent-normal layer names; final exports always use UVMap. Opened
the corrected source pair at `chain-link/renders/corrected/match_mesh-pair.jpg`:
round-wire tangent relief and the subtle over/under displacement now survive.
The fitted diamond landmarks have 1.7 px RMS on the 340×240 photo crop, lens
about 139.9 mm. The unsurveyed commercial photo is used for wire/fitting response;
its fence height and twisted upper selvage do not redefine our 4 ft residential
knuckled design. Fine loop topology is necessarily approximated by the alpha
card, and its wire responds less richly than actual round 3D wire up close.

Technical critique caught rotated tension bars (rotation after parenting had
moved them about the module origin), sleeve/strap intrusion into hinge bores,
and fork jaws crossing their pin. Corrected authoring transforms, hollow bores,
bent clamp necks and open fork jaws. Staggered the corner's second band set by
24 mm; added real downward stamped rail-end lugs instead of floating hollow
cups. Both high/game sampled gate and fork sweeps now pass without allowances,
and physical triangle-surface contacts check the fittings separately from GLB
serialization. Fabric ties are checked against the card support envelope;
this is not a claim of a continuous 3D wire collision surface.

The prefab gate bay is three budgeted modules (hinge post, latch post and the
moving gate), each under 2k. Its combined count is reported rather than hidden
behind the per-module number. Four bay end treatments and two terminal handed
versions are necessary to keep the fabric on the same side of the frame while
joining actual tension bars. The corner proof uses a true terminal-to-terminal
bay; a line-post infill would run through the corner's center.

UV packing initially gave thin 3 m bottom wire the same importance as hardware.
Reduced its unique UV priority and gave the alpha field a 256² repeat plus a
256×32 knuckle strip. Unique metal UVs now pass the ordinary non-overlap check;
explicit repeated fabric UVs pass separate region/density/MASK tests. The two
materials share three 1024² images, about 4 MiB total. Per-type studio/GLB review
and exact final budgets follow after the final build.


Final imported-corner testing caught two real fit issues that a serialization
comparison would miss: the decagonal cup bore pinched the round rail by
0.53 mm, and a straight bottom tension wire crossed its termination bar by
1.41 mm. Increased the authored cup bore with its wall retained, and ended the
wire at the inward bar surface instead of carrying it through the bar toward
the post center. The same low geometry is checked before rebake and again from
the final GLB; no collision exception masks either problem.


## Final chain-link delivery review

Opened the complete exported studio contact (14 Cycles views, Eevee, both
assembled corner views) and the final GLB/photo pair. Mesh scale, tube gauges,
round gate frame, terminal bands, top/bottom ties and fork latch read correctly
at backyard distance. Tangent relief survives the wire tile; close crossings
remain flatter than actual interwoven round wire, and subpixel alpha coverage
fades/aliases in the widest views, especially Eevee. This is the weakest part
of the alpha-card method and is documented rather than disguised with thicker
wire. The unique metal atlas also filters fine screw/spangle detail.

The pale studio reduced contrast on the thin wire. Changed only the chain-link
seamless to a darker neutral green-gray and opened the exported assembly preview
at `chain-link/renders/contrast/corner_good.png`; the fence reads more clearly.
No mesh, material maps or texture budget changed. Final studio views are
regenerated with that presentation setting before composing family docs.

All source and delivered tests pass: 9116 triangles in the complete library;
504 per bay, 492 line post, 876 either terminal, 1544 corner, and a 3312-triangle
gate prefab made of 1156/876-triangle posts plus a 1280-triangle gate/fork. The
GLB is 2,052,152 bytes with two materials sharing three 1024² maps. Unique UV
coverage 20.25%, zero overlaps; p5/median/p95 175/256/271 px/m. Reused fabric is
840 px/m, alpha-tested/double-sided, with 11.06% covered wire in the field tile.
110 evaluated support contacts per quality pass, maximum sampled distance
bound 0.000169 mm; 111 gate and 96 fork poses pass with no allowances. Imported
corner penetration and all post/gate snap errors measure zero at stored
precision. A repeated factory-startup game build produces geometry hash
`1da5a93a51651f2964a3b40a9151ac10feb0ee8dc499458782a9902e057ac22f`.


## Batch acceptance — complete family

`make -C fences all check` completed with exit 0. This includes both sublibrary
builds/checks, fresh opaque-path rebuilds after the additive atlas changes,
GLB photographic pairs, the privacy construction check, all final Cycles/Eevee
studio and short corner/gate runs, and repository rules. Final GLB/photo pairs
were opened for privacy (`renders/photo-glb/match_rails-pair.jpg`), picket
(`picket/renders/lookdev-glb/match_pickets-pair.jpg`) and chain-link
(`chain-link/renders/lookdev-glb/match_mesh-pair.jpg`). All 51 studio/assembly
images were reviewed through the per-type contacts and focused detail views.
The GLB metadata hashes match the current deliverables. 42 whole-object views
pass independent vertex-projection framing checks; intentional detail crops
are excluded from that check.

The five family docs JPGs were generated only after every fix and all framing
checks. Opened all five: three assembled heroes, one construction sheet and
one inventory/good-side/rail-side/human-scale sheet. Widths are 1440–1600 px;
file sizes 58,908–198,511 bytes. No reference photograph enters committed docs.
Family contact: `renders/family/contact.jpg`; per-type contacts remain in each
`renders/final/contact.jpg`. All are rendered from exported baked GLBs.

Final GLBs: privacy 9,875,704 bytes / 2,100 tris / 1 material / 2048² set;
picket 2,484,632 bytes / 2,936 tris / 1 material / 1024² set;
chain-link 2,052,152 bytes / 9,116 tris / 2 materials / one 1024² set.
All raw normal errors are below 1.2e-7, re-imported rest vertex error is zero,
and required socket matrix error is at most 1.2e-7. All unique UV overlaps are
zero; repeated alpha UVs are checked explicitly. Additional texture memory is
8 MiB (4 + 4), versus the 16 MiB allowance, for 24 MiB across all three types.
The README lists all per-piece budgets and the three-module chain gate prefab.

Four `kit.test_delivery` tests pass. The explicit-coordinate bake fixture
passes (1.43e-6 m max coordinate discrepancy); the no-GPU alpha-atlas fixture
passes real finalize/export/re-import, negative tests for escaped tile UVs and
unique UV intrusion, and checks of retained alpha holes and glTF MASK/double-sided policy.
Defaults remain compatible with the opaque asset path.

Weakest points remain close-up filtered wood/paint detail, simplified Gothic
shoulders and flattened/subpixel alpha wire. They are accepted at backyard
viewing distance. No additional art pass or texture memory is needed. Nothing
is needed from the lead. A future engine import helper could preserve alpha
coverage in generated mipmaps; no engine-specific integration is part of this
asset family.

## Phase 2 combined-kit regression and painted-picket wear

The privacy, painted-picket and chain-link libraries, all module variants and
all three corner/gate assemblies rebuilt from clean sources on the combined
kit. `make -C fences` and `make -C fences check` exited 0 (logs in
`../build/polish/`). Opened each new assembled hero against its committed JPG,
all studio/Eevee/assembly contact views and all six source/shipped photographic
pairs. No visible model/material integration regression. Privacy: 2,100 tris /
9,875,704 bytes; picket: 2,936 / 2,484,624; chain-link: 9,116 / 2,052,076. The
small PNG compression differences from the latter two README byte counts do
not change texture sizes/material counts. The reverse assembly views have a
dark studio corner away from the models; the picket's reverse studio orientation
is being aligned with its diagonal camera as part of its changed-look pass.

Used-picket reference: TriviaKing's installed, peeling painted fence, CC BY-SA
3.0, recorded in `refs/SOURCES.md`. Added measured envelope landmarks, explicitly
retaining the original French Gothic geometry; the reference has plain pointed,
leaning boards and different site construction. The photographic residual is
19.45 px at the 450×1050 crop and is separate from the independent camera check.

First wear checkpoint: opened the source and exported pairs in
`picket/renders/wear-pass1-{source,glb}/used_pickets-pair.jpg`, the GLB hero, and
all front/side/back/top/paint views. Low green-black mildew and splash now read
at full-frame scale and are stronger on the slow-drying rear face. The first
upper flakes were still too thin after the 1024 bake. Enlarged the paint-breakup
patches along cut ends and exposed rail edges to roughly 2 cm across the grain;
kept broad vertical faces coated. Cross-section edge masks now require proximity
to both section limits, using the actual rail thickness/height, so a rail's broad
face cannot be mistaken for one continuous edge. Source geometry is unchanged.

Second picket wear checkpoint: source and GLB pairs in
`picket/renders/wear-pass2-{source,glb}/used_pickets-pair.jpg` and the complete
hero/front/side/rear/top/paint probes were opened. Broad mildew survives the
bake, and the enlarged top flakes survive as gray patches, but the shipped
cut tips still look much cleaner than the used photograph. Rejected upper
wear strength again. Increased flake coverage only inside the existing cut-end
and manufactured-edge masks, and darkened the revealed aged cedar. Paint
across the broad board faces and the accepted low mildew remain unchanged.
Pass2 check passed: 2,936 triangles, one 1024 set, 2,962,696-byte GLB.

Third picket checkpoint: opened both used-photo pairs and all seven exported
hero/orthographic/paint/reverse probes in `picket/renders/wear-pass3-*`.
Accepted the now-visible exposed upper cedar and rail-edge paint loss; the
clean broad faces retain white paint, with graded green-black mildew at the
feet and stronger on the shaded back. The full hero reads used. The used
photograph is older and has plainer tips; it calibrates the causes and visible
scale of wear, not a geometry replica. The 1024 filter still softens small
flakes/nails, while the broader upper loss and low splash survive.
`make -C fences/picket export check` passed, 2,936 triangles / one material /
3,134,324 bytes. Maps BaseColor / Normal / ORM are
1,180,454 / 876,986 / 812,527 bytes. The reverse probe also verifies the
215-degree studio orientation removes the dark upper backdrop corner without
changing any camera or asset geometry. Final assembly verification follows.

Final picket `make` exited 0 (`../build/polish/picket-final.log`). Opened the
complete final Cycles/Eevee/assembly contact, both assembled corner views and
all four refreshed source/exported photo pairs. The good-side hero clearly
shows upper paint loss and a dirty foot; the shaded reverse has stronger
low mildew and a continuous backdrop. Family `make check`, independent posed
GLB framing and hash-checked five-image composition all passed; logs are
`../build/polish/family-{check,framing,docs}.log`. The three changed final JPGs
were opened and held for the end-of-pass docs commit. Unchanged privacy and
chain-link hero JPGs retain their original committed bytes.

A final presentation correction applies the same 215-degree studio orientation
to the chain-link reverse assembly. Its previous 180-degree setting left a dark
upper background corner away from the model. Full `make -C chain-link` passed;
opened all refreshed studio/Eevee/assembly views and both photo pairs. The
reverse background is continuous, with unchanged geometry, materials and
camera poses. Final independent family framing passes all 42 views, and the
51-view complete family contact is refreshed. The unchanged privacy and
chain-link hero JPGs retain their original committed bytes; this correction
adds no documentation image version. Logs: `../build/polish/chain-backdrop-final.log`
and `../build/polish/family-framing-final.log`.

Combined-library diagnostic limit: the unchanged chain-link frame bake retains
19 missed/black interior samples out of 2,886,844 checked at 4096 (normal misses
zero). This predates polish; the frame and analytical alpha weave have no
visible artifact in the reviewed final views. No texture fill or geometry
change was introduced. It remains a small documented coverage diagnostic.
