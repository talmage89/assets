.DEFAULT_GOAL := all
SEEDS ?= 101,202,303
WIDTH ?= 1200
SAMPLES ?= 24
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
VIEWS := $(foreach s,$(SEED_LIST),renders/lookdev/$(s)/hero.png renders/lookdev/$(s)/above.png) $(addprefix renders/lookdev/,clamp-deck.png stairs.png transfer.png slide-entrance.png slide-exit.png swing-hanger.png swing-hollow.png arch-swing.png swing-seat.png bucket-seat.png climber.png tube-junction.png rubber-wear.png scale.png pieces.png)
.NOTPARALLEL:
.PHONY: all compare before-match refs textures model check render match source-match review repeat check-repo FORCE
all: refs textures model check render match source-match review
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
$(MODELS) &: $(MAPS) build/model-parameters.txt $(filter-out src/render.py src/review.py src/check.py src/check_lookdev.py src/compare.py src/setting.py src/render_batch.py src/repeat.py src/photo_matches.py src/source_pairs.py,$(wildcard src/*.py))
	$(BP) --python src/build.py -- --lookdev --seeds $(SEEDS) --out build/Playground.blend
model: $(MODELS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
check: model check-repo
	$(BP) --python src/check.py -- --out build/check.json
	$(PYTHON) src/check_lookdev.py
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='$(WIDTH) $(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(VIEWS) &: $(MODELS) build/render-parameters.txt src/render.py src/setting.py
	$(PYTHON) src/render_batch.py --seeds $(SEEDS) --out renders/lookdev --width $(WIDTH) --samples $(SAMPLES)
render: $(VIEWS)
match: model refs
	$(PYTHON) src/photo_matches.py
	$(BP) --python src/render.py -- --matches --out renders/lookdev --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/lookdev/matches --out renders/lookdev/matches
review:
	$(PYTHON) src/review.py --out renders/lookdev
source-match: model refs
	$(PYTHON) src/photo_matches.py
	$(BP) --python src/source_pairs.py -- --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/source-matches --out renders/source-matches
repeat: model
	$(PYTHON) src/repeat.py

compare:
	$(PYTHON) src/compare.py

before-match:
	$(BP) --python src/render.py -- --matches --export-root build/before-export --no-setting --out renders/before --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/before/matches --out renders/before/matches
