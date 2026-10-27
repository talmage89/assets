"""GLB-only evidence, matched values, head windows and final compact docs."""
import argparse,sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.contact import contact,review_sheet
from values import measure,BOX_PATCHES,stats
from photo_matches import MATCHES
from hydrangea_matches import PATCHES

NAMES=('hero','front','side','back','top','close_1m','scale')

def review(folder,species,glb,eevee=None):
    metadata=json.loads((folder/'shots.json').read_text());digest=hashlib.sha256(glb.read_bytes()).hexdigest()
    assert all(x['source_sha256']==digest and x['stage'].startswith('EXPORTED GLB') for x in metadata.values()),'stale/non-GLB images'
    assert all((folder/(name+'.png')).exists() for name in metadata)
    paths=[folder/(n+'.png') for n in NAMES if n in metadata]
    if eevee:
        row=json.loads((eevee/'shots.json').read_text())['hero'];assert row['source_sha256']==digest and row['stage'].startswith('EXPORTED GLB')
        paths.append(eevee/'hero.png')
    contact(paths,folder/'contact.jpg',title=species.title()+' / exported GLB, baked shared maps')
    if all(n in metadata for n in ('front','side','back','top')):
        contact([folder/(n+'.png') for n in ('front','side','back','top')],folder/'turnaround.jpg',title=species.title()+' / front, side, back, top')
    patches=PATCHES if species=='hydrangea' else {k:dict(crop=MATCHES[k]['crop'],**v) for k,v in BOX_PATCHES.items()}
    calibration=ROOT/('shrubs/build/hydrangea/framed-cameras.json' if species=='hydrangea' else 'shrubs/build/framed-cameras.json')
    values=measure(folder,calibration,patches)
    head_values={}
    for name,row in metadata.items():
        if name in patches:
            im=Image.open(folder/(name+'.png'));bb=im.getchannel('A').getbbox();assert bb and bb[0]>1 and bb[1]>1 and bb[2]<im.width-1 and bb[3]<im.height-1,(name,'clipped',bb)
        if species!='hydrangea':continue
        im=Image.open(folder/(name+'.png'));rows=[]
        for i,window in enumerate(row['head_windows_normalized']):
            x0,y0,x1,y1=window;rect=(max(0,round(x0*im.width)),max(0,round(y0*im.height)),min(im.width,round(x1*im.width)),min(im.height,round(y1*im.height)))
            if rect[2]<=rect[0] or rect[3]<=rect[1]:continue
            v=stats(im.crop(rect),'flower')
            if not v.get('insufficient'):rows.append(dict(head=i,rect=rect,**v))
        head_values[name]=rows
    report=dict(passed=True,glb_sha256=digest,render_count=len(metadata),eevee=bool(eevee),scope='GLB provenance and display-value regions; projected head windows can include neighbors, not isolated head IDs')
    (folder/'render-check.json').write_text(json.dumps(report,indent=2))
    if head_values:(folder/'head-values.json').write_text(json.dumps(head_values,indent=2))
    return values


def main():
    p=argparse.ArgumentParser();p.add_argument('--boxwood',type=Path,default=Path('renders/final'));p.add_argument('--hydrangea',type=Path,default=Path('renders/hydrangea-final'));p.add_argument('--glb',type=Path,default=Path('export/Shrubs.glb'));p.add_argument('--docs',action='store_true');a=p.parse_args()
    values={}
    for species,folder,eevee in [('boxwood',a.boxwood,Path('renders/final-eevee')),('hydrangea',a.hydrangea,Path('renders/hydrangea-eevee'))]:
        values[species]=review(folder,species,a.glb,eevee if a.docs else None)
    out=Path('renders/family-final');out.mkdir(parents=True,exist_ok=True)
    rows=[[a.boxwood/(n+'.png'),a.hydrangea/(n+'.png')] for n in NAMES if (a.boxwood/(n+'.png')).exists() and (a.hydrangea/(n+'.png')).exists()]
    if a.docs:rows.append([Path('renders/final-eevee/hero.png'),Path('renders/hydrangea-eevee/hero.png')])
    review_sheet(rows,out/'contact.jpg',width=1600,title='Foundation shrubs / exported family GLB / one shared 2048 set')
    (out/'values.json').write_text(json.dumps(values,indent=2))
    if not a.docs:return
    docs=Path('docs');docs.mkdir(exist_ok=True)
    def jpg(source,target):
        im=Image.open(source).convert('RGB');im.thumbnail((1600,1600))
        for quality in (91,86,81,75,68,60,52):
            im.save(docs/target,quality=quality,optimize=True)
            if (docs/target).stat().st_size<=200000:break
        assert (docs/target).stat().st_size<=200000
    jpg(a.boxwood/'hero.png','boxwood.jpg');jpg(a.hydrangea/'hero.png','hydrangea.jpg')
    contact([a.boxwood/'turnaround.jpg',a.hydrangea/'turnaround.jpg'],out/'turnarounds.jpg',title='Boxwood / hydrangea — exported GLB turnaround')
    jpg(out/'turnarounds.jpg','turnarounds.jpg')
    contact([a.boxwood/'close_1m.png',a.hydrangea/'close_1m.png',a.boxwood/'scale.png',a.hydrangea/'scale.png',Path('renders/final-eevee/hero.png'),Path('renders/hydrangea-eevee/hero.png')],out/'details.jpg',title='Shared baked maps / leaf detail, scale and Eevee')
    jpg(out/'details.jpg','details.jpg')
    jpg(out/'contact.jpg','family.jpg')
if __name__=='__main__':main()
