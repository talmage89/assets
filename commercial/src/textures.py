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
      'Roof':(512,2.4384,2),'Concrete':(1024,1.524,3),'Equipment':(2048,2.0,3)}
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
 elif role=='Concrete':
  # Fine cement/sand and a dragged broom finish at measured millimeter scale.
  # No dark joint is painted into this tile; joints follow actual slab geometry.
  aggregate=noise(n,480,rng);sand=noise(n,1100,rng)
  bristle=rng.uniform(-1,1,1600).astype('float32')
  track=(y/coverage*1600+1.4*np.sin(x*5.2)).astype(int)%1600
  broom=bristle[track];pores=np.maximum(0,(.14-aggregate)*3)
  tone=.39+.022*(aggregate-.5)+.012*(sand-.5)-.025*pores
  color=np.stack((tone*1.015,tone*1.004,tone*.977),2)
  h=.00014*broom+.00012*(aggregate-.5)-.00035*pores
  rough=.82+.08*pores+.035*(sand-.5)
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
  palette=[(.69,.69,.66),(.036,.033,.035),(.46,.49,.50),(.012,.014,.014),(.86,.86,.83),(.68,.40,.020),(.43,.014,.010),(.012,.075,.32),(.66,.12,.010),(.23,.25,.25),(.075,.043,.020),(.021,.023,.023)]
  for index in range(32):
   # Cell IDs are bottom-up glTF UV coordinates.
   row,col=divmod(index,4);sl=(slice(n-(row+1)*stepy,n-row*stepy),slice(col*stepx,(col+1)*stepx))
   sh=(stepy,stepx);gy,gx=np.mgrid[:stepy,:stepx].astype('float32');u=(gx+.5)/stepx;v=1-(gy+.5)/stepy
   f=fine[sl];m=mid[sl];a=np.ones(sh,dtype='float32');hh=np.zeros(sh,dtype='float32');rr=np.full(sh,.65,dtype='float32');mm=np.zeros(sh,dtype='float32')
   cc=np.broadcast_to(np.array(palette[index] if index<12 else (.022,.020,.018),dtype='float32'),(*sh,3)).copy()
   if index<12:
    cc*=1+.026*(f-.5)[:,:,None];hh=.000035*(f-.5)
    if index==1:hh=.00015*(f-.5)+.00008*(m-.5);rr=.78+.09*(f-.5)
    if index==2:rr=.34+.06*(f-.5);mm[:]=.95;hh=.000012*(f-.5)
    elif index==3:rr[:]=.81;hh=.00012*(f-.5)
    elif index==10:
     # Shredded bark: overlapping tapered fibers, no Voronoi/paver cells.
     bark=np.random.default_rng(102940);cc[:]=(.019,.010,.004);hh[:]=0;rr[:]=.97
     for j in range(1400):
      cx,cy=bark.uniform(-.04,1.04,2);length=bark.uniform(.022,.095);width=bark.uniform(.005,.018);ang=bark.uniform(0,2*np.pi)
      radius=length*.65;ax=max(0,int((cx-radius)*stepx));bx=min(stepx,int((cx+radius)*stepx)+1);ay=max(0,int((1-cy-radius)*stepy));by=min(stepy,int((1-cy+radius)*stepy)+1)
      if ax>=bx or ay>=by:continue
      du=u[ay:by,ax:bx]-cx;dv=v[ay:by,ax:bx]-cy
      along=du*np.cos(ang)+dv*np.sin(ang);cross=-du*np.sin(ang)+dv*np.cos(ang)
      taper=np.maximum(0,1-abs(along)/(length/2));inside=(abs(along)<length/2)&(abs(cross)<width/2*(.3+.7*taper))
      fibers=.8+.2*np.sin(cross/width*27+along*700);tone=bark.uniform(.55,1.35)
      rgb=np.array((.055,.028,.011))*tone*fibers[:,:,None]
      cc[ay:by,ax:bx]=np.where(inside[:,:,None],rgb,cc[ay:by,ax:bx])
      ridge=bark.uniform(.001,.005)*(1-np.minimum(1,abs(cross)/(width/2)))
      hh[ay:by,ax:bx]=np.where(inside,ridge,hh[ay:by,ax:bx])
   elif 12<=index<=15:
    # Many absorbed droplets and small leaks combine into a standing band.
    rng2=np.random.default_rng(400+index);acc=np.zeros(sh,dtype='float32')
    bend=.04*np.sin(v*11+index);band=np.exp(-((u-.5-bend)/.27)**4)*np.exp(-((v-.5)/.44)**6)
    for k in range(240):
     # Engine and fuel-door concentrations, with much quieter incidental drops.
     px,py=(rng2.normal(.48,.14),rng2.normal(.64,.15)) if k<175 else (rng2.normal(.67,.11),rng2.normal(.29,.14))
     rx=rng2.uniform(.004,.035);ry=rx*rng2.uniform(.6,1.9)
     drop=np.exp(-(((u-px)/rx)**2+((v-py)/ry)**2)*1.5)*rng2.uniform(.12,.44)
     acc+=drop
    a=(.24*band+.70*(1-np.exp(-acc)))*smooth(np.minimum.reduce((u,1-u,v,1-v))/.09)
    a*=.84+.16*m;cc[:]=(.145,.119,.084);rr[:]=.74
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
    a=(.32 if index==18 else .40)*smooth((width-dist+(m-.5)*.035)/.045)*smooth(v/.12)*smooth((1-v)/.10)*(.55+.40*m)
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
   elif index==30:cc[:]=(.74,.75,.73);rr[:]=.61;hh=.000025*(f-.5)
   else:cc[:]=(.75,.75,.71);rr[:]=.56
   # 8 delivered pixels of constant edge dilation at 2K.
   g=max(2,round(n/2048*8))
   def guard(q):
    return np.pad(q[g:-g,g:-g],((g,g),(g,g))+(((0,0),) if q.ndim==3 else ()),mode='edge')
   color[sl]=guard(cc);h[sl]=guard(hh);rough[sl]=guard(rr);metal[sl]=guard(mm);alpha[sl]=guard(a)
 return color,h,ao,rough,metal,alpha


