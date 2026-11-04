"""Only missing own-family exports are rebuilt; record their immutable hashes."""
import hashlib,json,subprocess
from pathlib import Path
rows=[]
for folder,name in (('ground','Ground'),('trees','RedMaple'),('cars','AlderC150'),('shrubs','Shrubs'),('trees','PinOak')):
 source=Path('..')/folder/'export'/(name+'.glb')
 if not source.exists():
  command=['make','-C','../'+folder]+(['SPECIES=oak'] if name=='PinOak' else [])+['export']
  with Path(f'build/cape/delivery/context-{name}.log').open('w') as log:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
 rows.append(dict(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),bytes=source.stat().st_size))
Path('build/cape/delivery/context.json').write_text(json.dumps(rows,indent=2));print('CAPE_CONTEXT',[(r['source'],r['bytes']) for r in rows])
