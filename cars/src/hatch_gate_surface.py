"""Fair the gate draw and sample its reflected curvature in a physical chart.

The radial control net underresolved the 47 mm hollow. Restore the continuous
original die field locally, retaining the lamps, cuts, perimeter and lower hem.
Use the parent's smooth normal derivative through the blend: differentiating
its triangle positions would reintroduce facets. Game rows follow the crease.
"""
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from hatch_body import section_field,smoothstep,gate_crease_height
from hatch_reference_surface import field


def apply(b):
    ob=bpy.data.objects['Liftgate outer'];me=ob.data
    matrix=ob.matrix_world;inverse=matrix.inverted();nm=matrix.to_3x3().transposed()
    parent=field();cache={};normal_cache={}
    def weight(x,z):
        return (1-smoothstep(.54,.635,abs(x)))*smoothstep(.650,.695,z)*(1-smoothstep(.945,.982,z))
    def sample(x,z):
        key=(round(x,7),round(z,7))
        if key not in cache:
            p,n,_=parent((x,3,z),(0,-1,0));lo,hi=1.8,2.3
            for _ in range(30):
                y=(lo+hi)/2
                if section_field((x,y,z))>0:hi=y
                else:lo=y
            target=(lo+hi)/2;cache[key]=(p,n,target,p.y+weight(x,z)*(target-p.y))
        return cache[key]
    def normal(x,z):
        key=(x,z)
        if key not in normal_cache:
            p,pn,y,_=sample(x,z);q=Vector((x,y,z));h=.00001
            tn=Vector([(section_field(q+Vector([h if k==a else 0 for k in range(3)]))-section_field(q-Vector([h if k==a else 0 for k in range(3)])))/(2*h) for a in range(3)]).normalized()
            h=.00015;w=weight(x,z)
            wx=(weight(x+h,z)-weight(x-h,z))/(2*h);wz=(weight(x,z+h)-weight(x,z-h))/(2*h)
            dx=(1-w)*(-pn.x/pn.y)+w*(-tn.x/tn.y)+(y-p.y)*wx
            dz=(1-w)*(-pn.z/pn.y)+w*(-tn.z/tn.y)+(y-p.y)*wz
            normal_cache[key]=Vector((-dx,1,-dz)).normalized()
        return normal_cache[key]
    saved=me.attributes.new('H120 gate held normals','FLOAT_VECTOR','CORNER')
    for r,n in zip(saved.data,me.corner_normals):r.vector=n.vector
    role=me.attributes.get('hatch_outer_skin')
    if role is None:
        role=me.attributes.new('hatch_outer_skin','INT','FACE')
        for f in me.polygons:role.data[f.index].value=int(f.index<ob['outer_skin_faces'])
    maximum=0
    for v in me.vertices:
        p=matrix@v.co
        if not (-.636<p.x<.636 and .650<p.z<.982):continue
        parent_point,_,_,y=sample(p.x,p.z);delta=y-parent_point.y
        maximum=max(maximum,abs(delta));p.y+=delta;v.co=inverse@p
    if not b.high:
        bm=bmesh.new();bm.from_mesh(me);outer=bm.faces.layers.int['hatch_outer_skin'];bm.verts.index_update()
        selected=[f for f in bm.faces if f[outer] and abs((matrix@f.calc_center_median()).x)<.635 and .65<(matrix@f.calc_center_median()).z<.99]
        region=set(selected);boundary=list(dict.fromkeys(e for f in selected for e in f.edges if sum(q in region for q in e.link_faces)==1))
        verts=sorted({v for e in boundary for v in e.verts},key=lambda v:v.index);lookup={v:i for i,v in enumerate(verts)}
        points=[matrix@v.co for v in verts];coords=[Vector((p.x,p.z-gate_crease_height(p.x))) for p in points]
        edges=[tuple(lookup[v] for v in e.verts) for e in boundary]
        def inside(q):
            crossings=0
            for a,c in edges:
                a,c=coords[a],coords[c]
                if (a.y>q.y)!=(c.y>q.y) and q.x<(c.x-a.x)*(q.y-a.y)/(c.y-a.y)+a.x:crossings+=1
            return crossings%2==1
        def distance(q):
            distances=[]
            for a,c in edges:
                a,c=coords[a],coords[c];d=c-a;t=max(0,min(1,(q-a).dot(d)/d.length_squared))
                distances.append((q-a-d*t).length)
            return min(distances)
        for i in range(31):
            x=-.60+i*.04
            for j in range(33):
                q=Vector((x,-.25+j*.010))
                if inside(q) and distance(q)>.002:coords.append(q)
        uv,_,faces,original,*_=delaunay_2d_cdt(coords,edges,[],0,1e-8)
        faces=[f for f in faces if inside(sum((uv[i] for i in f),Vector((0,0)))/len(f))]
        newverts={}
        for i in sorted({i for f in faces for i in f}):
            ids=[j for j in original[i] if j<len(verts)]
            if ids:
                if len(ids)>1:raise ValueError('Gate boundary merged')
                newverts[i]=verts[ids[0]]
            else:
                x,t=uv[i];z=t+gate_crease_height(x)
                newverts[i]=bm.verts.new(inverse@Vector((x,sample(x,z)[3],z)))
        material=selected[0].material_index;old_count=sum(len(f.verts)-2 for f in selected)
        bmesh.ops.delete(bm,geom=selected,context='FACES_ONLY')
        for f in faces:
            vs=[newverts[i] for i in f];ps=[matrix@v.co for v in vs]
            if (ps[1]-ps[0]).cross(ps[2]-ps[0]).y<0:vs.reverse()
            nf=bm.faces.new(vs);nf[outer]=1;nf.smooth=True;nf.material_index=material
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.normal_update()
        for edge in boundary:
            if not edge.is_valid or len(edge.link_faces)!=2:raise ValueError('Gate boundary is not conforming')
        bm.to_mesh(me);bm.free()
        ob['gate_chart_old_triangles']=old_count;ob['gate_chart_new_triangles']=len(faces)
        ob['gate_chart_held_boundary_vertices']=len(verts)
        print('H120_GATE_CHART',old_count,'to',len(faces),'held boundary',len(verts),flush=True)
    saved=me.attributes['H120 gate held normals'];role=me.attributes['hatch_outer_skin'];custom=[]
    for f in me.polygons:
        for li in f.loop_indices:
            p=matrix@me.vertices[me.loops[li].vertex_index].co;old=saved.data[li].vector.copy()
            if f.use_smooth and (abs(p.x)<.636 and .650<p.z<.99 or old.length<.1 and role.data[f.index].value):
                n=nm@normal(p.x,p.z)
                custom.append(n if role.data[f.index].value else -n if old.dot(n)<-.5 else old)
            else:custom.append(old)
    me.normals_split_custom_set(custom);me.attributes.remove(saved)
    ob['gate_fairing_max_m']=maximum
    print('H120_GATE_FAIR',maximum,'m',flush=True)
