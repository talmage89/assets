"""S240 molded inserts: flush lips, open hexagonal webs and closed beds.

The H120's recessed-bed/open-web method, with a distinct hexagonal pattern.
All coordinates come from the sedan's existing manufactured aperture mouths;
the accepted painted stamping, lamp cuts and lower profile are retained.
"""
import math
import bpy,bmesh
import numpy as np
from mathutils import Vector
from kit import model as G


def crown_cover(cover,depth=.0015):
    """Refine the true convex optical die, retaining its fitting perimeter.

    Refracting surfaces need chord normals close to the limit field. A merely
    positive dot product still allowed eleven-degree mismatches and torn card
    reflections. A convex transverse crown avoids the flat ruled cover.
    """
    from sedan_optical_surface import rebuild
    rebuild(cover,None,bpy.context.scene['quality']=='high',crown=depth,normal_angle_limit=3)
    cover['s240_compound_optic_crown']=depth


def optical_border(cover):
    """Physical distance to the true swept rim, shared by both laminate sides."""
    me=cover.data;matrix=cover.matrix_world;number=len(me.vertices)//2;edges={}
    for face in me.polygons[:cover['lens_outer_faces']]:
        for a,c in zip(face.vertices,list(face.vertices[1:])+[face.vertices[0]]):
            key=tuple(sorted((a,c)));edges[key]=edges.get(key,0)+1
    points=[matrix@v.co for v in me.vertices[:number]]
    segments=[(points[a],points[c]) for (a,c),num in edges.items() if num==1]
    def distance(p,a,c):
        d=c-a;t=max(0,min(1,(p-a).dot(d)/max(d.length_squared,1e-15)))
        return (p-a-d*t).length
    values=[min(distance(p,a,c) for a,c in segments) for p in points]
    attr=me.attributes.get('S240LensEdgeDistance') or me.attributes.new('S240LensEdgeDistance','FLOAT','POINT')
    attr.data.foreach_set('value',values+values)


def mouth(blank):
    raw=list(blank['well_mouth_samples'])
    return [Vector(raw[i:i+3]) for i in range(0,len(raw),3)]


def painted_skin():
    """Actual outer triangles and their gauges, excluding reverse sheets."""
    from mathutils.bvhtree import BVHTree
    points=[];faces=[];gauges=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('part_category') not in ['body','fascia']:continue
        roles=ob.data.attributes.get('sheet_role')
        if roles is None:continue
        start=len(points);points += [ob.matrix_world@v.co for v in ob.data.vertices]
        ob.data.calc_loop_triangles()
        for t in ob.data.loop_triangles:
            if roles.data[t.polygon_index].value:continue
            faces.append(tuple(start+i for i in t.vertices));gauges.append(.003 if ob.get('part_category')=='fascia' else .0009)
    return BVHTree.FromPolygons(points,faces,all_triangles=True),gauges


def die(points):
    """Mirror-symmetric fair die, independent of the pocket's game triangles."""
    z0=min(p.z for p in points);dz=max(p.z for p in points)-z0
    def basis(x,z):
        t=(z-z0)/dz
        # The perimeter does not constrain interior cubic modes. Those modes
        # bowed the grille centre 250 mm behind its fitted rim. A quadratic
        # rake and transverse bow retain the real molding without ringing.
        return [1,t,x*x,t*t,x*x*t]
    A=np.array([basis(p.x,p.z) for p in points])
    coeff=np.linalg.lstsq(A,np.array([p.y for p in points]),rcond=None)[0]
    return lambda x,z:float(np.dot(basis(x,max(z0,min(z0+dz,z))),coeff))


