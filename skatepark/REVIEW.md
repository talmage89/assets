# Form / construction checkpoint review

This round deliberately stops before look-dev, baking, final UV allocation or
committed docs. Images come from fresh external glTF imports with quick form
materials. Photographs inform measurements and criticism; their pixels never
enter geometry or materials. Later look-dev must rejudge the baked delivery.

## Pass 1 — exported layout and construction, rejected

Color/value first: neutral quick concrete retains its gray under a lateral
sun, with dark bowl cavities, but the blue sky shifts shaded faces cool. The
untextured slab is too even to look used. That is an explicit look-dev task;
we must retain this contrast rather than bleach it later. Lawn and trees are
too uniform and coarse for final presentation. All eleven `renders/pass-1/`
images were opened, including the 101 hero and four construction details.

Compared with Alondra (neutral: unpainted light concrete behind its shallow
end), the bowl reads as an egg. Its north waist lacks the reference's kidney
indentation. The waterfall has a sharp floor junction. Fix the authored plan
with a concave waist and ease the floor derivative into the bottom tangent.
Compared with Memorial (neutral: bare gray deck at the upper left), our
coping looks chamfered and is cut into implausibly short blocks. Build the
63.5mm bullnose and curved nominal 600mm segments. The original close-up
looks from outside the pool and hides the tile: move inside above the lip.

The stair front post visibly ends below the sloped rail. Compute its actual
intersection with that rail, rather than using an independent height. The
ledge angle's horizontal leg oversails the concrete; turn it inward. Prefab
crossmembers emerge through the steep skin because a vertical offset loses
clearance on the steep part. Offset into the local surface normal, including
the curved stringers. Bottom runners must bear on the pad. The missing rear
fence endpoints and overly wide entry infills also need a measured closure.

The 2011 park has the right municipal program; the 2004 park is still too
similar from the same camera. The prefab construction reads 2000, but six
identical separated quarter units produce a catalog layout. Group end ramps
into practical shared runs, preserve roll-up distance, and vary one end.
Check all closures and circulation on actual imported surfaces next.

## Pass 2 — construction corrections, rejected bowl seam

Color/value first: the added east-side streets and houses replace the empty
green horizon in the eye-height image. Concrete still has deep shaded bowls
and a soft highlight roll-off; the cool shadow and dark foliage remain quick
material limitations. Every image in `renders/pass-2/` was opened at its native
1000px size. The site and prefab close-up improve, and the stair post now
visibly meets its rail. Imported paired rays independently confirm contact.

The apparent crack in the bowl is a real construction failure, not wear.
A nonperiodic waist function jumped 0.22mm at parameter zero; its finite
difference normal reversed and folded that section outward. Inspection also
found opposing normals on sector boundaries despite unit-length normals
passing the generic audit. Make the waist periodic, explicitly face the
ride surfaces upward, and carry analytic normals across sector boundaries.
Add independent orientation/seam checks so normalization cannot hide this.
The tile rows must use the local section angle at each point, rather than a
sector-center angle that produces a stepped band. The bullnose is rounder,
but that seam prevents acceptance of the close-up.

The prefab crossmember stripes are gone. Its riding sheets still ran over
the lip onto the deck as one impossible bent sheet. Separate the 4ft-wide
curved sheets from the deck, use a flush inclined 3mm toe plate, and add the
enclosure's actual side fasteners. Retain only visible slab skins beneath
poured construction; remove slab skin hidden by concrete obstacles.

The prefab now includes two opposed-quarter mini-ramp lanes; imported rays
sample all 82 points in those flat runs at grade. The municipal fence uses
whole 10ft bays with infills to the real gate posts; corners close on a single
post grid. The 2004 park remains intentionally smaller and simpler, but a
different ground camera will make that program clearer at the checkpoint.

## Pass 3 — continuous shading and a section failure

Color/value first: under the same side sun, the exported bowl's lit/shaded
halves are much more readable. Its previous black seam is reduced, but the
close-up still contains a pinched coping joint and the floor has radial
creases. All eleven `renders/pass-3/` images and three initial photo pairs
were opened. The prefab's uninterrupted curve, screw seats and separate toe
plate now read as assembled parts. The extreme uniformity is a finish issue.

