"""Build authorized library context in its own folders, never export it here."""
import hashlib
import json
from pathlib import Path
import subprocess

rows=[]
for folder,name in (('ground','Ground'),('trees','RedMaple'),('cars','AlderC150')):
    log=Path(f'build/context-{folder}.log')
    with log.open('w') as output:subprocess.run(['make','-C','../'+folder,'export'],stdout=output,stderr=subprocess.STDOUT,check=True)
    source=Path('..')/folder/'export'/(name+'.glb')
    rows.append(dict(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),bytes=source.stat().st_size))
Path('build/context.json').write_text(json.dumps(rows,indent=2))
print('CONTEXT own-library builds ready',[(r['source'],r['bytes']) for r in rows])
