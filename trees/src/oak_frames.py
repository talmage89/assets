"""Shared photo framing with explicit oak comparison daylight controls."""
import argparse,sys,json
from pathlib import Path
sys.path[:0]=[str(Path(__file__).resolve().parents[2]),str(Path(__file__).resolve().parent)]
from kit.photo_frame import frame
from oak_matches import MATCHES
p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--out');a=p.parse_args()
frame(a.source,a.out,.12,.08)
r=json.loads(Path(a.out).read_text())
for name,row in r.items():row['shot']['lighting']=MATCHES[name]['lighting']
Path(a.out).write_text(json.dumps(r,indent=2))
