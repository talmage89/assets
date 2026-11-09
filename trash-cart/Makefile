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
