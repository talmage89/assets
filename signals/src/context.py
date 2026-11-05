"""Build only missing same-clone context exports, preserving every existing byte."""
import subprocess,json
from preserve import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def ensure():
 cases=[
 ('ground','Ground.glb',['export']),
 ('street-light','StreetLight.glb',['export']),
 ('houses','HearthfieldRanch-11.gltf',['TYPE=ranch','SEEDS=11','export']),
 ('houses','HearthfieldCape-31.gltf',['TYPE=cape','SEEDS=31','export']),
 ('houses','HearthfieldSplit-51.gltf',['TYPE=split','SEEDS=51','export']),
 ('trees','PinOak.glb',['SPECIES=oak','export']),
 ('trees','RedMaple.glb',['SPECIES=maple','export']),
 ('cars','AlderC150.glb',['export']),
 ('cars','AlderH120.glb',['BODY=hatch','export']),
 ('cars','AlderX220.glb',['BODY=suv','export']),
 ('commercial','CommercialGas-101.gltf',['SEEDS=101','export'])]
 rows=[]
 for folder,name,args in cases:
  file=ROOT/folder/'export'/name
  if not file.exists():
   with (ROOT/'signals/build'/('context-'+name+'.log')).open('w') as log:
    subprocess.run(['make','-C',str(ROOT/folder),*args],check=True,stdout=log,stderr=subprocess.STDOUT)
  rows.append(dict(source=str(file.relative_to(ROOT)),sha256=sha256(file)))
 (ROOT/'signals/build/context.json').write_text(json.dumps(rows,indent=2))
 print('CONTEXT',len(rows),'local exports ready')
if __name__=='__main__':ensure()
