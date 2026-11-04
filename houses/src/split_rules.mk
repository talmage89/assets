# Form checkpoint only: no bake, final export, or portfolio publication.
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
SPLIT_SOURCE := src/split_plan.py src/split_build.py src/split_lookdev.py src/split_check.py src/split_sweep.py src/split_motion.py src/build.py src/plan.py src/cape_plan.py src/cape_build.py src/cape_profile.py src/ranch_build.py src/ranch_masonry.py src/ranch_drain.py src/ranch_lookdev.py src/ranch_fields.py src/cape_masonry.py src/lookdev.py src/textures.py src/additions.py src/check_mesh.py src/glb_budget.py
comma := ,
SPLIT_IDS := $(subst $(comma), ,$(SEEDS))
SPLIT_MODELS := $(foreach s,$(SPLIT_IDS),build/split/form-$(s).blend build/split/form-$(s).glb build/split/form-$(s).json build/split/house-$(s).blend build/split/house-$(s).json)
SPLIT_SHOTS := hero back levels side entry eave veneer garage roof scale
SPLIT_VIEWS := $(addprefix renders/split/checkpoint/,$(addsuffix .png,$(SPLIT_SHOTS))) $(foreach s,51 52 53 54 55 56,renders/split/checkpoint/seeds/$(s)/front.png renders/split/checkpoint/seeds/$(s)/rear.png)
.NOTPARALLEL:
.PHONY: split-checkpoint model check refs render matches review FORCE regression
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
refs:
	$(PYTHON) src/split_refs.py
build/split/plan-sweep.json: src/plan.py src/split_plan.py src/split_check.py src/check_plan.py src/cape_plan.py src/ranch_plan.py
	$(PYTHON) src/check_plan.py --count 1000 --out $@
build/split/regression/comparison.json: $(SPLIT_SOURCE) src/split_baseline.json src/split_regression.py
	$(BP) --python src/split_regression.py --
regression: build/split/regression/comparison.json
check: model build/split/plan-sweep.json regression
	$(PYTHON) src/split_present.py --check-only
	$(PYTHON) $(KIT)/repo_check.py
build/split/cameras.json: src/split_photo_matches.py src/split_plan.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/split_photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
build/split/render-parameters.txt: FORCE
	@mkdir -p build/split
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) seed=$(SEED)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(SPLIT_VIEWS) &: $(SPLIT_MODELS) src/split_render.py src/render.py build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_render.py -- --seed $(SEED) --out renders/split/checkpoint --family --width $(WIDTH) --samples $(SAMPLES)
renders/split/checkpoint/comparison/types.png: $(SPLIT_MODELS) src/split_render.py src/split_context.py build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_render.py -- --seed $(SEED) --out renders/split/checkpoint/comparison --shots types --types --width 2400 --samples $(SAMPLES)
render: $(SPLIT_VIEWS) renders/split/checkpoint/comparison/types.png
renders/split/matches/split_side.png renders/split/matches/split_foyer.png &: $(SPLIT_MODELS) build/split/cameras.json src/split_render.py build/split/render-parameters.txt | refs
	$(KIT)/with_gpu.sh $(BP) --python src/split_render.py -- --seed 56 --out renders/split/matches --shots split_side --camera-file build/split/cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/split_render.py -- --seed 55 --out renders/split/matches --shots split_foyer --camera-file build/split/cameras.json --width $(WIDTH) --samples $(SAMPLES)
matches: renders/split/matches/split_side.png renders/split/matches/split_foyer.png
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/split/cameras.json --renders renders/split/matches --out renders/split/matches
review: render matches
	$(PYTHON) src/split_present.py
split-checkpoint: refs model check review
endif
