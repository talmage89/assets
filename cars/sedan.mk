# Source-only sedan gate; the accepted pickup delivery graph stays independent.
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1600
SAMPLES ?= 40
PASS ?= sedan-form
OUT := renders/$(PASS)
SDEPS := src/build.py src/sedan_body.py src/sedan_spec.py src/forms.py src/wheels.py src/detail_helpers.py ../kit/model.py ../kit/vehicle.py
CLAY := front_three_quarter rear_three_quarter side front top
STRIPES := stripes_horizontal stripes_vertical
PAIRS := accord_front camry_rear
.NOTPARALLEL:
.PHONY: all model refs check render review FORCE
all: refs model check render review
build/sedan/parameters.txt: FORCE
	@mkdir -p build/sedan $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) out=$(OUT)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/sedan/game.blend: $(SDEPS)
	@mkdir -p build/sedan $(TMPDIR)
	$(BP) --python src/build.py -- --body sedan --form-only --quality game --out $@
build/sedan/high.blend: $(SDEPS)
	@mkdir -p build/sedan $(TMPDIR)
	$(BP) --python src/build.py -- --body sedan --form-only --quality high --out $@
model: build/sedan/game.blend build/sedan/high.blend
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only sedan-accord-front.jpg sedan-accord-rear.jpg sedan-camry-front.jpg sedan-camry-rear.jpg sedan-camry-side.jpg sedan-camry-specs.pdf
build/sedan/cameras.json: src/sedan_matches.py src/sedan_spec.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/sedan_matches.py --out $@
build/sedan/form-check.json: build/sedan/game.blend src/sedan_check.py
	$(BP) --python src/sedan_check.py -- --source $< --out $@
check: model refs build/sedan/cameras.json build/sedan/form-check.json
	$(BP) --python $(KIT)/audit.py -- --source build/sedan/game.blend --config src/sedan_config.py --out build/sedan/game-audit.json
	$(BP) --python $(KIT)/audit.py -- --source build/sedan/high.blend --config src/sedan_config.py --out build/sedan/high-audit.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/sedan/cameras.json
	$(PYTHON) $(KIT)/repo_check.py
$(addprefix $(OUT)/,$(addsuffix .png,$(CLAY))) &: build/sedan/game.blend build/sedan/form-check.json src/sedan_render.py build/sedan/parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/sedan_render.py -- --source build/sedan/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode clay
$(addprefix $(OUT)/,$(addsuffix .png,$(STRIPES))) &: build/sedan/game.blend build/sedan/form-check.json src/sedan_render.py build/sedan/parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/sedan_render.py -- --source build/sedan/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode stripes
$(addprefix $(OUT)/,$(addsuffix .png,$(PAIRS))) &: build/sedan/game.blend build/sedan/form-check.json build/sedan/cameras.json src/sedan_render.py build/sedan/parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/sedan_render.py -- --source build/sedan/game.blend --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --mode pairs --cameras build/sedan/cameras.json
render: $(addprefix $(OUT)/,$(addsuffix .png,$(CLAY) $(STRIPES) $(PAIRS)))
review: render
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/sedan/cameras.json --renders $(OUT) --out $(OUT)
	$(PYTHON) src/sedan_review.py --renders $(OUT) --report build/sedan/form-check.json --cameras build/sedan/cameras.json
