# Source form/look-dev gates: six plans and Cycles critiques, before bake.
ifeq ($(TYPE),cape)
.DEFAULT_GOAL := cape-lookdev
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
CAPE_SEED ?= $(if $(SEED),$(SEED),36)
CAPE_SEEDS ?= 31,32,33,34,35,36
WIDTH ?= 1440
SAMPLES ?= 48
CAPE_SOURCE_DEPS := src/cape_plan.py src/cape_build.py src/cape_check.py src/cape_lookdev.py src/cape_surfaces.py src/cape_shingle_fields.py src/cape_masonry.py src/cape_age.py src/cape_profile.py src/cape_sweep.py src/build.py src/plan.py src/ranch_build.py src/ranch_drain.py src/ranch_lookdev.py src/ranch_fields.py src/additions.py src/lookdev.py src/textures.py src/check_mesh.py src/glb_budget.py $(KIT)/model.py $(KIT)/tiling.py $(KIT)/materials.py
CAPE_RENDER_DEPS := src/cape_render.py src/cape_reflections.py src/render.py src/ranch_render.py
comma := ,
CAPE_IDS := $(subst $(comma), ,$(CAPE_SEEDS))
CAPE_MODELS := $(foreach seed,$(CAPE_IDS),build/cape/form-$(seed).blend build/cape/form-$(seed).glb build/cape/form-$(seed).json build/cape/house-$(seed).blend build/cape/house-$(seed).json) build/cape/authored-lookdev.blend build/cape/authored-lookdev.json
CAPE_VIEWS := $(addprefix renders/cape/checkpoint/,$(addsuffix .png,hero back roof dormer eave entry scale)) $(foreach seed,$(CAPE_IDS),renders/cape/checkpoint/seeds/$(seed)/front.png renders/cape/checkpoint/seeds/$(seed)/rear.png)
.NOTPARALLEL:
.PHONY: cape-checkpoint model check refs render matches review FORCE
build/cape/parameters.txt: FORCE
	@mkdir -p build/cape $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seeds=$(CAPE_SEEDS) hero=$(CAPE_SEED) plan=$(PLAN)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/cape/shared-source.stamp:
	@test -f textures/source/T_HouseTrim_BaseColor.png || ($(PYTHON) src/bake_family.py source --size 4096 && $(PYTHON) src/bake_family.py filter-source)
	@mkdir -p build/cape
	@touch $@
$(CAPE_MODELS) build/cape/checks.json &: $(CAPE_SOURCE_DEPS) build/cape/parameters.txt build/cape/shared-source.stamp $(PLAN)
	$(BP) --python src/cape_sweep.py -- --seeds $(CAPE_SEEDS) $(if $(PLAN),--plan $(PLAN))
model: $(CAPE_MODELS) build/cape/checks.json
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only cape-midatl-leaf.jpg cape-northeast-spring.jpg cape-ne-summer.jpg cape-ne-rear.jpg cape-midwest-survey.pdf cape-midatl-summer.jpg cape-midatl-dormers.jpg cape-midatl-plain.jpg cape-plan-1940.jpg
	$(PYTHON) src/cape_refs.py
build/cape/plan-sweep.json: src/plan.py src/cape_plan.py src/cape_check.py src/check_plan.py src/ranch_plan.py
	$(PYTHON) src/check_plan.py --count 1000 --out $@
build/cape/regression/comparison.json: src/plan.py src/build.py src/ranch_build.py src/cape_regression.py src/regression_payload.py src/cape_baseline.json
	$(BP) --python src/cape_regression.py --
check: model build/cape/plan-sweep.json build/cape/regression/comparison.json
	$(PYTHON) src/cape_memory.py
	$(PYTHON) $(KIT)/repo_check.py
build/cape/cameras.json: src/cape_photo_matches.py src/cape_plan.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/cape_photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
build/cape/render-parameters.txt: FORCE
	@mkdir -p build/cape
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) hero=$(CAPE_SEED)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(CAPE_VIEWS) &: $(CAPE_MODELS) $(CAPE_RENDER_DEPS) build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_render.py -- --seed $(CAPE_SEED) --out renders/cape/checkpoint --family --seeds $(CAPE_SEEDS) --width $(WIDTH) --samples $(SAMPLES)
renders/cape/checkpoint/comparison/types.png: $(CAPE_MODELS) $(CAPE_RENDER_DEPS) build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_render.py -- --seed $(CAPE_SEED) --out renders/cape/checkpoint/comparison --shots types --types --width 1800 --samples $(SAMPLES)
render: $(CAPE_VIEWS) renders/cape/checkpoint/comparison/types.png
renders/cape/matches/cape_dormers.png renders/cape/matches/cape_plain.png &: $(CAPE_MODELS) build/cape/cameras.json $(CAPE_RENDER_DEPS) build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_render.py -- --source build/cape/house-36.blend --out renders/cape/matches --camera-file build/cape/cameras.json --shots cape_dormers --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/cape_render.py -- --source build/cape/house-33.blend --out renders/cape/matches --camera-file build/cape/cameras.json --shots cape_plain --width $(WIDTH) --samples $(SAMPLES)
matches: refs renders/cape/matches/cape_dormers.png renders/cape/matches/cape_plain.png
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cape/cameras.json --renders renders/cape/matches --out renders/cape/matches
review: render matches
	$(PYTHON) src/cape_present.py renders/cape/checkpoint
