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
    # Chart-straight hull edges bend on the parent. A lens that keeps only
    # their endpoints chords through the skin, while the aperture cut follows
    # the curved parent; the visible result is a second, torn-looking outline.
    # Retain the same outline, adding only samples needed by its curvature.
    for _ in range(4):
        coords,_,faces,*_=delaunay_2d_cdt(uv,[],[],0,1e-6)
        edges={}
        for f in faces:
            for a,b in zip(f,f[1:]+f[:1]):
                key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
        points=[surface_point(Vector((q.x,q.y,0)),surface) for q in coords]
        add=[]
        for (a,b),count in sorted(edges.items()):
            if count!=1:continue
            q=(coords[a]+coords[b])/2
            p=surface_point(Vector((q.x,q.y,0)),surface)
            if (p-(points[a]+points[b])/2).length>.003:
                add.append(q)
        if not add:break
        uv=list(coords)+add
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
    # Preserve the chart's coherent winding. Flipping isolated bent chord
    # triangles made adjacent faces disagree and corrupted the Solidify gauge.
    # Pick the global handedness by area-weighted agreement with the parent.
    agreement=0.0
    for face in faces:
        a,b,c=[ps[i] for i in face]
        agreement+=(b-a).cross(c-a).dot(surface_uv((a+b+c)/3,surface)[1])
    if agreement<0:faces=[tuple(reversed(face)) for face in faces]
    ob['lens_outer_faces']=len(faces)
    count=len(ps);edges={}
    for face in faces:
        for a,b in zip(face,face[1:]+face[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
    closed=faces+[tuple(i+count for i in reversed(face)) for face in faces]
    closed += [(b,a,a+count,b+count) for rows in edges.values() if len(rows)==1 for a,b in rows]
    back=[p-surface_uv(p,surface)[1]*.0015 for p in ps]
    inverse=ob.matrix_world.inverted();old=ob.data
    mesh=bpy.data.meshes.new(old.name+' chart disk');mesh.from_pydata([inverse@p for p in ps+back],[],closed);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
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


def retile_metric(bm,ob,surface):
    """Triangulate a skin in an injective projection with physical spacing.

    The curved chart stretches the lamp-tip region almost tangentially. Its
    Delaunay diagonals can therefore become inverted world-space chords. The
    hood is an XY height field. Rear skins use radial projections from inside
    their convex envelope, retaining both sides of the lower lip as constraints.
    Every retained point stays on the same evaluated parent, including any
    CDT intersection vertex; there is no independent replacement surface.
    """
    from mathutils.bvhtree import BVHTree
    bm.verts.ensure_lookup_table();bm.verts.index_update()
    matrix=ob.matrix_world;inverse=matrix.inverted()
    points=[matrix@v.co for v in bm.verts]
    hood=ob.name=='Hood outer';quarter=ob.name.startswith(('Rear quarter','Front fender'))
    sign=-1 if ob.name.endswith('_L') else 1
    front=ob.name.startswith('Front fender')
    origin=Vector((0,-1.3 if front else 1.3,.0 if front else .75 if quarter else .55))
    def project(p):
        if hood:return Vector((p.x,p.y,0))
        if quarter:return Vector(((p.y-origin.y)/abs(p.x),(p.z-origin.z)/abs(p.x),0))
        return Vector((p.x/(p.y-origin.y),(p.z-origin.z)/(p.y-origin.y),0))
    def ray(q):
        if hood:return Vector((q.x,q.y,3)),Vector((0,0,-1))
        return origin,Vector((sign,q.x,q.y) if quarter else (q.x,1,q.y)).normalized()
    xy=[project(p) for p in points]
    edges=[]
    from hatch_body import shoulder_height,character_height
    for e in bm.edges:
        a,b=[matrix@v.co for v in e.verts];p=(a+b)/2
        crease=not hood and p.y>1.9 and (.55<p.z<.72 or .88<p.z<.94)
        aligned=False
        if quarter and abs(a.x)>.80 and abs(b.x)>.80 and abs(a.y-b.y)>.010:
            for height,offsets in [(shoulder_height,[-.018,0,.018]),(character_height,[.010,.037,.065])]:
                da,db=a.z-height(a.y),b.z-height(b.y)
                if abs(da-db)<.002 and min(max(abs(da-q),abs(db-q)) for q in offsets)<.002:aligned=True
        if len(e.link_faces)==1 or crease or aligned:edges.append(tuple(v.index for v in e.verts))
    old=BVHTree.FromPolygons(xy,[tuple(v.index for v in f.verts) for f in bm.faces])
    coords,_,faces,original,*_=delaunay_2d_cdt([p.to_2d() for p in xy],edges,[],0,1e-8)
    faces=[f for f in faces if old.ray_cast(sum((Vector((coords[i].x,coords[i].y,0)) for i in f),Vector())/len(f)+Vector((0,0,1)),Vector((0,0,-1)),2)[0] is not None]
    ps=[]
    for q,indices in zip(coords,original):
        if indices:ps.append(points[indices[0]])
        else:
            start,direction=ray(q);hit=surface['tree'].ray_cast(start,direction,4)[0]
            if hit is None:raise ValueError('Metric skin sample missed parent: '+ob.name)
            ps.append(hit)
    if not hood and (not quarter or sign<0):faces=[tuple(reversed(f)) for f in faces]
    mesh=bpy.data.meshes.new('Metric skin triangles');mesh.from_pydata([inverse@p for p in ps],[],faces);mesh.update()
    result=bmesh.new();result.from_mesh(mesh);bpy.data.meshes.remove(mesh);bm.free()
    return result


def metric_sample(p,surface):
    hit,_,fi,_=surface['tree'].find_nearest(p);a,b,c=surface['triangles'][fi]
    n=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['normals'][a],surface['normals'][b],surface['normals'][c]).normalized()
    return hit,n


def reduce_flat_samples(bm,ob,surface):
    """Retire redundant interior samples, with geometric/reflection bounds.

    Every rim and retained sample stays fixed. Candidate replacement triangles
    must remain within 0.3 mm of the parent at their centroid/edge midpoints,
    and interpolate its normals within 1.5 degrees at those same probes.
    This is a local error test, not a whole-panel decimation ratio.
    """
    from mathutils.geometry import tessellate_polygon
    from hatch_body import shoulder_height
    matrix=ob.matrix_world;removed=0;maximum=0.;normal_limit=.9996573249755573
    for _ in range(3):
        bm.normal_update();bm.verts.index_update()
        candidates=sorted(list(bm.verts),key=lambda v:(sum(f.calc_area() for f in v.link_faces),v.index))
        for v in candidates:
            if not v.is_valid or len(v.link_edges)<3 or len(v.link_edges)>9:continue
            if any(len(e.link_faces)!=2 for e in v.link_edges) or any(len(f.verts)!=3 for f in v.link_faces):continue
            p=matrix@v.co
            # Leave the two tight gate lines and the character-line turn intact.
            if p.y>1.9 and (.55<p.z<.72 or .87<p.z<.94):continue
            if p.y>1.35 and abs(p.x)>.80 and abs(p.z-shoulder_height(p.y))<.025:continue
            next_vertex={}
            for f in v.link_faces:
                ids=list(f.verts);i=ids.index(v);next_vertex[ids[(i+1)%3]]=ids[(i+2)%3]
            if len(next_vertex)!=len(v.link_faces):continue
            start=next(iter(next_vertex));ring=[start]
            while len(ring)<len(next_vertex) and next_vertex.get(ring[-1]) not in ring:ring.append(next_vertex[ring[-1]])
            if len(ring)!=len(next_vertex) or next_vertex.get(ring[-1])!=start:continue
            if max((q.co-v.co).length for q in ring)>.085:continue
            coords=[matrix@q.co for q in ring];lookup={tuple(p):q for p,q in zip(coords,ring)}
            triangles=tessellate_polygon([coords])
            triangles=[tuple(coords[q] if isinstance(q,int) else q for q in tri) for tri in triangles]
            accepted=bool(triangles);error=0.
            normals={tuple(q):metric_sample(q,surface)[1] for q in coords}
            for tri in triangles:
                a,b,c=tri;normal=(b-a).cross(c-a)
                ns=[normals[tuple(q)] for q in tri]
                probes=[((a+b+c)/3,sum(ns,Vector()).normalized())]
                probes += [((tri[i]+tri[(i+1)%3])/2,(ns[i]+ns[(i+1)%3]).normalized()) for i in range(3)]
                for q,n in probes:
                    hit,pn=metric_sample(q,surface);distance=(q-hit).length;error=max(error,distance)
                    if distance>.0003 or n.dot(pn)<normal_limit or normal.dot(pn)<=0:accepted=False;break
                if not accepted:break
            if not accepted:continue
            new_faces=[tuple(lookup[tuple(q)] for q in tri) for tri in triangles]
            if any(bm.faces.get(face) is not None for face in new_faces):continue
            bmesh.ops.delete(bm,geom=[v],context='VERTS')
            for face in new_faces:bm.faces.new(face)
            removed+=1;maximum=max(maximum,error)
    ob['retired_interior_samples']=removed;ob['retile_probe_error_m']=maximum
    bm.normal_update()


def resolve_turns(bm,ob,surface,fold_only=False):
    """Resolve tight reflections in physical space before closing sheet gauge."""
    matrix=ob.matrix_world;inverse=matrix.inverted();added=0
    front=ob.name=='Hood outer' or ob.name.startswith('Front fender')
    from hatch_body import shoulder_height
    for iteration in range(2):
        selected=[]
        for f in bm.faces:
            p=matrix@f.calc_center_median()
            hit,n=metric_sample(p,surface)
            normal=matrix.to_3x3().inverted().transposed()@f.normal
            if f.calc_area()>1e-10 and normal.dot(n)<0:selected.append(f);continue
            if fold_only:continue
            crown=.60<abs(p.x) and -2.05<p.y<-1.02 and p.z>.72
            shoulder=abs(p.x)>.80 and 1.35<p.y<1.85 and abs(p.z-shoulder_height(p.y))<.045
            if iteration and not front and not shoulder:continue
            corner=abs(p.x)>.65 and (p.y>1.60 and p.z<.99 or p.y<-1.70 and p.z<.72)
            if not (crown or corner):continue
            ps=[matrix@v.co for v in f.verts]
            interp=sum((metric_sample(q,surface)[1] for q in ps),Vector()).normalized()
            if abs((hit-p).dot(n))>(.0004 if crown else .0006) or interp.dot(n)<(.999390827 if crown else .999048222):selected.append(f)
        edges={e for f in selected for e in f.edges}
        if not edges:break
        bm.edges.index_update()
        for e in sorted(edges,key=lambda e:e.index):
            a,b=e.verts;mid=(matrix@a.co+matrix@b.co)/2
            if len(e.link_faces)==1:
                uv=(surface_uv(matrix@a.co,surface)[0]+surface_uv(matrix@b.co,surface)[0])/2
                point=surface_point(uv,surface)
            else:point=metric_sample(mid,surface)[0]
            _,v=bmesh.utils.edge_split(e,a,.5);v.co=inverse@point;added+=1
        bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if len(f.verts)>3],quad_method='BEAUTY',ngon_method='BEAUTY')
        bm.normal_update()
    ob['reflection_samples_added']=added


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
    # Cutter extensions leave many nearly coincident points on a straight
    # chart boundary. Keep authored surface samples, but retire redundant
    # intersection points where the physical chord misses by under 0.3 mm.
    # This spends the game budget on crowns/creases instead of clipping crumbs.
    retired=0
    for _ in range(3):
        count=0
        for v in list(bm.verts):
            if not v.is_valid or kd.find(v.co)[2]<1e-5:continue
            rim=[e for e in v.link_edges if len(e.link_faces)==1]
            if len(rim)!=2:continue
            aa,bb=[e.other_vert(v) for e in rim];delta=bb.co-aa.co
            if delta.length<1e-8:continue
            t=(v.co-aa.co).dot(delta)/delta.length_squared
            if not 0<t<1 or (v.co-aa.co-delta*t).length>2e-5:continue
            pa,pb=[surface_point(q.co,surface) for q in [aa,bb]]
            if (pb-pa).length>.030:continue
            pm=surface_point((aa.co+bb.co)/2,surface)
            if (pm-(pa+pb)/2).length>.0003:continue
            bmesh.ops.dissolve_verts(bm,verts=[v],use_face_split=False,use_boundary_tear=False)
            count+=1
        retired+=count
        if not count:break
    ob['retired_cut_boundary_points']=retired
    bm.verts.ensure_lookup_table();bm.verts.index_update()
    boundary={v for e in bm.edges if len(e.link_faces)==1 for v in e.verts}
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
    # A Delaunay triangle in chart coordinates need not be well shaped in
    # meters. At the hood's lamp tips, long nearly collinear chords reversed
    # their physical orientation even though their UV winding was coherent.
    # Optimize the interior diagonals in the actual surface metric; retain
    # every sample and every aperture/panel boundary.
    if ob.name=='Hood outer' or ob.name.startswith(('Rear quarter','Front fender')) or ob.name=='Rear molded fascia':
        bm=retile_metric(bm,ob,surface)
    bm.normal_update()
    if not surface['high']:
        if ob.name=='Rear molded fascia' or ob.name.startswith('Rear quarter'):
            reduce_flat_samples(bm,ob,surface)
        if ob.name=='Hood outer' or ob.name.startswith(('Front fender','Rear quarter')) or ob.name=='Rear molded fascia':
            resolve_turns(bm,ob,surface)
            reduce_flat_samples(bm,ob,surface)
        elif ob.name=='Front molded fascia':resolve_turns(bm,ob,surface,fold_only=True)
    bad=[f for f in bm.faces if f.calc_area()<1e-10]
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
