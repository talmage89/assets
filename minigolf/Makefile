# Look-dev checkpoint. No README gallery or docs images are generated here.
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
BP := $(BLENDER) -b --factory-startup -t 4 --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1440
SAMPLES ?= 32
MAPS := $(foreach c,BaseColor Normal ORM,textures/ship/T_Minigolf_$(c).png)
FENCE_MAPS := $(foreach c,BaseColor Normal ORM,../fences/textures/ship/T_WoodPrivacy_$(c).png)
CONTEXT_DEPS := ../cars/export/AlderC150.glb ../cars/export/AlderS240.glb ../trees/export/RedMaple.glb ../trees/export/PinOak.glb ../shrubs/export/Shrubs.glb ../street-light/export/StreetLight.glb
SOURCES := $(addprefix src/,build.py plan.py plan_check.py geometry.py holes.py fixtures.py site.py look.py textures.py preserve.py tangents.py landscape.py paths.py)
DELIVERIES := $(foreach s,71 92,export/Minigolf-$(s).gltf export/Minigolf-$(s).bin export/Minigolf-$(s).glb export/Minigolf-$(s).json)
.PHONY: source-match check-renders baseline all refs textures model export render check repeat match before-after context review clean FORCE
.NOTPARALLEL:
all: refs model check render match source-match before-after review
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
build/procedural/fields.json: src/textures.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/textures.py --size 4096
textures/bake/T_Minigolf_BaseColor.png textures/bake/T_Minigolf_Normal.png textures/bake/T_Minigolf_ORM.png &: build/procedural/fields.json
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source build/procedural --out textures/bake --name Minigolf --coverage 8 --size 4096 --samples 4 --height-distance .018
$(MAPS) &: textures/bake/T_Minigolf_BaseColor.png textures/bake/T_Minigolf_Normal.png textures/bake/T_Minigolf_ORM.png
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
	$(BP) --python src/build.py -- --out build/course.blend
model export: $(DELIVERIES) build/course.blend
check: model
	$(PYTHON) src/preserve.py
	$(PYTHON) src/test_tangents.py
	$(PYTHON) src/test_periodic.py
	$(PYTHON) src/routing.py
	$(BP) --python src/check.py
	$(BP) --python src/check_look.py
	$(PYTHON) $(KIT)/repo_check.py
render: model context
	$(PYTHON) src/render_batch.py --blender $(BLENDER) --out renders/lookdev --width $(WIDTH) --samples $(SAMPLES)
match: model context refs
	$(PYTHON) src/matches.py prepare
	$(PYTHON) src/matches_batch.py --blender $(BLENDER) --width $(WIDTH) --samples $(SAMPLES)
source-match: model context
	$(PYTHON) src/matches_batch.py --blender $(BLENDER) --source-fields --width $(WIDTH) --samples $(SAMPLES)
check-renders:
	$(PYTHON) src/look_review.py
baseline:
	$(PYTHON) src/baseline.py
before-after: model context baseline
	$(PYTHON) src/comparison_batch.py --blender $(BLENDER) --width $(WIDTH) --samples $(SAMPLES)
review:
	$(PYTHON) src/look_review.py
repeat: model
	$(PYTHON) src/repeat.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders','textures','export')]"
