"""Unobscured construction turnarounds from the baked course exports."""
import argparse,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
from render import render_one,views

def main(args):
 seed=71 if args.course=='classic' else 92
 source=Path(f'export/Minigolf-{seed}.gltf');p=json.loads(source.with_suffix('.json').read_text())['plan']
 for view in ('front','side','back','top'):
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
  # Leave the whole parcel, including its below-grade basins, unobstructed.
  # Four outside quads continue the ground without putting a plane over water.
  w,d=p['lot'];x,y=w/2+.002,d/2+.002;r=240
  outer=[(-r,-r,-.02),(r,-r,-.02),(r,r,-.02),(-r,r,-.02)]
  inner=[(-x,-y,-.02),(x,-y,-.02),(x,y,-.02),(-x,y,-.02)]
  mesh=bpy.data.meshes.new('Procedural outside-parcel surround');mesh.from_pydata(outer+inner,[],[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]);mesh.update()
  ob=bpy.data.objects.new(mesh.name,mesh);bpy.context.collection.objects.link(ob)
  mat=bpy.data.materials.new('Neutral matte surround');mat.diffuse_color=(.12,.13,.12,1);mat.use_nodes=True;bsdf=mat.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(.12,.13,.12,1);bsdf.inputs['Roughness'].default_value=.92;mesh.materials.append(mat)
  ctx=dict(scope='Isolated exported construction; optional landscape companion and presentation town omitted for unobscured inspection. Procedural surround is outside the parcel only.',turnaround_recipe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
  shot=views(p)[view]
  if view!='top':
   # Keep even the lowest orthographic ray above grade; otherwise rays start
   # below the surround and expose the sky texture's black lower hemisphere.
   shot=dict(shot,location=(*shot['location'][:2],max(w,d)*.55))
  render_one(args.course+'-'+view,shot,source,p,ctx,args)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--course',choices=('classic','adventure'),required=True);parser.add_argument('--out',default='renders/final');parser.add_argument('--width',type=int,default=1440);parser.add_argument('--samples',type=int,default=32);main(parser.parse_args(sys.argv[sys.argv.index('--')+1:]))
