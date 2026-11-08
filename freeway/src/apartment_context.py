"""Local distance copy of the library's 1967 garden-apartment construction.

Only this worktree's freeway cache is written. Native house tiles stay shared;
this is a context adapter, not a new apartment-family delivery.
"""
import sys,math
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'apartments/src'),str(ROOT)]
from plans import garden
from buildings import garden_building
from geometry import ROLES
from kit.tiling import material,world_uv
from kit.model import apply
bpy.ops.wm.read_factory_settings(use_empty=True)
p=garden(301);root=garden_building(p).root
mats={}
for role,name,folder in [('Siding','HouseSiding','houses/textures/ship'),('Shingles','RanchRoof','houses/textures/ranch-ship'),('Veneer','RanchBrick_red','houses/textures/ranch-ship'),('Concrete','HouseConcrete','houses/textures/ship'),('Trim','HouseTrim','houses/textures/ship')]:
 mats[role]=material(name,ROOT/folder,tint=True)
m=bpy.data.materials.new('Freeway apartment distance glazing');m.use_nodes=True
m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.018,.027,.029,1)
m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.24;mats['Glass']=m
parts=[o for o in bpy.context.scene.objects if o.type=='MESH']
for ob in parts:
 apply(ob)
 for i,old in enumerate(list(ob.data.materials)):
  role=old.name.split('ApartmentsForm_')[-1].split('.')[0]
  if role in mats:ob.data.materials[i]=mats[role]
 if not ob.data.uv_layers:world_uv(ob,2.4384)
bpy.ops.object.select_all(action='DESELECT')
for ob in parts:ob.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();ob=bpy.context.object;ob.name='Native garden apartment context'
# A distance building retains window apertures, external stairs and roof form.
# It is instanced as one static mesh; no gameplay door pivots are promised.
ob.parent=None;ob.matrix_world.identity()
import bmesh
bm=bmesh.new();bm.from_mesh(ob.data)
bad=[f for f in bm.faces if f.calc_area()<1e-12]
if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
# The library builder supplies staging charts before its own finish pass.
# This local adapter uses metric tiles and the painted trim strip explicitly,
# including bevel triangles whose inherited staging projection had collapsed.
ob.data.update();uv=ob.data.uv_layers.active
colors=ob.data.color_attributes.get('Tint')
for face in ob.data.polygons:
 name=ob.data.materials[face.material_index].name
 if colors and any(q in name for q in ('Brick','Concrete','Roof')):
  factor=(.90,.92,.87,1) if 'Brick' in name else (.84,.85,.84,1) if 'Concrete' in name else (.88,.82,.72,1)
  for vi in face.vertices:colors.data[vi].color=factor
 if name.startswith('Freeway apartment'):continue
 axes=[k for k in range(3) if k!=max(range(3),key=lambda k:abs(face.normal[k]))]
 pts=[ob.data.vertices[ob.data.loops[li].vertex_index].co for li in face.loop_indices]
 coverage=4.8768 if 'Roof' in name else 1.2192 if 'Brick' in name else 2.4384
 if 'Trim' in name:
  center=sum(v[axes[1]] for v in pts)/len(pts);span=max(1.,max(v[axes[1]] for v in pts)-min(v[axes[1]] for v in pts))
  coords=[(v[axes[0]]/4,.938+(v[axes[1]]-center)*.06/span) for v in pts]
 else:coords=[(v[axes[0]]/coverage,v[axes[1]]/coverage) for v in pts]
 for li,co in zip(face.loop_indices,coords):uv.data[li].uv=co
path=Path('build/context/Apartment.glb');path.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLB',use_selection=True,export_extras=True,export_animations=False,export_skins=False,export_tangents=False,export_all_vertex_colors=False,export_vertex_color='NAME',export_vertex_color_name='Tint')
print('NATIVE APARTMENT CONTEXT',sum(len(f.vertices)-2 for f in ob.data.polygons),flush=True)
