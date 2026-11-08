# Baked external-image family; CPU construction, bounded serial GPU view sets.
BLENDER ?= ./src/blender.sh
WIDTH ?= 1600
SAMPLES ?= 96
SEEDS ?= 117 229 341
ARCHETYPE ?=
CHECKPOINT_BLEND := build/gardens.blend
CHECKPOINT_OUT ?= renders/final
CHANNELS := BaseColor Normal ORM
PLANT_SOURCE := $(foreach c,$(CHANNELS),textures/4k-plants/T_GardenPlants_$(c).png)
PLANT_MAPS := $(foreach c,$(CHANNELS),textures/ship/T_GardenPlants_$(c).png)
SURFACE_SOURCE := $(foreach c,BaseColor ORM Height,textures/source-surfaces/T_GardenSurfaces_$(c).png)
SURFACE_BAKES := $(foreach c,$(CHANNELS),textures/4k-surfaces/T_GardenSurfaces_$(c).png)
SURFACE_MAPS := $(foreach c,$(CHANNELS),textures/ship/T_GardenSurfaces_$(c).png)
LAWN_MAPS := $(foreach c,$(CHANNELS),textures/ship/T_GardenLawn_$(c).png)
CHAIN_MAPS := $(foreach c,$(CHANNELS),build/context/chain/T_ChainLink_$(c).png)
SHIP_CHAIN_MAPS := $(foreach c,$(CHANNELS),textures/ship/T_ChainLink_$(c).png)
CHECKPOINT_ARGS := --seeds $(SEEDS) $(if $(ARCHETYPE),--archetype $(ARCHETYPE))
CHECKPOINT_OUTPUTS := build/gardens.blend build/pieces.json $(foreach s,$(SEEDS),build/garden-$(s).json export/final/Garden_$(s).gltf export/final/Garden_$(s).bin) export/final/CommunityGardenPieces.gltf export/final/CommunityGardenPieces.bin
CHECKPOINT_DEPS := $(addprefix src/,build.py geometry.py plants.py pieces.py fence.py plan.py groundcover.py surfaces.py atlas.py) $(PLANT_MAPS) $(SURFACE_MAPS) $(LAWN_MAPS) $(CHAIN_MAPS) $(SHIP_CHAIN_MAPS) build/context/shed.glb
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --out $(CHECKPOINT_OUT)
CHECKPOINT_RENDER_ARGS := --lookdev --final --seeds $(SEEDS)
COMMON_VIEWS := before-camera hero above corner compost water shed turf tomato bean squash front side back
VIEWS_117 := $(COMMON_VIEWS) scale eevee
VIEWS_229 := $(COMMON_VIEWS)
VIEWS_341 := $(COMMON_VIEWS) accessible
VIEW_PNGS := $(foreach s,$(SEEDS),$(foreach v,$(VIEWS_$(s)),$(CHECKPOINT_OUT)/$(s)/$(v).png)) $(CHECKPOINT_OUT)/pieces.png $(CHECKPOINT_OUT)/plants.png $(foreach s,tomato squash bean corn marigold corn-ear,$(CHECKPOINT_OUT)/plants/$(s).png)
MATCH_PNGS := $(foreach m,wise_bed cityhall_mature martin_place,$(CHECKPOINT_OUT)/matches/$(m).png)
MATCH_PAIRS := $(MATCH_PNGS:.png=-pair.jpg)
CHECKPOINT_RENDER_OUTPUTS := $(VIEW_PNGS) $(VIEW_PNGS:.png=.json) $(MATCH_PNGS) $(MATCH_PNGS:.png=.json) $(MATCH_PAIRS)
include ../kit/checkpoint_rules.mk
BP += -t 4
.PRECIOUS: $(CHECKPOINT_RENDER_OUTPUTS)

# Canonical deliveries are immutable inputs; only absent prerequisites build.
NATIVE_LAWN := $(foreach c,$(CHANNELS),../ground/textures/ship/T_Lawn_$(c).png)
NATIVE_CONTEXT := ../trees/export/RedMaple.glb ../houses/export/Hearthfield-27.gltf ../apartments/export/Building-301.gltf ../cars/export/AlderH120.glb ../utility/export/UtilityParts.gltf $(NATIVE_LAWN)
../trees/export/RedMaple.glb:
	$(MAKE) -C ../trees export
../houses/export/Hearthfield-27.gltf:
	$(MAKE) -C ../houses SEED=27 SEEDS=27 export
../apartments/export/Building-301.gltf:
	$(MAKE) -C ../apartments export
