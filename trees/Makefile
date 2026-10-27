ASSET := RedMaple
FINAL_PIPELINE := 1
SAMPLES ?= 72
WIDTH ?= 1600
PASS ?= checkpoint
STUDIO_SCRIPT := src/render.py
FINAL_SHOTS := hero,front,side,back,top,bark,bark_2m,branchlet,crown_up,scale,root_flare,unions,unions_reverse,unions_upper,unions_upper_reverse,dripline,silhouette,structure,daylight
EEVEE_SHOT := hero
MODEL_DEPS := src/build.py src/growth.py src/settings.py src/leaves.py src/bark.py src/bark_source.py src/leaf_material.py src/wood.py src/wood_uv.py ../kit/botany.py ../kit/model.py
BAKE_DEPS := src/leaves.py src/settings.py
BAKE_POSTPROCESS = $(PYTHON) src/leaves.py --out textures/bake --composite build/leaf-source
include ../kit/rules.mk
.DEFAULT_GOAL := all
TREE_SHOTS ?= daylight,crown_up,scale,structure,unions,unions_reverse,unions_upper,unions_upper_reverse,dripline,root_flare,silhouette
.PHONY: tree-checkpoint tree-render tree-match tree-contact check-structure check-framed-cameras check-botanical-delivery

tree-checkpoint: refs model check-scene check-structure tree-render tree-match tree-contact

tree-render: model
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/lookdev.blend --out renders/$(PASS) --shots $(TREE_SHOTS) --width $(WIDTH) --samples $(SAMPLES)

tree-match: refs model build/framed-cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source build/lookdev.blend --out renders/$(PASS) --camera-file build/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/framed-cameras.json --renders renders/$(PASS) --out renders/$(PASS)

tree-contact: build/reference-measurements.json
	$(PYTHON) src/review.py --renders renders/$(PASS)

check: check-structure check-framed-cameras check-botanical-delivery
check-structure: model
	$(BP) --python src/check_structure.py -- --source build/lookdev.blend --out build/structure-check.json

build/reference-measurements.json: src/reference_measurements.py
	$(PYTHON) src/reference_measurements.py

build/framed-cameras.json: build/matched-cameras.json src/frame_matches.py
	$(PYTHON) src/frame_matches.py --source build/matched-cameras.json --out $@

check-framed-cameras: build/framed-cameras.json
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/framed-cameras.json

renders/final/.matched: export/$(ASSET).glb build/framed-cameras.json src/render.py src/leaf_material.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --stage final --source $< --out renders/final --camera-file build/framed-cameras.json --width $(WIDTH) --samples $(SAMPLES)
	$(PYTHON) $(KIT)/photo_match.py compose --calibration build/framed-cameras.json --renders renders/final --out renders/final
	@touch $@
renders/final/.stamp: src/views.py src/leaf_material.py
# Final docs only consume imported GLB renders, including the calibrated pairs.
docs: renders/final/.matched build/reference-measurements.json

check-botanical-delivery: export/$(ASSET).glb
	$(BP) --python src/check_delivery.py -- --source build/finalized.blend --glb $< --out build/botanical-delivery-check.json

.PHONY: check-bake
check-bake: build/baked.stamp
	$(PYTHON) -c "import json; r=json.load(open('textures/bake/bake-report.json')); assert r['BaseColor']['alpha_missed_interior_texels']==0 and r['BaseColor']['black_interior_texels']==0, r['BaseColor']"
check: check-bake

.PHONY: check-bark
check-bark: renders/final/.matched src/bark_evidence.py
	$(BP) --python src/bark_evidence.py -- --renders renders/final
check: check-bark
