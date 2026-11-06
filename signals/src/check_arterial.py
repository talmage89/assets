"""Actual imported arterial surface probes, independent of export serialization."""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from ground.src.junction_surfaces import lanes
from layout import SITES
from plan import xy
from kit.gltf import GLB

def main():
 path=ROOT/'ground/export/ArterialSites.glb';bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path))
 bpy.context.view_layer.update();sc=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();rows=[]
 for seed,site in SITES.items():
  rt=bpy.data.objects['Junction_'+str(seed)];meshes=[o for o in rt.children_recursive if o.type=='MESH']
  bpy.context.view_layer.update()
  samples=[]
  def probe(point,label,expect):
   origin=rt.matrix_world@Vector(point);origin.z=2;ok,hit,n,index,ob,_=sc.ray_cast(dg,origin,Vector((0,0,-1)))
   assert ok,(seed,label,'missing surface')
   material=ob.data.materials[ob.data.polygons[index].material_index]
   assert material.name.startswith(expect),(seed,label,material.name,expect)
   samples.append(dict(label=label,point_m=list(hit),material=material.name,surface_normal=list(n)))
  for turn in site.approaches:
   stop=site.stop(turn)
   for c in lanes(site.data(),turn):
    for dx,dy in ((-.9144,0),(.9144,0),(0,-.9144),(0,.9144)):
     probe(xy(c+dx,stop+3+dy,turn*90),'loop sealed edge','Arterial loop seal')
    lead=stop+3.24+c*.045
    probe(xy((-site.half(turn)-.4572+c-.9144)/2,lead,turn*90),'loop lead-in','Arterial loop seal')
   probe(xy(-site.half(turn)-.2,stop+2.5,turn*90),'pull-box lid','Arterial loop seal')
   if turn==site.approaches[seed%len(site.approaches)]:probe(xy(-site.half(turn)+1.1,stop+18,turn*90),'utility wearing patch','Arterial dry asphalt')
  triangles=sum(len(ob.data.polygons) for ob in meshes)
  rows.append(dict(seed=seed,triangles=triangles,probes=samples))
 g=GLB(path);polished=[m for m in g.json['materials'] if m['name'].startswith('Arterial tire-polished')];dry=[m for m in g.json['materials'] if m['name'].startswith('Arterial dry')]
 assert polished and dry
 assert all(abs(m['pbrMetallicRoughness']['roughnessFactor']-.74)<1e-6 for m in polished)
 assert all(abs(m['pbrMetallicRoughness']['roughnessFactor']-.96)<1e-6 for m in dry)
 result=dict(passed=True,source=str(path.relative_to(ROOT)),bytes=path.stat().st_size,seeds=rows,scope='Downward surface rays on imported GLB at loop quadrants, lead-ins, pull-box lids and utility repairs; actual material responses, counts and hit coordinates. Does not certify electrical operation.')
 Path('build/arterial-check.json').write_text(json.dumps(result,indent=2));print('ARTERIAL',sum(len(r['probes']) for r in rows),'actual surface hits;',[(r['seed'],r['triangles']) for r in rows])
if __name__=='__main__':main()
