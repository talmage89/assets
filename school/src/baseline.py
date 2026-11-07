"""Rebuild accepted checkpoint comparison inputs from this repository's history.

The isolated archive stays under school/build. Native libraries and context
are read through links; no other checkout or canonical delivery is modified.
"""
import argparse,json,os,subprocess,tarfile,io
from pathlib import Path
HERE=Path(__file__).resolve().parent;SCHOOL=HERE.parent;ROOT=SCHOOL.parent
REVISION='1fd7b37'
SEEDS=(101,102,103);SHOTS=('hero','above','rear','windows')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');a=ap.parse_args()
    dest=SCHOOL/'renders/before'
    complete=all((dest/str(seed)/name).exists() for seed in SEEDS for name in [*(s+'.png' for s in SHOTS),'provenance.json'])
    if complete and not a.prepare_only:
        print('BASELINE preserved accepted checkpoint images');return
    sandbox=SCHOOL/'build/baseline';sandbox.mkdir(parents=True,exist_ok=True)
    archive=subprocess.check_output(['git','archive',REVISION,'school/src'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(sandbox,filter='data')
    for name in ('kit','houses','ground','fences','trees','street-furniture','street-light','shrubs'):
        link=sandbox/name
        if not link.exists():link.symlink_to(os.path.relpath(ROOT/name,sandbox),target_is_directory=True)
    old=sandbox/'school';build=old/'build';build.mkdir(exist_ok=True)
    context=build/'context'
    if not context.exists():context.symlink_to(os.path.relpath(SCHOOL/'build/context',build),target_is_directory=True)
    blend=['blender','-b','-t','4','--factory-startup','--python-exit-code','1']
    with (SCHOOL/'build/baseline-build.log').open('w') as log:
        subprocess.run([*blend,'--python','src/build.py','--','--seeds','101,102,103','--out','build/family.blend'],cwd=old,stdout=log,stderr=subprocess.STDOUT,check=True)
    if a.prepare_only:
        print('BASELINE isolated model',old);return
    with (SCHOOL/'build/baseline-render.log').open('w') as log:
        subprocess.run([str(ROOT/'kit/with_gpu.sh'),*blend,'--python','src/render.py','--','--seeds','101,102,103','--shots',','.join(SHOTS),'--out',str(dest),'--width','1400','--samples','32'],cwd=old,stdout=log,stderr=subprocess.STDOUT,check=True)
    (SCHOOL/'build/baseline-receipt.json').write_text(json.dumps(dict(revision=REVISION,scope='Original repository scripts rebuilt in an isolated archive; native libraries and school context are read-only inputs.',seeds=SEEDS,shots=SHOTS),indent=2))

if __name__=='__main__':main()
