"""Dense authored parts and additive relief, with immutable finish coordinates."""
import argparse,sys,json
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from kit import weapon as W
import lookdev
p=argparse.ArgumentParser();p.add_argument('--wear',type=float,default=1)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
W.pose(bpy.data.objects['R39Armature'],None,0)
with bpy.data.libraries.load(str(BASE/'build/ak.blend'),link=False) as (src,dst):
 dst.objects=[n for n in src.objects if n.startswith('HIGH_') and not n.startswith('HIGH_SightNumeral')]
for dense in dst.objects:
 name=dense.get('low_target');target=bpy.data.objects.get(name)
 if not target:continue
 if dense.name.removesuffix('.001')=='HIGH_'+name:
  target.data=dense.data.copy();target.vertex_groups.clear()
  vg=target.vertex_groups.new(name=target['bone']);vg.add(list(range(len(target.data.vertices))),1,'REPLACE')
  bpy.data.objects.remove(dense,do_unlink=True)
 else:
  # These are high-only pin, knurl, checkering and stamping surfaces. Keep
  # the target's full backing so every bake ray has a continuous substrate.
  bpy.context.scene.collection.objects.link(dense);dense.parent=target.parent
  dense.hide_render=False;dense.hide_set(False);dense['bone']=target['bone'];dense['asset_set']='R39'
  dense['finish_part']=name;dense['delivery_variant']=target.get('delivery_variant','ak')
  dense['part_name']=name
  if 'bake_only' in dense:del dense['bake_only']
  dense.vertex_groups.clear();vg=dense.vertex_groups.new(name=target['bone']);vg.add(list(range(len(dense.data.vertices))),1,'REPLACE')
  if not dense.data.materials:
   for mat in target.data.materials:dense.data.materials.append(mat)
# A broad machined land has one normal. Weighted bevel normals can leave
# faint triangular interpolation on a triangulated planar side. Correct only
# truly axis-planar faces; retain the small radii and curved collars.
planar={}
for name in ('Sight_RearBlock','GasBlock_Neck'):
 ob=bpy.data.objects[name];normals=[r.vector.copy() for r in ob.data.corner_normals];count=0
 for face in ob.data.polygons:
  if abs(face.normal.x)>.999999 or (name=='Sight_RearBlock' and abs(face.normal.y)<1e-6 and abs(face.normal.x)>.7 and face.area>20e-6):
   for i in face.loop_indices:normals[i]=face.normal.copy();count+=1
 ob.data.normals_split_custom_set(normals);planar[name]=count
print('PLANAR LAND CORNERS',planar,flush=True)
records=lookdev.assign(a.wear)
# Retain each high skin and its fine additive relief in one projection owner.
# This permits the existing kit's named static isolation without creating a
# second projection implementation or projecting wood onto a sight cheek.
groups={}
for ob in list(bpy.context.scene.objects):
 if ob.type=='MESH' and ob.get('finish_part'):groups.setdefault(ob['finish_part'],[]).append(ob)
for name,extras in groups.items():
 target=bpy.data.objects[name];bpy.ops.object.select_all(action='DESELECT')
 target.hide_set(False);target.select_set(True)
 for ob in extras:ob.hide_set(False);ob.select_set(True)
 bpy.context.view_layer.objects.active=target;bpy.ops.object.join()
bpy.context.scene['stage']='Dense original finish source / immutable rest attributes'
bpy.ops.wm.save_as_mainfile(filepath=str(BASE/'build/delivery/high.blend'))
(BASE/'build/delivery/finishes.json').write_text(json.dumps(records,indent=2))
print('HIGH FINISHES',len(records),flush=True)
