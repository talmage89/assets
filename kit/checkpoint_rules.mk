# Opt-in form-generator checkpoint. Assets supply their own measured checks
# and presentation. No bake/delivery target is enabled by this graph.
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO := $(abspath $(KIT)/..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1440
SAMPLES ?= 40
CHECKPOINT_BLEND ?= build/house.blend
CHECKPOINT_ARGS ?=
CHECKPOINT_DEPS ?= $(wildcard src/*.py)
CHECKPOINT_OUT ?= renders/checkpoint
.PHONY: all checkpoint model refs check check-repo render review clean FORCE
.NOTPARALLEL:
all: checkpoint
checkpoint: refs model check render review
build/checkpoint-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='$(CHECKPOINT_ARGS)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(CHECKPOINT_BLEND): $(CHECKPOINT_DEPS) build/checkpoint-parameters.txt
	$(BP) --python src/build.py -- $(CHECKPOINT_ARGS) --out $@
model: $(CHECKPOINT_BLEND)
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: model check-repo
	$(CHECKPOINT_CHECK)
build/checkpoint-render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(CHECKPOINT_OUT)/.stamp: $(CHECKPOINT_BLEND) build/checkpoint-render-parameters.txt src/render.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $(CHECKPOINT_BLEND:.blend=.glb) --out $(CHECKPOINT_OUT) --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
render: $(CHECKPOINT_OUT)/.stamp
review:
	$(CHECKPOINT_REVIEW)
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders')]"
