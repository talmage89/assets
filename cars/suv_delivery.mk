# Independent SUV products; pickup outputs are never prerequisites or targets.
SHIP := build/suv-delivery
SCONFIG := src/suv_delivery_config.py
SGLB := export/AlderX220.glb
STEX := textures/suv
BAKE_SIZE ?= 4096
BAKE_SAMPLES ?= 24
FINAL_SAMPLES ?= 64
FINAL_VIEWS := hero,rear,front,side,back,top,face,lamp,quarter,wheel,cargo,opened,scale,lamps_lit
SRENDER_DEPS := src/suv_final_render.py src/suv_final_views.py src/suv_lighting.py src/suv_delivery_materials.py src/delivery_materials.py src/lighting.py $(KIT)/studio.py
.PHONY: suv-delivery finalize bake export verify final-render final-pairs docs check-delivery
all: suv-delivery
$(SHIP)/material-source.blend: $(DETAIL)/game.blend src/suv_prepare_bake.py src/suv_tire_uv.py src/prepare_bake.py
	$(BP) --python src/suv_prepare_bake.py -- --source $< --out $@
$(SHIP)/finalized.blend $(SHIP)/uv-report.json &: $(SHIP)/material-source.blend $(SCONFIG) src/suv_finalize.py $(KIT)/finalize.py $(KIT)/uv.py
	$(BP) --python src/suv_finalize.py -- --source $< --out $(SHIP)/finalized.blend --report $(SHIP)/uv-report.json --config $(SCONFIG) --size 2048 --target-density 700 --margin .0015
finalize: $(SHIP)/finalized.blend
$(SHIP)/bake-parameters.txt: FORCE
	@mkdir -p $(SHIP) $(TMPDIR)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='size=$(BAKE_SIZE) samples=$(BAKE_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
$(STEX)/bake/bake-report.json $(addprefix $(STEX)/bake/T_AlderX220_,$(addsuffix .png,BaseColor Normal ORM)) &: $(SHIP)/finalized.blend $(SHIP)/bake-parameters.txt src/suv_surface_bake.py src/suv_height_normal.py
	$(KIT)/with_gpu.sh $(RP) --python src/suv_surface_bake.py -- --source $< --out $(STEX)/bake --size $(BAKE_SIZE) --samples $(BAKE_SAMPLES)
bake: $(STEX)/bake/bake-report.json
$(STEX)/ship/texture-report.json $(addprefix $(STEX)/ship/T_AlderX220_,$(addsuffix .png,BaseColor Normal ORM)) &: $(STEX)/bake/bake-report.json $(KIT)/downsample.py $(KIT)/image_io.py
	$(PYTHON) $(KIT)/downsample.py --source $(STEX)/bake --out $(STEX)/ship --asset AlderX220 --size 2048 --alpha-mode independent
$(SGLB) $(SHIP)/export-report.json &: $(SHIP)/finalized.blend $(STEX)/ship/texture-report.json $(SCONFIG) src/suv_export.py $(KIT)/export.py
	$(BP) --python src/suv_export.py -- --source $< --textures $(STEX)/ship --asset AlderX220 --out $(SGLB) --config $(SCONFIG) --report $(SHIP)/export-report.json
export: $(SGLB)
$(SHIP)/delivery-check.json: $(SGLB) $(SHIP)/export-report.json $(SCONFIG) $(KIT)/verify.py
	$(BP) --python $(KIT)/verify.py -- --source $< --expected $(SHIP)/export-report.json --config $(SCONFIG) --out $@ --size 2048
$(SHIP)/surface-check.json: $(SGLB) $(SHIP)/finalized.blend $(DETAIL)/game.counts.json src/suv_delivery_check.py
	$(BP) --python src/suv_delivery_check.py -- --source $< --finalized $(SHIP)/finalized.blend --counts $(DETAIL)/game.counts.json --out $@
verify check-delivery: $(SHIP)/delivery-check.json $(SHIP)/surface-check.json
$(SHIP)/height-normal-check.txt: src/suv_height_normal.py src/suv_height_normal_check.py
	@mkdir -p $(SHIP)
	$(BP) --python src/suv_height_normal_check.py > $@
check: $(SHIP)/height-normal-check.txt
$(SHIP)/render-parameters.txt: FORCE
	@mkdir -p $(SHIP)
	@$(PYTHON) -c "from pathlib import Path; p=Path('$@'); s='width=$(WIDTH) samples=$(FINAL_SAMPLES)\n'; p.write_text(s) if not p.exists() or p.read_text()!=s else None"
renders/suv-final/.stamp: $(SGLB) $(SRENDER_DEPS) $(SHIP)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_final_render.py -- --source $< --out renders/suv-final --shots $(FINAL_VIEWS) --width $(WIDTH) --samples $(FINAL_SAMPLES)
	$(KIT)/with_gpu.sh $(RP) --python src/suv_final_render.py -- --source $< --out renders/suv-final --colors --width $(WIDTH) --samples $(FINAL_SAMPLES)
	@touch $@
renders/suv-eevee/.stamp: $(SGLB) $(SRENDER_DEPS) $(SHIP)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_final_render.py -- --source $< --out renders/suv-eevee --shots hero --engine BLENDER_EEVEE --width $(WIDTH) --samples $(FINAL_SAMPLES)
	@touch $@
final-render: renders/suv-final/.stamp renders/suv-eevee/.stamp
renders/suv-final-pairs/.stamp: $(SGLB) $(DETAIL)/used-cameras.json $(SRENDER_DEPS) $(SHIP)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_final_render.py -- --source $< --out renders/suv-final-pairs --camera-file $(DETAIL)/used-cameras.json --paint Graphite --width $(WIDTH) --samples $(FINAL_SAMPLES)
	@touch $@
renders/suv-source-pairs/.stamp: $(DETAIL)/game.blend $(DETAIL)/used-cameras.json $(SRENDER_DEPS) $(SHIP)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_final_render.py -- --stage source --source $< --out renders/suv-source-pairs --camera-file $(DETAIL)/used-cameras.json --paint Graphite --width $(WIDTH) --samples $(FINAL_SAMPLES)
	@touch $@
final-pairs: renders/suv-final-pairs/.stamp renders/suv-source-pairs/.stamp
renders/suv-source-studio/.stamp: $(DETAIL)/game.blend $(SRENDER_DEPS) $(SHIP)/render-parameters.txt
	$(KIT)/with_gpu.sh $(RP) --python src/suv_final_render.py -- --stage source --source $< --out renders/suv-source-studio --shots hero,face,lamp,wheel --width $(WIDTH) --samples $(FINAL_SAMPLES)
	@touch $@
renders/suv-motion/.stamp: $(SGLB) $(SRENDER_DEPS)
	$(KIT)/with_gpu.sh $(RP) --python src/suv_final_render.py -- --source $< --out renders/suv-motion --gate-frames 21 --width 800 --samples 24
	@touch $@
docs: final-render final-pairs renders/suv-source-studio/.stamp renders/suv-motion/.stamp src/suv_delivery_review.py
	$(PYTHON) src/suv_delivery_review.py --docs
suv-delivery: detail-check verify final-render final-pairs docs
check: verify
.PHONY: clean
clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; paths=['build/suv','build/suv-detail','build/suv-delivery','textures/suv','renders/suv-final','renders/suv-final-pairs','renders/suv-source-pairs','renders/suv-source-studio','renders/suv-eevee','renders/suv-motion','export/AlderX220.glb']; [(p.unlink() if p.is_file() else shutil.rmtree(p,ignore_errors=True)) for p in map(Path,paths)]"
