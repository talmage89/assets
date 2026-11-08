"""Use the kit's channel-correct filter; all outputs stay inside this family."""
import json,sys,subprocess
from pathlib import Path
from textures import SETS
out=Path('textures/ship');out.mkdir(parents=True,exist_ok=True);rows={}
for name,spec in SETS.items():
 subprocess.run([sys.executable,'../kit/downsample.py','--source','textures/bake','--out',str(out),'--asset',name,'--size',str(spec['size'])],check=True)
 rows[name]=json.loads((out/'texture-report.json').read_text())
Path('build/texture-delivery.json').write_text(json.dumps(rows,indent=2))
