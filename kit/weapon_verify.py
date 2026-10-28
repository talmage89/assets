"""Reusable held-asset pose, socket and surface round-trip measurements.

These compare serialization. Intended state/contact checks are separate callers'
assertions; matching an incorrect source animation is never form acceptance.
"""
import math
import bpy
from mathutils.kdtree import KDTree
from kit import weapon


def surface_points(objects):
    result=[];deps=bpy.context.evaluated_depsgraph_get()
    for ob in objects:
        ev=ob.evaluated_get(deps);mesh=ev.to_mesh()
        result.extend(tuple(ev.matrix_world@v.co) for v in mesh.vertices)
        ev.to_mesh_clear()
    return result


def surface_delta(a,b):
    def directed(left,right):
        tree=KDTree(len(right))
        for i,p in enumerate(right):tree.insert(p,i)
        tree.balance()
        return max(tree.find(p)[2] for p in left)
    return max(directed(a,b),directed(b,a))


def capture(arm,samples,socket_names=()):
    """Rest-frame-invariant skin deformations plus complete socket transforms."""
    rows=[]
    for name,frame in samples:
        weapon.pose(arm,name,frame)
        rows.append(dict(clip=name,frame=frame,
            bones={b.name:[list(r) for r in arm.matrix_world@b.matrix@b.bone.matrix_local.inverted()]
                   for b in arm.pose.bones},
            sockets={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in socket_names}))
    weapon.pose(arm,None,0)
    return rows


def compare(arm,expected,*,position_tolerance_m=2e-6,linear_tolerance=2e-5):
    """Check source/import affine transforms, including orientation and scale."""
    rows=[]
    for row in expected:
        actual=capture(arm,[(row['clip'],row['frame'])],row['sockets'])[0]
        position=0.;linear=0.
        for group in ('bones','sockets'):
            for name,matrix in row[group].items():
                other=actual[group][name]
                position=max(position,math.dist([matrix[i][3] for i in range(3)],[other[i][3] for i in range(3)]))
                linear=max(linear,max(abs(matrix[i][j]-other[i][j]) for i in range(3) for j in range(3)))
        if position>position_tolerance_m or linear>linear_tolerance:
            raise AssertionError((row['clip'],row['frame'],position,linear))
        rows.append(dict(clip=row['clip'],frame=row['frame'],position_delta_m=position,linear_delta=linear))
    return rows


def import_glb(path,fps=60):
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=fps
    bpy.ops.import_scene.gltf(filepath=str(path))
    for ob in list(bpy.context.scene.objects):
        if ob.type=='MESH' and ob.name.startswith('Icosphere'):bpy.data.objects.remove(ob,do_unlink=True)
    return next((o for o in bpy.context.scene.objects if o.type=='ARMATURE'),None)


def normal_direction(glb):
    """Winding versus exported corner normals; independent of vector length."""
    import numpy as np
    worst=1.;count=0
    for mesh in glb.json['meshes']:
        for prim in mesh['primitives']:
            p=glb.accessor(prim['attributes']['POSITION']);n=glb.accessor(prim['attributes']['NORMAL'])
            triangles=glb.accessor(prim['indices']).reshape(-1,3)
            face=np.cross(p[triangles[:,1]]-p[triangles[:,0]],p[triangles[:,2]]-p[triangles[:,0]])
            length=np.linalg.norm(face,axis=1);valid=length>1e-13
            face=face[valid]/length[valid,None];triangles=triangles[valid]
            dots=np.einsum('ijk,ik->ij',n[triangles],face)
            worst=min(worst,float(dots.min()));count+=len(triangles)
            if np.any(dots<-.05):raise AssertionError('Exported normals oppose triangle winding')
    return dict(triangles=count,minimum_corner_dot=worst)
