CHECKPOINT_BLEND := build/river.blend
CHECKPOINT_OUTPUTS := build/river.blend build/manifest.json export/RiverCrossing-101.gltf export/RiverCrossing-202.gltf export/RiverModules.gltf
PIECES := TypeIII_Girder18 DeckPanel6 Parapet6 PierColumns PierWall Abutment GuardrailTerminal
CHECKPOINT_OUTPUTS += export/RiverCrossing-101.bin export/RiverCrossing-202.bin export/RiverModules.bin $(foreach p,$(PIECES),export/pieces/$(p).gltf export/pieces/$(p).bin)
CHECKPOINT_DEPS := $(wildcard src/*.py) textures/checkpoint/.stamp build/preservation.json build/dependencies.json
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/matches.py --compose && $(PYTHON) src/review.py --gate && $(PYTHON) src/report.py
CHECKPOINT_RENDER_ARGS := --seeds 101 202 --modules --matches
WIDTH ?= 1280
SAMPLES ?= 32
include ../kit/checkpoint_rules.mk

refs: river-refs
.PHONY: river-refs
river-refs:
	$(PYTHON) src/fetch_refs.py

textures/checkpoint/.stamp: src/textures.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/textures.py
	@touch $@
build/preservation.json: src/preserve.py
	@mkdir -p build
	$(PYTHON) src/preserve.py --capture
build/dependencies.json: src/dependencies.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
build/photo-calibration.json: build/manifest.json src/matches.py
	$(PYTHON) src/matches.py --prepare
$(CHECKPOINT_RENDER_OUTPUTS): build/photo-calibration.json

.PHONY: match repeat
match: render
	$(PYTHON) src/matches.py --compose
repeat: model
	$(PYTHON) src/repeat.py

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
