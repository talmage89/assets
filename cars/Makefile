ASSET := AlderC150
FINAL_PIPELINE := 0
CUSTOM_CHECKPOINT := 1
WIDTH ?= 1400
PASS ?= checkpoint
SHOTS := front_three_quarter,rear_three_quarter,side,front,top
include ../kit/rules.mk

# Workbench clay is the form gate. No bake/export/docs until lead review.
.PHONY: checkpoint render preview match stripes dimensions
checkpoint: refs model check render match stripes dimensions

render: model build/game-audit.blend
	$(BP) --python src/render_checkpoint.py -- --source build/game-audit.blend --out renders/$(PASS) --width $(WIDTH) --mode clay
preview: render
match: model build/game-audit.blend refs $(BUILD)/matched-cameras.json
	@mkdir -p renders/$(PASS)
	cp build/matched-cameras.json renders/$(PASS)/matched-cameras.json
	$(BP) --python src/render_checkpoint.py -- --source build/game-audit.blend --out renders/$(PASS) --width $(WIDTH) --mode match
	$(KIT)/with_gpu.sh $(BP) --python src/render_checkpoint.py -- --source build/game-audit.blend --out renders/$(PASS) --width $(WIDTH) --mode match-stripes
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
stripes: model build/game-audit.blend
	$(KIT)/with_gpu.sh $(BP) --python src/render_checkpoint.py -- --source build/game-audit.blend --out renders/$(PASS) --width $(WIDTH) --mode stripes
dimensions: render match stripes check-form
	$(PYTHON) src/side_overlay.py --renders renders/$(PASS)
	$(PYTHON) src/compare_form.py --renders renders/$(PASS)
	$(PYTHON) src/review.py --renders renders/$(PASS)

.PHONY: check-form
check-form: build/game-audit.blend
	$(BP) --python src/check_form.py -- --source $< --out build/form-check.json
check: check-form
