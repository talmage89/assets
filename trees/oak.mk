# Species-isolated oak build using the shared botanical delivery tools.
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
WIDTH ?= 1200
SAMPLES ?= 40
PASS ?= oak-source-review
WEAR ?= .35
OAK_DEPS := src/build.py src/growth.py src/oak_growth.py src/oak.py src/maple.py src/species.py src/leaves.py src/oak_leaves.py src/bark.py src/bark_source.py src/oak_bark.py src/leaf_material.py src/wood.py src/wood_uv.py ../kit/botany.py ../kit/model.py
OAK_SHOTS := daylight,crown_up,silhouette,scale,structure,lower_pins,bark,family
.NOTPARALLEL:
.PHONY: all model refs check render match contact FORCE
all: refs docs check
build/oak/parameters.txt: FORCE
	@mkdir -p build/oak $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/oak/lookdev.blend: $(OAK_DEPS) build/oak/parameters.txt
	@mkdir -p build/oak $(TMPDIR)
	$(BP) --python src/build.py -- --species oak --wear $(WEAR) --out $@
build/oak/game-audit.blend: $(OAK_DEPS) build/oak/parameters.txt
	@mkdir -p build/oak $(TMPDIR)
	$(BP) --python src/build.py -- --species oak --quality game --wear $(WEAR) --out $@
model: build/oak/lookdev.blend
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs
build/oak/matched-cameras.json: src/oak_matches.py
	$(PYTHON) $(KIT)/photo_match.py solve --config $< --out $@
build/oak/framed-cameras.json: build/oak/matched-cameras.json src/oak_frames.py
	$(PYTHON) src/oak_frames.py --source $< --out $@
check: build/oak/lookdev.blend build/oak/game-audit.blend build/oak/framed-cameras.json
	$(BP) --python src/check_structure.py -- --species oak --source build/oak/lookdev.blend --out build/oak/structure-check.json
	$(BP) --python $(KIT)/audit.py -- --source build/oak/lookdev.blend --config src/oak_config.py --out build/oak/source-audit.json
	$(BP) --python $(KIT)/audit.py -- --source build/oak/game-audit.blend --config src/oak_config.py --out build/oak/game-audit.json
	$(BP) --python src/oak_profile.py -- --source build/oak/lookdev.blend --out build/oak/crown-profile.json
	$(PYTHON) src/oak_review.py --check-audits
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/oak/framed-cameras.json
	$(PYTHON) $(KIT)/repo_check.py
render: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --species oak --source build/oak/lookdev.blend --maple-source build/lookdev.blend --out renders/$(PASS) --shots $(OAK_SHOTS) --width $(WIDTH) --samples $(SAMPLES)
match: refs model build/oak/framed-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --species oak --source build/oak/lookdev.blend --out renders/$(PASS) --camera-file build/oak/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/oak/framed-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
contact:
	$(PYTHON) src/oak_review.py --renders renders/$(PASS)
	$(PYTHON) src/oak_profile.py --renders renders/$(PASS) --profile build/oak/crown-profile.json

# Final delivery uses the same shared finalize/bake/filter/export/audit tools
# as maple, with isolated files so selecting a species never replaces another.
SHIP_SIZE ?= 2048
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 32
FINAL_WIDTH ?= 1600
FINAL_SAMPLES ?= 72
OAK_FINAL_SHOTS := hero,front,side,back,top,branchlet,cluster_3m,bark,bark_raking,lower_pins,crown_up,scale,root_flare,family
.PHONY: finalize bake export verify final-render docs check-delivery
build/oak/uv-source.blend: build/oak/game-audit.blend src/oak_uv.py
	$(BP) --python src/oak_uv.py -- --source $< --out $@
build/oak/finalized.blend: build/oak/uv-source.blend src/oak_config.py build/oak/delivery-parameters.txt
	$(BP) --python $(KIT)/finalize.py -- --source $< --config src/oak_config.py --out $@ --report build/oak/uv-report.json --size $(SHIP_SIZE) --target-density 850 --margin .0015