def slot_web(b,name,points,cols,rows,bar,hexagonal=False):
    """One closed perforated molding, with constant-width connected webs.

    A common constrained chart joins staggered hexagonal holes (upper) or
    narrow slots (lower). The continuous die supplies front normals; flat
    cell-by-cell normals would turn studio reflections into shiny fragments.
    """
    from mathutils.geometry import delaunay_2d_cdt
    zlo=min(p.z for p in points)+.008;zhi=max(p.z for p in points)-.008;f=die(points)
    def limits(z):
        cuts=[a.x+(c.x-a.x)*(z-a.z)/(c.z-a.z) for a,c in zip(points,points[1:]+points[:1]) if min(a.z,c.z)<=z<=max(a.z,c.z) and abs(a.z-c.z)>1e-8]
        return min(abs(min(cuts)),abs(max(cuts)))-.008
    boundary=[Vector((-1+2*i/cols,0)) for i in range(cols+1)]
    boundary += [Vector((1,j/rows)) for j in range(1,rows+1)]
    boundary += [Vector((1-2*i/cols,1)) for i in range(1,cols+1)]
    boundary += [Vector((-1,1-j/rows)) for j in range(1,rows)]
    holes=[]
    for i in range(cols):
        for j in range(rows):
            if hexagonal:
                w=2/(.75*cols+.25);h=1/(rows+.5);cx=-1+w/2+.75*w*i;cy=(j+.5+.5*(i%2))*h
                du=bar/limits(zlo+(zhi-zlo)*cy);dv=bar/(zhi-zlo)
                outer=[(-w/2,0),(-w/4,-h/2),(w/4,-h/2),(w/2,0),(w/4,h/2),(-w/4,h/2)]
                hole=[Vector((cx+u*(1-2*du/w),cy+v*(1-2*dv/h))) for u,v in outer]
            else:
                u0=-1+2*i/cols;u1=-1+2*(i+1)/cols;v0=j/rows;v1=(j+1)/rows
                du=bar/limits(zlo+(zhi-zlo)*(v0+v1)/2);dv=bar/(zhi-zlo)
                hole=[Vector(q) for q in [(u0+du,v0+dv),(u1-du,v0+dv),(u1-du,v1-dv),(u0+du,v1-dv)]]
            holes.append(hole)
    coords=list(boundary);outline=list(range(len(boundary)));edges=list(zip(outline,outline[1:]+outline[:1]))
    for hole in holes:
        start=len(coords);coords+=hole;ids=list(range(start,len(coords)));edges+=list(zip(ids,ids[1:]+ids[:1]))
    coords,_,triangles,*_=delaunay_2d_cdt(coords,edges,[outline],1,1e-8)
    def inside(q,polygon):
        return sum((a.y>q.y)!=(c.y>q.y) and q.x<(c.x-a.x)*(q.y-a.y)/(c.y-a.y)+a.x for a,c in zip(polygon,polygon[1:]+polygon[:1]))%2==1
    triangles=[t for t in triangles if not any(inside(sum((coords[i] for i in t),Vector((0,0)))/3,hole) for hole in holes)]
    used=sorted({i for t in triangles for i in t});remap={vi:i for i,vi in enumerate(used)};coords=[coords[i] for i in used];triangles=[tuple(remap[i] for i in t) for t in triangles]
    vertices=[];normals=[]
    for u,v in coords:
        z=zlo+(zhi-zlo)*v;x=limits(z)*u;vertices.append(Vector((x,f(x,z)+.021,z)))
        h=1e-5;normals.append(Vector(((f(x+h,z)-f(x-h,z))/(2*h),-1,(f(x,z+h)-f(x,z-h))/(2*h))).normalized())
    if sum((vertices[t[1]]-vertices[t[0]]).cross(vertices[t[2]]-vertices[t[0]]).dot(normals[t[0]]) for t in triangles)<0:triangles=[tuple(reversed(t)) for t in triangles]
    n=len(vertices);count=len(triangles);edge_uses={}
    for t in triangles:
        for a,c in zip(t,t[1:]+t[:1]):edge_uses.setdefault(tuple(sorted((a,c))),[]).append((a,c))
    faces=triangles+([tuple(i+n for i in reversed(t)) for t in triangles] if b.high else [])
    back_end=2*count if b.high else count
    faces += [(c,a,a+n,c+n) for uses in edge_uses.values() if len(uses)==1 for a,c in uses]
    ob=G.mesh(name,vertices+[p+Vector((0,.004,0)) for p in vertices],faces,b.m['grille_bar']);custom=[]
    if sum(ob.data.polygons[i].normal.dot(normals[ob.data.polygons[i].vertices[0]]) for i in range(count))<0:
        for face in ob.data.polygons:face.flip()
        ob.data.update()
    for face in ob.data.polygons:
        face.use_smooth=face.index<back_end
        for li in face.loop_indices:
            vi=ob.data.loops[li].vertex_index
            custom.append(normals[vi%n]*(1 if face.index<count else -1) if face.index<back_end else face.normal.copy())
    ob.data.normals_split_custom_set(custom)
    if not b.high:
        ob['allow_boundary']=True;ob['boundary_reason']='Molded web rear hidden against the closed radiator bed; front and every hole/rim relief wall retained'
    if b.high:G.bevel(ob,.0007,2)
    b.add(ob,category='openings');ob['open_slot_web']=True;ob['slot_columns']=cols;ob['slot_rows']=rows
    return ob


