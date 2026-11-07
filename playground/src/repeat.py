"""Isolated from-nothing regeneration and exact deterministic-output proof.

GPU rebakes use the kit's tolerance. Existing deliveries remain untouched.
"""
import hashlib,json,os,subprocess,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.compare_textures import compare

def hashes(root,procedural=True):
    files=[p for p in (root/'export').rglob('*') if p.is_file() and p.suffix in ('.gltf','.bin','.json','.png')]
    files += [root/'build/manifest.json']
    files += [root/'build/cameras.json',*sorted((root/'build/photo').glob('*-balanced.jpg'))]
    if procedural:files += [p for p in (root/'build/procedural').iterdir() if p.suffix in ('.png','.json')]
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}

def preserve():
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('export','textures/ship') for p in Path(folder).rglob('*') if p.is_file()}

base=Path('.').resolve();workspace=base/'build/repeat-work';package=workspace/'playground'
shutil.rmtree(workspace,ignore_errors=True);package.mkdir(parents=True)
shutil.copytree(base/'src',package/'src',ignore=shutil.ignore_patterns('__pycache__'))
(package/'refs').symlink_to(base/'refs',target_is_directory=True)
for name in ('kit','ground','trees','shrubs','fences','street-furniture','street-light'):
    (workspace/name).symlink_to(ROOT/name,target_is_directory=True)
(package/'build').mkdir();(package/'textures').mkdir()
seeds=','.join(str(s['seed']) for s in json.loads(Path('build/manifest.json').read_text())['sites'])
before=hashes(base);original=preserve();Path('build/repeat.json').write_text(json.dumps(dict(passed=False,status='in progress')))
env=dict(os.environ,TMPDIR=str(package/'build/tmp'));Path(env['TMPDIR']).mkdir()
log=Path('build/repeat.log')
with log.open('w') as stream:
    def run(args):subprocess.run(args,cwd=package,env=env,stdout=stream,stderr=subprocess.STDOUT,check=True,start_new_session=True)
    run(['python3','src/textures.py'])
    run(['python3','src/photo_matches.py'])
    run(['src/serial_blender.sh','-b','--factory-startup','--python-exit-code','1','--python','src/bake_tiles.py'])
    run(['src/serial_blender.sh','-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--lookdev','--out','build/Playground.blend','--seeds',seeds])
after=hashes(package);changed=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)]
texture=compare('textures/ship',package/'textures/ship',max_delta=2,rmse_limit=.02)
from PIL import Image
import numpy as np
alpha=[]
for p in Path('textures/ship').glob('T_Play*.png'):
    a=Image.open(p);b=Image.open(package/'textures/ship'/p.name)
    if 'A' in a.getbands():
        equal=np.array_equal(np.asarray(a.getchannel('A')),np.asarray(b.getchannel('A')))
        alpha.append(dict(file=p.name,byte_identical=equal));assert equal,alpha[-1]
Path('build/texture-repeat-check.json').write_text(json.dumps(texture,indent=2))
unchanged=original==preserve()
out=dict(passed=not changed and texture['passed'] and unchanged,exact_files=len(before),changed=changed,exact_sha256=after,original_exports_unchanged=unchanged,coverage_alpha=alpha,gpu_textures=texture,scope='Fresh procedural fields, factory-startup geometry and independent locked GPU bake. Procedural PNGs/layout, glTF/BIN, image copies and manifests compare exactly. GPU shipped maps use kit maximum delta 2/255 and byte RMSE .02; alpha is exact. Blend containers, image-byte receipts and stochastic renders are not claimed deterministic.')
Path('build/repeat.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='exact_sha256'},indent=2));assert out['passed'],changed
