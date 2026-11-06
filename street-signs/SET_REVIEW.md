# Additional sign set — form checkpoint review

The approved STOP/blade assembly and its final images/maps are untouched.
This log concerns `src/set_*` and `export/set/` only. Refer to the independent
StreetFurniture checkpoint contact sheet for the rendered sign lineup/details.

## Pass 1 — manual sheets and imported face

Opened the imported 30 × 36 in R2-1 close-up plus the SHS R1-2, W1-2, W3-1,
W11-2, S1-1 and R10-11 pages. Checked color/value before geometry: the
software Workbench preview is too dark for calibrated sheeting judgments,
but its black/white separation exposes the legend and border clearly.

The original DejaVu bold substitute was too heavy. Switched to installed
DejaVu Sans Condensed / Book, fitting cap height and line widths to the
published Series C/D/E values. This is still an open-font approximation;
individual Highway Gothic outlines are not claimed. The old assembly keeps
its original bold font and bytes.

Corrected YIELD from a wide word to the published 9.063 in word width and
3 in caps at 36 in, with a white outer margin and red band. Corrected
R10-11 to NO / TURN / ON RED and a plain red signal disc; the initial two-line
version was wrong for that designation. W1-2 now curves toward an oblique
arrowhead rather than ending vertically. Diamond border calculations now
use side length rather than treating the diagonal envelope as its side.

The imported R2-1 face shows its two carriage heads, real drilled .080 in
blank and slim edge. The tiny dark mark between LIMIT and the numerals
is an unused center post perforation visible through a clear area behind
the sheet, not standard sign artwork; investigate its depth in the next
Cycles pass. Rear date/stencil sheets had the same mixed-UV-name fault as
furniture graphics; unify their UV layer before joining.

Posts are hollow round, rolled U or telescoping square with sleeve and pin.
The post perforations are flat indications at this checkpoint, explicitly
not physical open bores. Blank bolt punches are real cuts. Their finished
normal representation and prismatic versus bead sheeting are look-dev work.
No unrelated warnings/regulations are stacked: only a school speed assembly
and the matching crossing arrow assemblies share supports.

## Pass 2 — Cycles faces, supports and independent lineups

Opened face/back/base and both lineups in the second software review, then
the Cycles R2-1 face and revised regulatory lineup. Regular open-font strokes
now fit the published line dimensions plausibly. SCHOOL is FYG; speed/time
remain white. R10-11 uses the correct disc and three-line legend.

The dark center dot was a modeling bug: assigning cutter Z overwrote its
relative height, putting both punches at mid-sheet. Corrected the transform
and independently measured bore vertices/radial errors and actual sheet
gauge. Bolts occupy the two physical cuts. Rear labels read from the back;
shanks/nuts now span the actual support depth. Supplier data also exposed
too-narrow U-channel. Corrected it to 3-1/8 in and sized its authored wall
outline from measured polygon area and stated steel density. The 25 mph
support has a physical 3° impact bend; sleeve/pin and hollow walls remain.

Added a related two-blank local parking assembly with time/day plate, explicitly
an agency R7 adaptation without an invented federal designation. The standard
integral-time R7-2 remains. All 28 face charts fit the one 2048 sheet.
Pictograms remain less exact than the dimensioned text and blanks; disclose
that limit instead of treating recognizable figures as exact SHS symbols.

## Pass 3 — complete export lineups and construction details

Opened both complete Cycles lineups, face/back/base and the furniture street
hero. Color/value first: white is neutral under the warm daylight rather than
blue, red/yellow/FYG separate, and the backs retain a dark underside. The
quick shader does not yet prove either bead or prismatic retroreflection;
the two sheet grades remain seeded metadata until look-dev. The face sheet's
single mip allocation is shared across every added sign.

The 30 × 36 face has the corrected published line dimensions, an actual edge,
two punched holes and two heads. The date/agency label reads from the back.
The sleeve and cross-pin show the telescoping construction. Corners and thin
edges are slightly faceted in a very close view, within the small-prop budget;
the final normal must not turn their edge into a thick plastic rim. The
open-font S/E/R and pedestrian/school outlines remain visibly different from
SHS, despite correct cap heights/line widths. They are approximations awaiting
owner form review, not certified sign artwork.

Found and corrected a false bent-state claim during the coordinate audit.
Joining retained a fastener's origin, so the first bend affected no relevant
vertices. Bend in the root frame instead. An independent regression fit to
the imported exposed-post perforations now measures **2.9996°**; an unbent
export would fail this check. The damaged sign's lowest edge therefore dips
slightly below the nominal seven-foot undamaged mounting height. This is
intentional damage, not an approved mounting example. No other delivery was
rebuilt or modified.

