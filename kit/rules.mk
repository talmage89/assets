# Asset supplies ASSET / CONFIG / MODEL_SCRIPT. Opt into delivery after look-dev approval.
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO := $(abspath $(KIT)/..)
BUILD := build
CONFIG ?= src/config.py
MODEL_SCRIPT ?= src/build.py
FINAL_PIPELINE ?= 0
WEAR ?= 0.35
SAMPLES ?= 80
WIDTH ?= 1400
BAKE_SAMPLES ?= 32
SHIP_SIZE ?= 2048
UV_TARGET_DENSITY ?= 850
UV_MARGIN ?= .0015
PASS ?= lookdev
SHOTS ?= hero_closed,hero_open,controls,front,side
FINAL_SHOTS ?= hero_closed,hero_open,front,side,back,top,controls,interior,regulator,scale,hose_pose,fit_check
TANK_REFERENCE ?=
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(abspath $(REPO)/../.locks/gpu.lock)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
MODEL_DEPS ?= $(filter-out src/config.py src/review.py src/check_fit.py src/markings.py src/photo_matches.py,$(wildcard src/*.py)) $(KIT)/model.py $(KIT)/materials.py $(KIT)/rig.py
.PHONY: all checkpoint model preview render check check-scene check-repo refs hook-install clean help finalize bake export verify final-render docs check-camera match match-final FORCE
.NOTPARALLEL: all checkpoint check final-render
ifeq ($(FINAL_PIPELINE),1)
all: refs docs check
else
all: checkpoint
endif

$(BUILD)/parameters.txt: FORCE
	@mkdir -p $(BUILD) $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(BUILD)/markings/.stamp: src/markings.py $(BUILD)/parameters.txt
	@mkdir -p $(BUILD)/markings $(TMPDIR)
	$(PYTHON) src/markings.py $(BUILD)/markings --wear $(WEAR)
	@touch $@
$(BUILD)/lookdev.blend: $(MODEL_DEPS) $(BUILD)/markings/.stamp $(BUILD)/parameters.txt
	$(BP) --python $(MODEL_SCRIPT) -- --wear $(WEAR) --out $@
$(BUILD)/game-audit.blend: $(MODEL_DEPS) $(BUILD)/markings/.stamp $(BUILD)/parameters.txt
	$(BP) --python $(MODEL_SCRIPT) -- --wear $(WEAR) --quality game --out $@
model: $(BUILD)/lookdev.blend
preview: model
	$(BP) --python $(KIT)/studio.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --out renders/preview --shots hero_closed,hero_open,controls,front,side --engine BLENDER_WORKBENCH --width 1000
render: model
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --out renders/$(PASS) --shots $(SHOTS) --width $(WIDTH) --samples $(SAMPLES) --fit-reference "$(TANK_REFERENCE)"
check-scene: $(BUILD)/game-audit.blend $(BUILD)/lookdev.blend
	$(BP) --python $(KIT)/audit.py -- --source $(BUILD)/game-audit.blend --config $(CONFIG) --out $(BUILD)/game-audit.json
	$(BP) --python $(KIT)/audit.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --out $(BUILD)/lookdev-audit.json
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: check-scene check-repo $(if $(wildcard src/photo_matches.py),check-camera)
ifeq ($(FINAL_PIPELINE),1)
check: verify
endif
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
hook-install:
	$(PYTHON) $(KIT)/install_hook.py
checkpoint: refs model check-scene check-repo render $(if $(wildcard src/photo_matches.py),match)
	@if test -f src/review.py; then $(PYTHON) src/review.py --renders renders/$(PASS); else $(PYTHON) $(KIT)/contact.py --out renders/$(PASS)/contact.jpg renders/$(PASS)/hero_closed.png; fi

$(BUILD)/matched-cameras.json: src/photo_matches.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
check-camera: $(BUILD)/matched-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $(BUILD)/matched-cameras.json
match: model refs $(BUILD)/matched-cameras.json
	@mkdir -p renders/$(PASS)
	@cp $(BUILD)/matched-cameras.json renders/$(PASS)/matched-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --camera-file $(BUILD)/matched-cameras.json --out renders/$(PASS) --shots "$(shell $(PYTHON) -c "import json; print(','.join(json.load(open('$(BUILD)/matched-cameras.json'))))" 2>/dev/null)" --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration $(BUILD)/matched-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
match-final: export refs $(BUILD)/matched-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source export/$(ASSET).glb --config $(CONFIG) --camera-file $(BUILD)/matched-cameras.json --out renders/$(PASS)-glb --shots "$(shell $(PYTHON) -c "import json; print(','.join(json.load(open('$(BUILD)/matched-cameras.json'))))" 2>/dev/null)" --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration $(BUILD)/matched-cameras.json --renders renders/$(PASS)-glb --out renders/$(PASS)-glb

$(BUILD)/delivery-parameters.txt: FORCE
	@mkdir -p $(BUILD)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(SHIP_SIZE) density=$(UV_TARGET_DENSITY) margin=$(UV_MARGIN)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(BUILD)/finalized.blend: $(BUILD)/game-audit.blend $(CONFIG) $(KIT)/finalize.py $(KIT)/uv.py $(BUILD)/delivery-parameters.txt
	$(BP) --python $(KIT)/finalize.py -- --source $< --config $(CONFIG) --out $@ --report $(BUILD)/uv-report.json --size $(SHIP_SIZE) --target-density $(UV_TARGET_DENSITY) --margin $(UV_MARGIN)
finalize: $(BUILD)/finalized.blend
$(BUILD)/baked.stamp: $(BUILD)/finalized.blend $(BUILD)/lookdev.blend $(KIT)/bake.py $(KIT)/image_io.py $(KIT)/gpu.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low $(BUILD)/finalized.blend --high $(BUILD)/lookdev.blend --out textures/bake --asset $(ASSET) --size 4096 --samples $(BAKE_SAMPLES) --config $(CONFIG)
	@touch $@
bake: $(BUILD)/baked.stamp
$(BUILD)/textures.stamp: $(BUILD)/baked.stamp $(KIT)/downsample.py $(KIT)/image_io.py
	$(PYTHON) $(KIT)/downsample.py --source textures/bake --out textures/ship --asset $(ASSET) --size $(SHIP_SIZE)
	@touch $@
export/$(ASSET).glb: $(BUILD)/finalized.blend $(BUILD)/textures.stamp $(KIT)/export.py
	$(BP) --python $(KIT)/export.py -- --source $(BUILD)/finalized.blend --textures textures/ship --asset $(ASSET) --out $@ --report $(BUILD)/export-report.json --config $(CONFIG)
export: export/$(ASSET).glb
verify: export/$(ASSET).glb
	$(BP) --python $(KIT)/verify.py -- --source $< --expected $(BUILD)/export-report.json --config $(CONFIG) --out $(BUILD)/delivery-check.json --size $(SHIP_SIZE)
	@if test -f src/check_fit.py; then $(BP) --python src/check_fit.py -- --grill $< --reference "$(TANK_REFERENCE)" --out $(BUILD)/fit-check.json; fi
$(BUILD)/studio-parameters.txt: FORCE
	@mkdir -p $(BUILD)
	@$(PYTHON) -c "from pathlib import Path; import sys; r=Path(sys.argv[1]).expanduser(); p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) reference='+sys.argv[1]+' mtime='+str(r.stat().st_mtime_ns if sys.argv[1] and r.is_file() else None); p.write_text(s) if not p.exists() or p.read_text()!=s else None" "$(TANK_REFERENCE)"
renders/final/.stamp: export/$(ASSET).glb $(CONFIG) $(KIT)/studio.py $(KIT)/rig.py $(BUILD)/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --out renders/final --shots $(FINAL_SHOTS) --width $(WIDTH) --samples $(SAMPLES) --fit-reference "$(TANK_REFERENCE)"
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --out renders/final-eevee --shots hero_closed --engine BLENDER_EEVEE --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-render: renders/final/.stamp
docs: final-render src/review.py
	$(PYTHON) src/review.py --final --renders renders/final
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders/final','renders/final-eevee')]"
help:
	@echo 'make | checkpoint | model | preview | render | match | finalize | bake | export | verify | final-render | docs | check | refs | hook-install'
	@echo 'FINAL_PIPELINE=1 opts into 4096 GPU bake / 2048 textures / skinned GLB / final imported-GLB studio'
