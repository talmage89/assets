"""Original standard-shape graphics; deterministic, causally located fading/grime."""
import argparse,math,random
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
PAIRS=[('Aldervale Rd','Juniper Mill Ln'),('Cinderbrook St','Oriole Hollow Dr'),('Wrenfield Ave','Hazel Run Ct'),('Morrow Glen Rd','Foxmeadow Ln')]
FONT='/usr/share/fonts/TTF/DejaVuSansCondensed-Bold.ttf'
def legend(im,text,box,exact=False):
    f=ImageFont.truetype(FONT,420);bb=f.getbbox(text);mask=Image.new('L',(bb[2]-bb[0]+4,bb[3]-bb[1]+4));d=ImageDraw.Draw(mask);d.text((-bb[0],-bb[1]),text,font=f,fill=255)
    mask=mask.crop(mask.getbbox())
    if exact:mask=mask.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    else:mask.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    im.paste((239,241,226),(box[0]+(box[2]-box[0]-mask.width)//2,box[1]+(box[3]-box[1]-mask.height)//2),mask)
def weather(im,wear,seed):
    a=np.asarray(im).astype(float);h,w=a.shape[:2];y,x=np.mgrid[0:h,0:w];rng=np.random.default_rng(seed)
    # Sun fading grows toward top; dust collects at the bottom lip. Noise only breaks these masks.
    fade=wear*.045*(1-y/h);soil=wear*.12*np.exp(-(h-y)/(h*.045))*(.7+.3*np.sin(x/29)**2)
    a=a*(1-fade[:,:,None])+np.array([214,213,187])*fade[:,:,None]
    a=a*(1-soil[:,:,None])+np.array([76,66,43])*soil[:,:,None]
    return Image.fromarray(np.uint8(np.clip(a,0,255)))
def main():
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--wear',type=float,default=.35);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(2048,2048),(181,13,22));d=ImageDraw.Draw(im);aa=1024;bb=aa*(math.sqrt(2)-1)
    def octagon(r):return [(1024+x*r,1024+y*r) for x,y in [(-1,-bb/aa),(-bb/aa,-1),(bb/aa,-1),(1,-bb/aa),(1,bb/aa),(bb/aa,1),(-bb/aa,1),(-1,bb/aa)]]
    d.polygon(octagon(.984*aa),fill=(232,232,216));d.polygon(octagon(.939*aa),fill=(181,13,22));legend(im,'STOP',(285,680,1763,1368),True);weather(im,a.wear,4).save(out/'stop.png')
    for i,pair in enumerate(PAIRS):
        for j,text in enumerate(pair):
            im=Image.new('RGB',(3072,922),(5,80,44));d=ImageDraw.Draw(im);d.rounded_rectangle((25,25,3047,897),radius=42,outline=(222,233,210),width=16);legend(im,text,(100,254,2972,668));weather(im,a.wear,10+i*2+j).save(out/f'name-{i}-{j}.png')
if __name__=='__main__':main()
