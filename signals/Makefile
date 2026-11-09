.DEFAULT_GOAL := all
.NOTPARALLEL:
.DELETE_ON_ERROR:
BLENDER ?= blender
PYTHON ?= python3
RUN := $(PYTHON) src/run_blender.py
KIT := $(abspath ../kit)
REPO := $(abspath ..)
BP := $(BLENDER) -t 2 -b --factory-startup --python-exit-code 1
RP := $(BLENDER) -t 2 -b --factory-startup --python-exit-code 1
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
all: refs context textures model arterial export check render matches review finals docs
build/parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
preserve:
	$(PYTHON) src/preserve.py
context: preserve
	$(PYTHON) src/context.py
$(MAPS) &: src/textures.py src/graphics.py src/plan.py build/parameters.txt
	$(PYTHON) src/graphics.py
	$(PYTHON) src/textures.py fields --wear $(WEAR)
	$(KIT)/with_gpu.sh $(RUN) --report build/memory/bake.json -- $(BP) --python src/textures.py -- bake
	$(PYTHON) src/textures.py ship
textures: $(MAPS)
$(MODELS) &: $(MODELDEPS) $(MAPS) | context
	$(RUN) --report build/memory/model.json -- $(BP) --python src/build.py -- --out build/Signals-201.blend
model: $(MODELS)
build/delivery.json: $(MODELS) src/deliver.py
	$(PYTHON) src/deliver.py
export: build/delivery.json
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: export arterial check-repo preserve
	$(PYTHON) src/check_delivery.py
	$(BP) --python src/check.py
	$(BP) --python src/construction.py
	$(BP) --python src/check_layout.py
	$(BP) --python src/check_arterial.py
	$(PYTHON) src/budget_report.py
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='$(WIDTH) $(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
renders/checkpoint/.stamp: build/delivery.json src/render.py src/setting.py src/layout.py ../ground/src/junction.py ../ground/src/junction_surfaces.py build/render-parameters.txt
	@for seed in $(SEEDS); do $(KIT)/with_gpu.sh $(RUN) --report build/memory/checkpoint-$$seed.json -- $(RP) --python src/render.py -- --source export/Signals-201.gltf --out renders/checkpoint --seeds $$seed --width $(WIDTH) --samples $(SAMPLES) || exit $$?; done
	$(KIT)/with_gpu.sh $(RP) --python src/lens_compare.py
	@touch $@
render: renders/checkpoint/.stamp
build/cameras.json: src/matches.py src/sidewalk_fit.py src/layout.py $(foreach n,$(SEEDS),build/Signals-$(n).json) | refs
	$(PYTHON) src/matches.py
build/pavement-camera.json: build/cameras.json src/pavement.py
	$(PYTHON) src/pavement.py camera
renders/matches/.stamp: build/delivery.json build/cameras.json build/pavement-camera.json src/render.py src/setting.py build/render-parameters.txt
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	@for seed in $(SEEDS); do $(KIT)/with_gpu.sh $(RUN) --report build/memory/matches-$$seed.json -- $(RP) --python src/render.py -- --source export/Signals-201.gltf --out renders/matches --seeds $$seed --camera-file build/cameras.json --width $(WIDTH) --samples $(SAMPLES) || exit $$?; done
	$(KIT)/with_gpu.sh $(RP) --python src/render.py -- --source export/Signals-201.gltf --out renders/matches --seeds 201 --camera-file build/pavement-camera.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose
	$(PYTHON) src/pavement.py compose
	@touch $@
matches: renders/matches/.stamp renders/source-matches/.stamp
review: render matches
	$(PYTHON) src/review.py --out renders/checkpoint
repeat: export
	$(PYTHON) src/repeat.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders/checkpoint','renders/matches','renders/source-matches','renders/final','renders/final-fixes')]"

build/sites.json: src/layout.py
	$(PYTHON) src/layout.py
../ground/export/ArterialSites.glb: build/sites.json ../ground/src/junction.py ../ground/src/junction_surfaces.py
	$(RUN) --report build/memory/arterial.json -- $(BP) --python ../ground/src/junction.py -- --spec build/sites.json --out $@
.PHONY: arterial
arterial: ../ground/export/ArterialSites.glb

renders/source-matches/.stamp: $(MODELS) build/cameras.json build/pavement-camera.json src/render.py src/setting.py build/render-parameters.txt
	@for seed in $(SEEDS); do $(KIT)/with_gpu.sh $(RUN) --report build/memory/source-matches-$$seed.json -- $(RP) --python src/render.py -- --source build/Signals-201.blend --out renders/source-matches --seeds $$seed --camera-file build/cameras.json --width $(WIDTH) --samples $(SAMPLES) || exit $$?; done
	$(KIT)/with_gpu.sh $(RP) --python src/render.py -- --source build/Signals-201.blend --out renders/source-matches --seeds 201 --camera-file build/pavement-camera.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose --renders renders/source-matches
	$(PYTHON) src/pavement.py compose --folder renders/source-matches
	@touch $@

# Final presentation remains serial and reads only exported shared-image parts.
GALLERY_PARTS := Head_three Head_fya PedHead PushButtonPost MastArm Pedestal Cabinet
GALLERY_OUTPUTS := $(foreach p,$(GALLERY_PARTS),$(foreach v,front side back top,renders/final/gallery/$(p)/$(v).png))
renders/final/gallery/.stamp $(GALLERY_OUTPUTS) &: build/delivery.json src/gallery.py build/render-parameters.txt
	@for part in $(GALLERY_PARTS); do $(KIT)/with_gpu.sh $(RUN) --report build/memory/gallery-$$part.json -- $(RP) --python src/gallery.py -- --parts $$part --width 1200 --samples $(SAMPLES) || exit $$?; done
	@touch renders/final/gallery/.stamp
renders/final/scale/.stamp renders/final/scale/MastArm/scale.png &: build/delivery.json src/gallery.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/gallery.py -- --parts MastArm --scale --out renders/final/scale --width $(WIDTH) --samples $(SAMPLES)
	@touch renders/final/scale/.stamp
renders/final/motion/.stamp renders/final/motion/green_fya_on.png renders/final/motion/green_fya_off.png renders/final/motion/yellow.png renders/final/motion/red.png &: build/delivery.json src/gallery.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/gallery.py -- --parts Head_three --motion --out renders/final/motion --width 800 --samples $(SAMPLES)
	@touch renders/final/motion/.stamp
renders/final/eevee/.stamp renders/final/eevee/202/hero.png &: renders/checkpoint/.stamp src/render.py
	$(KIT)/with_gpu.sh $(RP) --python src/render.py -- --source export/Signals-201.gltf --out renders/final/eevee --seeds 202 --shots hero --engine BLENDER_EEVEE --width $(WIDTH) --samples $(SAMPLES)
	@touch renders/final/eevee/.stamp
.PHONY: finals docs
finals: review renders/final/gallery/.stamp $(GALLERY_OUTPUTS) renders/final/scale/MastArm/scale.png renders/final/motion/green_fya_on.png renders/final/motion/green_fya_off.png renders/final/motion/yellow.png renders/final/motion/red.png renders/final/eevee/202/hero.png renders/final/scale/.stamp renders/final/motion/.stamp renders/final/eevee/.stamp
	$(PYTHON) src/finals.py
	$(PYTHON) src/final_crops.py
docs: finals
	$(PYTHON) src/finals.py --docs

# Opt-in chains of independently placed equipment; preserve all LOD0 payloads.
LOD_CONFIGS := src/lod-cabinet.json src/lod-mast-arm.json
include ../kit/lod_rules.mk
