"""One Bracken atlas, unchanged 1.5.0 rigid rig and isolated moving parts."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_VARIANT='lever'
EXPORT_SKIN_NAMES={'LeverArmature':'BrackenL20'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
MATERIAL_OVERRIDES={'':dict(specular=.16)}
# The kit's named-root isolation also protects stationary carvings from rays
# hitting their neighboring tangs, bands and screws. Rest attributes keep grain
# and wear in their original frames while projection copies are separated.
BAKE_POLICY=dict(isolate_rigid_bones=True,isolate_moving=True,
 moving_roots=['Stock','Forend'],consolidate_attribute_sources=True,
 cage_m=.001,ray_distance_m=.004,ao_distance_m=.009,
 material_ao_channel='micro_ao')
