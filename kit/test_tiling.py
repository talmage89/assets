"""Small real export/bake regression; run through with_gpu.sh, no downloads."""
from pathlib import Path
import sys
import bpy
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kit.tiling import material,world_uv,export,edge_error
from kit.image_io import write_png,read_png
from kit.gltf import GLB
from kit.flat_bake import bake

folder=Path(__file__).resolve().parents[1]/'build/test-tiling';folder.mkdir(parents=True,exist_ok=True)
a=np.zeros((32,32,3),np.float32);a[:]=(.2,.5,.7)
write_png(folder/'T_Fixture_BaseColor.png',a)
write_png(folder/'T_Fixture_Normal.png',np.tile([.5,.5,1],(32,32,1)))
write_png(folder/'T_Fixture_ORM.png',np.tile([.95,.8,0],(32,32,1)))
write_png(folder/'T_Fixture_Height.png',np.full((32,32,1),.5))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_plane_add(size=2,location=(3,5,0));ob=bpy.context.object;ob.name='Test tile'
world_uv(ob,2);ob.data.materials.append(material('Fixture',folder,tint=True))
attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
for i in range(4):attr.data[i].color=(.91,.93,.95,1)
# Mixed slots must not export unused COLOR_0 on an untinted atlas primitive.
rgba=np.concatenate([a,np.ones((32,32,1),np.float32)],axis=2);rgba[:8,:,3]=.4
write_png(folder/'T_Untinted_BaseColor.png',rgba)
write_png(folder/'T_Untinted_Normal.png',np.tile([.5,.5,1],(32,32,1)))
write_png(folder/'T_Untinted_ORM.png',np.tile([1,.9,0],(32,32,1)))
ob.data.materials.append(material('Untinted',folder,alpha=True,tint=False))
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.quads_convert_to_tris();bpy.ops.object.mode_set(mode='OBJECT')
ob.data.polygons[1].material_index=1
# Saving must not invalidate image paths; this failed with relative image loads.
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'nested.blend'))
path=folder/'Fixture.glb';export(path);g=GLB(path)
assert len(g.json['images'])==6 and len(g.json['materials'])==2
for primitive in g.json['meshes'][0]['primitives']:
    m=g.json['materials'][primitive['material']]
    assert ('COLOR_0' in primitive['attributes']) == m['extras']['tiling_vertex_tint']
p=next(p for p in g.json['meshes'][0]['primitives'] if 'COLOR_0' in p['attributes'])
uv=g.accessor(p['attributes']['TEXCOORD_0']);assert np.max(np.abs(uv[:,0]-np.round(uv[:,0])))<1e-6
m=next(m for m in g.json['materials'] if m['name']=='Fixture');assert 'normalTexture' in m and 'occlusionTexture' in m
assert 'baseColorTexture' in m['pbrMetallicRoughness']
first=[[0,0,0,0,0,1,0,0],[1,0,0,0,0,1,.5,0]]
assert edge_error(first,first)['passed']
for index in (0,3,6):
    bad=np.array(first,dtype=float);bad[0,index]+=.01
    assert not edge_error(first,bad)['passed']
bake(folder,folder/'bake','Fixture',2,32,2)
result=read_png(folder/'bake/T_Fixture_BaseColor.png');assert np.max(np.abs(result-a))<2/255
normal=read_png(folder/'bake/T_Fixture_Normal.png');assert np.max(np.abs(normal-np.array([.5,.5,1])))<.001
print('PASS tiling: authored UV, vertex tint, embedded PBR, saved-file paths, negative seams, flat-bake sRGB and tangent normal')
