ASSET := Skatepark
CHECKPOINT_BLEND := build/Skatepark.blend
CHECKPOINT_ARGS := --look
CHECKPOINT_OUTPUTS := build/Skatepark.blend build/Skatepark.json export/lookdev/SkateparkPieces.glb $(foreach seed,101 202 303,export/lookdev/Park_$(seed).glb export/lookdev/Park_$(seed).gltf)
CHECKPOINT_DEPS := $(addprefix src/,build.py geometry.py pieces.py bowl.py contour.py plan.py terrain.py park_site.py context_build.py finishes.py textures.py export_frames.py) textures/ship/.stamp ../ground/textures/ship/.stamp $(wildcard build/context/*.glb)
CHECKPOINT_CHECK = $(BP) --python src/check.py -- --folder export/lookdev && $(BP) --python src/audit_delivery.py -- --folder export/lookdev && $(BP) --python src/measure_layout.py -- --folder export/lookdev
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --folder renders/lookdev
CHECKPOINT_OUT := renders/lookdev
CHECKPOINT_RENDER_ARGS := --folder export/lookdev
include ../kit/checkpoint_rules.mk

.PHONY: context textures form match repeat before-after
context: build/context/ground.glb build/context/furniture.glb build/context/chain.glb build/context/tree.glb build/context/houses.glb build/context/light.glb
model: context
$(CHECKPOINT_OUTPUTS): | context
build/context/%.glb: src/context_build.py src/geometry.py
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/context_build.py -- $* --out $@
build/context/ground.glb: $(wildcard ../ground/src/*.py)
build/context/furniture.glb: $(wildcard ../street-furniture/src/*.py)
build/context/chain.glb: $(wildcard ../fences/chain-link/src/*.py ../fences/src/*.py)
build/context/tree.glb: ../trees/export/RedMaple.glb ../trees/export/PinOak.glb
build/context/houses.glb: $(wildcard ../houses/src/*.py)
build/context/light.glb: $(wildcard ../street-light/src/*.py)
../trees/export/RedMaple.glb:
	$(MAKE) -C ../trees export
../trees/export/PinOak.glb:
	$(MAKE) -C ../trees SPECIES=oak export
../ground/textures/ship/.stamp:
	$(MAKE) -C ../ground textures/ship/.stamp
build/procedural/.stamp: src/textures.py
	$(PYTHON) src/textures.py --out build/procedural --size 4096
	@touch $@
textures/ship/.stamp: build/procedural/.stamp src/bake_tiles.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake_tiles.py
	@touch $@
textures: textures/ship/.stamp ../ground/textures/ship/.stamp
form: context
	$(BP) --python src/build.py -- --out build/Form.blend

render: match
match: renders/lookdev-matches/.stamp
renders/lookdev-matches/.stamp: $(CHECKPOINT_OUTPUTS) src/photo_matches.py src/match.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/match.py -- --width $(WIDTH) --samples $(SAMPLES) --folder export/lookdev --out renders/lookdev-matches
	@touch $@
repeat: model
	$(PYTHON) src/repeat.py snapshot
	cd build/repeat && $(BP) --python "$(abspath src/build.py)" -- --look --out build/Skatepark.blend
	$(PYTHON) src/repeat.py compare
before-after: model
	$(KIT)/with_gpu.sh $(BP) --python src/before_after.py -- --stage before --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/before_after.py -- --stage after --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/compare_views.py
