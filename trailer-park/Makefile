# Dense communities and baked look-dev gate; no docs generation.
OLD_SEED ?= 101
NEW_SEED ?= 202
ROWS ?= 9
PASS ?= look4
WIDTH ?= 1440
SAMPLES ?= 32
CHECKPOINT_BLEND := build/family.blend
STEMS := SingleWide-120 SingleWide-147 SingleWide-168 DoubleWide-245 DoubleWide-228 DoubleWide-326 Deck Carport UtilityService PropaneBottles Condenser WindowAC SatelliteDish AddedRoom Household EntranceSign SupportFrame Modules HomeForms Park-$(OLD_SEED) Park-$(NEW_SEED)
CHECKPOINT_OUTPUTS := build/family.blend build/family.json $(foreach s,$(STEMS),export/$(s).gltf export/$(s).bin export/$(s).json)
CHECKPOINT_ARGS := --old-seed $(OLD_SEED) --new-seed $(NEW_SEED) --rows $(ROWS)
CHECKPOINT_DEPS := $(addprefix src/,build.py plans.py geometry.py homes.py era_details.py addons.py site.py ground_edges.py lot_dressing.py surfaces.py terrain.py textures.py) build/native.stamp build/preserved.json textures/ship/.stamp
CHECKPOINT_CHECK = $(BP) --python src/check.py && $(BP) --python src/check_motion.py && $(BP) --python src/look_check.py
CHECKPOINT_OUT := renders/checkpoint/$(PASS)
BASELINE_REVIEW := $(wildcard build/baseline/export/Baseline_Park-101.gltf)
CHECKPOINT_RENDER_ARGS := --cameras build/cameras.json $(if $(BASELINE_REVIEW),--baseline build/baseline/export)
CHECKPOINT_REVIEW = $(PYTHON) src/matches.py compose $(CHECKPOINT_OUT) && $(PYTHON) src/review.py --renders $(CHECKPOINT_OUT) && $(PYTHON) src/metrics.py --renders $(CHECKPOINT_OUT) $(if $(BASELINE_REVIEW),&& $(PYTHON) src/before_after.py $(CHECKPOINT_OUT))
include ../kit/checkpoint_rules.mk
BP += -t 2
export BLENDER
export PYTHONDONTWRITEBYTECODE := 1

build/native.stamp: src/native_build.py src/dependencies.py $(wildcard ../shed/src/*.py) $(wildcard ../utility/src/*.py) $(wildcard ../playground/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
	@touch $@

build/preserved.json: src/preservation.py
	$(PYTHON) src/preservation.py check

textures/source/.stamp: src/textures.py
	$(PYTHON) src/textures.py
	@touch $@
textures/4k/.stamp: textures/source/.stamp
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source textures/source --out textures/4k --name Manufactured --coverage 4.8768 --height-distance .012 --size 4096 --samples 8
	@touch $@
textures/ship/.stamp: textures/4k/.stamp
	$(PYTHON) $(KIT)/downsample.py --source textures/4k --out textures/ship --asset Manufactured --size 2048
	@touch $@
.PHONY: bake
bake: textures/ship/.stamp

build/cameras.json: src/matches.py src/park_matches.py src/plans.py
	@mkdir -p build
	$(PYTHON) src/matches.py
$(CHECKPOINT_RENDER_OUTPUTS): build/cameras.json src/town_context.py src/inspection.py $(BASELINE_REVIEW)

.PHONY: baseline
baseline:
	$(PYTHON) src/baseline.py

.PHONY: repeat check-preservation clean-family
repeat: model
	$(PYTHON) src/repeat.py
check-preservation:
	$(PYTHON) src/preservation.py check
clean: clean-family
clean-family:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"
