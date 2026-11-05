"""Rebuild the original H120 checkpoint locally for camera-method comparison.

The archived scripts come from this repository's own history, never a downloaded
model. No checkout or other worktree is modified. Only review geometry is built.
"""
import argparse,io,json,subprocess,tarfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'cars'
ROUND1='577ca2c'

def main():
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');p.add_argument('--model',action='store_true');p.add_argument('--renders',required=True);a=p.parse_args()
 dest=ASSET/'build/hatch-round1';dest.mkdir(parents=True,exist_ok=True)
 if a.model:
  archive=subprocess.check_output(['git','archive',ROUND1,'cars/src','kit'],cwd=ROOT)
  source=dest/'source';source.mkdir(exist_ok=True)
  with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(source,filter='data')
  prefix=[a.blender,'-t','1','-b','--factory-startup','--python-exit-code','1','--python']
  for script,args in [('hatch_build.py',['--quality','game','--out',str(dest/'game.blend')]),('hatch_check.py',['--source',str(dest/'game.blend'),'--out',str(dest/'form-check.json')])]:
   subprocess.run(prefix+[str(source/'cars/src'/script),'--']+args,cwd=ROOT,check=True)
 out=Path(a.renders).resolve();out.mkdir(parents=True,exist_ok=True)
 subprocess.run([str(ROOT/'kit/with_gpu.sh'),a.blender,'-b','--factory-startup','--python-exit-code','1','--python',str(ASSET/'src/hatch_render.py'),'--','--source',str(dest/'game.blend'),'--out',str(out),'--mode','clay','--shots','side','--preview','--width','1600'],cwd=ROOT,check=True)
 sys.path[:0]=[str(ASSET/'src'),str(ROOT)]
 from hatch_review import side_overlay
 side_overlay(out,json.loads((out/'shots.json').read_text()))
 (out/'baseline.json').write_text(json.dumps(dict(source_commit=ROUND1,scope='Original checkpoint geometry; orthographic axle registration',source_sha256=json.loads((out/'shots.json').read_text())['side']['source_sha256']),indent=2))
if __name__=='__main__':main()
