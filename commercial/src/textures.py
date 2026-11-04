"""Original commercial manufacture fields; no image/reference inputs.

Physical heights feed the kit's Cycles flat baker at 4096. The equipment
sheet reserves four oil footprints, tire contact, gum, runoff and package
fronts alongside reusable manufactured finishes. All regions have guards.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from kit.image_io import write_png,read_png,linear_to_srgb,srgb_to_linear
from kit.fonts import find_font

SETS={'CMU':(1024,2.4384,3),'Brick':(512,1.2192,3),'EIFS':(512,1.2192,2),
      'Roof':(512,2.4384,2),'Trim':(2048,2.4384,3),'Equipment':(2048,2.0,3)}
CELLS={'White':0,'Black':1,'Metal':2,'Rubber':3,'Primary':4,'Yellow':5,'Red':6,'Blue':7,
       'Orange':8,'Gray':9,'Soil':10,'Inside':11,'Oil0':12,'Oil1':13,'Oil2':14,'Oil3':15,
       'Tire':16,'Gum':17,'Salt':18,'Grime':19,'Package0':20,'Package1':21,'Package2':22,
       'Package3':23,'Package4':24,'Package5':25,'Louver':26,'Brushed':27,'Scuff':28,'Rust':29,'Lens':30,'Light':31}
TRIM={'White':0,'Metal':1,'Trim':2,'Soffit':3,'Galvanized':4,'Primary':5,'Louver':6,'Accent':7}


def noise(n,cells,rng):
 a=rng.random((cells,cells)).astype('float32');a=np.pad(a,1,mode='wrap')
 im=Image.fromarray(a).resize((round(n*(cells+2)/cells),)*2,Image.Resampling.BICUBIC)
 off=round(n/cells);return np.asarray(im)[off:off+n,off:off+n]


def smooth(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)


def fields(role,n,coverage):
 rng=np.random.default_rng(72138+list(SETS).index(role));yy,xx=np.mgrid[:n,:n].astype('float32')
 x=(xx+.5)/n*coverage;y=(n-.5-yy)/n*coverage
 fine=rng.random((n,n),dtype='float32');mid=noise(n,95,rng)
 h=np.zeros((n,n),dtype='float32');ao=np.ones_like(h);rough=np.full_like(h,.86);metal=np.zeros_like(h);alpha=np.ones_like(h)
 if role in ('CMU','Brick'):
  cw,ch=(.4064,.2032) if role=='CMU' else (.2032,.0677333333)
  rows=round(coverage/ch);cols=round(coverage/cw)
  row=np.floor(y/ch).astype(int)%rows;u=np.mod(x+(row%2)*cw*.5,cw);v=np.mod(y,ch)
  col=np.floor((x+(row%2)*cw*.5)/cw).astype(int)%cols
  edge=np.minimum.reduce((u,cw-u,v,ch-v));joint=.0048 if role=='CMU' else .004
  face=smooth((edge-joint)/.0025)
  tones=rng.uniform(.95,1.05,(rows,cols))[row,col] if role=='CMU' else rng.uniform(.84,1.15,(rows,cols))[row,col]
  if role=='CMU':
   body=np.array((.278,.281,.270),dtype='float32');mortar=np.array((.245,.245,.230),dtype='float32')
   aggregate=noise(n,178,rng);fracture=noise(n,43,rng)
   relief=.007*(.64*fracture+.36*aggregate-.5)+.0009*(fine-.5)
   color=body*(tones*(.94+.12*aggregate))[:,:,None]
   h=.008*face+relief*face;rough=.88+.08*(fine-.5)
  else:
   kiln=np.array(((.29,.075,.034),(.35,.10,.046),(.21,.050,.022),(.30,.062,.027),(.255,.086,.046)),dtype='float32')
   unit=kiln[rng.integers(0,len(kiln),(rows,cols))][row,col]
   mortar=np.array((.27,.26,.235),dtype='float32')
   # Vertical extruder drag and per-brick firing, rather than purple shading.
   drag=.5+.5*np.sin(x*2100+mid*3)
   color=unit*(tones*(.91+.15*mid+.025*drag))[:,:,None]
   h=.008*face+face*(.0009*(mid-.5)+.00017*(drag-.5));rough=.87+.08*(fine-.5)
  color=color*face[:,:,None]+mortar*(1-face[:,:,None]);ao=.72+.28*face
 elif role=='EIFS':
  color=np.array((.40,.36,.29),dtype='float32')*(.975+.05*mid)[:,:,None]
  h=.00036*(fine-.5)+.00022*(mid-.5);rough[:]=.88
 elif role=='Roof':
  # Welded membrane laps; the large scale ponding is placed on the building.
  lap=np.minimum(np.mod(x,1.2192),1.2192-np.mod(x,1.2192));seam=np.exp(-(lap/.014)**2)
  color=np.array((.17,.178,.178),dtype='float32')*(.94+.10*mid-.11*seam)[:,:,None]
  h=.0009*(mid-.5)+.0012*seam;rough[:]=.93
 elif role=='Trim':
  strip=np.minimum(7,(y/coverage*8).astype(int));v=np.mod(y/coverage*8,1)
  palette=np.array(((.69,.69,.66),(.47,.49,.50),(.027,.034,.038),(.70,.70,.67),(.39,.41,.41),(.86,.86,.83),(.37,.39,.40),(.85,.85,.83)),dtype='float32')
  color=palette[strip]*(.986+.028*(fine-.5))[:,:,None]
  brush=.5+.5*np.sin(y*12500+mid*1.8);h=.000020*(fine-.5)
  rough=np.choose(strip,(.54,.27,.38,.62,.48,.48,.43,.48)).astype('float32')
  metal=np.choose(strip,(0,.95,.65,0,.88,0,.85,0)).astype('float32')
  rough+=np.where((strip==1)|(strip==4),.08*(brush-.5),.018*(fine-.5))
  corr=(strip==3);rib=np.exp(-(np.minimum(np.mod(x,.2032),.2032-np.mod(x,.2032))/.004)**2)
  h+=corr*.0007*rib
  louver=(strip==6);phase=np.mod(v*12,1);h+=louver*.002*phase
  ao-=louver*.24*np.exp(-phase/.09);color*=1-(louver*.20*np.exp(-phase/.09))[:,:,None]
 else:
  color=np.zeros((n,n,3),dtype='float32');stepx=n//4;stepy=n//8
  palette=[(.69,.69,.66),(.0055,.0065,.0075),(.46,.49,.50),(.012,.014,.014),(.86,.86,.83),(.68,.40,.020),(.43,.014,.010),(.012,.075,.32),(.66,.12,.010),(.23,.25,.25),(.075,.043,.020),(.021,.023,.023)]
  for index in range(32):
   # Cell IDs are bottom-up glTF UV coordinates.
   row,col=divmod(index,4);sl=(slice(n-(row+1)*stepy,n-row*stepy),slice(col*stepx,(col+1)*stepx))
   sh=(stepy,stepx);gy,gx=np.mgrid[:stepy,:stepx].astype('float32');u=(gx+.5)/stepx;v=1-(gy+.5)/stepy
   f=fine[sl];m=mid[sl];a=np.ones(sh,dtype='float32');hh=np.zeros(sh,dtype='float32');rr=np.full(sh,.65,dtype='float32');mm=np.zeros(sh,dtype='float32')
   cc=np.broadcast_to(np.array(palette[index] if index<12 else (.022,.020,.018),dtype='float32'),(*sh,3)).copy()
   if index<12:
    cc*=1+.026*(f-.5)[:,:,None];hh=.000035*(f-.5)
    if index==1:hh=.00015*(f-.5)+.00008*(m-.5);rr=.78+.09*(f-.5)
    if index==2:rr=.25+.11*(f-.5);mm[:]=.95;hh=.000008*np.sin(v*1900+m*4)
    elif index==3:rr[:]=.81;hh=.00012*(f-.5)
    elif index==10:
     # Jittered, independently oriented angular bark chips. Their fibers
     # follow each chip instead of a single flowing wood-grain field.
     bark=np.random.default_rng(102940);count=14;sites=bark.uniform(.1,.9,(count,count,2));angles=bark.uniform(0,2*np.pi,(count,count));tones=bark.uniform(.48,1.40,(count,count));heights=bark.uniform(.001,.004,(count,count))
     gx=u*count;gy=v*count;ix=np.floor(gx).astype(int);iy=np.floor(gy).astype(int)
     best=np.full(sh,np.inf);second=best.copy();idsx=ix.copy();idsy=iy.copy();along=np.zeros(sh)
     for oy in (-1,0,1):
      for ox in (-1,0,1):
       cx0=ix+ox;cy0=iy+oy;cx1=cx0%count;cy1=cy0%count
       dx=gx-(cx0+sites[cy1,cx1,0]);dy=gy-(cy0+sites[cy1,cx1,1]);ang=angles[cy1,cx1]
       axial=dx*np.cos(ang)+dy*np.sin(ang);cross=-dx*np.sin(ang)+dy*np.cos(ang);distance=(axial/1.7)**2+(cross/.65)**2
       keep=distance<best;second=np.where(keep,best,np.minimum(second,distance));best=np.minimum(best,distance)
       idsx=np.where(keep,cx1,idsx);idsy=np.where(keep,cy1,idsy);along=np.where(keep,axial,along)
     face=smooth((second-best)/.10);tone=tones[idsy,idsx];fiber=.5+.5*np.sin(along*78+m*3)
     cc=np.array((.085,.041,.015))*(tone*(.78+.22*face+.08*fiber))[:,:,None]
     cc*=.65+.35*face[:,:,None];hh=heights[idsy,idsx]*face+.0003*fiber;rr[:]=.96
   elif 12<=index<=15:
    # Accumulated engine drips: overlapping irregular small rivulets and
    # splashes around a vehicle center, never a single circular stain.
    rng2=np.random.default_rng(400+index)
    def local(c):
     seed=rng2.random((c,c)).astype('float32')
     return np.asarray(Image.fromarray(seed).resize((stepx,stepy),Image.Resampling.BICUBIC))
    broad=local(11);grain=local(43);envelope=np.exp(-(((u-.5)/.24)**2+((v-.5)/.30)**2)*1.7)
    # Accumulated seepage coalesces into an irregular granular core with
    # sparse satellite drops. It has no large elliptical component.
    a=(.52*smooth((broad+.30*envelope-.61)/.16)+.12*grain)*envelope
    a*=.45+.55*smooth((grain-.26)/.45)
    for k in range(14):
     px,py=rng2.normal(.5,.19),rng2.normal(.5,.21);r0=rng2.uniform(.006,.015)
     dist=((u-px)/r0)**2+((v-py)/(r0*.75))**2
     a=np.maximum(a,smooth((1-dist+(grain-.5)*.6)/.18)*rng2.uniform(.22,.48))
    a*=smooth(np.minimum.reduce((u,1-u,v,1-v))/.07);rr[:]=.58
   elif index==16:
    # Parallel worn tread contacts. The path itself is swept on the lot.
    edge=smooth((.46-abs(u-.5))/.12);gaps=.55+.45*smooth((f-.25)/.50)
    tread=.72+.28*(np.sin(v*190+u*9)>-.2);a=edge*gaps*tread*.28;rr[:]=.86
   elif index==17:
    dist=((u-.5)/.33)**2+((v-.5)/.30)**2;a=smooth((1-dist+(m-.5)*.4)/.16)
    cc[:]=(.062,.060,.054);rr[:]=.93;hh=.0007*a
   elif index in (18,19):
    # Narrow vertical deposits with long tapered tails; geometry puts their
    # heads at a coping seam, drain, fascia joint or dispenser base.
    width=.018+.13*v*v;dist=abs(u-.5+.028*np.sin(v*18))
    a=.32*smooth((width-dist+(m-.5)*.035)/.045)*smooth(v/.12)*smooth((1-v)/.10)*(.55+.40*m)
    cc[:]=(.55,.54,.50) if index==18 else (.033,.029,.024);rr[:]=.93
   elif 20<=index<=25:
    pal=np.array(((.18,.29,.075),(.62,.26,.031),(.035,.18,.31),(.47,.035,.021),(.30,.22,.12),(.20,.11,.30)))
    cc[:]=pal[index-20];cc[(v>.72)|(v<.16)]=(.73,.69,.54)
    disk=((u-.5)/.34)**2+((v-.43)/.21)**2<1;cc[disk]=(.58,.43,.16)
    stripe=(abs(v-.61)<.028)|((v<.12)&(np.mod(u*14,1)<.35));cc[stripe]=(.035,.032,.026)
    rr[:]=.45
   elif index==26:
    phase=np.mod(v*15,1);cc[:]=(.21,.23,.24);cc*=1-(.7*np.exp(-phase/.10))[:,:,None];hh=.0015*phase;mm[:]=.8
   elif index==27:cc[:]=(.40,.43,.44);rr=.3+.08*np.sin(v*4000+m);mm[:]=.95
   elif index==28:
    strokes=(abs(v-.55+.12*np.sin(u*3))<.045)&(u>.12)&(u<.85);a=strokes*(.5+.5*f);cc[:]=(.15,.16,.16);mm[:]=.8;rr[:]=.58
   elif index==29:
    a=smooth((.39-abs(u-.5))/.08)*smooth((.48-abs(v-.5))/.08)*smooth((m-.35)/.3);cc[:]=(.16,.055,.016);rr[:]=.91
   elif index==30:cc[:]=(.56,.62,.64);rr[:]=.18;hh=.00015*np.sin(u*950)
   else:cc[:]=(.75,.75,.71);rr[:]=.56
   # 8 delivered pixels of constant edge dilation at 2K.
   g=max(2,round(n/2048*8))
   def guard(q):
    return np.pad(q[g:-g,g:-g],((g,g),(g,g))+(((0,0),) if q.ndim==3 else ()),mode='edge')
   color[sl]=guard(cc);h[sl]=guard(hh);rough[sl]=guard(rr);metal[sl]=guard(mm);alpha[sl]=guard(a)
 return color,h,ao,rough,metal,alpha


def source(size=4096,roles=None):
 folder=Path('build/procedural');folder.mkdir(parents=True,exist_ok=True);report=json.loads((folder/'fields.json').read_text()) if (folder/'fields.json').exists() else {}
 for role,(ship,coverage,count) in SETS.items():
  if roles and role not in roles:continue
  color,h,ao,rough,metal,alpha=fields(role,size,coverage);lo=float(h.min());distance=max(.00001,float(h.max())-lo)
  for channel,a in dict(BaseColor=linear_to_srgb(color),ORM=np.stack((ao,rough,metal),2),Height=((h-lo)/distance)[:,:,None]).items():
   write_png(folder/f'T_Commercial{role}_{channel}.png',a,bits=16 if channel=='Height' else 8)
  if role=='Equipment':write_png(folder/'EquipmentAlpha.png',alpha[:,:,None])
  report[role]=dict(ship_size=ship,size=size,coverage_m=coverage,height_distance_m=distance,channels=count)
  print('FIELDS',role,flush=True)
 (folder/'fields.json').write_text(json.dumps(report,indent=2))


def bake(size=4096,samples=4,roles=None):
 from kit.flat_bake import bake as flat
 rows=json.loads(Path('build/procedural/fields.json').read_text())
 for role,row in rows.items():
  if not roles or role in roles:flat(Path('build/procedural'),Path('textures/bake'),'Commercial'+role,row['coverage_m'],size,samples,row['height_distance_m'])


def ship():
 import subprocess
 folder=Path('textures/ship');folder.mkdir(parents=True,exist_ok=True)
 for role,(size,cov,count) in SETS.items():
  subprocess.run([sys.executable,str(HERE.parents[1]/'kit/downsample.py'),'--source','textures/bake','--out',str(folder),'--asset','Commercial'+role,'--size',str(size)],check=True)
  if count==2:(folder/f'T_Commercial{role}_ORM.png').unlink()
  if role=='Equipment':
   color=read_png(folder/'T_CommercialEquipment_BaseColor.png');alpha=read_png('build/procedural/EquipmentAlpha.png')
   factor=alpha.shape[0]//size;alpha=alpha.reshape(size,factor,size,factor,1).mean(axis=(1,3))
   write_png(folder/'T_CommercialEquipment_BaseColor.png',np.concatenate((color[:,:,:3],alpha),2))
 graphics(folder)
 report=dict(new_images=17,new_gpu_mib=39+2/3,sets=SETS,graphics_size=1024,source_size=4096)
 (folder/'sets.json').write_text(json.dumps(report,indent=2))


def graphics(folder):
 """Both brands and shared strings in fixed guarded cells, chosen through UVs."""
 strings=['RILLWAY','LATCHLINE','FRESH\nCOFFEE','DAILY\nGOODS','FOOD  •  COFFEE  •  EVERYDAY',
 '$\nGAL','25.02','7.234','PAY AT PUMP','INSERT CARD','87','89','93','3.459','3.759','4.059','1','2','3','4',
 'NO SMOKING\nSTOP ENGINE','CAIRN  M3','CLEARANCE 14 ft 6 in','REGULAR','PLUS','PREMIUM','CASH / CREDIT  •  PER GALLON',
 'ICE','PROPANE\nFLAMMABLE','CYLINDER EXCHANGE','AIR / WATER','RESERVED','VAN ACCESSIBLE','084216','kWh']
 image=Image.new('RGBA',(4096,4096),(255,255,255,0));d=ImageDraw.Draw(image);rects={};x=8;y=8;rh=0
 fontpath=find_font('DejaVu Sans','Bold')
 for s in strings+['@rillway','@latchline']:
  brand=s in ('RILLWAY','LATCHLINE');mark=s.startswith('@');fs=66 if brand else 32
  font=ImageFont.truetype(str(fontpath if brand else find_font('DejaVu Sans','Book')),fs);bb=d.multiline_textbbox((0,0),s,font=font,spacing=3,align='center')
  w,h=(128,128) if mark else ((464,90) if brand else (bb[2]-bb[0]+12,bb[3]-bb[1]+12))
  if x+w+8>1024:x=8;y+=rh+12;rh=0
  if y+h+8>1024:raise RuntimeError('Graphics sheet full')
  linear=(.72,.68,.58) if s=='RILLWAY' else (.68,.71,.70) if s=='LATCHLINE' else (.59,.255,.105) if s=='@rillway' else (.27,.31,.57) if s=='@latchline' else (.009,.012,.014) if s in ('87','89','93') else (.015,.095,.42) if s=='ICE' else (.52,.018,.015) if s in ('NO SMOKING\nSTOP ENGINE','PROPANE\nFLAMMABLE') else (.035,.043,.047) if s=='FOOD  •  COFFEE  •  EVERYDAY' else (.67,.67,.64)
  ink=tuple(int(round(v*255)) for v in linear_to_srgb(np.array(linear)))+(255,)
  def rectangle(box):d.rectangle(tuple(round(v*4) for v in box),fill=ink)
  if mark:
   if s=='@rillway':
    for i,f in enumerate((.68,1,.81)):rectangle((x+21+i*32,y+110-90*f,x+37+i*32,y+110))
   else:
    for sign in (-1,1):
     cx=x+64+sign*29;cy=y+64-sign*15
     rectangle((cx-7,cy-40,cx+7,cy+40))
     for t in (-1,1):rectangle((cx-7-(18 if sign>0 else 0),cy+t*34-6,cx+7+(18 if sign<0 else 0),cy+t*34+6))
  else:
   actual_font=ImageFont.truetype(font.path,fs*4)
   d.multiline_text(((x+(w-(bb[2]-bb[0]))/2-bb[0])*4,(y+(h-(bb[3]-bb[1]))/2-bb[1])*4),s,font=actual_font,spacing=12,align='center',fill=ink)
  rects[s]=dict(rect=(x/1024,1-(y+h)/1024,(x+w)/1024,1-y/1024),aspect=w/h,font_size=fs,pixel_height=h)
  x+=w+12;rh=max(rh,h)
 source=Path('build/procedural/T_CommercialGraphics_BaseColor.png');image.save(source)
 a=np.asarray(image,dtype='float32')/255;alpha=a[:,:,3:4];weighted=srgb_to_linear(a[:,:,:3])*alpha
 out_alpha=alpha.reshape(1024,4,1024,4,1).mean(axis=(1,3));weighted=weighted.reshape(1024,4,1024,4,3).mean(axis=(1,3))
 rgb=np.where(out_alpha>0,weighted/np.maximum(out_alpha,1e-8),1)
 write_png(folder/'T_CommercialGraphics_BaseColor.png',np.concatenate((linear_to_srgb(rgb),out_alpha),2));(folder/'graphics.json').write_text(json.dumps(rects,indent=2))


if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('stage',choices=('source','bake','ship'));a.add_argument('--size',type=int,default=4096);a.add_argument('--samples',type=int,default=4);a.add_argument('--roles')
 a=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 roles=a.roles.split(',') if a.roles else None
 source(a.size,roles) if a.stage=='source' else bake(a.size,a.samples,roles) if a.stage=='bake' else ship()
