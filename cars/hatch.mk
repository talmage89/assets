# Detail/look checkpoint. STAGE=form preserves the accepted round-four graph.
ifeq ($(STAGE),form)
include hatch_form.mk
else
.DEFAULT_GOAL := all
BLENDER ?= blender
PYTHON ?= python3
KIT := $(abspath ../kit)
REPO := $(abspath ..)
BP := $(BLENDER) -t 1 -b --factory-startup --python-exit-code 1
RP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(REPO)/build/tmp
export ASSETS_GPU_LOCK ?= $(REPO)/build/locks/gpu.lock
WIDTH ?= 1400
SAMPLES ?= 48
WEAR ?= .65
PASS ?= hatch-checkpoint
OUT := renders/$(PASS)
HD := build/hatch-detail
HC := src/hatch_detail_config.py
FORMDEPS := src/hatch_build.py src/hatch_body.py src/hatch_apertures.py src/hatch_character.py src/hatch_spec.py src/build.py src/wheels.py
DETAILDEPS := src/hatch_detail.py src/hatch_exterior.py src/hatch_finishes.py src/hatch_hardware.py src/hatch_interior.py src/hatch_mechanisms.py src/hatch_surface_detail.py src/hatch_underbody.py src/finishes.py src/detail_helpers.py ../kit/vehicle_materials.py
empty :=
space := $(empty) $(empty)
comma := ,
VIEWS := front_three_quarter rear_three_quarter face lamp_unlit lamp_lit wheel grille plate_detail mirror interior_glass cargo underbody underbody_layout opened_front opened_rear scale side front rear top
COLORS := Porcelain Carbon Graphite Aluminum Atlantic
COLORVIEWS := $(foreach c,$(COLORS),$(c)_front $(c)_rear)
MOTIONVIEWS := $(foreach g,doors hood liftgate steering wheels,$(foreach i,0 1 2 3 4,$(g)_$(i)))
.NOTPARALLEL:
.DELETE_ON_ERROR:
.PHONY: all refs model check render review FORCE
all: refs model check render review eevee source-pairs
RENDER_SOURCE ?= export/AlderH120.glb
$(HD)/wear.txt: FORCE
	@mkdir -p $(HD) $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='$(WEAR)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(HD)/parameters.txt: FORCE
	@mkdir -p $(HD) $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR) width=$(WIDTH) samples=$(SAMPLES) out=$(OUT)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only hatch-used-front.jpg hatch-used-rear.jpg hatch-color-report.pdf
build/markings/.hatch-family: src/markings.py ../kit/fonts.py
	$(PYTHON) src/markings.py build/markings
	@touch $@
$(HD)/markings/.stamp: src/hatch_markings.py ../kit/fonts.py
	$(PYTHON) src/hatch_markings.py $(HD)/markings
	@touch $@
build/hatch/game.blend: $(FORMDEPS)
	@mkdir -p build/hatch $(TMPDIR)
	$(BP) --python src/hatch_build.py -- --quality game --out $@
build/hatch/high.blend: $(FORMDEPS)
	@mkdir -p build/hatch $(TMPDIR)
	$(BP) --python src/hatch_build.py -- --quality high --out $@
$(HD)/game.blend $(HD)/game.counts.json &: build/hatch/game.blend build/hatch/high.blend $(DETAILDEPS) $(HD)/markings/.stamp build/markings/.hatch-family $(HD)/wear.txt
	$(BP) --python src/hatch_detail.py -- --source build/hatch/game.blend --out $(HD)/game.blend --wear $(WEAR)
$(HD)/high.blend $(HD)/high.counts.json &: build/hatch/high.blend $(DETAILDEPS) $(HD)/markings/.stamp build/markings/.hatch-family $(HD)/wear.txt
	$(BP) --python src/hatch_detail.py -- --source build/hatch/high.blend --out $(HD)/high.blend --wear $(WEAR)
model: $(HD)/game.blend $(HD)/high.blend
$(HD)/detail-check.json: $(HD)/game.blend src/hatch_detail_check.py src/hatch_coupled_motion.py
	$(BP) --python src/hatch_detail_check.py -- --source $< --out $@ --coupled-struts
