"""A symmetric optical mold and its single physical perspective cut chart.

Adapted from the hatch's physical optical mold and SUV's monotone radial guides.
The transparent cover bridges the stamping's draw; it never inherits a steel
crease. Body, fender and hood use the SAME injective physical chart for the cut.
"""
import math
import bpy
import numpy as np
from mathutils import Vector
from kit import model as G

ORIGIN=Vector((0,-1.30,.43))
REAR_ORIGIN=Vector((0,1.42,.60))


def chart(p,front=True):
    o=ORIGIN if front else REAR_ORIGIN
    return Vector(((p.y-o.y)/abs(p.x),(p.z-o.z)/abs(p.x),0))


def guides(b,sign,mat,tree,front=True):
    from sedan_body import hood_height
    from sedan_upper_surface import ease
    nu=33;nv=7;rows=[]
    for j in range(nv):
        row=[];v=j/(nv-1)
        for i in range(nu):
            u=i/(nu-1);theta=math.radians(28+34*u if front else 17+51*u)
            direction=Vector((math.sin(theta),(-1 if front else 1)*math.cos(theta),0))
            def hit(z):
                center=Vector((0,ORIGIN.y if front else REAR_ORIGIN.y,z));p,n,_,_=tree.ray_cast(center+direction*2,-direction,2)
                if p is None:raise ValueError(('Optical radial guide misses skin',u,z))
                p.x*=sign;n.x*=sign
                return p,n
            p,_=hit(.78 if front else .98)
            for _ in range(5):
                if front:top=hood_height(p.x,p.y)-.012
                else:
                    from sedan_upper_surface import height
                    top=height(p.x,p.y)-.014
                p,_=hit(top)
            gauge=(.075+.055*ease(0,.55,u))*(1-.83*ease(.78,1,u)) if front else (.055+.125*ease(0,.60,u))*(1-.87*ease(.80,1,u))
            p,n=hit(top-gauge*(1-v));row.append(p+n*.004)
        rows.append(row)
    anchors=[p for row in rows for p in row]
    if not b.high:
        target_u=25 if front else 33;target_v=4 if front else 5;resampled=[]
        for j in range(target_v):
            v=j*(nv-1)/(target_v-1);ja=min(nv-2,int(v));row=[]
            for i in range(target_u):
                u=i*(nu-1)/(target_u-1);ia=min(nu-2,int(u))
                row.append(rows[ja][ia].lerp(rows[ja][ia+1],u-ia).lerp(rows[ja+1][ia].lerp(rows[ja+1][ia+1],u-ia),v-ja))
            resampled.append(row)
        rows=resampled;nu=target_u;nv=target_v
    if front:groups=[('',rows)]
    else:
        from sedan_spec import PANEL_GAP
        groups=[]
        for inner in [True,False]:
            xx=.615+(-1 if inner else 1)*PANEL_GAP/2;subset=[]
            for row in rows:
                a,c=next((a,c) for a,c in zip(row,row[1:]) if abs(a.x)<=xx<=abs(c.x))
                p=a.lerp(c,(xx-abs(a.x))/(abs(c.x)-abs(a.x)))
                keep=[q for q in row if (abs(q.x)<xx if inner else abs(q.x)>xx)]
                keep=keep+[p] if inner else [p]+keep
                ds=[0.]
                for a,c in zip(keep,keep[1:]):ds.append(ds[-1]+(c-a).length)
                count=(25 if inner else 33) if b.high else (17 if inner else 21);regular=[]
                for i in range(count):
                    d=ds[-1]*i/(count-1);k=next((k for k in range(len(ds)-1) if ds[k+1]>=d),len(ds)-2)
                    regular.append(keep[k].lerp(keep[k+1],(d-ds[k])/(ds[k+1]-ds[k])))
                subset.append(regular)
            groups.append((' lid' if inner else ' quarter',subset))
    result=[]
    for suffix,rows in groups:
        nu=len(rows[0]);ps=[p for row in rows for p in row]
        ob=G.mesh(('Headlamp' if front else 'Taillamp')+' opening'+str(sign)+suffix,ps,[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(nv-1) for i in range(nu-1)],mat)
        ob['form_rows']=nv;ob['form_columns']=nu;ob['aperture_samples']=[c for p in ps for c in p]
        ob['physical_optical_chart']=True
        ob['optical_die_samples']=[c for p in anchors for c in p]
        if not front:ob['lamp_piece']=suffix.strip()
        result.append(ob)
    return result


