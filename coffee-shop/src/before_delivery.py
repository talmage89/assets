"""Recover our own 37e6af3 handoff, never an external model or another worktree.

Existing native handoff images are reused for identical cameras. In a fresh
clone, the same tracked source rebuilds isolated baseline exports and views.
"""
import argparse,io,json,shutil,subprocess,tarfile
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=1280);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--renders',type=Path,default=Path('renders/final'));a=ap.parse_args()
base=Path.cwd();out=base/'renders/delivery-fixes/before';out.mkdir(parents=True,exist_ok=True)
jobs={}
for seed in (117,228,339):
    for name in ('retained','above','site','table','awning','counter','use','wear','door','rail','hero'):
        src=base/a.renders/str(seed)/(name+'.json')
        if not src.exists():continue
        meta=json.loads(src.read_text());target=out/f'{seed}-{name}.png'
        if target.exists() and Image.open(target).size==(meta['width'],meta['height']) and json.loads(target.with_suffix('.json').read_text())['recipe']==meta['recipe']:continue
        old=base/f'build/before-delivery/renders/lookdev/{seed}/{"hero" if name=="retained" else name}.png'
        if old.exists() and Image.open(old).size==(meta['width'],meta['height']) and json.loads(old.with_suffix('.json').read_text())['recipe']==meta['recipe']:
            shutil.copy2(old,target);shutil.copy2(old.with_suffix('.json'),target.with_suffix('.json'));continue
        jobs[f'{seed}-{name}']=dict(seed=seed,shot=meta['recipe'],sun_elevation=18,sun_azimuth={117:-155,228:-145,339:-55}[seed])
        jobs[f'{seed}-{name}']['shot']['exposure']=-.35
        jobs[f'{seed}-{name}']['shot']['aspect']=meta['width']/meta['height']
if not jobs:raise SystemExit(0)
# Keep the legacy source's repository root outside the coffee-shop directory:
# its image packager identifies own maps by that path component. Native family
# symlinks must keep resolving as read-only canonical resources, not own maps.
stage=ROOT/'build/coffee-delivery-baseline-source';stage.mkdir(parents=True,exist_ok=True)
payload=subprocess.check_output(['git','archive','37e6af3','coffee-shop'],cwd=ROOT)
with tarfile.open(fileobj=io.BytesIO(payload)) as archive:archive.extractall(stage,filter='data')
for name in ('kit','downtown','commercial','patio-set','street-furniture','ground','trees','shrubs','cars','houses','street-light'):
    dst=stage/name
    if not dst.exists():dst.symlink_to(ROOT/name,target_is_directory=True)
work=stage/'coffee-shop';(work/'build').mkdir(exist_ok=True)
with (base/'build/delivery-baseline.log').open('w') as log:
    subprocess.run(['make','model','sites'],cwd=work,stdout=log,stderr=subprocess.STDOUT,check=True)
    # Old renderer accepts arbitrary fixed cameras through its match interface.
    cameras=work/'build/delivery-cameras.json';cameras.write_text(json.dumps(jobs))
    subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','-t','1','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--matches',str(cameras),'--out',str(out),'--width',str(a.width),'--samples',str(a.samples)],cwd=work,stdout=log,stderr=subprocess.STDOUT,check=True)
# Exposure is lighting, not a camera parameter. Keep it in a separate receipt.
for key in jobs:
    p=out/(key+'.json');doc=json.loads(p.read_text());doc['comparison_exposure']=doc['recipe'].pop('exposure');doc['recipe'].pop('aspect')
    if 'roll' not in jobs[key]['shot']:
        assert doc['recipe'].get('roll',0)==0
        doc['recipe'].pop('roll',None)
    p.write_text(json.dumps(doc,indent=2)+'\n')
