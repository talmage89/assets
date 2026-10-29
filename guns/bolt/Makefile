# PD Vesper B24: accepted geometry, original 4K source bake, 2K animated delivery.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../../kit)
REPO := $(abspath ../..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WEAR ?= .85
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 32
WIDTH ?= 1600
SAMPLES ?= 64
PASS ?= pass1
SHIP_SIZE := 2048
MODEL := build/bolt.blend build/sculpt.blend build/bolt.glb build/magazine_loaded.glb build/magazine_empty.glb build/case.glb build/triangles.json build/interface.json
PREPARED := build/delivery/finalized.blend $(addprefix build/delivery/,bolt-uv.json magazine-uv.json case-uv.json)
MARKS := $(addprefix build/markings/,receiver-left.png receiver-right.png headstamp.png scope.png turret.png)
BAKED := $(addprefix build/baked/4k/T_VesperB24_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_VesperB24_,BaseColor.png Normal.png ORM.png)
EXPORTS := export/bolt.glb export/magazine_loaded.glb export/magazine_empty.glb export/case.glb
SUBSET_LAYOUTS := $(addprefix build/delivery/detachables/,magazine_loaded/layout.json magazine_empty/layout.json case/layout.json)
comma := ,
FINAL_SHOTS := hero,hero_left,front,side,back,top,bolt_open,deployed,grip,optic,wrist,aimed,scale,crown,bipod_detail,rings,rear_cocked,bottom
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json renders/final/beauty/aimed-range.exr renders/final/beauty/aimed-range.png renders/final/beauty/scope-integration.json
EXTRAS := renders/final/loaded/magazine.png renders/final/empty/magazine.png renders/final/case/case.png renders/final/case/case_mouth.png
PAIRS := $(foreach v,right_photo profile_right left_photo open_photo wrist_photo used_open,renders/final/pairs/$(v)-pair.jpg)
WEAR_PAIR := renders/final/pairs/hero-wear-pair.jpg renders/final/pairs/hero-wear-values.json
CLIPS := Idle IdleEmpty Fire FireLast Reload ReloadEmpty Inspect BipodDeploy BipodFold
STRIPS := $(addprefix renders/final/strips/,$(addsuffix .jpg,$(CLIPS))) $(addprefix renders/final/strips/,$(addsuffix .webp,$(CLIPS))) renders/final/strips/timing.json
RENDER_DEPS := src/render.py src/shots.py src/final_shots.py src/scope_integration.py ../common/render.py build/render-parameters.txt
.PHONY: all refs model prepare lookdev bake export atlas check check-repo verify check-atlas check-repeat render match source-match strips shells extra orthos atlas-views review docs critique wear-audit sections clean FORCE check-high details trigger-match
all: refs export check render match strips extra source-match trigger-match review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: src/build.py src/geometry.py src/mechanism.py src/trigger.py src/clips.py src/interface.py ../../kit/model.py ../../kit/weapon.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/bolt.blend
model: $(MODEL)
$(PREPARED) &: $(MODEL) src/prepare.py src/trigger.py ../../kit/finalize.py ../../kit/uv.py
	$(BP) --python src/prepare.py
prepare: $(PREPARED)
$(MARKS) &: src/markings.py ../../kit/fonts.py
	$(PYTHON) src/markings.py
build/wear-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/bake-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES) ship=$(SHIP_SIZE)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/delivery/high.blend: $(PREPARED) $(MARKS) src/build_high.py src/lookdev.py build/sculpt.blend build/wear-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR)
lookdev: build/delivery/high.blend
$(BAKED) &: build/delivery/high.blend $(PREPARED) src/config.py build/bake-parameters.txt ../../kit/bake.py ../../kit/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high build/delivery/high.blend --out build/baked/4k --asset VesperB24 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED) ../../kit/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset VesperB24 --size $(SHIP_SIZE)
$(EXPORTS) $(SUBSET_LAYOUTS) &: $(TEXTURES) $(PREPARED) src/config.py src/case_config.py src/stable_delivery.py ../../kit/export.py ../../kit/weapon.py src/export_config.py ../../kit/detachable_textures.py ../../kit/detachable_clusters.py
	@mkdir -p export
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset VesperB24 --config src/export_config.py --out export/bolt.glb --report build/delivery/export.json
	$(BP) --python src/stable_delivery.py -- export/bolt.glb
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset VesperB24 --config src/case_config.py --out export/case.glb --report build/delivery/case-export.json
export: $(EXPORTS) $(SUBSET_LAYOUTS)
atlas: $(EXPORTS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: $(MODEL)
	$(BP) --python src/verify.py -- --source build/bolt.blend --out build/serialization.json
check-repeat: $(MODEL)
	$(BP) --python src/build.py -- --out build/repeat/bolt.blend
	$(BP) --python src/repeat.py
check-atlas: $(EXPORTS) $(SUBSET_LAYOUTS)
	$(BP) --python src/check.py -- --source build/delivery/finalized.blend --out build/delivery/construction.json --motion
	$(BP) --python src/atlas_verify.py
	$(BP) --python src/check.py -- --source build/delivery/imported-parts.blend --out build/delivery/imported-construction.json --motion

check-high: build/delivery/high.blend
	$(BP) --python src/check.py -- --source build/delivery/high.blend --dense --out build/delivery/high-construction.json --motion
check: check-repo verify check-atlas check-repeat check-high
	$(BP) --python src/check.py -- --source build/bolt.blend --out build/check.json --motion
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/bolt.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS)
renders/final/eevee/hero.png renders/final/eevee/shots.json &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/bolt.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png renders/final/eevee/shots.json
orthos: render
atlas-views: render match
build/cameras.json: src/photo_matches.py src/photo_calibration.py src/white_balance.py refs/SOURCES.md
	$(PYTHON) src/photo_calibration.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
