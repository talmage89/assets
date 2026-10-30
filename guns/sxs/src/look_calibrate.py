"""Fit review framing with the photograph's observed macro hemisphere fixed."""
import json,math,sys
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from look_matches import definitions,SHOTS
from kit.photo_match import project

def main():
 rows={}
 for name,row in definitions().items():
  # The free fit crossed to the muzzle side and hid the lever. Retain the
  # independently observed rearward/above view instead of accepting its RMS.
  location=np.array(row.get('fit_location',(3.0,.24,.62) if name=='look_side' else (.68,-.05,.36)))
  target=np.array(row.get('fit_target',(0,.235,0) if name=='look_side' else (0,.105,.025)));direction=target-location
  az=math.atan2(direction[1],direction[0]);el=math.atan2(direction[2],np.linalg.norm(direction[:2]))
  width=row['crop'][2]-row['crop'][0];height=row['crop'][3]-row['crop'][1]
  points=np.array([r['world'] for r in row['landmarks']]);observed=np.array([r['pixel'] for r in row['landmarks']])-row['crop'][:2]
  p=np.array([*location,math.log(row.get('fit_lens',82 if name=='look_side' else 60)),0.0]);initial=p.copy()
  def full(p):return np.array([az,el,*p[:3],p[3],p[4]])
  def residual(p):
   uv,depth,_=project(full(p),points,width,height)
   return np.r_[(uv-observed).ravel()/width,(p[3]-initial[3])*.015,p[4]*.02,np.minimum(depth-.02,0)*10]
  damping=.001
  for _ in range(150):
   r=residual(p);jac=np.stack([(residual(p+np.eye(5)[i]*1e-5)-r)/1e-5 for i in range(5)],axis=1)
   matrix=jac.T@jac;delta=np.linalg.solve(matrix+damping*np.diag(np.maximum(np.diag(matrix),1e-5)),-jac.T@r)
   candidate=p+delta;candidate[3]=np.clip(candidate[3],math.log(30),math.log(180));candidate[4]=np.clip(candidate[4],-.20,.20)
   if np.dot(residual(candidate),residual(candidate))<np.dot(r,r):p=candidate;damping=max(1e-9,damping*.4)
   else:damping=min(1e8,damping*5)
  uv,depth,forward=project(full(p),points,width,height)
  result=dict(photo=row['photo'],crop=row['crop'],title=row['title'],landmarks_world_m=points.tolist(),
   measured_pixels=observed.tolist(),projected_pixels=uv.tolist(),residual_rms_pixels=float(np.sqrt(np.mean(np.sum((uv-observed)**2,axis=1)))),
   shot=dict(location=p[:3].tolist(),target=(p[:3]+forward).tolist(),lens=math.exp(p[3]),roll=float(p[4]),aspect=width/height,exposure=-.15),
   lens_status='View-locked rearward/above comparison; accepted different makers have different wood/controls; not a form solve')
  result['shot'].update(look_light=SHOTS[name]['look_light'],light_target=SHOTS[name].get('light_target',(0,.22,0)),action='Idle',frame=0,background='transparent')
  for key in ('look_world','look_world_color','look_paper','look_paper_x','look_reflection_card','look_light_colors','look_strips','look_flags'):
   if key in SHOTS[name]:result['shot'][key]=SHOTS[name][key]
  rows[name]=result
 (BASE/'build/look-cameras.json').write_text(json.dumps(rows,indent=2))
 print({n:r['residual_rms_pixels'] for n,r in rows.items()})
if __name__=='__main__':main()