../cars/export/AlderH120.glb:
	$(MAKE) -C ../cars BODY=hatch export
../utility/export/UtilityParts.gltf:
	$(MAKE) -C ../utility export
$(NATIVE_LAWN) &:
	$(MAKE) -C ../ground textures

build/context/shed.glb build/context/shed.json &: src/context_build.py ../shed/src/build.py ../shed/src/dimensions.py
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/context_build.py
$(CHAIN_MAPS) build/context/chain/tile-report.json &: ../fences/chain-link/src/mesh_tile.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) ../fences/chain-link/src/mesh_tile.py --out build/context/chain
$(SHIP_CHAIN_MAPS) &: $(CHAIN_MAPS)
	@mkdir -p textures/ship
	cp $(CHAIN_MAPS) textures/ship/
$(PLANT_SOURCE) &: src/atlas.py ../ground/src/organic.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/atlas.py
$(PLANT_MAPS) &: $(PLANT_SOURCE) src/atlas.py ../ground/src/organic.py
	$(PYTHON) $(KIT)/downsample.py --source textures/4k-plants --out textures/ship --asset GardenPlants --size 1024
$(SURFACE_SOURCE) build/surface-layout.json &: src/surfaces.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/surfaces.py
$(SURFACE_BAKES) &: $(SURFACE_SOURCE) src/surfaces.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source textures/source-surfaces --out textures/4k-surfaces --name GardenSurfaces --coverage 4 --size 4096 --samples 8 --height-distance .030
$(SURFACE_MAPS) &: $(SURFACE_BAKES) src/surfaces.py
	$(PYTHON) $(KIT)/downsample.py --source textures/4k-surfaces --out textures/ship --asset GardenSurfaces --size 2048
$(LAWN_MAPS) &: src/groundcover.py $(NATIVE_LAWN)
	$(PYTHON) -c "import sys;sys.path.insert(0,'src');from groundcover import maps;maps('..','textures/ship')"

SCENES := $(foreach s,$(SEEDS),export/final/Site_$(s).gltf)
SCENE_OUTPUTS := $(SCENES) $(SCENES:.gltf=.bin) $(foreach s,$(SEEDS),build/context/site-$(s).json build/context/costs-$(s).json build/context/Site_$(s)-native-tangent.json)
$(SCENE_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) $(NATIVE_CONTEXT) $(addprefix src/,neighborhood.py package.py render.py park_hall.py groundcover.py)
	$(BP) --python src/package.py -- --seeds $(SEEDS)
.PHONY: scenes check-scenes check-motion check-look match fixes docs repeat check-texture-repeat look-review
scenes: model $(SCENE_OUTPUTS)
check-scenes: scenes
	$(PYTHON) src/review.py --sites-only
check-motion: scenes
	$(BP) --python src/motion.py
check-look: model
	$(PYTHON) src/look_audit.py
check: check-scenes check-motion check-look
$(CHECKPOINT_RENDER_OUTPUTS): $(SCENE_OUTPUTS) $(addprefix src/,blender.sh render_driver.py look_batch.py match.py photo_matches.py) | check-scenes
match: render
look-review:
	$(PYTHON) src/look_review.py --out $(CHECKPOINT_OUT)
fixes: render
	$(PYTHON) src/delivery_review.py --out $(CHECKPOINT_OUT)
review: look-review
# Explicit visual receipt is written only after all native final images/crops
# have been opened and critiqued. Rebuilding models/renders needs no approval.
docs: check render review
	$(PYTHON) src/delivery_review.py --out $(CHECKPOINT_OUT) --docs
repeat: model scenes
	$(PYTHON) src/repeat.py
check-texture-repeat: model
	@mkdir -p build/texture-repeat
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source textures/source-surfaces --out build/texture-repeat/4k --name GardenSurfaces --coverage 4 --size 4096 --samples 8 --height-distance .030
	$(PYTHON) $(KIT)/downsample.py --source build/texture-repeat/4k --out build/texture-repeat/ship --asset GardenSurfaces --size 2048
	$(PYTHON) $(KIT)/compare_textures.py --reference textures/4k-surfaces --candidate build/texture-repeat/4k --out build/texture-repeat-4k-check.json
	$(PYTHON) -c "from pathlib import Path;import shutil;p=Path('build/texture-repeat/reference');p.mkdir(exist_ok=True);[shutil.copy2(f,p/f.name) for f in Path('textures/ship').glob('T_GardenSurfaces_*.png')]"
	$(PYTHON) $(KIT)/compare_textures.py --reference build/texture-repeat/reference --candidate build/texture-repeat/ship --out build/texture-repeat-check.json