The normal audit found Blender's join/triangulate re-encoding some authored
normals; carry explicit corner vectors through that operation and reseed
them afterward, as the kit does. More importantly, a few actual triangles
still turn downward. This is a geometry problem: the deep end's convex plan
radius is smaller than the circular transition's inward run. Broaden and
round both ends, reduce the second harmonic that sharpens them, and keep
the kidney indentation broad enough that all inward-offset contours stay
regular. Use an analytic rim tangent, avoiding nested finite differences of
single-precision vectors. Check actual imported winding as well as normals.

The three initial pair views are rejected. Alondra's guessed correspondences
fit a camera with an implausibly thin bowl; infer correspondences on the fixed
original rim and preserve a near-vertical photographic frame. Burnham's
wide crop conflates bank and stairs: focus the comparison on its sloped
armored ledge and our hubba, and retain the residual for their different forms.
Memorial's parameter order admits a camera outside the pool, showing the back
of the coping. Reverse that correspondence and add the visible outside deck
point so only the inside-facing tile view fits. Neutral balance is measured
on bare concrete, with exposure left unchanged. Unknown photographed sizes
limit these comparisons; they are not survey evidence.

## Pass 4 — first cold build; paving cut rejected

Color/value first: the broader bowl has a smooth, deep cavity and a clear
rounded lip. No folded triangles remain; the actual deep/shallow sections
fit 2.4384m circles and have 2.1336/1.2192m depths. Across 9,060 imported shared
corner comparisons the worst normal angle is .054°. The hero stays at 1.65m
with a 35mm lens, and includes the street section, trees, fence and town.
All eleven 1440px first-cold renders were opened.

The flatwork optimization exposes black holes under the stair approach and
behind the hubba: a whole-module bound contains projecting rail returns and
empty space around the concrete. Remove paving only under the authored
concrete contact rectangles, including the separate hubba and return bank.
Add actual downward ray checks on the two exposed approaches. This must
pass before the checkpoint is complete. No black gap is being relabeled as
shadow or future dirt.

Linked library meshes are retained after consolidation. A former per-instance
join needlessly duplicated the tree/fence meshes. The smaller geometry buffers
now preserve repeated geometry, while placed-triangle counts still include
every tree and section. This is a serialization/resource fix, separate from
the circle, normal, rail-contact and surface-ray construction checks.

## Pass 5 — paving accepted; transform and allocation corrections

Color/value first: all eleven current ground/above/detail views were opened.
The stair approach now reads as continuous concrete, with contact shadows
at the actual risers and no black void. The bowl has a clear lit floor and
deep shade. Its porcelain-blue band is still darker/cooler than the balanced
Memorial photo; this remains a quick-material mismatch for look-dev. The
overhead views clearly distinguish the open 2011 program from the smaller
2004 park and the dense prefab park.

The hubba armor and some framed supports are unnaturally black under an
otherwise readable sun. The preserved normals were in each primitive's local
frame, while join rebased vertices to the module owner. Transform those saved
vectors to the owner's frame before restoring them. A new imported check
compares large armor-face shading normals to their actual geometric normals.

One street-light instance also had more triangles than its identical neighbor:
joining into a shared mesh modified its sibling's input. Copy shared data
before any join, consolidate the source light once, then retain linked placed
meshes. Both poles now have 3,180 triangles. Replace the temporary 8,325-triangle
rules text with an original shared 1K print; the complete sign is 142 triangles.
No library delivery is edited. These allocations are visible in the measured
whole-site and unique-geometry counts, not just a claim of engine batching.

The three photo comparison recipes now use sensible feature crops and the
correct inside-facing coping. The bowl/hubba remain approximate original-form
comparisons (22.5/17.8 native-pixel RMS), and Memorial is 14.8px. In particular,
the Burnham hubba's surrounding bank differs from our stair landing; it must
not be described as a dimensionally exact replica. Reduce the comparison sky's
chroma and soften the Memorial sun to approximate its visible light. The final
material/age round must repeat these judgments with baked maps.

