"""Actual face/pole frames against the road grammar, independent of roundtrip.

This checks the authored lane/approach semantics and a conservative horizontal
20-degree view cone at the stop bar. It is not a traffic engineering approval.
"""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from layout import SITES
from plan import LANE,xy

def run():
 rows=[]
 for seed,site in SITES.items():
  bpy.ops.wm.open_mainfile(filepath=str(Path(f'build/Signals-{seed}.blend').resolve()));bpy.context.view_layer.update();reg=json.loads(Path(f'build/Signals-{seed}-components.json').read_text());faces=[];poles=[];primary={t:[] for t in site.approaches}
  for ob in bpy.context.scene.objects:
   if ob.type=='MESH' and ob.data.attributes.get('Construction'):
    attr=ob.data.attributes['Construction'];names={reg.get(str(v.value),'') for v in attr.data}
    if any(n.startswith(('Tapered shaft','Steel strain pole')) for n in names):poles.append(ob.name)
   if not ob.get('part_kind','').startswith('Head_') or '__Near' in ob.name:continue
   direction=ob.matrix_world.to_3x3()@Vector((0,-1,0));direction.z=0;direction.normalize()
   port=max(range(4),key=lambda t:direction.dot(Vector(xy(0,1,t*90))))
   assert port in site.approaches,('Face aims toward a missing branch',seed,ob.name,port)
   lens=next(o for o in ob.children if o.get('signal_lens'));pts=[lens.matrix_world@v.co for v in lens.data.vertices];point=sum(pts,Vector())/len(pts)
   c,s=math.cos(-port*math.pi/2),math.sin(-port*math.pi/2);transverse=point.x*c-point.y*s
   candidates=[-LANE/2]
   if (site.ns if port%2==0 else site.ew)>=4:
    candidates=[-LANE,-2*LANE,0] if not site.median else [-site.median/2-LANE/2,-site.median/2-1.5*LANE,-site.median/4]
   lane=min(candidates,key=lambda x:abs(x-transverse));driver=Vector(xy(lane,site.stop(port),port*90,1.18));look=driver-point;look.z=0
   angle=math.degrees(direction.angle(look));assert angle<=20.01,('Face outside horizontal view cone',seed,ob.name,angle)
   if any(o.get('signal_kind')=='red' for o in ob.children):primary[port].append(transverse)
   faces.append(dict(head=ob.name,approach=port,actual_lens_center_m=list(point),transverse_m=transverse,selected_lane_center_m=lane,horizontal_angle_at_stop_degrees=angle))
  for port,positions in primary.items():
   assert len(positions)>=2,('Fewer than two circular primary faces',seed,port,positions)
   assert max(positions)-min(positions)>=2.4384-1e-5,('Primary faces less than eight feet apart',seed,port,positions)
  expected=2 if site.diagonal or seed==204 else 4;assert len(poles)==expected,(seed,poles)
  rows.append(dict(seed=seed,measured_pole_meshes=poles,pole_count=len(poles),primary_transverse_positions_m=primary,faces=faces))
 Path('build/layout-check.json').write_text(json.dumps(dict(passed=True,seeds=rows,scope=__doc__),indent=2));print('LAYOUT four road plans: actual poles, existing approach directions and measured face view cones')
if __name__=='__main__':run()
