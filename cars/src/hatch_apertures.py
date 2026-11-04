"""Lamp openings cut in the hatch's evaluated subdivision parameter chart.

Reference pixels never enter this operation. The original locator outline is
projected onto the parent, offset 2.25 mm in its tangent plane, and faired to a convex
outline in the 2D chart. Cut skin fragments retain their original face planes;
all gauge rims are constructed after cutting. No volume unions or thin booleans.
"""
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import barycentric_transform,convex_hull_2d,delaunay_2d_cdt
from mathutils.kdtree import KDTree
from kit import model as G


def surface_uv(p,surface):
    hit,_,fi,_=surface['tree'].find_nearest(p);a,b,c=surface['triangles'][fi]
    uv=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['uvs'][a],surface['uvs'][b],surface['uvs'][c])
    n=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['normals'][a],surface['normals'][b],surface['normals'][c]).normalized()
    return uv,n


def outline(lamp,surface):
    raw=list(lamp['aperture_samples']);points=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu,nv=lamp['form_columns'],lamp['form_rows']
    indices=list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]
    loop=[points[i] for i in indices]
    uv=[surface_uv(p,surface)[0] for p in loop]
    hull=list(convex_hull_2d([p.to_2d() for p in uv]));uv=[uv[i] for i in hull];loop=[loop[i] for i in hull]
    area=sum(a.x*b.y-b.x*a.y for a,b in zip(uv,uv[1:]+uv[:1]))
    if area<0:loop.reverse()
    expanded=[]
    for i,p in enumerate(loop):
        _,n=surface_uv(p,surface);edge=loop[(i+1)%len(loop)]-loop[i-1]
        outward=edge.cross(n).normalized()
        expanded.append(surface_uv(p+outward*.00225,surface)[0])
    hull=list(convex_hull_2d([p.to_2d() for p in expanded]));expanded=[expanded[i] for i in hull]
    area=sum(a.x*b.y-b.x*a.y for a,b in zip(expanded,expanded[1:]+expanded[:1]))
    if area<0:expanded.reverse()
    return [expanded]


def bounds(poly):
    return min(p.x for p in poly),max(p.x for p in poly),min(p.y for p in poly),max(p.y for p in poly)


