"""PD C9 delivery policy; the accepted interface and animation are unchanged."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_VARIANT='pistol'
EXPORT_SKIN_NAMES={'PistolArmature':'Pistol'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
MATERIAL_OVERRIDES={'':dict(specular=.28)}
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
                 cage_m=.00016,ray_distance_m=.0008,ao_distance_m=.012,
                 material_ao_channel='micro_ao')
DETACHABLES=[dict(armature='PistolArmature',bone='Magazine',
 bones=['Magazine','Follower','TopRound','ReserveRound'],name='Magazine',
 filename='magazine_'+state+'.glb',clip=clip,frame=0)
 for state,clip in [('loaded','Idle'),('empty','IdleOpen')]]
