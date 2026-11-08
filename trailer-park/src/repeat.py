"""Rebuild the deterministic geometry packages in place and compare bytes.

Canonical sibling images and cached local native adapters remain immutable
inputs. This checks package regeneration, not an independent GPU texture rebake.
"""
import hashlib,json,os,subprocess
from pathlib import Path


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline={str(p):digest(p) for p in Path('export').rglob('*') if p.is_file() and p.suffix in ('.gltf','.bin','.json','.png')}
    saved=Path('build/repeat-before');saved.mkdir(parents=True,exist_ok=True)
    for name in baseline:
        p=Path(name);q=saved/p.relative_to('export');q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
    plans=[json.loads(p.read_text())['plan'] for p in Path('export').glob('Park-*.json')]
    old=next(p for p in plans if p['kind']=='old');new=next(p for p in plans if p['kind']=='new')
    with Path('build/repeat.log').open('w') as log:
        subprocess.run([os.environ.get('BLENDER','blender'),'-b','-t','2','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--old-seed',str(old['seed']),'--new-seed',str(new['seed']),'--rows',str(round(old['span']/old['lot_frontage'])),'--out','build/family.blend'],stdout=log,stderr=subprocess.STDOUT,check=True)
    differences=[name for name,expected in baseline.items() if not Path(name).exists() or digest(Path(name))!=expected]
    result=dict(passed=not differences,compared_files=len(baseline),differences=differences,scope='glTF / BIN / sidecar JSON / local external PNG byte identity; cached native inputs, no GPU bake')
    Path('build/repeat.json').write_text(json.dumps(result,indent=2));assert not differences,result
    print('REPEAT PASS',len(baseline),'files byte-identical')

if __name__=='__main__':main()
