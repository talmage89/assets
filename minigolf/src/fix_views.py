"""Native-size correction views, frozen to the accepted checkpoint cameras."""
import argparse,json,sys,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE),str(HERE.parents[1])]
import bpy
from render import scene,render_one,views
from external import bundle
from plan import generate

def main(args):
 names=['classic-hero','adventure-hero','adventure-above','waterfall','pond','tee','border']
 selected=args.shots.split(',') if args.shots else names
 loaded=None
 for name in selected:
  seed=71 if name.startswith('classic-') else 92
  if loaded!=seed:source,p,ctx=scene(seed);loaded=seed
  original=Path('build/revision-before/lookdev')/(name+'.json')
  if original.exists():shot=json.loads(original.read_text())['camera']
  else:shot=views(p)[name]
  # A tee travels with its rerouted hole: preserve the full local camera
  # offset/direction; site-wide comparisons retain exact world camera values.
  if name in ('tee','border'):
   old_h=json.loads(Path('build/revision-before/export/Minigolf-92.json').read_text())['plan']['holes'][0];old=old_h['tee'];new_h=p['holes'][0];new=new_h['tee'];angle=math.radians(new_h['yaw']-old_h['yaw'])
   def moved(point):
    x,y,z=[a-b for a,b in zip(point,old)];return [new[0]+x*math.cos(angle)-y*math.sin(angle),new[1]+x*math.sin(angle)+y*math.cos(angle),new[2]+z]
   shot={**shot,'location':moved(shot['location']),'target':moved(shot['target'])}
   ctx['comparison_camera_scope']='Identical lens, orientation and tee-relative offset after whole-hole relocation'
  else:ctx['comparison_camera_scope']='Exact accepted world camera, lens and lighting'
  render_one('after-'+name,shot,source,p,ctx,args)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--shots');p.add_argument('--out',default='renders/fixes');p.add_argument('--width',type=int,default=1440);p.add_argument('--samples',type=int,default=24);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);main(a)
