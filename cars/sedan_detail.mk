# Detail replaces proxies, then ships one atlas and imported-GLB checkpoint views.
SEDAN_CONFIG := src/sedan_detail_config.py
DDEPS := src/sedan_detail.py src/sedan_hardware.py src/sedan_exterior.py src/sedan_interior.py src/sedan_underbody.py src/sedan_finishes.py src/sedan_colors.py src/sedan_spec.py src/finishes.py src/wheels.py src/build.py src/detail_helpers.py $(KIT)/vehicle_materials.py $(KIT)/materials.py
DOUT := renders/sedan-detail
DPAIRS := renders/sedan-used-pairs
DSHOTS := front_three_quarter rear_three_quarter face lamp_unlit lamp_lit wheel mirror interior_glass underbody underbody_layout opened_front opened_rear side front rear top scale
DSHOTS_ARG := front_three_quarter,rear_three_quarter,face,lamp_unlit,lamp_lit,wheel,mirror,interior_glass,underbody,underbody_layout,opened_front,opened_rear,side,front,rear,top,scale
DCOLORS := Porcelain Carbon Graphite Aluminum Atlantic
.PHONY: sedan-checkpoint detail-model check-detail check-motion sedan-export sedan-final sedan-pairs check

build/markings/.stamp: src/markings.py $(KIT)/fonts.py
	@mkdir -p build/markings $(TMPDIR)
	$(PYTHON) src/markings.py build/markings
	@touch $@
build/sedan/markings/.stamp: src/sedan_markings.py $(KIT)/fonts.py
	@mkdir -p build/sedan/markings $(TMPDIR)
	$(PYTHON) src/sedan_markings.py build/sedan/markings
	@touch $@
build/sedan/riggable-game.blend: $(SDEPS) src/sedan_shell.py
	$(BP) --python src/sedan_shell.py -- --quality game --out $@
build/sedan/riggable-high.blend: $(SDEPS) src/sedan_shell.py
	$(BP) --python src/sedan_shell.py -- --quality high --out $@
build/sedan/detail-game.blend: build/sedan/riggable-game.blend $(DDEPS) build/markings/.stamp build/sedan/markings/.stamp
	$(BP) --python src/sedan_detail.py -- --source $< --out $@
build/sedan/detail-high.blend: build/sedan/riggable-high.blend $(DDEPS) build/markings/.stamp build/sedan/markings/.stamp
	$(BP) --python src/sedan_detail.py -- --source $< --out $@
detail-model: build/sedan/detail-game.blend build/sedan/detail-high.blend
build/sedan/repeat-riggable.blend: $(SDEPS) src/sedan_shell.py
	$(BP) --python src/sedan_shell.py -- --quality game --out $@
build/sedan/repeat-detail.blend: build/sedan/repeat-riggable.blend $(DDEPS) build/markings/.stamp build/sedan/markings/.stamp
	$(BP) --python src/sedan_detail.py -- --source $< --out $@
build/sedan/repeat-check.json: build/sedan/detail-game.blend build/sedan/repeat-detail.blend src/sedan_repeat.py src/compare_pickup.py
	$(BP) --python src/sedan_repeat.py -- --before build/sedan/detail-game.blend --after build/sedan/repeat-detail.blend --out $@
check-repeat: build/sedan/repeat-check.json

build/sedan/detail-audit.json: build/sedan/detail-game.blend $(SEDAN_CONFIG)
	$(BP) --python $(KIT)/audit.py -- --source $< --config $(SEDAN_CONFIG) --out $@
build/sedan/detail-high-audit.json: build/sedan/detail-high.blend $(SEDAN_CONFIG)
	$(BP) --python $(KIT)/audit.py -- --source $< --config $(SEDAN_CONFIG) --out $@
build/sedan/detail-check.json: build/sedan/detail-game.blend src/sedan_detail_check.py
	$(BP) --python src/sedan_detail_check.py -- --source $< --out $@
