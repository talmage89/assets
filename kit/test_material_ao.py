"""Real GPU bake fixture for optional material visibility and default AO.

Run through with_gpu.sh in a clean Blender. All fixtures stay in build/.
"""
import sys,runpy,shutil
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit.materials import Nodes
out=ROOT/'build/material-ao-fixture';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
n=Nodes('Original cavity field');p=n.node('ShaderNodeTexCoord').outputs['Object'];x,y,z=n.split(p)
n.channel('micro_ao',n.ramp(x,-.1,.1,.35,.85));mat=n.finish((.1,.08,.05),.8,0)
bpy.ops.mesh.primitive_plane_add(size=1);o=bpy.context.object;o.name='Cavity plane';o['asset_set']='Cavity';o.data.materials.append(mat);o.data.uv_layers.active.name='BakeUV'
for uv in o.data.uv_layers.active.data:uv.uv=uv.uv*.8+Vector((.1,.1))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
shutil.copyfile(out/'source.blend',out/'high.blend')
for enabled in (False,True):
    cfg=out/'config.py';cfg.write_text('BAKE_POLICY='+repr(dict(cage_m=.003,ray_distance_m=.025,**({'material_ao_channel':'micro_ao'} if enabled else {}))))
    target=out/('material' if enabled else 'default')
    sys.argv=['bake.py','--','--low',str(out/'source.blend'),'--high',str(out/'high.blend'),'--out',str(target),'--asset','Cavity','--config',str(cfg),'--size','64','--samples','8']
    runpy.run_path(str(ROOT/'kit/bake.py'),run_name='__main__')
a=np.array(Image.open(out/'default/T_Cavity_ORM.png'))[:,:,0]/255
b=np.array(Image.open(out/'material/T_Cavity_ORM.png'))[:,:,0]/255
assert a[32,18]>.98 and a[32,46]>.98
assert abs(b[32,18]-.35)<.025 and abs(b[32,46]-.85)<.025,(b[32,18],b[32,46])
print('PASS: default geometric AO unchanged; material visibility .35/.85 survives actual bake and ORM packing')
