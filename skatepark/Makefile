ASSET := Skatepark
CHECKPOINT_BLEND := build/Skatepark.blend
CHECKPOINT_OUTPUTS := build/Skatepark.blend build/Skatepark.json
CHECKPOINT_DEPS := $(addprefix src/,build.py geometry.py pieces.py bowl.py plan.py park_site.py context_build.py) $(wildcard build/context/*.glb)
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_ARGS :=
include ../kit/checkpoint_rules.mk

.PHONY: context
context: build/context/ground.glb build/context/furniture.glb build/context/chain.glb build/context/tree.glb build/context/houses.glb build/context/light.glb
model: context
build/Skatepark.blend build/Skatepark.json: | context
build/context/%.glb: src/context_build.py src/geometry.py
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/context_build.py -- $* --out $@
build/context/ground.glb: $(wildcard ../ground/src/*.py)
build/context/furniture.glb: $(wildcard ../street-furniture/src/*.py)
build/context/chain.glb: $(wildcard ../fences/chain-link/src/*.py ../fences/src/*.py)
build/context/tree.glb: $(wildcard ../trees/src/*.py)
build/context/houses.glb: $(wildcard ../houses/src/*.py)
build/context/light.glb: $(wildcard ../street-light/src/*.py)

.PHONY: match repeat
render: match
match: renders/matches/.stamp
renders/matches/.stamp: $(CHECKPOINT_OUTPUTS) src/photo_matches.py src/match.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/match.py -- --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
repeat: model
	$(PYTHON) src/repeat.py snapshot
	cd build/repeat && $(BP) --python "$(abspath src/build.py)" -- --out build/Skatepark.blend
	$(PYTHON) src/repeat.py compare
