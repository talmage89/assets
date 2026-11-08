"""Isolated rebuild of form geometry and original graphic bytes.

There is no GPU bake at this checkpoint, so no texture-tolerance claim is made.
Native image resources remain immutable canonical inputs.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

HERE=Path(__file__).resolve().parent;ASSET=HERE.parent;ROOT=ASSET.parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    stage=ASSET/'build/repeat-repo'
    if stage.exists():shutil.rmtree(stage)
    folder=stage/'parking-garage';folder.mkdir(parents=True);shutil.copytree(HERE,folder/'src')
    for family in ('kit','ground','street-light','cars','trees'):(stage/family).symlink_to(ROOT/family,target_is_directory=True)
    (folder/'build').mkdir();env=dict(os.environ,TMPDIR=str(ASSET/'build/tmp'));Path(env['TMPDIR']).mkdir(parents=True,exist_ok=True)
    with (ASSET/'build/repeat.log').open('w') as log:
        subprocess.run([str(folder/'src/blender.sh'),'-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--out','build/ParkingGarage.blend'],cwd=folder,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    wanted=[p for p in (ASSET/'export').rglob('*') if p.is_file() and p.suffix in ('.gltf','.bin') and 'sites' not in p.relative_to(ASSET/'export').parts]
    wanted += list((ASSET/'textures/checkpoint').glob('*.png'))
    wanted += [ASSET/'build'/n for n in ('manifest.json','modules.json','garage-101.json','garage-202.json')]
    rows=[]
    for p in wanted:
        q=folder/p.relative_to(ASSET);assert q.exists(),q
        rows.append(dict(path=str(p.relative_to(ASSET)),bytes=p.stat().st_size,sha256=sha(p),repeated_sha256=sha(q),identical=p.read_bytes()==q.read_bytes()))
    report=dict(files=rows,passed=all(r['identical'] for r in rows),scope='Independent form geometry, shared-image glTF manifests and original graphics; no baked look-dev maps or stochastic renders.')
    (ASSET/'build/repeat.json').write_text(json.dumps(report,indent=2)+'\n')
    assert report['passed'],[r['path'] for r in rows if not r['identical']]
    print('REPEAT PASS',len(rows),'files',sum(r['bytes'] for r in rows),'bytes',flush=True)


if __name__=='__main__':main()
