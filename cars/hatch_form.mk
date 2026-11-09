# H120 source form checkpoint. No detail, textures or hatch GLB at this gate.
.DEFAULT_GOAL := all
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
PASS ?= hatch-round4
OUT := renders/$(PASS)
HDEPS := src/hatch_build.py src/hatch_body.py src/hatch_apertures.py src/hatch_character.py src/hatch_spec.py src/build.py src/forms.py src/wheels.py src/detail_helpers.py ../kit/model.py ../kit/vehicle.py
HDEPS += src/regular_chart.py
CLAY := front_three_quarter rear_three_quarter side front rear top side_raking
STRIPES := stripes_horizontal stripes_vertical stripes_rear_horizontal stripes_rear_vertical stripes_side_horizontal stripes_side_vertical stripes_hood_driver stripes_rear_unpainted
PAIRS := corolla_front corolla_rear hyundai_front hyundai_rear corolla_side hyundai_side
COMPARISONS := $(addsuffix _clay,$(PAIRS))
MAPVIEWS := front_three_quarter rear_three_quarter side front rear
GLOSS := $(addprefix gloss_,side front_three_quarter rear_three_quarter rear $(PAIRS))
MAPS := $(addprefix curvature_,$(MAPVIEWS))
MAPSTRIPES := $(addprefix map_stripes_,$(MAPVIEWS))
.NOTPARALLEL:
.DELETE_ON_ERROR:
.PHONY: all model refs check render review fairness baseline FORCE
all: refs model check render review
build/hatch/parameters.txt: FORCE
	@mkdir -p build/hatch $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) out=$(OUT)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/hatch/game.blend: $(HDEPS)
	@mkdir -p build/hatch $(TMPDIR)
	$(BP) --python src/hatch_build.py -- --quality game --out $@
build/hatch/high.blend: $(HDEPS)
	@mkdir -p build/hatch $(TMPDIR)
	$(BP) --python src/hatch_build.py -- --quality high --out $@
model: build/hatch/game.blend build/hatch/high.blend
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only hatch-corolla-front.jpg hatch-corolla-rear.jpg hatch-corolla-side.jpg hatch-corolla-back.jpg hatch-hyundai-front.jpg hatch-hyundai-rear.jpg hatch-hyundai-side.jpg hatch-hyundai-back.jpg hatch-corolla-specs.pdf hatch-hyundai-specs.pdf hatch-hyundai-au.pdf hatch-corolla-drawing.pdf hatch-hyundai-drawing.pdf
build/hatch/cameras.json: src/hatch_matches.py src/hatch_spec.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/hatch_matches.py --out $@
build/hatch/form-check.json: build/hatch/game.blend src/hatch_check.py
	$(BP) --python src/hatch_check.py -- --source $< --out $@
build/hatch/character-check.json: build/hatch/game.blend src/hatch_character_check.py src/hatch_fairness.py src/hatch_body.py
	$(BP) --python src/hatch_character_check.py -- --source $< --out $@
build/hatch/round2-check.json: build/hatch/game.blend src/hatch_round2_check.py
	$(BP) --python src/hatch_round2_check.py -- --source $< --out $@
build/hatch/round3-check.json: build/hatch/game.blend src/hatch_round3_check.py src/hatch_fairness.py
	$(BP) --python src/hatch_round3_check.py -- --source $< --out $@
build/hatch-round3-baseline/game.blend:
	$(PYTHON) src/hatch_round4_review.py --renders $(OUT) --cameras build/hatch/cameras.json --blender $(BLENDER) --baseline-model-only
build/hatch/round4-check.json: build/hatch/game.blend build/hatch-round3-baseline/game.blend src/hatch_round4_check.py src/hatch_curvature_map.py src/hatch_round3_check.py src/hatch_body.py
	$(BP) --python src/hatch_round4_check.py -- --source $< --baseline build/hatch-round3-baseline/game.blend --out $@ --parent
build/hatch/curvature.json: build/hatch/game.blend src/hatch_fairness.py
	$(BP) --python src/hatch_fairness.py -- --source $< --out $@
