"""Vesper B24: canonical 2K atlas, glass and the accepted animated interface."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_VARIANT='bolt'
EXPORT_SKIN_NAMES={'B24Armature':'VesperB24'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
DELIVERY_SURFACES={
 'Atlas':dict(principled={'Specular IOR Level':.33}),
 'Glass':dict(principled={'Transmission Weight':1.0,'IOR':1.46,
                         'Thin Film Thickness':380.0,'Thin Film IOR':1.38})}
SOURCE_MATERIAL_SURFACES={'CP_'+key+suffix:('Glass' if key=='glass' else 'Atlas')
 for key in ('steel','alloy','stock','rubber','bolt','brass','copper','marks','reticle','glass')
 for suffix in ['',*[f'.{i:03d}' for i in range(1,100)]]}
BAKE_POLICY=dict(isolate_rigid_bones=True,consolidate_attribute_sources=True,
 cage_m=.0008,ray_distance_m=.004,ao_distance_m=.012,material_ao_channel='micro_ao')
DETACHABLES=[dict(armature='B24Armature',bone='Magazine',
 bones=['Magazine','Follower','TopRound','ReserveRound'],name='Magazine',
 filename='magazine_'+state+'.glb',clip=clip,frame=0)
 for state,clip in [('loaded','Idle'),('empty','IdleEmpty')]]
