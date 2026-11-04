"""Carry manufactured sheet normals independently of cut/split smoothing fans.

BodyNormal is an outward vehicle-space POINT vector, sampled on the uncut
Catmull-Clark parent. BMesh interpolates it at joint cuts. Face provenance
selects outside, reverse and flat gauge rim without nearest-side ambiguity.
No surface vertex is moved here.
"""
import bpy
from mathutils import Vector
from mathutils.geometry import barycentric_transform
from mathutils.kdtree import KDTree


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
    optical=ob.get('part_category')=='glass' or ob.name.startswith(('Headlamp opening','Taillamp opening')) and 'cassette' not in ob.name
    if optical:
        # Opposite sides of the same physical laminate share the exterior
        # sample; independently querying the two surfaces made optical prisms.
        outer=sorted({i for f in me.polygons if role.data[f.index].value==0 for i in f.vertices})
        tree=KDTree(len(outer))
        for j,i in enumerate(outer):tree.insert(me.vertices[i].co,j)
        tree.balance()
        for f in me.polygons:
            if role.data[f.index].value==1:
                for i in f.vertices:ns[i]=ns[outer[tree.find(me.vertices[i].co)[1]]].copy()
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
        if ob.type=='MESH':reseed(ob)
