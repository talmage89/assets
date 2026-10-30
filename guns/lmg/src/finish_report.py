"""Controlled round-1/round-2 finish pairs and explicit tolerance results."""
import hashlib,json,sys,textwrap
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageOps
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from look_review import FONT,SMALL,REGIONS,polygon_mask,mask_crop
from image_masks import raster
from final_review import sheet,rgb

# Evidence-based exceptions belong here, not in the acceptance calculation.
NOTES={
 'paint_receiver':'The replacement photo has clipped black paint in its lower tail. Zero-valued targets are reported in encoded levels, with no relative-error claim. Its railed cover is outside the measured receiver.',
 'paint_cover':'Accepted original cover construction differs from the photographed front cylindrical pressing. Both complete visible cover distributions include those reflection families.',
 'molded_handguard':'The replacement photograph has the ribbed matte finish we build; the former glossy checkered molding is not a valid finish target.',
 'molded_stock':'Concrete neutral is an estimate. The original accepted stock contour differs; the camera now observes the same flank.',
 'molded_box':'Paper in a cast shadow is an estimated neutral; the broad white backdrop is clipped. The camera now observes the same flank and end.',
}

def acceptance(r,p):
 q=np.array(r['value_p10_p50_p90']);t=np.array(p['value_p10_p50_p90']);h=np.array(r['brightest_decile_rgb']);th=np.array(p['brightest_decile_rgb'])
 # A percentage of zero is undefined, so retain the absolute encoded error.
 errors=np.divide(q-t,t,out=np.full(3,np.nan),where=t>0)
 allowed=np.array((.15,.10,.15));passed=np.where(t>0,abs(q-t)<=allowed*t,abs(q-t)<=1)
 he=(h-th)/np.maximum(th,1);hc=h/max(h.max(),1);pc=th/max(th.max(),1)
 return dict(value_relative_errors=[None if not np.isfinite(v) else float(v) for v in errors],value_absolute_errors=(q-t).tolist(),value_pass=passed.tolist(),highlight_rgb_relative_errors=he.tolist(),highlight_value_relative_error=float((h.max()-th.max())/max(th.max(),1)),highlight_chroma_absolute_error=(hc-pc).tolist(),highlight_pass=bool(np.all(abs(he)<=.10)),passed=bool(passed.all() and np.all(abs(he)<=.10)))

def part_crop(root,geometry,role):
 photo,polys,shot,prefixes=REGIONS[role];meta=json.loads((root/'photos/shots.json').read_text())[shot];image=np.asarray(rgb(root/'photos'/(shot+'.png')));h,w=image.shape[:2]
 geo=np.load(geometry/(shot+'.npz'));assert str(geo['sha256'])==meta['sha256'];ids,_=raster(geo,meta,w,h);m=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)])
 return image,m

