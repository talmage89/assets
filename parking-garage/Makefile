ASSET := ParkingGarage
BLENDER := ./src/blender.sh
SEEDS ?= 101,202
CHECKPOINT_BLEND := build/ParkingGarage.blend
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_DEPS := src/build.py src/geometry.py src/pieces.py src/plan.py src/graphics.py ../kit/tiling.py ../kit/glb_textures.py ../kit/fonts.py ../kit/gltf.py
MODULE_NAMES := DoubleTee InvertedT LBeam ColumnCorbel CorbelPair ColumnPlain PTColumn PTSlab PTBeam Spandrel CableBarrier PTGuard Fixture WheelStop Drain Gate Ticket PayStation Tower Tower3 Tower5 StructuralBay EndBay RampBay PTStructuralBay
MODULE_FILES := $(foreach n,$(MODULE_NAMES),export/modules/$(n).gltf export/modules/$(n).bin)
CHECKPOINT_OUTPUTS := build/ParkingGarage.blend build/manifest.json build/modules.json build/graphics.json textures/checkpoint/T_GroundParkingTrim_BaseColor.png $(MODULE_FILES) export/ParkingGarage-101.gltf export/ParkingGarage-101.bin export/ParkingGarage-202.gltf export/ParkingGarage-202.bin export/ParkingGaragePieces.gltf export/ParkingGaragePieces.bin build/garage-101.json build/garage-202.json build/garage-101.blend build/garage-202.blend
CHECKPOINT_CHECK = $(BP) --python src/check_all.py
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
$(SITE_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) build/context/.stamp src/site.py src/setting.py src/tangent_rounding.py
	$(BP) --python src/site.py
site: $(SITE_OUTPUTS)
check: site
render: site
$(CHECKPOINT_RENDER_OUTPUTS): $(SITE_OUTPUTS)
MATCH_OUTPUTS := $(foreach name,precast pleasant harmon,renders/matches/$(name).png renders/matches/$(name)-pair.jpg) renders/matches/views.json renders/matches/contact.jpg build/matches/calibration.json build/matches/balance.json
matches: render $(MATCH_OUTPUTS)
$(MATCH_OUTPUTS) &: $(SITE_OUTPUTS) build/checkpoint-render-parameters.txt src/matches.py src/render.py ../kit/photo_match.py
	$(PYTHON) src/matches.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose
repeat: site
	$(PYTHON) src/repeat.py
clean: clean-family
clean-family:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures/checkpoint')]"

include src/lookdev_rules.mk
