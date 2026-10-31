# Covey 26: accepted form, baked field finishes and final presentation.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../../kit)
REPO := $(abspath ../..)
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 4000
SAMPLES ?= 48
BAKE_SIZE := 4096
SHIP_SIZE := 2048
BAKE_SAMPLES ?= 32
MODEL := build/sxs.blend build/sxs.glb build/shell.glb build/hull.glb
MODEL_DEPS := src/build.py src/head_surface.py src/head_mesh.py src/parameters.py src/clips.py src/interface.py ../common/shell12_visual.py ../common/interface_v1_7.py
PREPARED := build/delivery/finalized.blend build/delivery/dense.blend build/delivery/uv.json
BAKED := $(addprefix build/baked/4k/T_Covey26_,BaseColor.png Normal.png ORM.png) build/baked/4k/bake-report.json build/baked/4k/projection-owner.png
PROJECTED := $(addprefix build/baked/precise4k/T_Covey26_,BaseColor.png Normal.png ORM.png) build/baked/precise4k/projection-report.json
TEXTURES := $(addprefix textures/T_Covey26_,BaseColor.png Normal.png ORM.png) textures/texture-report.json
RENDER_DEPS := src/shots.py src/render.py ../common/render.py build/render-parameters.txt
SHOTS := hero,side,left,top,front,rake_right,rake_left,open,breech,action,action_left,triggers,trigger_quarter,forend,stock,muzzle,top_controls,lumps,aimed,action_rake_right,action_rake_left,action_rake_top,action_rake_bottom
comma := ,
BEAUTY := $(addprefix renders/checkpoint/beauty/,$(addsuffix .png,$(subst $(comma), ,$(SHOTS)))) renders/checkpoint/beauty/shots.json
PHOTO_SHOTS := right,left,action,action_left,action_top,action_bottom,open,barrel_flats,forend,forend_side,trigger,aimed_reference
.PHONY: all refs model prepare bake export check check-repo verify repeat render review evidence sections match strips ammo native-photos dense-rakes reflections fairness FORCE clean
all: refs export check final-render look-pairs source-review wear-review wear-detail family-review final-review
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
build/markings/headstamp.png: src/markings.py ../../kit/fonts.py
	$(PYTHON) src/markings.py
build/delivery/high.blend: $(PREPARED) src/lookdev.py src/build_high.py build/markings/headstamp.png
	$(BP) --python src/build_high.py > build/high.log 2>&1
$(BAKED) &: build/delivery/high.blend $(PREPARED) src/config.py src/bake_form.py build/bake-parameters.txt ../../kit/bake.py ../../kit/bake_groups.py
	$(KIT)/with_gpu.sh $(BP) --python src/bake_form.py -- --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES) > build/bake.log 2>&1
bake: $(BAKED)
$(PROJECTED) &: $(BAKED) $(PREPARED) src/normal_projection.py
	$(BP) --python src/normal_projection.py > build/normal-projection.log 2>&1
$(TEXTURES) &: $(PROJECTED) ../../kit/downsample.py src/ship_normal.py
	$(PYTHON) $(KIT)/downsample.py --source build/baked/precise4k --out textures --asset Covey26 --size $(SHIP_SIZE) --alpha-mode independent
	$(PYTHON) src/ship_normal.py
export/sxs.glb export/shell.glb export/hull.glb &: $(TEXTURES) $(PREPARED) src/export_config.py src/config.py ../../kit/export.py ../../kit/detachable_textures.py ../../kit/detachable_verify.py ../../kit/detachable_clusters.py
	$(BP) --python $(KIT)/export.py -- --source build/delivery/finalized.blend --textures textures --asset Covey26 --config src/export_config.py --out export/sxs.glb --report build/delivery/export.json > build/export.log 2>&1
export: export/sxs.glb export/shell.glb export/hull.glb
check-repo:
	$(PYTHON) $(KIT)/repo_check.py
verify: export
	$(BP) --python src/delivery_audit.py > build/detachable-proof.log 2>&1
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
form-render: $(BEAUTY)
evidence: sections match strips ammo dense-rakes reflections
review: form-render evidence
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

