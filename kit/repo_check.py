"""Check staged Git blobs (hook) or tracked + untracked source candidates (make).

Never inspects ignored rebuilt outputs. Git blobs, not the working tree, are the
source of truth in hook mode so partially staged files cannot bypass the rules.
"""
import argparse, subprocess, sys
from pathlib import Path
from PIL import Image
import io
FORBIDDEN={'.blend','.glb','.gltf','.fbx','.obj','.bin','.png','.exr','.hdr','.tif','.tiff','.webp','.pdf'}


def path_errors(name):
    """Validate Git paths even when someone force-adds an ignored review file."""
    f=Path(name);errors=[]
    if any(part in {'build','renders','export','textures'} for part in f.parts):
        errors.append(f'{name}: rebuilt output directories cannot be committed')
    if f.suffix.lower() in FORBIDDEN or '.blend' in f.suffix.lower():
        errors.append(f'{name}: forbidden generated/reference format')
    if f.suffix.lower() in {'.jpg','.jpeg','.gif'} and 'docs' not in f.parts:
        errors.append(f'{name}: only final docs JPGs/GIFs belong in Git')
    if 'refs' in f.parts and f.name!='SOURCES.md':
        errors.append(f'{name}: downloaded references must be ignored')
    return errors


def main():
    p=argparse.ArgumentParser();p.add_argument('--staged',action='store_true');a=p.parse_args()
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
    cmd=['git','diff','--cached','--name-only','--diff-filter=ACMR','-z'] if a.staged else ['git','ls-files','--cached','--others','--exclude-standard','-z']
    names=set(subprocess.check_output(cmd,cwd=root).decode().split('\0'))-{''};errors=[]
    # Count the complete candidate tree, including unchanged index entries in
    # hook mode. A second GIF must not bypass the limit in a later commit.
    candidates=set(subprocess.check_output(
        ['git','ls-files','-z'] if a.staged else cmd,cwd=root).decode().split('\0'))-{''}
    gifs={}
    for name in candidates:
        f=Path(name)
        if f.suffix.lower()=='.gif' and 'docs' in f.parts:
            if a.staged or (root/f).is_file():
                folder=Path(*f.parts[:f.parts.index('docs')+1])
                gifs.setdefault(folder,[]).append(name)
    for folder,files in sorted(gifs.items()):
        if len(files)>1:errors.append(f'{folder}: at most one docs GIF allowed ({len(files)} found)')
    for name in sorted(names):
        f=Path(name)
        if a.staged:data=subprocess.check_output(['git','show',':'+name],cwd=root)
        else:
            if not (root/f).is_file():continue
            data=(root/f).read_bytes()
        errors.extend(path_errors(name))
        if len(data)>500_000:errors.append(f'{name}: over 500 KB')
        if 'docs' in f.parts:
            if f.suffix.lower()=='.gif':
                im=Image.open(io.BytesIO(data))
                if im.format!='GIF':errors.append(f'{name}: docs GIF must contain GIF data')
                if im.width>960 or len(data)>450_000:errors.append(f'{name}: docs GIF over 960 px / 450 KB')
            elif f.suffix.lower() not in ('.jpg','.jpeg'):errors.append(f'{name}: docs must be JPG or one GIF')
            else:
                im=Image.open(io.BytesIO(data))
                if im.width>1600 or len(data)>200_000:errors.append(f'{name}: docs image over 1600 px / 200 KB')
    for e in errors:print('ERROR',e)
    print(f'Repository check: {len(names)} source files, {len(errors)} errors')
    return bool(errors)

if __name__=='__main__':sys.exit(main())