def insert(b,blank):
    points=mouth(blank);f=die(points);count=len(points)
    # Replace the reflective box by a bowed, closed radiator shadow bed.
    # Preserve the part and its aperture properties for the construction gate.
    from mathutils.geometry import delaunay_2d_cdt
    center=sum(points,Vector())/count;outline=[]
    for i,p in enumerate(points):
        tangent=points[(i+1)%count]-points[i-1];out=Vector((tangent.z,0,-tangent.x)).normalized()
        if out.dot(p-center)<0:out.negate()
        q=p+out*.005;outline.append(Vector((q.x,q.z)))
    coords=list(outline);boundary=list(range(count))
    xlo,xhi=min(p.x for p in outline),max(p.x for p in outline)
    zlo,zhi=min(p.y for p in outline),max(p.y for p in outline)
    for j in range(1,4):
        for i in range(1,24):coords.append(Vector((xlo+(xhi-xlo)*i/24,zlo+(zhi-zlo)*j/4)))
    coords,_,faces,*_=delaunay_2d_cdt(coords,list(zip(boundary,boundary[1:]+boundary[:1])),[boundary],1,1e-8)
    used=sorted({i for face in faces for i in face});remap={vi:i for i,vi in enumerate(used)}
    coords=[coords[i] for i in used];faces=[tuple(remap[i] for i in face) for face in faces]
    bed=G.mesh('S240 cavity bed',[(p.x,f(p.x,p.y)+.078,p.y) for p in coords],faces,b.m['grille'])
    if sum(face.normal.y for face in bed.data.polygons)>0:
        for face in bed.data.polygons:face.flip()
        bed.data.update()
    sol=bed.modifiers.new('Closed cavity bed gauge','SOLIDIFY');sol.thickness=.003;sol.offset=-1;G.apply(bed)
    old=blank.data;blank.data=bed.data;blank.data.transform(blank.matrix_world.inverted());bpy.data.objects.remove(bed,do_unlink=True)
    if old.users==0:bpy.data.meshes.remove(old)
    for key in ['lens_outer_faces','outer_skin_faces']:
        if key in blank:del blank[key]
    # A small rounded molding bead behind the aperture, then a single inward
    # return to the shadow bed. No broad flat top can stand above the fascia.
    old=bpy.data.objects[blank.name+' molded return'];parent=old.parent
    bpy.data.objects.remove(old,do_unlink=True)
    center=sum(points,Vector())/count;rings=[]
    for width,depth in [(.004,.007),(.001,.009),(-.002,.014),(-.002,.078)]:
        ring=[]
        for i,p in enumerate(points):
            tangent=points[(i+1)%count]-points[i-1]
            out=Vector((tangent.z,0,-tangent.x)).normalized()
            if out.dot(p-center)<0:out.negate()
            q=p+out*width;q.y=p.y+depth;ring.append(q)
        rings.append(ring)
    ob=G.loft(blank.name+' molded return',rings,b.m['plastic'],caps=False)
    ob['allow_boundary']=True;ob['construction']='Flush 6 mm molded lip and continuous recessed return, hidden back bonded to closed bed'
    b.add(G.smooth(ob,40),parent,'openings')
    return points


