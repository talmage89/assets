"""Regression for skew-grid split normals and a ground-supported ISO carcass."""
import math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kit import model as G
from kit.vehicle import panel,loaded_tire,samples

bpy.ops.wm.read_factory_settings(use_empty=True)
root=G.pivot('NonVehicleRoot',(.2,-.3,0))
def surface(u,v):return (1+.04*u*u+.10*v*v,u-.5,v+.2)
ob=panel('Analytic closed stamping',surface,samples(9),samples(7),None,(1,0,0))
G.attach(ob,root,asset_set='Fixture')
bpy.context.view_layer.update()
mesh=ob.data
bm=bmesh.new();bm.from_mesh(mesh)
assert all(e.is_manifold for e in bm.edges)
assert bm.calc_volume(signed=True)>0
bm.free()
errors=[]
for face in mesh.polygons[:9*7]:
    for li in face.loop_indices:
        p=ob.matrix_world@mesh.vertices[mesh.loops[li].vertex_index].co
        # Independent exact normal of x=1+.04*y_param^2+.10*z_param^2.
        normal=Vector((1,-.08*(p.y+.5),-.20*(p.z-.2))).normalized()
        errors.append((mesh.corner_normals[li].vector-normal).length)
assert max(errors)<.001, max(errors)
tire=loaded_tire('Tire',(.858,0,.39535),.275,.65,18,None,96,.39535)
G.apply(tire)
points=[tire.matrix_world@v.co for v in tire.data.vertices]
# World transforms must be updated before independent bounds measurements.
bpy.context.view_layer.update();points=[tire.matrix_world@v.co for v in tire.data.vertices]
assert abs(min(p.z for p in points))<1e-6
assert abs((max(p.x for p in points)-min(p.x for p in points))-.275)<1e-6
assert abs(max(p.z for p in points)-.8027)<1e-6
reduced=loaded_tire('Reduced tire',(.858,0,.39535),.275,.65,18,None,64,.39535,
                    profile_indices=[0,1,3,4,5,7,9,10,11,13,14])
G.apply(reduced);bpy.context.view_layer.update()
ps=[reduced.matrix_world@v.co for v in reduced.data.vertices]
assert abs(min(p.z for p in ps))<1e-6
assert abs(max(p.z for p in ps)-.8027)<1e-6
assert abs(max(p.x for p in ps)-min(p.x for p in ps)-.275)<1e-6
reduced.data.calc_loop_triangles();tire.data.calc_loop_triangles()
assert len(reduced.data.loop_triangles)<len(tire.data.loop_triangles)*.6
for indices in [[],[0,14,3],[1,3,14],[0,3,13]]:
    try:loaded_tire('Invalid',(0,0,0),.275,.65,18,None,64,.39535,indices)
    except ValueError:pass
    else:raise AssertionError('Invalid profile accepted')
print('VEHICLE FIXTURES PASS: manifold gauge, analytic normals, real tire width/top/contact')

from mathutils import Matrix
rolling=loaded_tire('Rolling approximation',(0,0,.40135),.275,.65,18,None,96,.40135,rolling_radius=.40135)
G.apply(rolling);bpy.context.view_layer.update()
for angle in range(0,361,5):
    rotation=Matrix.Rotation(math.radians(angle),4,'X')
    ps=[rolling.matrix_world@(rotation@v.co) for v in rolling.data.vertices]
    assert -1e-6<=min(p.z for p in ps)<.001
    assert abs(max(p.x for p in ps)-min(p.x for p in ps)-.275)<1e-6
print('ROLLING TIRE PASS: full revolution keeps contact, width and a circular loaded envelope')
# Exercise the actual finalize/edit-mode path, not only the modeling helper.
from kit import finalize
folder=Path(__file__).resolve().parents[1]/'build/vehicle-finalize-test';folder.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'source.blend'))
sys.argv=['blender','--','--source',str(folder/'source.blend'),'--out',str(folder/'final.blend'),
 '--report',str(folder/'uv.json'),'--size','512','--target-density','850']
finalize.main();ob=bpy.data.objects['Analytic closed stamping'];errors=[]
for face in ob.data.polygons:
 for li in face.loop_indices:
  p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
  n=ob.data.corner_normals[li].vector
  if n.x<.5:continue
  expected=Vector((1,-.08*(p.y+.5),-.20*(p.z-.2))).normalized()
  if abs(p.x-(1+.04*(p.y+.5)**2+.10*(p.z-.2)**2))<.00001:errors.append((n-expected).length)
assert errors and max(errors)<.001,max(errors)
print('FINALIZE NORMAL PASS: analytic corner field survives triangulation and UV editing')
