ASSET := StreetFurniture
WIDTH ?= 1440
SAMPLES ?= 32
CHECKPOINT_BLEND := build/StreetFurniture.blend
MODULES := BusStop Shelter Bench BikeRack BikeRackRow NewsDaily NewsPedestal NewsWeekly CollectionBox MeterSingle MeterTwin Litter Recycling ShelterMissingPanel NewsRow
CHECKPOINT_OUTPUTS := build/StreetFurniture.blend export/StreetFurniture.gltf export/StreetFurniture.bin export/textures/T_StreetFurniture_Checkpoint.png build/manifest.json $(addprefix export/,$(addsuffix .gltf,$(MODULES))) $(addprefix export/,$(addsuffix .bin,$(MODULES)))
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --folder renders/checkpoint
CHECKPOINT_DEPS := $(wildcard src/*.py) build/graphics.json ../street-signs/export/set/RoadSigns.gltf
CHECKPOINT_RENDER_ARGS := --source export/StreetFurniture.gltf
CHECKPOINT_RENDER_OUTPUTS := $(addprefix renders/checkpoint/,$(addsuffix .png,hero lineup signs-regulatory signs-warning sign-face sign-back post-base pole-band shelter-frame bench meter boxes collection receptacles rack))
include ../kit/checkpoint_rules.mk
.PHONY: signs match repeat
repeat: model
	$(PYTHON) src/repeat.py
build/graphics.json: src/graphics.py
	@mkdir -p build
	$(PYTHON) src/graphics.py
../street-signs/export/set/RoadSigns.gltf: $(wildcard ../street-signs/src/set_*.py)
	$(MAKE) -C ../street-signs set-model
signs:
	$(MAKE) -C ../street-signs set-model
MATCH_OUTPUTS := renders/match/used-shelter.png renders/match/used-meter.png renders/match/used-news.png renders/match/used-shelter-pair.jpg renders/match/used-meter-pair.jpg renders/match/used-news-pair.jpg
$(MATCH_OUTPUTS) &: $(CHECKPOINT_OUTPUTS) build/checkpoint-render-parameters.txt src/photo_matches.py src/render.py
	$(PYTHON) src/photo_matches.py --out build/photo-calibration.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/photo-calibration.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --match build/photo-calibration.json --out renders/match --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/photo-calibration.json --renders renders/match --out renders/match
match: $(MATCH_OUTPUTS)
review: match
