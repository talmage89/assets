"""Fund optical/upper-surface chords from shallow lower molding triangles.

Only nearly coplanar interior edges are eligible. All surviving positions and
manufactured corner normals are held. Independent probes against the original
outer triangles bound the sampled chord deviation; they do not claim a global
continuous error bound. Gauge backs are seated against the result afterwards.
"""
import math,json
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform


def collapse_lower(mesh,reference,ceiling,world,limit):
    """Conservative interior edge collapses against the original outer sheet."""
    reference.calc_loop_triangles();rr=reference.attributes['sheet_role']
    triangles=[t for t in reference.loop_triangles if rr.data[t.polygon_index].value==0]
    points=[v.co.copy() for v in reference.vertices]
    tree=BVHTree.FromPolygons(points,[tuple(t.vertices) for t in triangles],all_triangles=True)
    normals=[[reference.corner_normals[i].vector.copy() for i in t.loops] for t in triangles]
    def sample(p):
        q,_,i,distance=tree.find_nearest(p);t=triangles[i]
        n=barycentric_transform(q,*[points[k] for k in t.vertices],*normals[i]).normalized()
        return n,distance
    bm=bmesh.new();bm.from_mesh(mesh);role=bm.faces.layers.int['sheet_role']
    bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if f[role]==0]);bm.normal_update()
    count=0
    for iteration in range(64):
        pure={v for v in bm.verts if v.link_faces and all(f[role]==0 for f in v.link_faces) and (world@v.co).z<ceiling}
        bm.edges.index_update();used=set();changed=0
        edges=sorted([e for e in bm.edges if len(e.link_faces)==2 and all(v in pure for v in e.verts)],key=lambda e:(e.calc_length(),e.index))
        for e in edges:
            if count>=limit:break
            if not e.is_valid or e.calc_length()>.12:continue
            a,c=e.verts;na={q for ed in a.link_edges for q in ed.verts if q!=a};nc={q for ed in c.link_edges for q in ed.verts if q!=c}
            if len(na&nc)!=2:continue
            neighborhood=na|nc|{a,c}
            if neighborhood&used:continue
            point=(a.co+c.co)/2;valid=True
            for f in set(a.link_faces)|set(c.link_faces):
                if f in e.link_faces:continue
                ps=[point if v==a or v==c else v.co for v in f.verts]
                n=(ps[1]-ps[0]).cross(ps[2]-ps[0])
                if n.length<2e-10 or n.normalized().dot(f.normal)<.90:valid=False;break
                probes=ps+[sum(ps,Vector())/3]+[p.lerp(q,t) for p,q in zip(ps,ps[1:]+ps[:1]) for t in [.25,.5,.75]]
                if any(sample(p)[1]>.00075 for p in probes):valid=False;break
            if not valid:continue
            bmesh.ops.collapse(bm,edges=[e],uvs=False);used|=neighborhood;changed+=1;count+=1
        if not changed or count>=limit:break
        bm.normal_update()
    if any(not e.is_manifold for e in bm.edges):raise ValueError('Lower allocation lost its closed gauge')
    bm.to_mesh(mesh);bm.free();mesh.update();roles=mesh.attributes['sheet_role'];custom=[];field={}
    for f in mesh.polygons:
        for li in f.loop_indices:
            vi=mesh.loops[li].vertex_index
            if roles.data[f.index].value==0:
                if vi not in field:field[vi]=sample(mesh.vertices[vi].co)[0]
                custom.append(field[vi])
            else:custom.append((0,0,0))
    mesh.normals_split_custom_set(custom);mesh.calc_loop_triangles();maximum=0.
    for t in mesh.loop_triangles:
        if roles.data[t.polygon_index].value!=0:continue
        ps=[mesh.vertices[i].co for i in t.vertices]
        if max((world@p).z for p in ps)>ceiling+.005:continue
        for p in [sum(ps,Vector())/3]+[p.lerp(q,u) for p,q in zip(ps,ps[1:]+ps[:1]) for u in [.25,.5,.75]]:maximum=max(maximum,sample(p)[1])
    if maximum>.000751:raise ValueError(('Lower allocation exceeds its original-surface bound',maximum))
    return dict(collapsed_edges=count,iterations=iteration,sampled_chord_deviation_max_m=maximum)