finalize: build/oak/finalized.blend
build/oak/baked.stamp: build/oak/finalized.blend build/oak/lookdev.blend src/leaves.py src/oak_leaves.py build/oak/bake-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/bake.py -- --low build/oak/finalized.blend --high build/oak/lookdev.blend --out textures/oak/bake --asset PinOak --config src/oak_config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	$(PYTHON) src/leaves.py --species oak --out textures/oak/bake --composite build/oak/leaf-source
	@touch $@
bake: build/oak/baked.stamp
build/oak/textures.stamp: build/oak/baked.stamp
	$(PYTHON) $(KIT)/downsample.py --source textures/oak/bake --out textures/oak/ship --asset PinOak --size $(SHIP_SIZE)
	@touch $@
export/PinOak.glb: build/oak/finalized.blend build/oak/textures.stamp src/oak_config.py
	$(BP) --python $(KIT)/export.py -- --source build/oak/finalized.blend --textures textures/oak/ship --asset PinOak --out $@ --report build/oak/export-report.json --config src/oak_config.py
export: export/PinOak.glb
verify: export/PinOak.glb
	$(BP) --python $(KIT)/verify.py -- --source $< --expected build/oak/export-report.json --config src/oak_config.py --out build/oak/delivery-check.json --size $(SHIP_SIZE)
	$(BP) --python src/check_delivery.py -- --source build/oak/finalized.blend --glb $< --out build/oak/botanical-delivery-check.json
	$(PYTHON) -c "import json; r=json.load(open('textures/oak/bake/bake-report.json')); assert r['BaseColor']['alpha_missed_interior_texels']==0 and r['BaseColor']['black_interior_texels']==0, r['BaseColor']"
check-delivery: verify
renders/oak-final/.stamp: export/PinOak.glb build/oak/framed-cameras.json src/render.py src/oak_views.py src/leaf_material.py export/RedMaple.glb build/oak/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --species oak --stage final --source $< --maple-source export/RedMaple.glb --out renders/oak-final --shots $(OAK_FINAL_SHOTS) --width $(FINAL_WIDTH) --samples $(FINAL_SAMPLES)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --species oak --stage final --source $< --out renders/oak-final --camera-file build/oak/framed-cameras.json --width $(FINAL_WIDTH) --samples $(FINAL_SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/oak/framed-cameras.json --renders renders/oak-final --out renders/oak-final
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --species oak --stage final --source $< --out renders/oak-final-eevee --shots hero --engine BLENDER_EEVEE --width $(FINAL_WIDTH) --samples $(FINAL_SAMPLES)

	@touch $@
final-render: renders/oak-final/.stamp
build/oak/studio-parameters.txt: FORCE
	@mkdir -p build/oak
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(FINAL_WIDTH) samples=$(FINAL_SAMPLES) shots=$(OAK_FINAL_SHOTS)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
docs: final-render src/oak_final_review.py src/oak_evidence.py
	$(BP) --python src/oak_final_review.py -- --renders renders/oak-final --docs
check: verify
.PHONY: check-bark
check-bark: final-render src/oak_evidence.py src/oak_final_review.py
	$(BP) --python src/oak_final_review.py -- --renders renders/oak-final
check: check-bark
.PHONY: clean
clean:
	$(PYTHON) -c "import shutil; from pathlib import Path; [shutil.rmtree(p,ignore_errors=True) for p in ('build/oak','textures/oak','renders/oak-final','renders/oak-final-eevee')]; Path('export/PinOak.glb').unlink(missing_ok=True)"

export/RedMaple.glb:
	$(MAKE) SPECIES=maple export
build/lookdev.blend:
	$(MAKE) SPECIES=maple model
build/oak/delivery-parameters.txt: FORCE
	@mkdir -p build/oak
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='ship=$(SHIP_SIZE)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/oak/bake-parameters.txt: FORCE
	@mkdir -p build/oak
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
