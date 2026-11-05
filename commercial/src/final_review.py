"""Final contact sheets, current-export audit and bounded portfolio JPEGs."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from review import sheet,FONT
from review_look import digest
from context import recipe,bundle
NAMES=('hero','above','dispenser','canopy','column','entry','sign','rear','services','asphalt','landscape','dusk','scale','front','side','back','top')
PAIRS=('period_canopy','period_dispenser','used_forecourt','used_store','used_asphalt')


def stack(entries,path,width=1800):
 rows=[]
 for label,p in entries:
  im=Image.open(p).convert('RGB');im.thumbnail((width-16,1050),Image.Resampling.LANCZOS)
  row=Image.new('RGB',(width,im.height+48),'#e8e9e6');row.paste(im,((width-im.width)//2,40));ImageDraw.Draw(row).text((12,8),label,font=FONT,fill='#26352f');rows.append(row)
 canvas=Image.new('RGB',(width,sum(im.height for im in rows)),'#e8e9e6');y=0
 for im in rows:canvas.paste(im,(0,y));y+=im.height
 canvas.save(path,quality=92,optimize=True)


def jpg(source,destination):
 im=Image.open(source).convert('RGB');im.thumbnail((1600,10000),Image.Resampling.LANCZOS)
 for quality in range(94,44,-2):
  im.save(destination,quality=quality,optimize=True)
  if destination.stat().st_size<=200000:return
 raise AssertionError('Documentation cannot meet byte budget')



def portfolio_views(root,eevee):
 canvas=Image.new('RGB',(2100,1300),'#e8e9e6');draw=ImageDraw.Draw(canvas)
 def tile(label,path,x,y,width,maxheight):
  im=Image.open(path).convert('RGB');im.thumbnail((width-16,maxheight-42),Image.Resampling.LANCZOS)
  draw.text((x+10,y+8),label,font=FONT,fill='#26352f');canvas.paste(im,(x+(width-im.width)//2,y+40));return im.height+48
 for i,name in enumerate(('front','side','back')):tile(name,root/(name+'.png'),i*700,0,700,185)
 left=tile('top',root/'top.png',0,185,1050,1100)
 right=tile('scale',root/'scale.png',1050,185,1050,730)
 right+=tile('Eevee',eevee,1050,185+right,1050,460)
 canvas.crop((0,0,2100,185+max(left,right))).save(root/'portfolio-views.jpg',quality=94,optimize=True)

def main(docs=False):
 root=Path('renders/final');details=[(n,root/(n+'.png')) for n in NAMES]
 family=[(f'{s} / {n}',root/'seeds'/str(s)/(n+'.png')) for s in (101,102,103,104) for n in ('above','street')]
 pairs=[(n,Path('renders/look-matches')/(n+'-pair.jpg')) for n in PAIRS]
 fixes=[(p.stem,p) for p in sorted(Path('renders/delivery-fixes').glob('*-before-after.jpg'))];assert len(fixes)==8
 sheet(details,root/'details.jpg',3,(800,550));sheet(family,root/'family.jpg',2,(960,640));stack(pairs,root/'matched-pairs.jpg')
 sheet(fixes,root/'fixes.jpg',2,(900,440));sheet([(p.stem,p) for p in sorted(Path('renders/look-matches').glob('*-values.jpg'))],root/'values.jpg',2,(900,500))
 eevee=Path('renders/final-eevee/hero.png');sheet(details+family+[('Eevee',eevee)]+pairs+fixes,root/'contact.jpg',3,(750,500))
 rows=[]
 for folder in (root,Path('renders/look-matches'),eevee.parent):
  for p in folder.rglob('provenance.json'):
   for n,r in json.loads(p.read_text()).items():
    image=p.parent/(n+'.png');assert digest(image)==r['image_sha256'];assert digest(r['source'])==r['sha256'],('Stale export',image)
    assert r['source'].endswith('.gltf') and r['recipe_sha256']==recipe(),('Stale recipe',image)
    assert r['engine']==('BLENDER_EEVEE' if p.parent==eevee.parent else 'CYCLES')
    if n=='used_asphalt':assert r['comparison_recipe_sha256']==hashlib.sha256((HERE/'asphalt_match.py').read_bytes()).hexdigest()
    if r.get('ground'):
     assert digest(HERE.parents[1]/r['ground']['source'])==r['ground']['sha256']
     for ctx in r['ground'].get('neighbor_dependencies',[]):assert bundle(HERE.parents[1]/ctx['source'])==ctx
    rows.append(str(image))
 assert len(rows)==31,(len(rows),rows)
 values=json.loads(Path('renders/look-matches/values.json').read_text());surfaces=json.loads(Path('build/value-surface-check.json').read_text());assert surfaces['passed']
 from values import CASES
 for name,v in values['rows'].items():
  assert list(v['render_box'])==list(CASES[name]['render_box'])==surfaces['patches'][name]['render_box']
  assert v['image_sha256']==surfaces['patches'][name]['image_sha256']==digest(Path('renders/look-matches')/(v['pair']+'.png'))
 from preserve import run
 run()
 check=json.loads(Path('build/delivery-check.json').read_text());assert check['passed']
 result=dict(passed=True,views=rows,cycles_views=30,eevee_views=1,new_gpu_mib=check['new_gpu_mib'],contact=str(root/'contact.jpg'),scope='Current exported geometry/buffers/maps, original sky/sun recipe, real context and image hashes; visual audit logged separately in REVIEW')
 Path('build/final-view-check.json').write_text(json.dumps(result,indent=2))
 if docs:
  out=Path('docs');out.mkdir(exist_ok=True)
  sheet([(n,root/(n+'.png')) for n in ('dispenser','entry','sign','asphalt')],root/'portfolio-details.jpg',2,(900,630))
  sheet([(str(s),root/'seeds'/str(s)/'street.png') for s in (101,102,103,104)],root/'portfolio-family.jpg',2,(900,400))
  portfolio_views(root,eevee)
  for src,name in [('hero.png','hero'),('portfolio-details.jpg','details'),('portfolio-family.jpg','family'),('portfolio-views.jpg','views'),('dusk.png','dusk')]:jpg(root/src,out/('gas-'+name+'.jpg'))
  for p in out.glob('gas-*.jpg'):assert Image.open(p).width<=1600 and p.stat().st_size<=200000
 print('FINAL_REVIEW',len(rows),'current views; docs',docs)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--docs',action='store_true');main(p.parse_args().docs)
