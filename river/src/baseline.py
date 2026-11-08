"""Rebuild the accepted river in an isolated directory in this worktree.

Only trusted source files from the specified repository commit are extracted.
Native input directories are read-only symlinks. This is an evidence archive,
not another git worktree, and never rebuilds another family's delivery.
"""
import argparse
import io
import os
import subprocess
import tarfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'river/build/accepted-rebuild'
REVISION='9b1c8bc'


def prepare():
    DEST.mkdir(parents=True,exist_ok=True)
    data=subprocess.check_output(['git','archive',REVISION,'river/src'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers():
            assert (member.name=='river' or member.name.startswith('river/src')) and '..' not in Path(member.name).parts
        archive.extractall(DEST,filter='data')
    for folder in ROOT.iterdir():
        if not folder.is_dir() or folder.name in ('river','build','.git'):continue
        link=DEST/folder.name
        if not link.exists():link.symlink_to(os.path.relpath(folder,DEST),target_is_directory=True)
    local=DEST/'river';(local/'build').mkdir(exist_ok=True)
    link=local/'refs'
    if not link.exists():link.symlink_to(os.path.relpath(ROOT/'river/refs',local),target_is_directory=True)
    with (local/'build/textures.log').open('w') as log:
        subprocess.run(['python3','src/textures.py'],cwd=local,stdout=log,stderr=subprocess.STDOUT,check=True)


def build():
    local=DEST/'river'
    with (local/'build/model.log').open('w') as log:
        subprocess.run(['blender','-t','1','-b','--factory-startup','--python-exit-code','1',
                        '--python','src/build.py','--','--out','build/river.blend'],cwd=local,
                       stdout=log,stderr=subprocess.STDOUT,check=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--prepare',action='store_true');ap.add_argument('--build',action='store_true');a=ap.parse_args()
    if a.prepare:prepare()
    if a.build:build()
