# Source detail/look checkpoint. Deliberately no SUV UV, bake or export stage.
DETAIL := build/suv-detail
LOOK_PASS ?= suv-detail
LOOK_OUT := renders/$(LOOK_PASS)
DETAIL_MODULES := detail allocation finishes wheels interior underbody exterior joints mechanics construction weather spec grille surface_normals glazing
DETAIL_DEPS := $(addprefix src/suv_,$(addsuffix .py,$(DETAIL_MODULES))) src/build.py src/detail_helpers.py src/pickup_spec.py ../kit/vehicle_materials.py ../kit/materials.py ../kit/model.py ../kit/vehicle.py
LOOK_VIEWS := front_three_quarter rear_three_quarter side face lamp_unlit lamp_lit wheel cladding interior_glass interior_dash cargo_open underbody underbody_layout opened gate_open steering
COLOR_VIEWS := $(foreach color,Porcelain Carbon Aluminum Graphite Atlantic,$(addprefix $(color)_,front_three_quarter rear_three_quarter))
GLOSS_VIEWS := front_three_quarter rear_three_quarter side
.PHONY: detail detail-check detail-render detail-review check-form check-detail-repeat check-pickup
$(DETAIL)/markings/badge.png $(DETAIL)/markings/model.png $(DETAIL)/markings/plate.png $(DETAIL)/markings/display.png $(DETAIL)/markings/cluster.png $(DETAIL)/markings/tire_relief.png &: src/suv_markings.py src/markings.py ../kit/fonts.py
	@mkdir -p $(DETAIL)/markings $(TMPDIR)
	$(PYTHON) src/suv_markings.py $(DETAIL)/markings
$(DETAIL)/game.blend $(DETAIL)/game.counts.json &: build/suv/game.blend $(DETAIL_DEPS) $(DETAIL)/markings/badge.png $(DETAIL)/markings/model.png $(DETAIL)/markings/plate.png $(DETAIL)/markings/display.png $(DETAIL)/markings/cluster.png $(DETAIL)/markings/tire_relief.png
	$(BP) --python src/suv_detail.py -- --source $< --out $(DETAIL)/game.blend
$(DETAIL)/high.blend $(DETAIL)/high.counts.json &: build/suv/high.blend $(DETAIL_DEPS) $(DETAIL)/markings/badge.png $(DETAIL)/markings/model.png $(DETAIL)/markings/plate.png $(DETAIL)/markings/display.png $(DETAIL)/markings/cluster.png $(DETAIL)/markings/tire_relief.png
	$(BP) --python src/suv_detail.py -- --source $< --out $(DETAIL)/high.blend
detail: $(DETAIL)/game.blend $(DETAIL)/high.blend $(DETAIL)/game.counts.json $(DETAIL)/high.counts.json
$(DETAIL)/used-cameras.json: src/suv_calibrate_used.py src/suv_used_matches.py src/suv_spec.py ../kit/photo_match.py
	$(PYTHON) src/suv_calibrate_used.py --out $@
$(DETAIL)/game-audit.json: $(DETAIL)/game.blend src/suv_detail_config.py ../kit/audit.py
	$(BP) --python $(KIT)/audit.py -- --source $< --config src/suv_detail_config.py --out $@
$(DETAIL)/high-audit.json: $(DETAIL)/high.blend src/suv_detail_config.py ../kit/audit.py
	$(BP) --python $(KIT)/audit.py -- --source $< --config src/suv_detail_config.py --out $@
$(DETAIL)/game-check.json: $(DETAIL)/game.blend src/suv_detail_check.py
	$(BP) --python src/suv_detail_check.py -- --source $< --out $@
$(DETAIL)/high-check.json: $(DETAIL)/high.blend src/suv_detail_check.py
	$(BP) --python src/suv_detail_check.py -- --source $< --out $@
$(DETAIL)/grille-support.json: $(DETAIL)/game.blend src/suv_grille_check.py
	$(BP) --python src/suv_grille_check.py -- --source $< --out $@
$(DETAIL)/motion-game.json: $(DETAIL)/game.blend src/suv_motion.py ../kit/motion.py
	$(BP) --python src/suv_motion.py -- --source $< --out $@
$(DETAIL)/motion-high.json: $(DETAIL)/high.blend src/suv_motion.py ../kit/motion.py
	$(BP) --python src/suv_motion.py -- --source $< --out $@
check-pickup:
	$(PYTHON) src/suv_preserve_pickup.py --out $(DETAIL)/pickup-preservation.json
