"""Feature-aligned reflection chords on the upper fascia's narrow nose roll.

The old radial triangulation spans a changing normal phase along unrelated
long diagonals. Keep every cut boundary and sample our own evaluated parent
on rows parallel to the physical nose contour. No aperture or package refit.
"""
import bpy,bmesh
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
    def design_normal(p):
        q=p.copy();h=.00001
        def gradient(q):
            return Vector([(section_field(q+Vector([h if k==a else 0 for k in range(3)]))-section_field(q-Vector([h if k==a else 0 for k in range(3)])))/(2*h) for a in range(3)])
        for _ in range(6):
            g=gradient(q);q-=g*(section_field(q)/g.length_squared)
        return gradient(q).normalized()
    for f in me.polygons:
        for li in f.loop_indices:
            p=matrix@me.vertices[me.loops[li].vertex_index].co
            if role.data[f.index].value and abs(p.x)<.76 and p.y<-1.8 and .67<p.z<.80:
                from hatch_body import smoothstep
                original=parent.nearest_normal(p);target=design_normal(p)
                w=(1-smoothstep(.70,.76,abs(p.x)))*smoothstep(.67,.69,p.z)*(1-smoothstep(.78,.80,p.z))*(1-smoothstep(-1.85,-1.80,p.y))
                custom.append(nm@original.lerp(target,w).normalized())
            else:custom.append(saved.data[li].vector.copy())
    me.normals_split_custom_set(custom);me.attributes.remove(saved)
    ob['crown_removed_triangles']=old_count;ob['crown_new_triangles']=len(faces)
    print('H120_CROWN_PATCH',old_count,'to',len(faces),'held boundary',len(verts),flush=True)
