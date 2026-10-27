"""Curved pipe sweeps with continuous manifold unions and authored collar swell.

Each daughter already broadens 23% at its foot. Unioning those flared sweeps
removes intersecting caps. Fine limbs retain their cylindrical cross-sections:
there is no global reduction of a dense voxel network.
"""
import bpy,bmesh
from collections import defaultdict
from kit import model as G


def living_union(objects,stems,bark):
    ob=objects[0]
    def volume():
        bm=bmesh.new();bm.from_mesh(ob.data);v=bm.calc_volume(signed=True);bm.free();return v
    for part in objects[1:]:
        before=volume();mod=ob.modifiers.new('Living wood junction','BOOLEAN')
        mod.operation='UNION';mod.solver='MANIFOLD';mod.object=part;G.apply(ob)
        if volume()<before*.995:raise RuntimeError('Union lost load-bearing wood')
        bpy.data.objects.remove(part,do_unlink=True)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8)
    bmesh.ops.dissolve_limit(bm,angle_limit=.01745,use_dissolve_boundaries=False,verts=list(bm.verts),edges=list(bm.edges),delimit=set())
    # Cut slightly above the original bole cap to avoid coincident plane cuts,
    # then return the closed foot to grade. Roots disappear into the lawn.
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,
                          plane_co=(0,0,.002),plane_no=(0,0,1),clear_inner=True)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
    bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8)
    # Union n-gons can conceal paired, oppositely wound internal slivers.
    # Inspect the triangles that actually ship before accepting the solid.
    bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
    bm.verts.index_update();groups=defaultdict(list)
    for face in bm.faces:groups[tuple(sorted(v.index for v in face.verts))].append(face)
    remove=[]
    for faces in groups.values():
        if len(faces)>1:
            if len(faces)!=2 or max(f.calc_area() for f in faces)>.0001 or faces[0].normal.dot(faces[1].normal)>-.99:
                raise RuntimeError('Unexpected duplicate living wood surface')
            remove.extend(faces)
    if remove:bmesh.ops.delete(bm,geom=remove,context='FACES_ONLY')
    bmesh.ops.delete(bm,geom=[e for e in bm.edges if e.is_wire],context='EDGES')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_edges],context='VERTS')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    if any(not e.is_manifold for e in bm.edges):raise RuntimeError('Wood has unresolved nonmanifold junction')
    for v in bm.verts:v.co.z-=.002
    bm.to_mesh(ob.data);bm.free();ob.data.update();G.smooth(ob,85)
    ob['wood_union_scope']='Authored curved, tapered, flared sweeps; manifold-unioned caps; no whole-network decimation'
    return ob
