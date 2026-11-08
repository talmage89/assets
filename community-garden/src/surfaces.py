"""Shared metric finish tiles, authored analytically then baked with kit.flat_bake.

The atlas costs 16 MiB at 2K, shared by the entire family and all sites.
Wood UV V is height above soil; grain follows each timber's long axis.
"""
from pathlib import Path
import math,json,sys
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png
NAMES=('Wood','OldWood','EndWood','Soil','WetSoil','Straw','Chip','Gravel','Block','Zinc','Green','Blue','White','Hose','Steel','Roof')
# Small constant-color botanical/hardware swatches share the last atlas cell.
# These are physical albedo/roughness swatches, not lighting painted onto plants.
PALETTE={'Roof':((43,43,37),.90,0),'Stem':((72,108,43),.77,0),'Fruit':((173,45,22),.43,0),
         'Unripe':((101,127,36),.48,0),'Turning':((180,114,28),.46,0),'Yellow':((211,161,37),.76,0),
         'Flower':((184,100,25),.78,0),'Spent':((96,70,36),.94,0),'Red':((152,44,30),.76,0),
         'Cloth':((39,43,39),.95,0),'Brass':((142,111,56),.46,.83),'Glass':((103,124,129),.24,0),
         'Bark':((91,77,58),.90,0)}
ALIASES={}

