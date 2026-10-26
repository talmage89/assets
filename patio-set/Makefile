ASSET := PatioSet
MODEL_DEPS := src/build.py src/finishes.py ../kit/model.py ../kit/materials.py ../kit/prop.py
SHIP_SIZE := 2048
UV_TARGET_DENSITY := 390
UV_MARGIN := .0012
WIDTH ?= 1400
SAMPLES ?= 80
FINAL_PIPELINE := 1
SHOTS := hero_closed,hero_open,controls,casting,canopy,closed,front,side
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,casting,canopy,closed,scale
include ../kit/rules.mk
.PHONY: prepare-refs
refs: prepare-refs
prepare-refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
	$(PYTHON) src/prepare_refs.py
.PHONY: check-construction
check-construction: build/game-audit.blend build/lookdev.blend
	$(BP) --python src/check_construction.py -- --source build/game-audit.blend --out build/construction-game.json
	$(BP) --python src/check_construction.py -- --source build/lookdev.blend --out build/construction-high.json
check: check-construction
docs: check-construction
.PHONY: assembly
export/PatioDining.glb: export/PatioSet.glb src/assemble.py
	$(BP) --python src/assemble.py -- --source $< --out $@ --report build/assembly-delivery.json
assembly: export/PatioDining.glb
check: assembly
docs: assembly
.PHONY: review-pairs
renders/review-source/.stamp: export/PatioSet.glb build/lookdev.blend build/matched-cameras.json src/photo_matches.py $(KIT)/photo_match.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --source build/lookdev.blend --config $(CONFIG) --camera-file build/matched-cameras.json --out renders/review-source --shots sling_chair,used_set --width 1000 --samples 40
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/review-source --out renders/review-source
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source export/PatioSet.glb --config $(CONFIG) --camera-file build/matched-cameras.json --out renders/review-glb --shots sling_chair,used_set --width 1000 --samples 40
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/review-glb --out renders/review-glb
	@touch $@
review-pairs: renders/review-source/.stamp
all: review-pairs

.PHONY: check-projection
build/projection-check.json: export/PatioSet.glb src/check_projection.py
	$(BP) --python src/check_projection.py -- --source $< --out $@
check-projection: build/projection-check.json
renders/final/.stamp: | build/projection-check.json
export/PatioDining.glb: | build/projection-check.json
check: check-projection
docs: check-projection
.PHONY: check-weather
build/weather-check.json: export/PatioSet.glb src/check_weather.py build/parameters.txt
	$(BP) --python src/check_weather.py -- --source $< --wear $(WEAR) --out $@
check-weather: build/weather-check.json
check: check-weather
renders/final/.stamp: | build/weather-check.json
