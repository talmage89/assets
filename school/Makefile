# Look-dev gate: shared canonical bakes, no final documentation gallery.
WIDTH ?= 1400
SAMPLES ?= 32
BLENDER := ./src/blender.sh
SEEDS ?= 101,102,103
comma := ,
SEED_LIST := $(subst $(comma), ,$(SEEDS))
CHECKPOINT_BLEND := build/family.blend
CHECKPOINT_OUTPUTS := build/family.blend build/family.json $(foreach s,$(SEED_LIST),export/School-$(s).gltf export/Campus-$(s).gltf)
CHECKPOINT_DEPS := $(wildcard src/*.py) build/dependencies.json
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_CHECK = $(BP) --python src/check.py && $(PYTHON) src/delivery_audit.py
CHECKPOINT_OUT := renders/lookdev
CHECKPOINT_RENDER_ARGS := --seeds $(SEEDS)
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
include ../kit/checkpoint_rules.mk
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
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python src/render.py -- --matches --out renders/look-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/look-matches --out renders/look-matches
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python src/render.py -- --matches --source-scene --out renders/source-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/source-matches --out renders/source-matches
eevee: model
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python src/render.py -- --seeds 101 --shots hero --engine BLENDER_EEVEE --out renders/eevee --width $(WIDTH) --samples $(SAMPLES)
review: matches eevee
repeat: model
	$(PYTHON) src/repeat.py --seeds $(SEEDS)
.PHONY: clean-delivery
clean: clean-delivery
clean-delivery:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"
