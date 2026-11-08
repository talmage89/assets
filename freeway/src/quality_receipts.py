"""Measure exposed edge burial, lane actor spacing and hero display range."""
import argparse,json,math
from pathlib import Path
import numpy as np
from PIL import Image

def traffic():
 result={}
 for seed in (101,202):
  row=json.loads(Path(f'build/scene-{seed}.json').read_text());actors=row['traffic']['placements'];roles={}
  for a in actors:roles[a['role']]=roles.get(a['role'],0)+1
  # Record actual nearest plan distance in each role. Cars in adjacent lanes
  # are allowed alongside each other; a full traffic simulation is not claimed.
  main=[a for a in actors if a['role']=='mainline'];overlaps=[]
  for i,a in enumerate(main):
   for b in main[i+1:]:
    d=np.asarray(a['location'][:2])-b['location'][:2];yaw=math.radians(a['yaw']);forward=np.array([math.sin(yaw),-math.cos(yaw)]);lateral=np.array([math.cos(yaw),math.sin(yaw)])
    if abs(d@lateral)<1.7 and abs(d@forward)<4.8:overlaps.append([a['name'],b['name']])
  assert not overlaps,(seed,overlaps)
  result[str(seed)]=dict(actors=len(actors),roles=roles,bodies=sorted(set(a['body'] for a in actors)),colors=sorted(set(a['color'] for a in actors)),mainline_speed_mps=[min(a['speed_mps'] for a in main),max(a['speed_mps'] for a in main)],mainline_center_pairs_under_4_8m=len(overlaps),scope='Seeded static snapshot, not an animated traffic simulation or swept vehicle certification')
 Path('build/traffic-audit.json').write_text(json.dumps(result,indent=2));return result

def tones(folder):
 result={}
 for seed in (101,202):
  p=Path(folder)/str(seed)/'hero.png';a=np.asarray(Image.open(p).convert('RGB'),float)/255;y=a@np.array([.2126,.7152,.0722]);h,w=y.shape
  # Hero-specific object samples exclude the sky; they are display values,
  # deliberately not claims about spectral albedo or calibrated photometry.
  regions=({'pavement':[.15,.62,.55,.66],'shade':[.84,.41,.90,.47]} if seed==101 else
           {'pavement':[.45,.72,.80,.97],'shade':[.90,.50,.98,.55]})
  samples={}
  for name,(x0,y0,x1,y1) in regions.items():
   box=y[round(h*y0):round(h*y1),round(w*x0):round(w*x1)];samples[name]=np.quantile(box,[.05,.5,.95]).tolist()
  result[str(seed)]=dict(p01_p50_p99=np.quantile(y,[.01,.5,.99]).tolist(),rgb_clipped_fraction=float((a>=.99).mean()),object_display_luma=samples,normalized_sample_regions=regions,scope='Display luminance including scene illumination; no albedo/engineering calibration')
 Path('build/tones-look.json').write_text(json.dumps(result,indent=2));return result
def albedos():
 import sys
 sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
 from kit.image_io import srgb_to_linear
 files={'bridge_concrete':'textures/ship/T_FreewayConcrete_BaseColor.png','ground_concrete':'../ground/textures/ship/T_Concrete_BaseColor.png','asphalt':'../ground/textures/ship/T_Asphalt_BaseColor.png','zinc':'textures/ship/T_FreewayZinc_BaseColor.png'}
 result={}
 for name,path in files.items():
  a=srgb_to_linear(np.asarray(Image.open(path).convert('RGB'),np.float32)/255);luma=a@np.array([.2126,.7152,.0722]);result[name]=dict(linear_RGB_median=np.median(a.reshape(-1,3),axis=0).tolist(),linear_luma_p05_p50_p95=np.quantile(luma,[.05,.5,.95]).tolist())
 result['scope']='Actual BaseColor map values before vertex age and illumination. Zinc is metallic reflectance, not diffuse concrete albedo.'
 Path('build/albedos.json').write_text(json.dumps(result,indent=2));return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--folder',default='renders/lookdev');a=p.parse_args();print(traffic());print(tones(a.folder));print(albedos())
