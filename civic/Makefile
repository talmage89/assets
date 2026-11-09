# Form/construction checkpoint only. Original shared sets; external images.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
BP = $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
WIDTH ?= 1400
SAMPLES ?= 40
SOURCE := $(wildcard src/*.py)
.PHONY: all refs dependencies model render matches review check repeat clean
all: refs model check render matches review
refs:
	$(PYTHON) ../kit/fetch_refs.py refs
build/dependencies.json: src/prepare.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/prepare.py
dependencies: build/dependencies.json
build/family.json: $(SOURCE) build/dependencies.json
	$(BP) --python src/build.py
model: build/family.json
render: model
	../kit/with_gpu.sh $(BP) --python src/render.py -- --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES)
matches: model refs
	$(PYTHON) src/matches.py
	$(BP) --python ../kit/photo_match.py -- verify --calibration build/matched-cameras.json
	../kit/with_gpu.sh $(BP) --python src/render.py -- --matches --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) ../kit/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
review:
	$(PYTHON) src/review.py
check: model
	$(BP) --python src/check.py
	$(PYTHON) ../kit/repo_check.py
repeat: model
	$(PYTHON) src/repeat.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders','export','textures')]"