cape-checkpoint: refs model check review

# Current gate. The previous form presentation remains independently available.
CAPE_LOOK_ROOT := renders/cape/lookdev/checkpoint
CAPE_LOOK_VIEWS := $(addprefix $(CAPE_LOOK_ROOT)/,$(addsuffix .png,hero back roof dormer eave entry scale foundation peeling)) $(foreach seed,$(CAPE_IDS),$(foreach view,front rear siding,$(CAPE_LOOK_ROOT)/seeds/$(seed)/$(view).png)) $(foreach seed,32 35,$(CAPE_LOOK_ROOT)/seeds/$(seed)/hero.png $(CAPE_LOOK_ROOT)/seeds/$(seed)/connector.png) $(CAPE_LOOK_ROOT)/seeds/32/tired.png $(CAPE_LOOK_ROOT)/comparison/types.png $(CAPE_LOOK_ROOT)/painted_cedar/siding.png
CAPE_VALUE_ROOT := renders/cape/lookdev/values
CAPE_VALUE_IMAGES := $(addprefix $(CAPE_VALUE_ROOT)/,$(addsuffix .png,wood cedar roof vinyl aluminum cement concrete trim brick glass))
CAPE_PHOTO_FITS := $(addprefix refs/cape-used-white-,$(addsuffix -balanced.jpg,wood roof trim brick glass)) refs/cape-northeast-spring-concrete-balanced.jpg refs/cape-used-brown-cedar-balanced.jpg refs/cape-used-metal-aluminum-balanced.jpg refs/cape-used-striated-cement-balanced.jpg refs/cape-used-vinyl-houses-vinyl-balanced.jpg
CAPE_VALUE_REFS := $(addprefix refs/,$(addsuffix .jpg,cape-used-white cape-used-brown cape-used-metal cape-used-striated cape-used-vinyl-houses cape-northeast-spring))
.PHONY: cape-lookdev lookdev-render lookdev-values lookdev-review cape-context
cape-context: build/cape/shared-source.stamp
	$(BP) --python src/cape_context.py --
$(CAPE_VALUE_REFS):
	$(PYTHON) $(KIT)/fetch_refs.py refs --only $(@F)
build/cape/material-photos.json $(CAPE_PHOTO_FITS) &: src/cape_values.py refs/SOURCES.md $(CAPE_VALUE_REFS)
	$(PYTHON) $(KIT)/fetch_refs.py refs --only cape-used-white.jpg cape-used-brown.jpg cape-used-metal.jpg cape-used-striated.jpg cape-used-vinyl-houses.jpg cape-northeast-spring.jpg
	$(PYTHON) src/cape_values.py --prepare
$(CAPE_LOOK_VIEWS) &: $(CAPE_MODELS) $(CAPE_RENDER_DEPS) src/cape_checkpoint_render.py build/cape/render-parameters.txt | cape-context
	$(KIT)/with_gpu.sh $(BP) --python src/cape_checkpoint_render.py -- --out $(CAPE_LOOK_ROOT) --width $(WIDTH) --samples $(SAMPLES)
build/cape/value-render-parameters.txt: FORCE
	@mkdir -p build/cape
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=800 samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(CAPE_VALUE_IMAGES) &: $(CAPE_MODELS) $(CAPE_RENDER_DEPS) src/cape_value_render.py build/cape/material-photos.json build/cape/value-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_value_render.py -- --out $(CAPE_VALUE_ROOT) --width 800 --samples $(SAMPLES)
$(CAPE_VALUE_ROOT)/values.json: $(CAPE_VALUE_IMAGES) src/cape_values.py build/cape/material-photos.json
	$(PYTHON) src/cape_values.py --folder $(CAPE_VALUE_ROOT)
lookdev-render: $(CAPE_LOOK_VIEWS)
lookdev-values: $(CAPE_VALUE_ROOT)/values.json
lookdev-review: lookdev-render lookdev-values matches
	$(PYTHON) src/cape_present.py $(CAPE_LOOK_ROOT)
	$(PYTHON) src/cape_lookdev_check.py
cape-lookdev: refs model check lookdev-review
include src/cape_delivery.mk
endif
