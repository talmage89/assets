"""Real export fixture: legacy atlas and lossless small detachable texture sets.

No bake: these deliberately difficult original maps stand in for shipped baked
pixels. Run in a fresh Blender process; all outputs stay under build/.
"""
import json
import runpy
import sys
from pathlib import Path

import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from kit import export, model as G, weapon as W
from kit import detachable_textures as D, detachable_verify as V
from kit.gltf import GLB,stabilize_tangents
from kit.image_io import write_png,read_png

# Exercise the opaque-alpha specular idiom used by real deliverables.
original_material = export.atlas_material
def alpha_material(*args,**kwargs):
    material=original_material(*args,**kwargs);nt=material.node_tree
    shader=nt.nodes['SURFACE'];color=shader.inputs['Base Color'].links[0].from_node
    factor=nt.nodes.new('ShaderNodeMath');factor.operation='MULTIPLY';factor.inputs[1].default_value=.5
    nt.links.new(color.outputs['Alpha'],factor.inputs[0]);nt.links.new(factor.outputs[0],shader.inputs['Specular IOR Level'])
    return material
export.atlas_material=alpha_material

out = ROOT/'build/detachable-textures';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
arm = W.armature('Fixture',{'Root':(0,0,0),'Magazine':(0,.03,0),'Round':(0,.035,.01)},parents={'Round':'Magazine'})
for bone,center in [('Root',(0,0,0)),('Magazine',(0,.03,0)),('Round',(0,.035,.01))]:
    ob = G.box(bone+' part',center,(.01,.016,.006),None,0);G.apply(ob)
    ob['asset_set'] = 'SubsetFixture';W.rigid_bind(ob,arm,bone)
    uv = ob.data.uv_layers.new(name='BakeUV')
    # Small separated islands with fractional pixel phase. All faces are packed
    # deliberately far apart in the atlas; a simple global crop cannot fit.
    for face in ob.data.polygons:
        ox = 40+face.index%3*700+(23 if bone=='Round' else 0)
        oy = 50+face.index//3*800+(170 if bone=='Round' else 0)
        for i,loop in enumerate(face.loop_indices):
            x,y = [(0,0),(80,0),(80,100),(0,100)][i]
            uv.data[loop].uv = ((ox+x+.27)/2048,(oy+y+.39)/2048)
# A skew chart near the far atlas corner exercises glTF's rounded 1-v
# conversion, unlike axis-aligned box charts. Its storage error is measured
# in delivered pixels; a fixed normalized-UV threshold depends on map size.
mesh=bpy.data.meshes.new('Precision patch')
mesh.from_pydata([(.001,0,0),(0,.003,0),(0,.001,0)],[],[(0,1,2)])
patch=bpy.data.objects.new('Magazine precision patch',mesh)
bpy.context.collection.objects.link(patch);patch['asset_set']='SubsetFixture'
W.rigid_bind(patch,arm,'Magazine');layer=mesh.uv_layers.new(name='BakeUV')
for i,(u,v) in enumerate(((.8785316944,.8754293323),(.8764206767,.8779888749),(.8923629522,.8780236244))):
    layer.data[i].uv=(u,1-v)
