"""Arrange our verified module GLB into the four-chair dining set.

Mesh and texture data remain linked, preserving one chair geometry allocation
and one three-map atlas. This script imports only our own generated GLB.
"""
import argparse,sys,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
import bpy,numpy as np
from mathutils import Vector
from kit.studio import display_instances
from kit.gltf import GLB
from kit.glb_textures import compact
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--report',required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();out=Path(a.out).resolve()
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source))
for ob in list(bpy.context.scene.objects):
 if ob.type=='MESH' and 'asset_set' not in ob:bpy.data.objects.remove(ob,do_unlink=True)
closed=bpy.data.objects['Umbrella_Closed']
for ob in list(closed.children_recursive)[::-1]+[closed]:bpy.data.objects.remove(ob,do_unlink=True)
chair=bpy.data.objects['Chair'];chair.location=(-.43,-.97,0);chair.rotation_euler.z=math.pi
instances=display_instances([dict(source='Chair',name='Chair_2',location=(.43,-.97,0),rotation_degrees=(0,0,180)),dict(source='Chair',name='Chair_3',location=(-.43,.97,0)),dict(source='Chair',name='Chair_4',location=(.43,.97,0))])
bpy.data.objects['Chaise_Backrest'].rotation_euler.x=math.radians(45)
bpy.context.view_layer.update();bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_apply=False,export_texcoords=True,export_normals=True,export_tangents=True,export_materials='EXPORT',export_image_format='AUTO',export_skins=False,export_animations=False,export_extras=True,export_cameras=False,export_lights=False)
compact(out,Path(a.report).parent)
original=GLB(source);g=GLB(out);d=g.json
errors=[]
chairs=[n for n in d['nodes'] if n.get('extras',{}).get('asset_set')=='Chair' and 'mesh' in n]
mesh_indices=[n['mesh'] for n in chairs]
if len(chairs)!=4 or len(set(mesh_indices))!=1:errors.append('Four chair nodes must share one glTF mesh')
image_hashes=lambda glb:sorted(hashlib.sha256(glb.image(i)).hexdigest() for i in range(len(glb.json.get('images',[]))))
if image_hashes(original)!=image_hashes(g):errors.append('Assembly altered the shared atlas image bytes')
if len(d.get('materials',[]))!=1 or len(d.get('images',[]))!=3:errors.append('Assembly must use one material / three maps')
unique_triangles=sum(d['accessors'][p['indices']]['count']//3 for m in d['meshes'] for p in m['primitives'])
drawn_triangles=sum(sum(d['accessors'][p['indices']]['count']//3 for p in d['meshes'][n['mesh']]['primitives']) for n in d['nodes'] if 'mesh' in n)
# Raw glTF position transforms independently prove actual ground support per root.
roots={n.get('name'):i for i,n in enumerate(d['nodes']) if n.get('name') in ('Chair','Chair_2','Chair_3','Chair_4','Table','Chaise','Umbrella_Open')}
ground={}
for name,index in roots.items():
 selected=[]
 for j,node in enumerate(d['nodes']):
  ancestor=j
  while ancestor is not None and ancestor!=index:ancestor=g.parents.get(ancestor)
  if ancestor==index and 'mesh' in node:
   for primitive in d['meshes'][node['mesh']]['primitives']:
    v=g.accessor(primitive['attributes']['POSITION']);h=np.c_[v,np.ones(len(v))];selected.append((g.world(j)@h.T).T[:,:3])
 points=np.concatenate(selected);ground[name]=float(points[:,1].min()) # glTF +Y is vertical.
 if abs(ground[name])>1e-5:errors.append(name+' is not grounded')
# Reimport the assembly and measure real triangle clearance between each chair
# and table. Deliberate fabric/metal contacts inside modules are irrelevant here.
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(out));bpy.context.view_layer.update()
from kit.motion import surface,penetration
objects=list(bpy.context.scene.objects);table=next(o for o in objects if o.type=='MESH' and o.get('asset_set')=='Table');ts=surface(table)
clearance=[]
for ob in objects:
 if ob.type=='MESH' and ob.get('asset_set')=='Chair':
  depth,crossings=penetration(surface(ob),ts,.0005);clearance.append(dict(chair=ob.name,table_penetration_m=depth,triangle_crossings=crossings))
  if depth>.0005:errors.append(ob.name+' intersects table')
umbrella_checks=[]
for ob in objects:
 if ob.type=='MESH' and ob.get('asset_set')=='Umbrella_Open':
  depth,crossings=penetration(surface(ob),ts,.0005);umbrella_checks.append(dict(part=ob.name,table_penetration_m=depth,triangle_crossings=crossings))
  if depth>.0005:errors.append(ob.name+' intersects table')
report=dict(table_umbrella_clearance=umbrella_checks,passed=not errors,errors=errors,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),assembly=str(out),bytes=out.stat().st_size,chair_nodes=len(chairs),unique_chair_meshes=len(set(mesh_indices)),unique_triangles=unique_triangles,drawn_triangles=drawn_triangles,materials=1,images=3,texture_bytes_unchanged=image_hashes(original)==image_hashes(g),root_ground_y_m=ground,chair_table_clearance=clearance)
Path(a.report).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if errors:raise RuntimeError('Assembly delivery checks failed')
