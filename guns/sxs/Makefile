# Form round seven: turned/milled head with distance blends; finish/docs held.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../../kit)
REPO := $(abspath ../..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1440
SAMPLES ?= 32
BAKE_SIZE := 4096
SHIP_SIZE := 2048
BAKE_SAMPLES ?= 32
MODEL := build/sxs.blend build/sxs.glb build/shell.glb build/hull.glb
MODEL_DEPS := src/build.py src/head_surface.py src/head_mesh.py src/parameters.py src/clips.py src/interface.py ../common/shell12_visual.py ../common/interface_v1_7.py
PREPARED := build/delivery/finalized.blend build/delivery/high.blend build/delivery/uv.json
BAKED := $(addprefix build/baked/4k/T_Covey26_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json
PROJECTED := $(addprefix build/baked/precise4k/T_Covey26_,BaseColor.png Normal.png ORM.png) build/baked/precise4k/projection-report.json
TEXTURES := $(addprefix textures/T_Covey26_,BaseColor.png Normal.png ORM.png)
RENDER_DEPS := src/shots.py src/render.py ../common/render.py build/render-parameters.txt
SHOTS := hero,side,left,top,front,rake_right,rake_left,open,breech,action,action_left,triggers,trigger_quarter,forend,stock,muzzle,top_controls,lumps,aimed,action_rake_right,action_rake_left,action_rake_top,action_rake_bottom
comma := ,
BEAUTY := $(addprefix renders/checkpoint/beauty/,$(addsuffix .png,$(subst $(comma), ,$(SHOTS)))) renders/checkpoint/beauty/shots.json
PHOTO_SHOTS := right,left,action,action_left,action_top,action_bottom,open,barrel_flats,forend,forend_side,trigger,aimed_reference
.PHONY: all refs model prepare bake export check check-repo verify repeat render review evidence sections match strips ammo native-photos dense-rakes reflections fairness FORCE clean
all: refs export check render review
refs: native-photos
	$(PYTHON) $(KIT)/fetch_refs.py refs
native-photos:
	$(PYTHON) src/fetch_photos.py
$(MODEL) &: $(MODEL_DEPS) ../../kit/model.py ../../kit/weapon.py
	@mkdir -p build $(TMPDIR)
	$(BP) --python src/build.py -- --out build/sxs.blend > build/model.log 2>&1
model: $(MODEL)
$(PREPARED) &: $(MODEL) src/prepare.py src/normal_sources.py src/config.py ../../kit/finalize.py ../../kit/uv.py
	$(BP) --python src/prepare.py > build/prepare.log 2>&1
prepare: $(PREPARED)
build/bake-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES) ship=$(SHIP_SIZE)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(BAKED) &: $(PREPARED) src/config.py src/bake_form.py build/bake-parameters.txt ../../kit/bake.py ../../kit/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake_form.py -- --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES) > build/bake.log 2>&1
bake: $(BAKED)
$(PROJECTED) &: $(BAKED) $(PREPARED) src/normal_projection.py
	$(BP) --python src/normal_projection.py > build/normal-projection.log 2>&1
$(TEXTURES) &: $(PROJECTED) ../../kit/downsample.py src/ship_normal.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/precise4k --out textures --asset Covey26 --size $(SHIP_SIZE)
	$(PYTHON) src/ship_normal.py
export/sxs.glb &: $(TEXTURES) $(PREPARED) src/config.py ../../kit/export.py
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset Covey26 --config src/config.py --out $@ --report build/delivery/export.json > build/export.log 2>&1
export: export/sxs.glb
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: export
	$(BP) --python src/verify.py -- > build/verify.log 2>&1
	$(BP) --python src/check.py -- --source export/sxs.glb --out build/import-check.json > build/import-check.log 2>&1
build/repeat/sxs.blend: $(MODEL_DEPS)
	$(BP) --python src/build.py -- --out $@ > build/repeat-build.log 2>&1
repeat: model build/repeat/sxs.blend
	$(BP) --python src/repeat.py -- --first build/sxs.blend --second build/repeat/sxs.blend --out build/repeat.json > build/repeat.log 2>&1
check: model check-repo verify repeat fairness
	$(BP) --python src/check.py -- --source build/sxs.blend --out build/check.json > build/check.log 2>&1
build/render-parameters.txt: FORCE
	@mkdir -p build
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(BEAUTY) &: export/sxs.glb $(RENDER_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/sxs.glb --out renders/checkpoint/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(SHOTS) > build/render.log 2>&1
render: $(BEAUTY)
evidence: sections match strips ammo dense-rakes reflections
review: render evidence
	$(PYTHON) src/review.py
sections: export
	$(BP) --python src/sections.py -- > build/sections.log 2>&1
	$(BP) --python src/section_curvature.py -- > build/curvature.log 2>&1
	$(PYTHON) src/section_curvature.py --plot
match: verify
	$(BP) --python src/outline_capture.py > build/outline-capture.log 2>&1
	$(PYTHON) src/photo_matches.py
	$(PYTHON) src/photo_solve.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source export/sxs.glb --out renders/checkpoint/photos --camera-file build/cameras.json --shots $(PHOTO_SHOTS) --width $(WIDTH) --samples $(SAMPLES) > build/match.log 2>&1
	$(PYTHON) src/pair_review.py --renders renders/checkpoint/photos --out renders/checkpoint/pairs
	$(BP) --python src/camera_verify.py > build/camera-verify.log 2>&1
strips: export
	$(PYTHON) src/strips.py > build/strips.log 2>&1
	$(BP) --python src/render.py -- --source export/sxs.glb --out renders/checkpoint/opening-wide --width 500 --engine BLENDER_WORKBENCH --strip Open --wide > build/opening-wide.log 2>&1
ammo: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/shell.glb --out renders/checkpoint/shell --shots shell --width 1200 --samples $(SAMPLES) > build/shell-render.log 2>&1
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/hull.glb --out renders/checkpoint/hull --shots hull --width 1200 --samples $(SAMPLES) > build/hull-render.log 2>&1
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','renders','textures','export')]"

# Explicit original-source comparison requested for the new head, kept beside
# the baked-export rakes; never used as a final gun export or its photo pair.
dense-rakes: model
	$(BP) --python src/prepare_high.py > build/dense-prepare.log 2>&1
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source-diagnostic --source build/sculpt.blend --out renders/checkpoint/dense-rakes --width $(WIDTH) --samples $(SAMPLES) --shots action_rake_right,action_rake_left > build/dense-rakes.log 2>&1

# Diagnostic materials only. The delivered GLB's tangent normal remains
# connected; no texture or ordinary inspection constant is changed.
reflections: export dense-rakes
	$(KIT)/with_gpu.sh $(BP) --python src/reflections.py -- --source build/sculpt.blend --out renders/checkpoint/reflections/source --width $(WIDTH) --samples $(SAMPLES) > build/reflections-source.log 2>&1
	$(KIT)/with_gpu.sh $(BP) --python src/reflections.py -- --source export/sxs.glb --out renders/checkpoint/reflections/export --width $(WIDTH) --samples $(SAMPLES) > build/reflections-export.log 2>&1
fairness: model
	$(BP) --python src/fairness_gauges.py -- --source build/sxs.blend --out build/fairness.json > build/fairness.log 2>&1