def regularize_blank(ob,surface,front):
    """Triangulate a tapered lens in the parent's injective parameter chart.

    Closest-point projection of a Cartesian grid can fold its last tiny cells
    over the shoulder. A chart triangulation has one disk topology even at the
    narrow tip. All authored guide rows remain actual vertex samples.
    """
    from mathutils.bvhtree import BVHTree
    raw=list(ob['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    uv=[surface_uv(p,surface)[0].to_2d() for p in guides]
    coords,_,faces,*_=delaunay_2d_cdt(uv,[],[],0,1e-6)
    if 'uv_tree' not in surface:
        surface['uv_tree']=BVHTree.FromPolygons(surface['uvs'],surface['triangles'],all_triangles=True)
    ps=[]
    for q in coords:
        hit,_,fi,_=surface['uv_tree'].find_nearest(Vector((q.x,q.y,0)));a,b,c=surface['triangles'][fi]
        uvs=surface['uvs'];points=surface['points'];normals=surface['normals']
        p=barycentric_transform(hit,uvs[a],uvs[b],uvs[c],points[a],points[b],points[c])
        n=barycentric_transform(hit,uvs[a],uvs[b],uvs[c],normals[a],normals[b],normals[c]).normalized()
        ps.append(p+n*.004)
    inverse=ob.matrix_world.inverted();old=ob.data
    mesh=bpy.data.meshes.new(old.name+' chart disk');mesh.from_pydata([inverse@p for p in ps],[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    center=sum((ps[i] for i in faces[0]),Vector())/len(faces[0])
    hint=Vector((center.x,-1 if front else 1,0))
    if ob.data.polygons[0].normal.dot(hint)<0:
        for face in ob.data.polygons:face.flip()
    sol=ob.modifiers.new('Chart lens gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    kd=KDTree(len(ps))
    for i,p in enumerate(ps):kd.insert(p,i)
    kd.balance();snapped=[kd.find(p)[0].copy() for p in guides]
    ob['aperture_samples']=[v for p in snapped for v in p]
    ob['chart_disk_topology']=True


def difference(polygon,region):
    """Convex difference; vertices carry both UV and original 3D position."""
    pieces=[]
    for a,b in zip(region,region[1:]+region[:1]):
        edge=b-a
        def signed(uv):return edge.x*(uv.y-a.y)-edge.y*(uv.x-a.x)
        inside=[];outside=[]
        for p,q in zip(polygon,polygon[1:]+polygon[:1]):
            dp,dq=signed(p[0]),signed(q[0])
            (inside if dp>=0 else outside).append(p)
            if dp*dq<0:
                t=dp/(dp-dq);v=(p[0].lerp(q[0],t),p[1].lerp(q[1],t));inside.append(v);outside.append(v)
        if len(outside)>=3:pieces.append(outside)
        polygon=inside
        if len(polygon)<3:break
    return pieces


def cut_mesh(ob,cutters,surface):
    from hatch_body import closeable_sheet,conform_edges
    matrix=ob.matrix_world.copy();inverse=matrix.inverted();normal_matrix=matrix.to_3x3().inverted().transposed()
    points=[matrix@v.co for v in ob.data.vertices];uvs=[surface_uv(p,surface)[0] for p in points]
    polygons=[];affected=False
    cutter_boxes=[bounds(t) for t in cutters]
    def intersects(a,b):return not(a[0]>b[1] or a[1]<b[0] or a[2]>b[3] or a[3]<b[2])
    ob.data.calc_loop_triangles()
    for face in ob.data.loop_triangles:
        center=sum((points[i] for i in face.vertices),Vector())/3
        face_normal=face.normal
        _,n=surface_uv(center,surface)
        # Solidify preserves original outer faces first. An angular test alone
        # admits diagonal gauge rims at the folded chin and duplicates them.
        if face.polygon_index>=ob['outer_skin_faces']:continue
        original=[(uvs[i],points[i]) for i in face.vertices];pieces=[original]
        for region,box in zip(cutters,cutter_boxes):
            result=[]
            for piece in pieces:
                if not intersects(bounds([p[0] for p in piece]),box):result.append(piece);continue
                result.extend(difference(piece,region));affected=True
            pieces=result
            if not pieces:break
        polygons.extend(pieces)
    if not affected:return
    vertices=[];faces=[]
    for polygon in polygons:
        offset=len(vertices);vertices.extend(inverse@p[1] for p in polygon);faces.append(tuple(range(offset,len(vertices))))
    old=ob.data;mesh=bpy.data.meshes.new(old.name+' lamp apertures');mesh.from_pydata(vertices,[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);conform_edges(bm)
    bmesh.ops.dissolve_limit(bm,angle_limit=2e-5,verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False,delimit=set())
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bad=[f for f in bm.faces if f.calc_area()<1e-11]
    if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
    bm.to_mesh(ob.data);bm.free();closeable_sheet(ob)
    ob['outer_skin_faces']=len(ob.data.polygons)
    gauge=ob.modifiers.new('Cut aperture gauge','SOLIDIFY');gauge.thickness=.003 if ob.get('part_category')=='fascia' else .0009;gauge.offset=-1;gauge.use_even_offset=False;G.apply(ob)
    ob['lamp_apertures_cut']=True


def carve(front,lamps,surface,recess=.010):
    cutters=[region for lamp in lamps for region in outline(lamp,surface)]
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','fascia','pillars']:continue
        if (ob.matrix_world@ob.data.vertices[0].co).y*(1 if front else -1)>0:continue
        cut_mesh(ob,cutters,surface)
    for lamp in lamps:
        matrix=lamp.matrix_world.copy();inverse=matrix.inverted()
        for v in lamp.data.vertices:
            p=matrix@v.co;_,n=surface_uv(p,surface);v.co=inverse@(p-n*recess)
        raw=list(lamp['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];moved=[]
        actual=KDTree(len(lamp.data.vertices))
        for i,v in enumerate(lamp.data.vertices):actual.insert(matrix@v.co,i)
        actual.balance()
        for p in guides:
            _,n=surface_uv(p,surface);moved.append(actual.find(p-n*recess)[0].copy())
        lamp['aperture_samples']=[c for p in moved for c in p];lamp['opening_recess_m']=recess-.004
