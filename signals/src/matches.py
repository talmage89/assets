"""Measured camera fits and shadow-matched procedural sun/sky pairs.

The photograph's neutral is documented before any surface/LED measurements.
Photos stay in refs; comparison composites are never asset texels.
"""
import argparse,json,sys,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import calibrate,compose
from plan import *
from layout import SITES

def balance():
 rows=[]
 for name,rect,neutral in [('gadsden-2025',(1540,1960,1730,2050),'sunlit gray asphalt between vehicles'),('maryland-2006',(1350,1330,1450,1420),'bare asphalt patch, provisional neutral'),('span-2009',(1570,1042,1586,1070),'shadowed stainless latch at right of red module; small provisional neutral')]:
  im=Image.open('refs/'+name+'.jpg').convert('RGB');a=np.asarray(im).astype(float)/255
  lin=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);x0,y0,x1,y1=rect;med=np.median(lin[y0:y1,x0:x1].reshape(-1,3),axis=0);target=float(np.exp(np.mean(np.log(np.maximum(med,1e-8)))));gain=target/np.maximum(med,1e-6)
  # The small latch is imperfect; retain/record actual gains for scrutiny.
  q=np.clip(lin*gain,0,1);q=np.where(q<=.0031308,12.92*q,1.055*q**(1/2.4)-.055)
  Image.fromarray(np.uint8(np.round(q*255))).save('refs/'+name+'-balanced.jpg',quality=97)
  annotated=im.copy();ImageDraw.Draw(annotated).rectangle(rect,outline='magenta',width=5);annotated.save('refs/'+name+'-neutral.jpg',quality=95)
  rows.append(dict(photo=name,neutral=neutral,roi=rect,median_linear_rgb=med.tolist(),gain=gain.tolist(),limitation='Uncalibrated JPEG and provisional in-frame neutral; no physical albedo or candela claim'))
 Path('build/reference-balance.json').write_text(json.dumps(rows,indent=2))

