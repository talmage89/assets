# Relay 9: accepted form/rig; original 4K bake and canonical 2K delivery.
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
WIDTH ?= 1600
SAMPLES ?= 64
SHIP_SIZE := 2048
MODEL := $(addprefix build/,smg.blend smg.glb magazine_loaded.glb magazine_empty.glb cartridge.glb case.glb triangles.json)
PREPARED := build/delivery/finalized.blend $(addprefix build/delivery/,smg-uv.json magazine-uv.json cartridge-uv.json case-uv.json)
MARKS := $(addprefix build/markings/,receiver.png serial.png lower.png headstamp.png)
WEAR_FIELDS := $(addprefix build/markings/,receiver_wear_left.png receiver_wear_right.png receiver-wear-design.json)
BAKED := $(addprefix build/baked/4k/T_Relay9_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_Relay9_,BaseColor.png Normal.png ORM.png)
EXPORTS := $(addprefix export/,smg.glb magazine_loaded.glb magazine_empty.glb cartridge.glb case.glb)
SUBSET_LAYOUTS := $(addprefix build/delivery/detachables/,magazine_loaded/layout.json magazine_empty/layout.json cartridge/layout.json case/layout.json)
comma := ,
FINAL_SHOTS := hero,hero_right,front,side,back,top,receiver,handle,sights,front_sight,lower,aimed,locked,locked_close,port_open,stock,handguard,trigger,scale
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json
EXTRAS := renders/final/loaded/mag_standalone.png renders/final/loaded/mag_lips.png renders/final/empty/mag_standalone.png renders/final/empty/mag_lips.png renders/final/cartridge/cartridge.png renders/final/case/case.png renders/final/case/case_mouth.png
PHOTO_SHOTS := right_photo,left_photo,locked_photo,trigger_photo
PAIRS := $(addprefix renders/final/pairs/,$(addsuffix -pair.jpg,$(subst $(comma), ,$(PHOTO_SHOTS))))
RENDER_DEPS := src/final_render.py src/final_shots.py src/shots.py src/paint_lights.json ../common/paint_review.py ../common/render.py build/render-parameters.txt
.PHONY: all refs model prepare lookdev bake export check check-repo verify render match source-match strips extra review docs sections clean FORCE wear-audit
all: refs export check render match source-match strips extra review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: src/build.py src/clips.py src/interface.py ../common/ammo9_visual.py ../../kit/model.py ../../kit/weapon.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/smg.blend
model: $(MODEL)
$(PREPARED) &: $(MODEL) src/prepare.py ../../kit/finalize.py ../../kit/uv.py
	$(BP) --python src/prepare.py
prepare: $(PREPARED)
$(MARKS) &: src/markings.py ../../kit/fonts.py
	$(PYTHON) src/markings.py
$(WEAR_FIELDS) &: src/paint_masks.py
	$(PYTHON) src/paint_masks.py
build/wear-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/bake-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES) ship=$(SHIP_SIZE)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/delivery/high.blend: $(PREPARED) $(MARKS) $(WEAR_FIELDS) src/build_high.py src/high_ammo.py ../common/ammo9_bake.py src/lookdev.py build/wear-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR)
lookdev: build/delivery/high.blend
$(BAKED) &: build/delivery/high.blend $(PREPARED) src/config.py build/bake-parameters.txt ../../kit/bake.py ../../kit/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high build/delivery/high.blend --out build/baked/4k --asset Relay9 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED) ../../kit/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset Relay9 --size $(SHIP_SIZE) --alpha-mode independent
$(EXPORTS) $(SUBSET_LAYOUTS) &: $(TEXTURES) $(PREPARED) src/config.py src/cartridge_config.py src/case_config.py src/export_paint.py ../../kit/export.py src/export_config.py ../../kit/detachable_textures.py ../../kit/detachable_clusters.py ../../kit/gltf.py
	@mkdir -p export
	$(BP) --python src/export_paint.py -- --source build/delivery/finalized.blend --textures textures --asset Relay9 --config src/export_config.py --out export/smg.glb --report build/delivery/export.json
	$(BP) --python $(KIT)/gltf.py -- --source export/smg.glb --config src/export_config.py
	$(BP) --python src/export_paint.py -- --source build/delivery/finalized.blend --textures textures --asset Relay9 --config src/cartridge_config.py --out export/cartridge.glb --report build/delivery/cartridge-export.json
	$(BP) --python src/export_paint.py -- --source build/delivery/finalized.blend --textures textures --asset Relay9 --config src/case_config.py --out export/case.glb --report build/delivery/case-export.json
