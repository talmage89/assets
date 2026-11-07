"""Bake original manufacture fields at 4096 and filter into three shared sets."""
import sys,subprocess,shutil,argparse,json
from pathlib import Path
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT),str(Path(__file__).resolve().parent)]
from kit.flat_bake import bake
from kit.image_io import write_png,read_png
from textures import COVERAGE,HEIGHT,METAL
parser=argparse.ArgumentParser();parser.add_argument('--only',default='PlayMetal,PlayPlastic,PlaySurface');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
for name,size in [('PlayMetal',1024),('PlayPlastic',1024),('PlaySurface',2048)]:
    if name not in args.only.split(','):continue
    source=Path('build/procedural');rgb=Path('build/flat-source');rgb.mkdir(exist_ok=True)
    Image.open(source/f'T_{name}_BaseColor.png').convert('RGB').save(rgb/f'T_{name}_BaseColor.png')
    for c in ('ORM','Height'):shutil.copyfile(source/f'T_{name}_{c}.png',rgb/f'T_{name}_{c}.png')
    bake(rgb,Path('textures/bake'),name,COVERAGE[name],4096,8,height_distance=HEIGHT[name])
    if name=='PlayMetal':
        path=Path('textures/bake')/f'T_{name}_Normal.png';normal=read_png(path)[:,:,:3]*2-1
        calibration={}
        for cell,dimensions in [('Chain',(.036,.72)),('Fastener',(.016,.016))]:
            a,b,c,d=METAL[cell];x0,y0,x1,y1=round(a*4096),round((1-d)*4096),round(c*4096),round((1-b)*4096)
            coverage=((c-a-16/1024)*COVERAGE[name],(d-b-16/1024)*COVERAGE[name]);scale=[coverage[i]/dimensions[i] for i in range(2)]
            n=normal[y0:y1,x0:x1];n[:,:,0]*=scale[0];n[:,:,1]*=scale[1];n/=np.maximum(np.linalg.norm(n,axis=-1,keepdims=True),1e-8)
            calibration[cell]=dict(physical_chart_m=dimensions,tangent_slope_scale=scale)
        write_png(path,normal*.5+.5,bits=16)
        report_path=Path('textures/bake')/f'{name}-bake.json';report=json.loads(report_path.read_text());report['normal_slope_calibration']=calibration;report['channels']['Normal']['bytes']=path.stat().st_size;report_path.write_text(json.dumps(report,indent=2))
    im=np.asarray(Image.open(Path('textures/bake')/f'T_{name}_BaseColor.png').convert('RGB'),dtype=np.float32)/255
    alpha=np.asarray(Image.open(source/f'T_{name}_BaseColor.png').getchannel('A'),dtype=np.float32)/255
    write_png(Path('textures/bake')/f'T_{name}_BaseColor.png',np.dstack((im,alpha)))
    subprocess.run(['python3',str(ROOT/'kit/downsample.py'),'--source','textures/bake','--out','textures/ship','--asset',name,'--size',str(size)],check=True)
    Path('textures/ship/texture-report.json').replace(Path('textures/ship')/(name+'-texture-report.json'))
Path('textures/ship/.stamp').touch()
