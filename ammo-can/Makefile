ASSET := AmmoCan
SHIP_SIZE := 1024
UV_TARGET_DENSITY := 1000
SAMPLES ?= 48
SHOTS := hero_closed,hero_open,controls,casting,handle
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,casting,handle,scale
FINAL_PIPELINE := 1
MODEL_DEPS := src/build.py src/finishes.py ../kit/model.py ../kit/materials.py
include ../kit/rules.mk
.PHONY: check-construction check-sequence
check: check-construction check-sequence
check-construction: build/game-audit.blend build/lookdev.blend
	$(BP) --python $(KIT)/assembly.py -- --source build/game-audit.blend --config $(CONFIG) --out build/contacts-game.json
	$(BP) --python $(KIT)/assembly.py -- --source build/lookdev.blend --config $(CONFIG) --out build/contacts-high.json
check-sequence: build/game-audit.blend build/lookdev.blend
	$(BP) --python src/check_sequence.py -- --source build/game-audit.blend --out build/sequence-game.json
	$(BP) --python src/check_sequence.py -- --source build/lookdev.blend --out build/sequence-high.json

docs: renders/photo-final-glb/.stamp
renders/photo-final-glb/.stamp: export/AmmoCan.glb build/matched-cameras.json src/photo_studio.py ../kit/studio.py
	$(KIT)/with_gpu.sh $(BP) --python src/photo_studio.py -- --stage final --source export/AmmoCan.glb --config $(CONFIG) --camera-file build/matched-cameras.json --out renders/photo-final-glb --shots match_closed,match_latch --width 1000 --samples 32
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/photo-final-glb --out renders/photo-final-glb
	@touch $@
