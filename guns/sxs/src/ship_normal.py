"""Retain the kit's 16-bit normal precision at the unchanged 2048 size.

The standard kit downsampler supplies BaseColor/ORM. Its normal vector box
filter is repeated from the original 4096 normal, without the final 8-bit
quantization that broke smooth reflection bands on this upper forging.
"""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from kit.image_io import read_png,write_png
BASE=Path(__file__).resolve().parents[1]
size=2048
source=BASE/'build/baked/4k/T_Covey26_Normal.png'
normal=read_png(source)*2-1
assert normal.shape==(4096,4096,3)
normal=normal.reshape(size,2,size,2,3).mean(axis=(1,3))
normal/=np.maximum(np.linalg.norm(normal,axis=2,keepdims=True),1e-8)
path=BASE/'textures/T_Covey26_Normal.png'
write_png(path,normal*.5+.5,16)
report_path=BASE/'textures/texture-report.json';report=json.loads(report_path.read_text())
report['Normal'].update(bits_per_channel=16,bytes=path.stat().st_size,
    reason='Retain the original 4096 bake precision for continuous reflected bands; resolution/atlas unchanged')
report_path.write_text(json.dumps(report,indent=2))
print('SHIPPED NORMAL',size,'RGB16',path.stat().st_size,'bytes')
