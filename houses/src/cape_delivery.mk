# Shared-map game delivery. Source checkpoint targets remain independently usable.
.DEFAULT_GOAL := cape-final
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 8
.PHONY: cape-final bake export final-render final-seeds final-matches final-values source-values street docs check-delivery check-legacy
build/cape/delivery/bake-parameters.txt: FORCE
	@mkdir -p build/cape/delivery $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
textures/cape-bake/.stamp: src/cape_bake.py src/cape_shingle_fields.py src/cape_masonry.py build/cape/delivery/bake-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_bake.py -- bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch $@
textures/cape-ship/.stamp: textures/cape-bake/.stamp src/cape_bake.py $(KIT)/downsample.py
	$(PYTHON) src/cape_bake.py filter
	@touch $@
bake: textures/cape-ship/.stamp
build/cape/delivery/legacy.stamp: src/cape_ensure_family.py
	$(PYTHON) src/cape_ensure_family.py
	@touch $@
build/cape/delivery/export.stamp: $(CAPE_MODELS) textures/cape-ship/.stamp build/cape/delivery/legacy.stamp src/cape_deliver.py src/ranch_reduce.py src/ranch_uv.py src/deliver.py
	$(KIT)/with_gpu.sh $(BP) --python src/cape_deliver.py -- --seeds $(CAPE_SEEDS)
	@touch $@
export: build/cape/delivery/export.stamp
check-legacy: export
	$(PYTHON) src/cape_legacy_check.py
check-delivery: export check-legacy
	$(BP) --python src/cape_finish_proof.py --
	$(BP) --python src/cape_delivery_check.py -- --seeds $(CAPE_SEEDS)
check: check-delivery
renders/cape/final/.stamp: build/cape/delivery/export.stamp $(CAPE_RENDER_DEPS) src/cape_final.py build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_final.py -- --seed $(CAPE_SEED) --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
renders/cape/final-eevee/.stamp: build/cape/delivery/export.stamp $(CAPE_RENDER_DEPS) src/cape_final.py build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --gpu-backend opengl --python src/cape_final.py -- --seed $(CAPE_SEED) --mode eevee --out renders/cape/final-eevee --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-render: renders/cape/final/.stamp renders/cape/final-eevee/.stamp
renders/cape/final-seeds/.stamp: build/cape/delivery/export.stamp $(CAPE_RENDER_DEPS) src/cape_final.py build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_final.py -- --mode seeds --seeds $(CAPE_SEEDS) --out renders/cape/final-seeds --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-seeds: renders/cape/final-seeds/.stamp
renders/cape/final-matches/.stamp: build/cape/delivery/export.stamp build/cape/cameras.json $(CAPE_RENDER_DEPS) src/cape_final.py build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_final.py -- --mode matches --out renders/cape/final-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cape/cameras.json --renders renders/cape/final-matches --out renders/cape/final-matches
	@touch $@
final-matches: refs renders/cape/final-matches/.stamp
renders/cape/source-matches/.stamp: $(CAPE_MODELS) build/cape/cameras.json $(CAPE_RENDER_DEPS) src/cape_final.py build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_final.py -- --mode source-matches --out renders/cape/source-matches --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
renders/cape/final-values/.stamp: build/cape/delivery/export.stamp src/cape_value_render.py src/cape_values.py build/cape/material-photos.json $(CAPE_RENDER_DEPS) build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_value_render.py -- --final --out renders/cape/final-values --width 800 --samples $(SAMPLES)
	$(PYTHON) src/cape_values.py --folder renders/cape/final-values
	@touch $@
renders/cape/source-values/.stamp: $(CAPE_MODELS) src/cape_value_render.py src/cape_values.py build/cape/material-photos.json $(CAPE_RENDER_DEPS) build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_value_render.py -- --out renders/cape/source-values --width 800 --samples $(SAMPLES)
	$(PYTHON) src/cape_values.py --folder renders/cape/source-values
	@touch $@
final-values: renders/cape/final-values/.stamp
source-values: renders/cape/source-values/.stamp
build/cape/delivery/context.json: src/cape_final_context.py
	$(PYTHON) src/cape_final_context.py
renders/cape/street/.stamp: build/cape/delivery/export.stamp build/cape/delivery/context.json src/cape_street.py src/render.py build/cape/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/cape_street.py -- --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
street: renders/cape/street/.stamp
docs: final-render final-seeds final-matches final-values source-values street renders/cape/source-matches/.stamp
	$(PYTHON) $(KIT)/fetch_refs.py refs --only cape-used-peeling.jpg
	$(BP) --python src/cape_pair_masks.py --
	$(PYTHON) src/cape_final_review.py
cape-final: refs export check docs
