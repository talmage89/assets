# Explicit, additive LOD targets. Never depend on export/model/bake/all/check:
# delivered LOD0 is read-only input, even if its generator is newer on disk.
LOD_CONFIG ?= src/lod.json
LOD_THREADS ?= 4
# A caller may hold the shared GPU lock for this one serial pilot build.
LOD_GPU := $(if $(filter 1,$(ASSETS_GPU_HELD)),,$(KIT)/with_gpu.sh)
.PHONY: lod lod-mesh lod-render check-lod
lod: lod-mesh lod-render

lod-mesh:
	$(BP) --threads $(LOD_THREADS) --python $(KIT)/lod.py -- build --config $(LOD_CONFIG)

lod-render: lod-mesh
	$(LOD_GPU) $(BP) --threads $(LOD_THREADS) --python $(KIT)/lod_render.py -- --config $(LOD_CONFIG)

check-lod:
	@lod_status=0; \
	$(BP) --threads $(LOD_THREADS) --python $(KIT)/lod.py -- check --config $(LOD_CONFIG) || lod_status=$$?; \
	$(BP) --threads $(LOD_THREADS) --python $(KIT)/lod_normals.py -- --config $(LOD_CONFIG) || lod_status=$$?; \
	exit $$lod_status
