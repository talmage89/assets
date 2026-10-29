"""Reuse kit fitting with image pre-rotations for the open view.

Undo that rotation analytically in the final camera; the original photo/crop
and native pixel count remain unchanged. Blender independently checks all final
projected points through kit.photo_match.verify.
"""
import json,math,sys,copy
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.photo_match import calibrate,project
from photo_matches import MATCHES
def main():
 rows={}
 for name,source in MATCHES.items():
  spec=copy.deepcopy(source)
  if name in ('open','open_loaded'):
   candidates=[]
   x,y,x1,y1=spec['crop'];w=x1-x;h=y1-y
   for pre_angle in [0,-math.pi/4,-math.pi/2,math.pi/4,math.pi/2,math.pi]:
    c=math.cos(pre_angle);s=math.sin(pre_angle);rw=round(abs(w*c)+abs(h*s));rh=round(abs(w*s)+abs(h*c))
    for location in [(.30,-.15,.25),(.15,-.40,.25),(-.20,-.3,.25),(-.3,.25,.25),(.3,.3,.25)]:
     trial=copy.deepcopy(spec);trial['location']=location;trial['target']=(0,.12,.055);trial['lens']=65;trial['lens_bounds_mm']=(20,180)
     trial['camera_height_m']=source.get('camera_height_m') if name=='open' else None;trial['crop']=(0,0,rw,rh)
     for p in trial['landmarks']:
      xx,yy=p['pixel'];u=xx-x-w/2;v=yy-y-h/2;p['pixel']=(c*u-s*v+rw/2,s*u+c*v+rh/2)
     row=calibrate(trial);row['shot']['roll']-=pre_angle;row['shot']['lens']*=rw/w
     candidates.append(row)
   row=min(candidates,key=lambda r:r['residual_rms_pixels'])
  else:row=calibrate(spec)
  if name in ('open','open_loaded'):
   shot=row['shot']
   row.update(photo=source['photo'],crop=source['crop'],title=source['title'])
   row['measured_pixels']=[[p['pixel'][0]-x,p['pixel'][1]-y] for p in source['landmarks']]
   direction=np.array(shot['target'])-shot['location'];az=math.atan2(direction[1],direction[0]);el=math.atan2(direction[2],np.linalg.norm(direction[:2]))
   par=[az,el,*shot['location'],math.log(shot['lens']),shot['roll']]
   uv,_,_=project(np.array(par),np.array(row['landmarks_world_m']),w,h)
   row['projected_pixels']=uv.tolist();error=np.linalg.norm(uv-row['measured_pixels'],axis=1)
   row['residuals_pixels']=error.tolist();row['residual_rms_pixels']=float(np.sqrt(np.mean(error**2)))
   shot['aspect']=w/h
  rows[name]=row;print(name,'RMS',row['residual_rms_pixels'],'lens',row['shot']['lens'],'roll',math.degrees(row['shot']['roll']))
 (Path(__file__).resolve().parents[1]/'build/cameras.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
