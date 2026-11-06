"""Appearance values in documented, neutral-balanced photo/render rectangles.

These are display-image comparisons, not inverse albedo or photometry. Clipped
photo channels and original product/geography differences remain in the report.
"""
from pathlib import Path
import json,colorsys
import numpy as np
from PIL import Image,ImageDraw

def sample(path,rect,render=False):
 im=Image.open(path).convert('RGB');area=list(rect)
 if render:
  meta=json.loads(Path(path).with_suffix('.json').read_text());crop=meta.get('render_crop');f=meta.get('render_scale',1)
  if crop:area=[round((v-crop[i%2])*f) for i,v in enumerate(rect)]
 a=np.asarray(im.crop(area),dtype=float)/255;y=a@np.array([.2126,.7152,.0722]);p15,p85=np.quantile(y,[.15,.85]);flat=a.reshape(-1,3);rgb=np.median(flat,axis=0);hsv=colorsys.rgb_to_hsv(*rgb)
 return dict(file=str(path),photo_frame_roi=rect,actual_roi=area,display_RGB=rgb.tolist(),display_HSV=[hsv[0]*360,hsv[1],hsv[2]],display_Yprime=float(np.median(a@np.array([.2126,.7152,.0722]))),clipped_red_fraction=float((flat[:,0]>=.99).mean()),Yprime_p10_p90=np.quantile(y,[.1,.9]).tolist(),coverage_below_96_percent_p85=float((y<.96*p85).mean()),contrast_p85_p15=float((p85-p15)/max(p85,1e-9)))

def run():
 probes=json.loads(Path('renders/matches/pavement.json').read_text()).get('surface_probes',[])
 assert len(probes)==3 and all(not p.get('sun_occluded') for p in probes) and all('asphalt' in p['material'].lower() or 'tire-polished' in p['material'].lower() for p in probes),('Rejected non-asphalt comparison samples',probes)
 before=Path('../build/signals-finals-before');out=Path('renders/final-values');out.mkdir(exist_ok=True,parents=True)
 yellow=[]
 for label,rect in [('red_section_right_flat',(1538,800,1550,940)),('red_section_lower_right',(1508,1010,1530,1060)),('green_section_right_flat',(1500,1450,1525,1510))]:
  yellow.append(dict(surface=label,photo=sample('refs/span-2009-balanced.jpg',rect),before=sample(before/'renders/matches/head_201.png',rect,True) if (before/'renders/matches/head_201.png').exists() else None,after=sample('renders/matches/head_201.png',rect,True)))
 asphalt=[]
 for label,rect in [('near_travel_lane',(1200,1310,1330,1390)),('foreground_lane',(1065,1540,1195,1620)),('foreground_edge',(1265,1630,1395,1690))]:
  asphalt.append(dict(surface=label,photo=sample('refs/maryland-2006-balanced.jpg',rect),before=None,after=sample('renders/matches/pavement.png',rect,True)))
 for file,rects in [('refs/span-2009-balanced.jpg',[r['photo']['actual_roi'] for r in yellow]),('renders/matches/head_201.png',[r['after']['actual_roi'] for r in yellow]),('refs/maryland-2006-balanced.jpg',[r['photo']['actual_roi'] for r in asphalt]),('renders/matches/pavement.png',[r['after']['actual_roi'] for r in asphalt])]:
  im=Image.open(file).convert('RGB');d=ImageDraw.Draw(im)
  for i,rect in enumerate(rects):d.rectangle(rect,outline='magenta',width=2);d.text((rect[0],rect[1]-14),str(i+1),fill='magenta')
  im.save(out/(Path(file).stem+'-rois.jpg'),quality=96)
 data=dict(pavement_camera=json.loads(Path('build/pavement-camera.json').read_text()),yellow=yellow,asphalt=asphalt,pavement_surface_probes=json.loads(Path('renders/matches/pavement.json').read_text()).get('surface_probes'),neutral_balance=json.loads(Path('build/reference-balance.json').read_text()),scope='Matched camera/light display medians, hue in degrees. Red clipping in the close-head JPEG and field neutrals limit physical inference. Pavement uses a nominal curbside camera with estimated photo lighting, not an equipment-fit residual; original streets differ, so confirm actual asphalt hits and sun-path probes and judge the whole pair. The first inherited equipment camera hit sidewalk and was rejected; no asphalt-before statistic is claimed from it. Before material/image bytes are preserved outside clean targets.')
 Path('build/final-values.json').write_text(json.dumps(data,indent=2));print('VALUES',[(r['surface'],r['photo']['display_HSV'][0],r['before']['display_HSV'][0] if r['before'] else None,r['after']['display_HSV'][0]) for r in yellow])
if __name__=='__main__':run()
