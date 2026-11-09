"""Recover the 56cce73 before frames inside this worktree, if not cached.

Archive only our own scripts; native family inputs stay read-only symlinks.
This optional historical reconstruction never touches another worktree.
"""
import io
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'build/river-last-round/before'
DEST=ROOT/'river/build/last-baseline'


def main():
    required=[BASE/f'renders/final/{seed}/{name}.png' for seed in (101,202)
              for name in ('hero','above','under','abutment','pier','bearings','bar','riffle','driver')]
    required += [BASE/'renders/final/101/floodwall.png']
    required += [BASE/f'renders/final/wall-details/{name}.png' for name in ('outfall','ladder')]
    if all(p.exists() and p.with_suffix('.json').exists() for p in required):
        print('56cce73 before frames cached');return
    DEST.mkdir(parents=True,exist_ok=True)
    data=subprocess.check_output(['git','archive','56cce73','river/src'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        assert all('..' not in Path(m.name).parts and (m.name=='river' or m.name.startswith('river/src')) for m in archive.getmembers())
        archive.extractall(DEST,filter='data')
    for folder in ROOT.iterdir():
        if not folder.is_dir() or folder.name in ('river','build','.git'):continue
        link=DEST/folder.name
        if not link.exists():link.symlink_to(os.path.relpath(folder,DEST),target_is_directory=True)
    local=DEST/'river';(local/'build').mkdir(exist_ok=True)
    (local/'refs').symlink_to(os.path.relpath(ROOT/'river/refs',local),target_is_directory=True) if not (local/'refs').exists() else None
    def run(command):subprocess.run(command,cwd=local,check=True)
    blender=['blender','-t','1','-b','--factory-startup','--python-exit-code','1']
    run(['python3','src/bank_fields.py','prepare'])
    run([str(ROOT/'kit/with_gpu.sh'),*blender,'--python','src/bank_fields.py','--','bake'])
    run(['python3','src/bank_fields.py','ship'])
    run([*blender,'--python','src/native_town.py'])
    run([*blender,'--python','src/build.py','--','--out','build/river.blend'])
    # One lease for the complete historical render set, held only for renders.
    driver=local/'build/before_frames.py'
    driver.write_text('''import subprocess
blender=['blender','-t','1','-b','--factory-startup','--python-exit-code','1']
for seed in (101,202):
    names=['hero','above','under','abutment','pier','bearings','bar','riffle','driver']
    if seed==101:names.append('floodwall')
    for i in range(0,len(names),3):
        subprocess.run(blender+['--python','src/render.py','--','--seeds',str(seed),'--shots',*names[i:i+3],
            '--out','renders/handoff','--width','1280','--samples','32'],check=True)
expression="""import sys;from pathlib import Path
sys.path[:0]=[str(Path('src').resolve()),str(Path('../..').resolve())]
import bpy,render,wall_views
source=Path('export/RiverCrossing-101.gltf')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(source.resolve()))
render.restore_water();render.restore_native_leaves();scene,camera=render.setup(1280,32)
for name,definition in wall_views.definitions().items():
    render.shot(scene,camera,definition,Path('renders/handoff/wall-details')/(name+'.png'),source,1280,32)
"""
subprocess.run(blender+['--python-expr',expression],check=True)
''')
    run([str(ROOT/'kit/with_gpu.sh'),'python3',str(driver)])
    target=BASE/'renders/final';target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(local/'renders/handoff',target,dirs_exist_ok=True)
    assert all(p.exists() for p in required)
    print('56cce73 before frames rebuilt')


if __name__=='__main__':main()
