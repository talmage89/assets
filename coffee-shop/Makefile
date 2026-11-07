CHECKPOINT_BLEND := build/coffee.blend
CHECKPOINT_OUTPUTS := build/coffee.blend export/CoffeeShop-117.gltf export/CoffeeShop-228.gltf export/CoffeeShop-339.gltf export/CoffeeShopPieces.gltf
CHECKPOINT_DEPS := $(filter-out src/render.py src/review.py src/sites.py src/matches.py,$(wildcard src/*.py)) build/hosts/downtown.glb build/hosts/strip.glb build/hosts/pad.glb build/preservation.json textures/ship/.stamp
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_CHECK += && $(BP) --python src/check_lookdev.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_OUT := renders/lookdev
CHECKPOINT_RENDER_ARGS := --pass lookdev
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

../downtown/textures/ship/textures.json:
	$(MAKE) -C ../downtown bake
build/hosts/downtown.glb build/hosts/downtown-left.glb build/hosts/downtown-right.glb build/hosts/downtown-opposite.glb: ../downtown/textures/ship/textures.json

textures/ship/.stamp: src/graphics.py src/bake_atlas.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake_atlas.py
	@touch $@

.PHONY: sites
sites: build/sites/.stamp
build/sites/.stamp: $(CHECKPOINT_OUTPUTS) src/sites.py build/hosts/downtown-left.glb build/hosts/downtown-right.glb build/hosts/downtown-opposite.glb build/hosts/strip-neighbors.glb
	$(BP) --python src/sites.py
	@touch $@
$(CHECKPOINT_RENDER_OUTPUTS): | sites
check: sites

.PHONY: repeat match
review: match
match: render
	$(PYTHON) src/matches.py --prepare
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/photo-calibration.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches build/photo-calibration.json --out renders/lookdev-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose

repeat: model
	$(PYTHON) src/check.py --repeat

.PHONY: before-after
before-after: render
	$(PYTHON) src/compare_views.py
