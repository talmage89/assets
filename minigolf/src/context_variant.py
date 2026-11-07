"""Generate an additional native Boxwood seed without editing its family."""
import argparse,runpy,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--seed',type=int,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=args.out.resolve();out.parent.mkdir(parents=True,exist_ok=True)
sys.argv=[str(ROOT/'shrubs/src/build.py'),'--','--species','boxwood','--seed',str(args.seed),'--out',str(out.with_suffix('.blend'))]
runpy.run_path(str(ROOT/'shrubs/src/build.py'),run_name='__main__')
root=bpy.data.objects['Boxwood'];root['geometry_seed']=args.seed
# Native card/wood rectangles are shared across growth seeds. Bind the actual
# shipped leaf and wood materials, including their ORM swizzles and alpha.
source=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'shrubs/export/Shrubs.glb'))
added=set(bpy.context.scene.objects)-source
canonical=next(o for o in added if o.name.startswith('Boxwood') and o.type=='EMPTY')
parts=[o for o in canonical.children_recursive if o.type=='MESH']
leaf=next(o.data.materials[0] for o in parts if 'leaf' in o.name.lower());wood=next(o.data.materials[0] for o in parts if 'wood' in o.name.lower())
for ob in source:
 if ob.type=='MESH':ob.data.materials.clear();ob.data.materials.append(leaf if 'leaf' in ob.name.lower() else wood)
for ob in added:bpy.data.objects.remove(ob,do_unlink=True)
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_yup=True,export_apply=True,export_normals=True,export_tangents=True,export_extras=True,export_cameras=False,export_lights=False)
