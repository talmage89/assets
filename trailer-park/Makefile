# Dense communities: complete exported presentation and bounded gallery.
OLD_SEED ?= 101
NEW_SEED ?= 202
ROWS ?= 9
PASS ?= final
WIDTH ?= 1440
SAMPLES ?= 32
DELIVERY ?= 1
CHECKPOINT_BLEND := build/family.blend
STEMS := SingleWide-120 SingleWide-147 SingleWide-168 DoubleWide-245 DoubleWide-228 DoubleWide-326 Deck Carport UtilityService PropaneBottles Condenser WindowAC SatelliteDish AddedRoom Household EntranceSign SupportFrame Modules HomeForms Park-$(OLD_SEED) Park-$(NEW_SEED)
CHECKPOINT_OUTPUTS := build/family.blend build/family.json $(foreach s,$(STEMS),export/$(s).gltf export/$(s).bin export/$(s).json)
CHECKPOINT_ARGS := --old-seed $(OLD_SEED) --new-seed $(NEW_SEED) --rows $(ROWS)
CHECKPOINT_DEPS := $(addprefix src/,build.py plans.py geometry.py homes.py home_age.py patina.py era_details.py addons.py site.py site_age.py soil_finish.py sward.py ground_edges.py lot_dressing.py surfaces.py terrain.py textures.py) build/native.stamp build/preserved.json textures/ship/.stamp textures/ship/.lawn-stamp
CHECKPOINT_CHECK = $(BP) --python src/check.py && $(BP) --python src/check_motion.py && $(BP) --python src/look_check.py
CHECKPOINT_OUT := renders/checkpoint/$(PASS)
BASELINE_REVIEW := $(wildcard build/baseline/export/Baseline_Park-101.gltf)
CHECKPOINT_RENDER_ARGS := --cameras build/cameras.json $(if $(BASELINE_REVIEW),--baseline build/baseline/export)
CHECKPOINT_REVIEW = $(PYTHON) src/matches.py compose $(CHECKPOINT_OUT) && $(PYTHON) src/review.py --renders $(CHECKPOINT_OUT) && $(PYTHON) src/metrics.py --renders $(CHECKPOINT_OUT) $(if $(BASELINE_REVIEW),&& $(PYTHON) src/before_after.py $(CHECKPOINT_OUT))
ifeq ($(DELIVERY),1)
CHECKPOINT_OUT := renders/$(PASS)
BASELINE_REVIEW :=
CHECKPOINT_RENDER_ARGS := --cameras build/cameras.json --eevee --delivery
PARK_VIEWS := hero above entrance row
HOME_VIEWS := hero front side back top skirt entry scale
CHECKPOINT_RENDER_OUTPUTS := $(CHECKPOINT_OUT)/provenance.json $(CHECKPOINT_OUT)/Park-202/eevee.png $(foreach s,Park-101 Park-202,$(foreach v,$(PARK_VIEWS),$(CHECKPOINT_OUT)/$(s)/$(v).png)) $(foreach s,SingleWide-120 DoubleWide-228,$(foreach v,$(HOME_VIEWS),$(CHECKPOINT_OUT)/$(s)/$(v).png)) $(foreach s,Deck Carport UtilityService EntranceSign Modules HomeForms SupportFrame,$(CHECKPOINT_OUT)/$(s)/detail.png) $(CHECKPOINT_OUT)/SupportFrame/piers.png renders/source/provenance.json
CHECKPOINT_RENDER_OUTPUTS += $(foreach f,Park-101/single-2009 Park-101/street-2007 Park-101/aerial-2015 Park-202/newer-row-2024,$(CHECKPOINT_OUT)/matches/$(f).png renders/source/matches/$(f).png)
ifneq ($(wildcard build/round4-before/export/Park-101.gltf),)
ifeq ($(wildcard renders/finish-pass4/provenance.json),)
CHECKPOINT_RENDER_OUTPUTS += renders/finish-before/provenance.json renders/finish-before/Park-101/hero.png renders/finish-before/Park-101/row.png renders/finish-before/Park-202/hero.png renders/finish-before/matches/Park-101/street-2007.png
FINISH_CROPS = $(PYTHON) src/finish_crops.py --after $(CHECKPOINT_OUT) &&
endif
endif
ifneq ($(wildcard renders/finish-pass4/provenance.json),)
FINISH_CROPS = $(PYTHON) src/finish_crops.py --before renders/finish-pass4 --after $(CHECKPOINT_OUT) --out renders/last-round-fixes --before-label '5a3935d / same camera and light' &&
endif
CHECKPOINT_REVIEW = $(PYTHON) src/matches.py compose $(CHECKPOINT_OUT) && $(PYTHON) src/review.py --renders $(CHECKPOINT_OUT) && $(PYTHON) src/matches.py compose renders/source && $(PYTHON) src/review.py --renders renders/source && $(FINISH_CROPS) $(PYTHON) src/metrics.py --renders $(CHECKPOINT_OUT) && $(PYTHON) src/presentation_check.py --renders $(CHECKPOINT_OUT)
endif
include ../kit/checkpoint_rules.mk
BP += -t 2
export BLENDER
export PYTHONDONTWRITEBYTECODE := 1
# Completed frames have individual image/source receipts. Preserve them when
# a shared-machine render batch is interrupted; the driver validates reuse.
.PRECIOUS: $(CHECKPOINT_RENDER_OUTPUTS)

