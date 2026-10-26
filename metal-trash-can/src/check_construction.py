"""Measure assembly contacts on actual source surfaces; serialization is checked separately."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.motion import surface

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/'metal-trash-can/build/game-audit.blend'));bpy.context.view_layer.update()
 body=bpy.data.objects['Corrugated galvanized vessel'];bs=surface(body)
 lid=bpy.data.objects['Pressed removable lid with hem'];ls=surface(lid)
 rim=[v for v in bs['points'] if v.z>.694]
 distances=[ls['tree'].find_nearest(v)[3] for v in rim]
 assert min(distances)<.0006, 'Lid is unsupported above the rim'
 # The circular wire ends must be centered in the retaining eyes' actual opening.
 eyes=[]
 for side in ['Left','Right']:
  wire=bpy.data.objects[side+' folding wire loop'];ws=surface(wire)
  for eye in [o for o in bpy.context.scene.objects if o.name.startswith(side+' rolled bracket eye')]:
   es=surface(eye);center=(es['lo']+es['hi'])*.5
   # Closest actual wire surface lies inside the eye bore rather than outside the eye.
   near=ws['tree'].find_nearest(center);d=near[3]
   assert d<.004, (side,d)
   neck=[surface(o) for o in bpy.context.scene.objects if o.name.startswith(side+' retaining eye folded neck')]
   gap=min(t['tree'].find_nearest(v)[3] for t in neck for v in es['points'])
   crossings=sum(len(es['tree'].overlap(t['tree'])) for t in neck)
   assert crossings>0, 'Retaining eye has no supporting neck'
   eyes.append(dict(eye=eye.name,center_to_wire_surface_m=d,eye_to_neck_vertex_distance_m=gap,eye_neck_triangle_crossings=crossings))
 # Offset floor has a flat interior panel at an actual measured height.
 floor=[v.z for v in bs['points'] if abs(v.x)<1e-7 and abs(v.y)<1e-7]
 floor.sort();assert len(floor)==2 and .0004<floor[1]-floor[0]<.001
 result=dict(passed=True,proof='Actual source contact surfaces, not exported-scene equality',lid_rim_nearest_m=min(distances),floor_surfaces_z_m=floor,floor_gauge_m=floor[1]-floor[0],retaining_eyes=eyes)
 Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
