"""Real finalize/export fixture for authored tile normals and untinted data masks."""
import json,runpy,sys
from pathlib import Path
import bpy,numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import botany,finalize,export,gltf
runpy.run_path(str(ROOT/'kit/test_atlas.py'))
f=ROOT/'build/atlas-test'
legacy=gltf.GLB(f/'fixture.glb')
assert all('_WIND' not in p['attributes'] for m in legacy.json['meshes'] for p in m['primitives'])
bpy.ops.wm.open_mainfile(filepath=str(f/'source.blend'))
expected={}
for ob in bpy.context.scene.objects:
    if ob.type!='MESH':continue
    values=[(i/(len(ob.data.vertices)+1),.5,.37,.85) for i in range(len(ob.data.vertices))]
    botany.wind_attribute(ob,values)
    priority=ob.data.attributes.new(name='FixtureUVPriority',type='FLOAT',domain='FACE')
    for i,item in enumerate(priority.data):item.value=2.0 if i==0 else .6
    if ob.name=='Sheet_Fabric':
        ob.data.normals_split_custom_set([(0,-.6,.8)]*len(ob.data.loops))
        expected['normals']=np.array([n.vector for n in ob.data.corner_normals])
    expected[ob.name]={}
    for v in ob.data.vertices:
        expected[ob.name].setdefault(tuple(round(x,6) for x in v.co),[]).append(values[v.index])
bpy.ops.wm.save_as_mainfile(filepath=str(f/'botanical-source.blend'))
cfg=runpy.run_path(str(f/'config.py'));cfg={k:v for k,v in cfg.items() if not k.startswith('__')}
cfg['UV_NORMALIZE_ISLAND_SCALE']=True;cfg['UV_PRIORITY_ATTRIBUTE']='FixtureUVPriority';cfg['EXPORT_COLOR_DATA']={'Wind':'_WIND'};cfg['TILED_MESHES']['*_Fabric']['preserve_normals']=True
config=f/'botanical-config.py';config.write_text('\n'.join(k+'='+repr(v) for k,v in cfg.items()))
sys.argv=['blender','--','--source',str(f/'botanical-source.blend'),'--out',str(f/'botanical-final.blend'),'--report',str(f/'botanical-uv.json'),'--config',str(config),'--size','512','--target-density','1000']
finalize.main()
uv_result=json.loads((f/'botanical-uv.json').read_text())
densities=[r['density_px_m'] for r in uv_result['island_measurements']]
assert max(densities)/min(densities)>1.15,'Regional UV priority did not survive normalization/packing'
ob=bpy.data.objects['Sheet_Fabric']
assert np.max(np.abs(np.array([n.vector for n in ob.data.corner_normals])-expected['normals'][0]))<1e-4
sys.argv=['blender','--','--source',str(f/'botanical-final.blend'),'--textures',str(f/'textures'),'--asset','TileFixture','--out',str(f/'botanical.glb'),'--report',str(f/'botanical-export.json'),'--config',str(config)]
export.main();raw=gltf.GLB(f/'botanical.glb')
for mesh in raw.json['meshes']:
    for prim in mesh['primitives']:
        attrs=prim['attributes'];assert '_WIND' in attrs and not any(k.startswith('COLOR_') for k in attrs)
        pos=raw.accessor(attrs['POSITION']);pos=np.c_[pos[:,0],-pos[:,2],pos[:,1]]
        values=raw.accessor(attrs['_WIND'])
        name='Frame' if mesh['name']=='TileFixtureMesh' else mesh['name']
        for p,w in zip(pos,values):
            key=tuple(round(float(x),6) for x in p)
            assert min(max(abs(a-b) for a,b in zip(w,row)) for row in expected[name][key])<1e-6, (name,key,w,expected[name][key])
        if name=='Sheet_Fabric':
            normals=raw.accessor(attrs['NORMAL']);normals=np.c_[normals[:,0],-normals[:,2],normals[:,1]]
            assert np.max(np.abs(normals-expected['normals'][0]))<1e-4
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(f/'botanical.glb'))
assert '_WIND' in bpy.data.objects['Sheet_Fabric'].data.attributes
print('PASS: exact linear _WIND survives as untinted custom data; bent normals survive triangulate/export/import; legacy defaults unchanged')

