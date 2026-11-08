# Additive checkpoint graph: original exports and maps remain protected inputs.
# No docs target is part of this round. CPU construction never takes GPU lock.
.DEFAULT_GOAL := lookdev-checkpoint
LOOK_PASS ?= lookdev-checkpoint
LOOK_WIDTH ?= 1280
LOOK_SAMPLES ?= 32
LOOK_BP := blender -b -t 2 --factory-startup --python-exit-code 1
LOOK_MAPS := $(foreach c,BaseColor Normal ORM,textures/lookdev/ship/T_ParkingGarage_$(c).png)
LOOK_FORM := $(foreach s,101 202,export/form/ParkingGarageForm-$(s).gltf export/form/sites/ParkingGarageFormSite-$(s).gltf build/lookdev/form-$(s).blend build/lookdev/form-site-$(s).blend build/lookdev/garage-$(s).json)
LOOK_FORM += $(foreach s,101 202,export/form/ParkingGarageForm-$(s).bin export/form/sites/ParkingGarageFormSite-$(s).bin) textures/lookdev/T_GroundParkingTrim_BaseColor.png textures/lookdev/layout.json
LOOK_EXPORTS := $(foreach s,101 202,export/lookdev/ParkingGarageLook-$(s).gltf export/lookdev/ParkingGarageLook-$(s).bin export/lookdev/sites/ParkingGarageLookSite-$(s).gltf export/lookdev/sites/ParkingGarageLookSite-$(s).bin)
LOOK_MODULES := $(foreach n,$(MODULE_NAMES),export/lookdev/modules/$(n).gltf export/lookdev/modules/$(n).bin)
LOOK_SHOTS := hero retained_hero above aisle retained_aisle tee_detail ramp_turn tower tower_landing tower_open entry top_deck
LOOK_RENDERS := $(foreach s,101 202,$(foreach n,$(LOOK_SHOTS),renders/$(LOOK_PASS)/$(s)/$(n).png)) renders/$(LOOK_PASS)/101/plan_path.png
BEFORE_RENDERS := $(foreach s,101 202,$(foreach n,hero aisle tower above entry ramp_turn top_deck,renders/before/checkpoint/$(s)/$(n).png))
BEFORE_OPEN := $(foreach s,101 202,renders/before/open-lift/$(s)/tower_open.png)

.PHONY: lookdev-checkpoint lookdev-form lookdev-atlas lookdev-export lookdev-review lookdev-check lookdev-before-after
lookdev-checkpoint: refs check lookdev-review lookdev-before-after
lookdev-form: $(LOOK_FORM) build/lookdev/baseline-cameras.json
$(LOOK_FORM) &: $(CHECKPOINT_OUTPUTS) build/context/.stamp src/form_build.py src/form.py src/town_detail.py src/tower_detail.py src/tee_detail.py src/setting.py src/tangent_rounding.py
	mkdir -p build/lookdev
	$(LOOK_BP) --python src/form_build.py --
build/lookdev/baseline-cameras.json: $(SITE_OUTPUTS) src/baseline_views.py
	mkdir -p build/lookdev
	$(LOOK_BP) --python src/baseline_views.py --
build/lookdev/baseline.json: $(CHECKPOINT_OUTPUTS) $(SITE_OUTPUTS)
	$(PYTHON) src/preserve.py
build/lookdev/comparison-precast.blend build/lookdev/comparison-harmon.blend &: $(LOOK_FORM) src/comparison_build.py src/precast_specimen.py
	$(LOOK_BP) --python src/comparison_build.py --
build/lookdev/matches/calibration.json: src/match_revision.py build/lookdev/garage-101.json
	$(PYTHON) src/match_revision.py

build/lookdev/atlas-source/T_ParkingGarage_BaseColor.png build/lookdev/atlas-source/T_ParkingGarage_Height.png build/lookdev/atlas-source/T_ParkingGarage_ORM.png build/lookdev/atlas-layout.json &: src/atlas_source.py
	$(PYTHON) src/atlas_source.py
