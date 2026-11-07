"""Verify final export provenance, record tonal range, and assemble contacts.

This measures the files. Native-size artistic judgment is logged in REVIEW.md.
Docs are an explicit later target, after that judgment.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from external import bundle
from render_batch import frames,recipe_hash
from finish_views import SHOTS

def contact(paths,dest,tile=600,columns=3):
 paths=list(paths);cell=round(tile*.72)+30
 out=Image.new('RGB',(tile*columns,cell*((len(paths)+columns-1)//columns)),(224,224,215));d=ImageDraw.Draw(out)
 for i,path in enumerate(paths):
  im=Image.open(path).convert('RGB');im.thumbnail((tile,cell-30));x=i%columns*tile;y=i//columns*cell
  out.paste(im,(x+(tile-im.width)//2,y+30));d.text((x+7,y+7),path.stem,fill=(20,30,24))
 dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest,quality=90)
 return out

def main():
 values={};folder=Path('renders/final');names=frames()+['fixtures-sheet','holes-sheet']
 for name in names:
  path=folder/(name+'.png');meta=json.loads(path.with_suffix('.json').read_text())
  assert meta['sha256']==bundle(meta['source']),(path,'stale delivery')
  assert meta['recipe_sha256']==recipe_hash(),(path,'stale render recipe')
  if 'turnaround_recipe_sha256' in meta.get('context',{}):assert meta['context']['turnaround_recipe_sha256']==hashlib.sha256(Path('src/turnaround.py').read_bytes()).hexdigest(),(path,'stale isolated turnaround')
  if 'catalog_recipe_sha256' in meta.get('context',{}):assert meta['context']['catalog_recipe_sha256']==hashlib.sha256(Path('src/catalog.py').read_bytes()).hexdigest(),(path,'stale catalog')
  assert meta['engine']==('BLENDER_EEVEE' if name=='eevee' else 'CYCLES')
  im=Image.open(path).convert('RGB');assert im.width>=800
  rgb=np.asarray(im,float)/255;y=rgb@np.array([.2126,.7152,.0722])
  values[name]=dict(width=im.width,luma_percentiles=np.percentile(y,[1,5,50,95,99]).tolist(),white_clipped_fraction=float(np.mean(np.all(rgb>=.999,axis=-1))))
  if name.endswith(('hero','dusk')):assert abs(meta['eye_height']['eye_above_imported_support_m']-1.65)<1e-5 and 35<=meta['camera']['lens']<=50
  if name=='fixture':assert abs(meta['scale_silhouette']['measured_height_m']-1.8)<1e-5
 pairs=[]
 for name in SHOTS:
  path=Path('renders/finish-fixes')/(name+'-pair.jpg');assert Image.open(path).width>=1600;pairs.append(path)
  a,b=[json.loads(path.with_name(prefix+name+'.json').read_text()) for prefix in ('before-','after-')]
  assert a['camera']==b['camera'];assert b['sha256']==bundle(b['source'])
 photo_paths=[]
 for directory in ('look-matches','source-matches'):
  photo=[]
  for name in ('period_classic_green','period_lighthouse','period_castle'):
   path=Path('renders')/directory/(name+'-pair.jpg');assert Image.open(path).width>=1600
   meta=json.loads(path.with_name(name+'.json').read_text());assert meta['sha256']==bundle(meta['source']);photo.append(path)
  contact(photo,Path('renders')/directory/'contact.jpg',800);photo_paths+=photo
 contact([folder/(n+'.png') for n in names],folder/'contact.jpg')
 contact(pairs,Path('renders/finish-fixes/contact.jpg'),800)
 Path('build/tonal-review.json').write_text(json.dumps(values,indent=2))
 Path('build/render-check.json').write_text(json.dumps(dict(passed=True,scope='Provenance, camera, dimensions and tonal measurements; artistic judgment is separate in REVIEW.md',export_frames=len(names),same_camera_pairs=len(pairs),photo_pairs=len(photo_paths),values=values),indent=2))
 print('FINAL RENDER CHECK PASS',len(names),'export frames;',len(pairs),'same-camera pairs;',len(photo_paths),'photo/source-field pairs')

def docs():
 folder=Path('renders/final');out=Path('docs');out.mkdir(exist_ok=True)
 selections={
 'classic':[folder/'classic-hero.png'],
 'adventure':[folder/'adventure-hero.png'],
 'dusk':[folder/'classic-dusk.png',folder/'adventure-dusk.png'],
 'layouts':[folder/'classic-above.png',folder/'adventure-above.png'],
 'details':[folder/(n+'.png') for n in ('tee','cup','waterfall','clubhouse','fixture','fixtures-sheet','holes-sheet','eevee')]}
 for name,files in selections.items():
  im=Image.open(files[0]).convert('RGB') if len(files)==1 else contact(files,Path('build')/(name+'-docs-contact.jpg'),800,2)
  im.thumbnail((1600,1600));dest=out/(name+'.jpg')
  for quality in range(90,39,-3):
   im.save(dest,quality=quality,optimize=True,progressive=True)
   if dest.stat().st_size<=200000:break
  assert dest.stat().st_size<=200000 and Image.open(dest).width<=1600
  print('DOC',dest,Image.open(dest).size,dest.stat().st_size)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args();docs() if a.docs else main()
