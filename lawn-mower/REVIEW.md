# Meadow 21 review log

Every image listed is inspected locally. Photos are comparison only, never texture inputs.
Review renders and pairs remain ignored. Final docs are generated only after the delivery review.

## Pass 1 — construction blockout and material placement

Inspected `renders/pass1/{hero_closed,side,engine,bag}.png` (Eevee) beside
`refs/product0.jpg`, `product1.jpg`, the used Famartin mower and GPS 56 mower.
The manufacturer parts diagram p.4 and operator setup p.8 were opened too.

Rejected: tire sidewalls wrongly extend to the axle, obscuring molded dishes;
wheel carriers appear unsupported outside the round deck; discharge tunnel is
an implausible tall tower; bag wire stands proud; radial starter details look
like sharp fins; cap residue has a square tank-sized boundary; bag wear is an
even speckled wash; floating/intersecting identification and warning prints.
The source mesh also exceeds the brief's 15k cap.

Corrections: annular tire cross-section, lower wheel radial counts and small
profile counts, stamped outrigger shelves/returns, lower bag inlet/tunnel,
inset bag frame, recessed shader starter slots, localized fuel wetting,
subdued rear fabric abrasion, relocated print backing. The Boolean deck cut
had nearly coincident vertices at the rolled lip; welded numerically duplicate
vertices and removed degenerate edges, then audited closed solids.

## Pass 2 — photo comparisons and mechanical correction

Inspected all four Cycles studio images in `renders/pass2/`, plus
`match_product-pair.jpg`, `match_used-pair.jpg` and both calibration overlays.
The product pair confirms familiar envelope/handle/engine scale. Different
manufacturers and original styling preclude exact correspondence. The used
pair deliberately compares deck/wheel/engine wear only: its catcher is rigid.
Our initial full-handle fit to that different mower was unusable; fitting the
three wheel centers, their ground contacts and the engine top improves the
local comparison. Camera fits are estimates; residuals are reported, not hidden.

Still CG: bag too smooth, exposed frame corners, chalky metal appearance,
shroud too featureless, repetitive holes and excessive sharp recoil fins.
Wheel support and rear chute corrections above were carried into pass 3;
recoil slots now come from negative material relief rather than raised rods.
Oil now darkens the crankcase broadly toward its seam, without spotted blobs.
Full hero wear is plainly visible on tire shoulders and deck lip.

Motion tests found 1.28 mm bail/cable contact at rest. Moved the sheath entry
outside the wire pivot. Both high and game sweeps now pass at 0.5 mm tolerance.
The cable service loop and starter rope require release/re-routing for storage;
these flexible spans are explicitly excluded from the rigid handle sweep.

## Pass 3 — source refinement, exported bake rejection and construction proof

Inspected every image and both pairs/overlays in `renders/pass3/`, then all four
exported-GLB images in `renders/bake-review/` (hero, engine, bag, folded).

Source improvements: lower bag inlet and inset wires read more plausibly;
annular tires reveal the wheel dishes; the engine label reads; broad low sump
oil is better than the first speckled mask. Residue is visible at full framing.
Still rejected the noisy rear fabric and lifted deck sticker. Switched to
analytical, script-generated ink on the deck and fabric itself; subdued the
rear fade/scuff contrast, added larger weave/drape normal detail and polished
hand-contact zones, a painted bail, casting seam relief and a braided tan cord.

The first baked GLB passed numeric export verification but failed visual review:
a geometric source-only engine-mount bead produced black projection tears on
the deck; the thin elevated badge also showed a normal-map oval. Removed both
projection hazards. The mounting bead is now shader relief and identification
is analytic ink on the actual shroud. Nothing was painted out of the bake.

Cross-checked overall width against Toro's published 23-inch gas-mower envelope.
The initial 670 mm stance was too wide; narrowed wheel center spacing to 538 mm.
Measured final width is 608.8 mm including the side cover. Recentered the origin
on the actual asymmetric footprint. Opened the cloth inlet (20 boundary edges)
rather than leaving a hidden cap across the discharge. Cloth is intentionally a
double-sided sheet, with a closed rear and open framed mouth.

The narrower wheels exposed a high-source lug/lower-handle contact that the
smooth low tire did not have. Moved the lower tube's foot inboard, preserving the
upper fold joint. Both high and game sweeps pass. A longer provisional bail
stroke collided with the grip/upper U; measured its stop at −36.5°, where the
actual surfaces have a 0.43 mm gap. The initial −26° stop left it too far from
the hand grip. Physical support tests also caught a 2 mm carrier/return gap;
closed that gap and retested, rather than increasing the support tolerance.

The heavily used GPS 56 mower has a different wheelbase and rigid catcher.
Its camera fit forced an implausibly low lens position. It remains a looking
reference for old grass/oil, but the final matched used view uses Famartin's
in-service fabric-bag mower. Differences in rear wheel diameter remain explicit.

## Pass 4 — delivery views, underside correction and acceptance

Inspected the complete exported suite: hero; front/side/back/top; engine and bag;
posed underside; 135° folded handle; held bail; 1.8 m scale; and Eevee hero.
Also inspected both final source/photo pairs and their residual overlays, and
both baked/photo pairs. Product/used landmark RMS is 19.59 / 58.65 px in the
710 / 3200 px photographic crops; independent projection disagreement is below
0.002 px. Different mower styling is retained as an explicit comparison limit.

The deck projection tears and badge oval are gone. The full hero visibly shows
grass on the lip, wheel shoulders and bag bottom, dark sump oil and cap staining.
The bag's large original print survives delivery; tiny engine text and tread lose
sharpness. The used reference has larger rear wheels; its body, fabric and use
patterns are the comparison, not an exact wheel/silhouette match.

