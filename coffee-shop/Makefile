CHECKPOINT_BLEND := build/coffee.blend
CHECKPOINT_OUTPUTS := build/coffee.blend export/CoffeeShop-117.gltf export/CoffeeShop-228.gltf export/CoffeeShop-339.gltf export/CoffeeShopPieces.gltf
PIECES := BistroChair BistroTable UmbrellaTable AccessibleTable Counter EspressoMachine Grinder Brewer PastryCase SoftChair AFrame Planter Umbrella_Open Umbrella_Closed BikeRack Litter Recycling
CHECKPOINT_OUTPUTS += $(foreach seed,117 228 339,export/CoffeeShop-$(seed).bin build/shops/$(seed).json build/shops/$(seed).glb) export/CoffeeShopPieces.bin $(foreach p,$(PIECES),export/pieces/$(p).gltf export/pieces/$(p).bin)
CHECKPOINT_DEPS := $(addprefix src/,build.py geometry.py pieces.py daily_use.py finishes.py plan.py graphics.py package.py) build/hosts/downtown.glb build/hosts/strip.glb build/hosts/pad.glb build/preservation.json textures/ship/.stamp
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_CHECK += && $(BP) --python src/check_lookdev.py
CHECKPOINT_CHECK += && $(BP) --python src/check_motion.py
CHECKPOINT_CHECK += && $(BP) --python src/check_use.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py && $(BP) --python src/check_lookdev.py -- --presentation
CHECKPOINT_OUT := renders/final
SHOTS := hero above table counter awning chair scale site retained front side back top use wear door eevee
RAIL_OUTPUTS := renders/final/228/rail.png renders/final/228/rail.json
PHOTO_RENDER_OUTPUTS := $(foreach folder,final-matches final-source-matches,$(foreach shot,downtown umbrella pad daily-use,renders/$(folder)/$(shot).png renders/$(folder)/$(shot).json))
CHECKPOINT_RENDER_OUTPUTS := $(foreach seed,117 228 339,$(foreach shot,$(SHOTS),$(CHECKPOINT_OUT)/$(seed)/$(shot).png $(CHECKPOINT_OUT)/$(seed)/$(shot).json)) $(CHECKPOINT_OUT)/339/walkup.png $(CHECKPOINT_OUT)/339/walkup.json $(CHECKPOINT_OUT)/pieces.png $(CHECKPOINT_OUT)/pieces.json
LIBRARY_INPUTS := ../patio-set/export/PatioSet.glb ../street-furniture/export/BikeRack.gltf ../street-furniture/export/Litter.gltf ../street-furniture/export/Recycling.gltf ../ground/textures/ship/T_Concrete_BaseColor.png ../ground/textures/ship/T_Asphalt_BaseColor.png ../ground/textures/ship/T_Lawn_BaseColor.png ../trees/export/RedMaple.glb
CONTEXT_INPUTS := ../street-furniture/export/Bench.gltf ../street-furniture/export/NewsDaily.gltf ../street-furniture/export/MeterTwin.gltf ../street-light/export/StreetLight.glb ../cars/export/AlderC150.glb ../cars/export/AlderH120.glb ../cars/export/AlderX220.glb ../houses/export/HearthfieldRanch-11.gltf ../houses/export/HearthfieldCape-34.gltf
CHECKPOINT_DEPS += $(LIBRARY_INPUTS)
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1280
SAMPLES ?= 40
# Match the vehicle pipelines: a single CPU worker keeps evaluated normals,
# bevel interpolation and MikkTSpace accumulation reproducible. Cycles uses GPU.
BP := $(BLENDER) -b -t 1 --factory-startup --python-exit-code 1

.PHONY: all model render review docs check check-repo clean FORCE
all: refs model sites check render match source-matches before-after review docs
build/checkpoint-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='default three seeded shops\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(CHECKPOINT_OUTPUTS) &: $(CHECKPOINT_DEPS) build/checkpoint-parameters.txt
	$(BP) --python src/build.py -- --out build/coffee.blend
