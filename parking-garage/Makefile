ASSET := ParkingGarage
BLENDER := ./src/blender.sh
SEEDS ?= 101,202
CHECKPOINT_BLEND := build/ParkingGarage.blend
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_OUTPUTS := build/ParkingGarage.blend build/manifest.json export/ParkingGarage-101.gltf export/ParkingGarage-101.bin export/ParkingGarage-202.gltf export/ParkingGarage-202.bin export/ParkingGaragePieces.gltf
CHECKPOINT_CHECK = $(BP) --python src/check.py && $(BP) --python src/motion_check.py && $(PYTHON) src/site_check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_OUTPUTS := $(foreach seed,101 202,$(foreach shot,hero above aisle ramp_turn top_deck entry tower scale,renders/checkpoint/$(seed)/$(shot).png)) renders/checkpoint/modules.png renders/checkpoint/.stamp
include ../kit/checkpoint_rules.mk

all: matches

.PHONY: context site matches repeat clean-family
build/context/.stamp: src/context_build.py src/dependencies.py
	$(PYTHON) src/dependencies.py
	@touch $@
context: build/context/.stamp
check: context
SITE_OUTPUTS := export/sites/ParkingGarageSite-101.gltf export/sites/ParkingGarageSite-101.bin export/sites/ParkingGarageSite-202.gltf export/sites/ParkingGarageSite-202.bin build/sites.json
$(SITE_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) build/context/.stamp src/site.py src/setting.py
	$(BP) --python src/site.py
site: $(SITE_OUTPUTS)
check: site
render: site
$(CHECKPOINT_RENDER_OUTPUTS): $(SITE_OUTPUTS)
matches: render
	$(PYTHON) src/matches.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose
repeat: model
	$(PYTHON) src/repeat.py
clean: clean-family
clean-family:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures/checkpoint')]"
