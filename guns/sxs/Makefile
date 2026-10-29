CHECKPOINT_BLEND := build/sxs.blend
CHECKPOINT_OUTPUTS := build/sxs.blend build/sxs.glb build/shell.glb build/hull.glb
CHECKPOINT_DEPS := $(wildcard src/*.py) ../common/shell12_visual.py ../common/interface_v1_7.py
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --source build/sxs.blend --out build/check.json > build/check.log 2>&1
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
WIDTH ?= 1440
SAMPLES ?= 32
CHECKPOINT_OUT := renders/checkpoint/beauty
include ../../kit/checkpoint_rules.mk

.PHONY: verify sections match strips source-preview
check: verify
verify: model
	$(BP) --python src/verify.py -- > build/verify.log 2>&1
	$(BP) --python src/check.py -- --source build/sxs.glb --out build/import-check.json > build/import-check.log 2>&1
sections: model
	$(BP) --python src/sections.py -- > build/sections.log 2>&1
match: model
	$(PYTHON) src/photo_matches.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/sxs.glb --out renders/checkpoint/photos --camera-file build/cameras.json --shots right,left,action,open,trigger --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/photos --out renders/checkpoint/pairs
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
strips: model
	$(PYTHON) src/strips.py
