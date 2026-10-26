ASSET := StreetLight
FINAL_PIPELINE := 0
SHIP_SIZE := 1024
WIDTH ?= 1200
SAMPLES ?= 48
BAKE_SAMPLES ?= 16
UV_TARGET_DENSITY := 600
WEAR ?= .45
MODEL_DEPS = src/build.py src/dimensions.py $(KIT)/model.py $(KIT)/materials.py $(KIT)/prop.py
SHOTS := hero_closed,controls,casting,lit
FINAL_SHOTS := hero_closed,front,side,back,top,controls,casting,scale,lit
include ../kit/rules.mk
.PHONY: photo check-assembly
photo: refs
	pdfimages -j refs/fixture.pdf refs/photo
	$(PYTHON) src/prepare_refs.py
match match-final: photo
all: photo
check: check-assembly
check-assembly: build/game-audit.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/assembly-check.json
ifeq ($(FINAL_PIPELINE),1)
check: check-optics
endif
.PHONY: check-optics
check-optics: export/$(ASSET).glb
	$(PYTHON) src/check_emission.py --source $< --out build/optics-check.json
