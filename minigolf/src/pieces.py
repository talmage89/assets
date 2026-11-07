"""Selectable unplaced hole and fixture roots, sharing the course images."""
import json
from pathlib import Path
import bpy
from mathutils import Matrix
from external import share
from tangents import repair

def export(courses):
 root=bpy.data.objects.new('MinigolfPieces',None);bpy.context.collection.objects.link(root);copies=[];seen=set();rows=[]
 for course,plan in courses:
  candidates=[o for o in course.children_recursive if o.get('module_kind')=='hole' or o.get('fixture_kind')]
  for source in candidates:
   kind=source.get('fixture_kind')
   if kind and kind in seen:continue
   if kind:seen.add(kind)
   descendants=[o for o in source.children_recursive if not any(a.get('fixture_kind') for a in ancestors(o,source))] if not kind else list(source.children_recursive)
   descendants=[o for o in descendants if not o.get('fixture_kind')] if not kind else descendants
   mapping={}
   for old in [source]+descendants:
    ob=old.copy();bpy.context.collection.objects.link(ob);mapping[old]=ob;copies.append(ob)
   for old,ob in mapping.items():ob.parent=mapping.get(old.parent,root)
   top=mapping[source];top.matrix_basis=Matrix.Identity(4);top.name='Fixture_'+kind if kind else plan['kind'].title()+'_'+source.name.split('.')[0]
   total=0
   for ob in mapping.values():
    if ob.type=='MESH':ob.data.calc_loop_triangles();total+=len(ob.data.loop_triangles)
   rows.append(dict(root=top.name,kind=kind or 'hole',triangles=total))
 bpy.ops.object.select_all(action='DESELECT');root.select_set(True)
 for ob in copies:ob.select_set(True)
 path=Path('export/MinigolfPieces.gltf')
 options=dict(use_selection=True,export_yup=True,export_apply=True,export_texcoords=True,export_normals=True,export_tangents=True,export_materials='EXPORT',export_extras=True,export_cameras=False,export_lights=False,export_animations=False)
 bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',export_texture_dir='textures',**options);repair(path);share(path)
 mirror=Path('build/embedded/MinigolfPieces.glb');bpy.ops.export_scene.gltf(filepath=str(mirror.resolve()),export_format='GLB',**options);repair(mirror)
 Path('build/pieces.json').write_text(json.dumps(rows,indent=2))
 for ob in reversed(copies):bpy.data.objects.remove(ob,do_unlink=True)
 bpy.data.objects.remove(root,do_unlink=True)

def ancestors(ob,stop):
 q=ob.parent
 while q and q!=stop:yield q;q=q.parent