def build(b):
    for ob in list(bpy.context.scene.objects):
        if ob.name.startswith(('Low wide grille opening cascade vane','Lower intake opening blade','S240 upper vertical slot grille','S240 upper hexagonal grille','S240 lower staggered slot intake','S240 sealed corner lamp mask','S240 corner lamp bonded seal','S240 corner pocket side return')):
            bpy.data.objects.remove(ob,do_unlink=True)
    upper=insert(b,bpy.data.objects['Low wide grille opening'])
    lower=insert(b,bpy.data.objects['Lower intake opening'])
    slot_web(b,'S240 upper hexagonal grille',upper,23,4,.0015,hexagonal=True)
    slot_web(b,'S240 lower staggered slot intake',lower,32,1,.0016)
    # The corner lamps are sealed cassettes with opaque black beds, rather
    # than a shiny compound pocket that reflects as broken silver foil.
    skin,gauges=painted_skin()
    for side in ['L','R']:
        ob=bpy.data.objects['DRL pocket '+side+' opening']
        ob.data.materials.clear();ob.data.materials.append(b.m['plastic'])
        G.smooth(ob,60)
        # A molded front blank seals the former open corner box. The light
        # guide is embedded into this face, with its rear half inside it.
        raw=list(ob['aperture_samples']);ps=[Vector(raw[i:i+3])+Vector((0,.003,0)) for i in range(0,len(raw),3)]
        nu,nv=ob['form_columns'],ob['form_rows']
        mask=G.mesh('S240 sealed corner lamp mask '+side,ps,
            [(j*nu+i,(j+1)*nu+i,(j+1)*nu+i+1,j*nu+i+1) for j in range(nv-1) for i in range(nu-1)],b.m['plastic'])
        if sum(f.normal.y for f in mask.data.polygons)>0:
            for face in mask.data.polygons:face.flip()
            mask.data.update()
        G.smooth(mask,70)
        if b.high:
            sol=mask.modifiers.new('Corner lamp mask gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;G.apply(mask)
        else:
            mask['allow_boundary']=True;mask['boundary_reason']='Molded front insert retained inside the closed corner pocket and its continuous return; concealed back omitted'
        b.add(mask,category='lamps')
        # Bridge the actual 2.25 mm aperture reveal. The former broad backing
        # fans protruded through the face; this narrow seal seats under the
        # measured steel instead of spanning across the whole pocket.
        ids=list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]
        rim=[ps[i] for i in ids];center=sum(rim,Vector())/len(rim);land=[]
        for i,p in enumerate(rim):
            t=rim[(i+1)%len(rim)]-rim[i-1];out=Vector((t.z,0,-t.x)).normalized()
            if out.dot(p-center)<0:out.negate()
            for distance in [.004,.006,.008,.010,.014,.020]:
                q=p+out*distance;hit,n,fi,_=skin.ray_cast(Vector((q.x,-4,q.z)),Vector((0,1,0)),4)
                if hit is not None and hit.y<-1.5:land.append(hit-n*(gauges[fi]+.0008));break
            else:
                # The outboard pocket wraps beyond the front projection.
                # Its mounting land is on the actual returning side wall.
                hit,n,fi,distance=skin.find_nearest(p+out*.006)
                if distance>.075:raise ValueError(('Corner lamp has no actual fascia seat',side,i,distance))
                land.append(hit-n*(gauges[fi]+.0008))
        seal=G.loft('S240 corner lamp bonded seal '+side,[rim,land],b.m['rubber'],caps=False)
        if b.high:
            sol=seal.modifiers.new('Corner gasket gauge','SOLIDIFY');sol.thickness=.001;sol.offset=-1;G.apply(seal)
        else:
            seal['allow_boundary']=True;seal['boundary_reason']='Thin molded gasket bonded between the sealed corner insert and actual fascia underside; hidden rear omitted'
        b.add(seal,category='lamps');seal['measured_seat_span_max_m']=max((p-q).length for p,q in zip(rim,land))
    # Short molded side returns finish the wrap at each corner pocket. The
    # joint centre is an authored construction datum; its support is measured
    # on the actual side skin. A front-facing gasket alone leaves this grazing
    # side ray open where the pocket turns around the nose.
    y,z=-2.095,.535
    for sign in [-1,1]:
        supports=[]
        for dy,dz in [(-.022,0),(.022,0),(0,-.022),(0,.022),(-.022,.022),(.022,-.022)]:
            hit=skin.ray_cast(Vector((sign*2,y+dy,z+dz)),Vector((-sign,0,0)),4)[0]
            if hit is not None and sign*hit.x>.78:supports.append(sign*hit.x)
        if not supports:raise ValueError('Corner pocket side return has no fascia support')
        x=min(supports)
        section=[(x-.0035,y-.022),(x-.014,y-.022),(x-.014,y+.022),(x-.0035,y+.022),
                 (x-.0035,y+.020),(x-.012,y+.020),(x-.012,y-.020),(x-.0035,y-.020)]
        ob=G.profile('S240 corner pocket side return '+str(sign),[(sign*xx,yy) for xx,yy in section],z-.022,z+.022,b.m['frame'],axis='Z')
        b.add(ob,category='lamps');ob['return_gauge_m']=.002;ob['measured_support_x_min_max_m']=[min(supports),max(supports)]


def seat_optical_backings(b):
    """Fit reveal closures behind the sealed lens, rather than across it.

    The generic 60 mm flange expansion crossed the long swept lamp cut.
    These are concealed opening returns, not any accepted painted panel.
    Subdivide only crossing triangles if a long chord still enters the mold.
    """
    from mathutils.bvhtree import BVHTree
    from sedan_exterior import optical_normal
    from sedan_surface_check import intersects
    # The four opening fans were a temporary reveal closure. They extended
    # through the front of the grille and corner lamps, producing comb teeth
    # and white shards. The fitted closed inserts now own those openings.
    # Retain the outer-perimeter return: it spans the full fascia height and
    # closes the accepted side joint. Its measured height distinguishes it
    # from the four shorter opening loops at both source densities.
    liners=[o for o in bpy.context.scene.objects if o.name.startswith('S240 inner aperture liner Front molded fascia ')]
    outer=max(liners,key=lambda o:max((o.matrix_world@v.co).z for v in o.data.vertices)-min((o.matrix_world@v.co).z for v in o.data.vertices))
    for ob in liners:
        if ob!=outer:
            print('S240_REPLACE_APERTURE_FAN',ob.name,flush=True)
            bpy.data.objects.remove(ob,do_unlink=True)
    for cover in [o for o in bpy.context.scene.objects if o.name.startswith('Headlamp opening')]:
        cassette_wall(b,cover)
        normal=optical_normal(cover);cover.data.calc_loop_triangles()
        ps=[cover.matrix_world@v.co for v in cover.data.vertices]
        fs=[tuple(t.vertices) for t in cover.data.loop_triangles if t.polygon_index<cover['lens_outer_faces']]
        tree=BVHTree.FromPolygons(ps,fs,all_triangles=True)
        for ob in list(bpy.context.scene.objects):
            if ob.type!='MESH' or not ob.name.startswith(('S240 inner aperture liner Hood outer','S240 inner aperture liner Front molded fascia','S240 inner aperture liner moving hem Hood outer')):continue
            inverse=ob.matrix_world.inverted();changed=0
            for iteration in range(8):
                for vertex in ob.data.vertices:
                    p=ob.matrix_world@vertex.co;hit,_,_,distance=tree.find_nearest(p)
                    if distance>.080:continue
                    n=normal(hit);depth=-(p-hit).dot(n)
                    target=.032
                    if depth<target:
                        vertex.co=inverse@(p-n*(target-depth));changed+=1
                ob.data.update();ob.data.calc_loop_triangles()
                qs=[ob.matrix_world@v.co for v in ob.data.vertices];ts=list(ob.data.loop_triangles)
                other=BVHTree.FromPolygons(qs,[tuple(t.vertices) for t in ts],all_triangles=True)
                crossings=[bi for ai,bi in tree.overlap(other) if intersects([ps[k] for k in fs[ai]],[qs[k] for k in ts[bi].vertices])]
                if not crossings:break
                indices={ts[i].polygon_index for i in crossings};bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table()
                edges={e for i in indices for e in bm.faces[i].edges}
                bmesh.ops.subdivide_edges(bm,edges=list(edges),cuts=1,use_grid_fill=True)
                bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
            else:raise ValueError(('Optical backing still crosses sealed lens',ob.name,len(crossings)))
            if changed:
                # The hidden return is matte molded plastic/inner steel;
                # geometric normals preserve its actual inward-facing folds.
                for face in ob.data.polygons:face.use_smooth=False
                ob.data.normals_split_custom_set([f.normal.copy() for f in ob.data.polygons for _ in f.loop_indices])
                ob['optical_backing_seated_vertices']=changed
                ob['optical_backing_crossings_after']=len(crossings)
                print('S240_OPTICAL_BACKING',ob.name,changed,'seated vertices; crossings',len(crossings),flush=True)
    optical_joint_returns(b)


