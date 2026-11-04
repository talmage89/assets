"""Carry manufactured sheet normals independently of cut/split smoothing fans.

BodyNormal is an outward vehicle-space POINT vector, sampled on the uncut
Catmull-Clark parent. BMesh interpolates it at joint cuts. Face provenance
selects outside, reverse and flat gauge rim without nearest-side ambiguity.
No surface vertex is moved here.
"""
import bpy
from mathutils import Vector
from mathutils.geometry import barycentric_transform
from mathutils.bvhtree import BVHTree


def capture(ob, surface):
    me=ob.data
    if me.attributes.get('skin_face_role') is None:
        return
    field=me.attributes.get('BodyNormal') or me.attributes.new('BodyNormal','FLOAT_VECTOR','POINT')
    for v,d in zip(me.vertices,field.data):
        p=ob.matrix_world@v.co
        hit,_,fi,_=surface['tree'].find_nearest(p)
        a,c,e=surface['triangles'][fi]
        d.vector=barycentric_transform(hit,*[surface['points'][i] for i in [a,c,e]],
                                      *[surface['normals'][i] for i in [a,c,e]]).normalized()
    reseed(ob)


def reseed(ob):
    me=ob.data;field=me.attributes.get('BodyNormal');role=me.attributes.get('skin_face_role')
    if field is None or role is None:return
    ns=[d.vector.normalized() for d in field.data]
    # Closed-volume winding repair can reverse a chart disk after Solidify.
    # Provenance then needs the same outside/reverse swap. Validate the role
    # against the known parent hemisphere, rather than trusting index zero.
    normal_matrix=ob.matrix_world.to_3x3().inverted().transposed()
    orientation=sum(f.area*(normal_matrix@f.normal).dot(sum((ns[i] for i in f.vertices),Vector()).normalized())
                    for f in me.polygons if role.data[f.index].value==0)
    if orientation<0:
        for d in role.data:
            if d.value in [0,1]:d.value=1-d.value
        ob['sheet_role_orientation_repaired']=True
    optical=ob.get('part_category')=='glass' or ob.name.startswith(('Headlamp opening','Taillamp opening')) and 'cassette' not in ob.name
    if optical:
        # Opposite sides of the same physical laminate share the exterior
        # sample; independently querying the two surfaces made optical prisms.
        me.calc_loop_triangles()
        ts=[tuple(t.vertices) for t in me.loop_triangles if role.data[t.polygon_index].value==0]
        ps=[v.co.copy() for v in me.vertices]
        tree=BVHTree.FromPolygons(ps,ts,all_triangles=True);outside=[n.copy() for n in ns]
        for f in me.polygons:
            if role.data[f.index].value==1:
                for i in f.vertices:
                    hit,_,ti,_=tree.find_nearest(me.vertices[i].co);a,c,e=ts[ti]
                    ns[i]=barycentric_transform(hit,ps[a],ps[c],ps[e],outside[a],outside[c],outside[e]).normalized()
    inverse=ob.matrix_world.to_3x3().transposed();custom=[]
    for f in me.polygons:
        r=role.data[f.index].value;f.use_smooth=r!=2
        for li in f.loop_indices:
            vi=me.loops[li].vertex_index
            custom.append(f.normal if r==2 else inverse@(ns[vi] if r==0 else -ns[vi]))
    me.normals_split_custom_set(custom)
    ob['normal_basis']='Uncut parent POINT BodyNormal; outside/reverse/rim provenance, reseeded after final allocation'


def finish():
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        if ob.get('optical_patch'):
            from suv_glazing import field
            field(ob)
        else:reseed(ob)