$(HD)/detail-high-check.json: $(HD)/high.blend src/hatch_detail_check.py src/hatch_coupled_motion.py
	$(BP) --python src/hatch_detail_check.py -- --source $< --out $@ --coupled-struts
$(HD)/used-cameras.json: src/hatch_used_matches.py src/hatch_spec.py
	$(PYTHON) $(KIT)/photo_match.py solve --config $< --out $@
$(HD)/audit-game.json: $(HD)/game.blend $(HC)
	$(BP) --python $(KIT)/audit.py -- --source $< --config $(HC) --out $@
$(HD)/audit-high.json: $(HD)/high.blend $(HC)
	$(BP) --python $(KIT)/audit.py -- --source $< --config $(HC) --out $@
$(HD)/motion-game.json: $(HD)/game.blend $(HC)
	$(BP) --python $(KIT)/motion.py -- --source $< --config $(HC) --out $@
$(HD)/motion-high.json: $(HD)/high.blend $(HC)
	$(BP) --python $(KIT)/motion.py -- --source $< --config $(HC) --out $@
$(HD)/repeat-game.blend: build/hatch/game.blend build/hatch/high.blend $(DETAILDEPS) $(HD)/markings/.stamp build/markings/.hatch-family $(HD)/wear.txt
	$(BP) --python src/hatch_detail.py -- --source $< --out $@ --wear $(WEAR)
$(HD)/determinism.json: $(HD)/game.blend $(HD)/repeat-game.blend src/hatch_repeat.py src/compare_pickup.py
	$(BP) --python src/hatch_repeat.py -- --before $(HD)/game.blend --after $(HD)/repeat-game.blend --out $@
check: $(HD)/detail-check.json $(HD)/detail-high-check.json $(HD)/audit-game.json $(HD)/audit-high.json $(HD)/motion-game.json $(HD)/motion-high.json $(HD)/used-cameras.json $(HD)/delivery-check.json $(HD)/determinism.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $(HD)/used-cameras.json
	$(PYTHON) $(KIT)/repo_check.py
$(addprefix $(OUT)/,$(addsuffix .png,$(VIEWS))) &: $(RENDER_SOURCE) src/hatch_lookdev.py src/hatch_colors.py src/hatch_views.py src/hatch_lighting.py $(HD)/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_lookdev.py -- --source $< --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --shots $(subst $(space),$(comma),$(VIEWS))
$(OUT)/colors.stamp: $(RENDER_SOURCE) src/hatch_lookdev.py src/hatch_colors.py src/hatch_views.py $(HD)/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_lookdev.py -- --source $< --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --colors
	@touch $@
$(OUT)/motions.stamp: $(RENDER_SOURCE) src/hatch_lookdev.py src/hatch_colors.py src/hatch_views.py $(HD)/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_lookdev.py -- --source $< --out $(OUT) --width 960 --samples 32 --motions
	@touch $@
$(OUT)/pairs.stamp: $(RENDER_SOURCE) $(HD)/used-cameras.json src/hatch_lookdev.py src/hatch_lighting.py $(HD)/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_lookdev.py -- --source $< --out $(OUT) --width $(WIDTH) --samples $(SAMPLES) --paint Porcelain --camera-file $(HD)/used-cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration $(HD)/used-cameras.json --renders $(OUT) --out $(OUT)
	@touch $@
render: $(addprefix $(OUT)/,$(addsuffix .png,$(VIEWS))) $(OUT)/colors.stamp $(OUT)/motions.stamp $(OUT)/pairs.stamp
review: render
	$(PYTHON) src/hatch_detail_review.py --renders $(OUT) --source $(RENDER_SOURCE)
ifeq ($(suffix $(RENDER_SOURCE)),.glb)
review: eevee
endif

$(HD)/material-source.blend: $(HD)/game.blend src/hatch_prepare_bake.py src/prepare_bake.py
	$(BP) --python src/hatch_prepare_bake.py -- --source $< --out $@
