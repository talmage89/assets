# Exported-course finals. Docs are generated explicitly after native-size review.
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
BP := $(BLENDER) -b --factory-startup -t 4 --python-exit-code 1
# Serialize mesh evaluation/export as well as frame execution. GPU validation
# and rendering retain their own bounded thread settings.
MODEL := $(KIT)/with_gpu.sh $(BLENDER) -b --factory-startup -t 1 --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1440
SAMPLES ?= 32
MAPS := $(foreach c,BaseColor Normal ORM,textures/ship/T_Minigolf_$(c).png)
FENCE_MAPS := $(foreach c,BaseColor Normal ORM,../fences/textures/ship/T_WoodPrivacy_$(c).png)
CONTEXT_DEPS := ../cars/export/AlderC150.glb ../cars/export/AlderS240.glb ../trees/export/RedMaple.glb ../trees/export/PinOak.glb ../shrubs/export/Shrubs.glb ../street-light/export/StreetLight.glb
SOURCES := $(addprefix src/,build.py plan.py plan_check.py geometry.py holes.py fixtures.py site.py look.py textures.py terraces.py external.py pieces.py preserve.py tangents.py landscape.py paths.py walk_audit.py joins.py)
DELIVERIES := export/MinigolfPieces.gltf export/MinigolfPieces.bin $(foreach s,71 92,export/Minigolf-$(s).gltf export/Minigolf-$(s).bin build/embedded/Minigolf-$(s).glb export/Minigolf-$(s).json)
.PHONY: source-match check-renders baseline all refs textures model export render catalog docs check repeat check-texture-repeat match before-after context review clean FORCE plants
.NOTPARALLEL:
all: refs model plants context check before-after match source-match render catalog review
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
build/procedural/fields.json: src/textures.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/textures.py --size 4096
textures/bake/T_Minigolf_BaseColor.png textures/bake/T_Minigolf_Normal.png textures/bake/T_Minigolf_ORM.png textures/bake/Minigolf-ready.json &: build/procedural/fields.json src/finish_bake.py
	$(PYTHON) -c "from pathlib import Path; Path('textures/bake/Minigolf-ready.json').unlink(missing_ok=True)"
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source build/procedural --out textures/bake --name Minigolf --coverage 8 --size 4096 --samples 4 --height-distance .018
	$(PYTHON) src/finish_bake.py
$(MAPS) &: textures/bake/T_Minigolf_BaseColor.png textures/bake/T_Minigolf_Normal.png textures/bake/T_Minigolf_ORM.png textures/bake/Minigolf-ready.json
	$(PYTHON) $(KIT)/downsample.py --source textures/bake --out textures/ship --asset Minigolf --size 2048
textures: $(MAPS)
../ground/export/Ground.glb:
	$(MAKE) -C ../ground export
# Existing library deliveries have no source prerequisites here: keep them
# byte-identical. Only an absent dependency invokes its family's exporter.
$(FENCE_MAPS) &:
	$(MAKE) -C ../fences export/WoodPrivacy.glb
../cars/export/AlderC150.glb:
	$(MAKE) -C ../cars BODY=pickup export/AlderC150.glb
../cars/export/AlderS240.glb:
	$(MAKE) -C ../cars BODY=sedan export/AlderS240.glb
../trees/export/RedMaple.glb:
	$(MAKE) -C ../trees SPECIES=maple export/RedMaple.glb
../trees/export/PinOak.glb:
	$(MAKE) -C ../trees SPECIES=oak export/PinOak.glb
../shrubs/export/Shrubs.glb:
	$(MAKE) -C ../shrubs export/Shrubs.glb
../street-light/export/StreetLight.glb:
	$(MAKE) -C ../street-light export/StreetLight.glb
context: ../ground/export/Ground.glb $(CONTEXT_DEPS)
	$(PYTHON) src/context_build.py
$(DELIVERIES) build/course.blend build/manifest.json &: $(SOURCES) $(MAPS) ../ground/export/Ground.glb $(FENCE_MAPS)
	$(MODEL) --python src/build.py -- --out build/course.blend
model export: $(DELIVERIES) build/course.blend
LANDSCAPES := $(foreach s,71 92,export/Minigolf-$(s)-landscape.gltf export/Minigolf-$(s)-landscape.bin)
$(LANDSCAPES) &: src/plant_export.py src/context.py src/paths.py src/plan.py src/landscape.py src/external.py $(CONTEXT_DEPS) | context
	$(KIT)/with_gpu.sh $(BP) --python src/plant_export.py
plants: $(LANDSCAPES)
check: model plants
	$(PYTHON) src/preserve.py
	$(PYTHON) src/test_tangents.py
	$(PYTHON) src/test_periodic.py
	$(PYTHON) src/routing.py
	$(KIT)/with_gpu.sh $(BP) --python src/check_all.py
	$(PYTHON) src/costs.py
	$(PYTHON) $(KIT)/repo_check.py
render: model plants context
	$(KIT)/with_gpu.sh $(PYTHON) src/render_batch.py --course classic --blender $(BLENDER) --out renders/final --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(PYTHON) src/render_batch.py --course adventure --blender $(BLENDER) --out renders/final --width $(WIDTH) --samples $(SAMPLES)
catalog: model
	$(KIT)/with_gpu.sh $(BP) --python src/catalog.py -- --kind fixtures --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/catalog.py -- --kind holes --width $(WIDTH) --samples $(SAMPLES)
match: model plants context refs
	$(PYTHON) src/matches.py prepare
	$(KIT)/with_gpu.sh $(PYTHON) src/matches_batch.py --blender $(BLENDER) --width $(WIDTH) --samples $(SAMPLES)
source-match: model plants context
	$(KIT)/with_gpu.sh $(PYTHON) src/matches_batch.py --blender $(BLENDER) --source-fields --width $(WIDTH) --samples $(SAMPLES)
check-renders:
	$(PYTHON) src/look_review.py
baseline:
	$(PYTHON) src/finish_views.py --prepare-only --blender $(BLENDER)
before-after: model plants context refs baseline
	$(PYTHON) src/matches.py prepare
	$(KIT)/with_gpu.sh $(PYTHON) src/finish_views.py --blender $(BLENDER) --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(PYTHON) src/finish_views.py --after-only --blender $(BLENDER) --width $(WIDTH) --samples $(SAMPLES) --shots classic-tee,classic-walks,adventure-walks
review:
	$(PYTHON) src/look_review.py
docs: review
	$(PYTHON) src/look_review.py --docs
repeat: model
	$(PYTHON) src/repeat.py
check-texture-repeat: repeat
	$(PYTHON) -c "import json; assert json.load(open('build/texture-repeat.json'))['passed']"
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders','textures','export')]"
