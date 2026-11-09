.DELETE_ON_ERROR:
# Final shared-image utility family; all Blender jobs run serially.
WIDTH ?= 1600
SAMPLES ?= 64
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 4
WEAR ?= 1
CHECKPOINT_BLEND := build/utility.blend
CHECKPOINT_OUTPUTS := build/utility.blend build/utility.glb build/utility.json $(foreach s,101 102 103 104,build/street-$(s).blend build/street-$(s).glb build/street-$(s).json)
MAPS := $(foreach c,BaseColor Normal ORM,textures/ship/T_Utility_$(c).png)
DELIVERIES := $(foreach n,UtilityParts UtilityStreet-101 UtilityStreet-102 UtilityStreet-103 UtilityStreet-104,export/$(n).gltf export/$(n).bin export/$(n).json)
CHECKPOINT_DEPS := $(addprefix src/,build.py construction.py plan.py span.py cables.py surfaces.py atlas.py markings.py) build/context.json $(MAPS) ../kit/model.py ../kit/tiling.py
CHECKPOINT_CHECK = $(PYTHON) -m unittest discover -s src -p 'test_*.py' -v
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --renders renders/final
CHECKPOINT_OUT := renders/final
FINAL_IMAGES := $(foreach s,101 102 103 104,$(foreach v,street above,renders/final/$(s)/$(v).png)) $(addprefix renders/final/101/,$(addsuffix .png,hero transformer crossarm communication deadend anchor service base tags distance distance_filtered dusk)) renders/final/103/bank.png renders/final/103/riser.png
# Individual jobs keep completed images when the shared machine interrupts a
# later process. The kit's concluding batch only validates/skips current views.
CHECKPOINT_RENDER_OUTPUTS := renders/final/.stamp
include ../kit/checkpoint_rules.mk
BP += -t 4
export PYTHONDONTWRITEBYTECODE := 1
all: docs

build/look-parameters.txt: FORCE
	@mkdir -p build $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='wear=$(WEAR) size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
build/fields/fields.json: src/textures.py src/atlas.py build/look-parameters.txt
	$(PYTHON) src/textures.py source --size $(BAKE_SIZE) --wear $(WEAR)
textures/bake/T_Utility_BaseColor.png textures/bake/T_Utility_Normal.png textures/bake/T_Utility_ORM.png &: build/fields/fields.json src/textures.py
	$(KIT)/with_gpu.sh $(BP) --python src/textures.py -- bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
$(MAPS) &: textures/bake/T_Utility_BaseColor.png textures/bake/T_Utility_Normal.png textures/bake/T_Utility_ORM.png
	$(PYTHON) $(KIT)/downsample.py --source textures/bake --out textures/ship --asset Utility --size 2048
.PHONY: textures export context matches check-surfaces repeat before-after wire-review final-eevee
textures: $(MAPS)
build/context.json: src/context.py src/context_finish.py src/context_build.py $(wildcard ../houses/src/*.py) $(wildcard ../trees/src/*.py) $(wildcard ../cars/src/*.py) ../ground/src/textures.py ../ground/src/build.py ../street-light/src/build.py
	$(PYTHON) src/context.py
context: build/context.json
$(DELIVERIES) build/delivery.json &: $(CHECKPOINT_OUTPUTS) src/deliver.py $(MAPS)
	$(PYTHON) src/deliver.py
export: $(DELIVERIES) build/delivery.json
$(FINAL_IMAGES): $(DELIVERIES) src/render.py src/ribbon.py src/context.py src/setting.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/final --width $(WIDTH) --samples $(SAMPLES) --seeds $(notdir $(patsubst %/,%,$(dir $@))) --shots $(basename $(notdir $@))
$(CHECKPOINT_RENDER_OUTPUTS): $(FINAL_IMAGES)
render: $(FINAL_IMAGES)
check: check-surfaces
check-surfaces: export
	$(BP) --python src/check.py
	$(BP) --python src/check_delivery.py
	$(BP) --python src/render.py -- --validate-only
	$(PYTHON) src/costs.py > build/costs.log

build/matched-cameras.json: src/photo_matches.py $(CHECKPOINT_OUTPUTS)
	$(PYTHON) src/photo_matches.py $@
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration $@
renders/matches/.stamp: build/matched-cameras.json $(DELIVERIES) src/render.py src/ribbon.py src/setting.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/matches --width $(WIDTH) --samples $(SAMPLES) --seeds 101,104 --camera-file build/matched-cameras.json
	$(PYTHON) src/photo_matches.py --crop build/matched-cameras.json renders/matches build/matched-pairs.json
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/matched-pairs.json --renders renders/matches --out renders/matches
	@touch $@
matches: refs renders/matches/.stamp
renders/wires/.stamp: $(DELIVERIES) src/wire_review.py src/ribbon.py src/render.py build/checkpoint-render-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/wire_review.py -- render --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) src/wire_review.py measure
	@touch $@
wire-review: renders/wires/.stamp
renders/final-eevee/101/hero.png: $(DELIVERIES) src/render.py src/ribbon.py src/eevee.py src/setting.py
	$(KIT)/with_gpu.sh $(BP) --python src/eevee.py -- --out renders/final-eevee --width $(WIDTH) --samples $(SAMPLES) > build/eevee-render.log 2>&1
	$(PYTHON) -c "from pathlib import Path; s=Path('build/eevee-render.log').read_text(errors='replace'); assert 'Error: C' not in s and 'Shader compilation error' not in s; print('EEVEE SHADERS PASS')"
final-eevee: renders/final-eevee/101/hero.png
renders/fixes/.stamp: $(DELIVERIES) $(CHECKPOINT_RENDER_OUTPUTS) renders/matches/.stamp src/comparison.py
	$(PYTHON) src/comparison.py --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
before-after: renders/fixes/.stamp
review: matches wire-review final-eevee before-after
GALLERY_PARTS := tangent-top deadend-guy transformer-top bank riser light-bracket crossarm splice-case
GALLERY_OUTPUTS := $(foreach p,$(GALLERY_PARTS),$(foreach v,front side back top,renders/gallery/$(p)-$(v).png)) renders/gallery/scale-front.png
review: gallery
review: wear-review
renders/wear/101/wood_10m.png: $(DELIVERIES) src/render.py src/setting.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/wear --seeds 101 --shots wood_10m --width $(WIDTH) --samples $(SAMPLES)
.PHONY: wear-review
wear-review: renders/wear/101/wood_10m.png
renders/gallery/.stamp $(GALLERY_OUTPUTS) &: $(DELIVERIES) src/gallery.py src/gallery_views.py
	$(KIT)/with_gpu.sh $(BP) --python src/gallery.py -- --width 800 --samples 48
	@touch $@
.PHONY: gallery docs
gallery: renders/gallery/.stamp $(GALLERY_OUTPUTS)
docs: review
	$(PYTHON) src/review.py --renders renders/final --docs
repeat: export
	$(PYTHON) src/repeat.py --blender "$(BLENDER)"
.PHONY: clean-family
clean: clean-family
clean-family:
	$(PYTHON) -c "import shutil; [shutil.rmtree(p,ignore_errors=True) for p in ('textures','export')]"

# Additional checked kinds only; the original delivery graph is unchanged.
LOD_CONFIGS := src/lod-tangent.json src/lod-transformer-pole.json
include ../kit/lod_rules.mk
.PHONY: check-lod-atlas
check-lod: check-lod-atlas
check-lod-atlas:
	@set -e; for lod_config in $(LOD_CONFIGS); do \
		$(BP) --threads $(LOD_THREADS) --python src/check_lod_atlas.py -- --config "$$lod_config"; \
	done
