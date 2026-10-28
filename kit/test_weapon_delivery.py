"""Actual isolated atlas bake + animated delivery + loaded/empty detachments.

Small GPU fixture. Run via with_gpu.sh; output stays under build/.
"""
import sys,json,hashlib
from pathlib import Path
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from kit import model as G,weapon as W,weapon_verify as V,finalize,bake,export
from kit.materials import Nodes
from kit.gltf import GLB
out=ROOT/'build/weapon-delivery';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
n=Nodes('Original fixture finish');mat=n.finish((.025,.018,.012),.55,.2)
arm=W.armature('Fixture',{'Root':(0,0,0),'Magazine':(0,.03,0),'Round':(0,.035,.01)},parents={'Round':'Magazine'})
parts=[]
for bone,center in [('Root',(0,0,0)),('Magazine',(0,.03,0)),('Round',(0,.035,.01))]:
    ob=G.box(bone+' part',center,(.01,.016,.006),mat,0);G.apply(ob)
    ob['asset_set']='WeaponFixture';W.rigid_bind(ob,arm,bone);parts.append(ob)
socket=W.sockets(arm,{'Socket_Magazine':(0,.03,0)},{'Socket_Magazine':'Magazine'})[0]
W.action(arm,'Loaded',[(0,{}),W.hold(1)])
W.action(arm,'Empty',[(0,{'Round':dict(scale=(0,0,0))}),W.hold(1)])
W.action(arm,'Cycle',[(0,{}),W.hold(3),(6,{'Magazine':dict(loc=(0,-.02,-.03),rot_deg=(25,0,0)),
     'Round':dict(scale=(0,0,0))}),W.hold(12),(18,{'Magazine':dict(loc=(0,0,0),rot_deg=(0,0,0))}),
     W.hold(21),(24,{'Round':dict(scale=(1,1,1))})])
expected=V.capture(arm,[('Cycle',f) for f in (0,2.5,4,6,8.5,11.99,15,18,23.999,24)],[socket.name])
bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
cfg=dict(BUDGETS={'WeaponFixture':100},UV_MIN_COVERAGE=.01,
 UV_PACK_SHAPE='AABB',UV_DENSITY_BANDS=dict(reference_size=128,p5_min=1,median_min=1,median_max=1e5,p95_max=1e6),
 EXPORT_SKIN_NAMES={'Fixture':'WeaponFixture'},EXPORT_ANIMATIONS={'clips':['Loaded','Empty','Cycle']},
 BAKE_POLICY=dict(isolate_rigid_bones=True,cage_m=.0005,ray_distance_m=.002,ao_distance_m=.01),
 DETACHABLES=[dict(armature='Fixture',bone='Magazine',bones=['Magazine','Round'],name='Magazine',
    clip=state,frame=0,filename=state.lower()+'.glb') for state in ('Loaded','Empty')])
config=out/'config.py';config.write_text('\n'.join(k+'='+repr(v) for k,v in cfg.items()))
def args(values):sys.argv=['blender','--',*map(str,values)]
args(['--source',out/'source.blend','--config',config,'--out',out/'finalized.blend','--report',out/'uv.json','--size',128,'--target-density',500]);finalize.main()
args(['--low',out/'finalized.blend','--high',out/'source.blend','--out',out/'textures','--asset','WeaponFixture','--config',config,'--size',128,'--samples',8]);bake.main()
args(['--source',out/'finalized.blend','--textures',out/'textures','--asset','WeaponFixture','--out',out/'fixture.glb','--report',out/'export.json','--config',config]);export.main()
g=GLB(out/'fixture.glb');assert len(g.json['images'])==3 and len(g.json['materials'])==1
assert any(s['interpolation']=='STEP' for a in g.json['animations'] for s in a['samplers'])
arm=V.import_glb(out/'fixture.glb');V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
for f in (6,12,18,23.999):
    W.pose(arm,'Cycle',f);assert max(abs(v) for v in arm.pose.bones['Round'].matrix.to_scale())<1e-7
W.pose(arm,'Cycle',24);assert abs(arm.pose.bones['Round'].matrix.to_scale().x-1)<1e-6
# Byte hashes prove the same atlas payload, not runtime texture-cache behavior.
def images(data):
    return {hashlib.sha256(data.image(i)).hexdigest() for i in range(len(data.json['images']))}
shared=images(g);counts=[]
for name in ('loaded','empty'):
    d=GLB(out/(name+'.glb'));assert images(d)==shared
    assert not d.json.get('skins') and not d.json.get('animations')
    counts.append(sum(len(d.accessor(p['indices']))//3 for m in d.json['meshes'] for p in m['primitives']))
    V.import_glb(out/(name+'.glb'))
    assert len([o for o in bpy.context.scene.objects if o.type=='MESH'])==1
assert counts==[24,12],counts
stats=json.loads((out/'textures/bake-report.json').read_text()) if (out/'textures/bake-report.json').exists() else None
print('ANIMATED ATLAS DELIVERY PASS: actual bake, STEP states, compound poses, 24/12 loaded/empty triangles, byte-identical images')
