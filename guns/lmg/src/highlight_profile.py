"""Observed cover highlight width, on native pixels with explicit construction limits."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from look_review import FONT,SMALL
from image_masks import raster,projection

def profile(a,x,y0,y1):
 x=int(x);y0=int(y0);y1=int(y1);v=np.median(a[y0:y1,max(0,x-2):x+3,:3].max(2),axis=1);floor=float(np.percentile(v,10));peak=float(np.percentile(v,95));threshold=(floor+peak)/2;above=v>=threshold
 # Broad width of the principal reflection, excluding separate chipped peaks.
 runs=[];start=None
 for i,on in enumerate(np.r_[above,False]):
  if on and start is None:start=i
  if not on and start is not None:runs.append((start,i));start=None
 largest=max(runs,key=lambda r:r[1]-r[0]) if runs else (0,0)
 return dict(value_profile=v.tolist(),bounds=[x,y0,x,y1],floor=floor,peak=peak,half_height=threshold,principal_width_pixels=largest[1]-largest[0],part_span_pixels=len(v),width_fraction=(largest[1]-largest[0])/max(len(v),1))

def main():
 root=BASE/'renders/final';meta=json.loads((root/'photos/shots.json').read_text())['used_photo'];im=np.asarray(Image.open(root/'photos/used_photo.png').convert('RGB'));h,w=im.shape[:2];geo=np.load(BASE/'build/image-geometry/used_photo.npz');assert str(geo['sha256'])==meta['sha256'];ids,_=raster(geo,meta,w,h)
 select=[i+1 for i,n in enumerate(geo['names']) if str(n)=='FeedCover_Shell'];mask=np.isin(ids,select);point,_=projection(np.array([[-.03,.190,.137]]),meta,w,h);x=int(point[0,0]);ys=np.flatnonzero(mask[:,x]);render=profile(im,x,ys.min(),ys.max()+1)
 photo=np.asarray(Image.open(BASE/'build/white-balanced/used_receiver.jpg').convert('RGB'));reference=profile(photo,630,320,393)
 record=dict(render=render,photo=reference,sha256=meta['sha256'],limit='The photo station crosses the front cylindrical pressing. The accepted original has a hemmed sheet crown at the analogous axial station. Width is normalized to the apparent part span; it is not a recovered BRDF or identical geometry.')
 out=root/'surface-pairs';out.mkdir(exist_ok=True);(out/'paint-highlight-width.json').write_text(json.dumps(record,indent=2))
 canvas=Image.new('RGB',(1800,950),'#e7e9e6');d=ImageDraw.Draw(canvas);d.text((25,15),'Paint satin / native reflection profile, source GLB vs gray-balanced studio photo',font=FONT,fill='black')
 for col,(a,r,label) in enumerate(((im,render,'Exported 2048 GLB'),(photo,reference,'Native photograph'))):
  x0,y0,_,y1=r['bounds'];crop=Image.fromarray(a).crop((max(0,x0-150),max(0,y0-12),x0+150,y1+12));crop.thumbnail((840,390));canvas.paste(crop,(25+900*col,65));q=np.array(r['value_profile']);points=[(35+900*col+i/max(len(q)-1,1)*780,720-v*1.1) for i,v in enumerate(q)];d.line(points,fill=(140,55,25) if col==0 else (25,90,145),width=3)
  d.text((25+900*col,775),label+' FWHM %.1f%% of visible station'%(r['width_fraction']*100),font=FONT,fill='black');d.text((25+900*col,810),'P95 profile value %.1f / native span %d px'%(r['peak'],r['part_span_pixels']),font=SMALL,fill='black')
 import textwrap
 for i,line in enumerate(textwrap.wrap(record['limit'],155)):d.text((25,865+i*24),line,font=SMALL,fill='black')
 canvas.save(out/'paint-highlight-width.jpg',quality=94)
 print('PAINT HIGHLIGHT WIDTH',render['width_fraction'],reference['width_fraction'])
if __name__=='__main__':main()
