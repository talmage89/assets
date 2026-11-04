# Final game delivery; the accepted source checkpoint remains independently usable.
.DEFAULT_GOAL := split-final
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 8
SPLIT_DELIVERY := src/split_deliver.py src/cape_deliver.py src/ranch_uv.py src/ranch_reduce.py src/split_atlas.py src/deliver.py src/glb_budget.py
SPLIT_EXPORTS := $(foreach s,$(SPLIT_IDS),export/HearthfieldSplit-$(s).gltf export/HearthfieldSplit-$(s).bin export/HearthfieldSplit-$(s).json build/split/delivery/game-$(s).blend build/split/delivery/game-$(s).json) build/split/delivery/delivery.json export/textures/T_SplitStone_BaseColor.png export/textures/T_SplitStone_Normal.png
SPLIT_FINAL := renders/split/final
.PHONY: split-final bake export final-render final-seeds final-matches source-matches final-values source-values street docs check-delivery check-legacy
build/split/delivery/bake-parameters.txt: FORCE
	@mkdir -p build/split/delivery $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
textures/split-bake/T_SplitStone_BaseColor.png textures/split-bake/T_SplitStone_Normal.png &: src/split_bake.py src/split_atlas.py src/split_fields.py src/split_surfaces.py src/cape_masonry.py build/split/delivery/bake-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_bake.py -- bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
textures/split-ship/T_SplitStone_BaseColor.png textures/split-ship/T_SplitStone_Normal.png &: textures/split-bake/T_SplitStone_BaseColor.png textures/split-bake/T_SplitStone_Normal.png src/split_bake.py
	$(PYTHON) src/split_bake.py filter
bake: textures/split-ship/T_SplitStone_BaseColor.png textures/split-ship/T_SplitStone_Normal.png
build/split/delivery/legacy.stamp: src/split_ensure_family.py
	$(PYTHON) src/split_ensure_family.py
	@touch $@
build/split/delivery/export.stamp: $(SPLIT_MODELS) textures/split-ship/T_SplitStone_BaseColor.png textures/split-ship/T_SplitStone_Normal.png $(SPLIT_DELIVERY) | build/split/delivery/legacy.stamp
	$(KIT)/with_gpu.sh $(BP) --python src/split_deliver.py -- --seeds $(SEEDS)
	@touch $@
$(SPLIT_EXPORTS) &: | build/split/delivery/export.stamp
	$(KIT)/with_gpu.sh $(BP) --python src/split_deliver.py -- --seeds $(SEEDS)
	@touch build/split/delivery/export.stamp
export: build/split/delivery/export.stamp $(SPLIT_EXPORTS)
check-legacy:
	$(PYTHON) src/split_preserved.py
check-delivery: export check-legacy
	$(BP) --python src/split_delivery_check.py -- --seeds $(SEEDS)
	$(PYTHON) src/split_privacy.py
check: check-delivery
$(SPLIT_FINAL)/.stamp: $(SPLIT_EXPORTS) $(SPLIT_RENDER) src/split_final.py build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_final.py -- --seed $(SEED) --out $(SPLIT_FINAL) --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
renders/split/final-eevee/.stamp: $(SPLIT_EXPORTS) $(SPLIT_RENDER) src/split_final.py build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --gpu-backend opengl --python src/split_final.py -- --mode eevee --seed $(SEED) --out renders/split/final-eevee --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-render: $(SPLIT_FINAL)/.stamp renders/split/final-eevee/.stamp
renders/split/final-seeds/.stamp: $(SPLIT_EXPORTS) $(SPLIT_RENDER) src/split_final.py build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_final.py -- --mode seeds --seeds $(SEEDS) --out renders/split/final-seeds --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-seeds: renders/split/final-seeds/.stamp
renders/split/final-matches/.stamp: $(SPLIT_EXPORTS) $(SPLIT_RENDER) src/split_final.py build/split/cameras-look.json build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_final.py -- --mode matches --out renders/split/final-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/split/cameras-look.json --renders renders/split/final-matches --out renders/split/final-matches
	@touch $@
