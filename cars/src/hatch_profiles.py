"""Perspective profile evidence; photography is read only for review.

Camera landmarks are wheel geometry only. Held-out outline picks never change
camera or asset vertices. Deviations are screen-axis distances converted at the
body center plane, not an asserted recovered three-dimensional surface error.
"""
import json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from kit.photo_match import project
from hatch_review import ASSET,PROFILE_PICKS,font,save,rgb

REGIONS={'hood lead':'hood','hood middle':'hood','cowl':'hood','windshield':'windshield header',
 'roof front':'windshield header','roof peak':'roof','roof aft':'roof','spoiler':'spoiler',
 'backlight':'backlight','tail':'gate','nose upper':'nose','nose bumper':'front bumper',
 'chin':'front bumper','tail upper':'gate','tail bumper':'rear bumper','tail lower':'rear bumper'}

def parameters(shot):
 c=np.array(shot['location']);f=np.array(shot['target'])-c;f/=np.linalg.norm(f)
 return np.array([math.atan2(f[1],f[0]),math.asin(f[2]),*c,math.log(shot['lens']),shot.get('roll',0)])

def profiles(out,cameras):
 out=Path(out);records={}
 for make,picks in PROFILE_PICKS.items():
  camera=cameras[make+'_side'];photo=Image.open(camera['photo']).convert('RGBA').crop(camera['crop'])
  render=Image.open(out/(make+'_side_clay.png')).convert('RGBA').resize(photo.size,Image.Resampling.LANCZOS)
  mask=np.array(render.getchannel('A'))>200;factor=2100/1200
  p=parameters(camera['shot']);w,h=photo.size
  # Local center-plane scale; both vertical and longitudinal derivatives are
  # retained. Perspective is applied by Blender, never a silhouette warp.
  base=np.array([[0,0,.75],[0,.001,.75],[0,0,.751]])
  uv,_,_=project(p,base,w,h);ppmy=abs(uv[1,0]-uv[0,0])/.001;ppmz=abs(uv[2,1]-uv[0,1])/.001
  measure=[]
  for label,x,y in picks['top']:
   xx,yy=round(x*factor),round(y*factor);ys=np.nonzero(np.any(mask[:,xx-1:xx+2],axis=1))[0]
   if len(ys):measure.append(dict(feature=label,region=REGIONS[label],signed_deviation_m=(yy-int(ys[0]))/ppmz,photo_pixel=[xx,yy],render_pixel=[xx,int(ys[0])],axis='height'))
  for label,x,y,front in picks['ends']:
   xx,yy=round(x*factor),round(y*factor);xs=np.nonzero(np.any(mask[yy-1:yy+2,:],axis=0))[0]
   if len(xs):
    rx=int(xs[0] if front else xs[-1]);measure.append(dict(feature=label,region=REGIONS[label],signed_deviation_m=(xx-rx if front else rx-xx)/ppmy,photo_pixel=[xx,yy],render_pixel=[rx,yy],axis='outward'))
  tint=Image.new('RGBA',photo.size,(20,112,205,0));tint.putalpha(render.getchannel('A').point(lambda v:round(v*.38)));photo.alpha_composite(tint)
  im=photo.convert('RGB');d=ImageDraw.Draw(im)
  d.text((25,25),'H120 / '+make.upper()+' / PERSPECTIVE-MATCHED PROFILE',font=font(29),fill=(25,55,75))
  d.text((25,70),f"Wheel-anchor RMS {camera['residual_rms_pixels']:.2f} px / estimated {camera['shot']['lens']:.1f} mm lens / outline held out",font=font(23),fill=(25,55,75))
  for row in measure:
   q,r=row['photo_pixel'],row['render_pixel'];d.line((*q,*r),fill=(210,60,25),width=3);d.ellipse((q[0]-4,q[1]-4,q[0]+4,q[1]+4),fill=(210,60,25))
  save(im,out/('side-perspective-'+make+'.jpg'))
  regions={n:max(abs(r['signed_deviation_m']) for r in measure if r['region']==n) for n in dict.fromkeys(r['region'] for r in measure)}
  records[make]=dict(method='Blender perspective silhouette through independently fitted wheel-anchor camera; no outline warp',camera_rms_px=camera['residual_rms_pixels'],lens_mm=camera['shot']['lens'],center_plane_pixels_per_m=dict(longitudinal=ppmy,vertical=ppmz),pick_uncertainty_m=4*factor/ppmz,measurements=measure,region_worst_absolute_m=regions,worst_absolute_deviation_m=max(regions.values()),limits='Four coplanar chassis anchors; lens prior makes depth approximate. Millimeters are projected center-plane equivalents. No body landmark enters calibration.')
  old=out/('side-overlay-'+make+'.jpg')
  if old.exists():
   a,b=Image.open(old).convert('RGB'),im
   a.thumbnail((1200,900));b.thumbnail((1200,900));pair=Image.new('RGB',(2400,980),(229,231,232));pair.paste(a,(0,70));pair.paste(b,(1200,70));draw=ImageDraw.Draw(pair)
   draw.text((20,20),'OLD ORTHOGRAPHIC REGISTRATION',font=font(25),fill=(25,55,75));draw.text((1220,20),'MATCHED PERSPECTIVE',font=font(25),fill=(25,55,75));save(pair,out/('side-methods-'+make+'.jpg'))
  baseline=ASSET/'renders/hatch-round1-overlays'/('side-overlay-'+make+'.jpg')
  if baseline.exists():
   a,b=Image.open(baseline).convert('RGB'),im.copy()
   a.thumbnail((1200,900));b.thumbnail((1200,900));pair=Image.new('RGB',(2400,980),(229,231,232));pair.paste(a,(0,70));pair.paste(b,(1200,70));draw=ImageDraw.Draw(pair)
   draw.text((20,20),'ROUND 1 / ORIGINAL ORTHOGRAPHIC OVERLAY',font=font(24),fill=(25,55,75));draw.text((1220,20),'ROUND 2 / MATCHED PERSPECTIVE',font=font(24),fill=(25,55,75));save(pair,out/('side-rounds-'+make+'.jpg'))
 (out/'side-perspective.json').write_text(json.dumps(records,indent=2))
 return records
