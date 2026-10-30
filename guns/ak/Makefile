# Original 4K bake, canonical 2K atlas; accepted 1.6 rig and clip schedules.
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
MODEL := $(addprefix build/,ak.blend ak.glb magazine_loaded.glb magazine_empty.glb cartridge.glb case.glb triangles.json)
PREPARED := build/delivery/finalized.blend $(addprefix build/delivery/,ak-uv.json magazine-uv.json cartridge-uv.json case-uv.json)
MARKS := $(addprefix build/markings/,receiver.png headstamp.png leaf.png)
BAKED := $(addprefix build/baked/4k/T_Rill39_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
TEXTURES := $(addprefix textures/T_Rill39_,BaseColor.png Normal.png ORM.png)
EXPORTS := $(addprefix export/,ak.glb magazine_loaded.glb magazine_empty.glb cartridge.glb case.glb)
SUBSET_LAYOUTS := $(addprefix build/delivery/detachables/,magazine_loaded/layout.json magazine_empty/layout.json cartridge/layout.json case/layout.json)
comma := ,
FINAL_SHOTS := hero,hero_right,front,side,back,top,receiver,cover_rear,controls,rear_sight,rear_ortho_side,front_sight,gas_muzzle,gas_ortho_side,retainer,retainer_side,wood,grip_stock,grip_detail,trigger,open,aimed,magazine,scale
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json
PHOTO_SHOTS := right_photo,left_photo,receiver_photo,trigger_photo,trigger_sharp,rear_sight_side,rear_sight_photo,rear_sight_sharp,front_sight_photo,front_sight_behind,front_sight_installed,gas_block_photo,grip_photo,trigger_guard,topcover_side,topcover_top,topcover_sharp,selector_photo,used_photo,retainer_photo
PAIRS := $(addprefix renders/final/pairs/,$(addsuffix -pair.jpg,$(subst $(comma), ,$(PHOTO_SHOTS))))
RENDER_DEPS := src/final_render.py src/final_shots.py src/shots.py src/paint_lights.json ../common/paint_review.py src/delivery.py ../common/render.py build/render-parameters.txt
.PHONY: all refs model prepare lookdev bake export check check-repo check-bake-identity verify render match source-match strips extra review docs sections clean FORCE
all: refs export check render match source-match strips extra raw-audit review docs
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
$(MODEL) &: src/build.py src/geometry.py src/form_normals.py src/clips.py src/interface.py ../common/ammo762_visual.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --preview --out build/ak.blend
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
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high build/delivery/high.blend --out build/baked/4k --asset Rill39 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(BAKED)
$(TEXTURES) &: $(BAKED) ../../kit/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/4k --out textures --asset Rill39 --size $(SHIP_SIZE) --alpha-mode independent
$(EXPORTS) $(SUBSET_LAYOUTS) &: $(TEXTURES) $(PREPARED) src/config.py src/export_config.py src/cartridge_config.py src/case_config.py src/export_finish.py ../../kit/export.py ../../kit/detachable_textures.py ../../kit/detachable_clusters.py ../../kit/gltf.py
	@mkdir -p export
	$(BP) --python src/export_finish.py -- --source build/delivery/finalized.blend --textures textures --asset Rill39 --config src/export_config.py --out export/ak.glb --report build/delivery/export.json
	$(BP) --python $(KIT)/gltf.py -- --source export/ak.glb --config src/export_config.py
	$(BP) --python src/export_finish.py -- --source build/delivery/finalized.blend --textures textures --asset Rill39 --config src/cartridge_config.py --out export/cartridge.glb --report build/delivery/cartridge-export.json
	$(BP) --python src/export_finish.py -- --source build/delivery/finalized.blend --textures textures --asset Rill39 --config src/case_config.py --out export/case.glb --report build/delivery/case-export.json
export: $(EXPORTS) $(SUBSET_LAYOUTS)
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: $(MODEL)
	$(BP) --python src/verify.py -- --source build/ak.blend --out build/serialization.json
check-bake-identity:
	$(PYTHON) -m unittest discover -s src -p test_bake_identity.py
check: check-repo check-bake-identity verify $(EXPORTS) $(SUBSET_LAYOUTS)
	$(PYTHON) src/texture_preservation.py
	$(BP) --python src/preserve_look.py
	$(BP) --python src/check.py -- --source build/ak.blend --out build/check.json --motion
	$(BP) --python src/check.py -- --source build/delivery/finalized.blend --out build/delivery/construction.json --motion
	$(BP) --python src/atlas_verify.py
	$(BP) --python src/check.py -- --source build/delivery/imported-parts.blend --out build/delivery/imported-construction.json --motion
	$(BP) --python src/retainer_fit.py
$(FINAL_IMAGES) &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/ak.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS)
renders/final/eevee/hero.png renders/final/eevee/shots.json &: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/ak.glb --out renders/final/eevee --engine BLENDER_EEVEE --width $(WIDTH) --samples 64 --shots hero
render: $(FINAL_IMAGES) renders/final/eevee/hero.png
build/cameras.json: src/calibrate.py src/photo_matches.py src/reference.py refs/SOURCES.md
	$(PYTHON) src/reference.py
	$(PYTHON) src/calibrate.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
