"""Standalone fired hull, in the same head-centered frame as the live shell."""
EXPORT_VARIANT='hull'
MATERIAL_OVERRIDES={'':dict(specular=.33)}

# Lossless subset of the shipped gun atlas; keep the source bake unchanged.
EXPORT_TEXTURE_SIZE=512
