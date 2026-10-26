"""Three final bounded JPGs and a complete exported-GLB contact sheet."""
import sys,json,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet
from kit.delivery_docs import jpg
p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--final',action='store_true');a=p.parse_args();folder=Path(a.renders)
meta=json.loads((folder/'shots.json').read_text());names=[n for n in meta if not meta[n].get('skipped')]
paths=[folder/(n+'.png') for n in names]
if a.final:
    digest=meta['hero_closed']['source_sha256']
    assert all(meta[n]['stage']=='final' and meta[n]['source_sha256']==digest for n in names)
    eevee=folder.parent/'final-eevee/hero_closed.png'
    assert json.loads((eevee.parent/'shots.json').read_text())['hero_closed']['source_sha256']==digest
    paths.append(eevee)
contact(paths,folder/'contact.jpg',width=2400,title='Evening 89 / exported GLB' if a.final else 'Evening 89 / source critique')
if a.final:
    review_sheet([[folder/'front.png',folder/'side.png'],[folder/'back.png',folder/'top.png']],folder/'turnaround.jpg',width=2000,title='Evening 89 / exported turnaround')
    review_sheet([[folder/'controls.png',folder/'burner.png'],[folder/'hero_open.png',folder/'lit.png']],folder/'details.jpg',width=2000,title='Evening 89 / control, emitter, tank access, lit state')
    for src,dst in [('hero_closed.png','hero.jpg'),('turnaround.jpg','turnaround.jpg'),('details.jpg','details.jpg')]:jpg(folder/src,ROOT/'patio-heater/docs'/dst)