check-detail: build/sedan/detail-audit.json build/sedan/detail-high-audit.json build/sedan/detail-check.json
build/sedan/motion-game.json: build/sedan/detail-game.blend $(SEDAN_CONFIG)
	$(BP) --python $(KIT)/motion.py -- --source $< --config $(SEDAN_CONFIG) --out $@
build/sedan/motion-high.json: build/sedan/detail-high.blend $(SEDAN_CONFIG)
	$(BP) --python $(KIT)/motion.py -- --source $< --config $(SEDAN_CONFIG) --out $@
check-motion: build/sedan/motion-game.json build/sedan/motion-high.json

build/sedan/finalized.blend build/sedan/uv-report.json &: build/sedan/material-source.blend $(SEDAN_CONFIG) $(KIT)/finalize.py $(KIT)/uv.py
	$(BP) --python $(KIT)/finalize.py -- --source $< --out build/sedan/finalized.blend --config $(SEDAN_CONFIG) --report build/sedan/uv-report.json --size 2048 --target-density 360 --margin .0012
build/sedan/bake-source.blend: build/sedan/detail-high.blend src/prepare_bake.py
	$(BP) --python src/prepare_bake.py -- --source $< --out $@
build/sedan/material-source.blend: build/sedan/detail-game.blend src/prepare_bake.py
	$(BP) --python src/prepare_bake.py -- --source $< --out $@
build/sedan/projection-check.json: build/sedan/detail-game.blend build/sedan/detail-high.blend src/sedan_projection_check.py
	$(BP) --python src/sedan_projection_check.py -- --low build/sedan/detail-game.blend --high build/sedan/detail-high.blend --out $@
textures/sedan/material-bake/bake-report.json $(addprefix textures/sedan/material-bake/T_AlderS240_,$(addsuffix .png,BaseColor Normal ORM)) &: build/sedan/finalized.blend src/sedan_surface_bake.py $(KIT)/bake.py
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_surface_bake.py -- --source build/sedan/finalized.blend --out textures/sedan/material-bake --size 4096 --samples 24
textures/sedan/geometry-bake/bake-report.json $(addprefix textures/sedan/geometry-bake/T_AlderS240_,$(addsuffix .png,BaseColor Normal ORM)) &: build/sedan/finalized.blend build/sedan/bake-source.blend $(SEDAN_CONFIG) $(KIT)/bake.py
	$(KIT)/with_gpu.sh $(RP) --python $(KIT)/bake.py -- --low build/sedan/finalized.blend --high build/sedan/bake-source.blend --out textures/sedan/geometry-bake --asset AlderS240 --size 4096 --samples 24 --config $(SEDAN_CONFIG)
textures/sedan/bake/bake-report.json $(addprefix textures/sedan/bake/T_AlderS240_,$(addsuffix .png,BaseColor Normal ORM)) &: textures/sedan/material-bake/bake-report.json textures/sedan/geometry-bake/bake-report.json build/sedan/projection-check.json src/sedan_bake_merge.py
	$(BP) --python src/sedan_bake_merge.py -- --low build/sedan/finalized.blend --game build/sedan/detail-game.blend --material textures/sedan/material-bake --geometry textures/sedan/geometry-bake --projection build/sedan/projection-check.json --out textures/sedan/bake
textures/sedan/ship/texture-report.json $(addprefix textures/sedan/ship/T_AlderS240_,$(addsuffix .png,BaseColor Normal ORM)) &: textures/sedan/bake/bake-report.json $(KIT)/downsample.py
	$(PYTHON) $(KIT)/downsample.py --source textures/sedan/bake --out textures/sedan/ship --asset AlderS240 --size 2048 --alpha-mode independent
export/AlderS240.glb build/sedan/export-report.json &: build/sedan/finalized.blend textures/sedan/ship/texture-report.json $(SEDAN_CONFIG) $(KIT)/export.py
	$(BP) --python $(KIT)/export.py -- --source build/sedan/finalized.blend --textures textures/sedan/ship --asset AlderS240 --out export/AlderS240.glb --config $(SEDAN_CONFIG) --report build/sedan/export-report.json
