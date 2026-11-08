"""Build only missing native inputs, through their existing public targets."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def main():
    jobs=[('ground',[f'textures/ship/T_{a}_{c}.png' for a in ('Asphalt','Concrete','Lawn','GroundTrim') for c in ('BaseColor','Normal','ORM')],['textures/ship/.stamp']),
          ('trees',['export/RedMaple.glb'],['export/RedMaple.glb']),
          ('trees',['export/PinOak.glb'],['SPECIES=oak','export/PinOak.glb']),
          ('downtown',[f'export/Midwest_411_{i:02d}.gltf' for i in range(1,7)],['model']),
          ('school',[f'build/context/{k}.glb' for k in ('car','houses-ranch','houses-cape','furniture','light')],['build/dependencies.json']),
          ('street-signs',['export/set/RoadSigns.gltf'],['set-model']),
          ('freeway',[f'textures/ship/T_{n}_{c}.png' for n in ('FreewayConcrete','FreewayZinc') for c in ('BaseColor','Normal','ORM')],['textures'])]
    for family,required,args in jobs:
        if all((ROOT/family/name).exists() for name in required):continue
        log=Path('build')/('dependency-'+family+'.log')
        with log.open('w') as f:
            subprocess.run(['make','-C',str(ROOT/family),*args,'BLENDER=blender -t 1'],stdout=f,stderr=subprocess.STDOUT,check=True)
        missing=[p for p in required if not (ROOT/family/p).exists()]
        if missing:raise ValueError((family,missing))
    Path('build/dependencies.json').write_text(json.dumps(dict(passed=True,native_only=True),indent=2)+'\n')


if __name__=='__main__':main()
