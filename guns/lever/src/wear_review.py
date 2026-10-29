"""2D observed wear, actual-map mask, components and both area-share axes.

Comparison-only: photographs never enter a shader, mask or delivered texture.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from value_review import projection
from kit.fonts import find_font

def sample(im,xy):
 a=np.asarray(im.convert('RGB'),dtype=float);x=np.clip(xy[...,0],0,im.width-1.001);y=np.clip(xy[...,1],0,im.height-1.001)
 ix=x.astype(int);iy=y.astype(int);fx=(x-ix)[...,None];fy=(y-iy)[...,None]
 return (a[iy,ix]*(1-fx)+a[iy,ix+1]*fx)*(1-fy)+(a[iy+1,ix]*(1-fx)+a[iy+1,ix+1]*fx)*fy

def components(mask):
 unseen=set(zip(*np.nonzero(mask)));rows=[]
 while unseen:
  seed=unseen.pop();group=[seed];todo=[seed]
  while todo:
   y,x=todo.pop()
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     p=(y+dy,x+dx)
     if p in unseen:unseen.remove(p);group.append(p);todo.append(p)
  a=np.asarray(group);lo=a.min(0);hi=a.max(0)
  rows.append(dict(area_mm2=len(group)*.25,length_mm=float(hi[1]-lo[1]+1)*.5,height_mm=float(hi[0]-lo[0]+1)*.5,
   boundary_clipped=bool((lo==0).any() or hi[0]==mask.shape[0]-1 or hi[1]==mask.shape[1]-1)))
 return sorted(rows,key=lambda r:-r['area_mm2'])

def main():
 out=BASE/'renders/final/pairs';out.mkdir(parents=True,exist_ok=True)
 data=np.load(BASE/'build/review/wear-grid.npz');points=data['points'];height,width=points.shape[:2]
 hero=Image.open(BASE/'renders/final/beauty/hero_left.png');shot=json.loads((BASE/'renders/final/beauty/shots.json').read_text())['hero_left']
 rendered=sample(hero,projection(shot,points.reshape(-1,3),hero.size).reshape(height,width,2))
 # Independently observed lower-edge quadrilateral in the white-balanced
 # used photograph. Approximately 115 x 8 mm: different original forging,
 # perspective and light. Four corners are explicit, never fitted to a mask.
 photo=Image.open(BASE/'build/white-balanced/receiver.png');quad=np.array(((650,225),(300,207),(300,184),(650,202)),dtype=float)
 u,v=np.meshgrid((np.arange(width)+.5)/width,(np.arange(height)+.5)/height)
 xy=(1-v)[...,None]*((1-u)[...,None]*quad[0]+u[...,None]*quad[1])+v[...,None]*((1-u)[...,None]*quad[3]+u[...,None]*quad[2])
 photographed=sample(photo,xy)
 # Independent native observations of the apparent gray rubbed fillet. These
 # are comparison annotations, never read by modeling/material/bake code.
 # The oxide and reflected sky have similar luma, so a single brightness
 # threshold cannot identify the photographed substrate honestly.
 xs=[300,325,350,375,400,425,450,475,500,525,550,575,600,625,650]
 tops=[195,197,198,199,201,202,204,205,207,209,213,215,215,213,215]
 bottoms=[200,202,203,204,207,208,210,211,214,216,221,224,222,220,221]
 polygon=list(zip(xs,tops))+list(reversed(list(zip(xs,bottoms))))
 marked=Image.new('L',photo.size);ImageDraw.Draw(marked).polygon(polygon,fill=255)
 annotated=sample(marked.convert('RGB'),xy)[...,0]>127
 # Exposed steel is now darker satin. A brightness threshold would shrink
 # an unchanged contact field simply because its reflectance was corrected.
 # Inspect the actual scalar factor, independently projected on shipping UVs.
 base=data['base'].astype(float);physical=data['contact']>.42
 images={'exported_hero':rendered,'white_balanced_photo':photographed};rows={};masks={};threshold=75
 for name,rgb in images.items():
  luma=rgb@np.array((.2126,.7152,.0722));mask=physical if name=='exported_hero' else annotated;masks[name]=mask
  rows[name]=dict(worn_share=float(mask.mean()),along_length=mask.mean(0).tolist(),across_height=mask.mean(1).tolist(),
   thirds_length=[float(p.mean()) for p in np.array_split(mask,3,axis=1)],quarters_height=[float(p.mean()) for p in np.array_split(mask,4,axis=0)],
   components=components(mask),threshold_sensitivity={str(t):float(np.mean(luma>t)) for t in (60,65,70,75,80,85,90)},
   worn_median_rgb=np.median(rgb[mask],axis=0).tolist() if mask.any() else [],
   mask_method='actual projected OUT_wear >0.42, independently of steel brightness' if name=='exported_hero' else 'independent observed gray-fillet polygon; native coordinates recorded')
 rows['contact_factor_mask']=dict(worn_share=float(physical.mean()),along_length=physical.mean(0).tolist(),across_height=physical.mean(1).tolist(),components=components(physical),
  worn_base_rgb=np.median(base[physical],axis=0).tolist() if physical.any() else [],worn_orm=np.median(data['orm'][physical],axis=0).tolist() if physical.any() else [],
  factor_threshold=.42,factor_threshold_sensitivity={str(t):float((data['contact']>t).mean()) for t in (.35,.4,.42,.45,.5,.6)})
 result=dict(scope='Two-dimensional equal physical-grid comparison: shader contact factor projected on delivery UVs versus independently annotated apparent gray fillet; actual shipping RGB/ORM sampled separately. Brightness is not used to classify the darker satin steel. No albedo inversion.',
  grid_step_mm=.5,dimensions_mm=[width*.5,height*.5],photo_quad_native=quad.tolist(),observed_threshold_luma=threshold,
  photo_neutral='Polished pivot-screw facet, native (363,100)-(369,105); estimated reflected silver.',photo_worn_polygon_native=polygon,
  limitations='The photo quadrilateral is an approximate 115 mm class envelope with a different fillet contour; annotation is uncertain about one native pixel. Gray oxide, wear and reflected light cannot establish coating chemistry. Hero sampling and atlas filtering prevent exact scratch-history equivalence.',rows=rows)
 (out/'wear-2d-values.json').write_text(json.dumps(result,indent=2))
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),19);canvas=Image.new('RGB',(1600,780),(231,231,226));draw=ImageDraw.Draw(canvas)
 for j,(name,rgb) in enumerate(images.items()):
  draw.text((12+j*800,8),name.replace('_',' ')+' / same 115 x 8 mm grid',font=font,fill='black')
  for k,a in enumerate((rgb,np.repeat((masks[name]*255)[...,None],3,axis=2))):
   im=Image.fromarray(np.uint8(np.clip(a,0,255)));im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((770,104),Image.Resampling.NEAREST)
   canvas.paste(im,(15+j*800,45+k*145))
  draw.text((15+j*800,155),'Color above; '+('contact factor at delivery UVs' if j==0 else 'observed gray fillet annotation')+' below',font=font,fill='black')
  draw.text((15+j*800,300),'Worn area %.2f%%; %d connected regions'%(rows[name]['worn_share']*100,len(rows[name]['components'])),font=font,fill='black')
  for axis,key in enumerate(('along_length','across_height')):
   values=rows[name][key];x0=20+j*800;y0=370+axis*170
   draw.text((x0,y0-30),'Worn share '+('along the area' if axis==0 else 'across its height (bottom to top)'),font=font,fill='black')
   draw.rectangle((x0,y0,x0+755,y0+105),outline=(100,100,100))
   line=[(x0+i*755/max(1,len(values)-1),y0+105-v*105) for i,v in enumerate(values)]
   draw.line(line,fill=(75,95,160),width=2)
 draw.text((15,730),'Contact factor >0.42: %.2f%% / photographic annotation +/-1 px; shipping RGB/ORM and threshold sensitivity in JSON'%(physical.mean()*100),font=font,fill='black')
 canvas.save(out/'wear-2d-pair.jpg',quality=94,optimize=True)
 print('2D WEAR',[(n,round(r['worn_share']*100,2)) for n,r in rows.items()],flush=True)
if __name__=='__main__':main()
