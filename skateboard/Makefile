# Look-dev checkpoint only. No docs or README-gallery target is part of all.
.DEFAULT_GOAL := all
.NOTPARALLEL:
BLENDER ?= blender
PYTHON ?= python3
SEED ?= 0
WIDTH ?= 1440
SAMPLES ?= 48
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 24
SHIP_SIZE ?= 2048
CYCLES_LOCK ?= ../kit/with_gpu.sh
BP := $(BLENDER) -b --factory-startup --python-exit-code 1
export TMPDIR := $(abspath ../build/tmp)
export ASSETS_GPU_LOCK ?= $(abspath ../build/locks/gpu.lock)
STATES := new season beat
SOURCES := $(wildcard src/*.py)
.PHONY: all refs form model bake export check check-repo render match match-source review repeat clean FORCE
all: refs model form export check render match match-source review
refs:
	$(PYTHON) ../kit/fetch_refs.py refs
build/parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='seed=$(SEED) bake=$(BAKE_SIZE) samples=$(BAKE_SAMPLES) ship=$(SHIP_SIZE)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/art/.stamp: src/graphics.py build/parameters.txt
	$(PYTHON) src/graphics.py --out build/art --seed $(SEED)
	@touch $@
build/%/model.blend build/%/model.glb build/%/model.json &: src/build.py src/spec.py build/parameters.txt
	@mkdir -p $(@D)
	$(BP) --python src/build.py -- --seed $(SEED) --state $* --out build/$*/model.blend
model: $(foreach s,$(STATES),build/$(s)/model.blend build/$(s)/model.glb build/$(s)/model.json)
build/%/high.blend build/%/palette.json &: build/%/model.blend build/art/.stamp src/lookdev.py
	$(BP) --python src/lookdev.py -- --source $< --out build/$*/high.blend --art build/art --palette build/$*/palette.json
build/%/low.blend: build/%/model.blend src/prepare_low.py
	$(BP) --python src/prepare_low.py -- --source $< --out $@
build/%/finalized.blend build/%/uv.json &: build/%/low.blend src/config.py
	$(BP) --python ../kit/finalize.py -- --source $< --out build/$*/finalized.blend --report build/$*/uv.json --config src/config.py --size $(SHIP_SIZE) --target-density 3000 --margin .002
build/%/bake/.stamp build/%/bake/T_Skateboard_BaseColor.png build/%/bake/T_Skateboard_Normal.png build/%/bake/T_Skateboard_ORM.png &: build/%/high.blend build/%/finalized.blend src/config.py
	$(CYCLES_LOCK) $(BP) --python ../kit/bake.py -- --low build/$*/finalized.blend --high build/$*/high.blend --out build/$*/bake --asset Skateboard --config src/config.py --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
	@touch build/$*/bake/.stamp
textures/%/.stamp textures/%/T_Skateboard_BaseColor.png textures/%/T_Skateboard_Normal.png textures/%/T_Skateboard_ORM.png &: build/%/bake/.stamp build/%/bake/T_Skateboard_BaseColor.png build/%/bake/T_Skateboard_Normal.png build/%/bake/T_Skateboard_ORM.png
	$(PYTHON) ../kit/downsample.py --source build/$*/bake --out textures/$* --asset Skateboard --size $(SHIP_SIZE)
	@touch textures/$*/.stamp
export/%.glb build/%/export.json &: build/%/finalized.blend textures/%/.stamp textures/%/T_Skateboard_BaseColor.png textures/%/T_Skateboard_Normal.png textures/%/T_Skateboard_ORM.png src/config.py
	$(BP) --python ../kit/export.py -- --source $< --textures textures/$* --asset Skateboard --out export/$*.glb --report build/$*/export.json --config src/config.py
bake: $(foreach s,$(STATES),textures/$(s)/.stamp $(foreach c,BaseColor Normal ORM,textures/$(s)/T_Skateboard_$(c).png))
export: $(foreach s,$(STATES),export/$(s).glb)
build/%/verify.json: export/%.glb build/%/export.json
	$(BP) --python ../kit/verify.py -- --source $< --expected build/$*/export.json --config src/config.py --out $@ --size $(SHIP_SIZE)
build/%/construction.json: build/%/model.blend build/%/model.glb src/check.py
	$(BP) --python src/check.py -- --source $< --out $@
check-repo:
	$(PYTHON) ../kit/repo_check.py
build/%/high-check.json: build/%/high.blend src/check_high.py
	$(BP) --python src/check_high.py -- --source $< --out $@
check: $(foreach s,$(STATES),build/$(s)/construction.json build/$(s)/high-check.json build/$(s)/verify.json) check-repo
build/before/model.glb: src/baseline.py
	$(PYTHON) src/baseline.py
	$(BP) --python build/baseline-src/build.py -- --state new --out build/before/model.blend
FORM_SHOTS := hero side truck truck_inner wheel_bearing tail_plies section_stance section_truck section_kick lean_left lean_center lean_right
FORM_IMAGES := $(foreach stage,before after,$(foreach n,$(FORM_SHOTS),renders/form-fixes/$(stage)/$(n).png))
renders/form-fixes/.stamp $(FORM_IMAGES) &: build/new/model.glb build/before/model.glb src/render.py src/crops.py
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source build/new/model.glb --out renders/form-fixes/after --width $(WIDTH) --samples $(SAMPLES) --shots hero,side,truck,truck_inner,wheel_bearing,tail_plies,section_stance,section_truck,section_kick,lean_left,lean_center,lean_right
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source build/before/model.glb --out renders/form-fixes/before --width $(WIDTH) --samples $(SAMPLES) --shots hero,side,truck,truck_inner,wheel_bearing,tail_plies,section_stance,section_truck,section_kick,lean_left,lean_center,lean_right
	$(PYTHON) src/crops.py
	@touch renders/form-fixes/.stamp
form: renders/form-fixes/.stamp $(FORM_IMAGES)
LOOK_SHOTS := hero hero_bottom tail_plies truck truck_inner wheel_bearing grip_edge grip_macro
renders/lookdev/%/.stamp renders/lookdev/%/hero.png renders/lookdev/%/hero_bottom.png renders/lookdev/%/tail_plies.png renders/lookdev/%/truck.png renders/lookdev/%/truck_inner.png renders/lookdev/%/wheel_bearing.png renders/lookdev/%/grip_edge.png renders/lookdev/%/grip_macro.png &: export/%.glb src/render.py
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source $< --out renders/lookdev/$* --width $(WIDTH) --samples $(SAMPLES) --shots hero,hero_bottom,tail_plies,truck,truck_inner,wheel_bearing,grip_edge,grip_macro
	@touch renders/lookdev/$*/.stamp
render: $(foreach s,$(STATES),renders/lookdev/$(s)/.stamp $(foreach n,$(LOOK_SHOTS),renders/lookdev/$(s)/$(n).png))
build/cameras.json: src/calibrate.py src/photo_matches.py src/spec.py
	$(PYTHON) src/calibrate.py
renders/lookdev/pairs/.stamp: export/season.glb build/cameras.json src/render.py
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source export/season.glb --out renders/lookdev/pairs --width 3072 --samples $(SAMPLES) --cameras build/cameras.json
	$(PYTHON) ../kit/photo_match.py compose --calibration build/cameras.json --renders renders/lookdev/pairs --out renders/lookdev/pairs
	@touch $@
match: renders/lookdev/pairs/.stamp
review: render match
	$(PYTHON) src/look_review.py
repeat: export
	$(PYTHON) src/repeat_delivery.py
clean:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('build','textures','export','renders/lookdev','renders/form-fixes')]"
# Retain all build intermediates for inspection and stable incremental rebuilds.
.SECONDARY:

