"""Read-only whole-part paint measurements of the two accepted precedents.

Only this asset's ignored evidence directory is written. Each precedent keeps
its original photographic camera, light, embedded maps, scripts and output.
"""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from look_review import metrics,polygon_mask,mask_crop,FONT,SMALL
from image_masks import raster
from PIL import ImageDraw

SPECS={
 'ak':dict(shot='right_photo',photo='museum.jpg',polygons=[[(580,162),(1136,153),(1137,229),(581,243)]],prefixes=('Receiver_Sheet','Receiver_Rivet','Selector_')),
 'smg':dict(shot='locked_photo',photo='navy2.png',polygons=[[(1702,218),(2040,186),(2330,183),(2580,174),(2625,197),(2637,350),(1724,395)]],prefixes=('Receiver_Shell','Receiver_FoldSeam','Receiver_SpotWeld')),
}
def main():
 out=BASE/'renders/final/family-paint';out.mkdir(parents=True,exist_ok=True);rows={}
 for gun,s in SPECS.items():
  b=BASE.parent/gun;source=b/'export'/(gun+'.glb');sha=hashlib.sha256(source.read_bytes()).hexdigest()
  metadata=json.loads((b/'renders/final/photos/shots.json').read_text())[s['shot']]
  assert sha==metadata['sha256'],(gun,'stale accepted photo render')
  im=np.asarray(Image.open(b/'renders/final/photos'/(s['shot']+'.png')).convert('RGB'));h,w=im.shape[:2]
  if gun=='ak':geo=np.load(b/'build/value-geometry.npz')
  else:
   d=np.load(b/'build/value-surfaces.npz');geo=dict(xyz=d['triangles'],uv=d['uvs'],ids=d['parts']+1,names=d['names'])
  ids,_=raster(geo,metadata,w,h);mask=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(s['prefixes'])])
  mask=np.asarray(Image.fromarray(mask.astype('uint8')*255).filter(ImageFilter.MinFilter(3)))>0
  ref=np.asarray(Image.open(b/'build/white-balanced'/s['photo']).convert('RGB'));pm=polygon_mask((ref.shape[1],ref.shape[0]),s['polygons'])
  pm=np.asarray(Image.fromarray(pm.astype('uint8')*255).filter(ImageFilter.MinFilter(3)))>0
  corrections=json.loads((b/'build/white-balanced/corrections.json').read_text());neutral=corrections['museum.jpg' if gun=='ak' else 'navy2.jpg']
  r=metrics(im[mask]);p=metrics(ref[pm]);rows[gun]=dict(render=r,photo=p,neutral=neutral,source_sha256=sha,render_shot=s['shot'],photo_source=s['photo'],photo_polygons=s['polygons'],whole_parts=s['prefixes'],unchanged=True)
  panel=Image.new('RGB',(1800,850),'#e7e9e6');draw=ImageDraw.Draw(panel)
  draw.text((25,15),gun.upper()+' / unchanged exported asset, whole painted receiver / original photographic light',font=FONT,fill='black')
  panel.paste(mask_crop(im,mask),(25,65));panel.paste(mask_crop(ref,pm),(925,65))
  for col,(label,m) in enumerate([('Accepted GLB',r),('White-balanced photo',p)]):
   x=25+900*col
   draw.text((x,480),label+' V10/50/90 '+str(np.round(m['value_p10_p50_p90'],1).tolist()),font=FONT,fill='black')
   draw.text((x,520),'Highlight RGB '+str(np.round(m['brightest_decile_rgb'],1).tolist()),font=SMALL,fill='black')
   hist=np.array(m['value_histogram'],float);hist/=max(hist.max(),1)
   draw.line([(x+10+j*25,740-v*150) for j,v in enumerate(hist)],fill=(130,60,30) if col==0 else (30,90,140),width=3)
  draw.text((25,790),'Includes existing wear. Geometry masks eroded one pixel; same V and brightest-decile conventions as Harrow.',font=SMALL,fill='black')
  panel.save(out/(gun+'-paint-histograms.jpg'),quality=94)
 (out/'finish-values.json').write_text(json.dumps(rows,indent=2))
 for g,r in rows.items():print(g,r['render']['value_p10_p50_p90'],r['photo']['value_p10_p50_p90'],r['render']['brightest_decile_rgb'],r['photo']['brightest_decile_rgb'])
if __name__=='__main__':main()
