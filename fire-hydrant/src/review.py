"""Generate final docs only from the baked, exported GLB studio images."""
import argparse,json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet


def jpg(source,target):
    im=Image.open(source).convert('RGBA')
    bg=Image.new('RGBA',im.size,(231,233,229,255));bg.alpha_composite(im);im=bg.convert('RGB')
    im.thumbnail((1600,16000),Image.Resampling.LANCZOS)
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    for quality in range(90,39,-3):
        im.save(target,quality=quality,optimize=True)
        if target.stat().st_size<=200000:return
    raise RuntimeError('Docs JPG exceeds 200 KB: '+str(target))


def main():
    p=argparse.ArgumentParser();p.add_argument('--renders',required=True);p.add_argument('--final',action='store_true');a=p.parse_args()
    folder=Path(a.renders)
    names=['hero_closed','front','side','back','top','controls','casting','scale']
    if a.final:
        meta=json.loads((folder/'shots.json').read_text())
        for name in names:
            shot=meta[name]
            if shot['stage']!='final' or not shot['source'].endswith('.glb'):raise RuntimeError('Final docs require GLB images')
        eevee=folder.parent/'final-eevee/hero_closed.png'
        em=json.loads((eevee.parent/'shots.json').read_text())['hero_closed']
        if em['stage']!='final' or em['source_sha256']!=meta['hero_closed']['source_sha256']:raise RuntimeError('Eevee GLB provenance differs')
        paths=[folder/(n+'.png') for n in names]+[eevee]
        contact(paths,folder/'contact.jpg',width=2400,title='Bellford H-54 / exported GLB / Cycles + Eevee last',captions={str(eevee):'Eevee / exported GLB'})
        review_sheet([[folder/'front.png',folder/'side.png'],[folder/'back.png',folder/'top.png']],folder/'turnaround.jpg',width=2000,title='Bellford H-54 / exported turnaround')
        review_sheet([[folder/'controls.png',folder/'casting.png']],folder/'details.jpg',width=2400,title='Bellford H-54 / caps, chains and cast lettering')
        docs=Path(__file__).resolve().parents[1]/'docs'
        for source,name in [(folder/'hero_closed.png','hero.jpg'),(folder/'turnaround.jpg','turnaround.jpg'),(folder/'details.jpg','details.jpg')]:jpg(source,docs/name)
    else:
        paths=[folder/(n+'.png') for n in names if (folder/(n+'.png')).exists()]
        contact(paths,folder/'contact.jpg',width=1800,title='Bellford H-54 / source review')

if __name__=='__main__':main()
