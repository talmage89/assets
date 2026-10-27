"""Ignored source-checkpoint contacts and freshness/tonal evidence; no docs JPGs."""
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.fonts import find_font
FONT=ImageFont.truetype(str(find_font('DejaVu Sans','Book')),20)
OUT=Path('renders/ranch');FINAL=OUT/'checkpoint'

def sheet(rows,path,columns=2,width=800):
 tiles=[]
 for title,p in rows:
  im=Image.open(p).convert('RGB');im.thumbnail((width,500));tile=Image.new('RGB',(width,540),(230,232,228));tile.paste(im,((width-im.width)//2,35+(500-im.height)//2));ImageDraw.Draw(tile).text((12,8),title,font=FONT,fill=(25,34,26));tiles.append(tile)
 canvas=Image.new('RGB',(width*columns,540*((len(tiles)+columns-1)//columns)),(230,232,228))
 for i,tile in enumerate(tiles):canvas.paste(tile,((i%columns)*width,(i//columns)*540))
 canvas.save(path,quality=91,optimize=True)


def main():
 checks=json.loads(Path('build/ranch/checks.json').read_text());seeds=[r['seed'] for r in checks['rows']]
 rows=[]
 for seed in seeds:
  for name in ('front','rear'):rows.append((f'Ranch {seed} / {name}',FINAL/'seeds'/str(seed)/(name+'.png')))
 sheet(rows,OUT/'family.jpg',2,1000)
 sheet([(f'Roof {s}',FINAL/'seeds'/str(s)/'roof.png') for s in seeds],OUT/'roofs.jpg',2,900)
 details=[(n,FINAL/(n+'.png')) for n in ('hero','back','roof','eave','window','entry','chimney','scale')]
 details.extend([(f'Period 11 / {n}',FINAL/'period-11'/(n+'.png')) for n in ('entry','window')])
 details.append(('Ranch + colonial, same scale',FINAL/'comparison/types.png'))
 sheet(details,OUT/'contact.jpg',2,900)
 sheet([(n,OUT/'matches'/(n+'-pair.jpg')) for n in ('ranch_summer','ranch_brick_picture','ranch_sun_oblique','ranch_sun_1960')],OUT/'photo-pairs.jpg',1,1400)
 stale=[];views=0
 for folder in [FINAL,FINAL/'period-11',FINAL/'comparison',OUT/'matches',*[FINAL/'seeds'/str(s) for s in seeds]]:
  records=json.loads((folder/'provenance.json').read_text())
  for key,r in records.items():
   views+=1
   if r.get('context'):
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('house_delivery_io',Path('src/delivery_io.py'));module=module_from_spec(spec);spec.loader.exec_module(module)
    cp=Path(r['context']['source']);assert (module.bundle_hash(cp) if cp.suffix=='.gltf' else hashlib.sha256(cp.read_bytes()).hexdigest())==r['context']['sha256']
   if hashlib.sha256(Path(r['source']).read_bytes()).hexdigest()!=r['source_sha256']:stale.append(str(folder/key))
   for file,digest in r.get('material_sha256',{}).items():
    if hashlib.sha256(Path(file).read_bytes()).hexdigest()!=digest:stale.append(file)
 assert not stale,stale
 tonal=json.loads((FINAL/'tonal.json').read_text())
 assert tonal['clipped_white_fraction']<.005,tonal
 report=dict(passed=True,views=views,seeds=seeds,tonal=tonal,stage='source checkpoint only; no ranch bake or final delivery',contacts=[str(OUT/n) for n in ('family.jpg','roofs.jpg','contact.jpg','photo-pairs.jpg')])
 Path('build/ranch/view-check.json').write_text(json.dumps(report,indent=2));print('RANCH_VIEWS',views,'fresh; source tonal check',tonal)


if __name__=='__main__':main()
