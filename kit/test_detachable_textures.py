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
from kit.gltf import GLB
from kit.image_io import write_png

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
W.action(arm,'Loaded',[(0,{}),W.hold(1)])
W.action(arm,'Empty',[(0,{'Round':dict(scale=(0,0,0))}),W.hold(1)])
W.action(arm,'Tilt',[(0,{}),(12,{'Magazine':dict(loc=(.01,-.02,.03),rot_deg=(24,32,-13))}),W.hold(15)])
bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
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
                        audit=V.audit(path,textures,'SubsetFixture',layout))
    assert records[state]['audit']['size']==512,'Must honor requested size'
    assert path.stat().st_size < (legacy/(state+'.glb')).stat().st_size
    # Legacy path remains byte-identical to canonical source PNGs.
    g=GLB(legacy/(state+'.glb'))
    assert {g.image(i) for i in range(3)} == {p.read_bytes() for p in textures.glob('*.png')}
    assert records[state]['audit']['padding_px']>=2
# Determinism, including copied texture/material datablock names.
repeat=out/'repeat';deliver(opted,repeat)
for name in ('main','loaded','empty','tilt'):
    assert (small/(name+'.glb')).read_bytes()==(repeat/(name+'.glb')).read_bytes()
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
V.audit(out/'static-small/main.glb',textures,'SubsetFixture',out/'static-small/detachables/main/layout.json')
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
(out/'results.json').write_text(json.dumps(records,indent=2))
print('DETACHABLE TEXTURES PASS: legacy/main bytes, 512/1024, UV bounds, guards, sampled RGBA/normal/ORM, tangent frame, posed origins, determinism and negative cases')
