"""Assemble detail over the reviewed SUV form; supports fast material iteration."""
import argparse,sys,json
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from build import Build
import suv_spec as S


def build(source,out,wear=.65):
 bpy.ops.wm.open_mainfile(filepath=str(Path(source).resolve()));sc=bpy.context.scene
 b=Build.__new__(Build);b.high=sc.get('quality')=='high';b.detail=True;b.wear=wear;b.asset_set=S.ASSET_SET;b.root=bpy.data.objects[S.NAME]
 from suv_finishes import palette,assign
 b.m=palette(wear);assign(b)
 for ob in list(sc.objects):
  if ob.name=='Form cavity closure' or ob.get('part_category') in ['tires','wheels','brakes'] or ob.name.startswith(('Wheel_','Steer_')):bpy.data.objects.remove(ob,do_unlink=True)
 import suv_wheels,suv_interior,suv_underbody,suv_exterior
 suv_wheels.build(b,S);suv_interior.build(b);suv_underbody.build(b);suv_exterior.build(b)
 from suv_mechanics import build as mechanisms
 mechanisms(b)
 from suv_joints import build as joints
 joints(b)
 from suv_construction import fit
 fit(b)
 if not b.high:
  from suv_allocation import remove_hidden_backs,simplify_glazing,simplify_moldings
  sc['concealed_back_allocation']=json.dumps(remove_hidden_backs())
  sc['glass_allocation']=json.dumps(simplify_glazing())
  sc['molding_allocation']=json.dumps(simplify_moldings())
 for m in list(bpy.data.materials):
  if not m.users:bpy.data.materials.remove(m)
 sc['stage']='X220 detail and procedural look-dev checkpoint; UV/bake/export pending'
 bpy.context.view_layer.update()
 # Mesh allocation and axial wheel scaling must precede the final rest-space
 # coordinates. Those operations replace data blocks or move actual vertices.
 for ob in sc.objects:
  if ob.type=='MESH':
   attr=ob.data.attributes.get('VehicleRest') or ob.data.attributes.new('VehicleRest','FLOAT_VECTOR','POINT')
   attr.data.foreach_set('vector',[q for v in ob.data.vertices for q in ob.matrix_world@v.co])
 from suv_weather import edge_attributes,cladding_fasteners,freeze_exposure_normals
 edge_attributes();cladding_fasteners(b.m['cladding']);freeze_exposure_normals()
 Path(out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(out).resolve()))
 counts={};parts={}
 for ob in sc.objects:
  if ob.type=='MESH':
   ob.data.calc_loop_triangles();count=len(ob.data.loop_triangles);parts[ob.name]=count;key=ob['part_category'];counts[key]=counts.get(key,0)+count
 report=dict(triangles=sum(counts.values()),categories=counts,parts=parts,quality=sc['quality'])
 Path(out).with_suffix('.counts.json').write_text(json.dumps(report,indent=2));print('SUV_DETAIL',json.dumps(counts),report['triangles'],flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--wear',type=float,default=.65);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);build(a.source,a.out,a.wear)
