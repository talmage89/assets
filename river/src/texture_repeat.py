"""Independent 4096 bank rebake and exact original card/normal regeneration."""
import os
import shlex
import subprocess
from pathlib import Path
from bank_fields import prepare,ship,compare,REPO


def main():
    base=Path('build/texture-repeat');prepare(base);baked=base/'baked'
    command=[str(REPO/'kit/with_gpu.sh'),*shlex.split(os.environ.get('BLENDER','blender -t 1')),
        '-b','--factory-startup','--python-exit-code','1','--python','src/bank_fields.py','--','bake',
        '--base',str(base),'--baked',str(baked)]
    subprocess.run(command,check=True)
    output=base/'ship';ship(base,baked,output);compare(Path('textures/checkpoint'),output)


if __name__=='__main__':main()
