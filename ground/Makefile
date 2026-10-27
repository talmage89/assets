ASSET := Ground
ASSEMBLY := GroundStreet
TILE_PROOF := GroundTiles
TILE_NAMES := Asphalt Concrete Lawn
TILE_COVERAGE_Asphalt := 6.096
TILE_COVERAGE_Concrete := 3.048
TILE_COVERAGE_Lawn := 3.048
include ../kit/tiling_rules.mk
export/$(ASSET).glb: src/additions.py src/organic.py
build/material-sources.stamp: src/organic.py
CONTEXT_FOLDERS := fire-hydrant mailbox trash-cart street-signs street-light
CONTEXT_DEPS := $(foreach item,$(CONTEXT_FOLDERS),$(wildcard ../$(item)/Makefile ../$(item)/src/*.py))
.PHONY: context
context: build/context-props.json
build/context-props.json: src/context.py $(CONTEXT_DEPS)
	$(PYTHON) src/context.py --out $@
renders/final/.stamp: build/context-props.json

.PHONY: lawn-tile
tile-render: lawn-tile
lawn-tile: export/$(ASSEMBLY).glb
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/$(TILE_PROOF).glb --out renders/tiles --shots tile_lawn --width $(WIDTH) --samples $(SAMPLES)
