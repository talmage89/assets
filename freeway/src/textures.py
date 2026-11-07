"""Original manufacture fields and causal maintenance sprites; no photo inputs."""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import write_png,linear_to_srgb,srgb_to_linear
SETS={'FreewayConcrete':dict(coverage=3.048,size=2048,height=.004),'FreewayZinc':dict(coverage=3.048,size=1024,height=.0007),'FreewaySigns':dict(coverage=1,size=2048,height=.0004),'FreewayMaintenance':dict(coverage=1,size=1024,height=.008)}
SPRITES=['crack','spall','tire','oil','runoff','salts','patch','ghost','seal','silt','rust','weed','rubber','litter','repair','blank']
def rect(name):
 i=SPRITES.index(name);x=i%4;y=i//4;g=8/1024
 return (x/4+g,1-(y+1)/4+g,(x+1)/4-g,1-y/4-g)
def manufacture(name,size):
 rng=np.random.default_rng(741 if name=='FreewayConcrete' else 983);grain=rng.normal(0,1,(size,size)).astype(np.float32)
 def field(n):return np.asarray(Image.fromarray(rng.random((n,n),dtype=np.float32)).resize((size,size),Image.Resampling.BICUBIC),np.float32)-.5
 if name=='FreewayConcrete':
  sand=field(size//8);pores=np.minimum(0,grain+2);v=.008*grain+.018*sand+.006*field(32)
  rgb=np.stack([.28+v,.269+v,.243+v],axis=2);height=np.clip(.55+.08*grain+.13*sand+pores*.25,0,1)
  orm=np.dstack([np.clip(1+pores*.08,0,1),np.clip(.87+.025*grain,0,1),np.zeros_like(grain)])
 else:
  crystals=field(180);white=np.maximum(0,field(95)-.19)*1.4;v=.39+.11*crystals+.007*grain
  rgb=np.stack([v+white*.25,v+.012+white*.26,v+.015+white*.25],axis=2);height=np.clip(.5+crystals*.11+grain*.02+white*.06,0,1)
  orm=np.dstack([np.ones_like(grain),np.clip(.53+white*.9+crystals*.1,0,1),np.clip(.95-white*1.9,0,1)])
 return np.clip(rgb,0,1),orm,height

def maintenance(size):
 rng=np.random.default_rng(431);im=Image.new('RGBA',(size,size),(80,77,66,0));w=size//4;g=round(w*.05)
 for i,name in enumerate(SPRITES):
  tile=Image.new('RGBA',(w,w),(80,77,66,0));d=ImageDraw.Draw(tile)
  if name in ('crack','seal'):
   for branch in range(1 if name=='seal' else 3):
    pts=[(int(w*(.5+branch*.07)+rng.normal(0,w*.018)),j) for j in range(g,w-g,max(1,w//40))]
    d.line(pts,fill=(42,39,32,245),width=max(2,w//95 if name=='crack' else w//30))
    if name=='crack':
     for k in (10,25):
      a=pts[min(k,len(pts)-1)];d.line([a,(a[0]+int(w*.18),a[1]+int(w*.15))],fill=(54,48,38,180),width=max(2,w//180))
  elif name=='spall':
   for j in range(46):
    x=rng.uniform(g,w-g);y=w*.5+rng.normal(0,w*.025);r=rng.uniform(w*.008,w*.035)
    d.polygon([(x-r,y),(x,y-r*.7),(x+r,y+.5*r),(x-r*.4,y+r)],fill=(112,106,90,int(rng.integers(120,245))))
   d.line([(g,w//2),(w-g,w//2)],fill=(34,34,28,230),width=max(2,w//140))
  elif name in ('tire','rubber','oil','silt'):
   for j in range(360 if name=='oil' else 160):
    x=w*.5+rng.normal(0,w*(.10 if name=='oil' else .16));y=rng.uniform(g,w-g);ww=rng.uniform(w*.002,w*.035);hh=rng.uniform(w*.004,w*.07)
    a=int(rng.integers(12,58 if name=='oil' else 38));color=(39,36,29,a) if name!='silt' else (119,107,77,a)
    d.rectangle((x-ww,y-hh,x+ww,y+hh),fill=color)
   tile=tile.filter(ImageFilter.GaussianBlur(w*.006))
  elif name in ('runoff','salts','rust'):
   for j in range(75):
    x=w*.5+rng.normal(0,w*.19);length=rng.uniform(.12,.92);ww=rng.uniform(.005,.06)*w
    color=(59,53,40) if name=='runoff' else (206,202,177) if name=='salts' else (117,58,23)
    for k in range(35):
     y=g+length*(w-2*g)*k/35;a=int((1-k/35)**1.5*rng.uniform(45,170));d.rectangle((x-ww,y,x+ww,y+w/35),fill=(*color,a))
   tile=tile.filter(ImageFilter.GaussianBlur(w*.005))
  elif name in ('patch','repair'):
   pts=[(g+int(rng.integers(-g//3,g//3)),g),(w-g,g+7),(w-g-4,w-g),(g,w-g-8)]
   d.polygon(pts,fill=(103,101,87,240) if name=='patch' else (149,147,128,245));d.line(pts+[pts[0]],fill=(50,47,37,215),width=max(2,w//65))
  elif name=='ghost':
   for j in range(200):
    x=rng.uniform(w*.30,w*.70);y=rng.uniform(g,w-g);r=rng.uniform(1,w*.02);d.rectangle((x,y,x+r,y+r*3),fill=(193,190,159,int(rng.integers(10,80))))
  elif name=='weed':
   for j in range(40):
    x=rng.uniform(g,w-g);y=rng.uniform(g,w-g);d.line([(x,y),(x+w*.03,y-w*.10)],fill=(77,85,39,245),width=max(1,w//90))
  elif name=='litter':
   d.polygon([(w*.35,w*.35),(w*.69,w*.31),(w*.61,w*.70),(w*.40,w*.62)],fill=(197,189,164,250));d.line([(w*.4,w*.6),(w*.58,w*.42),(w*.64,w*.34)],fill=(127,123,109,245),width=max(1,w//60))
  im.paste(tile,(i%4*w,i//4*w))
 a=np.asarray(im).astype(np.float32)/255;orm=np.dstack([np.ones((size,size)),np.full((size,size),.85),np.zeros((size,size))])
 return srgb_to_linear(a[:,:,:3]),orm,.5-.3*a[:,:,3],a[:,:,3]

def save(path,array,bits=8):
 scratch=Path('build/texture-fields')/path.name;scratch.parent.mkdir(parents=True,exist_ok=True);write_png(scratch,array,bits=bits)
 data=scratch.read_bytes()
 if not path.exists() or path.read_bytes()!=data:path.write_bytes(data)
 path.touch();scratch.unlink()

def source(size=4096):
 out=Path('textures/source');out.mkdir(parents=True,exist_ok=True)
 for name,spec in SETS.items():
  alpha=None
  if name=='FreewaySigns':
   rgb=srgb_to_linear(np.asarray(Image.open('textures/checkpoint/T_Freeway_Signs.png').convert('RGB').resize((size,size),Image.Resampling.LANCZOS),np.float32)/255)
   yy=np.arange(size,dtype=np.float32)[:,None]%(size/4)/(size/4);rgb=rgb*(.90+.07*yy)[:,:,None];h=np.full((size,size),.5,np.float32)
   orm=np.dstack([np.ones((size,size)),np.full((size,size),.56),np.zeros((size,size))])
  elif name=='FreewayMaintenance':rgb,orm,h,alpha=maintenance(size)
  else:rgb,orm,h=manufacture(name,size)
  save(out/f'T_{name}_BaseColor.png',linear_to_srgb(rgb),bits=8);save(out/f'T_{name}_ORM.png',orm,bits=8);save(out/f'T_{name}_Height.png',np.repeat(h[:,:,None],3,axis=2),bits=16)
  if alpha is not None:save(out/f'T_{name}_Alpha.png',np.repeat(alpha[:,:,None],3,axis=2),bits=8)
  print('SOURCE',name,size,flush=True)
 Path('build/texture-plan.json').write_text(json.dumps(SETS,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--size',type=int,default=4096);a=ap.parse_args();source(a.size)
