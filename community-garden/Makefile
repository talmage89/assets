CHECKPOINT_BLEND := build/gardens.blend
CHECKPOINT_OUT ?= renders/checkpoint
SEEDS ?= 117 229 341
ARCHETYPE ?=
CHECKPOINT_ARGS := --seeds $(SEEDS) $(if $(ARCHETYPE),--archetype $(ARCHETYPE))
CHECKPOINT_OUTPUTS := build/gardens.blend $(foreach s,$(SEEDS),export/checkpoint/Garden_$(s).gltf) export/checkpoint/CommunityGardenPieces.gltf
CHECKPOINT_DEPS := src/build.py src/geometry.py src/plants.py src/pieces.py src/fence.py src/plan.py build/context/shed.glb build/context/chain/T_ChainLink_BaseColor.png textures/checkpoint/T_GardenPlants_BaseColor.png
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --out $(CHECKPOINT_OUT)
CHECKPOINT_RENDER_ARGS := --seeds $(SEEDS)
VIEWS_117 := hero above corner compost water scale eevee tomato bean
VIEWS_229 := hero above corner compost water tomato bean
VIEWS_341 := hero above corner compost water accessible tomato bean
CHECKPOINT_RENDER_OUTPUTS := $(foreach s,$(SEEDS),$(foreach v,$(VIEWS_$(s)),$(CHECKPOINT_OUT)/$(s)/$(v).png)) $(CHECKPOINT_OUT)/pieces.png $(CHECKPOINT_OUT)/plants.png $(foreach s,$(SEEDS),export/checkpoint/Site_$(s).gltf)
include ../kit/checkpoint_rules.mk
BP += -t 4
$(CHECKPOINT_RENDER_OUTPUTS): src/neighborhood.py
.PRECIOUS: $(CHECKPOINT_RENDER_OUTPUTS)

# Build missing native prerequisites only. Existing accepted deliveries are
# read-only inputs and never invalidated by this family's source changes.
NATIVE_CONTEXT := ../trees/export/RedMaple.glb ../houses/export/Hearthfield-27.gltf ../apartments/export/Building-301.gltf ../cars/export/AlderH120.glb ../utility/export/UtilityParts.gltf ../ground/textures/ship/T_Lawn_BaseColor.png
render match: $(NATIVE_CONTEXT)
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

.PHONY: repeat match
repeat: model
	$(PYTHON) src/repeat.py
check: check-motion
.PHONY: check-motion
check-motion: model
	$(BP) --python src/motion.py
MATCH_OUTPUTS := $(foreach m,wise_bed oliver_construction martin_place,$(CHECKPOINT_OUT)/matches/$(m)-pair.jpg $(CHECKPOINT_OUT)/matches/$(m).png)
$(MATCH_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) src/match.py src/photo_matches.py src/render.py src/neighborhood.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/match.py -- --out $(CHECKPOINT_OUT)/matches --width $(WIDTH) --samples $(SAMPLES)
match: model refs $(MATCH_OUTPUTS)
review: match
