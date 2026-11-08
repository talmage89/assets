"""Reproduce handoff views from our own git source, without another worktree.

Existing native handoff images and frozen exported resources are reused. From
an empty freeway folder, the 0d5b092 generator is archived under build/, built
against read-only library inputs, and rendered in one serial GPU set.
"""
import io,json,os,subprocess,sys,tarfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ASSET=HERE.parent;ROOT=ASSET.parent
COMMIT='0d5b092'
# label, old frame if present, final frame, seed, original isolated-module view
PAIRS=[('town','lookdev/101/above_clean','101/above_clean',101,False),
 ('hero-town','reframed/101/hero','101/hero',101,False),
 ('backyards','reframed/202/hero','202/hero',202,False),
 ('traffic','look-matches/traffic_2007','../final-matches/traffic_2007',202,False),
 ('grass','reframed/101/hero_previous','101/hero_previous',101,False),
 ('concrete','lookdev/101/pier_girders','101/pier_girders',101,False),
 ('bearing-surroundings','look-matches/bearing_2008','../final-matches/bearing_2008',101,True),
 ('sky-diamond','lookdev/101/hero','101/hero_cut',101,False),
 ('sky-curved','lookdev/202/hero','202/hero_old',202,False)]

def prepare():
 frozen=Path('build/freeway-final-baseline/export')
 if (frozen/'Freeway-101.gltf').exists():return frozen
 cache=Path('build/before-final/source');cache.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(['git','archive',COMMIT,'freeway'],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(data)) as ar:ar.extractall(cache,filter='data')
 for family in ROOT.iterdir():
  if not family.is_dir() or family.name in ('freeway','build','.git'):continue
  link=cache/family.name
  if not link.exists():link.symlink_to(family,target_is_directory=True)
 old=cache/'freeway';(old/'refs').mkdir(exist_ok=True)
 for photo in (ASSET/'refs').iterdir():
  if photo.suffix.lower() not in ('.jpg','.pdf','.png'):continue
  link=old/'refs'/photo.name
  if not link.exists():link.symlink_to(photo)
 # The archived generator writes only under its own local freeway directory.
 with Path('build/before-final/build.log').open('w') as log:
  subprocess.run(['make','model'],cwd=old,check=True,stdout=log,stderr=subprocess.STDOUT)
 return old/'export'

def render_jobs(path):
 # Executed inside Blender; the legacy renderer, procedural lighting and
 # exported PBR are preserved. Only the requested camera pose is supplied.
 import importlib.util
 sys.path[:0]=[str(ROOT),str(HERE)]
 legacy=ASSET/'build/before-final/legacy/render.py';legacy.parent.mkdir(parents=True,exist_ok=True)
 legacy.write_bytes(subprocess.check_output(['git','show',COMMIT+':freeway/src/render.py'],cwd=ROOT))
 spec=importlib.util.spec_from_file_location('freeway_handoff_renderer',legacy);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 for row in json.loads(Path(path).read_text()):
  out=Path(row['out']);mod.render(row['source'],out.parent,row['width'],row['samples'],'CYCLES',custom={out.stem:row['camera']})

def frame(after,new,matches=None):
 after=Path(after)
 if new.startswith('../final-matches/'):
  return Path(matches or str(after)+'-matches')/(Path(new).name+'.png')
 return after/(new+'.png')

def ensure(after='renders/final',width=1400,samples=32,matches=None):
 after=Path(after);jobs=[];before=Path('renders/before-final')
 # Frozen images are comparison evidence, never generation inputs.
 for label,old,new,seed,isolated in PAIRS:
  target=before/(old+'.png');final=frame(after,new,matches);camera=json.loads(final.with_suffix('.json').read_text())['camera']
  if target.exists():
   record=json.loads(target.with_suffix('.json').read_text())
   if all(record['camera'].get(k)==camera.get(k) for k in ('location','target','lens','aspect')):continue
  source=prepare()/('modules/Overpass.gltf' if isolated else f'Freeway-{seed}.gltf')
  shot=dict(camera)
  if isolated:shot['stage_floor']=dict(size=200,location=(0,0,-.06))
  jobs.append(dict(out=str(target),source=str(source),camera=shot,width=width,samples=samples))
 if jobs:
  path=Path('build/before-final/jobs.json');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(jobs,indent=2))
  command=[str(ROOT/'kit/with_gpu.sh'),os.environ.get('BLENDER_BINARY','blender'),'-t','2','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'final_baseline.py'),'--','--render',str(path)]
  with Path('build/before-final/render.log').open('w') as log:subprocess.run(command,check=True,stdout=log,stderr=subprocess.STDOUT)
 return PAIRS

if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
 if args and args[0]=='--render':render_jobs(args[1])
 else:ensure()
