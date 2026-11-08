"""Checkpoint inventory, import provenance and immutable delivery/image receipt.

Capture after a full render, before repeat rebuilds touch file timestamps.
Subsequent checks use bytes, so byte-identical re-exports remain valid.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
from proof_views import REQUIRED

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bundle(path):
 doc=json.loads(path.read_text());files=[path]+[path.parent/r['uri'] for key in ('buffers','images') for r in doc.get(key,[]) if 'uri' in r]
 return {str(p):sha(p) for p in sorted(set(files))}

def check(capture=False):
 bundles={str(seed):bundle(Path(f'export/Minigolf-{seed}.gltf')) for seed in (71,92)};images={};frames=[]
 for name in REQUIRED:frames.append(Path('renders/checkpoint')/(name+'.png'))
 for name in ('period_lighthouse','period_classic_green','period_castle'):frames.append(Path('renders/matches')/(name+'.png'))
 for path in frames:
  assert path.is_file(),path;meta=json.loads(path.with_suffix('.json').read_text());source=Path(meta['source']);seed=source.stem.split('-')[-1]
  assert meta['engine']=='CYCLES' and meta['sha256']==sha(source),(path,'wrong source')
  assert Image.open(path).width>=640,(path,'insufficient review resolution')
  if capture:
   for f in bundles[seed]:assert Path(f).stat().st_mtime<=path.stat().st_mtime,(path,'delivery was changed after rendering',f)
  images[str(path)]=sha(path)
  if path.stem=='fixture':assert abs(meta['scale_silhouette']['measured_height_m']-1.8)<1e-5
 hero=json.loads(Path('renders/checkpoint/hero.json').read_text())['camera'];assert 35<=hero['lens']<=50
 ground=.015+.025*max(0,hero['location'][1]+9);assert abs(hero['location'][2]-ground-1.65)<1e-5
 for seed in (71,92):
  doc=json.loads(Path(f'export/Minigolf-{seed}.gltf').read_text());assert all(im['uri'].startswith('textures/') for im in doc['images'])
 recipe={str(p):sha(p) for p in [Path('src/render.py'),Path('src/context.py'),Path('src/matches.py'),Path('src/photo_matches.py')]}
 actual=dict(bundles=bundles,images=images,recipe=recipe);receipt=Path('build/render-receipt.json')
 if capture:receipt.write_text(json.dumps(actual,indent=2))
 else:assert json.loads(receipt.read_text())==actual,'Rendered bytes, delivery or recipe changed'
 Path('build/render-check.json').write_text(json.dumps(dict(passed=True,cycles_frames=len(frames),source='fresh external-image glTF imports',scope=__doc__),indent=2));print('RENDER CHECK',len(frames),'Cycles frames PASS')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--capture',action='store_true');a=p.parse_args();check(a.capture)
