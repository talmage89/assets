# Final civic family. Original shared sets; external images.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
BP = $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
WIDTH ?= 1400
SAMPLES ?= 40
SOURCE := $(addprefix src/,aging.py build.py buildings.py delivery.py door_motion.py flags.py geo.py library.py order.py parts.py plans.py services.py sheets.py sites.py station.py turf.py wear.py)
BUILD_IDS := 101 202 303 404 505 606 707
MODEL := build/family.json build/modules.json $(foreach s,$(BUILD_IDS),export/Civic-$(s).gltf export/Civic-$(s).bin build/review/Civic-$(s).glb) $(foreach s,101 202,export/Site-$(s).gltf export/Site-$(s).bin build/review/Site-$(s).glb) export/CivicPieces.gltf export/CivicPieces.bin build/review/CivicPieces.glb
.PHONY: all refs dependencies model render matches source-matches changes review check repeat check-texture-repeat docs clean
all: refs model check render matches review docs
refs:
	$(PYTHON) ../kit/fetch_refs.py refs
build/dependencies.json: src/prepare.py src/native_props.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/prepare.py
dependencies: build/dependencies.json
$(MODEL) &: $(SOURCE) build/dependencies.json
	$(BP) --python src/build.py
model: $(MODEL)
render: model
	../kit/with_gpu.sh $(PYTHON) src/render_batch.py --out renders/final --width $(WIDTH) --samples $(SAMPLES)
matches: model refs
	$(PYTHON) src/matches.py
	$(BP) --python ../kit/photo_match.py -- verify --calibration build/matched-cameras.json
	../kit/with_gpu.sh $(PYTHON) src/render_batch.py --matches --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) ../kit/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
source-matches: matches
	../kit/with_gpu.sh $(BP) --python src/source_matches.py
	$(PYTHON) ../kit/photo_match.py compose --calibration build/matched-cameras.json --renders renders/source-matches --out renders/source-matches
changes:
	$(PYTHON) src/compare.py
review:
	$(PYTHON) src/review.py
check: model
	$(BP) --python src/check.py
	$(BP) --python src/motion_check.py
	$(PYTHON) ../kit/repo_check.py
repeat: model
	$(PYTHON) src/repeat.py
check-texture-repeat: model
	$(PYTHON) src/texture_repeat.py
docs:
	$(PYTHON) src/gallery.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders','export','textures')]"
