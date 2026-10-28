"""Rebuild our own round-one geometry from its ancestor for fair comparisons.

Only this asset's authored source blobs are read from Git. Shared kit imports
come from the current checkout; no other worktree is opened or changed.
"""
import hashlib,json,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
COMMIT='f622cc9'
ORIGINAL_GLB_SHA='d0249bc2b9293765c13f6353de0a7099824b5c022d64154b3f3216dc36a2fa29'
from shots import DEFAULT_SHOTS

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(command,cwd=BASE,env=None):
 print('BASELINE',*map(str,command),flush=True)
 subprocess.run(list(map(str,command)),cwd=cwd,env=env,check=True)
def main():
 out=BASE/'build/round1';out.mkdir(exist_ok=True)
 manifest=BASE/'build/baseline.json'
 old=json.loads(manifest.read_text()) if manifest.exists() else {}
 glb=out/'bolt.glb';model_ok=glb.exists() and old.get('commit')==COMMIT and old.get('glb_sha256')==sha(glb)
 if not model_ok or not (out/'sculpt.blend').exists() or not (out/'magazine_loaded.glb').exists():
  staged=BASE/'build/baseline-source/guns/bolt';(staged/'src').mkdir(parents=True,exist_ok=True)
  listing=subprocess.check_output(['git','ls-tree','-r','--name-only',COMMIT,'--','guns/bolt/src'],cwd=ROOT,text=True)
  for name in listing.splitlines():
   data=subprocess.check_output(['git','show',f'{COMMIT}:{name}'],cwd=ROOT)
   (staged/'src'/Path(name).name).write_bytes(data)
  launcher=BASE/'build/baseline-source/run.py'
  launcher.write_text('import sys,runpy\nsys.path.insert(0,'+repr(str(ROOT))+')\nrunpy.run_path('+repr(str(staged/'src/build.py'))+",run_name='__main__')\n")
  run(['blender','-b','--factory-startup','--python-exit-code','1','--python',launcher,'--','--out',out/'bolt.blend'],cwd=staged)
 signature=hashlib.sha256((''.join(sha(p) for p in [BASE/'src/baseline.py',BASE/'src/shots.py',BASE/'src/render.py',BASE/'src/sections.py',ROOT/'guns/common/render.py'])+'1440/32').encode()).hexdigest()
 render_out=BASE/'renders/round1';render_out.mkdir(parents=True,exist_ok=True)
 needed=[render_out/(n+'.png') for n in DEFAULT_SHOTS.split(',')]
 needed.extend([render_out/'loaded/magazine.png',render_out/'sections/sections.jpg'])
 if old.get('presentation_signature')!=signature or not all(p.exists() for p in needed):
  command=[ROOT/'kit/with_gpu.sh','blender','-b','--factory-startup','--python-exit-code','1','--python',BASE/'src/render.py','--']
  run(command+['--source',glb,'--out',render_out,'--width','1440','--samples','32'])
  run(command+['--source',out/'magazine_loaded.glb','--out',render_out/'loaded','--width','1000','--samples','32','--shots','magazine'])
  run(['blender','-b','--factory-startup','--python-exit-code','1','--python',BASE/'src/sections.py','--','--game',glb,'--sculpt',out/'sculpt.blend','--out',render_out/'sections'])
 manifest.write_text(json.dumps(dict(commit=COMMIT,glb_sha256=sha(glb),presentation_signature=signature,
   original_checkpoint_sha256=ORIGINAL_GLB_SHA,matches_original_checkpoint_bytes=sha(glb)==ORIGINAL_GLB_SHA,
   meaning='Our historical geometry, rerendered with current cameras and quick lights; no external model'),indent=2))
 print('Baseline ready:',COMMIT,sha(glb))
if __name__=='__main__':main()
