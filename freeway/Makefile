ASSET := Freeway
BLENDER ?= blender -t 2
WIDTH ?= 1400
SAMPLES ?= 32
SEEDS := 101 202
CHECKPOINT_BLEND := build/Freeway.blend
PARTS := MedianF WBeam GuardrailEnd CableBay SoundPanel SignTruss Cantilever DavitLight GoreAttenuator Overpass PrestressedGirder24 PierBent GorePaving36 RoadStraight RoadCurve RoadBankTransition RampBranch
NATIVE := Hatch SUV HeroHatch Ranch Cape TreeOak TreeMaple Ground Gas
CONTEXT := $(foreach p,$(NATIVE),build/context/$(p).glb) build/context/Signal.glb build/context/Utility.glb
FORM_MAPS := textures/checkpoint/T_Freeway_Signs.png $(foreach c,BaseColor Normal ORM,textures/checkpoint/T_FreewayFenceForm_$(c).png)
CHECKPOINT_OUTPUTS := build/Freeway.blend build/modules.json $(foreach s,$(SEEDS),export/Freeway-$(s).gltf export/Freeway-$(s).bin build/scene-$(s).json build/Freeway-$(s).blend) export/FreewayModules.gltf export/FreewayModules.bin $(foreach p,$(PARTS),export/modules/$(p).gltf export/modules/$(p).bin)
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_DEPS := $(addprefix src/,build.py geom.py plan.py pieces.py roads.py site.py materials.py external.py) $(CONTEXT) $(FORM_MAPS)
CHECKPOINT_OUT := renders/checkpoint
SCENE_SHOTS_101 := hero above alignment barrier guardrail_end sign_structure south_sign pier_girders gore terminal
SCENE_SHOTS_202 := hero above alignment sound_wall cable_median
CHECKPOINT_RENDER_OUTPUTS := renders/checkpoint/.stamp $(foreach s,$(SEEDS),$(foreach v,$(SCENE_SHOTS_$(s)),renders/checkpoint/$(s)/$(v).png))
CHECKPOINT_RENDER_ARGS := --source export/Freeway-101.gltf --seeds $(SEEDS)
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
include ../kit/checkpoint_rules.mk

.PHONY: preserve inputs context sheet scale matches preview repeat
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
renders/checkpoint/modules.png: export/FreewayModules.gltf src/render.py src/module_sheet.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/module_sheet.py -- --width $(WIDTH) --samples $(SAMPLES)
sheet: renders/checkpoint/modules.png
renders/checkpoint/scale.png: export/modules/GuardrailEnd.gltf build/context/Hatch.glb src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --scale --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES)
scale: renders/checkpoint/scale.png
build/cameras.json: src/matches.py | refs
	$(PYTHON) src/matches.py
renders/matches/.stamp: build/cameras.json $(CHECKPOINT_OUTPUTS) src/render.py build/checkpoint-render-parameters.txt
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --camera-file build/cameras.json --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/matches.py --compose
	@touch $@
matches: renders/matches/.stamp
review: sheet scale matches
preview: model
	$(BP) --python src/render.py -- --out renders/preview --engine BLENDER_EEVEE --shots hero above --width 1000 --samples 16
repeat: model
	$(PYTHON) src/repeat.py
