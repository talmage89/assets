"""Prepare only the bake channels; the reviewed source scene is never edited."""
import argparse,sys
from pathlib import Path
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
 # Preserve each manufacturing object's generated bounds before the baker
 # consolidates coordinate frames. Joined glass must retain its own frit field.
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or 'asset_set' not in ob:continue
  local=ob.data.attributes.new('BakeObject','FLOAT_VECTOR','POINT')
  for row,v in zip(local.data,ob.data.vertices):row.vector=v.co
  low=[min(v.co[k] for v in ob.data.vertices) for k in range(3)]
  high=[max(v.co[k] for v in ob.data.vertices) for k in range(3)]
  if ob.data.uv_layers:
   layer=next((uv for uv in ob.data.uv_layers if uv.active_render),ob.data.uv_layers.active)
   stored=ob.data.attributes.new('BakeSourceUV','FLOAT_VECTOR','CORNER')
   for row,point in zip(stored.data,layer.data):row.vector=(*point.uv,0)
  attr=ob.data.attributes.new('BakeGenerated','FLOAT_VECTOR','POINT')
  for row,v in zip(attr.data,ob.data.vertices):row.vector=[(v.co[k]-low[k])/max(high[k]-low[k],1e-9) for k in range(3)]
 for m in bpy.data.materials:
  nt=m.node_tree
  generated=nt.nodes.new('ShaderNodeAttribute');generated.attribute_name='BakeGenerated'
  local=nt.nodes.new('ShaderNodeAttribute');local.attribute_name='BakeObject'
  printuv=nt.nodes.new('ShaderNodeAttribute');printuv.attribute_name='BakeSourceUV'
  for node in list(nt.nodes):
   if node.type=='TEX_COORD':
    if node.object:raise ValueError('Explicit shader frame needs a separate attribute conversion')
    for link in list(node.outputs['Object'].links):nt.links.new(local.outputs['Vector'],link.to_socket)
    for link in list(node.outputs['Generated'].links):nt.links.new(generated.outputs['Vector'],link.to_socket)
    for link in list(node.outputs['UV'].links):nt.links.new(printuv.outputs['Vector'],link.to_socket)
   if node.type=='TEX_IMAGE' and not node.inputs['Vector'].is_linked:nt.links.new(printuv.outputs['Vector'],node.inputs['Vector'])
  if m.get('vehicle_paint'):
   # Uniform factory metallic is applied after the shared texture. Paint RGB
   # retains the default Atlantic fallback; alpha carries neutral coverage.
   out=nt.nodes['OUT_metal']
   for link in list(out.inputs[0].links):nt.links.remove(link)
   out.inputs[0].default_value=1
  if m.get('lamp_lit_strength',0)>0:
   value=nt.nodes.new('ShaderNodeValue');value.name='OUT_paint_coverage'
   value.outputs[0].default_value=m['lamp_lit_strength']/80
 Path(a.out).parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.out).resolve()))
if __name__=='__main__':main()
