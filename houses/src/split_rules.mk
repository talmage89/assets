# Source look-development checkpoint only. Intentionally stops before bake.
ifeq ($(TYPE),split)
.DEFAULT_GOAL := split-checkpoint
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
WIDTH ?= 1440
SAMPLES ?= 40
SEED ?= 51
SEEDS ?= 51,52,53,54,55,56
SPLIT_SOURCE := $(filter-out src/split_checkpoint.py src/split_render.py src/split_present.py src/split_photo_matches.py src/split_photo_audit.py src/split_pair_refs.py src/split_values.py src/split_value_render.py,$(wildcard src/*.py))
SPLIT_RENDER := src/split_checkpoint.py src/split_render.py src/render.py src/cape_render.py src/cape_reflections.py src/ranch_render.py src/split_context.py
SPLIT_ROOT := renders/split/lookdev/checkpoint
comma := ,
SPLIT_IDS := $(subst $(comma), ,$(SEEDS))
SPLIT_MODELS := $(foreach s,$(SPLIT_IDS),build/split/form-$(s).blend build/split/form-$(s).glb build/split/form-$(s).json build/split/house-$(s).blend build/split/house-$(s).json)
.NOTPARALLEL:
.PHONY: split-checkpoint model check refs render matches values review FORCE regression
build/split/parameters.txt: FORCE
	@mkdir -p build/split $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seeds=$(SEEDS) plan=$(PLAN)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/split/shared-source.stamp:
	@test -f textures/source/T_HouseTrim_BaseColor.png || ($(PYTHON) src/bake_family.py source --size 4096 && $(PYTHON) src/bake_family.py filter-source)
	@mkdir -p build/split
	@touch $@
$(SPLIT_MODELS) build/split/checks.json &: $(SPLIT_SOURCE) build/split/parameters.txt build/split/shared-source.stamp $(PLAN)
	$(BP) --python src/split_sweep.py -- --seeds $(SEEDS) $(if $(PLAN),--plan $(PLAN))
model: $(SPLIT_MODELS) build/split/checks.json
build/split/pair-references.json build/split/material-photos.json &: src/split_pair_refs.py src/split_values.py src/split_refs.py refs/SOURCES.md
	$(PYTHON) src/split_refs.py
	$(PYTHON) src/split_pair_refs.py
	$(PYTHON) src/split_values.py --prepare
refs: build/split/pair-references.json build/split/material-photos.json
build/split/plan-sweep.json: src/plan.py src/split_plan.py src/split_check.py src/check_plan.py src/cape_plan.py src/ranch_plan.py
	$(PYTHON) src/check_plan.py --count 1000 --out $@
build/split/regression/comparison.json: $(SPLIT_SOURCE) src/split_baseline.json src/split_regression.py
	$(BP) --python src/split_regression.py --
regression: build/split/regression/comparison.json
check: model build/split/plan-sweep.json regression
	$(PYTHON) src/split_present.py --check-only
	$(PYTHON) $(KIT)/repo_check.py
build/split/cameras-look.json: src/split_photo_matches.py src/split_plan.py $(KIT)/photo_match.py build/split/pair-references.json
	$(PYTHON) $(KIT)/photo_match.py solve --config src/split_photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
build/split/photo-audit.json: src/split_photo_audit.py build/split/cameras-look.json
	$(PYTHON) src/split_photo_audit.py
build/split/render-parameters.txt: FORCE
	@mkdir -p build/split
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(SPLIT_ROOT)/main.stamp: $(SPLIT_MODELS) $(SPLIT_RENDER) build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_checkpoint.py -- --group main --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
render: $(SPLIT_ROOT)/main.stamp
$(SPLIT_ROOT)/pairs.stamp: $(SPLIT_MODELS) $(SPLIT_RENDER) build/split/cameras-look.json build/split/photo-audit.json build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_checkpoint.py -- --group pairs --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/split/cameras-look.json --renders $(SPLIT_ROOT)/clay --out $(SPLIT_ROOT)/clay
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/split/cameras-look.json --renders $(SPLIT_ROOT)/look --out $(SPLIT_ROOT)/look
	@touch $@
matches: $(SPLIT_ROOT)/pairs.stamp
$(SPLIT_ROOT)/values.stamp: $(SPLIT_MODELS) $(SPLIT_RENDER) src/split_value_render.py src/split_values.py src/cape_value_render.py build/split/material-photos.json build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_checkpoint.py -- --group values --samples $(SAMPLES)
	$(PYTHON) src/split_values.py --folder $(SPLIT_ROOT)/values
	@touch $@
values: $(SPLIT_ROOT)/values.stamp
review: render matches values
	$(PYTHON) src/split_present.py
split-checkpoint: refs model check review
endif
