CHECKPOINT_BLEND := build/sxs.blend
CHECKPOINT_OUTPUTS := build/sxs.blend build/sxs.glb build/shell.glb build/hull.glb
CHECKPOINT_DEPS := src/build.py src/parameters.py src/clips.py src/interface.py ../common/shell12_visual.py ../common/interface_v1_7.py
CHECKPOINT_RENDER_DEPS := src/shots.py ../common/render.py
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --source build/sxs.blend --out build/check.json > build/check.log 2>&1
CHECKPOINT_REVIEW = $(MAKE) evidence && $(PYTHON) src/review.py
WIDTH ?= 1440
SAMPLES ?= 32
CHECKPOINT_OUT := renders/checkpoint/beauty
CHECKPOINT_RENDER_OUTPUTS := $(addprefix $(CHECKPOINT_OUT)/,hero.png side.png left.png top.png front.png rake_right.png rake_left.png open.png breech.png action.png action_left.png triggers.png trigger_quarter.png forend.png stock.png muzzle.png top_controls.png lumps.png aimed.png shots.json)
include ../../kit/checkpoint_rules.mk

$(CHECKPOINT_RENDER_OUTPUTS): $(CHECKPOINT_RENDER_DEPS)

PHOTO_SHOTS := right,left,action,action_left,action_top,action_bottom,open,barrel_flats,forend,forend_side,trigger

.PHONY: native-photos
refs: native-photos
native-photos:
	$(PYTHON) src/fetch_photos.py

.PHONY: verify sections match strips ammo source-match evidence repeat
evidence: sections match strips ammo source-match
review: render
check: verify repeat
verify: model
	$(BP) --python src/verify.py -- > build/verify.log 2>&1
	$(BP) --python src/check.py -- --source build/sxs.glb --out build/import-check.json > build/import-check.log 2>&1
build/repeat/sxs.blend: $(CHECKPOINT_DEPS)
	$(BP) --python src/build.py -- --out $@ > build/repeat-build.log 2>&1
repeat: model build/repeat/sxs.blend
	$(BP) --python src/repeat.py -- --first build/sxs.blend --second build/repeat/sxs.blend --out build/repeat.json > build/repeat.log 2>&1
sections: model
	$(BP) --python src/sections.py -- > build/sections.log 2>&1
match: model
	$(PYTHON) src/photo_matches.py
	$(PYTHON) src/photo_solve.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/sxs.glb --out renders/checkpoint/photos --camera-file build/cameras.json --shots $(PHOTO_SHOTS) --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/photos --out renders/checkpoint/pairs
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
strips: model
	$(PYTHON) src/strips.py
	$(BP) --python src/render.py -- --source build/sxs.glb --out renders/checkpoint/opening-wide --width 500 --engine BLENDER_WORKBENCH --strip Open --wide > build/opening-wide.log 2>&1
ammo: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/shell.glb --out renders/checkpoint/shell --shots shell --width 1200 --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/hull.glb --out renders/checkpoint/hull --shots hull --width 1200 --samples $(SAMPLES)
source-match: model match
	$(BP) --python src/prepare_high.py -- > build/prepare-high.log 2>&1
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/sculpt.blend --out renders/checkpoint/source-photos --camera-file build/cameras.json --shots $(PHOTO_SHOTS) --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/source-photos --out renders/checkpoint/source-pairs
