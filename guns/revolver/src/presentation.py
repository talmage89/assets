"""Asset-owned render recipe provenance alongside the exported-source hash."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest():
 h=hashlib.sha256()
 for name in ('final_shots.py','shots.py','render.py','source_render.py','hammer_review.py','presentation.py'):
  h.update(name.encode()+b'\0'+(HERE/name).read_bytes())
 return h.hexdigest()
def stamp(folder):
 path=Path(folder)/'shots.json';data=json.loads(path.read_text())
 for row in data.values():row['presentation_sha256']=digest()
 path.write_text(json.dumps(data,indent=2))
