"""Member-owned receiver observations; source and exported-GLB audits."""
import argparse,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE.parents[1]))
from guns.common.paint_review import audit
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--renders',default='renders/final/photos');p.add_argument('--out',default='renders/final/paint-review');p.add_argument('--preview',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
 rows=audit(BASE,BASE/a.renders,BASE/a.out,a.preview)
 if a.check:assert rows and all(r['within_requested_bounds'] for r in rows.values()),'Receiver paint outside photographic bounds'