## Pass 6 — cold build accepted; comparison light rejected

Color/value first: the eleven cold-build views retain deep cavity and contact
shadows without white clipping. The whole-image hero's display-Y p5/p50/p95
are .0064/.6043/.7492; p99 is .8034. This includes sky, foliage and buildings,
so it proves display headroom, not correct concrete albedo. Uniform clean
concrete is still much flatter than the used Alondra photograph, and the
Memorial blue band is too dark. Those are disclosed finish differences at
this gate, not accepted final materials.

All eleven current images, three comparison renders/pairs and both sheets
were opened. The hubba's facing wall is in direct opposition to Burnham's
soft visible-face light. Memorial's interior wall also receives too little
light relative to its deck. Correct the estimated sun directions, soften the
Burnham source and increase its sky contribution before retaining these pairs.
Do not brighten the material to compensate for a shadow-side comparison.
The geometry, camera fits and exports remain frozen during this correction.

The cold `make WIDTH=1440 SAMPLES=32`, independent `make check` and isolated
`make repeat` all passed. Repeat compared 15 glTF/BIN/shared PNG files byte for
byte and verified that the original exports were untouched. The corrected
armor normals now agree with their geometric faces (minimum dot .99999994);
the stair approach rays hit continuous paving at grade. All 56 exported roots
also have two exact six-inch-grid reservation sockets enclosing their bounds.

Site limits remain visible: coarse and similar maple crowns, one repeated
house type, little age distinction between the two concrete parks, and
compressed wire spacing in the scaled short gate infills. The prefab program
clearly reads as a lower-cost earlier installation. The concrete programs
need the next stage's finish/repair language to separate their decades more
strongly. No claim of photorealism, final UV validation or bake quality is made.

## Pass 7 — retained form checkpoint

Color/value first: the revised Burnham light reveals the hubba's facing wall
instead of disguising it in blue shade. Its steel cap is still darker and more
uniform than the used photographic edge. Memorial now has readable interior
light, but the quick blue ceramic and gray wall still miss the photograph's
bright band and warm stained concrete. Alondra's clean surface lacks the
dark polished lip and mottled riding lanes. These differences are visible in
the retained pairs and belong to the expressly deferred material/age stage.

The final three 1440px Cycles comparison PNGs, their pairs, and regenerated
contact sheets were opened. The rounded coping projection and band, continuous
transition sections, inward ledge angles and supported rail all read clearly.
Our kidney has a broader waterfall/waist than Alondra. The hubba follows our
6in/12in stair line, not the photographed bank's slope, and its full-width
steel cap is an original construction choice. Approximate original-feature
fits remain 22.45 / 17.80 / 14.75 native pixels RMS; they do not certify a
replica, surveyed scale or lighting/albedo identity.

`make match` (1440px, 40 samples) and `python3 src/review.py` passed after the
focused lighting correction. The main cold-build views remain at 32 samples.
The comparison sheet now stacks each pair at its natural aspect ratio, avoiding
large empty fixed-height cells. No mesh, material or delivery byte changed
during this pass. All physical checks and the 15-file byte-repeat receipt
therefore remain applicable. Repository checks and whitespace checks pass.

Stop here, before look-dev. No kit or existing delivery changed. A useful
future kit improvement would add geometric-normal orientation and inter-piece
seam comparisons to the existing unit-normal checks; the local checks caught
failures that normalized vectors alone could not expose. Nothing is needed
from the lead to review this checkpoint.

## Pass 8 — site assembly error caught at native size

Color/value first: the quick finish and its previously documented color
mismatches are unchanged. Native-size ground views expose unsupported fabric
at the near fence corner and bare posts along the side. This is construction,
not a transparent-material or wear effect. The imported source roots use
quaternion mode, so assigning Euler yaw did nothing. Explicitly select Euler
mode before applying placement yaw. This also restores the intended bench,
tree and presentation-house orientations.

