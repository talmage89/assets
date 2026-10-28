"""An independent factory-startup build must reproduce all inspection exports."""
import json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
rows={}
for name in ('bolt','magazine_loaded','magazine_empty','case'):
 a=BASE/'build'/(name+'.glb');b=BASE/'build/repeat'/(name+'.glb')
 x=hashlib.sha256(a.read_bytes()).hexdigest();y=hashlib.sha256(b.read_bytes()).hexdigest()
 assert x==y,(name,x,y);rows[name]=x
(BASE/'build/repeat.json').write_text(json.dumps(dict(passed=True,sha256=rows),indent=2))
print('B24 independent rebuild: four byte-identical GLBs')
