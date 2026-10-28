# Meridian Six form reference

An original medium-frame stainless six-shot .357 service revolver, with a
101.6 mm / four-inch barrel and full ejector shroud. Fictional maker/model:
**Propane Defense Meridian Six**. None of the real products' markings or logos
are reproduced. Every mesh is scripted; photographs only enter comparison tools.

Published class anchors are the manufacturer's [GP100 catalog](https://ruger-docs.s3.amazonaws.com/Ruger_Firearms.pdf),
pp51–52 (six rounds, 106.7 mm barrel, 241.3 mm overall, 1,134 g unloaded), and
the U.S. government's [686 test report](https://ojp.gov/pdffiles1/Digitization/105573NCJRS.pdf),
Appendix C p74 (six-shot DA/SA, four-inch barrel, stainless, 40.6 oz / 1,151 g).
These bound an original 240 mm design; its nominal unloaded mass is 1.13 kg,
metadata rather than a claim of weighing the visual mesh. Manufacturer
[nomenclature and six-shot parts illustrations](https://ruger-docs.s3.amazonaws.com/_manuals/gp100.pdf),
pp8, 32, establish which visible assemblies move. Hidden working parts are omitted.

The [C.I.P. exterior sheet](https://bobp.cip-bobp.org/uploads/tdcc/tab-iv/357-magnum-en.pdf)
bounds the cartridge at 32.77 mm case length, 40.39 mm overall and 11.18 mm rim
diameter. Our jacketed soft-point is 40.20 mm with an 11.12 mm rim. Fired case
mouths are open, with a struck primer; fine fictional `PD 357 / 26` headstamp
relief is reserved for the later normal bake.

The [Marine Corps pistol marksmanship manual](https://www.trngcmd.marines.mil/Portals/207/Docs/wtbn/MCRP%203-01B%20-%20Pistol%20Marksmanship.pdf)
is a posture reference for a two-handed extended hold. Ishigaki, Edagawa and
Miyao's [1995 pistol-sighting study](https://pubmed.ncbi.nlm.nih.gov/8532455/)
reports a foresight approximately 80 cm from the eye in eleven marksmen.
Our front blade is 800 mm ahead of Eye; subtracting our 150 mm sight radius
puts Eye **650 mm behind the notch**. This applies that published optical
distance to an authored two-hand posture, not a universal anthropometric
measurement or a number supplied by the Marine manual. Both sight tops and
the eye are at Z=83 mm, with the notch floor below the ray and a 3 mm front
blade inside a 4 mm rear notch. The delivered exact camera is shown against gray.

Photographic form cues and authors/licenses are in [refs/SOURCES.md](refs/SOURCES.md).
The ATF photo is the principal four-inch service-grip side reference. The
Stephen Z side photographs show longer barrels and wood target grips; camera
fits use the frame/cylinder landmarks, and those differences are retained in
the comparison captions. Dmoore5556's open seven-shot cylinder is a crane,
star, window and thumbpiece comparator, not a six-chamber layout template.
Spencer Dutch's macro photos establish broad radii and machined transitions.

Finish sites planned for **after** form acceptance: satin machined stainless,
turned cylinder texture, dark sights and rubber. Visible causal wear will be
a thin polished cylinder stop track, carbon rings on the chamber face and
forcing-cone/topstrap underside, narrow holster polish at the muzzle, cylinder
lands and shroud nose, and smoother rubber at the palm/finger contact crests.
There are no wear shaders or baked textures in this checkpoint.

## Round-two form gauges

The ATF side photograph is used for shape only: its white background clips.
Manual native-pixel gauges use the cylinder's approximately 118 px projected
height (about 39.4 mm in our class envelope), approximately **3.0 px/mm**.
These are visual estimates, with at least ±2 px placement uncertainty and
additional perspective/class uncertainty; they are not shop dimensions.

| Side photograph gauge | Native pixels | Approximate class estimate | Authored revision |
| --- | --- | --- | --- |
| Hammer spur's side thickness | x≈400, y≈137–146 | 3.0 ±0.8 mm | 3.4 mm at the tip; thicker root |
| Spur below the topstrap | y≈132 versus y≈100 | 10.7 ±1.2 mm | approximately 11 mm, same pivot/pull |
| Trigger's upper working blade | y≈300, x≈512–531 | 6.3 ±0.8 mm | 6.11 mm measured at Z=10 mm; taper toward toe |
| Guard's lower band | x≈530, y≈361–370 | 3.0 ±0.8 mm | 2.8 mm nominal, rounded edges |

The oblique `open.jpg` and `target.jpg` show the hammer body nearly filling
its narrow slot, with a visibly wider thumb spur, and flat transverse guard
sides. Foreshortening prevents a reliable millimeter width from those views.
The **7.6 mm hammer body, 8.0 mm slot, approximately 9.8 mm spur and 8.4 mm
guard width** are original class estimates based on those width ratios, with
roughly ±1.5 mm photographic uncertainty. Actual source/import rays and cuts
are in `build/form-metrics.json` and `renders/checkpoint/sections/`; the
reference uncertainty must not be replaced by those precise mesh numbers.

The wrap-around rubber now has a broad-backed egg section, a narrower finger
face, a changing palm swell, a curved rear silhouette and a high rounded web.
The authored butt is domed, rather than cut off on a plane. Its steel seat is
cut from the actual forging after cage subdivision. Round two cut it before
voxel relaxation; round three moves the final cavity cut after relaxation to
retain a clean molded lip.

The shroud is bored around the rest-position rod, with a narrow left release
passage following the accepted crane arc. The round-three brief confirms this
construction: a closed fixed tube would trap the rod. Independent source/import
rays now measure the departure passage and prove the right wall hides the rod;
the unchanged-tolerance animation sweep separately proves swing clearance.

## Round-three machined surfaces

The high-resolution open-cylinder photograph supplies the resting hammer's
concave root, rising curved thumb roof and thin rounded tip. Its native crop is
`(2420,320)–(2980,730)`. The target photograph supplies the cocked cheek and roof,
crop `(1650,720)–(2370,1350)`. Camera directions, roll and scale are visual
estimates in `src/hammer_review.py`, kept explicit instead of deforming the
asset to fit a picture. The separate top macro makes the transverse form clear.
The checkering is original geometry: roughly 0.7 mm longitudinal pitch and
0.6–0.8 mm transverse pitch over most of the curved roof, with a tapered margin.
This is a photographic estimate, not a manufacturer pitch specification.

The rest photograph is balanced on its gray foam. The target photograph has
mixed blue lighting and no dependable backdrop neutral; its presumed uncoated
hammer cheek supplies a local neutral estimate. Its colors establish no material
acceptance. The registered side/quarter photographs remain the references for
the rib root, rolled lower lug nose, flush sideplate seam, contoured latch and
the sights' tapered bodies. No photograph is traced, projected or textured.

The former black rectangle below the front frame is the lower crane-yoke web
and pivot, with the closed-seat hardware behind it. Its actual pivot remains
unchanged. The reshaped boss/web and integrated right forging bolster replace
the hanging rectangular outline; the small round bearing projection remains.

## Last hammer and forging revision

The two native hammer crops are separate photographs and estimated viewpoints,
not two calibrated views of one specimen. Manual comparison gauges on the rest
crop give approximately 69 px at the tongue root, 47 px near the end, and 208 px
of exposed sweep (placement uncertainty about 5 px). The cocked crop gives about
81 px at the root and 45 px near the end; its curved roof is seen more obliquely.
Their root/tip ratios, about 1.5–1.8, reject the previous nearly wire-thin tip.
The resting roof's roughly 25 px transverse projection is strongly foreshortened:
using the approximately 15° estimated view gives a class width around 9–11 mm,
with at least ±2 mm uncertainty. This is an estimate, not a published width.

Scale and perspective uncertainty put the visual side gauges at approximately
5–7 mm at the root, 3–4 mm near the end, and 14–18 mm beyond the rear frame.
They are construction/appearance estimates only. They do not constitute shop
measurements or certify a replica. No photograph outline is traced into a mesh.
The one subdivision cage is adjusted against both views and the independent top
view. The game mesh spends its hammer allocation on curved cheeks and a broad
rounded tongue; the curved roof's fine crossed cuts transfer through the bake.

`src/form_metrics.py` measures actual triangle hits in source and fresh import:
about **6.02 mm root, 3.58 mm near-tip, 9.95 mm transverse width and 16.02 mm past
the frame**. Root and tip gauges are at Y=−4/−7.5 mm; the transverse cut is at
Y=−5, Z=71 mm. The extension gauge uses the actual rear forging at X=5, Z=66 mm,
then its Y distance to the actual rear of the hammer. These precise mesh gauges
must not be confused with the uncertain photographic estimates above.

The rear forging edge has an authored 1.25 mm round, rather than a 3.5 mm broad
chamfer. A continuous monotone belly flow blends the guard's front into the
crane-bearing corner; the former separate bolster and heel boxes are gone.
The crane remains the accepted moving yoke, flush in its relieved seat. The
lower lug rolls axially and transversely around its open-left rod passage;
the protected crown remains 1.45 mm recessed. The recoil shield has a narrower
rolled edge and the window's upper shoulders follow the cylinder radius.
The accepted forcing-cone gap, central window light and rod release remain
independent actual-surface gauges, not authored constants reported as measures.
