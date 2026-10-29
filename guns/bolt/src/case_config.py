"""Standalone fired case, sharing the canonical B24 maps."""
EXPORT_VARIANT='case'
EXPORT_ANIMATIONS=False
MATERIAL_OVERRIDES={'':dict(specular=.33)}

# Lossless subset of the shipped gun atlas; keep the source bake unchanged.
EXPORT_TEXTURE_SIZE=512
