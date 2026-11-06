# Shared-map PBR checkpoint; no docs images are published at this gate.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
WIDTH ?= 1440
SAMPLES ?= 40
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 1
REGIONS := midwest western northeast southern
MODEL := build/downtown.blend build/downtown.json $(foreach r,$(REGIONS),build/blocks/$(r)/block.blend build/blocks/$(r)/block.glb build/blocks/$(r)/block.json)
SOURCE := $(addprefix src/,build.py plan.py building.py geometry.py graphics.py ornament.py surfaces.py age.py delivery.py street.py)
.PHONY: all refs bake model context check check-repo repeat check-repeat render matches review clean FORCE
all: refs model context check render matches
build/parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/procedural/fields.json: src/textures.py build/parameters.txt
	$(PYTHON) src/textures.py source --size $(BAKE_SIZE)
textures/bake/.stamp: build/procedural/fields.json
	$(KIT)/with_gpu.sh $(BP) --python src/textures.py -- bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch $@
textures/ship/textures.json: textures/bake/.stamp src/textures.py src/graphics.py
	$(PYTHON) src/textures.py ship
bake: textures/ship/textures.json
$(MODEL) &: $(SOURCE) textures/ship/textures.json
	$(BP) --python src/build.py -- --out build/downtown.blend
model: $(MODEL)
build/context/manifest.json: src/context.py src/context_build.py
	$(PYTHON) src/context.py
build/context/blocks/.stamp: $(MODEL) src/context_blocks.py
	$(BP) --python src/context_blocks.py
	@touch $@
context: build/context/manifest.json build/context/blocks/.stamp
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
build/cameras.json: src/photo_matches.py src/matches.py $(MODEL)
	$(PYTHON) src/matches.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
renders/checkpoint/.stamp: $(MODEL) build/context/manifest.json build/context/blocks/.stamp src/render.py src/town.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
render: renders/checkpoint/.stamp
renders/matches/.stamp: $(MODEL) build/cameras.json build/context/manifest.json build/context/blocks/.stamp src/render.py src/town.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --camera-file build/cameras.json --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/matches/raw --out renders/matches
	@touch $@
matches: refs renders/matches/.stamp
review: render matches
	$(PYTHON) src/review.py
	$(PYTHON) src/report.py
	$(PYTHON) src/values.py
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: model check-repo
	$(PYTHON) src/check_plan.py
	$(PYTHON) src/run_checks.py
repeat check-repeat: model
	$(PYTHON) src/repeat.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders','textures','export')]"
.PHONY: before crops source-matches
before:
	$(KIT)/with_gpu.sh $(PYTHON) src/baseline.py --width $(WIDTH)
crops: render matches before
	$(PYTHON) src/proof_crops.py
source-matches: renders/source-matches/.stamp
renders/source-matches/.stamp: $(MODEL) build/cameras.json build/context/manifest.json build/context/blocks/.stamp src/render.py src/town.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source-look --camera-file build/cameras.json --out renders/source-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/source-matches/raw --out renders/source-matches
	@touch $@
all: crops source-matches
.PHONY: eevee
renders/eevee/.stamp: $(MODEL) build/context/manifest.json build/context/blocks/.stamp src/render.py src/town.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --region midwest --shots hero --out renders/eevee --engine BLENDER_EEVEE --width $(WIDTH)
	@touch $@
eevee: renders/eevee/.stamp
all: eevee review