renders/lookdev/source-pairs/.stamp: build/season/high.blend build/cameras.json src/render.py
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source $< --out renders/lookdev/source-pairs --width 3072 --samples $(SAMPLES) --cameras build/cameras.json
	$(PYTHON) ../kit/photo_match.py compose --calibration build/cameras.json --renders renders/lookdev/source-pairs --out renders/lookdev/source-pairs
	@touch $@
match-source: renders/lookdev/source-pairs/.stamp

.PHONY: repeat-form variants check-variants variant-renders
repeat-form: build/new/model.glb
	$(BP) --python src/build.py -- --seed $(SEED) --state new --out build/repeat-form.blend
	$(PYTHON) src/repeat.py
build/variants/seed%.blend build/variants/seed%.glb build/variants/seed%.json &: src/build.py src/spec.py
	$(BP) --python src/build.py -- --seed $* --state new --out build/variants/seed$*.blend
build/variants/seed%-check.json: build/variants/seed%.blend build/variants/seed%.glb src/check.py
	$(BP) --python src/check.py -- --source $< --out $@
variants: $(foreach s,1 2 3,build/variants/seed$(s).blend build/variants/seed$(s).glb build/variants/seed$(s).json)
check-variants: $(foreach s,1 2 3,build/variants/seed$(s)-check.json)
check: check-variants
variant-renders: check-variants
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source build/variants/seed1.glb --out renders/seeds/seed1 --width 1000 --samples 24 --shots hero
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source build/variants/seed2.glb --out renders/seeds/seed2 --width 1000 --samples 24 --shots hero
	$(CYCLES_LOCK) $(BP) --python src/render.py -- --source build/variants/seed3.glb --out renders/seeds/seed3 --width 1000 --samples 24 --shots hero,side
