"""Exact procedural/delivery replay plus a separate real-GPU tolerance check."""
import hashlib,json,subprocess,sys,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.compare_textures import compare
from render_batch import gpu_command

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def gpu_snapshot(folder):
 folder.mkdir(parents=True,exist_ok=True)
 for channel in ('BaseColor','Normal','ORM'):
  source=Path('textures/bake')/f'T_Minigolf_{channel}_GPU.png';assert source.exists(),source
  shutil.copyfile(source,folder/f'T_Minigolf_{channel}.png')

files=sorted(set(
 [p for p in Path('export').glob('*') if p.suffix in ('.gltf','.bin','.json') and not p.name.endswith('-context.json')]
 +list(Path('textures/ship').glob('*.png'))+list(Path('build/procedural').glob('*'))
 +list(Path('build/embedded').glob('*.glb'))
 +[Path('textures/bake')/f'T_Minigolf_{ch}.png' for ch in ('BaseColor','Normal','ORM')]
 +[Path('build')/name for name in ('manifest.json','pieces.json','source-construction.json')]))
assert files
before={str(p):sha(p) for p in files};gpu_snapshot(Path('build/repeat-gpu/before'))
Path('build/repeat.json').unlink(missing_ok=True)
kit=Path(__file__).resolve().parents[2]/'kit'
commands=[
 [sys.executable,'src/textures.py','--size','4096'],
 gpu_command(['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python',str(kit/'flat_bake.py'),'--','--source','build/procedural','--out','textures/bake','--name','Minigolf','--coverage','8','--size','4096','--samples','4','--height-distance','.018']),
 [sys.executable,'src/finish_bake.py'],
 [sys.executable,str(kit/'downsample.py'),'--source','textures/bake','--out','textures/ship','--asset','Minigolf','--size','2048'],
 gpu_command(['blender','-b','--factory-startup','-t','1','--python-exit-code','1','--python','src/build.py','--','--out','build/course.blend']),
 gpu_command(['blender','-b','--factory-startup','-t','4','--python-exit-code','1','--python','src/plant_export.py'])]
with Path('build/repeat.log').open('w') as log:
 for command in commands:subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
after={p:sha(p) for p in before};changed={p:(v,after[p]) for p,v in before.items() if v!=after[p]};assert not changed,changed
gpu_snapshot(Path('build/repeat-gpu/after'));texture=compare('build/repeat-gpu/before','build/repeat-gpu/after',2,.02);assert texture['passed'],texture
Path('build/texture-repeat.json').write_text(json.dumps(texture,indent=2))
Path('build/repeat.json').write_text(json.dumps(dict(passed=True,scope='Rebuilt model/plant deliveries, maps, fields and source construction receipts. Blender authoring files, GPU renders and presentation-only context receipts are excluded.',exact_files=len(before),byte_identical=True,files=before,gpu_rebake_compared=True,gpu_max_byte_delta=max(r['max_byte_delta'] for r in texture['textures']),gpu_max_rmse_bytes=max(r['rmse_bytes'] for r in texture['textures'])),indent=2))
print('REPEAT PASS',len(before),'exact original-field/delivery files; GPU maximum delta',max(r['max_byte_delta'] for r in texture['textures']),'maximum RMSE',max(r['rmse_bytes'] for r in texture['textures']))
