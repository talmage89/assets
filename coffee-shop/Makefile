CHECKPOINT_BLEND := build/coffee.blend
CHECKPOINT_OUTPUTS := build/coffee.blend export/CoffeeShop-117.gltf export/CoffeeShop-228.gltf export/CoffeeShop-339.gltf export/CoffeeShopPieces.gltf
CHECKPOINT_DEPS := $(wildcard src/*.py) build/hosts/downtown.glb build/hosts/strip.glb build/hosts/pad.glb build/preservation.json
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_OUT := renders/checkpoint
CHECKPOINT_RENDER_ARGS := --pass checkpoint
LIBRARY_INPUTS := ../patio-set/export/PatioSet.glb ../street-furniture/export/BikeRack.gltf ../street-furniture/export/Litter.gltf ../street-furniture/export/Recycling.gltf ../ground/textures/ship/T_Concrete_BaseColor.png ../ground/textures/ship/T_Asphalt_BaseColor.png ../ground/textures/ship/T_Lawn_BaseColor.png ../trees/export/RedMaple.glb
CHECKPOINT_DEPS += $(LIBRARY_INPUTS)
include ../kit/checkpoint_rules.mk

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
../street-furniture/export/BikeRack.gltf ../street-furniture/export/Litter.gltf ../street-furniture/export/Recycling.gltf &:
	$(MAKE) -C ../street-furniture export
../ground/textures/ship/T_Concrete_BaseColor.png ../ground/textures/ship/T_Asphalt_BaseColor.png ../ground/textures/ship/T_Lawn_BaseColor.png &:
	$(MAKE) -C ../ground export/Ground.glb
../trees/export/RedMaple.glb:
	$(MAKE) -C ../trees export/RedMaple.glb

build/hosts/%.glb: src/hosts.py
	@mkdir -p build/hosts $(TMPDIR)
	$(BP) --python src/hosts.py -- --kind $* --out $@

.PHONY: repeat match
review: match
match: render
	$(PYTHON) src/matches.py --prepare
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/photo-calibration.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches build/photo-calibration.json --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose

repeat: model
	$(PYTHON) src/check.py --repeat
