"""Original meter-scale fields, GPU flat bake and guarded shared PBR sheets.
No photographic pixels enter generation. Strip numbers start at image bottom.
"""
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT),str(HERE)]
from kit.image_io import write_png,linear_to_srgb
SETS={'Masonry':(2048,4.8768),'MineralRoof':(1024,4.),'Finish':(2048,4.)}


def noise(h,w,cells,rng):
 rows=max(2,round(cells*h/w));a=rng.random((rows,cells)).astype('float32');a=np.pad(a,2,mode='wrap')
 sx=round(w/cells);sy=round(h/rows)
 full=np.asarray(Image.fromarray(a).resize((w+4*sx,h+4*sy),Image.Resampling.BICUBIC))
 return full[2*sy:2*sy+h,2*sx:2*sx+w]


def fields(role,n):
 rng=np.random.default_rng(89614+list(SETS).index(role));coverage=SETS[role][1]
 color=np.zeros((n,n,3),np.float32);height=np.zeros((n,n),np.float32);orm=np.ones((n,n,3),np.float32);orm[:,:,2]=0
 count=8 if role=='Finish' else 4;rows=n//count;guard=round(n*8/2048);inner=rows-2*guard
 for strip in range(count):
  yy,xx=np.mgrid[:inner,:n].astype('float32');x=xx/n*coverage;y=(inner-yy-.5)/inner*(coverage/count)
  fine=rng.random((inner,n)).astype('float32');mid=noise(inner,n,180,rng)
  h=np.zeros_like(x);ao=np.ones_like(x);rough=np.full_like(x,.8);metal=np.zeros_like(x)
  if role=='Masonry':
   cw=.2032;ch=cw/3;y=y/(coverage/count)*1.2192;row=np.floor(y/ch).astype(int)%18
   header=(row%6==5)&(strip in (0,3));unit=np.where(header,cw/2,cw);offset=np.where(header,cw/4,(row%2)*cw/2)
   wx=x+offset+.0007*np.sin(y*187);wy=y+.0005*np.sin(x*76)
   ix=np.floor(wx/unit).astype(int)%np.where(header,48,24);lx=np.mod(wx,unit);ly=np.mod(wy,ch)
   edge=np.minimum.reduce([lx,unit-lx,ly,ch-ly]);width=rng.uniform(.0032,.0050,(18,48))[row,ix]
   mask=np.clip((edge-width)/.0020,0,1);mask=mask*mask*(3-2*mask)
   tone=rng.uniform(.60,1.34,(18,48))[row,ix];flashed=rng.random((18,48))[row,ix]<.12;tone*=1-.24*flashed*np.exp(-lx/.05)
   base=((.24,.105,.06) if strip==0 else (.22,.115,.077)) if strip<2 else (.62,.62,.60) if strip==2 else (.36,.27,.17)
   brick=np.array(base)*(tone*(.90+.20*mid))[:,:,None];mortar=np.array((.18,.175,.158))*(.96+.08*mid)[:,:,None]
   if strip==2:brick=np.array(base)*(.96+.08*mid)[:,:,None];mortar=np.array(base)*.88
   c=brick*mask[:,:,None]+mortar*(1-mask[:,:,None]);h=.0045*mask+.00065*(mid-.5)*mask+.00015*(fine-.5)
   ao=.78+.22*mask;rough=.91+.055*(fine-.5)
   h-=.0008*((mid<.16)&(fine<.3)&(mask>.95))
  elif role=='MineralRoof':
   c=np.ones((*x.shape,3),np.float32)*(.92+.12*(mid-.5)+.04*(fine-.5))[:,:,None]
   h=.0004*(mid-.5)+.00010*(fine-.5);rough[:]=.83
   if strip==0:
    h+=.00017*np.sin(x*1200+mid*2)*np.sin(y*1600);pores=(fine<.018)&(mid<.44);h-=.0007*pores;c*=1-.12*pores[:,:,None]
   elif strip==1:
    course=1/3;row=np.floor(y/course);lx=np.mod(x+(row%2)*.4,.8);ly=np.mod(y,course);edge=np.minimum.reduce((lx,.8-lx,ly,course-ly));face=np.clip((edge-.002)/.003,0,1);h=.0018*face+.00007*(mid-.5);c*= (.82+.18*face)[:,:,None];ao=.86+.14*face;rough[:]=.83
   elif strip==2:
    seam=np.exp(-np.mod(x,.98)/.009);c*=((.82+.27*fine)*(1-.14*seam))[:,:,None];h=.0012*fine+.0015*seam;rough[:]=.96
   else:c*=((.91+.17*fine))[:,:,None];h+=.00018*np.sin(x*2100);rough[:]=.91
  else:
   c=np.ones((*x.shape,3),np.float32)*(.96+.055*(mid-.5))[:,:,None];h=.000028*(fine-.5);rough[:]=.54
   if strip==0:
    grain=np.sin(x*170+mid*6)*np.sin(x*410+mid*3);h+=.00016*grain;c*=1-.035*grain[:,:,None];rough[:]=.61
   elif strip==1:
    edge=np.minimum(y,.5-y);chips=(edge<.009)&(mid>.59);h+=.00007*(mid-.5)-.00016*chips;c*=1-.65*chips[:,:,None];rough[:]=.57;rough+=.21*chips
   elif strip in (2,3):h+=.000012*np.sin(x*2800);rough[:]=.38 if strip==2 else .43;metal[:]=.85
   elif strip==4:
    weave=np.sin(x*3100)*np.sin(y*3100);h=.000028*weave;rough[:]=.92;c*=((.90+.07*mid+.035*weave))[:,:,None]
    c*=np.where(np.mod(x,.48)<.24,.96,.75)[:,:,None];h+=.00022*np.exp(-np.minimum(np.mod(x,.48),.48-np.mod(x,.48))/.002)
   elif strip==5:
    edge=np.minimum(y,.5-y);loss=(edge<.012)&(mid>.55);h+=.00006*(mid-.5)-.00018*loss;c*=1-.61*loss[:,:,None];rough[:]=.58;rough+=.20*loss
   elif strip==6:
    cx=np.mod(x,.44)-.22;cy=y-.25;radius=np.sqrt((cx/.20)**2+(cy/.21)**2);theta=np.arctan2(cy,cx);relief=np.exp(-((radius-.67)/.10)**2)*(.75+.25*np.cos(theta*10));h+=.0018*relief;c*=.96+.04*relief[:,:,None]
   else:
    phase=np.mod(y,.025)/.025;groove=np.exp(-phase/.065);h=.0025*phase;c*=1-.25*groove[:,:,None];ao=1-.24*groove;rough[:]=.66
  for target,a in zip((color,height,orm),(c,h,np.stack((ao,rough,metal),2))):
   padded=np.concatenate((a[-guard:],a,a[:guard]),axis=0);start=n-(strip+1)*rows;target[start:start+rows]=padded
 return color,height,orm


