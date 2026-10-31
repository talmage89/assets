"""Shared measured-landmark units and calibrated camera/pose configuration.

Each gun owns its photographic landmarks and action selection. Photographs
are read only by the comparison pipeline, never by geometry or material code.
"""
import json,math
import numpy as np
from pathlib import Path
from kit.photo_match import calibrate,project

def L(world_mm,pixel,weight=1):
 return dict(world=tuple(x*.001 for x in world_mm),pixel=pixel,weight=weight)

def camera_shots(path):
 return {name:dict(row['shot'],background='transparent',
         aspect=(row['crop'][2]-row['crop'][0])/(row['crop'][3]-row['crop'][1]))
         for name,row in json.loads(Path(path).read_text()).items()}


# Fixed observed view; source geometry and diagnostic camera residuals stay explicit.
def constrained(match):
 width,height=match['crop'][2]-match['crop'][0],match['crop'][3]-match['crop'][1]
 points=np.array([r['world'] for r in match['landmarks']])
 targets=np.array([r['pixel'] for r in match['landmarks']])-np.array(match['crop'][:2])
 weights=np.sqrt([r.get('weight',1) for r in match['landmarks']])
 camera=np.array(match['location']);d=np.array(match['target'])-camera
 az=math.atan2(d[1],d[0]);el=math.atan2(d[2],np.linalg.norm(d[:2]))
 p=np.array([az,el,*camera,math.log(300),0.]);active=[2,3,4,6]
 def residual(q):
  uv,depth,_=project(q,points,width,height)
  return np.r_[((uv-targets)*weights[:,None]/width).ravel(),np.minimum(depth-.05,0)*10]
 damping=.001
 for _ in range(100):
  r=residual(p);cols=[]
  for k in active:
   q=p.copy();q[k]+=1e-5;cols.append((residual(q)-r)/1e-5)
  jac=np.stack(cols,axis=1);matrix=jac.T@jac
  delta=np.linalg.solve(matrix+damping*np.diag(np.maximum(np.diag(matrix),1e-6)),-jac.T@r)
  q=p.copy();q[active]+=delta;q[6]=np.clip(q[6],-.35,.35)
  if np.linalg.norm(residual(q))<np.linalg.norm(r):
   p=q;damping=max(1e-9,damping*.4)
   if np.linalg.norm(delta)<1e-8:break
  else:damping=min(1e8,damping*5)
 uv,depth,forward=project(p,points,width,height);errors=np.linalg.norm(uv-targets,axis=1)
 result=calibrate(match)
 result.update(shot=dict(result['shot'],location=p[2:5].tolist(),target=(p[2:5]+forward).tolist(),lens=300.,roll=float(p[6])),
  residual_rms_pixels=float(np.sqrt(np.mean(errors**2))),residuals_pixels=errors.tolist(),
  projected_pixels=uv.tolist(),lens_status='fixed 300 mm comparison lens; observed side/axial direction held',
  framing_policy='yaw/elevation fixed; translation and roll fitted; residual is not form approval')
 return result