build/lookdev/atlas-bake/T_ParkingGarage_BaseColor.png build/lookdev/atlas-bake/T_ParkingGarage_Normal.png build/lookdev/atlas-bake/T_ParkingGarage_ORM.png &: build/lookdev/atlas-source/T_ParkingGarage_BaseColor.png build/lookdev/atlas-source/T_ParkingGarage_Height.png build/lookdev/atlas-source/T_ParkingGarage_ORM.png src/bake_atlas.py
	$(KIT)/with_gpu.sh $(LOOK_BP) --python src/bake_atlas.py --
$(LOOK_MAPS) &: build/lookdev/atlas-bake/T_ParkingGarage_BaseColor.png build/lookdev/atlas-bake/T_ParkingGarage_Normal.png build/lookdev/atlas-bake/T_ParkingGarage_ORM.png
	mkdir -p textures/lookdev/ship
	$(PYTHON) $(KIT)/downsample.py --source build/lookdev/atlas-bake --out textures/lookdev/ship --asset ParkingGarage --size 2048
lookdev-atlas: $(LOOK_MAPS)
$(LOOK_EXPORTS) $(LOOK_MODULES) build/lookdev/sites.json build/lookdev/modules.json export/lookdev/comparison-precast.gltf export/lookdev/comparison-harmon.gltf &: $(LOOK_FORM) $(LOOK_MAPS) build/lookdev/comparison-precast.blend build/lookdev/comparison-harmon.blend src/lookdev_build.py src/atlas_binding.py src/service_age.py
	$(LOOK_BP) --python src/lookdev_build.py --
lookdev-export: $(LOOK_EXPORTS) $(LOOK_MODULES)

build/lookdev/render-parameters.json: FORCE
	mkdir -p build/lookdev
	$(PYTHON) src/render_parameters.py --width $(LOOK_WIDTH) --samples $(LOOK_SAMPLES)
$(LOOK_RENDERS) $(BEFORE_OPEN) renders/$(LOOK_PASS)/views.json renders/$(LOOK_PASS)-matches/contact.jpg renders/$(LOOK_PASS)-source-matches/contact.jpg &: $(LOOK_EXPORTS) build/lookdev/baseline-cameras.json build/lookdev/matches/calibration.json build/lookdev/render-parameters.json src/light_review.py src/lookdev_render.py src/match_render.py src/review_batch.py
	$(KIT)/with_gpu.sh $(LOOK_BP) --python src/review_batch.py -- --stage lookdev --pass-name $(LOOK_PASS) --width $(LOOK_WIDTH) --samples $(LOOK_SAMPLES) --source-pairs --baselines
	$(PYTHON) src/lookdev_review.py --pass-name $(LOOK_PASS)
lookdev-review: $(LOOK_RENDERS) renders/$(LOOK_PASS)-matches/contact.jpg renders/$(LOOK_PASS)-source-matches/contact.jpg
lookdev-check: $(LOOK_EXPORTS) $(LOOK_MODULES) build/lookdev/baseline.json
	$(LOOK_BP) --python src/lookdev_check.py --
	$(LOOK_BP) --python src/motion_check.py -- --lookdev
	$(PYTHON) src/dependencies.py
	$(PYTHON) $(KIT)/repo_check.py
check: lookdev-check
$(BEFORE_RENDERS) &: | $(SITE_OUTPUTS) build/lookdev/baseline-cameras.json
	$(KIT)/with_gpu.sh $(LOOK_BP) --python src/lookdev_render.py -- --stage baseline --out renders/before/checkpoint --shots retained_hero,retained_aisle,tower,above,entry,ramp_turn,top_deck --width 1200 --samples 24
lookdev-before-after: lookdev-review $(BEFORE_RENDERS) $(BEFORE_OPEN)
	$(PYTHON) src/before_after.py --pass-name $(LOOK_PASS)
.PHONY: lookdev-repeat lookdev-bake-repeat
lookdev-repeat:
	$(PYTHON) src/lookdev_repeat.py
lookdev-bake-repeat:
	$(KIT)/with_gpu.sh $(LOOK_BP) --python src/bake_repeat.py --
