# Construction checkpoint only. No final look-dev, baking or docs JPGs.
CHECKPOINT_BLEND := build/utility.blend
CHECKPOINT_OUTPUTS := build/utility.blend build/utility.glb build/utility.json $(foreach s,101 102 103 104,build/street-$(s).blend build/street-$(s).glb build/street-$(s).json)
CHECKPOINT_DEPS := src/build.py src/construction.py src/plan.py src/span.py src/markings.py src/label_image.py build/context.json ../kit/model.py ../kit/tiling.py
CHECKPOINT_CHECK = $(PYTHON) -m unittest discover -s src -p test_span.py -v
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --renders $(CHECKPOINT_OUT)
CHECKPOINT_RENDER_OUTPUTS := $(foreach s,101 102 103 104,$(foreach v,street above,renders/checkpoint/$(s)/$(v).png)) $(addprefix renders/checkpoint/101/,$(addsuffix .png,hero transformer crossarm communication deadend anchor service base distance distance_filtered))
CHECKPOINT_RENDER_OUTPUTS += renders/checkpoint/103/bank.png renders/checkpoint/103/riser.png
WIDTH ?= 1280
SAMPLES ?= 40
include ../kit/checkpoint_rules.mk

CONTEXT_OUTPUTS := build/context.json $(addprefix build/context/,$(addsuffix .blend,builder_colonial ranch cape split pickup light maple ground)) $(addprefix build/context/,$(addsuffix .glb,builder_colonial ranch cape split)) $(addprefix build/context/,$(addsuffix .json,builder_colonial ranch cape split))
$(CONTEXT_OUTPUTS) &: src/context.py src/context_build.py ../houses/src/build.py ../cars/src/build.py ../street-light/src/build.py ../trees/src/build.py ../ground/src/build.py
	$(PYTHON) src/context.py

.PHONY: context matches check-surfaces
context: build/context.json
check: check-surfaces
check-surfaces: model
	$(BP) --python src/check.py

build/matched-cameras.json: src/photo_matches.py $(foreach s,101 104,build/street-$(s).json)
	$(PYTHON) src/photo_matches.py $@
	$(BP) --python ../kit/photo_match.py -- verify --calibration $@

renders/matches/.stamp: build/matched-cameras.json $(CHECKPOINT_OUTPUTS) src/render.py
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --out renders/matches --width $(WIDTH) --samples $(SAMPLES) --seeds 101,104 --camera-file build/matched-cameras.json
	$(PYTHON) ../kit/photo_match.py compose --calibration build/matched-cameras.json --renders renders/matches --out renders/matches
	@touch $@
matches: refs renders/matches/.stamp
review: matches