# A blue transparent texel must not pollute a retained red cutout in linear filtering.
from kit.image_io import write_png,read_png
src=f/'rgba-source';dst=f/'rgba-ship';src.mkdir(exist_ok=True)
bc=np.zeros((8,8,4));bc[:,:,:3]=(0,0,1);bc[::2,::2]=(1,0,0,1)
write_png(src/'T_RGBA_BaseColor.png',bc)
write_png(src/'T_RGBA_Normal.png',np.full((8,8,3),(.5,.5,1)))
write_png(src/'T_RGBA_ORM.png',np.full((8,8,3),(1,.7,0)))
sys.path.insert(0,str(ROOT/'kit'))
sys.argv=['downsample','--source',str(src),'--out',str(dst),'--asset','RGBA','--size','4']
runpy.run_path(str(ROOT/'kit/downsample.py'),run_name='__main__')
filtered=read_png(dst/'T_RGBA_BaseColor.png')
assert filtered.shape==(4,4,4)
assert np.max(np.abs(filtered-np.array([1,0,0,.25])))<1/255
print('PASS: linear alpha and premultiplied color filtering reject transparent-color contamination')

# Coincident blade vertices may carry different flutter AND split normals.
# Exercise the shared audit through real export/import, then corrupt one mask.
from kit import botanical_delivery,model as G
bpy.ops.wm.open_mainfile(filepath=str(f/'botanical-final.blend'))
frame=bpy.data.objects['Frame'];frame.name='TileFixtureMesh';frame['export_part']=frame.name
verts=[(0,-.1,0),(.4,-.1,0),(.4,-.1,.6),(0,-.1,.6)]*2
ob=G.mesh('Coincident_Fabric',verts,[(0,1,2,3),(4,5,6,7)],bpy.data.materials[0])
G.attach(ob,bpy.data.objects['TileFixture'],asset_set='TileFixture');ob['export_part']=ob.name;ob['allow_boundary']=True
uv=ob.data.uv_layers.new(name='BakeUV')
for face in ob.data.polygons:
    for li,co in zip(face.loop_indices,[(.01,.01),(.25,.01),(.25,.25),(.01,.25)]):uv.data[li].uv=co
ob.data.normals_split_custom_set([(0,-.6,.8)]*4+[(0,-.8,.6)]*4)
botany.wind_attribute(ob,[(.2,.5,.3,.8)]*4+[(.8,.75,.6,.9)]*4)
bpy.ops.wm.save_as_mainfile(filepath=str(f/'coincident.blend'))
sys.argv=['blender','--','--source',str(f/'coincident.blend'),'--textures',str(f/'textures'),'--asset','TileFixture','--out',str(f/'coincident.glb'),'--report',str(f/'coincident-export.json'),'--config',str(config)]
export.main()
sys.argv=['blender','--','--source',str(f/'coincident.blend'),'--glb',str(f/'coincident.glb'),'--out',str(f/'coincident-audit.json')]
botanical_delivery.main()
assert json.loads((f/'coincident-audit.json').read_text())['passed']
bpy.ops.wm.open_mainfile(filepath=str(f/'coincident.blend'))
bpy.data.objects['Coincident_Fabric'].data.color_attributes['Wind'].data[0].color=(.9,.1,.1,.1)
bpy.ops.wm.save_as_mainfile(filepath=str(f/'coincident-corrupt.blend'))
sys.argv=['blender','--','--source',str(f/'coincident-corrupt.blend'),'--glb',str(f/'coincident.glb'),'--out',str(f/'coincident-rejected.json')]
try:botanical_delivery.main()
except RuntimeError:pass
else:raise AssertionError('Changed Wind passed the shared audit')
print('PASS: coincident vertices retain independent Wind/normals; changed Wind is rejected')
