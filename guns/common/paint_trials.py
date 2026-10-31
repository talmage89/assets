"""Fixed-light enamel BRDF diagnostics; fresh source/GLB pairs accept the result."""
import sys,json
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2]
i=sys.argv.index('--member');member=sys.argv[i+1];del sys.argv[i:i+2]
BASE=ROOT/'guns'/member;sys.path[:0]=[str(ROOT),str(BASE/'src')]
import final_shots as F,interface
from guns.common.photo_matches import camera_shots
from guns.common.render import main
spec=json.loads((BASE/'src/paint_review.json').read_text())['studio_receiver'];shot=spec['shot'];original_configure=F.configure_scene;original_prepare=F.prepare_shot

def configure(scene,source):
 original_configure(scene,source)
 for mat in {m for o in scene.objects if o.type=='MESH' and not o.get('studio') for m in o.data.materials if m and m.use_nodes}:
  nt=mat.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if not bs or not bs.inputs['Base Color'].links:continue
  tex=bs.inputs['Base Color'].links[0].from_node
  if tex.type!='TEX_IMAGE':continue
  subtract=nt.nodes.new('ShaderNodeMath');subtract.operation='SUBTRACT';subtract.inputs[1].default_value=.56;nt.links.new(tex.outputs['Alpha'],subtract.inputs[0])
  fraction=nt.nodes.new('ShaderNodeMath');fraction.operation='DIVIDE';fraction.inputs[1].default_value=.24;fraction.use_clamp=True;nt.links.new(subtract.outputs[0],fraction.inputs[0])
  for channel,initial,divisor in [('Roughness',.42 if member=='ak' else .29,1),('Specular IOR Level',.8,2)]:
   old=bs.inputs[channel].links[0].from_socket
   value=nt.nodes.new('ShaderNodeValue');value.name='TRIAL '+channel
   delta=nt.nodes.new('ShaderNodeMath');delta.operation='MULTIPLY';nt.links.new(value.outputs[0],delta.inputs[0]);nt.links.new(fraction.outputs[0],delta.inputs[1])
   add=nt.nodes.new('ShaderNodeMath');add.operation='ADD';nt.links.new(old,add.inputs[0]);nt.links.new(delta.outputs[0],add.inputs[1]);nt.links.new(add.outputs[0],bs.inputs[channel])

def prepare(scene,shot):
 original_prepare(scene,shot)
 for mat in bpy.data.materials:
  if not mat.use_nodes:continue
  for channel,value in [('Roughness',shot['trial_roughness']-(.42 if member=='ak' else .29)),('Specular IOR Level',(shot['trial_specular']-.8)/2)]:
   node=mat.node_tree.nodes.get('TRIAL '+channel)
   if node:node.outputs[0].default_value=value
F.configure_scene=configure;F.prepare_shot=prepare
F.RENDER_STAGE='REVIEW ONLY fixed-light paint parameter diagnostic; not shipping acceptance'
photo=dict(camera_shots(BASE/'build/cameras.json')[shot],**F.PHOTO_POSES[shot]);hero=F.SHOTS['hero'];F.SHOTS={}
for rough in (.02,.04,.06,.08,.12,.16,.22,.29,.36,.42,.50,.58):
 for specular in (.2,.4,.6,.8):
  for role,s in [('photo',photo),('hero',hero)]:
   name=f'{role}_r{round(rough*100):02d}_s{round(specular*100):02d}';F.SHOTS[name]=dict(s,trial_roughness=rough,trial_specular=specular)
F.DEFAULT_SHOTS=','.join(F.SHOTS)
main(F,interface)
