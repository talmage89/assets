"""Fit photographic cameras, retaining native residuals and view constraints.

Image pre-rotations only initialize the kit solver; the final camera is undone
analytically and checked independently in Blender. No mesh is changed.
"""
import json,math,sys,copy
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.photo_match import calibrate,project
from photo_matches import MATCHES

def fixed_view(source):
 """Keep the visually observed side of the part fixed while fitting framing.

 Unconstrained angle optimization can conceal a form discrepancy by orbiting
 around it. Only camera translation, focal estimate and roll vary here.
 """
 source=copy.deepcopy(source);x,y,x1,y1=source['crop'];w=x1-x;h=y1-y
 points=np.array([r['world'] for r in source['landmarks']]);target=np.array([r['pixel'] for r in source['landmarks']])-[x,y]
 weights=np.sqrt(np.array([r['weight'] for r in source['landmarks']]))
 direction=np.array(source['target'])-source['location'];direction/=np.linalg.norm(direction)
 az=math.atan2(direction[1],direction[0]);el=math.asin(direction[2]);initial=np.array([*source['location'],math.log(120),0.0]);p=initial.copy()
 def projection(q):return project(np.array([az,el,*q[:3],q[3],q[4]]),points,w,h)
 def residual(q):
  uv,depth,_=projection(q)
  return np.r_[((uv-target)*weights[:,None]/w).ravel(),(q[3]-initial[3])*.02,np.minimum(depth-.03,0)*10]
 damping=.001
 for _ in range(160):
  r=residual(p);jac=np.stack([(residual(p+np.eye(5)[k]*1e-5)-r)/1e-5 for k in range(5)],axis=1);mat=jac.T@jac
  delta=np.linalg.solve(mat+damping*np.diag(np.maximum(np.diag(mat),1e-5)),-jac.T@r)
  q=p+delta;q[3]=np.clip(q[3],math.log(45),math.log(300))
  if residual(q)@residual(q)<r@r:
   p=q;damping=max(1e-9,damping*.4)
   if np.linalg.norm(delta)<1e-8:break
  else:damping=min(1e8,damping*5)
 uv,depth,_=projection(p);assert min(depth)>0
 source['lens_bounds_mm']=(45,300)
 row=calibrate(source);row['shot'].update(location=p[:3].tolist(),target=(p[:3]+direction).tolist(),lens=math.exp(p[3]),roll=float(p[4]),aspect=w/h)
 row.update(projected_pixels=uv.tolist(),measured_pixels=target.tolist(),view_direction_cosine=1.0,
  view_constraint='Visually observed view direction locked; translation/lens/roll fit only',residuals_pixels=np.linalg.norm(uv-target,axis=1).tolist(),residual_rms_pixels=float(np.sqrt(np.mean(np.sum((uv-target)**2,axis=1)))))
 return row

def main():
 rows={}
 for name,source in MATCHES.items():
  if source.get('locked_view'):
   row=fixed_view(source);rows[name]=row;print(name,'LOCKED VIEW RMS',round(row['residual_rms_pixels'],2),flush=True);continue
  x,y,x1,y1=source['crop'];w=x1-x;h=y1-y;candidates=[]
  for pre_angle in [0,-math.pi/2,math.pi/2,math.pi]:
   c=math.cos(pre_angle);s=math.sin(pre_angle);rw=round(abs(w*c)+abs(h*s));rh=round(abs(w*s)+abs(h*c))
   for shift in (0,.12,-.12):
    trial=copy.deepcopy(source);trial['crop']=(0,0,rw,rh);trial['location']=list(trial['location']);trial['location'][1]+=shift
    for p in trial['landmarks']:
     xx,yy=p['pixel'];u=xx-x-w/2;v=yy-y-h/2;p['pixel']=(c*u-s*v+rw/2,s*u+c*v+rh/2)
    row=calibrate(trial);shot=row['shot'];shot['roll']-=pre_angle;shot['lens']*=rw/w
    row.update(photo=source['photo'],crop=source['crop'],title=source['title'])
    row['measured_pixels']=[[p['pixel'][0]-x,p['pixel'][1]-y] for p in source['landmarks']]
    direction=np.array(shot['target'])-shot['location'];az=math.atan2(direction[1],direction[0]);el=math.atan2(direction[2],np.linalg.norm(direction[:2]))
    par=[az,el,*shot['location'],math.log(shot['lens']),shot['roll']]
    uv,_,_=project(np.array(par),np.array(row['landmarks_world_m']),w,h)
    row['projected_pixels']=uv.tolist();error=np.linalg.norm(uv-row['measured_pixels'],axis=1)
    row['residuals_pixels']=error.tolist();row['residual_rms_pixels']=float(np.sqrt(np.mean(error**2)));shot['aspect']=w/h
    nominal=np.array(source['target'])-source['location'];nominal/=np.linalg.norm(nominal);actual=direction/np.linalg.norm(direction)
    agreement=float(nominal@actual)
    row['view_direction_cosine']=agreement;row['view_constraint']='within 64 degrees of observed view hemisphere; visually reviewed separately'
    if agreement>.44:candidates.append(row)
  if not candidates:raise AssertionError((name,'no camera in observed hemisphere'))
  row=min(candidates,key=lambda r:r['residual_rms_pixels']);rows[name]=row
  print(name,'RMS',round(row['residual_rms_pixels'],2),'lens',round(row['shot']['lens'],1),'view cosine',round(row['view_direction_cosine'],3),flush=True)
 (Path(__file__).resolve().parents[1]/'build/cameras.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
