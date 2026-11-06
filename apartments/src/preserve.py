"""Snapshot existing deliveries/docs before this family's build; never rewrite."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];out=Path('build/preservation.json')
if not out.exists():
 rows={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and 'apartments' not in p.relative_to(ROOT).parts and ('export' in p.parts or 'docs' in p.parts)}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(rows,indent=2));print('PRESERVATION baseline',len(rows))
