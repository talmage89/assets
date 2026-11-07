"""Serial look build. Every Cycles job uses the shared GPU lock."""
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(args):subprocess.run(args,check=True)
if __name__=='__main__':
 run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(ROOT/'kit/flat_bake.py'),'--','--source','build/procedural','--out','textures/bake','--name','Minigolf','--coverage','8','--size','4096','--samples','4','--height-distance','.018'])
 run(['python3',str(ROOT/'kit/downsample.py'),'--source','textures/bake','--out','textures/ship','--asset','Minigolf','--size','2048'])
 run([str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python','src/build.py','--','--out','build/course.blend'])