The underside view caught detached lift sails caused by rotating an already
attached object about the assembly origin. Replaced these with bent 3.5 mm sheet
profiles meeting the blade edge. Added independent surface-intersection support
checks for both sails; both measure 0 mm separation. Opened the top framing to
include the entire grip. These changes were rebaked and all delivery views were
regenerated from the resulting GLB, with matching source hashes.

Retained limitations: the simplified casting/shroud and regular shield-hole
layout are less rich than the photographed engine; fabric folds and seams remain
regular, and Eevee shows a harsher bag-normal transition than Cycles. Tread is
normal-map detail and the smooth tire silhouette is visible in close-ups. Very
small print is blurred by the shared 2048 atlas. The underside blade is a simple
working profile, without a sharpened-edge micro bevel. Rope/cable re-routing for
storage is manual, with service spans removed in that view; no flex simulation
or armature is claimed. These are documented, not passed off as photo identity.

Acceptance: `make` and `make check` exit 0. The final game has 14,878 triangles;
all 11 Cycles views, Eevee and both baked photo comparisons match GLB SHA-256
`e796cd8a77f90145c8dac4352287e6509ca3c0b0b87b178ac27f95439ac6316e`. The two source comparisons match
the current high-scene hash. `build/final-evidence.json` records the provenance;
`build/determinism.json` proves the independent game rebuild. The complete
contact sheet is `renders/final/contact.jpg`. Three final docs JPGs pass the
1600 px / 200 KB limits. No kit changes, downloads of code or extra tools.

## Owner's four acceptance corrections

Scope: retain the accepted deck exterior, wheels/adjusters, engine shroud and
moving-node set. Correct the handle cable, presence bail, catcher construction
and interior clipping cake. No kit changes or new reference pixels.

- Replaced the airborne brake span with a 5.6 mm sheath following the right
  handle under three wrap retainers. It leaves below the catcher mouth in a
  slack loop to the engine brake bracket. The pale diagonal was the extended
  starter rope: the recoil pull now rests at its outlet with its cord retracted.
- Replaced the thin standing bail with 9 mm coated rod and two pivot bosses,
  sprung forward of the operator grip. Its held stop is −64.5°. A shortened
  upper bend clears the starter cover at the full retained 135° handle fold.
- Fabric side/bottom sections bulge and sag between five frame stations; the
  back panel bows outward. Corner gathers, welt stitches, weave, fading and drag
  abrasion are in the same atlas. A crowned molded polypropylene top with deep
  returned edges carries a thick molded handle. The source preview shows clear
  material/shape separation between this rigid top and the soft side panels.
- Interior-facing deck surfaces use exposed oxidized steel beneath olive and
  green-brown packed fibers. Outer blade throw and the discharge throat retain
  the heaviest cake; broken-away areas expose steel/rust rather than orange paint.

Inspected `renders/owner-fixes-preview/{hero_closed,bag,underside,bail_held}.png`
(Eevee, 1000 px). Cable routing, bag silhouette and green interior read clearly.
Both high/game motion sweeps pass after the released bend correction; the held
bail is 0.37 mm from the actual grip surface. Final delivery/pair evidence follows.

Bake preparation caught two numerical issues before final rendering. The new
curved fabric quads selected different implicit diagonals in source and game,
causing 31,054 missed interior texels. Triangulating the cloth explicitly at
construction gives identical source/game triangle positions and diagonals
(`build/cloth-projection-check.json`, 162 triangles). The new clip paths also
had coincident end caps; opening their undersides as sprung C retainers removes
those self-contacts. UV overlap returns below the unchanged verification limit.
The resulting game mesh has 14,942 triangles and all source/game motion sweeps pass.

The corrected bake reduces missed interior samples to 10 out of 8.8 million.
Before the final bake, measured all three cable retainers against the sheath,
and the stamped brake bracket against the crankcase: every declared support
intersects its mating surface. Those contacts are now part of `make check`.
The accepted wheel/deck-exterior/shroud geometry and wheel/handle pivots are retained.

Inspected the single current exported pair and its calibration overlay:
`renders/owner-fixes-used-glb/match_used-pair.jpg`. The bag is visibly rounded
between frame members; the rigid top and handle are distinct from the fabric.
The diagonal recoil line is gone; sheath clips and the lower engine loop read
at the used-photo camera. The thicker released bail stands forward of the grip.
Camera calibration is unchanged: 46.15 mm estimated lens, 58.65 px landmark RMS
in the 3200 px photographic crop. The reference has different rear wheels and
an all-fabric top, so this is a construction/wear comparison, not a replica claim.

Final correction acceptance: `make` and the subsequent `make check` completed
successfully. Refreshed the 11 Cycles views, Eevee hero and three docs JPGs once;
inspected the full contact sheet, hero, turnaround, engine/bag/underside details,
folded and held-bail poses, scale view and Eevee output. The clipping cake reads
olive rather than orange; the service loop and bag sag survive the baked export.
Fine weave remains limited by the shared 2048 atlas, and the fabric folds are
more regular than photographed cloth. Manual cable rerouting for storage remains
the documented limitation.

Delivery is 14,942 triangles, one material and one 2048 BaseColor/Normal/ORM set
(about 16 MB compressed GPU memory); GLB is 10,247,348 bytes. All 11 final Cycles
views, Eevee and the single current used-photo pair match GLB SHA-256
`afd9a1a47ee32a22397416e3fa035f0055d60931293205e219f25b79efff6cde`.
`build/final-evidence.json` records those hashes and doc limits; the independent
game rebuild is recorded in `build/determinism.json`. Source/game motion sweeps,
measured support contacts, UV/scale/normals and GLB re-import pass. Repository
check reports zero errors. Contact sheet: `renders/final/contact.jpg`.
