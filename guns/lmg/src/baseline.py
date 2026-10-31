"""Rebuild the accepted round-1 finish from our own pinned local git source.

Existing preserved GLBs are verified and retained. A clean clone uses the same
accepted geometry/UVs and historical lookdev through the kit bake/export path.
No other gun, worktree or downloaded script is changed or executed.
"""
import hashlib,json,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1];REVISION='8ff9031'
folder=BASE/'build/look-round2/before';source=folder/'export/lmg.glb';manifest=folder/'provenance.json'
if source.exists() and manifest.exists():
 row=json.loads(manifest.read_text());assert row['commit']==REVISION and row['sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
 print('Retained verified accepted round-1 GLB',row['sha256']);raise SystemExit(0)
folder.mkdir(parents=True,exist_ok=True)
def run(args):subprocess.run([str(v) for v in args],cwd=BASE,check=True)
bp=['blender','-b','--factory-startup','--python-exit-code','1','--python']
rel=folder.relative_to(BASE);high=rel/'build/delivery/high.blend';baked=rel/'build/baked';textures=rel/'textures'
run([*bp,'src/build_high.py','--','--out',high,'--wear','1','--revision',REVISION])
run([ROOT/'kit/with_gpu.sh',*bp,ROOT/'kit/bake.py','--','--low','build/delivery/bake-target.blend','--high',high,'--out',baked,'--asset','Harrow56','--config','src/config.py','--size','4096','--samples','32'])
run(['python3',ROOT/'kit/downsample.py','--source',baked,'--out',textures,'--asset','Harrow56','--size','2048','--alpha-mode','independent'])
run([*bp,'src/export_finish.py','--','--textures',textures,'--out',rel/'export'])
manifest.write_text(json.dumps(dict(commit=REVISION,sha256=hashlib.sha256(source.read_bytes()).hexdigest(),rebuild='Pinned original procedural finish; unchanged accepted surfaces and kit delivery'),indent=2))
