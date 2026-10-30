"""Site-off evidence GLBs from two independent kit bakes on identical UVs.

The clean bake preserves all manufacture and removes use. Each site owns a
separate part or a disjoint physical region of a part. Integer texel masks copy
that region from the clean bake into the used atlas; no values are painted or
resampled. The normal map keeps RGB16. All variants use the kit exporter.
"""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy,numpy as np
from PIL import Image
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];sys.path[:0]=[str(ROOT),str(BASE/'src')]
from kit import export,weapon as W
from kit.image_io import read_png,write_png
from kit.gltf import GLB
SIZE=2048
SITES={
 'barrel_carry':['Barrel_R','Barrel_L'], 'muzzles':['Barrel_R','Barrel_L'],
 'action_fade':['Action_Body','Trigger_Plate','Top_Strap','Hinge_Pin'],
 'lever_thumb':['Top_Lever'], 'guard_fingers':['Trigger_Guard','Guard_RearTang'],
 'wrist_points':['Stock_Walnut'], 'stock_toe':['Stock_Walnut'],
 'forend_points':['Forend_Walnut'], 'forend_edges':['Forend_Walnut'],
}

def domain(site,y):
 if site=='barrel_carry':return y<.65
 if site=='muzzles':return y>=.65
 if site=='wrist_points':return y>-.15
 if site=='stock_toe':return y<=-.15
 if site=='forend_points':return (y>.201)&(y<.326)
 if site=='forend_edges':return (y<=.201)|(y>=.326)
 return np.ones(y.shape,bool)

def masks():
 bpy.ops.wm.open_mainfile(filepath=str(BASE/'build/delivery/finalized.blend'))
 arm=bpy.data.objects['SXSArmature'];W.pose(arm,None,0)
 fields={name:np.zeros((SIZE,SIZE),bool) for name in SITES};partmap=np.zeros((SIZE,SIZE),np.uint8)
 parts=sorted([o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('asset_set')],key=lambda o:o.name)
 owners={o.name:i for i,o in enumerate(parts,1)}
 for ob in parts:
  mesh=ob.data;mesh.calc_loop_triangles();uv=mesh.uv_layers['BakeUV'];selected=[s for s,parts in SITES.items() if ob.name in parts]
  for tri in mesh.loop_triangles:
   q=np.array([(uv.data[j].uv.x*SIZE,(1-uv.data[j].uv.y)*SIZE) for j in tri.loops])
   lo=np.maximum(0,np.floor(q.min(0)).astype(int));hi=np.minimum(SIZE-1,np.ceil(q.max(0)).astype(int))
   if np.any(hi<lo):continue
   yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];xx=xx+.5;yy=yy+.5
   v=q[1]-q[0];w=q[2]-q[0];det=v[0]*w[1]-v[1]*w[0]
   if abs(det)<1e-10:continue
   b=((xx-q[0,0])*w[1]-(yy-q[0,1])*w[0])/det;c=(v[0]*(yy-q[0,1])-v[1]*(xx-q[0,0]))/det;a=1-b-c
   inside=(a>=0)&(b>=0)&(c>=0);region=(slice(lo[1],hi[1]+1),slice(lo[0],hi[0]+1))
   partmap[region][inside]=owners[ob.name]
   if not selected:continue
   ys=np.array([(ob.matrix_world@mesh.vertices[j].co).y for j in tri.vertices]);y=a*ys[0]+b*ys[1]+c*ys[2]
   for site in selected:fields[site][region]|=inside&domain(site,y)
 for site,mask in fields.items():
  # Six delivered pixels equal the kit's 12-at-4096 bake margin. Protect
  # every other part's actual occupied texels, even in overlapping chart boxes.
  valid=mask.copy();block=(partmap>0)&~np.isin(partmap,[owners[n] for n in SITES[site]])
  for _ in range(6):
   spread=valid.copy()
   for dy,dx in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)):
    spread|=np.roll(valid,(dy,dx),axis=(0,1))
   valid=spread&~block
  fields[site]=valid
 return fields,partmap

def fingerprint(path):
 g=GLB(path)
 # These accessors cover geometry, UVs, skinning and every sampled clip.
 return {str(i):hashlib.sha256(g.accessor(i).tobytes()).hexdigest() for i in range(len(g.json.get('accessors',[])))}

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=BASE/'build/wear');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);regions,partmap=masks()
 used={c:read_png(BASE/f'textures/T_Covey26_{c}.png') for c in ('BaseColor','Normal','ORM')}
 clean={c:read_png(out/f'clean-textures/T_Covey26_{c}.png') for c in used}
 cfg=out/'evidence-export.py';cfg.write_text('import runpy\nglobals().update(runpy.run_path('+repr(str(BASE/'src/export_config.py'))+'))\nDETACHABLES=[]\n')
 reference=fingerprint(BASE/'export/sxs.glb');rows={}
 for site,region in regions.items():
  folder=out/'textures'/site;folder.mkdir(parents=True,exist_ok=True)
  for c,array in used.items():
   result=array.copy();result[region]=clean[c][region]
   write_png(folder/f'T_Covey26_{c}.png',result,16 if c=='Normal' else 8)
  Image.fromarray(np.uint8(region)*255).save(out/(site+'-atlas-region.png'))
  path=out/'export'/(site+'-off.glb');path.parent.mkdir(exist_ok=True)
  sys.argv=['blender','--','--source',str(BASE/'build/delivery/finalized.blend'),'--textures',str(folder),'--asset','Covey26',
            '--config',str(cfg),'--out',str(path),'--report',str(out/'export'/(site+'.json'))]
  export.main()
  actual=fingerprint(path);assert actual==reference,(site,'geometry/UV/weights/animations changed')
  rows[site]=dict(glb=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
   region_texels=int(region.sum()),parts=SITES[site],exact_accessor_preservation=True)
 all_regions=np.logical_or.reduce(list(regions.values()));outside={}
 for c in used:
  channels=slice(1,3) if c=='ORM' else slice(None)
  delta=np.max(abs(used[c][:,:,channels]-clean[c][:,:,channels]),axis=2);outside[c]=float(delta[(~all_regions)&(partmap>0)].max())
  assert outside[c]<2/255,(c,'Use changed outside the independently defined sites',outside[c])
 (out/'variants.json').write_text(json.dumps(dict(sites=rows,main_sha256=hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest(),
  contact_ao_note='Outside-site AO can change through the source bump and Monte Carlo contact rays; outside-site assertions compare BaseColor, normal, roughness and metallic. Site-off maps retain all untouched used pixels.',
  method='Two kit 4096 bakes, same UVs; disjoint causal site domains; integer 2048 texel copying; 6-pixel guarded support; all GLB accessors exact',
  maximum_change_outside_sites=outside),indent=2))
 print('WEAR VARIANTS',len(rows),'exact accessor preservation')
if __name__=='__main__':main()
