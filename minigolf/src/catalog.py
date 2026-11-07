"""Arrange the actual exported modules for final fixture and hole-kind sheets."""
import argparse,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
from plan import generate
from render import render_one
from external import bundle

def main(args):
 source=Path('export/MinigolfPieces.gltf')
 for kind in ([args.kind] if args.kind else ('fixtures','holes')):
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
  modules=[o for o in bpy.context.scene.objects if o.parent and o.parent.name=='MinigolfPieces'];keep=[]
  if kind=='fixtures':keep=sorted([o for o in modules if o.get('fixture_kind')],key=lambda o:o.name)
  else:
   seen=set()
   for ob in modules:
    feature=ob.get('feature')
    if ob.get('module_kind')=='hole' and feature not in seen:seen.add(feature);keep.append(ob)
  for ob in modules:
   if ob not in keep:
    for child in reversed(list(ob.children_recursive)):bpy.data.objects.remove(child,do_unlink=True)
    bpy.data.objects.remove(ob,do_unlink=True)
  placements=[]
  for i,ob in enumerate(keep):
   ob.location=(((i%5)-2)*6.5,0,0) if kind=='fixtures' else (((i%3)-1)*7.5,(i//3)*11-11,0)
   bpy.context.view_layer.update()
   lowest=min((child.matrix_world@v.co).z for child in ob.children_recursive if child.type=='MESH' for v in child.data.vertices)
   # Graded hole modules retain their authored elevation. Translate the whole
   # module for the sheet, measuring its actual underside rather than guessing.
   if kind=='holes':ob.location.z-=lowest+.04
   placements.append(dict(root=ob.name,feature=ob.get('feature'),fixture=ob.get('fixture_kind'),position=list(ob.location),measured_lowest_before_translation_m=lowest))
  mat=bpy.data.materials.new('Procedural neutral stage');mat.diffuse_color=(.15,.14,.12,1)
  bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.04));bpy.context.object.data.materials.append(mat)
  shot=dict(location=(15,-35,18),target=(0,0,1.8),lens=48,aspect=2.1) if kind=='fixtures' else dict(location=(17,-28,35),target=(0,0,0),ortho=40,lens=45,aspect=1.2)
  render_one(kind+'-sheet',shot,source,generate(92,'adventure'),dict(scope='Actual exported selectable modules, translated only for comparison; holes seated by measured underside on procedural neutral stage',placements=placements,catalog_recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),args)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',default='renders/final');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=32);p.add_argument('--kind',choices=('fixtures','holes'));main(p.parse_args(sys.argv[sys.argv.index('--')+1:]))
