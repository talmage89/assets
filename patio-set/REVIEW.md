# Visual and construction review — Larkspur / Terrace

References are the original product photographs embedded in General Products
and Hanover catalogs and California Umbrella's Sunset sheet. Source pixels are
inspection aids only. `make match` uses the original 252 × 268 Hanover dining
chair photograph extracted without a rescale; the lens is estimated. The
10-landmark fit has 14.19 px RMS, with independent Blender projection agreement
of 0.00011 px. That is a coarse product-photo comparison with real differences
in the original frame design, not evidence of photographic identity.

## Pass 1 — source geometry and look-dev

Inspected every image in `renders/clay/` and `renders/pass1/`: assembled set,
chair, chaise hinge, canopy and furled variant. Compared the chair frame and
sling to `refs/foxhill-photo-000.jpg`, the chaise to the original photographed
chaise in `refs/chaise-reference.jpg`, the slat layout/connections to the table
photos on Hanover p2, and canopy/runner/crank construction to the Sunset sheet.

CG tells: angular arm corners; plain fabric reading like vinyl; a small chair
seat bolt floating off the frame; rib chords leaving gaps under curved cloth;
a weak front hem on the chaise; a shaft without a modeled bottom stop in the
base; very regular closed-canopy folds. The studio controls crop also cuts the
front feet, so it must remain a detail shot rather than scale evidence.

Corrections: quadratic corner rounding along the bent arms; stronger paired
warp/weft and yarn normal relief; welded seat mounting bosses with bolts seated
on the legs; six-station ribs matching the canopy; sewn spline pockets and end
plugs on the chaise; captive socket bottom stops; measured ground-footprint
recentering. Oriented the cloth shell normals upward before solidification.
The repeated chair remains 1,648 triangles. The chaise was 2,008 triangles before the final mechanical correction;
small handwheels retain a round silhouette without overspending the family.

The closed shell intentionally keeps eight regular analytic folds. Its tie,
buckle, loose tails and exposed rib tips establish the furled state, but the
fold symmetry remains a limitation. No cloth simulation was used.

## Pass 2 — calibrated source and shipped atlas

Inspected `renders/pass2/sling_chair-pair.jpg` against the original photograph.
The bent arm transitions are smoother and the floating front bolt is corrected.
The authored narrower spline/fabric design, lighter sun-faded finish, round
rather than rectangular tubing and opaque fabric remain visible differences.
Fine weave is stronger in the source hinge detail than in the overall chair;
the final atlas must be judged at normal scene distances.

The full handwheel sweep exposed 8.41 mm interference with the long chassis
and 7.00 mm with a support bracket. Corrected the physical layout rather than
allowing those collisions: dropped the chassis under the hinge, made the
support cheek thin, bored both hinge members and connected each handwheel with
a captive shaft. Added two contact checks. The final chaise has 2,464 triangles.
All five motions now pass 158 samples on both source and game meshes, with no
unallowed penetration above the 0.5 mm tolerance.

A broader assembly inspection also found the lower table guide too close to
the umbrella base sleeve, and foot caps that did not sufficiently overlap their
leg ends. Enlarged the lower guide bore from 56 to 76 mm and deepened all
furniture foot boots to 26 mm. Brought the handwheel clamp faces onto the fixed
cheeks. Added explicit foot/clamp contacts and whole-table versus whole-umbrella
surface checks in both source/game and in the arranged GLB. These are physical
checks, not comparisons against an exported constant.

The first complete shipped review exposed black streaks on the tied canopy.
BaseColor coverage was intact, but 6.25% of sampled tied-umbrella texels had
normals facing into the low surface; 4.08% had nearly black AO. The high fold
shell had twice the angular sampling of the game shell, and the 1.8 mm cage
could start inside it. Matched that source fold shell to the game tessellation
and widened the bake cage to 3.5 mm with 14 mm ray distance. Added an independent
GLB texture probe for uncovered BaseColor and grossly inverted umbrella normals.
The probe samples UV-face interiors (faces ≥4 texel²), not unused atlas pixels.

The repaired exported tied view has no black streaks. Reopened all eleven
Cycles renders, the Eevee hero, source/GLB photo pairs and the contact sheet.
The new probe measures tied-umbrella inward-normal samples at 0.40% (from 6.25%)
and open umbrella at 0.91% (from 5.73%); BaseColor has no missed interior samples.
The check is deliberately a coarse fault detector, not proof that every normal
texel is correct.

The exported chair still has slight triangular shading at the upper sling
corners and softer seams than the source. Hinge/index recesses blur and frame
cross-sections facet in close-up. The 2048 atlas retains a hint of the coarse
basket weave; fine yarn averages away. The opaque fabric and very regular tied
folds are the largest remaining photographic differences. Powder coat reads
lighter and smoother than the darker reference chair. Those limitations remain
visible in the committed details; the assembly reads consistently at ordinary
backyard scene distances.

