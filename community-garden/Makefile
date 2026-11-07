CHECKPOINT_BLEND := build/gardens.blend
SEEDS ?= 117 229 341
ARCHETYPE ?=
CHECKPOINT_ARGS := --seeds $(SEEDS) $(if $(ARCHETYPE),--archetype $(ARCHETYPE))
CHECKPOINT_OUTPUTS := build/gardens.blend $(foreach s,$(SEEDS),export/checkpoint/Garden_$(s).gltf) export/checkpoint/CommunityGardenPieces.gltf
CHECKPOINT_DEPS := src/build.py src/geometry.py src/plants.py src/pieces.py src/fence.py src/plan.py build/context/shed.glb build/context/chain/T_ChainLink_BaseColor.png textures/checkpoint/T_GardenPlants_BaseColor.png
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --out $(CHECKPOINT_OUT)
CHECKPOINT_RENDER_ARGS := --seeds $(SEEDS)
include ../kit/checkpoint_rules.mk
BP += -t 4

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
match: model refs
	$(KIT)/with_gpu.sh $(BP) --python src/match.py -- --out $(CHECKPOINT_OUT)/matches --width $(WIDTH) --samples $(SAMPLES)
