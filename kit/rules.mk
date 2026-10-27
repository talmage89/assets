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
BAKE_SIZE ?= 4096
# TEX_SIZE is the older grill spelling. Normalize it once; reject ambiguity.
ifdef TEX_SIZE
ifdef SHIP_SIZE
ifneq ($(SHIP_SIZE),$(TEX_SIZE))
$(error SHIP_SIZE and legacy TEX_SIZE disagree; specify only SHIP_SIZE)
endif
else
SHIP_SIZE := $(TEX_SIZE)
endif
endif
SHIP_SIZE ?= 2048
UV_TARGET_DENSITY ?= 850
UV_MARGIN ?= .0015
PASS ?= lookdev
SHOTS ?= hero_closed,hero_open,controls,front,side
EEVEE_SHOT ?= hero_closed
FINAL_SHOTS ?= hero_closed,hero_open,front,side,back,top,controls,interior,regulator,scale,hose_pose,fit_check
REFS_DIR ?= refs
TANK_REFERENCE ?=
FIT_CHECK_ARGS ?=
EXPORT_ARGS ?=
STUDIO_ARGS ?=
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
MODEL_DEPS ?= $(filter-out src/config.py src/review.py src/check_fit.py src/check_construction.py src/markings.py src/photo_matches.py,$(wildcard src/*.py)) $(KIT)/model.py $(KIT)/materials.py $(KIT)/rig.py
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
$(BUILD)/markings/.stamp: src/markings.py $(MARKINGS_DEPS) $(BUILD)/parameters.txt
	@mkdir -p $(BUILD)/markings $(TMPDIR)
	$(PYTHON) src/markings.py $(BUILD)/markings --wear $(WEAR)
	@touch $@
$(BUILD)/lookdev.blend: $(MODEL_DEPS) $(BUILD)/markings/.stamp $(BUILD)/parameters.txt
	$(BP) --python $(MODEL_SCRIPT) -- --wear $(WEAR) --out $@
$(BUILD)/game-audit.blend: $(MODEL_DEPS) $(BUILD)/markings/.stamp $(BUILD)/parameters.txt
	$(BP) --python $(MODEL_SCRIPT) -- --wear $(WEAR) --quality game --out $@
model: $(BUILD)/lookdev.blend
preview: model
	$(BP) --python $(KIT)/studio.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --out renders/preview --shots hero_closed,hero_open,controls,front,side --engine BLENDER_WORKBENCH --width 1000 $(STUDIO_ARGS)
render: model
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --out renders/$(PASS) --shots $(SHOTS) --width $(WIDTH) --samples $(SAMPLES) --fit-reference "$(TANK_REFERENCE)" $(STUDIO_ARGS)
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
	$(PYTHON) $(KIT)/fetch_refs.py $(REFS_DIR)
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
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --camera-file $(BUILD)/matched-cameras.json --out renders/$(PASS) --shots "$(shell $(PYTHON) -c "import json; print(','.join(json.load(open('$(BUILD)/matched-cameras.json'))))" 2>/dev/null)" --width $(WIDTH) --samples $(SAMPLES) $(STUDIO_ARGS)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration $(BUILD)/matched-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
match-final: export refs $(BUILD)/matched-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source export/$(ASSET).glb --config $(CONFIG) --camera-file $(BUILD)/matched-cameras.json --out renders/$(PASS)-glb --shots "$(shell $(PYTHON) -c "import json; print(','.join(json.load(open('$(BUILD)/matched-cameras.json'))))" 2>/dev/null)" --width $(WIDTH) --samples $(SAMPLES) $(STUDIO_ARGS)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration $(BUILD)/matched-cameras.json --renders renders/$(PASS)-glb --out renders/$(PASS)-glb

$(BUILD)/delivery-parameters.txt: FORCE
	@mkdir -p $(BUILD)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(SHIP_SIZE) density=$(UV_TARGET_DENSITY) margin=$(UV_MARGIN) export_args=$(EXPORT_ARGS)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(BUILD)/finalized.blend: $(BUILD)/game-audit.blend $(CONFIG) $(KIT)/finalize.py $(KIT)/uv.py $(KIT)/atlas.py $(BUILD)/delivery-parameters.txt
	$(BP) --python $(KIT)/finalize.py -- --source $< --config $(CONFIG) --out $@ --report $(BUILD)/uv-report.json --size $(SHIP_SIZE) --target-density $(UV_TARGET_DENSITY) --margin $(UV_MARGIN)
finalize: $(BUILD)/finalized.blend
$(BUILD)/bake-parameters.txt: FORCE
	@mkdir -p $(BUILD)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(BUILD)/baked.stamp: $(BUILD)/bake-parameters.txt $(BUILD)/finalized.blend $(BUILD)/lookdev.blend $(KIT)/bake.py $(KIT)/atlas.py $(KIT)/bake_groups.py $(KIT)/image_io.py $(KIT)/gpu.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low $(BUILD)/finalized.blend --high $(BUILD)/lookdev.blend --out textures/bake --asset $(ASSET) --config $(CONFIG) --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch $@
bake: $(BUILD)/baked.stamp
$(BUILD)/textures.stamp: $(BUILD)/baked.stamp $(KIT)/downsample.py $(KIT)/image_io.py $(TEXTURE_DEPS)
	$(PYTHON) $(KIT)/downsample.py --source textures/bake --out textures/ship --asset $(ASSET) --size $(SHIP_SIZE)
	$(if $(TEXTURE_POSTPROCESS),$(TEXTURE_POSTPROCESS),@:)
	@touch $@
export/$(ASSET).glb: $(BUILD)/finalized.blend $(BUILD)/textures.stamp $(KIT)/export.py $(KIT)/atlas.py $(KIT)/glb_textures.py
	$(BP) --python $(KIT)/export.py -- --source $(BUILD)/finalized.blend --textures textures/ship --asset $(ASSET) --out $@ --report $(BUILD)/export-report.json --config $(CONFIG) $(EXPORT_ARGS)
export: export/$(ASSET).glb
verify: export/$(ASSET).glb
	$(BP) --python $(KIT)/verify.py -- --source $< --expected $(BUILD)/export-report.json --config $(CONFIG) --out $(BUILD)/delivery-check.json --size $(SHIP_SIZE)
	@if test -f src/check_fit.py; then $(BP) --python src/check_fit.py -- --grill $< --reference "$(TANK_REFERENCE)" --out $(BUILD)/fit-check.json $(FIT_CHECK_ARGS); fi
$(BUILD)/studio-parameters.txt: FORCE
	@mkdir -p $(BUILD)
	@$(PYTHON) -c "from pathlib import Path; import sys; r=Path(sys.argv[1]).expanduser(); p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) shots=$(FINAL_SHOTS) eevee=$(EEVEE_SHOT) args=$(STUDIO_ARGS) reference='+sys.argv[1]+' mtime='+str(r.stat().st_mtime_ns if sys.argv[1] and r.is_file() else None); p.write_text(s) if not p.exists() or p.read_text()!=s else None" "$(TANK_REFERENCE)"
renders/final/.stamp: export/$(ASSET).glb $(CONFIG) $(KIT)/studio.py $(KIT)/rig.py $(BUILD)/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --out renders/final --shots $(FINAL_SHOTS) --width $(WIDTH) --samples $(SAMPLES) --fit-reference "$(TANK_REFERENCE)" $(STUDIO_ARGS)
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --out renders/final-eevee --shots $(EEVEE_SHOT) --engine BLENDER_EEVEE --width $(WIDTH) --samples $(SAMPLES) $(STUDIO_ARGS)
	@touch $@
final-render: renders/final/.stamp
docs: final-render src/review.py
	$(PYTHON) src/review.py --final --renders renders/final
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders/final','renders/final-eevee')]"
help:
	@echo 'make | checkpoint | model | preview | render | match | finalize | bake | export | verify | final-render | docs | check | refs | hook-install'
	@echo 'FINAL_PIPELINE=1: BAKE_SIZE=$(BAKE_SIZE) GPU bake / SHIP_SIZE=$(SHIP_SIZE) textures / GLB / imported-GLB studio'

.PHONY: check-motion
check-motion: $(BUILD)/game-audit.blend $(BUILD)/lookdev.blend
	$(BP) --python $(KIT)/motion.py -- --source $(BUILD)/game-audit.blend --config $(CONFIG) --out $(BUILD)/motion-game.json
	$(BP) --python $(KIT)/motion.py -- --source $(BUILD)/lookdev.blend --config $(CONFIG) --out $(BUILD)/motion-high.json
check: check-motion

.PHONY: check-texture-repeat
# Opt-in expensive reproducibility test; normal `check` never rebakes other assets.
check-texture-repeat: $(BUILD)/textures.stamp
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low $(BUILD)/finalized.blend --high $(BUILD)/lookdev.blend --out $(BUILD)/repeat-bake --asset $(ASSET) --config $(CONFIG) --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	$(PYTHON) $(KIT)/downsample.py --source $(BUILD)/repeat-bake --out $(BUILD)/repeat-ship --asset $(ASSET) --size $(SHIP_SIZE)
	$(PYTHON) $(KIT)/compare_textures.py --reference textures/ship --candidate $(BUILD)/repeat-ship --out $(BUILD)/texture-repeat.json $(TEXTURE_COMPARE_ARGS)
