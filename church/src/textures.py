"""Original compact craft strips and art glass; no reference-pixel inputs."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font


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
    tone=.8+.36*rng.random((43,14))[np.clip(row.astype(int),0,42),np.clip(ix.astype(int),0,13)]
    color[slate]=(np.array((.064,.071,.074))*tone[slate,None]);color[slate&joint]*=.43
    height[slate]=.0013*(~joint[slate])+.00018*rng.random(np.count_nonzero(slate));orm[slate,1]=.83
    patina=(.5+.5*np.sin(x*.13+np.sin(y*.045)*6))**6
    color[bronze]=np.array((.19,.115,.038))*(1-patina[bronze,None]*.62)+np.array((.035,.09,.055))*patina[bronze,None]*.62
    orm[bronze,1]=.54;orm[bronze,2]=.78;height[bronze]=rng.random(np.count_nonzero(bronze))*.0002
    dy,dx=np.gradient(height);normal=np.stack((-dx*n/2,dy*n/2,np.ones_like(dx)),axis=2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
    # linear generated albedos -> sRGB; ORM and tangent normals remain linear.
    srgb=np.where(color<=.0031308,color*12.92,1.055*np.maximum(color,0)**(1/2.4)-.055)
    for suffix,a in [('BaseColor',srgb),('Normal',normal*.5+.5),('ORM',orm)]:Image.fromarray(np.uint8(np.clip(a*255+.5,0,255))).save(out/f'T_ChurchCraft_{suffix}.png')
    glass(out);letters(out)


def glass(out):
    n=1024;im=Image.new('RGB',(n,n),(6,8,10));d=ImageDraw.Draw(im)
    colors=[(49,66,72),(79,36,33),(92,72,34),(39,62,58),(49,43,72),(48,74,85)]
    rng=np.random.default_rng(906)
    # Three tall lancets plus a wheel chart. Leading is always dark; muted
    # colored panes become luminous through the switchable emission material.
    for cell in range(4):
        x0=(cell%2)*512;y0=(cell//2)*512
        for row in range(14):
            for col in range(7):
                x=x0+col*73+(row%2)*36;y=y0+row*37
                poly=[(x,y-37),(x+36,y),(x,y+37),(x-36,y)]
                d.polygon(poly,fill=colors[int(rng.integers(6))]);d.line(poly+[poly[0]],fill=(6,7,8),width=2)
        # An original plain geometric medallion, not religious iconography.
        cx=x0+256;cy=y0+240
        if cell in (1,2):
            d.ellipse((cx-96,cy-96,cx+96,cy+96),fill=(93,68,31),outline=(8,9,9),width=3)
            for k in range(8):
                a=k*np.pi/4;d.line((cx,cy,cx+96*np.cos(a),cy+96*np.sin(a)),fill=(8,9,9),width=2)
    a=np.array(im).astype(float)/255
    yy,xx=np.mgrid[:n,:n];waver=.96+.04*np.sin(xx*.18+np.sin(yy*.03)*2)*np.sin(yy*.13)
    a*=waver[:,:,None];Image.fromarray(np.uint8(np.clip(a*255,0,255))).save(out/'T_ChurchGlass_BaseColor.png')
    lead=np.max(a,axis=2)<.055
    h=lead*.0014+.00011*np.sin(xx*.09)*np.sin(yy*.13)
    dy,dx=np.gradient(h);norm=np.stack((-dx*n/3,dy*n/3,np.ones_like(dx)),axis=2);norm/=np.linalg.norm(norm,axis=2,keepdims=True)
    Image.fromarray(np.uint8((norm*.5+.5)*255)).save(out/'T_ChurchGlass_Normal.png')
    orm=np.ones((n,n,3));orm[:,:,1]=np.where(lead,.76,.28);orm[:,:,2]=np.where(lead,.35,0)
    Image.fromarray(np.uint8(orm*255)).save(out/'T_ChurchGlass_ORM.png')


def letters(out):
    im=Image.new('RGBA',(1024,512),(255,255,255,0));d=ImageDraw.Draw(im)
    font=ImageFont.truetype(find_font('DejaVu Sans','Bold'),52);layout={}
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789&-:.'
    for i,c in enumerate(chars):
        x=(i%16)*64;y=(i//16)*128;d.text((x+32,y+50),c,font=font,anchor='mm',fill=(20,24,21,255),stroke_width=0)
        layout[c]=((x+2)/1024,1-(y+88)/512,(x+62)/1024,1-(y+12)/512)
    im.save(out/'T_ChurchLetters_BaseColor.png');Path('build/letters.json').write_text(json.dumps(layout))


if __name__=='__main__':make()
