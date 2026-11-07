"""Snapshot existing deliveries/docs before this family's build; never rewrite."""
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];out=Path('build/preservation.json')
if not out.exists():
 rows={}
 for folder,dirs,files in os.walk(ROOT):
  dirs[:]=sorted(d for d in dirs if d not in ('apartments','build','.git'))
  relative=Path(folder).relative_to(ROOT)
  if not any(q in relative.parts for q in ('export','docs','textures')):continue
  for name in sorted(files):
   p=Path(folder)/name
   if p.is_file():rows[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(rows,indent=2));print('PRESERVATION baseline',len(rows))
