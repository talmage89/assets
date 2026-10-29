"""Raw-GLB orthographic diagnostic: explicit box mips and trilinear sampling.

Run in Blender for kit.gltf/mathutils; CPU rasterization requires no GPU lock.
This is a sampling diagnostic; the preserved Cycles studio pairs remain the
photographic look reference. Pixel derivatives select the same LOD at identical
texel density. No resizing a full-size render to fake the distant render.
"""
import sys,json,hashlib,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from kit.gltf import GLB
from kit.fonts import find_font
from kit import detachable_verify as V
from kit.image_io import linear_to_srgb

def unit(v):
 return v/np.maximum(np.linalg.norm(v,axis=-1,keepdims=True),1e-12)

def geometry(g):
 rows=[]
 for index,node in enumerate(g.json['nodes']):
  if 'mesh' not in node:continue
  matrix=g.world(index);normal_matrix=np.linalg.inv(matrix[:3,:3]).T
  for primitive in g.json['meshes'][node['mesh']]['primitives']:
   values={k:g.accessor(i).astype(float) for k,i in primitive['attributes'].items()}
   values['POSITION']=(np.column_stack((values['POSITION'],np.ones(len(values['POSITION']))))@matrix.T)[:,:3]
   values['NORMAL']=unit(values['NORMAL']@normal_matrix.T)
   if 'TANGENT' in values:
    tangent=values['TANGENT'];values['TANGENT']=np.column_stack((unit(tangent[:,:3]@matrix[:3,:3].T),tangent[:,3]))
   for indices in g.accessor(primitive['indices']).reshape(-1,3):
    row={k:v[indices] for k,v in values.items()}
    if 'TANGENT' not in row:
     duv=row['TEXCOORD_0'][1:]-row['TEXCOORD_0'][0];dp=row['POSITION'][1:]-row['POSITION'][0]
     # Derive tangent handedness from the delivered UV gradient, without
     # assuming a source Blender coordinate convention.
     if abs(np.linalg.det(duv))>1e-14:
      gradient=np.linalg.solve(duv,dp);t=unit(gradient[0]);b=unit(gradient[1])
      signs=np.sign(np.cross(row['NORMAL'],t)@b)
     else:t=unit(np.cross(row['NORMAL'][0],(1,.3,.2)));signs=np.ones(3)
     row['TANGENT']=np.column_stack((np.tile(t,(3,1)),signs))
    rows.append(row)
 return rows

def filtered(chains,uv,lod):
 lod=np.clip(lod,0,len(chains)-1);lower=np.floor(lod).astype(int);frac=lod-lower
 result=np.zeros((len(uv),chains[0].shape[2]))
 for level in np.unique(lower):
  selected=lower==level
  result[selected]=V.sample(chains[level],uv[selected])*(1-frac[selected,None])+V.sample(chains[min(level+1,len(chains)-1)],uv[selected])*frac[selected,None]
 return result

def shade(values,chains,uv,lod,camera):
 base=filtered(chains['BaseColor'],uv,lod)[:,:3]
 orm=filtered(chains['ORM'],uv,lod);normal=filtered(chains['Normal'],uv,lod)[:,:3]*2-1
 n=unit(values['NORMAL']);t=unit(values['TANGENT'][:,:3]-n*np.sum(n*values['TANGENT'][:,:3],axis=1,keepdims=True))
 b=np.cross(n,t)*np.sign(values['TANGENT'][:,3:]);n=unit(t*normal[:,:1]+b*normal[:,1:2]+n*normal[:,2:3])
 rough=np.clip(orm[:,1:2],.06,1);metal=orm[:,2:3];ao=orm[:,:1]
 f0=.04*(1-metal)+base*metal
 color=(base*(1-metal)*.18+f0*.35)*ao
 for direction,power in [((-.7,1,.8),2.2),((.9,.35,.5),1.0),((.3,.7,-1),1.4)]:
  light=unit(np.array(direction,float));h=unit(light+camera)
  nl=np.maximum(n@light,0)[:,None];nv=np.maximum(n@camera,1e-4)[:,None];nh=np.maximum(n@h,0)[:,None]
  vh=max(float(camera@h),0);alpha=rough**2;a2=alpha**2
  distribution=a2/(np.pi*(nh**2*(a2-1)+1)**2+1e-12)
  k=(rough+1)**2/8;visibility=(nl/(nl*(1-k)+k))*(nv/(nv*(1-k)+k))
  fresnel=f0+(1-f0)*(1-vh)**5
  specular=distribution*visibility*fresnel/(4*nl*nv+1e-8)
  color+=(base*(1-metal)/np.pi+specular)*nl*power
 # Same smooth exposure/rolloff on both versions. AO comes from shipped ORM.
 return np.clip(color/(color+.65),0,1)

