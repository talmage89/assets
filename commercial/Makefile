SEEDS ?= 101,102,103,104
comma := ,
SEED_LIST := $(subst $(comma), ,$(SEEDS))
MAPS := $(foreach role,CMU Brick Trim Equipment,$(foreach channel,BaseColor Normal ORM,textures/ship/T_Commercial$(role)_$(channel).png)) $(foreach role,EIFS Roof,$(foreach channel,BaseColor Normal,textures/ship/T_Commercial$(role)_$(channel).png)) textures/ship/T_CommercialGraphics_BaseColor.png
DELIVERIES := $(foreach seed,$(SEED_LIST),export/CommercialGas-$(seed).gltf export/CommercialGas-$(seed).bin export/CommercialGas-$(seed).json)
CHECKPOINT_BLEND := build/look/station-101.blend
CHECKPOINT_OUTPUTS := $(foreach seed,$(SEED_LIST),build/look/station-$(seed).blend build/look/station-$(seed).glb build/look/station-$(seed).json)
CHECKPOINT_DEPS := $(wildcard src/*.py) $(MAPS) textures/ship/graphics.json ../kit/model.py ../kit/fonts.py ../ground/src/build.py ../ground/src/dimensions.py ../ground/export/Ground.glb ../shrubs/export/Shrubs.glb
CHECKPOINT_ARGS := --look --seeds $(SEEDS)
SHOTS := hero,above,dispenser,canopy,column,entry,sign,rear,services,asphalt,landscape,dusk
CHECKPOINT_RENDER_OUTPUTS := $(foreach shot,hero above dispenser canopy column entry sign rear services asphalt landscape dusk,renders/look-checkpoint/$(shot).png) $(foreach seed,$(SEED_LIST),renders/look-checkpoint/seeds/$(seed)/above.png renders/look-checkpoint/seeds/$(seed)/street.png)
CHECKPOINT_RENDER_ARGS := --source export/CommercialGas-101.gltf --family --shots $(SHOTS)
CHECKPOINT_CHECK = $(PYTHON) src/check_plan.py && $(BP) --python src/check.py -- --source-root build/look --seeds $(SEEDS) --motion && $(BP) --python src/check_delivery.py -- --seeds $(SEEDS)
CHECKPOINT_REVIEW = $(PYTHON) src/review_look.py
CHECKPOINT_OUT := renders/look-checkpoint
include ../kit/checkpoint_rules.mk

.PHONY: textures export match before-after repeat fit context ground-context street-context look-review
build/procedural/fields.json: src/textures.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/textures.py source
build/textures-baked.stamp: build/procedural/fields.json
	$(KIT)/with_gpu.sh $(BP) --python src/textures.py -- bake --samples 4
	@touch $@
$(MAPS) textures/ship/graphics.json textures/ship/sets.json &: build/textures-baked.stamp src/textures.py
	$(PYTHON) src/textures.py ship
textures: $(MAPS) textures/ship/graphics.json
$(DELIVERIES) build/delivery.json &: $(CHECKPOINT_OUTPUTS) src/deliver.py $(MAPS)
	$(PYTHON) src/deliver.py --seeds $(SEEDS)
export: $(DELIVERIES) build/delivery.json
$(CHECKPOINT_RENDER_OUTPUTS): $(DELIVERIES) src/presentation.py
$(CHECKPOINT_RENDER_OUTPUTS): | street-context
check: export ground-context
context:
	$(PYTHON) src/context.py
ground-context:
	$(PYTHON) src/context.py --ground-only
street-context:
	$(PYTHON) src/context.py --street
../shrubs/export/Shrubs.glb:
	$(MAKE) -C ../shrubs export
../ground/export/Ground.glb:
	$(MAKE) -C ../ground export
review: match before-after
match: export refs
	$(PYTHON) src/prepare_refs.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out build/look-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/matches.py -- --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/look-cameras.json --renders renders/look-matches --out renders/look-matches
	$(PYTHON) src/values.py
before-after: export render
	$(PYTHON) src/form_comparison.py --blender "$(BLENDER)" --width $(WIDTH) --samples $(SAMPLES)
repeat: export
	$(PYTHON) src/check_repeat.py --blender "$(BLENDER)" --look --brand-swap
fit: model
	$(BP) --python src/check_fit.py -- --reference $(TANK_REFERENCE)
look-review:
	$(CHECKPOINT_REVIEW)
