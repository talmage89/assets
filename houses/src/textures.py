"""Original periodic house fields. No photographic inputs and no projection bake.

Linear albedo and meter-scale heights are authored first; the PNGs carry sRGB
color, OpenGL tangent normals and linear ORM. This is source look development.
"""
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.image_io import write_png,linear_to_srgb

SETS=dict(Siding=(1024,2.4384),Shingles=(2048,4.8768),Veneer=(512,1.2192),Concrete=(512,2.4384),Trim=(2048,4.0))


def noise(n,cells,rng):
    a=rng.random((cells,cells)).astype('float32')
    a=np.pad(a,1,mode='wrap')
    im=Image.fromarray(a).resize((round(n*(cells+2)/cells),)*2,Image.Resampling.BICUBIC)
    a=np.asarray(im);off=round(n/cells)
    return a[off:off+n,off:off+n]


def fields(name,n,coverage):
    rng=np.random.default_rng(7901+list(SETS).index(name));y,x=np.mgrid[0:n,0:n].astype('float32')
    x=x/n*coverage;y=(n-1-y)/n*coverage
    fine=rng.random((n,n)).astype('float32');broad=noise(n,16,rng);mid=noise(n,64,rng)
    h=np.zeros((n,n),dtype='float32');rough=np.full_like(h,.72);metal=np.zeros_like(h);ao=np.ones_like(h)
    if name=='Siding':
        course=np.mod(y,.1016)/.1016
        butt=np.exp(-course/.12)
        grain=np.sin(x*410+mid*5)*np.sin(x*176+mid*3)
        h=.0105*course+.00007*grain+.00032*np.sin(x*np.pi*2/.4064)*np.sin(course*np.pi)
        value=(1.00-.58*butt+.012*(mid-.5))
        color=np.repeat(value[:,:,None],3,axis=2)
        ao=1-.38*butt;rough[:]=.53;rough+=.045*(fine-.5)
    elif name=='Shingles':
        exposure=coverage/34;row=np.floor(y/exposure).astype(int);v=np.mod(y,exposure)/exposure
        # Eight irregular laminated tabs per meter, row staggering and seeded widths.
        tab=np.zeros((n,n),dtype=int);val=np.zeros_like(h)
        table=rng.uniform(.88,1.14,(34,28))
        for j in range(34):
            boundaries=np.cumsum(rng.uniform(.13,.34,26));boundaries=boundaries/boundaries[-1]*coverage
            mask=row==j;tab[mask]=np.searchsorted(boundaries,np.mod(x[mask]+j*.137,coverage))
            val[mask]=table[j,tab[mask]]
        overlap=np.exp(-v/.032);lam=((tab+row*7)%5<2)&(v<.45)
        base=.105*val*(.78+.44*fine)*(.92+.16*broad)
        base*=1-.47*overlap;base*=np.where(lam,.90,1.)
        color=np.stack([base*.98,base,base*.98],axis=-1)
        h=.006*v+.0022*lam+.00038*(fine-.5)
        ao=1-.40*overlap;rough=.88+.1*(fine-.5)
    elif name=='Veneer':
        cw=coverage/6;ch=coverage/18;row=np.floor(y/ch).astype(int)
        xx=np.mod(x+(row%2)*cw/2,cw);col=np.floor((x+(row%2)*cw/2)/cw).astype(int)%6
        yy=np.mod(y,ch);edge=np.minimum.reduce([xx,cw-xx,yy,ch-yy])
        brick=np.clip((edge-.0038)/.003,0,1)
        table=rng.uniform(.72,1.30,(18,6));v=table[row%18,col]
        red=np.array([.265,.080,.044]);mortar=np.array([.235,.215,.181])
        face=red[None,None,:]*v[:,:,None]*(.86+.28*mid[:,:,None])
        color=face*brick[:,:,None]+mortar*(1-brick[:,:,None])
        h=.009*brick+.00065*(mid-.5)*brick;ao=.70+.30*brick;rough=.9+.06*(fine-.5)
    elif name=='Concrete':
        value=.95+.12*(broad-.5)+.08*(mid-.5)+.07*(fine-.5)
        color=np.array([.39,.38,.35])*value[:,:,None]
        # Poured-form tie divots on a 4 ft by 2 ft staggered grid.
        dx=np.abs(np.mod(x+.6096,1.2192)-.6096);dy=np.abs(np.mod(y+.3048,.6096)-.3048)
        tie=np.exp(-(dx*dx+dy*dy)/.00012)
        color*=1-.48*tie[:,:,None];h=.0009*(mid-.5)-.005*tie
        ao=1-.35*tie;rough=.87+.08*(fine-.5)
    else:
        # Eight horizontal, U-periodic 256 px strips. UVs select the physical finish.
        q=y/coverage;strip=np.floor(q*8).astype(int);local=np.mod(q*8,1)
        color=np.ones((n,n,3),dtype='float32')*.985
        h=.000035*(fine-.5);rough[:]=.49
        louvers=strip==1;phase=np.mod(local*16,1)
        color[louvers]*=(1-.32*np.exp(-phase[louvers]/.09))[:,None]
        h[louvers]+=.0014*phase[louvers]
        perf=(strip==2)&(np.sin(x*2*np.pi/.015)>.60)&(np.sin(local*2*np.pi*20)>.62)
        color[perf]*=.28;h[perf]-=.0009
        wood=strip==3;grain=np.sin(x*240+mid*8)*.5+.5
        color[wood]*=(.78+.20*grain[wood])[:,None];h[wood]+=.00022*grain[wood];rough[wood]=.81
        blind=strip==4;phase=np.mod(local*18,1)
        color[blind]*=(.92-.30*np.exp(-phase[blind]/.1))[:,None];h[blind]+=.0008*phase[blind]
        met=strip==5;rough[met]=.37
        metal[met&(x>coverage*.75)]=.8
        clear=strip==6;color[clear]=[.97,.985,1.];rough[clear]=.035;h[clear]=0
        screen=strip==7
        # Effective coverage of a subpixel insect screen, no oversized checker mesh.
        color[screen]=[.83,.85,.84];rough[screen]=.105;h[screen]=.000006*(fine[screen]-.5)
    return color,h,ao,rough,metal


def main(folder=Path('textures/source')):
    folder.mkdir(parents=True,exist_ok=True);report={}
    for name,(n,coverage) in SETS.items():
        color,h,ao,rough,metal=fields(name,n,coverage)
        dx=(np.roll(h,-1,axis=1)-np.roll(h,1,axis=1))/(2*coverage/n)
        dy=(np.roll(h,-1,axis=0)-np.roll(h,1,axis=0))/(2*coverage/n)
        normal=np.stack([-dx,dy,np.ones_like(h)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
        maps=dict(BaseColor=linear_to_srgb(color),Normal=normal*.5+.5,ORM=np.stack([ao,rough,metal],axis=-1))
        paths=[]
        for channel,a in maps.items():
            path=folder/f'T_House{name}_{channel}.png';write_png(path,a,bits=8);paths.append(path)
        # BC7 base + BC5 normal + BC7 ORM, full mip chain, rounding negligible.
        memory=n*n*3*4/3
        report[name]=dict(size=n,coverage_m=coverage,texels_per_m=n/coverage,
            linear_albedo_mean=list(map(float,color.mean(axis=(0,1)))),
            gpu_mib=memory/1048576,png_bytes=sum(p.stat().st_size for p in paths),
            maps=[str(p) for p in paths],stage='authored source fields, not a Cycles projection bake')
        print(name,report[name])
    (folder/'sets.json').write_text(json.dumps(report,indent=2))


if __name__=='__main__':main()
