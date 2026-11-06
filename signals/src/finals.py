"""Final family evidence and compact docs, with export provenance checks."""
import argparse,json,shutil,sys,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).parent)]
from kit.contact import contact,review_sheet,FONT
from deliver import bundle

def jpg(im,path,width=1600,limit=200000):
 im=im.convert('RGB');im.thumbnail((width,20000),Image.Resampling.LANCZOS)
 for quality in range(94,39,-2):
  im.save(path,quality=quality,optimize=True)
  if path.stat().st_size<=limit:return
 raise AssertionError(('Docs compression failed',path))

def run(docs=False):
 out=Path('renders/final');out.mkdir(parents=True,exist_ok=True)
 gallery_recipe=hashlib.sha256(Path('src/gallery.py').read_bytes()).hexdigest()
 def gallery_receipt(path):
  meta=json.loads(path.with_suffix('.json').read_text());assert meta['recipe_sha256']==gallery_recipe,('Stale studio recipe',path)
  for p,digest in meta['sources'].items():assert bundle(p)==digest,('Stale studio export',path)
  return meta
 order=['202/hero','202/dusk','201/hero','201/above','201/driver','202/above','202/driver','203/above','203/driver','204/above','204/driver','201/head_lit','201/head_dark','201/lens_detail','201/pavement','201/connection','204/span_hanger','201/cabinet_open','201/button','201/dusk']
 for rel in order:
  source=Path('renders/checkpoint')/(rel+'.png');meta=json.loads(source.with_suffix('.json').read_text());assert meta['bundle_sha256']==bundle(meta['source'])
  target=out/(rel+'.png');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target);shutil.copy2(source.with_suffix('.json'),target.with_suffix('.json'))
 files=[out/(rel+'.png') for rel in order]
 gallery=[]
 for part in ('Head_three','Head_fya','PedHead','PushButtonPost','MastArm','Pedestal','Cabinet'):
  for view in ('front','side','back','top'):
   path=out/'gallery'/part/(view+'.png');gallery_receipt(path)
   gallery.append(path)
 review_sheet([[out/'gallery'/part/(v+'.png') for v in ('front','side','back','top')] for part in ('Head_three','Head_fya','PedHead','PushButtonPost','MastArm','Pedestal','Cabinet')],out/'turnarounds.jpg',width=2400,title='Waycroft reusable parts / front, side, rear, top / exported shared maps')
 sheet=Image.open(out/'turnarounds.jpg').convert('RGB');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype(FONT,20)
 for row,part in enumerate(('Head_three','Head_fya','PedHead','PushButtonPost','MastArm','Pedestal','Cabinet')):
  for col,view in enumerate(('front','side','back','top')):
   x=20+col*594;y=90+row*636+578
   draw.rectangle((x,y,x+578,y+42),fill=(232,233,229));draw.text((x,y+10),part.replace('_',' ')+' / '+view,font=font,fill=(37,45,40))
 sheet.save(out/'turnarounds.jpg',quality=92,optimize=True)
 extra=[out/'scale/MastArm/scale.png',out/'eevee/202/hero.png'];files+=gallery+extra
 gallery_receipt(extra[0]);eevee=json.loads(extra[1].with_suffix('.json').read_text());assert eevee['bundle_sha256']==bundle(eevee['source'])
 for path in extra:assert path.exists(),path
 contact(files,out/'contact.jpg',width=2400,title='Waycroft / final exported equipment / Cycles except labeled Eevee',captions={str(p):str(p.relative_to(out).with_suffix('')) for p in files})
 contact([out/(rel+'.png') for rel in order if rel.endswith(('above','driver'))],out/'four-towns.jpg',width=2400,title='Four road plans / four towns / above and driver')
 contact([out/(rel+'.png') for rel in ('201/head_lit','201/head_dark','201/lens_detail','201/pavement','201/connection','204/span_hanger','201/cabinet_open','201/button')],out/'details.jpg',width=2000,title='Waycroft / optics, construction and service')
 recipe=hashlib.sha256(b''.join((Path('src')/n).read_bytes() for n in ('render.py','setting.py','plan.py'))).hexdigest()
 for folder in ('renders/matches','renders/source-matches'):
  for path in Path(folder).glob('*.png'):
   meta=json.loads(path.with_suffix('.json').read_text());assert meta['recipe_sha256']==recipe,('Stale pair recipe',path)
   if meta['source'].endswith('.gltf'):assert meta['bundle_sha256']==bundle(meta['source']),('Stale pair export',path)
   else:assert meta['sha256']==hashlib.sha256(Path(meta['source']).read_bytes()).hexdigest(),('Stale pair source',path)
 pairs=sorted(Path('renders/matches').glob('*-pair.jpg'));review_sheet([[p] for p in pairs],out/'photo-pairs.jpg',width=2400,title='Exported equipment photo pairs / nominal pavement comparison / balanced references')
 # Four distinct exported phase states, repeated with explicit holds/flashes.
 motion=out/'motion';names=['green_fya_on','green_fya_off','green_fya_on','green_fya_off','yellow','red'];durations=[900,500,500,500,1400,2400]
 for name in set(names):gallery_receipt(motion/(name+'.png'))
 frames=[Image.open(motion/(n+'.png')).convert('RGB') for n in names]
 for frame in frames:frame.thumbnail((800,600),Image.Resampling.LANCZOS)
 chart=Image.new('RGB',(frames[0].width*4,frames[0].height))
 for i,index in enumerate((0,1,4,5)):chart.paste(frames[index],(i*frames[0].width,0))
 gif=motion/'signals-cycle.gif'
 for colors in (128,96,64):
  palette=chart.quantize(colors=colors,method=Image.Quantize.MEDIANCUT);indexed=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
  indexed[0].save(gif,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=True,disposal=1)
  if gif.stat().st_size<=450000:break
 assert gif.stat().st_size<=450000,(gif,gif.stat().st_size)
 recipe=dict(phase_frames=names,durations_ms=durations,bytes=gif.stat().st_size,width=indexed[0].width,scope='Demonstration of named material states; not a traffic timing plan')
 (motion/'sequence.json').write_text(json.dumps(recipe,indent=2))
 if docs:
  folder=Path('docs');folder.mkdir(exist_ok=True)
  for name,source in [('hero',out/'202/hero.png'),('towns',out/'four-towns.jpg'),('parts',out/'turnarounds.jpg'),('details',out/'details.jpg'),('dusk',out/'202/dusk.png')]:jpg(Image.open(source),folder/('signals-'+name+'.jpg'))
  shutil.copy2(gif,folder/'signals-cycle.gif')
  (Path('build/docs.json')).write_text(json.dumps({str(p):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in folder.iterdir()},indent=2))
 from values import run as measure_values
 measure_values()
 print('FINALS',len(files),'views;',len(pairs),'photo pairs; GIF',gif.stat().st_size,'bytes; docs',docs)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');a=p.parse_args();run(a.docs)
