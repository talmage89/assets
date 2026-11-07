.DEFAULT_GOAL := all
SEEDS ?= 101,202,303
WIDTH ?= 1200
SAMPLES ?= 32
OUT ?= renders/final
PYTHON ?= python3
BLENDER ?= src/serial_blender.sh
KIT := ../kit
BP = $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
MODULES := RampHeadBridge Deck72 Barrier72 NeckGuard Deck Barrier InfillPanel HipRoof Shade Stairs48 Transfer24 RampSegment RampLanding InterdeckSteps RoofRiser SlideStraight24 SlideStraight48 SlideWave48 SlideWave72 SlideSpiral72 SlideTube48 Arch48 Ladder72 VerticalLadder48 ChainNet48 RockWall48 FirePole OverheadLadder OverheadRings PanelWheel PanelTic PanelPeriscope SwingFrame SwingArchFrame SwingBelt SwingBucket SpringRider Roundabout Post1730 Post2339 Post2949
comma := ,
SEED_LIST := $(subst $(comma), ,$(SEEDS))
SETS := PlayMetal PlayPlastic PlaySurface
MAPS := $(foreach s,$(SETS),$(foreach c,BaseColor Normal ORM,textures/ship/T_$(s)_$(c).png))
MODELS := build/Playground.blend build/manifest.json $(foreach m,$(MODULES) PlaygroundPieces ComparisonDeck ComparisonSwings $(addprefix Playground-,$(SEED_LIST)),export/$(m).gltf export/$(m).bin)
SITE_SHOTS := hero above front side back eevee
DETAIL_SHOTS := clamp-deck stairs transfer slide-entrance slide-exit swing-hanger swing-hollow arch-swing swing-seat bucket-seat climber tube-junction rubber-wear rubber-seams fiber-carryout scale pieces
VIEWS := $(foreach s,$(SEED_LIST),$(foreach v,$(SITE_SHOTS),$(OUT)/$(s)/$(v).png)) $(addprefix $(OUT)/,$(addsuffix .png,$(DETAIL_SHOTS)))
CALIBRATION := build/cameras.json $(addprefix build/photo/,$(addsuffix -balanced.jpg,roswell-2009 adair-2009 playground-2005))
MODEL_SCRIPTS := $(filter-out src/render.py src/review.py src/check.py src/check_lookdev.py src/compare.py src/fix_crops.py src/final_docs.py src/setting.py src/render_batch.py src/repeat.py src/photo_matches.py src/source_pairs.py,$(wildcard src/*.py))
empty :=
space := $(empty) $(empty)
.NOTPARALLEL:
.PHONY: all refs textures model check check-repo render match source-match review docs repeat check-texture-repeat clean compare before-match FORCE
all: refs textures model check render match source-match review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
build/procedural/.stamp: src/textures.py src/finishes.py
	@mkdir -p build/procedural $(TMPDIR)
	$(PYTHON) src/textures.py
	@touch $@
$(MAPS) &: build/procedural/.stamp src/bake_tiles.py $(KIT)/flat_bake.py $(KIT)/downsample.py
	$(BP) --python src/bake_tiles.py
textures: $(MAPS)
build/model-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='$(SEEDS)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(MODELS) &: $(MAPS) build/model-parameters.txt $(MODEL_SCRIPTS)
	$(BP) --python src/build.py -- --lookdev --seeds $(SEEDS) --out build/Playground.blend
model: $(MODELS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: model check-repo
	$(BP) --python src/check.py -- --out build/check.json
	$(PYTHON) src/check_lookdev.py
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='$(WIDTH) $(SAMPLES) $(OUT)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(VIEWS) &: $(MODELS) build/render-parameters.txt src/render.py src/render_batch.py src/setting.py
	$(PYTHON) src/render_batch.py --seeds $(SEEDS) --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --batch-size 5 --shots $(subst $(space),$(comma),$(SITE_SHOTS) $(DETAIL_SHOTS))
render: $(VIEWS)
$(CALIBRATION) &: src/photo_matches.py $(KIT)/photo_match.py
	$(PYTHON) src/photo_matches.py
match: model refs $(CALIBRATION)
	$(BP) --python src/render.py -- --matches --out $(OUT) --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders $(OUT)/matches --out $(OUT)/matches
source-match: model refs $(CALIBRATION)
	$(BP) --python src/source_pairs.py -- --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/source-matches --out renders/source-matches
review:
	$(PYTHON) src/review.py --out $(OUT)
docs: check render match review
	$(PYTHON) src/final_docs.py --renders $(OUT)
repeat: model $(CALIBRATION)
	$(PYTHON) src/repeat.py
check-texture-repeat: repeat
compare:
	$(PYTHON) src/fix_crops.py --after $(OUT)
before-match: $(CALIBRATION)
	$(BP) --python src/render.py -- --matches --export-root ../build/playground-before/export --out renders/fixes-before --width $(WIDTH) --samples $(SAMPLES)
clean:
	rm -rf build export textures renders/final renders/source-matches
