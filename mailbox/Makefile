ASSET := Mailbox
FINAL_PIPELINE := 1
SHIP_SIZE := 1024
WIDTH ?= 1100
SAMPLES ?= 48
BAKE_SAMPLES ?= 16
WEAR ?= .45
MODEL_DEPS = src/build.py src/dimensions.py $(KIT)/model.py $(KIT)/materials.py $(KIT)/prop.py
SHOTS := hero_closed,hero_open,controls,casting
FINAL_SHOTS := hero_closed,front,side,back,top,controls,casting,scale,hero_open
include ../kit/rules.mk
.PHONY: check-assembly
check: check-assembly
check-assembly: build/game-audit.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/assembly-check.json
ifeq ($(FINAL_PIPELINE),1)
check: check-delivery-motion
endif
.PHONY: check-delivery-motion
check-delivery-motion: export/$(ASSET).glb
	$(BP) --python src/check_delivery.py -- --source $< --out build/motion-glb.json
