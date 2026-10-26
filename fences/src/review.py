"""Only final GLB imagery becomes the three bounded documentation JPGs."""
import argparse,json,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.contact import contact,review_sheet

def bounded(source,target):
    im=Image.open(source).convert('RGBA');bg=Image.new('RGBA',im.size,(232,233,229,255));bg.alpha_composite(im)
    im=bg.convert('RGB');im.thumbnail((1600,16000))
    for quality in range(90,39,-3):
        im.save(target,quality=quality,optimize=True)
        if Path(target).stat().st_size<200000:return
    raise RuntimeError('Documentation image too large')

p=argparse.ArgumentParser();p.add_argument('--final',action='store_true');p.add_argument('--renders',required=True);a=p.parse_args();f=Path(a.renders)
meta=json.loads((f/'shots.json').read_text())
if a.final:
    assert all(v['stage']=='final' and v['source'].endswith('.glb') for v in meta.values())
paths=[f/(n+'.png') for n in meta if (f/(n+'.png')).exists()]
eevee=f.parent/'final-eevee/hero_closed.png'
if eevee.exists():paths.append(eevee)
assembly=f.parent/'assembly'
if (assembly/'corner_good.png').exists():paths.extend([assembly/'corner_good.png',assembly/'corner_rails.png'])
contact(paths,f/'contact.jpg',width=2200,title='Wood privacy kit / exported GLB / Cycles + Eevee last')
if a.final:
    review_sheet([[f/'front.png',f/'back.png'],[f/'side.png',f/'top.png'],[f/'gate.png',f/'gate_back.png'],[f/'posts.png',f/'scale.png']],f/'modules-contact.jpg',width=2000,title='Privacy fence / module views / construction / scale')
    review_sheet([[f/'hero_open.png'],[f/'grain.png',f/'joinery.png',f/'hardware.png']],f/'construction-contact.jpg',width=2200,title='Rail side / original baked pine / physical hardware')
    docs=ROOT/'fences/docs';docs.mkdir(exist_ok=True)
    for src,name in [('../assembly/corner_good.png','privacy-hero'),('construction-contact.jpg','privacy-construction'),('modules-contact.jpg','privacy-modules')]:bounded(f/src,docs/(name+'.jpg'))
