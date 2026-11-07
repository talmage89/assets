"""Independent deterministic external geometry/image rebuild; no GPU bake."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path

def snapshot():
    files=list(Path('export').glob('*.gltf'))+list(Path('export').glob('*.bin'))+list(Path('export').glob('*.json'))
    files += [Path('build/family.json')]+list(Path('build').glob('School-*.json'))+list(Path('build').glob('Campus-*.json'))
    # Construction audit reports are verification products, not builder output.
    files=[p for p in files if not p.stem.endswith('-construction')]
    files += list(Path('textures/checkpoint').glob('*.png'))+list(Path('textures/ship').glob('*.png'))
    for f in Path('export').glob('*.gltf'):files += [f.parent/r['uri'] for r in json.loads(f.read_text()).get('images',[])]
    return {os.path.relpath(p,Path.cwd()):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted({p.resolve() for p in files})}

parser=argparse.ArgumentParser();parser.add_argument('--seeds',default='101,102,103');args=parser.parse_args()
old=snapshot()
with Path('build/repeat.log').open('w') as log:subprocess.run(['./src/blender.sh','-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--seeds',args.seeds,'--out','build/family.blend'],check=True,stdout=log,stderr=subprocess.STDOUT)
new=snapshot();changed=sorted(set(old)^set(new))+[p for p in sorted(set(old)&set(new)) if new[p]!=old[p]]
Path('build/repeat.json').write_text(json.dumps(dict(passed=not changed,changed=changed,files=new,scope='Independent deterministic geometry, metadata and external-image re-export. Canonical shared GPU bakes are immutable inputs; the school mask is regenerated. Blender source containers and stochastic review renders are excluded.'),indent=2))
assert not changed,changed
print('REPEAT PASS',len(old),'deterministic geometry/metadata/image files')
