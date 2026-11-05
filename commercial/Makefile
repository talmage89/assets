SEEDS ?= 101,102,103,104
comma := ,
SEED_LIST := $(subst $(comma), ,$(SEEDS))
MAPS := $(foreach role,CMU Brick Concrete Equipment,$(foreach channel,BaseColor Normal ORM,textures/ship/T_Commercial$(role)_$(channel).png)) $(foreach role,EIFS Roof,$(foreach channel,BaseColor Normal,textures/ship/T_Commercial$(role)_$(channel).png)) textures/ship/T_CommercialGraphics_BaseColor.png textures/ship/T_CommercialGraphics_Emission.png
DELIVERIES := $(foreach seed,$(SEED_LIST),export/CommercialGas-$(seed).gltf export/CommercialGas-$(seed).bin export/CommercialGas-$(seed).json)
CHECKPOINT_BLEND := build/look/station-101.blend
CHECKPOINT_OUTPUTS := $(foreach seed,$(SEED_LIST),build/look/station-$(seed).blend build/look/station-$(seed).glb build/look/station-$(seed).json)
CHECKPOINT_DEPS := $(addprefix src/,build.py plan.py geometry.py building.py equipment.py siteworks.py ground_adapter.py landscape.py age.py surfaces.py textures.py paving.py) $(MAPS) textures/ship/graphics.json ../kit/model.py ../kit/fonts.py ../kit/tiling.py ../ground/src/build.py ../ground/src/dimensions.py ../ground/export/Ground.glb ../shrubs/export/Shrubs.glb
CHECKPOINT_ARGS := --look --seeds $(SEEDS)
SHOTS := hero,above,dispenser,canopy,column,entry,sign,rear,services,asphalt,landscape,dusk,scale,front,side,back,top
CHECKPOINT_RENDER_OUTPUTS := $(foreach shot,hero above dispenser canopy column entry sign rear services asphalt landscape dusk scale front side back top,renders/final/$(shot).png) $(foreach seed,$(SEED_LIST),renders/final/seeds/$(seed)/above.png renders/final/seeds/$(seed)/street.png)
CHECKPOINT_RENDER_ARGS := --source export/CommercialGas-101.gltf --family --shots $(SHOTS)
CHECKPOINT_CHECK = $(PYTHON) src/check_plan.py && $(BP) --python src/check.py -- --source-root build/look --seeds $(SEEDS) --motion && $(BP) --python src/check_delivery.py -- --seeds $(SEEDS)
CHECKPOINT_REVIEW = $(PYTHON) src/final_review.py
CHECKPOINT_OUT := renders/final
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
review: match before-after final-eevee
match: export refs
	$(PYTHON) src/prepare_refs.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out build/look-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/matches.py -- --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py solve --config src/asphalt_match.py --out build/asphalt-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/asphalt_match.py -- --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/look-cameras.json --renders renders/look-matches --out renders/look-matches
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/asphalt-cameras.json --renders renders/look-matches --out renders/look-matches
	$(PYTHON) src/values.py
	$(BP) --python src/check_values.py
before-after: export render
	$(PYTHON) src/revision_comparison.py --blender "$(BLENDER)" --width $(WIDTH) --samples $(SAMPLES)
repeat: export
	$(PYTHON) src/check_repeat.py --blender "$(BLENDER)" --look --brand-swap
fit: model
	$(BP) --python src/check_fit.py -- --reference $(TANK_REFERENCE)
look-review:
	$(CHECKPOINT_REVIEW)

WRITE_DOCS ?= 1
.PHONY: final-eevee docs
all: docs
renders/final-eevee/hero.png: $(DELIVERIES) src/render.py src/presentation.py src/paving.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/CommercialGas-101.gltf --out renders/final-eevee --engine BLENDER_EEVEE --shots hero --width $(WIDTH) --samples $(SAMPLES)
final-eevee: renders/final-eevee/hero.png
docs: review
	$(PYTHON) src/final_review.py $(if $(filter 1,$(WRITE_DOCS)),--docs,)

.PHONY: protected
protected:
	$(PYTHON) src/preserve.py --capture
refs: protected
check: protected

RENDER_DEPS := $(addprefix src/,render.py siteworks.py context.py ground_adapter.py photo_matches.py presentation.py paving.py) ../houses/src/render.py
$(CHECKPOINT_RENDER_OUTPUTS) renders/final-eevee/hero.png: $(RENDER_DEPS)
