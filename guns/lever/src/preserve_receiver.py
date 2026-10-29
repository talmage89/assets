"""Optional handoff proof: receiver finish alone changes; no baseline dependency.

Compare every accepted mesh, rest bone, clip and socket, then the full material
node graphs of every other part. The baseline stays ignored review evidence.
"""
import argparse, ast, json, sys
from pathlib import Path
import bpy
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
import preserved

def graphs(path):
 bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
 result={}
 def value(v):
  if isinstance(v,(str,int,float,bool)):return v
  try:return list(v)
  except TypeError:return str(v)
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or not ob.get('asset_set') or ob.name=='Receiver':continue
  materials=[]
  for mat in ob.data.materials:
   nt=mat.node_tree;nodes=[]
   for n in nt.nodes:
    properties={k:value(getattr(n,k)) for k in ('operation','data_type','clamp_factor',
      'blend_type','attribute_name','noise_dimensions','feature','distance','interpolation',
      'extension','vector_type','convert_from','convert_to','use_clamp') if hasattr(n,k)}
    if n.type=='TEX_IMAGE':properties['image']=Path(n.image.filepath).name
    nodes.append(dict(name=n.name,type=n.bl_idname,properties=properties,
      inputs=[(s.identifier,value(s.default_value)) for s in n.inputs if hasattr(s,'default_value')]))
   links=sorted((l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in nt.links)
   materials.append(dict(nodes=nodes,links=links))
  result[ob.name]=materials
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 old=a.before
 bpy.ops.wm.open_mainfile(filepath=str((old/'lever.blend').resolve()))
 preserved.ACCEPTED=tuple(o.name for o in bpy.context.scene.objects if o.type=='MESH')
 before=preserved.capture(old/'lever.blend');after=preserved.capture(BASE/'build/lever.blend')
 assert before==after,'accepted geometry/rig/clip/socket changed'
 bg=graphs(old/'high.blend');ag=graphs(BASE/'build/delivery/high.blend')
 assert bg==ag,('accepted finish changed',[k for k in bg if bg[k]!=ag.get(k)])
 def lower(path):
  names={'striae','drag','lower_width','lower_center','lower'}
  return {n.targets[0].id:ast.dump(n.value) for n in ast.walk(ast.parse(path.read_text()))
    if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names}
 before_lower=lower(old/'lookdev.py');after_lower=lower(BASE/'src/lookdev.py')
 assert before_lower==after_lower and len(before_lower)==5
 r=dict(passed=True,identical_meshes=len(preserved.ACCEPTED),bones=len(before['bones']),
  clips=len(before['clips']),socket_frames=len(before['sockets']),unchanged_finish_parts=len(bg),
  accepted_lower_fillet_expressions_exact=sorted(before_lower),
  scope='Exact accepted geometry/normals/owners, bones, clip keys/interpolation, socket matrices; all nonreceiver shader nodes, defaults and links.')
 (BASE/'build/receiver-preserved.json').write_text(json.dumps(r,indent=2));print(r,flush=True)
if __name__=='__main__':main()
