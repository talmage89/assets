# Seeded family delivery, with retained construction/source checkpoint targets.
SAMPLES ?= 64
SEED ?= 27
PLAN ?=
export HOUSE_SEED := $(SEED)
export HOUSE_PLAN := $(PLAN)
CHECKPOINT_ARGS = --seed $(SEED) $(if $(PLAN),--plan $(PLAN))
CHECKPOINT_DEPS = src/build.py src/plan.py src/additions.py src/glb_budget.py $(KIT)/model.py $(KIT)/tiling.py $(KIT)/fonts.py $(PLAN)
CHECKPOINT_CHECK = $(PYTHON) src/check_plan.py --count 1000
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
include ../kit/checkpoint_rules.mk

.PHONY: check-mesh check-motion seed-models seed-render matches check-camera preview
check: check-mesh check-motion seed-models check-camera
check-mesh: model
	$(BP) --python src/check_mesh.py -- --source build/house.blend
check-motion: model
	$(BP) --python ../kit/motion.py -- --source build/house.blend --config src/config.py --out build/motion.json
build/seeds/.stamp: src/build.py src/plan.py src/additions.py src/glb_budget.py src/sweep.py src/check_mesh.py
	$(BP) --python src/sweep.py -- --out build/seeds
	@touch $@
seed-models: build/seeds/.stamp
renders/seeds/.stamp: build/seeds/.stamp src/render.py src/render_seeds.py
	$(KIT)/with_gpu.sh $(BP) --python src/render_seeds.py -- --width 760 --samples 24
	@touch $@
seed-render: renders/seeds/.stamp
build/matched-cameras.json: src/photo_matches.py src/plan.py build/checkpoint-parameters.txt $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
check-camera: build/matched-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $<
renders/matches/.stamp: build/house.blend build/matched-cameras.json src/render.py build/checkpoint-render-parameters.txt $(wildcard refs/*.jpg)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/house.glb --out renders/matches --camera-file build/matched-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
	@touch $@
matches: model refs renders/matches/.stamp
preview: model
	$(BP) --python src/render.py -- --source build/house.glb --out renders/preview --shots hero --width 1100 --engine BLENDER_EEVEE
review: seed-render matches

# Retained analytic source comparison. The shared bake graph follows below.
.DEFAULT_GOAL := lookdev
.PHONY: lookdev lookdev-model lookdev-render lookdev-seeds lookdev-matches lookdev-review check-lookdev
build/fields.stamp: src/textures.py src/bake_family.py $(KIT)/image_io.py build/family-bake-parameters.txt
	$(PYTHON) src/bake_family.py source --size $(BAKE_SIZE)
	@touch $@
textures/source/.stamp: build/fields.stamp
	$(PYTHON) src/bake_family.py filter-source
	@touch $@
build/lookdev.blend: build/house.blend textures/source/.stamp src/lookdev.py
	$(BP) --python src/lookdev.py -- --source $< --out $@
lookdev-model: build/lookdev.blend
check-lookdev: build/lookdev.blend
	$(PYTHON) src/check_textures.py
	$(BP) --python src/check_lookdev.py
check: check-lookdev build/lookdev-seeds/.stamp
build/lookdev-seeds/.stamp: textures/source/.stamp $(CHECKPOINT_DEPS) src/lookdev.py src/lookdev_sweep.py src/check_mesh.py
	$(BP) --python src/lookdev_sweep.py -- --no-render
	@touch $@
renders/lookdev-seeds/.stamp: build/lookdev-seeds/.stamp src/render.py src/render_seeds.py
	$(KIT)/with_gpu.sh $(BP) --python src/render_seeds.py -- --lookdev --width 900 --samples 32
	@touch $@
lookdev-seeds: renders/lookdev-seeds/.stamp
renders/lookdev/.stamp: build/lookdev.blend src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --out renders/lookdev --shots hero,back,window,entry,entry_closed,shingles,eave,side,scale,roof --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
lookdev-render: renders/lookdev/.stamp
renders/lookdev-matches/.stamp: build/lookdev.blend build/matched-cameras.json src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --out renders/lookdev-matches --camera-file build/matched-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/lookdev-matches --out renders/lookdev-matches
	@touch $@
lookdev-matches: refs renders/lookdev-matches/.stamp
lookdev-review: lookdev-render lookdev-seeds lookdev-matches
	$(PYTHON) src/review_lookdev.py
lookdev: refs lookdev-model check lookdev-review

.PHONY: clean-family-fields
clean: clean-family-fields

# Final path. All rendering imports the delivered glTF and shared PNGs.
.DEFAULT_GOAL := final
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 8
START_SEED ?= 0
SEEDS ?= $(if $(COUNT),$(shell $(PYTHON) -c "print(','.join(map(str,range($(START_SEED),$(START_SEED)+$(COUNT)))))"),$(SEED),2,3,6,8,14)
.PHONY: final bake export final-render final-seeds final-matches final-source-matches street docs check-delivery
build/family-bake-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/family-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seeds=$(SEEDS) plan=$(PLAN)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
textures/bake/.stamp: build/fields.stamp src/bake_family.py $(KIT)/flat_bake.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake_family.py -- bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch $@
textures/ship/.stamp: textures/bake/.stamp $(KIT)/downsample.py
	$(PYTHON) src/bake_family.py filter-ship
	@touch $@
bake: textures/ship/.stamp
build/family/.stamp: textures/ship/.stamp $(CHECKPOINT_DEPS) src/lookdev.py src/deliver.py src/delivery_io.py build/family-parameters.txt
	$(BP) --python src/deliver.py -- --seeds $(SEEDS) $(if $(PLAN),--plan $(PLAN))
	@touch $@
export: build/family/.stamp
renders/final/.stamp: build/family/.stamp src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/Hearthfield-$(SEED).gltf --out renders/final --shots hero,front,side,back,rear,top,eave,window,entry,entry_closed,scale,shingles --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
renders/final-eevee/.stamp: build/family/.stamp src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/Hearthfield-$(SEED).gltf --out renders/final-eevee --shots hero --engine BLENDER_EEVEE --width $(WIDTH)
	@touch $@
final-render: renders/final/.stamp renders/final-eevee/.stamp
renders/final-seeds/.stamp: build/family/.stamp src/render.py src/final_seeds.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/final_seeds.py -- --seeds $(SEEDS) --width 900 --samples $(SAMPLES)
	@touch $@
final-seeds: renders/final-seeds/.stamp
renders/final-matches/.stamp: build/family/.stamp build/matched-cameras.json src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/Hearthfield-$(SEED).gltf --out renders/final-matches --camera-file build/matched-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/final-matches --out renders/final-matches
	@touch $@
final-matches: refs renders/final-matches/.stamp
final-source-matches: lookdev-matches
build/context.json: src/context.py
	$(PYTHON) src/context.py
renders/street/.stamp: build/family/.stamp build/context.json src/street.py src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/street.py -- --seed $(SEED) --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
street: renders/street/.stamp
check-delivery: build/family/.stamp
	$(BP) --python src/check_delivery.py -- --seeds $(SEEDS)
check: check-delivery
# Presentations are independent of the seed-count export interface.
docs: final-render final-seeds final-matches final-source-matches street
	$(PYTHON) src/review_final.py --seed $(SEED) --seeds $(SEEDS)
final: refs export check docs
clean-family-fields:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures/source','textures/bake','textures/ship')]"
