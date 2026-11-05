.DEFAULT_GOAL := all
.NOTPARALLEL:
.DELETE_ON_ERROR:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
BP := $(BLENDER) -t 2 -b --factory-startup --python-exit-code 1
RP := $(BLENDER) -t 4 -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1600
SAMPLES ?= 32
WEAR ?= .8
SEEDS := 201 202 203 204
MODELDEPS := $(addprefix src/,build.py equipment.py geometry.py graphics.py plan.py layout.py surfaces.py deliver.py)
MAPS := $(addprefix textures/ship/T_Signals_,BaseColor.png Normal.png ORM.png Emissive.png Names.png)
MODELS := $(foreach n,$(SEEDS),build/Signals-$(n).blend build/Signals-$(n).glb build/Signals-$(n).json build/Signals-$(n)-components.json)
PARTS := MastArm Pedestal Cabinet Head_three Head_fya Head_five Head_protected PushButton PushButtonPost PedHead SpanSet
MODELS += $(foreach p,$(PARTS),build/parts/$(p).glb)
.PHONY: all refs context preserve textures model export check render matches review repeat check-repo clean FORCE
all: refs context textures model arterial export check render matches review
build/parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
preserve:
	$(PYTHON) src/preserve.py
context: preserve
	$(PYTHON) src/context.py
$(MAPS) &: src/textures.py src/graphics.py build/parameters.txt
	$(PYTHON) src/graphics.py
	$(PYTHON) src/textures.py fields --wear $(WEAR)
	$(KIT)/with_gpu.sh $(BP) --python src/textures.py -- bake
	$(PYTHON) src/textures.py ship
textures: $(MAPS)
$(MODELS) &: $(MODELDEPS) $(MAPS) | context
	$(BP) --python src/build.py -- --out build/Signals-201.blend
model: $(MODELS)
build/delivery.json: $(MODELS) src/deliver.py
	$(PYTHON) src/deliver.py
export: build/delivery.json
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: export check-repo preserve
	$(PYTHON) src/check_delivery.py
	$(BP) --python src/check.py
	$(BP) --python src/construction.py
	$(BP) --python src/check_layout.py
	$(PYTHON) src/budget_report.py
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='$(WIDTH) $(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
renders/checkpoint/.stamp: build/delivery.json src/render.py src/setting.py src/layout.py ../ground/src/junction.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/render.py -- --source export/Signals-201.gltf --out renders/checkpoint --seeds 201,202,203,204 --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(RP) --python src/lens_compare.py
	@touch $@
render: renders/checkpoint/.stamp
build/cameras.json: src/matches.py src/sidewalk_fit.py src/layout.py $(foreach n,$(SEEDS),build/Signals-$(n).json) | refs
	$(PYTHON) src/matches.py
renders/matches/.stamp: build/delivery.json build/cameras.json src/render.py src/setting.py build/render-parameters.txt
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	$(KIT)/with_gpu.sh $(RP) --python src/render.py -- --source export/Signals-201.gltf --out renders/matches --seeds 201,202,203,204 --camera-file build/cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose
	@touch $@
matches: renders/matches/.stamp renders/source-matches/.stamp
review: render matches
	$(PYTHON) src/review.py --out renders/checkpoint
repeat: export
	$(PYTHON) src/repeat.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders/checkpoint','renders/matches','renders/source-matches')]"

build/sites.json: src/layout.py
	$(PYTHON) src/layout.py
../ground/export/ArterialSites.glb: build/sites.json ../ground/src/junction.py
	$(BP) --python ../ground/src/junction.py -- --spec build/sites.json --out $@
.PHONY: arterial
arterial: ../ground/export/ArterialSites.glb

renders/source-matches/.stamp: $(MODELS) build/cameras.json src/render.py src/setting.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/render.py -- --source build/Signals-201.blend --out renders/source-matches --seeds 201,202,203,204 --camera-file build/cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose --renders renders/source-matches
	@touch $@
