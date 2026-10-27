ASSET := AlderC150
FINAL_PIPELINE := 0
CUSTOM_CHECKPOINT := 1
WIDTH ?= 1400
SAMPLES ?= 64
WEAR ?= .65
PASS ?= lookdev
SHOTS ?= front_three_quarter,rear_three_quarter,side,front_detail,wheel_detail,lamps_lit,interior
MARKINGS_DEPS := ../kit/fonts.py
MODEL_DEPS := src/build.py src/body.py src/forms.py src/wheels.py src/pickup_spec.py src/exterior.py src/interior.py src/underbody.py src/detail_helpers.py src/finishes.py ../kit/model.py ../kit/materials.py ../kit/vehicle.py ../kit/vehicle_materials.py
include ../kit/rules.mk

# Source-only review gate. No finalize, UV, bake or export in the default build.
.PHONY: checkpoint render preview match colors review check-form check-detail form-diagnostics
checkpoint: refs model check render match colors review
render: model
	$(KIT)/with_gpu.sh $(BP) --python src/render_lookdev.py -- --source build/lookdev.blend --out renders/$(PASS) --shots $(SHOTS) --width $(WIDTH) --samples $(SAMPLES) --masks
preview:
	$(MAKE) render WIDTH=1000 SAMPLES=24 PASS=preview
build/used-cameras.json: src/used_matches.py src/calibrate_used.py $(KIT)/photo_match.py
	$(PYTHON) src/calibrate_used.py --out $@
match: model refs build/used-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/used-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render_lookdev.py -- --source build/lookdev.blend --out renders/$(PASS) --camera-file build/used-cameras.json --width $(WIDTH) --samples $(SAMPLES) --masks
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/used-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
colors: model
	$(KIT)/with_gpu.sh $(BP) --python src/render_lookdev.py -- --source build/lookdev.blend --out renders/$(PASS) --colors --width $(WIDTH) --samples $(SAMPLES) --masks
review:
	$(PYTHON) src/review_lookdev.py --renders renders/$(PASS)
check-form: build/game-audit.blend
	$(BP) --python src/check_form.py -- --source $< --out build/form-check.json
check-detail: build/game-audit.blend build/lookdev.blend
	$(BP) --python src/check_detail.py -- --source build/game-audit.blend --out build/detail-check.json
	$(BP) --python src/check_detail.py -- --source build/lookdev.blend --out build/detail-high-check.json
check: check-form check-detail

# Rebuild corrected-form clay/stripes separately; never replace source finishes.
build/form-game.blend: $(MODEL_DEPS) build/markings/.stamp
	$(BP) --python src/build.py -- --form-only --quality game --out $@
form-diagnostics: build/form-game.blend refs build/matched-cameras.json
	@mkdir -p renders/$(PASS)
	cp build/matched-cameras.json renders/$(PASS)/matched-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render_checkpoint.py -- --source build/form-game.blend --out renders/$(PASS) --width $(WIDTH) --mode clay
	$(KIT)/with_gpu.sh $(BP) --python src/render_checkpoint.py -- --source build/form-game.blend --out renders/$(PASS) --width $(WIDTH) --mode match
	$(KIT)/with_gpu.sh $(BP) --python src/render_checkpoint.py -- --source build/form-game.blend --out renders/$(PASS) --width $(WIDTH) --mode stripes
	$(KIT)/with_gpu.sh $(BP) --python src/render_checkpoint.py -- --source build/form-game.blend --out renders/$(PASS) --width $(WIDTH) --mode match-stripes
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-cameras.json --renders renders/$(PASS) --out renders/$(PASS)
	$(PYTHON) src/side_overlay.py --renders renders/$(PASS)
	$(PYTHON) src/compare_form.py --renders renders/$(PASS)
	$(PYTHON) src/review.py --renders renders/$(PASS)
