"""One real GPU bake set, preserving original coverage before filtering."""
import hashlib,json,sys,shutil
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.flat_bake import bake
from kit.image_io import read_png,write_png,srgb_to_linear,linear_to_srgb


def reconcile_guards(folder):
    layout=json.loads(Path('build/lookdev/atlas-layout.json').read_text())
    for channel in ('BaseColor','Normal','ORM'):
        path=folder/f'T_ParkingGarage_{channel}.png';data=read_png(path)
        work=srgb_to_linear(data[:,:,:3]) if channel=='BaseColor' else data*2-1 if channel=='Normal' else data.copy()
        if channel=='ORM':work[:,:,1]**=2
        for name in ('precast','cast','steel'):
            a,b,c,d=layout[name]['rect'];lo=round((1-d)*len(work));hi=round((1-b)*len(work))
            # Duplicate analytic samples carry independent bake-AA estimates.
            for left,right in ((slice(lo-16,lo),slice(hi-16,hi)),(slice(hi,hi+16),slice(lo,lo+16))):
                mean=(work[left]+work[right])/2
                if channel=='Normal':mean/=np.maximum(np.linalg.norm(mean,axis=2,keepdims=True),1e-8)
                work[left]=mean;work[right]=mean
        if channel=='BaseColor':data[:,:,:3]=linear_to_srgb(work)
        elif channel=='Normal':data=work*.5+.5
        else:work[:,:,1]=np.sqrt(work[:,:,1]);data=work
        write_png(path,data,bits=16 if channel=='Normal' else 8)


def main():
    source=Path('build/lookdev/atlas-source');out=Path('build/lookdev/atlas-bake')
    inputs=Path('build/lookdev/atlas-bake-input');inputs.mkdir(parents=True,exist_ok=True)
    # Texture-node color is associated with PNG coverage. Bake opaque RGB so
    # transparent mark margins cannot darken the lighting-independent albedo.
    Image.open(source/'T_ParkingGarage_BaseColor.png').convert('RGB').save(inputs/'T_ParkingGarage_BaseColor.png')
    for channel in ('Height','ORM'):shutil.copyfile(source/f'T_ParkingGarage_{channel}.png',inputs/f'T_ParkingGarage_{channel}.png')
    bake(inputs,out,'ParkingGarage',6.096,4096,8,height_distance=.008)
    rgb=read_png(out/'T_ParkingGarage_BaseColor.png')
    alpha=np.asarray(Image.open(source/'T_ParkingGarage_BaseColor.png'))[:,:,3].astype(float)/255
    write_png(out/'T_ParkingGarage_BaseColor.png',np.dstack([rgb,alpha]))
    reconcile_guards(out)
    report=json.loads((out/'ParkingGarage-bake.json').read_text());report['coverage']='Original analytic alpha retained exactly before linear coverage filtering'
    report['channels']['BaseColor']['bytes']=(out/'T_ParkingGarage_BaseColor.png').stat().st_size
    report['periodic_guards']='Duplicate analytic guard samples averaged in linear color, RMS roughness and normalized tangent-vector space.'
    for channel in ('Normal','ORM'):report['channels'][channel]['bytes']=(out/f'T_ParkingGarage_{channel}.png').stat().st_size
    report['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('*.png')}
    report['baked_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')}
    (out/'ParkingGarage-bake.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