def rebuild(ob,surface,high=False):
    raw=list(ob['aperture_samples']);guides=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu,nv=ob['form_columns'],ob['form_rows'];sign=1 if guides[0].x>0 else -1
    front=ob.name.startswith('Headlamp');origin=ORIGIN if front else REAR_ORIGIN;end=-1 if front else 1
    raw=list(ob['optical_die_samples']);anchors=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    # Straighten the narrow optical band for fitting. A global polynomial in
    # perspective U/V is ill-conditioned on this long diagonal strip. The cut
    # still uses the common projective chart; this is the mold's own loft chart.
    angle=lambda p:math.atan2(abs(p.x),end*(p.y-origin.y))
    theta=np.array([angle(p) for p in anchors]);middle=(float(theta.min())+float(theta.max()))/2
    span=(float(theta.max())-float(theta.min()))/2
    bottom=anchors[:33];top=anchors[-33:]
    from sedan_upper_surface import Curve
    def fit_height(points):
        return Curve([((angle(points[i])-middle)/span,points[i].z) for i in range(0,33,4)])
    low=fit_height(bottom);upper=fit_height(top)
    def derivative(c,x):
        from bisect import bisect_right
        i=max(0,min(len(c.x)-2,bisect_right(c.x,x)-1));h=c.x[i+1]-c.x[i]
        a=(c.x[i+1]-x)/h;b=(x-c.x[i])/h
        return (c.y[i+1]-c.y[i])/h+h*((1-3*a*a)*c.m[i]+(3*b*b-1)*c.m[i+1])/6
    # Local C2 B-spline sections follow the real upper roll without a global
    # high-degree fit or a recess chosen from a distant part of the lamp.
    knots_a=[-1.]*4+[-.75,-.50,-.25,0,.25,.50,.75]+[1.]*4
    knots_t=[0.]*4+[.60,.85]+[1.]*4
    def spline(x,knots,degree=3):
        x=max(knots[0]+1e-12,min(knots[-1]-1e-12,x))
        values=[1. if knots[i]<=x<knots[i+1] else 0. for i in range(len(knots)-1)]
        for k in range(1,degree+1):
            values=[((x-knots[i])*values[i]/(knots[i+k]-knots[i]) if knots[i+k]>knots[i] else 0.)+
                    ((knots[i+k+1]-x)*values[i+1]/(knots[i+k+1]-knots[i+1]) if knots[i+k+1]>knots[i+1] else 0.) for i in range(len(values)-1)]
        return values
    def spline_derivative(x,knots):
        v=spline(x,knots,2)
        return [(3*v[i]/(knots[i+3]-knots[i]) if knots[i+3]>knots[i] else 0.)-
                (3*v[i+1]/(knots[i+4]-knots[i+1]) if knots[i+4]>knots[i+1] else 0.) for i in range(len(v)-1)]
    def basis(a,t):
        return [u*v for u in spline((a-middle)/span,knots_a) for v in spline(t,knots_t)]
    anchor_uv=[(angle(p),(i//33)/6) for i,p in enumerate(anchors)]
    A=np.array([basis(a,t) for a,t in anchor_uv]);radius=np.array([math.hypot(p.x,p.y-origin.y) for p in anchors])
    coefficients=np.linalg.lstsq(A,radius,rcond=None)[0];residual=A@coefficients-radius
    recess=max(0,float(residual.max())+.0015)
    def mold(a,t):
        q=(a-middle)/span;ba=spline(q,knots_a);bt=spline(t,knots_t)
        da=spline_derivative(q,knots_a);dt=spline_derivative(t,knots_t)
        r=float(np.dot(basis(a,t),coefficients))-recess
        ra=float(np.dot([u*v for u in da for v in bt],coefficients))/span
        rt=float(np.dot([u*v for u in ba for v in dt],coefficients))
        z=low(q)*(1-t)+upper(q)*t
        za=(derivative(low,q)*(1-t)+derivative(upper,q)*t)/span;zt=upper(q)-low(q)
        sa,ca=math.sin(a),math.cos(a)
        da=Vector((sign*(ra*sa+r*ca),end*(ra*ca-r*sa),za))
        dt=Vector((sign*rt*sa,end*rt*ca,zt))
        n=da.cross(dt).normalized()*(-end*sign)
        return Vector((sign*r*sa,origin.y+end*r*ca,z)),n
    coordinates=[(angle(p),(i//nu)/(nv-1)) for i,p in enumerate(guides)]
    if not front:
        from sedan_spec import PANEL_GAP
        inner=ob.get('lamp_piece')=='lid';limit=.615+(-1 if inner else 1)*PANEL_GAP/2
        for j in range(nv):
            k=j*nu+(nu-1 if inner else 0);a,t=coordinates[k]
            for _ in range(16):
                p,_=mold(a,t);error=abs(p.x)-limit
                if abs(error)<1e-7:break
                h=.0001;slope=(abs(mold(a+h,t)[0].x)-abs(mold(a-h,t)[0].x))/(2*h)
                if abs(slope)<1e-5:raise ValueError('Optical lid-plane intersection is singular')
                a-=error/slope
            else:raise ValueError('Optical lid-plane intersection did not converge')
            coordinates[k]=(a,t)
    ps=[];ns=[]
    for a,t in coordinates:
        p,n=mold(a,t);ps.append(p);ns.append(n)
    faces=[]
    for j in range(nv-1):
        for i in range(nu-1):
            a=j*nu+i;b=a+1;c=a+nu;d=c+1
            faces += [(a,b,d),(a,d,c)] if (i+j)%2==0 else [(a,b,c),(b,d,c)]
    if sum((ps[f[1]]-ps[f[0]]).cross(ps[f[2]]-ps[f[0]]).dot(ns[f[0]]) for f in faces)<0:faces=[tuple(reversed(f)) for f in faces]
    grid_ps=list(ps);grid_ns=list(ns);refinement=[]
    for iteration in range(7):
        selected=set();minimum=1.
        for f in faces:
            a,b,c=[ps[i] for i in f];n=(b-a).cross(c-a).normalized()
            agreement=n.dot(sum((ns[i] for i in f),Vector()).normalized());minimum=min(minimum,agreement)
            if agreement<.50:selected.add(tuple(sorted(max(zip(f,f[1:]+f[:1]),key=lambda e:(ps[e[0]]-ps[e[1]]).length_squared))))
        refinement.append(dict(iteration=iteration,triangles=len(faces),minimum_chord_normal_agreement=minimum,split_edges=len(selected)))
        if not selected:break
        midpoint={}
        for a,b in sorted(selected):
            midpoint[(a,b)]=len(ps);q=tuple((x+y)/2 for x,y in zip(coordinates[a],coordinates[b]));coordinates.append(q);p,n=mold(*q);ps.append(p);ns.append(n)
        refined=[]
        for f in faces:
            mids=[midpoint.get(tuple(sorted((f[i],f[(i+1)%3])))) for i in range(3)];number=sum(m is not None for m in mids)
            if number==0:refined.append(f)
            elif number==1:
                i=next(i for i,m in enumerate(mids) if m is not None);a,b,c=f[i],f[(i+1)%3],f[(i+2)%3];m=mids[i];refined.extend([(a,m,c),(m,b,c)])
            elif number==2:
                i=next(i for i,m in enumerate(mids) if m is None);a,b,c=f[i],f[(i+1)%3],f[(i+2)%3];bc,ca=mids[(i+1)%3],mids[(i+2)%3];refined.extend([(a,b,bc),(a,bc,ca),(ca,bc,c)])
            else:
                a,b,c=f;ab,bc,ca=mids;refined.extend([(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)])
        faces=refined
    if minimum<=0:raise ValueError(('Optical physical chords remain reversed',ob.name,refinement))
    number=len(ps);count=len(faces);edges={}
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
    closed=faces+[tuple(i+number for i in reversed(f)) for f in faces]
    closed += [(b,a,a+number,b+number) for es in edges.values() if len(es)==1 for a,b in es]
    old=ob.data;mesh=bpy.data.meshes.new('S240 fair lofted optical mold')
    mesh.from_pydata(ps+[p-n*.0015 for p,n in zip(ps,ns)],[],closed);mesh.update()
    for m in old.materials:mesh.materials.append(m)
    ob.data=mesh;custom=[]
    for f in mesh.polygons:
        r=0 if f.index<count else 1 if f.index<2*count else 2;f.use_smooth=r!=2
        for li in f.loop_indices:
            vi=mesh.loops[li].vertex_index;custom.append(ns[vi%number]*(1 if r==0 else -1) if r!=2 else f.normal)
    mesh.normals_split_custom_set(custom)
    ob['lens_outer_faces']=count;ob['aperture_samples']=[c for p in grid_ps for c in p]
    ob['aperture_chart_samples']=[c for p in grid_ps for c in chart(p,front)[:2]]
    ob['optical_patch_normals']=[c for n in grid_ns for c in n]
    ob['form_row_fractions']=[j/(nv-1) for j in range(nv)]
    ob['optical_fit_residual_max_m']=float(np.max(np.abs(residual)));ob['optical_seating_recess_m']=recess
    ob['optical_fit_condition']=float(np.linalg.cond(A))
    ob['optical_chord_refinement']=str(refinement)
    ob['normal_basis']='Own smooth radial/height optical loft; paired laminate normals; common physical perspective cut'
    if old.users==0:bpy.data.meshes.remove(old)
    print('S240_PHYSICAL_OPTIC',ob.name,count,'outer triangles; extra seating',recess,'fit',float(np.max(np.abs(residual))),'condition',float(np.linalg.cond(A)),flush=True)
