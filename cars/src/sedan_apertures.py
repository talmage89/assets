"""Lamp openings cut in the sedan's evaluated subdivision parameter chart.

Reference pixels never enter this operation. The original locator outline is
projected onto the parent and expanded by the manufactured reveal. Convex
pieces retain its true concavity; the hood uses its natural XY plane. Cut skin fragments retain their original face planes;
all gauge rims are constructed after cutting. No volume unions or thin booleans.
"""
import math
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import barycentric_transform,convex_hull_2d,delaunay_2d_cdt,tessellate_polygon
from mathutils.kdtree import KDTree
from kit import model as G


def surface_uv(p,surface):
    hit,_,fi,_=surface['tree'].find_nearest(p);a,b,c=surface['triangles'][fi]
    uv=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['uvs'][a],surface['uvs'][b],surface['uvs'][c])
    n=barycentric_transform(hit,surface['points'][a],surface['points'][b],surface['points'][c],surface['normals'][a],surface['normals'][b],surface['normals'][c]).normalized()
    return uv,n


def convex_pieces(poly):
    """Convex decomposition of the true bent optical outline, without hull loss."""
    pieces=[[poly[v] if isinstance(v,int) else v for v in t] for t in tessellate_polygon([poly])]
    def area(ps):return abs(sum(a.x*c.y-c.x*a.y for a,c in zip(ps,ps[1:]+ps[:1])))*.5
    changed=True
    while changed:
        changed=False
        for i,a in enumerate(pieces):
            for j in range(i+1,len(pieces)):
                c=pieces[j]
                shared=sum(any((p-q).length<1e-7 for q in c) for p in a)
                if shared<2:continue
                candidates=[]
                for q in a+c:
                    if not any((p-q).length<1e-7 for p in candidates):candidates.append(q)
                hull=[candidates[k] for k in convex_hull_2d([p.to_2d() for p in candidates])]
                if abs(area(hull)-area(a)-area(c))>1e-9:continue
                if sum(p.x*q.y-q.x*p.y for p,q in zip(hull,hull[1:]+hull[:1]))<0:hull.reverse()
                pieces[i]=hull;pieces.pop(j);changed=True;break
            if changed:break
    return pieces


def outline(lamp,surface):
    raw=list(lamp['aperture_samples']);points=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu,nv=lamp['form_columns'],lamp['form_rows']
    indices=list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]
    loop=[points[i] for i in indices]
    if lamp.get('fascia_axial'):
        # These end openings are a height field in world X/Z. Cut in their
        # original projection plane, so repeated cuts never reconstruct UVs
        # from a faceted chord and grow long, thin stars around a sharp pocket.
        plane=[Vector((p.x,p.z,0)) for p in loop]
        plane=[plane[i] for i in convex_hull_2d([p.to_2d() for p in plane])]
        if sum(a.x*b.y-b.x*a.y for a,b in zip(plane,plane[1:]+plane[:1]))<0:plane.reverse()
        expanded=[]
        for i,p in enumerate(plane):
            edge=(plane[(i+1)%len(plane)]-plane[i-1]).normalized()
            expanded.append(p+Vector((edge.y,-edge.x,0))*.00225)
        return [expanded]
    if lamp.name.startswith('Headlamp') and 'aperture_chart_samples' in lamp:
        raw=list(lamp['aperture_chart_samples']);chart=[Vector((raw[i],raw[i+1],0)) for i in range(0,len(raw),2)]
        uv=[chart[i] for i in indices]
        if sum(p.x*q.y-q.x*p.y for p,q in zip(uv,uv[1:]+uv[:1]))<0:uv.reverse()
        def position(q):
            hit,_,fi,_=surface['uv_tree'].find_nearest(Vector((q.x,q.y,0)));a,c,d=surface['triangles'][fi]
            us=surface['uvs'];ps=surface['points']
            return barycentric_transform(hit,us[a],us[c],us[d],ps[a],ps[c],ps[d])
        expanded=[]
        for i,q in enumerate(uv):
            tangent=(uv[(i+1)%len(uv)]-uv[i-1]).normalized();outward=Vector((tangent.y,-tangent.x,0))
            eps=.001;scale=(position(q+outward*eps)-position(q-outward*eps)).length/(2*eps)
            expanded.append(q+outward*(.00325/max(scale,.001)))
        return convex_pieces(expanded)
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