Final bracket close-up exposed chord boxes disappearing into the host; replaced
them with continuous closed 19 × 1 mm bands. Opened the corrected close-up and
all final sign views again. The bracket is 712 triangles; the full addition
16,116. Repeat export is byte-identical and fresh-import budgets/normals,
image sharing and the bent-post regression pass. The earlier finished STOP
and blades retain every baseline delivery hash. Final sheet response, detailed
symbol refinement, wear and final UV/bake gates remain for after this review.

## Finish pass 1 — symbol book and sheeting values

Color and value first: the checkpoint white/red/yellow/FYG colors separate,
but one uniform shader makes the back, galvanized post and sheeting look
like the same paint. Added separate stock-glTF sheeting and metal states,
sharing the same 2048 image. Engineering-grade is satin, prismatic smoother;
true headlight retroreflection requires an engine shader and is not claimed.
Edge road film, upper exposure fading and short bolt tracks are located by
the face's construction; printed black stays dark.

Opened SHS Appendix 6-10 and 6-58 and the original generated figures side by
side at 1600 px. Replaced the generic stick-person routine with hand-entered
grid primitives and sampled cubic torso curves. The pedestrian retains the
bent far arm, forward arm, curved trunk and distinct stride. School now has
the child on the left, adult on the right, skirt, satchels and open elbow
gaps. No PDF path/raster is imported or traced. Comparison JPGs live under
root build/. Remaining CG tells: open-font letter outlines differ from the
federal alphabet; plain PBR cannot reproduce a headlamp's retroreflective
return. Source artwork is sharper than the shared delivery cells and still
needs an imported warning-lineup check.

## Finish pass 2 — exported face and full warning lineup

Color and value first: opened `renders/look1/sign-face.png` and
`signs-warning.png` at native 1440 px, plus the street hero. White sheeting is
neutral, black legend stays dark, and yellow/FYG are distinct under the raking
sun. The daylight dielectric sheen differs from the plain metallic support.
The source sheet's mild upper fade and edge film retain their underlying color;
exact color agreement must still be measured under each photo's own light.

The complete warning lineup now shows the SHS-style pedestrian stride and
child-left/adult-right school group. The former approximate stick figures are
gone. Both figures retain their book proportions at the delivered cell size.
The speed face exposes the accepted open-font substitution and mildly faceted
blank corners at extreme close range. These small repeated signs retain their
accepted triangle budgets. They are not regulatory-fabrication artwork.

Rejected the first extended street setting because a presentation lawn plane
covered the road. Its fix belongs only to furniture's presentation script.
The used R2-1 comparison uses an overcast photograph, so its own render gets
soft sky rather than the hero's directional sun; sunny shelter/meter pairs
retain their directional light. Neutral paving controls and fit residuals are
recorded separately from any albedo claim. Remaining CG tells: standard PBR
cannot return headlight retroreflection, and tiny post perforations are flat
color indications. No accepted STOP/blade byte changed.


## Finish pass 3 — final sun, shaded comparison and delivery

Color and value first: opened the complete 1600 px warning/regulatory lineups,
face/back/base/band details and town hero from the shared exported delivery.
Printed black remains dark under sun because the reused sheet alpha supplies
stock-glTF specular strength; it adds no image. White, yellow and FYG remain
distinct. The neutral-balanced shaded R2-1 pair now measures white sheeting
at 0.434 display luminance against 0.436 in the photograph; this is not an
albedo measurement. Sunlight and shade have separate procedural lighting.
Bare concrete is the photo's balance control. Its first sky-contaminated ROI
was rejected; the final control coordinates and gains are retained.

Checked pedestrian/school figures beside the actual SHS appendix grid sheets
and again at delivered chart size. The stride, arm gap and curved torso read;
the school child-left/adult-right, skirt and satchels remain distinct. Local
book comparisons are `../build/pedestrian-symbol-pair.jpg` and
`../build/school-symbol-pair.jpg`. The figures use independently authored
primitives; no book pixels or paths become texture artwork.

Every assembly remains within 1,500 triangles, with two shipped states (one
for the standalone band), one canonical 2048 sheet and no per-instance image.
The tables in README now report actual glTF/BIN bytes as well as triangles.
No accepted STOP/blade image, export or texture was changed. All final images
and their hashes are under `../street-furniture/renders/`; the final contact
includes the Eevee shot and four matched-light pairs. Docs are generated only
after this full-size audit and committed in their own final commit.

What still reads as CG: DejaVu glyph outlines remain an accepted substitute;
the shared cells soften minute sheeting/soil detail; small support holes are
flat indications and blank corners can facet at macro distance. Standard PBR
shows daylight sheen, not true headlamp retroreflection. The photograph's
graffiti is not reproduced. The town's repeating context remains apparent.