def optical_joint_returns(b):
    """A folded 2 mm return closes the lamp/fender/fascia three-way joint."""
    from sedan_apertures import FRONT_PARTING
    from sedan_check import mesh_tree
    skin=mesh_tree([o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('part_category') in ['body','doors','fascia']])
    z=.708;y=FRONT_PARTING(z)
    for sign in [-1,1]:
        support=[]
        for dz in [-.018,0,.018]:
            for dy in [-.025,.025]:
                p=skin.ray_cast(Vector((sign*2,y+dy,z+dz)),Vector((-sign,0,0)),3)[0]
                if p is not None and sign*p.x>.78:support.append(sign*p.x)
        if not support:raise ValueError('Missing lower optical joint support')
        x=min(support)
        section=[(x-.0035,y-.025),(x-.014,y-.025),(x-.014,y+.025),(x-.0035,y+.025),
                 (x-.0035,y+.023),(x-.012,y+.023),(x-.012,y-.023),(x-.0035,y-.023)]
        ob=G.profile('S240 optical joint return Headlamp '+str(sign),[(sign*xx,yy) for xx,yy in section],z-.018,z+.018,b.m['frame'],axis='Z')
        b.add(ob,category='lamps');ob['painted_support_x_min_max_m']=[min(support),max(support)];ob['return_gauge_m']=.002
        # Translate the rigid folded channel behind the actual wrapped lens;
        # preserve its gauge rather than collapsing individual front vertices.
        from sedan_exterior import optical_normal
        from mathutils.bvhtree import BVHTree
        cover=bpy.data.objects['Headlamp opening'+str(sign)];normal=optical_normal(cover);cover.data.calc_loop_triangles()
        ps=[cover.matrix_world@v.co for v in cover.data.vertices]
        fs=[tuple(t.vertices) for t in cover.data.loop_triangles if t.polygon_index<cover['lens_outer_faces']]
        tree=BVHTree.FromPolygons(ps,fs,all_triangles=True);translation=0
        for _ in range(8):
            probes=[ob.matrix_world@v.co for v in ob.data.vertices]
            probes += [ob.matrix_world@f.center for f in ob.data.polygons]
            shift=0
            for p in probes:
                hit,_,_,distance=tree.find_nearest(p);n=normal(hit)
                if distance<.080 and sign*n.x>.25:shift=max(shift,((p-hit).dot(n)+.008)/(sign*n.x))
            if shift<1e-7:break
            delta=ob.matrix_world.inverted().to_3x3()@Vector((-sign*(shift+.0001),0,0))
            for v in ob.data.vertices:v.co+=delta
            ob.data.update();translation+=shift+.0001
        ob['measured_optical_seating_translation_x_m']=-sign*translation


