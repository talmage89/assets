"""Measured budget, scale, state and source/GLB serialization audit.

Physical clearance measurements are reported separately from raw-export and
reimport serialization. Raw external glTF UV/map tests live in check_delivery.
"""
import sys,json,math,hashlib
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.gltf import GLB
from kit import motion
from plan import *
from layout import SITES
from preserve import run as preserve
def bounds(o):
 pts=[m.matrix_world@v.co for m in [o,*o.children_recursive] if m.type=='MESH' for v in m.data.vertices]
 return np.min(pts,axis=0),np.max(pts,axis=0)
def triangles(o):return sum(len(m.data.polygons) for m in [o,*o.children_recursive] if m.type=='MESH')
def snapshot():
 bpy.context.view_layer.update()
 return {o.name:dict(matrix=np.array(o.matrix_world),triangles=len(o.data.polygons) if o.type=='MESH' else None,positions=np.array([o.matrix_world@v.co for v in o.data.vertices]) if o.type=='MESH' else None) for o in bpy.context.scene.objects}
def main():
 preserve();rows=[]
 for seed in PLANS:
  source=Path(f'build/Signals-{seed}.blend');glb=source.with_suffix('.glb');meta=json.loads(source.with_suffix('.json').read_text())
  bpy.ops.wm.open_mainfile(filepath=str(source.resolve()));expected=snapshot()
  g=GLB(glb)
  from PIL import Image
  import io
  offmat=next(m for m in g.json['materials'] if m['name']=='SharedLens_Off')
  litmat=next(m for m in g.json['materials'] if m['name']=='SharedLens_Lit')
  index=offmat['pbrMetallicRoughness']['baseColorTexture']['index'];imageindex=g.json['textures'][index]['source']
  offpixels=np.array(Image.open(io.BytesIO(g.image(imageindex))).convert('RGBA'))
  assert max(offmat['pbrMetallicRoughness']['baseColorFactor'][:3])<=.02,('Off-state factor lost',seed)
  assert litmat.get('emissiveTexture') and max(litmat.get('emissiveFactor',[0]))>0
  rawtri=sum(len(g.accessor(p['indices']))//3 for n in g.json['nodes'] if 'mesh' in n for p in g.json['meshes'][n['mesh']]['primitives'])
  assert rawtri==meta['equipment_triangles'],(seed,rawtri,meta['equipment_triangles'])
  states=[o for o in bpy.context.scene.objects if o.get('signal_lens')]
  assert len({o.name for o in states})==len(states)
  budget=[]
  for o in bpy.context.scene.objects:
   kind=o.get('part_kind','')
   count=triangles(o)
   limit=1500 if kind.startswith('Head_') else 14000 if kind=='MastArm' else 4000 if kind in ('Pedestal','PushButtonPost') else 3000 if kind=='Cabinet' else None
   if limit:assert count<=limit,(o.name,count,limit);budget.append(dict(name=o.name,kind=kind,triangles=count,limit=limit))
  clear=[]
  for o in bpy.context.scene.objects:
   if not o.get('part_kind','').startswith('Head_') or '__Near' in o.name:continue
   lo,hi=bounds(o)
   # Highest asphalt crown under this footprint is conservative for the actual road.
   pavement=.012
   clearance=float(lo[2]-pavement)
   assert clearance>=5.334,(o.name,clearance)
   registry=json.loads(source.with_name(source.stem+'-components.json').read_text())
   housing=[]
   for m in o.children_recursive:
    if m.type!='MESH':continue
    attr=m.data.attributes.get('Construction')
    for f in m.data.polygons:
     if attr and registry.get(str(attr.data[f.index].value),'').startswith(('Top mounting stem','Indexed top boss')):continue
     housing.extend(m.matrix_world@m.data.vertices[i].co for i in f.vertices)
   housingtop=max(p.z for p in housing)
   assert housingtop-pavement<=7.80288,(o.name,housingtop)
   assert abs(o.location.z)>0 # physical hinge frame
   clear.append(dict(head=o.name,underside_m=float(lo[2]),pavement_bound_m=pavement,clearance_m=clearance))
  covers=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.endswith('_Cover')]
  # Covers join fixed construction, so independently measure the actual LED card.
  radii=[]
  for o in states:
   if o.get('signal_kind') in ('red','yellow','green','red_arrow','yellow_arrow','green_arrow'):
    v=o.data.vertices;w=max(x.co.x for x in v)-min(x.co.x for x in v);h=max(x.co.z for x in v)-min(x.co.z for x in v)
    assert abs(w-.3048)<1e-6 and abs(h-.3048)<1e-6;(radii.append(w))
  # Door's outward rotation is signed toward its actual front, negative local Y.
  door=bpy.data.objects.get('Controller__Door');assert door and list(door['range_degrees'])==[-110,0]
  door_rest=door.matrix_basis.copy();door.rotation_euler.z=math.radians(-95);bpy.context.view_layer.update()
  moving=next(m for m in door.children if m.type=='MESH');fixed=next(m for m in door.parent.children if m.type=='MESH')
  depth,crossings=motion.penetration(motion.surface(moving),motion.surface(fixed),.001)
  assert depth<.001,('Cabinet leaf at 95 degrees',depth)
  door.matrix_basis=door_rest
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb.resolve()));actual=snapshot()
  maxerr=0
  for name,row in expected.items():
   assert name in actual,('Lost named node',name)
   if row['positions'] is None:
    assert np.max(np.abs(row['matrix']-actual[name]['matrix']))<2e-5,('Pivot frame changed',name)
    continue
   m=bpy.data.objects[name];m.data.calc_loop_triangles();assert len(m.data.loop_triangles)==row['triangles'],name
   # GLB splits vertices along normals/material boundaries. Every imported point
   # must lie within 20 microns of a source point, and conversely.
   from mathutils.kdtree import KDTree
   kd=KDTree(len(row['positions']))
   for i,p in enumerate(row['positions']):kd.insert(p,i)
   kd.balance()
   errs=[kd.find(p)[2] for p in actual[name]['positions']];
   if max(errs)>.00002:print('ROUNDTRIP FAILURE',seed,name,max(errs),flush=True)
   maxerr=max(maxerr,max(errs))
   kd=KDTree(len(actual[name]['positions']))
   for i,p in enumerate(actual[name]['positions']):kd.insert(p,i)
   kd.balance();maxerr=max(maxerr,max(kd.find(p)[2] for p in row['positions']))
  assert maxerr<.00002,(seed,maxerr)
  normal_error=max(float(np.max(np.abs(np.linalg.norm(g.accessor(p['attributes']['NORMAL']),axis=1)-1))) for m in g.json['meshes'] for p in m['primitives'])
  assert normal_error<1e-4,(seed,'Normals',normal_error)
  assert all(np.isfinite(g.accessor(p['attributes']['POSITION'])).all() for mesh in g.json['meshes'] for p in mesh['primitives'])
  row=dict(seed=seed,passed=True,equipment_triangles=rawtri,materials=len(g.json['materials']),primitives=sum(len(g.json['meshes'][n['mesh']]['primitives']) for n in g.json['nodes'] if 'mesh' in n),max_normal_length_error=normal_error,glb_bytes=glb.stat().st_size,named_lenses=len(states),lens_diameter_measured_m=[min(radii),max(radii)],budget=budget,overhead_clearances=clear,max_roundtrip_position_error_m=maxerr,cabinet_open95_penetration_m=depth)
  rows.append(row);print('CHECK',seed,rawtri,'triangles',len(states),'states',maxerr,'m roundtrip')
 Path('build/checks.json').write_text(json.dumps(dict(passed=True,scope='Budgets, dimensions, named states, clearance bound, outward door pose, raw and fresh-import serialization. External map/UV audit is in delivery-check.json.',seeds=rows),indent=2))
if __name__=='__main__':main()
