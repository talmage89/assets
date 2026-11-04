"""Lamp openings cut in the hatch's evaluated subdivision parameter chart.

Reference pixels never enter this operation. The original locator outline is
projected onto the parent, offset 2.25 mm in its tangent plane, and faired to a convex
outline in the 2D chart. Cut skin vertices return to the evaluated fair parent;
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
    uv.z=0.0  # Barycentric roundoff must never bend the two-dimensional chart.
    n=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['normals'][a],surface['normals'][b],surface['normals'][c]).normalized()
    return uv,n


def surface_point(uv,surface):
    """Project a new cut vertex onto the same fair parent used by its outline."""
    from mathutils.bvhtree import BVHTree
    if 'uv_tree' not in surface:
        surface['uv_tree']=BVHTree.FromPolygons(surface['uvs'],surface['triangles'],all_triangles=True)
    p,_,fi,_=surface['uv_tree'].find_nearest(uv);a,b,c=surface['triangles'][fi]
    return barycentric_transform(p,surface['uvs'][a],surface['uvs'][b],surface['uvs'][c],surface['points'][a],surface['points'][b],surface['points'][c])


def outline(lamp,surface):
    raw=list(lamp['aperture_samples']);points=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu,nv=lamp['form_columns'],lamp['form_rows']
    indices=list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]
    # The lens disk is the convex hull of ALL projected guide samples.
    # A folded Cartesian guide may put an interior row beyond its perimeter;
    # cutting only the perimeter leaves painted triangles through the lens.
    loop=points if lamp.get('chart_disk_topology') else [points[i] for i in indices]
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
    # Orient triangles from their evaluated positions, not a possibly stale
    # polygon normal immediately after from_pydata()/flip(). The mirrored
    # chart reverses handedness; both optical skins must face away from metal.
    oriented=[]
    for face in faces:
        a,b,c=[ps[i] for i in face]
        n=surface_uv((a+b+c)/3,surface)[1]
        oriented.append(tuple(reversed(face)) if (b-a).cross(c-a).dot(n)<0 else face)
    faces=oriented
    inverse=ob.matrix_world.inverted();old=ob.data
    mesh=bpy.data.meshes.new(old.name+' chart disk');mesh.from_pydata([inverse@p for p in ps],[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    ob['lens_outer_faces']=len(ob.data.polygons)
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
    from mathutils.bvhtree import BVHTree
    matrix=ob.matrix_world.copy();inverse=matrix.inverted();normal_matrix=matrix.to_3x3().inverted().transposed()
    points=[matrix@v.co for v in ob.data.vertices];uvs=[surface_uv(p,surface)[0] for p in points]
    polygons=[];affected=False
    cutter_boxes=[bounds(t) for t in cutters]
    def intersects(a,b):return not(a[0]>b[1] or a[1]<b[0] or a[2]>b[3] or a[3]<b[2])
    ob.data.calc_loop_triangles()
    outer_indices=sorted({i for f in ob.data.polygons[:ob['outer_skin_faces']] for i in f.vertices})
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
        # Stitch the cut in the injective parameter chart. Projecting first
        # bends a subdivided edge away from its old chord, so a geometric
        # collinearity test misses its T vertices and leaves hairline tears.
        offset=len(vertices);vertices.extend(p[0] for p in polygon);faces.append(tuple(range(offset,len(vertices))))
    old=ob.data;mesh=bpy.data.meshes.new(old.name+' lamp apertures');mesh.from_pydata(vertices,[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    bm=bmesh.new();bm.from_mesh(ob.data)
    # Chart units span 0..48, so use a tolerance above float32's local ULP.
    # This is a few microns on the body, below any visible manufacturing edge.
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5);conform_edges(bm,tolerance=2e-5)
    # Convex difference extends each cutter edge through every intersected
    # triangle. Those interior intersection points are clipping machinery,
    # not surface detail. Retile the chart with the original samples plus the
    # true cut perimeter; constrain every boundary, including holes.
    bm.verts.ensure_lookup_table();bm.verts.index_update()
    boundary={v for e in bm.edges if len(e.link_faces)==1 for v in e.verts}
    # Original pre-cut UV samples were saved before replacing the mesh.
    source_uvs=[uvs[i] for i in outer_indices]
    kd=KDTree(len(source_uvs))
    for i,q in enumerate(source_uvs):kd.insert(q,i)
    kd.balance()
    required={v for v in bm.verts if v in boundary or kd.find(v.co)[2]<1e-5}
    constraints={e for e in bm.edges if len(e.link_faces)==1}
    if ob.name=='Rear molded fascia':
        for e in bm.edges:
            if not all(v in required for v in e.verts):continue
            p=surface_point((e.verts[0].co+e.verts[1].co)/2,surface)
            if p.y>1.9 and .55<p.z<.72:constraints.add(e)
    chart_points=[v.co.copy() for v in bm.verts]
    region_tree=BVHTree.FromPolygons(chart_points,[tuple(v.index for v in f.verts) for f in bm.faces])
    before_area=sum(f.calc_area() for f in bm.faces)
    max_probe_gap=0.0
    for attempt in range(4):
        max_probe_gap=0.0
        kept=sorted(required,key=lambda v:v.index);lookup={v:i for i,v in enumerate(kept)}
        edges=sorted(tuple(sorted((lookup[e.verts[0]],lookup[e.verts[1]]))) for e in constraints)
        coords,_,disk,*_=delaunay_2d_cdt([v.co.to_2d() for v in kept],edges,[],0,1e-7)
        chart=[Vector((q.x,q.y,0)) for q in coords]
        disk=[f for f in disk if region_tree.ray_cast(
            sum((chart[i] for i in f),Vector())/len(f)+Vector((0,0,1)),Vector((0,0,-1)),2)[0] is not None]
        # Old projected triangles can overlap in the chart at a folded rim.
        # Require coverage of every old centroid and edge midpoint. If a
        # narrow fragment crosses a new chord, retain its edges explicitly.
        new_tree=BVHTree.FromPolygons(chart,disk,all_triangles=True);missed=set()
        for f in bm.faces:
            if f.calc_area()<1e-9:continue
            probes=[f.calc_center_median()]+[(e.verts[0].co+e.verts[1].co)/2 for e in f.edges]
            for q in probes:
                if new_tree.ray_cast(q+Vector((0,0,1)),Vector((0,0,-1)),2)[0] is None:
                    hit,_,_,distance=new_tree.find_nearest(q)
                    if distance>1e-5:
                        gap=(surface_point(q,surface)-surface_point(hit,surface)).length
                        max_probe_gap=max(max_probe_gap,gap)
                        # Float32 chart coordinates represent microns on the
                        # body. Judge residual error in meters, not UV units.
                        if gap>2e-5:missed.add(f)
        if not missed:break
        for f in missed:required.update(f.verts);constraints.update(f.edges)
    if missed:raise ValueError(('Cut retessellation lost chart coverage',ob.name,len(missed),max_probe_gap,[list(f.calc_center_median()) for f in missed]))
    ob['cut_max_chart_probe_gap_m']=max(float(ob.get('cut_max_chart_probe_gap_m',0)),max_probe_gap)
    after_area=sum(abs((chart[f[1]]-chart[f[0]]).cross(chart[f[2]]-chart[f[0]]).z)/2 for f in disk)
    ob['cut_chart_overlap_area_removed']=float(ob.get('cut_chart_overlap_area_removed',0))+max(0,before_area-after_area)
    # Preserve the parent's chart handedness (the connected sheet has one).
    # Parent U then V is outward everywhere on the single connected sheet.
    bm.free();mesh=bpy.data.meshes.new('Constrained aperture chart');mesh.from_pydata(chart,[],disk);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bpy.data.meshes.remove(mesh)
    # Clipped convex polygons are convex in this chart, not necessarily in
    # space. Triangulate before bending them onto the parent: a 3D n-gon
    # tessellator can otherwise fold a skinny cut fragment over its neighbor.
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    for v in bm.verts:v.co=inverse@surface_point(v.co,surface)
    bm.normal_update()
    bad=[f for f in bm.faces if f.calc_area()<1e-11]
    if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
    bm.to_mesh(ob.data);bm.free();closeable_sheet(ob,weld=False)
    ob['outer_skin_faces']=len(ob.data.polygons)
    # Extrude along the fair parent's normals. Averaging the newly clipped
    # triangle fans can cancel at a very narrow mouth vertex, producing a
    # zero-thickness corner and collapsed Solidify rim. The parent field has
    # a defined normal everywhere along this continuous sheet.
    thickness=.003 if ob.get('part_category')=='fascia' else .0009
    ps=[v.co.copy() for v in ob.data.vertices];count=len(ps)
    back=[inverse@(matrix@p-surface_uv(matrix@p,surface)[1]*thickness) for p in ps]
    fs=[tuple(f.vertices) for f in ob.data.polygons];edges={}
    for face in fs:
        for aa,bb in zip(face,face[1:]+face[:1]):edges.setdefault(tuple(sorted((aa,bb))),[]).append((aa,bb))
    closed=fs+[tuple(i+count for i in reversed(face)) for face in fs]
    closed += [(bb,aa,aa+count,bb+count) for rows in edges.values() if len(rows)==1 for aa,bb in rows]
    old=ob.data;mesh=bpy.data.meshes.new(old.name+' parent-normal gauge');mesh.from_pydata(ps+back,[],closed);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    ob['lamp_apertures_cut']=True


def carve(front,lamps,surface,recess=.010):
    # A newly parented garnish/lens has already been baked into pivot-local
    # coordinates by attach(); evaluate its world matrix before any ray query.
    bpy.context.view_layer.update()
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
        if 'lens_outer_faces' in lamp:
            # The optical blank shares the parent's continuous mold. Its
            # skinny chart triangles must not generate independent facets.
            G.smooth(lamp,90);custom=[];normal_matrix=matrix.to_3x3().transposed()
            count=lamp['lens_outer_faces']
            for face in lamp.data.polygons:
                outer=face.index<count;inner=count<=face.index<2*count
                face.use_smooth=outer or inner
                for li in face.loop_indices:
                    p=matrix@lamp.data.vertices[lamp.data.loops[li].vertex_index].co
                    n=surface_uv(p,surface)[1]
                    custom.append(normal_matrix@(n if outer else -n) if outer or inner else face.normal)
            lamp.data.normals_split_custom_set(custom)
