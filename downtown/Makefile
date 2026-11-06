# This family intentionally stops before look-dev, baking and final delivery.
WIDTH ?= 1440
SAMPLES ?= 32
CHECKPOINT_BLEND := build/downtown.blend
CHECKPOINT_OUTPUTS := build/downtown.blend build/downtown.json $(foreach r,midwest western northeast southern,build/blocks/$(r)/block.blend build/blocks/$(r)/block.glb build/blocks/$(r)/block.json)
CHECKPOINT_DEPS := src/build.py src/plan.py src/building.py src/geometry.py src/graphics.py
CHECKPOINT_CHECK = $(PYTHON) src/check_plan.py
CHECKPOINT_RENDER_ARGS := --with-matches
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_OUTPUTS := $(foreach r,midwest western northeast southern,export/DowntownStreet_$(r).glb) renders/checkpoint/.stamp $(foreach r,midwest western northeast southern,renders/checkpoint/$(r)/across.png renders/checkpoint/$(r)/above.png renders/checkpoint/$(r)/rear.png) renders/checkpoint/midwest/hero.png renders/checkpoint/midwest/storefront.png renders/checkpoint/midwest/window.png renders/checkpoint/midwest/cornice.png renders/checkpoint/midwest/corner.png renders/checkpoint/midwest/ghost.png renders/checkpoint/midwest/escape.png renders/checkpoint/southern/gallery.png
include ../kit/checkpoint_rules.mk
.PHONY: context matches check-mesh check-repeat
build/context/manifest.json: src/context.py src/context_build.py
	$(PYTHON) src/context.py
context: build/context/manifest.json
$(CHECKPOINT_RENDER_OUTPUTS): build/context/manifest.json build/cameras.json src/street.py src/geometry.py src/graphics.py
check: check-mesh
check-mesh: model
	$(BP) --python src/check.py
build/cameras.json: src/photo_matches.py src/matches.py $(CHECKPOINT_OUTPUTS)
	$(PYTHON) src/matches.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
renders/matches/.stamp: build/cameras.json src/render.py $(CHECKPOINT_OUTPUTS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --camera-file build/cameras.json --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/matches/raw --out renders/matches
	@touch $@
matches: refs model renders/matches/.stamp
review: matches

check-repeat: model
	$(PYTHON) src/repeat.py
.PHONY: check-sweep
check-sweep:
	$(BP) --python src/sweep.py
.PHONY: check-resources
check-resources: model
	$(BP) --python src/check_resources.py
check: check-resources

.PRECIOUS: $(CHECKPOINT_RENDER_OUTPUTS)
