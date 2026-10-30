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
 """Fit shared landmarks inside the visually observed 20-degree view cone.

 A fixed 150 mm review lens avoids focal/distance ambiguity in small crops.
 The same view hemisphere is independently inspected; native residual vectors
 and a photo-outline overlay remain visible even when a sparse fit is small.
 """
 source=copy.deepcopy(source);x,y,x1,y1=source['crop'];w=x1-x;h=y1-y
 points=np.array([r['world'] for r in source['landmarks']]);target=np.array([r['pixel'] for r in source['landmarks']])-[x,y]
 weights=np.sqrt(np.array([r['weight'] for r in source['landmarks']]))
 direction=np.array(source['target'])-source['location'];direction/=np.linalg.norm(direction)
 az=math.atan2(direction[1],direction[0]);el=math.asin(direction[2]);initial=np.array([az,el,*source['location'],source.get('roll',0.0)]);p=initial.copy()
 def projection(q):return project(np.array([*q[:5],math.log(150),q[5]]),points,w,h)
 def residual(q):
  uv,depth,_=projection(q)
  return np.r_[((uv-target)*weights[:,None]/w).ravel(),(projection(q)[2]-direction)*.01,np.minimum(depth-.03,0)*10]
 damping=.001
 for _ in range(220):
  r=residual(p);jac=np.stack([(residual(p+np.eye(6)[k]*1e-5)-r)/1e-5 for k in range(6)],axis=1);mat=jac.T@jac
  delta=np.linalg.solve(mat+damping*np.diag(np.maximum(np.diag(mat),1e-5)),-jac.T@r)
  q=p+delta;q[1]=np.clip(q[1],-1.54,1.54)
  for boundary in range(16):
   if direction@projection(q)[2]>=math.cos(math.radians(20)):break
   q[:2]=p[:2]+(q[:2]-p[:2])*.5
  if residual(q)@residual(q)<r@r:
   p=q;damping=max(1e-9,damping*.4)
   if np.linalg.norm(delta)<1e-8:break
  else:damping=min(1e8,damping*5)
 uv,depth,actual=projection(p);assert min(depth)>0
 row=calibrate(source);row['shot'].update(location=p[2:5].tolist(),target=(p[2:5]+actual).tolist(),lens=150,roll=float(p[5]),aspect=w/h)
 row.update(projected_pixels=uv.tolist(),measured_pixels=target.tolist(),view_direction_cosine=float(direction@actual),
  view_constraint='View direction within 20 degrees of visually observed view; 150 mm review lens (EXIF unavailable)',residuals_pixels=np.linalg.norm(uv-target,axis=1).tolist(),residual_rms_pixels=float(np.sqrt(np.mean(np.sum((uv-target)**2,axis=1)))))
 # The photographic open view looks from the muzzle side onto the exterior
 # flats. A chamber-facing fit would be the wrong side despite a small RMS.
 if source['title'].startswith('Open /'):
  from photo_matches import opened
  rear=np.array(opened((0,115,44)))*.001
  bore=np.array([0,math.cos(math.pi/6),-math.sin(math.pi/6)])
  row['barrel_front_hemisphere_m']=float((p[2:5]-rear)@bore)
  assert row['barrel_front_hemisphere_m']>.02,'Open camera looks into chambers instead of at exterior flats'
 return row

def append_head_landmarks(rows):
 """Review-only endpoints at 0.10 mm rise; no influence on camera solve."""
 base=Path(__file__).resolve().parents[1]
 stats=json.loads((base/'build/serialization.json').read_text())
 head=stats['form_gauges']['head_round5'];row=rows['action_top']
 from photo_matches import px
 observations={(-1,'outer'):(150,716),(1,'outer'):(345,711),(-1,'inner'):(222,761),(1,'inner'):(255,759)}
 extras=[]
 for record in head['return_endpoints']:
  label=('right' if record['side']>0 else 'left')+' return '+record['end']
  extras.append((label,record['point_mm'],px('plain-2',observations[record['side'],record['end']])))
 for y,pixel in [(103,(232,763)),(108,(233,738)),(114.5,(235,709))]:
  point=min(head['centerline']['points_mm'],key=lambda p:abs(p[1]-y))
  extras.append((f'centerline Y{y:g}',point,px('plain-2',pixel)))
 row['camera_fit_rms_pixels']=row['residual_rms_pixels'];row['camera_fit_landmark_count']=len(row['projected_pixels'])
 row['review_only_landmark_scope']='Four rear-return ends at 0.10 mm rise above adjacent head; three approximate centerline stations; excluded from camera fit'
 shot=row['shot'];direction=np.array(shot['target'])-shot['location'];direction/=np.linalg.norm(direction)
 parameters=np.array([math.atan2(direction[1],direction[0]),math.asin(direction[2]),*shot['location'],math.log(shot['lens']),shot['roll']])
 width=row['crop'][2]-row['crop'][0];height=row['crop'][3]-row['crop'][1]
 world=np.array([point for name,point,pixel in extras])*.001
 projected,_,_=project(parameters,world,width,height)
 for (label,point,pixel),uv,wp in zip(extras,projected,world):
  measured=(np.array(pixel)-row['crop'][:2]).tolist()
  row['landmark_names'].append(label);row['landmarks_world_m'].append(wp.tolist());row['projected_pixels'].append(uv.tolist());row['measured_pixels'].append(measured)
 row['residuals_pixels']=np.linalg.norm(np.array(row['projected_pixels'])-row['measured_pixels'],axis=1).tolist()
 row['residual_rms_pixels']=float(np.sqrt(np.mean(np.square(row['residuals_pixels']))))

def main():
 rows={}
 for name,source in MATCHES.items():
  if source.get('locked_view'):
   row=fixed_view(source);row['landmark_names']=[r.get('name','landmark '+str(i+1)) for i,r in enumerate(source['landmarks'])];rows[name]=row;print(name,'BOUNDED VIEW RMS',round(row['residual_rms_pixels'],2),flush=True);continue
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
 append_head_landmarks(rows)
 (Path(__file__).resolve().parents[1]/'build/cameras.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
