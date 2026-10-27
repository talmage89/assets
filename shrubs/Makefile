ASSET := Shrubs
FINAL_PIPELINE := 1
MODEL_SCRIPT := src/family_build.py
STUDIO_SCRIPT := src/render.py
STUDIO_ARGS := --species boxwood
FINAL_SHOTS := hero,front,side,back,top,close_1m,scale
EEVEE_SHOT := hero
BAKE_DEPS := textures/source/.stamp src/composite.py
BAKE_POSTPROCESS = $(PYTHON) src/composite.py --source textures/source --out textures/bake
CUSTOM_CHECKPOINT := 1
SHIP_SIZE := 2048
UV_MARGIN := .0005
WIDTH ?= 1600
SAMPLES ?= 48
PASS ?= checkpoint
SPECIMEN_DEPS := src/build.py src/growth.py src/hydrangea.py src/hydrangea_atlas.py src/materials.py src/settings.py ../kit/botany.py ../kit/foliage.py textures/analytic/.stamp
MODEL_DEPS := src/family_build.py build/boxwood/lookdev.blend build/hydrangea/lookdev.blend
include ../kit/rules.mk
.DEFAULT_GOAL := all

textures/source/.stamp: src/atlas.py src/hydrangea_atlas.py src/settings.py
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/atlas.py --out textures/source --size 4096
	@touch $@
textures/analytic/.stamp: textures/source/.stamp ../kit/downsample.py ../kit/image_io.py
	$(PYTHON) $(KIT)/downsample.py --asset Shrubs --source textures/source --out textures/analytic --size $(SHIP_SIZE)
	@touch $@
checkpoint: refs model check-scene check-repo check-botany check-framed-cameras render match contact
render: build/boxwood/lookdev.blend
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/boxwood/lookdev.blend --out renders/$(PASS) --shots "$(CHECKPOINT_SHOTS)" --width $(WIDTH) --samples $(SAMPLES)
preview: model
	$(BP) --python src/render.py -- --source build/boxwood/lookdev.blend --out renders/preview --shots three_quarter,side --engine BLENDER_EEVEE --width 900 --samples 16
match: refs build/boxwood/lookdev.blend build/framed-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/boxwood/lookdev.blend --out renders/$(PASS) --camera-file build/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/framed-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
contact:
	$(PYTHON) src/review.py --renders renders/$(PASS)
check-botany: build/boxwood/lookdev.blend
	$(BP) --python src/check.py -- --source build/boxwood/lookdev.blend --out build/botanical-check.json
check: check-botany

build/framed-cameras.json: build/matched-cameras.json ../kit/photo_frame.py Makefile
	$(PYTHON) $(KIT)/photo_frame.py --source $< --out $@ --margin-fraction .20 --vertical-fraction .36
check-framed-cameras: build/framed-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $<
check: check-framed-cameras

HYD_BUILD := build/hydrangea
HYD_PASS ?= hydrangea-checkpoint
$(HYD_BUILD)/lookdev.blend: $(SPECIMEN_DEPS) textures/analytic/.stamp
	@mkdir -p $(HYD_BUILD)
	$(BP) --python src/build.py -- --species hydrangea --out $@
$(HYD_BUILD)/game-audit.blend: $(SPECIMEN_DEPS) textures/analytic/.stamp
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

build/boxwood/lookdev.blend: $(SPECIMEN_DEPS)
	@mkdir -p build/boxwood
	$(BP) --python src/build.py -- --species boxwood --out $@

renders/hydrangea-final/.stamp: export/$(ASSET).glb src/render.py src/settings.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --stage final --source $< --species hydrangea --out renders/hydrangea-final --shots $(FINAL_SHOTS) --width $(WIDTH) --samples $(SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --stage final --source $< --species hydrangea --out renders/hydrangea-eevee --shots hero --engine BLENDER_EEVEE --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
final-render: renders/hydrangea-final/.stamp
renders/final/.matched: export/$(ASSET).glb build/framed-cameras.json build/hydrangea/framed-cameras.json src/render.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --stage final --source $< --species boxwood --out renders/final --camera-file build/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/framed-cameras.json --renders renders/final --out renders/final
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --stage final --source $< --species hydrangea --out renders/hydrangea-final --camera-file build/hydrangea/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/hydrangea/framed-cameras.json --renders renders/hydrangea-final --out renders/hydrangea-final
	@touch $@
docs: renders/final/.matched renders/hydrangea-final/.stamp
check-delivery: export/$(ASSET).glb
	$(BP) --python src/check_delivery.py -- --source build/finalized.blend --glb $< --out build/botanical-delivery-check.json
check-bake: build/baked.stamp
	$(PYTHON) -c "import json; r=json.load(open('textures/bake/bake-report.json')); assert r['BaseColor']['alpha_missed_interior_texels']==0 and r['BaseColor']['black_interior_texels']==0, r['BaseColor']"
check: check-delivery check-bake

renders/final/.stamp: src/materials.py src/settings.py
renders/hydrangea-final/.stamp: src/materials.py

renders/boxwood-source-final/.matched: build/boxwood/lookdev.blend build/framed-cameras.json src/render.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --species boxwood --out renders/boxwood-source-final --camera-file build/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/framed-cameras.json --renders renders/boxwood-source-final --out renders/boxwood-source-final
	@touch $@
renders/hydrangea-source-final/.matched: build/hydrangea/lookdev.blend build/hydrangea/framed-cameras.json src/render.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --species hydrangea --out renders/hydrangea-source-final --camera-file build/hydrangea/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/hydrangea/framed-cameras.json --renders renders/hydrangea-source-final --out renders/hydrangea-source-final
	@touch $@
build/bake-loss.json: renders/boxwood-source-final/.matched renders/hydrangea-source-final/.matched renders/final/.matched src/bake_loss.py
	$(BP) --python src/bake_loss.py
check-bake-loss: build/bake-loss.json
check: check-bake-loss
