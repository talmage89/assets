"""Fit physical area-light energies; final images must be rerendered in Cycles."""
import json,sys,math,argparse
from pathlib import Path
import numpy as np
import OpenImageIO as oiio,PyOpenColorIO as ocio
from PIL import Image,ImageFilter
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from look_review import REGIONS,LEGACY_LINK,metrics,polygon_mask
from image_masks import raster,projection
# Whole-view guards stop a favorable barrel fit from washing out the rest.
REGIONS=dict(REGIONS)
# The same field frame must explain the accepted cases/jackets and the links.
REGIONS["field_steel_links"]=LEGACY_LINK
REGIONS['guard_cover']=('used_right', [[(918,283),(1290,362),(1294,392),(1033,342),(1016,338),(914,313)]], 'used_right_photo', ('FeedCover_Shell','FeedCover_PressedBead','FeedCover_SidePress'))
REGIONS['guard_grip']=('used_right', [[(1114,503),(1169,516),(1185,592),(1229,658),(1203,680),(1123,684),(1108,660),(1122,625),(1104,555)]], 'used_right_photo', ('PistolGrip_Sculpt','Grip_MoldRib'))
REGIONS['guard_handle']=('used_right', [[(888,163),(1040,193),(1030,230),(876,201)]], 'used_right_photo', ('CarryHandle_Grip',))

parser=argparse.ArgumentParser();parser.add_argument('--basis',default='build/light-response');parser.add_argument('--restarts',type=int,default=6);parser.add_argument('--cover-profile',action='store_true');parser.add_argument('--mixed-light',action='store_true');parser.add_argument('--shots');parser.add_argument('--samples-per-part',type=int,default=2200);parser.add_argument('--initial');parser.add_argument('--geometry',default='build/image-geometry');parser.add_argument('--output',default='build/light-response/fitted-lights.json');args=parser.parse_args();basis=BASE/args.basis;B=json.loads((basis/'bases.json').read_text());meta=json.loads((basis/'shots.json').read_text())
c=ocio.Config.CreateFromFile((basis/'ocio-path.txt').read_text().strip());g=ocio.GroupTransform();g.appendTransform(ocio.LookTransform(src='Linear Rec.709',dst='Linear Rec.709',looks='AgX - Medium High Contrast'));g.appendTransform(ocio.DisplayViewTransform(src='Linear Rec.709',display='sRGB',view='AgX'));proc=c.getProcessor(g).getDefaultCPUProcessor()
rng=np.random.default_rng(56);results={};color_count=4 if args.mixed_light else 2
upper=np.array([not b.get('world') and b['position'][2]>.25 for b in B])
def read(p):
 p=p if p.exists() else p.with_suffix('.png');f=oiio.ImageInput.open(str(p));a=f.read_image();f.close();return a[:,:,:3]
