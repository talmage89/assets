CHECKPOINT_BLEND := build/Signals-201.blend
CHECKPOINT_ARGS := --seeds 201,202,203,204
CHECKPOINT_OUT := renders/checkpoint
CHECKPOINT_OUTPUTS := $(foreach n,201 202 203 204,build/Signals-$(n).blend build/Signals-$(n).glb build/Signals-$(n).json build/Signals-$(n)-components.json)
CHECKPOINT_OUTPUTS += $(foreach p,MastArm Pedestal Cabinet Head_three Head_fya Head_five Head_protected PushButton PushButtonPost PedHead SpanSet,build/parts/$(p).glb)
SHOTS_201 := above driver hero head_lit head_dark connection base pedestrian button cabinet_open cabinet dusk
SHOTS_202 := above driver
SHOTS_203 := above driver
SHOTS_204 := above driver span_hanger
CHECKPOINT_RENDER_OUTPUTS := $(foreach n,201 202 203 204,$(foreach s,$(SHOTS_$(n)),$(CHECKPOINT_OUT)/$(n)/$(s).png $(CHECKPOINT_OUT)/$(n)/$(s).json))
CHECKPOINT_CHECK = $(BP) --python src/check.py
CHECKPOINT_REVIEW = $(PYTHON) src/review.py --out $(CHECKPOINT_OUT)
CHECKPOINT_RENDER_ARGS := --seeds 201,202,203,204
include ../kit/checkpoint_rules.mk
.PHONY: arterial matches preserve check-construction check-cameras
model: arterial
arterial: preserve
	$(MAKE) -C ../ground arterial
preserve:
	$(PYTHON) src/preserve.py
check-construction: model
	$(BP) --python src/construction.py
check: check-construction
matches: model refs
	$(PYTHON) src/matches.py
	$(BP) --python $(KIT)/photo_match.py -- verify --calibration build/cameras.json
	$(KIT)/with_gpu.sh $(BP) --python src/render.py -- --source $(CHECKPOINT_BLEND:.blend=.glb) --out renders/matches --width $(WIDTH) --samples $(SAMPLES) --seeds 202,204 --camera-file build/cameras.json
	$(PYTHON) src/matches.py --compose
review: render matches

.PHONY: context
context: preserve
	$(PYTHON) src/context.py
$(CHECKPOINT_OUTPUTS): | context
arterial: context