detail-check: detail check-form $(DETAIL)/game-audit.json $(DETAIL)/high-audit.json $(DETAIL)/game-check.json $(DETAIL)/high-check.json $(DETAIL)/motion-game.json $(DETAIL)/motion-high.json $(DETAIL)/grille-support.json $(DETAIL)/used-cameras.json check-pickup
	$(PYTHON) -c "import json,sys; failed=[p for p in sys.argv[1:] if not json.load(open(p))['passed']]; assert not failed, failed" $(addprefix $(DETAIL)/,game-audit.json high-audit.json game-check.json high-check.json motion-game.json motion-high.json grille-support.json)
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $(DETAIL)/used-cameras.json
	$(PYTHON) $(KIT)/repo_check.py
check-detail-repeat: $(DETAIL)/game.blend
	$(BP) --python src/suv_detail.py -- --source build/suv/game.blend --out $(DETAIL)/repeat.blend
	$(BP) --python src/suv_repro.py -- --source $(DETAIL)/game.blend --repeat $(DETAIL)/repeat.blend --out $(DETAIL)/repeat-check.json
$(DETAIL)/render-parameters.txt: FORCE
	@mkdir -p $(DETAIL) $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES) out=$(LOOK_OUT)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(addprefix $(LOOK_OUT)/,$(addsuffix .png,$(LOOK_VIEWS)) $(addsuffix -mask.png,$(LOOK_VIEWS))) &: $(DETAIL)/game.blend src/suv_lookdev.py src/suv_lighting.py src/lighting.py $(DETAIL)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_lookdev.py -- --source $< --out $(LOOK_OUT) --shots $(subst $(space),$(comma),$(LOOK_VIEWS)) --width $(WIDTH) --samples $(SAMPLES) --masks
$(addprefix $(LOOK_OUT)/,$(addsuffix .png,$(COLOR_VIEWS)) $(addsuffix -mask.png,$(COLOR_VIEWS))) &: $(DETAIL)/game.blend src/suv_lookdev.py src/suv_lighting.py $(DETAIL)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_lookdev.py -- --source $< --out $(LOOK_OUT) --colors --width $(WIDTH) --samples $(SAMPLES) --masks
$(LOOK_OUT)/used_front.png $(LOOK_OUT)/used_rear.png $(LOOK_OUT)/used_front-mask.png $(LOOK_OUT)/used_rear-mask.png &: $(DETAIL)/game.blend $(DETAIL)/used-cameras.json src/suv_lookdev.py src/suv_lighting.py $(DETAIL)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_lookdev.py -- --source $< --out $(LOOK_OUT) --camera-file $(DETAIL)/used-cameras.json --width $(WIDTH) --samples $(SAMPLES) --masks
$(addprefix $(OUT)/gloss/,$(addsuffix .png,$(GLOSS_VIEWS))) &: build/suv/game.blend src/suv_render.py src/suv_lighting.py build/suv/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source $< --out $(OUT)/gloss --mode gloss --shots front_three_quarter,rear_three_quarter,side --width $(WIDTH) --samples $(SAMPLES)
$(addprefix $(OUT)/gloss-pairs/,$(addsuffix .png,$(PAIRS))) &: build/suv/game.blend build/suv/cameras.json src/suv_render.py src/suv_lighting.py build/suv/parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_render.py -- --source $< --out $(OUT)/gloss-pairs --mode gloss_pairs --cameras build/suv/cameras.json --width $(WIDTH) --samples $(SAMPLES)
$(LOOK_OUT)/sweeps_front.png $(LOOK_OUT)/sweeps_rear.png &: $(DETAIL)/game.blend src/suv_motion_render.py $(DETAIL)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_motion_render.py -- --source $< --out $(LOOK_OUT) --width $(WIDTH)
detail-render: render curvature-map diagnostic-stripes $(addprefix $(LOOK_OUT)/,$(addsuffix .png,$(LOOK_VIEWS) $(COLOR_VIEWS))) $(LOOK_OUT)/used_front.png $(LOOK_OUT)/used_rear.png $(LOOK_OUT)/sweeps_front.png $(addprefix $(OUT)/gloss/,$(addsuffix .png,$(GLOSS_VIEWS))) $(addprefix $(OUT)/gloss-pairs/,$(addsuffix .png,$(PAIRS)))
detail-review: detail-render $(DETAIL)/game-check.json $(DETAIL)/used-cameras.json
	$(PYTHON) src/suv_detail_review.py --renders $(LOOK_OUT) --form $(OUT) --cameras $(DETAIL)/used-cameras.json --report $(DETAIL)/game-check.json

# Surface gate: preserves the earlier detail renders for the before/after crops.
.PHONY: surfaces
surfaces: detail $(DETAIL)/used-cameras.json
	$(PYTHON) src/suv_surface_checkpoint.py --source $(DETAIL)/game.blend --out renders/suv-surfaces --before renders/suv-detail --width $(WIDTH) --samples $(SAMPLES) --blender $(BLENDER)