for shot in dict.fromkeys(v[2] for v in REGIONS.values()):
 if shot+'__0' not in meta or (args.shots and shot not in args.shots.split(',')):continue
 regions={k:v for k,v in REGIONS.items() if v[2]==shot};s=meta[shot+'__0'];first=read(basis/(shot+'__0.exr'));h,w=first.shape[:2];geo=np.load(BASE/args.geometry/(shot+'.npz'));assert str(geo['sha256'])==s['sha256'],(shot,'stale geometry for light fit');ids,_=raster(geo,s,w,h)
 pack=[];targets={};slices={};start=0
 for role,(name,polys,_,prefixes) in regions.items():
  m=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(prefixes)])
  if role in ('brass','copper_green_tip'):
   suffix='_Case' if role=='brass' else '_Jacket'
   m &= np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).endswith(suffix)])
  m=np.asarray(Image.fromarray(np.uint8(m)*255).filter(ImageFilter.MinFilter(3)))>0
  indices=np.flatnonzero(m);indices=rng.choice(indices,min(len(indices),args.samples_per_part),replace=False);pack.extend(indices);slices[role]=slice(start,start+len(indices));start+=len(indices)
  ref=np.asarray(Image.open(BASE/'build/white-balanced'/(name+'.jpg')).convert('RGB'));pm=polygon_mask((ref.shape[1],ref.shape[0]),polys);pm=np.asarray(Image.fromarray(np.uint8(pm)*255).filter(ImageFilter.MinFilter(3)))>0;targets[role]=metrics(ref[pm])
 profile_data=None
 if args.cover_profile and shot=='used_photo':
  point,_=projection(np.array([[-.03,.190,.137]]),s,w,h);px=int(point[0,0])
  shell=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n)=='FeedCover_Shell']);ys=np.flatnonzero(shell[:,px]);yy=np.arange(ys.min(),ys.max()+1)
  profile_slice=slice(len(pack),len(pack)+len(yy)*5)
  pack.extend((yy[:,None]*w+np.arange(px-2,px+3)[None,:]).ravel().tolist())
  ref=np.asarray(Image.open(BASE/'build/white-balanced/used_receiver.jpg').convert('RGB'),float)
  def profile_stats(a):
   v=np.median(a.max(2),axis=1);floor,peak=np.percentile(v,[10,95]);threshold=(floor+peak)/2
   # Guide the same principal connected band as the native FWHM audit.
   # Summing all disconnected reflections incorrectly penalizes the hem's
   # separate top facet as though it widened the principal satin band.
   runs=[];start=None
   for i,on in enumerate(np.r_[v>=threshold,False]):
    if on and start is None:start=i
    if not on and start is not None:runs.append((start,i));start=None
   lo,hi=max(runs,key=lambda r:r[1]-r[0]) if runs else (0,0)
   band=v[max(0,lo-2):min(len(v),hi+2)]
   width=np.sum(1/(1+np.exp(np.clip(-(band-threshold)/4,-50,50))))/len(v)
   return float(peak),float(width),(hi-lo)/len(v)
  profile_data=(profile_slice,len(yy),profile_stats(ref[320:393,628:633]))
 data=np.stack([read(basis/(shot+'__'+str(i)+'.exr')).reshape(-1,3)[pack] for i in range(len(B))]);data=np.transpose(data,(1,2,0)).reshape(-1,len(B)).astype(np.float32);gain=2**s.get('exposure',.45)
 # Near-crown cards are much more efficient per watt. Fit hundredths of a
 # watt there so the same numerical steps resolve them instead of clipping.
 energy_scale=np.array([.01 if not b.get('world') and max(b['size'])<=.03 else 1 for b in B])
 data*=energy_scale
 def predict(p):
  if args.mixed_light:
   rgb=(data[:,upper]@p[:len(B)][upper]).reshape(-1,3)*np.r_[p[-4:-2],1]+(data[:,~upper]@p[:len(B)][~upper]).reshape(-1,3)*np.r_[p[-2:],1];rgb*=gain
  else:rgb=(data@p[:len(B)]).reshape(-1,3)*gain*np.r_[p[-2:],1]
  rgb=np.ascontiguousarray(rgb,dtype=np.float32);proc.applyRGB(rgb);return np.clip(rgb*255,0,255)
 def objective(p,report=False):
  rgb=predict(p);loss=0;rows={};residuals=[]
  for role,sl in slices.items():
   a=rgb[sl];v=a.max(1);l=a@np.array((.2126,.7152,.0722));q=np.percentile(v,[10,50,90]);hi=a[l>=np.percentile(l,90)].mean(0);t=targets[role];tq=np.array(t['value_p10_p50_p90']);th=np.array(t['brightest_decile_rgb']);er=(q-tq)/np.maximum(tq,10);eh=(hi-th)/np.maximum(th,20)
   guard=role.startswith('guard_');weight=1
   if guard:
    residuals.extend([max(0,er[1]-.20)*30,*np.maximum(eh-.15,0)*30])
   else:
    residuals.extend((er/np.array((.15,.10,.15))*np.sqrt(np.array((1,2,1)))).tolist());residuals.extend((eh/.10*np.sqrt(.65)).tolist())
    residuals.extend((np.maximum(abs(er)-np.array((.14,.09,.14)),0)*80).tolist());residuals.extend((np.maximum(abs(eh)-.09,0)*60).tolist())
   if not guard:
    chroma=hi/max(hi.max(),1);target_chroma=th/max(th.max(),1);ce=(chroma-target_chroma)/np.maximum(target_chroma,1e-6)
    residuals.extend((ce/.10).tolist());residuals.extend((np.maximum(abs(ce)-.09,0)*80).tolist())
   mr=np.median(a,axis=0);mt=np.array(t['median_rgb']);residuals.extend((((mr-mt)/np.maximum(tq[1],10)*np.sqrt(5)) if not guard else np.zeros(3)).tolist())
   rows[role]=dict(predicted_q=q.tolist(),photo_q=tq.tolist(),predicted_h=hi.tolist(),photo_h=th.tolist())
  if profile_data:
   sl,count,(peak_target,width_target,hard_target)=profile_data;peak,width,hard=profile_stats(rgb[sl].reshape(count,5,3))
   pe=(peak-peak_target)/peak_target;we=(width-width_target)/width_target
   residuals.extend([pe/.10*2,we/.10*2,max(abs(pe)-.09,0)*80,max(abs(we)-.09,0)*80,max(abs(hard/hard_target-1)-.09,0)*80])
   rows['cover_reflection_profile']=dict(predicted_peak=peak,photo_peak=peak_target,predicted_soft_width=width,photo_soft_width=width_target,predicted_native_width=hard,photo_native_width=hard_target)
  residuals.extend((p[:len(B)]*.001).tolist());residuals=np.array(residuals);loss=residuals@residuals
  return (float(loss),rows) if report is True else residuals if report=='residual' else float(loss)
 best=None
 initial=json.loads((BASE/args.initial).read_text()).get(shot) if args.initial else None
 if initial:
  p=np.zeros(len(B)+color_count);p[-color_count:]=np.tile(initial['color'][:2],color_count//2)
  if args.mixed_light and initial.get('light_colors'):
   for above,target in ((True,slice(-4,-2)),(False,slice(-2,None))):
    colors=[c[:2] for b,c in zip(initial['bases'],initial['light_colors']) if not b.get('world') and (b['position'][2]>.25)==above]
    if colors:p[target]=colors[0]
  for energy,old in zip(initial['energies'],initial['bases']):
   for i,b in enumerate(B):
    if b==old:p[i]=energy/energy_scale[i];break
  best=(objective(p),p)
 for restart in range(args.restarts):
  p=np.r_[np.zeros(len(B)),np.tile((.90,.96),color_count//2)];p[0]=.08;p[1+rng.integers(len(B)-1)]=12
  if best is not None:
   p=best[1].copy()
   if restart%2:p=np.maximum(p+rng.normal(0,1,len(p))*np.r_[np.full(len(B),3),np.full(color_count,.04)],0);p[-color_count:]=np.clip(p[-color_count:],.65,1.2)
  cost=objective(p)
  for step in (15,5,1.5,.5,.15):
   for iteration in range(10):
    improved=False
    for k in rng.permutation(len(B)+color_count):
     old=p[k];choices=[max(0,old-step),old+step] if k<len(B) else [max(.65,old-.025*step),min(1.2,old+.025*step)]
     for value in choices:
      z=p.copy();z[k]=value;v=objective(z)
      if v<cost:p=z;cost=v;improved=True
    # Exchange light energy also escapes coordinate saddles.
    for _ in range(5):
     z=p.copy();j,k=rng.choice(len(B),2,replace=False);amount=min(z[j],step);z[j]-=amount;z[k]+=amount;v=objective(z)
     if v<cost:p=z;cost=v;improved=True
    if not improved:break
  damping=.02
  for iteration in range(70):
   residual=objective(p,'residual');columns=[]
   for k in range(len(p)):
    step=.003 if k>=len(B) else max(.03,p[k]*.003);z=p.copy();z[k]+=step;columns.append((objective(z,'residual')-residual)/step)
   jac=np.stack(columns,axis=1);normal=jac.T@jac
   try:delta=np.linalg.solve(normal+damping*np.diag(np.maximum(np.diag(normal),1e-4)),-jac.T@residual)
   except np.linalg.LinAlgError:break
   z=p+delta;z[:len(B)]=np.maximum(z[:len(B)],0);z[-color_count:]=np.clip(z[-color_count:],.65,1.2);candidate=objective(z)
   if candidate<cost:p=z;cost=candidate;damping=max(damping*.5,1e-7)
   else:damping=min(damping*5,1e8)
   if damping>1e7:break
  if best is None or cost<best[0]:best=(cost,p.copy())
  print(shot,restart,'loss',round(best[0],2),flush=True)
  bc,bp=best;_,br=objective(bp,True)
  progress=dict(loss=bc,energies=(bp[:len(B)]*energy_scale).tolist(),color=[*bp[-2:],1],predictions=br,bases=B,source_sha256=s['sha256'])
  if args.mixed_light:progress['light_colors']=[[*bp[-4:-2],1] if above else [*bp[-2:],1] for above in upper]
  path=(BASE/args.output).with_suffix('.progress.json');temp=path.with_suffix('.tmp')
  temp.write_text(json.dumps({**results,shot:progress},indent=2));temp.replace(path)
  if best[0]<.7:break
 cost,p=best;_,rows=objective(p,True);results[shot]=dict(loss=cost,energies=(p[:len(B)]*energy_scale).tolist(),color=[*p[-2:],1],predictions=rows,bases=B,source_sha256=s['sha256'])
 if args.mixed_light:results[shot]['light_colors']=[[*p[-4:-2],1] if above else [*p[-2:],1] for above in upper]
 (BASE/args.output).write_text(json.dumps(results,indent=2))
 for role,row in rows.items():
  if 'predicted_q' in row:print(role,'V',np.round(row['predicted_q']),np.round(row['photo_q']),'H',np.round(row['predicted_h']),np.round(row['photo_h']),flush=True)
  else:print(role,row,flush=True)
