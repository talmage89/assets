"""Canonical URI/payload and indexed surface equality, external versus build GLB."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.gltf import GLB

class External(GLB):
 def __init__(self,path):
  self.json=json.loads(path.read_text());self.binary=(path.parent/self.json['buffers'][0]['uri']).read_bytes();self.parents={c:i for i,n in enumerate(self.json['nodes']) for c in n.get('children',[])}

def main():
 records=[];shared={}
 for name in ('Minigolf-71','Minigolf-92','MinigolfPieces','Minigolf-71-landscape','Minigolf-92-landscape'):
  path=Path('export')/(name+'.gltf');g=External(path);mirror=GLB(Path('build/embedded')/(name+'.glb'));other={n['name']:(i,n) for i,n in enumerate(mirror.json['nodes'])};corners=0
  for i,node in enumerate(g.json['nodes']):
   j,old=other[node['name']];assert np.max(abs(g.world(i)-mirror.world(j)))<2e-6
   if 'mesh' not in node:continue
   for a,b in zip(g.json['meshes'][node['mesh']]['primitives'],mirror.json['meshes'][old['mesh']]['primitives']):
    ia=g.accessor(a['indices']).ravel();ib=mirror.accessor(b['indices']).ravel();assert len(ia)==len(ib)
    assert set(a['attributes'])==set(b['attributes'])
    for channel in a['attributes']:
     av=g.accessor(a['attributes'][channel])[ia];bv=mirror.accessor(b['attributes'][channel])[ib]
     if channel=='COLOR_0' and av.shape[1]!=bv.shape[1]:
      if av.shape[1]==3:av=np.c_[av,np.ones(len(av))]
      if bv.shape[1]==3:bv=np.c_[bv,np.ones(len(bv))]
     assert np.array_equal(av,bv),(name,node['name'],channel,float(np.max(abs(av-bv))))
    corners+=len(ia)
  embedded={hashlib.sha256(mirror.image(i)).hexdigest() for i in range(len(mirror.json['images']))};images=[];mib=0
  for im in g.json['images']:
   target=(path.parent/im['uri']).resolve();assert target.is_file() and 'export/textures' not in str(target)
   raw=target.read_bytes();digest=hashlib.sha256(raw).hexdigest();assert digest in embedded
   w,h=Image.open(target).size;mib+=w*h*4/3/1048576;shared[str(target)]=digest;images.append(dict(uri=im['uri'],bytes=len(raw),size=[w,h],sha256=digest))
  records.append(dict(name=name,indexed_corners_compared=corners,gltf_bytes=path.stat().st_size,bin_bytes=len(g.binary),materials=len(g.json['materials']),compressed_full_mip_mib=mib,images=images))
 Path('build/external-check.json').write_text(json.dumps(dict(passed=True,records=records,shared_image_files=len(shared),scope=__doc__),indent=2));print('EXTERNAL PASS',[(r['name'],r['gltf_bytes']+r['bin_bytes'],r['compressed_full_mip_mib']) for r in records])
if __name__=='__main__':main()
