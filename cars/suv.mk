# X220 source form plus detail/look checkpoint. UV/bake/delivery remain later.
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
BP := $(BLENDER) -t 1 -b --factory-startup --python-exit-code 1
RP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1600
SAMPLES ?= 40
PASS ?= suv-detail-form
OUT := renders/$(PASS)
DEPS := src/suv_build.py src/suv_body.py src/suv_spec.py src/suv_apertures.py src/suv_character.py src/suv_greenhouse.py src/suv_cladding.py src/suv_sculpt.py src/suv_optimize.py src/suv_resample.py src/build.py src/forms.py src/wheels.py src/detail_helpers.py ../kit/model.py ../kit/vehicle.py
CLAY := front_three_quarter rear_three_quarter side front rear top side_raking
STRIPES := stripes_horizontal stripes_vertical stripes_rear_horizontal stripes_rear_vertical stripes_side_horizontal stripes_side_vertical stripes_hood_driver
PAIRS := crv_front rav4_front crv_rear rav4_rear
.NOTPARALLEL:
.PHONY: all model refs check check-repeat render fairness review FORCE
all: detail-check detail-render detail-review
build/suv/game.blend: $(DEPS)
	@mkdir -p build/suv $(TMPDIR)
	$(BP) --python src/suv_build.py -- --out $@ --quality game
build/suv/high.blend: $(DEPS)
	@mkdir -p build/suv $(TMPDIR)
	$(BP) --python src/suv_build.py -- --out $@ --quality high
model: build/suv/game.blend build/suv/high.blend
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only suv-crv-front.jpg suv-crv-rear.jpg suv-crv-side.jpg suv-crv-back.jpg suv-rav4-front.jpg suv-rav4-rear.jpg suv-rav4-side.jpg suv-rav4-back.jpg suv-rav4-specs.pdf suv-rav4-uk.pdf suv-rav4-plan.pdf suv-crv-plan.pdf suv-rav4-face.jpg suv-crv-face.jpg suv-used-crv-front.jpg suv-used-rav4-rear.jpg
build/suv/cameras.json: src/suv_matches.py src/suv_spec.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/suv_matches.py --out $@
build/suv/profile-cameras.json: src/suv_profile_matches.py src/suv_spec.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/suv_profile_matches.py --out $@
build/suv/form-check.json: build/suv/game.blend src/suv_check.py src/suv_measure.py src/suv_round2_measure.py src/suv_round3_measure.py src/suv_fairness.py
	$(BP) --python src/suv_check.py -- --source $< --out $@
build/suv/curvature.json: build/suv/game.blend src/suv_fairness.py
	$(BP) --python src/suv_fairness.py -- --source $< --out $@
build/suv/parent-curvature.json: build/suv/game.blend src/suv_fairness.py
	$(BP) --python src/suv_fairness.py -- --source $< --out $@ --parent
fairness: build/suv/curvature.json build/suv/parent-curvature.json
	$(PYTHON) src/suv_curvature_plot.py --report build/suv/curvature.json --out $(OUT)
	$(PYTHON) src/suv_curvature_plot.py --report build/suv/parent-curvature.json --out $(OUT)/parent
check-form: model refs build/suv/cameras.json build/suv/profile-cameras.json build/suv/form-check.json fairness
	$(BP) --python $(KIT)/audit.py -- --source build/suv/game.blend --config src/suv_config.py --out build/suv/game-audit.json
	$(BP) --python $(KIT)/audit.py -- --source build/suv/high.blend --config src/suv_config.py --out build/suv/high-audit.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/suv/cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/suv/profile-cameras.json
	$(PYTHON) $(KIT)/repo_check.py
check-repeat: build/suv/game.blend
	$(BP) --python src/suv_build.py -- --out build/suv/repeat.blend --quality game
	$(BP) --python src/suv_repro.py -- --source build/suv/game.blend --repeat build/suv/repeat.blend --out build/suv/repeat-check.json
