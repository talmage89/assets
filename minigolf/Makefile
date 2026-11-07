# Form/construction gate only. Look-dev and final bake are deliberately absent.
CHECKPOINT_DEPS := src/build.py src/plan.py src/geometry.py src/holes.py src/fixtures.py src/site.py
CHECKPOINT_BLEND := build/course.blend
CHECKPOINT_OUTPUTS := build/course.blend export/Minigolf-71.gltf export/Minigolf-71.bin export/Minigolf-92.gltf export/Minigolf-92.bin build/manifest.json build/source-construction.json export/Minigolf-71.json export/Minigolf-92.json export/textures/T_Minigolf_Quick_BaseColor.png export/textures/T_Minigolf_Quick_ORM.png export/textures/T_Minigolf_Quick_Graphics.png
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_OUTPUTS := renders/checkpoint/classic-ground.png renders/checkpoint/classic-above.png renders/checkpoint/adventure-ground.png renders/checkpoint/adventure-above.png renders/checkpoint/hero.png renders/checkpoint/tee.png renders/checkpoint/cup.png renders/checkpoint/border.png renders/checkpoint/waterfall.png renders/checkpoint/fixture.png renders/checkpoint/bridge.png renders/checkpoint/clubhouse.png
CHECKPOINT_RENDER_OUTPUTS := $(CHECKPOINT_RENDER_OUTPUTS) $(CHECKPOINT_RENDER_OUTPUTS:.png=.json)
include ../kit/checkpoint_rules.mk
$(CHECKPOINT_RENDER_OUTPUTS): src/context.py
.PHONY: repeat match
repeat:
	$(PYTHON) src/repeat.py
match: model refs
	$(PYTHON) src/matches.py prepare
	$(KIT)/with_gpu.sh $(BP) --python src/matches.py -- render --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/review.py --matches
	$(PYTHON) src/check_renders.py --capture
checkpoint: match
.PHONY: context
context:
	$(PYTHON) src/prepare_context.py
$(CHECKPOINT_RENDER_OUTPUTS): | context
.PHONY: check-renders
check-renders:
	$(PYTHON) src/check_renders.py
