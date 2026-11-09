CHECKPOINT_BLEND := build/river.blend
BLENDER ?= blender -t 1
CHECKPOINT_OUTPUTS := build/river.blend build/manifest.json export/RiverCrossing-101.gltf export/RiverCrossing-202.gltf export/RiverModules.gltf
PIECES := TypeIII_Girder18 DeckPanel6 Parapet6 PierColumns PierWall Abutment GuardrailTerminal
CHECKPOINT_OUTPUTS += export/RiverCrossing-101.bin export/RiverCrossing-202.bin export/RiverModules.bin $(foreach p,$(PIECES),export/pieces/$(p).gltf export/pieces/$(p).bin)
MODEL_SCRIPTS := build plan geometry channel bridge freeway_bridge site age weather plaques context background urban rural materials package storage wall_details
CHECKPOINT_DEPS := $(addprefix src/,$(addsuffix .py,$(MODEL_SCRIPTS))) textures/checkpoint/.stamp build/preservation.json build/dependencies.json
CHECKPOINT_DEPS += build/town/manifest.json
CHECKPOINT_DEPS += $(addprefix ../freeway/src/,pieces.py geom.py plan.py graphics.py)
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/matches.py --compose && $(PYTHON) src/review.py --gate && $(PYTHON) src/resources.py && $(PYTHON) src/report.py && $(PYTHON) src/evidence.py && $(PYTHON) src/checkpoint_report.py && $(PYTHON) src/values.py
CHECKPOINT_REVIEW += && $(PYTHON) src/matches.py --compose --folder renders/source-matches
CHECKPOINT_CHECK += && $(PYTHON) src/storage_check.py
CHECKPOINT_RENDER_ARGS := --seeds 101 202 --modules --matches --with-baseline --eevee
WIDTH ?= 1280
SAMPLES ?= 32
include ../kit/checkpoint_rules.mk
export BLENDER
# Like freeway, keep the kit's render graph and single GPU lease, but limit
# each Blender process to three views. The dispatcher inherits that lease.
RBP = $(PYTHON) src/render_batch.py --locked --width $(WIDTH) --samples $(SAMPLES) --kit-worker --
$(CHECKPOINT_RENDER_OUTPUTS): private BP = $(RBP)
$(CHECKPOINT_RENDER_OUTPUTS): src/render_batch.py src/render.py src/package.py

refs: river-refs
.PHONY: river-refs
river-refs:
	$(PYTHON) src/fetch_refs.py

textures/baked/.stamp: src/textures.py src/bank_fields.py ../kit/flat_bake.py ../kit/image_io.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/bank_fields.py prepare
	$(KIT)/with_gpu.sh $(BP) --python src/bank_fields.py -- bake
	@touch $@
textures/checkpoint/.stamp: textures/baked/.stamp src/bank_fields.py ../kit/downsample.py
	$(PYTHON) src/bank_fields.py ship
	@touch $@
build/preservation.json: src/preserve.py | build/dependencies.json
	@mkdir -p build
	$(PYTHON) src/preserve.py --capture
build/dependencies.json: src/dependencies.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
build/photo-calibration.json: build/manifest.json src/matches.py
	$(PYTHON) src/matches.py --prepare
check: build/photo-calibration.json
build/town/manifest.json: src/native_town.py
	$(BP) --python src/native_town.py
$(CHECKPOINT_RENDER_OUTPUTS): build/photo-calibration.json
$(CHECKPOINT_RENDER_OUTPUTS): src/views.py src/materials.py build/accepted-rebuild/river/export/RiverCrossing-101.gltf
build/accepted-rebuild/river/export/RiverCrossing-101.gltf: src/baseline.py
	$(PYTHON) src/baseline.py --prepare --build

.PHONY: match repeat
match: render
	$(PYTHON) src/matches.py --compose
repeat: model
	$(PYTHON) src/repeat.py

.PHONY: check-texture-repeat
check-texture-repeat: textures/checkpoint/.stamp
	$(PYTHON) src/texture_repeat.py

.PHONY: docs
docs: checkpoint
	$(PYTHON) src/delivery.py

.PHONY: wall
WALL_VIEWS := renders/wall-details/outfall.png renders/wall-details/ladder.png renders/wall-before/outfall.png renders/wall-before/ladder.png
wall: $(WALL_VIEWS)
review: wall
$(WALL_VIEWS) &: $(CHECKPOINT_OUTPUTS) src/wall_views.py src/render.py src/materials.py build/accepted-rebuild/river/export/RiverCrossing-101.gltf
	$(KIT)/with_gpu.sh $(BP) --python src/wall_views.py -- --width $(WIDTH) --samples $(SAMPLES)

# Only a camera correction with otherwise current hash/camera receipts can
# refresh the batch stamp. Any changed geometry or other camera fails the gate.
.PHONY: inspection
inspection: model check build/photo-calibration.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES) --seeds 101 --shots abutment
	$(PYTHON) src/review.py --gate
	@touch $(CHECKPOINT_RENDER_OUTPUTS)

clean: river-clean
.PHONY: river-clean
river-clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"
