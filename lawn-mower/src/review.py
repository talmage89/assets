"""Three bounded final docs and an inspected GLB-only contact sheet."""
import sys,json,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
from kit.delivery_docs import jpg
p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--final',action='store_true');a=p.parse_args();d=Path(a.renders)
meta=json.loads((d/'shots.json').read_text());names=[n for n in meta if not meta[n].get('skipped')];paths=[d/(n+'.png') for n in names]
if a.final:
 digest=meta['hero_closed']['source_sha256'];assert all(meta[n]['stage']=='final' and meta[n]['source_sha256']==digest for n in names)
 e=d.parent/'final-eevee/hero_closed.png';assert json.loads((e.parent/'shots.json').read_text())['hero_closed']['source_sha256']==digest;paths.append(e)
contact(paths,d/'contact.jpg',width=2400,title='Meadow 21 / exported GLB' if a.final else 'Meadow 21 / source review',captions={str(e):'Eevee / exported GLB'} if a.final else None)
if a.final:
 review_sheet([[d/'front.png',d/'side.png'],[d/'back.png',d/'top.png']],d/'turnaround.jpg',width=2000,title='Meadow 21 / exported turnaround')
 review_sheet([[d/'engine.png',d/'bag.png'],[d/'underside.png',d/'folded.png']],d/'details.jpg',width=2000,title='Meadow 21 / engine, textile, deck, folding handle')
 for src,dst in [('hero_closed.png','hero.jpg'),('turnaround.jpg','turnaround.jpg'),('details.jpg','details.jpg')]:jpg(d/src,ROOT/'lawn-mower/docs'/dst)
