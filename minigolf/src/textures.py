"""Original carpet loops, painted masonry, strata and metal. Never reads refs.

One 4K source field is GPU-validated and deterministically evaluated, then
filtered to the accepted 2K course atlas. UV rectangles have 8 delivered texels of protective inset. Large-scale
traffic/exposure/water masks live on the actual surface as linear Tint data.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from kit.image_io import write_png,linear_to_srgb
COLORS={
 'carpet':(.065,.22,.067),'carpet2':(.060,.175,.070),'carpet3':(.14,.245,.055),
 'concrete':(.38,.37,.32),'brick':(.25,.072,.035),'mortar':(.15,.145,.12),
 'wood':(.20,.18,.135),'rock':(.22,.18,.12),'rocklight':(.29,.23,.155),
 'red':(.32,.024,.016),'ivory':(.58,.55,.43),'navy':(.012,.042,.065),'white':(.62,.65,.59),
 'black':(.009,.013,.012),'metal':(.35,.37,.35),'rubber':(.009,.012,.011),
 'soil':(.040,.025,.012),'grass':(.065,.115,.027),'asphalt':(.035,.038,.038),
 'yellow':(.60,.32,.016),'leaf':(.18,.095,.018),'liner':(.16,.34,.38),
 'coping':(.62,.65,.59),'water':(.94,.98,.99),'glass':(.055,.085,.085),'foam':(.72,.75,.69),'stonepaint':(.40,.41,.36),'fallwater':(.78,.88,.85),'wetrock':(.29,.23,.155),'clothred':(.32,.024,.016),'clothivory':(.58,.55,.43)}
RECTS={name:(i*.25,0,(i+1)*.25,.5) for i,name in enumerate(list(COLORS)[:3])}
slots=[(i/8,j/8,(i+1)/8,(j+1)/8) for j in range(4,8) for i in range(8)]
RECTS.update(zip(list(COLORS)[3:],slots))

def noise(h,w,cells,rng):
 return np.asarray(Image.fromarray(rng.random((cells,cells),dtype=np.float32)).resize((w,h),Image.Resampling.BICUBIC))

def periodic_noise(u,v,cells,rng):
 lattice=rng.random((cells,cells),dtype=np.float32);x=u*cells;y=v*cells;ix=np.floor(x).astype(int);iy=np.floor(y).astype(int);fx=x-ix;fy=y-iy
 fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy)
 return (lattice[iy%cells,ix%cells]*(1-fx)+lattice[iy%cells,(ix+1)%cells]*fx)*(1-fy)+(lattice[(iy+1)%cells,ix%cells]*(1-fx)+lattice[(iy+1)%cells,(ix+1)%cells]*fx)*fy

def source(n=4096):
 out=Path('build/procedural');out.mkdir(parents=True,exist_ok=True)
 # Padding is a physical neutral paint, not black empty texels.
 bc=np.full((n,n,3),.16,np.float32);orm=np.zeros_like(bc);orm[:]=(1,.85,0);height=np.full((n,n),.5,np.float32)
 for key,(u0,v0,u1,v1) in RECTS.items():
  rng=np.random.default_rng(191+list(COLORS).index('rocklight' if key=='wetrock' else key));x0,x1=round(u0*n),round(u1*n);y0,y1=round((1-v1)*n),round((1-v0)*n);w=x1-x0;h=y1-y0
  yy,xx=np.mgrid[:h,:w].astype(np.float32);u=(xx+.5)/w;v=(yy+.5)/h
  fine=rng.random((h,w),dtype=np.float32);mid=noise(h,w,38,rng);broad=noise(h,w,6,rng)
  # The repeat is the protected interior, not the whole atlas rectangle.
  # This keeps both values and slopes continuous at the two-metre cell edges.
  pad_u=8/(2048*(u1-u0));pad_v=8/(2048*(v1-v0));pu=(u-pad_u)/(1-2*pad_u);pv=(v-pad_v)/(1-2*pad_v)
  if key in ('soil','rock','rocklight','wetrock'):
   fine=periodic_noise(pu,pv,180,rng);mid=periodic_noise(pu,pv,38,rng);broad=periodic_noise(pu,pv,6,rng)
  col=np.zeros((h,w,3),np.float32);col[:]=COLORS[key];rough=np.full((h,w),.86,np.float32);relief=np.full((h,w),.5,np.float32);metal=np.zeros((h,w),np.float32)
  if key.startswith('carpet'):
   # Rows of interlaced polypropylene loops. The roll is 3.66 x 9m here;
   # tuft pitch 5.2mm, sampled at 4K before normal/filtering.
   loops=(np.sin(u*math_tau*344+.35*np.sin(v*math_tau*130))*np.sin(v*math_tau*860))*.5+.5
   traffic=np.clip(np.exp(-((u-.5)/.095)**2)*np.sin(np.pi*v)**.5+np.exp(-((u-.5)/.10)**2-((v-.88)/.035)**2),0,1)
   # The delivered lane chart cannot resolve individual 5.2 mm tufts.
   # Preserve a small effective nap response: full pile-height relief aliases
   # into centimetre-scale lumps after filtering, especially beside the cup.
   relief=.35+(.045*loops+.018*(fine-.5))*(1-.65*traffic)
   col*=1+.29*(mid-.5)[:,:,None]+.24*(fine-.5)[:,:,None]
   col*=1+(.28*traffic)[:,:,None]
   rough[:]=.94-.09*traffic
   # Glue line, lengthwise roll join, and a rectangular repaired patch.
   seam=np.exp(-((u-.68)/.0025)**2);col*=1-.22*seam[:,:,None];relief-=.05*seam
   patch=(u>.19)&(u<.39)&(v>.18)&(v<.255);col[patch]*=(.79,.88,.78)
   edges=patch & ((abs(u-.19)<.003)|(abs(u-.39)<.003)|(abs(v-.18)<.002)|(abs(v-.255)<.002));col[edges]*=.64
  elif key in ('rock','rocklight','wetrock'):
   # Carved fracture network, irregular mineral washes and open aggregate.
   # Several octave scales, without evenly spaced horizontal bedding rules.
   cloud=periodic_noise(pu+.06*mid,pv+.04*broad,11,rng)
   stone=np.clip((cloud-.23)*1.6,0,1)
   gray=np.array((.46,.335,.18));tan=np.array((.265,.155,.066) if key!='rock' else (.20,.12,.055))
   col=gray[None,None,:]*(1-stone[:,:,None])+tan[None,None,:]*stone[:,:,None]
   col*=np.clip(.72+.58*broad+.32*(mid-.5),.5,1.4)[:,:,None]
   dist=[]
   for cx,cy in rng.random((13,2)):
    dx=(pu-cx+.5)%1-.5;dy=(pv-cy+.5)%1-.5
    dist.append(np.sqrt((dx+.035*(mid-.5))**2+(dy+.035*(broad-.5))**2))
   nearest=np.partition(np.stack(dist),1,axis=0)
   crack=np.exp(-((nearest[1]-nearest[0])/.004)**2)*np.clip((cloud-.49)*8,0,1)
   pores=np.clip((.38-fine)*5,0,1)*np.clip((mid-.28)*4,0,1)
   relief=.53+.045*(mid-.5)+.005*(fine-.5)-.23*crack-.025*pores
   col*=1-(.48*crack+.22*pores)[:,:,None]
   rough[:]=.96 if key!='wetrock' else .82
  elif key=='wood':
   grain=np.sin(u*math_tau*48+mid*4+np.sin(v*8)*2)
   col*=1+(.19*grain+.15*(broad-.5))[:,:,None];relief=.5+.07*grain+.07*(fine-.5)
   check=np.exp(-((u-(.44+.006*np.sin(v*30)))/.003)**2)*np.clip((v-.15)*4,0,1);col*=1-.50*check[:,:,None];rough[:]=.93
  elif key=='coping':
   # UV V follows the cast section: abrasion is confined to the outer nose
   # and the submerged inner face, never scattered across the crown.
   fragment=np.clip((mid-.39)*5,0,1)
   edge=np.exp(-((v-.10)/.047)**2)
   waterline=np.exp(-((v-.88)/.07)**2)
   chip=np.clip(edge*fragment*.85+waterline*fragment*.48,0,1)
   col=col*(1-chip[:,:,None])+np.array((.22,.235,.18))*chip[:,:,None]
   col*=1+.035*(mid-.5)[:,:,None]
   relief=.5-.012*chip+.002*(fine-.5);rough[:]=.92
  elif key in ('red','ivory','white','navy','concrete','brick','stonepaint'):
   col*=1+.10*(mid-.5)[:,:,None]+.045*(fine-.5)[:,:,None]
   if key in ('concrete','brick','stonepaint'):
    mortar=(np.abs((v*7)%1-.5)>.46)|((np.abs((u*4+(np.floor(v*7)%2)*.5)%1-.5)>.475))
    col[mortar]*=.58;relief[mortar]-=.12
    if key=='brick':
     relief+=.055*(fine-.5)+.035*(mid-.5);pits=fine<.035
     relief[pits]-=.055;col[pits]*=.72;rough[:]=.91
   else:
    rough[:]=.84
    # Exposed lower paint layer in irregular abrasion fragments at panel edges.
    edge=np.minimum.reduce((u,1-u,v,1-v));chip=(edge<(.13 if key=='white' else .06))&(mid+fine*.20<(.54 if key=='white' else .43))
    col[chip]=np.array((.12,.155,.11) if key=='white' else (.23,.19,.115));relief[chip]-=.012;rough[chip]=.95
    relief+=.004*(fine-.5)
  elif key.startswith('cloth'):
   col*=1+.065*(mid-.5)[:,:,None]+.025*(fine-.5)[:,:,None]
   relief=.5+.012*np.sin(u*math_tau*120)*np.sin(v*math_tau*500)+.004*(fine-.5);rough[:]=.84
  elif key=='metal':
   rough[:]=.34;metal[:]=.88;relief+=.008*np.sin(u*1450);col*=1+.035*(fine-.5)[:,:,None]
  elif key=='rubber':
   # Molded ribbed tee mat, dusty and abraded on its middle.
   tread=(np.sin(u*math_tau*44)>.25).astype(float)
   wear=np.exp(-((u-.5)/.30)**4-((v-.5)/.37)**4)
   col[:]=(.025,.031,.025);col+=wear[:,:,None]*np.array((.030,.034,.023))
   col*=.90+.20*mid[:,:,None];relief=.5+.025*tread*(1-.6*wear);rough[:]=.94
  elif key=='liner':
   col*=.93+.13*mid[:,:,None];rough[:]=.82
   relief=.5+.005*(fine-.5)
  elif key=='glass':
   rough[:]=.025;relief[:]=.5
  elif key=='water':
   relief=np.full((h,w),.5,np.float32)
   # Crossing wind wavelets break reflected lines in both directions. The
   # previous two low-frequency waves read as corrugated metal.
   for fx,fy,amplitude,phase in ((4,1,.003,.7),(2,-5,.002,2.8),(8,3,.001,1.7)):
    relief+=amplitude*np.sin(math_tau*(u*fx+v*fy)+phase)
   rough[:]=.09
  elif key=='fallwater':
   relief=.5+.009*np.sin(u*93+v*9+mid*3)+.004*np.sin(u*197+v*11);rough[:]=.08
  elif key=='foam':
   col*=.8+.2*fine[:,:,None];relief+=.03*(fine-.5);rough[:]=.42
  elif key=='soil':
   col*=1+.14*(mid-.5)[:,:,None]+.12*(fine-.5)[:,:,None];relief+=.035*(fine-.5)
   # Original pointed bark chips, in a two-metre repeat. Grain belongs to
   # the material; weathering remains tied to physical exposure elsewhere.
   for j in range(1800):
    cx,cy=rng.random(2);angle=rng.uniform(0,math_tau);co,si=np.cos(angle),np.sin(angle);length=rng.uniform(.012,.035);width=rng.uniform(.004,.009);radius=length+width
    shade=rng.uniform(.65,2.5);color=np.array(COLORS[key])*shade*np.array((1,.94,.82));z=rng.uniform(.015,.085)
    for dx in (-1,0,1):
     for dy in (-1,0,1):
      x,y=cx+dx,cy+dy;tx=pad_u+x*(1-2*pad_u);ty=pad_v+y*(1-2*pad_v)
      xa,xb=max(0,int((tx-radius*(1-2*pad_u))*w)),min(w,int((tx+radius*(1-2*pad_u))*w)+1);ya,yb=max(0,int((ty-radius*(1-2*pad_v))*h)),min(h,int((ty+radius*(1-2*pad_v))*h)+1)
      if xa>=xb or ya>=yb:continue
      uu,vv=pu[ya:yb,xa:xb]-x,pv[ya:yb,xa:xb]-y;along=uu*co+vv*si;across=-uu*si+vv*co
      mask=(abs(along)<length)&(abs(across)<width*(1-.65*abs(along)/length));grain=.94+.12*np.sin(along*1700+j)
      patch=col[ya:yb,xa:xb];patch[mask]=(color[None,:]*grain[mask,None]);relief[ya:yb,xa:xb][mask]=.50+z;rough[ya:yb,xa:xb][mask]=.94
  else:
   col*=1+.22*(mid-.5)[:,:,None]+.12*(fine-.5)[:,:,None];relief+=.07*(fine-.5)
  bc[y0:y1,x0:x1]=col;orm[y0:y1,x0:x1]=np.stack((np.clip(1-(.5-relief)*.20,.8,1),rough,metal),axis=-1);height[y0:y1,x0:x1]=relief
 write_png(out/'T_Minigolf_BaseColor.png',linear_to_srgb(np.clip(bc,0,1)))
 write_png(out/'T_Minigolf_ORM.png',orm)
 write_png(out/'T_Minigolf_Height.png',height[:,:,None],bits=16)
 (out/'fields.json').write_text(json.dumps(dict(size=n,rectangles=RECTS,seed=191,reference_pixels=False),indent=2))
math_tau=np.pi*2
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--size',type=int,default=4096);a=p.parse_args();source(a.size)
