"""Factory-startup repeat, including the external glTF/BIN delivery."""
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
    assert row['passed'],row
    if look:
        # Convert the independently rebuilt scene at the canonical delivery path
        # so relative shared-image URIs are part of the exact-byte comparison.
        # Restore all three baseline files even if the converter/test fails.
        from strip_delivery import run as deliver
        paths=[Path('export/CommercialStrip-201'+suffix) for suffix in ('.gltf','.bin','.json')]
        baseline={p:p.read_bytes() for p in paths}
        try:
            deliver([201],folder)
            external=[dict(file=str(p),bytes=len(baseline[p]),
                           baseline_sha256=hashlib.sha256(baseline[p]).hexdigest(),repeat_sha256=sha(p))
                      for p in paths[:2]]
            assert all(r['baseline_sha256']==r['repeat_sha256'] for r in external),external
        finally:
            for p,data in baseline.items():p.write_bytes(data)
        row['external_delivery']=dict(passed=True,files=external,bytes=sum(r['bytes'] for r in external))
        row['scope']+=' External glTF/BIN bytes, including canonical shared-image URIs and punctual lights, are also identical.'
    (folder/'check.json').write_text(json.dumps(row,indent=2)+'\n')
    print('STRIP REPEAT: byte-identical',row['bytes'],'embedded intermediate bytes',
          'and '+str(row['external_delivery']['bytes'])+' external delivery bytes' if look else '')


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--blender',default='blender');a.add_argument('--look',action='store_true');a=a.parse_args();main(a.blender,a.look)
