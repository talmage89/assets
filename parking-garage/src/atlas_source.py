"""Original concrete/steel manufacture and causal-mark coverage, never photos.

4096 source channels are baked with kit.flat_bake, then filtered to 2048.
Horizontal tile bands repeat in U; mesh V is clipped to the declared band.
Fine manufacture belongs here; per-placement use history is separate.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT))
from kit.image_io import write_png

N=4096
BANDS={'precast':(0,2048),'cast':(2048,3072),'steel':(3072,3328)}
PALETTE={'Seal':('#252725',.90,0),'Yellow':('#c59728',.65,0),'Blue':('#294955',.65,0),
         'White':('#d5cdb4',.68,0),'Red':('#813b2d',.68,0),'Patch':('#938f7e',.91,0),'Light':('#e7e2c8',.38,0),
         'Stainless':('#b1b9b9',.44,.9)}
MARKS=('runoff','rust','mineral','oil','rubber','spall','droppings','scuff')


def field(w,h,seed,scale=32):
    rng=np.random.default_rng(seed);small=rng.uniform(0,1,(max(2,h//scale),max(2,w//scale))).astype('float32')
    ny,nx=small.shape
    wrapped=Image.fromarray(np.tile(small,(3,3)))
    return np.asarray(wrapped.resize((w,h),Image.Resampling.BICUBIC,box=(nx,ny,2*nx,2*ny))).copy()


def generate(folder=Path('build/lookdev/atlas-source'),layout_path=Path('build/lookdev/atlas-layout.json')):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    bc=np.empty((N,N,4),dtype=np.uint8);bc[:]=[145,139,125,255]
    orm=np.empty((N,N,3),dtype=np.uint8);orm[:]=[255,220,0]
    height=np.full((N,N),.5,np.float32);layout={};rng=np.random.default_rng(81288)
    for j,(key,(y0,y1)) in enumerate(BANDS.items()):
        h=y1-y0
        guarded=lambda seed,scale=32:np.pad(field(N,h-32,seed,scale),((16,16),(0,0)),mode='wrap')
        noise=guarded(31+j);fine=guarded(75+j,3)
        if key=='steel':
            color=np.array([93,99,95]);grain=guarded(12,2);variation=(noise-.5)*9+(grain-.5)*3
            orm[y0:y1]=[255,127,225];height[y0:y1]=.5+(fine-.5)*.008
        else:
            color=np.array([178,175,167] if key=='precast' else [165,162,154])
            variation=(noise-.5)*7+(fine-.5)*3
            pores=guarded(981+j,2)<.14
            variation-=pores*7
            # Faint form-bed drag and cement laitance; no fake brick grid.
            drag=np.pad(np.sin(np.arange(h-32)[:,None]*2*np.pi*round((h-32)/3.6)/(h-32)),((16,16),(0,0)),mode='wrap')*.7 if key=='precast' else 0
            variation+=drag;orm[y0:y1,:,1]=np.clip(213+(noise-.5)*28,0,255)
            height[y0:y1]=.5+(fine-.5)*.055-pores*.10
            if key=='cast':orm[y0:y1,:,1]=np.clip(165+(noise-.5)*24,0,255)
        bc[y0:y1,:,:3]=np.clip(color+variation[:,:,None],0,255)
        layout[key]=dict(rect=[0,1-(y1-16)/N,1,1-(y0+16)/N],coverage=[6.096,(y1-y0)/N*6.096],repeat_u=True)
    for j,(key,(color,r,m)) in enumerate(PALETTE.items()):
        x0=j*512;x1=x0+512;y0,y1=3328,3456
        rgb=tuple(bytes.fromhex(color[1:]));bc[y0:y1,x0:x1,:3]=rgb;orm[y0:y1,x0:x1]=[255,round(r*255),round(m*255)]
        layout[key]=dict(rect=[(x0+16)/N,1-(y1-16)/N,(x1-16)/N,1-(y0+16)/N],coverage=None,repeat_u=False)
    # Guarded coverage fields. Black is oil/rubber, rust is dilute iron oxide,
    # minerals/droppings remain chalky. They never tint the whole assembly.
    for j,key in enumerate(MARKS):
        x0=j*512;x1=x0+512;y0,y1=3456,4096;w,h=x1-x0,y1-y0
        yy,xx=np.mgrid[:h,:w];u=(xx-w/2)/(w/2-24);v=(yy-20)/(h-40)
        grain=field(w,h,709+j,7);macro=field(w,h,7091+j,32)
        rim=np.clip((1-np.abs(u))*7,0,1)*np.clip(v*12,0,1)*np.clip((1-v)*12,0,1)
        if key in ('runoff','rust','mineral'):
            # One leaking joint feeds a broad irregular root and narrowing
            # tributaries. In image space v=0 is the water source (mesh top).
            center=.10*np.sin(v*5.8)+.035*np.sin(v*23)
            fall=np.clip(1-v,0,1)
            width=.44*fall**1.25+.025+(macro-.5)*.12
            plume=np.exp(-((u-center)/np.maximum(width,.018))**2)
            branch=np.exp(-((u+.24-.30*v+.035*np.sin(v*11))/.055)**2)*np.clip((.72-v)*5,0,1)
            alpha=(plume*.88+branch*.40)*fall**.48*rim*(.62+.38*grain)
            if key=='mineral':
                # Salts crystallize beside the wetted core and at its toe.
                edge=np.exp(-((np.abs(u-center)-width*.72)/.065)**2)
                alpha=(edge*.8+plume*.22)*rim*(.48+.52*grain)*fall**.35
            alpha=np.clip(alpha*1.35,0,1)
            rgb={'runoff':(53,49,39),'rust':(126,57,24),'mineral':(224,218,195)}[key]
        elif key in ('oil','spall','droppings'):
            warp=(macro-.5)*.42;rad=(u*1.1+warp)**2+((v-.5)*2.25+warp)**2
            alpha=np.clip((.8-rad)*3,0,1)*(.35+.65*grain)*rim
            if key=='spall':
                fracture=np.maximum(np.abs(u*1.15+warp),np.abs((v-.5)*2.2-warp))+.09*np.sin(u*17+v*13)
                alpha=np.clip((.82-fracture)*9,0,1)*(.5+.5*grain)*rim
            if key=='oil':alpha*=.7+.3*np.sin(v*29+u*4)**2
            if key=='droppings':alpha*=np.clip((grain-.35)*4,0,1)
            rgb={'oil':(39,36,28),'spall':(126,122,109),'droppings':(209,202,177)}[key]
        else:
            alpha=np.exp(-((u+.08*np.sin(v*11))/.64)**4)*rim*(.38+.52*grain)
            alpha*=.55+.45*np.sin(u*34+v*3)**2
            rgb=(42,39,31) if key=='rubber' else (186,179,155)
        bc[y0:y1,x0:x1,:3]=rgb;bc[y0:y1,x0:x1,3]=np.rint(np.clip(alpha,0,1)*255)
        orm[y0:y1,x0:x1]=[255,110 if key=='rubber' else 120 if key=='oil' else 230,0]
        if key=='spall':height[y0:y1,x0:x1]=.5-.18*alpha
        layout[key]=dict(rect=[(x0+16)/N,1-(y1-16)/N,(x1-16)/N,1-(y0+16)/N],coverage=None,repeat_u=False)
    Image.fromarray(bc).save(folder/'T_ParkingGarage_BaseColor.png')
    Image.fromarray(orm).save(folder/'T_ParkingGarage_ORM.png')
    write_png(folder/'T_ParkingGarage_Height.png',height[:,:,None],bits=16)
    Path(layout_path).write_text(json.dumps(layout,indent=2)+'\n')
    print('ORIGINAL 4096 manufacture and eight causal coverage charts',flush=True)


if __name__=='__main__':generate()
