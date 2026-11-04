"""Compare actual exported ground curb sections with actual station triangles."""
from pathlib import Path
import numpy as np
from mathutils import Vector
from kit.gltf import GLB
from ground_adapter import FLOW


def canonical(g,name):
 nodes=g.json['nodes'];ri=next(i for i,n in enumerate(nodes) if n.get('name')==name)
 inverse=np.linalg.inv(g.world(ri));out=[]
 def visit(i):
  node=nodes[i]
  if 'mesh' in node:
   for pr in g.json['meshes'][node['mesh']]['primitives']:
    xyz=g.accessor(pr['attributes']['POSITION']);h=np.c_[xyz,np.ones(len(xyz))]
    out.extend((h@(inverse@g.world(i)).T)[:,:3])
  for child in node.get('children',[]):visit(child)
 visit(ri);out=np.array(out)
 # The exporter can retain an axis-conversion frame on a root. Identify that
 # representation against both independent envelope axes, not a guessed sign.
 candidates=[out,out[:,[0,2,1]]*np.array([1,-1,1])]
 valid=[x for x in candidates if abs(np.ptp(x[:,1])-(3.048 if name=='Curb_Straight' else 6.096))<1e-4 and np.ptp(x[:,2])<.16]
 assert len(valid)==1,'Ambiguous native ground frame'
 return valid[0]


def audit(p,tree,station_matrix):
 source=Path('../ground/export/Ground.glb');g=GLB(source);W,D=p['lot'];rows=[]
 for kind in ('Curb_Straight','Curb_DrivewayCut'):
  vertices=canonical(g,kind)
  # Straight endpoint avoids its intentional center control joint. On the cut,
  # the 5-ft station is exactly the start of the full 10-ft depressed span.
  samples=vertices[np.abs(vertices[:,1]-1.524)<3e-5]
  qz=np.unique(np.round(samples[:,[0,2]],7),axis=0)
  assert len(qz)>=10,'Missing native section samples'
  for drive in p['driveways']:
   south=drive['edge']=='south';u=(W/2-.3048 if south else D/2-.3048) if kind=='Curb_Straight' else (drive['center'][0] if south else drive['center'][1])
   errors=[]
   for q,z in qz:
    local=(u,-D/2-3.3528+q,FLOW+z) if south else (-W/2-3.3528+q,u,FLOW+z)
    world=station_matrix@Vector(local);errors.append(tree.find_nearest(world)[3])
   maximum=max(errors);assert maximum<5e-5,(kind,drive['edge'],maximum)
   rows.append(dict(native_module=kind,street=drive['edge'],samples=len(errors),maximum_actual_surface_distance_m=maximum))
 return dict(passed=True,scope='Raw delivered Ground profile vertices to actual station triangle surfaces; unchanged curb and pan section, widened clear run. Not a whole-road crown or full tiling seam certification.',rows=rows)
