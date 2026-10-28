"""Hearth 12: one atlas, preserved 1.1.0 rig and isolated rigid projection."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_VARIANT='shotgun'
EXPORT_SKIN_NAMES={'ShotgunArmature':'Hearth12'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
MATERIAL_OVERRIDES={'':dict(specular=.33)}
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
 cage_m=.0010,ray_distance_m=.004,ao_distance_m=.012,
 material_ao_channel='micro_ao')
