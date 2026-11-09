"""Original compact craft strips and art glass; no reference-pixel inputs."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
from art_glass import glass


def make():
    out=Path('textures/ship');out.mkdir(parents=True,exist_ok=True)
    n=1024;rng=np.random.default_rng(4018);y,x=np.mgrid[:n,:n];u=x/n;v=1-y/n
    color=np.zeros((n,n,3));height=np.zeros((n,n));orm=np.ones((n,n,3));orm[:,:,2]=0
    grain=.5+.21*np.sin(x*.63+np.sin(y*.018)*1.6)+.07*np.sin(x*2.8+np.sin(y*.05))
    timber=v<1/3;slate=(v>=1/3)&(v<2/3);bronze=v>=2/3
    laminations=np.exp(-((np.mod(u,.055)-.001)/.002)**2)
    color[timber]=(np.array((.36,.19,.075))[None,:]*(.82+.32*grain[timber,None]))
    color[timber]*=(1-.20*laminations[timber,None]);height[timber]=grain[timber]*.00035;orm[timber,1]=.62
    row=np.floor(v*42);xx=u*12+np.mod(row,2)*.5;ix=np.floor(xx);joint=(np.mod(xx,1)<.025)|(np.mod(v*42,1)<.06)
    tone=.57+.92*rng.random((43,14))[np.clip(row.astype(int),0,42),np.clip(ix.astype(int),0,13)]
    color[slate]=(np.array((.064,.071,.074))*tone[slate,None]);color[slate&joint]*=.43
    height[slate]=.0013*(~joint[slate])+.00018*rng.random(np.count_nonzero(slate));orm[slate,1]=.83
    # Fine discontinuous oxidation; no broad sinusoidal bronze ribbons.
    granular=rng.random((n,n))
    for k in (1,3,7):granular=(granular+np.roll(granular,k,0)+np.roll(granular,k,1))/3
    patina=np.clip((granular-.47)*13,0,.8)
    color[bronze]=np.array((.19,.115,.038))*(1-patina[bronze,None]*.62)+np.array((.035,.09,.055))*patina[bronze,None]*.62
    orm[bronze,1]=.54;orm[bronze,2]=.78;height[bronze]=rng.random(np.count_nonzero(bronze))*.0002
    dy,dx=np.gradient(height);normal=np.stack((-dx*n/2,dy*n/2,np.ones_like(dx)),axis=2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
    # linear generated albedos -> sRGB; ORM and tangent normals remain linear.
    srgb=np.where(color<=.0031308,color*12.92,1.055*np.maximum(color,0)**(1/2.4)-.055)
    for suffix,a in [('BaseColor',srgb),('Normal',normal*.5+.5),('ORM',orm)]:Image.fromarray(np.uint8(np.clip(a*255+.5,0,255))).save(out/f'T_ChurchCraft_{suffix}.png')
    glass(out);letters(out)
    from turf import maps
    maps(out)


def letters(out):
    im=Image.new('RGBA',(1024,512),(255,255,255,0));d=ImageDraw.Draw(im)
    font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),52);layout={}
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&-:.'
    for i,c in enumerate(chars):
        x=(i%16)*64;y=(i//16)*128;d.text((x+32,y+50),c,font=font,anchor='mm',fill=(20,24,21,255),stroke_width=0)
        layout[c]=((x+2)/1024,1-(y+88)/512,(x+62)/1024,1-(y+12)/512)
    im.save(out/'T_ChurchLetters_BaseColor.png');Path('build/letters.json').write_text(json.dumps(layout))


if __name__=='__main__':make()