# Final evidence is imported from the baked GLB; the source comparisons are
# labeled diagnostics. Historical form evidence remains available explicitly.
FINAL_SHOTS := hero,hero_left,side,left,front,back,top,shooter_three_quarter,aimed,open,breech,open_side,action,wrist,forend,stock,muzzle,top_controls,triggers,scale
FINAL_IMAGES := $(addprefix renders/final/beauty/,$(addsuffix .png,$(subst $(comma), ,$(FINAL_SHOTS)))) renders/final/beauty/shots.json
FINAL_DEPS := src/final_shots.py src/final_render.py ../common/render.py build/render-parameters.txt
LOOK_SHOTS := look_side,look_macro,look_muzzle,look_safety,look_deep_blue
LOOK_IMAGES := $(addprefix renders/final/photos/,$(addsuffix .png,$(subst $(comma), ,$(LOOK_SHOTS)))) renders/final/photos/shots.json
.PHONY: final-render look-pairs wear-review family-review final-review final-masks render
$(FINAL_IMAGES) &: export/sxs.glb $(FINAL_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/sxs.glb --out renders/final/beauty --width $(WIDTH) --samples $(SAMPLES) --shots $(FINAL_SHOTS) > build/final-render.log 2>&1
renders/final/eevee/hero.png renders/final/eevee/shots.json &: export/sxs.glb $(FINAL_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/sxs.glb --out renders/final/eevee --width $(WIDTH) --samples 32 --engine BLENDER_EEVEE --shots hero > build/eevee.log 2>&1
renders/final/shell/shell.png renders/final/shell/shots.json &: export/shell.glb $(FINAL_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/shell.glb --out renders/final/shell --width 1100 --samples $(SAMPLES) --shots shell > build/final-shell.log 2>&1
renders/final/hull/hull.png renders/final/hull/shots.json &: export/hull.glb $(FINAL_DEPS)
	$(KIT)/with_gpu.sh $(BP) --python src/final_render.py -- --source export/hull.glb --out renders/final/hull --width 1100 --samples $(SAMPLES) --shots hull > build/final-hull.log 2>&1
final-render render: $(FINAL_IMAGES) renders/final/eevee/hero.png renders/final/shell/shell.png renders/final/hull/hull.png
build/look-photos/white-balance.json: src/white_balance.py src/look_matches.py refs/SOURCES.md
	$(PYTHON) src/white_balance.py > build/white-balance.log
build/look-cameras.json: build/look-photos/white-balance.json src/look_calibrate.py src/look_matches.py
	$(PYTHON) src/look_calibrate.py > build/look-calibration.log
$(LOOK_IMAGES) &: export/sxs.glb build/look-cameras.json $(FINAL_DEPS) src/look_matches.py src/photo_render.py
	$(PYTHON) src/photo_render.py --source export/sxs.glb --out renders/final/photos --samples $(SAMPLES) > build/look-photos.log 2>&1
renders/final/cpu-masks/shots.json: $(LOOK_IMAGES) src/part_masks.py
	$(BP) --python src/part_masks.py -- --source export/sxs.glb --photos renders/final/photos --out renders/final/cpu-masks > build/look-masks.log 2>&1
renders/final/look-review/values.json: renders/final/cpu-masks/shots.json src/look_review.py src/look_matches.py
	$(PYTHON) src/look_review.py --folder renders/final > build/look-values.log
look-pairs: renders/final/look-review/values.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/look-cameras.json > build/look-camera-verify.log 2>&1
build/delivery/clean.blend: $(PREPARED) src/lookdev.py src/build_high.py build/markings/headstamp.png
	$(BP) --python src/build_high.py -- --wear 0 --out build/delivery/clean.blend > build/clean-high.log 2>&1
CLEAN_BAKED := $(addprefix build/wear/clean4k/T_Covey26_,BaseColor.png Normal.png ORM.png) build/wear/clean4k/bake-report.json build/wear/clean4k/projection-owner.png
$(CLEAN_BAKED) &: build/delivery/clean.blend $(PREPARED) src/bake_form.py build/bake-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/bake_form.py -- --high build/delivery/clean.blend --out build/wear/clean4k --size 4096 --samples $(BAKE_SAMPLES) > build/clean-bake.log 2>&1
build/wear/precise4k/projection-report.json: $(CLEAN_BAKED) src/normal_projection.py
	$(BP) --python src/normal_projection.py -- --high build/delivery/clean.blend --baked build/wear/clean4k --out build/wear/precise4k > build/clean-projection.log 2>&1
build/wear/clean-textures/texture-report.json: build/wear/precise4k/projection-report.json src/ship_normal.py
	$(PYTHON) $(KIT)/downsample.py --source build/wear/precise4k --out build/wear/clean-textures --asset Covey26 --size 2048 --alpha-mode independent
	$(PYTHON) src/ship_normal.py --source build/wear/precise4k/T_Covey26_Normal.png --out build/wear/clean-textures
# The wood-edge fractures overlap the hand-flattened point field. Bake each
# cause off independently; an all-clean UV crop cannot separate those causes.
FORE_CAUSES := forend_edges forend_points
FORE_HIGH := $(foreach cause,$(FORE_CAUSES),build/delivery/off-$(cause).blend)
FORE_BAKED := $(foreach cause,$(FORE_CAUSES),build/wear/off-$(cause)/4k/bake-report.json)
FORE_PROJECTED := $(foreach cause,$(FORE_CAUSES),build/wear/off-$(cause)/precise4k/projection-report.json)
FORE_TEXTURES := $(foreach cause,$(FORE_CAUSES),build/wear/off-$(cause)/textures/texture-report.json)
.SECONDARY: $(FORE_HIGH) $(FORE_BAKED) $(FORE_PROJECTED) $(FORE_TEXTURES)
build/delivery/off-%.blend: $(PREPARED) src/lookdev.py src/build_high.py build/markings/headstamp.png
	$(BP) --python src/build_high.py -- --disable $* --out $@ > build/off-$*-high.log 2>&1
build/wear/off-%/4k/bake-report.json: build/delivery/off-%.blend $(PREPARED) src/bake_form.py build/bake-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/bake_form.py -- --high build/delivery/off-$*.blend --out build/wear/off-$*/4k --size 4096 --samples $(BAKE_SAMPLES) > build/off-$*-bake.log 2>&1
build/wear/off-%/precise4k/projection-report.json: build/wear/off-%/4k/bake-report.json src/normal_projection.py
	$(BP) --python src/normal_projection.py -- --high build/delivery/off-$*.blend --baked build/wear/off-$*/4k --out build/wear/off-$*/precise4k > build/off-$*-projection.log 2>&1
build/wear/off-%/textures/texture-report.json: build/wear/off-%/precise4k/projection-report.json src/ship_normal.py
	$(PYTHON) $(KIT)/downsample.py --source build/wear/off-$*/precise4k --out build/wear/off-$*/textures --asset Covey26 --size 2048 --alpha-mode independent
	$(PYTHON) src/ship_normal.py --source build/wear/off-$*/precise4k/T_Covey26_Normal.png --out build/wear/off-$*/textures
build/wear/variants.json: export/sxs.glb build/wear/clean-textures/texture-report.json $(FORE_TEXTURES) src/wear_variants.py
	$(BP) --python src/wear_variants.py > build/wear-variants.log 2>&1
renders/final/hero-masks/shots.json: $(FINAL_IMAGES) src/part_masks.py
	$(BP) --python src/part_masks.py -- --source export/sxs.glb --photos renders/final/beauty --out renders/final/hero-masks --shots hero > build/hero-masks.log 2>&1
renders/final/wear/measurements.json: build/wear/variants.json $(FINAL_IMAGES) renders/final/hero-masks/shots.json src/wear_review.py src/wear_reference.py $(FINAL_DEPS)
	$(PYTHON) src/wear_review.py --width $(WIDTH) --samples $(SAMPLES) > build/wear-review.log 2>&1
wear-review: renders/final/wear/measurements.json
family-review: final-render src/family_review.py
	$(PYTHON) src/family_review.py --width $(WIDTH) --samples $(SAMPLES) > build/family-review.log 2>&1
.PHONY: source-review
source-review: look-pairs src/source_review.py
	$(PYTHON) src/source_review.py --width $(WIDTH) --samples $(SAMPLES) > build/source-review.log 2>&1
final-review: final-render look-pairs source-review wear-review wear-detail family-review src/final_review.py
	$(PYTHON) src/final_review.py > build/final-review.log 2>&1

.PHONY: wear-detail
renders/final/wear-native/measurements.json: renders/final/wear/measurements.json src/wear_detail.py
	$(PYTHON) src/wear_detail.py --samples $(SAMPLES) > build/wear-detail.log 2>&1
wear-detail: renders/final/wear-native/measurements.json

# Signature loop uses the shared exported-GLB tool.
EXPORTS := export/sxs.glb export/shell.glb export/hull.glb
include ../common/gif.mk

.PHONY: docs
all: docs
docs: final-review src/docs.py
	$(PYTHON) src/docs.py
