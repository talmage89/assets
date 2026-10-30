# Bracken L20: original dense source -> kit atlas/bake/export -> GLB finals.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../../kit)
REPO := $(abspath ../..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WEAR ?= 1
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 32
SHIP_SIZE := 2048
WIDTH ?= 1600
SAMPLES ?= 64
MODEL := $(addprefix build/,lever.blend lever.glb sculpt.blend cartridge.glb case.glb interface.json triangles.json)
PREPARED := build/delivery/finalized.blend $(addprefix build/delivery/,lever-uv.json cartridge-uv.json case-uv.json)
BAKED := $(addprefix build/baked/4k/T_BrackenL20_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_BrackenL20_,BaseColor.png Normal.png ORM.png)
EXPORTS := export/lever.glb export/cartridge.glb export/case.glb
SUBSET_LAYOUTS := $(addprefix build/delivery/detachables/,cartridge/layout.json case/layout.json)
FINAL_SHOTS := hero,hero_left,right,left,front,back,top,receiver,receiver_left,wrist,wrist_raking,forend,sights,sight_blade,front_sight,stock,butt_plate,open,lever_open,aimed,scale,muzzle
PHOTO_SHOTS := right_photo,left_photo,open_photo,trigger_right,trigger_quarter,hammer_photo,lever_rest_photo,used_photo,sight_photo
comma := ,
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json
RENDER_DEPS := src/final_render.py src/final_shots.py src/shots.py ../common/render.py build/render-parameters.txt
PHOTO_DEPS := build/cameras.json src/white_balance.py src/photo_matches.py
PAIRS := $(addprefix renders/final/pairs/,$(addsuffix -pair.jpg,$(subst $(comma), ,$(PHOTO_SHOTS))))
.PHONY: all refs model prepare lookdev bake export check check-repo verify check-atlas repeat render match source-match strips extra review docs clean FORCE checkpoint
all: refs export feed-audit check form-review render match source-match strips feed-strips extra wear-review look-review review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: $(addprefix src/,build.py clips.py dimensions.py forms.py geometry.py mechanism.py interface.py feed.py) ../common/feed_sampling.py ../common/ammo_3030.py ../common/interface_v1_5.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/lever.blend
model: $(MODEL)
$(PREPARED) &: $(MODEL) src/prepare.py $(KIT)/finalize.py $(KIT)/uv.py
	$(BP) --python src/prepare.py
prepare: $(PREPARED)
build/wear-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/bake-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES) ship=$(SHIP_SIZE)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/markings/receiver.png build/markings/barrel.png build/markings/serial.png &: src/markings.py $(KIT)/fonts.py
	$(PYTHON) src/markings.py
build/delivery/high.blend: $(PREPARED) src/build_high.py src/lookdev.py build/markings/receiver.png build/markings/barrel.png build/markings/serial.png build/wear-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR)
lookdev: build/delivery/high.blend
$(BAKED) &: build/delivery/high.blend $(PREPARED) src/config.py build/bake-parameters.txt $(KIT)/bake.py $(KIT)/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high build/delivery/high.blend --out build/baked/4k --asset BrackenL20 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED) $(KIT)/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset BrackenL20 --size $(SHIP_SIZE)
$(EXPORTS) $(SUBSET_LAYOUTS) &: $(TEXTURES) $(PREPARED) src/config.py src/cartridge_config.py src/case_config.py $(KIT)/export.py ../../kit/detachable_textures.py ../../kit/detachable_clusters.py ../../kit/gltf.py src/export_config.py
	@mkdir -p export
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset BrackenL20 --config src/export_config.py --out export/lever.glb --report build/delivery/export.json
	$(BP) --python ../common/feed_sampling.py -- --source build/delivery/finalized.blend --out export/lever.glb --bones Lever,Link,Carrier,CarrierGuide,CarrierRound,FiredGuide,FiredCase,ChamberRound,Follower,TubeFeedGuide,Tube1,Tube2,Tube3,Tube4,Tube5,Tube6
	$(BP) --python $(KIT)/gltf.py -- --source export/lever.glb --config src/export_config.py
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset BrackenL20 --config src/cartridge_config.py --out export/cartridge.glb --report build/delivery/cartridge-export.json
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset BrackenL20 --config src/case_config.py --out export/case.glb --report build/delivery/case-export.json
export: $(EXPORTS) $(SUBSET_LAYOUTS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: $(MODEL)
	$(BP) --python src/verify.py --
check-atlas: $(EXPORTS) $(SUBSET_LAYOUTS)
	$(BP) --python src/check.py -- --source build/delivery/finalized.blend --out build/delivery/construction.json --motion
	$(BP) --python src/atlas_verify.py -- --stage serialization
	$(BP) --python src/atlas_verify.py -- --stage construction
check: model check-repo verify check-atlas
	$(BP) --python src/check.py -- --motion
	$(BP) --python src/topology.py
repeat: model
	$(BP) --python src/build.py -- --out build/repeat/lever.blend
	$(BP) --python src/repeat.py --
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/lever.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS)
renders/final/eevee/hero.png renders/final/eevee/shots.json &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/lever.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png
build/cameras.json: src/photo_matches.py src/white_balance.py refs/SOURCES.md
	$(PYTHON) src/white_balance.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/photo_matches.py --out $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
	$(PYTHON) src/reference_measurements.py