def regularize_blank(ob,surface,front,high=False):
    """A feature-aligned cover strip on the continuous parent chart.

    A convex-hull triangulation joined distant optical tips with long chords
    through the hood. Instead, resample the authored centerline and solve a
    transverse tangent frame in the parent's metric. Every outer vertex is on
    that parent; no image contour or replacement volume defines this cover.
    """
    if not front:
        return regularize_rear(ob,surface,high)
    from bisect import bisect_right
    from mathutils.bvhtree import BVHTree
    raw=list(ob['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    old_nu,old_nv=ob['form_columns'],ob['form_rows']
    center_points=guides[(old_nv//2)*old_nu:(old_nv//2+1)*old_nu]
    guide_uv=[surface_uv(p,surface)[0].to_2d() for p in guides]
    center_uv=guide_uv[(old_nv//2)*old_nu:(old_nv//2+1)*old_nu]
    heights=[(guides[(old_nv-1)*old_nu+i]-guides[i]).length for i in range(old_nu)]
    if 'uv_tree' not in surface:
        surface['uv_tree']=BVHTree.FromPolygons(surface['uvs'],surface['triangles'],all_triangles=True)
    def sample(q):
        hit,_,fi,_=surface['uv_tree'].find_nearest(Vector((q.x,q.y,0)));a,b,c=surface['triangles'][fi]
        uvs=surface['uvs'];points=surface['points'];normals=surface['normals']
        p=barycentric_transform(hit,uvs[a],uvs[b],uvs[c],points[a],points[b],points[c])
        n=barycentric_transform(hit,uvs[a],uvs[b],uvs[c],normals[a],normals[b],normals[c]).normalized()
        return p+n*.004,n
    arc=[0.]
    for a,c in zip(center_points,center_points[1:]):arc.append(arc[-1]+(c-a).length)
    def center(s):
        s=max(0,min(arc[-1],s));i=min(len(arc)-2,max(0,bisect_right(arc,s)-1));span=arc[i+1]-arc[i]
        t=(s-arc[i])/max(span,1e-8);a,c=center_uv[i:i+2]
        ia=max(0,i-1);ic=min(len(arc)-1,i+2)
        ma=(center_uv[i+1]-center_uv[ia])/max(arc[i+1]-arc[ia],1e-7)
        mc=(center_uv[ic]-center_uv[i])/max(arc[ic]-arc[i],1e-7)
        q=a*(2*t**3-3*t*t+1)+ma*(span*(t**3-2*t*t+t))+c*(-2*t**3+3*t*t)+mc*(span*(t**3-t*t))
        return q,heights[i]*(1-t)+heights[i+1]*t
    steps=max(4,math.ceil(arc[-1]/(.020 if high else .030)))
    stations=[arc[-1]*i/steps for i in range(steps+1)]
    nu=len(stations);nv=7 if high else 4;rows=[[] for _ in range(nv)];charts=[[] for _ in range(nv)];row_normals=[[] for _ in range(nv)];eps=.002
    for s in stations:
        q,height=center(s);p,n=sample(q)
        qa,_=center(s-.002);qc,_=center(s+.002);tangent=(sample(qc)[0]-sample(qa)[0]).normalized()
        up=n.cross(tangent).normalized()
        if up.z<0:up.negate()
        du=(sample(q+Vector((eps,0)))[0]-sample(q-Vector((eps,0)))[0])/(2*eps)
        dv=(sample(q+Vector((0,eps)))[0]-sample(q-Vector((0,eps)))[0])/(2*eps)
        aa,bb,cc=du.dot(du),du.dot(dv),dv.dot(dv);det=aa*cc-bb*bb
        if det<1e-12:raise ValueError('Singular optical tangent frame')
        au,av=du.dot(up),dv.dot(up)
        across=Vector(((cc*au-bb*av)/det,(aa*av-bb*au)/det))
        for j in range(nv):
            offset=height*(j/(nv-1)-.5)
            qq=q+across*offset;p,n=sample(qq);rows[j].append(p);charts[j].append(qq);row_normals[j].append(n)
    ps=[p for row in rows for p in row]
    faces=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(nv-1) for i in range(nu-1)]
    inverse=ob.matrix_world.inverted();old=ob.data
    mesh=bpy.data.meshes.new(old.name+' aligned optical strip');mesh.from_pydata([inverse@p for p in ps],[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    for face in ob.data.polygons:
        p=sum((ps[i] for i in face.vertices),Vector())/len(face.vertices);_,n=surface_uv(p,surface)
        if face.normal.dot(n)<0:face.flip()
    ob.data.update();count=len(faces)
    sol=ob.modifiers.new('Aligned lens gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    custom=[]
    for face in ob.data.polygons:
        role=0 if face.index<count else 1 if face.index<2*count else 2;face.use_smooth=role!=2
        for li in face.loop_indices:
            p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co;_,n=surface_uv(p,surface)
            custom.append(n if role==0 else -n if role==1 else (0,0,0))
    ob.data.normals_split_custom_set(custom)
    ob['form_rows']=nv;ob['form_columns']=nu;ob['aperture_samples']=[v for p in ps for v in p]
    ob['lens_outer_faces']=count;ob['chart_disk_topology']=True
    ob['aperture_chart_samples']=[c for row in charts for q in row for c in [q.x,q.y]]
    ob['optical_patch_normals']=[c for row in row_normals for n in row for c in n]
    ob['form_row_fractions']=[j/(nv-1) for j in range(nv)]


def regularize_rear(ob,surface,high):
    """Sample the outermost rear sheet along a physical horizontal normal.

    The quarter's thin rolled tip is not injective under nearest-point UV
    inversion. A radial surface ray chooses the exposed surface explicitly.
    This retains the authored centerline, envelope and five-row lens section.
    """
    from bisect import bisect_right
    raw=list(ob['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    old_nu,old_nv=ob['form_columns'],ob['form_rows']
    middle=guides[(old_nv//2)*old_nu:(old_nv//2+1)*old_nu]
    heights=[abs(guides[(old_nv-1)*old_nu+i].z-guides[i].z) for i in range(old_nu)]
    arc=[0.]
    for a,c in zip(middle,middle[1:]):arc.append(arc[-1]+(c-a).length)
    steps=max(4,math.ceil(arc[-1]/(.018 if high else .027)));nu=steps+1;nv=7 if high else 5
    rows=[[] for _ in range(nv)];sign=1 if middle[0].x>0 else -1
    for k in range(nu):
        s=arc[-1]*k/steps;i=min(old_nu-2,max(0,bisect_right(arc,s)-1));t=(s-arc[i])/max(arc[i+1]-arc[i],1e-8)
        center=middle[i].lerp(middle[i+1],t);height=heights[i]*(1-t)+heights[i+1]*t
        tangent=middle[min(old_nu-1,i+2)]-middle[max(0,i-1)]
        radial=Vector((-tangent.y,tangent.x,0)).normalized()
        if radial.dot(Vector((sign,1,0)))<0:radial.negate()
        for j in range(nv):
            row=j*(old_nv-1)/(nv-1);r=min(old_nv-2,int(row));fraction=row-r
            lower=guides[r*old_nu+i].lerp(guides[r*old_nu+i+1],t)
            upper=guides[(r+1)*old_nu+i].lerp(guides[(r+1)*old_nu+i+1],t)
            guess=lower.lerp(upper,fraction)
            hit,n,_,_=surface['tree'].ray_cast(guess+radial*.70,-radial,2.0)
            if hit is None or (hit-guess).length>.045:
                hit,n,_,distance=surface['tree'].find_nearest(guess)
                if distance>.025:raise ValueError(('Outer rear optical ray missed',ob.name,k,j,distance))
            if n.dot(radial)<0:n.negate()
            q=hit+n*.004
            # A radial surface ray can walk across the lid's constant-X cut.
            # Intersect the exposed sheet at the actual reveal instead: the
            # cover must remain on its own moving/stationary side of that cut.
            from sedan_spec import PANEL_GAP
            inner=ob.get('lamp_piece')=='lid'
            limit=.615+(-1 if inner else 1)*PANEL_GAP/2
            if (abs(q.x)>limit if inner else abs(q.x)<limit):
                xx=sign*limit
                for _ in range(5):
                    ph,nh,_,_=surface['tree'].ray_cast(Vector((xx,4,guess.z)),Vector((0,-1,0)),6)
                    if ph is None:raise ValueError(('Rear optical reveal misses parent',ob.name,xx,guess.z))
                    q=ph+nh*.004;xx-=q.x-sign*limit
            rows[j].append(q)
    ps=[p for row in rows for p in row]
    faces=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(nv-1) for i in range(nu-1)]
    inverse=ob.matrix_world.inverted();old=ob.data
    mesh=bpy.data.meshes.new(old.name+' outer ray strip');mesh.from_pydata([inverse@p for p in ps],[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    for face in mesh.polygons:
        hint=sum((ps[i] for i in face.vertices),Vector())/len(face.vertices);hint=Vector((hint.x,1,0))
        if face.normal.dot(hint)<0:face.flip()
    mesh.update();count=len(faces)
    sol=ob.modifiers.new('Outer ray lens gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    # Shade the physical cover itself; no inward normal from a folded parent
    # chart is allowed to enter its smooth optical surface.
    for face in ob.data.polygons:face.use_smooth=face.index<2*count
    ob.data.update()
    ob['form_rows']=nv;ob['form_columns']=nu;ob['aperture_samples']=[v for p in ps for v in p]
    ob['lens_outer_faces']=count;ob['chart_disk_topology']=True


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


def cut_mesh(ob,cutters,surface,axial=False,front=False,spatial_boxes=None,top_projection=False):
    from sedan_body import closeable_sheet,conform_edges
    matrix=ob.matrix_world.copy();inverse=matrix.inverted();normal_matrix=matrix.to_3x3().inverted().transposed()
    points=[matrix@v.co for v in ob.data.vertices]
    uvs=[Vector((p.x,p.y,0)) if top_projection else Vector((p.x,p.z,0)) if axial else surface_uv(p,surface)[0] for p in points]
    polygons=[];affected=False
    cutter_boxes=[bounds(t) for t in cutters]
    def intersects(a,b):return not(a[0]>b[1] or a[1]<b[0] or a[2]>b[3] or a[3]<b[2])
    ob.data.calc_loop_triangles()
    for face in ob.data.loop_triangles:
        center=sum((points[i] for i in face.vertices),Vector())/3
        face_normal=face.normal
        _,n=surface_uv(center,surface)
        if ob.get('sheet_roles'):
            if ob.data.polygons[face.polygon_index].material_index!=0:continue
        elif (normal_matrix@face_normal).dot(n)<.5:continue
        original=[(uvs[i],points[i]) for i in face.vertices]
        if not any(intersects(bounds([q for q,p in original]),box) for box in cutter_boxes):
            polygons.append(original);continue
        if axial:
            sign=-1 if front else 1
            # A coarse triangle's center is a chord, not a surface sample.
            # At the tight upper grille roll it lies >15 mm behind the parent
            # even though all three vertices belong to the exposed end sheet.
            # Classifying only its center skipped the cut and left painted
            # triangular teeth inside the grille. Test its real parent vertices
            # as well; another side/roof branch still fails every end ray.
            probes=[center]+[points[i] for i in face.vertices]
            exposed=False
            for p in probes:
                outer=surface['tree'].ray_cast(Vector((p.x,sign*4,p.z)),Vector((0,-sign,0)),6)[0]
                if outer is not None and abs(outer.y-p.y)<=.015:
                    exposed=True;break
            if not exposed:
                # Keep this original triangle; it is another side/roof chart,
                # not the outer end face reached by the aperture projection.
                polygons.append([(uvs[i],points[i]) for i in face.vertices]);continue
        pieces=[original]
        world_lo=[min(points[i][k] for i in face.vertices) for k in range(3)]
        world_hi=[max(points[i][k] for i in face.vertices) for k in range(3)]
        for cutter_index,(region,box) in enumerate(zip(cutters,cutter_boxes)):
            if spatial_boxes is not None:
                lo,hi=spatial_boxes[cutter_index]
                if any(world_lo[k]>hi[k] or world_hi[k]<lo[k] for k in range(3)):continue
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
        offset=len(vertices);vertices.extend(inverse@p for q,p in polygon);faces.append(tuple(range(offset,len(vertices))))
    old=ob.data;mesh=bpy.data.meshes.new(old.name+' lamp apertures');mesh.from_pydata(vertices,[],faces);mesh.update()
    for mat in old.materials:mesh.materials.append(mat)
    ob.data=mesh
    if old.users==0:bpy.data.meshes.remove(old)
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);conform_edges(bm)
    # A broad coplanar dissolve can bridge two holes with a repeated-vertex
    # polygon. Keep convex cut fragments; only remove sub-50-micron crumbs
    # before closing the gauge. This is below a stamped reveal's tolerance.
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00005)
    bmesh.ops.triangulate(bm,faces=list(bm.faces))
    bad=[f for f in bm.faces if f.calc_area()<1e-11]
    if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
    bm.to_mesh(ob.data);bm.free();closeable_sheet(ob)
    # Clipping subdivides the original game facets. Lifting only the new
    # intersections onto the dense parent folds skinny cut fragments and
    # opens triangular teeth. Keep every original chord plane intact.
    ob.data.update()
    from sedan_body import sheet_gauge
    sheet_gauge(ob,.003 if ob.get('part_category')=='fascia' else .0009)
    ob['lamp_apertures_cut']=True


def carve(front,lamps,surface,recess=.010):
    cutters=[];spatial=[]
    for lamp in lamps:
        raw=list(lamp['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
        box=([min(p[k] for p in ps)-.012 for k in range(3)],[max(p[k] for p in ps)+.012 for k in range(3)])
        for region in outline(lamp,surface):cutters.append(region);spatial.append(box)
    axial=all(lamp.get('fascia_axial') for lamp in lamps)
    for ob in list(bpy.context.scene.objects):
        if ob.type!='MESH' or ob.get('part_category') not in ['body','doors','fascia','pillars']:continue
        if (ob.matrix_world@ob.data.vertices[0].co).y*(1 if front else -1)>0:continue
        if ob.name=='Hood outer' and all(lamp.name.startswith('Headlamp') for lamp in lamps):
            # The hood is a height field in XY. Its coarse chord intersections
            # cannot be inverted reliably through a nearest-parent UV lookup.
            # Cut its actual facet coordinates in that manufacturing plane.
            top_cutters=[]
            for lamp in lamps:
                raw=list(lamp['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
                raw=list(lamp['optical_patch_normals']);ns=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
                ps=[p-n*.0045 for p,n in zip(ps,ns)]  # final laminate seat, including the optical assembly offset
                nu,nv=lamp['form_columns'],lamp['form_rows']
                ids=list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]
                poly=[Vector((ps[i].x,ps[i].y,0)) for i in ids]
                if sum(a.x*c.y-c.x*a.y for a,c in zip(poly,poly[1:]+poly[:1]))<0:poly.reverse()
                expanded=[]
                for i,p in enumerate(poly):
                    tangent=(poly[(i+1)%len(poly)]-poly[i-1]).normalized()
                    expanded.append(p+Vector((tangent.y,-tangent.x,0))*.00325)
                top_cutters.extend(convex_pieces(expanded))
            cut_mesh(ob,top_cutters,surface,front=front,top_projection=True)
        else:cut_mesh(ob,cutters,surface,axial=axial,front=front,spatial_boxes=spatial if not axial else None)
    for lamp in lamps:
        matrix=lamp.matrix_world.copy();inverse=matrix.inverted()
        if lamp.name.startswith('Headlamp') and 'aperture_chart_samples' in lamp:
            raw=list(lamp['aperture_chart_samples']);chart=[Vector((raw[i],raw[i+1],0)) for i in range(0,len(raw),2)]
            raw=list(lamp['optical_patch_normals']);ns=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
            if len(lamp.data.vertices)!=2*len(chart):raise ValueError('Unexpected optical laminate vertex layout')
            for v in lamp.data.vertices:
                p=matrix@v.co;v.co=inverse@(p-ns[v.index%len(chart)]*.0035)
            lamp['aperture_samples']=[c for v in list(lamp.data.vertices)[:len(chart)] for c in matrix@v.co]
            lamp['opening_recess_m']=-.0005
            continue

        for v in lamp.data.vertices:
            p=matrix@v.co;_,n=surface_uv(p,surface);v.co=inverse@(p-n*recess)
        raw=list(lamp['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];moved=[]
        actual=KDTree(len(lamp.data.vertices))
        for i,v in enumerate(lamp.data.vertices):actual.insert(matrix@v.co,i)
        actual.balance()
        for p in guides:
            _,n=surface_uv(p,surface);moved.append(actual.find(p-n*recess)[0].copy())
        lamp['aperture_samples']=[c for p in moved for c in p];lamp['opening_recess_m']=recess-.004
