"""Regenerate fields, GPU bake, filter and rebuild; compare delivered bytes."""
import hashlib,json,subprocess,sys,os
from pathlib import Path
files=[p for p in Path('export').rglob('*') if p.suffix in ('.gltf','.bin','.glb','.png')]
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
fields=sorted(Path('build/procedural').glob('*'));field_before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in fields if p.is_file()}
subprocess.run([sys.executable,'src/textures.py','--size','4096'],check=True)
field_after={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in field_before};assert field_before==field_after
kit=Path(__file__).resolve().parents[2]/'kit'
with Path('build/repeat-bake.log').open('w') as f:
 subprocess.run([str(kit/'with_gpu.sh'),'blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(kit/'flat_bake.py'),'--','--source','build/procedural','--out','textures/bake','--name','Minigolf','--coverage','8','--size','4096','--samples','4','--height-distance','.018'],stdout=f,stderr=subprocess.STDOUT,check=True)
 subprocess.run([sys.executable,str(kit/'downsample.py'),'--source','textures/bake','--out','textures/ship','--asset','Minigolf','--size','2048'],stdout=f,stderr=subprocess.STDOUT,check=True)
with Path('build/repeat.log').open('w') as f:subprocess.run(['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python','src/build.py','--','--out','build/course.blend'],stdout=f,stderr=subprocess.STDOUT,check=True)
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
assert before==after,{p:(h,after[p]) for p,h in before.items() if h!=after[p]}
Path('build/repeat.json').write_text(json.dumps(dict(passed=True,files=len(files),source_fields=len(field_before),byte_identical=True,gpu_rebake=True),indent=2));print('REPEAT',len(files),'delivery files and',len(field_before),'source fields byte-identical')
