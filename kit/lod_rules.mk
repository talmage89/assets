# Explicit, additive LOD targets. Never depend on export/model/bake/all/check:
# delivered LOD0 is read-only input, even if its generator is newer on disk.
LOD_CONFIG ?= src/lod.json
# Families declare all independently placed kinds here. An explicit single
# LOD_CONFIG on the command line still selects just that kind.
ifeq ($(origin LOD_CONFIG),command line)
LOD_CONFIGS := $(LOD_CONFIG)
else
LOD_CONFIGS ?= $(LOD_CONFIG)
endif
LOD_THREADS ?= 4
# A caller may hold the shared GPU lock for this one serial pilot build.
LOD_GPU := $(if $(filter 1,$(ASSETS_GPU_HELD)),,$(KIT)/with_gpu.sh)
.PHONY: lod lod-mesh lod-render check-lod
lod: lod-mesh lod-render

lod-mesh:
	@set -e; for lod_config in $(LOD_CONFIGS); do \
		$(BP) --threads $(LOD_THREADS) --python $(KIT)/lod.py -- build --config "$$lod_config"; \
	done

lod-render: lod-mesh
	@set -e; for lod_config in $(LOD_CONFIGS); do \
		$(LOD_GPU) $(BP) --threads $(LOD_THREADS) --python $(KIT)/lod_render.py -- --config "$$lod_config"; \
	done

check-lod:
	@lod_status=0; for lod_config in $(LOD_CONFIGS); do \
		$(BP) --threads $(LOD_THREADS) --python $(KIT)/lod.py -- check --config "$$lod_config" || lod_status=$$?; \
		$(BP) --threads $(LOD_THREADS) --python $(KIT)/lod_normals.py -- --config "$$lod_config" || lod_status=$$?; \
	done; exit $$lod_status
