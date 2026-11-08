"""Native correction crops and bounded final gallery; never fabricates pixels.

Before images are archived historical export renders. Every after image has
its current export-bundle receipt. Gallery generation is a separate final step.
"""
import argparse,json,hashlib,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.fonts import find_font
from kit.contact import review_sheet,contact
FONT=find_font('Noto Sans')


def corrections(folder):
    before=Path('build/delivery-before/renders');after=Path(folder);out=Path('renders/fix-crops');out.mkdir(parents=True,exist_ok=True);rows=[]
    fixes=[('01-summer-turf','229/hero.png',(0,230,1200,727)),
           ('02-park-plots-and-building','229/hero.png',None),
           ('03a-tomato','plants/tomato.png',None),
           ('03b-varied-heads','229/hero.png',(0,325,1000,727)),
           ('04-upright-corn-ears','plants/corn-ear.png',None),
           ('05-row-cover-at-frame-edge','117/hero.png',(400,200,1200,727)),
           ('06-granular-accessible-court','341/hero.png',(0,220,1200,727)),
           *[(f'07-{n}-whole-garden-pair',f'matches/{n}.png',None) for n in ('wise_bed','cityhall_mature','martin_place')],
           *[(f'08-{s}-clear-low-sun',f'{s}/hero.png',None) for s in (117,229,341)]]
    for name,file,box in fixes:
        paths=[]
        for stage,root in [('before',before),('after',after)]:
            image=Image.open(root/file).convert('RGB')
            if box:
                # Crop at identical normalized sensor bounds when a final is
                # rendered wider; no upsampling of historical evidence.
                scale=image.width/1200;crop=tuple(round(x*scale) for x in box);image=image.crop(crop)
            assert image.width>=800,(name,stage,image.size)
            path=out/(name+'-'+stage+'.png');image.save(path);paths.append(path)
        # Individual PNG panels retain every native pixel. The comparison
        # reduces only a larger raster to the smaller pane's scale, so equal
        # camera framing is also equal display size. Never upsample evidence.
        ims=[Image.open(p) for p in paths];w=min(i.width for i in ims)
        display=[i if i.width==w else i.resize((w,round(i.height*w/i.width)),Image.Resampling.LANCZOS) for i in ims];h=max(i.height for i in display)
        canvas=Image.new('RGB',(w*2,h+70),(232,234,228));d=ImageDraw.Draw(canvas);font=ImageFont.truetype(FONT,22)
        for j,(im,label) in enumerate(zip(display,('Before','After'))):
            canvas.paste(im,(j*w,70));d.text((j*w+15,12),name+' / '+label,font=font,fill=(20,30,20))
        target=out/(name+'.jpg');canvas.save(target,quality=95,optimize=True)
        rows.append(dict(fix=name,source=file,crop_1200px=box,before=str(paths[0]),after=str(paths[1]),pair=str(target),panels=[list(i.size) for i in ims],comparison_panels=[list(i.size) for i in display]))
    # Cameras are unchanged for the three heroes and botanical specimens.
    for file in ('117/hero.json','229/hero.json','341/hero.json','plants/tomato.json','plants/corn.json','plants/corn-ear.json'):
        old=json.loads((before/file).read_text())['camera'];new=json.loads((after/file).read_text())['camera']
        for key in ('location','target','lens','aspect'):assert np.allclose(old[key],new[key]),(file,key)
    (out/'receipt.json').write_text(json.dumps(dict(crops=rows,hero_and_specimen_cameras_identical=True,scope='native crops of actual historical/current exported renders; pair cameras move from isolated fixtures to equivalent landmarks inside full sites'),indent=2))


def docs(folder):
    folder=Path(folder)
    provenance=json.loads((folder/'provenance.json').read_text());assert provenance['passed']
    visual=json.loads(Path('build/final-visual-review.json').read_text())
    assert visual['passed'] and visual['fixes_visible']
    for path,digest in visual['images'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,('Unreviewed changed image',path)
    assert set(visual['images'])=={str(p) for p in folder.rglob('*.png')},'A final render has not been reviewed'
    target=Path('docs');target.mkdir(exist_ok=True)
    files={f'hero-{s}.jpg':folder/str(s)/'hero.png' for s in (117,229,341)}
    construction=[folder/str(s)/'above.png' for s in (117,229,341)]+[folder/'plants.png',folder/'pieces.png']
    contact(construction,folder/'family-gallery.jpg',width=1600,title='Three gardens / growth stages / construction')
    files['family.jpg']=folder/'family-gallery.jpg'
    detail=[folder/'117/corner.png',folder/'117/tomato.png',folder/'341/bean.png',folder/'341/squash.png',folder/'117/compost.png',folder/'117/water.png',folder/'117/shed.png',folder/'117/scale.png',folder/'117/eevee.png']
    review_sheet([detail[i:i+3] for i in range(0,len(detail),3)],folder/'detail-gallery.jpg',width=1600,title='Construction / midsummer crops / scale / Eevee')
    files['details.jpg']=folder/'detail-gallery.jpg';rows=[]
    for name,source in files.items():
        original=Image.open(source).convert('RGB');path=target/name;width=1600
        while True:
            im=original.copy();im.thumbnail((width,8000),Image.Resampling.LANCZOS)
            for q in range(94,24,-2):
                im.save(path,quality=q,optimize=True)
                if path.stat().st_size<=200000:break
            if path.stat().st_size<=200000:break
            width=round(width*.9);assert width>=800,'Gallery remains too large at readable width'
        assert path.stat().st_size<=200000
        rows.append(dict(path=str(path),size=list(im.size),bytes=path.stat().st_size,source=str(source),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    Path('build/docs.json').write_text(json.dumps(rows,indent=2))


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='renders/final');p.add_argument('--docs',action='store_true');a=p.parse_args()
    if a.docs:docs(a.out)
    else:corrections(a.out)

if __name__=='__main__':main()