The new check reads actual imported fabric vertices and actual post-bottom
rings, rather than comparing declared rotation metadata. All 24 side bays on
101 and 20 each on 202/303 span 3.048m along Y; the maximum discrepancy between
fabric endpoints, their 34mm stand-off and supporting post axes is 2.915µm.
The previous crosswise bays fail this test. Triangle and material counts stay
unchanged; glTF byte sizes rise slightly because rotations are now serialized.

The final requirements audit also corrected the proof programs to explicitly
span three decades: Mill Creek 1999, Cedar Junction 2004 and Alder Glen 2011.
The form sign is regenerated once per fresh scene, so an old cached print
cannot retain its earlier 2000 date. No skating geometry changed. Re-render
the corrected sites and repeat the independent byte proof before stopping.

## Pass 9 — corrected site retained; stop before look-dev

Color/value first: the regenerated hero keeps a readable gray skating surface,
deep bowl shadow and unclipped highlights. Current whole-image display-Y
p5/p50/p95/p99 are .0039/.6004/.7405/.7822, with zero white clipping. These
are display diagnostics including context, not albedo validation. The clean
concrete, dark blue tile and uniform steel still differ visibly from the used
photographs; the finish gate remains necessary.

All eleven final main PNGs, all three final comparison PNGs, and both regenerated
sheets were opened. The stray corner fabric and bare side bays are gone.
Bench orientation, varied tree silhouettes and continuous context roads now
read correctly. The skating geometry and comparison-fit limitations remain
as recorded above. Coarse foliage, repeated housing, compressed short-infill
wire spacing and the weak age distinction between the two concrete parks
remain disclosed limits. These quick-material sites are not final assets.

The final `make WIDTH=1440 SAMPLES=32` passed the expanded fresh-import checks,
rendered all fourteen Cycles views from the external glTF deliveries and
regenerated both sheets. The final isolated `make repeat` again passed all
15 files byte for byte. Measured whole-site triangles remain 265,018 / 252,900 /
253,592; skating triangles remain 44,236 / 42,154 / 42,438. The sign and updated
node transforms are included in the final delivery receipts. No further form,
look-dev, baking or final-atlas work is performed in this checkpoint.

## Follow-up pass 10 — first baked GLB views, rejected

Color/value first: `renders/look-1/` was opened at its native 1000px width
(all eleven views). Concrete is too uniformly cool under the saturated sky;
the bowl has almost no service history away from its drain. Burnished quarter
lanes are black cutouts, unlike the broad gray pumping wear in the Alondra
and sunny Venice photographs. The drain deposit reads as rounded mud islands.
These are failures, not an accepted wear treatment. The newer and middle-aged
parks do not yet differ enough at full frame. Prefab composite is distinct but
its galvanized plates look excessively rippled.

The connected transition decks, graded connection, elevated street plaza,
cheeks and concrete-topped armored hubba now read as construction. Both bowl
plans have real pockets; the clover has three lobes and the kidney a waist.
Coping ends are radial planes and the lawn meets concrete mow strips. The
canonical maple/oak leaf masks remove the opaque-square foliage fault.

Diagnosis: the generic solid mesh helper recalculated the winding of open
curved wear skins while their authored shading normals stayed upward. Raw
exported triangle/normal dots reached -0.99986. Open skins now preserve their
authored winding; a separate exported audit requires agreement on every wear
primitive. Wear albedo is raised toward concrete, cutout coverage is stippled
at texel scale, sky chroma is reduced, and bowl pumping/contact wear is driven
by physical surface chainage and distance below the lip. The sediment will
use fine grit coverage instead of contiguous round blobs. The trim normal
strength is reduced to stop flat gauge steel reading as crumpled foil.

The first byte audit also found an unnecessary ORM copy caused by constant
wax roughness. Wax now uses a roughness factor on the shared ORM. This is
checked on embedded exported images, not assumed from the source allocation.

## Follow-up pass 11 — corrected shading, photo comparisons still reject finish

