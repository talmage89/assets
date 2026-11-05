"""Original shared manufactured trims and causal service-age fields.

32 guarded trim cells. No photographic pixels are accepted. Physical height
fields are baked with Cycles at 4096 then filtered to 2048 with the kit.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import write_png,linear_to_srgb
from kit.fonts import find_font
ROLES=['zinc','green','black','bronze','yellow','inside','steel','white','concrete','cabinet','rubber','border','r10','panel','record','rust','zinc_top','yellow_top','black_top','bronze_top','green_top','cabinet_lower','optics','sticker','zinc_base','yellow_chalk','black_chalk','bronze_chalk','green_chalk','concrete_form','white_aged','button_worn']
COLORS=[(.235,.245,.245),(.014,.038,.025),(.009,.011,.010),(.047,.034,.022),(.70,.285,.010),(.004,.005,.006),(.31,.33,.33),(.60,.61,.58),(.32,.325,.303),(.32,.345,.345),(.006,.007,.006),(.62,.39,.012)]
def smooth(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)
def noise(w,h,cells,rng):
 a=rng.random((max(2,round(cells*h/w)),cells)).astype('float32')
 return np.asarray(Image.fromarray(a).resize((w,h),Image.Resampling.BICUBIC))
def fields(size=4096,wear=.8):
 out=Path('build/procedural');out.mkdir(parents=True,exist_ok=True)
 W,H=size//4,size//8;rng=np.random.default_rng(510219)
 rgb=np.empty((size,size,3),dtype='float32');orm=np.ones_like(rgb);height=np.zeros((size,size),dtype='float32')
 y,x=np.mgrid[:H,:W].astype('float32');u=(x+.5)/W;v=1-(y+.5)/H
 for i,role in enumerate(ROLES):
  base=role.split('_')[0];j=ROLES.index(base) if base in ROLES[:12] else 0
  c=np.broadcast_to(np.array(COLORS[j],dtype='float32'),(H,W,3)).copy();rough=np.full((H,W),.69,dtype='float32');metal=np.zeros((H,W),dtype='float32');ao=np.ones((H,W),dtype='float32');hh=np.zeros((H,W),dtype='float32')
  fine=rng.random((H,W),dtype='float32');mid=noise(W,H,57,rng);broad=noise(W,H,14,rng)
  c*=1+.035*(fine-.5)[:,:,None]
  if base in ('zinc','steel','cabinet'):
   # Small zinc crystallites/brushed sheet, patina reduces specular response.
   metal[:]=.82 if base=='zinc' else .95;rough[:]=.62 if base=='zinc' else .45
   grains=noise(W,H,95,rng);c*=.98+.04*grains[:,:,None];hh=.000018*(grains-.5)
   if base=='zinc':
    patina=smooth((broad-.44)/.28)*.22*wear;c=c*(1-patina[:,:,None])+np.array((.40,.41,.39))*patina[:,:,None];rough+=patina*.5
   else:rough+=.025*np.sin(v*1100+mid*3)
   if role=='zinc':
    # Lower sheltered zinc retains water and develops a white zinc oxide film.
    stain=smooth((.27-v)/.15)*np.exp(-((u-.62)/.13)**2)*wear*.48
    c=c*(1-stain[:,:,None])+np.array((.43,.44,.42))*stain[:,:,None];rough+=stain*.35
    # Runoff below the upper cap/perch, down one real exposed shaft face.
    trail=np.exp(-((u-.60-.006*np.sin(v*14))/.025)**2)*smooth((.94-v)/.035)*smooth((v-.69)/.12)*wear*.55
    c=c*(1-trail[:,:,None])+np.array((.60,.57,.48))*trail[:,:,None];rough+=trail*.4
  elif base=='concrete':
   rough[:]=.93;c*=.95+.10*mid[:,:,None];hh=.00019*(fine-.5)-.00030*np.maximum(0,.18-mid)
  elif base=='rubber':rough[:]=.86;hh=.00006*(fine-.5)
  elif base in ('yellow','green','black','bronze','white'):
   rough[:]=.63;hh=.000025*(fine-.5)
   # Sun-facing surfaces retain hue as binder chalks. Direction chosen in UVs.
   fade=smooth((v-.40)/.5)*wear*.42
   c=c*(1-fade[:,:,None])+np.array(COLORS[j])*1.7*fade[:,:,None];rough+=fade*.55
   # Narrow unequal gravity tracks start below retained dirt ledges.
   tails=np.zeros_like(u)
   for cx,length,width in ((.24,.32,.065),(.71,.24,.047)):
    tails+=np.exp(-((u-cx-.010*np.sin(v*11))/width)**2)*smooth((length-v)/.18)
   dirt=np.clip(tails*.60*wear*(.65+.35*mid),0,.5)
   c*=1-dirt[:,:,None];rough+=dirt*.22
  if role.endswith('_top'):
   # Droppings only on upward exposed surfaces under perches. One deposit and
   # its gravity tail, not mottling painted uniformly over the support.
   deposit=np.zeros_like(u)
   for cx,cy in ((.27,.55),(.68,.44)):
    core=np.exp(-(((u-cx)/.075)**2+((v-cy)/.12)**2)*1.8)
    tail=np.exp(-((u-cx-.01*np.sin(v*22))/.022)**2)*smooth((cy-v)/.15)*smooth((v-cy+.38)/.12)
    deposit+=core+.38*tail
   deposit=np.clip(deposit*wear,0,.92)*( .75+.25*mid)
   c=c*(1-deposit[:,:,None])+np.array((.60,.57,.48))*deposit[:,:,None];hh+=.00035*deposit;rough+=deposit*.25
  if role in ('rust','zinc_base'):
   # Crevice/edge oxidation: rusty nuts and plate perimeter, no broad red wash.
   c[:]=COLORS[6] if role=='rust' else COLORS[0];metal[:]=.86
   edge=np.minimum.reduce((u,1-u,v,1-v));mask=smooth((.10+.04*(mid-.5)-edge)/.06)*wear*smooth((broad-.30)/.42)
   c=c*(1-mask[:,:,None])+np.array((.12,.043,.012))*mask[:,:,None];metal*=1-mask;rough=.57+.36*mask;hh-=.00012*mask
  if role=='cabinet_lower':
   splash=smooth((.38-v+(broad-.5)*.12)/.27)*wear*.62*(.55+.45*mid)
   c=c*(1-splash[:,:,None])+np.array((.085,.075,.052))*splash[:,:,None];rough+=splash*.6
  if role=='concrete_form':
   seam=np.exp(-((v-.32)/.009)**2)+np.exp(-((v-.72)/.012)**2);hh-=seam*.0006;c*=1-seam[:,:,None]*.13
  if role=='button_worn':
   c[:]=(.24,.255,.25);metal[:]=.92;rough[:]=.44
   radius=((u-.5)/.5)**2+((v-.5)/.5)**2;touch=np.exp(-radius*2.5);rough-=.20*touch
   scratches=np.zeros_like(u)
   for cx,cy,length in ((.38,.57,.14),(.51,.48,.18),(.61,.44,.09),(.45,.38,.10)):
    scratches+=np.exp(-((v-cy+.12*(u-cx))/.003)**2)*smooth((length-abs(u-cx))/.02)
   c*=1-np.clip(scratches*.30,0,.3)[:,:,None];hh=-.000018*scratches
  if role=='optics':c[:]=(.002,.004,.004);rough[:]=.27;metal[:]=0;hh[:]=0
  if role in ('r10','panel','record','sticker'):
   c[:]=(.52,.53,.49) if role in ('r10','record','sticker') else (.075,.084,.078);hh[:]=0;rough[:]=.72;metal[:]=0
   im=Image.fromarray(np.uint8(linear_to_srgb(c)*255+.5));d=ImageDraw.Draw(im);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),max(9,W//32))
   if role=='r10':
    source=Image.open('build/graphics/r10.png').convert('RGB');im=source.resize((W,H),Image.Resampling.LANCZOS)
   elif role=='panel':
    small=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),max(10,W//45))
    # Four original unit fronts share this guarded tile, selected by trim UVs.
    for unit,label in enumerate(('CONTROLLER','CONFLICT MONITOR','DETECTOR INPUTS','POWER / BREAKERS')):
     ox=(unit%2)*W/2;oy=(unit//2)*H/2;ww=W/2;hh2=H/2
     d.rectangle((ox+8,oy+8,ox+ww-8,oy+hh2-8),outline=(110,119,111),width=2)
     d.text((ox+ww*.06,oy+hh2*.77),label,font=small,fill=(189,191,177))
     if unit==0:
      d.rectangle((ox+ww*.07,oy+hh2*.16,ox+ww*.59,oy+hh2*.64),fill=(24,61,48),outline=(134,151,133),width=2)
      d.text((ox+ww*.10,oy+hh2*.22),'PHASE 02\nRUN / 24 SEC',font=small,fill=(104,137,106))
      for row in range(3):
       for col in range(3):
        xx=ox+ww*(.68+col*.08);yy=oy+hh2*(.22+row*.16);d.rectangle((xx,yy,xx+ww*.047,yy+hh2*.08),fill=(124,127,115))
     elif unit==1:
      for row in range(3):
       for col in range(8):
        xx=ox+ww*(.08+col*.105);yy=oy+hh2*(.19+row*.18);d.ellipse((xx,yy,xx+ww*.025,yy+ww*.025),fill=(90,112,48) if row==0 and col<4 else (40,49,36))
     elif unit==2:
      for col in range(8):
       xx=ox+ww*(.07+col*.11);d.rectangle((xx,oy+hh2*.16,xx+ww*.075,oy+hh2*.67),fill=(52,64,54),outline=(124,130,110),width=2)
       d.ellipse((xx+ww*.02,oy+hh2*.24,xx+ww*.05,oy+hh2*.29),fill=(122,128,48))
     else:
      for col in range(6):
       xx=ox+ww*(.07+col*.145);d.rectangle((xx,oy+hh2*.20,xx+ww*.09,oy+hh2*.59),fill=(23,27,24));d.rectangle((xx+ww*.02,oy+hh2*.32,xx+ww*.07,oy+hh2*.42),fill=(94,95,80))
   else:
    d.text((W*.08,H*.1),'SERVICE RECORD\nINSPECTED\nWAYCROFT / DISTRICT 04',font=font,fill=(46,54,48))
    for k in range(5):d.line((W*.08,H*(.43+k*.09),W*.91,H*(.43+k*.09)),fill=(91,95,86),width=2)
    if role=='sticker':d.rectangle((W*.05,H*.04,W*.95,H*.96),outline=(90,91,75),width=3)
   a=np.asarray(im).astype('float32')/255;c=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
  guard=12 # six delivered pixels, dilation on all four edges.
  def pad(a):return np.pad(a[guard:-guard,guard:-guard],((guard,guard),(guard,guard))+(((0,0),) if a.ndim==3 else ()),mode='edge')
  row,col=divmod(i,4);sl=(slice(size-(row+1)*H,size-row*H),slice(col*W,(col+1)*W))
  rgb[sl]=pad(c);orm[sl]=pad(np.stack((ao,np.clip(rough,0,1),metal),2));height[sl]=pad(hh)
 lo=float(height.min());distance=float(height.max()-lo)
 for channel,values in dict(BaseColor=linear_to_srgb(rgb),ORM=orm,Height=((height-lo)/distance)[:,:,None]).items():write_png(out/f'T_Signals_{channel}.png',values,bits=16 if channel=='Height' else 8)
 (out/'fields.json').write_text(json.dumps(dict(size=size,height_distance_m=distance,wear=wear,roles=ROLES),indent=2))
def bake():
 from kit.flat_bake import bake
 r=json.loads(Path('build/procedural/fields.json').read_text());bake(Path('build/procedural'),Path('textures/bake'),'Signals',4,r['size'],4,r['height_distance_m'])
def ship():
 import subprocess
 subprocess.run([sys.executable,str(ROOT/'kit/downsample.py'),'--source','textures/bake','--out','textures/ship','--asset','Signals','--size','2048'],check=True)
 folder=Path('textures/ship')
 im=Image.open('build/graphics/lenses.png');im=im.resize((1024,1024),Image.Resampling.NEAREST);im.save(folder/'T_Signals_Emissive.png')
 Image.open('build/graphics/names.png').resize((512,256),Image.Resampling.LANCZOS).save(folder/'T_Signals_Names.png')
 (folder/'sets.json').write_text(json.dumps(dict(atlas=2048,emissive=1024,names=[512,256],gpu_compressed_full_mips_mib=17.5,compression='8 bpp per map, full mip chain; runtime engine compression required'),indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['fields','bake','ship']);p.add_argument('--wear',type=float,default=.8);a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 fields(wear=a.wear) if a.stage=='fields' else globals()[a.stage]()
