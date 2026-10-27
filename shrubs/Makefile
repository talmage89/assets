ASSET := Boxwood
CUSTOM_CHECKPOINT := 1
SHIP_SIZE := 2048
WIDTH ?= 1200
SAMPLES ?= 40
PASS ?= checkpoint
MODEL_DEPS := src/build.py src/growth.py src/hydrangea.py src/hydrangea_atlas.py src/materials.py src/settings.py ../kit/botany.py ../kit/foliage.py textures/ship/.stamp
include ../kit/rules.mk
.DEFAULT_GOAL := all

textures/source/.stamp: src/atlas.py src/hydrangea_atlas.py src/settings.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/atlas.py --out textures/source --size 4096
	@touch $@
textures/ship/.stamp: textures/source/.stamp ../kit/downsample.py ../kit/image_io.py
	$(PYTHON) $(KIT)/downsample.py --asset Shrubs --source textures/source --out textures/ship --size $(SHIP_SIZE)
	@touch $@
checkpoint: refs model check-scene check-repo check-botany check-framed-cameras render match contact
render: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/lookdev.blend --out renders/$(PASS) --shots "$(CHECKPOINT_SHOTS)" --width $(WIDTH) --samples $(SAMPLES)
preview: model
	$(BP) --python src/render.py -- --source build/lookdev.blend --out renders/preview --shots three_quarter,side --engine BLENDER_EEVEE --width 900 --samples 16
match: refs model build/framed-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/lookdev.blend --out renders/$(PASS) --camera-file build/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/framed-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
contact:
	$(PYTHON) src/review.py --renders renders/$(PASS)
check-botany: model
	$(BP) --python src/check.py -- --source build/lookdev.blend --out build/botanical-check.json
check: check-botany

build/framed-cameras.json: build/matched-cameras.json ../kit/photo_frame.py Makefile
	$(PYTHON) $(KIT)/photo_frame.py --source $< --out $@ --margin-fraction .20 --vertical-fraction .36
check-framed-cameras: build/framed-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $<
check: check-framed-cameras

HYD_BUILD := build/hydrangea
HYD_PASS ?= hydrangea-checkpoint
$(HYD_BUILD)/lookdev.blend: $(MODEL_DEPS) textures/ship/.stamp
	@mkdir -p $(HYD_BUILD)
	$(BP) --python src/build.py -- --species hydrangea --out $@
$(HYD_BUILD)/game-audit.blend: $(MODEL_DEPS) textures/ship/.stamp
	@mkdir -p $(HYD_BUILD)
	$(BP) --python src/build.py -- --species hydrangea --quality game --out $@
hydrangea-model: $(HYD_BUILD)/lookdev.blend
hydrangea-render: hydrangea-model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --species hydrangea --source $(HYD_BUILD)/lookdev.blend --out renders/$(HYD_PASS) --shots "$(CHECKPOINT_SHOTS)" --width $(WIDTH) --samples $(SAMPLES)
$(HYD_BUILD)/matched-cameras.json: src/hydrangea_matches.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config $< --out $@
$(HYD_BUILD)/framed-cameras.json: $(HYD_BUILD)/matched-cameras.json $(KIT)/photo_frame.py Makefile
	$(PYTHON) $(KIT)/photo_frame.py --source $< --out $@ --margin-fraction .30 --vertical-fraction .30
hydrangea-match: hydrangea-model $(HYD_BUILD)/framed-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --species hydrangea --source $(HYD_BUILD)/lookdev.blend --out renders/$(HYD_PASS) --camera-file $(HYD_BUILD)/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration $(HYD_BUILD)/framed-cameras.json --renders renders/$(HYD_PASS) --out renders/$(HYD_PASS)

check-hydrangea: $(HYD_BUILD)/lookdev.blend $(HYD_BUILD)/game-audit.blend $(HYD_BUILD)/framed-cameras.json
	$(BP) --python $(KIT)/audit.py -- --source $(HYD_BUILD)/game-audit.blend --config $(CONFIG) --out $(HYD_BUILD)/game-audit.json
	$(BP) --python $(KIT)/audit.py -- --source $(HYD_BUILD)/lookdev.blend --config $(CONFIG) --out $(HYD_BUILD)/lookdev-audit.json
	$(BP) --python src/check.py -- --species Hydrangea --source $(HYD_BUILD)/lookdev.blend --out $(HYD_BUILD)/botanical-check.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $(HYD_BUILD)/framed-cameras.json
hydrangea-contact:
	$(PYTHON) src/review.py --species hydrangea --renders renders/$(HYD_PASS)
check: check-hydrangea

family-contact:
	$(PYTHON) src/family_review.py --boxwood renders/$(PASS) --hydrangea renders/$(HYD_PASS)
checkpoint: check-hydrangea hydrangea-render hydrangea-match hydrangea-contact family-contact
