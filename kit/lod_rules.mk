# Explicit, additive LOD targets. Never depend on export/model/bake/all/check:
# delivered LOD0 is read-only input, even if its generator is newer on disk.
LOD_CONFIG ?= src/lod.json
.PHONY: lod lod-mesh lod-render check-lod
lod: lod-mesh lod-render

lod-mesh:
	$(BP) --python $(KIT)/lod.py -- build --config $(LOD_CONFIG)

lod-render: lod-mesh
	$(KIT)/with_gpu.sh $(BP) --python $(KIT)/lod_render.py -- --config $(LOD_CONFIG)

check-lod:
	$(BP) --python $(KIT)/lod.py -- check --config $(LOD_CONFIG)
	$(BP) --python $(KIT)/lod_normals.py -- --config $(LOD_CONFIG)
