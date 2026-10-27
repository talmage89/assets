"""Freshness gates and final-only portfolio JPGs, leaving colonial docs intact."""
import argparse,hashlib,json,sys
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from ranch_review import sheet
from delivery_io import bundle_hash


def main(a):
 seeds=list(map(int,a.seeds.split(',')));base=Path('renders/ranch/final');family=Path('renders/ranch/final-seeds');pairs=Path('renders/ranch/final-matches')
 sheet([(n,base/(n+'.png')) for n in ('front','side','rear','top')],base/'turnaround.jpg',2,900)
 sheet([(n,base/(n+'.png')) for n in ('eave','window','entry','chimney')],base/'details.jpg',2,1000)
 sheet([(f'{s} / {n}',family/str(s)/(n+'.png')) for s in seeds for n in ('front','rear')],base/'family.jpg',2,1100)
 sheet([(f'Roof {s}',family/str(s)/'roof.png') for s in seeds],base/'roofs.jpg',2,900)
 sheet([(n,pairs/(n+'-pair.jpg')) for n in ('ranch_summer','ranch_brick_picture','ranch_sun_oblique','ranch_sun_1960')],pairs/'pairs.jpg',1,1600)
 paths=[(n,base/(n+'.png')) for n in ('hero','front','side','rear','back','top','roof','eave','window','entry','chimney','scale')]
 paths.extend([('Eevee',Path('renders/ranch/final-eevee/hero.png')),('Street',Path('renders/ranch/street/street.png'))])
 paths.extend([(f'{s} / {n}',family/str(s)/(n+'.png')) for s in seeds for n in ('front','rear','roof')])
 paths.extend([(f'Period 11 / {n}',family/'period-11'/(n+'.png')) for n in ('entry','window')])
 sheet(paths,base/'contact.jpg',3,800)
 views=[]
 for folder in (base,family/'period-11',pairs,Path('renders/ranch/final-eevee'),*[family/str(s) for s in seeds]):
  for name,row in json.loads((folder/'provenance.json').read_text()).items():
   source=Path(row['source']);assert source.suffix=='.gltf' and bundle_hash(source)==row['source_sha256'],(folder,name,'stale export')
   for file,digest in row['material_sha256'].items():assert hashlib.sha256(Path(file).read_bytes()).hexdigest()==digest
   assert row['stage']=='baked ranch delivery; shared external images';assert (folder/(name+'.png')).exists();views.append(str(folder/(name+'.png')))
 street=json.loads(Path('renders/ranch/street/provenance.json').read_text())
 for row in street['houses']:assert bundle_hash(Path(row['source']))==row['bundle_sha256']
 for row in street['context']:assert hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()==row['sha256']
 tonal=json.loads((base/'tonal.json').read_text());assert tonal['clipped_white_fraction']<.001
 band=None
 if json.loads((base/'provenance.json').read_text())['hero']['seed']==12:
  band=json.loads((base/'eave-band.json').read_text())
  assert .4572<=band['median_band_height_m']<=.6858,band['median_band_height_m']
  assert abs(band['band_encoded_y']-band['shaded_side']['encoded_y'])<.03
  assert band['ground_shadow_in_frame']
 assert abs(street['eye_height_above_sidewalk_m']-1.68)<1e-5
 assert .28<=street['houses'][0]['projected_frame_width']<=.42
 result=dict(passed=True,views=len(views)+1,paths=views+['renders/ranch/street/street.png'],tonal=tonal,eave_band=band,street_eye_height_m=street['eye_height_above_sidewalk_m'],nearest_house_frame_width=street['houses'][0]['projected_frame_width'])
 Path('build/ranch/delivery/view-check.json').write_text(json.dumps(result,indent=2))
 for name,path in dict(hero=base/'hero.png',turnaround=base/'turnaround.jpg',details=base/'details.jpg',family=base/'family.jpg',street=Path('renders/ranch/street/street.png')).items():
  im=Image.open(path).convert('RGB');im.thumbnail((1600,2400),Image.Resampling.LANCZOS);dest=Path('docs')/('ranch-'+name+'.jpg')
  for quality in range(91,39,-4):
   im.save(dest,quality=quality,optimize=True)
   if dest.stat().st_size<=200000:break
  assert im.width<=1600 and dest.stat().st_size<=200000
 print('RANCH_FINAL_VIEWS',result['views'],'current bundles; tonal',tonal)


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seeds',default='11,12,13,14,15,16');main(p.parse_args())
