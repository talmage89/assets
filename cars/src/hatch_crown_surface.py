"""Feature-aligned reflection chords on the upper fascia's narrow nose roll.

The old radial triangulation spans a changing normal phase along unrelated
long diagonals. Keep every cut boundary and sample our own evaluated parent
on rows parallel to the physical nose contour. A smooth height fit to our own
parent supplies mold derivatives, avoiding normal phase changes caused by
nearest-point projection across the roll. No aperture or package refit.
"""
import bpy,bmesh,numpy as np
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from hatch_reference_surface import field
from hatch_body import section_field


def apply(b):
    if b.high:return
    ob=bpy.data.objects['Front molded fascia'];me=ob.data;matrix=ob.matrix_world;inverse=matrix.inverted()
    saved=me.attributes.new('H120 crown held normals','FLOAT_VECTOR','CORNER')
    for r,n in zip(saved.data,me.corner_normals):r.vector=n.vector
    bm=bmesh.new();bm.from_mesh(me);role=bm.faces.layers.int['hatch_outer_skin'];bm.verts.index_update()
    selected=[]
    for f in bm.faces:
        p=matrix@f.calc_center_median()
        if f[role] and abs(p.x)<.70 and p.y<-1.85 and .69<p.z<.78:selected.append(f)
    region=set(selected);boundary=list(dict.fromkeys(e for f in selected for e in f.edges if sum(q in region for q in e.link_faces)==1))
    verts=sorted({v for e in boundary for v in e.verts},key=lambda v:v.index);lookup={v:i for i,v in enumerate(verts)}
    cache={}
    def nose(x):
        key=round(x,7)
        if key not in cache:
            lo,hi=-2.30,-1.60
            for _ in range(28):
                y=(lo+hi)/2
                if section_field((x,y,.72))>0:lo=y
                else:hi=y
            cache[key]=(lo+hi)/2
        return cache[key]
    ps=[matrix@v.co for v in verts];coords=[Vector((p.x,p.y-nose(p.x))) for p in ps];edges=[tuple(lookup[v] for v in e.verts) for e in boundary]
    def inside(q):
        n=0
        for a,c in edges:
            a,c=coords[a],coords[c]
            if (a.y>q.y)!=(c.y>q.y) and q.x<(c.x-a.x)*(q.y-a.y)/(c.y-a.y)+a.x:n+=1
        return n%2==1
    def distance(q):
        ds=[]
        for a,c in edges:
            a,c=coords[a],coords[c];d=c-a;t=max(0,min(1,(q-a).dot(d)/d.length_squared));ds.append((q-a-d*t).length)
        return min(ds)
    for i in range(19):
        x=-.675+i*.075
        for t in [-.012,0,.012,.024,.036,.050,.075]:
            q=Vector((x,t))
            if inside(q) and distance(q)>.0015:coords.append(q)
    uv,_,faces,original,*_=delaunay_2d_cdt(coords,edges,[],0,1e-8)
    faces=[f for f in faces if inside(sum((uv[i] for i in f),Vector((0,0)))/len(f))]
    print('H120_CROWN_PLAN',sum(len(f.verts)-2 for f in selected),'to',len(faces),'held boundary',len(verts),flush=True)
    parent=field()
    newverts={};needed={i for f in faces for i in f}
    for i in sorted(needed):
        ids=[j for j in original[i] if j<len(verts)]
        if ids:
            if len(ids)>1:raise ValueError('Crown boundary merged')
            newverts[i]=verts[ids[0]]
        else:
            x,t=uv[i];y=nose(x)+t;hit=parent((x,y,3),(0,0,-1))
            if hit is None:raise ValueError('Crown sample missed parent')
            newverts[i]=bm.verts.new(inverse@hit[0])
    mat=selected[0].material_index;old_count=sum(len(f.verts)-2 for f in selected)
    bmesh.ops.delete(bm,geom=selected,context='FACES_ONLY')
    for f in faces:
        vs=[newverts[i] for i in f];p=[matrix@v.co for v in vs]
        if (p[1]-p[0]).cross(p[2]-p[0]).z<0:vs.reverse()
        nf=bm.faces.new(vs);nf[role]=1;nf.smooth=True;nf.material_index=mat
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.normal_update()
    for e in boundary:
        if not e.is_valid or len(e.link_faces)!=2:raise ValueError('Crown boundary is not conforming')
    bm.to_mesh(me);bm.free();saved=me.attributes['H120 crown held normals'];role=me.attributes['hatch_outer_skin'];custom=[];nm=matrix.to_3x3().transposed()
    anchors=[]
    for i in range(41):
        x=-.75+i*.0375
        for j in range(25):
            t=-.035+j*.006;y=nose(x)+t;hit=parent((x,y,3),(0,0,-1))
            if hit and .66<hit[0].z<.83:anchors.append((x,t,hit[0].z))
    terms=[(i,j) for i in range(5) for j in range(6) if i+j<=6]
    rows=np.array([[(x/.75)**i*(t/.10)**j for i,j in terms] for x,t,z in anchors]);values=np.array([z for x,t,z in anchors]);coef=np.linalg.lstsq(rows,values,rcond=None)[0];residual=rows@coef-values
    ob['crown_normal_fit_residual_p95_m']=float(np.percentile(abs(residual),95));ob['crown_normal_fit_residual_max_m']=float(abs(residual).max())
    def normal(p):
        x=p.x/.75;t=(p.y-nose(p.x))/.10
        dx=sum(c*i*x**(i-1)*t**j/.75 for c,(i,j) in zip(coef,terms) if i)
        dt=sum(c*j*x**i*t**(j-1)/.10 for c,(i,j) in zip(coef,terms) if j)
        h=.0001;d=(nose(p.x+h)-nose(p.x-h))/(2*h)
        return Vector((-dx+dt*d,-dt,1)).normalized()
    for f in me.polygons:
        for li in f.loop_indices:
            p=matrix@me.vertices[me.loops[li].vertex_index].co
            if role.data[f.index].value and abs(p.x)<.78 and p.y<-1.8 and .64<p.z<.82:
                from hatch_body import smoothstep
                original=parent.nearest_normal(p);target=normal(p)
                w=(1-smoothstep(.72,.78,abs(p.x)))*smoothstep(.64,.66,p.z)*(1-smoothstep(.80,.82,p.z))*(1-smoothstep(-1.85,-1.80,p.y))
                custom.append(nm@original.lerp(target,w).normalized())
            else:custom.append(nm@parent.nearest_normal(p) if role.data[f.index].value and saved.data[li].vector.length<.1 else saved.data[li].vector.copy())
    me.normals_split_custom_set(custom);me.attributes.remove(saved)
    ob['crown_removed_triangles']=old_count;ob['crown_new_triangles']=len(faces)
    print('H120_CROWN_PATCH',old_count,'to',len(faces),'held boundary',len(verts),flush=True)
