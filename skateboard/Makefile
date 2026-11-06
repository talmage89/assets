SEED ?= 0
STATE ?= season
WIDTH ?= 1440
SAMPLES ?= 40
PASS ?= checkpoint
CHECKPOINT_BLEND := build/skateboard.blend
CHECKPOINT_OUTPUTS := build/skateboard.blend build/skateboard.glb build/skateboard.json
CHECKPOINT_ARGS := --seed $(SEED) --state $(STATE)
CHECKPOINT_OUT := renders/$(PASS)
CHECKPOINT_SHOTS := hero top bottom side front concave_section truck truck_inner wheel_bearing tail_plies grip_edge lean_left lean_center lean_right rest_wall scale
CHECKPOINT_RENDER_OUTPUTS := $(CHECKPOINT_OUT)/.stamp $(addprefix $(CHECKPOINT_OUT)/,$(addsuffix .png,$(CHECKPOINT_SHOTS)))
PAIR_NAMES := period_horizontal period_used period_mini
PAIR_OUTPUTS = renders/$(PASS)/pairs/.stamp $(foreach n,$(PAIR_NAMES),renders/$(PASS)/pairs/$(n).png renders/$(PASS)/pairs/$(n)-pair.jpg renders/$(PASS)/pairs/$(n)-calibration.jpg)
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --source $(CHECKPOINT_BLEND) --out build/check.json
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --renders $(CHECKPOINT_OUT)
include ../kit/checkpoint_rules.mk

.PHONY: match repeat variants
build/cameras.json: src/calibrate.py src/photo_matches.py build/skateboard.glb
	$(PYTHON) src/calibrate.py
$(PAIR_OUTPUTS) &: build/cameras.json build/skateboard.glb src/render.py build/checkpoint-render-parameters.txt
	../kit/with_gpu.sh $(BP) --python src/render.py -- --source build/skateboard.glb --out renders/$(PASS)/pairs --width $(WIDTH) --samples $(SAMPLES) --cameras build/cameras.json
	$(PYTHON) ../kit/photo_match.py compose --calibration build/cameras.json --renders renders/$(PASS)/pairs --out renders/$(PASS)/pairs
	@touch renders/$(PASS)/pairs/.stamp
match: refs model $(PAIR_OUTPUTS)
review: match
repeat: model
	$(BP) --python src/build.py -- --seed $(SEED) --state $(STATE) --out build/repeat.blend
	$(PYTHON) src/repeat.py
variants:
	$(BP) --python src/build.py -- --seed 1 --out build/seed1.blend
	$(BP) --python src/build.py -- --seed 2 --out build/seed2.blend
	$(BP) --python src/build.py -- --seed 3 --out build/seed3.blend

.PHONY: sections check-variants
sections: model
	$(BP) --python src/sections.py -- --source $(CHECKPOINT_BLEND) --out build/sections.json
check: sections

check-variants: variants
	$(BP) --python src/check.py -- --source build/seed1.blend --out build/seed1-check.json
	$(BP) --python src/check.py -- --source build/seed2.blend --out build/seed2-check.json
	$(BP) --python src/check.py -- --source build/seed3.blend --out build/seed3-check.json

.PHONY: variant-renders
variant-renders: check-variants
	../kit/with_gpu.sh $(BP) --python src/render.py -- --source build/seed1.glb --out renders/seeds/seed1 --width 1000 --samples 24 --shots hero
	../kit/with_gpu.sh $(BP) --python src/render.py -- --source build/seed2.glb --out renders/seeds/seed2 --width 1000 --samples 24 --shots hero
	../kit/with_gpu.sh $(BP) --python src/render.py -- --source build/seed3.glb --out renders/seeds/seed3 --width 1000 --samples 24 --shots hero,side