Final default measurements: library 13,620 triangles, one material, three
2048² maps, GLB 7,766,900 bytes; arranged four-chair set 14,848 drawn triangles
and one shared chair mesh, GLB 7,615,352 bytes. Atlas 48.52%, density p5/median/p95
223/287/340 px/m, no measured overlaps/outside/degenerate UVs. All nineteen
source/game contacts, ground/origin checks, conservative 6.73 mm table-hole
clearance, full table/umbrella assembly checks, sampled motion and fresh GLB
verification pass.

`make` completes the GPU bake, both GLBs, eleven imported-GLB Cycles views,
Eevee, three JPG docs, calibrated source/shipped photo pairs and all checks.
The new shared-family declaration and optional linked studio instances are the
only kit changes; both preserve single-asset defaults. Nothing is required
from the lead. A future generic kit warning for large inverted-normal regions
would catch this class of thin-shell bake fault earlier.

## Owner refinement — sewn canopy and visible default weathering

The accepted family was too smooth and clean at patio viewing distance. The
revision-source hero/canopy/furled/chair renders have been opened and compared
with the installed garden umbrella and used cafe set, not just the original
catalog photograph. Hem scallops now change the silhouette at player height;
16 mm rib pockets and bound hem interrupt the smooth cone. The vent has a 23 mm
valance with a physical gap below. Closed cloth keeps stitched seams and the
scalloped gathered hem. The 2048 family atlas and opaque sling are retained.

Default weathering has been strengthened inside physical masks: direct sun and
upward exposure against shaded cloth, fold ridges against valleys and protected
tie band, top-only coat chalk, foot-height scrapes, mineral rings on upward
faces, and corner/ground deposits. Source preview shows cream/sage exposed cloth
against darker green backs and furled valleys; coat tops are noticeably lighter
than vertical uprights. Water rings remain subtle individual deposits.

The installed-set camera fit has 4.85 px RMS at the 1600 px photographic width,
using four table face/foot anchors. Exact reference dimensions and lens are
unknown; the resulting estimate is a framing aid, not a measured product match.
The reference umbrella sits behind/right of its table, so only this comparison
poses our pole there. The ordinary delivered dining arrangement stays centered.

The exported comparison exposed black triangular hem regions. Fixed the high
binding orientation and made source/game saddle triangulation identical. Replaced
high-only pocket strips with closed sewn tunnels; actual tunnel/cloth and
rib/tunnel surface contacts pass. Open/closed umbrellas remain 3,920/3,908
triangles. The weather regression measures broad cloth faces, with a 50% exposed
versus protected contrast floor at default wear (rather than counting the shaded
rib tunnels as exposed canopy).

One remaining black underside patch was traced by a camera ray to a canopy face
with BaseColor (72,101,71), tangent Normal (127,127,255), ORM (255,199,0): no
texture defect at that point. The old 1.65 m studio reflection flag intersected
the moved comparison umbrella. Merged main's canonical STUDIO.scale feature and
set scale=2 so the flags clear the full family; kept both tile and explicit
family-atlas behaviors while resolving the bake merge. No duplicate studio
feature was added. Main's atlas and composed export-policy fixtures both pass.

The corrected GLB used-set pair has been opened: no black underside patch or
black hem remains. The comparison reveals a believable eight-panel silhouette,
bound rib tunnels, vent gap and darker shaded underside. Relative to the used
photograph, our original canopy is shorter and rounder, and the original sage
fabric is more cream on sun-facing faces; those are documented design choices.
The exact age of the photographed installed cafe set is unknown. Individual
stitched thread and water rings are restrained by atlas resolution. Main's bake
coverage check reports zero missed BaseColor projections across 5,417,521
interior texels. Broad canopy/sling delivered color ratios are 1.59/1.72;
powder top/vertical ratio is 2.50. The physical checks measure 75 mm hem sag,
35–49 mm vent gap, twenty contacts and unchanged 6.73 mm pole clearance.

The revised final documentation was rendered once after these fixes. Opened
all eleven delivered Cycles shots, Eevee, the contact sheet and both source
photo pairs. No canopy projection defects remain. The three committed JPGs
are 86,097 / 107,156 / 85,714 bytes. The normal-map weave and source scuffs lose
some contrast at atlas resolution; very regular furled folds and faceted small
frame sections remain the weakest close-view details. Neither changes the
accepted opaque-sling design.

`make check` passes: topology/budgets, scale, UVs (38.17%, no overlap/outside/
degenerate triangles), independent twenty contacts/ground/pole checks, source
and game motion sweeps, actual four-chair GLB instancing, fresh re-import and
repository rules. Library: 14,004 triangles, one material, three shared 2048
maps, 9,143,676 bytes. Arranged set: 15,040 drawn triangles, 8,945,004 bytes.
The final default build also regenerates the source and shipped comparisons;
its review stamp is kept separate from the one final documentation render.
