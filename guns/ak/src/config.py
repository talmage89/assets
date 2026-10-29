"""Canonical 2048 PBR atlas and accepted 1.6.0 binding."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_VARIANT='ak'
EXPORT_SKIN_NAMES={'R39Armature':'Rill39'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
BAKE_BASECOLOR_ALPHA_CHANNEL='specular_factor'
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
 isolate_moving=True,moving_roots=['Sight_RearBlock','Sight_TangentLeaf',
 'Sight_SliderButton-1','Sight_SliderButton1','Sight_FrontTower','GasBlock_Neck',
 'PistolGrip_Sculpt','Handguard_Retainer363','TopCover_Pressed','LowerHandguard_Sculpt','UpperHandguard_Sculpt'],
 cage_m=.0010,ray_distance_m=.006,ao_distance_m=.01,material_ao_channel='micro_ao')
DETACHABLES=[dict(armature='R39Armature',bone='Magazine',
 bones=['Magazine','Follower','TopRound','SecondRound','ThirdRound'],name='Magazine',
 filename='magazine_'+state+'.glb',clip=clip,frame=0)
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]]
