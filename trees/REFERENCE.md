# Red maple / Acer rubrum / summer front-yard specimen

Absolute target dimensions and the approximate 20-year age come from the brief.
Age cannot be inferred reliably from height or DBH alone. This is an original
seeded specimen, not a recreation of either photographed individual or a named
commercial cultivar. All source/credit URLs are in [refs/SOURCES.md](refs/SOURCES.md).

## Species evidence and authored choices

| Feature | Evidence | Modeling interpretation |
| --- | --- | --- |
| Form | Oregon State: ascending branches and irregular ovoid/rounded crown; UConn: elliptical young trees spread with age | Round-3 decurrent specimen: four co-dominants start at 2.19–2.73 m, 23 scaffolds and three secondary limbs per mass |
| Crown density | UF/IFAS: moderate density, irregular outline | 23 scaffold-supported masses with six smaller subclumps each, overlapping cores and a thinner distal-interior population |
| Branch attachment | UF/IFAS describes upright branches with potentially weak unions; recommends wider angles and subordinate branches | Four co-dominants following the lead’s open-grown/decurrent brief; leaf-load pipe profiles and fused coarse collars. Numerical angles remain authored controls, not a published species-wide invariant |
| Leaf arrangement | Oregon State: opposite, simple; most leaves three lobes, sometimes five | Opposite pairs on original three-axis 24–30-leaf branchlet sprites |
| Leaf size | Oregon State: typically 5–10 cm; UConn 2–4 in | Original 6.6–9.4 cm blades, with 0.94–1.05 card scale variation |
| Leaf color | Oregon State: medium/dark green upper, silver lower | Original lobed/serrated blades, palmate ribs, gray-green backs, red petioles/shoots and thin-leaf diffuse transmission |
| Bark | UConn: smooth ash/silver gray young bark, scaly gray-brown older wood | Procedural gray-brown lower-bole fissures and shallow flakes, fading to smoother younger limbs |
| Base | UF/IFAS and Oregon State describe surface roots | Modest trunk swelling into five low buttress roots; retained roots sink into grade within about 0.4 m |

## Photograph interpretation

`psu-form.jpg`: full-leaf spreading summer specimen, Jodi Sulpizio / Penn State
Extension. Its low outer foliage and open divided interior inform the lower
branch masses. It is distinctly broader relative to height than our target.

`osu-form.jpg`: Oregon State's side-by-side spring/summer habit image; only the
right, fully foliated half is calibrated for the summer comparison. Its upright
oval habit is closer to the brief. The left half is a supplemental leaf-off
branching reference, not a second summer photo.

The trees are plausibly in the same landscape size class using visible context,
but neither photograph includes a height survey or verified age. There is no
claim that either is exactly 12 m tall or 20 years old. The brief supplies 11–13 m
height and 30–40 cm DBH. The finishing brief supersedes the wider round-3
checkpoint: the retained crown is now 9.8 m wide, inside the original range.

`osu-branch.jpg` and `osu-shoot.jpg` provide supplemental branch and opposite-leaf
comparison. `ifas-form.webp` was rejected for summer comparison after opening:
it shows autumn color. It is retained locally and cited transparently.

Camera fits use anatomical landmarks, estimated focal length, an eye-height
prior and downweighted lateral anchors because these are different living
individuals. All residuals remain in the pair captions/calibration JSON. They
are composition aids, not surveyed reconstruction or proof of shape agreement.
No photographic pixels enter Blender, the leaf atlas, or committed docs.

## Round-2 measured crown evidence (historical)

Original image coordinates and uncertainty are tracked in
`src/reference_measurements.py`; labeled image overlays are rebuilt into
`renders/round2-measurements/`. Penn State: crown box (126,32)–(817,582), grade
y=659; **691/550 = 1.256** crown width/height, **12.3%** image-height base. Oregon
State summer half: (748,24)–(1414,718), grade y=841; **666/694 = 0.960**, **15.1%**
base. Bounds describe the continuous leafy mass, not a few isolated tips.

The generated tree's retained-alpha 3D crown measures **9.429 × 10.234 m**
in X/height, ratio **0.921**, starting at **2.120 m**. In the two photo cameras,
its projected image ratios are **0.973 / 0.972**. Those are separately measured
quantities; 3D and projected ratios are not interchangeable. The broader Penn
State crown remains a mismatch. The 9–10 m width, 12.4 m height and 2–2.5 m lawn
clearance from the brief favor the Oregon State oval rather than the wider
Penn State individual. This tradeoff is exposed in the measured pair captions.

## Structure round 3: branch masses and widest-band height

The lead's round-3 interpretation is now the growth target: a lower-heavy,
asymmetric crown built from individual scaffold ends; 1–3 m foliage masses,
smaller tufts, upper notches, a drooping drip line and clear walking space at the
bole. The photograph measurements are comparison evidence, never tracing input.

The same crown/grade landmarks remain. Added manually inspected broad widest
bands: **Penn State y=442 ±30 px**, **OSU y=465 ±30 px** in the upright originals.
They lie **25.5% / 36.5% above their respective crown bases**. On an illustrative
12.4 m whole-tree normalization they are **4.29 / 5.71 m above grade**. These are
not surveyed real-tree heights. Ref crown W/H remains **1.256 / 0.960**.
Annotations are rebuilt at `renders/round3-measurements/`.

For the model, a green/alpha crown mask measures projected W/H and row spans;
1st–99th percentile spans are smoothed over 3% of crown image height to reject
one stray blade. The widest band is compared as both fraction of crown height
above its base and 12.4 m normalized image height. A separate retained-alpha
support calculation measures physical source leaf bounds. Those scopes are
reported separately. The camera fits stay the same across rounds, despite
being approximate fits between different living individuals.

The round-3 checkpoint reached 10.7 m retained width while pursuing its broader
W/H target. The finishing brief explicitly asks for about 10 m again: the final
retained width is 9.801 m, with more overlap through the waist and fuller upper
sides. That newer width instruction takes precedence over the earlier 1.0–1.15
ratio target. Current physical and photographic measurements are reported
separately rather than retaining a superseded dimensional claim.

The final round-3 comparisons use `build/framed-cameras.json`: unchanged crop
pixels with neutral side margins, the same camera pose/roll and vertical FOV,
and an expanded horizontal field. The independent kit projection check is
within 0.001 px. This corrects clipping in the old OSU comparison, rather than
scaling or distorting the tree to fit the crop. Original solve residuals remain
in the captions. Current source measurements and pair metrics are in README.


## Final surface reference and color policy

The Penn State summer photograph is the color/value reference. The Oregon State
habit slide has a dark/blue shift identified by the lead and is used only for
form. `osu-shoot.jpg` supplies visual leaf/vein/petiole comparison; original
mathematical outlines are never traced from it. Supplemental `osu-trunk.jpg`
and `osu-bark.jpg` show flare, shallow plates and young/old bark transitions.
Their author/rights and direct image URLs are in the reference register.

The final flare is measured from closed mesh/plane section loops at .01, .05,
.25, .50, .70 and 1.35 m. The near-grade section's .620 m area-equivalent
diameter is 1.72× the independently fitted .361 m DBH. The final shader uses
age-dependent longitudinal fissures and shallow flakes, rain-darkened tracks
and sparse sheltered lichen. No reference texels are sampled.
