# Form/construction checkpoint: existing native deliveries are read-only inputs.
WIDTH ?= 1400
SAMPLES ?= 32
CHECKPOINT_BLEND := build/family.blend
CHECKPOINT_OUTPUTS := build/family.blend build/metrics.json export/Church-101.gltf export/Church-202.gltf export/ChurchSite-101.gltf export/ChurchSite-202.gltf export/Range.gltf
CHECKPOINT_OUTPUTS += $(patsubst %.gltf,%.bin,$(filter %.gltf,$(CHECKPOINT_OUTPUTS)))
CHURCH_MAPS := $(foreach set,Craft Glass,$(foreach map,BaseColor Normal ORM,textures/ship/T_Church$(set)_$(map).png)) textures/ship/T_ChurchLetters_BaseColor.png build/letters.json
CHURCH_MAPS += $(foreach map,BaseColor Normal ORM,textures/ship/T_GardenLawn_$(map).png)
CHECKPOINT_DEPS := $(wildcard src/*.py) build/dependencies.json $(CHURCH_MAPS)
CHECKPOINT_CHECK = $(PYTHON) src/check.py && $(BP) --python src/construction_check.py && $(BP) --python src/site_check.py
CHECKPOINT_OUT := renders/checkpoint
CHECKPOINT_REVIEW = $(PYTHON) src/review.py
CHECKPOINT_RENDER_ARGS := --shots hero,above,doors,window,window_dusk,tower,wing,sign,scale
include ../kit/checkpoint_rules.mk
BP := $(BLENDER) -b -t 4 --factory-startup --python-exit-code 1

build/dependencies.json: src/dependencies.py src/context_hosts.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
$(CHURCH_MAPS) &: src/textures.py src/art_glass.py src/turf.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/textures.py
.PHONY: matches module-render range-render eevee repeat
matches: model refs
	$(PYTHON) src/matches.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/matched-cameras.json
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
