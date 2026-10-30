# Meridian Six: procedural source, 4K bake, single 2K animated atlas delivery.
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
SHIP_SIZE := 2048
BEFORE ?= ../../build/revolver-last-fixes/before
MODEL := build/revolver.blend build/sculpt.blend build/revolver.glb build/cartridge.glb build/case.glb build/speedloader_loaded.glb build/triangles.json
BAKED := $(addprefix build/baked/4k/T_MeridianSix_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_MeridianSix_,BaseColor.png Normal.png ORM.png)
EXPORTS := export/revolver.glb export/cartridge.glb export/case.glb export/speedloader_loaded.glb
SUBSET_LAYOUTS := $(addprefix build/delivery/detachables/,cartridge/layout.json case/layout.json speedloader_loaded/layout.json)
MARKS := $(addprefix build/markings/,barrel.png frame.png headstamp.png)
comma := ,
FINAL_SHOTS := hero,hero_left,wear_front,side,front,back,top,open,star,reload,sights,grip,muzzle,shank,frame_bottom,hammer_rest,hammer_cocked,hammer_top,grip_seam,aimed,scale,rod_detail,lug_under,rear_slot
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json
PHOTO_SHOTS := right_photo,left_photo,open_photo,used_photo
PAIRS := $(foreach v,right left open used,renders/final/pairs/$(v)_photo-pair.jpg)
RENDER_DEPS := src/presentation.py src/hammer_review.py src/render.py src/final_shots.py src/shots.py ../common/render.py build/render-parameters.txt
.PHONY: all refs model prepare lookdev bake export check check-repo verify check-repeat render match source-match hammers strips standalones review docs fix-pairs form clean FORCE
all: refs export check render match source-match hammers strips standalones review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: src/build.py src/parameters.py src/clips.py src/interface.py ../common/magnum357.py ../../kit/model.py ../../kit/weapon.py ../../kit/rig.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/revolver.blend
model: $(MODEL)
build/delivery/finalized.blend build/delivery/uv.json &: $(MODEL) src/prepare.py src/config.py ../../kit/finalize.py ../../kit/uv.py
	$(BP) --python src/prepare.py
prepare: build/delivery/finalized.blend
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
build/delivery/high.blend: build/delivery/finalized.blend build/sculpt.blend $(MARKS) src/build_high.py src/lookdev.py build/wear-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR)
lookdev: build/delivery/high.blend
$(BAKED) &: build/delivery/high.blend build/delivery/finalized.blend src/config.py build/bake-parameters.txt ../../kit/bake.py ../../kit/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high build/delivery/high.blend --out build/baked/4k --asset MeridianSix --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED) ../../kit/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset MeridianSix --size $(SHIP_SIZE)
$(EXPORTS) $(SUBSET_LAYOUTS) &: $(TEXTURES) build/delivery/finalized.blend src/config.py ../../kit/export.py ../../kit/weapon.py src/export_config.py ../../kit/detachable_textures.py ../../kit/detachable_clusters.py ../../kit/gltf.py
	@mkdir -p export
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset MeridianSix --config src/export_config.py --out export/revolver.glb --report build/delivery/export.json
	$(BP) --python $(KIT)/gltf.py -- --source export/revolver.glb --config src/export_config.py
export: $(EXPORTS) $(SUBSET_LAYOUTS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
build/check.json: $(MODEL) src/check.py src/contacts.py src/semantics.py
	$(BP) --python src/check.py -- --source build/revolver.blend --out $@
build/serialization.json: $(MODEL) src/verify.py src/contacts.py src/semantics.py
	$(BP) --python src/verify.py -- --source build/revolver.blend --out $@
verify: build/serialization.json
build/form-metrics.json: $(MODEL) src/form_metrics.py
	$(BP) --python src/form_metrics.py -- --source build/revolver.blend --out $@
build/repeat/revolver.blend: $(MODEL)
	$(BP) --python src/build.py -- --out $@
build/repeat.json: build/repeat/revolver.blend $(MODEL) src/repeat.py
	$(BP) --python src/repeat.py -- --first build/revolver.blend --second build/repeat/revolver.blend --out $@
check-repeat: build/repeat.json
build/delivery/construction.json: build/delivery/finalized.blend src/check.py src/contacts.py src/semantics.py
	$(BP) --python src/check.py -- --source build/delivery/finalized.blend --out $@
build/delivery/verify.json build/delivery/imported-parts.blend &: $(EXPORTS) $(SUBSET_LAYOUTS) build/delivery/finalized.blend src/atlas_verify.py ../../kit/detachable_verify.py
	$(BP) --python src/atlas_verify.py
build/delivery/imported-construction.json: build/delivery/imported-parts.blend src/check.py src/contacts.py src/semantics.py
	$(BP) --python src/check.py -- --source build/delivery/imported-parts.blend --out $@
build/surface-audit.json: $(EXPORTS) src/surface_audit.py
	$(BP) --python src/surface_audit.py
build/delivery/high-critical.json: build/delivery/high.blend src/high_check.py src/contacts.py
	$(BP) --python src/high_check.py
check: check-repo build/delivery/high-critical.json build/surface-audit.json build/check.json build/serialization.json build/form-metrics.json build/repeat.json build/delivery/construction.json build/delivery/verify.json build/delivery/imported-construction.json
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/revolver.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS)
renders/final/eevee/hero.png renders/final/eevee/shots.json &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/revolver.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png renders/final/eevee/shots.json
build/references/whitebalance.json: src/prepare_refs.py refs/SOURCES.md | refs
	$(PYTHON) src/prepare_refs.py
