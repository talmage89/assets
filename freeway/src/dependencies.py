"""Build missing native inputs only; never touch an existing delivery."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
INPUTS=[
    ('ground/export/Ground.glb','ground',['export']),
    ('cars/export/AlderH120.glb','cars',['BODY=hatch','export']),
    ('cars/export/AlderC150.glb','cars',['BODY=crossover','export']),
    ('street-light/export/StreetLight.glb','street-light',['export']),
    ('commercial/export/CommercialStrip-201.gltf','commercial',['SEEDS=201','export']),
    ('cars/export/AlderX220.glb','cars',['BODY=suv','export']),
    ('houses/export/HearthfieldRanch-11.gltf','houses',['TYPE=ranch','SEEDS=11','export']),
    ('houses/export/HearthfieldCape-31.gltf','houses',['TYPE=cape','SEEDS=31','export']),
    ('trees/export/PinOak.glb','trees',['SPECIES=oak','export']),
    ('trees/export/RedMaple.glb','trees',['SPECIES=maple','export']),
    ('commercial/export/CommercialGas-101.gltf','commercial',['SEEDS=101','export']),
]
def main():
    for path,family,args in INPUTS:
        if (ROOT/path).exists():continue
        print('Building missing native input',path,flush=True)
        subprocess.run(['make','-C',str(ROOT/family),*args],check=True)
        assert (ROOT/path).exists(),path
if __name__=='__main__':main()