W.action(arm,'Loaded',[(0,{}),W.hold(1)])
W.action(arm,'Empty',[(0,{'Round':dict(scale=(0,0,0))}),W.hold(1)])
W.action(arm,'Tilt',[(0,{}),(12,{'Magazine':dict(loc=(.01,-.02,.03),rot_deg=(24,32,-13))}),W.hold(15)])
bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
rigged_source_bytes=(out/'source.blend').read_bytes()
# High frequency changes catch even one-texel errors. Independent alpha tests
# opaque specular data preservation, not just RGB.
y,x = np.mgrid[:2048,:2048];textures = out/'textures'
color = np.stack((x%251/250,y%241/240,((x//3+y//5)%2)*.8+.1,(x+y)%239/238),axis=-1)
normal = np.stack((.25*np.sin(x*.7),.25*np.cos(y*.6),np.ones_like(x)),axis=-1)
normal /= np.linalg.norm(normal,axis=-1,keepdims=True);normal=normal*.5+.5
orm = np.stack(((x%31)/30,(y%53)/52,((x+y)%71)/70),axis=-1)
for channel,values in [('BaseColor',color),('Normal',normal),('ORM',orm)]:
    write_png(textures/f'T_SubsetFixture_{channel}.png',values)
base = dict(EXPORT_VARIANT=0,EXPORT_SKIN_NAMES={'Fixture':'FixtureSkin'},
            EXPORT_ANIMATIONS={'clips':['Loaded','Empty','Tilt']},
            MATERIAL_OVERRIDES={'':dict(specular=.28)},
            DETACHABLES=[dict(armature='Fixture',bone='Magazine',bones=['Magazine','Round'],
                              name='Magazine',filename=state.lower()+'.glb',clip=state,frame=0)
                         for state in ('Loaded','Empty','Tilt')])
def deliver(config, directory):
    directory.mkdir(exist_ok=True);cfg=directory/'config.py'
    cfg.write_text('\n'.join(k+'='+repr(v) for k,v in config.items()))
    sys.argv=['blender','--','--source',str(out/'source.blend'),'--textures',str(textures),
              '--asset','SubsetFixture','--out',str(directory/'main.glb'),
              '--report',str(directory/'export.json'),'--config',str(cfg)]
    export.main()
legacy=out/'legacy';small=out/'small'
deliver(base,legacy)
opted={**base,'DETACHABLES':[{**row,'texture_size':512} for row in base['DETACHABLES']]}
deliver(opted,small)
assert (legacy/'main.glb').read_bytes()==(small/'main.glb').read_bytes(), 'Main delivery changed'
records={}
for state in ('loaded','empty','tilt'):
    path=small/(state+'.glb');layout=small/'detachables'/state/'layout.json'
    records[state]=dict(comparison=V.compare(legacy/(state+'.glb'),path),
                        audit=V.audit(path,textures,'SubsetFixture',layout,gun=small/'main.glb'),
                        mip_bleed=V.mip_bleed(path,textures,'SubsetFixture',layout,gun=small/'main.glb'))
    assert records[state]['audit']['size']==512,'Must honor requested size'
    assert path.stat().st_size < (legacy/(state+'.glb')).stat().st_size
    # Legacy path remains byte-identical to canonical source PNGs.
    g=GLB(legacy/(state+'.glb'))
    assert {g.image(i) for i in range(3)} == {p.read_bytes() for p in textures.glob('*.png')}
    assert records[state]['audit']['padding_px']>=6
# Exercise the negative mip checks against the same unmodified surface texels.
# Append replacement PNG views: original mesh/accessor BIN bytes stay intact.
import io,struct,copy
from PIL import Image

def mutated(path,name,*,black_background=False,sampler=False):
    g=GLB(path);document=copy.deepcopy(g.json);binary=bytearray(g.binary)
    if sampler:document['samplers'][0]['minFilter']=9729
    if black_background:
        size=V.maps(g)['Normal'].shape[0]
        footprint=V._footprint([t['TEXCOORD_0'].astype(float)*size for t in V._triangles(g)],(size,size))
        for index,image in enumerate(document['images']):
            pixels=np.array(Image.open(io.BytesIO(g.image(index))))
            pixels[~footprint]=0
            encoded=io.BytesIO();Image.fromarray(pixels).save(encoded,format='PNG')
            binary.extend(b'\0'*(-len(binary)%4));offset=len(binary);binary.extend(encoded.getvalue())
            document['bufferViews'][image['bufferView']].update(byteOffset=offset,byteLength=len(encoded.getvalue()))
    document['buffers'][0]['byteLength']=len(binary)
    payload=json.dumps(document,separators=(',',':')).encode();payload+=b' '*(-len(payload)%4)
    binary.extend(b'\0'*(-len(binary)%4))
    chunks=struct.pack('<II',len(payload),0x4e4f534a)+payload+struct.pack('<II',len(binary),0x004e4942)+binary
    target=out/name;target.write_bytes(struct.pack('<III',0x46546c67,2,12+len(chunks))+chunks)
    return target

path=small/'loaded.glb';layout=small/'detachables/loaded/layout.json'
for name,changes in [('bad-sampler.glb',dict(sampler=True)),
                     ('black-background.glb',dict(black_background=True))]:
    broken=mutated(path,name,**changes)
    try:V.mip_bleed(broken,textures,'SubsetFixture',layout,gun=small/'main.glb')
    except AssertionError as error:
        assert ('Sampler differs' if changes.get('sampler') else 'New mip bleed exceeds atlas') in str(error),str(error)
    else:raise AssertionError('Mip/sampler regression accepted '+name)
for state in ('loaded','empty','tilt'):
    images=V.maps(GLB(small/(state+'.glb')))
    assert np.all(images['BaseColor'][:,:,2]>.09), 'Unfilled background texels'
    assert V.mip_chain(images['BaseColor'],color=True)[-1][0,0,2]>.005
# Determinism, including copied texture/material datablock names.
repeat=out/'repeat';deliver(opted,repeat)
for name in ('main','loaded','empty','tilt'):
    assert (small/(name+'.glb')).read_bytes()==(repeat/(name+'.glb')).read_bytes()
# Explicit exporter option reaches the cluster path without changing main bytes.
cluster_config={**base,'DETACHABLES':[{**r,'texture_size':1024,'texture_clusters':True}
                                     for r in base['DETACHABLES']]}
deliver(cluster_config,out/'cluster-option')
assert (out/'cluster-option/main.glb').read_bytes()==(legacy/'main.glb').read_bytes()
for state in ('loaded','empty','tilt'):
    record=json.loads((out/'cluster-option/detachables'/state/'layout.json').read_text())
    assert record['packing']=='atlas_clusters'
    V.compare(legacy/(state+'.glb'),out/'cluster-option'/(state+'.glb'))
# Static variant path uses exactly the same operation; the gun's low-level
# weapon.detachable() API and all legacy entries remain unchanged.
static={**base,'EXPORT_ANIMATIONS':False,'DETACHABLES':[], 'EXPORT_TEXTURE_SIZE':1024}
# This static fixture contains an armature, which the static-only option must
# reject (protect against accidentally applying it to an animated main gun).
try:deliver(static,out/'invalid-static')
except ValueError as error:assert 'static' in str(error).lower()
else:raise AssertionError('Static texture option accepted a main skin')
# Positive static variant: no skin or clips, same mesh and origin. Reuse
# authored pixels/UVs from the fixture, then export both policies.
bpy.ops.wm.open_mainfile(filepath=str(out/'source.blend'))
W.pose(bpy.data.objects['Fixture'],None,0)
parts=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('bone')=='Magazine']
static_ob=W.detachable(parts,bpy.data.objects['Fixture'],'Magazine','StaticMagazine')
for other in list(bpy.context.scene.objects):
    if other!=static_ob:bpy.data.objects.remove(other,do_unlink=True)
root=G.pivot('StaticRoot',(0,0,0));root['static_root']=True
G.attach(static_ob,root,asset_set='SubsetFixture')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
static_base=dict(EXPORT_ANIMATIONS=False,MATERIAL_OVERRIDES={'':dict(specular=.28)})
deliver(static_base,out/'static-legacy')
deliver({**static_base,'EXPORT_TEXTURE_SIZE':512},out/'static-small')
V.compare(out/'static-legacy/main.glb',out/'static-small/main.glb')
V.audit(out/'static-small/main.glb',textures,'SubsetFixture',out/'static-small/detachables/main/layout.json',gun=out/'static-legacy/main.glb')
V.mip_bleed(out/'static-small/main.glb',textures,'SubsetFixture',out/'static-small/detachables/main/layout.json',gun=out/'static-legacy/main.glb')
# Guarded last-digit export stabilization must restore only the accepted bytes,
# and must reject a changed source signature or a larger tangent difference.
import struct,copy
original=(out/'static-legacy/main.glb').read_bytes();g=GLB(out/'static-legacy/main.glb')
primitive=g.json['meshes'][0]['primitives'][0];attributes=primitive['attributes']
anchor=dict(mesh=0,primitive=0,vertex=0,
 position=g.accessor(attributes['POSITION'])[0].tolist(),normal=g.accessor(attributes['NORMAL'])[0].tolist(),
 uv=g.accessor(attributes['TEXCOORD_0'])[0].tolist(),tangent=g.accessor(attributes['TANGENT'])[0].tolist())
accessor=g.json['accessors'][attributes['TANGENT']];view=g.json['bufferViews'][accessor['bufferView']]
offset=12
while struct.unpack_from('<II',original,offset)[1]!=0x004e4942:
    offset+=8+struct.unpack_from('<I',original,offset)[0]
component=offset+8+view.get('byteOffset',0)+accessor.get('byteOffset',0)
payload=bytearray(original);struct.pack_into('<f',payload,component,anchor['tangent'][0]+.0001)
rounded=out/'rounded.glb';rounded.write_bytes(payload)
stabilize_tangents(rounded,[anchor]);assert rounded.read_bytes()==original
for field in ('uv','tangent'):
    bad=copy.deepcopy(anchor);bad[field][0]+=.01
    try:stabilize_tangents(rounded,[bad])
    except ValueError:pass
    else:raise AssertionError('Unsafe tangent stabilization accepted')
    assert rounded.read_bytes()==original
# A single 650px-wide original chart requires 1024, even with a 512 limit.
bpy.ops.wm.read_factory_settings(use_empty=True)
mesh=bpy.data.meshes.new('Wide');mesh.from_pydata([(0,0,0),(1,0,0),(1,1,0),(0,1,0)],[],[(0,1,2,3)])
ob=bpy.data.objects.new('Wide',mesh);bpy.context.collection.objects.link(ob)
layer=mesh.uv_layers.new(name='UVMap')
for i,point in enumerate(((.1,.1),(.1+650/2048,.1),(.1+650/2048,.2),(.1,.2))):layer.data[i].uv=point
ob.data.materials.append(export.atlas_material('SubsetFixture',textures))
for invalid in (256,2048,512.0,True):
    try:D.extract([ob],textures,'SubsetFixture',out/'bad',invalid)
    except ValueError:pass
    else:raise AssertionError('Accepted unsupported size')
try:D.extract([ob],textures,'SubsetFixture',out/'too-small',512)
except ValueError:pass
else:raise AssertionError('Silently reduced texel density')
layout=D.extract([ob],textures,'SubsetFixture',out/'wide',1024)
assert layout['size']==1024
assert layout['protected_mip_level']>=6 and layout['padding_px']>=32
W.export(out/'wide.glb',[ob],animations=False)
records['wide_mips']=V.mip_bleed(out/'wide.glb',textures,'SubsetFixture',out/'wide/layout.json')
assert records['wide_mips']['maximum_level']>=6
# Dense disconnected charts: 8px guards cannot fit 512, while 6px guards on
# the very same mip grid can. Prove the fallback keeps density and mip quality,
# rather than silently reducing either or forcing a larger allocation.
bpy.ops.wm.read_factory_settings(use_empty=True)
vertices=[];faces=[]
for index in range(400):
    x=(index%20)*.003;y=(index//20)*.003;start=len(vertices)
    vertices.extend([(x,y,0),(x+.002,y,0),(x+.002,y+.002,0),(x,y+.002,0)])
    faces.append(tuple(range(start,start+4)))
mesh=bpy.data.meshes.new('Dense charts');mesh.from_pydata(vertices,[],faces)
ob=bpy.data.objects.new('Dense charts',mesh);bpy.context.collection.objects.link(ob)
layer=mesh.uv_layers.new(name='UVMap')
for face in mesh.polygons:
    ox=16+(face.index%20)*80;oy=16+(face.index//20)*80
    for loop,(x,y) in zip(face.loop_indices,((0,0),(8,0),(8,8),(0,8))):
        layer.data[loop].uv=((ox+x+.27)/2048,(oy+y+.39)/2048)
ob.data.materials.append(export.atlas_material('SubsetFixture',textures))
W.export(out/'dense-legacy.glb',[ob],animations=False)
layout=D.extract([ob],textures,'SubsetFixture',out/'dense',512)
assert layout['size']==512 and layout['padding_px']==6 and layout['mip_grid_px']==8
W.export(out/'dense.glb',[ob],animations=False)
records['dense_fallback']=dict(comparison=V.compare(out/'dense-legacy.glb',out/'dense.glb'),
    audit=V.audit(out/'dense.glb',textures,'SubsetFixture',out/'dense/layout.json',gun=out/'dense-legacy.glb'),
    mip_bleed=V.mip_bleed(out/'dense.glb',textures,'SubsetFixture',out/'dense/layout.json',gun=out/'dense-legacy.glb'))
# Neighboring charts retain their atlas margins as a cluster. This cluster is
# taller than 1024 and has no horizontal gap through its overlapping y ranges.
# Split around whole islands, duplicating source halos at the empty-margin seam.
bpy.ops.wm.read_factory_settings(use_empty=True)
vertices=[];faces=[]
for index in range(3):
    start=len(vertices);x=index*.01
    vertices.extend([(x,0,0),(x+.005,0,0),(x+.005,.02,0),(x,.02,0)])
    faces.append(tuple(range(start,start+4)))
mesh=bpy.data.meshes.new('Atlas neighbors');mesh.from_pydata(vertices,[],faces)
ob=bpy.data.objects.new('Atlas neighbors',mesh);bpy.context.collection.objects.link(ob)
layer=mesh.uv_layers.new(name='UVMap')
for face,(ox,oy,height) in zip(mesh.polygons,((100,100,850),(124,600,850),(100,960,800))):
    for loop,(x,y) in zip(face.loop_indices,((0,0),(12,0),(12,height),(0,height))):
        layer.data[loop].uv=((ox+x+.27)/2048,(oy+y+.39)/2048)
ob.data.materials.append(export.atlas_material('SubsetFixture',textures))
W.export(out/'cluster-legacy.glb',[ob],animations=False)
layout=D.extract([ob],textures,'SubsetFixture',out/'clusters',1024,clusters=True)
assert layout['packing']=='atlas_clusters' and layout['original_cluster_count']==1
assert len(layout['regions'])==3 and layout['splits']
W.export(out/'clusters.glb',[ob],animations=False)
records['clusters']=dict(comparison=V.compare(out/'cluster-legacy.glb',out/'clusters.glb'),
    audit=V.audit(out/'clusters.glb',textures,'SubsetFixture',out/'clusters/layout.json',gun=out/'cluster-legacy.glb'),
    mip_bleed=V.mip_bleed(out/'clusters.glb',textures,'SubsetFixture',out/'clusters/layout.json',gun=out/'cluster-legacy.glb'))
# Every copied region, including nonmember atlas texels and original margins,
# remains byte-exact; the outside fill is the only generated part.
images=V.maps(GLB(out/'clusters.glb'))
for channel,image in images.items():
    source=read_png(textures/f'T_SubsetFixture_{channel}.png')[::-1]
    for region in layout['regions']:
        x,y=region['destination_origin'];ox,oy=region['source_origin'];w,h=region['shape']
        assert np.max(np.abs(image[::-1][y:y+h,x:x+w]-source[oy:oy+h,ox:ox+w]))<1e-7
# Repeat extraction from the original UVs proves deterministic cluster packing.
for row in layout['islands']:
    offset=np.array(row['destination_origin'])-row['source_origin']
    for loop in row['loops']:layer.data[loop].uv=(np.array(layer.data[loop].uv)*1024-offset)/2048
ob.data.materials.clear();ob.data.materials.append(export.atlas_material('SubsetFixture',textures))
repeat_layout=D.extract([ob],textures,'SubsetFixture',out/'clusters-repeat',1024,clusters=True)
assert repeat_layout['regions']==layout['regions']
for channel in D.CHANNELS:
    assert Path(layout['maps'][channel]).read_bytes()==Path(repeat_layout['maps'][channel]).read_bytes()
# RGB16 normals must retain every original precision step in both packers.
# The earlier RGB8 fixtures still prove byte preservation for existing callers.
y16,x16=np.mgrid[:2048,:2048]
n16=np.stack((.25*np.sin(x16*.7),.25*np.cos(y16*.6),np.ones_like(x16)),axis=-1)
n16/=np.linalg.norm(n16,axis=-1,keepdims=True)
write_png(textures/'T_SubsetFixture_Normal.png',n16*.5+.5,16)
(out/'source.blend').write_bytes(rigged_source_bytes)
legacy16=out/'precision16-legacy';deliver(base,legacy16)
for clustered in (False,True):
    folder=out/('precision16-clusters' if clustered else 'precision16-islands')
    settings={**base,'DETACHABLES':[{**row,'texture_size':512,'texture_clusters':clustered} for row in base['DETACHABLES']]}
    deliver(settings,folder)
    assert (folder/'main.glb').read_bytes()==(legacy16/'main.glb').read_bytes()
    for state in ('loaded','empty','tilt'):
        path=folder/(state+'.glb');layout=folder/'detachables'/state/'layout.json'
        data=GLB(path)
        assert sorted(data.image(i)[24] for i in range(3))==[8,8,16]
        records[folder.name+'-'+state]=dict(
            comparison=V.compare(legacy16/(state+'.glb'),path),
            audit=V.audit(path,textures,'SubsetFixture',layout,gun=folder/'main.glb'),
            mip_bleed=V.mip_bleed(path,textures,'SubsetFixture',layout,gun=folder/'main.glb'))
        report=json.loads(layout.read_text())
        assert report['bits_per_channel']==dict(BaseColor=8,Normal=16,ORM=8)
        if clustered:
            image=V.maps(data)['Normal'][::-1]
            source=read_png(textures/'T_SubsetFixture_Normal.png')[::-1]
            for region in report['regions']:
                x,y=region['destination_origin'];ox,oy=region['source_origin'];w,h=region['shape']
                assert np.array_equal(image[y:y+h,x:x+w],source[oy:oy+h,ox:ox+w].astype(float))

(out/'results.json').write_text(json.dumps(records,indent=2))
print('DETACHABLE TEXTURES PASS: legacy/main bytes, 512/1024, UV bounds, guards, sampled RGBA/normal/ORM, pointwise box mip bleed, inherited samplers, full fill/unit normals, tangent frame, posed origins, determinism and negative cases')