$(PAIRS) &: $(EXPORTS) $(RENDER_DEPS) build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/ak.glb --out renders/final/photos --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS) --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/photos --out renders/final/pairs
match: refs $(PAIRS)
source-match: build/delivery/high.blend build/cameras.json $(RENDER_DEPS) src/source_render.py
	$(KIT)/with_gpu.sh $(BP) --python src/source_render.py -- --source build/delivery/high.blend --out renders/final/source-photos --width $(WIDTH) --samples $(SAMPLES) --shots $(PHOTO_SHOTS) --camera-file build/cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/cameras.json --renders renders/final/source-photos --out renders/final/source-pairs
renders/final/strips/timing.json: $(EXPORTS) $(RENDER_DEPS) src/final_strips.py src/interface.py ../common/strips.py
	$(PYTHON) src/final_strips.py
strips: renders/final/strips/timing.json
extra: $(EXPORTS) $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/magazine_loaded.glb --out renders/final/loaded --width 1100 --samples $(SAMPLES) --shots mag_standalone,mag_lips
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/magazine_empty.glb --out renders/final/empty --width 1100 --samples $(SAMPLES) --shots mag_standalone,mag_lips
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/cartridge.glb --out renders/final/cartridge --width 1100 --samples $(SAMPLES) --shots cartridge
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/case.glb --out renders/final/case --width 1100 --samples $(SAMPLES) --shots case,case_mouth
review: render match source-match strips extra
	$(PYTHON) src/final_review.py
docs: review
	$(PYTHON) src/final_review.py --docs
sections: $(MODEL)
	$(BP) --python src/sections.py
	$(PYTHON) src/reference.py
	$(PYTHON) src/form_observations.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders')]"

build/delivery/imported-parts.blend: $(EXPORTS) src/atlas_verify.py src/delivery.py
	$(BP) --python src/atlas_verify.py
build/value-geometry.npz: build/delivery/imported-parts.blend src/value_geometry.py
	$(BP) --python src/value_geometry.py
renders/final/precedent/smg_hero.png: ../smg/export/smg.glb $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source ../smg/export/smg.glb --out renders/final/precedent --width $(WIDTH) --samples $(SAMPLES) --shots smg_hero
.PHONY: look-review
look-review: render match source-match build/value-geometry.npz
	$(PYTHON) src/look_review.py
	$(PYTHON) src/furniture_review.py
	$(PYTHON) src/wood_scales.py
	$(PYTHON) src/wood_edges.py
review: look-review

# The asset rebuild is independent of other guns. When the accepted reference
# export is available, this optional comparison writes only into this asset.
.PHONY: precedent
precedent: renders/final/precedent/smg_hero.png

.PHONY: raw-audit
raw-audit: render
	cp export/ak.glb build/ak_raw.glb
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source build/ak_raw.glb --out renders/final/raw-check --width $(WIDTH) --samples $(SAMPLES) --shots hero,grip_detail,gas_muzzle,rear_sight
	$(PYTHON) src/raw_review.py

# A complete independent bake/export, changing only metal abrasion. This is
# comparison evidence; none of its images enter the shipped atlas or GLBs.
build/metal-control/high.blend: $(PREPARED) $(MARKS) src/build_high.py src/lookdev.py build/wear-parameters.txt
	$(BP) --python src/build_high.py -- --wear $(WEAR) --metal-wear 0 --out $@
build/metal-control/baked/bake-report.json: build/metal-control/high.blend $(PREPARED) src/config.py build/bake-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/delivery/finalized.blend --high $< --out build/metal-control/baked --asset Rill39 --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
build/metal-control/export/ak.glb: build/metal-control/baked/bake-report.json src/export_finish.py
	$(PYTHON) $(KIT)/downsample.py --source build/metal-control/baked --out build/metal-control/textures --asset Rill39 --size $(SHIP_SIZE) --alpha-mode independent
	$(BP) --python src/export_finish.py -- --source build/delivery/finalized.blend --textures build/metal-control/textures --asset Rill39 --config src/config.py --out $@ --report build/metal-control/export.json
renders/final/metal-control/hero.png: build/metal-control/export/ak.glb $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source $< --out renders/final/metal-control --width $(WIDTH) --samples $(SAMPLES) --shots hero
.PHONY: metal-control
metal-control: render renders/final/metal-control/hero.png build/value-geometry.npz src/metal_difference.py
	$(PYTHON) src/metal_difference.py
review: metal-control

include ../common/gif.mk

# Whole receiver distribution from the shipped GLB, with member-owned photo
# outlines and one physical rig per photo. No reference pixels enter the bake.
.PHONY: paint-review
paint-review: match build/value-geometry.npz
	$(PYTHON) src/paint_review.py --check
review: paint-review
