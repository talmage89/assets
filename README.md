# assets

Realistic, original, game-ready 3D assets, each generated entirely by scripts in Blender 5.2: parametric modeling
against measured references, procedural materials baked to standard PBR textures, a GLB export, and studio renders
of the exported asset. Nothing is downloaded or adapted from existing models or textures.

Each asset folder has its own README with renders, dimensions and rebuild steps. `kit/` is the shared toolkit.

## Build requirements

- Blender 5.2, GNU make, Python 3, Git, a POSIX shell and `flock` (util-linux).
- Pillow (`PIL`) and NumPy in the Python environment used by `PYTHON` (default
  `python3`); Blender supplies its own `bpy`, `bmesh` and `mathutils` modules.
- fontconfig (`fc-match`), Noto Sans Regular/Bold and DejaVu Sans Book/Bold/
  Condensed Bold. Font discovery uses family/style names rather than install
  paths and reports missing faces instead of substituting another font.
- Poppler's `pdfimages` for the street light, traffic cone and patio set references.
- An NVIDIA GPU with Cycles OptiX or CUDA support is recommended. If neither
  device is available, Cycles warns and uses the CPU; baking/rendering is slower.
  The lock wrapper is used for both paths. `ASSETS_GPU_LOCK` may point to a shared
  lab lock; its default is `build/locks/gpu.lock` inside this clone.

Run `make` in an asset folder; `BLENDER` and `PYTHON` can select the executables. Paths under an asset's `renders/` and `build/`
named in its README are what `make` builds; only `docs/` images are committed.
Reference targets retrieve cited images/PDFs and need network access. The optional
external tank fit check/render skips by default; enable it with
`make TANK_REFERENCE=/path/to/propane-tank.glb` using the original compatible
reference, which is not distributed here.

## Assets

Backyard and patio
- [Gas grill](gas-grill/README.md): three-burner LP grill on an open cart, with a rigged hose and an external-tank socket.
- [Patio heater](patio-heater/README.md): freestanding propane mushroom heater with a tank door and an emissive emitter.
- [Lawn mower](lawn-mower/README.md): 21-inch gas push mower; wheels, operator bail and handle fold move.
- [Storage shed](shed/README.md): 8×10 ft timber shed on skids, with a framed interior, shingle roof and hinged double doors.
- [Trampoline](trampoline/README.md): 14 ft galvanized frame on W legs, with sewn padding, a woven mat and a safety-net enclosure.
- [Patio set](patio-set/README.md): table, sling chairs, chaise and a market umbrella, open and furled, on one shared set.
- [Cooler](cooler/README.md): 47-quart rotomolded cooler with a hinged lid, T-latches and a drain cap.
- [Kiddie pool](kiddie-pool/README.md): five-foot rigid wading pool with an optional water surface.
- [Fences](fences/README.md): wood privacy, white picket and chain-link sections, posts and gates.

Street
- [Fire hydrant](fire-hydrant/README.md): three-way dry-barrel hydrant, installed at grade.
- [Street signs](street-signs/README.md): stop sign with crossed street-name blades.
- [Street light](street-light/README.md): LED cobra head on a tapered steel pole.
- [Traffic cone](traffic-cone/README.md): 28-inch PVC cone with a weighted base.
- [Mailbox](mailbox/README.md): curbside mailbox on a wooden post; door and flag move.
- [Trash cart](trash-cart/README.md): 96-gallon wheeled cart in trash and recycling variants.
- [Metal garbage can](metal-trash-can/README.md): 31-gallon galvanized steel can with its lid.
- [Ammo can](ammo-can/README.md): .50 caliber steel ammo can with a working latch and lid.

Ground
- [Street ground](ground/README.md): modular road, intersection, curb and gutter, sidewalk and curb ramps,
  driveways, lawn, a storm inlet and a manhole, on three seamless tiling sets and one trim and decal atlas.

Houses
- [Builder colonials and postwar ranches](houses/README.md): seeded two-story and one-story houses with garages
  or carports, moving doors and one shared weathered tiling-and-trim texture family.

Vehicles
- [Pickup](cars/README.md): full-size crew-cab pickup in five factory colors; doors, hood, tailgate, steering and
  wheels move.

Trees
- [Red maple](trees/README.md): 12.5 m open-grown summer red maple with leaf cards, flaky lower bark and wind
  weights.
- [Pin oak](trees/README.md): 17 m street pin oak with drooping lower limbs, lobed leaf cards, ridged bark and
  wind weights, from the same species-driven generator.
- [Foundation shrubs](shrubs/README.md): a sheared boxwood and a blooming bigleaf hydrangea in one GLB on one
  shared set, with wind weights.

Held weapons
- [Guns](guns/README.md): the PD C9 compact 9 mm pistol, the family's pilot, rigged with ten clips on the rifle's
  frame and sockets, with loaded and empty magazines and a fired case; the PD Hearth 12 pump shotgun in blued steel
  and walnut, with eighteen clips, a live shell and a fired hull; the PD Vesper B24 bolt-action rifle with a variable
  scope and bipod, nine clips, magazines and a fired case.

Toolkit
- [Shared toolkit](kit/README.md): procedural modeling and materials, UV, bake and export, verification and studio
  renders of the exported GLB.
