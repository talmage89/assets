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
 'barrel_phosphate':'Whole exposed barrel bay in front of the gas block. The previous assembly mask included shadowed protected barrel, chamber and collar surfaces absent from the photo outline; full-assembly diagnostics remain in finish-values.json and the separate coverage pair.',
 'paint_cover':'Accepted original cover construction differs from the photographed front cylindrical pressing. The native local reflection profile is measured separately; its surface pair and rebuilt physical trial retain the actual pass/miss measurements.',
 'molded_handguard':'The replacement photograph has the ribbed matte finish we build; the former glossy checkered molding is not a valid finish target.',
 'molded_stock':'Concrete neutral is an estimate. The original accepted stock contour differs; the camera now observes the same flank.',
 'steel_links':'Primary target is a studio photograph of a blackened-steel link, balanced on unclipped paper. The original field-belt diagnostic remains beside this comparison; its clipped range highlights are not a studio-light target.',
 'brass':'Accepted cartridge material is unchanged. The retained field photo clips bright brass highlights; this is an explicit diagnostic, not an assertion of a studio finish match.',
 'copper_green_tip':'Accepted copper jacket and green tip remain unchanged. The retained field photo clips its bright copper highlights; highlight clipping limits interpretation of an exact lighting fit.',
 'molded_box':'Paper in a cast shadow is an estimated neutral; the broad white backdrop is clipped. The camera now observes the same flank and end.',
}

def acceptance(r,p):
 q=np.array(r['value_p10_p50_p90']);t=np.array(p['value_p10_p50_p90']);h=np.array(r['brightest_decile_rgb']);th=np.array(p['brightest_decile_rgb'])
 # A percentage of zero is undefined, so retain the absolute encoded error.
 errors=np.divide(q-t,t,out=np.full(3,np.nan),where=t>0)
 allowed=np.array((.15,.10,.15));passed=abs(q-t)<=allowed*t
 he=(h-th)/np.maximum(th,1);hc=h/max(h.max(),1);pc=th/max(th.max(),1);ce=(hc-pc)/np.maximum(pc,1e-6)
 highlight_ok=bool(np.all(abs(he)<=.10) and np.all(abs(ce)<=.10))
 return dict(value_relative_errors=[None if not np.isfinite(v) else float(v) for v in errors],value_absolute_errors=(q-t).tolist(),value_pass=passed.tolist(),highlight_rgb_relative_errors=he.tolist(),highlight_value_relative_error=float((h.max()-th.max())/max(th.max(),1)),highlight_chroma_absolute_error=(hc-pc).tolist(),highlight_chroma_relative_errors=ce.tolist(),highlight_chroma_pass=bool(np.all(abs(ce)<=.10)),highlight_pass=highlight_ok,passed=bool(passed.all() and highlight_ok))

def part_crop(root,geometry,role):
 photo,polys,shot,prefixes=REGIONS[role];meta=json.loads((root/'photos/shots.json').read_text())[shot];image=np.asarray(rgb(root/'photos'/(shot+'.png')));h,w=image.shape[:2]
 geo=np.load(geometry/(shot+'.npz'));assert str(geo['sha256'])==meta['sha256'];ids,_=raster(geo,meta,w,h);m=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)])
 return image,m

