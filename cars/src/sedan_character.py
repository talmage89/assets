"""Original S240 molding wells and compound-curved door mirror housings.

All shapes are generated from authored dimensions and the fair parent sheet.
No reference imagery is read. Fine optics and molded grille detail are deferred.
"""
import math
import bpy
from mathutils import Vector
from mathutils.geometry import convex_hull_2d
from kit import model as G


def well(b,blank,surface,depth,front):
    """Close a real aperture with a continuous inward return and recessed bed."""
    from sedan_apertures import surface_uv,carve
    raw=list(blank['aperture_samples']);ps=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    nu,nv=blank['form_columns'],blank['form_rows']
    indices=list(range(nu))+[j*nu+nu-1 for j in range(1,nv)]+list(range((nv-1)*nu+nu-2,(nv-1)*nu-1,-1))+[j*nu for j in range(nv-2,0,-1)]
    loop=[ps[i] for i in indices]
    # The projected grid may fold at a tight corner. Use the same convex chart
    # boundary as the actual cut, rather than lofting a zigzag guide perimeter.
    if not blank.get('fascia_axial'):
        uv=[surface_uv(p,surface)[0].to_2d() for p in loop]
        loop=[loop[i] for i in convex_hull_2d(uv)]
    normals=[surface_uv(p,surface)[1] for p in loop]
    rings=[[p-n*d for p,n in zip(loop,normals)] for d in [.002,depth]]
    # Cut before adding the well, so its return can never be mistaken for skin.
    carve(front,[blank],surface,recess=depth)
    ob=G.loft(blank.name+' molded return',rings,b.m['body'] if blank.name.startswith('Plate pocket') else b.m['rubber'],caps=False)
    sol=ob.modifiers.new('Molded return gauge','SOLIDIFY');sol.thickness=.002;sol.offset=-1;G.apply(ob)
    b.add(ob,category='openings')
    blank['well_depth_m']=depth-.004
    blank['well_mouth_samples']=[v for p in loop for v in p]
    return ps


def bars(b,blank,points,front):
    """Broad original horizontal grille blades, within the recessed opening."""
    nu,nv=blank['form_columns'],blank['form_rows']
    raw=list(blank['aperture_samples']);bed=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    if blank.name.startswith('Low wide grille'):
        # Seventeen splayed vertical vanes: original Alder cascade motif.
        # A center station gives each vane a shallow molded bow.
        # The recessed bed remains behind the bars, rather than a radiator face.
        for j in range(17):
            t=(j+.5)/17
            def point(row):
                u=t*(nu-1);i=min(nu-2,int(u));return bed[row*nu+i].lerp(bed[row*nu+i+1],u-i)
            lower=point(0);upper=point(nv-1)
            lower.z+=.008;upper.z-=.008
            loops=[]
            for p in [lower,lower.lerp(upper,.5)+Vector((0,-.008,0)),upper]:
                p+=Vector((0,-.018,0))
                loops.append([p+Vector((dx,dy,0)) for dx,dy in [(-.006,-.009),(.006,-.009),(.006,.009),(-.006,.009)]])
            if b.high:
                bar=G.loft(blank.name+f' cascade vane {j:02d}',loops,b.m['bumper'])
            else:
                ps=loops[0]+loops[1][:2]+loops[2]
                fs=[(3,2,1,0),(6,7,8,9),(0,1,5,4),(4,5,7,6),
                    (1,2,8,7,5),(0,4,6,9,3),(2,3,9,8)]
                bar=G.mesh(blank.name+f' cascade vane {j:02d}',ps,fs,b.m['bumper'])
            if b.high:G.bevel(bar,.0012,2)
            b.add(bar,category='openings')
        return
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
    """Door-corner rounded wedges, 250 x 120 x 150 mm, 2110 mm span.

    The aft face is planar; the forward cap shrinks and rounds into the wind.
    Glass and painted shell are separate closed solids, carried by a short arm.
    """
    for side,sign in [('L',-1),('R',1)]:
        parent=bpy.data.objects['Door_F'+side]
        contour=G.fillet_polygon([(-.125,-.055),(.102,-.075),(.125,.037),(.074,.075),(-.105,.060)],.022,4)
        loops=[[(sign*(.930+x*scale+shift),y,.990+z*scale) for x,z in contour]
               for y,scale,shift in [(-.915,.40,-.015),(-.902,.76,-.007),(-.875,.98,0),(-.830,1,0),(-.795,.97,0)]]
        cap=G.loft('Mirror housing_'+side,loops,b.m['body']);G.smooth(cap,50);b.add(cap,parent,category='mirrors')
        pane_outline=G.fillet_polygon([(-.105,-.044),(.086,-.061),(.104,.030),(.063,.059),(-.089,.048)],.016,4)
        pane=G.loft('Mirror pane_'+side,[[(sign*(.930+x),y,.990+z) for x,z in pane_outline] for y in [-.797,-.793]],b.m['glass'])
        b.add(pane,parent,category='mirrors')
        stem=G.tube('Mirror stalk_'+side,[(sign*.867,-1.010,.943),(sign*.851,-.944,.952),(sign*.849,-.872,.971)],.017,b.m['rubber'],sides=8)
        b.add(stem,parent,category='mirrors')


