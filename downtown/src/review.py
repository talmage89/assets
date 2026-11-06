"""Audit exported evidence and compose ignored review sheets."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np
import sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.fonts import find_font
sys.path.insert(0,str(Path(__file__).parent))
from delivery import bundle_hash

def audit_checkpoint(folder):
 """Verify the image evidence belongs to the current exported geometry."""
 expected={r:['hero','dusk','across','above','rear'] for r in ('midwest','western','northeast','southern')}
 expected['midwest']+=['cornice_profile','scale','awning','storefront','window','cornice','corner','ghost','escape']
 expected['southern']+=['gallery']
 expected['northeast']+=['storefront','hood'];views=[]
 def check(region,name,base):
  provenance=json.loads((base/region/'provenance.json').read_text())[name]
  source=Path(provenance['source']);assert provenance['sha256']==hashlib.sha256(source.read_bytes()).hexdigest(),(region,name,'stale export')
  for bundle in provenance.get('bundles',[]):assert bundle_hash(Path(bundle['path']))==bundle['sha256'],(region,name,'stale image/buffer bundle')
  street=provenance['street_bundle'];assert bundle_hash(Path(street['path']))==street['sha256'],(region,name,'stale exported pavement')
  assert provenance['engine']=='CYCLES',(region,name,'checkpoint requires Cycles')
  path=base/region/(name+'.png')
  with Image.open(path) as im:im.verify()
  return provenance
 for region,names in expected.items():
  for name in names:
   item=check(region,name,folder);views.append(str(folder/region/(name+'.png')))
   if name in ('hero','dusk'):
    assert 35<=item['camera']['lens']<=50 and abs(item['camera']['location'][2]-1.60)<1e-6
 calibration=json.loads(Path('build/cameras.json').read_text());pairs=[]
 for name,camera in calibration.items():
  check(camera['region'],name,Path('renders/matches'));path=Path('renders/matches')/(name+'-pair.jpg')
  with Image.open(path) as im:im.verify()
  pairs.append(dict(path=str(path),residual_rms_pixels=camera['residual_rms_pixels'],lens_mm=camera['shot']['lens']))
 hero=check('midwest','hero',folder);cam=hero['camera'];plan=json.loads(Path('build/blocks/midwest/block.json').read_text())
 assert 35<=cam['lens']<=50 and abs(cam['location'][2]-1.60)<1e-6
 assert -2*plan['walk']-plan['road_width']<=cam['location'][1]<=-plan['walk']-plan['road_width']
 assert {v['name'] for v in hero['context']}=={'pickup','crossover','hatchback','light','maple','house'}
 for item in hero['context']:assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
 rgb=np.asarray(Image.open(folder/'midwest/hero.png').convert('RGB'));luma=rgb@np.asarray((.2126,.7152,.0722))
 report=dict(passed=True,views=views,pairs=pairs,hero_camera=cam,hero_display_luma_percentiles=dict(zip(('p01','p05','p50','p95','p99'),np.percentile(luma,[1,5,50,95,99]).tolist())),pixels_with_channel_255=int(np.any(rgb==255,axis=2).sum()),scope='Current exported baked geometry, camera and context provenance; PNG display values are not linear albedo measurements')
 report['town_hero_tones']={}
 for region in expected:
  a=np.asarray(Image.open(folder/region/'hero.png').convert('RGB'));y=a@np.array((.2126,.7152,.0722))
  report['town_hero_tones'][region]=dict(display_luma_percentiles=dict(zip(('p01','p05','p50','p95','p99'),np.percentile(y,[1,5,50,95,99]).tolist())),pixels_with_channel_255=int(np.any(a==255,axis=2).sum()),pixels=int(y.size))
 Path('build/render-check.json').write_text(json.dumps(report,indent=2)+'\n');print('RENDER AUDIT PASS',len(views),'Cycles views,',len(pairs),'photo pairs')

def sheet(paths,out,columns=3,cell=520):
 paths=list(paths)
 if not paths:raise ValueError('No rendered images found')
 rows=(len(paths)+columns-1)//columns;im=Image.new('RGB',(cell*columns,round(cell*.72)*rows),(232,230,220));d=ImageDraw.Draw(im);font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),15)
 for i,p in enumerate(paths):
  a=Image.open(p).convert('RGB');a.thumbnail((cell-16,round(cell*.72)-38));x=(i%columns)*cell;y=(i//columns)*round(cell*.72)
  im.paste(a,(x+(cell-a.width)//2,y+29));d.text((x+10,y+7),str(p).replace('renders/',''),font=font,fill=(30,35,30))
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True);im.save(out,quality=90,optimize=True);print('SHEET',out,len(paths));return out

def storefront_detail(folder):
 """An explicit storefront pair from the same Foster fit, with native render pixels."""
 folder=Path(folder);raw=folder/'raw/foster.png'
 if not raw.exists():return
 c=json.loads(Path('build/cameras.json').read_text())['foster'];box=c['crop']
 render=Image.open(raw).convert('RGB');cut=round(render.height*(240-box[1])/(box[3]-box[1]))
 render=render.crop((0,cut,render.width,render.height))
 photo=ImageOps.exif_transpose(Image.open(c['photo'])).convert('RGB').crop((box[0],240,box[2],box[3]))
 photo=photo.resize(render.size,Image.Resampling.LANCZOS)
 width,height=render.size;pair=Image.new('RGB',(2*width,height+104),(238,239,236));d=ImageDraw.Draw(pair)
 font=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),22)
 pair.paste(render,(0,64));pair.paste(photo,(width,64))
 d.text((18,14),'Foster storefront / native exported render pixels',font=font,fill=(22,38,29))
 d.text((width+18,14),'HABS IN-86 / same fitted frame crop',font=font,fill=(22,38,29))
 d.text((18,height+73),'Same Foster calibration; monochrome photograph checks form only.',font=font,fill=(49,64,52))
 path=folder/'foster_storefront-pair.jpg';pair.save(path,quality=94,optimize=True)
 print('STOREFRONT DETAIL',path,render.size,'native pixels per panel')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--folder',default='renders/checkpoint');p.add_argument('--out');a=p.parse_args()
 for folder in ('renders/matches','renders/source-matches'):storefront_detail(folder)
 if Path(a.folder)==Path('renders/checkpoint'):audit_checkpoint(Path(a.folder))
 files=sorted(Path(a.folder).glob('*/*.png'))
 if Path(a.folder)==Path('renders/checkpoint') and Path('renders/eevee/midwest/hero.png').exists():files.append(Path('renders/eevee/midwest/hero.png'))
 sheet(files,a.out or a.folder+'/contact.jpg')
 if Path('renders/matches').exists():
  pairs=sorted(Path('renders/matches').glob('*-pair.jpg'))
  if pairs:sheet(pairs,'renders/matches/contact.jpg',1,1600)
