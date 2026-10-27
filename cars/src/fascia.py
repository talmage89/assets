"""A single original molded/plated fascia with inset upper-corner lamps.

All openings are cut in one closed frame before its face is swept around the
nose. Frame land widths are 60–69 mm; its section is 65 mm deep. Dimensions
and independent surface checks are recorded at the source checkpoint.
"""
import math
import bpy,bmesh
from mathutils import Vector
from kit import model as G
from kit.vehicle import samples
from forms import nose_y,side_x,hood_z,hermite,lamp_surface
from detail_helpers import box,tube,print_quad

TOP=1.305
BOTTOM=.795
DEPTH=.065
LAMP_CENTER=.665
LAMP_WIDTH=.500
LAMP_BOTTOM=1.080
LAMP_TOP=1.245


def rounded(w,h,r,steps):
    return G.rounded_rectangle(w,h,r,steps)


def build_form(b):
    steps=5 if b.high else 3
    outline=[(x,1.050+z) for x,z in rounded(1.968,.510,.035,steps)]
    mat=b.m['wheel'] if b.detail else b.m['body']
    frame=G.profile('Fascia shared frame',outline,0,DEPTH,mat,axis='Y')
    for sign in [-1,1]:
        hole=[(sign*LAMP_CENTER+x,(LAMP_BOTTOM+LAMP_TOP)/2+z) for x,z in rounded(LAMP_WIDTH,LAMP_TOP-LAMP_BOTTOM,.018,steps)]
        G.boolean(frame,G.profile('Fascia lamp tool',hole,-.1,DEPTH+.1,mat,axis='Y'))
    # Wide lower mouth reaches underneath both lamps; the central upper throat
    # rises between them. A continuous 60 mm web holds all three apertures.
    mouth=[(-.915,.855),(.915,.855),(.915,1.020),(.355,1.020),(.355,1.245),(-.355,1.245),(-.355,1.020),(-.915,1.020)]
    from body import rounded_polygon
    mouth=rounded_polygon(mouth,[.012]*len(mouth),steps)
    G.boolean(frame,G.profile('Fascia grille tool',mouth,-.1,DEPTH+.1,mat,axis='Y'))
    G.bevel(frame,.003,3 if b.high else 1);G.apply(frame)
    # Add curvature stations to the turned corners, not triangles to flat land.
    bm=bmesh.new();bm.from_mesh(frame.data)
    for sign in [-1,1]:
        for x in [.760,.805,.845,.875,.900,.929,.950,.967,.978]:
            bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(sign*x,0,0),plane_no=(1,0,0),clear_outer=False,clear_inner=False)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
    bm.to_mesh(frame.data);bm.free()
    axial=[v.co.y for v in frame.data.vertices]
    for v in frame.data.vertices:v.co.y+=nose_y(v.co.x,v.co.z)
    # Analytic cap normals prevent triangulated boolean caps from denting the
    # swept front. The actual side walls and bevel keep geometric normals.
    custom=[(0,0,0)]*len(frame.data.loops)
    for f in frame.data.polygons:
        front=all(abs(axial[i])<1e-6 for i in f.vertices);back=all(abs(axial[i]-DEPTH)<1e-6 for i in f.vertices)
        if front or back:
            f.use_smooth=True
            for li in f.loop_indices:
                p=frame.data.vertices[frame.data.loops[li].vertex_index].co;e=1e-5
                dx=(nose_y(p.x+e,p.z)-nose_y(p.x-e,p.z))/(2*e)
                custom[li]=Vector((dx,-1,.1)).normalized()*(1 if front else -1)
    frame.data.normals_split_custom_set(custom)
    frame['frame_depth_m']=DEPTH
    b.add(frame,category='nose')
    # Painted corner closures continue into the accepted fender field.
    for sign,side in [(-1,'L'),(1,'R')]:
        def cheek(u,v,sign=sign):
            z=.795+(hood_z(.984,-2.499)-.0045-.795)*v
            start=nose_y(.984,z)+DEPTH;end=-2.499;y=start+(end-start)*u
            e=1e-5;slope=(side_x(end+e,z)-side_x(end-e,z))/(2*e)
            x=hermite(u,[(0,.984,.006),(1,side_x(end,z),slope*(end-start))])
            return sign*x,y,z
        b.skin('Fascia body corner_'+side,cheek,8,12,b.m['body'],(sign,0,0),category='nose',gauge=.0009,return_depth=.006)
        def lens(u,v,sign=sign):
            x,y,z=lamp_surface(u,v);return sign*x,y,z
        b.skin('Headlamp envelope_'+str(sign),lens,28,6,b.m['lens'],(sign,-1,0),category='lamp_forms',gauge=.0026,return_depth=0,
                   us=sorted(set(samples(24 if b.high else 12)+[.03,.06,.94,.97])))


