"""4096 Cycles manufacture bake, channel-aware 2048 delivery; original fields."""
import sys,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path[:0]=[str(HERE.parents[1]),str(HERE)]
from PIL import Image
from graphics import bake_fields
from kit.flat_bake import bake

folder=bake_fields()
bake(folder,Path('textures/bake'),'CoffeeShop',2.0,4096,1,height_distance=.004)
subprocess.run([sys.executable,str(HERE.parents[1]/'kit/downsample.py'),'--source','textures/bake','--out','textures/ship','--asset','CoffeeShop','--size','2048'],check=True)
path=Path('textures/ship/T_CoffeeShop_BaseColor.png');im=Image.open(path).convert('RGBA');im.putalpha(Image.open('build/atlas/T_CoffeeShop_BaseColor.png').getchannel('A'));im.save(path)
Path('textures/ship/layout.json').write_bytes(Path('build/atlas/layout.json').read_bytes())
print('COFFEE ATLAS BAKED 4096 -> 2048; shared charts, OpenGL normal, ORM, original coverage')
