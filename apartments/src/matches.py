"""Use the kit solver, retaining the family asset selector in its result."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.photo_match import solve
import runpy
runpy.run_path("src/neutral_refs.py")
from photo_matches import MATCHES
solve('src/photo_matches.py','build/matched-cameras.json')
p=Path('build/matched-cameras.json');d=json.loads(p.read_text())
for key,row in d.items():
 row['asset']=MATCHES[key]['asset']
 row['shot']['light']=MATCHES[key]['light']
 if key=='garage-row':row['lens_status']='Type fit, not camera recovery: photograph EXIF gives 38 mm equivalent; solver lens differs because this is an original plan.'
p.write_text(json.dumps(d,indent=2))
