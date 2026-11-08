"""Independent fresh GPU rebake; kit tolerance, exact authored alpha coverage."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];ASSET=HERE.parent;sys.path[:0]=[str(ROOT),str(HERE)]
from textures import SETS
from kit.compare_textures import compare
out=ASSET/'build/texture-repeat'
if out.exists():shutil.rmtree(out)
(out/'textures').mkdir(parents=True);(out/'build').mkdir();(out/'textures/source').symlink_to(ASSET/'textures/source',target_is_directory=True)
cmd=[str(ROOT/'kit/with_gpu.sh'),os.environ.get('BLENDER_BINARY','blender'),'-t','2','-b','--factory-startup','--python-exit-code','1','--python',str(HERE/'bake.py')]
with (out/'bake.log').open('w') as log:subprocess.run(cmd,cwd=out,stdout=log,stderr=subprocess.STDOUT,check=True)
for name,spec in SETS.items():
 subprocess.run([sys.executable,str(ROOT/'kit/downsample.py'),'--source','textures/bake','--out','textures/ship','--asset',name,'--size',str(spec['size'])],cwd=out,check=True,stdout=subprocess.DEVNULL)
result=compare(ASSET/'textures/ship',out/'textures/ship')
a=np.asarray(Image.open(ASSET/'textures/ship/T_FreewayMaintenance_BaseColor.png'))[:,:,3]
b=np.asarray(Image.open(out/'textures/ship/T_FreewayMaintenance_BaseColor.png'))[:,:,3]
result['coverage_alpha_byte_exact']=bool(np.array_equal(a,b));assert result['coverage_alpha_byte_exact']
Path('build/texture-repeat.json').write_text(json.dumps(result,indent=2));assert result['passed'],result
print('TEXTURE REPEAT PASSED',max(r['max_byte_delta'] for r in result['textures']),max(r['rmse_bytes'] for r in result['textures']),'alpha exact')
