ASSET := Shed
FINAL_PIPELINE := 1
WEAR := .8
UV_TARGET_DENSITY := 170
UV_MARGIN := .0012
WIDTH ?= 1440
SAMPLES ?= 48
SHOTS := hero_closed,hero_open,interior,casting
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,casting,interior,scale
include ../kit/rules.mk
check-construction: build/finalized.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/construction-check.json
	$(BP) --python src/check_construction.py -- --source $< --out build/dimensions-check.json
check: check-construction
