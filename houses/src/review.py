"""Ignored checkpoint sheets only. Never creates final docs JPGs."""
import json
import math
from pathlib import Path
import sys
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.contact import contact,review_sheet
from kit.fonts import find_font
from plan import PROOF_SEEDS as SEEDS

FONT=find_font('Noto Sans','Regular')


def annotate(folder):
    meta=json.loads((folder/'provenance.json').read_text())
    for name in ('front','side'):
        im=Image.open(folder/(name+'.png')).convert('RGB');d=ImageDraw.Draw(im)
        font=ImageFont.truetype(FONT,19)
        for row in meta[name]['dimensions']:
            a,c=map(tuple,row['points']);d.line([a,c],fill=(18,28,24),width=2)
            delta=(c[0]-a[0],c[1]-a[1]);length=math.hypot(*delta)
            normal=(-delta[1]/length,delta[0]/length)
            for p in (a,c):d.line([(p[0]-normal[0]*7,p[1]-normal[1]*7),(p[0]+normal[0]*7,p[1]+normal[1]*7)],fill=(18,28,24),width=2)
            x,y=(a[0]+c[0])/2,(a[1]+c[1])/2
            text=row['label'];box=d.textbbox((0,0),text,font=font);w=box[2]-box[0]
            x=max(6,min(im.width-w-6,x-w/2));y=max(6,min(im.height-28,y-26))
            d.rounded_rectangle((x-4,y-1,x+w+4,y+27),radius=3,fill=(232,234,228));d.text((x,y),text,font=font,fill=(18,28,24))
        d.text((18,im.height-30),'Authored dimensions / actual mesh measurements in build/mesh-check.json',font=ImageFont.truetype(FONT,15),fill=(18,28,24))
        im.save(folder/(name+'-dimensions.jpg'),quality=94)


def seed_sheet():
    width=3600;cell=width//6;head=104;height=cell*5//8+62
    im=Image.new('RGB',(width,head+height),(231,234,229));d=ImageDraw.Draw(im)
    d.text((22,16),'One grammar / six independently built and reimported seeds',font=ImageFont.truetype(FONT,31),fill=(24,37,31))
    d.text((22,61),'Construction checkpoint • shared material roles / vertex tint • Cycles / procedural daylight',font=ImageFont.truetype(FONT,23),fill=(51,65,56))
    for i,seed in enumerate(SEEDS):
        source=Path(f'renders/seeds/{seed}/hero.png');img=Image.open(source).convert('RGB');img=ImageOps.contain(img,(cell,cell*5//8))
        im.paste(img,(i*cell,head));meta=json.loads(Path(f'build/seeds/house-{seed}.json').read_text())
        label=f"{seed} / {meta['spec']['main']['roof']} / {meta['spec']['garage']['side']} / {meta['triangles']:,} tris"
        d.text((i*cell+12,head+cell*5//8+12),label,font=ImageFont.truetype(FONT,21),fill=(24,37,31))
    im.save('renders/checkpoint/six-seeds.jpg',quality=94,optimize=True)
    contact([f'renders/seeds/{s}/hero.png' for s in SEEDS],'renders/checkpoint/seed-contact.jpg',width=2000,title='Six seeded construction proofs')


def main():
    folder=Path('renders/checkpoint');annotate(folder);seed_sheet()
    names=['hero.png','front-dimensions.jpg','side-dimensions.jpg','roof.png','top.png','eave.png','window.png','scale.png','back.png','door_open.png','valley.png']
    contact([folder/n for n in names if (folder/n).exists()],folder/'contact.jpg',width=2000,title='Builder colonial / construction checkpoint / reimported GLB')
    rows=[[folder/'hero.png'],[folder/'front-dimensions.jpg',folder/'side-dimensions.jpg'],[folder/'eave.png',folder/'window.png'],[folder/'roof.png',folder/'scale.png'],[Path('renders/matches/colonial_rog_ri-pair.jpg')],[Path('renders/matches/colonial_1991_oh-pair.jpg')]]
    review_sheet(rows,folder/'review-sheet.jpg',width=2200,title='Form checkpoint / placeholder materials / photo comparisons')
    im=np.asarray(Image.open(folder/'hero.png').convert('RGB'),dtype=float)/255
    # An image-region statistic, not a physical albedo measurement or a mask.
    crop=im[round(im.shape[0]*.23):round(im.shape[0]*.76),round(im.shape[1]*.16):round(im.shape[1]*.84)]
    l=crop@np.array([.2126,.7152,.0722])
    report=dict(scope='Display RGB luminance in approximate house region; includes sky at roof corners',
        percentiles=dict(zip(['p1','p5','p50','p95','p99'],map(float,np.percentile(l,[1,5,50,95,99])))),
        clipped_white_fraction=float(np.mean(np.all(crop>=.995,axis=-1))),
        pending='Physical albedo, dirt and used-roof calibration belong to look development')
    Path('build/tonal-check.json').write_text(json.dumps(report,indent=2))
    print('CHECKPOINT_SHEETS',folder/'contact.jpg',folder/'six-seeds.jpg',folder/'review-sheet.jpg')


if __name__=='__main__':main()
