CHECKPOINT_BLEND := build/ak.blend
CHECKPOINT_OUTPUTS := build/ak.blend build/ak.glb build/magazine_loaded.glb build/magazine_empty.glb build/cartridge.glb build/case.glb
CHECKPOINT_DEPS := src/build.py src/geometry.py src/clips.py src/interface.py ../common/ammo762_visual.py
CHECKPOINT_OUT := renders/checkpoint/beauty
CHECKPOINT_RENDER_OUTPUTS := $(addprefix renders/checkpoint/beauty/,$(addsuffix .png,right left side top front raking_right raking_left receiver cover_rear controls trigger trigger_side wood grip_stock rear_sight front_sight gas_muzzle open aimed magazine))
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --motion && $(BP) --python src/verify.py --
CHECKPOINT_REVIEW = $(MAKE) sections match strips extra && $(PYTHON) src/review.py
WIDTH := 1440
SAMPLES := 32
include ../../kit/checkpoint_rules.mk
$(CHECKPOINT_RENDER_OUTPUTS): src/shots.py ../common/render.py
.PHONY: sections match strips extra
sections: model
	$(BP) --python src/sections.py
	$(PYTHON) src/reference.py
	$(PYTHON) src/cheek_weld.py
build/cameras.json: src/photo_matches.py src/reference.py refs/SOURCES.md
	$(PYTHON) src/reference.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
match: model build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/ak.glb --out renders/checkpoint/photos --width $(WIDTH) --samples $(SAMPLES) --camera-file build/cameras.json --shots right_photo,left_photo,receiver_photo,trigger_photo,trigger_sharp
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/photos --out renders/checkpoint/pairs
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/ak.blend --out renders/checkpoint/source-photos --width $(WIDTH) --samples $(SAMPLES) --camera-file build/cameras.json --shots right_photo,left_photo,receiver_photo,trigger_photo,trigger_sharp
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/source-photos --out renders/checkpoint/source-pairs
strips: model
	$(PYTHON) src/strips.py
extra: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/ak.glb --out renders/checkpoint/selector --width 900 --samples $(SAMPLES) --shots selector_safe,selector_auto,selector_semi
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/magazine_loaded.glb --out renders/checkpoint/loaded --width 1000 --samples $(SAMPLES) --shots mag_standalone,mag_lips
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/magazine_empty.glb --out renders/checkpoint/empty --width 1000 --samples $(SAMPLES) --shots mag_standalone,mag_lips
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/cartridge.glb --out renders/checkpoint/cartridge --width 1000 --samples $(SAMPLES) --shots cartridge
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/case.glb --out renders/checkpoint/case --width 1000 --samples $(SAMPLES) --shots case,case_mouth