def main():
 root=BASE/'renders/final';out=root/'look-review/comparison';out.mkdir(parents=True,exist_ok=True)
 before=json.loads((root/'before/look-review/finish-values.json').read_text());after=json.loads((root/'look-review/finish-values.json').read_text());rows={};entries=[]
 for role,a in after.items():
  b=before[role];assert a['photo_source']==b['photo_source'] and a['photo_polygons']==b['photo_polygons'];test=acceptance(a['render'],a['photo']);rows[role]=dict(before=b['render'],after=a['render'],photo=a['photo'],acceptance=test,note=NOTES.get(role,''),before_sha256=b['sha256'],after_sha256=a['sha256'])
  canvas=Image.new('RGB',(1800,1860),'#e7e9e6');d=ImageDraw.Draw(canvas)
  d.text((25,12),role+' / controlled before and after / same camera, lights and white-balanced photo',font=FONT,fill='black')
  canvas.paste(Image.open(root/'before/look-review'/(role+'-histograms.jpg')),(0,45));canvas.paste(Image.open(root/'look-review'/(role+'-histograms.jpg')),(0,900))
  status='WITHIN REQUESTED TOLERANCES' if test['passed'] else 'MISSES REMAIN: '+', '.join([label for label,ok in zip(('P10','median','P90'),test['value_pass']) if not ok]+([] if test['highlight_pass'] else ['highlight RGB']))
  d.text((25,1760),status,font=FONT,fill=(35,90,45) if test['passed'] else (150,45,20))
  for i,line in enumerate(textwrap.wrap(NOTES.get(role,'Whole visible parts; accepted ammunition materials remain unchanged.'),155)):d.text((25,1795+i*23),line,font=SMALL,fill='black')
  path=out/(role+'-before-after.jpg');canvas.save(path,quality=94);entries.append((role,path))
 (out/'finish-comparison.json').write_text(json.dumps(rows,indent=2));sheet(entries,out/'all-finishes.jpg',columns=3,cell=(600,620))
 # These crops keep the full observed part, with no favorable tiny sample.
 surface=root/'surface-pairs';surface.mkdir(exist_ok=True);surfaces=[]
 for role in ('paint_cover','barrel_phosphate','molded_handguard','molded_grip','molded_stock','molded_box','handle_polymer'):
  im,m=part_crop(root,BASE/'build/image-geometry',role);name,polys,_,_=REGIONS[role];photo=np.asarray(Image.open(BASE/'build/white-balanced'/(name+'.jpg')).convert('RGB'));pm=polygon_mask((photo.shape[1],photo.shape[0]),polys)
  canvas=Image.new('RGB',(1800,950),'#e7e9e6');d=ImageDraw.Draw(canvas);d.text((25,15),role+' / shipped surface and photographic construction, whole-part close pair',font=FONT,fill='black')
  for col,(a,p) in enumerate(((im,m),(photo,pm))):
   crop=mask_crop(a,p);canvas.paste(crop,(25+900*col,65));ys,xs=np.nonzero(p);cx=int(np.median(xs));cy=int(np.median(ys));bounds=(max(0,cx-220),max(0,cy-140),min(a.shape[1],cx+220),min(a.shape[0],cy+140));detail=Image.fromarray(a).crop(bounds);detail=ImageOps.contain(detail,(840,390),Image.Resampling.LANCZOS);canvas.paste(detail,(25+900*col,480));d.text((25+900*col,900),('Actual 2048 GLB' if col==0 else 'White-balanced native photograph')+' / center crop, no sharpening',font=SMALL,fill='black')
  path=surface/(role+'-surface.jpg');canvas.save(path,quality=94);surfaces.append((role,path))
 # Heat/construction cross-check uses the sharp existing oblique photograph.
 sheet([('Exported GLB / chamber and handle',root/'beauty/barrel_handle.png'),('Used phosphate / oblique photo, estimated paper neutral',BASE/'build/white-balanced/used_oblique.jpg'),('Exported GLB / gas parts',root/'beauty/front_sight.png')],surface/'phosphate-heat-construction.jpg',columns=1,cell=(1600,950))
 surfaces.append(('Phosphate / heat and dry grain',surface/'phosphate-heat-construction.jpg'));sheet(surfaces,surface/'all-surfaces.jpg',columns=2,cell=(900,500))
 lines=['| Finish | Before V10/50/90 | After V10/50/90 | Photo V10/50/90 | Result |','| --- | --- | --- | --- | --- |']
 for role,row in rows.items():
  f=lambda v:'/'.join(str(round(x)) for x in v)
  lines.append('| '+role+' | '+f(row['before']['value_p10_p50_p90'])+' | '+f(row['after']['value_p10_p50_p90'])+' | '+f(row['photo']['value_p10_p50_p90'])+' | '+('pass' if row['acceptance']['passed'] else 'miss')+' |')
 (out/'table.md').write_text('\n'.join(lines)+'\n')
 print('\n'.join(lines));print('FINISH TOLERANCES',sum(r['acceptance']['passed'] for r in rows.values()),'/',len(rows))
if __name__=='__main__':main()
