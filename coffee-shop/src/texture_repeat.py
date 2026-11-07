"""Isolated real GPU rebake; originals remain read-only, compare shipped pixels."""
import hashlib,json,shutil,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import read_png

def main():
    base=Path.cwd();stage=base/'build/texture-repeat'
    original={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (base/'textures/ship').glob('T_CoffeeShop_*.png')}
    if stage.exists():shutil.rmtree(stage)
    stage.mkdir(parents=True)
    cmd=[str(ROOT/'kit/with_gpu.sh'),'blender','-b','--factory-startup','--python-exit-code','1','--python',str(ROOT/'coffee-shop/src/bake_atlas.py')]
    with (base/'build/texture-repeat.log').open('w') as log:subprocess.run(cmd,cwd=stage,stdout=log,stderr=subprocess.STDOUT,check=True)
    rows=[]
    for channel in ('BaseColor','Normal','ORM'):
        filename=f'T_CoffeeShop_{channel}.png';a=read_png(base/'textures/ship'/filename);b=read_png(stage/'textures/ship'/filename);assert a.shape==b.shape
        assert hashlib.sha256((base/'textures/ship'/filename).read_bytes()).hexdigest()==original[filename]
        delta=np.abs(a-b)*255;rmse=float(np.sqrt(np.mean(delta*delta)));maximum=float(delta.max())
        assert maximum<=2.0001 and rmse<=.020001,(channel,maximum,rmse)
        if a.shape[2]==4:assert np.array_equal(a[:,:,3],b[:,:,3]),'Coverage changed'
        rows.append(dict(channel=channel,max_byte_delta=maximum,byte_rmse=rmse,coverage_exact=a.shape[2]!=4 or bool(np.array_equal(a[:,:,3],b[:,:,3]))))
    report=dict(maps=rows,status='real 4096 GPU rebake + channel-aware 2048 filtering; originals unchanged',limits='GPU pixels use max 2/255 and byte-domain RMSE .02, separate from exact source/geometry repeat')
    (base/'build/texture-repeat-check.json').write_text(json.dumps(report,indent=2)+'\n');print('TEXTURE REPEAT PASS',rows)

if __name__=='__main__':main()