final-matches: refs renders/split/final-matches/.stamp
renders/split/source-matches/.stamp: $(SPLIT_MODELS) $(SPLIT_RENDER) src/split_final.py build/split/cameras-look.json build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_final.py -- --mode source-matches --out renders/split/source-matches --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
source-matches: refs renders/split/source-matches/.stamp
renders/split/final-values/.stamp: $(SPLIT_EXPORTS) $(SPLIT_RENDER) src/split_value_render.py src/split_values.py build/split/material-photos.json build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_value_render.py -- --final --out renders/split/final-values --width 600 --samples $(SAMPLES)
	$(PYTHON) src/split_values.py --folder renders/split/final-values
	@touch $@
final-values: renders/split/final-values/.stamp
renders/split/source-values/.stamp: $(SPLIT_MODELS) $(SPLIT_RENDER) src/split_value_render.py src/split_values.py build/split/material-photos.json build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_value_render.py -- --out renders/split/source-values --width 600 --samples $(SAMPLES)
	$(PYTHON) src/split_values.py --folder renders/split/source-values
	@touch $@
source-values: renders/split/source-values/.stamp
renders/split/street/.stamp renders/split/street/street.png renders/split/street/provenance.json &: $(filter export/%,$(SPLIT_EXPORTS)) src/split_street.py src/cape_street.py src/render.py build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/split_street.py -- --width $(WIDTH) --samples $(SAMPLES)
	@touch renders/split/street/.stamp
street: renders/split/street/.stamp renders/split/street/street.png renders/split/street/provenance.json
docs: final-batch street
	$(BP) --python src/split_pair_masks.py --
	$(PYTHON) src/split_final_review.py
split-final: export check docs

# A full final build acquires the shared GPU once. Explicit per-group targets
# above remain available for focused rerenders. Missing declared images rebuild
# the batch, just as missing grouped geometry outputs rebuild the export.
SPLIT_MAIN_IMAGES := $(addprefix renders/split/final/,$(addsuffix .png,hero front side rear back top entry eave veneer garage driveway tired scale peeling garage_half garage_open)) renders/split/final/bay/bay.png renders/split/final/foyer/lower.png
SPLIT_SEED_IMAGES := $(foreach s,$(SPLIT_IDS),renders/split/final-seeds/$(s)/front.png renders/split/final-seeds/$(s)/rear.png renders/split/final-seeds/$(s)/veneer_face.png) $(foreach s,51 52 53 55 56,renders/split/final-seeds/$(s)/siding.png)
SPLIT_PAIR_IMAGES := $(foreach d,final-matches source-matches,$(foreach n,side_pa side_oh foyer_pa foyer_oh,renders/split/$(d)/$(n).png))
SPLIT_MATERIAL_NAMES := roof brick51 brick53 brick54 brick55 brick56 stone52 battens blue_lap vinyl garage driveway wood aluminum concrete trim glass
SPLIT_MATERIAL_OUTPUTS := $(foreach d,final-values source-values,$(foreach n,$(SPLIT_MATERIAL_NAMES),renders/split/$(d)/$(n).png renders/split/$(d)/$(n)-mask.png renders/split/$(d)/$(n)-pair.jpg) renders/split/$(d)/values.json renders/split/$(d)/patches.json)
SPLIT_PROVENANCE := $(foreach d,final final/bay final/foyer final-matches source-matches final-eevee,renders/split/$(d)/provenance.json) $(foreach s,$(SPLIT_IDS),renders/split/final-seeds/$(s)/provenance.json)
SPLIT_BATCH_OUTPUTS := $(SPLIT_MATERIAL_OUTPUTS) $(SPLIT_PROVENANCE) $(SPLIT_MAIN_IMAGES) $(SPLIT_SEED_IMAGES) $(SPLIT_PAIR_IMAGES) renders/split/final-eevee/hero.png build/split/delivery/final-batch.stamp
$(SPLIT_BATCH_OUTPUTS) &: $(filter export/%,$(SPLIT_EXPORTS)) $(SPLIT_MODELS) $(SPLIT_RENDER) src/split_final.py src/split_value_render.py src/split_values.py src/cape_value_render.py build/split/cameras-look.json build/split/material-photos.json build/split/render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --gpu-backend opengl --python src/split_final_batch.py -- --seed $(SEED) --seeds $(SEEDS) --width $(WIDTH) --samples $(SAMPLES)
	@touch build/split/delivery/final-batch.stamp
.PHONY: final-batch
final-batch: $(SPLIT_BATCH_OUTPUTS)