build/photo-cameras.json: build/references/whitebalance.json src/photo_matches.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
$(PAIRS) &: $(EXPORTS) $(RENDER_DEPS) build/photo-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/revolver.glb --out renders/final/photos --width $(WIDTH) --samples $(SAMPLES) --camera-file build/photo-cameras.json --shots $(PHOTO_SHOTS)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/photo-cameras.json --renders renders/final/photos --out renders/final/pairs
build/value-loci.json: $(EXPORTS) build/photo-cameras.json src/value_loci.py
	$(BP) --python src/value_loci.py -- --source export/revolver.glb --out $@
renders/final/photos/values.json: $(PAIRS) build/value-loci.json src/value_review.py
	$(PYTHON) src/value_review.py
match: $(PAIRS) renders/final/photos/values.json
renders/final/source-pairs/.stamp: build/delivery/high.blend $(RENDER_DEPS) build/photo-cameras.json src/source_render.py
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/source-photos --width $(WIDTH) --samples $(SAMPLES) --camera-file build/photo-cameras.json --shots $(PHOTO_SHOTS)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/photo-cameras.json --renders renders/final/source-photos --out renders/final/source-pairs
	touch $@
source-match: renders/final/source-pairs/.stamp
renders/final/hammer-pairs/.stamp: $(EXPORTS) $(RENDER_DEPS) build/references/whitebalance.json src/hammer_review.py
	$(KIT)/with_gpu.sh $(BP) --python src/hammer_review.py -- --source export/revolver.glb --out renders/final/hammer --width 1200 --samples $(SAMPLES) --shots hammer_rest_photo,hammer_cocked_photo
	$(PYTHON) src/hammer_review.py --compose --renders renders/final/hammer --out renders/final/hammer-pairs
	touch $@
hammers: renders/final/hammer-pairs/.stamp
renders/final/strips/timing.json: $(EXPORTS) $(RENDER_DEPS) src/strips.py ../common/strips.py
	$(PYTHON) src/strips.py
strips: renders/final/strips/timing.json
renders/final/ammo/.stamp: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/cartridge.glb --out renders/final/ammo/cartridge --width 1200 --samples $(SAMPLES) --shots cartridge,cartridge_head
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/case.glb --out renders/final/ammo/case --width 1200 --samples $(SAMPLES) --shots case,case_head
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/speedloader_loaded.glb --out renders/final/ammo/loader --width 1200 --samples $(SAMPLES) --shots speedloader
	touch $@
renders/final/ammo/calibration/shots.json: export/cartridge.glb $(RENDER_DEPS) src/ammo_calibration.py
	$(KIT)/with_gpu.sh $(BP) --python src/ammo_calibration.py -- --source export/cartridge.glb --out renders/final/ammo/calibration --width 1200 --samples $(SAMPLES)
standalones: renders/final/ammo/.stamp renders/final/ammo/calibration/shots.json
renders/final/ammo/values.json: renders/final/ammo/calibration/shots.json renders/final/ammo/.stamp src/ammo_values.py build/references/whitebalance.json
	$(BP) --python src/ammo_values.py
review: render match hammers strips standalones renders/final/ammo/values.json
	$(PYTHON) src/final_review.py
	$(PYTHON) src/photo_gauges.py
docs: review
	$(PYTHON) src/final_review.py --docs
# Historical binary evidence is optional and stays ignored. The ordinary
# from-nothing build never depends on a preserved previous-session artifact.
fix-pairs: render hammers build/photo-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/fix_render.py -- --source $(BEFORE)/revolver.glb --out $(BEFORE)/matched --width $(WIDTH) --samples $(SAMPLES) --shots rod_detail,muzzle,lug_under,rear_slot
	$(PYTHON) src/fix_review.py --before $(BEFORE)
form:
	$(MAKE) -f src/form_rules.mk
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"

include ../common/gif.mk
