"""Rifle-frame rigid binding, independent clips, socket and collision regression."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy
from mathutils import Vector
from kit import model,weapon,motion

bpy.ops.wm.read_factory_settings(use_empty=True)
arm=weapon.armature('Fixture',{'Root':(0,0,0),'Slider':(0,.02,0)})
outline=model.fillet_polygon([(0,0),(3,0),(3,1),(1,1),(1,3),(0,3)],.1)
assert len(outline)>6 and all(-1e-6<=u<=3.000001 and -1e-6<=v<=3.000001 for u,v in outline)
a=model.box('Fixed',(0,0,0),(.01,.01,.01),None,radius=0)
b=model.box('Moving',(0,.02,0),(.008,.008,.008),None,radius=0)
for ob,bone in ((a,'Root'),(b,'Slider')):
    model.apply(ob);weapon.rigid_bind(ob,arm,bone)
sock=weapon.sockets(arm,{'Socket_Magazine':(0,.02,0)}, {'Socket_Magazine':'Slider'})[0]
weapon.action(arm,'Clear',[(0,{}),(2,{'Slider':dict(loc=(0,.01,0))})])
weapon.action(arm,'Collision',[(0,{}),(2,{'Slider':dict(loc=(0,-.02,0))})])
weapon.pose(arm,'Clear',2);assert abs(sock.matrix_world.translation.y-.03)<1e-6
weapon.pose(arm,'Collision',0);assert arm.pose.bones['Slider'].location.length<1e-8
for bone in arm.data.bones:assert (bone.tail_local-bone.head_local).normalized().dot(Vector((0,1,0)))>.99999
assert motion.sweep_clips(arm,['Clear'])['passed']
assert not motion.sweep_clips(arm,['Collision'])['passed']
assert motion.sweep_clips(arm,['Collision'],allow=[dict(a='Fixed',b='Moving',reason='negative fixture override')])['passed']
assert not motion.sweep_clips(arm,['Collision'],allow=[dict(a='Fixed',b='Moving',reason='bounded negative fixture',max_penetration_m=.0005)])['passed']
assert motion.sweep_clips(arm,['Collision'],allow=[dict(a='Fixed',b='Moving',reason='bounded fixture allowance',max_penetration_m=.01)])['passed']
weapon.action(arm,'Grazing',[(0,{}),(2,{'Slider':dict(loc=(0,-.0111,0))})])
assert motion.sweep_clips(arm,['Grazing'])['passed']
assert not motion.sweep_clips(arm,['Grazing'],allow=[dict(a='Fixed',b='Moving',reason='stricter than global tolerance',max_penetration_m=.00005)])['passed']
print('WEAPON FIXTURE PASS')
