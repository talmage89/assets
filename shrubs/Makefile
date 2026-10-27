ASSET := Boxwood
CUSTOM_CHECKPOINT := 1
SHIP_SIZE := 2048
WIDTH ?= 1200
SAMPLES ?= 40
PASS ?= checkpoint
MODEL_DEPS := src/build.py src/growth.py src/settings.py ../kit/botany.py ../kit/foliage.py textures/ship/.stamp
include ../kit/rules.mk
.DEFAULT_GOAL := all

textures/source/.stamp: src/atlas.py src/settings.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/atlas.py --out textures/source --size 4096
	@touch $@
textures/ship/.stamp: textures/source/.stamp
	$(PYTHON) $(KIT)/downsample.py --asset Shrubs --source textures/source --out textures/ship --size $(SHIP_SIZE)
	@touch $@
checkpoint: refs model check-scene check-repo check-botany render match contact
render: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/lookdev.blend --out renders/$(PASS) --width $(WIDTH) --samples $(SAMPLES)
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

build/framed-cameras.json: build/matched-cameras.json ../kit/photo_frame.py
	$(PYTHON) $(KIT)/photo_frame.py --source $< --out $@ --margin-fraction .08 --vertical-fraction .12
check-framed-cameras: build/framed-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $<
check: check-framed-cameras
