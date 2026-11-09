# Final external PBR delivery; presentation libraries remain read-only.
WIDTH ?= 1600
SAMPLES ?= 48
CHECKPOINT_OUT := renders/final
SEEDS := 301 302 303 304
ROWS := 401 402 403 404
STEMS := $(foreach s,$(SEEDS),Building-$(s) Complex-$(s)) Building-305 $(foreach s,$(ROWS),Row-$(s))
CHECKPOINT_BLEND := build/family.blend
CHECKPOINT_OUTPUTS := $(CHECKPOINT_BLEND) build/family.json $(foreach s,$(STEMS),build/$(s).blend export/$(s).gltf export/$(s).bin export/$(s).json)
CHECKPOINT_DEPS := $(addprefix src/,build.py buildings.py components.py geometry.py plans.py siteworks.py context.py occupancy.py garage_motion.py surfaces.py) ../houses/src/build.py ../houses/src/plan.py ../houses/src/additions.py ../houses/src/glb_budget.py ../houses/src/split_motion.py ../kit/model.py ../kit/tiling.py ../kit/fonts.py build/dependencies.json
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py && $(PYTHON) src/report.py
CHECKPOINT_RENDER_OUTPUTS := $(foreach s,$(SEEDS),$(foreach v,hero above ground rear,renders/final/Complex-$(s)/$(v).png)) $(foreach s,$(ROWS),$(foreach v,hero above ground rear entry patios,renders/final/Row-$(s)/$(v).png)) $(foreach s,$(SEEDS) 305,$(foreach v,stairs balcony meters,renders/final/Building-$(s)/$(v).png)) renders/final/Building-302/mansard.png renders/final/Building-304/mansard.png renders/final/Building-305/mansard.png renders/final/Complex-301/dusk.png
CHECKPOINT_RENDER_OUTPUTS += renders/final/Complex-304/dusk.png $(foreach v,scale front side back top,renders/final/Building-301/$(v).png) $(foreach v,gallery gallery_dusk,renders/final/Building-304/$(v).png) $(foreach v,hero above front side back top dusk,renders/final/Building-305/$(v).png) renders/final/Row-403/garage.png renders/final/Row-403/dusk.png
include ../kit/checkpoint_rules.mk
BP += -t 4

CONTEXT := car tree shrub fence ground
CONTEXT_OUTPUTS := $(foreach c,car tree shrub fence,build/context/$(c)/source.blend) build/context/ground/source.glb
DEPENDENCY_OUTPUTS := build/dependencies.json build/context/utility.glb $(foreach c,BaseColor Normal ORM,textures/ship/T_ApartmentsConcrete_$(c).png textures/ship/T_ApartmentsCedar_$(c).png)
$(DEPENDENCY_OUTPUTS) &: src/dependencies.py src/derive_surfaces.py
	$(PYTHON) src/dependencies.py
$(CHECKPOINT_OUTPUTS): $(DEPENDENCY_OUTPUTS)
build/context/car/source.blend: src/context_build.py ../kit/blender_command.py $(wildcard ../cars/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(PYTHON) ../kit/blender_command.py --threads 1 -- $(BP) --python src/context_build.py -- car > build/context-car.log 2>&1
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
$(CHECKPOINT_RENDER_OUTPUTS): src/presentation.py src/landscaping.py
renders/matches/.stamp: $(CHECKPOINT_OUTPUTS) build/matched-cameras.json src/render.py src/presentation.py src/landscaping.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --camera-file build/matched-cameras.json --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source-pairs --camera-file build/matched-cameras.json --out renders/source-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/source-matches --out renders/source-matches
	@touch $@
matches: refs check-camera renders/matches/.stamp
review: matches
renders/eevee/Complex-301/hero.png: $(CHECKPOINT_OUTPUTS) src/render.py src/presentation.py src/landscaping.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --only Complex-301 --shots hero --engine BLENDER_EEVEE --out renders/eevee --width $(WIDTH) --samples $(SAMPLES)
review: renders/eevee/Complex-301/hero.png

.PHONY: repeat
repeat: model
	$(PYTHON) src/repeat.py

.PHONY: bake export clean-delivery
bake: $(DEPENDENCY_OUTPUTS)
export: model
clean: clean-delivery
clean-delivery:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"

build/preservation.json: src/preserve.py
	$(PYTHON) src/preserve.py
$(CHECKPOINT_OUTPUTS): | build/preservation.json

.PHONY: docs
all: docs
docs: review
	$(PYTHON) src/docs.py
