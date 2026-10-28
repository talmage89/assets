"""One canonical 2K PBR atlas, unchanged 21-clip 1.3 binding."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_VARIANT='smg'
EXPORT_SKIN_NAMES={'SMGArmature':'Relay9'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
MATERIAL_OVERRIDES={'':dict(specular=.28)}
BAKE_BASECOLOR_ALPHA_CHANNEL='specular_factor'
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
 cage_m=.00065,ray_distance_m=.004,ao_distance_m=.010,material_ao_channel='micro_ao')
DETACHABLES=[dict(armature='SMGArmature',bone='Magazine',
 bones=['Magazine','Follower','TopRound','SecondRound','ThirdRound'],name='Magazine',
 filename='magazine_'+state+'.glb',clip=clip,frame=0)
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]]
