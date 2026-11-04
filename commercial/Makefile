SEEDS ?= 101,102,103,104
CHECKPOINT_BLEND := build/station-101.blend
CHECKPOINT_OUTPUTS := $(foreach seed,101 102 103 104,build/station-$(seed).blend build/station-$(seed).glb build/station-$(seed).json)
CHECKPOINT_DEPS := $(addprefix src/,build.py building.py equipment.py geometry.py ground_adapter.py plan.py siteworks.py) ../kit/model.py ../kit/fonts.py ../ground/src/build.py ../ground/src/dimensions.py
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_RENDER_OUTPUTS := renders/checkpoint/hero.png renders/checkpoint/above.png renders/checkpoint/dispenser.png renders/checkpoint/canopy.png renders/checkpoint/entry.png renders/checkpoint/sign.png renders/checkpoint/rear.png renders/checkpoint/motion.png $(foreach seed,101 102 103 104,renders/checkpoint/seeds/$(seed)/above.png renders/checkpoint/seeds/$(seed)/street.png)
CHECKPOINT_RENDER_ARGS := --family --shots hero,above,dispenser,canopy,entry,sign,rear,motion
CHECKPOINT_CHECK = $(PYTHON) src/check_plan.py && $(BP) --python src/check.py -- --seeds $(SEEDS) --motion
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
include ../kit/checkpoint_rules.mk

.PHONY: match scale fit repeat context ground-context
context:
	$(PYTHON) src/context.py
ground-context:
	$(PYTHON) src/context.py --ground-only
check: ground-context
review: scale match
match: model refs
	$(PYTHON) src/prepare_refs.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/matches.py -- --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/matches --out renders/matches

scale: model context
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/station-101.glb --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES) --shots scale

fit: model
	$(BP) --python src/check_fit.py -- --reference $(TANK_REFERENCE)

repeat: model
	$(PYTHON) src/check_repeat.py --blender "$(BLENDER)"
