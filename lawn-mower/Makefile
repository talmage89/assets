ASSET := LawnMower
FINAL_PIPELINE := 1
WIDTH ?= 1400
SAMPLES ?= 64
SHOTS := hero_closed,engine,bag,side
FINAL_SHOTS := hero_closed,front,side,back,top,engine,bag,underside,folded,bail_held,scale
STUDIO_ARGS := --lid-node HandleFold --lid-axis X
include ../kit/rules.mk
.PHONY: check-construction
check-construction: build/finalized.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/construction-check.json
check: check-construction
.PHONY: check-geometry
check-geometry: build/finalized.blend
	$(BP) --python src/check_geometry.py -- --source $< --out build/geometry-check.json
check: check-geometry
.PHONY: photo-credits
photo-credits:
	$(PYTHON) src/photo_matches.py --credit-dir renders/$(PASS)
	$(PYTHON) src/photo_matches.py --credit-dir renders/$(PASS)-glb
match match-final: photo-credits
