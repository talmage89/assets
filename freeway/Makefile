ASSET := Freeway
BLENDER ?= blender -t 2
WIDTH ?= 1400
SAMPLES ?= 32
SEEDS := 101 202
PARTS := MedianF WBeam GuardrailEnd CableBay SoundPanel SignTruss Cantilever DavitLight GoreAttenuator Overpass PrestressedGirder24 PierBent GorePaving36 RoadStraight RoadCurve RoadBankTransition RampBranch
NATIVE := Hatch SUV Crossover HeroHatch HeroSUV HeroCrossover Ranch Cape Ranch14 Cape33 Cape36 Apartment TreeOak TreeMaple Ground Gas Strip StreetLight
CONTEXT := $(foreach p,$(NATIVE),build/context/$(p).glb) build/context/Signal.glb build/context/Utility.glb
CONTEXT_COLOR_MAPS := $(foreach b,AlderH120 AlderX220 AlderC150,$(foreach c,Porcelain Carbon Aluminum Graphite Garnet Spruce Sand,textures/context/$(b)Paint_$(c).png))
SETS := FreewayConcrete FreewayZinc FreewaySigns FreewayMaintenance
CHANNELS := BaseColor Normal ORM
FORM_MAPS := textures/checkpoint/T_Freeway_Signs.png $(foreach c,$(CHANNELS),textures/checkpoint/T_FreewayFenceForm_$(c).png)
SOURCE_MAPS := $(foreach n,$(SETS),$(foreach c,BaseColor ORM Height,textures/source/T_$(n)_$(c).png)) textures/source/T_FreewayMaintenance_Alpha.png
BAKE_MAPS := $(foreach n,$(SETS),$(foreach c,$(CHANNELS),textures/bake/T_$(n)_$(c).png))
SHIP_MAPS := $(foreach n,$(SETS),$(foreach c,$(CHANNELS),textures/ship/T_$(n)_$(c).png))
CHECKPOINT_BLEND := build/Freeway.blend
CHECKPOINT_OUTPUTS := build/Freeway.blend build/modules.json $(foreach s,$(SEEDS),$(foreach n,Freeway Town Traffic,export/$(n)-$(s).gltf export/$(n)-$(s).bin) build/scene-$(s).json build/Freeway-$(s).blend) export/FreewayModules.gltf export/FreewayModules.bin $(foreach p,$(PARTS),export/modules/$(p).gltf export/modules/$(p).bin)
CHECKPOINT_ARGS := --seeds $(SEEDS) --stage look
CHECKPOINT_DEPS := $(addprefix src/,build.py geom.py plan.py pieces.py roads.py site.py roadside.py neighborhood.py weather.py column_age.py materials.py look_materials.py textures.py external.py context_colors.py town_context.py landscape.py turf_cards.py) $(CONTEXT) $(CONTEXT_COLOR_MAPS) $(FORM_MAPS) $(SHIP_MAPS)
CHECKPOINT_OUT := renders/final
SCENE_SHOTS_101 := hero hero_previous hero_cut above above_clean alignment barrier guardrail_end sign_structure south_sign pier_girders bearings gore terminal terminal_controls rail_repair
SCENE_SHOTS_202 := hero hero_old above above_clean alignment sound_wall cable_median
PRESENTATION_OUTPUTS := renders/final/modules.png renders/final/scale.png renders/final-eevee/101/hero.png renders/final-matches/.stamp renders/final-source-matches/.stamp $(foreach p,$(PARTS),renders/final/modules/$(p).png)
CHECKPOINT_RENDER_OUTPUTS := renders/final/.stamp $(foreach s,$(SEEDS),$(foreach v,$(SCENE_SHOTS_$(s)),renders/final/$(s)/$(v).png)) $(PRESENTATION_OUTPUTS)
CHECKPOINT_RENDER_ARGS := --source export/Freeway-101.gltf --seeds $(SEEDS) --all-inspections
CHECKPOINT_CHECK = $(PYTHON) src/accepted_check.py && $(BP) --python src/check.py && $(BP) --python src/edge_check.py && $(BP) --python src/bridge_check.py && $(BP) --python src/context_check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py && $(PYTHON) src/quality_receipts.py --folder renders/final
include ../kit/checkpoint_rules.mk

# The kit still owns the grouped render graph and its single GPU lease. Limit
# scene lifetime inside that lease rather than retaining twelve Cycles views.
RBP = $(PYTHON) src/render_batch.py --blender '$(BLENDER)'
$(CHECKPOINT_RENDER_OUTPUTS): private BP = $(RBP)
$(CHECKPOINT_RENDER_OUTPUTS): src/render_batch.py src/module_sheet.py src/presentation_batch.py src/source_compare.py src/foliage_adapter.py src/render_recipe.py ../kit/foliage.py ../trees/src/leaf_material.py build/camera-verification.stamp

.PHONY: preserve inputs context textures sheet scale matches preview repeat check-look evidence
preserve:
	$(PYTHON) src/preserve.py
inputs: preserve
	$(PYTHON) src/dependencies.py
$(foreach p,$(filter-out Apartment,$(NATIVE)),build/context/$(p).glb) &: src/prepare_context.py src/house_context.py | inputs
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/prepare_context.py -- --kind native
build/context/Apartment.glb: src/apartment_context.py | inputs
	$(BP) --python src/apartment_context.py
build/context/Signal.glb: src/prepare_context.py | preserve
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/prepare_context.py -- --kind signal
build/context/Utility.glb: src/prepare_context.py | preserve
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/prepare_context.py -- --kind utility
context: $(CONTEXT)
$(CONTEXT_COLOR_MAPS) &: src/context_colors.py build/context/Hatch.glb build/context/SUV.glb build/context/Crossover.glb
	$(PYTHON) src/context_colors.py
$(FORM_MAPS) &: src/graphics.py
	@mkdir -p build
	$(PYTHON) src/graphics.py
$(SOURCE_MAPS) &: src/textures.py $(FORM_MAPS)
	$(PYTHON) src/textures.py --size 4096
$(BAKE_MAPS) &: $(SOURCE_MAPS) src/bake.py src/bake_dispatch.py
	$(PYTHON) src/bake_dispatch.py --blender '$(BLENDER)'
$(SHIP_MAPS) &: $(BAKE_MAPS) src/filter_textures.py
	$(PYTHON) src/filter_textures.py
textures: $(SHIP_MAPS)
check-look: model
	$(PYTHON) src/look_audit.py
check: check-look check-retained
.PHONY: check-retained
check-retained: model
	$(PYTHON) src/retained_context.py
build/cameras.json: src/matches.py | refs
	$(PYTHON) src/matches.py
build/camera-verification.stamp: build/cameras.json $(KIT)/photo_match.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	@touch $@
sheet: renders/final/modules.png
scale: renders/final/scale.png
matches: renders/final-matches/.stamp
review: sheet scale matches evidence source-pairs
preview: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/look-preview --engine BLENDER_EEVEE --shots hero above terminal pier_girders --width 1000 --samples 16
repeat: model
	$(PYTHON) src/repeat.py
evidence: render
	$(PYTHON) src/final_evidence.py
	$(PYTHON) src/round4_evidence.py

.PHONY: source-pairs
source-pairs: renders/final-source-matches/.stamp

.PHONY: check-texture-repeat
check-texture-repeat: textures
	$(PYTHON) src/texture_repeat.py

.PHONY: docs
all: docs
docs: review
	$(PYTHON) src/docs.py
