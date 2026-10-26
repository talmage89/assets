ASSET := PatioHeater
MARKINGS_DEPS := src/settings.py
FINAL_PIPELINE := 1
STUDIO_ARGS := --lid-node TankDoor --lid-axis Z
TANK_REFERENCE ?= $(REPO)/../.foundry/shared/propane-tank.glb
FIT_CHECK_ARGS := --parts-source build/finalized.blend
WIDTH ?= 1400
SAMPLES ?= 72
SHOTS := hero_closed,hero_open,controls,burner,casting
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,burner,casting,scale,fit_check,lit
include ../kit/rules.mk
.PHONY: check-construction
check-construction: build/finalized.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/construction-check.json
check: check-construction
.PHONY: check-bake-surface
check-bake-surface: export/$(ASSET).glb
	$(BP) --python src/check_construction.py -- --source $< --textures textures/ship --out build/printed-face-check.json
check: check-bake-surface
