ASSET := MetalTrashCan
SHIP_SIZE := 1024
SAMPLES ?= 48
SHOTS := hero_closed,controls,handle,interior
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,handle,interior,scale
FINAL_PIPELINE := 1
MODEL_DEPS := src/build.py src/finishes.py ../kit/model.py ../kit/materials.py
include ../kit/rules.mk
.PHONY: check-construction
check: check-construction
check-construction: build/game-audit.blend
	$(BP) --python src/check_construction.py -- --out build/construction-check.json

docs: renders/photo-final/.stamp
renders/photo-final/.stamp: export/MetalTrashCan.glb build/matched-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --camera-file build/matched-cameras.json --out renders/photo-final --shots match_front --width 1000 --samples 32
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/photo-final --out renders/photo-final
	@touch $@

# Identical thin structural shells carry shader microrelief directly. Other maps
# retain the kit's high-to-low isolation and stationary contact AO.
build/self-normal.stamp: build/baked.stamp build/finalized.blend src/bake_normal.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake_normal.py -- --out textures/bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch $@
build/textures.stamp: build/self-normal.stamp
bake: build/self-normal.stamp

# Bare metal requires a captured studio environment for Eevee reflections.
docs: renders/final-eevee-reflected/.stamp
renders/final-eevee-reflected/.stamp: export/MetalTrashCan.glb src/eevee.py renders/final/.stamp
	$(KIT)/with_gpu.sh $(BP) --python src/eevee.py -- --stage final --source $< --config $(CONFIG) --out renders/final-eevee --shots hero_closed --engine BLENDER_EEVEE --width $(WIDTH) --samples $(SAMPLES)
	@mkdir -p renders/final-eevee-reflected
	@touch $@
