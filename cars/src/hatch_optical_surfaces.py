"""Smooth molded lamp shells on an injective physical perspective chart.

The old parameter-chart disk could make reversed chords in world space. The
outer shape follows the accepted evaluated parent and physical cut outline.
The radial recess avoids a folded normal-offset shell at the body crease;
outer and inner normal fields remain separate across the laminate gauge.
"""
import math
import bpy
import numpy as np
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt,convex_hull_2d
_canonical_uv=None


def normal(p):
    from hatch_reference_surface import field
    return field().nearest_normal(p)


def on_section(u,v,sign,with_normal=False):
    from hatch_reference_surface import field
    direction=Vector((sign,u,v)).normalized();origin=Vector((0,-1.30,.43))
    result=field()(origin,direction)
    if result is None:raise ValueError('Physical optical ray missed the accepted parent')
    p,n,_=result
    return (p-direction*.0078,n) if with_normal else p-direction*.0078


def rebuild(cover,high=False):
    """Retain the old physical cut perimeter; regularize the shell inside it."""
    me=cover.data;count=cover['lens_outer_faces'];matrix=cover.matrix_world;sign=1 if cover.name.endswith('1') and not cover.name.endswith('-1') else -1
    global _canonical_uv
    if _canonical_uv is None:
        # Both original optical molds use one symmetric contour. Source CDT
        # roundoff had given the two sides different near-collinear tip fans.
        reference=bpy.data.objects.get('Headlamp opening-1',cover);rm=reference.data;edges0={}
        for face in rm.polygons[:reference['lens_outer_faces']]:
            for a,b in zip(face.vertices,list(face.vertices[1:])+[face.vertices[0]]):
                key=tuple(sorted((a,b)));edges0[key]=edges0.get(key,0)+1
        ids=sorted({i for e,c in edges0.items() if c==1 for i in e});points=[]
        for i in ids:
            p=reference.matrix_world@rm.vertices[i].co;points.append(Vector(((p.y+1.30)/abs(p.x),(p.z-.43)/abs(p.x))))
        hull=[points[i] for i in convex_hull_2d(points)]
        changed=True
        while changed and len(hull)>5:
            changed=False
            for i,p in enumerate(hull):
                a,b=hull[i-1],hull[(i+1)%len(hull)];edge=b-a;t=max(0,min(1,(p-a).dot(edge)/max(edge.length_squared,1e-12)))
                if (p-a-edge*t).length<.0015:
                    hull.pop(i);changed=True;break
        _canonical_uv=[tuple(q) for q in hull]
    uv=[Vector(q) for q in _canonical_uv];boundary=list(range(len(uv)));edges=[(i,(i+1)%len(uv)) for i in range(len(uv))]
    def edge_distance(q):
        distances=[]
        for a,b in edges:
            a,b=uv[a],uv[b];d=b-a;t=max(0,min(1,(q-a).dot(d)/max(d.length_squared,1e-12)));distances.append((q-a-d*t).length)
        return min(distances)
    # Interior samples in a perspective chart looking out from inside the
    # convex mold. Unlike angle/absolute-height, this chart stays transverse
    # to both the face and hood ends of the shell.
    u0,u1=min(p.x for p in uv),max(p.x for p in uv);z0,z1=min(p.y for p in uv),max(p.y for p in uv)
    # Smooth glass has no source-only relief: use the same physical chords
    # in both densities, with continuous analytical normals on each.
    step=.050
    for j in range(1,math.ceil((z1-z0)/step)):
        z=z0+j*step
        for k in range(1,math.ceil((u1-u0)/step)):
            q=Vector((u0+k*step,z))
            if edge_distance(q)>.005:uv.append(q)
    coords,_,faces,*_=delaunay_2d_cdt(uv,edges,[],1,1e-7)
    used=sorted({i for f in faces for i in f});remap={v:i for i,v in enumerate(used)}
    coords=[coords[i] for i in used];faces=[tuple(remap[i] for i in f) for f in faces]
    # The optical mold bridges the stamping's tight draw line. Fit a smooth
    # radial patch in this physical chart instead of inheriting its crease.
    # Anchors and fit are independent of game/high tessellation density.
    anchor=list(uv[:len(boundary)])
    def inside(q):
        crossings=0
        for a,b in edges:
            a,b=uv[a],uv[b]
            if (a.y>q.y)!=(b.y>q.y) and q.x<(b.x-a.x)*(q.y-a.y)/(b.y-a.y)+a.x:crossings+=1
        return crossings%2==1
    for j in range(1,30):
        for k in range(1,60):
            q=Vector((u0+(u1-u0)*k/60,z0+(z1-z0)*j/30))
            if inside(q):anchor.append(q)
    origin=Vector((0,-1.30,.43));du=u1-u0;dv=z1-z0
    terms=[(i,j) for i in range(4) for j in range(4-i)]
    def basis(u,v):
        x=2*(u-u0)/du-1;y=2*(v-z0)/dv-1
        return np.array([x**i*y**j for i,j in terms])
    values=np.array([(on_section(q.x,q.y,sign)-origin).length for q in anchor])
    rows=np.array([basis(q.x,q.y) for q in anchor]);penalty=np.diag([0 if i+j<2 else 1e-5 for i,j in terms])
    coeff=np.linalg.solve(rows.T@rows+penalty,rows.T@values)
    residual=rows@coeff-values
    # The lens remains behind the cut stamping at every fit anchor. This is
    # a geometrical seating constraint, not a render-only normal correction.
    recess=max(0,float(residual.max())+.001)
    def mold(u,v):
        direction=Vector((sign,u,v)).normalized();radius=float(np.dot(basis(u,v),coeff))-recess
        return origin+direction*radius
    def mold_normal(u,v):
        x=2*(u-u0)/du-1;y=2*(v-z0)/dv-1
        radius=float(np.dot(basis(u,v),coeff))-recess
        ru=sum(c*i*x**(i-1)*y**j for c,(i,j) in zip(coeff,terms) if i)*2/du
        rv=sum(c*j*x**i*y**(j-1) for c,(i,j) in zip(coeff,terms) if j)*2/dv
        length=math.sqrt(1+u*u+v*v);inv=1/length;cube=inv**3
        a=(ru*sign*inv-radius*sign*u*cube,ru*u*inv+radius*(inv-u*u*cube),ru*v*inv-radius*v*u*cube)
        c=(rv*sign*inv-radius*sign*v*cube,rv*u*inv-radius*u*v*cube,rv*v*inv+radius*(inv-v*v*cube))
        # Subtract/differentiate in doubles, then pack the unit vector once.
        return Vector((a[1]*c[2]-a[2]*c[1],a[2]*c[0]-a[0]*c[2],a[0]*c[1]-a[1]*c[0])).normalized()*sign
    faces=list({tuple(sorted(f)):tuple(f) for f in faces}.values())
    if any(len(f)!=3 for f in faces):raise ValueError('Optical chart must contain triangles')
    initial=[mold(q.x,q.y) for q in coords]
    if sum((initial[f[1]]-initial[f[0]]).cross(initial[f[2]]-initial[f[0]]).dot(mold_normal(*(sum((coords[i] for i in f),Vector((0,0)))/3))) for f in faces)<0:faces=[tuple(reversed(f)) for f in faces]
    # Resolve chord error on the actual smooth mold, including skinny tip
    # triangles. A 2D disk alone does not guarantee physically fair chords.
    refinement=[]
    for iteration in range(10):
        ps=[mold(q.x,q.y) for q in coords];normals=[mold_normal(q.x,q.y) for q in coords];selected=set();worst=0
        for f in faces:
            a,b,c=[ps[i] for i in f];n=(b-a).cross(c-a).normalized();shade=sum((normals[i] for i in f),Vector()).normalized()
            angle=math.degrees(n.angle(shade));worst=max(worst,angle)
            if angle>25:
                edge=max([(f[i],f[(i+1)%3]) for i in range(3)],key=lambda e:(ps[e[0]]-ps[e[1]]).length_squared)
                selected.add(tuple(sorted(edge)))
        refinement.append(dict(iteration=iteration,triangles=len(faces),maximum_angle_deg=worst,split_edges=len(selected)))
        if not selected:break
        midpoint={}
        for a,b in sorted(selected):
            midpoint[(a,b)]=len(coords);coords.append((coords[a]+coords[b])/2)
        refined=[]
        for f in faces:
            mids=[midpoint.get(tuple(sorted((f[i],f[(i+1)%3])))) for i in range(3)];number=sum(i is not None for i in mids)
            if number==0:refined.append(f)
            elif number==1:
                i=next(i for i,m in enumerate(mids) if m is not None);a,b,c=f[i],f[(i+1)%3],f[(i+2)%3];m=mids[i]
                refined.extend([(a,m,c),(m,b,c)])
            elif number==2:
                i=next(i for i,m in enumerate(mids) if m is None);a,b,c=f[i],f[(i+1)%3],f[(i+2)%3];bc,ca=mids[(i+1)%3],mids[(i+2)%3]
                refined.extend([(a,b,bc),(a,bc,ca),(ca,bc,c)])
            else:
                a,b,c=f;ab,bc,ca=mids;refined.extend([(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)])
        faces=refined
    ps=[mold(q.x,q.y) for q in coords];normals=[mold_normal(q.x,q.y) for q in coords]
    cover['optical_refinement']=str(refinement)

    cover['optical_fit_max_error_m']=float(np.max(np.abs(residual)));cover['optical_fit_seating_recess_m']=recess
    # Winding chosen once in the injective chart, never independently flipped.
    if sum((ps[f[1]]-ps[f[0]]).cross(ps[f[2]]-ps[f[0]]).dot(normals[f[0]]) for f in faces)<0:faces=[tuple(reversed(f)) for f in faces]
    num=len(ps);outer=len(faces);es={}
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):es.setdefault(tuple(sorted((a,b))),[]).append((a,b))
    closed=faces+[tuple(i+num for i in reversed(f)) for f in faces]
    closed += [(b,a,a+num,b+num) for rows in es.values() if len(rows)==1 for a,b in rows]
    gauge=.0015;back=[p-n*gauge for p,n in zip(ps,normals)];inverse=matrix.inverted()
    mesh=bpy.data.meshes.new('H120 physical-chart molded lens');mesh.from_pydata([inverse@p for p in ps+back],[],closed);mesh.update()
    for m in me.materials:mesh.materials.append(m)
    cover.data=mesh;nm=matrix.to_3x3().transposed();custom=[]
    for f in mesh.polygons:
        f.use_smooth=f.index<2*outer
        for li in f.loop_indices:
            vi=mesh.loops[li].vertex_index
            custom.append(nm@(normals[vi%num]*(1 if f.index<outer else -1)) if f.index<2*outer else f.normal)
    mesh.normals_split_custom_set(custom);cover['lens_outer_faces']=outer
    cover['physical_lens_chart']=True;cover['sheet_gauge_m']=gauge
    for label,fraction in [('lower',.18),('upper',.82)]:
        path=[]
        for k in range(16 if not high else 32):
            theta=u0+(u1-u0)*(.025+.95*k/(15 if not high else 31));cuts=[]
            for a,b in edges:
                a,b=uv[a],uv[b]
                if min(a.x,b.x)<=theta<=max(a.x,b.x) and abs(a.x-b.x)>1e-9:
                    cuts.append(a.y+(b.y-a.y)*(theta-a.x)/(b.x-a.x))
            if len(cuts)<2:continue
            z=min(cuts)+(max(cuts)-min(cuts))*fraction
            p=mold(theta,z);n=mold_normal(theta,z);path.append(p-n*.012)
        cover['molded_guide_'+label]=[v for p in path for v in p]

    raw=list(cover['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    projected=[mold((p.y+1.30)/abs(p.x),(p.z-.43)/abs(p.x)) for p in guides]
    cover['aperture_samples']=[v for p in projected for v in p]
    if me.users==0:bpy.data.meshes.remove(me)
    worst=max(math.degrees(f.normal.angle(sum((mesh.corner_normals[i].vector for i in f.loop_indices),Vector()).normalized())) for f in mesh.polygons[:outer])
    cover['optical_normal_mismatch_max_deg']=worst
    print('H120_PHYSICAL_LENS',cover.name,'outer triangles',outer,'vertices',num,'max normal disagreement',worst,'fit error',float(np.max(np.abs(residual))),'extra recess',recess,flush=True)
    if worst>80:raise ValueError('Unresolved physical lens chord: '+cover.name)
