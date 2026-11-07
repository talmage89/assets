"""Repeat exports from the accepted UVs/maps; does not claim a repeated GPU bake."""
from pathlib import Path
import subprocess,hashlib,json,os
result={}
for state in ('new','season','beat'):
    dst=Path(f'build/{state}/repeat.glb')
    subprocess.run(['../kit/with_gpu.sh',os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python-exit-code','1','--python','../kit/export.py','--','--source',f'build/{state}/finalized.blend','--textures',f'textures/{state}','--asset','Skateboard','--out',str(dst),'--report',f'build/{state}/repeat-export.json','--config','src/config.py'],check=True)
    old=Path(f'export/{state}.glb').read_bytes();new=dst.read_bytes();assert old==new,state+' export differs'
    result[state]=dict(byte_identical=True,sha256=hashlib.sha256(new).hexdigest())
Path('build/repeat-delivery.json').write_text(json.dumps(result,indent=2));print(result)
