"""Fast form diagnostic. Source fields only; never certified as baked delivery."""
import sys,json,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import bpy
import geometry,look,build

def quick():
 atlas=geometry.image_material('FORM_Minigolf','build/procedural/T_Minigolf_BaseColor.png','build/procedural/T_Minigolf_ORM.png')
 nt=atlas.node_tree;b=nt.nodes.get('Principled BSDF');tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
 vc=nt.nodes.new('ShaderNodeVertexColor');vc.layer_name='Tint';mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
 nt.links.new(tex.outputs[0],mix.inputs[1]);nt.links.new(vc.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],b.inputs['Base Color'])
 return atlas,{key:geometry.M[key] for key in ('concrete','asphalt','grass','wood','water','glass')}
if __name__=='__main__':
 look.materials=quick
 a=argparse.Namespace(classic_seed=71,adventure_seed=92,out='build/form.blend');build.build(a)
