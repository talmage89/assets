# Sedan form and detail checkpoint; the pickup graph stays independent.
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
# Fixed CPU evaluation for reproducible subdivision; free CPU denoising for views.
BP := $(BLENDER) -t 1 -b --factory-startup --python-exit-code 1
RP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1600
SAMPLES ?= 40
PASS ?= sedan-round6
OUT := renders/$(PASS)
SDEPS := src/build.py src/sedan_body.py src/sedan_apertures.py src/sedan_character.py src/sedan_fairness.py src/sedan_spec.py src/forms.py src/wheels.py src/detail_helpers.py ../kit/model.py ../kit/vehicle.py
CLAY := front_three_quarter rear_three_quarter side front rear top side_raking side_matched side_matched_wide side_matched_long
STRIPES := stripes_horizontal stripes_vertical stripes_rear_horizontal stripes_rear_vertical stripes_side_horizontal stripes_side_vertical stripes_hood_driver
PAIRS := accord_front camry_rear camry_front accord_rear
COMPARISONS := $(addsuffix _clay,$(PAIRS))
.DELETE_ON_ERROR:
.NOTPARALLEL:
.PHONY: all model refs check render review fairness FORCE
all: refs sedan-checkpoint
form: refs model check-form render review
build/sedan/parameters.txt: FORCE
	@mkdir -p build/sedan $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) out=$(OUT)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/sedan/game.blend: $(SDEPS)
	@mkdir -p build/sedan $(TMPDIR)
	$(BP) --python src/build.py -- --body sedan --form-only --quality game --out $@
build/sedan/high.blend: $(SDEPS)
	@mkdir -p build/sedan $(TMPDIR)
	$(BP) --python src/build.py -- --body sedan --form-only --quality high --out $@
model: build/sedan/game.blend build/sedan/high.blend
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only sedan-accord-front.jpg sedan-accord-rear.jpg sedan-camry-front.jpg sedan-camry-rear.jpg sedan-camry-side.jpg sedan-camry-specs.pdf sedan-mondeo-specs.pdf sedan-used-front.jpg sedan-used-rear.jpg sedan-color-popularity.pdf
build/sedan/cameras.json: src/sedan_matches.py src/sedan_spec.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/sedan_matches.py --out $@
build/sedan/profile-camera.json: src/sedan_profile_match.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config $< --out $@
build/sedan/form-check.json: build/sedan/game.blend src/sedan_check.py
	$(BP) --python src/sedan_check.py -- --source $< --out $@
build/sedan/shaping-check.json: build/sedan/game.blend src/sedan_shaping.py src/sedan_check.py
	$(BP) --python src/sedan_shaping.py -- --source $< --out $@
build/sedan/character-check.json: build/sedan/game.blend src/sedan_character_check.py src/sedan_fairness.py
	$(BP) --python src/sedan_character_check.py -- --source $< --out $@
build/sedan/rear-check.json: build/sedan/game.blend src/sedan_rear_check.py
	$(BP) --python src/sedan_rear_check.py -- --source $< --out $@
check-form: model refs build/sedan/cameras.json build/sedan/profile-camera.json build/sedan/form-check.json build/sedan/shaping-check.json build/sedan/character-check.json build/sedan/rear-check.json
	$(BP) --python $(KIT)/audit.py -- --source build/sedan/game.blend --config src/sedan_config.py --out build/sedan/game-audit.json
	$(BP) --python $(KIT)/audit.py -- --source build/sedan/high.blend --config src/sedan_config.py --out build/sedan/high-audit.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/sedan/cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/sedan/profile-camera.json
	$(PYTHON) $(KIT)/repo_check.py
$(addprefix $(OUT)/,$(addsuffix .png,$(CLAY))) &: build/sedan/game.blend build/sedan/form-check.json src/sedan_render.py build/sedan/profile-camera.json build/sedan/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_render.py -- --source build/sedan/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode clay
$(addprefix $(OUT)/,$(addsuffix .png,$(STRIPES))) &: build/sedan/game.blend build/sedan/form-check.json src/sedan_render.py build/sedan/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_render.py -- --source build/sedan/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode stripes
$(addprefix $(OUT)/,$(addsuffix .png,$(PAIRS))) &: build/sedan/game.blend build/sedan/form-check.json build/sedan/cameras.json src/sedan_render.py build/sedan/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_render.py -- --source build/sedan/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode pairs --cameras build/sedan/cameras.json
$(addprefix $(OUT)/,$(addsuffix .png,$(COMPARISONS))) &: build/sedan/game.blend build/sedan/form-check.json build/sedan/cameras.json src/sedan_render.py build/sedan/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_render.py -- --source build/sedan/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode comparisons --cameras build/sedan/cameras.json
render: $(addprefix $(OUT)/,$(addsuffix .png,$(CLAY) $(STRIPES) $(PAIRS) $(COMPARISONS)))
build/sedan/curvature.json: build/sedan/game.blend src/sedan_fairness.py
	$(BP) --python src/sedan_fairness.py -- --source $< --out $@
build/sedan/parent-curvature.json: build/sedan/game.blend src/sedan_fairness.py src/sedan_body.py
	$(BP) --python src/sedan_fairness.py -- --source $< --out $@ --parent
fairness: build/sedan/curvature.json build/sedan/parent-curvature.json
	$(PYTHON) src/sedan_curvature_plot.py --report build/sedan/curvature.json --out $(OUT)
	$(PYTHON) src/sedan_curvature_plot.py --report build/sedan/parent-curvature.json --out $(OUT)/parent
review: render fairness
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/sedan/cameras.json --renders $(OUT) --out $(OUT)
	$(PYTHON) src/sedan_review.py --renders $(OUT) --report build/sedan/form-check.json --cameras build/sedan/cameras.json

include sedan_detail.mk
