"""Local review contact sheets and tonal receipts; never writes docs/."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from render_batch import recipe_hash

def contact(paths,dest,tile=600):
 paths=list(paths);width=tile*3;cell=round(tile*.72)+30;out=Image.new('RGB',(width,cell*((len(paths)+2)//3)),(224,224,215));d=ImageDraw.Draw(out)
 for i,p in enumerate(paths):
  im=Image.open(p).convert('RGB');im.thumbnail((tile,cell-30));x=i%3*tile;y=i//3*cell;out.paste(im,(x,y+30));d.text((x+7,y+7),p.stem,fill=(20,30,24))
 out.save(dest,quality=90)

def main():
 files=sorted(Path('renders/lookdev').glob('*.png'));assert files,'No GLB renders'
 expected={k+'-'+v for k in ('classic','adventure') for v in ('ground','above','hero','dusk')}|set('tee cup border waterfall pond fixture bridge clubhouse lighthouse castle bank planting road sign'.split())
 assert {p.stem for p in files}==expected,('Incomplete frame inventory',expected-{p.stem for p in files})
 contact(files,'renders/lookdev/contact.jpg');values={}
 for p in files:
  a=np.asarray(Image.open(p).convert('RGB'),dtype=float)/255;y=a@np.array([.2126,.7152,.0722]);meta=json.loads(p.with_suffix('.json').read_text());source=Path(meta['source']);assert source.suffix=='.glb' and meta['sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
  assert meta['engine']=='CYCLES' and a.shape[1]>=800,(p,meta['engine'],a.shape)
  assert meta.get('recipe_sha256')==recipe_hash(),('Stale frame recipe',p)
  if p.stem.endswith(('hero','dusk')):
   assert abs(meta['eye_height']['eye_above_imported_support_m']-1.65)<1e-5
   assert 35<=meta['camera']['lens']<=50
  values[p.stem]=dict(display_luma_percentiles=np.percentile(y,[1,5,50,95,99]).tolist(),white_clipped_fraction=float(np.mean(np.all(a>=.999,axis=-1))),camera=meta['camera'])
 Path('build/tonal-review.json').write_text(json.dumps(values,indent=2))
 pairs=list(Path('renders/look-matches').glob('*-pair.jpg'))
 assert len(pairs)==3,('Missing photo pairs',len(pairs))
 visibility=json.loads(Path('build/landmark-visibility.json').read_text())
 for key,row in visibility.items():
  assert row['sha256']==hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()
  assert max(p['first_opaque_surface_before_anchor_m'] for p in row['probes'])<1.2
 source_pairs=list(Path('renders/source-matches').glob('*-pair.jpg'));assert len(source_pairs)==3
 # A composed pair alone can outlive its GLB. Verify the actual imported
 # image receipts and the measured source-field resolution before accepting it.
 fits=json.loads(Path('build/photo-calibration.json').read_text())
 from photo_matches import LIGHTING
 match_fingerprint=hashlib.sha256(Path('src/matches.py').read_bytes()).hexdigest()
 for directory,is_source in (('renders/look-matches',False),('renders/source-matches',True)):
  for key,fit in fits.items():
   png=Path(directory)/(key+'.png');meta=json.loads(png.with_suffix('.json').read_text());source=Path(meta['source'])
   assert meta['engine']=='CYCLES' and Image.open(png).width>=800
   assert source.suffix=='.glb' and meta['sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
   assert meta['recipe_sha256']==recipe_hash() and meta['context']['match_recipe_sha256']==match_fingerprint
   expected=dict(fit['shot'],**LIGHTING[key]);expected['aspect']=(fit['crop'][2]-fit['crop'][0])/(fit['crop'][3]-fit['crop'][1]);expected=json.loads(json.dumps(expected))
   assert meta['requested_camera']==expected,('Stale calibrated camera',png)
   if is_source:
    sizes=meta['context']['source_field_sizes'];assert set(sizes)=={'BaseColor','ORM','Normal'}
    assert all(r['pixels']==[4096,4096] and r['shader_nodes']>0 for r in sizes.values())
    for ch,digest in meta['context']['source_fields'].items():
     field=Path('textures/bake' if ch=='Normal' else 'build/procedural')/('T_Minigolf_'+ch+'.png')
     assert digest==hashlib.sha256(field.read_bytes()).hexdigest()
 if pairs:contact(pairs,'renders/look-matches/contact.jpg',800)
 if source_pairs:contact(source_pairs,'renders/source-matches/contact.jpg',800)
 compare=Path('renders/comparison');rows=[]
 comparison_fingerprint=hashlib.sha256(Path('src/comparison.py').read_bytes()).hexdigest()
 for after in sorted(compare.glob('after-*.png')):
  before=after.with_name(after.name.replace('after-','before-',1))
  if not before.exists():continue
  a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');assert a.size==b.size and a.width>=800
  before_meta=json.loads(before.with_suffix('.json').read_text());after_meta=json.loads(after.with_suffix('.json').read_text());assert before_meta['camera']==after_meta['camera'],('Comparison camera mismatch',after)
  assert before_meta['recipe_sha256']==after_meta['recipe_sha256']==recipe_hash()
  for meta in (before_meta,after_meta):
   assert meta['sha256']==hashlib.sha256(Path(meta['source']).read_bytes()).hexdigest(),('Stale comparison source',after)
   assert meta['context']['comparison_recipe_sha256']==comparison_fingerprint,('Stale comparison recipe',after)
  staged='staged' in before_meta.get('context',{}).get('comparison_scope','')
  label='BEFORE FIXTURE GEOMETRY / REVISED PLACEMENT' if staged else 'ACCEPTED CHECKPOINT / BEFORE'
  sheet=Image.new('RGB',(a.width*2,a.height+40),(230,230,220));sheet.paste(a,(0,40));sheet.paste(b,(a.width,40));d=ImageDraw.Draw(sheet);d.text((12,10),label,fill='black');d.text((a.width+12,10),'FORM + LOOK REVISION / AFTER',fill='black');sheet.save(compare/(after.stem.removeprefix('after-')+'-pair.jpg'),quality=93);rows.append(compare/(after.stem.removeprefix('after-')+'-pair.jpg'))
 from comparison_batch import KEYS
 assert {p.stem.removesuffix('-pair') for p in rows}==set(KEYS),('Missing same-camera comparisons',len(rows))
 if rows:contact(rows,compare/'contact.jpg',800)
 Path('build/render-check.json').write_text(json.dumps(dict(passed=True,glb_frames=len(files),photo_pairs=len(pairs),source_field_pairs=len(source_pairs),same_camera_pairs=len(rows),minimum_width=800,frames=values),indent=2))
 print('Review receipt',len(files),'GLB frames;',len(pairs),'photo pairs;',len(rows),'same-camera comparisons')
if __name__=='__main__':main()
