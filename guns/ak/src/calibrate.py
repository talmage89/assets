"""Asset camera policy: constrain side/rear frames, reuse kit projection/verify.

The free kit fit remains appropriate for independent receiver and oblique
anchors. A nominal side/axial photograph may not invent yaw or elevation to
lower its residual: those directions are held at the observed view. Only
camera translation and roll are fitted, at a long fixed lens. Residuals are
retained honestly; this is framing, not shape acceptance.
"""
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.photo_match import calibrate,project
from photo_matches import MATCHES

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

def main():
 results={n:(constrained(m) if m.get('fixed_view') else calibrate(m)) for n,m in MATCHES.items()}
 out=Path(__file__).resolve().parents[1]/'build/cameras.json';out.write_text(json.dumps(results,indent=2))
 for n,r in results.items():print(n,round(r['residual_rms_pixels'],2),'px',r.get('framing_policy','free oblique fit'))
if __name__=='__main__':main()
