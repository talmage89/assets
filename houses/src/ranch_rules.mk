# The ranch stops at the requested source/form checkpoint, before any bake.
ifeq ($(TYPE),ranch)
.DEFAULT_GOAL := ranch-checkpoint
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
RANCH_SEED ?= $(if $(SEED),$(SEED),12)
RANCH_SEEDS ?= 11,12,13,14,15,16
export RANCH_SEED
export HOUSE_PLAN := $(PLAN)
WIDTH ?= 1440
SAMPLES ?= 48
.NOTPARALLEL:
.PHONY: ranch-checkpoint model check refs render matches review FORCE
build/ranch/parameters.txt: FORCE
	@mkdir -p build/ranch $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seeds=$(RANCH_SEEDS) plan=$(PLAN)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/ranch/shared-source.stamp:
	@test -f textures/source/T_HouseTrim_BaseColor.png || ($(PYTHON) src/bake_family.py source --size 4096 && $(PYTHON) src/bake_family.py filter-source)
	@mkdir -p build/ranch
	@touch $@
build/ranch/models.stamp: src/build.py src/plan.py src/ranch_plan.py src/ranch_build.py src/ranch_drain.py src/ranch_masonry.py src/ranch_fields.py src/additions.py src/lookdev.py src/ranch_lookdev.py src/textures.py src/ranch_sweep.py src/ranch_check.py src/ranch_revision_check.py src/check_mesh.py src/glb_budget.py build/ranch/parameters.txt build/ranch/shared-source.stamp $(PLAN)
	$(BP) --python src/ranch_sweep.py -- --seeds $(RANCH_SEEDS) $(if $(PLAN),--plan $(PLAN))
	@touch $@
model: build/ranch/models.stamp
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
build/ranch/plan-sweep.json: src/plan.py src/ranch_plan.py src/check_plan.py
	$(PYTHON) src/check_plan.py --count 1000 --out $@
build/ranch/colonial-regression/comparison.json: src/build.py src/plan.py src/additions.py src/ranch_regression.py src/colonial_baseline.json
	$(BP) --python src/ranch_regression.py --
check: model build/ranch/plan-sweep.json build/ranch/colonial-regression/comparison.json
	$(PYTHON) $(KIT)/repo_check.py
build/ranch/cameras.json: src/ranch_photo_matches.py src/ranch_plan.py build/ranch/parameters.txt
	$(PYTHON) $(KIT)/photo_match.py solve --config src/ranch_photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
build/ranch/render-parameters.txt: FORCE
	@mkdir -p build/ranch
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seed=$(RANCH_SEED) width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
renders/ranch/checkpoint/.stamp: build/ranch/models.stamp src/ranch_render.py src/ranch_present.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_present.py -- --seed $(RANCH_SEED) --seeds $(RANCH_SEEDS) --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
build/ranch/colonial-context.stamp: build/ranch/shared-source.stamp
	@test -f export/Hearthfield-27.gltf || $(MAKE) TYPE=builder_colonial SEED=27 PLAN= lookdev-model
	@touch $@
renders/ranch/checkpoint/comparison/.stamp: build/ranch/colonial-context.stamp build/ranch/models.stamp src/ranch_render.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_render.py -- --source build/ranch/house-$(RANCH_SEED).blend --out renders/ranch/checkpoint/comparison --shots types --comparison --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
render: renders/ranch/checkpoint/.stamp renders/ranch/checkpoint/comparison/.stamp
renders/ranch/matches/.stamp: build/ranch/models.stamp build/ranch/cameras.json src/ranch_render.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_render.py -- --source build/ranch/house-$(RANCH_SEED).blend --out renders/ranch/matches --shots ranch_summer,ranch_brick_picture,ranch_sun_oblique,ranch_sun_1960 --camera-file build/ranch/cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/ranch/cameras.json --renders renders/ranch/matches --out renders/ranch/matches
	@touch $@
matches: refs renders/ranch/matches/.stamp
review: render matches src/ranch_review.py src/ranch_values.py src/ranch_memory.py
	$(PYTHON) src/ranch_review.py
	$(PYTHON) src/ranch_memory.py
	@if [ "$(RANCH_SEED)" = "12" ] && [ -z "$(PLAN)" ]; then $(PYTHON) src/ranch_values.py; fi
ranch-checkpoint: refs model check review
endif

ifeq ($(TYPE),ranch)
include src/ranch_delivery.mk
endif
