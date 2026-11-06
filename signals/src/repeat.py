"""Fresh-factory replay of equipment geometry, shared image bindings and states."""
from pathlib import Path
import subprocess,json,hashlib,shutil

def main():
 folder=Path('build/repeat');shutil.rmtree(folder,ignore_errors=True);folder.mkdir()
 baseline={str(p.relative_to('build')):hashlib.sha256(p.read_bytes()).hexdigest() for p in [*sorted(Path('build').glob('Signals-*.glb')),*sorted(Path('build/parts').glob('*.glb'))]}
 with Path('build/repeat.log').open('w') as log:subprocess.run(['blender','-t','2','-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out',str(folder/'Signals-201.blend')],check=True,stdout=log,stderr=subprocess.STDOUT)
 rows=[]
 for name,digest in baseline.items():
  p=folder/name;actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==digest,('Not byte-identical',name)
  rows.append(dict(file=name,sha256=actual,bytes=p.stat().st_size))
 Path('build/repeat-check.json').write_text(json.dumps(dict(passed=True,files=rows,scope='Factory-startup recipe replay; exact geometry/state/image bytes. Does not rebake the GPU fields.'),indent=2));print('REPEAT',len(rows),'byte-identical GLBs',sum(x['bytes'] for x in rows),'bytes')
if __name__=='__main__':main()
