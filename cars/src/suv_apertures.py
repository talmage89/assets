"""Lamp openings cut in the SUV's evaluated subdivision parameter chart.

Reference pixels never enter this operation. The original locator outline is
projected onto the parent and offset 2.25 mm in its tangent plane. Wrapped optical
borders retain their concavity in the 2D chart. Cut skin fragments retain their original face planes;
all gauge rims are constructed after cutting. No volume unions or thin booleans.
"""
import bpy,bmesh,math
from mathutils import Vector
from mathutils.geometry import barycentric_transform,convex_hull_2d,delaunay_2d_cdt,tessellate_polygon
from mathutils.kdtree import KDTree
from kit import model as G


def surface_uv(p,surface):
    hit,_,fi,_=surface['tree'].find_nearest(p);a,b,c=surface['triangles'][fi]
    uv=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['uvs'][a],surface['uvs'][b],surface['uvs'][c])
    n=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['normals'][a],surface['normals'][b],surface['normals'][c]).normalized()
    if surface.get('polar'):
        front=surface['front'];cy=-1.37 if front else 1.42
        uv=Vector((math.atan2(p.x,(-1 if front else 1)*(p.y-cy)),p.z,0))
    return uv,n


def evaluate_chart(uv,surface):
    if surface.get('polar'):
        from suv_sculpt import radial_point
        return radial_point(surface['tree'],abs(uv.x),uv.y,surface['front'],-1 if uv.x<0 else 1)
    from mathutils.bvhtree import BVHTree
    if 'uv_tree' not in surface:
        surface['uv_tree']=BVHTree.FromPolygons(surface['uvs'],surface['triangles'],all_triangles=True)
    hit,_,fi,_=surface['uv_tree'].find_nearest(Vector((uv.x,uv.y,0)));a,b,c=surface['triangles'][fi]
    us=surface['uvs'];ps=surface['points'];ns=surface['normals']
    return (barycentric_transform(hit,us[a],us[b],us[c],ps[a],ps[b],ps[c]),
            barycentric_transform(hit,us[a],us[b],us[c],ns[a],ns[b],ns[c]).normalized())


def boundary_indices(nu,nv):
    return list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]


def outline_loop(lamp,surface):
    raw=list(lamp['aperture_samples']);points=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu,nv=lamp['form_columns'],lamp['form_rows']
    indices=boundary_indices(nu,nv)
    loop=[points[i] for i in indices]
    uv=[surface_uv(p,surface)[0] for p in loop]
    wrapped=bool(surface.get('polar')) or lamp.name.startswith(('Taillamp','Headlamp'))
    if not wrapped:
        hull=list(convex_hull_2d([p.to_2d() for p in uv]));uv=[uv[i] for i in hull];loop=[loop[i] for i in hull]
    area=sum(a.x*b.y-b.x*a.y for a,b in zip(uv,uv[1:]+uv[:1]))
    if area<0:loop.reverse()
    expanded=[]
    for i,p in enumerate(loop):
        _,n=surface_uv(p,surface);edge=loop[(i+1)%len(loop)]-loop[i-1]
        outward=edge.cross(n).normalized()
        if surface.get('polar') and not surface['front']:outward.negate()
        expanded.append(surface_uv(p+outward*.00225,surface)[0])
    if not wrapped:
        expanded=[expanded[i] for i in convex_hull_2d([p.to_2d() for p in expanded])]
    area=sum(a.x*b.y-b.x*a.y for a,b in zip(expanded,expanded[1:]+expanded[:1]))
    if area<0:expanded.reverse()
    return expanded


