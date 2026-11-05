"""Feature-aligned physical chords on the newly lofted rear greenhouse.

Port of the hatch shoulder's held-boundary resampling method. Y/radial-angle
coordinates follow the manufactured sections; the old coarse cage diagonals
were not reflection-aligned. Every cut boundary stays fixed and conforming.
"""
import math,json
import bpy,bmesh
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt
from mathutils.bvhtree import BVHTree
from kit import model as G
from sedan_upper_surface import field,rail
from sedan_surface_normals import normal


def rebuild(ob,surface,high=False):
    from sedan_fairness import field as old_field
    from sedan_body import shoulder_height,sheet_gauge,closeable_sheet
    world=ob.matrix_world;inverse=world.inverted();nm=world.to_3x3().transposed();old=ob.data
    original_normal=old_field([ob]).nearest_normal
    ps=[world@v.co for v in old.vertices];old.calc_loop_triangles();roles=old.attributes['sheet_role']
    tree=BVHTree.FromPolygons(ps,[tuple(t.vertices) for t in old.loop_triangles if roles.data[t.polygon_index].value==0],all_triangles=True)
    bm=bmesh.new();bm.from_mesh(old);role=bm.faces.layers.int['sheet_role'];bm.verts.index_update()
    # Rebuild the gauge after resampling, so its hidden skin corresponds to
    # the new physical chords at both source densities.
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if f[role]!=0],context='FACES_ONLY')
    selected=[]
    for f in bm.faces:
        p=world@f.calc_center_median()
        if p.y>.50 and p.z>shoulder_height(p.y)+.055:selected.append(f)
    region=set(selected);boundary=list(dict.fromkeys(e for f in selected for e in f.edges if sum(q in region for q in e.link_faces)==1))
    boundary_degree={e:len(e.link_faces) for e in boundary}
    verts=sorted({v for e in boundary for v in e.verts},key=lambda v:v.index);lookup={v:i for i,v in enumerate(verts)}
    sign=-1 if ob.name.endswith('L') else 1
    def chart(p):return Vector((p.y,abs(p.x)-rail(p.y)))
    # Cut intersections on a coarse chord can be centimeters below the real
    # parent. Reconstruct their height from that SAME dense surface; retaining
    # those wrong heights would retain the wavering frame by construction.
    for v in verts:
        p=world@v.co
        if p.y>.50 and p.z>shoulder_height(p.y)+.055:
            hit=surface['tree'].ray_cast(Vector((p.x,p.y,3)),Vector((0,0,-1)),4)[0]
            if hit is None:raise ValueError('Upper cut boundary misses the dense parent')
            v.co=inverse@hit
    coords=[chart(world@v.co) for v in verts];edges=[tuple(lookup[v] for v in e.verts) for e in boundary]
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
    y0,y1=min(q.x for q in coords),max(q.x for q in coords);v0,v1=min(q.y for q in coords),max(q.y for q in coords)
    dy,dv=(.020,.020) if high else (.040,.040)
    transverse=sorted(set([v0+k*dv for k in range(1,math.ceil((v1-v0)/dv)) if abs(v0+k*dv)>.050]+
        [i*.012 for i in range(-4,5) if v0<i*.012<v1]))
    for j in range(1,math.ceil((y1-y0)/dy)):
        for v in transverse:
            q=Vector((y0+j*dy,v))
            if inside(q) and distance(q)>.004:coords.append(q)
    result,_,faces,original,*_=delaunay_2d_cdt(coords,edges,[],0,1e-8)
    faces=[f for f in faces if inside(sum((result[i] for i in f),Vector((0,0)))/len(f))]
    needed={i for f in faces for i in f};newverts={};deviation=0.;example=None
    for i in sorted(needed):
        held=[j for j in original[i] if j<len(verts)]
        if held:
            if len(held)!=1:raise ValueError('Upper loft chart merged distinct boundary stations')
            newverts[i]=verts[held[0]]
        else:
            y,v=result[i];x=sign*(rail(y)+v)
            p=surface['tree'].ray_cast(Vector((x,y,3)),Vector((0,0,-1)),4)[0]
            if p is None:raise ValueError('Upper physical row misses the dense parent')
            hit,_,_,d=tree.find_nearest(p)
            if d>deviation:deviation=d;example=dict(new_m=list(p),original_m=list(hit),chart=list(result[i]))
            newverts[i]=bm.verts.new(inverse@p)
    before=sum(len(f.verts)-2 for f in selected)
    bmesh.ops.delete(bm,geom=selected,context='FACES_ONLY')
    for f in faces:
        vs=[newverts[i] for i in f];p=[world@v.co for v in vs];q=sum(p,Vector())/len(p)
        n=normal(q,original_normal(q))
        if (p[1]-p[0]).cross(p[2]-p[0]).dot(n)<0:vs.reverse()
        nf=bm.faces.new(vs);nf[role]=0;nf.material_index=0;nf.smooth=True
    for e in boundary:
        if not e.is_valid or len(e.link_faces)!=boundary_degree[e]:raise ValueError('Upper loft boundary is not conforming')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.normal_update();bm.to_mesh(old);bm.free()
    closeable_sheet(ob);old=ob.data
    # Retained normals come from the same smooth die, not from the new fans.
    outside=[normal(world@v.co,original_normal(world@v.co)) for v in old.vertices]
    num=len(outside);sheet_gauge(ob,.0009);me=ob.data;custom=[];roles=me.attributes.get('sheet_role') or me.attributes.new('sheet_role','INT','FACE')
    for f in me.polygons:
        r=f.material_index;roles.data[f.index].value=r;f.use_smooth=r!=2
        for li in f.loop_indices:
            vi=me.loops[li].vertex_index;custom.append(nm@(outside[vi%num]*(1 if r==0 else -1)) if r!=2 else f.normal)
        f.material_index=0
    material=me.materials[0];me.materials.clear();me.materials.append(material);me.normals_split_custom_set(custom)
    ob['upper_physical_rows']=json.dumps(dict(removed_outer_triangles=before,new_outer_triangles=len(faces),boundary_vertices=len(verts),boundary_xy_held=True,longitudinal_spacing_m=dy,transverse_chart_spacing_m=dv,maximum_new_vertex_distance_to_old_game_chord_m=deviation,old_game_chord_example=example,reference='Actual dense uncut C2 parent, not the coarse game triangles'))
    print('S240_UPPER_PHYSICAL_ROWS',ob.name,before,'to',len(faces),'held boundary',len(verts),'max distance',deviation,flush=True)


def build(surface,high=False):
    for side in ['L','R']:rebuild(bpy.data.objects['Greenhouse_'+side],surface,high)
