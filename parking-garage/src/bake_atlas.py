"""One real GPU bake set, preserving original coverage before filtering."""
import hashlib,json,sys,shutil
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.flat_bake import bake
from kit.image_io import read_png,write_png


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
    report=json.loads((out/'ParkingGarage-bake.json').read_text());report['coverage']='Original analytic alpha retained exactly before linear coverage filtering'
    report['channels']['BaseColor']['bytes']=(out/'T_ParkingGarage_BaseColor.png').stat().st_size
    report['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.glob('*.png')}
    report['baked_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')}
    (out/'ParkingGarage-bake.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
