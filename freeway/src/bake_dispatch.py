"""Keep verified cache-only work out of the shared GPU queue."""
import argparse,hashlib,json,shlex,subprocess
from pathlib import Path
from textures import SETS

p=argparse.ArgumentParser();p.add_argument('--blender',default='blender -t 2');a=p.parse_args()
root=Path(__file__).resolve().parents[2]
kit_hash=hashlib.sha256((root/'kit/flat_bake.py').read_bytes()).hexdigest()
verified=True
for name,spec in SETS.items():
 sources=[Path('textures/source')/f'T_{name}_{c}.png' for c in ('BaseColor','ORM','Height')]
 if name=='FreewayMaintenance':sources.append(Path('textures/source/T_FreewayMaintenance_Alpha.png'))
 inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
 signature=hashlib.sha256((json.dumps([inputs,spec],sort_keys=True)+kit_hash).encode()).hexdigest()
 receipt=Path('textures/bake')/(name+'-bake.json')
 old=json.loads(receipt.read_text()) if receipt.exists() else {}
 verified &= old.get('source_signature')==signature and all((Path('textures/bake')/f'T_{name}_{c}.png').exists() for c in ('BaseColor','Normal','ORM'))
command=shlex.split(a.blender)+['-b','--factory-startup','--python-exit-code','1','--python','src/bake.py']
if verified:
 print('Verified manufacture cache: CPU-only receipt/mtime refresh',flush=True)
 command+=['--','--cache-only']
else:command=[str(root/'kit/with_gpu.sh'),*command]
subprocess.run(command,check=True)
