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
SOURCES := $(wildcard src/*.py)
DELIVERIES := $(foreach s,71 92,export/Minigolf-$(s).gltf export/Minigolf-$(s).bin export/Minigolf-$(s).glb export/Minigolf-$(s).json)
.PHONY: baseline all refs textures model export render check repeat match before-after context review clean FORCE
.NOTPARALLEL:
all: refs model check render match before-after review
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
context: ../ground/export/Ground.glb
	$(PYTHON) src/context_build.py
$(DELIVERIES) build/course.blend build/manifest.json &: $(SOURCES) $(MAPS) ../ground/export/Ground.glb ../fences/textures/ship/T_WoodPrivacy_BaseColor.png
	$(BP) --python src/build.py -- --out build/course.blend
model export: $(DELIVERIES) build/course.blend
check: model
	$(PYTHON) src/preserve.py
	$(PYTHON) src/plan_check.py
	$(PYTHON) src/routing.py
	$(BP) --python src/check.py
	$(BP) --python src/check_look.py
	$(PYTHON) $(KIT)/repo_check.py
render: model context
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/lookdev --width $(WIDTH) --samples $(SAMPLES)
match: model context refs
	$(PYTHON) src/matches.py prepare
	$(KIT)/with_gpu.sh $(BP) --python src/matches.py -- render --width $(WIDTH) --samples $(SAMPLES)
baseline:
	$(PYTHON) src/baseline.py
before-after: model context baseline
	$(KIT)/with_gpu.sh $(BP) --python src/comparison.py -- --width $(WIDTH) --samples $(SAMPLES)
review:
	$(PYTHON) src/look_review.py
repeat: model
	$(PYTHON) src/repeat.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders','textures','export')]"
