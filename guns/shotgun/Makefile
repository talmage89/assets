# PD Hearth 12: accepted geometry, original 4K source bake, 2K animated delivery.
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
MODEL := build/shotgun.blend build/shotgun.glb build/shell.glb build/hull.glb build/triangles.json
PREPARED := build/delivery/finalized.blend $(addprefix build/delivery/,shotgun-uv.json shell-uv.json hull-uv.json)
MARKS := $(addprefix build/markings/,receiver-left.png receiver-right.png headstamp.png)
BAKED := $(addprefix build/baked/4k/T_Hearth12_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_Hearth12_,BaseColor.png Normal.png ORM.png)
EXPORTS := export/shotgun.glb export/shell.glb export/hull.glb
SUBSET_LAYOUTS := $(addprefix build/delivery/detachables/,shell/layout.json hull/layout.json)
comma := ,
FINAL_SHOTS := hero,hero_left,front,side,back,top,receiver,wrist,forend,aimed,open,scale,muzzle,stock,guard,underside,pad,aimed_socket,muzzle_under,trigger_right,trigger_quarter,trigger_pulled
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json
EXTRAS := renders/final/shell/shell.png renders/final/shell/shell_crimp.png renders/final/shell/shots.json renders/final/hull/hull.png renders/final/hull/hull_primer.png renders/final/hull/shots.json
PAIRS := $(foreach v,right left open used wood,renders/final/pairs/$(v)_photo-pair.jpg renders/final/pairs/$(v)_photo-calibration.jpg)
WEAR_PAIR := renders/final/pairs/hero-wear_photo-pair.jpg renders/final/pairs/hero-wear-values.json
CLIPS := Idle Fire FireLast Reload ReloadEmpty Inspect IdleEmpty IdleOpen IdleTube0 IdleTube1 IdleTube2 IdleTube3 Fire1 Fire2 Fire3 Reload1 Reload2 Reload3
STRIPS := $(addprefix renders/final/strips/,$(addsuffix .jpg,$(CLIPS))) $(addprefix renders/final/strips/,$(addsuffix .webp,$(CLIPS))) renders/final/strips/timing.json
RENDER_DEPS := src/render.py src/shots.py src/final_shots.py ../common/render.py build/render-parameters.txt
.PHONY: all refs model prepare lookdev bake export atlas check check-repo verify check-atlas check-repeat render match source-match strips shells extra orthos atlas-views review docs critique wear-audit sections clean FORCE
all: refs export feed-audit check render match strips feed-strips extra source-match review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: src/build.py src/clips.py src/feed.py src/interface.py ../common/feed_sampling.py ../../kit/model.py ../../kit/weapon.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/shotgun.blend
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
build/delivery/high.blend: $(PREPARED) $(MARKS) src/build_high.py src/lookdev.py build/wear-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR)
lookdev: build/delivery/high.blend
$(BAKED) &: build/delivery/high.blend $(PREPARED) src/config.py build/bake-parameters.txt ../../kit/bake.py ../../kit/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high build/delivery/high.blend --out build/baked/4k --asset Hearth12 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED) ../../kit/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset Hearth12 --size $(SHIP_SIZE)
$(EXPORTS) $(SUBSET_LAYOUTS) &: $(TEXTURES) $(PREPARED) src/config.py src/shell_config.py src/hull_config.py ../../kit/export.py ../../kit/weapon.py ../../kit/detachable_textures.py ../../kit/detachable_clusters.py
	@mkdir -p export
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset Hearth12 --config src/config.py --out export/shotgun.glb --report build/delivery/export.json
	$(BP) --python ../common/feed_sampling.py -- --source build/delivery/finalized.blend --out export/shotgun.glb --bones Carrier,CarrierGuide,CarrierShell,ChamberShell,FiredGuide,FiredHull,ShellGuide,InsertShell,Follower,TubeFeedGuide,Tube1,Tube2,Tube3,Tube4
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset Hearth12 --config src/shell_config.py --out export/shell.glb --report build/delivery/shell-export.json
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset Hearth12 --config src/hull_config.py --out export/hull.glb --report build/delivery/hull-export.json
export: $(EXPORTS) $(SUBSET_LAYOUTS) src/rounding_config.py ../../kit/gltf.py
	$(BP) --python $(KIT)/gltf.py -- --source export/shotgun.glb --config src/rounding_config.py
