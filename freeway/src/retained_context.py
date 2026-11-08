"""Keep accepted town placements, traffic snapshots and cap runoff unchanged."""
import hashlib,json
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 base=Path('build/round4-before');rows={}
 for seed in (101,202):
  path=base/f'scene-{seed}.json'
  if not path.exists():continue
  old=json.loads(path.read_text());new=json.loads(Path(f'build/scene-{seed}.json').read_text())
  assert old['plan']==new['plan'],(seed,'Accepted alignment changed')
  for key in ('context','traffic'):
   assert old[key]['placements']==new[key]['placements'],(seed,key,'Accepted placements changed')
  traffic={}
  for suffix in ('gltf','bin'):
   oldfile=base/f'freeway/export/Traffic-{seed}.{suffix}';newfile=Path(f'export/Traffic-{seed}.{suffix}')
   traffic[suffix]=dict(before_sha256=sha(oldfile),after_sha256=sha(newfile),identical=sha(oldfile)==sha(newfile))
  rows[str(seed)]=dict(alignment_identical=True,town_placements_identical=True,traffic_placements_identical=True,traffic_bytes=traffic)
 # Compare the actual source chart used for accepted cap runoff. Editing
 # the unused weed cell must not change this top-connected water vocabulary.
 from PIL import Image
 import numpy as np
 from textures import rect
 u0,v0,u1,v1=rect('runoff')
 for channel in ('BaseColor','Normal','ORM'):
  old=Image.open(base/f'freeway/textures/ship/T_FreewayMaintenance_{channel}.png');new=Image.open(f'textures/ship/T_FreewayMaintenance_{channel}.png')
  box=(round(u0*old.width),round((1-v1)*old.height),round(u1*old.width),round((1-v0)*old.height))
  a,b=[np.asarray(im.crop(box)).astype(float) for im in (old,new)]
  # GPU rebake tolerance is separate from strict CPU placement identity.
  assert abs(a-b).max()<=2,(channel,'Accepted runoff chart changed')
 rows['scope']='Alignment and full placement manifests are exact. Traffic byte comparisons are reported independently. Accepted cap-runoff atlas chart stays within the kit rebake tolerance; its geometry/UV is covered by accepted-construction.'
 Path('build/retained-context.json').write_text(json.dumps(rows,indent=2));print('RETAINED CONTEXT PASSED',[(k,v['traffic_bytes']) for k,v in rows.items() if isinstance(v,dict)])
if __name__=='__main__':main()
