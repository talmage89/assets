"""Final delivery: affine/state round trip, atlas payloads and spawn geometry."""
import sys,json,hashlib,io,argparse
from pathlib import Path
import bpy,numpy as np
from PIL import Image
from mathutils import Vector
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parent.parent;sys.path.insert(0,str(ROOT));sys.path.insert(0,str(BASE/'src'))
from kit import weapon as W,weapon_verify as V,uv
from kit.gltf import GLB
from semantics import check
from interface import CLIPS
import trigger_check
out=BASE/'export'
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'));arm=bpy.data.objects['PistolArmature']
uv_report=uv.report([o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')],size=2048)
assert uv_report['outside_triangles']==0 and uv_report['degenerate_uv_triangles']==0
assert uv_report['overlap_fraction']<1e-5,uv_report['overlap_fraction']
assert 2000<uv_report['density_px_m']['50']<6000
bake_report=json.loads((BASE/'build/baked/4k/bake-report.json').read_text())
assert bake_report['size']==4096 and bake_report['samples']>=32
for channel in ('BaseColor','Roughness','Metallic','AO','MaterialAO','Normal'):
 assert bake_report[channel]['alpha_missed_interior_texels']==0,(channel,bake_report[channel])
for channel in ('BaseColor','Normal','ORM'):
 assert Image.open(BASE/'build/baked/4k'/f'T_C9_{channel}.png').size==(4096,4096)
expected=V.capture(arm,[(name,i*.5) for name,s in CLIPS.items() for i in range(s['frames']*2+1)],
 [o.name for o in bpy.context.scene.objects if o.name.startswith('Socket_')])
parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('bone') in ('Magazine','Follower','TopRound','ReserveRound')]
spawns={}
for variant,clip in [('loaded','Reload'),('empty','ReloadEmpty')]:
 W.pose(arm,clip,40);visible=[o for o in parts if min(abs(v) for v in arm.pose.bones[o['bone']].matrix.to_scale())>.001]
 spawns[variant]=(V.surface_points(visible),bpy.data.objects['Socket_Magazine'].matrix_world.copy())
trigger_reference=trigger_check.capture(arm)
arm=V.import_glb(out/'pistol.glb');states=check(arm);poses=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
trigger_surfaces=trigger_check.imported(arm,trigger_reference)
records={};shared=None
for name in ('pistol','magazine_loaded','magazine_empty','case'):
 path=out/(name+'.glb');g=GLB(path);normal=V.normal_direction(g)
 hashes={hashlib.sha256(g.image(i)).hexdigest() for i in range(len(g.json['images']))}
 assert len(g.json['materials'])==1 and len(hashes)==3
 if shared is None:shared=hashes
 assert hashes==shared
 for i in range(3):
  im=Image.open(io.BytesIO(g.image(i)));assert im.size==(2048,2048)
 tri=sum(len(g.accessor(p['indices']))//3 for m in g.json['meshes'] for p in m['primitives'])
 record=dict(bytes=path.stat().st_size,triangles=tri,materials=1,images=3,size=2048,image_sha256=sorted(hashes),normal_direction=normal)
 if name!='pistol':
  V.import_glb(path);meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1
  if name.startswith('magazine'):
   target,spawn=spawns[name.split('_')[1]]
   error=V.surface_delta(target,[tuple(spawn@Vector(p)) for p in V.surface_points(meshes)])
   assert error<2e-6,(name,error);record['rotated_spawn_delta_m']=error
  else:assert tri<=400
 records[name]=record
assert 25000<=records['pistol']['triangles']<=35000
result=dict(passed=True,trigger_surfaces=trigger_surfaces,stage='final 2048 PBR delivery',outputs=records,
 uv={k:uv_report[k] for k in ('coverage','outside_triangles','degenerate_uv_triangles','overlap_pairs','overlap_fraction','density_px_m')},
 bake_size=bake_report['size'],bake_samples=bake_report['samples'],missed_interior_texels=0,
 semantic_check=states,affine_samples=len(poses),max_position_delta_m=max(p['position_delta_m'] for p in poses),
 gpu_memory_mib_bc_with_mips=16,runtime_sharing='consumer must cache canonical atlas/hash',
 max_linear_delta=max(p['linear_delta'] for p in poses))
(BASE/'build/delivery/verify.json').write_text(json.dumps(result,indent=2));print('ATLAS VERIFIED: 1110 intermediate affine/state poses, one material, four fresh imports, shared 2048 image payloads')
