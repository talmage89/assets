"""Independent rebuild; compare external bytes and retain reviewed witnesses."""
import hashlib,json,subprocess,os,shutil,shlex
from pathlib import Path

def snapshot():
 files=list(Path('export').glob('*.gltf'))+list(Path('export').glob('*.bin'))
 for gltf in Path('export').glob('*.gltf'):
  files.extend(gltf.parent/i['uri'] for i in json.loads(gltf.read_text()).get('images',[]))
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}
old=snapshot();cache=Path('build/repeat/before');rebuilt=Path('build/repeat/rebuilt')
owned=[p for p in Path('build').glob('*') if p.suffix in ('.blend','.json')]+[p for p in Path('export').glob('*') if p.suffix in ('.gltf','.bin','.json')]
for p in owned:
 target=cache/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
with Path('build/repeat.log').open('w') as log:
 result=subprocess.run([*shlex.split(os.environ.get('BLENDER','blender')),'-b','-t','4','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/family.blend'],stdout=log,stderr=subprocess.STDOUT)
new=snapshot();changed=[p for p,h in old.items() if new.get(p)!=h]
# Retain the independent build for investigation; restore the reviewed source
# blend and identical package files, including their timestamps/provenance.
for p in owned:
 target=rebuilt/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 shutil.copy2(cache/p,p)
Path('build/repeat.json').write_text(json.dumps(dict(passed=result.returncode==0 and not changed,changed=changed,files=new,scope='Independent geometry re-export with the accepted shared bakes; rebuilt source witnesses retained under build/repeat/rebuilt'),indent=2))
assert result.returncode==0,'Independent build failed; see build/repeat.log'
assert not changed,changed
print('EXTERNAL REPEAT PASS',len(old),'geometry/image files')
