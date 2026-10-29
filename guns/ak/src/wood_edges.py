"""Review only: exposed film loss versus adjacent intact wood on the same blank.

Masks use actual imported surface IDs, physical Y/Z regions and shipped ORM.
Both BaseColor and native hero are sampled on exactly the same visible pixels.
No photo or diagnostic image enters the shader, bake or export.
"""
from pathlib import Path
import argparse, colorsys, hashlib, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
BASE=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from image_masks import raster,bilinear
from kit.fonts import find_font
LUMA=np.array([.2126,.7152,.0722])
# Each pair is (worn Ymin,Ymax,Zmin,Zmax), then its adjacent intact land.
# Regions are physical and fixed before looking at any pixel's color.
SITES=[
 ('Lower handguard rear lower','LowerHandguard_Sculpt',(.245,.305,.045,.064),(.245,.305,.064,.073)),
 ('Upper handguard rear lower','UpperHandguard_Sculpt',(.250,.305,.088,.102),(.250,.305,.102,.111)),
 ('Stock toe','Stock_Sculpt',(-.279,-.211,-.014,.012),(-.279,-.211,.012,.027)),
 ('Stock heel','Stock_Sculpt',(-.279,-.249,.071,.090),(-.279,-.249,.056,.071)),
 ('Stock comb','Stock_Sculpt',(-.245,-.065,.079,.090),(-.245,-.065,.067,.079)),
 ('Lower handguard front','LowerHandguard_Sculpt',(.345,.363,.045,.090),(.327,.343,.045,.090)),
 ('Upper handguard front','UpperHandguard_Sculpt',(.331,.346,.088,.125),(.313,.330,.088,.125)),
]
def stats(rgb):
 rgb=np.asarray(rgb);med=np.median(rgb,axis=0)
 hue,sat,val=colorsys.rgb_to_hsv(*(med/255))
 return dict(pixels=len(rgb),median_rgb=med.round(2).tolist(),median_luma=float(np.median(rgb@LUMA)),
             median_value=float(np.median(rgb.max(axis=1))),hue_of_median_degrees=hue*360,
             saturation_of_median=sat)
def bounds(mask):
 j,i=np.where(mask)
 return [int(i.min()),int(j.min()),int(i.max()+1),int(j.max()+1)] if len(i) else None
