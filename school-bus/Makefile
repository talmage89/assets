# Form/construction checkpoint only. Final look development is deliberately deferred.
CHECKPOINT_BLEND := build/bus-101.blend
CHECKPOINT_ARGS := --seed 101
CHECKPOINT_DEPS := src/build.py src/spec.py src/finishes.py src/markings.py build/markings/.stamp
CHECKPOINT_OUT := renders/checkpoint
WIDTH ?= 1400
SAMPLES ?= 48
BLENDER ?= blender -t 4
SEEDS := 101 102 103
DELIVERIES := $(foreach s,$(SEEDS),export/C75-$(s).gltf export/C75-$(s).bin)
VIEWS := hero front side rear top rear_three_quarter front_detail entrance interior aisle warning emergency roof scale fleet
CHECKPOINT_RENDER_OUTPUTS := $(foreach v,$(VIEWS),renders/checkpoint/$(v).png) renders/checkpoint/provenance.json
# The family checkpoint supports glTF external images, superseding the kit's GLB default argument.
CHECKPOINT_RENDER_ARGS := --source export/C75-101.gltf --school ../school/export/Campus-101.gltf
CHECKPOINT_CHECK := $(PYTHON) src/report_checks.py
CHECKPOINT_REVIEW := $(PYTHON) src/review.py
include ../kit/checkpoint_rules.mk

build/markings/.stamp: src/markings.py src/spec.py
	@mkdir -p build/markings
	$(PYTHON) src/markings.py build/markings
	@touch $@

build/prepared.blend: $(CHECKPOINT_BLEND) ../cars/src/prepare_bake.py
	$(BP) --python ../cars/src/prepare_bake.py -- --source $< --out $@

build/finalized.blend build/uv.json &: build/prepared.blend src/config.py src/finalize.py ../cars/src/sedan_finalize.py
	$(BP) --python src/finalize.py -- --source $< --out build/finalized.blend --config src/config.py --report build/uv.json --size 2048 --target-density 300 --margin .0012

textures/4k/T_SchoolBus_BaseColor.png textures/4k/T_SchoolBus_Normal.png textures/4k/T_SchoolBus_ORM.png &: build/finalized.blend src/bake.py
	@mkdir -p textures/4k
	$(KIT)/with_gpu.sh $(BP) --python src/bake.py -- --source $< --out textures/4k --size 4096 --samples 12

textures/2k/T_SchoolBus_BaseColor.png textures/2k/T_SchoolBus_Normal.png textures/2k/T_SchoolBus_ORM.png &: textures/4k/T_SchoolBus_BaseColor.png textures/4k/T_SchoolBus_Normal.png textures/4k/T_SchoolBus_ORM.png
	@mkdir -p textures/2k
	$(PYTHON) $(KIT)/downsample.py --source textures/4k --out textures/2k --asset SchoolBus --size 2048 --alpha-mode independent

define EXPORT_SEED
export/C75-$(1).gltf export/C75-$(1).bin build/export-$(1).json &: build/finalized.blend textures/2k/T_SchoolBus_BaseColor.png textures/2k/T_SchoolBus_Normal.png textures/2k/T_SchoolBus_ORM.png src/export.py src/config.py
	@mkdir -p export
	$$(BP) --python src/export.py -- --source build/finalized.blend --textures textures/2k --asset SchoolBus --out export/C75-$(1).glb --report build/export-$(1).json --config src/config.py --variant $(1)
endef
$(foreach s,$(SEEDS),$(eval $(call EXPORT_SEED,$(s))))

build/model-check.json: $(CHECKPOINT_BLEND) src/check.py
	$(BP) --python src/check.py -- --model $< --out $@

build/delivery-%.json: export/C75-%.gltf export/C75-%.bin src/check.py
	$(BP) --python src/check.py -- --gltf $< --parts build/finalized.blend --out $@

build/motion.json: $(CHECKPOINT_BLEND) src/motion_config.py
	$(BP) --python $(KIT)/motion.py -- --source $< --config src/motion_config.py --out $@

renders/seethrough/counts.json: export/C75-101.gltf export/C75-101.bin build/finalized.blend src/seethrough.py
	$(KIT)/with_gpu.sh $(BP) --python src/seethrough.py -- --source $< --parts build/finalized.blend --out renders/seethrough --width 1400

build/calibration.json: refs/SOURCES.md src/photo_matches.py src/balance_refs.py
	$(PYTHON) src/balance_refs.py
	PYTHONPATH=src:.. $(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@

renders/matches/provenance.json: export/C75-101.gltf export/C75-101.bin build/calibration.json src/render.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/calibration.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --out renders/matches --calibration build/calibration.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/calibration.json --renders renders/matches --out renders/matches

renders/source-matches/provenance.json: $(CHECKPOINT_BLEND) build/calibration.json src/render.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --out renders/source-matches --calibration build/calibration.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/calibration.json --renders renders/source-matches --out renders/source-matches

renders/eevee/hero.png: export/C75-101.gltf export/C75-101.bin src/render.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $< --out renders/eevee --shots hero --engine BLENDER_EEVEE --width $(WIDTH) --samples $(SAMPLES)

build/school-fit.json: export/C75-101.gltf export/C75-101.bin build/model-check.json src/check_school_fit.py
	$(BP) --python src/check_school_fit.py

$(CHECKPOINT_RENDER_OUTPUTS): $(DELIVERIES) src/views.py src/lamp_states.py
check: build/model-check.json $(foreach s,$(SEEDS),build/delivery-$(s).json) build/motion.json renders/seethrough/counts.json build/school-fit.json
render: renders/matches/provenance.json renders/source-matches/provenance.json renders/eevee/hero.png
.PHONY: export matches
export: $(DELIVERIES)
matches: renders/matches/provenance.json
