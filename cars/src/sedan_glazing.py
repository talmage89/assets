"""Pane-local optical molds with collared, injective physical triangulation.

Ported from the SUV's optical construction: fit only our generated uncut glass
positions, never the neighboring steel normals. Each border chord connects to
a nearby inward collar; entrance and exit share one parametric normal field.
The normal atlas is disconnected for glass by the existing delivery policy.
"""
import json
import math,bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from kit import model as G
from mathutils.geometry import barycentric_transform


def cut_opening(bm,names,parent):
    """Cut the accepted physical windshield outline from the uncut stamping.

    Cage columns identify materials, not a manufactured glass opening. Their
    varying transverse widths had put the upper corners into the pillar roll
    and narrowed the bottom. These measured package guides retain the former
    1.67 m base and 1.35 m header, independently of that column spacing.
    """
    from sedan_upper_surface import Curve
    width=Curve([(-1.0773,.8346),(-.9817,.8128),(-.8131,.7825),
                 (-.5788,.7340),(-.4079,.6893),(-.3266,.6733)])
    y0,y1=-1.0773,-.3266
    stations=[y0+(y1-y0)*i/24 for i in range(25)]
    def candidates():
        return [f for f in bm.faces if names[f.material_index] in ['Windshield','Greenhouse_L','Greenhouse_R','Roof']
            and -1.16<f.calc_center_median().y<-.24 and f.calc_center_median().z>.85]
    def split(fs,point,normal):
        es={e for f in fs for e in f.edges};vs={v for f in fs for v in f.verts}
        bm.verts.index_update();bm.edges.index_update();bm.faces.index_update()
        bmesh.ops.bisect_plane(bm,geom=sorted(vs,key=lambda v:v.index)+sorted(es,key=lambda e:e.index)+sorted(fs,key=lambda f:f.index),dist=1e-8,plane_co=point,plane_no=normal,clear_inner=False,clear_outer=False)
    for y in stations:split(candidates(),(0,y,0),(0,1,0))
    for a,c in zip(stations,stations[1:]):
        slope=(width(c)-width(a))/(c-a)
        for sign in [-1,1]:
            fs=[f for f in candidates() if a-1e-7<f.calc_center_median().y<c+1e-7]
            split(fs,(sign*width(a),a,0),(sign,-slope,0))
    for f in candidates():
        p=f.calc_center_median()
        if y0<p.y<y1 and abs(p.x)<width(p.y):f.material_index=names.index('Windshield')
        elif names[f.material_index]=='Windshield':f.material_index=names.index('Greenhouse_L' if p.x<0 else 'Greenhouse_R')
    for v in {v for f in candidates() for v in f.verts}:
        p=v.co
        if y0-1e-6<=p.y<=y1+1e-6 and abs(abs(p.x)-width(p.y))<.0003:
            hit=parent.ray_cast(Vector((p.x,p.y,3)),Vector((0,0,-1)),4)[0]
            if hit is None:raise ValueError('Windshield frame misses its parent stamping')
            v.co.z=hit.z


def seat_on_parent(ob,surface):
    """Pair both laminate faces on the physical opening, preserving its XY."""
    me=ob.data;roles=me.attributes['sheet_role'];world=ob.matrix_world;inverse=world.inverted();nm=world.to_3x3().transposed()
    outside=sorted({i for f in me.polygons if roles.data[f.index].value==0 for i in f.vertices});num=len(me.vertices)//2
    if outside!=list(range(num)):raise ValueError(('Unexpected original laminate pairing',ob.name))
    normals=[];maximum=0.
    for i in outside:
        old=world@me.vertices[i].co;hit,_,fi,_=surface['tree'].ray_cast(Vector((old.x,old.y,3)),Vector((0,0,-1)),4)
        if hit is None:raise ValueError(('Glazing opening misses parent',ob.name,list(old)))
        a,b,c=surface['triangles'][fi]
        n=barycentric_transform(hit,*[surface['points'][k] for k in [a,b,c]],*[surface['normals'][k] for k in [a,b,c]]).normalized()
        p=Vector((old.x,old.y,hit.z-.002*n.z));maximum=max(maximum,(p-old).length)
        me.vertices[i].co=inverse@p;me.vertices[i+num].co=inverse@(p-n*.0048);normals.append(n)
    me.update();custom=[]
    for f in me.polygons:
        r=roles.data[f.index].value;f.use_smooth=r!=2
        for li in f.loop_indices:
            i=me.loops[li].vertex_index;custom.append(nm@(normals[i%num]*(1 if r==0 else -1)) if r!=2 else f.normal)
    me.normals_split_custom_set(custom);ob['opening_parent_height_reconstruction_max_m']=maximum


