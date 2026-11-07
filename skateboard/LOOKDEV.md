# Delivery evidence

`make` rebuilds sources, 4096 Cycles bakes, 2048 delivery maps, embedded GLBs,
construction checks, imported-GLB audits, sunlit finals, photograph comparisons,
native comparison crops and five compact docs JPGs. Blender runs serially;
all Blender work holds the shared kit lock. Every source texel is script-generated.

- `export/{new,season,beat}.glb`: one atlas per age, three response classes
  sharing three images, seven rigid meshes with the accepted steering/wheel
  pivots and five sockets. New/season are 13,888 triangles; beat is 13,928.
- `textures/<state>/T_Skateboard_{BaseColor,Normal,ORM}.png`: 2048 images.
  ORM is R occlusion/G roughness/B metallic. Normal is OpenGL +Y.
- `build/<state>/{model,high,finalized}.blend`: measured source form, dense
  finish source and packed game assembly. Manufacturing helpers do not export.
- `build/<state>/{construction,high-check,verify}.json`: separate actual-surface
  construction/motion and fresh-import delivery proof.
- `renders/final/<state>/`: eight Cycles hero/detail views of each baked GLB.
  Season also has top, bottom, side, front and 1.8 m human scale views.
  Beat has an additional axial wheel view proving the skid flat.
- `renders/final/eevee/hero.png`: season GLB in Eevee, same camera and sun.
- `renders/final/{contact,turnaround,graphics-sheet,matched-pairs}.jpg`:
  complete review sheets; `budgets.json`, `values.json` and `provenance.json`
  record costs, display tones and each final's export hash.
- `renders/final/{pairs,source-pairs}/`: three matched-light comparisons of
  the export and dense source, respectively. Two photographs show used boards.
- `renders/fixes/*-before-after.jpg`: nine same-camera native comparisons
  covering grit, filed/frayed trim, tag removal, season and beat slide tracks,
  both hanger faces, separated tread/sidewall color and the beat skid flat.
  `crops.json` records source hashes, cameras and native rectangles. Each side
  is at least 800 px wide, with no enlargement.
- `docs/`: five final JPGs, each at most 1600 px wide and 200,000 bytes.

Appearance baseline `b0939d8` is reconstructed with `src/accepted.py` only if
missing. It reads our own scripts from this clone's history and uses the same
kit; it never reads another checkout. Earlier form comparisons at `8cc0710`
remain available through `make form` and are outside the default final build.

One resident age costs about 16 MiB for three 2048 8-bpp compressed maps with
complete mip chains; all three cost 48 MiB. This is a compression estimate,
not measured engine residency. Original graphics are Ditchlight orbital
contours, Kilnline fired-brick/lightning and Static Orchard interrupted
radio/growth forms. All three ages export the default Ditchlight design.
Other seeded widths/designs remain parametric construction variants.

Photographs are comparison/measurement only, never textures. Concrete balances
the two used-board photos; a zinc washer balances the indoor loose truck.
The 2006 horizontal-board fit is 15.34 px RMS on a 1285 px crop, the 2010 used
complete is 22.60 px on 3072 px, and the 2005 full-size loose truck is 13.65 px
on 600 px. A 1140 px truck/wheel crop retains the full-board calibration.
Lenses, mixed light, exposure and the real truck's exact dimensions remain
uncertain; neither upsampling nor a serialization pass makes these exact.

`make repeat` checks byte-identical GLB serialization from the finalized
scenes/maps and independent byte-identical original PNG-field regeneration.
It does not claim an independent repeated GPU bake. `make repeat-form` rebuilds
the untextured new form; `make check-variants` checks the three other widths.
`REVIEW.md` records the full-size appearance judgment separately from checks.