build/hatch/parent-curvature.json: build/hatch/game.blend src/hatch_fairness.py src/hatch_body.py
	$(BP) --python src/hatch_fairness.py -- --source $< --out $@ --parent
fairness: build/hatch/curvature.json build/hatch/parent-curvature.json
	$(PYTHON) src/hatch_curvature_plot.py --report build/hatch/curvature.json --out $(OUT)
	$(PYTHON) src/hatch_curvature_plot.py --report build/hatch/parent-curvature.json --out $(OUT)/parent
check: model refs build/hatch/cameras.json build/hatch/form-check.json build/hatch/character-check.json build/hatch/round2-check.json build/hatch/round3-check.json build/hatch/round4-check.json fairness
	$(BP) --python $(KIT)/audit.py -- --source build/hatch/game.blend --config src/hatch_config.py --out build/hatch/game-audit.json
	$(BP) --python $(KIT)/audit.py -- --source build/hatch/high.blend --config src/hatch_config.py --out build/hatch/high-audit.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/hatch/cameras.json
	$(PYTHON) $(KIT)/repo_check.py
$(addprefix $(OUT)/,$(addsuffix .png,$(CLAY))) &: build/hatch/game.blend build/hatch/form-check.json src/hatch_render.py build/hatch/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_render.py -- --source build/hatch/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode clay
$(addprefix $(OUT)/,$(addsuffix .png,$(STRIPES))) &: build/hatch/game.blend build/hatch/form-check.json src/hatch_render.py build/hatch/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_render.py -- --source build/hatch/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode stripes
$(addprefix $(OUT)/,$(addsuffix .png,$(PAIRS))) &: build/hatch/game.blend build/hatch/form-check.json build/hatch/cameras.json src/hatch_render.py build/hatch/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_render.py -- --source build/hatch/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode pairs --cameras build/hatch/cameras.json
$(addprefix $(OUT)/,$(addsuffix .png,$(COMPARISONS))) &: build/hatch/game.blend build/hatch/form-check.json build/hatch/cameras.json src/hatch_render.py build/hatch/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_render.py -- --source build/hatch/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode comparisons --cameras build/hatch/cameras.json
$(addprefix $(OUT)/,$(addsuffix .png,$(MAPS))) &: build/hatch/game.blend src/hatch_round4_render.py src/hatch_curvature_map.py build/hatch/parameters.txt
	$(BP) --python src/hatch_round4_render.py -- --source build/hatch/game.blend --out $(OUT) --mode curvature --width $(WIDTH)
$(addprefix $(OUT)/,$(addsuffix .png,$(GLOSS))) &: build/hatch/game.blend src/hatch_round4_render.py build/hatch/cameras.json build/hatch/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_round4_render.py -- --source build/hatch/game.blend --out $(OUT) --mode gloss --width $(WIDTH) --samples $(SAMPLES) --cameras build/hatch/cameras.json
$(addprefix $(OUT)/,$(addsuffix .png,$(MAPSTRIPES))) &: build/hatch/game.blend src/hatch_round4_render.py build/hatch/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_round4_render.py -- --source build/hatch/game.blend --out $(OUT) --mode map-stripes --width $(WIDTH) --samples $(SAMPLES)
render: $(addprefix $(OUT)/,$(addsuffix .png,$(CLAY) $(STRIPES) $(PAIRS) $(COMPARISONS) $(MAPS) $(GLOSS) $(MAPSTRIPES)))
renders/hatch-round1-overlays/baseline.json: src/hatch_baseline.py
	$(PYTHON) src/hatch_baseline.py --blender $(BLENDER) --model --renders renders/hatch-round1-overlays
baseline: renders/hatch-round1-overlays/baseline.json
review: render fairness baseline
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/hatch/cameras.json --renders $(OUT) --out $(OUT)
	$(PYTHON) src/hatch_review.py --renders $(OUT) --report build/hatch/form-check.json --cameras build/hatch/cameras.json
	$(PYTHON) src/hatch_round4_review.py --renders $(OUT) --cameras build/hatch/cameras.json --blender $(BLENDER) --width $(WIDTH) --samples $(SAMPLES)
