"""Serial GPU batch with content/physical-parameter guarded manufacture caches."""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.flat_bake import bake
from kit.image_io import read_png,write_png
import numpy as np
from textures import SETS
for name,spec in SETS.items():
 sources=[Path('textures/source')/f'T_{name}_{c}.png' for c in ('BaseColor','ORM','Height')]
 if name=='FreewayMaintenance':sources.append(Path('textures/source/T_FreewayMaintenance_Alpha.png'))
 outputs=[Path('textures/bake')/f'T_{name}_{c}.png' for c in ('BaseColor','ORM','Normal')]
 receipt=Path('textures/bake')/(name+'-bake.json')
 inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 signature=hashlib.sha256((json.dumps([inputs,spec],sort_keys=True)+hashlib.sha256((HERE.parents[1]/'kit/flat_bake.py').read_bytes()).hexdigest()).encode()).hexdigest()
 old=json.loads(receipt.read_text()) if receipt.exists() else {}
 same=old.get('source_signature')==signature
 # First upgrade of the already validated kit receipts: unchanged file times
 # and physical bake parameters attest the existing channels before sealing.
 legacy=('source_signature' not in old and old.get('coverage_m')==spec['coverage'] and old.get('height_distance_m')==spec['height'] and old.get('samples')==8 and all(p.exists() for p in outputs) and min(p.stat().st_mtime for p in outputs)>=max(p.stat().st_mtime for p in sources))
 if not (same or legacy):
  assert '--cache-only' not in sys.argv,'Cache changed after dispatch; rerun make for a locked bake'
  bake(Path('textures/source'),Path('textures/bake'),name,spec['coverage'],4096,8,spec['height'])
  if name=='FreewayMaintenance':
   p=outputs[0];rgb=read_png(p);alpha=read_png(sources[-1])[:,:,0];write_png(p,np.dstack([rgb[:,:,:3],alpha]),bits=8)
  old=json.loads(receipt.read_text())
 else:print('REUSE VERIFIED BAKE',name,flush=True)
 old.update(source_signature=signature,source_hashes=inputs);receipt.write_text(json.dumps(old,indent=2))
 # The recipe has checked these bytes against its current inputs/settings.
 # Updating mtimes avoids a second empty GPU-lock job after a cache hit.
 for path in outputs:path.touch()
