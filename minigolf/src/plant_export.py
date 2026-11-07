"""Native planted landscape as a shared-image, instanced glTF companion.

Construction stays independently budgeted. This component contains only site
plants; the surrounding town, cars, poles and distant trees stay presentation.
"""
import json,sys,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
import context
from plan import generate
from external import share
from tangents import repair
from preserve import check

def main():
 check()
 for seed,kind in ((71,'classic'),(92,'adventure')):
  bpy.ops.wm.read_factory_settings(use_empty=True);p=generate(seed,kind);proof=context.make(p,plants_only=True)
  root=bpy.data.objects.new('Landscape_'+str(seed),None);bpy.context.collection.objects.link(root);root['seed']=seed;root['component']='optional_native_landscape';root['units']='meters'
  for ob in list(bpy.context.scene.objects):
   if ob.type=='MESH' and ob.parent is None:ob.parent=root
  meshes=[o for o in root.children_recursive if o.type=='MESH'];placed=0;unique={}
  for ob in meshes:ob.data.calc_loop_triangles();placed+=len(ob.data.loop_triangles);unique[ob.data.name]=len(ob.data.loop_triangles)
  path=Path(f'export/Minigolf-{seed}-landscape.gltf');options=dict(export_yup=True,export_apply=True,export_texcoords=True,export_normals=True,export_tangents=True,export_attributes=True,export_materials='EXPORT',export_extras=True,export_cameras=False,export_lights=False,export_animations=False)
  bpy.ops.export_scene.gltf(filepath=str(path.resolve()),export_format='GLTF_SEPARATE',export_texture_dir='plant-images',**options);repair(path);images=share(path)
  mirror=Path('build/embedded')/path.with_suffix('.glb').name;bpy.ops.export_scene.gltf(filepath=str(mirror.resolve()),export_format='GLB',**options);repair(mirror)
  doc=json.loads(path.read_text());proof.update(placed_triangles=placed,unique_mesh_triangles=sum(unique.values()),gltf_bytes=path.stat().st_size,bin_bytes=path.with_suffix('.bin').stat().st_size,images=images,materials=len(doc['materials']),scope=__doc__)
  path.with_suffix('.json').write_text(json.dumps(proof,indent=2));print('PLANT COMPANION',seed,placed,'placed triangles;',sum(unique.values()),'unique;',len(images),'canonical images',flush=True)
 shutil.rmtree('export/plant-images',ignore_errors=True);check()
if __name__=='__main__':main()