def rect(name):
    if name in PALETTE:
        i=list(PALETTE).index(name);x=3+(i%4)/4;y=3+(i//4)/4;step=.0625
        return (x/4+.001,y/4+.001,x/4+step-.001,y/4+step-.001)
    i=NAMES.index(name);x=i%4;y=i//4
    return (x/4+.003,y/4+.003,(x+1)/4-.003,(y+1)/4-.003)

def generate(size=4096):
    out=Path('textures/source-surfaces');out.mkdir(parents=True,exist_ok=True)
    bc=np.empty((size,size,3),np.uint8);orm=np.full((size,size,3),(255,210,0),np.uint8);height=np.zeros((size,size),np.float32)
    rng=np.random.default_rng(7351);n=size//4;x,y=np.meshgrid(np.linspace(0,1,n),np.linspace(1,0,n))
    # Periodic multiscale noise: all source pixels are our own seeded fields.
    noise=np.zeros((n,n));fine=rng.random((n,n))-.5
    for freq,amp in ((3,.38),(11,.19),(37,.085),(103,.038)):
        for j in range(3):
            a=rng.uniform(0,math.tau);noise+=amp/3*np.sin(math.tau*freq*(x*math.cos(a)+y*math.sin(a))+rng.random()*6.28)
    for i,name in enumerate(NAMES):
        base=np.zeros((n,n,3));h=np.zeros((n,n));rough=np.full((n,n),.85);metal=np.zeros((n,n));ao=np.ones((n,n))
        if 'Wood' in name:
            old=name!='Wood';wave=y+.018*np.sin(x*11)+.006*np.sin(x*31+y*5)
            grain=np.sin(wave*math.tau*75+np.sin(wave*40+x*6)*2);checks=np.clip((np.cos(wave*math.tau*91)-.985)*60,0,1)*np.clip(np.sin(x*41+y*3)*3-.8,0,1)
            knot=np.exp(-(((x-.30)/.07)**2+((y-.57)/.12)**2));rings=np.sin(np.hypot((x-.30)*2,y-.57)*210)*knot
            base[:]=([119,117,103] if old else [142,113,76]);base+=(noise*.12+grain*.035+rings*.04)[:,:,None]*np.array([90,82,65]);h=grain*.00018-checks*.0014+knot*rings*.00045
            # Soil contact: local dampness at low timber only, broken by grain.
            damp=np.clip((.18-y+noise*.06)/.16,0,1);base*=1-damp[:,:,None]*.47;base-=checks[:,:,None]*26
            if name=='EndWood':base*=.81
            rough[:]=.88;ao-=checks*.25
        elif name in ('Soil','WetSoil'):
            wet=name=='WetSoil';moist=np.clip(.62+noise*1.6+np.sin(x*11+y*8)*.16,0,1) if wet else np.clip(noise*.6,0,.3)
            base[:]=[81,64,42];base*=1-moist[:,:,None]*.52
            crumbs=np.clip(fine*2+.15,0,1);base+=noise[:,:,None]*24+fine[:,:,None]*11;h=noise*.009+crumbs*.0017;rough=.97-moist*.19;ao-=crumbs*.12
        elif name in ('Straw','Chip'):
            base[:]=[126,111,72] if name=='Straw' else [101,77,48];h=noise*.004;base+=noise[:,:,None]*28+fine[:,:,None]*7
            # Settled broken fibers/chips with their own orientation, ends and shade.
            c=Image.fromarray(np.uint8(np.clip(base,0,255)));hm=Image.fromarray(np.uint8(np.clip(h/.015+.4,0,1)*255));d=ImageDraw.Draw(c);hd=ImageDraw.Draw(hm)
            for k in range(2100 if name=='Straw' else 2200):
                xx,yy=rng.integers(0,n,2);a=rng.uniform(0,math.tau);l=rng.uniform(.018,.085 if name=='Straw' else .055)*n;w=rng.uniform(.0015,.005 if name=='Straw' else .008)*n
                dx,dy=math.cos(a)*l,math.sin(a)*l;px,py=-math.sin(a)*w,math.cos(a)*w;poly=[(xx-px,yy-py),(xx+dx-px*.6,yy+dy-py*.6),(xx+dx+px*.6,yy+dy+py*.6),(xx+px,yy+py)]
                col=np.array([155,133,83] if name=='Straw' else ([125,120,105] if rng.random()<.35 else [122,93,61]))*rng.uniform(.55,1.32)
                d.polygon(poly,fill=tuple(np.uint8(col)));hd.polygon(poly,fill=int(rng.uniform(120,205)))
            base=np.asarray(c);h=(np.asarray(hm,dtype=float)/255-.4)*.015;ao=.78+.22*np.clip(h/.006,0,1)
        elif name=='Gravel':
            # 2–12 mm crushed stone in warm compacted fines. Individual
            # angular grains and facets survive 4K -> 2K at the metric scale.
            base[:]=[132,119,94];base+=noise[:,:,None]*11+fine[:,:,None]*8
            c=Image.fromarray(np.uint8(np.clip(base,0,255)));hm=Image.new('L',(n,n),106)
            draw=ImageDraw.Draw(c);hd=ImageDraw.Draw(hm)
            for k in range(14000):
                xx,yy=rng.integers(0,n,2);radius=rng.uniform(1.5,6.0);a=rng.random()*math.tau
                points=[(xx+radius*rng.uniform(.65,1.2)*math.cos(a+j*math.tau/5),yy+radius*rng.uniform(.65,1.2)*math.sin(a+j*math.tau/5)) for j in range(5)]
                color=np.array(([163,153,131],[116,111,98],[184,172,144],[98,94,84])[k%4])*rng.uniform(.82,1.07)
                draw.polygon(points,fill=tuple(np.uint8(color)));hd.polygon(points,fill=round(rng.uniform(125,200)))
                # Fractured mineral face; height belongs to the real grain.
                draw.polygon([points[0],points[1],(xx,yy)],fill=tuple(np.uint8(np.clip(color*1.09,0,255))))
            base=np.asarray(c,dtype=float);h=(np.asarray(hm,dtype=float)/255-.40)*.009
            rough[:]=.94;ao=.79+.21*np.clip(h/.0035,0,1)
            compressed=(x>.94)&(x<.985)&(y>.02)&(y<.05)
            base[compressed]=np.array([115,106,85])+fine[compressed,None]*7
            h[compressed]=fine[compressed]*.00035;ao[compressed]=.98
        elif name=='Block':
            base[:]=[133,132,119];base+=noise[:,:,None]*22+fine[:,:,None]*21
            moss=np.clip((.20-y+noise*.12)*6,0,.8);salt=np.clip(noise*2.3+.10,0,.55)*(1-y*.55)
            base=base*(1-moss[:,:,None])+np.array([59,71,36])*moss[:,:,None];base+=salt[:,:,None]*35;h=noise*.0007+fine*.0013;rough[:]=.94;ao-=abs(fine)*.16
        elif name=='Zinc':
            base[:]=[133,143,143];base+=noise[:,:,None]*35;rust=np.clip((.16-y+noise*.23)*5,0,.85);base=base*(1-rust[:,:,None])+np.array([106,60,28])*rust[:,:,None];metal=.92-rust*.82;rough=.47+rust*.34;h=noise*.0001
        elif name in ('Green','Blue','White','Hose','Steel','Roof'):
            colors={'Green':[59,91,75],'Blue':[58,91,116],'White':[175,170,148],'Hose':[38,63,40],'Steel':[67,67,58],'Roof':[43,43,37]};base[:]=colors[name]
            sunfade=np.clip(y-.38+noise*.22,0,.6);base+=sunfade[:,:,None]*22+noise[:,:,None]*12
            mud=np.clip((.18-y+noise*.10)*5,0,.65);base=base*(1-mud[:,:,None])+np.array([69,58,36])*mud[:,:,None]
            if name in ('Green','Blue'):
                chips=np.clip((noise+.13)*8,0,1)*np.clip((.08-y)*25,0,1);base=base*(1-chips[:,:,None])+np.array([109,76,45])*chips[:,:,None]
            h=noise*(.001 if name=='Roof' else .00018);rough[:]=.78
        ya=(3-i//4)*n;xa=i%4*n;bc[ya:ya+n,xa:xa+n]=np.uint8(np.clip(base,0,255));orm[ya:ya+n,xa:xa+n]=np.uint8(np.stack((np.broadcast_to(ao,(n,n)),np.broadcast_to(rough,(n,n)),np.broadcast_to(metal,(n,n))),axis=-1)*255);height[ya:ya+n,xa:xa+n]=np.clip(h/.030+.5,0,1)
    for name,(color,rough,metal) in PALETTE.items():
        i=list(PALETTE).index(name);xa=(12+i%4)*size//16;ya=(3-i//4)*size//16;nn=size//16
        bc[ya:ya+nn,xa:xa+nn]=color;orm[ya:ya+nn,xa:xa+nn]=(255,round(rough*255),round(metal*255));height[ya:ya+nn,xa:xa+nn]=.5
    for channel,a in [('BaseColor',bc),('ORM',orm),('Height',np.repeat(np.uint16(height*65535)[:,:,None],3,axis=2))]:write_png(out/f'T_GardenSurfaces_{channel}.png',a.astype(np.float32)/(65535 if channel=='Height' else 255),bits=16 if channel=='Height' else 8)
    Path('build/surface-layout.json').write_text(json.dumps({n:rect(n) for n in NAMES},indent=2))

if __name__=='__main__':generate()
