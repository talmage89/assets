"""Sidewalk-constrained camera refinement using the kit's pinhole projection.

The standing location/height are explicit priors from the authored site, not
measurements inferred from a photograph. Landmark residuals remain measured.
"""
import math
import numpy as np
from kit.photo_match import project

def fit(result,fixed_y=-6.4,height=1.7524,fixed_x=None,surface_z=.1524,lens_min=25):
 r=result;shot=r['shot'];camera=np.array(shot['location']);forward=np.array(shot['target'])-camera
 p=np.array([math.atan2(forward[1],forward[0]),math.atan2(forward[2],np.linalg.norm(forward[:2])),*camera,math.log(shot['lens']),shot['roll']])
 p[3]=fixed_y if fixed_x is None else p[3];p[2]=fixed_x if fixed_x is not None else p[2];p[4]=height;width=r['crop'][2]-r['crop'][0];h=r['crop'][3]-r['crop'][1];points=np.array(r['landmarks_world_m']);target=np.array(r['measured_pixels']);indices=[0,1,2 if fixed_x is None else 3,5,6];initial=p.copy()
 def residual(q):
  uv,depth,_=project(q,points,width,h)
  return np.r_[((uv-target)/width).ravel(),(q[5]-initial[5])*.012,q[6]*.02,np.minimum(depth-.02,0)*10]
 damp=.001
 for _ in range(120):
  error=residual(p);cols=[]
  for k in indices:
   q=p.copy();step=1e-5*max(1,abs(p[k]));q[k]+=step;cols.append((residual(q)-error)/step)
  jac=np.stack(cols,axis=1);a=jac.T@jac;step=np.linalg.solve(a+damp*np.diag(np.maximum(np.diag(a),1e-6)),-jac.T@error);q=p.copy();q[indices]+=step;q[5]=np.clip(q[5],math.log(lens_min),math.log(160))
  if residual(q)@residual(q)<error@error:p=q;damp=max(1e-9,damp*.4)
  else:damp=min(1e8,damp*5)
 uv,depth,forward=project(p,points,width,h);errors=np.linalg.norm(uv-target,axis=1)
 shot.update(location=p[2:5].tolist(),target=(p[2:5]+forward).tolist(),lens=math.exp(p[5]),roll=float(p[6]));r.update(projected_pixels=uv.tolist(),residuals_pixels=errors.tolist(),residual_rms_pixels=float(np.sqrt(np.mean(errors**2))),site_constraint=dict(fixed_axis='Y' if fixed_x is None else 'X',fixed_coordinate_m=fixed_y if fixed_x is None else fixed_x,eye_z_m=height,standing_surface_z_m=surface_z,eye_height_m=height-surface_z))
 return r
