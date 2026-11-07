"""Regenerate fields, GPU bake, filter and rebuild; compare delivered bytes."""
import hashlib,json,subprocess,sys,os,shutil
from pathlib import Path
files=[p for p in Path('export').rglob('*') if p.suffix in ('.gltf','.bin','.glb','.png')]
Path('build/repeat.json').unlink(missing_ok=True)
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
shutil.copyfile('textures/ship/T_Minigolf_Normal.png','build/repeat-normal-before.png')
snapshot=Path('build/repeat-mesh-before');snapshot.mkdir(exist_ok=True)
for seed in (71,92):
 for ext in ('gltf','bin'):
  p=Path(f'export/Minigolf-{seed}.{ext}');shutil.copyfile(p,snapshot/p.name)
fields=sorted(Path('build/procedural').glob('*'));field_before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in fields if p.is_file()}
subprocess.run([sys.executable,'src/textures.py','--size','4096'],check=True)
Path('textures/bake/Minigolf-ready.json').unlink(missing_ok=True)
field_after={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in field_before};assert field_before==field_after
kit=Path(__file__).resolve().parents[2]/'kit'
with Path('build/repeat-bake.log').open('w') as f:
 subprocess.run([str(kit/'with_gpu.sh'),'blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(kit/'flat_bake.py'),'--','--source','build/procedural','--out','textures/bake','--name','Minigolf','--coverage','8','--size','4096','--samples','4','--height-distance','.018'],stdout=f,stderr=subprocess.STDOUT,check=True)
 subprocess.run([sys.executable,'src/finish_bake.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
 subprocess.run([sys.executable,str(kit/'downsample.py'),'--source','textures/bake','--out','textures/ship','--asset','Minigolf','--size','2048'],stdout=f,stderr=subprocess.STDOUT,check=True)
with Path('build/repeat.log').open('w') as f:subprocess.run(['blender','-b','--factory-startup','-t','1','--python-exit-code','1','--python','src/build.py','--','--out','build/course.blend'],stdout=f,stderr=subprocess.STDOUT,check=True)
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
if before.get('export/textures/T_Minigolf_Normal.png')!=after.get('export/textures/T_Minigolf_Normal.png'):
 import numpy as np
 from PIL import Image
 a=np.asarray(Image.open('build/repeat-normal-before.png'),np.int16);b=np.asarray(Image.open('textures/ship/T_Minigolf_Normal.png'),np.int16);q=np.argwhere(a!=b)
 print('NORMAL REPEAT DIFFERENCES',len(q),[(p.tolist(),a[tuple(p[:2])].tolist(),b[tuple(p[:2])].tolist()) for p in q[:20]],flush=True)
for seed in (71,92):
 key=f'export/Minigolf-{seed}.bin'
 if before[key]==after[key]:continue
 import numpy as np
 a=(snapshot/f'Minigolf-{seed}.bin').read_bytes();b=Path(key).read_bytes()
 assert len(a)==len(b),('Buffer size changed',seed,len(a),len(b))
 changed=np.flatnonzero(np.frombuffer(a,np.uint8)!=np.frombuffer(b,np.uint8))
 print('MESH REPEAT BYTE DIFFERENCES',seed,len(changed),changed[:20].tolist(),flush=True)
 doc=json.loads(Path(f'export/Minigolf-{seed}.gltf').read_text())
 for mesh in doc['meshes']:
  for primitive in mesh['primitives']:
   for name,index in primitive['attributes'].items():
    accessor=doc['accessors'][index];view=doc['bufferViews'][accessor['bufferView']];lo=view.get('byteOffset',0);hi=lo+view['byteLength']
    if accessor['componentType']!=5126 or not np.any((changed>=lo)&(changed<hi)):continue
    x=np.frombuffer(a[lo:hi],'<f4');y=np.frombuffer(b[lo:hi],'<f4');q=np.flatnonzero(x!=y)
    print('MESH ATTRIBUTE DIFFERENCE',mesh['name'],name,'max',float(np.max(abs(x-y))),'values',[(int(i),float(x[i]),float(y[i])) for i in q[:20]],flush=True)
assert before==after,{p:(h,after[p]) for p,h in before.items() if h!=after[p]}
Path('build/repeat.json').write_text(json.dumps(dict(passed=True,files=len(files),source_fields=len(field_before),byte_identical=True,gpu_rebake=True),indent=2));print('REPEAT',len(files),'delivery files and',len(field_before),'source fields byte-identical')
