"""Bake manufactured microrelief on the game shell itself, avoiding thin-wall ray crossings.

Structural high/game shells are identical; all fine zinc and pressed bead detail
lives in their shared authored shader height. No reference pixels or normal repair.
"""
import argparse,json,sys,time
from pathlib import Path
import bpy,numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit import gpu
from kit.image_io import write_png

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=32);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/'metal-trash-can/build/finalized.blend'));sc=bpy.context.scene
 sc.render.engine='CYCLES';gpu.enable();sc.cycles.samples=a.samples;sc.cycles.use_denoising=False
 sc.render.bake.use_selected_to_active=False;sc.render.bake.use_clear=True;sc.render.bake.margin=12
 obs=[o for o in sc.objects if o.type=='MESH' and 'asset_set' in o];bpy.ops.object.select_all(action='DESELECT')
 image=bpy.data.images.new('Self surface tangent normal',a.size,a.size,alpha=True,float_buffer=True);image.colorspace_settings.name='Non-Color'
 for ob in obs:
  ob.select_set(True);ob.data.uv_layers.active=ob.data.uv_layers['BakeUV']
  for mat in ob.data.materials:
   nt=mat.node_tree;n=nt.nodes.get('SELF_NORMAL_TARGET') or nt.nodes.new('ShaderNodeTexImage');n.name='SELF_NORMAL_TARGET';n.image=image;nt.nodes.active=n
 bpy.context.view_layer.objects.active=obs[0];start=time.time()
 bpy.ops.object.bake(type='NORMAL',normal_space='TANGENT',normal_r='POS_X',normal_g='POS_Y',normal_b='POS_Z')
 values=np.empty(a.size*a.size*4,np.float32);image.pixels.foreach_get(values);values=np.flipud(values.reshape(a.size,a.size,4)).copy()
 mask=Image.new('L',(a.size,a.size),0);draw=ImageDraw.Draw(mask)
 for ob in obs:
  ob.data.calc_loop_triangles();uv=ob.data.uv_layers['BakeUV']
  for tri in ob.data.loop_triangles:draw.polygon([(float(uv.data[i].uv.x)*a.size,(1-float(uv.data[i].uv.y))*a.size) for i in tri.loops],fill=255)
 interior=np.asarray(mask.filter(ImageFilter.MinFilter(5)))>0
 missed=int(np.count_nonzero(interior & (values[:,:,3]<.5)))
 assert missed==0, ('Uncovered self-normal surface texels',missed)
 # Uncovered atlas padding is neutral; actual covered samples remain untouched.
 values[values[:,:,3]<.5,:3]=(.5,.5,1)
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);write_png(out/'T_MetalTrashCan_Normal.png',values[:,:,:3],16)
 report=dict(method='Direct game surface shader normal; no high-to-low projection',size=a.size,samples=a.samples,seconds=time.time()-start,objects=len(obs),checked_interior_texels=int(interior.sum()),alpha_missed_interior_texels=missed)
 (out/'normal-self-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=='__main__':main()
