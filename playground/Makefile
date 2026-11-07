SEEDS ?= 101,202,303
comma := ,
SEED_LIST := $(subst $(comma), ,$(SEEDS))
MODULES := RampHeadBridge Deck72 Barrier72 NeckGuard Deck Barrier InfillPanel HipRoof Shade Stairs48 Transfer24 RampSegment RampLanding InterdeckSteps RoofRiser SlideStraight24 SlideStraight48 SlideWave48 SlideWave72 SlideSpiral72 SlideTube48 Arch48 Ladder72 VerticalLadder48 ChainNet48 RockWall48 FirePole OverheadLadder OverheadRings PanelWheel PanelTic PanelPeriscope SwingFrame SwingBelt SwingBucket SpringRider Roundabout Post1730 Post2339 Post2949
LIBRARIES := PlaygroundPieces ComparisonDeck ComparisonSwings $(addprefix Playground-,$(SEED_LIST))
CHECKPOINT_BLEND := build/Playground.blend
CHECKPOINT_OUTPUTS := build/Playground.blend build/manifest.json $(foreach n,$(MODULES) $(LIBRARIES),export/$(n).gltf export/$(n).bin) $(foreach n,ChainLink PinOak,$(foreach c,BaseColor Normal ORM,export/images/T_$(n)_$(c).png)) export/images/T_Playground_CheckpointChain.png export/images/T_Playground_CheckpointDeck.png
CHECKPOINT_DEPS := $(addprefix src/,build.py context.py geometry.py parts.py plan.py dimensions.py) ../kit/model.py ../street-furniture/src/pieces.py ../street-furniture/src/forms.py ../fences/chain-link/src/build.py ../fences/chain-link/src/mesh_tile.py ../fences/chain-link/src/dimensions.py ../fences/src/modular.py ../street-light/src/build.py ../street-light/src/dimensions.py ../trees/export/PinOak.glb ../trees/export/RedMaple.glb ../shrubs/export/Shrubs.glb ../ground/textures/ship/T_Lawn_BaseColor.png
CHECKPOINT_ARGS := --seeds $(SEEDS)
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --out build/check.json
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_ARGS := --source export/Playground-101.gltf --seeds $(SEEDS)
WIDTH ?= 1200
SAMPLES ?= 24
include ../kit/checkpoint_rules.mk
.PHONY: match repeat
all: match
match: model refs
	$(PYTHON) src/photo_matches.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/checkpoint/matches --out renders/checkpoint/matches
	$(CHECKPOINT_REVIEW)
repeat: model
	$(PYTHON) src/repeat.py

# Read-only reuse when present; a clean clone can build only the missing libraries.
../trees/export/PinOak.glb:
	$(MAKE) -C ../trees SPECIES=oak export/PinOak.glb
../trees/export/RedMaple.glb:
	$(MAKE) -C ../trees export/RedMaple.glb
../shrubs/export/Shrubs.glb:
	$(MAKE) -C ../shrubs export/Shrubs.glb
../ground/textures/ship/T_Lawn_BaseColor.png:
	$(MAKE) -C ../ground textures/ship/.stamp
