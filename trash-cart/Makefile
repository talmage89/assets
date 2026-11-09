ASSET := TrashCart
SHIP_SIZE := 1024
SAMPLES ?= 64
VARIANT ?= trash
EXPORT_ARGS := --variant trash
SHOTS := hero_closed,hero_open,controls,hinge,wheel,front,side,back,top
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,controls,hinge,wheel,scale
MODEL_DEPS := src/build.py src/finishes.py ../kit/model.py ../kit/materials.py
FINAL_PIPELINE := 1
include ../kit/rules.mk

.PHONY: variants
variants: export export/TrashCartRecycling.glb
export/TrashCartRecycling.glb: build/finalized.blend build/textures.stamp ../kit/export.py
	$(BP) --python $(KIT)/export.py -- --source build/finalized.blend --textures textures/ship --asset TrashCart --out $@ --report build/recycling-export-report.json --variant recycling

.PHONY: variant verify-recycling
variant: $(if $(filter recycling,$(VARIANT)),export/TrashCartRecycling.glb,export/TrashCart.glb)
verify: verify-recycling
verify-recycling: export/TrashCartRecycling.glb
	$(BP) --python $(KIT)/verify.py -- --source $< --expected build/recycling-export-report.json --config $(CONFIG) --out build/recycling-delivery-check.json --size $(SHIP_SIZE)
docs: renders/recycling/.stamp
renders/recycling/.stamp: export/TrashCartRecycling.glb $(CONFIG) $(KIT)/studio.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --out renders/recycling --shots hero_closed,top --width $(WIDTH) --samples $(SAMPLES)
	@touch $@

.PHONY: check-cart
check: check-cart
check-cart: export/TrashCart.glb export/TrashCartRecycling.glb
	$(BP) --python src/check_cart.py -- --out build/cart-check.json

.PHONY: check-supports
check: check-supports
check-supports: build/game-audit.blend build/lookdev.blend
	$(BP) --python $(KIT)/assembly.py -- --source build/game-audit.blend --config $(CONFIG) --out build/support-game.json
	$(BP) --python $(KIT)/assembly.py -- --source build/lookdev.blend --config $(CONFIG) --out build/support-high.json

# Joint-specific delivered sweeps retain finite bearing exemptions only.
.PHONY: check-joints repeat
check: check-joints
check-joints: export/TrashCart.glb export/TrashCartRecycling.glb
	$(BP) --python src/check_lod_motion.py -- --config src/lod-trash.json --source-only
	$(BP) --python src/check_lod_motion.py -- --config src/lod-recycling.json --source-only

.PHONY: joint-views
joint-views: variants
	@set -e; for cart_name in TrashCart TrashCartRecycling; do \
		$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source export/$$cart_name.glb --config src/joint_views.py --out renders/joint-$$cart_name --shots closed,swing,open --width 960 --samples $(SAMPLES); \
	done

repeat: check-scene build/finalized.blend
	@mkdir -p build/repeat
	$(BP) --python src/build.py -- --wear $(WEAR) --quality game --out build/repeat/game.blend
	$(BP) --python $(KIT)/audit.py -- --source build/repeat/game.blend --config $(CONFIG) --out build/repeat/game-audit.json
	$(BP) --python src/build.py -- --wear $(WEAR) --quality high --out build/repeat/high.blend
	$(BP) --python $(KIT)/audit.py -- --source build/repeat/high.blend --config $(CONFIG) --out build/repeat/lookdev-audit.json
	$(PYTHON) src/check_repeat.py
	$(BP) --python $(KIT)/finalize.py -- --source build/repeat/game.blend --config $(CONFIG) --out build/repeat/finalized.blend --report build/repeat/uv-report.json --size $(SHIP_SIZE) --target-density $(UV_TARGET_DENSITY) --margin $(UV_MARGIN)
	$(BP) --python src/check_repeat_fields.py

LOD_CONFIGS := src/lod-trash.json src/lod-recycling.json
include ../kit/lod_rules.mk

.PHONY: check-lod-joints
check-lod: check-lod-joints
check-lod-joints:
	@set -e; for lod_config in $(LOD_CONFIGS); do \
		$(BP) --threads $(LOD_THREADS) --python src/check_lod_motion.py -- --config "$$lod_config"; \
	done
