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
cut from the actual forging after cage subdivision and before voxel relaxation.

The shroud is bored around the rest-position rod, with a narrower left release
passage following the accepted crane arc. A fully closed fixed tube would
trap the rod and prevent that swing. The remaining left-side exposure is
explicitly recorded as an unresolved difference from the requested enclosure,
not called accepted merely because the sweep passes.
