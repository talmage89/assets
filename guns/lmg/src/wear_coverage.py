"""Whole-part worn fractions: independent photo observations versus baked GLB.

The shipped mask comes from on/off material differences at the actual visible
imported triangle UVs. Render RGB differences separately prove visibility.
Photographic thresholds retain uncertainty instead of labeling highlights as
known paint loss. No comparison mask is used in asset generation.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageOps
BASE=Path(__file__).resolve().parents[1];sys.path[:0]=[str(BASE.parents[1]),str(BASE/'src')]
from image_masks import raster,bilinear
from look_review import FONT,SMALL,mask_crop
from wear_observations import observed
from finish_parameters import SITES
from final_review import sheet
PREFIXES={
 'receiver':('Receiver_Sheet','Receiver_RearDoubler','SideWell_Housing'),
 'cover':('FeedCover_Shell','FeedCover_PressedBead','FeedCover_SidePress'),
 'cover_top':('FeedCover_Shell',),'rivets':('Receiver_Rivet',),
 'handle':('CarryHandle_Grip',),'flash':('FlashHider',),
 'regulator':('GasRegulator','Regulator_Grip'),
 'ports':('Receiver_Sheet','LinkPort_Rim','ChargingGuide'),
 'feet':('Bipod_Foot',),'box':('Box_Shell','Box_EndRib','Box_MoldRib'),
 'butt':('Stock_Sculpt','Buttpad'),
}
def main():
 out=BASE/(sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else 'renders/final/look-review/coverage');out.mkdir(parents=True,exist_ok=True)
 root=BASE/(sys.argv[sys.argv.index('--root')+1] if '--root' in sys.argv else 'renders/final/beauty');geometry=BASE/(sys.argv[sys.argv.index('--geometry')+1] if '--geometry' in sys.argv else 'build/image-geometry');meta=json.loads((root/'shots.json').read_text());cache={};rows={};entries=[]
 atlas={c:np.asarray(Image.open(BASE/'textures'/('T_Harrow56_'+c+'.png')),float) for c in ('BaseColor','ORM')}
 for site in (sys.argv[sys.argv.index('--sites')+1].split(',') if '--sites' in sys.argv else SITES):
  shot='hero_right' if site=='ports' else 'hero';m=meta[shot];im=np.asarray(Image.open(root/(shot+'.png')).convert('RGB'));h,w=im.shape[:2]
  geo=np.load(geometry/(shot+'.npz'));assert str(geo['sha256'])==m['sha256']
  if shot not in cache:cache[shot]=raster(geo,m,w,h)
  ids,uv=cache[shot];part=np.isin(ids,[i+1 for i,n in enumerate(geo['names']) if str(n).startswith(PREFIXES[site])]);points=np.stack((uv[:,:,0].ravel()*2048,(1-uv[:,:,1].ravel())*2048),1)
  diffs={}
  for c in ('BaseColor','ORM'):
   control=np.asarray(Image.open(BASE/'build/controls'/site/'textures'/('T_Harrow56_'+c+'.png')),float)
   on=bilinear(atlas[c],points).reshape(h,w,-1);off=bilinear(control,points).reshape(h,w,-1);diffs[c]=abs(on-off)
  # BC >=8 encoded levels or roughness >=.06 identifies meaningful material
  # change, independent of whether this lighting happens to show a highlight.
  worn=part&((diffs['BaseColor'][:,:,:3].max(2)>=8)|(diffs['ORM'][:,:,1]>=15))
  photo,pp,pw,note=observed(BASE,site);sensitivity=[float(observed(BASE,site,v)[2].sum()/pp.sum()) for v in (-8,8)]
  row=dict(render_shot=shot,render_part_pixels=int(part.sum()),render_worn_pixels=int(worn.sum()),render_worn_fraction=float(worn.sum()/max(part.sum(),1)),photo_part_pixels=int(pp.sum()),photo_worn_pixels=int(pw.sum()),photo_worn_fraction=float(pw.sum()/pp.sum()),photo_threshold_sensitivity=sorted(sensitivity),photo_observation=note,render_rule='BC on/off max RGB >=8/255 OR roughness on/off >=15/255, at actual visible imported UVs',sha256=m['sha256'])
  off_path=BASE/'renders/final/wear'/site/(shot+'.png')
  if off_path.exists() and root==BASE/'renders/final/beauty':
   off=np.asarray(Image.open(off_path).convert('RGB'),float);visible=worn&(np.max(abs(im.astype(float)-off),axis=2)>=4)
   row['visible_worn_pixels']=int(visible.sum());row['visible_worn_fraction']=float(visible.sum()/max(part.sum(),1));row['visibility_rule']='On/off maximum RGB difference >=4/255 inside physically changed pixels'
  rows[site]=row
  canvas=Image.new('RGB',(1800,1050),'#e7e9e6');d=ImageDraw.Draw(canvas)
  d.text((25,15),site+' / whole-part wear area, actual baked export and native photograph',font=FONT,fill='black')
  for col,(a,p,q,label) in enumerate([(im,part,worn,'Exported '+shot),(photo,pp,pw,'White-balanced photo')]):
   overlay=np.uint8(a).copy();overlay[q]=np.uint8(overlay[q]*.4+np.array((230,125,45))*.6)
   canvas.paste(mask_crop(a,p),(25+900*col,60));canvas.paste(mask_crop(overlay,p),(25+900*col,450))
   frac=row['render_worn_fraction' if col==0 else 'photo_worn_fraction']
   d.text((25+900*col,860),label+' worn fraction %.2f%%'%(100*frac),font=FONT,fill='black')
  import textwrap
  for i,line in enumerate(textwrap.wrap(note['limit'],145)):d.text((25,905+i*27),line,font=SMALL,fill='black')
  d.text((25,1000),'Photo threshold +/-8 levels: %.2f%% to %.2f%%. Bright/dark appearance is not a calibrated material label.'%tuple(100*v for v in sorted(sensitivity)),font=SMALL,fill='black')
  path=out/(site+'-coverage.jpg');canvas.save(path,quality=94);entries.append((site,path))
 (out/'worn-fractions.json').write_text(json.dumps(rows,indent=2));sheet(entries,out/'all-sites.jpg',columns=3,cell=(600,380))
 for site,r in rows.items():print(site,'GLB %.3f%% / PHOTO %.3f%%'%(r['render_worn_fraction']*100,r['photo_worn_fraction']*100),flush=True)
if __name__=='__main__':main()
