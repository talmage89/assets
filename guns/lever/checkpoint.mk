CHECKPOINT_BLEND := build/lever.blend
CHECKPOINT_OUTPUTS := build/lever.blend build/lever.glb build/sculpt.blend build/cartridge.glb build/case.glb build/interface.json build/triangles.json
CHECKPOINT_DEPS := $(addprefix src/,build.py clips.py dimensions.py forms.py geometry.py mechanism.py interface.py) ../common/ammo_3030.py ../common/interface_v1_5.py
CHECKPOINT_OUT := renders/checkpoint/views
CHECKPOINT_RENDER_OUTPUTS := $(addprefix renders/checkpoint/views/,$(addsuffix .png,hero_right hero_left right left top front receiver receiver_left raking_right raking_left open open_left lever_open lever_rest_ortho lever_mid_ortho lever_open_ortho hammer trigger trigger_quarter_view sights front_sight stock butt_plate butt_plate_profile wrist_under receiver_raking_right receiver_raking_left forend gate_open aimed) shots.json)
PHOTO_SHOTS := right_photo,left_photo,open_photo,trigger_right,trigger_quarter,hammer_photo,lever_rest_photo,used_photo,sight_photo
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --motion && $(BP) --python src/verify.py --
CHECKPOINT_REVIEW = $(MAKE) sections match strips extra && $(PYTHON) src/review.py
WIDTH := 1440
SAMPLES := 32
include ../../kit/checkpoint_rules.mk

$(CHECKPOINT_RENDER_OUTPUTS): src/shots.py ../common/render.py

.PHONY: sections match strips extra
sections: model
	$(BP) --python src/sections.py --
match: refs model
	$(PYTHON) src/white_balance.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out build/cameras.json
	$(PYTHON) src/reference_measurements.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/lever.glb --out renders/checkpoint/pairs --camera-file build/cameras.json --shots $(PHOTO_SHOTS) --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/pairs --out renders/checkpoint/pairs
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/sculpt.blend --out renders/checkpoint/source-pairs --camera-file build/cameras.json --shots $(PHOTO_SHOTS) --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/source-pairs --out renders/checkpoint/source-pairs
strips: model
	$(PYTHON) src/strips.py
extra: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/cartridge.glb --out renders/checkpoint/cartridge --shots cartridge,headstamp --width 1100 --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/case.glb --out renders/checkpoint/case --shots case,mouth,headstamp --width 1100 --samples $(SAMPLES)


.PHONY: repeat
repeat: model
	$(BP) --python src/build.py -- --out build/repeat/lever.blend
	$(BP) --python src/repeat.py --

.PHONY: check-topology
check: check-topology
check-topology: model
	$(BP) --python src/topology.py
