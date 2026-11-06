# Form/construction checkpoint only; no look-dev or final bake is enabled.
SEEDS := 301 302 303 304
ROWS := 401 402 403 404
STEMS := $(foreach s,$(SEEDS),Building-$(s) Complex-$(s)) $(foreach s,$(ROWS),Row-$(s))
CHECKPOINT_BLEND := build/family.blend
CHECKPOINT_OUTPUTS := $(CHECKPOINT_BLEND) build/family.json $(foreach s,$(STEMS),build/$(s).blend export/$(s).gltf export/$(s).bin export/$(s).json)
CHECKPOINT_DEPS := $(addprefix src/,build.py buildings.py components.py geometry.py plans.py siteworks.py context.py occupancy.py garage_motion.py) ../houses/src/build.py ../houses/src/plan.py ../houses/src/additions.py ../houses/src/glb_budget.py ../houses/src/split_motion.py ../kit/model.py ../kit/tiling.py ../kit/fonts.py
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_OUTPUTS := $(foreach s,$(SEEDS),$(foreach v,hero above ground rear,renders/checkpoint/Complex-$(s)/$(v).png)) $(foreach s,$(ROWS),$(foreach v,hero above ground rear entry patios,renders/checkpoint/Row-$(s)/$(v).png)) $(foreach s,$(SEEDS),$(foreach v,stairs balcony meters,renders/checkpoint/Building-$(s)/$(v).png))
include ../kit/checkpoint_rules.mk

CONTEXT := car tree shrub fence ground
CONTEXT_OUTPUTS := $(foreach c,car tree shrub fence,build/context/$(c)/source.blend) build/context/ground/source.glb
$(CHECKPOINT_OUTPUTS): $(CONTEXT_OUTPUTS)
build/context/car/source.blend: src/context_build.py $(wildcard ../cars/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/context_build.py -- car > build/context-car.log 2>&1
build/context/tree/source.blend: src/context_build.py $(wildcard ../trees/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/context_build.py -- tree > build/context-tree.log 2>&1
build/context/shrub/source.blend: src/context_build.py $(wildcard ../shrubs/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/context_build.py -- shrub > build/context-shrub.log 2>&1
build/context/fence/source.blend: src/context_build.py $(wildcard ../fences/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/context_build.py -- fence > build/context-fence.log 2>&1
build/context/ground/source.glb: src/context_build.py $(wildcard ../ground/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/context_build.py -- ground > build/context-ground.log 2>&1

.PHONY: matches check-camera
build/reference-crops.stamp: src/refs.py refs/SOURCES.md
	$(PYTHON) src/refs.py
	@touch $@
build/matched-cameras.json: src/photo_matches.py src/matches.py src/neutral_refs.py src/plans.py build/reference-crops.stamp
	$(PYTHON) src/matches.py
check-camera: build/matched-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $<
renders/matches/.stamp: $(CHECKPOINT_OUTPUTS) build/matched-cameras.json src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --camera-file build/matched-cameras.json --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source-pairs --camera-file build/matched-cameras.json --out renders/source-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/source-matches --out renders/source-matches
	@touch $@
matches: refs check-camera renders/matches/.stamp
review: matches

build/preservation.json: src/preserve.py
	$(PYTHON) src/preserve.py
$(CHECKPOINT_OUTPUTS): build/preservation.json
