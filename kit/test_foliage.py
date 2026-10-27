"""Golden snapshot captured before extracting the maple shader; Blender 5.2."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy
from kit.foliage import material
images=[bpy.data.images.new(n,8,8) for n in ('albedo','normal','orm')]
def snapshot(mat):
 def value(v):
  if isinstance(v,(bool,str,int,float)):return v
  try:return list(v)
  except:return str(v)
 return dict(nodes=[dict(type=n.bl_idname,name=n.name,label=n.label,properties={k:value(getattr(n,k)) for k in ('operation','blend_type','interpolation_type','clamp','use_clamp') if hasattr(n,k)},inputs=[(s.identifier,value(s.default_value)) for s in n.inputs if hasattr(s,'default_value')]) for n in mat.node_tree.nodes],links=[(l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in mat.node_tree.links],props={k:value(v) for k,v in mat.items()})
state=snapshot(material(*images))
digest=hashlib.sha256(json.dumps(state,sort_keys=True).encode()).hexdigest()
assert digest=='015cd23d2cc7b4f1dfc8e04f80dc7885ae5253918257ba4686535f81a3d5cc95',digest
print('Original maple shader nodes/links/defaults/properties: byte-identical',digest)
custom=material(*images,name='Glossy shrub',transmission=.18,specular=.4)
assert abs(custom.node_tree.nodes['Leaf transmission fraction'].inputs[0].default_value-.18)<1e-6
assert custom.name=='Glossy shrub'
print('Optional family controls: passed')
