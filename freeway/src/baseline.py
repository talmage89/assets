"""Rebuild the accepted 3681a2c comparison in an isolated local source archive.

No other worktree is read. Library deliveries are read-only symlink inputs;
the original freeway generator writes only below this family's build folder.
"""
import io,os,subprocess,tarfile,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ASSET=ROOT/'freeway';OUT=ASSET/'renders/before-lookdev';CACHE=ASSET/'build/accepted-source'

def main():
    if (OUT/'checkpoint/101/terminal.png').exists() and (OUT/'checkpoint/202/hero.png').exists():return
    CACHE.mkdir(parents=True,exist_ok=True)
    data=subprocess.check_output(['git','archive','3681a2c','freeway'],cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(CACHE,filter='data')
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in ('freeway','.git','build'):
            link=CACHE/p.name
            if not link.exists():link.symlink_to(p,target_is_directory=True)
    fw=CACHE/'freeway';(fw/'refs').mkdir(exist_ok=True)
    for p in (ASSET/'refs').iterdir():
        if p.is_file() and p.suffix.lower() in ('.jpg','.pdf'):
            dest=fw/'refs'/p.name
            if not dest.exists():dest.symlink_to(p)
    def run(*args):subprocess.run(args,cwd=fw,check=True)
    run('make','model')
    run('make','render','sheet','WIDTH=1400','SAMPLES=32')
    OUT.mkdir(parents=True,exist_ok=True);shutil.copytree(fw/'renders/checkpoint',OUT/'checkpoint',dirs_exist_ok=True)
if __name__=='__main__':main()
