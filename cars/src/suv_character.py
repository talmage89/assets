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
    """Door sail and rounded wedge: 260 x 125 x 162 mm, 2117 mm span."""
    for side,sgn in [('L',-1),('R',1)]:
        parent=bpy.data.objects['Door_F'+side];loops=[]
        for t,r in [(0,.30),(.06,.68),(.16,.94),(.28,1),(.68,.98),(.94,.80),(1,.25)]:
            ring=[]
            for k in range(20):
                a=math.tau*k/20;c=math.cos(a);ss=math.sin(a)
                # Rounded rectangular YZ section, flat rear optical face.
                yy=math.copysign(abs(c)**.55,c);zz=math.copysign(abs(ss)**.65,ss)
                ring.append((sgn*(.7985+.260*t),-.735+.0625*r*yy,1.218+.081*r*zz+.008*t))
            loops.append(ring)
        ob=G.loft('Mirror housing_'+side,loops,b.m['body']);b.add(ob,parent,category='mirrors')
        pane=G.box('Mirror pane_'+side,(sgn*.942,-.674,1.225),(.177,.003,.112),b.m['glass'],.018,3);b.add(pane,parent,category='mirrors')
        stem=G.tube('Mirror sail_'+side,[(sgn*.855,-.899,1.146),(sgn*.897,-.818,1.154),(sgn*.916,-.751,1.185)],.021,b.m['rubber'],sides=8);b.add(stem,parent,category='mirrors')


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
        q,_,fi,_=surface['uv_tree'].find_nearest(Vector((uv.x,uv.y,0)));ia,ib,ic=surface['triangles'][fi]
        chart=surface['uvs'];points=surface['points'];normals=surface['normals']
        p=barycentric_transform(q,chart[ia],chart[ib],chart[ic],points[ia],points[ib],points[ic])
        n=barycentric_transform(q,chart[ia],chart[ib],chart[ic],normals[ia],normals[ib],normals[ic]).normalized()
        return p-n*depth
    for uv in border:
        mouth.append(sample(uv,.003));bed.append(sample(uv,.045))
    count=len(mouth);faces=[(i,(i+1)%count,count+(i+1)%count,count+i) for i in range(count)]
    # A constrained bed follows the same sweep instead of an n-gon spanning it.
    uv=[p.to_2d() for p in border]
    for x in range(math.floor(min(p.x for p in uv)),math.ceil(max(p.x for p in uv))+1):
        for y in range(math.floor(min(p.y for p in uv)),math.ceil(max(p.y for p in uv))+1):uv.append(Vector((x,y)))
    coords,_,caps,*_=delaunay_2d_cdt(uv,[],[list(range(count))],1,1e-6)
    vertices=mouth+bed;lookup={}
    for index in sorted({i for face in caps for i in face}):
        p=coords[index]
        near=min(range(count),key=lambda i:(border[i].to_2d()-p).length)
        if (border[near].to_2d()-p).length<1e-5:lookup[index]=count+near
        else:lookup[index]=len(vertices);vertices.append(sample(p,.045))
    faces.extend(tuple(lookup[i] for i in face) for face in caps)
    ob=G.mesh(lamp.name+' optical cassette',vertices,faces,b.m['rubber'])
    cap=ob.data.polygons[-1];center=cap.center;hint=Vector((center.x,-1 if front else 1,0))
    if cap.normal.dot(hint)<0:
        for face in ob.data.polygons:face.flip()
    sol=ob.modifiers.new('Molded optical cassette gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;sol.use_even_offset=False;G.apply(ob)
    ob['case_loop_vertices']=count
    b.add(ob,bpy.data.objects['Liftgate'] if lamp.get('lamp_piece')=='gate' else None,category='openings')
