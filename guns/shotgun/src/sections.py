"""Actual source triangle/plane section intersections, in visual asset mm."""
import sys,json
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[3]));sys.path.insert(0,str(Path(__file__).parent))
from kit import weapon as W
def extract(ob,y):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles()
 pts=[ev.matrix_world@v.co for v in m.vertices];segments=[]
 for f in m.loop_triangles:
  cross=[]
  for a,b in zip(f.vertices,(*f.vertices[1:],f.vertices[0])):
   p,q=pts[a],pts[b]
   if (p.y-y)*(q.y-y)<0:
    v=p+(q-p)*((y-p.y)/(q.y-p.y));cross.append([v.x*1000,v.z*1000])
  if len(cross)==2:segments.append(cross)
 ev.to_mesh_clear();return segments
def main():
 base=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(base/'build/shotgun.blend'))
 arm=bpy.data.objects['ShotgunArmature'];W.pose(arm,'Idle',0)
 rows=[]
 for region,ys,prefixes in [('Wrist',[-85,-70,-55],['Stock']),('Comb',[-210,-175,-148],['Stock']),
  ('Forend',[340,385,430],['Forend_Wood','Forend_Sleeve','Magazine_Tube']),
  ('Receiver',[50,100,165],['Receiver']),('Barrel / tube at ring',[529],['Barrel','Magazine_Tube','Barrel_Ring','Ring_Bridge'])]:
  for y in ys:
   parts={o.name:extract(o,(y+55)*.001) for o in bpy.context.scene.objects if o.type=='MESH' and o.name in prefixes}
   flat=[p for segs in parts.values() for s in segs for p in s]
   dims=[max(p[k] for p in flat)-min(p[k] for p in flat) for k in range(2)]
   rows.append(dict(region=region,station_mm=y+55,source_station_mm=y,parts=parts,width_mm=dims[0],height_mm=dims[1]))
 (base/'build/sections.json').write_text(json.dumps(rows,indent=2));print('MEASURED SECTIONS',len(rows))
if __name__=='__main__':main()
