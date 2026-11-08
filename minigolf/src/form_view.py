"""Workbench silhouette review from the exported original geometry."""
import sys,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
from render import scene,views,camera
if __name__=='__main__':
 for seed in (71,92):
  import json,context
  bpy.ops.wm.open_mainfile(filepath=str(Path('build/source-form.blend').resolve()))
  root=bpy.data.objects['Course_'+str(seed)];keep={root,*root.children_recursive}
  for ob in list(bpy.context.scene.objects):
   if ob not in keep:bpy.data.objects.remove(ob,do_unlink=True)
  from plan import generate
  p=generate(seed,'classic' if seed==71 else 'adventure');context.make(p)
  for mat in bpy.data.materials:
   if mat.use_nodes:
    bsdf=mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:mat.diffuse_color=bsdf.inputs['Base Color'].default_value
  sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=1200;sc.render.resolution_y=800;sc.render.resolution_percentage=100
  sc.display.shading.light='STUDIO';sc.display.shading.studiolight_rotate_z=.4;sc.display.shading.color_type='MATERIAL';sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True;sc.display.shading.cavity_type='BOTH';sc.display.shading.curvature_ridge_factor=1.4;sc.display.shading.curvature_valley_factor=1.1
  sc.world=bpy.data.worlds.new('Form sky');sc.world.color=(.18,.18,.18)
  for name in ('above','hero','waterfall','fixture','clubhouse'):
   if seed==71 and name not in ('above','hero'):continue
   cam=camera(views(p)[name]);out=Path('renders/form')/(p['kind']+'-'+name+'.png');out.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(out.resolve());bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