build/native.stamp: src/native_build.py src/dependencies.py $(wildcard ../shed/src/*.py) $(wildcard ../utility/src/*.py) $(wildcard ../playground/src/*.py)
	@mkdir -p build $(TMPDIR)
	$(PYTHON) src/dependencies.py
	@touch $@

build/preserved.json: src/preservation.py
	$(PYTHON) src/preservation.py check

textures/source/.stamp: src/textures.py src/weather_fields.py ../ground/src/organic.py
	$(PYTHON) src/textures.py
	@touch $@
textures/4k/.stamp: textures/source/.stamp src/pack_alpha.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/flat_bake.py -- --source textures/source --out textures/4k --name Manufactured --coverage 4.8768 --height-distance .012 --size 4096 --samples 8
	$(PYTHON) src/pack_alpha.py --source textures/source --out textures/4k
	@touch $@
textures/ship/.stamp: textures/4k/.stamp
	$(PYTHON) $(KIT)/downsample.py --source textures/4k --out textures/ship --asset Manufactured --size 2048
	@touch $@
.PHONY: bake
bake: textures/ship/.stamp

textures/ship/.lawn-stamp: src/lawn_maps.py ../community-garden/src/groundcover.py build/native.stamp
	$(PYTHON) src/lawn_maps.py
	@touch $@

build/cameras.json: src/matches.py src/park_matches.py src/plans.py
	@mkdir -p build
	$(PYTHON) src/matches.py
$(CHECKPOINT_RENDER_OUTPUTS): build/cameras.json src/town_context.py src/inspection.py $(BASELINE_REVIEW)
ifeq ($(DELIVERY),1)
$(CHECKPOINT_RENDER_OUTPUTS): src/render_batch.py src/traffic.py
build/age-baseline/.stamp: $(CHECKPOINT_OUTPUTS) src/age_baseline.py
	$(PYTHON) src/age_baseline.py --prepare
	@touch $@
.PHONY: docs
docs: review
	$(PYTHON) src/docs.py --renders $(CHECKPOINT_OUT)
all: docs
endif

.PHONY: baseline
baseline:
	$(PYTHON) src/baseline.py

.PHONY: repeat check-preservation clean-family
repeat: model
	$(PYTHON) src/repeat.py
.PHONY: check-texture-repeat
check-texture-repeat: bake
	$(PYTHON) src/texture_repeat.py
check-preservation:
	$(PYTHON) src/preservation.py check
clean: clean-family
clean-family:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('export','textures')]"
