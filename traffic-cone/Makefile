ASSET := TrafficCone
FINAL_PIPELINE := 1
SHIP_SIZE := 512
UV_TARGET_DENSITY := 850
UV_MARGIN := .004
WIDTH ?= 1100
SAMPLES ?= 48
BAKE_SAMPLES ?= 16
WEAR ?= .55
SHOTS := hero_closed,controls,casting
FINAL_SHOTS := hero_closed,front,side,back,top,controls,casting,scale
include ../kit/rules.mk
MODEL_DEPS += $(KIT)/prop.py
.PHONY: photo check-assembly
photo: refs
	pdfimages -j refs/dimensions.pdf refs/sheet
match match-final: photo
all: photo
check: check-assembly
check-assembly: build/game-audit.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/assembly-check.json
MODEL_DEPS := src/build.py $(KIT)/model.py $(KIT)/materials.py $(KIT)/prop.py
.PHONY: check-stack
check: check-stack
check-stack: export/$(ASSET).glb
	$(BP) --python src/check_stack.py -- --source $< --out build/stack-check.json
