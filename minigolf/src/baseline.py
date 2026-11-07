"""Reconstruct the accepted form into an isolated ignored directory, serially."""
import argparse,subprocess,tarfile,io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'minigolf/build/baseline'
def prepare():
 BASE.mkdir(parents=True,exist_ok=True)
 data=subprocess.check_output(['git','archive','0aedb91:minigolf/src'],cwd=ROOT)
 with tarfile.open(fileobj=io.BytesIO(data)) as archive:
  for member in archive.getmembers():
   if member.isfile() and member.name.endswith('.py'):
    path=BASE/'src'/member.name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(archive.extractfile(member).read())
 launcher=BASE/'run.py';launcher.write_text("import sys,argparse\nfrom pathlib import Path\nsys.path[:0]=[str(Path(__file__).resolve().parent/'src'),str(Path(__file__).resolve().parents[3])]\nimport build\nbuild.preserve=lambda:None\nbuild.build(argparse.Namespace(classic_seed=71,adventure_seed=92,out='build/course.blend'))\n")
 return launcher
if __name__=='__main__':
 if not (BASE/'export/Minigolf-92.gltf').exists():
  launcher=prepare();subprocess.run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(launcher)],cwd=BASE,check=True)
