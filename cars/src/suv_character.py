"""Original X220 molding wells and compound-curved door mirror housings.

All shapes are generated from authored dimensions and the fair parent sheet.
No reference imagery is read. Fine optics and molded grille detail are deferred.
"""
import math
import bpy
from mathutils import Vector
from kit import model as G


def well(b,blank,surface,depth,front):
    """Close a real aperture with a continuous inward return and recessed bed."""
    from suv_apertures import surface_uv,carve
    raw=list(blank['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu,nv=blank['form_columns'],blank['form_rows']
    indices=list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]
    loop=[ps[i] for i in indices]
    normals=[surface_uv(p,surface)[1] for p in loop]
    rings=[[p-n*d for p,n in zip(loop,normals)] for d in [.002,depth]]
    # Cut before adding the well, so its return can never be mistaken for skin.
    carve(front,[blank],surface,recess=depth)
    if blank.name=='Plate pocket opening':
        # Cut only the aperture. The surrounding convex sheet is never pushed.
        # Its bed is a plane parallel to the gate's tangent at the mouth center.
        center=sum(ps,Vector())/len(ps);hit,_,_,_=surface['tree'].find_nearest(center)
        _,n=surface_uv(hit,surface);plane=hit-n*depth
        def flat(p):
            q=p.copy();q.y=plane.y-(n.x*(q.x-plane.x)+n.z*(q.z-plane.z))/n.y
            return q
        bed=[flat(p) for p in ps];matrix=blank.matrix_world.copy();inverse=matrix.inverted()
        # Rebuild the bed as a closed plane, so no inherited curved normals or
        # reduction can restore the former soft pocket.
        verts=bed+[q-n*.0015 for q in bed]
        fs=[(j*nu+i,j*nu+i+1,(j+1)*nu+i+1,(j+1)*nu+i) for j in range(nv-1) for i in range(nu-1)]
        fs+= [tuple(nu*nv+i for i in reversed(f)) for f in fs.copy()]
        fs += [(a,c,nu*nv+c,nu*nv+a) for a,c in zip(indices,indices[1:]+indices[:1])]
        mesh=bpy.data.meshes.new('Planar plate bed');mesh.from_pydata([inverse@q for q in verts],[],fs);mesh.update()
        old=blank.data;blank.data=mesh;blank.data.materials.append(b.m['rubber'])
        if old.users==0:bpy.data.meshes.remove(old)
        blank['aperture_samples']=[q for p in bed for q in p]
        rings[1]=[bed[i] for i in indices]
        blank['bed_plane_normal']=list(n)
    ob=G.loft(blank.name+' molded return',rings,b.m['rubber'],caps=False)
    sol=ob.modifiers.new('Molded return gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;G.apply(ob)
    b.add(ob,category='openings')
    blank['well_depth_m']=depth-.004
    blank['well_mouth_samples']=[v for p in loop for v in p]
    return ps


def bars(b,blank,points,front):
    """Broad original horizontal grille blades, within the recessed opening."""
    nu,nv=blank['form_columns'],blank['form_rows']
    raw=list(blank['aperture_samples']);bed=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    for j in [1,2,3]:
        row=bed[j*nu:(j+1)*nu]
        if not b.high:row=row[::2]
        # A rectangular section follows the crown, rather than a bar in space.
        loops=[]
        for p in row:
            p=p+Vector((0,-.008 if front else .008,0))
            loops.append([p+Vector((0,dy,dz)) for dy,dz in [(-.003,-.005),(.003,-.005),(.003,.005),(-.003,.005)]])
        b.add(G.loft(blank.name+f' blade {j}',loops,b.m['bumper']),category='openings')


def mirrors(b):
    """Door-corner rounded wedge, compound nose and planar rear glazing."""
    # X/Z outline is deliberately asymmetric: a low inner heel, rounded crown,
    # and an aft optical plane. Several shaped sections make the compound cap.
    # Evenly distributed elliptical sections replace the rounded-polygon cage
    # and QEM collapse, whose long fans made the front surface visibly faceted.
    count=64 if b.high else 48;steps=20 if b.high else 12
    def rounded(q):return math.copysign(abs(q)**.78,q)
    profile=[(.9285+.130*rounded(math.cos(math.tau*i/count)),1.215+.080*rounded(math.sin(math.tau*i/count))) for i in range(count)]
    for side,sgn in [('L',-1),('R',1)]:
        parent=bpy.data.objects['Door_F'+side];rings=[]
        for j in range(1,steps+1):
            a=(math.pi/2)*j/steps;r=math.sin(a);y=-.714+.126*(1-math.cos(a))
            # The inner heel draws toward the door; crown and outboard end
            # remain elliptical instead of planar segments of a polygon.
            rings.append([(sgn*(.9285+(x-.9285)*r-.018*(1-r)),y,1.215+(z-1.215)*r) for x,z in profile])
        rings.append([(sgn*x,-.584,1.215+(z-1.215)*.97) for x,z in profile])
        verts=[(sgn*(.9285-.018),-.714,1.215)]+[q for ring in rings for q in ring]
        fs=[(0,1+(i+1)%count,1+i) for i in range(count)]
        fs += [(1+j*count+i,1+j*count+(i+1)%count,1+(j+1)*count+(i+1)%count,1+(j+1)*count+i) for j in range(len(rings)-1) for i in range(count)]
        fs.append(tuple(reversed(range(1+(len(rings)-1)*count,len(verts)))))
        housing=G.mesh('Mirror housing_'+side,verts,fs,b.m['body'])
        b.add(housing,parent,category='mirrors');G.smooth(housing,80)
        rear=rings[-1][::1 if b.high else 2];center=Vector((sgn*.9285,-.583,1.215))
        border=[(center.x+(x-center.x)*.86,-.581,center.z+(z-center.z)*.80) for x,y,z in rear]
        pane=G.loft('Mirror pane_'+side,[[(x,-.585,z) for x,y,z in border],border],b.m['glass'])
        b.add(pane,parent,category='mirrors')
        sail=[[(sgn*x,y,z) for x,y,z in row] for row in [
          [(.854,-.890,1.137),(.854,-.790,1.131),(.866,-.760,1.165),(.860,-.858,1.186)],
          [(.875,-.818,1.140),(.891,-.690,1.142),(.909,-.667,1.171),(.882,-.770,1.190)],
          [(.893,-.715,1.146),(.912,-.641,1.154),(.925,-.646,1.176),(.913,-.711,1.185)]]]
        b.add(G.loft('Mirror sail_'+side,sail,b.m['rubber']),parent,category='mirrors')


def optical_case(b,lamp,polygon,surface,front):
    """Closed molded bowl behind the exact projected aperture, not a flat cap."""
    from mathutils.geometry import barycentric_transform,delaunay_2d_cdt
    from mathutils.bvhtree import BVHTree
    if 'uv_tree' not in surface:
        surface['uv_tree']=BVHTree.FromPolygons(surface['uvs'],surface['triangles'],all_triangles=True)
    # Follow the curved chart between guide corners. Straight chords through
    # a concave corner can emerge through the painted skin as black teeth.
    border=[]
    for a,c in zip(polygon,polygon[1:]+polygon[:1]):
        steps=max(1,math.ceil((c-a).length/.60))
        border.extend(a.lerp(c,i/steps) for i in range(steps))
    mouth=[];bed=[]
    def sample(uv,depth):
        from suv_apertures import evaluate_chart
        p,n=evaluate_chart(uv,surface);return p-n*depth
    for uv in border:
        mouth.append(sample(uv,.003));bed.append(sample(uv,.045))
    count=len(mouth);faces=[(i,(i+1)%count,count+(i+1)%count,count+i) for i in range(count)]
    # A constrained bed follows the same sweep instead of an n-gon spanning it.
    uv=[p.to_2d() for p in border]
    step=(.045 if b.high else .075) if surface.get('polar') else 1.
    for x in range(math.floor(min(p.x for p in uv)/step),math.ceil(max(p.x for p in uv)/step)+1):
        for y in range(math.floor(min(p.y for p in uv)/step),math.ceil(max(p.y for p in uv)/step)+1):uv.append(Vector((x*step,y*step)))
    coords,_,caps,*_=delaunay_2d_cdt(uv,[],[list(range(count))],1,1e-6)
    vertices=mouth+bed;lookup={}
    for index in sorted({i for face in caps for i in face}):
        p=coords[index]
        near=min(range(count),key=lambda i:(border[i].to_2d()-p).length)
        if (border[near].to_2d()-p).length<1e-5:lookup[index]=count+near
        else:lookup[index]=len(vertices);vertices.append(sample(p,.045))
    faces.extend(tuple(lookup[i] for i in face) for face in caps)
    ob=G.mesh(lamp.name+' optical cassette',vertices,faces,b.m['rubber'])
    ob['cassette_sheet_vertex_count']=len(vertices)
    cap=ob.data.polygons[-1];center=cap.center;hint=Vector((center.x,-1 if front else 1,0))
    if cap.normal.dot(hint)<0:
        for face in ob.data.polygons:face.flip()
    sol=ob.modifiers.new('Molded optical cassette gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    ob['case_loop_vertices']=count
    b.add(ob,bpy.data.objects['Liftgate'] if lamp.get('lamp_piece')=='gate' else None,category='openings')