model: $(CHECKPOINT_OUTPUTS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: model sites check-repo
	$(CHECKPOINT_CHECK)
build/checkpoint-render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(CHECKPOINT_RENDER_OUTPUTS) $(PHOTO_RENDER_OUTPUTS) $(RAIL_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) $(SITE_OUTPUTS) build/checkpoint-render-parameters.txt build/photo-calibration.json src/render.py src/render_batch.py src/render_rail.py
	$(KIT)/with_gpu.sh $(PYTHON) src/render_batch.py --width $(WIDTH) --samples $(SAMPLES) --photographs
render: $(CHECKPOINT_RENDER_OUTPUTS)
review: render match before-after
	$(PYTHON) src/review.py
	$(BP) --python src/check_lookdev.py -- --presentation
docs: review
	$(PYTHON) src/delivery_docs.py
clean:
	$(PYTHON) src/clean.py

refs: coffee-refs
.PHONY: coffee-refs
coffee-refs:
	$(PYTHON) src/fetch_refs.py

build/preservation.json:
	@mkdir -p build
	$(PYTHON) src/check.py --capture

# Existing canonical deliveries are read-only inputs. A clean clone builds
# missing dependencies through their own public targets; present ones have no
# source prerequisites here and are never refreshed by the coffee build.
../patio-set/export/PatioSet.glb:
	$(MAKE) -C ../patio-set export/PatioSet.glb
../street-furniture/export/BikeRack.gltf ../street-furniture/export/Litter.gltf ../street-furniture/export/Recycling.gltf ../street-furniture/export/Bench.gltf ../street-furniture/export/NewsDaily.gltf ../street-furniture/export/MeterTwin.gltf &:
	$(MAKE) -C ../street-furniture export
../ground/textures/ship/T_Concrete_BaseColor.png ../ground/textures/ship/T_Asphalt_BaseColor.png ../ground/textures/ship/T_Lawn_BaseColor.png &:
	$(MAKE) -C ../ground export/Ground.glb
../trees/export/RedMaple.glb:
	$(MAKE) -C ../trees export/RedMaple.glb
../street-light/export/StreetLight.glb:
	$(MAKE) -C ../street-light export/StreetLight.glb
../cars/export/AlderC150.glb:
	$(MAKE) -C ../cars BODY=pickup export/AlderC150.glb
../cars/export/AlderH120.glb:
	$(MAKE) -C ../cars BODY=hatch export/AlderH120.glb
../cars/export/AlderX220.glb:
	$(MAKE) -C ../cars BODY=suv export/AlderX220.glb
../houses/export/HearthfieldRanch-11.gltf:
	$(MAKE) -C ../houses TYPE=ranch RANCH_SEED=11 RANCH_SEEDS=11 export
../houses/export/HearthfieldCape-34.gltf:
	$(MAKE) -C ../houses TYPE=cape CAPE_SEED=34 CAPE_SEEDS=34 export

build/hosts/%.glb: src/hosts.py
	@mkdir -p build/hosts $(TMPDIR)
	$(BP) --python src/hosts.py -- --kind $* --out $@

../downtown/textures/ship/textures.json:
	$(MAKE) -C ../downtown bake
build/hosts/downtown.glb build/hosts/downtown-left.glb build/hosts/downtown-right.glb build/hosts/downtown-opposite.glb: ../downtown/textures/ship/textures.json

textures/ship/.stamp: src/graphics.py src/bake_atlas.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake_atlas.py
	@touch $@

.PHONY: sites
SITE_OUTPUTS := build/sites/.stamp $(foreach seed,117 228 339,export/sites/CoffeeSite-$(seed).gltf export/sites/CoffeeSite-$(seed).bin build/sites/$(seed).json build/sites/$(seed).glb)
sites: $(SITE_OUTPUTS)
$(SITE_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) $(CONTEXT_INPUTS) src/sites.py src/context_tangents.json build/hosts/downtown-left.glb build/hosts/downtown-right.glb build/hosts/downtown-opposite.glb build/hosts/strip-neighbors.glb
	$(BP) --python src/sites.py
	@touch build/sites/.stamp
$(CHECKPOINT_RENDER_OUTPUTS): $(SITE_OUTPUTS)
check: sites

# The ground-facing wear view misses the strip rail's contact-chip groups.
# The serial batch includes its dedicated close-up under the same GPU lock.
.PHONY: render-rail
render-rail: $(RAIL_OUTPUTS)
render: $(RAIL_OUTPUTS)

.PHONY: repeat match
build/photo-calibration.json: src/matches.py build/shops/117.json
	$(PYTHON) src/matches.py --prepare
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/photo-calibration.json
match: renders/final-matches/.stamp
renders/final-matches/.stamp: $(CHECKPOINT_RENDER_OUTPUTS) build/photo-calibration.json src/render.py src/matches.py
	$(PYTHON) src/matches.py --compose --renders renders/final-matches
	@touch $@

.PHONY: source-matches
source-matches: renders/final-source-matches/.stamp
renders/final-source-matches/.stamp: $(SITE_OUTPUTS) build/photo-calibration.json src/render.py textures/ship/.stamp
	$(PYTHON) src/matches.py --compose --renders renders/final-source-matches
	@touch $@

renders/final-matches/.stamp: $(filter renders/final-matches/%,$(PHOTO_RENDER_OUTPUTS))
renders/final-source-matches/.stamp: $(filter renders/final-source-matches/%,$(PHOTO_RENDER_OUTPUTS))
$(PHOTO_RENDER_OUTPUTS): $(SITE_OUTPUTS)

repeat: model build/photo-calibration.json
	$(PYTHON) src/check.py --repeat

.PHONY: before-after
before-after: render
	$(PYTHON) src/before_delivery.py --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/delivery_evidence.py

.PHONY: texture-repeat
texture-repeat: textures/ship/.stamp
	$(PYTHON) src/texture_repeat.py
.PHONY: check-texture-repeat
check-texture-repeat: texture-repeat
