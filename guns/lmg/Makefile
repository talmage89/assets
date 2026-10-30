# Form checkpoint only. Look-dev, bake and final delivery remain gated.
CHECKPOINT_BLEND := build/lmg.blend
CHECKPOINT_OUTPUTS := build/lmg.blend build/lmg.glb build/triangles.json build/interface.json build/box_loaded.glb build/box_empty.glb build/cartridge.glb build/case.glb build/link.glb
CHECKPOINT_DEPS := src/build.py src/geometry.py src/clips.py src/interface.py src/belt.py ../common/ammo556_visual.py ../common/interface_v1_8.py
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --source build/lmg.blend --out build/check.json --motion && $(BP) --python src/verify.py && $(BP) --python src/test_contacts.py && $(BP) --python src/form_evidence.py && $(PYTHON) src/test_belt.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_ARGS := --shots hero,raking_right,side,left,top,front,cover_open,cover_open_full,rear_sight,barrel_handle,front_sight,charging_handle,trigger,lower_raking,furniture,handguard,bipod,belt,box,aimed,aimed_macro,shooter_three_quarter
include ../../kit/checkpoint_rules.mk
.PHONY: verify motion sections pairs strips
verify: model
	$(BP) --python src/verify.py
motion: model
	$(BP) --python src/check.py -- --source build/lmg.blend --out build/motion.json --motion
sections: model
	$(BP) --python src/sections.py
	$(BP) --python src/measurements.py
	$(PYTHON) src/reference_measures.py
pairs: refs model
	$(PYTHON) src/white_balance.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out build/cameras.json
	$(PYTHON) src/refine_cameras.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/lmg.glb --out renders/checkpoint/photos --camera-file build/cameras.json --shots right_photo,left_photo,open_photo,trigger_photo,belt_photo,receiver_photo,cover_detail_photo,tray_detail_photo,sight_detail_photo,box_detail_photo --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/photos --out renders/checkpoint/pairs
	$(PYTHON) src/annotate_pairs.py
strips: model
	$(PYTHON) src/strips.py
.PHONY: extra review-all dimensions evidence
extra: model
	$(KIT)/with_gpu.sh $(BP) --python src/render_extra.py
dimensions: sections render
	$(PYTHON) src/dimensions.py
evidence: dimensions pairs strips extra
	$(PYTHON) src/evidence.py
review-all: evidence
	$(CHECKPOINT_REVIEW)
checkpoint: sections pairs strips extra review-all

$(CHECKPOINT_RENDER_OUTPUTS): src/render.py src/shots.py ../common/render.py

.PHONY: markings
markings:
	$(PYTHON) src/markings.py
