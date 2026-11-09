"""Local, reversible reduction of concealed gauge backs; exterior is immutable."""
import math,hashlib,json
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def reduce_gauge(ob):
    mesh=ob.data;mesh.calc_loop_triangles();matrix=ob.matrix_world
    ps=[v.co.copy() for v in mesh.vertices];outside=[tuple(t.vertices) for t in mesh.loop_triangles if mesh.polygons[t.polygon_index].material_index==0]
    tree=BVHTree.FromPolygons(ps,outside,all_triangles=True)
    original=[(tuple(f.vertices),f.material_index,f.use_smooth) for f in mesh.polygons]
    before=sum(len(f)-2 for f,_,_ in original);bm=bmesh.new();bm.from_mesh(mesh);bm.normal_update()
    ids=bm.verts.layers.int.new('Original gauge vertex')
    for v in bm.verts: v[ids]=v.index
    # Retain original patch boundaries. A rejected patch is restored verbatim,
    # rather than letting one concave corner cancel every flat panel saving.
    groups={};old_groups={};tiles={}
    for f in bm.faces:
        role=f.material_index
        if role==1:
            p=f.calc_center_median();cell=tuple(math.floor(q/.15) for q in p)
            group=tiles.setdefault(cell,len(tiles)+3);old_groups.setdefault(group,[]).append((tuple(v[ids] for v in f.verts),role,f.smooth))
            f.material_index=group
        groups[f.index]=f.material_index
    pure={v for v in bm.verts if v.link_faces and all(f.material_index>=3 for f in v.link_faces)}
    edges=[e for e in bm.edges if len(e.link_faces)==2 and all(v in pure for v in e.verts) and e.link_faces[0].material_index==e.link_faces[1].material_index]
    bm.verts.index_update();bm.edges.index_update()
    bmesh.ops.dissolve_limit(bm,angle_limit=math.radians(5),verts=sorted(pure,key=lambda v:v.index),edges=sorted(edges,key=lambda e:e.index),use_dissolve_boundaries=False,delimit={'MATERIAL'})
    bad=set();maximum={}
    for tri in bm.calc_loop_triangles():
        f=tri[0].face;group=f.material_index
        if group<3:continue
        vv=[l.vert.co for l in tri];probes=[sum(vv,Vector())/3]+[(a+b)/2 for a,b in zip(vv,vv[1:]+vv[:1])]
        for q in probes:
            hit,n,_,_=tree.find_nearest(q);signed=(q-hit).dot(n);maximum[group]=max(maximum.get(group,-1),signed)
            if signed>-.0004:bad.add(group)
    faces=[]
    for f in bm.faces:
        group=f.material_index
        if group in bad:continue
        faces.append((tuple(v[ids] for v in f.verts),1 if group>=3 else group,f.smooth))
    for group in sorted(bad):faces+=old_groups[group]
    bm.free()
    used=sorted({i for f,_,_ in faces for i in f});lookup={v:i for i,v in enumerate(used)}
    candidate=bpy.data.meshes.new(mesh.name+' local gauge');candidate.from_pydata([ps[i] for i in used],[],[tuple(lookup[i] for i in f) for f,_,_ in faces]);candidate.update()
    for m in mesh.materials:candidate.materials.append(m)
    for f,(_,role,smooth) in zip(candidate.polygons,faces):f.material_index=role;f.use_smooth=smooth
    bm=bmesh.new();bm.from_mesh(candidate);bmesh.ops.triangulate(bm,faces=list(bm.faces));closed=all(e.is_manifold for e in bm.edges)
    bm.to_mesh(candidate);bm.free()
    # Compare the complete exposed polygon soup by coordinate, independent of
    # renumbering. This proves exterior positions AND connectivity unchanged.
    def skin_key(me):
        me.calc_loop_triangles();rows=[]
        for t in me.loop_triangles:
            if me.polygons[t.polygon_index].material_index==0:rows.append(tuple(sorted(tuple(me.vertices[i].co) for i in t.vertices)))
        return hashlib.sha256(repr(sorted(rows)).encode()).hexdigest()
    unchanged=skin_key(mesh)==skin_key(candidate);after=len(candidate.loop_triangles)
    accepted=closed and unchanged and after<before
    ob['gauge_reduction_report']=json.dumps(dict(before=before,after=after if accepted else before,saved=before-after if accepted else 0,patches=len(tiles),rejected_patches=len(bad),exterior_soup_identical=unchanged,closed=closed,accepted=accepted))
    if accepted:
        ob.data=candidate
        if mesh.users==0:bpy.data.meshes.remove(mesh)
    else:bpy.data.meshes.remove(candidate)