def render(path,resolution,coverage,*,frame=None):
 g=GLB(path)
 assert len(g.json['materials'])==1 and not g.json.get('skins') and not g.json.get('animations'), 'Static one-material detachables only'
 triangles=geometry(g);textures=V.maps(g)
 for channel,sampler in V.samplers(g).items():
  assert sampler.get('minFilter')==9987 and sampler.get('magFilter')==9729,(path,channel,sampler)
 chains={c:V.mip_chain(a,color=c=='BaseColor') for c,a in textures.items()}
 # Generic quarter view in glTF +Y-up space, same fixed world frame in a pair.
 camera=unit(np.array((1.1,.65,1.5)));right=unit(np.cross((0,1,0),camera));up=np.cross(camera,right)
 basis=np.stack((right,-up,camera))
 points=np.concatenate([t['POSITION'] for t in triangles]);projected=points@basis.T
 if frame is None:
  lo=projected.min(axis=0);hi=projected.max(axis=0);frame=((lo+hi)/2,max((hi-lo)[:2]))
 center,span=frame;scale=coverage/span
 depth=np.full((resolution,resolution),-np.inf);color=np.full((resolution,resolution,3),.022)
 lods=[];covered=np.zeros(depth.shape,bool)
 for triangle in triangles:
  p=(triangle['POSITION']@basis.T-center)*scale;p[:,:2]+=resolution/2
  low=np.maximum(np.floor(p[:,:2].min(axis=0)).astype(int),0);high=np.minimum(np.ceil(p[:,:2].max(axis=0)).astype(int),resolution)
  if np.any(high<=low):continue
  matrix=(p[1:,:2]-p[0,:2]).T
  if abs(np.linalg.det(matrix))<1e-10:continue
  inv=np.linalg.inv(matrix);yy,xx=np.mgrid[low[1]:high[1],low[0]:high[0]]
  st=(np.stack((xx+.5,yy+.5),axis=-1)-p[0,:2])@inv.T
  weights=np.stack((1-st.sum(axis=-1),st[...,0],st[...,1]),axis=-1)
  z=weights@p[:,2];target=depth[low[1]:high[1],low[0]:high[0]]
  hit=np.all(weights>=-1e-8,axis=-1)&(z>target)
  if not hit.any():continue
  bary=weights[hit];uv=bary@triangle['TEXCOORD_0']
  derivatives=(triangle['TEXCOORD_0'][1:]-triangle['TEXCOORD_0'][0]).T@inv
  lod=np.log2(max(np.linalg.norm(derivatives,axis=0))*textures['Normal'].shape[0]+1e-20)
  levels=np.full(len(uv),max(lod,0));values={k:bary@v for k,v in triangle.items() if k!='TEXCOORD_0'}
  color[low[1]:high[1],low[0]:high[0]][hit]=shade(values,chains,uv,levels,camera)
  target[hit]=z[hit];covered[low[1]:high[1],low[0]:high[0]][hit]=True;lods.extend(levels.tolist())
 image=Image.fromarray(np.uint8(np.clip(linear_to_srgb(color),0,1)*255+.5))
 y,x=np.where(covered)
 return image,frame,dict(lod_min=min(lods),lod_max=max(lods),coverage_pixels=[int(np.ptp(x)+1),int(np.ptp(y)+1)] if len(x) else [0,0],sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def main():
 p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
 a.out.mkdir(parents=True,exist_ok=True);records={}
 font=ImageFont.truetype(find_font('DejaVu Sans','Book'),16)
 for label,resolution,coverage in [('full',640,570),('distant',192,40)]:
  old,frame,old_record=render(a.before,resolution,coverage);new,_,new_record=render(a.after,resolution,coverage,frame=frame)
  for name,image in [('old',old),('new',new)]:image.save(a.out/(label+'-'+name+'.png'))
  pair=Image.new('RGB',(resolution*2,resolution+32),(35,35,35));pair.paste(old,(0,32));pair.paste(new,(resolution,32));draw=ImageDraw.Draw(pair)
  draw.text((8,8),'OLD atlas' if label=='distant' else 'OLD gun atlas / mipmapped',font=font,fill='white');draw.text((resolution+8,8),'NEW own set' if label=='distant' else 'NEW own set / mipmapped',font=font,fill='white')
  pair.save(a.out/(label+'-pair.png'))
  if label=='distant':
   # Native 40px item plus a nearest magnification for inspecting those texels.
   crop=pair.crop((resolution//2-26,32+resolution//2-26,resolution//2+26,32+resolution//2+26))
   crop_new=pair.crop((resolution+resolution//2-26,32+resolution//2-26,resolution+resolution//2+26,32+resolution//2+26))
   detail=Image.new('RGB',(832,416));detail.paste(crop.resize((416,416),Image.Resampling.NEAREST),(0,0));detail.paste(crop_new.resize((416,416),Image.Resampling.NEAREST),(416,0));detail.save(a.out/'distant-texels.png')
  records[label]=dict(old=old_record,new=new_record,filter='Box mips in linear RGB/data; trilinear derivative LOD; repeat wrapping',renderer='CPU raw-accessor orthographic diagnostic, analytic GGX lighting',renderer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 (a.out/'provenance.json').write_text(json.dumps(records,indent=2))
if __name__=='__main__':main()
