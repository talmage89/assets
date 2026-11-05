# Additive form-checkpoint rules. No station targets or artifacts are replaced.
STRIP_SEEDS ?= 201,202,203,204
STRIP_IDS := $(subst $(comma), ,$(STRIP_SEEDS))
STRIP_SOURCES := $(wildcard src/strip_*.py)
STRIP_GEOMETRY := src/strip_plan.py src/strip_build.py src/strip_building.py src/strip_site.py src/strip_graphics.py
STRIP_MODELS := $(foreach s,$(STRIP_IDS),build/strip/strip-$(s).blend build/strip/strip-$(s).glb build/strip/strip-$(s).json)
STRIP_MAIN_SHOTS := hero storefront walk tower pylon rear services
STRIP_IMAGES := $(addprefix renders/strip/checkpoint/,$(addsuffix .png,$(STRIP_MAIN_SHOTS))) $(foreach s,$(STRIP_IDS),renders/strip/checkpoint/seeds/$(s)/above.png renders/strip/checkpoint/seeds/$(s)/street.png) renders/strip/checkpoint/scale.png
.PHONY: strip strip-model strip-check strip-refs strip-render strip-match strip-review strip-context strip-repeat
strip: strip-refs strip-model strip-check strip-render strip-match strip-review
build/strip/parameters.txt: FORCE
	@mkdir -p build/strip $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seeds=$(STRIP_SEEDS) plan=$(STRIP_PLAN)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(STRIP_MODELS) &: $(STRIP_GEOMETRY) src/geometry.py src/building.py src/equipment.py src/siteworks.py src/ground_adapter.py build/strip/parameters.txt $(STRIP_PLAN) ../shrubs/export/Shrubs.glb
	$(BP) --python src/strip_build.py -- --seeds $(STRIP_SEEDS) --out build/strip $(if $(STRIP_PLAN),--plan $(STRIP_PLAN))
strip-model: $(STRIP_MODELS)
strip-refs:
	$(PYTHON) $(KIT)/fetch_refs.py refs --only strip-commerce.jpg strip-sunnyvale.jpg strip-sterling.pdf
strip-check: strip-model ../ground/export/Ground.glb
	$(PYTHON) src/strip_check_plan.py
	$(BP) --python src/strip_check.py -- --seeds $(STRIP_SEEDS)
	$(PYTHON) $(KIT)/repo_check.py
build/strip/context/split.glb:
	$(BP) --python ../houses/src/build.py -- --type split --seed 51 --out build/strip/context/split.blend
build/strip/context/station-101.glb: ../shrubs/export/Shrubs.glb
	$(BP) --python src/build.py -- --seeds 101 --out build/strip/context/station-101.blend
../cars/export/AlderC150.glb:
	$(MAKE) -C ../cars export
strip-context: ../ground/export/Ground.glb ../cars/export/AlderC150.glb build/strip/context/split.glb build/strip/context/station-101.glb
build/strip/render-parameters.txt: FORCE
	@mkdir -p build/strip
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(STRIP_IMAGES) &: $(STRIP_MODELS) src/strip_render.py build/strip/render-parameters.txt | strip-context
	$(KIT)/with_gpu.sh $(BP) --python src/strip_render.py -- --family --scale --width $(WIDTH) --samples $(SAMPLES)
strip-render: $(STRIP_IMAGES)
build/strip/cameras.json: src/strip_photo_matches.py src/strip_plan.py src/strip_refs.py $(KIT)/photo_match.py | strip-refs
	$(PYTHON) src/strip_refs.py
	$(PYTHON) $(KIT)/photo_match.py solve --config src/strip_photo_matches.py --out $@
renders/strip/matches/commerce-pair.jpg renders/strip/matches/sunnyvale-pair.jpg renders/strip/matches/sterling-pair.jpg &: $(STRIP_MODELS) src/strip_render.py src/strip_photo_matches.py build/strip/cameras.json build/strip/render-parameters.txt | strip-context
	$(KIT)/with_gpu.sh $(BP) --python src/strip_render.py -- --matches --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/strip/cameras.json --renders renders/strip/matches --out renders/strip/matches
strip-match: renders/strip/matches/commerce-pair.jpg renders/strip/matches/sunnyvale-pair.jpg renders/strip/matches/sterling-pair.jpg
strip-review: strip-render strip-match
	$(PYTHON) src/strip_review.py
strip-repeat: strip-model
	$(PYTHON) src/strip_repeat.py --blender "$(BLENDER)"
