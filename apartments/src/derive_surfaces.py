"""Original maintained dark stain over the existing baked cedar manufacture.

Only one small color image is added. Grain/relief and scalar roughness retain
the houses' exact image bytes. No photograph is read by this generator.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from kit.image_io import read_png,write_png,srgb_to_linear,linear_to_srgb

def main():
 source=ROOT/'houses/textures/cape-bake/T_CapeShingle_BaseColor.png'
 a=read_png(source);a=srgb_to_linear(a[len(a)//2:,:,:3])
 y=a@np.array([.2126,.7152,.0722]);level=np.maximum(y,.00001)
 # Maintained semi-solid stain limits exposed-wood color variation while
 # preserving the black key gaps and the underlying physical relief.
 gain=np.clip((level/.30)**.22,.67,1.32)*np.minimum(1,(level/.045)**.5)
 rgb=gain[:,:,None]*np.array([.0735,.0511,.0315])[None,None,:]
 h,w=rgb.shape[:2];rgb=rgb.reshape(256,h//256,512,w//512,3).mean((1,3))
 out=Path('textures/ship');out.mkdir(parents=True,exist_ok=True)
 write_png(out/'T_ApartmentsCedar_BaseColor.png',linear_to_srgb(rgb))
 for channel in ('Normal','ORM'):
  p=ROOT/f'houses/textures/cape-ship/T_CapeCedar_{channel}.png'
  (out/f'T_ApartmentsCedar_{channel}.png').write_bytes(p.read_bytes())
 report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),new_color_pixels=[512,256],new_color_gpu_mib_8bpp_mips=1/6,normal_and_roughness='Exact canonical CapeCedar image bytes')
 Path('build/cedar-stain.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':main()
