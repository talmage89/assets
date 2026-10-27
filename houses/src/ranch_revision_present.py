"""Exported before/after weather views and source/export photographic pairs."""
import argparse,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]


def cameras():
 for seed in (11,12,13,15,16):
  env={**os.environ,'RANCH_SEED':str(seed),'HOUSE_PLAN':''}
  subprocess.run([sys.executable,'../kit/photo_match.py','solve','--config','src/ranch_photo_matches.py','--out',f'build/ranch/revision2/cameras-{seed}.json'],env=env,check=True)
  subprocess.run([os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python','../kit/photo_match.py','--','verify','--calibration',f'build/ranch/revision2/cameras-{seed}.json'],env=env,check=True)


def renders(scope='all'):
 from ranch_render import render
 for seed in ((11,13) if scope in ('all','compare') else ()):
  root=Path(f'renders/ranch/revision2/compare/{seed}')
  render(Path(f'build/ranch/revision2/before/export/HearthfieldRanch-{seed}.gltf'),root/'before','hero,weather',1200,32)
  render(Path(f'export/HearthfieldRanch-{seed}.gltf'),root/'after','hero,weather',1200,32)
 for seed in ((11,12,13,15,16) if scope in ('all','bake-loss') else ()):
  calibration=Path(f'build/ranch/revision2/cameras-{seed}.json');root=Path(f'renders/ranch/revision2/bake-loss/{seed}');names='ranch_summer,ranch_brick_picture,ranch_sun_oblique,ranch_sun_1960'
  render(Path(f'build/ranch/house-{seed}.blend'),root/'source',names,1100,24,camera_file=calibration)
  render(Path(f'export/HearthfieldRanch-{seed}.gltf'),root/'export',names,1100,24,camera_file=calibration)


def sheets(scope='all'):
 from ranch_review import sheet
 for seed in ((11,13) if scope in ('all','compare') else ()):
  folder=Path(f'renders/ranch/revision2/compare/{seed}')
  sheet([(label+' / '+name,folder/label/(name+'.png')) for name in ('hero','weather') for label in ('before','after')],folder/'before-after.jpg',2,1000)
 for seed in ((11,12,13,15,16) if scope in ('all','bake-loss') else ()):
  calibration=Path(f'build/ranch/revision2/cameras-{seed}.json');root=Path(f'renders/ranch/revision2/bake-loss/{seed}')
  subprocess.run([sys.executable,'../kit/photo_match.py','compose','--calibration',str(calibration),'--renders',str(root/'export'),'--out',str(root/'export')],check=True)
  sheet([(label+' / '+name,root/label/(name+'.png')) for name in ('ranch_summer','ranch_brick_picture','ranch_sun_oblique','ranch_sun_1960') for label in ('source','export')],root/'source-export.jpg',2,900)
  sheet([(name,root/'export'/(name+'-pair.jpg')) for name in ('ranch_summer','ranch_brick_picture','ranch_sun_oblique','ranch_sun_1960')],root/'photo-pairs.jpg',1,1600)


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=('cameras','renders','sheets'));p.add_argument('--scope',choices=('all','compare','bake-loss'),default='all');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else None)
 cameras() if a.stage=='cameras' else globals()[a.stage](a.scope)
