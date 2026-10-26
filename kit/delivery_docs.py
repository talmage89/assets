"""Shared three-JPG delivery report, with exported-image provenance checks."""
import argparse,json,runpy
from pathlib import Path
from PIL import Image
from kit.contact import contact,review_sheet

def jpg(src,dst):
    im=Image.open(src).convert('RGBA');bg=Image.new('RGBA',im.size,(232,233,229,255));bg.alpha_composite(im);im=bg.convert('RGB');im.thumbnail((1600,16000),Image.Resampling.LANCZOS)
    dst.parent.mkdir(parents=True,exist_ok=True)
    for q in range(90,35,-3):
        im.save(dst,quality=q,optimize=True)
        if dst.stat().st_size<=200000:return
    raise RuntimeError('Documentation image exceeds 200 KB')

def main(root):
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--final',action='store_true');a=p.parse_args();folder=Path(a.renders)
    cfg=runpy.run_path(str(root/'src/config.py'));title=cfg.get('TITLE',root.name)
    meta=json.loads((folder/'shots.json').read_text())
    if not a.final:
        contact([folder/(n+'.png') for n in meta],folder/'contact.jpg',title=title);return
    names=['hero_closed','front','side','back','top','controls','casting','scale']+cfg.get('EXTRA_SHOTS',[])
    digest=meta['hero_closed']['source_sha256']
    for n in names:
        assert meta[n]['stage']=='final' and meta[n]['source'].endswith('.glb') and meta[n]['source_sha256']==digest
    eevee=folder.parent/'final-eevee/hero_closed.png'
    assert json.loads((eevee.parent/'shots.json').read_text())['hero_closed']['source_sha256']==digest
    contact([folder/(n+'.png') for n in names]+[eevee],folder/'contact.jpg',width=2400,title=title+' / exported GLB / Eevee last',captions={str(eevee):'Eevee / exported GLB'})
    review_sheet([[folder/'front.png',folder/'side.png'],[folder/'back.png',folder/'top.png']],folder/'turnaround.jpg',width=2000,title=title+' / exported turnaround')
    review_sheet([[folder/'controls.png',folder/'casting.png']],folder/'details.jpg',width=2400,title=title+' / exported details')
    for src,dst in [('hero_closed.png','hero.jpg'),('turnaround.jpg','turnaround.jpg'),('details.jpg','details.jpg')]:jpg(folder/src,root/'docs'/dst)