Color/value first: all eleven `renders/look-2/` views and the three native
`renders/matches-2/*-pair.jpg` canvases were opened. The black curved-skin
fault is gone. The common sunlit exported concrete probes measured .568 / .572 /
.572 display Y, with actual concrete hits and clear sun/camera rays. The
balanced sunny Venice deck measures about .797 / .777 / .859 in three verified
sunlit rectangles. Two initial photo rectangles accidentally sampled shaded
walls; they were rejected and relocated on the annotated photograph. These
are exposed image comparisons, not a reflectance measurement or a claim that
unknown photographic exposure has been recovered. Ground's accepted concrete
pixels stay unchanged. The studio camera exposure is being calibrated upward;
normal strength and local, darker use masks remain material decisions.

The corrected gray quarter lanes are still too regular: repeated pairs look
painted. Vary their count, spacing, path and taper, lighten the new park's
contact material, and retain stronger wear in the middle-aged park. The bowl
pumping paths need more value separation to survive a full-frame hero. The
sediment remains blotchy in this pass because the revised grit mask had not
yet been regenerated/baked. The next bake replaces it. Native plate detail is
less rippled; the lifted fixing needs a dedicated toe-plate close-up.

The pairs now compare a kidney with a kidney and six concrete hubba corners
with the same six corners. Fit RMS is 11.11px at 866px photo width (kidney
contour), 1.84px at 400px (hubba), and 6.78px at 580px (coping). The contour
phases and coping scale remain inferred; the kidney's approximately 9.4-degree
fitted roll makes it weaker than the rigid hubba fit. This is disclosed rather
than calling the fit surveyed. The source full-frame equivalent is 27mm for
Alondra and about 48.6mm for Burnham. The 372.9mm number is the narrow crop's
projection lens, not the camera's taking lens; the new pair captions say both.

The coping looks too clean beside Memorial's dark ground-in nose. Its UVs
will follow tangent chainage and actual radial profile width, putting wax on
the nose and top contact zone instead of an arbitrary projected face edge.
Increase stained/chipped contrast and salts on the tile. The original section,
block end planes and triangle budget remain unchanged. The newer park should
retain less damage than the two older installations; matching a different
park's entire material color/age is not claimed.

## Follow-up pass 12 — value control passes; close-up and spacing corrections

Color/value first: all 22 `renders/look-3/` views, all three `matches-3`
pairs and the three `values-3` images were opened at native size. Verified
sunlit concrete now measures .759 / .760 / .761 display Y against the balanced
photo's .794 / .776 / .859. It remains .015 below the darkest photo sample.
The unchanged Ground albedo is not relabeled as a measured reflectance: this
corrects the studio exposure. The reference neutral is explicitly the sunlit
unpainted concrete deck/coping; photographic processing remains unknown.

The same views reject two finer tells. The large pumping mask has an angular
join at the chainage wrap; it now uses continuous surface position for its
phase, while retaining actual section arc height. The grit is finer but too
round. Its actual-floor triangle footprint is now an upstream fan tapering
toward the grate, and the leaves favor that arrival side. The zinc toe plate
still looks rippled at close range. Its final source uses finer grain, higher
roughness and micron-scale relief rather than sharing the coping chip height.
A dedicated opposite-light coping view will show the bare contact crown.

Missing tile assignments are now explicit and sparse, rather than trusting
object-name hashing to land on the damaged atlas cells visible to a camera.
The planter has four real walls and a recessed soil opening. A misplaced
native plaque with no material and the rules print's mismatched UV-layer name
were also found by export audits and corrected locally.

Fresh-import section/contact checks pass. The expanded raw audit passes with
UV area, density, normal-map tangent frames, trim image reuse, six alpha-cut
trees with `_WIND`, and zero bowl plan overlaps above tolerance. Normal-mapped
exporter zero tangents are repaired from incident UV triangles; valid frames,
positions, UVs and every canonical delivery file remain unchanged. The pin
oak canonical GLB itself contains eleven zero tangent vertices; re-import/
export introduces one on maple. The new park copies also have small bevel-fan
cases. These are serialized-frame corrections, not geometry detail.