atlas: $(EXPORTS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: $(MODEL)
	$(BP) --python src/verify.py -- --source build/shotgun.blend --out build/serialization.json
check-repeat: $(MODEL)
	$(BP) --python src/build.py -- --out build/repeat/shotgun.blend
	$(BP) --python src/repeat.py -- --reference build/shotgun.glb --repeat build/repeat/shotgun.glb --out build/repeat.json
check-atlas: export $(EXPORTS) $(SUBSET_LAYOUTS)
	$(BP) --python src/check.py -- --source build/delivery/finalized.blend --out build/delivery/construction.json --motion
	$(BP) --python src/atlas_verify.py
	$(BP) --python src/surface_audit.py
check: check-repo verify check-atlas check-repeat
	$(BP) --python src/check.py -- --source build/shotgun.blend --out build/check.json --motion
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/shotgun.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS)
renders/final/eevee/hero.png renders/final/eevee/shots.json &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/shotgun.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png renders/final/eevee/shots.json
orthos: render
atlas-views: render match
build/cameras.json: src/photo_matches.py refs/SOURCES.md
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
$(PAIRS) &: $(EXPORTS) $(RENDER_DEPS) src/photo_matches.py build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/shotgun.glb --out renders/final/photos --width $(WIDTH) --samples $(SAMPLES) --shots right_photo,left_photo,open_photo,used_photo,wood_photo --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/photos --out renders/final/pairs
$(WEAR_PAIR) &: $(FINAL_IMAGES) src/wear_review.py src/value_review.py refs/SOURCES.md
	$(PYTHON) src/wear_review.py
TRIGGER_PAIRS := $(foreach v,right quarter,renders/final/trigger-pairs/trigger_$(v)_photo-pair.jpg)
$(TRIGGER_PAIRS) &: $(EXPORTS) src/trigger_render.py src/trigger_matches.py ../common/trigger_review.py $(RENDER_DEPS) refs/SOURCES.md
	$(KIT)/with_gpu.sh $(BP) --python src/trigger_render.py -- --source export/shotgun.glb --out renders/final/trigger-photos --width 1100 --samples $(SAMPLES) --shots trigger_right_photo,trigger_quarter_photo
	$(PYTHON) src/trigger_render.py --compose --renders renders/final/trigger-photos --out renders/final/trigger-pairs
match: refs $(PAIRS) $(WEAR_PAIR) $(TRIGGER_PAIRS)
source-match: build/delivery/high.blend build/cameras.json $(RENDER_DEPS) src/source_render.py
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/source-photos --width $(WIDTH) --samples $(SAMPLES) --shots right_photo,left_photo,open_photo,used_photo,wood_photo --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/source-photos --out renders/final/source-pairs
$(EXTRAS) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/shell.glb --out renders/final/shell --width 1100 --samples $(SAMPLES) --shots shell,shell_crimp
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/hull.glb --out renders/final/hull --width 1100 --samples $(SAMPLES) --shots hull,hull_primer
extra shells: $(EXTRAS)
$(STRIPS) &: $(EXPORTS) $(RENDER_DEPS) src/strips.py src/interface.py ../common/strips.py
	$(PYTHON) src/strips.py
strips: $(STRIPS)
.PHONY: feed-strips feed-before-strips feed-audit
feed-strips: $(EXPORTS) src/cycle_views.py src/feed_strips.py ../common/feed_views.py ../common/feed_strips.py
	$(PYTHON) src/feed_strips.py
feed-before-strips:
	$(PYTHON) src/feed_strips.py --before
feed-audit: model
	$(BP) --python src/feed_audit.py
critique: $(EXPORTS) build/cameras.json
	$(PYTHON) src/critique.py --pass $(PASS)
wear-audit: $(EXPORTS) src/wear_mask.py
	$(KIT)/with_gpu.sh $(BP) --python src/wear_mask.py -- --out build/review/wear-final
review: render match strips extra
	$(PYTHON) src/final_review.py
docs: review
	$(PYTHON) src/final_review.py --docs
sections: $(MODEL)
	$(BP) --python src/sections.py
	$(PYTHON) src/section_sheet.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"
