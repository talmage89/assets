"""Small real GLB regression for shared RGBA atlases and per-face profiles."""
import sys,json,io,runpy
from pathlib import Path
import bpy,numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'kit')]
from kit import model as G,export
from kit.gltf import GLB
from kit.image_io import write_png,read_png
folder=ROOT/'build/surface-test';folder.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
for channel in ['BaseColor','Normal','ORM']:
    array=np.empty((16,16,4 if channel=='BaseColor' else 3),np.float32)
    array[:]=(.2,.4,.6,.25) if channel=='BaseColor' else ((.5,.5,1) if channel=='Normal' else (1,.3,.8))
    write_png(folder/f'T_Fixture_{channel}.png',array)
root=G.pivot('Fixture',(0,0,0));root['static_root']=True
for i,name in enumerate(['SourcePaint','SourceTrim','SourceGlass','SourceLamp']):
    mat=bpy.data.materials.new(name);ob=G.box(name,(i,0,0),(.5,.5,.5),mat,0)
    G.attach(ob,root,asset_set='Fixture');ob.data.uv_layers.new(name='BakeUV')
    if i==0:
        other=bpy.data.materials.new('MixedTrim');ob.data.materials.append(other)
        ob.data.polygons[0].material_index=1
source=folder/'source.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source))
cfg=dict(SOURCE_MATERIAL_SURFACES=dict(SourcePaint='Paint',SourceTrim='Trim',MixedTrim='Trim',SourceGlass='Glass',SourceLamp='Lamp'),
 DELIVERY_SURFACES=dict(Paint=dict(principled={'Coat Weight':1,'Coat Roughness':.035},factors={'Metallic':.12},extras={'paint_reference_color':[.1,.2,.3]}),Trim={},Glass=dict(principled={'Transmission Weight':1,'IOR':1.5}),Lamp=dict(emission_strength=80)))
config=folder/'config.py';config.write_text('\n'.join(k+'='+repr(v) for k,v in cfg.items()))
sys.argv=['blender','--','--source',str(source),'--textures',str(folder),'--asset','Fixture','--out',str(folder/'fixture.glb'),'--report',str(folder/'report.json'),'--config',str(config)]
export.main();glb=GLB(folder/'fixture.glb');doc=glb.json
assert len(doc['materials'])==4
assert len(doc['images'])==len(doc['textures'])==3
paint=next(m for m in doc['materials'] if m['name']=='Fixture Paint')
assert abs(paint['pbrMetallicRoughness'].get('metallicFactor',1)-.12)<1e-6,paint
assert paint['extras']['paint_reference_color']==[.1,.2,.3]
image_index=doc['textures'][paint['pbrMetallicRoughness']['baseColorTexture']['index']]['source']
rgba=np.asarray(Image.open(io.BytesIO(glb.image(image_index))).convert('RGBA'))
assert (rgba[:,:,3]==64).all(),np.unique(rgba[:,:,3])
# Also exercise the real downsampler: alpha is linear coverage, never sRGB.
sys.argv=['downsample','--source',str(folder),'--out',str(folder/'ship'),'--asset','Fixture','--size','8']
runpy.run_path(str(ROOT/'kit/downsample.py'),run_name='__main__')
shipped=read_png(folder/'ship/T_Fixture_BaseColor.png')
assert shipped.shape==(8,8,4) and abs(float(shipped[:,:,3].mean())-64/255)<1e-6
print('PASS: four per-face profiles share three textures; metallic factor, RGBA coverage and linear alpha filtering survive')
