"""Fit whole-receiver statistics with nonnegative physical card energies.

Uses installed OpenImageIO/OCIO and NumPy only. Nothing is installed or fetched.
No fitted image is accepted: export, source and original before GLBs are all
rendered afresh through the committed member recipe.
"""
import argparse
import json
from pathlib import Path
import sys

import numpy as np
import OpenImageIO as oiio
import PyOpenColorIO as ocio

ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from guns.common.paint_review import masks,reference,metrics,LUMA,geometry,raster

p=argparse.ArgumentParser();p.add_argument('member');p.add_argument('--basis',default='build/paint-light-response');p.add_argument('--restarts',type=int,default=8);p.add_argument('--out',default='build/paint-light-response/fitted.json');p.add_argument('--initial');a=p.parse_args()
base=ROOT/'guns'/a.member;folder=base/a.basis
bases=json.loads((folder/'bases.json').read_text());meta=json.loads((folder/'shots.json').read_text())
config=ocio.Config.CreateFromFile((folder/'ocio-path.txt').read_text())
group=ocio.GroupTransform();group.appendTransform(ocio.LookTransform(src='Linear Rec.709',dst='Linear Rec.709',looks='AgX - Medium High Contrast'));group.appendTransform(ocio.DisplayViewTransform(src='Linear Rec.709',display='sRGB',view='AgX'))
proc=config.getProcessor(group).getDefaultCPUProcessor();rng=np.random.default_rng(39);result={}
specs=json.loads((base/'src/paint_review.json').read_text())
for name,spec in specs.items():
    shot=spec['shot']
    if shot+'__0' not in meta:continue
    s=meta[shot+'__0']
    def read(index):
        f=oiio.ImageInput.open(str(folder/(shot+'__'+str(index)+'.exr')))
        arr=f.read_image();f.close();return arr[:,:,:3]
    first=read(0);h,w=first.shape[:2];mask,_=masks(base,spec,s,w,h)
    indices=np.flatnonzero(mask);indices=rng.choice(indices,min(9000,len(indices)),replace=False)
    main_count=len(indices);anchors=[];all_indices=list(indices)
    for anchor in spec.get('anchors',[]):
        am,_=masks(base,anchor,s,w,h);ai=np.flatnonzero(am);ai=rng.choice(ai,min(4500,len(ai)),replace=False)
        begin=len(all_indices);all_indices.extend(ai.tolist())
        ref,rm=reference(base,anchor);anchors.append((slice(begin,len(all_indices)),metrics(ref[rm])))
    data=np.stack([read(i).reshape(-1,3)[all_indices] for i in range(len(bases))],axis=-1).astype(np.float32)
    photo,pm=reference(base,spec);target=metrics(photo[pm]);tq=np.asarray(target['value_p10_p50_p90']);th=np.asarray(target['highlight_rgb'])
    guards=[]
    if spec.get('height_guards'):
        geo=geometry(base);geo['uv']=geo['xyz'][:,:,[2,1]]
        height=raster(geo,s,w,h)[1][:,:,0].reshape(-1)[indices]
        for guard in spec['height_guards']:
            selected=(height>=guard.get('z_min',-1))&(height<guard.get('z_max',1))
            ref,rm=reference(base,dict(spec,polygons=guard['polygons']))
            guards.append((selected,np.asarray(metrics(ref[rm])['value_p10_p50_p90'])))
    gain=2**s.get('exposure',-.3)
    def predict(params):
        rgb=np.ascontiguousarray((data@params[:-2])*np.r_[params[-2:],1]*gain,dtype=np.float32)
        proc.applyRGB(rgb)
        return np.clip(rgb*255,0,255)
    def objective(params,report=False):
        rgb=predict(params);main=rgb[:main_count];v=main.max(1);lum=main@LUMA
        q=np.percentile(v,(10,50,90));hi=main[lum>=np.percentile(lum,90)].mean(0)
        er=(q-tq)/np.maximum(tq,1);eh=(hi-th)/np.maximum(th,1)
        residual=np.r_[er/np.array((.15,.10,.15)),eh/.1,
            np.maximum(abs(er)-np.array((.13,.08,.13)),0)*200,
            np.maximum(abs(eh)-.08,0)*200,
            ((hi/max(hi.max(),1))/(th/max(th.max(),1))-1)/.10,
            params[:-2]*.0003]
        # Broad spatial guards reject a statistical match with the bright
        # reflection on the wrong land. They never replace the whole-part fit.
        for selected,goal in guards:
            measured=np.percentile(v[selected],(10,50,90))
            residual=np.r_[residual,(measured-goal)/np.maximum(goal,10)/.20]
        for sl,goal in anchors:
            ar=rgb[sl];med=np.median(ar.max(1));al=ar@LUMA;ah=ar[al>=np.percentile(al,90)].mean(0)
            target=goal['value_p10_p50_p90'][1]
            residual=np.r_[residual,(med-target)/max(target,10)/.15,
                np.maximum(ah/np.asarray(goal['highlight_rgb'])-1.20,0)*30]
        return (float(residual@residual),q.tolist(),hi.tolist()) if report else residual
    best=None
    if a.initial:
        initial=json.loads((base/a.initial).read_text()).get(shot)
        if initial:
            x=np.r_[np.zeros(len(bases)),initial['color'][:2]];x[0]=initial['world']
            for card in initial['lights']:
                for k,b in enumerate(bases[1:],1):
                    if list(b['position'])==card['position'] and list(b['size'])==card['size']:x[k]=card['power']
            rr=objective(x);best=(float(rr@rr),x)
    for restart in range(a.restarts):
        x=np.r_[np.zeros(len(bases)),1.,1.]
        seeds=[3,6,13,18,19,22,23]
        k=seeds[(restart//3)%len(seeds)] if guards and len(bases)>23 else 1+rng.integers(len(bases)-1)
        x[k]=.5 if k>=17 else 5
        if best is not None and restart%3:
            x=best[1].copy()
            if restart%2:x[:-2]=np.maximum(x[:-2]+rng.normal(0,2,len(bases)),0)
        cost=float(objective(x)@objective(x))
        for step in (10,3,1,.3,.1):
            for iteration in range(8):
                improved=False
                for k in rng.permutation(len(x)):
                    delta=step if k<len(bases) else step*.015
                    for sign in (-1,1):
                        z=x.copy();z[k]=max(0,x[k]+sign*delta) if k<len(bases) else np.clip(x[k]+sign*delta,.8,1.2)
                        r=objective(z);value=float(r@r)
                        if value<cost:x=z;cost=value;improved=True
                if not improved:break
        damping=.02
        for iteration in range(60):
            r=objective(x);columns=[]
            for k in range(len(x)):
                step=.002 if k>=len(bases) else max(.02,x[k]*.003)
                z=x.copy();z[k]+=step;columns.append((objective(z)-r)/step)
            jac=np.stack(columns,axis=1);normal=jac.T@jac
            delta=np.linalg.solve(normal+damping*np.diag(np.maximum(np.diag(normal),1e-4)),-jac.T@r)
            z=x+delta;z[:-2]=np.maximum(z[:-2],0);z[-2:]=np.clip(z[-2:],.8,1.2)
            rr=objective(z);value=float(rr@rr)
            if value<cost:x=z;cost=value;damping=max(damping*.5,1e-7)
            else:damping=min(damping*5,1e8)
            if damping>1e7:break
        if best is None or cost<best[0]:best=(cost,x.copy())
        cost,x=best;_,q,hi=objective(x,True)
        color=[*x[-2:],1.]
        row=dict(world=float(x[0]),color=color,lights=[dict(b,power=float(power)) for b,power in zip(bases[1:],x[1:-2]) if power>.00001],diagnostic=dict(predicted_value=q,predicted_highlight=hi,photo_value=tq.tolist(),photo_highlight=th.tolist(),loss=cost,source_sha256=s['sha256']))
        parameters=folder/'diagnostic-parameters.json'
        if parameters.exists():row['diagnostic']['material_overrides']=json.loads(parameters.read_text())
        prediction=predict(x);pred=prediction[:main_count].max(1)
        row['diagnostic']['height_guards']=[dict(predicted_value=np.percentile(pred[selected],(10,50,90)).tolist(),photo_value=goal.tolist()) for selected,goal in guards]
        row['diagnostic']['anchors']=[dict(predicted=metrics(prediction[sl]),photo=goal) for sl,goal in anchors]
        result[shot]=row;(base/a.out).write_text(json.dumps(result,indent=2)+'\n')
        print(a.member,shot,restart,round(cost,3),np.round(q,1),np.round(hi,1),flush=True)
        if cost<.4:break
