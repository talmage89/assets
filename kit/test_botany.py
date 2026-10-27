"""Blender fixture: opt-in rooted unions, default component retention and solids."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import bpy,bmesh
from kit import model as G,botany


def fixture(connected):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    trunk=G.cylinder('Bole',(0,0,0),(0,0,1),.1,None,16)
    branch=G.cylinder('Lateral',(0,0,.5),(.6,0,.9),.05,None,10)
    crumb=G.cylinder('Separate remesh fragment',(3,0,.1),(3,0,.2),.035,None,8)
    # Apply source transforms as actual botanical sweeps already do.
    for ob in [trunk,branch,crumb]:
        bpy.context.view_layer.objects.active=ob;ob.select_set(True)
        bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);ob.select_set(False)
    ob=botany.fuse_stems([trunk,branch,crumb],voxel_size=.01,triangle_target=1500,connected_only=connected)
    bm=bmesh.new();bm.from_mesh(ob.data)
    assert all(e.is_manifold for e in bm.edges),'Union must remain sealed'
    assert bm.calc_volume(signed=True)>.02,'Main stem volume collapsed'
    xmax=max(v.co.x for v in ob.data.vertices)
    assert xmax<1 if connected else xmax>2.9,'Opt-in component policy changed'
    bm.free();print('BOTANY FIXTURE PASSED connected_only =',connected)

fixture(False);fixture(True)

# Optional mass normals retain the legacy default and give local lobes a
# different lighting direction without altering plane geometry or UVs.
def normal_fixture():
    from mathutils import Vector
    legacy=botany.Cards();explicit=botany.Cards();local=botany.Cards()
    args=((2,0,5),(1,0,0),.2,.6,(0,0,1,1),(0,0,5),(0,1,.4,.7),.9)
    legacy.add(*args);explicit.add(*args,clump_center=(2,0,4),clump_blend=0)
    local.add(*args,clump_center=(2,0,4),clump_blend=.75)
    assert legacy.vertices==local.vertices and legacy.uvs==local.uvs
    assert legacy.normals==explicit.normals,'Zero blend must preserve legacy normals'
    assert sum(Vector(n).z for n in local.normals)>sum(Vector(n).z for n in legacy.normals)+1
    assert all(abs(Vector(n).length-1)<1e-6 for n in local.normals)
    print('BOTANY FIXTURE PASSED clump-normal optional compatibility')

normal_fixture()
