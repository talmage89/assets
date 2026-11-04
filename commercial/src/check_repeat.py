"""Independent factory-startup repeat of the default diagnostic form export."""
import argparse,hashlib,json,subprocess
from pathlib import Path


def main(blender='blender'):
 out=Path('build/repeat');out.mkdir(parents=True,exist_ok=True)
 with Path('build/repeat.log').open('w') as log:
  subprocess.run([blender,'-b','--factory-startup','--python-exit-code','1','--python','src/build.py','--','--seeds','101','--out',str(out/'station-101.blend')],stdout=log,stderr=subprocess.STDOUT,check=True)
 a=Path('build/station-101.glb');b=out/a.name
 sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 result=dict(seed=101,scope='Separate factory-startup build; byte equality includes geometry, node frames, preview materials and embedded original lettering. Not a bake repeat test.',baseline_sha256=sha(a),repeat_sha256=sha(b),bytes=a.stat().st_size)
 result['passed']=result['baseline_sha256']==result['repeat_sha256']
 Path('build/repeat-check.json').write_text(json.dumps(result,indent=2))
 assert result['passed'],'Nondeterministic default station export'
 print('REPEAT byte-identical',result['bytes'],'bytes',result['baseline_sha256'])


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--blender',default='blender');main(p.parse_args().blender)
