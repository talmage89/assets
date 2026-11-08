"""Independent 4096 GPU rebake, channel filtering, kit tolerance plus alpha."""
import argparse,json,shlex,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.compare_textures import compare

def main():
    p=argparse.ArgumentParser();p.add_argument('--blender',default='blender -t 4');a=p.parse_args()
    folder=Path('build/texture-repeat');folder.mkdir(exist_ok=True)
    commands=[['../kit/with_gpu.sh']+shlex.split(a.blender)+['-b','--factory-startup',
        '--python-exit-code','1','--python','src/bake.py','--','--source','build/finalized.blend',
        '--out',str(folder/'4k'),'--size','4096','--samples','12'],
        ['python3','../kit/downsample.py','--source',str(folder/'4k'),'--out',str(folder/'2k'),
         '--asset','SchoolBus','--size','2048','--alpha-mode','independent']]
    with (folder/'rebake.log').open('w') as log:
        for cmd in commands:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
    result=compare('textures/2k',folder/'2k')
    left=np.asarray(Image.open('textures/2k/T_SchoolBus_BaseColor.png'))[:,:,3].astype(float)
    right=np.asarray(Image.open(folder/'2k/T_SchoolBus_BaseColor.png'))[:,:,3].astype(float)
    delta=left-right;maximum=float(np.abs(delta).max());rmse=float(np.sqrt(np.mean(delta**2)))
    result['independent_alpha']=dict(max_byte_delta=maximum,rmse_bytes=rmse,
                                      passed=maximum<=2 and rmse<=.02)
    result['passed'] &= result['independent_alpha']['passed']
    Path('build/texture-repeat.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if not result['passed']:raise SystemExit(1)

if __name__=='__main__':main()
