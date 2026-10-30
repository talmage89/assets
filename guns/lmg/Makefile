# Accepted form, original 4K source bake, one canonical 2K PBR set.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../../kit)
REPO := $(abspath ../..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 32
WIDTH ?= 1600
SAMPLES ?= 64
WEAR ?= 1
MODEL := $(addprefix build/,lmg.blend lmg.glb box_loaded.glb box_empty.glb cartridge.glb case.glb link.glb triangles.json interface.json)
PREPARED := build/delivery/finalized.blend build/delivery/bake-target.blend
BAKED := $(addprefix build/baked/4k/T_Harrow56_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_Harrow56_,BaseColor.png Normal.png ORM.png)
EXPORTS := $(addprefix export/,lmg.glb box_loaded.glb box_empty.glb cartridge.glb case.glb link.glb)
SHOTS := hero,hero_right,side,left,front,back,top,cover_open_full,rear_sight,barrel_handle,front_sight,charging_handle,trigger,furniture,handguard,bipod,belt,box,aimed,aimed_macro,shooter_three_quarter,scale,ammo_pair
PHOTO_SHOTS := right_photo,left_photo,open_photo,trigger_photo,belt_photo,receiver_photo,cover_detail_photo,tray_detail_photo,sight_detail_photo,box_detail_photo,used_photo,used_field_photo,ammo_photo,used_right_photo
SITES := receiver cover handle flash regulator ports feet box butt
comma := ,
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(SHOTS))))
RENDER_DEPS := src/final_render.py src/final_shots.py src/shots.py src/delivery.py ../common/render.py build/render-parameters.txt
.PHONY: all refs model prepare lookdev bake export check render match source-match wear-review precedent extra raw-audit review clean FORCE
all: refs export check render match source-match wear-review precedent extra raw-audit review
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: src/build.py src/geometry.py src/clips.py src/interface.py src/belt.py ../common/ammo556_visual.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/lmg.blend
model: $(MODEL)
$(PREPARED) &: $(MODEL) src/prepare.py ../../kit/finalize.py ../../kit/uv.py
	$(BP) --python src/prepare.py
prepare: $(PREPARED)
build/markings/receiver.png build/markings/headstamp.png &: src/markings.py
	$(PYTHON) src/markings.py
build/bake-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES) wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/render-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/delivery/high.blend: $(PREPARED) build/markings/receiver.png build/markings/headstamp.png src/lookdev.py src/build_high.py build/bake-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR)
lookdev: build/delivery/high.blend
$(BAKED) &: build/delivery/high.blend $(PREPARED) src/config.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/bake-target.blend --high build/delivery/high.blend --out build/baked/4k --asset Harrow56 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED)
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset Harrow56 --size 2048 --alpha-mode independent
$(EXPORTS) &: $(TEXTURES) $(PREPARED) src/export_finish.py
	$(BP) --python src/export_finish.py -- --detachables
export: $(EXPORTS)
check: $(EXPORTS)
	$(PYTHON) $(KIT)/repo_check.py
	$(BP) --python src/check.py -- --source build/lmg.blend --out build/check.json --motion
	$(BP) --python src/verify.py
	$(BP) --python src/test_contacts.py
	$(BP) --python src/form_evidence.py
	$(PYTHON) src/test_belt.py
	$(BP) --python src/preserve_form.py
	$(BP) --python src/atlas_verify.py
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/lmg.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(SHOTS)
renders/final/eevee/hero.png: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/lmg.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png
build/cameras.json: src/white_balance.py src/photo_matches.py src/refine_cameras.py refs/SOURCES.md
	$(PYTHON) src/white_balance.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
	$(PYTHON) src/refine_cameras.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
renders/final/pairs/used_photo-pair.jpg: $(EXPORTS) $(RENDER_DEPS) build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/lmg.glb --out renders/final/photos --camera-file build/cameras.json --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/photos --out renders/final/pairs
match: refs renders/final/pairs/used_photo-pair.jpg
renders/final/source-photos/shots.json: build/delivery/high.blend build/cameras.json $(RENDER_DEPS) src/source_render.py
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/source-photos --camera-file build/cameras.json --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/source-photos --out renders/final/source-pairs
source-match: renders/final/source-photos/shots.json
build/controls/%/high.blend: $(PREPARED) build/markings/receiver.png src/lookdev.py src/build_high.py build/bake-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR) --omit $* --out $@
build/controls/%/baked/bake-report.json: build/controls/%/high.blend src/config.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/bake-target.blend --high $< --out build/controls/$*/baked --asset Harrow56 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
build/controls/%/export/lmg.glb: build/controls/%/baked/bake-report.json src/export_finish.py
	$(PYTHON) $(KIT)/downsample.py --source build/controls/$*/baked --out build/controls/$*/textures --asset Harrow56 --size 2048 --alpha-mode independent
	$(BP) --python src/export_finish.py -- --textures build/controls/$*/textures --out build/controls/$*/export
renders/final/wear/%/hero.png: build/controls/%/export/lmg.glb $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source $< --out renders/final/wear/$* --width $(WIDTH) --samples $(SAMPLES) --shots hero,hero_right
.PRECIOUS: build/controls/%/high.blend build/controls/%/baked/bake-report.json build/controls/%/export/lmg.glb
wear-review: $(addprefix renders/final/wear/,$(addsuffix /hero.png,$(SITES)))
renders/final/precedents/ak/shots.json renders/final/precedents/smg/shots.json &: $(EXPORTS) $(RENDER_DEPS) src/precedents.py $(wildcard ../ak/export/ak.glb ../smg/export/smg.glb)
	$(PYTHON) src/precedents.py --width $(WIDTH) --samples $(SAMPLES)
precedent: renders/final/precedents/ak/shots.json renders/final/precedents/smg/shots.json
renders/final/detachables/done.stamp: $(EXPORTS) $(RENDER_DEPS) src/final_extra.py
	$(PYTHON) src/final_extra.py --width 1000 --samples $(SAMPLES)
	@touch $@
extra: renders/final/detachables/done.stamp
renders/final/raw-check/raw-comparison.json: $(EXPORTS) $(RENDER_DEPS) src/raw_review.py $(FINAL_IMAGES)
	$(PYTHON) src/raw_review.py --samples $(SAMPLES)
raw-audit: renders/final/raw-check/raw-comparison.json
review: render match source-match wear-review precedent extra raw-audit
	$(BP) --python src/control_verify.py
	$(BP) --python src/value_geometry.py
	$(PYTHON) src/look_review.py
	$(PYTHON) src/final_review.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"
