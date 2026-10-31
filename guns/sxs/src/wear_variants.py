"""Site-off evidence GLBs from independent kit bakes on identical UVs.

Seven disjoint causal fields use the all-clean bake. The forend's fracture
and point-wear fields overlap; each uses its own single-cause-off source
and bake, retaining the other cause. Integer texel copies preserve all
untouched used pixels. RGB16 normals and every GLB accessor are retained.
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
  # every occupied texel outside this physical domain, including another
  # domain of the same named part in adjacent UV charts.
  valid=mask.copy();block=(partmap>0)&~mask
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
 counterfactual={};provenance={}
 for site in ('forend_edges','forend_points'):
  high=BASE/f'build/delivery/off-{site}.blend';metadata=json.loads(high.with_suffix('.json').read_text())
  assert metadata['wear']==1 and metadata['disabled']==site,(site,'Counterfactual disabled the wrong cause')
  assert metadata['source_sha256']==json.loads((BASE/'build/delivery/high.json').read_text())['source_sha256']
  high_digest=hashlib.sha256(high.read_bytes()).hexdigest()
  projection=json.loads((out/f'off-{site}/precise4k/projection-report.json').read_text())
  assert projection['source_sha256']['high.blend']==high_digest,(site,'Stale counterfactual projection')
  folder=out/f'off-{site}/textures'
  counterfactual[site]={c:read_png(folder/f'T_Covey26_{c}.png') for c in used}
  provenance[site]=dict(disabled_cause=site,retained_other_causes=True,
   high_sha256=high_digest,projection_sha256=hashlib.sha256((out/f'off-{site}/precise4k/projection-report.json').read_bytes()).hexdigest(),
   texture_sha256={c:hashlib.sha256((folder/f'T_Covey26_{c}.png').read_bytes()).hexdigest() for c in used})
 cfg=out/'evidence-export.py';cfg.write_text('import runpy\nglobals().update(runpy.run_path('+repr(str(BASE/'src/export_config.py'))+'))\nDETACHABLES=[]\n')
 reference=fingerprint(BASE/'export/sxs.glb');rows={}
 for site,region in regions.items():
  folder=out/'textures'/site;folder.mkdir(parents=True,exist_ok=True)
  for c,array in used.items():
   result=array.copy();result[region]=counterfactual.get(site,clean)[c][region]
   assert np.array_equal(result[~region],array[~region]),(site,c,'Untouched used pixels changed')
   write_png(folder/f'T_Covey26_{c}.png',result,16 if c=='Normal' else 8)
  Image.fromarray(np.uint8(region)*255).save(out/(site+'-atlas-region.png'))
  path=out/'export'/(site+'-off.glb');path.parent.mkdir(exist_ok=True)
  embedded=sorted(hashlib.sha256(GLB(path).image(i)).hexdigest() for i in range(3)) if path.exists() else []
  expected=sorted(hashlib.sha256((folder/f'T_Covey26_{c}.png').read_bytes()).hexdigest() for c in used)
  current=embedded==expected and fingerprint(path)==reference if path.exists() else False
  sys.argv=['blender','--','--source',str(BASE/'build/delivery/finalized.blend'),'--textures',str(folder),'--asset','Covey26',
            '--config',str(cfg),'--out',str(path),'--report',str(out/'export'/(site+'.json'))]
  if not current:export.main()
  actual=fingerprint(path);assert actual==reference,(site,'geometry/UV/weights/animations changed')
  rows[site]=dict(glb=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
   region_texels=int(region.sum()),parts=SITES[site],exact_accessor_preservation=True,
   bake_source=provenance.get(site,dict(disabled_cause='all use',disjoint_domain=True)))
 all_regions=np.logical_or.reduce(list(regions.values()));outside={};edge_outliers={}
 interior=partmap>0
 for dy,dx in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)):
  interior&=partmap==np.roll(partmap,(dy,dx),axis=(0,1))
 # A single-cause bake must also preserve every other part's surface data.
 # The exported counterfactual copies only this forend's guarded atlas support,
 # but this separate check catches an accidental all-clean source upstream.
 for site,channels_by_name in counterfactual.items():
  unchanged=interior&~regions[site];errors={}
  for c in used:
   channels=slice(1,3) if c=='ORM' else slice(None)
   delta=np.max(abs(used[c][:,:,channels]-channels_by_name[c][:,:,channels]),axis=2)
   errors[c]=float(delta[unchanged].max())
   assert errors[c]<2/255,(site,c,'Single-cause bake changed another part',errors[c])
  rows[site]['maximum_change_other_part_interiors']=errors
 for c in used:
  channels=slice(1,3) if c=='ORM' else slice(None)
  delta=np.max(abs(used[c][:,:,channels]-clean[c][:,:,channels]),axis=2);outside[c]=float(delta[(~all_regions)&interior].max())
  edge=(~all_regions)&(partmap>0)&~interior&(delta>=2/255)
  edge_outliers[c]=dict(pixels=int(edge.sum()),maximum=float(delta[edge].max()) if edge.any() else 0)
  # Independent Cycles bakes need not agree on partially covered chart-edge
  # samples. Restrict the exception to this measured one-pixel boundary; all
  # occupied interiors still have the strict two-code-value assertion below.
  edge_outliers[c]['fraction_of_occupied_texels']=float(edge.sum()/max(1,int((partmap>0).sum())))
  edge_outliers[c]['uv_pixel_coordinates_xy']=np.argwhere(edge)[:,::-1].tolist()
  assert outside[c]<2/255,(c,'Use changed outside the independently defined sites',outside[c])
 (out/'variants.json').write_text(json.dumps(dict(sites=rows,main_sha256=hashlib.sha256((BASE/'export/sxs.glb').read_bytes()).hexdigest(),
  boundary_note='One-pixel UV boundaries have bounded filtering differences between independent bakes. Actual count and maximum are retained. Every untouched site-off texel still comes byte-exactly from the used maps.',
  contact_ao_note='Outside-site AO can change through the source bump and Monte Carlo contact rays; outside-site assertions compare BaseColor, normal, roughness and metallic. Site-off maps retain all untouched used pixels.',
  method='Used and all-clean kit 4096 bakes plus two single-cause-off forend bakes; same UVs; integer 2048 texel copying; 6-pixel guarded support; all GLB accessors exact',
  maximum_change_outside_site_interiors=outside,boundary_filtering_differences=edge_outliers),indent=2))
 print('WEAR VARIANTS',len(rows),'exact accessor preservation')
if __name__=='__main__':main()
