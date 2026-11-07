"""Neutral-balance photos, fit with kit, independently verify, render imports."""
import argparse,json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import numpy as np
from PIL import Image
from kit.photo_match import solve,compose
ROIS={'sunnyvale-2007':(545,1450,590,1480),'michigan-2011':(1550,1200,1640,1240),'castro-2011':(2240,2290,2280,2320),'henderson-used-falls':(210,140,260,190)}
NEUTRALS={'sunnyvale-2007':'sunlit concrete walk','michigan-2011':'sunlit gray concrete','castro-2011':'sunlit pale-gray castle wall','henderson-used-falls':'unclipped shaded white fence panel; mixed sun/shade lighting remains'}

def balance():
 report={}
 for name,rect in ROIS.items():
  im=np.asarray(Image.open('refs/'+name+'.jpg').convert('RGB'),dtype=float)/255
  linear=np.where(im<=.04045,im/12.92,((im+.055)/1.055)**2.4);x0,y0,x1,y1=rect;roi=linear[y0:y1,x0:x1];med=np.median(roi,axis=(0,1));gain=np.exp(np.mean(np.log(med)))/med
  value=linear*gain;rgb=np.where(value<=.0031308,12.92*value,1.055*np.maximum(value,0)**(1/2.4)-.055)
  Image.fromarray(np.uint8(np.clip(rgb,0,1)*255+.5)).save('build/balanced-'+name+'.png')
  report[name]=dict(neutral_roi=rect,linear_channel_gain=gain.tolist(),neutral=NEUTRALS[name],scope='White balance only; exposure and photographic processing remain unknown. Photo is never an asset texture.')
 Path('build/reference-balance.json').write_text(json.dumps(report,indent=2))

def render(args):
 import bpy
 from external import bundle
 from mathutils import Matrix,Vector
 from mathutils.bvhtree import BVHTree
 from kit.photo_match import verify
 from render import render_one
 from photo_matches import SELECTION,LIGHTING
 verify('build/photo-calibration.json');fits=json.loads(Path('build/photo-calibration.json').read_text())
 visibility_path=Path('build/landmark-visibility.json');visibility=json.loads(visibility_path.read_text()) if visibility_path.exists() else {}
 for key,data in fits.items():
  if getattr(args,'key',None) and key!=args.key:continue
  seed,kind=SELECTION[key]
  from render import scene
  source,plan,ctx=scene(seed)
  ctx['match_recipe_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
  root=next(o for o in bpy.context.scene.objects if o.get('module_kind')=='course');vertices=[];faces=[]
  for ob in root.children_recursive:
   if ob.type!='MESH':continue
   ob.data.calc_loop_triangles();off=len(vertices);vertices.extend(ob.matrix_world@v.co for v in ob.data.vertices)
   faces.extend(tuple(off+k for k in t.vertices) for t in ob.data.loop_triangles if not ob.data.materials[t.material_index].name.startswith(('Minigolf_water','Minigolf_glass')))
  opaque=BVHTree.FromPolygons(vertices,faces,all_triangles=True);eye=Vector(data['shot']['location']);probes=[]
  foot=opaque.ray_cast(eye,Vector((0,0,-1)),10)
  if foot[0] is not None:
   ctx['match_eye_height']=dict(above_imported_core_support_m=eye.z-foot[0].z,support_world_m=list(foot[0]))
  if key=='period_lighthouse':
   assert foot[0] is not None and 1.65<eye.z-foot[0].z<1.95,('Lighthouse comparison needs a supported player camera',list(eye),foot)
  for point in data['landmarks_world_m']:
   delta=Vector(point)-eye;hit=opaque.ray_cast(eye,delta.normalized(),delta.length)
   ahead=delta.length-hit[3] if hit[0] is not None else 0
   probes.append(dict(landmark_world_m=point,first_opaque_surface_before_anchor_m=ahead))
  visibility[key]=dict(probes=probes,source=str(source),sha256=bundle(source),scope='Core external-glTF opaque surfaces only; homologous anchors may lie inside their own fixture. Context foliage is judged in the image.')
  visibility_path.write_text(json.dumps(visibility,indent=2))
  assert max(p['first_opaque_surface_before_anchor_m'] for p in probes)<1.2,('Landmark hidden behind another course structure',key,probes)
  if getattr(args,'source_fields',False):
   fields={ch:Path('build/procedural' if ch!='Normal' else 'textures/bake')/('T_Minigolf_'+ch+'.png') for ch in ('BaseColor','ORM','Normal')}
   sizes={}
   for image in list(bpy.data.images):
    for ch,path in fields.items():
     if not image.name.startswith('T_Minigolf_'+ch):continue
     replacement=bpy.data.images.load(str(path.resolve()),check_existing=False);replacement.colorspace_settings.name=image.colorspace_settings.name
     assert tuple(replacement.size)==(4096,4096),('Wrong source-field resolution',ch,list(replacement.size))
     users=0
     for material in bpy.data.materials:
      if not material.use_nodes:continue
      for node in material.node_tree.nodes:
       if node.type=='TEX_IMAGE' and node.image==image:node.image=replacement;users+=1
     assert users,('Source field has no shader users',ch)
     sizes[ch]=dict(pixels=list(replacement.size),shader_nodes=users)
   assert set(sizes)==set(fields),('Missing source-field replacement',sizes)
   ctx['source_field_sizes']=sizes
   ctx['source_field_scope']='Original 4096 source BaseColor/ORM and physical height-field normal on identical imported geometry; GPU-validated deterministic fields compare delivery filtering, not high-poly geometry projection.'
   ctx['source_fields']={ch:hashlib.sha256(path.read_bytes()).hexdigest() for ch,path in fields.items()}

  shot=data['shot'];shot.update(LIGHTING[key]);shot['aspect']=(data['crop'][2]-data['crop'][0])/(data['crop'][3]-data['crop'][1]);args.out='renders/source-matches' if getattr(args,'source_fields',False) else 'renders/look-matches'
  render_one(key,shot,source,plan,dict(ctx,scope='complete placed course in calibrated framing; no rescaling',landmark_rms=data['residual_rms_pixels']),args)
 if not getattr(args,'no_compose',False):compose('build/photo-calibration.json',args.out,args.out)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=('prepare','render','compose'));p.add_argument('--source-fields',action='store_true');p.add_argument('--key');p.add_argument('--no-compose',action='store_true');p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=32);a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 if a.mode=='prepare':
  balance();solve('src/photo_matches.py','build/photo-calibration.json')
  path=Path('build/photo-calibration.json');data=json.loads(path.read_text())
  for key,original,crop_equivalent in (('period_classic_green',35,38),('period_castle',60,60),('period_lighthouse',None,None)):
   data[key]['original_full_frame_equivalent_exif_mm']=original;data[key]['cropped_frame_equivalent_prior_mm']=crop_equivalent;data[key]['lens_status']='Broad course framing; original design homologues, not surveyed reference geometry.'
  path.write_text(json.dumps(data,indent=2))
 elif a.mode=='compose':compose('build/photo-calibration.json','renders/look-matches','renders/look-matches')
 else:render(a)
