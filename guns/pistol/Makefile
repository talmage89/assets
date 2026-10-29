# PD C9 final delivery. All geometry and image pixels are generated locally.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../../kit)
REPO := $(abspath ../..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WEAR ?= .72
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 32
WIDTH ?= 1600
SAMPLES ?= 64
PASS ?= pass1
SHIP_SIZE := 2048
MODEL := build/pistol.blend build/sculpt.blend build/pistol.glb build/magazine_loaded.glb build/magazine_empty.glb build/case.glb build/triangles.json
PREPARED := build/delivery/finalized.blend build/delivery/pistol-uv.json build/delivery/magazine-uv.json build/delivery/case-uv.json
MARKS := $(addprefix build/markings/,slide-left.png slide-right.png frame-left.png frame-right.png magazine.png)
BAKED := $(addprefix build/baked/4k/T_C9_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_C9_,BaseColor.png Normal.png ORM.png)
EXPORTS := export/pistol.glb export/magazine_loaded.glb export/magazine_empty.glb export/case.glb
SUBSET_LAYOUTS := $(addprefix build/delivery/detachables/,magazine_loaded/layout.json magazine_empty/layout.json case/layout.json)
comma := ,
FINAL_SHOTS := hero,hero_left,front,side,back,top,rear_sights,grip_texture,port_hood,markings,aimed,locked,scale,hand_frame,trigger_right,trigger_quarter,trigger_pulled
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json
EXTRAS := $(foreach v,loaded empty,renders/final/$(v)/mag_standalone.png renders/final/$(v)/mag_rear.png renders/final/$(v)/shots.json) renders/final/case/case.png renders/final/case/case_mouth.png renders/final/case/shots.json
PAIRS := $(foreach v,right open left,renders/final/pairs/$(v)_photo-pair.jpg renders/final/pairs/$(v)_photo-calibration.jpg)
CLIPS := Idle Fire FireSemi FireLast Reload ReloadEmpty Inspect Charge IdleOpen IdleEmpty
STRIPS := $(addprefix renders/final/strips/,$(addsuffix .jpg,$(CLIPS))) $(addprefix renders/final/strips/,$(addsuffix .webp,$(CLIPS))) renders/final/strips/timing.json
RENDER_DEPS := src/render.py src/final_shots.py src/shots.py ../common/render.py ../common/photo_matches.py build/render-parameters.txt
.PHONY: all refs model prepare lookdev bake export atlas atlas-views orthos check verify check-atlas check-repo render match strips extra review docs critique sections clean FORCE
all: refs export check render match strips extra review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: src/build.py src/frame_form.py src/clips.py src/interface.py ../../kit/model.py ../../kit/weapon.py ../../kit/rig.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/pistol.blend
model: $(MODEL)
$(PREPARED) &: $(MODEL) src/prepare.py ../../kit/finalize.py ../../kit/uv.py
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
build/delivery/high.blend: $(PREPARED) $(MARKS) build/sculpt.blend src/build_high.py src/lookdev.py build/wear-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR)
lookdev: build/delivery/high.blend
$(BAKED) &: build/delivery/high.blend $(PREPARED) src/config.py build/bake-parameters.txt ../../kit/bake.py ../../kit/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high build/delivery/high.blend --out build/baked/4k --asset C9 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED) ../../kit/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset C9 --size $(SHIP_SIZE)
$(EXPORTS) $(SUBSET_LAYOUTS) &: $(TEXTURES) $(PREPARED) src/config.py src/case_config.py ../../kit/export.py ../../kit/weapon.py src/export_config.py ../../kit/detachable_textures.py ../../kit/gltf.py
	@mkdir -p export
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset C9 --config src/export_config.py --out export/pistol.glb --report build/delivery/export.json
	$(BP) --python $(KIT)/gltf.py -- --source export/pistol.glb --config src/export_config.py
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset C9 --config src/case_config.py --out export/case.glb --report build/delivery/case-export.json
export: $(EXPORTS) $(SUBSET_LAYOUTS)
atlas: export
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: $(MODEL)
	$(BP) --python src/verify.py -- --source build/pistol.blend --out build/serialization.json
check-atlas: $(EXPORTS) $(SUBSET_LAYOUTS)
	$(BP) --python src/check.py -- --source build/delivery/finalized.blend --out build/delivery/construction.json --motion
	$(BP) --python src/atlas_verify.py
	$(BP) --python src/surface_audit.py
check: check-repo verify check-atlas
	$(BP) --python src/check.py -- --source build/pistol.blend --out build/check.json --motion
	$(BP) --python src/check.py -- --source build/sculpt.blend --dense-source --out build/sculpt-check.json --motion
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/pistol.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS)
renders/final/eevee/hero.png renders/final/eevee/shots.json &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/pistol.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png renders/final/eevee/shots.json
atlas-views: render match
orthos: render
build/cameras.json: src/photo_matches.py refs/SOURCES.md refs/round2-right.jpg refs/round2-open.jpg refs/daylight-side.jpg
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
$(PAIRS) &: $(EXPORTS) $(RENDER_DEPS) build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/pistol.glb --out renders/final/photos --width $(WIDTH) --samples $(SAMPLES) --shots right_photo,open_photo,left_photo --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/photos --out renders/final/pairs
TRIGGER_PAIRS := $(foreach v,right quarter,renders/final/trigger-pairs/trigger_$(v)_photo-pair.jpg)
$(TRIGGER_PAIRS) &: $(EXPORTS) src/trigger_render.py src/trigger_matches.py ../common/trigger_review.py $(RENDER_DEPS) refs/SOURCES.md
	$(KIT)/with_gpu.sh $(BP) --python src/trigger_render.py -- --source export/pistol.glb --out renders/final/trigger-photos --width 1100 --samples $(SAMPLES) --shots trigger_right_photo,trigger_quarter_photo
	$(PYTHON) src/trigger_render.py --compose --renders renders/final/trigger-photos --out renders/final/trigger-pairs
match: refs $(PAIRS) $(TRIGGER_PAIRS)
$(EXTRAS) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/magazine_loaded.glb --out renders/final/loaded --width 1200 --samples $(SAMPLES) --shots mag_standalone,mag_rear
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/magazine_empty.glb --out renders/final/empty --width 1200 --samples $(SAMPLES) --shots mag_standalone,mag_rear
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/case.glb --out renders/final/case --width 1100 --samples $(SAMPLES) --shots case,case_mouth
extra: $(EXTRAS)
$(STRIPS) &: $(EXPORTS) $(RENDER_DEPS) src/strips.py ../common/strips.py src/interface.py
	$(PYTHON) src/strips.py
strips: $(STRIPS)
critique: $(EXPORTS) build/cameras.json
	$(PYTHON) src/critique.py --pass $(PASS)
review: render match strips extra
	$(PYTHON) src/review.py
docs: review
	$(PYTHON) src/review.py --docs
sections: $(EXPORTS) build/sculpt.blend src/sections.py
	$(BP) --python src/sections.py -- --source export/pistol.glb --high build/sculpt.blend --out renders/final/sections
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"
