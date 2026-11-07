BLENDER := $(abspath src/serial_blender.sh)
ASSET := Skatepark
CHECKPOINT_BLEND := build/Skatepark.blend
CHECKPOINT_ARGS := --look
CHECKPOINT_OUTPUTS := build/Skatepark.blend build/Skatepark.json build/embedded/SkateparkPieces.glb export/final/SkateparkPieces.gltf export/final/SkateparkPieces.bin $(foreach seed,101 202 303,build/embedded/Park_$(seed).glb export/final/Park_$(seed).gltf export/final/Park_$(seed).bin)
CHECKPOINT_DEPS := $(addprefix src/,build.py geometry.py pieces.py bowl.py contour.py plan.py terrain.py park_site.py context_build.py finishes.py textures.py export_frames.py external.py) textures/ship/.stamp ../ground/textures/ship/.stamp $(wildcard build/context/*.glb)
CHECKPOINT_CHECK = $(BP) --python src/validate.py -- --folder export/final
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --folder renders/final
CHECKPOINT_OUT := renders/final
CHECKPOINT_RENDER_ARGS := --folder export/final
include ../kit/checkpoint_rules.mk

.PHONY: context textures form match repeat before-after values fixes
context: build/context/ground.glb build/context/furniture.glb build/context/chain.glb build/context/tree.glb build/context/houses.glb build/context/light.glb
model: context
$(CHECKPOINT_OUTPUTS): | context
build/context/%.glb: src/context_build.py src/geometry.py
	@mkdir -p build/context $(TMPDIR)
	$(BP) --python src/context_build.py -- $* --out $@
build/context/chain.glb: ../fences/chain-link/build/textures.stamp
../fences/chain-link/build/textures.stamp:
	$(MAKE) -C ../fences/chain-link BLENDER="$(BLENDER)" build/textures.stamp
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

render: match renders/final/modules.png renders/final/eevee/101/hero.png
renders/final/modules.png: $(CHECKPOINT_OUTPUTS) src/modules_render.py src/render.py
	$(KIT)/with_gpu.sh $(BP) --python src/modules_render.py
renders/final/eevee/101/hero.png: $(CHECKPOINT_OUTPUTS) src/render.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --folder export/final --out renders/final/eevee --width $(WIDTH) --samples $(SAMPLES) --seed 101 --shots hero --engine BLENDER_EEVEE
fixes: model
	$(KIT)/with_gpu.sh $(BP) --python src/delivery_fixes.py -- --samples $(SAMPLES)
match: renders/final-matches/.stamp
renders/final-matches/.stamp: $(CHECKPOINT_OUTPUTS) src/photo_matches.py src/match.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/match.py -- --width $(WIDTH) --samples $(SAMPLES) --folder export/final --out renders/final-matches
	@touch $@
repeat: model
	$(PYTHON) src/repeat.py snapshot
	cd build/repeat && $(PYTHON) "$(abspath src/textures.py)" --out build/procedural --size 4096
	cd build/repeat && $(KIT)/with_gpu.sh $(BP) --python "$(abspath src/bake_tiles.py)"
	cd build/repeat && $(BP) --python "$(abspath src/build.py)" -- --look --out build/Skatepark.blend
	$(PYTHON) src/repeat.py compare
before-after: model
	$(KIT)/with_gpu.sh $(BP) --python src/before_after.py -- --stage before --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/before_after.py -- --stage after --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/compare_views.py
all: values
values: refs model
	$(PYTHON) src/ratios.py