build/suv/parameters.txt: FORCE
	@mkdir -p build/suv $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) out=$(OUT)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
# Measurements validate the same source hash; changing a reported measurement
# cannot change the rendered pixels. Keep that check as an ordering barrier.
$(addprefix $(OUT)/,$(addsuffix .png,$(CLAY))) &: build/suv/game.blend src/suv_render.py build/suv/parameters.txt | build/suv/form-check.json
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source build/suv/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode clay
$(addprefix $(OUT)/,$(addsuffix .png,$(STRIPES))) &: build/suv/game.blend src/suv_render.py build/suv/parameters.txt | build/suv/form-check.json
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source build/suv/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode stripes
$(addprefix $(OUT)/,$(addsuffix .png,$(PAIRS))) &: build/suv/game.blend build/suv/cameras.json src/suv_render.py build/suv/parameters.txt | build/suv/form-check.json
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source build/suv/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode pairs --cameras build/suv/cameras.json
$(addprefix $(OUT)/,$(addsuffix _clay.png,$(PAIRS))) &: build/suv/game.blend build/suv/cameras.json src/suv_render.py build/suv/parameters.txt | build/suv/form-check.json
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source build/suv/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode comparisons --cameras build/suv/cameras.json
$(OUT)/rav4_profile.png $(OUT)/crv_profile.png &: build/suv/game.blend build/suv/profile-cameras.json src/suv_render.py build/suv/parameters.txt | build/suv/form-check.json
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source build/suv/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode profiles --cameras build/suv/profile-cameras.json
render: $(OUT)/rav4_profile.png $(OUT)/crv_profile.png $(addprefix $(OUT)/,$(addsuffix .png,$(CLAY) $(STRIPES) $(PAIRS))) $(addprefix $(OUT)/,$(addsuffix _clay.png,$(PAIRS)))
review: render fairness curvature-map diagnostic-stripes
	@mkdir -p $(REPO)/build/suv-reference-pages
	pdftoppm -f 1 -singlefile -scale-to 1800 -png refs/suv-rav4-plan.pdf $(REPO)/build/suv-reference-pages/suv-rav4-plan
	pdftoppm -f 1 -singlefile -scale-to 1800 -png refs/suv-crv-plan.pdf $(REPO)/build/suv-reference-pages/suv-crv-plan
	$(PYTHON) src/suv_references.py --refs refs --out $(OUT)/measurements --plan-pages $(REPO)/build/suv-reference-pages
	$(PYTHON) src/suv_review.py --renders $(OUT) --report build/suv/form-check.json --cameras build/suv/cameras.json

# Mean curvature uses the exact game triangles, including their sampling error.
.PHONY: curvature-map diagnostic-stripes
build/suv/mean-curvature/mean-curvature.blend: build/suv/game.blend src/suv_curvature_map.py
	$(BP) --python src/suv_curvature_map.py -- --source $< --out build/suv/mean-curvature
CURVATURE_VIEWS := front_three_quarter rear_three_quarter side front rear
curvature-map: $(addprefix $(OUT)/mean_curvature_,$(addsuffix .png,$(CURVATURE_VIEWS)))
$(addprefix $(OUT)/mean_curvature_,$(addsuffix .png,$(CURVATURE_VIEWS))) &: build/suv/mean-curvature/mean-curvature.blend src/suv_render.py build/suv/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source $< --out $(OUT) --width $(WIDTH) --samples 16 --mode curvature
diagnostic-stripes: $(addprefix $(OUT)/curvature_stripes_,$(addsuffix .png,$(CURVATURE_VIEWS)))
$(addprefix $(OUT)/curvature_stripes_,$(addsuffix .png,$(CURVATURE_VIEWS))) &: build/suv/game.blend src/suv_render.py build/suv/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source $< --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode diagnostic_stripes

empty :=
space := $(empty) $(empty)
comma := ,
include suv_detail.mk
check: detail-check
