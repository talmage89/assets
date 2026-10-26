ASSET := WhitePicket
MODEL_DEPS := src/build.py src/dimensions.py src/finishes.py ../src/modular.py ../../kit/model.py ../../kit/materials.py
REFS_DIR := ../refs
FINAL_PIPELINE := 1
WEAR := .55
SHIP_SIZE := 1024
UV_TARGET_DENSITY := 200
UV_MARGIN := .003
WIDTH ?= 1440
SAMPLES ?= 48
SHOTS := hero_closed,hero_open,paint,hardware
FINAL_SHOTS := hero_closed,hero_open,front,side,back,top,paint,hardware,joinery,gate,gate_back,pieces,posts,scale
include ../../kit/rules.mk
renders/final/.stamp: src/views.py

export/PicketAssembly.glb: export/WhitePicket.glb src/assemble.py
	$(BP) --python src/assemble.py -- --source $< --out $@
renders/assembly/.stamp: export/PicketAssembly.glb $(CONFIG) src/views.py $(KIT)/studio.py build/studio-parameters.txt
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/studio.py -- --stage final --source $< --config $(CONFIG) --out renders/assembly --shots corner_good,corner_rails --width $(WIDTH) --samples $(SAMPLES)
	@touch $@
assembly-render: renders/assembly/.stamp
docs: assembly-render
check-construction: build/finalized.blend build/lookdev.blend export/WhitePicket.glb
	$(BP) --python src/check_construction.py -- --game build/finalized.blend --high build/lookdev.blend --glb export/WhitePicket.glb --out build/construction-check.json
check: check-construction
all: match-final match
