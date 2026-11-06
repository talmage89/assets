"""Balanced photo / matched-light export measurements on explicit surface ROIs.

ROI values are display-referred sRGB; albedo is independently listed in the
source finishes. Median luminance and chroma do not prove geometric agreement.
"""
import json,argparse
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.photo_match import project
from PIL import Image,ImageOps,ImageDraw

def sample(path,roi):
 a=np.asarray(Image.open(path).convert('RGB')).astype(float)/255;h,w=a.shape[:2]
 if isinstance(roi[0],(list,tuple)):
  mask=Image.new('L',(w,h));ImageDraw.Draw(mask).polygon([(round(x*w),round(y*h)) for x,y in roi],fill=255);r=a[np.asarray(mask)>0]
 else:
  x0,y0,x1,y1=roi;r=a[round(y0*h):round(y1*h),round(x0*w):round(x1*w)].reshape(-1,3)
 assert len(r)>2,(path,roi);rgb=np.median(r,axis=0);return dict(roi_normalized=roi,median_srgb_rgb=rgb.tolist(),median_luminance=float(np.median(r@np.array([.2126,.7152,.0722]))),sampled_pixels=len(r))

def projected_roi(d,points):
 s=d['shot'];direction=np.asarray(s['target'])-s['location'];direction/=np.linalg.norm(direction);p=[np.arctan2(direction[1],direction[0]),np.arcsin(direction[2]),*s['location'],np.log(s['lens']),s.get('roll',0)];w=d['crop'][2]-d['crop'][0];h=d['crop'][3]-d['crop'][1]
 pixels,_,_=project(np.asarray(p),np.asarray(points),w,h);return (pixels/np.array([w,h])).tolist()
PHYSICAL={
 'used-shelter':[(1.76825,.58,1.5),(1.76825,.60,1.5),(1.76825,.60,2.0),(1.76825,.58,2.0)],
 'used-meter':[(-.03,-.080,1.3702),(.03,-.080,1.3702),(.03,-.080,1.3722),(-.03,-.080,1.3722)],
 'used-news':[(-.2175,-.2415,.55),(-.2055,-.2415,.55),(-.2055,-.2415,.82),(-.2175,-.2415,.82)]}
# Filled with meaningful surface crops after the matches have been inspected.
ROIS={
 'used-shelter':dict(photo=(.129,.25,.136,.42),render=(.129,.25,.136,.42),surface='rear frame; different original design, compare value not exact hue'),
 'used-meter':dict(photo=(.35,.477,.65,.489),render=(.35,.48,.65,.496),surface='unpainted bezel; exclude blue housing as an alloy target'),
 'used-news':dict(photo=(.325,.405,.345,.505),render=(.135,.48,.15,.64),surface='red front door stile, exposed painted steel; excludes side skin and rivets'),
 'used-sign':dict(photo=(.20,.11,.28,.16),render=(.20,.11,.28,.16),surface='white sheeting away from text and border')}
ap=argparse.ArgumentParser();ap.add_argument('--renders',type=Path,default=Path('renders/match'));ap.add_argument('--out',type=Path,default=Path('build/color-review.json'));args=ap.parse_args();
cal=json.loads(Path('build/photo-calibration.json').read_text());rows={};folder=Path('build/value-crops');folder.mkdir(parents=True,exist_ok=True)
for name,d in cal.items():
 image=Image.open(d['photo']).convert('RGB');crop=d['crop'];image=image.crop(tuple(crop));p=folder/(name+'.png');image.save(p)
 r=ROIS[name]
 if name in PHYSICAL:r['render']=projected_roi(d,PHYSICAL[name])
 photo=sample(p,r['photo']);render=sample(args.renders/(name+'.png'),r['render']);rows[name]=dict(surface=r['surface'],neutral=d['white_balance'],light=d['shot']['light'],photo=photo,render=render,luminance_delta=render['median_luminance']-photo['median_luminance'],landmark_rms_pixels=d['residual_rms_pixels'])
args.out.write_text(json.dumps(dict(scope=__doc__,pairs=rows),indent=2));print(json.dumps(rows,indent=2))

canvas=Image.new('RGB',(1000,2600),(229,232,225));draw=ImageDraw.Draw(canvas)
for j,(name,row) in enumerate(rows.items()):
 for col,(path,roi) in enumerate([(args.renders/(name+'.png'),ROIS[name]['render']),(folder/(name+'.png'),ROIS[name]['photo'])]):
  im=Image.open(path).convert('RGB');d=ImageDraw.Draw(im);w,h=im.size;
  if isinstance(roi[0],(list,tuple)):d.line([(round(x*w),round(y*h)) for x,y in roi]+[(round(roi[0][0]*w),round(roi[0][1]*h))],fill='red',width=5)
  else:d.rectangle(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(roi)),outline='red',width=5)
  im.thumbnail((490,580));canvas.paste(im,(col*500+(500-im.width)//2,j*650+45));draw.text((col*500+10,j*650+10),name+(' render' if col==0 else ' balanced photo'),fill='black')
canvas.save(folder/'roi-audit.jpg',quality=94)
