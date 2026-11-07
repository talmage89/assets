# Final external-image delivery, native context and explicit visual evidence.
WIDTH ?= 1400
SAMPLES ?= 48
BLENDER := ./src/blender.sh
SEEDS ?= 101,102,103
comma := ,
SEED_LIST := $(subst $(comma), ,$(SEEDS))
CHECKPOINT_BLEND := build/family.blend
CHECKPOINT_OUTPUTS := build/family.blend build/family.json $(foreach s,$(SEED_LIST),export/School-$(s).gltf export/Campus-$(s).gltf)
CHECKPOINT_DEPS := $(addprefix src/,build.py buildings.py geometry.py plans.py siteplan.py siteworks.py surfaces.py) build/dependencies.json
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_CHECK = $(BP) --python src/check.py && $(PYTHON) src/delivery_audit.py
CHECKPOINT_OUT := renders/final
CHECKPOINT_RENDER_ARGS := --seeds $(SEEDS) --shots hero,above,plan,rear,windows,entry,gym,door,roof,scale,blacktop,front,side,accepted_hero
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
include ../kit/checkpoint_rules.mk
$(CHECKPOINT_RENDER_OUTPUTS): src/neighborhood.py src/siteplan.py src/plans.py
# Cycles recipes use the kit's shared GPU lock; construction/checks use CPU.
BP := $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1
build/dependencies.json: src/dependencies.py src/context_export.py src/neighborhood_build.py src/bake_shared.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
.PHONY: matches repeat eevee baseline
baseline: build/dependencies.json
	$(PYTHON) src/baseline.py
model: baseline
matches: model refs
	$(PYTHON) src/matches.py
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python $(KIT)/photo_match.py -- verify --calibration build/matched-cameras.json
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python src/render.py -- --matches --out renders/final-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/final-matches --out renders/final-matches
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python src/render.py -- --matches --source-scene --out renders/source-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/source-matches --out renders/source-matches
eevee: model
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python src/render.py -- --seeds 101 --shots hero --engine BLENDER_EEVEE --out renders/eevee --width $(WIDTH) --samples $(SAMPLES)
review: matches eevee fixes
repeat: model
	$(PYTHON) src/repeat.py --seeds $(SEEDS)
.PHONY: fixes docs check-texture-repeat
BEFORE_STAMPS := $(foreach s,$(SEED_LIST),renders/fix-before/$(s)/.stamp)
renders/fix-before/%/.stamp: $(CHECKPOINT_OUTPUTS) src/render.py src/neighborhood.py build/checkpoint-render-parameters.txt | baseline
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --package-dir build/accepted-lookdev/export --seeds $* --shots hero,above,entry,windows,door --out renders/fix-before --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
renders/fix-before-matches/.stamp: $(CHECKPOINT_OUTPUTS) src/render.py src/neighborhood.py build/matched-cameras.json build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --package-dir build/accepted-lookdev/export --matches --shots ribbon --out renders/fix-before-matches --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
fixes: model render $(BEFORE_STAMPS) renders/fix-before-matches/.stamp
	$(PYTHON) src/fix_evidence.py
docs:
	$(PYTHON) src/review.py --final
check-texture-repeat: model
	$(PYTHON) src/texture_repeat.py
.PHONY: clean-delivery
clean: clean-delivery
clean-delivery:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"