def main():
 p=argparse.ArgumentParser();p.add_argument('--baseline',action='store_true');a=p.parse_args()
 root=BASE/'build/wood-edge-baseline' if a.baseline else BASE
 final=root/('final' if a.baseline else 'renders/final')
 out=BASE/('build/wood-edge-baseline/edge-review' if a.baseline else 'renders/final/look-review')
 out.mkdir(parents=True,exist_ok=True)
 meta=json.loads((final/'beauty/shots.json').read_text())['hero']
 assert meta['sha256']==hashlib.sha256((root/'export/ak.glb').read_bytes()).hexdigest()
 hero=np.asarray(Image.open(final/'beauty/hero.png').convert('RGB')).astype(float);h,w=hero.shape[:2]
 g=np.load(BASE/'build/value-geometry.npz');geo={k:g[k] for k in g.files}
 ids,uv=raster(geo,meta,w,h)
 _,yz=raster(dict(geo,uv=geo['xyz'][:,:,1:]),meta,w,h);y,z=yz[:,:,0],yz[:,:,1]
 coords=np.stack([uv[:,:,0].ravel()*2047,(1-uv[:,:,1].ravel())*2047],axis=1).astype(float)
 maps={}
 for key in ('BaseColor','ORM'):
  im=np.asarray(Image.open(root/'textures'/('T_Rill39_'+key+'.png')).convert('RGB')).astype(float)
  maps[key]=bilinear(im,coords).reshape(h,w,3)
 rough=maps['ORM'][:,:,1]
 labels=Image.fromarray(hero.astype('uint8'));draw=ImageDraw.Draw(labels)
 font=ImageFont.truetype(find_font('Noto Sans','Regular'),15)
 rows=[]
 for number,(name,part,wear_region,neighbor_region) in enumerate(SITES,1):
  selected=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n)==part])
  def region(b):return selected&(y>=b[0])&(y<b[1])&(z>=b[2])&(z<b[3])
  # .62 is above intact film including the dull upper, below exposed .70.
  worn=region(wear_region)&(rough>158)
  intact=region(neighbor_region)&(rough<150)
  assert worn.sum()>4 and intact.sum()>4,(name,int(worn.sum()),int(intact.sum()))
  row=dict(site=name,part=part,worn_yz_m=wear_region,neighbor_yz_m=neighbor_region,
           worn_region_xyxy=bounds(worn),neighbor_region_xyxy=bounds(intact),
           worn_pixels=int(worn.sum()),intact_pixels=int(intact.sum()))
  for key,rgb in [('basecolor',maps['BaseColor']),('hero',hero)]:
   used=stats(rgb[worn]);adjacent=stats(rgb[intact])
   delta=(used['hue_of_median_degrees']-adjacent['hue_of_median_degrees']+180)%360-180
   row[key]=dict(worn=used,intact=adjacent,hue_delta_degrees=delta,
                 value_ratio=used['median_value']/adjacent['median_value'])
  for mask,color in [(worn,(210,156,42)),(intact,(52,173,204))]:
   box=bounds(mask);draw.rectangle(box,outline=color,width=1)
  box=bounds(worn);draw.text((box[0],max(0,box[1]-18)),str(number),font=font,fill=(238,187,66))
  rows.append(row)
 labels.save(out/'wood-edge-regions.png')
 report=dict(method=__doc__,render_sha256=meta['sha256'],resolution=[w,h],rows=rows,
             classification='Worn: shipped ORM G >158/255. Intact neighbor: G <150/255. Fixed physical regions; no RGB gating, morphology, exposure or white-balance correction.',
             values='8-bit sRGB BaseColor sampled bilinearly at visible surface UVs; native hero display RGB. Y is Rec.709 display luma; V is max RGB. Hue is HSV hue of median RGB.',
             limits='Visible pixel footprints, not total authored area. Adjacent wood differs in grain, grime, curvature and illumination; ratios are observations, not an inverse BRDF estimate.')
 (out/'wood-edge-values.json').write_text(json.dumps(report,indent=2)+'\n')
 chart=Image.new('RGB',(1600,160+len(rows)*120),'#ebede9');d=ImageDraw.Draw(chart)
 d.text((20,12),'Wood film loss / same visible surface samples in shipped BaseColor and native hero',font=font,fill='black')
 d.text((20,42),'Fixed physical regions; worn ORM G >158, intact G <150. Hue and value include grain, grime and (hero) light.',font=font,fill='black')
 for k,title in enumerate(('BaseColor worn','BaseColor intact','Hero worn','Hero intact')):
  d.text((350+k*305,85),title,font=font,fill='black')
 for i,row in enumerate(rows):
  yy=122+i*120;d.text((20,yy+8),row['site'],font=font,fill='black')
  for k,(key,state) in enumerate((('basecolor','worn'),('basecolor','intact'),('hero','worn'),('hero','intact'))):
   v=row[key][state];x=350+k*305;rgb=tuple(round(c) for c in v['median_rgb'])
   d.rectangle((x,yy,x+90,yy+55),fill=rgb)
   d.text((x+100,yy),'/'.join(str(c) for c in rgb),font=font,fill='black')
   d.text((x+100,yy+25),f"Y {v['median_luma']:.1f}; V {v['median_value']:.1f}",font=font,fill='black')
   d.text((x,yy+65),f"Hue {v['hue_of_median_degrees']:.1f}°; saturation {v['saturation_of_median']:.3f}",font=font,fill='black')
 chart.save(out/'wood-edge-colors.jpg',quality=95)
 lines=['| Site | BaseColor worn / intact RGB; V ratio; Δh | Hero worn / intact RGB; V ratio; Δh |',
        '| --- | --- | --- |']
 for row in rows:
  cells=[]
  for key in ('basecolor','hero'):
   v=row[key];fmt=lambda b:'/'.join(str(round(c)) for c in b['median_rgb'])
   cells.append(f"{fmt(v['worn'])} / {fmt(v['intact'])}; {v['value_ratio']:.3f}; {v['hue_delta_degrees']:+.1f}°")
  lines.append('| '+row['site']+' | '+' | '.join(cells)+' |')
 (out/'wood-edge-table.md').write_text('\n'.join(lines)+'\n')
 print('\n'.join(lines),flush=True)
if __name__=='__main__':main()
