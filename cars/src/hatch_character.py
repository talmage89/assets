"""Original H120 molding wells and compound-curved door mirror housings.

All shapes are generated from authored dimensions and the fair parent sheet.
No reference imagery is read. Fine optics and molded grille detail are deferred.
"""
import math
import bpy
from mathutils import Vector
from kit import model as G


def well(b,blank,surface,depth,front):
    """Close a real aperture with a continuous inward return and recessed bed."""
    from hatch_apertures import surface_uv,carve
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
    b.add(ob,blank.parent,category='openings')
    blank['well_depth_m']=depth-.004
    # Locators sit slightly above the paint to make projection robust. Depth
    # metrology must start at the evaluated parent skin, not that offset guide.
    skin_loop=[surface['tree'].find_nearest(p)[0] for p in loop]
    blank['well_mouth_samples']=[v for p in skin_loop for v in p]
    blank['well_mouth_basis']='Actual evaluated parent skin before cut; no locator standoff'
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


def surround(b,blank,surface):
    """A proud 9 mm molding follows the actual curved opening mouth."""
    from hatch_apertures import surface_uv
    raw=list(blank['well_mouth_samples']);loop=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    if not b.high:loop=loop[::2]
    frames=[]
    center=sum(loop,Vector())/len(loop)
    for i,p in enumerate(loop):
        n=surface_uv(p,surface)[1]
        tangent=(loop[(i+1)%len(loop)]-loop[i-1]).normalized()
        outward=tangent.cross(n).normalized()
        if outward.dot(p-center)<0:outward.negate()
        section=[]
        for w,d in [(-.001,-.003),(-.001,.0005),(.008,.0005),(.008,-.003)]:
            q=surface['tree'].find_nearest(p+outward*w)[0]
            section.append(q+surface_uv(q,surface)[1]*d)
        frames.append(section)
    frames.append(frames[0])
    ob=G.loft('Grille proud surround',frames,b.m['bumper'],caps=False)
    import bmesh
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    b.add(ob,category='openings')


def mirrors(b):
    """Crowned teardrop caps: continuous cubic sections, planar rear glass.

    The outboard quarter rounds through a 50 mm design radius. Longitudinal
    rings taper the molded nose into the door; there is no flat box top.
    """
    from hatch_check import mesh_tree
    curves=[
      ((-.114,-.025),(-.114,.021),(-.084,.053),(-.030,.063)),
      ((-.030,.063),(.012,.073),(.052,.068),(.077,.047)),
      ((.077,.047),(.102,.029),(.114,.014),(.114,-.009)),
      ((.114,-.009),(.114,-.044),(.088,-.065),(.057,-.068)),
      ((.057,-.068),(-.008,-.068),(-.104,-.064),(-.114,-.025))]
    outline=[]
    for curve in curves:
        for i in range(8 if b.high else 5):
            t=i/(8 if b.high else 5);s=1-t
            outline.append(tuple(s**3*curve[0][k]+3*s*s*t*curve[1][k]+3*s*t*t*curve[2][k]+t**3*curve[3][k] for k in [0,1]))
    for side,sign in [('L',-1),('R',1)]:
        parent=bpy.data.objects['Door_F'+side]
        loops=[]
        for y,scale,shift in [(-.682,.10,-.035),(-.675,.48,-.023),
                              (-.650,.81,-.009),(-.612,1,0),
                              (-.559,1,0),(-.554,.985,0)]:
            loops.append([(sign*(.90565+x*scale+shift),y,1.0628+z*scale) for x,z in outline])
        cap=G.loft('Mirror housing_'+side,loops,b.m['body'])
        G.smooth(cap,90);b.add(cap,parent,category='mirrors')
        G.smooth(cap,90)
        pane=G.loft('Mirror pane_'+side,[[(sign*(.90565+x*.89),y,1.0628+z*.87) for x,z in outline] for y in [-.554,-.551]],b.m['glass'])
        b.add(pane,parent,category='mirrors')
        door=mesh_tree([bpy.data.objects['Door F_'+side]])
        sail_outline=[(-.839,.967),(-.679,.978),(-.800,1.059)]
        roots=[door.find_nearest(Vector((sign*.85,y,z)))[0] for y,z in sail_outline]
        sail=G.loft('Mirror sail_'+side,[[p+Vector((sign*d,0,0)) for p in roots] for d in [-.002,.009]],b.m['rubber'])
        b.add(sail,parent,category='mirrors')
        shoe=G.profile('Mirror mounting shoe_'+side,[(-.740,1.001),(-.612,1.009),(-.625,1.030),(-.718,1.037)],sign*.840,sign*.881,b.m['rubber'],axis='X',radius=.006,segments=2)
        b.add(shoe,parent,category='mirrors')


def spoiler(b,surface):
    """Supported roof lip with a fair free edge and a closed molded underside."""
    import numpy as np
    def roof(x):
        hit=surface.ray_cast(Vector((x,1.480,2)),Vector((0,0,-1)),2)[0]
        if hit is None:raise ValueError(('Spoiler attachment absent',x))
        return hit.z
    center=roof(0);a,bend=np.linalg.solve([[.35**2,.35**4],[.64**2,.64**4]],[center-roof(.35),center-roof(.64)])
    xs=sorted(set([-.695+1.390*i/16 for i in range(17)]+[-.690,.690]))
    loops=[]
    for x in xs:
        root=roof(x);lip=center-a*x*x-bend*x**4
        loops.append([(x,y,z) for y,z in [(1.475,root+.004),(1.500,root+.022),
          (1.625,lip+.020),(1.655,lip+.013),(1.656,lip-.001),
          (1.625,lip-.007),(1.515,root-.011),(1.480,root-.007)]])
    ob=G.loft('Roof spoiler',loops,b.m['body'])
    sub=ob.modifiers.new('Molded lip smoothing','SUBSURF');sub.levels=2 if b.high else 1;G.apply(ob)
    G.smooth(ob,90);b.add(ob,bpy.data.objects['Liftgate'],category='spoiler')
