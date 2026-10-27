# Baked delivery is now the default; source checkpoint targets remain usable.
.DEFAULT_GOAL := ranch-final
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 8
.PHONY: ranch-final bake export final-render final-seeds final-matches street docs check-delivery bake-loss-pairs clean
build/ranch/delivery/bake-parameters.txt: FORCE
	@mkdir -p build/ranch/delivery $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/ranch/delivery/fields.stamp: src/ranch_fields.py src/ranch_bake.py build/ranch/delivery/bake-parameters.txt
	$(PYTHON) src/ranch_bake.py source --size $(BAKE_SIZE)
	@touch $@
textures/ranch-bake/.stamp: build/ranch/delivery/fields.stamp src/ranch_bake.py $(KIT)/flat_bake.py
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_bake.py -- bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch $@
textures/ranch-ship/.stamp: textures/ranch-bake/.stamp src/ranch_bake.py $(KIT)/downsample.py
	$(PYTHON) src/ranch_bake.py filter
	@touch $@
bake: textures/ranch-ship/.stamp
build/ranch/delivery/colonial.stamp: src/deliver.py src/check_delivery.py
	$(MAKE) TYPE=builder_colonial SEED=27 PLAN= export
	@mkdir -p build/ranch/delivery
	@touch $@
build/ranch/delivery/export.stamp: build/ranch/models.stamp textures/ranch-ship/.stamp build/ranch/delivery/colonial.stamp src/ranch_deliver.py src/ranch_reduce.py src/ranch_uv.py src/deliver.py
	$(BP) --python src/ranch_deliver.py -- --seeds $(RANCH_SEEDS)
	@touch $@
export: build/ranch/delivery/export.stamp
check-delivery: export
	$(BP) --python src/ranch_delivery_check.py -- --seeds $(RANCH_SEEDS)
check: check-delivery
	$(MAKE) TYPE=builder_colonial SEED=27 PLAN= check
renders/ranch/final/.stamp: build/ranch/delivery/export.stamp src/ranch_final.py src/ranch_render.py src/ranch_shadow.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_final.py -- --seed $(RANCH_SEED) --seeds $(RANCH_SEEDS) --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
renders/ranch/final-eevee/.stamp: build/ranch/delivery/export.stamp src/ranch_render.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_final.py -- --seed $(RANCH_SEED) --mode eevee --out renders/ranch/final-eevee --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-render: renders/ranch/final/.stamp renders/ranch/final-eevee/.stamp
renders/ranch/final-seeds/.stamp: build/ranch/delivery/export.stamp src/ranch_final.py src/ranch_render.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_final.py -- --mode seeds --seeds $(RANCH_SEEDS) --out renders/ranch/final-seeds --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-seeds: renders/ranch/final-seeds/.stamp
renders/ranch/final-matches/.stamp: build/ranch/delivery/export.stamp build/ranch/cameras.json src/ranch_render.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_final.py -- --mode matches --out renders/ranch/final-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/ranch/cameras.json --renders renders/ranch/final-matches --out renders/ranch/final-matches
	@touch $@
final-matches: refs renders/ranch/final-matches/.stamp
bake-loss-pairs: refs export
	$(PYTHON) src/ranch_revision_present.py cameras
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_revision_present.py -- renders --scope bake-loss
	$(PYTHON) src/ranch_revision_present.py sheets --scope bake-loss
	$(BP) --python src/ranch_bake_loss.py --
build/ranch/delivery/context.json: src/ranch_context.py
	$(PYTHON) src/ranch_context.py
renders/ranch/street/.stamp: build/ranch/delivery/export.stamp build/ranch/delivery/context.json src/ranch_street.py build/ranch/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/ranch_street.py -- --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
street: renders/ranch/street/.stamp
docs: final-render final-seeds final-matches street
	$(PYTHON) src/ranch_final_review.py --seeds $(RANCH_SEEDS)
	@if [ "$(RANCH_SEED)" = "12" ] && [ -z "$(PLAN)" ]; then $(PYTHON) src/ranch_values.py --folder renders/ranch/final-matches --out build/ranch/delivery/values.json; fi
ranch-final: refs export check docs
clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build/ranch','renders/ranch','textures/ranch-bake','textures/ranch-ship')]; [p.unlink() for p in Path('export').glob('HearthfieldRanch-*')]; [p.unlink() for p in Path('export/textures').glob('T_Ranch*.png')]"
