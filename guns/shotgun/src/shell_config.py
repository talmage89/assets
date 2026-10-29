"""Standalone exterior shell with its own lossless Hearth atlas subset."""
EXPORT_VARIANT='shell'
MATERIAL_OVERRIDES={'':dict(specular=.33)}

# Lossless subset of the shipped gun atlas; keep the source bake unchanged.
EXPORT_TEXTURE_SIZE=1024

# Retain the atlas neighborhood when that produces a smaller standalone file.
EXPORT_TEXTURE_CLUSTERS=True
