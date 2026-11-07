ASSET := ParkingGarage
BLENDER := ./src/blender.sh
SEEDS ?= 101,202
CHECKPOINT_BLEND := build/ParkingGarage.blend
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_OUTPUTS := build/ParkingGarage.blend build/manifest.json export/ParkingGarage-101.gltf export/ParkingGarage-101.bin export/ParkingGarage-202.gltf export/ParkingGarage-202.bin export/ParkingGaragePieces.gltf
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_OUTPUTS := renders/checkpoint/.stamp
include ../kit/checkpoint_rules.mk

.PHONY: context matches repeat
build/context/.stamp: src/context_build.py src/dependencies.py
	$(PYTHON) src/dependencies.py
	@touch $@
context: build/context/.stamp
check: context
render: context
$(CHECKPOINT_RENDER_OUTPUTS): build/context/.stamp
matches: render
	$(PYTHON) src/matches.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose
repeat: model
	$(PYTHON) src/repeat.py
