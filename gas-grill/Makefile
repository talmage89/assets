ASSET := GasGrill
MARKINGS_DEPS := src/settings.py
FIT_CHECK_ARGS := --parts-source build/finalized.blend
STUDIO_ARGS := --lid-node Lid --lid-axis X
FINAL_PIPELINE := 1
WIDTH ?= 1600
SAMPLES ?= 112
TANK_REFERENCE ?=
SHOTS := hero_closed,hero_open,controls,front,side,interior,construction,combustion,scale,hose_pose,fit_check,drawer_open,grease_support
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,interior,construction,combustion,regulator,scale,hose_pose,fit_check,drawer_open,grease_support
include ../kit/rules.mk
.PHONY: check-construction
check-construction: build/finalized.blend
	$(BP) --python src/check_construction.py -- --source $< --out build/construction-check.json
check: check-construction
docs: check-construction
