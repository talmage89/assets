SEEDS ?= 101,202,303
CHECKPOINT_BLEND := build/Playground.blend
CHECKPOINT_OUTPUTS := build/Playground.blend build/manifest.json export/Playground-101.gltf export/Playground-202.gltf export/Playground-303.gltf export/PlaygroundPieces.gltf
CHECKPOINT_DEPS := $(wildcard src/*.py) ../kit/model.py
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --out build/check.json
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_ARGS := --seeds $(SEEDS)
WIDTH ?= 1200
SAMPLES ?= 24
include ../kit/checkpoint_rules.mk
.PHONY: match repeat
all: match
match: model refs
	$(PYTHON) src/photo_matches.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/matches --out renders/checkpoint/matches
	$(CHECKPOINT_REVIEW)
repeat: model
	$(PYTHON) src/repeat.py