build/sedan/delivery-check.json: export/AlderS240.glb build/sedan/export-report.json $(SEDAN_CONFIG) $(KIT)/verify.py
	$(BP) --python $(KIT)/verify.py -- --source export/AlderS240.glb --expected build/sedan/export-report.json --config $(SEDAN_CONFIG) --out $@ --size 2048
sedan-export: export/AlderS240.glb build/sedan/delivery-check.json

build/sedan/used-cameras.json: src/sedan_used_matches.py $(KIT)/photo_match.py
	$(PYTHON) $(KIT)/photo_match.py solve --config $< --out $@
$(DOUT)/.stamp: build/sedan/parameters.txt export/AlderS240.glb src/sedan_lookdev.py src/sedan_views.py src/sedan_colors.py src/delivery_materials.py src/lighting.py src/sedan_lighting.py
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_lookdev.py -- --source export/AlderS240.glb --out $(DOUT) --width $(WIDTH) --samples $(SAMPLES) --shots $(DSHOTS_ARG)
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_lookdev.py -- --source export/AlderS240.glb --out $(DOUT) --width $(WIDTH) --samples $(SAMPLES) --colors
	@touch $@
# Literal list avoids relying on the pickup rules' helper variables.
$(DOUT)/.stamp: private DSHOTS_ARG := front_three_quarter,rear_three_quarter,face,lamp_unlit,lamp_lit,wheel,mirror,interior_glass,underbody,underbody_layout,opened_front,opened_rear,side,front,rear,top,scale
renders/sedan-motion/.stamp: export/AlderS240.glb src/sedan_lookdev.py src/sedan_views.py src/sedan_colors.py src/delivery_materials.py src/sedan_lighting.py
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_lookdev.py -- --source export/AlderS240.glb --out renders/sedan-motion --width 800 --samples 24 --motions
	@touch $@
sedan-final: $(DOUT)/.stamp renders/sedan-motion/.stamp
build/sedan/used-balanced-cameras.json: build/sedan/used-cameras.json src/sedan_pair_measure.py
	$(PYTHON) src/sedan_pair_measure.py balance --calibration $< --out $@
$(DPAIRS)/.stamp: build/sedan/parameters.txt export/AlderS240.glb build/sedan/used-balanced-cameras.json src/sedan_lookdev.py src/sedan_views.py src/sedan_colors.py src/delivery_materials.py src/lighting.py src/sedan_lighting.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/sedan/used-balanced-cameras.json
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_lookdev.py -- --source export/AlderS240.glb --out $(DPAIRS) --width $(WIDTH) --samples $(SAMPLES) --camera-file build/sedan/used-balanced-cameras.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/sedan/used-balanced-cameras.json --renders $(DPAIRS) --out $(DPAIRS)
	$(PYTHON) src/sedan_pair_measure.py measure --calibration build/sedan/used-balanced-cameras.json --renders $(DPAIRS) --out $(DPAIRS)/appearance-patches.json
	@touch $@
sedan-pairs: $(DPAIRS)/.stamp
renders/sedan-eevee/.stamp: build/sedan/parameters.txt export/AlderS240.glb src/sedan_lookdev.py src/sedan_views.py src/sedan_colors.py src/delivery_materials.py
	$(KIT)/with_gpu.sh $(RP) --python src/sedan_lookdev.py -- --source export/AlderS240.glb --out renders/sedan-eevee --width $(WIDTH) --samples 128 --shots front_three_quarter --engine BLENDER_EEVEE
	@touch $@
sedan-checkpoint: form check-detail check-motion sedan-export sedan-final sedan-pairs renders/sedan-eevee/.stamp
	$(PYTHON) src/sedan_detail_review.py --renders $(DOUT) --pairs $(DPAIRS) --form $(OUT)
check: check-form check-detail check-motion check-repeat build/sedan/delivery-check.json
	$(PYTHON) $(KIT)/repo_check.py
