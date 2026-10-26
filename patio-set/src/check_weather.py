"""Independent delivered BaseColor exposure contrast, measured on GLB surfaces."""
import sys,json,io,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.gltf import GLB
import numpy as np
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--wear',type=float,default=.35);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
g=GLB(Path(a.source));i=next(i for i,r in enumerate(g.json['images']) if 'BaseColor' in r['name']);tex=np.array(Image.open(io.BytesIO(g.image(i))).convert('RGB'))/255;h,w=tex.shape[:2]
sets={}
for mesh in g.json['meshes']:
 if mesh['name'] not in ('Umbrella_OpenMesh','TableMesh','ChairMesh'):continue
 points=[];normals=[];colors=[];rgb=[];areas=[]
 for prim in mesh['primitives']:
  idx=g.accessor(prim['indices']).reshape(-1,3);v=g.accessor(prim['attributes']['POSITION'])[idx];uv=g.accessor(prim['attributes']['TEXCOORD_0'])[idx].mean(axis=1)
  cr=np.cross(v[:,1]-v[:,0],v[:,2]-v[:,0]);ar=np.linalg.norm(cr,axis=1);nn=cr/np.maximum(ar[:,None],1e-12)
  px=np.clip((uv[:,0]*w).astype(int),0,w-1);py=np.clip((uv[:,1]*h).astype(int),0,h-1)
  points.append(v.mean(axis=1));normals.append(nn);colors.append(tex[py,px]@np.array([.2126,.7152,.0722]));rgb.append(tex[py,px]);areas.append(ar)
 xyz=np.concatenate(points);nn=np.concatenate(normals);c=np.concatenate(colors);ar=np.concatenate(areas);rgb=np.concatenate(rgb)
 if mesh['name']=='Umbrella_OpenMesh':
  # Broad canopy faces only; exclude the protected sewn rib tunnels.
  domain=(xyz[:,1]>1.94)&(np.linalg.norm(xyz[:,[0,2]],axis=1)>.5)&(ar>.005);first=domain&(nn[:,1]>.6);second=domain&(nn[:,1]<-.6)
 elif mesh['name']=='ChairMesh':
  domain=(xyz[:,1]>.55)&(xyz[:,1]<.90)&(np.abs(xyz[:,0])<.24);first=domain&(nn[:,2]>.6);second=domain&(nn[:,2]<-.6)
 else:
  first=(xyz[:,1]>.744)&(nn[:,1]>.9);second=(xyz[:,1]>.09)&(xyz[:,1]<.65)&(np.abs(nn[:,1])<.3)
 mean=lambda m:float(np.average(c[m],weights=ar[m]))
 color_mean=lambda m:np.average(rgb[m],weights=ar[m],axis=0).tolist()
 sets[mesh['name']]=dict(exposed_srgb=color_mean(first),protected_srgb=color_mean(second),exposed_srgb_luminance=mean(first),protected_srgb_luminance=mean(second),ratio=mean(first)/mean(second),samples=[int(first.sum()),int(second.sum())])
factor=max(0,min(1,a.wear/.35))
# Dye retains its green hue; a single thin sling cannot have radically different faces.
limits={'Umbrella_OpenMesh':(.98+.08*factor,1.55),'TableMesh':(.98+.27*factor,10),'ChairMesh':(.98,1.30)}
errors=[]
for k,r in sets.items():
 lo,hi=limits[k]
 if not lo<=r['ratio']<=hi:errors.append(k+': exposure contrast')
 if k!='TableMesh':
  for side in ('exposed_srgb','protected_srgb'):
   red,green,blue=r[side]
   if not (green>red*1.08 and green>blue*1.15):errors.append(k+': green dye lost on '+side)
out=dict(passed=not errors,source=a.source,wear=a.wear,scope='Area-weighted delivered BaseColor, independent of studio lights; green dye retained; exposure bounded independently of studio lights',limits=limits,measurements=sets,errors=errors)
Path(a.out).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if errors:raise RuntimeError('Delivered exposure contrast or retained green hue is outside the calibrated range')
