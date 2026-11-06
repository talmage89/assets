# Form/construction gate only. Look-dev and final bake are deliberately absent.
CHECKPOINT_DEPS := src/build.py src/plan.py src/geometry.py src/holes.py src/fixtures.py src/site.py
CHECKPOINT_BLEND := build/course.blend
CHECKPOINT_OUTPUTS := build/course.blend export/Minigolf-71.gltf export/Minigolf-71.bin export/Minigolf-92.gltf export/Minigolf-92.bin build/manifest.json
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_OUTPUTS := renders/checkpoint/classic-ground.png renders/checkpoint/classic-above.png renders/checkpoint/adventure-ground.png renders/checkpoint/adventure-above.png renders/checkpoint/hero.png renders/checkpoint/tee.png renders/checkpoint/cup.png renders/checkpoint/border.png renders/checkpoint/waterfall.png renders/checkpoint/fixture.png renders/checkpoint/bridge.png renders/checkpoint/clubhouse.png
include ../kit/checkpoint_rules.mk
$(CHECKPOINT_RENDER_OUTPUTS): src/context.py
.PHONY: repeat match
repeat:
	$(PYTHON) src/repeat.py
match: model refs
	$(PYTHON) src/matches.py prepare
	$(KIT)/with_gpu.sh $(BP) --python src/matches.py -- render --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/review.py --matches
checkpoint: match
