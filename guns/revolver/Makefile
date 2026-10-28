CHECKPOINT_BLEND := build/revolver.blend
CHECKPOINT_OUTPUTS := build/revolver.blend build/sculpt.blend build/revolver.glb build/cartridge.glb build/case.glb build/speedloader_loaded.glb build/triangles.json
CHECKPOINT_DEPS := src/build.py src/clips.py src/parameters.py src/interface.py ../common/magnum357.py ../common/interface_v1_4.py $(wildcard ../../kit/*.py)
CHECKPOINT_OUT := renders/checkpoint/beauty
VIEWS := hero side left top front rake_right rake_left open star reload rear trigger_side trigger_quarter grip grip_left sights hammer_cocked recoil_shield lug_front muzzle rear_sight latch grip_seam shank hammer_rest hammer_top aimed
CHECKPOINT_RENDER_OUTPUTS := $(addprefix $(CHECKPOINT_OUT)/,$(addsuffix .png,$(VIEWS)))
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --source $(CHECKPOINT_BLEND) --out build/check.json
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
include ../../kit/checkpoint_rules.mk
$(CHECKPOINT_RENDER_OUTPUTS): src/shots.py

.PHONY: match source-match strips sections verify standalones
build/serialization.json: $(CHECKPOINT_OUTPUTS) src/verify.py src/contacts.py src/semantics.py
	$(BP) --python src/verify.py -- --source $(CHECKPOINT_BLEND) --out $@
verify: build/serialization.json
build/repeat/revolver.blend: $(CHECKPOINT_OUTPUTS)
	$(BP) --python src/build.py -- --out $@
build/repeat.json: build/repeat/revolver.blend $(CHECKPOINT_OUTPUTS) src/repeat.py
	$(BP) --python src/repeat.py -- --first build/revolver.blend --second build/repeat/revolver.blend --out $@
.PHONY: repeat
repeat: build/repeat.json
check: verify repeat
build/imported-check.json: $(CHECKPOINT_OUTPUTS) src/check.py src/contacts.py src/semantics.py
	$(BP) --python src/check.py -- --source build/revolver.glb --out $@
check: build/imported-check.json

build/references/whitebalance.json: src/prepare_refs.py refs/SOURCES.md | refs
	$(PYTHON) src/prepare_refs.py
build/photo-cameras.json: build/references/whitebalance.json src/photo_matches.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
renders/checkpoint/pairs/.stamp: build/photo-cameras.json $(CHECKPOINT_OUTPUTS) src/shots.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/revolver.glb --out renders/checkpoint/photos --width $(WIDTH) --samples $(SAMPLES) --camera-file build/photo-cameras.json --shots right_photo,left_photo,open_photo
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/photo-cameras.json --renders renders/checkpoint/photos --out renders/checkpoint/pairs
	touch $@
match: renders/checkpoint/pairs/.stamp
renders/checkpoint/source-pairs/.stamp: build/photo-cameras.json $(CHECKPOINT_OUTPUTS) src/shots.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/sculpt.blend --out renders/checkpoint/source-photos --width $(WIDTH) --samples $(SAMPLES) --camera-file build/photo-cameras.json --shots right_photo,left_photo,open_photo
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/photo-cameras.json --renders renders/checkpoint/source-photos --out renders/checkpoint/source-pairs
	touch $@
source-match: renders/checkpoint/source-pairs/.stamp
renders/checkpoint/strips/timing.json: $(CHECKPOINT_OUTPUTS) src/clips.py src/shots.py
	$(PYTHON) src/strips.py
strips: renders/checkpoint/strips/timing.json
renders/checkpoint/sections/sections.jpg: $(CHECKPOINT_OUTPUTS) src/sections.py
	$(BP) --python src/sections.py -- --source build/revolver.glb --high build/sculpt.blend --out renders/checkpoint/sections
sections: renders/checkpoint/sections/sections.jpg
renders/checkpoint/ammo/.stamp: $(CHECKPOINT_OUTPUTS) src/shots.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/cartridge.glb --out renders/checkpoint/ammo --width $(WIDTH) --samples $(SAMPLES) --shots cartridge,cartridge_head
	mv renders/checkpoint/ammo/shots.json renders/checkpoint/ammo/cartridge-shots.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/case.glb --out renders/checkpoint/ammo --width $(WIDTH) --samples $(SAMPLES) --shots case,case_head
	mv renders/checkpoint/ammo/shots.json renders/checkpoint/ammo/case-shots.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/speedloader_loaded.glb --out renders/checkpoint/ammo --width $(WIDTH) --samples $(SAMPLES) --shots speedloader
	mv renders/checkpoint/ammo/shots.json renders/checkpoint/ammo/speedloader-shots.json
	touch $@
standalones: renders/checkpoint/ammo/.stamp
render: standalones
renders/checkpoint/trigger-pairs/.stamp: $(CHECKPOINT_OUTPUTS) build/references/whitebalance.json src/trigger_matches.py
	$(KIT)/with_gpu.sh $(BP) --python src/trigger_render.py -- --source build/revolver.glb --out renders/checkpoint/trigger --width 1000 --samples $(SAMPLES) --shots trigger_right,trigger_quarter
	$(PYTHON) src/trigger_render.py --compose --renders renders/checkpoint/trigger --out renders/checkpoint/trigger-pairs
	touch $@
.PHONY: triggers
triggers: renders/checkpoint/trigger-pairs/.stamp
review: match source-match strips sections triggers

renders/checkpoint/hammer-pairs/.stamp: $(CHECKPOINT_OUTPUTS) build/references/whitebalance.json src/hammer_review.py src/shots.py
	$(KIT)/with_gpu.sh $(BP) --python src/hammer_review.py -- --source build/revolver.glb --out renders/checkpoint/hammer --width 1100 --samples $(SAMPLES) --shots hammer_rest_photo,hammer_cocked_photo
	$(PYTHON) src/hammer_review.py --compose
	touch $@
.PHONY: hammers
hammers: renders/checkpoint/hammer-pairs/.stamp
review: hammers

build/form-metrics.json: $(CHECKPOINT_OUTPUTS) src/form_metrics.py
	$(BP) --python src/form_metrics.py -- --source $(CHECKPOINT_BLEND) --out $@
check: build/form-metrics.json
