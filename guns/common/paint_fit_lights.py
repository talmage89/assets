"""Fit only unchanged finishes and the neutral; paint is a held-out observation.

The linear unit-card responses are independently rendered. This fit never sees
receiver pixels, quantiles, spatial guards or highlights in its objective.
A fresh Cycles image, rather than this approximation, supplies final evidence.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
import OpenImageIO as oiio
import PyOpenColorIO as ocio
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from guns.common.paint_review import masks,reference,metrics,comparison
p=argparse.ArgumentParser();p.add_argument('member');p.add_argument('--basis',default='build/paint-light-response');p.add_argument('--restarts',type=int,default=5);p.add_argument('--samples',type=int,default=1200);p.add_argument('--out',default='build/paint-light-response/fitted.json');p.add_argument('--initial');p.add_argument('--mixed-light',action='store_true');a=p.parse_args()
base=ROOT/'guns'/a.member;folder=base/a.basis
bases=json.loads((folder/'bases.json').read_text());meta=json.loads((folder/'shots.json').read_text())
count=len(bases);color_count=4 if a.mixed_light else 2
upper=np.array([not b.get('world') and b['position'][2]>.25 for b in bases])
color_lo=np.tile((.5,.65),2) if a.mixed_light else np.array((.95,.95))
color_hi=np.tile((2.5,2.),2) if a.mixed_light else np.array((1.05,1.05))
def clamp(x):
 x[:count]=np.maximum(x[:count],0);x[count:]=np.clip(x[count:],color_lo,color_hi)
 return x
c=ocio.Config.CreateFromFile((folder/'ocio-path.txt').read_text());group=ocio.GroupTransform();group.appendTransform(ocio.LookTransform(src='Linear Rec.709',dst='Linear Rec.709',looks='AgX - Medium High Contrast'));group.appendTransform(ocio.DisplayViewTransform(src='Linear Rec.709',display='sRGB',view='AgX'));proc=c.getProcessor(group).getDefaultCPUProcessor()
rng=np.random.default_rng(39);results={};specs=json.loads((base/'src/paint_review.json').read_text())
for name,spec in specs.items():
 shot=spec['shot']
 if shot+'__0' not in meta:continue
 assert spec.get('anchors'),'A light cannot be fitted without independent finish anchors'
 s=meta[shot+'__0']
 def read(i):
  f=oiio.ImageInput.open(str(folder/(shot+'__'+str(i)+'.exr')));rgb=f.read_image();f.close();return rgb[:,:,:3]
 first=read(0);h,w=first.shape[:2];indices=[];regions=[]
 receiver_mask,_=masks(base,spec,s,w,h)
 for anchor in spec['anchors']:
  mask,_=masks(base,anchor,s,w,h);ii=np.flatnonzero(mask)
  assert not np.any(mask&receiver_mask),(anchor['role'],'paint pixels entered an independent light anchor')
  assert len(ii)>20,(anchor['role'],'empty or tiny projected anchor',len(ii))
  ii=rng.choice(ii,min(a.samples,len(ii)),replace=False);start=len(indices);indices.extend(ii.tolist())
  photo,pm=reference(base,anchor);target=metrics(photo[pm]);regions.append((anchor['role'],slice(start,len(indices)),target))
 data=np.stack([read(i).reshape(-1,3)[indices] for i in range(len(bases))],axis=-1).astype(np.float32)
 # Normalize numerical steps by the measured NONPAINT response. One solver
 # unit contributes about .02 linear radiance at its lit anchors, regardless
 # of a card's distance/area. This changes conditioning, never physical watts
 # or the objective, and avoids skipping useful sub-watt fills near a part.
 response=np.percentile(data.max(axis=1),95,axis=0)
 energy_scale=np.clip(.02/np.maximum(response,1e-6),1e-4,10000)
 data*=energy_scale
 gain=2**s.get('exposure',-.3)
 def predict(x):
  if a.mixed_light:
   rgb=(data[:,:,upper]@x[:count][upper])*np.r_[x[-4:-2],1]+(data[:,:,~upper]@x[:count][~upper])*np.r_[x[-2:],1]
  else:rgb=(data@x[:count])*np.r_[x[-2:],1]
  rgb=np.ascontiguousarray(rgb*gain,dtype=np.float32);proc.applyRGB(rgb);return np.clip(rgb*255,0,255)
 def objective(x,report=False):
  rgb=predict(x);res=[];rows={}
  for role,sl,t in regions:
   ar=rgb[sl];v=ar.max(1);lum=ar@np.array((.2126,.7152,.0722));q=np.percentile(v,(10,50,90));hi=ar[lum>=np.percentile(lum,90)].mean(0);tq=np.array(t['value_p10_p50_p90']);th=np.array(t['highlight_rgb'])
   er=(q-tq)/np.maximum(tq,10);eh=(hi-th)/np.maximum(th,20)
   # All unchanged finishes have the same weight and requested tolerances.
   res.extend(er/np.array((.15,.10,.15)));res.extend(eh/.10)
   res.extend((np.maximum(abs(er)-np.array((.15,.10,.15)),0)*12));res.extend(np.maximum(abs(eh)-.10,0)*12)
   # Prioritize the cross-part exposure/color anchors over residual differences
   # in photographed versus accepted manufacturing and wear distributions.
   res.append(max(abs(er[1])-.09,0)*80);res.extend(np.maximum(abs(eh)-.09,0)*50)
   res.extend(((hi/max(hi.max(),1))-t['highlight_color'])/.10)
   if report:
    m=metrics(ar);errors,passed=comparison(m,t);rows[role]=dict(predicted=m,photo=t,relative_errors=errors,within_requested_bounds=passed)
  res.extend(x[:count]*.0005)
  rr=np.array(res)
  return (float(rr@rr),rows) if report else rr
 best=None
 if a.initial:
  init=json.loads((base/a.initial).read_text()).get(shot)
  if init:
   x=np.r_[np.zeros(count),np.tile(init['color'][:2],color_count//2)];x[0]=init['world']/energy_scale[0]
   for card in init['lights']:
    for k,b in enumerate(bases[1:],1):
     if list(b['position'])==card['position'] and list(b['size'])==card['size']:
      x[k]=card['power']/energy_scale[k]
      if a.mixed_light and upper[k] and card.get('color'):x[-4:-2]=card['color'][:2]
   clamp(x)
   rr=objective(x);best=(rr@rr,x)
 for restart in range(a.restarts):
  x=np.r_[np.zeros(count),np.ones(color_count)];x[0]=.2;x[1+rng.integers(count-1)]=10
  if best is not None:
   x=best[1].copy()
   if restart%2:x[:count]=np.maximum(x[:count]+rng.normal(0,3,count),0)
  rr=objective(x);cost=rr@rr
  for step in (15,5,1.5,.5,.15):
   for iteration in range(6):
    improved=False
    for k in rng.permutation(len(x)):
     for sign in (-1,1):
      z=x.copy();z[k]+=sign*step*(1 if k<count else .015);clamp(z)
      rr=objective(z);value=rr@rr
      if value<cost:x=z;cost=value;improved=True
    if not improved:break
  damping=.02
  for iteration in range(60):
   rr=objective(x);columns=[]
   for k in range(len(x)):
    step=.002 if k>=len(bases) else max(.02,x[k]*.003);z=x.copy();z[k]+=step;columns.append((objective(z)-rr)/step)
   jac=np.stack(columns,axis=1);normal=jac.T@jac
   try:delta=np.linalg.solve(normal+damping*np.diag(np.maximum(np.diag(normal),1e-4)),-jac.T@rr)
   except np.linalg.LinAlgError:break
   z=clamp(x+delta);rr=objective(z);value=rr@rr
   if value<cost:x=z;cost=value;damping=max(damping*.5,1e-7)
   else:damping=min(damping*5,1e8)
   if damping>1e7:break
  if best is None or cost<best[0]:best=(float(cost),x.copy())
  cost,x=best;_,rows=objective(x,True)
  lights=[]
  for i,(b,v) in enumerate(zip(bases[1:],x[1:count]*energy_scale[1:]),1):
   if v<=.00001:continue
   card=dict(b,power=float(v))
   if a.mixed_light:card['color']=[*(x[-4:-2] if upper[i] else x[-2:]),1.]
   lights.append(card)
  row=dict(world=float(x[0]*energy_scale[0]),color=[*x[-2:],1.],lights=lights,backdrop=spec['backdrop'],diagnostic=dict(objective='unchanged finish anchors and neutral constraints ONLY; receiver excluded',mixed_light=a.mixed_light,anchors=rows,loss=cost,source_sha256=s['sha256'],all_anchors_pass=all(v['within_requested_bounds'] for v in rows.values())))
  results[shot]=row;(base/a.out).write_text(json.dumps(results,indent=2)+'\n')
  print(a.member,shot,restart,'loss',round(cost,3),'anchors',[(k,np.round(v['predicted']['value_p10_p50_p90']).tolist(),v['photo']['value_p10_p50_p90']) for k,v in rows.items()],flush=True)
