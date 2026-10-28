"""Reserved final delivery policy; checkpoint does not bake or pack UVs."""
from interface import CLIPS
EXPORT_SKIN_NAMES={'R39Armature':'Rill39'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
BAKE_POLICY=dict(isolate_rigid_bones=True,cage_m=.0006,ray_distance_m=.004,ao_distance_m=.01)
DETACHABLES=[dict(armature='R39Armature',bone='Magazine',
 bones=['Magazine','Follower','TopRound','SecondRound','ThirdRound'],name='Magazine',
 filename='magazine_'+state+'.glb',clip=clip,frame=0)
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]]