def details(b):
    for sign,side in [(-1,'L'),(1,'R')]:
        # Full-depth sealed optical well, seated inside the common frame.
        def back(u,v,sign=sign):
            x,y,z=lamp_surface(u,v);return sign*x,y+.062,z
        b.skin('Headlamp housing back_'+side,back,24,4,b.m['plastic'],(sign,-1,0),category='lamps',gauge=.002,return_depth=0)
        rings=[]
        for w,h,r,depth in [(.498,.163,.016,.013),(.498,.163,.016,.075),(.492,.157,.013,.075),(.492,.157,.013,.013)]:
            rings.append([(sign*(LAMP_CENTER+x),nose_y(LAMP_CENTER+x,(LAMP_BOTTOM+LAMP_TOP)/2+z)+depth,(LAMP_BOTTOM+LAMP_TOP)/2+z) for x,z in rounded(w,h,r,5 if b.high else 3)])
        b.add(G.ring_loft('Headlamp well walls_'+side,rings,b.m['plastic']),category='lamps')
        x=sign*.552;z=1.161;yf=nose_y(x,z)+.025;yb=yf+.045
        b.add(G.lathe('Headlamp reflector_'+side,[(yb,.014),(yb,.025),(yf,.058),(yf,.057),(yb+.001,.014)],b.m['chrome'],32 if b.high else 20,axis='Y',center=(x,z),closed=True),category='lamps')
        b.add(G.lathe('Projector optic_'+side,[(yf-.004,0),(yf-.001,.041),(yf+.004,.047),(yf+.010,.041),(yf+.013,0)],b.m['lens'],32 if b.high else 20,axis='Y',center=(x,z)),category='lamps')
        b.add(G.lathe('Projector emitter_'+side,[(yb-.004,0),(yb-.004,.018),(yb,.018),(yb,0)],b.m['headlight'],16,axis='Y',center=(x,z)),category='lamps')
        for k in range(4):
            xx=.675+k*.043;zz=1.143
            box(b,'Headlamp lateral reflector_'+side+str(k),(sign*xx,nose_y(xx,zz)+.029,zz),(.037,.022,.060),b.m['chrome'],'lamps',radius=.005)
        # Keep the accepted light-guide section and powered state; stretch its
        # original open angular signature around the new low, wide aperture.
        uv=[(.08,.85),(.40,.85),(.82,.85),(.94,.75),(.94,.26),(.86,.15),(.35,.15),(.16,.23)]
        path=[]
        for a,c in zip(uv,uv[1:]):
            for t in samples(3)[:-1]:
                u,v=[a[k]+(c[k]-a[k])*t for k in range(2)];xx,y,zz=lamp_surface(u,v);path.append((sign*xx,y+.016,zz))
        xx,y,zz=lamp_surface(*uv[-1]);path.append((sign*xx,y+.016,zz))
        tube(b,'Alder running signature_'+side,path,.008,b.m['drl'],'lamps',sides=6)
        xx,y,zz=lamp_surface(.96,.50)
        box(b,'Amber side marker_'+side,(sign*xx,y+.008,zz),(.010,.020,.065),b.m['amber'],'lamps',radius=.003)
    # Deep lamellae span beneath the two lamp pockets, supported at both ends.
    for k,z in enumerate([.888,.944,.999]):
        loops=[]
        for x in [-.924,-.90,-.875,-.845,-.805,-.760,-.5,0,.5,.760,.805,.845,.875,.90,.924]:
            y=nose_y(x,z)+.080
            loops.append([(x,y+dy,z+dz) for dy,dz in [(0,-.010),(0,.010),(.027,.007),(.027,-.007)]])
        b.add(G.loft('Alder grille lamella_'+str(k),loops,b.m['chrome']),category='grille')
    for sign in [-1,1]:
        x=sign*.916;z=.944
        box(b,'Grille end mount_'+str(sign),(x,nose_y(x,z)+.074,z),(.030,.044,.162),b.m['frame'],'grille',radius=.002)
    # The repeating fine perforations remain relief on the original map.
    for name,x0,x1,z0,z1 in [('lower',-.910,.910,.856,1.019),('upper',-.354,.354,1.018,1.244)]:
        # Curve/split the field at the same X stations as its surrounding frame.
        xs=sorted(set([x0,x1]+[s*v for s in [-1,1] for v in [.760,.805,.845,.875,.90] if x0<s*v<x1]))
        for i,(lo,hi) in enumerate(zip(xs,xs[1:])):
            corners=[(x,nose_y(x,z)+.116,z) for x,z in [(lo,z0),(hi,z0),(hi,z1),(lo,z1)]]
            ob=print_quad(b,'Alder grille field_'+name+str(i),corners,b.m['grille'],'grille')
            uv=ob.data.uv_layers.active
            for f in ob.data.polygons:
                for li in f.loop_indices:
                    p=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=((p.x+.915)/1.83,(p.z-.855)/.39)
        b.skin('Grille cavity_'+name,lambda u,v,x0=x0,x1=x1,z0=z0,z1=z1:(x0+(x1-x0)*u,nose_y(x0+(x1-x0)*u,z0+(z1-z0)*v)+.128,z0+(z1-z0)*v),20,2,b.m['frame'],(0,-1,0),category='grille',gauge=.002,return_depth=0)
    box(b,'Alder grille badge',(0,nose_y(0,1.135)+.083,1.135),(.253,.023,.064),b.m['plastic'],'grille',radius=.008)
    y=nose_y(0,1.135)+.069
    print_quad(b,'Alder front badge',[(-.117,y,1.113),(.117,y,1.113),(.117,y,1.157),(-.117,y,1.157)],b.m['badge'],'grille')