def reduce(ob):
    ceiling={'Front molded fascia':.690,'Rear molded fascia':.930,'Trunk outer':.980}.get(ob.name)
    if ob.name.startswith('Rear quarter'):ceiling=.80
    if ob.name.startswith('Front fender'):ceiling=.70
    if ceiling is None:return
    old=ob.data;roles=old.attributes.get('sheet_role')
    if roles is None:return
    old.calc_loop_triangles();world=ob.matrix_world;ps=[world@v.co for v in old.vertices]
    tris=[tuple(t.vertices) for t in old.loop_triangles if roles.data[t.polygon_index].value==0]
    original_triangles={frozenset(tuple(old.vertices[i].co) for i in t) for t in tris}
    tree=BVHTree.FromPolygons(ps,tris,all_triangles=True);before=len(old.loop_triangles)
    held={}
    for f in old.polygons:
        if roles.data[f.index].value!=0:continue
        for li in f.loop_indices:
            p=old.vertices[old.loops[li].vertex_index].co
            held[tuple(p)]=old.corner_normals[li].vector.copy()
    attempts=[]
    for degrees in [3.,2.,1.,.5,.25]:
        bm=bmesh.new();bm.from_mesh(old);role=bm.faces.layers.int['sheet_role']
        edges=[e for e in bm.edges if len(e.link_faces)==2 and all(f[role]==0 for f in e.link_faces)
               and max((world@v.co).z for v in e.verts)<ceiling]
        bmesh.ops.dissolve_limit(bm,angle_limit=math.radians(degrees),use_dissolve_boundaries=False,verts=[],edges=edges,delimit=set())
        bmesh.ops.triangulate(bm,faces=[f for f in bm.faces if f[role]==0])
        wire=[e for e in bm.edges if not e.link_faces]
        if wire:bmesh.ops.delete(bm,geom=wire,context='EDGES')
        bm.normal_update();candidate=bpy.data.meshes.new(old.name+' lower molding allocation');bm.to_mesh(candidate);bm.free()
        cr=candidate.attributes['sheet_role'];candidate.calc_loop_triangles();maximum=0.;valid=True;bad=[]
        for t in candidate.loop_triangles:
            if cr.data[t.polygon_index].value!=0:continue
            q=[world@candidate.vertices[i].co for i in t.vertices]
            if max(p.z for p in q)>ceiling+.005:continue
            for p in [sum(q,Vector())/3]+[a.lerp(c,f) for a,c in zip(q,q[1:]+q[:1]) for f in [.25,.5,.75]]:
                maximum=max(maximum,tree.find_nearest(p)[3])
            expected=sum((held[tuple(candidate.vertices[i].co)] for i in t.vertices),Vector()).normalized()
            changed=frozenset(tuple(candidate.vertices[i].co) for i in t.vertices) not in original_triangles
            if t.area>=1e-8 and (t.normal.dot(expected)<=0 or (changed and t.normal.dot(expected)<.25)):
                valid=False
                if len(bad)<6:bad.append(dict(area_m2=t.area,dot=t.normal.dot(expected),center_m=list(sum(q,Vector())/3)))
        valid=valid and maximum<=.00075
        attempts.append(dict(angle_degrees=degrees,triangles=len(candidate.loop_triangles),sampled_chord_deviation_max_m=maximum,accepted=valid,poor_chords=bad))
        if valid:
            for mat in old.materials:candidate.materials.append(mat)
            ob.data=candidate;custom=[]
            for f in candidate.polygons:
                r=cr.data[f.index].value
                for li in f.loop_indices:
                    p=candidate.vertices[candidate.loops[li].vertex_index].co
                    custom.append(held[tuple(p)] if r==0 else (0,0,0))
            candidate.normals_split_custom_set(custom)
            limit=(900 if ob.name.startswith('Front') else 700) if 'fascia' in ob.name else 300 if ob.name=='Trunk outer' else 120
            collapse=collapse_lower(candidate,old,ceiling,world,limit)
            ob['lower_allocation']=json.dumps(dict(original_triangles=before,triangles=len(candidate.loop_triangles),ceiling_m=ceiling,attempts=attempts,collapse=collapse,method='Boundary-preserving interior edge allocation against the original outer sheet; source normals resampled; original-surface center and quarter-edge probes'))
            if old.users==0:bpy.data.meshes.remove(old)
            print('S240_LOWER_ALLOCATION',ob.name,before,'to',len(candidate.loop_triangles),'sampled deviation',maximum,flush=True)
            return
        bpy.data.meshes.remove(candidate)
    raise ValueError(('No bounded lower molding allocation',ob.name,attempts))
