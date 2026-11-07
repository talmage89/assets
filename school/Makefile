# Form/construction gate only. No look-dev bake or final documentation gallery.
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
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_OUT := renders/checkpoint
CHECKPOINT_RENDER_ARGS := --seeds $(SEEDS)
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
include ../kit/checkpoint_rules.mk
# Cycles recipes use the kit's shared GPU lock; construction/checks use CPU.
BP := $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1
build/dependencies.json: src/dependencies.py src/context_export.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
.PHONY: matches repeat
matches: model refs
	$(PYTHON) src/matches.py
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python $(KIT)/photo_match.py -- verify --calibration build/matched-cameras.json
	$(KIT)/with_gpu.sh $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1 --python src/render.py -- --matches --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
review: matches
repeat: model
	$(PYTHON) src/repeat.py --seeds $(SEEDS)
.PHONY: clean-delivery
clean: clean-delivery
clean-delivery:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"
