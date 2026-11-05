"""Neutral-balanced period photos and kit landmark-calibrated comparison pairs."""
import argparse,json,sys,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import calibrate,compose
from plan import *
def balance():
 rows=[]
 for name,rect in [('trenton-2014',(1450,1900,1550,1970)),('maryland-2006',(1350,1330,1450,1420))]:
  im=Image.open('refs/'+name+'.jpg').convert('RGB');a=np.asarray(im).astype(float)/255
  lin=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
  x0,y0,x1,y1=rect;med=np.median(lin[y0:y1,x0:x1].reshape(-1,3),axis=0);target=float(np.exp(np.mean(np.log(np.maximum(med,1e-8)))));gain=target/med
  q=np.clip(lin*gain,0,1);q=np.where(q<=.0031308,12.92*q,1.055*q**(1/2.4)-.055)
  Image.fromarray(np.uint8(np.round(q*255))).save('refs/'+name+'-balanced.jpg',quality=96)
  annotation=im.copy();ImageDraw.Draw(annotation).rectangle(rect,outline='magenta',width=6);annotation.thumbnail((1400,1400));annotation.save('refs/'+name+'-neutral.jpg')
  rows.append(dict(photo=name,neutral='Provisional neutral: bare asphalt in frame; weathering/camera response make this an estimate',roi=rect,median_linear_rgb=med.tolist(),gain=gain.tolist()))
 Path('build/reference-balance.json').write_text(json.dumps(rows,indent=2))
def solve():
 balance()
 def lm(world,pixel):return dict(world=world,pixel=pixel)
 z=GRADE+ARM_Z;dist=POLE_X-LANE;hz=z+(dist-.2735)*.03492+.55
 trenton=dict(title='2014 New Jersey / far mast-arm construction',photo='refs/trenton-2014-balanced.jpg',crop=(0,0,3264,2448),location=(8,-25,1.7),target=(POLE_X,POLE_Y,3),lens=40,camera_height_m=(1.7,.35),lens_bounds_mm=(25,100),landmarks=[
  lm((POLE_X,POLE_Y,GRADE+.2735),(2538,1575)),
  lm((POLE_X,POLE_Y,GRADE+POLE_TOP),(2524,920)),
  lm((POLE_X-.2735,POLE_Y,z),(2510,1035)),
  lm((POLE_X-9.144,POLE_Y,z+(9.144-.2735)*.03492),(1970,925)),
  lm((LANE,POLE_Y-.42,hz-.390),(2269,945)),
  lm((LANE,POLE_Y-.42,hz-1.130),(2269,1004)),
 ])
 a=np.array((-(FACE+4.2),-(CORE+4),0.));b=-a
 def center(t,row):
  p=a+(b-a)*t;p[2]=7.72-4*.26*t*(1-t)-.20-.390-row*.370;return p.tolist()
 maryland=dict(title='2006 Maryland / span-wire approach',photo='refs/maryland-2006-balanced.jpg',crop=(0,0,2592,1944),location=(14,-46,1.7),target=(0,0,4.5),lens=42,camera_height_m=(1.7,.4),lens_bounds_mm=(22,100),landmarks=[
  lm(center(.53,0),(1632,531)),lm(center(.53,1),(1633,551)),lm(center(.53,2),(1634,571)),
  lm(center(.62,0),(1794,549)),lm(center(.62,1),(1795,570)),lm(center(.62,2),(1796,589))
 ])
 result={}
 for name,data,seed in [('trenton',trenton,202),('maryland',maryland,204)]:
  r=calibrate(data);r['seed']=seed;r['shot']['aspect']=data['crop'][2]/data['crop'][3];r['shot']['overcast']=False
  r['scope']='Nominal 12-inch lens/shaft landmarks matched to an original layout, not a survey of the photographed street. Different state support styles remain visible.'
  result[name]=r
  print('PHOTO FIT',name,round(r['residual_rms_pixels'],2),'pixels',round(r['shot']['lens'],2),'mm',r['shot']['location'])
 Path('build/cameras.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--compose',action='store_true');a=p.parse_args()
 if a.compose:
  # The whole-frame fits are retained. Crop photo and render by exactly the
  # same pinhole image rectangle, to inspect hardware without a scene survey.
  data=json.loads(Path('build/cameras.json').read_text());out=Path('renders/matches/crops');out.mkdir(parents=True,exist_ok=True)
  crops={'trenton':(1850,800,2700,1660),'maryland':(1370,460,1900,670)}
  for name,r in data.items():
   area=crops[name];im=Image.open(Path('renders/matches')/(name+'.png'))
   scale=im.width/(r['crop'][2]-r['crop'][0])
   im.crop(tuple(round(v*scale) for v in area)).save(out/(name+'.png'))
   for key in ('measured_pixels','projected_pixels'):
    r[key]=[[x-area[0],y-area[1]] for x,y in r[key]]
   r['crop']=area
  Path('build/cameras-crops.json').write_text(json.dumps(data,indent=2))
  compose('build/cameras-crops.json',out,'renders/matches')
 else:solve()