def source(size=4096):
 folder=Path('build/procedural');folder.mkdir(parents=True,exist_ok=True);report={}
 for role,(ship,coverage) in SETS.items():
  c,h,orm=fields(role,size);lo=float(h.min());distance=float(h.max()-lo)
  for channel,a in {'BaseColor':linear_to_srgb(c),'ORM':orm,'Height':((h-lo)/distance)[:,:,None]}.items():write_png(folder/f'T_Downtown{role}_{channel}.png',a,bits=16 if channel=='Height' else 8)
  report[role]=dict(ship_size=ship,coverage_m=coverage,height_offset_m=lo,height_distance_m=distance,size=size);print('SOURCE',role,report[role],flush=True)
 (folder/'fields.json').write_text(json.dumps(report,indent=2))


def bake(size=4096,samples=8):
 from kit.flat_bake import bake as flat
 report=json.loads(Path('build/procedural/fields.json').read_text())
 for role,r in report.items():flat(Path('build/procedural'),Path('textures/bake'),'Downtown'+role,r['coverage_m'],size,samples,r['height_distance_m'])


def ship():
 out=Path('textures/ship');out.mkdir(parents=True,exist_ok=True)
 for role,(size,_) in SETS.items():subprocess.run([sys.executable,str(ROOT/'kit/downsample.py'),'--source','textures/bake','--out',str(out),'--asset','Downtown'+role,'--size',str(size)],check=True)
 im=Image.new('RGBA',(1024,1024),(0,0,0,255));d=ImageDraw.Draw(im);d.rectangle((0,0,1023,255),fill=(255,202,117,255))
 for j in range(9):
  x=22+j*112;d.rectangle((x,300,x+70,740),fill=(106,93,73,255))
  for k in range(4):
   y=340+k*100;d.rectangle((x,y,x+68,y+9),fill=(36,31,25,255))
   for t in range(4):d.rectangle((x+5+t*16,y-43,x+15+t*16,y-2),fill=(151+13*t,118+6*t,69+7*t,255))
 im.save(out/'T_DowntownInterior_BaseColor.png')
 from graphics import generate
 generate(Path('build/signs'))
 report={p.name:dict(bytes=p.stat().st_size,size=Image.open(p).size) for p in out.glob('*.png')};report['memory']=dict(bc_8bpp_mips_MiB=42+2/3,rgba8_mips_MiB=170+2/3)
 (out/'textures.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['source','bake','ship']);p.add_argument('--size',type=int,default=4096);p.add_argument('--samples',type=int,default=8)
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:];a=p.parse_args(args)
 {'source':lambda:source(a.size),'bake':lambda:bake(a.size,a.samples),'ship':ship}[a.stage]()
