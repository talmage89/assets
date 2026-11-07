"""Neutral-balance photos, fit with kit, independently verify, render imports."""
import argparse,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
import numpy as np
from PIL import Image
from kit.photo_match import solve,compose
ROIS={'sunnyvale-2007':(545,1450,590,1480),'michigan-2011':(1550,1200,1640,1240),'castro-2011':(2240,2290,2280,2320)}

def balance():
 report={}
 for name,rect in ROIS.items():
  im=np.asarray(Image.open('refs/'+name+'.jpg').convert('RGB'),dtype=float)/255
  linear=np.where(im<=.04045,im/12.92,((im+.055)/1.055)**2.4);x0,y0,x1,y1=rect;roi=linear[y0:y1,x0:x1];med=np.median(roi,axis=(0,1));gain=np.exp(np.mean(np.log(med)))/med
  value=linear*gain;rgb=np.where(value<=.0031308,12.92*value,1.055*np.maximum(value,0)**(1/2.4)-.055)
  Image.fromarray(np.uint8(np.clip(rgb,0,1)*255+.5)).save('build/balanced-'+name+'.png')
  report[name]=dict(neutral_roi=rect,linear_channel_gain=gain.tolist(),neutral='sunlit concrete walk' if 'sunny' in name else ('sunlit gray concrete' if 'michigan' in name else 'sunlit pale-gray castle wall'),scope='White balance only; exposure and photographic processing remain unknown. Photo is never an asset texture.')
 Path('build/reference-balance.json').write_text(json.dumps(report,indent=2))

def render(args):
 import bpy
 from mathutils import Matrix
 from kit.photo_match import verify
 from render import render_one
 from photo_matches import SELECTION,LIGHTING
 verify('build/photo-calibration.json');fits=json.loads(Path('build/photo-calibration.json').read_text())
 for key,data in fits.items():
  seed,kind=SELECTION[key];bpy.ops.wm.read_factory_settings(use_empty=True);source=Path(f'export/Minigolf-{seed}.gltf');bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
  if kind=='hole':root=next(o for o in bpy.context.scene.objects if o.get('module_kind')=='hole' and o.get('hole_number')==1)
  else:root=next(o for o in bpy.context.scene.objects if o.get('fixture_kind')==kind)
  keep={root,*root.children_recursive};root.parent=None;root.matrix_world=Matrix.Identity(4)
  for o in list(bpy.context.scene.objects):
   if o not in keep:bpy.data.objects.remove(o,do_unlink=True)
  import context,geometry as F
  context.palette();floor=F.root('Matched neutral ground');F.box('Matched ground',(0,0,-.04),(20000,20000,.08),'grass' if kind!='hole' else 'concrete',floor,0)
  shot=data['shot'];shot.update(LIGHTING[key]);shot['aspect']=(data['crop'][2]-data['crop'][0])/(data['crop'][3]-data['crop'][1]);args.out='renders/matches'
  render_one(key,shot,source,{},dict(scope='isolated original export in calibrated framing; no rescaling',landmark_rms=data['residual_rms_pixels']),args)
 compose('build/photo-calibration.json','renders/matches','renders/matches')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=('prepare','render','compose'));p.add_argument('--width',type=int,default=1000);p.add_argument('--samples',type=int,default=32);a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 if a.mode=='prepare':
  balance();solve('src/photo_matches.py','build/photo-calibration.json')
  path=Path('build/photo-calibration.json');data=json.loads(path.read_text())
  for key,original,crop_equivalent in (('period_classic_green',35,96),('period_castle',60,200),('period_lighthouse',None,360)):
   data[key]['original_full_frame_equivalent_exif_mm']=original;data[key]['cropped_frame_equivalent_prior_mm']=crop_equivalent;data[key]['lens_status']='Estimated framing of different original designs; original EXIF/crop prior recorded separately; Sunnyvale equivalent is estimated from its compact-camera lens.'
  path.write_text(json.dumps(data,indent=2))
 elif a.mode=='compose':compose('build/photo-calibration.json','renders/matches','renders/matches')
 else:render(a)