The output spacing audit, rather than the planned centers, found 7.95–8.09m
from the large park's north toes to its bowl. Advance that row 2.4384m, retain
and extend its continuous rear deck, and tighten the two street connections.
The rebuilt actual gaps are 5.51–5.65m and 4.21 / 4.57m. Compact poured gaps
are 1.78–4.57m; prefab north quarter to funbox is 5.30m. Published drawing reads
span 2.04–6.83m, with ±.4m reading uncertainty. Major-feature envelopes and
all raised terrain are reported separately: broad shared circulation decks
must not be silently counted as obstacle envelopes. The prefab slab's flat
underside was erroneously counted in an initial mask and is now excluded.

The kidney fit is now upright, at the EXIF-informed 27mm equivalent. Its
28.33px / 866px outline RMS (maximum 69.17px) is weaker than the rolled fit,
but defensible as a different original kidney's contour comparator. It does
not prove dimensional identity. The rigid hubba remains 1.84px / 400px; coping
is 6.78px / 580px with inferred lip scale. This limitation stays on the pairs
and in the final report.

## Follow-up pass 13 — full-size form evidence and remaining look gap

Color/value first: all 24 final `renders/lookdev/` PNGs, three native photo
pairs and their three landmark overlays, both contact sheets, and all 17
before/after canvases were opened. Each before/after canvas retains two native
1000px panels. Whole-image hero display-Y p5/p50/p95 is .032/.755/.900 for
2011, .022/.477/.892 for 2004 and .012/.524/.688 for 1999; white clipping is
zero in each. These include sky and context and do not measure concrete albedo.
The sunlit concrete control remains approximately .76 against the balanced
photo's .776–.859. The neutral remains the unpainted sunlit concrete coping/deck.

The comparison still rejects a photographic finish. Burnham's concrete has
stronger irregular streaks below its armor; Memorial's nose carries more
ground-in dark wax, and Alondra has much broader pumping abrasion. The rendered
concrete is more uniform and its curved wear paths still repeat too neatly.
The prefab's lighter riding paths, dark painted frame and bare plate make its
hard use clear at full frame. The 2004/2011 difference is subtler than intended,
particularly on their street terraces. These remain explicit checkpoint
weaknesses; no README gallery or docs images are promoted from these renders.

The overhead plans show distinct kidney pockets/waist and three clover lobes.
The shared transition decks, closed wing returns, elevated street landings,
stair cheek and concrete-topped hubba now read as connected construction.
Radial coping caps no longer shear diagonally. Native-size review found four
tiny rectangle-corner holes around each bowl deck: exact corner infills replace
the chords, and fresh-import downward probes hit actual concrete at all eight
locations. The refined zinc plate is satin instead of crumpled; fine leaf and
grit silhouettes remain economical. Native alpha-cut maple/oak foliage removes
the opaque squares. Flat lawn, constant-color fixture finishes and repeated
housing still reveal the procedural presentation context.

The first full byte repeat exposed one stale unused ORM image and MikkTSpace's
four-decimal rounding boundary at one oak trunk corner. Generated images with
no current glTF reference are now removed. The kit's guarded tangent stabilizer
sets that single corner after checking exact position, normal and UV signatures
and a maximum one-rounding-step change. The companion external BIN uses the
same guards. Every other valid tangent, every position/normal/UV and all image
pixels remain unchanged; canonical tree delivery bytes are never edited.

Final receipts: fresh `make check` passes; `make repeat` compares all 40 files
byte for byte successfully, with shared read-only baked/context inputs. All
24 main and three matched render source hashes equal the final GLBs. The two
reframed details were reopened: the wider end view exposes the actual wing
bank, and corresponding old/new stair roots are isolated in the calibrated
hubba pose. The old stair moves in the revised layout, so its narrow archived
crop is truncated; the wide stair pair remains the complete form comparison.
All 17 pairs pass projection/light/hash checks without altering placements.
All three final value-control images were opened. Actual clear-ray concrete
probes are .759384 / .760218 / .760501 display Y; balanced photo patches are
.793573 / .775668 / .859118. No kit files, README gallery or docs images changed.
