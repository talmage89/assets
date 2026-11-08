# Final views consume the baked exported family. Historical checkpoint renders
# remain optional comparison evidence, never prerequisites for a fresh clone.
.DEFAULT_GOAL := delivery
FINAL_WIDTH ?= 1600
FINAL_SAMPLES ?= 64
FINAL_SHOTS := hero above aisle tee_detail ramp_turn tower tower_landing tower_open entry top_deck scale eevee front side back top
FINAL_VIEWS := $(foreach s,101 202,$(foreach n,$(FINAL_SHOTS),renders/final/$(s)/$(n).png)) renders/final/101/plan_path.png
FINAL_PIECES := $(foreach n,$(MODULE_NAMES),renders/final/modules/$(n).png)
FINAL_PAIRS := $(foreach n,precast pleasant harmon,renders/final-matches/$(n).png renders/final-matches/$(n)-pair.jpg renders/final-source-matches/$(n).png renders/final-source-matches/$(n)-pair.jpg)
FINAL_SCRIPTS := src/light_review.py src/lookdev_render.py src/render.py src/delivery_render.py src/match_render.py
FINAL_BASES := $(foreach s,101 202,ParkingGarage-$(s) sites/ParkingGarageSite-$(s)) $(addprefix modules/,$(MODULE_NAMES)) comparison-precast comparison-harmon
FINAL_EXPORTS := $(foreach n,$(FINAL_BASES),export/final/$(n).gltf export/final/$(n).bin build/final-glb/$(n).glb)
.PRECIOUS: $(FINAL_VIEWS) $(FINAL_PIECES) $(FINAL_PAIRS) renders/final/modules.png renders/final/views.json
.PHONY: delivery delivery-review delivery-fixes docs check-texture-repeat
delivery: refs check delivery-review
$(FINAL_EXPORTS) build/final-package.json &: $(LOOK_EXPORTS) $(LOOK_MODULES) $(LOOK_MAPS) src/delivery_package.py
	$(PYTHON) src/delivery_package.py
check: delivery-check
.PHONY: delivery-check
delivery-check: $(FINAL_EXPORTS)
	$(LOOK_BP) --python src/delivery_check.py --
	$(PYTHON) src/delivery_metrics.py
build/delivery-render-parameters.json: FORCE
	$(PYTHON) -c "from pathlib import Path; import json; p=Path('$@'); s=json.dumps(dict(width=$(FINAL_WIDTH),samples=$(FINAL_SAMPLES)),sort_keys=True)+'\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(FINAL_VIEWS) $(FINAL_PIECES) $(FINAL_PAIRS) renders/final/modules.png renders/final/views.json &: $(FINAL_EXPORTS) build/lookdev/matches/calibration.json build/lookdev/baseline-cameras.json build/delivery-render-parameters.json $(FINAL_SCRIPTS)
	$(KIT)/with_gpu.sh $(LOOK_BP) --python src/delivery_render.py -- --width $(FINAL_WIDTH) --samples $(FINAL_SAMPLES)
renders/final/contact.jpg: $(FINAL_VIEWS) $(FINAL_PIECES) $(FINAL_PAIRS) src/delivery_review.py
	$(PYTHON) src/delivery_review.py
	$(PYTHON) src/lookdev_review.py --pass-name final
delivery-review: renders/final/contact.jpg
delivery-fixes: delivery-review
	$(PYTHON) src/delivery_review.py
repeat: lookdev-repeat
repeat: context-repeat
.PHONY: context-repeat
context-repeat:
	$(PYTHON) src/context_repeat.py
lookdev-repeat: $(FINAL_EXPORTS)
lookdev-repeat: context-repeat
check-texture-repeat: lookdev-bake-repeat
docs: delivery-review
	$(PYTHON) src/delivery_docs.py
# A reviewed recipe makes docs reproducible in a fresh clone. A changed recipe
# must be reviewed again; no automatic approval is inferred from passing tests.
ifneq ($(wildcard src/delivery-acceptance.json),)
delivery: docs
endif