export: $(EXPORTS) $(SUBSET_LAYOUTS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: $(MODEL)
	$(BP) --python src/verify.py -- --source build/smg.blend --out build/serialization.json
NEUTRAL_REFS := $(addprefix refs/,left.jpg right.jpg navy2.jpg trigger-ref.jpg daylight.jpg)
$(NEUTRAL_REFS) &: refs/SOURCES.md $(KIT)/fetch_refs.py
	$(PYTHON) $(KIT)/fetch_refs.py refs --only $(notdir $(NEUTRAL_REFS))
build/white-balanced/navy2.png: src/white_balance.py refs/SOURCES.md $(NEUTRAL_REFS)
	$(PYTHON) src/white_balance.py
check: check-repo verify $(EXPORTS) $(SUBSET_LAYOUTS) build/white-balanced/navy2.png
	$(BP) --python src/check.py -- --source build/smg.blend --out build/check.json --motion
	$(BP) --python src/check.py -- --source build/delivery/finalized.blend --out build/delivery/construction.json --motion
	$(BP) --python src/atlas_verify.py
	$(BP) --python src/check.py -- --source build/delivery/imported-parts.blend --out build/delivery/imported-construction.json --motion
	$(BP) --python src/wear_audit.py
	$(PYTHON) src/finish_review.py --layout-only
wear-audit: $(EXPORTS) build/white-balanced/navy2.png
	$(BP) --python src/wear_audit.py
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/smg.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS)
renders/final/eevee/hero.png renders/final/eevee/shots.json &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/smg.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png
build/cameras.json: src/photo_matches.py src/photo_calibration.py src/white_balance.py refs/SOURCES.md
	$(PYTHON) src/photo_calibration.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
$(PAIRS) &: $(EXPORTS) $(RENDER_DEPS) build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/smg.glb --out renders/final/photos --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS) --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/photos --out renders/final/pairs
build/value-loci.json build/value-surfaces.npz &: $(PREPARED) src/value_loci.py
	$(BP) --python src/value_loci.py
match: refs $(PAIRS) build/value-loci.json build/value-surfaces.npz
source-match: build/delivery/high.blend build/cameras.json $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/source-photos --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS) --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/source-photos --out renders/final/source-pairs
renders/final/strips/timing.json: $(EXPORTS) $(RENDER_DEPS) src/final_strips.py src/interface.py ../common/strips.py
	$(PYTHON) src/final_strips.py
strips: renders/final/strips/timing.json
$(EXTRAS) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/magazine_loaded.glb --out renders/final/loaded --width 1100 --samples $(SAMPLES) --shots mag_standalone,mag_lips
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/magazine_empty.glb --out renders/final/empty --width 1100 --samples $(SAMPLES) --shots mag_standalone,mag_lips
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/cartridge.glb --out renders/final/cartridge --width 1100 --samples $(SAMPLES) --shots cartridge
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/case.glb --out renders/final/case --width 1100 --samples $(SAMPLES) --shots case,case_mouth
extra: $(EXTRAS)
review: render match source-match strips extra
	$(PYTHON) src/final_review.py
docs: review
	$(PYTHON) src/final_review.py --docs
sections: $(MODEL)
	$(BP) --python src/sections.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"

RESPONSE := renders/final/finish-response/paint_response.png renders/final/finish-response/shots.json
$(RESPONSE) &: $(EXPORTS) $(RENDER_DEPS) src/response_render.py
	$(KIT)/with_gpu.sh $(BP) --python src/response_render.py -- --source export/smg.glb --out renders/final/finish-response --width 1400 --samples $(SAMPLES) --shots paint_response
review: $(RESPONSE)

.PHONY: wear-2d
wear-2d: $(FINAL_IMAGES) build/value-surfaces.npz
	$(PYTHON) src/wear_2d_review.py

include ../common/gif.mk

# Whole receiver distribution from the shipped GLB, with member-owned photo
# outlines and one physical rig per photo. No reference pixels enter the bake.
.PHONY: paint-review
paint-review: match build/value-surfaces.npz
	$(PYTHON) src/paint_review.py --check
review: paint-review
