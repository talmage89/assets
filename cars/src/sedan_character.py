"""Original S240 molding wells and compound-curved door mirror housings.

All shapes are generated from authored dimensions and the fair parent sheet.
No reference imagery is read. Fine optics and molded grille detail are deferred.
"""
import math
import bpy
from mathutils import Vector
from kit import model as G


def well(b,blank,surface,depth,front):
    """Close a real aperture with a continuous inward return and recessed bed."""
    from sedan_apertures import surface_uv,carve
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
    """250 mm outboard by 157 mm tall caps; 2110 mm across both housings.

    A smooth loft is used in all three axes, with an inset rear mirror pane
    and a supported door-mounted stalk. Fold articulation is a later gate.
    """
    for side,sign in [('L',-1),('R',1)]:
        parent=bpy.data.objects['Door_F'+side]
        loops=[]
        for t,r in [(0,.10),(.06,.58),(.18,.88),(.38,1),(.68,.94),(.90,.66),(1,.12)]:
            x=.805+.250*t;zc=1.077+.008*math.sin(math.pi*t)
            loop=[]
            for k in range(16):
                a=math.tau*k/16
                loop.append((sign*x,-.745+.102*r*math.cos(a),zc+.0785*r*math.sin(a)))
            loops.append(loop)
        cap=G.loft('Mirror housing_'+side,loops,b.m['body']);G.smooth(cap,45);b.add(cap,parent,category='mirrors')
        # Elliptical inset rear pane, facing aft with a shallow convex crown.
        rings=[]
        for r in [.06,.65,1]:
            rings.append([(sign*(.930+.100*r*math.cos(math.tau*k/20)),-.647-.012*r*r,1.082+.060*r*math.sin(math.tau*k/20)) for k in range(20)])
        pane=G.loft('Mirror pane_'+side,rings,b.m['glass'],caps=True)
        sol=pane.modifiers.new('Mirror glass gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;G.apply(pane);b.add(pane,parent,category='mirrors')
        stem=G.tube('Mirror stalk_'+side,[(sign*.857,-.810,.976),(sign*.900,-.790,1.011),(sign*.913,-.767,1.048)],.019,b.m['rubber'],sides=8)
        b.add(stem,parent,category='mirrors')
