"""Review-space measurements; photographs never enter a material generator.

Y' is Rec.709 luma of encoded sRGB, not an inferred paint/brick albedo.
The sunny camera exposure is stated in calibration and held for every patch.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.photo_match import project


def stats(im,polygon):
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(polygon,fill=255)
 rgb=np.asarray(im.convert('RGB'))[np.asarray(mask)>0]/255.
 linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
 weights=np.array([.2126,.7152,.0722])
 return dict(encoded_y=float(np.mean(rgb@weights)),linear_y=float(np.mean(linear@weights)),pixels=len(rgb))


def measure(folder=Path('renders/ranch/matches'),out=Path('build/ranch/values.json')):
 meta=json.loads(Path('build/ranch/house-12.json').read_text());m=meta['blocks'][0]
 cameras=json.loads(Path('build/ranch/cameras.json').read_text());results={}
 # Front bedroom pier below the sill; highest patch is above the head in
 # eave shade. Roof patch is the unobstructed main front slope.
 world=dict(brick=[(m['x0']+x,m['y0']-.072,z) for x,z in [(1.15,.85),(1.95,.85),(1.95,1.15),(1.15,1.15)]],
  shade=[(m['x0']+x,m['y0']-.072,z) for x,z in [(1.15,2.78),(1.95,2.78),(1.95,2.92),(1.15,2.92)]],
  roof=[(m['x0']+x,m['y0']+y,m['eave']+m['pitch']*y) for x,y in [(3.3,1.3),(4.3,1.3),(4.3,2.2),(3.3,2.2)]])
 def nc(x,y):return (434+x*2641/1600,1938+y*2641/1600)
 rois=dict(ranch_sun_1960=dict(brick=(1015,740,1070,760),shade=(1015,682,1070,728),roof=(1225,425,1330,480)),
  ranch_sun_oblique=dict(brick=(*nc(700,315),*nc(745,350)),shade=(*nc(690,255),*nc(750,290)),roof=(*nc(750,165),*nc(830,200))))
 for name,patches in rois.items():
  data=cameras[name];s=data['shot'];im=Image.open(folder/(name+'.png'));photo=Image.open(data['photo']);f=np.array(s['target'])-s['location'];f/=np.linalg.norm(f)
  parameters=[math.atan2(f[1],f[0]),math.atan2(f[2],np.linalg.norm(f[:2])),*s['location'],math.log(s['lens']),s['roll']]
  comparisons={}
  for role,box in patches.items():
   x0,y0,x1,y1=box;reference=stats(photo,[(x0,y0),(x1,y0),(x1,y1),(x0,y1)])
   polygon=project(parameters,np.array(world[role]),im.width,im.height)[0].tolist();source=stats(im,polygon)
   comparisons[role]=dict(photo_roi_pixels=box,source_world_polygon_m=world[role],source_polygon_pixels=polygon,photo=reference,source=source,delta_encoded_y=source['encoded_y']-reference['encoded_y'])
  results[name]=dict(lighting=json.loads((folder/'provenance.json').read_text())[name]['lighting'],exposure_ev=s['exposure'],camera_rms_px=data['residual_rms_pixels'],patches=comparisons)
  for role,comparison in comparisons.items():assert abs(comparison['delta_encoded_y'])<=.03,(name,role,comparison)
 # Recover course period from the actual generated 512 map, then convert
 # pixel spacing using the UV metric chart. This includes texel quantization.
 im=np.asarray(Image.open('build/ranch/materials/red/T_RanchBrick_BaseColor.png').convert('RGB'))/255
 curve=(im@np.array([.2126,.7152,.0722])).mean(axis=1)
 # Weighted centers of complete pale beds avoid picking arbitrary maxima
 # within a noisy mortar plateau. Exclude the two clipped tile-edge beds.
 indices=np.flatnonzero(curve>.60)
 groups=np.split(indices,np.flatnonzero(np.diff(indices)>1)+1)
 beds=[float(np.average(g,weights=curve[g]-.59)) for g in groups if len(g)>1 and g[0]>0 and g[-1]<511]
 spans=[(beds[i+3]-beds[i])*1.2192/512 for i in range(len(beds)-3)]
 assert len(spans)>=8 and max(abs(v-.2032) for v in spans)<.003,(beds,spans)
 result=dict(passed=True,scope='Display comparison of the stated render folder, not inverse-rendered physical albedo',render_folder=str(folder),comparisons=results,
  three_course_map_measurement_m=dict(mean=float(np.mean(spans)),minimum=min(spans),maximum=max(spans),samples=len(spans)))
 out.write_text(json.dumps(result,indent=2));print('RANCH_VALUES', {name:{role:round(patch['delta_encoded_y'],5) for role,patch in row['patches'].items()} for name,row in results.items()}, 'three courses:',round(float(np.mean(spans)),7),'m')
 return result


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--folder',type=Path,default=Path('renders/ranch/matches'));p.add_argument('--out',type=Path,default=Path('build/ranch/values.json'));a=p.parse_args();measure(a.folder,a.out)