def rebuild(ob,high=False):
    from sedan_exterior import perimeter
    old=ob.data;world=ob.matrix_world;inverse=world.inverted()
    border=perimeter(ob)
    # Dense fixed physical anchors make the optical mold independent of the
    # delivery triangulation. All data are from our own procedural source.
    roles=old.attributes.get('sheet_role')
    ids=sorted({i for f in old.polygons if roles.data[f.index].value==0 for i in f.vertices})
    points=[world@old.vertices[i].co for i in ids]
    xy=np.array([(p.x,p.y) for p in points]);center=xy.mean(axis=0);scale=np.maximum(xy.std(axis=0),.1)
    # A symmetric C2 sag eliminates the parent's pillar/rail roll
    # while retaining the gentle compound curvature of the manufactured pane.
    center[0]=0
    powers=([(0,0),(0,1),(0,2),(2,0),(2,1),(2,2)] if ob.name=='Windshield' else
            [(0,j) for j in range(4)]+[(2,0),(2,1)])
    q=(xy-center)/scale;A=np.column_stack([q[:,0]**i*q[:,1]**j for i,j in powers])
    target=np.array([p.z for p in points]);co=np.linalg.lstsq(A,target,rcond=None)[0]
    residual=A@co-target
    def mold(u,v):
        x=(u-center[0])/scale[0];y=(v-center[1])/scale[1]
        z=sum(c*x**i*y**j for c,(i,j) in zip(co,powers))
        dx=sum(c*i*x**(i-1)*y**j for c,(i,j) in zip(co,powers) if i)/scale[0]
        dy=sum(c*j*x**i*y**(j-1) for c,(i,j) in zip(co,powers) if j)/scale[1]
        return Vector((u,v,z)),Vector((-dx,-dy,1)).normalized()
    coords=[p.to_2d() for p in border];outline=list(range(len(coords)))
    middle=sum(coords,Vector((0,0)))/len(coords);collar=[]
    for i in outline:
        p=coords[i];collar.append(len(coords));coords.append(p.lerp(middle,min(.25,.025/(p-middle).length)))
    edges=list(zip(outline,outline[1:]+outline[:1]))+list(zip(collar,collar[1:]+collar[:1]))+list(zip(outline,collar))
    def inside(p):
        n=0
        for i,j in zip(outline,outline[1:]+outline[:1]):
            a,b=coords[i],coords[j]
            if (a.y>p.y)!=(b.y>p.y) and p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x:n+=1
        return n%2==1
    def distance(p):
        values=[]
        for i,j in zip(outline,outline[1:]+outline[:1]):
            a,b=coords[i],coords[j];d=b-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared));values.append((p-a-d*t).length)
        return min(values)
    step=.050 if high else .100
    x0,x1=min(p.x for p in coords),max(p.x for p in coords);y0,y1=min(p.y for p in coords),max(p.y for p in coords)
    for j in range(1,int((y1-y0)/step)+1):
        for i in range(1,int((x1-x0)/step)+1):
            p=Vector((x0+i*step,y0+j*step))
            if inside(p) and distance(p)>.040:coords.append(p)
    uv,_,faces,*_=delaunay_2d_cdt(coords,edges,[outline],1,1e-8)
    used=sorted({i for f in faces for i in f});remap={v:i for i,v in enumerate(used)}
    uv=[uv[i] for i in used];faces=[tuple(remap[i] for i in f) for f in faces]
    ps=[];ns=[]
    for u,v in uv:
        p,n=mold(u,v);ps.append(p);ns.append(n)
    if sum((ps[f[1]]-ps[f[0]]).cross(ps[f[2]]-ps[f[0]]).z for f in faces)<0:faces=[tuple(reversed(f)) for f in faces]
    # Reflection directions, rather than silhouette error alone, determine
    # optical chords. The old sparse diagonal interpolation made a smooth
    # analytic sag reflect the softbox as several straight torn segments.
    import math
    angle_limit=math.radians(.08 if ob.name=='Windshield' else .15)
    chord_limit=.00060 if ob.name=='Windshield' else .00080
    refinement=[]
    for iteration in range(7):
        selected=set();worst=0.;chord=0.
        for f in faces:
            for a,b in zip(f,f[1:]+f[:1]):
                q=(uv[a]+uv[b])/2;p,n=mold(q.x,q.y)
                error=n.angle((ns[a]+ns[b]).normalized());deviation=(p-(ps[a]+ps[b])/2).length
                worst=max(worst,error);chord=max(chord,deviation)
                if error>angle_limit or deviation>chord_limit:selected.add(tuple(sorted((a,b))))
            q=sum((uv[i] for i in f),Vector((0,0)))/3;_,n=mold(q.x,q.y)
            if n.angle(sum((ns[i] for i in f),Vector()).normalized())>angle_limit:
                selected.add(tuple(sorted(max(zip(f,f[1:]+f[:1]),key=lambda e:(ps[e[0]]-ps[e[1]]).length_squared))))
        refinement.append(dict(iteration=iteration,triangles=len(faces),normal_midpoint_error_max_degrees=math.degrees(worst),chord_deviation_max_m=chord,split_edges=len(selected)))
        if not selected:break
        midpoint={}
        for a,b in sorted(selected):
            midpoint[(a,b)]=len(uv);q=(uv[a]+uv[b])/2;uv.append(q);p,n=mold(q.x,q.y);ps.append(p);ns.append(n)
        refined=[]
        for f in faces:
            mids=[midpoint.get(tuple(sorted((f[i],f[(i+1)%3])))) for i in range(3)];number=sum(m is not None for m in mids)
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
    num=len(ps);count=len(faces);boundary={}
    for f in faces:
        for a,b in zip(f,f[1:]+f[:1]):boundary.setdefault(tuple(sorted((a,b))),[]).append((a,b))
    closed=faces+[tuple(i+num for i in reversed(f)) for f in faces]
    closed += [(b,a,a+num,b+num) for rows in boundary.values() if len(rows)==1 for a,b in rows]
    mesh=bpy.data.meshes.new(ob.name+' independent optical mold')
    mesh.from_pydata([inverse@p for p in ps]+[inverse@(p-n*.0048) for p,n in zip(ps,ns)],[],closed);mesh.update()
    for m in old.materials:mesh.materials.append(m)
    ob.data=mesh;roles=mesh.attributes.new('sheet_role','INT','FACE');custom=[];nm=world.to_3x3().transposed()
    for f in mesh.polygons:
        r=0 if f.index<count else 1 if f.index<2*count else 2;roles.data[f.index].value=r;f.use_smooth=r!=2
        for li in f.loop_indices:
            vi=mesh.loops[li].vertex_index
            custom.append(nm@(ns[vi%num]*(1 if r==0 else -1)) if r!=2 else f.normal)
    mesh.normals_split_custom_set(custom)
    worst=int(np.argmax(abs(residual)))
    ob['optical_mold']=json.dumps(dict(center=center.tolist(),scale=scale.tolist(),powers=powers,coefficients=co.tolist(),residual_p50_p95_max_m=np.percentile(abs(residual),[50,95,100]).tolist(),maximum_residual_source_m=list(points[worst]),maximum_residual_fitted_z_m=float((A@co)[worst]),border_vertices=len(outline),collar_width_m=.025))
    ob['normal_basis']='Own symmetric C2 optical sag; identical entrance/exit parameters; flat 4.8 mm gauge rim'
    ob['optical_reflection_refinement']=json.dumps(refinement)
    if old.users==0:bpy.data.meshes.remove(old)
    print('S240_OPTICAL_MOLD',ob.name,len(faces),'outer triangles; fit residual',np.percentile(abs(residual),[50,95,100]),flush=True)


def build(high=False,surface=None):
    if surface is not None:
        for ob in list(bpy.context.scene.objects):
            if ob.type=='MESH' and ob.get('part_category')=='glass':seat_on_parent(ob,surface)
    for name in ['Windshield','Backlight']:rebuild(bpy.data.objects[name],high)
