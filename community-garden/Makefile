CHECKPOINT_BLEND := build/gardens.blend
CHECKPOINT_OUT ?= renders/lookdev
SEEDS ?= 117 229 341
ARCHETYPE ?=
CHECKPOINT_ARGS := --seeds $(SEEDS) $(if $(ARCHETYPE),--archetype $(ARCHETYPE))
CHECKPOINT_OUTPUTS := build/gardens.blend $(foreach s,$(SEEDS),export/checkpoint/Garden_$(s).gltf) export/checkpoint/CommunityGardenPieces.gltf
CHECKPOINT_DEPS := src/surfaces.py textures/checkpoint/T_GardenSurfaces_BaseColor.png  src/build.py src/geometry.py src/plants.py src/pieces.py src/fence.py src/plan.py build/context/shed.glb build/context/chain/T_ChainLink_BaseColor.png textures/checkpoint/T_GardenPlants_BaseColor.png
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --out $(CHECKPOINT_OUT)
CHECKPOINT_RENDER_ARGS := --lookdev --seeds $(SEEDS)
VIEWS_117 := before-camera hero above corner compost water scale eevee tomato bean squash
VIEWS_229 := before-camera hero above corner compost water tomato bean squash
VIEWS_341 := before-camera hero above corner compost water accessible tomato bean squash
CHECKPOINT_RENDER_OUTPUTS := $(foreach sp,tomato squash bean corn marigold,$(CHECKPOINT_OUT)/plants/$(sp).png) $(foreach s,$(SEEDS),$(foreach v,$(VIEWS_$(s)),$(CHECKPOINT_OUT)/$(s)/$(v).png)) $(CHECKPOINT_OUT)/pieces.png $(CHECKPOINT_OUT)/plants.png
include ../kit/checkpoint_rules.mk
BP += -t 4
$(CHECKPOINT_RENDER_OUTPUTS): src/neighborhood.py
.PRECIOUS: $(CHECKPOINT_RENDER_OUTPUTS)

# Build missing native prerequisites only. Existing accepted deliveries are
# read-only inputs and never invalidated by this family's source changes.
NATIVE_CONTEXT := ../trees/export/RedMaple.glb ../houses/export/Hearthfield-27.gltf ../apartments/export/Building-301.gltf ../cars/export/AlderH120.glb ../utility/export/UtilityParts.gltf ../ground/textures/ship/T_Lawn_BaseColor.png
render match scenes: $(NATIVE_CONTEXT)
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
../ground/textures/ship/T_Lawn_BaseColor.png:
	$(MAKE) -C ../ground textures
$(CHECKPOINT_OUTPUTS): | ../ground/textures/ship/T_Lawn_BaseColor.png

build/context/shed.glb: src/context_build.py ../shed/src/build.py ../shed/src/dimensions.py
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/context_build.py
build/context/chain/T_ChainLink_BaseColor.png: ../fences/chain-link/src/mesh_tile.py
	$(PYTHON) ../fences/chain-link/src/mesh_tile.py --out build/context/chain
textures/checkpoint/T_GardenPlants_BaseColor.png: src/atlas.py
	$(PYTHON) src/atlas.py
	$(PYTHON) $(KIT)/downsample.py --source textures/4k-plants --out textures/checkpoint --asset GardenPlants --size 1024

.PHONY: repeat match scenes check-scenes
SCENES := $(foreach s,$(SEEDS),export/checkpoint/Site_$(s).gltf)
$(SCENES) &: $(CHECKPOINT_OUTPUTS) $(NATIVE_CONTEXT) src/neighborhood.py src/package.py src/render.py
	$(BP) --python src/package.py -- --seeds $(SEEDS)
scenes: model $(SCENES)
define seed_scene_dependency
$(foreach v,$(VIEWS_$(1)),$(CHECKPOINT_OUT)/$(1)/$(v).png): export/checkpoint/Site_$(1).gltf
endef
$(foreach s,$(SEEDS),$(eval $(call seed_scene_dependency,$(s))))
check-scenes: scenes
	$(PYTHON) src/review.py --sites-only
check: check-scenes
$(CHECKPOINT_RENDER_OUTPUTS): | check-scenes
repeat: model
	$(PYTHON) src/repeat.py
check: check-motion
.PHONY: check-motion
check-motion: model
	$(BP) --python src/motion.py
MATCH_OUTPUTS := $(foreach m,wise_bed cityhall_mature martin_place,$(CHECKPOINT_OUT)/matches/$(m)-pair.jpg $(CHECKPOINT_OUT)/matches/$(m).png)
$(MATCH_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) src/match.py src/photo_matches.py src/render.py src/neighborhood.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/match.py -- --out $(CHECKPOINT_OUT)/matches --width $(WIDTH) --samples $(SAMPLES)
match: model refs $(MATCH_OUTPUTS)
$(MATCH_OUTPUTS): $(SCENES) | check-scenes
review: match

# Source fields are entirely analytic. One GPU bake lock covers the complete set.
textures/source-surfaces/T_GardenSurfaces_Height.png: src/surfaces.py
	$(PYTHON) src/surfaces.py
textures/4k-surfaces/T_GardenSurfaces_Normal.png: textures/source-surfaces/T_GardenSurfaces_Height.png
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source textures/source-surfaces --out textures/4k-surfaces --name GardenSurfaces --coverage 4 --size 4096 --samples 8 --height-distance .030
textures/checkpoint/T_GardenSurfaces_BaseColor.png: textures/4k-surfaces/T_GardenSurfaces_Normal.png
	$(PYTHON) $(KIT)/downsample.py --source textures/4k-surfaces --out textures/checkpoint --asset GardenSurfaces --size 2048

.PHONY: look-batch
look-batch: scenes
	$(KIT)/with_gpu.sh $(BP) --python src/look_batch.py -- --out $(CHECKPOINT_OUT) --width $(WIDTH) --samples $(SAMPLES)

$(CHECKPOINT_RENDER_OUTPUTS): src/look_batch.py src/match.py src/photo_matches.py
.PHONY: check-look
check-look: model
	$(PYTHON) src/look_audit.py
check: check-look
review: look-review
.PHONY: look-review
look-review:
	$(PYTHON) src/look_review.py --out $(CHECKPOINT_OUT)