def source(size=4096,roles=None):
 folder=Path('build/procedural');folder.mkdir(parents=True,exist_ok=True);report={k:v for k,v in json.loads((folder/'fields.json').read_text()).items() if k in SETS} if (folder/'fields.json').exists() else {}
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
 for p in folder.glob('T_CommercialTrim_*.png'):p.unlink()
 report=dict(new_images=18,new_gpu_mib=29,sets=SETS,graphics_size=1024,source_size=4096)
 (folder/'sets.json').write_text(json.dumps(report,indent=2))


def service_deposit(name,width=1024,height=432):
 """Analytic service deposits, sampled directly into the existing ink sheet.

 These are coverage/color fields, not manufactured relief: they need no
 Cycles rebake. Keep every other finish and powered pixel byte-identical.
 """
 yy,xx=np.mgrid[:height,:width].astype('float32');u=(xx+.5)/width;v=1-(yy+.5)/height
 rng=np.random.default_rng(8912+CELLS[name]);alpha=np.zeros_like(u)
 if name.startswith('Oil'):
  # Dispersed drip clusters from many cars; larger old absorption halos
  # remain legible after projection to a few dozen hero pixels.
  band=np.exp(-((u-.5-.035*np.sin(v*15))/.31)**4-((v-.5)/.46)**6)
  acc=np.zeros_like(u)
  for i in range(620):
   px,py=(rng.normal(.48,.21),rng.normal(.64,.18)) if i<450 else (rng.normal(.66,.18),rng.normal(.28,.18))
   radius=rng.uniform(.006,.028) if i<520 else rng.uniform(.026,.060)
   # Correct for the footprint's physical aspect, rather than stretching
   # circular oil drops into long streaks in the vehicle direction.
   rx=radius;ry=radius*(3.0/9.0)*rng.uniform(.7,1.5)
   acc+=np.exp(-(((u-px)/rx)**2+((v-py)/ry)**2)*1.7)*rng.uniform(.18,.70)
  alpha=(.05*band+.56*(1-np.exp(-acc)))*smooth(np.minimum.reduce((u,1-u,v,1-v))/.16)
  color=(.050,.046,.038)
 elif name=='Tire':
  edge=smooth((.48-abs(u-.5))/.14)
  tread=.70+.30*(np.sin(v*185+u*12)>-.2)
  alpha=edge*tread*(.24+.06*np.sin(v*11)**2);color=(.008,.008,.007)
  alpha*=smooth(v/.20)*smooth((1-v)/.20)
 else:
  # Gravity tails below seam heads: unequal side rivulets and no rectangle.
  center=.50+.035*np.sin(v*15);width=.025+.19*v*v
  alpha=.51*smooth((width-abs(u-center))/.045)*smooth(v/.08)*smooth((1-v)/.06)
  alpha+=.15*np.exp(-((u-.68)/.035)**2)*smooth(v/.35)*smooth((1-v)/.13)
  color=(.033,.029,.024)
 rgb=np.broadcast_to(linear_to_srgb(np.array(color)),(*u.shape,3))
 return Image.fromarray(np.uint8(np.clip(np.dstack((rgb,alpha)),0,1)*255+.5),'RGBA')


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
 # The lower 384px hold broad wear at its appropriate texel density.
 eq=Image.open(folder/'T_CommercialEquipment_BaseColor.png').convert('RGBA')
 wear=('Oil0','Oil1','Oil2','Oil3','Tire','Gum','Salt','Grime','Scuff','Rust')
 for i,name in enumerate(wear):
  cell=CELLS[name];row,col=divmod(cell,4);piece=eq.crop((col*512,(7-row)*256,(col+1)*512,(8-row)*256))
  x,y=(i%4)*256,640+(i//4)*108;w,h=256,108
  piece=service_deposit(name,w*4,h*4) if name.startswith('Oil') or name in ('Tire','Grime') else piece.resize((w*4,h*4),Image.Resampling.BICUBIC)
  image.paste(piece,(x*4,y*4))
  rects['Wear:'+name]=dict(rect=((x+4)/1024,1-(y+h-4)/1024,(x+w-4)/1024,1-(y+4)/1024),aspect=w/h,font_size=0,pixel_height=h)
 for i,name in enumerate(('CanopyLamp','InteriorLamp','WallPackLamp','LotLamp','PriceLED','Blank','BrandRillway','BrandLatchline')):
  x,y=i*40,980;ink=(225,227,223,255) if name!='PriceLED' else (255,166,48,255)
  if name.startswith('Brand'):
   from plan import BRANDS
   rgb=BRANDS['rillway' if name=='BrandRillway' else 'latchline']['primary'];ink=tuple(round(q*255) for q in linear_to_srgb(np.array(rgb)))+(255,)
  d.rectangle((x*4,y*4,(x+32)*4,(y+32)*4),fill=ink)
  rects[name]=dict(rect=((x+3)/1024,1-(y+29)/1024,(x+29)/1024,1-(y+3)/1024),aspect=1,font_size=0,pixel_height=32)
 source=Path('build/procedural/T_CommercialGraphics_BaseColor.png');image.save(source)
 a=np.asarray(image,dtype='float32')/255;alpha=a[:,:,3:4];weighted=srgb_to_linear(a[:,:,:3])*alpha
 out_alpha=alpha.reshape(1024,4,1024,4,1).mean(axis=(1,3));weighted=weighted.reshape(1024,4,1024,4,3).mean(axis=(1,3))
 rgb=np.where(out_alpha>0,weighted/np.maximum(out_alpha,1e-8),1)
 write_png(folder/'T_CommercialGraphics_BaseColor.png',np.concatenate((linear_to_srgb(rgb),out_alpha),2));(folder/'graphics.json').write_text(json.dumps(rects,indent=2))
 emission=np.zeros((1024,1024,3),dtype='float32')
 for name,strength in [(x,1.7) for x in ('RILLWAY','LATCHLINE','@rillway','@latchline')]+[('CanopyLamp',40),('InteriorLamp',16),('WallPackLamp',15),('LotLamp',55),('PriceLED',3),('BrandRillway',.40),('BrandLatchline',.40)]:
  r=rects[name]['rect'];x0,x1=round(r[0]*1024)-2,round(r[2]*1024)+2;y0,y1=round((1-r[3])*1024)-2,round((1-r[1])*1024)+2
  emission[y0:y1,x0:x1]=rgb[y0:y1,x0:x1]*strength/300
 write_png(folder/'T_CommercialGraphics_Emission.png',linear_to_srgb(emission),bits=16)



if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('stage',choices=('source','bake','ship'));a.add_argument('--size',type=int,default=4096);a.add_argument('--samples',type=int,default=4);a.add_argument('--roles')
 a=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 roles=a.roles.split(',') if a.roles else None
 source(a.size,roles) if a.stage=='source' else bake(a.size,a.samples,roles) if a.stage=='bake' else ship()
