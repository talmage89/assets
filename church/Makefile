# Form/construction checkpoint: existing native deliveries are read-only inputs.
WIDTH ?= 1400
SAMPLES ?= 32
CHECKPOINT_BLEND := build/family.blend
CHECKPOINT_OUTPUTS := build/family.blend build/metrics.json export/Church-101.gltf export/Church-202.gltf export/ChurchSite-101.gltf export/ChurchSite-202.gltf export/Range.gltf
CHECKPOINT_DEPS := $(addprefix src/,build.py geometry.py surfaces.py architecture.py buildings.py modern.py windows.py hardware.py details.py plan.py package.py siteworks.py library.py) build/dependencies.json textures/ship/T_ChurchCraft_BaseColor.png
CHECKPOINT_CHECK = $(PYTHON) src/check.py && $(BP) --python src/construction_check.py
CHECKPOINT_OUT := renders/checkpoint
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_ARGS := --shots hero,above,doors,window,window_dusk,tower,wing,sign,scale
include ../kit/checkpoint_rules.mk
BP := $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1

build/dependencies.json: src/dependencies.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
textures/ship/T_ChurchCraft_BaseColor.png: src/textures.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/textures.py
.PHONY: matches module-render range-render eevee repeat
matches: model refs
	$(PYTHON) src/matches.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/photo_match.py -- verify --calibration build/matched-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches --out renders/matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --matches --source-scene --out renders/source-matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/source-matches --out renders/source-matches
module-render: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --modules --out renders/modules --width 720 --samples 24
range-render: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --range --out renders/checkpoint --width $(WIDTH) --samples $(SAMPLES)
eevee: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --seeds 101 --shots hero --engine BLENDER_EEVEE --out renders/eevee --width $(WIDTH) --samples $(SAMPLES)
review: matches module-render range-render eevee
repeat: model
	$(PYTHON) src/repeat.py
