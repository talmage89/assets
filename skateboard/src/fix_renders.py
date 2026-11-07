"""Prepare native 1440 px after views; reuse final renders only at that width."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess
from PIL import Image
SHOTS=('hero','hero_bottom','tail_plies','truck','truck_inner','wheel_bearing','grip_edge','grip_macro')
for state in ('season','beat'):
    shots=SHOTS+('wheel_profile',) if state=='beat' else SHOTS
    dst=Path('renders/fixes/after')/state;dst.mkdir(parents=True,exist_ok=True)
    final=Path('renders/final')/state;meta=json.loads((final/'shots.json').read_text())
    digest=hashlib.sha256(Path(f'export/{state}.glb').read_bytes()).hexdigest()
    if all(Image.open(final/(n+'.png')).width==1440 and meta[n]['sha256']==digest for n in shots):
        for name in shots:shutil.copy2(final/(name+'.png'),dst/(name+'.png'))
        (dst/'shots.json').write_text(json.dumps({name:meta[name] for name in shots},indent=2))
    else:
        subprocess.run(['../kit/with_gpu.sh',os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python-exit-code','1','--python','src/render.py','--','--source',f'export/{state}.glb','--out',str(dst),'--width','1440','--samples',os.environ.get('SAMPLES','48'),'--shots',','.join(SHOTS)],check=True)

        if state=='beat':
            subprocess.run(['../kit/with_gpu.sh',os.environ.get('BLENDER','blender'),'-b','--factory-startup','--python-exit-code','1','--python','src/flat_view.py','--','--source',f'export/{state}.glb','--out',str(dst),'--width','1440','--samples',os.environ.get('SAMPLES','48')],check=True)
