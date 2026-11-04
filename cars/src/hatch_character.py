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
    """Door-mounted rounded wedges, 240 x 120 x 145 mm; flat rear glass."""
    for side,sign in [('L',-1),('R',1)]:
        parent=bpy.data.objects['Door_F'+side];loops=[]
        count=24 if b.high else 16
        # Superelliptic sections keep a continuously bowed cap instead of four
        # planar faces converging on the nose of a scaled rounded rectangle.
        outline=[]
        for i in range(count):
            a=math.tau*i/count;c,t=math.cos(a),math.sin(a)
            outline.append((.120*math.copysign(abs(c)**(2/2.8),c),.0725*math.copysign(abs(t)**(2/2.8),t)))
        for y,scale in [(-.768,.12),(-.763,.42),(-.746,.80),(-.716,.98),(-.656,1),(-.645,.98),(-.642,.96)]:
            loops.append([(sign*(.9025+x*scale),y,1.052+z*scale-.035*x) for x,z in outline])
        cap=G.loft('Mirror housing_'+side,loops,b.m['body'])
        sub=cap.modifiers.new('Compound plastic wedge','SUBSURF');sub.levels=2 if b.high else 1;G.apply(cap)
        for f in cap.data.polygons:f.use_smooth=True
        G.smooth(cap,90);b.add(cap,parent,category='mirrors')
        outline=G.rounded_rectangle(.211,.119,.025,5 if b.high else 3)
        pane=G.loft('Mirror pane_'+side,[[(sign*(.9025+x),y,1.052+z-.035*x) for x,z in outline] for y in [-.643,-.640]],b.m['glass'])
        b.add(pane,parent,category='mirrors')
        stem=G.tube('Mirror stalk_'+side,[(sign*.827,-.792,.979),(sign*.860,-.765,.992),(sign*.883,-.713,1.000)],.016,b.m['rubber'],sides=8)
        b.add(stem,parent,category='mirrors')
        sail=G.profile('Mirror sail_'+side,[(-.849,.972),(-.752,.978),(-.790,1.036)],sign*.821,sign*.844,b.m['rubber'],axis='X',radius=.004,segments=2)
        b.add(sail,parent,category='mirrors')


def spoiler(b,surface):
    """Molded roof lip overhangs the steep glass, with a closed underside."""
    loops=[]
    for i in range(25 if b.high else 17):
        x=-.695+1.390*i/(24 if b.high else 16);t=x/.695
        hit=surface.ray_cast(Vector((x,1.480,2)),Vector((0,0,-1)),2)[0]
        if hit is None:raise ValueError(('Spoiler roof attachment missing',x))
        drop=1.414-hit.z
        # Rounded wedge section: supported root, 145 mm overhang, 19 mm edge.
        loops.append([(x,y,z-drop) for y,z in [(1.475,1.418),(1.500,1.436),(1.625,1.434),(1.655,1.427),(1.656,1.413),(1.625,1.407),(1.515,1.403),(1.480,1.407)]])
    ob=G.loft('Roof spoiler',loops,b.m['body']);G.smooth(ob,50);b.add(ob,bpy.data.objects['Liftgate'],category='spoiler')