$(HD)/bake-source.blend: $(HD)/high.blend src/hatch_prepare_bake.py src/prepare_bake.py
	$(BP) --python src/hatch_prepare_bake.py -- --source $< --out $@
$(HD)/finalized.blend $(HD)/uv-report.json &: $(HD)/material-source.blend $(HC) src/hatch_finalize.py $(KIT)/finalize.py $(KIT)/uv.py
	$(BP) --python src/hatch_finalize.py -- --source $< --out $(HD)/finalized.blend --config $(HC) --report $(HD)/uv-report.json --size 2048 --target-density 360 --margin .0012
$(HD)/projection-check.json: $(HD)/game.blend $(HD)/high.blend src/hatch_projection_check.py
	$(BP) --python src/hatch_projection_check.py -- --low $(HD)/game.blend --high $(HD)/high.blend --out $@
textures/hatch/material-bake/bake-report.json: $(HD)/finalized.blend src/hatch_surface_bake.py $(KIT)/bake.py
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_surface_bake.py -- --source $< --out textures/hatch/material-bake --size 4096 --samples 24
textures/hatch/geometry-bake/bake-report.json: $(HD)/finalized.blend $(HD)/bake-source.blend $(HC) src/hatch_geometry_bake.py
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_geometry_bake.py -- --low $(HD)/finalized.blend --high $(HD)/bake-source.blend --out textures/hatch/geometry-bake --size 4096 --samples 24 --config $(HC)
textures/hatch/bake/bake-report.json: textures/hatch/material-bake/bake-report.json textures/hatch/geometry-bake/bake-report.json $(HD)/projection-check.json src/hatch_bake_merge.py
	$(BP) --python src/hatch_bake_merge.py -- --low $(HD)/finalized.blend --game $(HD)/game.blend --material textures/hatch/material-bake --geometry textures/hatch/geometry-bake --projection $(HD)/projection-check.json --out textures/hatch/bake
textures/hatch/ship/texture-report.json: textures/hatch/bake/bake-report.json $(KIT)/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source textures/hatch/bake --out textures/hatch/ship --asset AlderH120 --size 2048 --alpha-mode independent
export/AlderH120.glb $(HD)/export-report.json &: $(HD)/finalized.blend textures/hatch/ship/texture-report.json $(HC) $(KIT)/export.py
	$(BP) --python $(KIT)/export.py -- --source $< --textures textures/hatch/ship --asset AlderH120 --out export/AlderH120.glb --config $(HC) --report $(HD)/export-report.json
$(HD)/delivery-check.json: export/AlderH120.glb $(HD)/export-report.json $(HC) $(KIT)/verify.py
	$(BP) --python $(KIT)/verify.py -- --source $< --expected $(HD)/export-report.json --config $(HC) --out $@ --size 2048
.PHONY: export source-render
export: export/AlderH120.glb $(HD)/delivery-check.json
.PHONY: eevee
renders/hatch-eevee/.stamp: export/AlderH120.glb src/hatch_lookdev.py src/hatch_views.py src/delivery_materials.py
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_lookdev.py -- --source $< --out renders/hatch-eevee --width $(WIDTH) --samples 128 --shots front_three_quarter --engine BLENDER_EEVEE
	@touch $@
eevee: renders/hatch-eevee/.stamp
.PHONY: source-pairs
renders/hatch-source-pairs/.stamp: $(HD)/game.blend $(HD)/used-cameras.json src/hatch_lookdev.py src/hatch_lighting.py src/hatch_pair_measure.py
	$(KIT)/with_gpu.sh $(RP) --python src/hatch_lookdev.py -- --source $< --out renders/hatch-source-pairs --width $(WIDTH) --samples $(SAMPLES) --paint Porcelain --camera-file $(HD)/used-cameras.json
	$(PYTHON) src/hatch_pair_measure.py --renders renders/hatch-source-pairs
	@touch $@
source-pairs: renders/hatch-source-pairs/.stamp
source-render:
	$(MAKE) BODY=hatch RENDER_SOURCE=$(HD)/game.blend PASS=hatch-source render review
endif
