"""Small Blender regression fixtures for optional asset policy and solid motion.

Run: blender -b --factory-startup --python-exit-code 1 --python kit/test_policy.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy
from kit import model as G,rig
from kit.motion import surface,penetration
bpy.ops.wm.read_factory_settings(use_empty=True)
a=G.box('Fixed',(0,0,0),(.2,.2,.2),None,0);b=G.box('Moving',(.09,0,0),(.1,.1,.1),None,0)
bpy.context.view_layer.update();assert penetration(surface(a),surface(b),.0005)[0]>.005
b.location.x=.15;bpy.context.view_layer.update();assert penetration(surface(a),surface(b),.0005)[0]==0
b.location.x=.151;bpy.context.view_layer.update();assert penetration(surface(a),surface(b),.0005)[0]==0
b.location.x=0;bpy.context.view_layer.update();assert penetration(surface(a),surface(b),.0005)[0]>.005 # containment, no crossings
# A bounding box is not solid: a small object in a hollow box must stay clear.
loops=[]
for z,r in [(-.1,.1),(.1,.1),(.1,.08),(-.1,.08)]:
    loops.append([(-r,-r,z),(r,-r,z),(r,r,z),(-r,r,z)])
hollow=G.ring_loft('Hollow',loops,None)
bpy.context.view_layer.update();assert penetration(surface(hollow),surface(b),.0005)[0]==0
root=G.pivot('OtherAsset',(0,0,0));root['asset_set']='Fixture'
G.attach(b,root);assert b['asset_set']=='Grill' # legacy default preserved
G.attach(b,root,asset_set='Other');assert b['asset_set']=='Other'
G.attach(b,root,inherit_asset_set=True);assert b['asset_set']=='Fixture'
arm=rig.chain('CableRig',[(0,0,0),(0,0,.1),(0,0,.2),(0,0,.3)],root,prefix='Cable')
rig.bind(b,arm,[{'Cable_03':1} for _ in b.data.vertices],export_part='CableMesh',modifier_name='Cable skin')
assert b['export_part']=='CableMesh'
rig.dangling(arm,angles=[10,20,30],lateral=.05,twist_step=5,initial_z=(1,0,0))
assert len(arm.pose.bones)==3
rig.reset(arm)
print('PASS: penetration, containment, hollow clearance, tangent clearance, legacy and configured asset tags, non-grill three-bone bind/pose')
