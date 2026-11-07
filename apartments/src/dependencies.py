"""Build only missing canonical libraries, serially; hash existing bytes first."""
import hashlib,json,os,subprocess,shlex
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
JOBS=[('houses','export/Hearthfield-27.gltf',['SEEDS=27,2','export']),
 ('houses','export/Hearthfield-2.gltf',['SEEDS=2','export']),
 ('houses','textures/ranch-ship/T_RanchBrick_buff_BaseColor.png',['TYPE=ranch','bake']),
 ('houses','textures/cape-ship/T_CapeCedar_BaseColor.png',['TYPE=cape','bake']),
 ('ground','export/Ground.glb',['export']),('shrubs','export/Shrubs.glb',['export']),
 ('trees','export/RedMaple.glb',['SPECIES=maple','export']),('fences','export/WoodPrivacy.glb',['export']),
 ('cars','export/AlderC150.glb',['export']),('cars','export/AlderX220.glb',['BODY=suv','export']),
 ('cars','export/AlderH120.glb',['BODY=hatch','export']),('street-light','export/StreetLight.glb',['export']),
 ('utility','textures/ship/T_Utility_BaseColor.png',['textures'])]

def snapshot():
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for family in ('houses','ground','shrubs','trees','fences','cars','street-light','utility') for folder in ('export','textures/ship','textures/suv/ship','textures/hatch/ship') for p in (ROOT/family/folder).rglob('*') if p.is_file()}

def main():
 out=Path('build');out.mkdir(exist_ok=True);before=snapshot()
 for family,name,args in JOBS:
  if (ROOT/family/name).exists():continue
  print('DEPENDENCY',family,args,flush=True)
  with (out/('dependency-'+family+'-'+Path(name).stem+'.log')).open('w') as log:
   subprocess.run(['make','-C',str(ROOT/family),*args,'BLENDER='+os.environ.get('BLENDER','blender')+' -t 4'],stdout=log,stderr=subprocess.STDOUT,check=True)
 after=snapshot();changed=[p for p,h in before.items() if after.get(p)!=h];assert not changed,changed
 subprocess.run(['python3','src/derive_surfaces.py'],check=True)
 # The ground family's 4K floated/broomed concrete has no form-tie holes.
 # Filter that existing bake to a small balcony/walk set, rather than making
 # each building load the terrain's full 2048 concrete set.
 concrete=Path('textures/ship');concrete.mkdir(parents=True,exist_ok=True)
 if not (concrete/'T_ApartmentsConcrete_BaseColor.png').exists():
  target=out/'concrete-filter';target.mkdir(exist_ok=True)
  subprocess.run(['python3',str(ROOT/'kit/downsample.py'),'--source',str(ROOT/'ground/textures/bake'),'--out',str(target),'--asset','Concrete','--size','512'],check=True)
  for p in target.glob('T_Concrete_*.png'):(concrete/p.name.replace('T_Concrete_','T_ApartmentsConcrete_')).write_bytes(p.read_bytes())
 # Build the utility's parts alone, avoiding its own neighborhood fixtures.
 source=out/'context/utility.glb'
 if not source.exists():
  source.parent.mkdir(parents=True,exist_ok=True);script=out/'context/utility-build.py'
  script.write_text("import sys\nfrom pathlib import Path\nsys.path[:0]=["+repr(str(ROOT/'utility/src'))+","+repr(str(ROOT))+ "]\nfrom build import parts\nparts(Path("+repr(str(source.with_suffix('.blend').resolve()))+"))\n")
  with (out/'utility-parts.log').open('w') as log:
   subprocess.run([*shlex.split(os.environ.get('BLENDER','blender')),'-b','-t','4','--factory-startup','--python-exit-code','1','--python',str(script.resolve())],cwd=ROOT/'utility',stdout=log,stderr=subprocess.STDOUT,check=True)
 (out/'dependencies.json').write_text(json.dumps(dict(preserved=before,passed=True),indent=2))
if __name__=='__main__':main()
