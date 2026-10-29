"""One canonical atlas, complete staged rig, and three posed detachments."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interface import CLIPS
EXPORT_VARIANT='revolver'
EXPORT_SKIN_NAMES={'RevolverArmature':'MeridianSix'}
EXPORT_ANIMATIONS={'clips':list(CLIPS)}
MATERIAL_OVERRIDES={'':dict(specular=.33)}
UV_SMART_ANGLE=45
UV_SMART_ASPECT=False
UV_PACK_SHAPE='AABB'
UV_NORMALIZE_ISLAND_SCALE=True
UV_PRIORITY={'Hammer_Body':1.25,'Frame_':1.15,'Grip_Rubber':1.2,'Barrel':1.05,
 'RearSight_':1.25,'Cylinder_Fluted':1.2,'Extractor_Rod':.5,'Ejector_Tip':1.8,'Crane_Axle':.6,
 'Live':.8,'LoaderRound':.75,'Case':.8,'InsertRound':.8,'Speedloader':.75}
# The accepted grip lip is close to steel. Isolate it for projection so
# selected-to-active rays cannot copy the frame finish into the rubber.
BAKE_POLICY=dict(isolate_moving=True,moving_roots=['Grip_RubberMold'],
 isolate_rigid_bones=True,consolidate_attribute_sources=True,
 cage_m=.00022,ray_distance_m=.0012,ao_distance_m=.008,material_ao_channel='micro_ao')
DETACHABLES=[
 dict(armature='RevolverArmature',bone='Live0',bones=['Live0'],name='Cartridge',filename='cartridge.glb',clip='Idle',frame=0),
 dict(armature='RevolverArmature',bone='Case0',bones=['Case0'],name='Case',filename='case.glb',clip='IdleAfter6',frame=0),
 dict(armature='RevolverArmature',bone='LoaderGuide',bones=['LoaderBody','LoaderRelease',*['LoaderRound'+str(i) for i in range(6)]],name='LoadedSpeedloader',filename='speedloader_loaded.glb',clip='Reload',frame=142)]
