.DELETE_ON_ERROR:
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
BP = $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1
KIT := ../kit
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
WIDTH ?= 1600
SAMPLES ?= 48
BAKE_SIZE := 4096
BAKE_SAMPLES ?= 16
MODULES := BusStop Shelter Bench BikeRack BikeRackRow NewsDaily NewsPedestal NewsWeekly CollectionBox MeterSingle MeterTwin Litter Recycling ShelterMissingPanel NewsRow
MAPS := $(foreach c,BaseColor Normal ORM Graphics,textures/ship/T_StreetFurniture_$(c).png)
EXPORTS := export/StreetFurniture.gltf export/StreetFurniture.bin $(foreach n,$(MODULES),export/$(n).gltf export/$(n).bin)
MODEL_DEPS := src/build.py src/forms.py src/pieces.py src/surfaces.py build/graphics.json
SHOTS := hero lineup signs-regulatory signs-warning sign-face sign-back post-base pole-band shelter-frame bench meter boxes collection receptacles rack route-plate front side back top
RENDERS := $(foreach s,$(SHOTS),renders/final/$(s).png renders/final/$(s).json)
.PHONY: all refs model export textures signs check check-repo check-motion render match review docs repeat clean FORCE
all: refs model check render match review
build/graphics.json: src/graphics.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/graphics.py
build/game.blend build/game.json &: $(MODEL_DEPS)
	$(BP) --python src/build.py -- --out build/game.blend
build/high.blend build/high.json &: $(MODEL_DEPS)
	$(BP) --python src/build.py -- --quality high --out build/high.blend
build/finalized.blend build/uv.json &: build/game.blend src/bake_config.py src/finalize.py
	$(BP) --python src/finalize.py -- --source build/game.blend --out build/finalized.blend --config src/bake_config.py --report build/uv.json --size 2048 --margin .001 --target-density 650
build/bake-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
textures/bake/T_StreetFurniture_BaseColor.png textures/bake/T_StreetFurniture_Normal.png textures/bake/T_StreetFurniture_ORM.png &: build/finalized.blend build/high.blend build/bake-parameters.txt src/bake_config.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/finalized.blend --high build/high.blend --out textures/bake --asset StreetFurniture --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES) --config src/bake_config.py
$(MAPS) &: textures/bake/T_StreetFurniture_BaseColor.png textures/bake/T_StreetFurniture_Normal.png textures/bake/T_StreetFurniture_ORM.png src/texture_finish.py
	$(PYTHON) $(KIT)/downsample.py --source textures/bake --out textures/ship --asset StreetFurniture --size 2048
	$(PYTHON) src/texture_finish.py
textures: $(MAPS)
$(EXPORTS) build/manifest.json &: build/finalized.blend $(MAPS) src/deliver.py
	$(BP) --python src/deliver.py --
export: $(EXPORTS)
../street-signs/export/set/RoadSigns.gltf: $(wildcard ../street-signs/src/set_*.py)
	$(MAKE) -C ../street-signs set-model
signs: ../street-signs/export/set/RoadSigns.gltf
model: export signs
build/context/UtilityContext.glb: src/context_build.py $(wildcard ../utility/src/*.py)
	$(BP) --python src/context_build.py
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(RENDERS) &: $(EXPORTS) ../street-signs/export/set/RoadSigns.gltf build/context/UtilityContext.glb src/render.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/StreetFurniture.gltf --out renders/final --shots $(subst $(space),$(comma),$(strip $(SHOTS))) --width $(WIDTH) --samples $(SAMPLES)
# Explicit comma list keeps command construction portable in ordinary GNU make.
comma := ,
space := $(empty) $(empty)
render: $(RENDERS) renders/eevee/hero.png
renders/eevee/hero.png: $(EXPORTS) ../street-signs/export/set/RoadSigns.gltf build/context/UtilityContext.glb src/render.py src/eevee.py build/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/StreetFurniture.gltf --out renders/eevee --shots hero --engine BLENDER_EEVEE --width $(WIDTH) --samples $(SAMPLES)
build/photo-calibration.json: src/photo_matches.py
	$(PYTHON) src/photo_matches.py --out $@
renders/match/.stamp: $(EXPORTS) ../street-signs/export/set/RoadSigns.gltf build/photo-calibration.json src/render.py build/render-parameters.txt
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/photo-calibration.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/StreetFurniture.gltf --match build/photo-calibration.json --out renders/match --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/photo-calibration.json --renders renders/match --out renders/match
	@touch $@
match: refs renders/match/.stamp
refs:
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/fetch_refs.py
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: model check-repo
	$(BP) --python src/check.py
	$(BP) --python src/check_delivery.py
	$(MAKE) -C ../street-signs set-check
	$(PYTHON) src/costs.py
build/motion-parts.blend: $(MODEL_DEPS)
	$(BP) --python src/build.py -- --parts --out $@
check-motion: build/motion-parts.blend
	$(BP) --python src/check_motion.py -- $<
review: render match
	$(PYTHON) src/review.py --folder renders/final
	$(PYTHON) src/values.py
# Docs are written only after the full-size visual audit. They are not automatic.
docs: review
	$(PYTHON) src/review.py --folder renders/final --docs
repeat: model
	$(PYTHON) src/repeat.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"

# Independently placed kinds require their own additive proof.
LOD_CONFIGS := src/lod-bench.json src/lod-meter-single.json src/lod-meter-twin.json src/lod-shelter.json
include ../kit/lod_rules.mk
.PHONY: check-lod-parts
check-lod: check-lod-parts
check-lod-parts:
	@set -e; for lod_config in $(LOD_CONFIGS); do \
		$(BP) --threads $(LOD_THREADS) --python src/check_lod_parts.py -- --config "$$lod_config"; \
	done
