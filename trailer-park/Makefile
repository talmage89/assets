# Form and construction gate only. No bake, final docs or game-ready claim.
OLD_SEED ?= 101
NEW_SEED ?= 202
ROWS ?= 5
PASS ?= pass4
WIDTH ?= 1440
SAMPLES ?= 32
CHECKPOINT_BLEND := build/family.blend
STEMS := SingleWide-120 SingleWide-147 SingleWide-168 DoubleWide-245 DoubleWide-228 DoubleWide-326 Deck Carport UtilityService PropaneBottles Condenser WindowAC SatelliteDish AddedRoom Household EntranceSign SupportFrame Modules HomeForms Park-$(OLD_SEED) Park-$(NEW_SEED)
CHECKPOINT_OUTPUTS := build/family.blend build/family.json $(foreach s,$(STEMS),export/$(s).gltf export/$(s).bin export/$(s).json)
CHECKPOINT_ARGS := --old-seed $(OLD_SEED) --new-seed $(NEW_SEED) --rows $(ROWS)
CHECKPOINT_DEPS := $(addprefix src/,build.py plans.py geometry.py homes.py addons.py site.py ground_edges.py) build/native.stamp build/preserved.json
CHECKPOINT_CHECK = $(BP) --python src/check.py && $(BP) --python src/check_motion.py
CHECKPOINT_OUT := renders/checkpoint/$(PASS)
CHECKPOINT_RENDER_ARGS := --cameras build/cameras.json
CHECKPOINT_REVIEW = $(PYTHON) src/matches.py compose $(CHECKPOINT_OUT) && $(PYTHON) src/review.py --renders $(CHECKPOINT_OUT)
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

build/cameras.json: src/matches.py src/plans.py
	@mkdir -p build
	$(PYTHON) src/matches.py
$(CHECKPOINT_RENDER_OUTPUTS): build/cameras.json

.PHONY: repeat check-preservation clean-family
repeat: model
	$(PYTHON) src/repeat.py
check-preservation:
	$(PYTHON) src/preservation.py check
clean: clean-family
clean-family:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"
