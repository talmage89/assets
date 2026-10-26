ASSET := Cooler
SHIP_SIZE := 1024
UV_TARGET_DENSITY := 640
FINAL_PIPELINE := 1
MODEL_DEPS := src/build.py src/finishes.py ../kit/model.py ../kit/materials.py ../kit/prop.py
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,casting,gasket,scale
SHOTS := hero_closed,hero_open,controls,casting
include ../kit/rules.mk
.PHONY: check-construction
check-construction: build/game-audit.blend build/lookdev.blend
	$(BP) --python src/check_construction.py -- --source build/game-audit.blend --out build/construction-game.json
	$(BP) --python src/check_construction.py -- --source build/lookdev.blend --out build/construction-high.json
check: check-construction

.PHONY: review-pairs
renders/review-glb/.stamp: export/Cooler.glb build/matched-cameras.json src/photo_matches.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source export/Cooler.glb --config $(CONFIG) --camera-file build/matched-cameras.json --out renders/review-glb --shots outdoor,used_full --width 1000 --samples 40
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/review-glb --out renders/review-glb
	@touch $@
review-pairs: renders/review-glb/.stamp
all: review-pairs
