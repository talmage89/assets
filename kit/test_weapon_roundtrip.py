"""Explicit holds, STEP states, nested compound motion and detached full frames."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy
from mathutils import Matrix,Vector
from kit import model as G,weapon as W,weapon_verify as V
from kit.gltf import GLB

root=Path(__file__).resolve().parents[1];out=root/'build/weapon-roundtrip';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
arm=W.armature('Compound',{'Root':(0,0,0),'Pump':(0,.04,0),'Lifter':(0,.06,0),'Round':(0,.065,.01)},
               parents={'Lifter':'Pump','Round':'Lifter'})
parts=[]
for bone in arm.data.bones:
    ob=G.box(bone.name+' part',bone.head_local,(.005,.008,.006),None,radius=0)
    G.apply(ob);W.rigid_bind(ob,arm,bone.name);parts.append(ob)
socket=W.sockets(arm,{'Socket_Part':(0,.06,0)}, {'Socket_Part':'Lifter'})[0]
W.action(arm,'Cycle',[(0,{}),W.hold(3),
    (6,{'Pump':dict(loc=(0,-.02,0)),'Lifter':dict(rot_deg=(50,0,0)),'Round':dict(scale=(0,0,0))}),
    W.hold(12),(18,{'Pump':dict(loc=(0,0,0)),'Lifter':dict(rot_deg=(0,0,0))}),W.hold(21),
    (24,{'Round':dict(scale=(1,1,1))})])
def semantics():
    for frame in (0,1.25,2.99):
        W.pose(arm,'Cycle',frame);assert arm.pose.bones['Pump'].location.length<1e-7
    for frame in (6,7.5,9,11.99):
        W.pose(arm,'Cycle',frame);assert abs(arm.pose.bones['Pump'].location.y+.02)<1e-6
    for frame in (6,10.5,18,23.999):
        W.pose(arm,'Cycle',frame);assert max(abs(x) for x in arm.pose.bones['Round'].matrix.to_scale())<1e-7
    W.pose(arm,'Cycle',24);assert abs(arm.pose.bones['Round'].matrix.to_scale().x-1)<1e-7
semantics()
samples=[('Cycle',i*.25) for i in range(97)]
expected=V.capture(arm,samples,[socket.name])
W.pose(arm,'Cycle',9)
detached=W.detachable([parts[2]],arm,'Lifter','Detached')
source=V.surface_points([parts[2]]);spawn=socket.matrix_world.copy()
assert V.surface_delta(source,[tuple(spawn@v.co) for v in detached.data.vertices])<1e-7
bpy.data.objects.remove(detached,do_unlink=True)
W.pose(arm,None,0);W.export(out/'compound.glb',[arm,*parts,socket])
g=GLB(out/'compound.glb');assert any(s['interpolation']=='STEP' for a in g.json['animations'] for s in a['samplers'])
arm=V.import_glb(out/'compound.glb');semantics();rows=V.compare(arm,expected,position_tolerance_m=2e-5,linear_tolerance=5e-4)
print('COMPOUND WEAPON ROUNDTRIP PASS',len(rows),'subframe poses')
