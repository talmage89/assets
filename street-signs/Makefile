ASSET := StreetSigns
FINAL_PIPELINE := 1
SHIP_SIZE := 1024
UV_TARGET_DENSITY := 900
UV_MARGIN := .002
WIDTH ?= 1200
SAMPLES ?= 48
BAKE_SAMPLES ?= 16
SHOTS := hero_closed,controls,casting
FINAL_SHOTS := hero_closed,front,side,back,top,controls,casting,scale
NAME_VARIANT ?= 0
export NAME_VARIANT
include ../kit/rules.mk
MODEL_DEPS += $(KIT)/prop.py
# Additional checkpoint scripts must not invalidate the approved STOP bake.
MODEL_DEPS := $(filter-out src/set_%.py,$(MODEL_DEPS))
.PHONY: variants
build/name-variant.txt: FORCE
	@python3 -c "from pathlib import Path; p=Path('$@'); s='$(NAME_VARIANT)'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
export/$(ASSET).glb: build/name-variant.txt
variants: build/finalized.blend build/textures.stamp
	@for v in 0 1 2 3; do NAME_VARIANT=$$v $(BP) --python $(KIT)/export.py -- --source build/finalized.blend --textures textures/ship --asset $(ASSET) --config src/config.py --out export/StreetSigns_$$v.glb --report build/variant-$$v.json; done

.PHONY: check-assembly
check: check-assembly
check-assembly: build/game-audit.blend
	$(BP) --python $(KIT)/assembly.py -- --source $< --config $(CONFIG) --out build/assembly-check.json

# Independent 2009-period expansion. The existing final targets above keep
# their original dependencies and delivery bytes, STOP and blades included.
.PHONY: set-model set-check set-checkpoint
build/set/layout.json: src/set_graphics.py src/set_catalog.py
	@mkdir -p build/set
	$(PYTHON) src/set_graphics.py build/set
export/set/RoadSigns.gltf build/set/Signs.blend build/set/manifest.json &: src/set_build.py src/set_catalog.py build/set/layout.json
	$(BP) --python src/set_build.py -- --out build/set/Signs.blend
set-model: export/set/RoadSigns.gltf
set-check: set-model
	$(BP) --python src/set_check.py
set-checkpoint: set-check
	$(MAKE) -C ../street-furniture render
