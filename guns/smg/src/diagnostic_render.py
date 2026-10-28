"""Explicit review-only shader diagnostics for separating reflection and form."""
import sys
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[3]),str(Path(__file__).parent)]
from guns.common.render import main
import final_shots,interface
mode=sys.argv[sys.argv.index('--diagnostic')+1];i=sys.argv.index('--diagnostic');del sys.argv[i:i+2]
original=final_shots.configure_scene

def configure(scene,source):
 original(scene,source)
 materials={m for ob in scene.objects if ob.type=='MESH' and not ob.get('studio') for m in ob.data.materials if m and m.use_nodes}
 for mat in materials:
  nt=mat.node_tree;bs=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED')
  sockets=('Normal',) if mode=='normal_off' else ('Base Color','Metallic','Roughness')
  for name in sockets:
   for link in list(bs.inputs[name].links):nt.links.remove(link)
  if mode=='clay':
   bs.inputs['Base Color'].default_value=(.18,.18,.18,1);bs.inputs['Metallic'].default_value=0;bs.inputs['Roughness'].default_value=.8;bs.inputs['Specular IOR Level'].default_value=0
final_shots.configure_scene=configure
final_shots.RENDER_STAGE='explicit '+mode+' diagnosis; not final material presentation'
if __name__=='__main__':main(final_shots,interface)
