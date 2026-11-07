"""Recreate the accepted b638448 packages/views in a worktree-local archive.

Only tracked school scripts are restored. Canonical library deliveries and
school-owned context are read-only inputs; no other worktree is accessed.
"""
import argparse,json,os,subprocess,tarfile,io,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;SCHOOL=HERE.parent;ROOT=SCHOOL.parent
REVISION='b638448';SEEDS=(101,102,103);SHOTS=('hero','above','rear','windows')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');a=ap.parse_args()
    dest=SCHOOL/'renders/accepted-lookdev';packages=SCHOOL/'build/accepted-lookdev/export'
    images=all((dest/str(seed)/name).exists() for seed in SEEDS for name in [*(s+'.png' for s in SHOTS),'provenance.json'])
    if images and all((packages/f'Campus-{s}.gltf').exists() for s in SEEDS):
        print('BASELINE preserved accepted look-dev packages and images');return
    sandbox=SCHOOL/'build/fix-baseline';sandbox.mkdir(parents=True,exist_ok=True)
    archive=subprocess.check_output(['git','archive',REVISION,'school/src'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(sandbox,filter='data')
    for folder in ROOT.iterdir():
        if not folder.is_dir() or folder.name in ('school','build','.git'):continue
        link=sandbox/folder.name
        if not link.exists():link.symlink_to(os.path.relpath(folder,sandbox),target_is_directory=True)
    old=sandbox/'school';build=old/'build';build.mkdir(exist_ok=True)
    for link,target in ((build/'context',SCHOOL/'build/context'),(old/'textures/checkpoint',SCHOOL/'textures/checkpoint')):
        link.parent.mkdir(exist_ok=True,parents=True)
        if not link.exists():link.symlink_to(os.path.relpath(target,link.parent),target_is_directory=True)
    blend=['blender','-b','-t','4','--factory-startup','--python-exit-code','1']
    with (SCHOOL/'build/baseline-build.log').open('w') as log:
        subprocess.run([*blend,'--python','src/build.py','--','--seeds','101,102,103','--out','build/family.blend'],cwd=old,stdout=log,stderr=subprocess.STDOUT,check=True)
    packages.mkdir(parents=True,exist_ok=True)
    for source in (old/'export').glob('*'):
        if source.suffix not in ('.gltf','.bin','.json'):continue
        target=packages/source.name
        if source.suffix=='.gltf':
            data=json.loads(source.read_text())
            for row in data.get('images',[]):row['uri']=os.path.relpath((source.parent/row['uri']).resolve(),target.parent)
            target.write_text(json.dumps(data,separators=(',',':'))+'\n')
        else:shutil.copyfile(source,target)
    if not images and not a.prepare_only:
        with (SCHOOL/'build/baseline-render.log').open('w') as log:
            subprocess.run([str(ROOT/'kit/with_gpu.sh'),*blend,'--python','src/render.py','--','--seeds','101,102,103','--shots',','.join(SHOTS),'--out',str(dest),'--width','1400','--samples','32'],cwd=old,stdout=log,stderr=subprocess.STDOUT,check=True)
    (SCHOOL/'build/baseline-receipt.json').write_text(json.dumps(dict(revision=REVISION,scope='Isolated tracked scripts, immutable native library inputs; accepted package images and same-world-camera comparisons.',seeds=SEEDS,shots=SHOTS),indent=2))

if __name__=='__main__':main()
