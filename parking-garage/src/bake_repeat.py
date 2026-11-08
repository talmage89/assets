"""Independently repeat the real bake without touching canonical deliveries.

Run through kit/with_gpu.sh. Fixed acceptance: <= one 8-bit code maximum,
mean absolute normalized error <= 1e-5, checked on the actual shipped maps.
"""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path[:0]=[str(ROOT),str(HERE)]
from kit.flat_bake import bake
from kit.image_io import read_png,write_png
from bake_atlas import reconcile_guards


def main():
    Path('build/lookdev/bake-repeat.json').unlink(missing_ok=True)
    out=Path('build/lookdev/repeat-bake');ship=Path('build/lookdev/repeat-ship')
    ship.mkdir(parents=True,exist_ok=True)
    bake(Path('build/lookdev/atlas-bake-input'),out,'ParkingGarage',6.096,4096,8,height_distance=.008)
    rgb=read_png(out/'T_ParkingGarage_BaseColor.png')
    alpha=np.asarray(Image.open('build/lookdev/atlas-source/T_ParkingGarage_BaseColor.png'))[:,:,3]/255
    write_png(out/'T_ParkingGarage_BaseColor.png',np.dstack([rgb,alpha]))
    reconcile_guards(out)
    subprocess.run(['python3',str(ROOT/'kit/downsample.py'),'--source',str(out),'--out',str(ship),'--asset','ParkingGarage','--size','2048'],check=True)
    channels={}
    for channel in ('BaseColor','Normal','ORM'):
        name=f'T_ParkingGarage_{channel}.png';a=Path('textures/lookdev/ship')/name;b=ship/name
        delta=np.abs(read_png(a)-read_png(b))
        channels[channel]=dict(byte_identical=a.read_bytes()==b.read_bytes(),max_error=float(delta.max()),
            mean_error=float(delta.mean()),sha256=hashlib.sha256(b.read_bytes()).hexdigest())
        assert delta.max()<=1/255+1e-7 and delta.mean()<=1e-5,channels[channel]
    report=dict(passed=True,channels=channels,max_allowed=1/255,mean_allowed=1e-5,
        canonical_outputs_modified=False,method='Independent 4096 Cycles bake and coverage/vector/RMS 2048 filter')
    Path('build/lookdev/bake-repeat.json').write_text(json.dumps(report,indent=2)+'\n')
    print('INDEPENDENT GPU BAKE REPEAT PASS',report,flush=True)


if __name__=='__main__':main()
