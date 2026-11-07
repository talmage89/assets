ASSET := Freeway
BLENDER ?= blender -t 2
WIDTH ?= 1400
SAMPLES ?= 32
SEEDS := 101 202
PARTS := MedianF WBeam GuardrailEnd CableBay SoundPanel SignTruss Cantilever DavitLight GoreAttenuator Overpass PrestressedGirder24 PierBent GorePaving36 RoadStraight RoadCurve RoadBankTransition RampBranch
NATIVE := Hatch SUV Crossover HeroHatch HeroSUV HeroCrossover Ranch Cape TreeOak TreeMaple Ground Gas Strip StreetLight
CONTEXT := $(foreach p,$(NATIVE),build/context/$(p).glb) build/context/Signal.glb build/context/Utility.glb
SETS := FreewayConcrete FreewayZinc FreewaySigns FreewayMaintenance
CHANNELS := BaseColor Normal ORM
FORM_MAPS := textures/checkpoint/T_Freeway_Signs.png $(foreach c,$(CHANNELS),textures/checkpoint/T_FreewayFenceForm_$(c).png)
SOURCE_MAPS := $(foreach n,$(SETS),$(foreach c,BaseColor ORM Height,textures/source/T_$(n)_$(c).png)) textures/source/T_FreewayMaintenance_Alpha.png
BAKE_MAPS := $(foreach n,$(SETS),$(foreach c,$(CHANNELS),textures/bake/T_$(n)_$(c).png))
SHIP_MAPS := $(foreach n,$(SETS),$(foreach c,$(CHANNELS),textures/ship/T_$(n)_$(c).png))
CHECKPOINT_BLEND := build/Freeway.blend
CHECKPOINT_OUTPUTS := build/Freeway.blend build/modules.json $(foreach s,$(SEEDS),$(foreach n,Freeway Town Traffic,export/$(n)-$(s).gltf export/$(n)-$(s).bin) build/scene-$(s).json build/Freeway-$(s).blend) export/FreewayModules.gltf export/FreewayModules.bin $(foreach p,$(PARTS),export/modules/$(p).gltf export/modules/$(p).bin)
CHECKPOINT_ARGS := --seeds $(SEEDS) --stage look
CHECKPOINT_DEPS := $(addprefix src/,build.py geom.py plan.py pieces.py roads.py site.py roadside.py neighborhood.py weather.py materials.py look_materials.py textures.py external.py) $(CONTEXT) $(FORM_MAPS) $(SHIP_MAPS)
CHECKPOINT_OUT := renders/lookdev
SCENE_SHOTS_101 := hero above alignment barrier guardrail_end sign_structure south_sign pier_girders gore terminal terminal_controls rail_repair
SCENE_SHOTS_202 := hero above alignment sound_wall cable_median
CHECKPOINT_RENDER_OUTPUTS := renders/lookdev/.stamp $(foreach s,$(SEEDS),$(foreach v,$(SCENE_SHOTS_$(s)),renders/lookdev/$(s)/$(v).png))
CHECKPOINT_RENDER_ARGS := --source export/Freeway-101.gltf --seeds $(SEEDS)
CHECKPOINT_CHECK = $(BP) --python src/check.py && $(BP) --python src/edge_check.py && $(BP) --python src/bridge_check.py && $(BP) --python src/context_check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py && $(PYTHON) src/quality_receipts.py
include ../kit/checkpoint_rules.mk

# The kit still owns the grouped render graph and its single GPU lease. Limit
# scene lifetime inside that lease rather than retaining twelve Cycles views.
RBP = $(PYTHON) src/render_batch.py --blender '$(BLENDER)'
$(CHECKPOINT_RENDER_OUTPUTS): private BP = $(RBP)
$(CHECKPOINT_RENDER_OUTPUTS): src/render_batch.py

.PHONY: preserve inputs context textures sheet scale matches preview repeat check-look evidence
preserve:
	$(PYTHON) src/preserve.py
inputs: preserve
	$(PYTHON) src/dependencies.py
$(foreach p,$(NATIVE),build/context/$(p).glb) &: src/prepare_context.py src/house_context.py | inputs
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/prepare_context.py -- --kind native
build/context/Signal.glb: src/prepare_context.py | preserve
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/prepare_context.py -- --kind signal
build/context/Utility.glb: src/prepare_context.py | preserve
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/prepare_context.py -- --kind utility
context: $(CONTEXT)
$(FORM_MAPS) &: src/graphics.py
	@mkdir -p build
	$(PYTHON) src/graphics.py
$(SOURCE_MAPS) &: src/textures.py $(FORM_MAPS)
	$(PYTHON) src/textures.py --size 4096
$(BAKE_MAPS) &: $(SOURCE_MAPS) src/bake.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake.py
$(SHIP_MAPS) &: $(BAKE_MAPS) src/filter_textures.py
	$(PYTHON) src/filter_textures.py
textures: $(SHIP_MAPS)
check-look: model
	$(PYTHON) src/look_audit.py
check: check-look
renders/lookdev/modules.png: export/FreewayModules.gltf src/render.py src/module_sheet.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/module_sheet.py -- --out renders/lookdev --width 2000 --samples $(SAMPLES)
sheet: renders/lookdev/modules.png
renders/lookdev/scale.png: export/modules/GuardrailEnd.gltf build/context/HeroHatch.glb src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --scale --out renders/lookdev --width $(WIDTH) --samples $(SAMPLES)
scale: renders/lookdev/scale.png
build/cameras.json: src/matches.py | refs
	$(PYTHON) src/matches.py
renders/look-matches/.stamp: build/cameras.json $(CHECKPOINT_OUTPUTS) src/render.py build/checkpoint-render-parameters.txt
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	$(KIT)/with_gpu.sh $(RBP) --python src/render.py -- --camera-file build/cameras.json --out renders/look-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose
	@touch $@
matches: renders/look-matches/.stamp
review: sheet scale matches evidence source-pairs
preview: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/look-preview --engine BLENDER_EEVEE --shots hero above terminal pier_girders --width 1000 --samples 16
repeat: model
	$(PYTHON) src/repeat.py
evidence: render renders/lookdev/modules.png
	$(PYTHON) src/baseline.py
	$(PYTHON) src/evidence.py

.PHONY: source-pairs
renders/source-matches/.stamp: renders/look-matches/.stamp src/source_compare.py
	$(KIT)/with_gpu.sh $(RBP) --python src/render.py -- --camera-file build/cameras.json --source-fields --out renders/source-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) -c "import sys;sys.path.insert(0,'..');from kit.photo_match import compose;compose('build/cameras.json','renders/source-matches','renders/source-matches')"
	@touch $@
source-pairs: renders/source-matches/.stamp

.PHONY: check-texture-repeat
check-texture-repeat: textures
	$(PYTHON) src/texture_repeat.py
