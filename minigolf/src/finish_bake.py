"""Canonical Minigolf raster fields after validating their GPU emission bakes.

The original color/ORM rasters already describe this flat atlas exactly.
GPU resampling can differ at rounding boundaries between runs. Validate the
projection, then retain authored color/ORM and deterministic physical height
derivatives as authoritative. Keep the GPU normal as an independent check.
"""
import hashlib,json,shutil,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kit.image_io import read_png,write_png

def finish():
 source=Path('build/procedural');out=Path('textures/bake')
 receipt=out/'Minigolf-bake.json';report=json.loads(receipt.read_text());rows={}
 for channel in ('BaseColor','ORM'):
  name='T_Minigolf_'+channel+'.png';original=source/name;baked=out/name
  a=np.asarray(Image.open(original).convert('RGB'),np.float32)/255
  b=np.asarray(Image.open(baked).convert('RGB'),np.float32)/255
  assert a.shape==b.shape==(4096,4096,3),(channel,a.shape,b.shape)
  delta=np.abs(a-b);mean=float(delta.mean());bias=float(np.max(np.abs(a.mean((0,1),dtype=np.float64)-b.mean((0,1),dtype=np.float64))))
  assert mean<.02 and bias<.005,('GPU emission projection/color-space mismatch',channel,mean,bias)
  rows[channel]=dict(source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),gpu_emission_mean_code_error=mean,gpu_emission_max_code_error=float(delta.max()),gpu_emission_mean_code_bias=bias)
  shutil.copyfile(original,baked)
 report['delivery_color_fields']=dict(policy='Exact original 4096 color/ORM raster fields after GPU projection validation; CPU delivery filtering.',channels=rows)
 # Evaluate the same .018 m height range over the same eight-metre tile.
 # Image Y runs down; OpenGL tangent Y runs up. Symmetric derivatives avoid
 # inventing a preferred sampling direction for these authored raster fields.
 height=read_png(source/'T_Minigolf_Height.png')[:,:,0].astype(np.float64)
 size=height.shape[0];assert height.shape==(4096,4096)
 scale=.018/(2*8/size)
 dx=(np.roll(height,-1,axis=1)-np.roll(height,1,axis=1))*scale
 dy=(np.roll(height,-1,axis=0)-np.roll(height,1,axis=0))*scale
 normal=np.stack((-dx,dy,np.ones_like(height)),axis=-1)
 normal/=np.linalg.norm(normal,axis=2,keepdims=True)
 gpu=read_png(out/'T_Minigolf_Normal.png')*2-1
 gpu/=np.linalg.norm(gpu,axis=2,keepdims=True)
 angles=np.degrees(np.arccos(np.clip(np.sum(normal*gpu,axis=2),-1,1)))
 mean=float(angles.mean());p95=float(np.percentile(angles,95))
 assert mean<4 and p95<12,('Physical normal/polarity/footprint mismatch',mean,p95)
 shutil.copyfile(out/'T_Minigolf_Normal.png',out/'T_Minigolf_Normal_GPU.png')
 write_png(out/'T_Minigolf_Normal.png',normal*.5+.5,bits=16)
 report['delivery_normal']=dict(method='Deterministic float64 symmetric height derivatives, OpenGL +Y; GPU Cycles bake retained as independent footprint/polarity check. Sampling kernels differ.',coverage_m=8,height_distance_m=.018,source_height_sha256=hashlib.sha256((source/'T_Minigolf_Height.png').read_bytes()).hexdigest(),gpu_mean_angle_degrees=mean,gpu_p95_angle_degrees=p95)
 report['scope']='channels describe the independent GPU validation bake; delivery_maps describe authoritative deterministic fields.'
 report['delivery_maps']={ch:dict(bytes=(out/f'T_Minigolf_{ch}.png').stat().st_size,sha256=hashlib.sha256((out/f'T_Minigolf_{ch}.png').read_bytes()).hexdigest()) for ch in ('BaseColor','ORM','Normal')}
 receipt.write_text(json.dumps(report,indent=2))
 ready=out/'Minigolf-ready.pending.json'
 ready.write_text(json.dumps(report['delivery_maps'],indent=2));ready.replace(out/'Minigolf-ready.json')
 print('CANONICAL ORIGINAL FIELDS',rows,'NORMAL GPU CHECK',mean,p95)

if __name__=='__main__':finish()