$(PAIRS) &: $(EXPORTS) $(RENDER_DEPS) src/photo_matches.py build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/bolt.glb --out renders/final/photos --width $(WIDTH) --samples $(SAMPLES) --shots right_photo,profile_right,left_photo,open_photo,wrist_photo,used_open --camera-file build/cameras.json
	$(PYTHON) src/compose_pairs.py --renders renders/final/photos --out renders/final/pairs
$(WEAR_PAIR) &: $(FINAL_IMAGES) src/wear_review.py refs/SOURCES.md build/cameras.json
	$(PYTHON) src/wear_review.py
build/value-loci.json: $(PREPARED) src/value_loci.py
	$(BP) --python src/value_loci.py
match: refs $(PAIRS) $(WEAR_PAIR) build/value-loci.json
source-match: build/delivery/high.blend build/cameras.json $(RENDER_DEPS) src/source_render.py
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/source-photos --width $(WIDTH) --samples $(SAMPLES) --shots right_photo,profile_right,left_photo,open_photo,wrist_photo,used_open --camera-file build/cameras.json
	$(PYTHON) src/compose_pairs.py --renders renders/final/source-photos --out renders/final/source-pairs
build/trigger-cameras.json: src/trigger_matches.py refs/SOURCES.md
	$(PYTHON) $(KIT)/photo_match.py solve --config src/trigger_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
TRIGGER_SHOTS := trigger_right trigger_quarter trigger_pulled trigger_photo_right trigger_photo_quarter
TRIGGER_PAIRS := trigger_photo_right trigger_photo_quarter
TRIGGER_IMAGES := $(addprefix renders/final/trigger/,$(addsuffix .png,$(TRIGGER_SHOTS))) renders/final/trigger/shots.json $(addprefix renders/final/trigger-pairs/,$(addsuffix -pair.jpg,$(TRIGGER_PAIRS)))
TRIGGER_SOURCE := $(addprefix renders/final/trigger-source/,$(addsuffix .png,$(TRIGGER_PAIRS))) renders/final/trigger-source/shots.json $(addprefix renders/final/trigger-source-pairs/,$(addsuffix -pair.jpg,$(TRIGGER_PAIRS)))
$(TRIGGER_IMAGES) &: $(EXPORTS) build/trigger-cameras.json src/trigger_views.py src/compose_pairs.py $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/trigger_views.py -- --source export/bolt.glb --out renders/final/trigger --width $(WIDTH) --samples $(SAMPLES) --shots trigger_right,trigger_quarter,trigger_pulled,trigger_photo_right,trigger_photo_quarter --camera-file build/trigger-cameras.json
	$(PYTHON) src/compose_pairs.py --calibration build/trigger-cameras.json --renders renders/final/trigger --out renders/final/trigger-pairs
$(TRIGGER_SOURCE) &: build/delivery/high.blend build/trigger-cameras.json src/source_render.py src/compose_pairs.py $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/trigger-source --width $(WIDTH) --samples $(SAMPLES) --shots trigger_photo_right,trigger_photo_quarter --camera-file build/trigger-cameras.json
	$(PYTHON) src/compose_pairs.py --calibration build/trigger-cameras.json --renders renders/final/trigger-source --out renders/final/trigger-source-pairs
trigger-match: $(TRIGGER_IMAGES) $(TRIGGER_SOURCE)
$(EXTRAS) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/magazine_loaded.glb --out renders/final/loaded --width 1100 --samples $(SAMPLES) --shots magazine
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/magazine_empty.glb --out renders/final/empty --width 1100 --samples $(SAMPLES) --shots magazine
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/case.glb --out renders/final/case --width 1100 --samples $(SAMPLES) --shots case,case_mouth
DETAIL_IMAGES := renders/final/details/receiver_markings.png renders/final/details/forend_wear.png renders/final/details/shots.json
$(DETAIL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS) src/details.py
	$(KIT)/with_gpu.sh $(BP) --python src/details.py -- --source export/bolt.glb --out renders/final/details --width $(WIDTH) --samples $(SAMPLES) --shots receiver_markings,forend_wear
details: $(DETAIL_IMAGES)
extra: $(EXTRAS) $(DETAIL_IMAGES)
$(STRIPS) &: $(EXPORTS) $(RENDER_DEPS) src/strips.py src/interface.py ../common/strips.py
	$(PYTHON) src/strips.py
strips: $(STRIPS)
critique: $(EXPORTS) build/cameras.json
	$(PYTHON) src/critique.py --pass $(PASS)
wear-audit: $(EXPORTS) src/wear_mask.py
	$(KIT)/with_gpu.sh $(BP) --python src/wear_mask.py -- --out build/review/wear-final
review: render match strips extra trigger-match
	$(PYTHON) src/final_review.py
docs: review
	$(PYTHON) src/final_review.py --docs
sections: $(MODEL)
	$(BP) --python src/sections.py

clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"
