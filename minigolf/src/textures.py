"""Original carpet loops, painted masonry, strata and metal. Never reads refs.

One 4K source field is Cycles baked, then filtered to the accepted 2K course
atlas. UV rectangles have 8 delivered texels of protective inset. Large-scale
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
 'wood':(.20,.18,.135),'rock':(.22,.18,.12),'rocklight':(.36,.285,.19),
 'red':(.32,.024,.016),'ivory':(.58,.55,.43),'navy':(.012,.042,.065),'white':(.62,.65,.59),
 'black':(.009,.013,.012),'metal':(.35,.37,.35),'rubber':(.009,.012,.011),
 'soil':(.040,.025,.012),'grass':(.065,.115,.027),'asphalt':(.035,.038,.038),
 'yellow':(.60,.32,.016),'leaf':(.18,.095,.018),'liner':(.014,.019,.012),
 'water':(.014,.075,.058),'glass':(.055,.085,.085),'foam':(.48,.55,.48),'stonepaint':(.40,.41,.36)}
RECTS={name:(i*.25,0,(i+1)*.25,.5) for i,name in enumerate(list(COLORS)[:3])}
slots=[(i/8,j/8,(i+1)/8,(j+1)/8) for j in range(4,8) for i in range(8)]
RECTS.update(zip(list(COLORS)[3:],slots))

def noise(h,w,cells,rng):
 return np.asarray(Image.fromarray(rng.random((cells,cells),dtype=np.float32)).resize((w,h),Image.Resampling.BICUBIC))

def source(n=4096):
 out=Path('build/procedural');out.mkdir(parents=True,exist_ok=True)
 # Padding is a physical neutral paint, not black empty texels.
 bc=np.full((n,n,3),.16,np.float32);orm=np.zeros_like(bc);orm[:]=(1,.85,0);height=np.full((n,n),.5,np.float32)
 for key,(u0,v0,u1,v1) in RECTS.items():
  rng=np.random.default_rng(191+list(COLORS).index(key));x0,x1=round(u0*n),round(u1*n);y0,y1=round((1-v1)*n),round((1-v0)*n);w=x1-x0;h=y1-y0
  yy,xx=np.mgrid[:h,:w].astype(np.float32);u=(xx+.5)/w;v=(yy+.5)/h
  fine=rng.random((h,w),dtype=np.float32);mid=noise(h,w,38,rng);broad=noise(h,w,6,rng)
  col=np.zeros((h,w,3),np.float32);col[:]=COLORS[key];rough=np.full((h,w),.86,np.float32);relief=np.full((h,w),.5,np.float32);metal=np.zeros((h,w),np.float32)
  if key.startswith('carpet'):
   # Rows of interlaced polypropylene loops. The roll is 3.66 x 9m here;
   # tuft pitch 5.2mm, sampled at 4K before normal/filtering.
   loops=(np.sin(u*math_tau*344+.35*np.sin(v*math_tau*130))*np.sin(v*math_tau*860))*.5+.5
   traffic=np.clip(np.exp(-((u-.5)/.095)**2)*np.sin(np.pi*v)**.5+np.exp(-((u-.5)/.10)**2-((v-.88)/.035)**2),0,1)
   relief=.35+(.23*loops+.15*(fine-.5))*(1-.65*traffic)
   col*=1+.14*(mid-.5)[:,:,None]+.16*(fine-.5)[:,:,None]
   rough[:]=.94-.09*traffic
   # Glue line, lengthwise roll join, and a rectangular repaired patch.
   seam=np.exp(-((u-.68)/.0025)**2);col*=1-.22*seam[:,:,None];relief-=.05*seam
   patch=(u>.19)&(u<.39)&(v>.18)&(v<.255);col[patch]*=(.79,.88,.78)
   edges=patch & ((abs(u-.19)<.003)|(abs(u-.39)<.003)|(abs(v-.18)<.002)|(abs(v-.255)<.002));col[edges]*=.64
  elif key in ('rock','rocklight'):
   strata=np.sin(v*math_tau*12+mid*.5+np.sin(u*17)*.6)
   beds=np.exp(-((strata+.95)/.13)**2)
   col*=1+(.20*(broad-.5)+.11*(mid-.5)-.22*beds)[:,:,None]
   relief=.48+.08*mid-.16*beds+.04*fine;rough[:]=.91
   crack=np.exp(-((u-(.35+.07*np.sin(v*8)+.02*np.sin(v*27)))/.006)**2)
   col*=1-.50*crack[:,:,None];relief-=.16*crack
  elif key=='wood':
   grain=np.sin(u*math_tau*48+mid*4+np.sin(v*8)*2)
   col*=1+(.19*grain+.15*(broad-.5))[:,:,None];relief=.5+.07*grain+.07*(fine-.5)
   check=np.exp(-((u-(.44+.006*np.sin(v*30)))/.003)**2)*np.clip((v-.15)*4,0,1);col*=1-.50*check[:,:,None];rough[:]=.93
  elif key in ('red','ivory','white','navy','concrete','brick','stonepaint'):
   col*=1+.10*(mid-.5)[:,:,None]+.045*(fine-.5)[:,:,None]
   if key in ('concrete','brick','stonepaint'):
    mortar=(np.abs((v*7)%1-.5)>.46)|((np.abs((u*4+(np.floor(v*7)%2)*.5)%1-.5)>.475))
    col[mortar]*=.58;relief[mortar]-=.12
   else:
    # Exposed lower paint layer in irregular abrasion fragments at panel edges.
    edge=np.minimum.reduce((u,1-u,v,1-v));chip=(edge<.06)&(mid+fine*.20<.43)
    col[chip]=np.array((.23,.19,.115));relief[chip]-=.09;rough[chip]=.95
    relief+=.02*(fine-.5)
  elif key=='metal':
   rough[:]=.34;metal[:]=.88;relief+=.008*np.sin(u*1450);col*=1+.035*(fine-.5)[:,:,None]
  elif key=='water':
   relief=.5+.008*(np.sin(u*100+np.sin(v*37))+np.sin(v*143+u*17));rough[:]=.16
  elif key=='foam':
   col*=.8+.2*fine[:,:,None];relief+=.03*(fine-.5);rough[:]=.42
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
