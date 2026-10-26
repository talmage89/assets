ASSET := WoodPrivacy
MODEL_DEPS := src/build.py src/dimensions.py ../kit/model.py ../kit/materials.py
FINAL_PIPELINE := 1
WEAR := .65
SHIP_SIZE := 2048
UV_TARGET_DENSITY := 260
UV_MARGIN := .0015
WIDTH ?= 1440
SAMPLES ?= 64
SHOTS := hero_closed,hero_open,grain,joinery,gate,gate_back
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,grain,joinery,hardware,gate,gate_back,pieces,posts,scale
include ../kit/rules.mk
.PHONY: check-construction match-final
check-construction: build/finalized.blend export/WoodPrivacy.glb
	$(BP) --python src/check_construction.py -- --source build/finalized.blend --glb export/WoodPrivacy.glb --out build/construction-check.json
check: check-construction
match-final: export/WoodPrivacy.glb refs build/matched-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --camera-file build/matched-cameras.json --out renders/match-final --shots match_rails --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/match-final --out renders/match-final

.PHONY: assembly-render
export/PrivacyAssembly.glb: export/WoodPrivacy.glb src/assemble.py
	$(BP) --python src/assemble.py -- --source $< --out $@
renders/assembly/.stamp: export/PrivacyAssembly.glb $(CONFIG) $(KIT)/studio.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --out renders/assembly --shots corner_good,corner_rails --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
assembly-render: renders/assembly/.stamp
docs: assembly-render
