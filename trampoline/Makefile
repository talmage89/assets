ASSET := Trampoline
FINAL_PIPELINE := 1
WEAR := .65
SHIP_SIZE := 1024
UV_TARGET_DENSITY := 300
UV_MARGIN := .0018
MODEL_DEPS := src/build.py src/dimensions.py src/fabric_tile.py src/finishes.py ../kit/model.py ../kit/materials.py
TEXTURE_DEPS := src/fabric_tile.py src/dimensions.py
TEXTURE_POSTPROCESS = $(PYTHON) src/fabric_tile.py --out textures/ship --wear $(WEAR)
WIDTH ?= 1440
SAMPLES ?= 48
SHOTS := hero_closed,controls,casting,underpad
FINAL_SHOTS := hero_closed,front,side,back,top,controls,casting,fabric,underpad,underside,scale
include ../kit/rules.mk
renders/final/.stamp: src/views.py
check-construction: build/finalized.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/construction-check.json
	$(BP) --python src/check_construction.py -- --source $< --tile build/fabric-source/T_Trampoline_BaseColor.png --out build/geometry-contact-check.json
check: check-construction
.PHONY: photo-credit
photo-credit:
	$(PYTHON) src/photo_matches.py --credit-dir renders/$(PASS)
	$(PYTHON) src/photo_matches.py --credit-dir renders/$(PASS)-glb
match match-final: photo-credit

.PHONY: check-bake
check-bake: build/baked.stamp
	$(PYTHON) -c "import json; r=json.load(open('textures/bake/bake-report.json')); assert r['BaseColor']['alpha_missed_interior_texels']==0 and r['BaseColor']['black_interior_texels']==0, r['BaseColor']"
check: check-bake
