CHECKPOINT_BLEND := build/river.blend
CHECKPOINT_OUTPUTS := build/river.blend build/manifest.json export/RiverCrossing-101.gltf export/RiverCrossing-202.gltf export/RiverModules.gltf
CHECKPOINT_DEPS := $(wildcard src/*.py) textures/checkpoint/.stamp build/preservation.json build/dependencies.json
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_ARGS := --seeds 101 202
WIDTH ?= 1280
SAMPLES ?= 32
include ../kit/checkpoint_rules.mk

refs: river-refs
.PHONY: river-refs
river-refs:
	$(PYTHON) src/fetch_refs.py

textures/checkpoint/.stamp: src/textures.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/textures.py
	@touch $@
build/preservation.json: src/preserve.py
	@mkdir -p build
	$(PYTHON) src/preserve.py --capture
build/dependencies.json: src/dependencies.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py

.PHONY: match repeat
match: render
	$(PYTHON) src/matches.py --compose
repeat: model
	$(PYTHON) src/repeat.py
