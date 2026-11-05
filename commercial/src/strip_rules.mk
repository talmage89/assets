# Surface checkpoint: separate strip outputs, shared accepted commercial maps.
STRIP_SEEDS ?= 201,202,203,204
STRIP_IDS := $(subst $(comma), ,$(STRIP_SEEDS))
STRIP_PLAN ?=
STRIP_BUILD := build/strip-look
STRIP_GEOMETRY := $(addprefix src/,strip_build.py strip_building.py strip_plan.py strip_graphics.py strip_maps.py strip_age.py strip_surfaces.py strip_site.py)
STRIP_MODELS := $(foreach s,$(STRIP_IDS),$(STRIP_BUILD)/strip-$(s).blend $(STRIP_BUILD)/strip-$(s).glb $(STRIP_BUILD)/strip-$(s).json)
STRIP_MAIN_SHOTS := hero storefront walk tower endcap pylon rear services stalls dusk scale
STRIP_IMAGES := $(addprefix renders/strip/checkpoint/,$(addsuffix .png,$(STRIP_MAIN_SHOTS))) $(foreach s,$(STRIP_IDS),renders/strip/checkpoint/seeds/$(s)/above.png renders/strip/checkpoint/seeds/$(s)/street.png)
STRIP_PAIRS := commerce sunnyvale sterling period_walk period_lot used_rear
.PHONY: strip strip-model strip-check strip-refs strip-render strip-match strip-review strip-context strip-repeat strip-export strip-protected strip-eevee
strip: strip-protected strip-refs strip-model strip-export strip-check strip-render strip-match strip-eevee strip-review
$(STRIP_BUILD)/parameters.txt: FORCE
	@mkdir -p $(STRIP_BUILD) $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seeds=$(STRIP_SEEDS) plan=$(STRIP_PLAN) look=1\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(STRIP_MODELS) &: $(STRIP_GEOMETRY) src/geometry.py src/building.py src/equipment.py src/siteworks.py src/ground_adapter.py src/surfaces.py src/paving.py src/age.py src/textures.py $(STRIP_BUILD)/parameters.txt $(STRIP_PLAN) $(MAPS) textures/ship/graphics.json ../shrubs/export/Shrubs.glb ../houses/textures/ship/T_HouseShingles_BaseColor.png
	$(BP) --python src/strip_build.py -- --look --seeds $(STRIP_SEEDS) --out $(STRIP_BUILD) $(if $(STRIP_PLAN),--plan $(STRIP_PLAN))
strip-model: $(STRIP_MODELS)
strip-refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only strip-commerce.jpg strip-sunnyvale.jpg strip-sterling.pdf strip-westlakes.pdf strip-rear.jpg strip-walk.jpg strip-lot.jpg
strip-check: strip-model ../ground/export/Ground.glb strip-protected
	$(PYTHON) src/strip_check_plan.py
	$(BP) --python src/strip_check.py -- --source-root $(STRIP_BUILD) --seeds $(STRIP_SEEDS)
	$(BP) --python src/strip_check_delivery.py -- --source-root $(STRIP_BUILD) --seeds $(STRIP_SEEDS)
	$(PYTHON) $(KIT)/repo_check.py
strip-export: strip-model
	$(PYTHON) src/strip_delivery.py --source-root $(STRIP_BUILD) --seeds $(STRIP_SEEDS)
../houses/textures/ship/T_HouseShingles_BaseColor.png:
	$(MAKE) -C ../houses bake
../cars/export/AlderC150.glb:
	$(MAKE) -C ../cars export
../cars/export/AlderH120.glb:
	$(MAKE) -C ../cars BODY=hatch export
../cars/export/AlderX220.glb:
	$(MAKE) -C ../cars BODY=suv export
strip-context: ../ground/export/Ground.glb ../cars/export/AlderC150.glb ../cars/export/AlderH120.glb ../cars/export/AlderX220.glb
	$(PYTHON) src/strip_context.py
$(STRIP_BUILD)/render-parameters.txt: FORCE
	@mkdir -p $(STRIP_BUILD)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(STRIP_IMAGES) &: $(STRIP_MODELS) src/strip_render.py src/strip_presentation.py $(STRIP_BUILD)/render-parameters.txt | strip-context
	$(KIT)/with_gpu.sh $(BP) --python src/strip_render.py -- --source-root $(STRIP_BUILD) --family --scale --width $(WIDTH) --samples $(SAMPLES)
strip-render: $(STRIP_IMAGES)
build/strip/cameras.json: src/strip_photo_matches.py src/strip_plan.py src/strip_refs.py $(KIT)/photo_match.py | strip-refs
	$(PYTHON) src/strip_refs.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/strip_photo_matches.py --out $@
$(addprefix renders/strip/matches/,$(addsuffix -pair.jpg,$(STRIP_PAIRS))) &: $(STRIP_MODELS) src/strip_render.py src/strip_presentation.py src/strip_photo_matches.py src/strip_matches.py build/strip/cameras.json $(STRIP_BUILD)/render-parameters.txt | strip-context
	$(KIT)/with_gpu.sh $(BP) --python src/strip_matches.py -- --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/strip/cameras.json --renders renders/strip/matches --out renders/strip/matches
strip-match: $(addprefix renders/strip/matches/,$(addsuffix -pair.jpg,$(STRIP_PAIRS)))
renders/strip/eevee/hero.png: $(STRIP_MODELS) src/strip_render.py src/strip_presentation.py $(STRIP_BUILD)/render-parameters.txt | strip-context
	$(KIT)/with_gpu.sh $(BP) --python src/strip_render.py -- --source-root $(STRIP_BUILD) --out renders/strip/eevee --engine BLENDER_EEVEE --shots hero --width $(WIDTH) --samples $(SAMPLES)
strip-eevee: renders/strip/eevee/hero.png
strip-review: strip-render strip-match strip-eevee
	$(PYTHON) src/strip_review.py
strip-repeat: strip-model
	$(PYTHON) src/strip_repeat.py --blender "$(BLENDER)" --look
strip-protected:
	$(PYTHON) src/strip_preserve.py

.PHONY: strip-fixes
renders/strip/form-fixes/comparison.json: src/strip_form_comparison.py src/strip_render.py src/strip_presentation.py src/strip_plan.py src/strip_building.py src/strip_site.py | strip-context
	$(KIT)/with_gpu.sh $(PYTHON) src/strip_form_comparison.py --blender "$(BLENDER)"
strip-fixes: renders/strip/form-fixes/comparison.json
strip: strip-fixes

.PHONY: strip-values
strip-values: strip-match
	$(PYTHON) src/strip_measure.py
	$(BP) --python src/strip_check_values.py
strip-review: strip-values strip-fixes
