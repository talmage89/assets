"""Build missing same-worktree presentation exports; preserve existing files."""
import argparse,hashlib,json,subprocess
from pathlib import Path


def recipe():
 here=Path(__file__).resolve().parent
 return hashlib.sha256(b''.join((here/n).read_bytes() for n in ('render.py','siteworks.py','context.py','ground_adapter.py','photo_matches.py','presentation.py','paving.py'))+(here.parents[1]/'houses/src/render.py').read_bytes()).hexdigest()


def bundle(path):
 """Hash an export and every local external buffer/image, without changing it."""
 path=Path(path);files=[path]
 if path.suffix=='.gltf':
  doc=json.loads(path.read_text())
  files += [path.parent/r['uri'] for key in ('buffers','images') for r in doc.get(key,[]) if r.get('uri') and not r['uri'].startswith('data:')]
 files=sorted(set(files));repo=Path(__file__).resolve().parents[2]
 rows=[dict(source=str(f.relative_to(repo)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in files]
 return dict(source=str(path.relative_to(repo)),sha256=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest(),files=rows)


def ensure(ground_only=False,street=False):
 repo=Path(__file__).resolve().parents[2];rows=[]
 cases=[('ground','Ground.glb',['export'])]
 if street:cases += [('houses','HearthfieldSplit-51.gltf',['TYPE=split','SEEDS=51','export']),('trees','PinOak.glb',['SPECIES=oak','export'])]
 elif not ground_only:cases += [('houses','HearthfieldSplit-51.gltf',['TYPE=split','SEEDS=51','export']),('cars','AlderC150.glb',['export'])]
 for folder,name,args in cases:
  file=repo/folder/'export'/name
  if not file.exists():
   log=Path('build')/('context-'+folder+'.log')
   with log.open('w') as f:subprocess.run(['make','-C',str(repo/folder),*args],stdout=f,stderr=subprocess.STDOUT,check=True)
  rows.append(bundle(file))
 Path('build/context.json').write_text(json.dumps(rows,indent=2));print('CONTEXT ready',len(rows))
 return rows

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--ground-only',action='store_true');p.add_argument('--street',action='store_true');a=p.parse_args();ensure(a.ground_only,a.street)