def main():
 root=BASE/'renders/final';geometry=BASE/(sys.argv[sys.argv.index('--geometry')+1] if '--geometry' in sys.argv else 'build/image-geometry');out=root/'look-review/comparison';out.mkdir(parents=True,exist_ok=True)
 before=json.loads((root/'before/look-review/finish-values.json').read_text());after=json.loads((root/'look-review/finish-values.json').read_text());rows={};entries=[]
 for role,a in after.items():
  b=before[role];assert a['photo_source']==b['photo_source'] and a['photo_polygons']==b['photo_polygons'];test=acceptance(a['render'],a['photo']);rows[role]=dict(before=b['render'],after=a['render'],photo=a['photo'],acceptance=test,note=NOTES.get(role,''),before_sha256=b['sha256'],after_sha256=a['sha256'])
  canvas=Image.new('RGB',(1800,1980),'#e7e9e6');d=ImageDraw.Draw(canvas)
  d.text((25,12),role+' / controlled before and after / same camera, lights and white-balanced photo',font=FONT,fill='black')
  canvas.paste(Image.open(root/'before/look-review'/(role+'-histograms.jpg')),(0,45));canvas.paste(Image.open(root/'look-review'/(role+'-histograms.jpg')),(0,900))
  status='WHOLE-PART VALUE / HIGHLIGHT TOLERANCES PASS' if test['passed'] else 'MISSES REMAIN: '+', '.join([label for label,ok in zip(('P10','median','P90'),test['value_pass']) if not ok]+([] if test['highlight_pass'] else ['highlight RGB']))
  d.text((25,1760),status,font=FONT,fill=(35,90,45) if test['passed'] else (150,45,20))
  for i,line in enumerate(textwrap.wrap(NOTES.get(role,'Whole visible parts; accepted ammunition materials remain unchanged.'),155)):d.text((25,1795+i*23),line,font=SMALL,fill='black')
  if role=='barrel_phosphate':
   rows[role]['unmatched_assembly_before']=b['full_assembly_diagnostic'];rows[role]['unmatched_assembly_after']=a['full_assembly_diagnostic']
   d.text((25,1890),'Unmatched full-assembly V10/50/90: before '+str(np.round(b['full_assembly_diagnostic']['value_p10_p50_p90'],1).tolist())+'; after '+str(np.round(a['full_assembly_diagnostic']['value_p10_p50_p90'],1).tolist()),font=SMALL,fill='black')
  path=out/(role+'-before-after.jpg');canvas.save(path,quality=94);entries.append((role,path))
 (out/'finish-comparison.json').write_text(json.dumps(rows,indent=2))
 # Keep the original field-link observation alongside the new studio target.
 fb=json.loads((root/'before/look-review/legacy-field-links.json').read_text())
 fa=json.loads((root/'look-review/legacy-field-links.json').read_text())
 field=dict(before=fb['render'],after=fa['render'],photo=fa['photo'],acceptance=acceptance(fa['render'],fa['photo']),before_sha256=fb['sha256'],after_sha256=fa['sha256'],note='One shared field rig constrains brass, copper/green tips and links together. The studio-link observation remains the primary finish pair.')
 (out/'field-links-comparison.json').write_text(json.dumps(field,indent=2))
 canvas=Image.new('RGB',(1800,1980),'#e7e9e6');d=ImageDraw.Draw(canvas)
 d.text((25,12),'Links / retained original field frame / controlled before and after',font=FONT,fill='black')
 canvas.paste(Image.open(root/'before/look-review/legacy-field-links-histograms.jpg'),(0,45))
 canvas.paste(Image.open(root/'look-review/legacy-field-links-histograms.jpg'),(0,900))
 d.text((25,1760),'WITHIN REQUESTED TOLERANCES' if field['acceptance']['passed'] else 'MISSES REMAIN: see field-links-comparison.json',font=FONT,fill='black')
 for i,line in enumerate(textwrap.wrap(field['note'],155)):d.text((25,1800+i*25),line,font=SMALL,fill='black')
 path=out/'field-links-before-after.jpg';canvas.save(path,quality=94);entries.append(('Links / original field frame',path))
 sheet(entries,out/'all-finishes.jpg',columns=3,cell=(600,620))
 # These crops keep the full observed part, with no favorable tiny sample.
 surface=root/'surface-pairs';surface.mkdir(exist_ok=True);surfaces=[]
 for role in ('paint_cover','barrel_phosphate','molded_handguard','molded_grip','molded_stock','molded_box','handle_polymer'):
  im,m=part_crop(root,geometry,role);name,polys,_,_=REGIONS[role];photo=np.asarray(Image.open(BASE/'build/white-balanced'/(name+'.jpg')).convert('RGB'));pm=polygon_mask((photo.shape[1],photo.shape[0]),polys)
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