$(PAIRS) &: $(EXPORTS) $(RENDER_DEPS) $(PHOTO_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/lever.glb --out renders/final/photos --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS) --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/photos --out renders/final/pairs
match: refs $(PAIRS)
source-match: build/delivery/high.blend $(RENDER_DEPS) $(PHOTO_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/source-photos --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS) --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/source-photos --out renders/final/source-pairs
strips: $(EXPORTS) $(RENDER_DEPS)
	$(PYTHON) src/final_strips.py
.PHONY: feed-strips feed-before-strips feed-audit
feed-strips: $(EXPORTS) src/cycle_views.py src/feed_strips.py ../common/feed_views.py ../common/feed_strips.py
	$(PYTHON) src/feed_strips.py
feed-before-strips:
	$(PYTHON) src/feed_strips.py --before
feed-audit: model
	$(BP) --python src/feed_audit.py
extra: $(EXPORTS) $(RENDER_DEPS) src/ammo_render.py
	$(KIT)/with_gpu.sh $(BP) --python src/ammo_render.py -- --source export/cartridge.glb --out renders/final/cartridge --width 1100 --samples $(SAMPLES) --shots cartridge,headstamp
	$(KIT)/with_gpu.sh $(BP) --python src/ammo_render.py -- --source export/case.glb --out renders/final/case --width 1100 --samples $(SAMPLES) --shots case,mouth,headstamp
review: render match extra
	$(PYTHON) src/final_review.py
docs: review
	$(PYTHON) src/final_review.py --docs
checkpoint:
	$(MAKE) -f checkpoint.mk
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"

.PHONY: form-review wear-review
renders/form3/form-fixes.jpg renders/form3/lever-stroke.jpg build/final-form-measurements.json &: $(MODEL) build/cameras.json src/form_review.py src/shots.py
	$(PYTHON) src/form_review.py
form-review: renders/form3/form-fixes.jpg renders/form3/lever-stroke.jpg build/final-form-measurements.json
build/review/contact-mask.npy: $(EXPORTS) build/delivery/high.blend src/wear_mask.py
	$(KIT)/with_gpu.sh $(BP) --python src/wear_mask.py
build/review/wear-grid.npz: $(EXPORTS) $(PREPARED) src/wear_sample.py build/review/contact-mask.npy
	$(BP) --python src/wear_sample.py
renders/final/pairs/wear-2d-pair.jpg renders/final/pairs/wear-2d-values.json &: $(FINAL_IMAGES) build/review/wear-grid.npz src/wear_review.py
	$(PYTHON) src/wear_review.py
wear-review: renders/final/pairs/wear-2d-pair.jpg renders/final/pairs/wear-2d-values.json

.PHONY: look-review
look-review: render match wear-details src/plate_review.py
	$(PYTHON) src/plate_review.py $(if $(SHOTGUN_RENDERS),--shotgun-renders $(SHOTGUN_RENDERS),)

.PHONY: wear-details
renders/final/wear-details/forend_band.png renders/final/wear-details/muzzle_band.png renders/final/wear-details/shots.json &: $(EXPORTS) src/wear_render.py $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/wear_render.py -- --source export/lever.glb --out renders/final/wear-details --width $(WIDTH) --samples $(SAMPLES)
wear-details: renders/final/wear-details/forend_band.png renders/final/wear-details/muzzle_band.png renders/final/wear-details/shots.json
extra: wear-details

include ../common/gif.mk