def solve():
 balance()
 measured={seed:json.loads(Path(f'build/Signals-{seed}.json').read_text())['lenses'] for seed in SITES}
 def face(seed,head,row):return next(r for r in measured[seed] if r['parent']==head and r['name'].startswith(head+f'__S{row:02d}_'))
 def lm(world,pixel):return dict(world=world,pixel=pixel)
 m=[lm(face(202,'Mast_1__Head0',row)['center_world_m'],pixel) for row,pixel in enumerate([(1416,1116),(1417,1148),(1418,1180)])]
 f=face(202,'Mast_1__Head0',0)
 m += [lm(f['left_world_m'],(1402,1116)),lm(f['right_world_m'],(1430,1116))]
 mast=dict(title='Straight mast / sidewalk support framing / 202',photo='refs/gadsden-2025-balanced.jpg',crop=(500,850,2600,2250),location=(-65,-6.4,1.65),target=(5,-2,6),lens=80,camera_height_m=(1.65,.4),lens_bounds_mm=(25,160),landmarks=m)
 # Same installed support in a wider driver's frame, independently fitted.
 driver=dict(mast);driver.update(title='Driver approach / straight mast / 202',crop=(0,0,3264,2448))
 def center(t,row):return face(204,'SpanWire__Head'+('0' if t==.53 else '1'),row)['center_world_m']
 span=dict(title='Span approach / sag and cable construction / 204',photo='refs/maryland-2006-balanced.jpg',crop=(850,350,2300,1700),location=(14,-46,1.7),target=(0,0,4.5),lens=42,camera_height_m=(1.7,.4),lens_bounds_mm=(22,100),landmarks=[lm(center(.53,0),(1632,531)),lm(center(.53,1),(1633,551)),lm(center(.53,2),(1634,571)),lm(center(.66,0),(1794,549)),lm(center(.66,1),(1795,570)),lm(center(.66,2),(1796,589))])
 close=dict(title='Sunlit maintained LED head / 204',photo='refs/span-2009-balanced.jpg',crop=(1120,450,1700,1950),location=(.6,-20,1.65),target=center(.53,1),lens=300,camera_height_m=(1.65,.3),lens_bounds_mm=(150,900),landmarks=[lm(center(.53,0),(1375,907)),lm(center(.53,1),(1373,1283)),lm(center(.53,2),(1371,1658)),lm(face(204,'SpanWire__Head0',0)['left_world_m'],(1220,907)),lm(face(204,'SpanWire__Head0',0)['right_world_m'],(1530,907))])
 extra=[]
 for seed,photo,pixels,crop in [(201,'span-2009',[(1375,907),(1373,1283),(1371,1658)],(1120,680,1700,1900)),(203,'span-2009',[(1375,907),(1373,1283),(1371,1658)],(1120,680,1700,1900))]:
  f=face(seed,'Mast_0__Head0',0);x,y,z=f['center_world_m']
  definition=dict(title=('Yellow case / galvanized arterial / 201' if seed==201 else 'Yellow case / bronze boulevard / 203'),photo='refs/'+photo+'-balanced.jpg',crop=crop,location=(x+.2,y-20,1.65),target=(x,y,z-.37),lens=300,camera_height_m=(1.65,.3),lens_bounds_mm=(150,900),landmarks=[lm(face(seed,'Mast_0__Head0',row)['center_world_m'],pixel) for row,pixel in enumerate(pixels)]+[lm(f['left_world_m'],(1220,907)),lm(f['right_world_m'],(1530,907))])
  extra.append(('head_'+str(seed),definition,seed,dict(sun_direction=(-.40,.90,-.68),sun_elevation=35,sun_rotation=-66,sky_strength=.14)))
 result={}
 for name,data,seed,light in [('mast_sidewalk',mast,202,dict(sun_direction=(.65,-.45,-1),sun_elevation=47,sun_rotation=145,sky_strength=.12)),('driver_approach',driver,202,dict(sun_direction=(.65,-.45,-1),sun_elevation=47,sun_rotation=145,sky_strength=.12)),('span',span,204,dict(sun_direction=(.8,.4,-1),sun_elevation=41,sun_rotation=206,sky_strength=.18)),('heads_close',close,204,dict(sun_direction=(-.40,.90,-.68),sun_elevation=35,sun_rotation=-66,sky_strength=.14))]+extra:
  # Calibration expects the landmarks in full-image pixels, then applies crop.
  crop=data['crop'];im=Image.open(data['photo']);data=dict(data,crop=(0,0,*im.size));r=calibrate(data)
  if seed==201:
   candidates=[r]
   for pos in [(-6,35,1.65),(0,35,1.65),(9,40,1.65),(-15,55,1.65),(15,65,1.65)]:
    trial=dict(data,location=pos,lens=60)
    candidates.append(calibrate(trial))
   r=min(candidates,key=lambda x:x['residual_rms_pixels'])
  # Preserve full-image projection when presenting a native crop.
  if name=='mast_sidewalk':
   from sidewalk_fit import fit
   r=fit(r)
  full_rms=r['residual_rms_pixels'];w=crop[2]-crop[0];h=crop[3]-crop[1];cx=(crop[0]+crop[2])/2;cy=(crop[1]+crop[3])/2
  if crop!=(0,0,*im.size):
   # Render the full calibrated frame, then crop both image panels identically.
   r['presentation_crop']=crop
  r['seed']=seed;r['shot'].update(light);r['shot']['aspect']=im.width/im.height;r['shot']['exposure']=-.5
  if name in ('mast_sidewalk','driver_approach'):r['shot']['phase']='red';r['shot']['equipment_roots']=['Mast_0','Mast_1']
  r['landmark_source']='Actual lens apex/diameter vertices measured in build.py; independent raw/reimport check in checks.json'
  r['scope']='Original exported equipment in measured photo framing. Sun estimated from visor/ground shadows; original product and street geometry differ. Projection residual is not material or construction proof.'
  result[name]=r;print('PHOTO FIT',name,round(r['residual_rms_pixels'],3),'px',r['shot']['lens'],'mm')
 Path('build/cameras.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--compose',action='store_true');p.add_argument('--renders',default='renders/matches');a=p.parse_args()
 if a.compose:
  data=json.loads(Path('build/cameras.json').read_text());folder=Path(a.renders);cropped=folder/'crops';cropped.mkdir(exist_ok=True)
  for name,r in data.items():
   im=Image.open(folder/(name+'.png'));area=r.get('presentation_crop',r['crop']);factor=im.width/(r['crop'][2]-r['crop'][0])
   im.crop(tuple(round(v*factor) for v in area)).save(cropped/(name+'.png'))
   r['crop']=area
   for key in ('measured_pixels','projected_pixels'):r[key]=[[x-area[0],y-area[1]] for x,y in r[key]]
  Path('build/cameras-cropped.json').write_text(json.dumps(data,indent=2));compose('build/cameras-cropped.json',cropped,folder)
 else:solve()