def outline(lamp,surface):
    """Convex partition of the actual border, never its convex hull.

    A straight hull across the wrapped rear corner cut a triangular bite out
    of the D-pillar even though the three-dimensional optical guide was level.
    Preserve concavity in chart space and merge only provably convex neighbors.
    """
    loop=outline_loop(lamp,surface)
    parts=[[loop[i] for i in t] for t in tessellate_polygon([loop])]
    def key(p):return tuple(round(v,6) for v in p)
    changed=True
    while changed:
        changed=False
        for i,a in enumerate(parts):
            for j in range(i+1,len(parts)):
                bb=parts[j];edges=[(p,q) for poly in [a,bb] for p,q in zip(poly,poly[1:]+poly[:1])]
                remaining=[(p,q) for p,q in edges if not any(key(p)==key(s) and key(q)==key(r) for r,s in edges)]
                if len(remaining)==len(edges):continue
                order={key(p):q for p,q in remaining};merged=[remaining[0][0]]
                for _ in range(len(remaining)-1):merged.append(order[key(merged[-1])])
                if key(order[key(merged[-1])])!=key(merged[0]):continue
                if any((merged[(k+1)%len(merged)]-p).cross(merged[(k+2)%len(merged)]-merged[(k+1)%len(merged)]).z < -1e-7 for k,p in enumerate(merged)):continue
                parts[i]=merged;parts.pop(j);changed=True;break
            if changed:break
    return parts


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
    border=boundary_indices(ob['form_columns'],ob['form_rows'])
    if sum(uv[a].x*uv[c].y-uv[c].x*uv[a].y for a,c in zip(border,border[1:]+border[:1]))<0:border.reverse()
    wrapped=ob.name.startswith(('Taillamp','Headlamp'));optical=ob.name.startswith(('Taillamp','Headlamp'))
    # Retain every original guide, especially seam endpoints, in the CDT.
    # A nearest point on a coarser optical disk moved the border by millimeters
    # and made a staircase when it was projected back for the paint cut.
    coords,_,faces,*_=delaunay_2d_cdt(uv,[],[border] if optical else [],1 if optical else 0,1e-6)
    used=sorted({i for face in faces for i in face});remap={old:i for i,old in enumerate(used)}
    coords=[coords[i] for i in used];faces=[tuple(remap[i] for i in face) for face in faces]
    if 'uv_tree' not in surface:
        surface['uv_tree']=BVHTree.FromPolygons(surface['uvs'],surface['triangles'],all_triangles=True)
    ps=[]
    for q in coords:
        p,n=evaluate_chart(q,surface);ps.append(p+n*.004)
    inverse=ob.matrix_world.inverted();old=ob.data
    mesh=bpy.data.meshes.new(old.name+' chart disk');mesh.from_pydata([inverse@p for p in ps],[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    center=sum((ps[i] for i in faces[0]),Vector())/len(faces[0])
    hint=Vector((center.x,-1 if front else 1,0))
    if ob.data.polygons[0].normal.dot(hint)<0:
        for face in ob.data.polygons:face.flip()
    sol=ob.modifiers.new('Chart lens gauge','SOLIDIFY');sol.thickness=ob.get('glazing_gauge_m',.0015);sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    actual=KDTree(len(ps))
    for i,p in enumerate(ps):actual.insert(p,i)
    actual.balance()
    snapped=[actual.find(p)[0].copy() for p in guides]
    ob['aperture_samples']=[v for p in snapped for v in p]
    ob['chart_disk_topology']=True


def difference(polygon,region):
    """Convex difference; vertices carry both UV and original 3D position."""
    original=polygon;pieces=[]
    for a,b in zip(region,region[1:]+region[:1]):
        edge=b-a
        def signed(uv):return edge.x*(uv.y-a.y)-edge.y*(uv.x-a.x)
        inside=[];outside=[]
        for p,q in zip(polygon,polygon[1:]+polygon[:1]):
            dp,dq=signed(p[0]),signed(q[0])
            (inside if dp>=0 else outside).append(p)
            if dp*dq<0:
                t=dp/(dp-dq);v=(p[0].lerp(q[0],t),p[1].lerp(q[1],t),True);inside.append(v);outside.append(v)
        if len(outside)>=3:pieces.append(outside)
        polygon=inside
        if len(polygon)<3:return [original]  # no intersection; don't fragment untouched skin
    return pieces


def cut_mesh_clipped(ob,cutters,surface):
    from suv_body import closeable_sheet,conform_edges,skin_gauge
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
        if ob.get('skin_face_provenance'):
            if face.material_index!=0:continue
        elif (normal_matrix@face_normal).dot(n)<.90:continue
        original=[(uvs[i],points[i],False) for i in face.vertices];pieces=[original]
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
        offset=len(vertices)
        vertices.extend(inverse@(evaluate_chart(p[0],surface)[0] if surface.get('polar') and p[2] else p[1]) for p in polygon)
        faces.append(tuple(range(offset,len(vertices))))
    old=ob.data;mesh=bpy.data.meshes.new(old.name+' lamp apertures');mesh.from_pydata(vertices,[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);conform_edges(bm)
    bmesh.ops.dissolve_limit(bm,angle_limit=.001,verts=list(bm.verts),edges=list(bm.edges),use_dissolve_boundaries=False,delimit=set())
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bad=[f for f in bm.faces if f.calc_area()<1e-11]
    if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
    bm.to_mesh(ob.data);bm.free();closeable_sheet(ob)
    skin_gauge(ob,.003 if ob.get('part_category') in ['fascia','cladding'] else .0009)
    ob['lamp_apertures_cut']=True


def cut_mesh(ob,cutters,surface):
    """Constrain only triangles crossed by a physical end-face aperture.

    The angular/height chart is injective on the local fascia. Unaffected
    triangles retain their exact positions and winding; they never pass through
    another chart. Complete hole loops replace convex-partition extensions.
    """
    if not surface.get('polar'):return cut_mesh_clipped(ob,cutters,surface)
    from suv_body import closeable_sheet,skin_gauge,conform_edges
    matrix=ob.matrix_world.copy();inverse=matrix.inverted()
    points=[matrix@v.co for v in ob.data.vertices]
    uvs=[surface_uv(p,surface)[0].to_2d() for p in points]
    boxes=[bounds(p) for p in cutters]
    def intersects(a,c):return not (a[0]>c[1] or a[1]<c[0] or a[2]>c[3] or a[3]<c[2])
    ob.data.calc_loop_triangles();active=[];fixed=[]
    for tri in ob.data.loop_triangles:
        if tri.material_index!=0:continue
        ids=tuple(tri.vertices);box=bounds([uvs[i] for i in ids])
        crosses=any(intersects(box,b) for b in boxes)
        if crosses:
            center=sum((points[i] for i in ids),Vector())/3
            radial=Vector((center.x,center.y-(-1.37 if surface['front'] else 1.42),0)).normalized()
            # The hood can share theta/Z with the vertical fascia below its
            # crest. Only the outward wall belongs to this local chart.
            crosses=abs((matrix.to_3x3()@tri.normal).dot(radial))>.25
        _,normal=surface_uv(sum((points[i] for i in ids),Vector())/3,surface)
        if (matrix.to_3x3()@tri.normal).dot(normal)<0:ids=tuple(reversed(ids))
        (active if crosses else fixed).append(ids)
    if not active:return
    used=sorted({i for f in active for i in f});lookup={old:i for i,old in enumerate(used)}
    coords=[uvs[i] for i in used];positions=[points[i] for i in used]
    def ccw(face):
        area=sum(coords[i].x*coords[j].y-coords[j].x*coords[i].y for i,j in zip(face,face[1:]+face[:1]))
        return tuple(reversed(face)) if area<0 else tuple(face)
    constraints=[ccw([lookup[i] for i in f]) for f in active];count=len(constraints)
    from mathutils.bvhtree import BVHTree
    local_chart=BVHTree.FromPolygons([Vector((*q,0)) for q in coords],constraints,all_triangles=True)
    for poly in cutters:
        first=len(coords);coords.extend(p.to_2d() for p in poly);constraints.append(ccw(list(range(first,len(coords)))))
    result,_,triangles,originals,_,ids=delaunay_2d_cdt(coords,[],constraints,0,1e-7)
    kept=[f for f,orig in zip(triangles,ids) if any(i<count for i in orig) and not any(i>=count for i in orig)]
    vertices=[];faces=[]
    for f in fixed:
        offset=len(vertices);vertices.extend(inverse@points[i] for i in f);faces.append(tuple(range(offset,offset+3)))
    mapping={}
    for i in sorted({i for f in kept for i in f}):
        old=next((j for j in originals[i] if j<len(positions)),None)
        if old is not None:p=positions[old]
        else:
            # Intersect the physical game triangle, not a different curved
            # surface. Mixing projected new vertices with old coarse chords
            # created ridges through the skinny aperture-cut triangles.
            hit,_,fi,_=local_chart.find_nearest(Vector((*result[i],0)))
            a,c,d=constraints[fi]
            p=barycentric_transform(hit,Vector((*coords[a],0)),Vector((*coords[c],0)),Vector((*coords[d],0)),positions[a],positions[c],positions[d])
        mapping[i]=len(vertices);vertices.append(inverse@p)
    for face in kept:
        ordered=face if surface['front'] else list(reversed(face))
        faces.append(tuple(mapping[i] for i in ordered))
    old=ob.data;mesh=bpy.data.meshes.new(old.name+' local angular cuts');mesh.from_pydata(vertices,[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);conform_edges(bm)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bm.to_mesh(mesh);bm.free();closeable_sheet(ob)
    skin_gauge(ob,.003 if ob.get('part_category') in ['fascia','cladding'] else .0009)
    ob['lamp_apertures_cut']=True


def carve(front,lamps,surface,recess=.010):
    cutters=([outline_loop(lamp,surface) for lamp in lamps] if surface.get('polar') else [region for lamp in lamps for region in outline(lamp,surface)])
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','fascia','pillars','cladding']:continue
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
