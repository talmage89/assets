"""Factory-startup repeat, including sign sheet and instanced stock shrubs."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def main(blender,look=False):
    folder=Path('build/strip-look/repeat' if look else 'build/strip/repeat');folder.mkdir(parents=True,exist_ok=True)
    with (folder/'build.log').open('w') as log:
        subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python','src/strip_build.py','--','--seeds','201','--out',str(folder)]+(['--look'] if look else []),stdout=log,stderr=subprocess.STDOUT,check=True)
    a=Path('build/strip-look/strip-201.glb' if look else 'build/strip/strip-201.glb');b=folder/a.name
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    row=dict(passed=sha(a)==sha(b),baseline_sha256=sha(a),repeat_sha256=sha(b),bytes=a.stat().st_size,
             scope='Independent factory-startup GLB byte identity, including referenced shipping map bytes. Manufactured maps are reused without another surface bake.')
    (folder/'check.json').write_text(json.dumps(row,indent=2)+'\n');assert row['passed'],row
    print('STRIP REPEAT: byte-identical',row['bytes'],'bytes')


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--blender',default='blender');a.add_argument('--look',action='store_true');a=a.parse_args();main(a.blender,a.look)
