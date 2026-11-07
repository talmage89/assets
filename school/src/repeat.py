"""Independent deterministic external geometry/image rebuild; no GPU bake."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path

def snapshot():
    files=list(Path('export').glob('*.gltf'))+list(Path('export').glob('*.bin'))
    for f in Path('export').glob('*.gltf'):files += [f.parent/r['uri'] for r in json.loads(f.read_text()).get('images',[])]
    return {p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}

parser=argparse.ArgumentParser();parser.add_argument('--seeds',default='101,102,103');args=parser.parse_args()
old=snapshot()
with Path('build/repeat.log').open('w') as log:subprocess.run(['./src/blender.sh','-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--seeds',args.seeds,'--out','build/family.blend'],check=True,stdout=log,stderr=subprocess.STDOUT)
new=snapshot();changed=[p for p,h in old.items() if new.get(p)!=h]
Path('build/repeat.json').write_text(json.dumps(dict(passed=not changed,changed=changed,files=new,scope='Independent deterministic geometry and external-image re-export. Canonical shared bakes are immutable inputs; the school adds no new texture recipe.'),indent=2))
assert not changed,changed
print('REPEAT PASS',len(old),'external geometry/image files')
