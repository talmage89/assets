"""Independent delivered cart checks: shared texture bytes, footprint and hinges."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 paths=[ROOT/'trash-cart/export'/n for n in ['TrashCart.glb','TrashCartRecycling.glb']]
 digests=[];rows=[]
 for path in paths:
  glb=GLB(path);digests.append([hashlib.sha256(glb.image(i)).hexdigest() for i in range(3)])
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path));bpy.context.view_layer.update()
  sc=bpy.context.scene;mesh=[o for o in sc.objects if o.type=='MESH' and 'asset_set' in o]
  assert len(mesh)==4, 'Expected static body plus lid and two wheels'
  assert not any(o.name.startswith('AtlasBlue') for o in sc.objects),'Atlas staging node leaked'
  root=bpy.data.objects['TrashCart'];assert root.matrix_world.translation.length<1e-6
  points=[o.matrix_world@v.co for o in mesh for v in o.data.vertices]
  ground=[v for v in points if abs(v.z)<1e-6]
  assert len(ground)>=4
  midpoint=[(min(v[i] for v in ground)+max(v[i] for v in ground))/2 for i in (0,1)]
  assert max(map(abs,midpoint))<1e-5,('Footprint origin',midpoint)
  expected={'Lid':(0,.391075,1.032),'Wheel_Left':(-.305,.314925,.127),'Wheel_Right':(.305,.314925,.127)}
  for name,pos in expected.items():
   pivot=bpy.data.objects[name];assert (pivot.matrix_world.translation-Vector(pos)).length<1e-6
   assert pivot['pivot_axis']=='X'
  wheel_errors=[]
  for name in ['Wheel_Left','Wheel_Right']:
   pivot=bpy.data.objects[name]
   coords=[v.co for ob in pivot.children if ob.type=='MESH' for v in ob.data.vertices]
   radius=max(math.hypot(v.y,v.z) for v in coords);wheel_errors.append(abs(radius-.127))
   assert abs(radius-.127)<1e-6
   pivot.rotation_mode='XYZ';pivot.rotation_euler.x=math.radians(73)
  lid=bpy.data.objects['Lid'];part=next(o for o in lid.children if o.type=='MESH')
  before=[part.matrix_world@v.co for v in part.data.vertices];hinge=lid.matrix_world.translation.copy()
  lid.rotation_mode='XYZ';lid.rotation_euler.x=math.radians(-100);bpy.context.view_layer.update()
  after=[part.matrix_world@v.co for v in part.data.vertices]
  travel=max((b-a).length for a,b in zip(before,after))
  assert travel>.9 and (lid.matrix_world.translation-hinge).length<1e-6
  radius_error=max(abs((b-hinge).length-(a-hinge).length) for a,b in zip(before,after))
  assert radius_error<1e-6
  rows.append(dict(file=path.name,meshes=len(mesh),ground_midpoint_m=midpoint,wheel_radius_errors_m=wheel_errors,lid_vertex_travel_m=travel,lid_radius_error_m=radius_error))
 assert digests[0]==digests[1], 'Variants do not embed byte-identical atlas images'
 result=dict(passed=True,texture_sha256=digests[0],variants=rows)
 Path(a.out).write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

if __name__=='__main__':main()
