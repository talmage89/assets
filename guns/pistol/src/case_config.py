"""The accepted fired case carries a small C9 atlas subset, with no rig or clips."""
EXPORT_VARIANT='case'
EXPORT_ANIMATIONS=False
MATERIAL_OVERRIDES={'':dict(specular=.28)}

# Lossless subset of the shipped gun atlas; keep the source bake unchanged.
EXPORT_TEXTURE_SIZE=512

# Retain the atlas neighborhood when that produces a smaller standalone file.
EXPORT_TEXTURE_CLUSTERS=True