def cassette_wall(b,cover):
    """A real closed-gauge bucket and bonded reveal seal at the inner lens.

    Keep every boundary station. Reducing that loop, or moving its whole rim
    18 mm behind the cover, leaves an escape path at oblique gallery cameras.
    The 3 mm opaque seal overlaps the transparent lens from behind.
    """
    from sedan_exterior import perimeter,optical_normal
    from sedan_optical_surface import chart,ORIGIN
    from mathutils.bvhtree import BVHTree
    for stem in ['S240 bonded lens seal ','S240 molded optical mask ','S240 projector shroud ']:
        old=bpy.data.objects.get(stem+cover.name)
        if old:bpy.data.objects.remove(old,do_unlink=True)
    boundary=perimeter(cover,0);normal=optical_normal(cover)
    # At the hooked outer tip the global center can lie outside the strip's
    # local half-plane. Use incident outer faces to distinguish inside/outside.
    from mathutils.kdtree import KDTree
    cover.data.calc_loop_triangles();cp=[cover.matrix_world@v.co for v in cover.data.vertices];into={}
    for tri in cover.data.loop_triangles:
        if tri.polygon_index>=cover['lens_outer_faces']:continue
        c=sum((cp[i] for i in tri.vertices),Vector())/3
        for i in tri.vertices:into[i]=into.get(i,Vector())+(c-cp[i])
    lookup=KDTree(len(into))
    for i in into:lookup.insert(cp[i],i)
    lookup.balance();front=[];back=[];flange=[];seal_inner=[]
    # The cover is more upright than the steel draw. A proper reveal joins
    # those two surfaces; a fixed 8 mm lip left a deep, exposed optical well.
    # Follow the opening's physical chart to the actual cut skin, avoiding a
    # nearest-point jump to the opposite side of its narrow wrapped tip.
    skin_points=[];skin_faces=[]
    for panel in bpy.context.scene.objects:
        if panel.type!='MESH' or panel.get('part_category') not in ['body','fascia']:continue
        roles=panel.data.attributes.get('sheet_role')
        if roles is None:continue
        start=len(skin_points);skin_points += [panel.matrix_world@v.co for v in panel.data.vertices]
        panel.data.calc_loop_triangles()
        skin_faces += [tuple(start+i for i in t.vertices) for t in panel.data.loop_triangles if roles.data[t.polygon_index].value==0]
    skin=BVHTree.FromPolygons(skin_points,skin_faces,all_triangles=True)
    sign=1 if boundary[0].x>0 else -1
    for i,p in enumerate(boundary):
        n=normal(p);t=boundary[(i+1)%len(boundary)]-boundary[i-1];out=t.cross(n).normalized()
        _,vi,distance=lookup.find(p)
        if distance>1e-6:raise ValueError('Cassette boundary lost its optical vertex')
        if out.dot(into[vi])>0:out.negate()
        front.append(p-out*.003-n*.0025);back.append(p-n*.060)
        q=chart(p,True).to_2d();qt=(chart(boundary[(i+1)%len(boundary)],True)-chart(boundary[i-1],True)).to_2d()
        qo=Vector((qt.y,-qt.x)).normalized()
        if qo.dot(chart(p+out*.001,True).to_2d()-q)<0:qo.negate()
        for step in range(3,46):
            qq=q+qo*(step*.002);direction=Vector((sign,qq.x,qq.y)).normalized()
            hit,sn,_,_=skin.ray_cast(ORIGIN,direction,3)
            if hit is not None and hit.y<-1.5 and .4<abs(hit.x)<1.0 and hit.z>.5:
                # One additional 2 mm chart step gives a measured overlap.
                qq=q+qo*((step+1)*.002);direction=Vector((sign,qq.x,qq.y)).normalized()
                hit2,sn2,_,_=skin.ray_cast(ORIGIN,direction,3)
                if hit2 is not None:hit,sn=hit2,sn2
                flange.append(hit+sn*.0008);break
        else:raise ValueError(('No actual steel seat for lamp reveal',cover.name,i,list(p)))
        seal_inner.append(p+out*.0015-n*.003)
    old=bpy.data.objects['S240 optical housing '+cover.name];parent=old.parent;bpy.data.objects.remove(old,do_unlink=True)
    ob=G.loft('S240 optical housing '+cover.name,[front,back],b.m['plastic'],caps=False)
    sol=ob.modifiers.new('Injection molded bucket gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    b.add(ob,parent,'lamps');ob['sealed_rim_stations']=len(boundary);ob['wall_gauge_m']=.0015
    seal=G.loft('S240 bonded lens seal '+cover.name,[seal_inner,flange],b.m['rubber'],caps=False)
    if b.high:
        sol=seal.modifiers.new('Bonded seal gauge','SOLIDIFY');sol.thickness=.001;sol.offset=-1;sol.use_even_offset=False;G.apply(seal)
    else:
        seal['allow_boundary']=True;seal['boundary_reason']='Thin bonded reveal seal; hidden back supported between the closed bucket, lens and fascia mounting land'
    b.add(seal,parent,'lamps')
    if 'casing_flange_max_span_m' in cover:del cover['casing_flange_max_span_m']
    cover['casing_mounting_curve_vertices']=len(boundary)
    cover['opaque_rim_measured_maximum_span_m']=max((a-c).length for a,c in zip(front,flange))
    optical_bezel(b,cover,boundary,normal,parent)


def optical_bezel(b,cover,boundary,normal,parent):
    """Molded black mask behind the guides, with a real projector aperture.

    A deep empty bucket alone leaves an oblique ray grazing the swept cover
    and escaping through it again. This fitted inner mask is real optical
    construction; only the projector's metalized bowl remains exposed.
    """
    from mathutils.bvhtree import BVHTree
    from mathutils.geometry import delaunay_2d_cdt,barycentric_transform
    from sedan_optical_surface import chart
    me=cover.data;me.calc_loop_triangles();ps=[cover.matrix_world@v.co for v in me.vertices]
    fs=[tuple(t.vertices) for t in me.loop_triangles if t.polygon_index<cover['lens_outer_faces']]
    charts=[chart(p,True) for p in ps];tree=BVHTree.FromPolygons(charts,fs,all_triangles=True)
    outer=BVHTree.FromPolygons(ps,fs,all_triangles=True)
    def sample(q,depth):
        hit,_,fi,_=tree.find_nearest(Vector((q.x,q.y,0)));a,c,d=fs[fi]
        p=barycentric_transform(hit,charts[a],charts[c],charts[d],ps[a],ps[c],ps[d])
        return p-normal(p)*depth
    rim=[chart(p,True).to_2d() for p in boundary];coords=list(rim);outline=list(range(len(rim)))
    edges=list(zip(outline,outline[1:]+outline[:1]))
    # The actual existing projector axis determines its opening, rather than
    # a decorative circle at an assumed point on the cover.
    optic=bpy.data.objects['S240 low optic '+cover.name]
    optic_points=[optic.matrix_world@v.co for v in optic.data.vertices]
    _,axes=np.linalg.eigh(np.cov(np.array([tuple(p) for p in optic_points]).T))
    axis=Vector(axes[:,0]).normalized()
    if axis.y>0:axis.negate()
    center=max(optic_points,key=lambda p:p.dot(axis))
    u=axis.cross(Vector((0,0,1))).normalized();v=u.cross(axis).normalized()
    hole=[]
    for i in range(24):
        p=center+u*(.031*math.cos(math.tau*i/24))+v*(.031*math.sin(math.tau*i/24))-axis*.030
        hit,_,_,_=outer.ray_cast(p,axis,.20)
        if hit is None:raise ValueError(('Projector aperture misses optical mold',cover.name,i))
        hole.append(chart(hit,True).to_2d())
    start=len(coords);coords+=hole;hole_ids=list(range(start,len(coords)));edges+=list(zip(hole_ids,hole_ids[1:]+hole_ids[:1]))
    raw=list(cover['aperture_samples']);grid=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)];nu=cover['form_columns'];nv=cover['form_rows']
    coords += [chart(grid[j*nu+i],True).to_2d() for j in range(1,nv-1) for i in range(1,nu-1,2)]
    coords,_,faces,*_=delaunay_2d_cdt(coords,edges,[outline],1,1e-8)
    def inside(q,polygon):
        crossings=0
        for a,c in zip(polygon,polygon[1:]+polygon[:1]):
            if (a.y>q.y)!=(c.y>q.y) and q.x<(c.x-a.x)*(q.y-a.y)/(c.y-a.y)+a.x:crossings+=1
        return crossings%2==1
    faces=[f for f in faces if not inside(sum((coords[i] for i in f),Vector((0,0)))/len(f),hole)]
    used=sorted({i for f in faces for i in f});remap={vi:i for i,vi in enumerate(used)}
    positions=[sample(coords[i],.012) for i in used];faces=[tuple(remap[i] for i in f) for f in faces]
    if sum((positions[f[1]]-positions[f[0]]).cross(positions[f[2]]-positions[f[0]]).dot(normal(positions[f[0]])) for f in faces)<0:faces=[tuple(reversed(f)) for f in faces]
    ob=G.mesh('S240 molded optical mask '+cover.name,positions,faces,b.m['plastic'])
    if b.high:
        sol=ob.modifiers.new('Optical mask gauge','SOLIDIFY');sol.thickness=.0015;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    else:
        ob['allow_boundary']=True;ob['boundary_reason']='Thin molded optical mask supported inside the closed bucket; hidden rear omitted'
    b.add(ob,parent,'lamps')
    # Close the real annulus from the mask to the metalized projector rim.
    from sedan_check import mesh_tree
    metal=bpy.data.objects['S240 low reflector '+cover.name];metal_tree=mesh_tree([metal])
    front=[sample(q,.012) for q in hole];back=[]
    for i in range(len(hole)):
        p=center-axis*.007+u*(.02912*math.cos(math.tau*i/len(hole)))+v*(.02912*math.sin(math.tau*i/len(hole)))
        back.append(metal_tree.find_nearest(p)[0])
    shroud=G.loft('S240 projector shroud '+cover.name,[front,back],b.m['plastic'],caps=False)
    if b.high:
        sol=shroud.modifiers.new('Projector shroud gauge','SOLIDIFY');sol.thickness=.001;sol.offset=-1;sol.use_even_offset=False;G.apply(shroud)
    else:
        shroud['allow_boundary']=True;shroud['boundary_reason']='Molded aperture return bonded between the mask and actual reflector lip; concealed back omitted'
    b.add(shroud,parent,'lamps')
    if not b.high:
        # The shadow bed is invisible behind the fitted mask. Its exact rim
        # and a few inner stations suffice; put triangles into the sealed lip.
        qs=list(rim)+[chart(grid[(nv//2)*nu+i],True).to_2d() for i in range(2,nu-2,3)]
        qs,_,back_faces,*_=delaunay_2d_cdt(qs,list(zip(outline,outline[1:]+outline[:1])),[outline],1,1e-8)
        used=sorted({i for f in back_faces for i in f});remap={vi:i for i,vi in enumerate(used)}
        old=bpy.data.objects['S240 optical back '+cover.name]
        bed=G.mesh('S240 economy optical bed',[sample(qs[i],.060) for i in used],[tuple(remap[i] for i in f) for f in back_faces],b.m['plastic'])
        old.data=bed.data;old.data.transform(old.matrix_world.inverted());bpy.data.objects.remove(bed,do_unlink=True)


def hidden_normals():
    """Freeze hidden molding chords before assigning their geometric normals.

    A nonplanar quad's averaged normal can oppose one of its final triangles.
    Preserve all clean smoothing fans and the optical cover's analytic field.
    """
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.get('lens_outer_faces') is not None:continue
        if ob.get('part_category') not in ['lamps','openings']:continue
        me=ob.data;me.calc_loop_triangles()
        bad=any(min(t.normal.dot(me.corner_normals[i].vector) for i in t.loops)<=0 for t in me.loop_triangles)
        if not bad:continue
        mod=ob.modifiers.new('Physical molding triangles','TRIANGULATE');mod.keep_custom_normals=True;G.apply(ob)
        me=ob.data;custom=[n.vector.copy() for n in me.corner_normals];repairs=0
        for face in me.polygons:
            if min(face.normal.dot(custom[i]) for i in face.loop_indices)>0:continue
            face.use_smooth=False;repairs+=1
            for li in face.loop_indices:custom[li]=face.normal.copy()
        me.normals_split_custom_set(custom)
        print('S240_MOLD_NORMALS',ob.name,repairs,'hidden triangle fans',flush=True)


def fair_molding_normals(radius=.070):
    """Fair the small cut-corner normal outliers on the molded nose.

    Area-weighted 70 mm neighborhoods retain the broad draw while preventing
    densely cut slivers from steering its reflection. Every position, cut,
    silhouette and triangle is held. One normal is shared at coincident points;
    it must remain in the positive hemisphere of every incident triangle.
    """
    from mathutils.kdtree import KDTree
    from sedan_upper_surface import ease
    ob=bpy.data.objects['Front molded fascia'];me=ob.data;roles=me.attributes['sheet_role']
    custom=[n.vector.copy() for n in me.corner_normals];groups={}
    for face in me.polygons:
        if roles.data[face.index].value:continue
        for li in face.loop_indices:
            p=me.vertices[me.loops[li].vertex_index].co;key=tuple(round(v,7) for v in p)
            row=groups.setdefault(key,dict(p=p.copy(),weight=0,n=Vector(),loops=[],faces=[]))
            area=face.area/3;row['weight']+=area;row['n']+=custom[li]*area
            row['loops'].append(li);row['faces'].append(face.normal.copy())
    rows=list(groups.values());tree=KDTree(len(rows))
    for i,row in enumerate(rows):row['n'].normalize();tree.insert(row['p'],i)
    tree.balance();changes=[];sigma=radius
    for row in rows:
        p=row['p'];w=ease(.40,.52,abs(p.x))*(1-ease(.81,.89,abs(p.x)))*ease(.49,.55,p.z)*(1-ease(.69,.75,p.z))
        if not w:continue
        n=Vector()
        for _,i,distance in tree.find_range(p,3*sigma):
            n+=rows[i]['n']*rows[i]['weight']*math.exp(-distance*distance/(2*sigma*sigma))
        n.normalize();n=row['n'].lerp(n,w).normalized()
        target=min(.03,.5*min(row['n'].dot(f) for f in row['faces']))
        for _ in range(24):
            if min(n.dot(f) for f in row['faces'])>=target:break
            n=n.lerp(row['n'],.5).normalized()
        else:raise ValueError('Molding normal leaves its geometric hemisphere')
        changes.append(math.degrees(n.angle(row['n'])))
        for li in row['loops']:custom[li]=n
    me.normals_split_custom_set(custom)
    from sedan_surface_normals import coalesce
    coalesce(ob)
    ob['front_reflection_fairing_radius_m']=sigma
    ob['front_reflection_fairing_max_correction_degrees']=max(changes,default=0)
    print('S240_FRONT_REFLECTION_FAIRING',len(changes),max(changes,default=0),flush=True)
