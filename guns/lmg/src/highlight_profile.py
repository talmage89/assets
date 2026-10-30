"""Observed cover highlight width, on native pixels with explicit construction limits."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from look_review import FONT,SMALL,REGIONS,metrics,polygon_mask
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
 root=BASE/'renders/final';geometry=BASE/(sys.argv[sys.argv.index('--geometry')+1] if '--geometry' in sys.argv else 'build/image-geometry');meta=json.loads((root/'photos/shots.json').read_text())['used_photo'];im=np.asarray(Image.open(root/'photos/used_photo.png').convert('RGB'));h,w=im.shape[:2];geo=np.load(geometry/'used_photo.npz');assert str(geo['sha256'])==meta['sha256'];ids,_=raster(geo,meta,w,h)
 select=[i+1 for i,n in enumerate(geo['names']) if str(n)=='FeedCover_Shell'];mask=np.isin(ids,select);point,_=projection(np.array([[-.03,.190,.137]]),meta,w,h);x=int(point[0,0]);ys=np.flatnonzero(mask[:,x]);render=profile(im,x,ys.min(),ys.max()+1)
 photo=np.asarray(Image.open(BASE/'build/white-balanced/used_receiver.jpg').convert('RGB'));reference=profile(photo,630,320,393)
 record=dict(render=render,photo=reference,sha256=meta['sha256'],limit='The photo station crosses the front cylindrical pressing. The accepted original has a hemmed sheet crown at the analogous axial station. Width is normalized to the apparent part span; it is not a recovered BRDF or identical geometry.')
 record['local_profile_pass']=bool(abs(render['width_fraction']/reference['width_fraction']-1)<=.10 and abs(render['peak']/reference['peak']-1)<=.10)
 out=root/'surface-pairs';out.mkdir(exist_ok=True);(out/'paint-highlight-width.json').write_text(json.dumps(record,indent=2))
 canvas=Image.new('RGB',(1800,950),'#e7e9e6');d=ImageDraw.Draw(canvas);d.text((25,15),'Paint satin / native reflection profile, source GLB vs gray-balanced studio photo',font=FONT,fill='black')
 d.text((25,42),'Native width and peak: '+('PASS' if record['local_profile_pass'] else 'MISS; retain measured construction difference'),font=SMALL,fill='black')
 for col,(a,r,label) in enumerate(((im,render,'Exported 2048 GLB'),(photo,reference,'Native photograph'))):
  x0,y0,_,y1=r['bounds'];crop=Image.fromarray(a).crop((max(0,x0-150),max(0,y0-12),x0+150,y1+12));crop.thumbnail((840,390));canvas.paste(crop,(25+900*col,65));q=np.array(r['value_profile']);points=[(35+900*col+i/max(len(q)-1,1)*780,720-v*1.1) for i,v in enumerate(q)];d.line(points,fill=(140,55,25) if col==0 else (25,90,145),width=3)
  d.text((25+900*col,775),label+' FWHM %.1f%% of visible station'%(r['width_fraction']*100),font=FONT,fill='black');d.text((25+900*col,810),'P95 profile value %.1f / native span %d px'%(r['peak'],r['part_span_pixels']),font=SMALL,fill='black')
 import textwrap
 for i,line in enumerate(textwrap.wrap(record['limit'],155)):d.text((25,865+i*24),line,font=SMALL,fill='black')
 canvas.save(out/'paint-highlight-width.jpg',quality=94)
 # A separately rebuilt physical trial shows why the narrower local band was
 # rejected; it must also satisfy complete-part values under the same rig.
 trial_meta=json.loads((root/'reflection-trial/shots.json').read_text())['used_photo']
 assert trial_meta['sha256']==meta['sha256']
 for key in ('location','target','lens','roll','aspect','action','frame','layers','inspection_parts','hide_box'):assert trial_meta.get(key)==meta.get(key),(key,'mismatched trial camera or pose')
 trial=np.asarray(Image.open(root/'reflection-trial/used_photo.png').convert('RGB'))
 assert trial.shape==im.shape
 tr=profile(trial,x,ys.min(),ys.max()+1)
 from finish_report import acceptance
 from PIL import ImageFilter,ImageOps
 rows={}
 for role in ('paint_cover','molded_grip','handle_polymer'):
  name,polys,_,prefixes=REGIONS[role];part=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)])
  part=np.asarray(Image.fromarray(np.uint8(part)*255).filter(ImageFilter.MinFilter(3)))>0
  ref=np.asarray(Image.open(BASE/'build/white-balanced'/(name+'.jpg')).convert('RGB'));pm=polygon_mask((ref.shape[1],ref.shape[0]),polys)
  pm=np.asarray(Image.fromarray(np.uint8(pm)*255).filter(ImageFilter.MinFilter(3)))>0
  r,t=metrics(trial[part]),metrics(ref[pm]);rows[role]=dict(render=r,photo=t,acceptance=acceptance(r,t))
 record['rejected_trial']=dict(profile=tr,whole_parts=rows,sha256=trial_meta['sha256'],limit='Earlier existing-fixture profile trial fails complete-part finish constraints. Its geometry and materials are identical to the retained rig.')
 (out/'paint-highlight-width.json').write_text(json.dumps(record,indent=2))
 canvas=Image.new('RGB',(1800,1050),'#e7e9e6');d=ImageDraw.Draw(canvas)
 d.text((25,15),'Cover reflection / retained rig, rejected physical trial and native photograph',font=FONT,fill='black')
 d.text((25,45),'Retained native width and peak: '+('PASS' if record['local_profile_pass'] else 'MISS'),font=SMALL,fill='black')
 for col,(a,r,label) in enumerate(((im,render,'Retained rig'),(trial,tr,'Rejected profile trial'),(photo,reference,'Native photograph'))):
  xx,y0,_,y1=r['bounds'];crop=Image.fromarray(a).crop((max(0,xx-150),max(0,y0-12),xx+150,y1+12));crop=ImageOps.contain(crop,(550,390));canvas.paste(crop,(25+600*col,80))
  q=np.array(r['value_profile']);d.line([(35+600*col+i/max(len(q)-1,1)*520,750-v) for i,v in enumerate(q)],fill=(30,80,120),width=3)
  d.text((25+600*col,795),label,font=FONT,fill='black');d.text((25+600*col,835),'FWHM %.1f%% / P95 %.1f'%(r['width_fraction']*100,r['peak']),font=SMALL,fill='black')
 failed=[name for name,row in rows.items() if not row['acceptance']['passed']]
 d.text((25,890),'Trial complete-part failures: '+(', '.join(failed) if failed else 'none; inspect local profile separately'),font=FONT,fill='black')
 for i,line in enumerate(textwrap.wrap(record['limit'],150)):d.text((25,940+i*25),line,font=SMALL,fill='black')
 canvas.save(out/'paint-highlight-trial.jpg',quality=94)
 print('PAINT HIGHLIGHT WIDTH',render['width_fraction'],reference['width_fraction'])
if __name__=='__main__':main()