def plate_lamp(b,blank,points):
    """Small downward-facing license lamp tucked under the crisp pocket brow."""
    nu=blank['form_columns'];p=points[-nu+nu//2]
    lamp=G.box('Plate illumination housing',p+Vector((0,-.004,-.006)),(.092,.016,.014),b.m['bumper'],.003,1)
    b.add(lamp,bpy.data.objects['Trunk'],category='openings')
    lens=G.box('Plate illumination lens',p+Vector((0,.001,-.012)),(.074,.010,.003),b.m['glass'],.001,1)
    b.add(lens,bpy.data.objects['Trunk'],category='openings')
    raw=list(blank['aperture_samples']);bed=[Vector(raw[i:i+3]) for i in range(0,len(raw),3)]
    center=sum(bed,Vector())/len(bed)
    lower,upper=bed[nu//2],bed[-nu+nu//2]
    tilt=math.atan2(lower.y-upper.y,upper.z-lower.z);n=Vector((0,math.cos(tilt),math.sin(tilt)))
    proud=max((p-center).dot(n) for p in bed)+.0018
    plate=G.box('Plate blank 12x6 inch',center+n*proud,(.3048,.001,.1524),b.m['wheel'],0)
    plate.rotation_euler.x=tilt
    b.add(plate,bpy.data.objects['Trunk'],category='openings')


def rear_trim(b,tree):
    """Flush reflector inserts and one rolled exhaust finisher in the molding."""
    for side,sign in [('L',-1),('R',1)]:
        from sedan_body import form_blank,locator_y_guess
        rows=[]
        for j in range(3):
            z=.315+(j-1)*.012;half=.0625 if j==1 else .057
            xs=[sign*(.615+(2*i/6-1)*half) for i in range(7)]
            rows.append([(x,locator_y_guess(x,z,False),z) for x in xs])
        ob=form_blank('Rear reflector_'+side,rows,b.m['wheel'],tree,False,axial=True)
        for v in ob.data.vertices:
            _,n,_,_=tree.find_nearest(v.co);v.co-=n*.011
        b.add(ob,category='openings')
    # A rolled lip with an actual dark bore; the inner return sits inside the
    # black molding, with no broad horizontal plate protruding behind the car.
    p,n,_,_=tree.find_nearest(Vector((.500,2.37,.330)))
    p-=n*.006
    tangent=Vector((n.y,-n.x,0)).normalized();up=tangent.cross(n).normalized()
    outline=G.rounded_rectangle(.135,.052,.019,2)
    loops=[]
    for depth,scale in [(-.002,1),(.004,1),(.004,.84),(-.042,.84)]:
        loops.append([p+tangent*(x*scale)+up*(z*scale)+n*depth for x,z in outline])
    count=len(outline);vs=[p for loop in loops for p in loop]
    fs=[(j*count+i,j*count+(i+1)%count,((j+1)%4)*count+(i+1)%count,((j+1)%4)*count+i) for j in range(4) for i in range(count)]
    b.add(G.mesh('Exhaust finisher rolled lip',vs,fs,b.m['wheel']),category='openings')
    bore_outline=G.rounded_rectangle(.117,.037,.013,2)
    bore=G.loft('Exhaust dark bore',[[p+tangent*x+up*z+n*d for x,z in bore_outline] for d in [-.043,-.040]],b.m['rubber'])
    b.add(bore,category='openings')
