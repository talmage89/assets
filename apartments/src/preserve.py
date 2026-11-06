"""Snapshot existing deliveries/docs before this family's build; never rewrite."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];out=Path('build/preservation.json')
if not out.exists():
 rows={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
       for family in ROOT.iterdir() if family.is_dir() and family.name not in ('apartments','build','.git')
       for folder in ('export','docs','textures') for p in (family/folder).rglob('*') if p.is_file()}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(rows,indent=2));print('PRESERVATION baseline',len(rows))
