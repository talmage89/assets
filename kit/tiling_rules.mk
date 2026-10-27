# Script interface for modular multi-material terrain families. Unique-atlas
# props continue to use rules.mk unchanged. See README "Tiling families".
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO := $(abspath $(KIT)/..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(abspath $(REPO)/../.locks/gpu.lock)
SHIP_SIZE ?= 2048
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 8
WIDTH ?= 1440
SAMPLES ?= 64
WEAR ?= 1
PASS ?= review
MODEL_DEPS := src/build.py src/dimensions.py src/textures.py $(KIT)/tiling.py
.PHONY: all refs model export preview render docs check check-repo match match-final check-camera clean FORCE
.NOTPARALLEL:
all: refs docs check
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
build/parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR) bake=$(BAKE_SIZE) samples=$(BAKE_SAMPLES) ship=$(SHIP_SIZE)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/material-sources.stamp: src/textures.py src/dimensions.py build/parameters.txt
	$(PYTHON) src/textures.py source --out build/procedural --size $(BAKE_SIZE) --wear $(WEAR)
	$(PYTHON) src/textures.py atlas --out textures/bake --size $(BAKE_SIZE) --wear $(WEAR)
	@touch $@
define TILE_RULE
build/bake-$(1).stamp: build/material-sources.stamp $(KIT)/flat_bake.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source build/procedural --out textures/bake --name $(1) --coverage $(TILE_COVERAGE_$(1)) --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch $$@
endef
$(foreach tile,$(TILE_NAMES),$(eval $(call TILE_RULE,$(tile))))
textures/ship/.stamp: $(foreach tile,$(TILE_NAMES),build/bake-$(tile).stamp) src/textures.py $(KIT)/downsample.py
	@mkdir -p textures/ship
	$(foreach tile,$(TILE_NAMES),$(PYTHON) $(KIT)/downsample.py --source textures/bake --out textures/ship --asset $(tile) --size $(SHIP_SIZE);)
	$(PYTHON) src/textures.py ship --source textures/bake --out textures/ship --size $(SHIP_SIZE)
	@touch $@
export/$(ASSET).glb: textures/ship/.stamp $(MODEL_DEPS)
	$(BP) --python src/build.py -- --out $@
model export: export/$(ASSET).glb
export/$(ASSEMBLY).glb export/$(TILE_PROOF).glb build/lookdev-assembly.blend &: export/$(ASSET).glb src/assemble.py src/weather.py $(KIT)/tiling.py
	$(BP) --python src/assemble.py -- --source $< --out export/$(ASSEMBLY).glb
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
renders/final/.stamp: export/$(ASSEMBLY).glb src/render.py src/views.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --out renders/final --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
renders/final-eevee/.stamp: export/$(ASSEMBLY).glb src/render.py src/views.py build/render-parameters.txt
	$(BP) --python src/render.py -- --source $< --out renders/final-eevee --shots hero --engine BLENDER_EEVEE --width $(WIDTH)
	@touch $@
render: renders/final/.stamp renders/final-eevee/.stamp
preview: export/$(ASSEMBLY).glb
	$(BP) --python src/render.py -- --source $< --out renders/preview --shots hero,block,curb,ramp --engine BLENDER_EEVEE --width 1000
build/matched-cameras.json: src/photo_matches.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
check-camera: build/matched-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $<
match-final: export/$(ASSEMBLY).glb build/matched-cameras.json refs
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --out renders/$(PASS)-glb --camera-file build/matched-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/$(PASS)-glb --out renders/$(PASS)-glb
match: match-final
docs: render match-final match-source tile-render src/review.py
	$(PYTHON) src/review.py --final
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: export/$(ASSEMBLY).glb check-camera
	$(BP) --python src/check.py -- --library export/$(ASSET).glb --assembly export/$(ASSEMBLY).glb
	$(PYTHON) src/check_tiles.py
	$(PYTHON) $(KIT)/repo_check.py
clean:
	rm -rf build export textures renders

.PHONY: match-source tile-render
match-source: export/$(ASSEMBLY).glb build/matched-cameras.json refs
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --stage source --source build/lookdev-assembly.blend --out renders/$(PASS)-source --camera-file build/matched-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/$(PASS)-source --out renders/$(PASS)-source
tile-render: export/$(ASSEMBLY).glb
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/$(TILE_PROOF).glb --out renders/tiles --shots tile_asphalt,tile_concrete --width $(WIDTH) --samples $(SAMPLES)
