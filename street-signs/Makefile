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
