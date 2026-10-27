"""Original swept Alder nose: separate grille, wrapped optics and formed bumper.

The crown/rake lives in forms.py. This module builds closed manufacturing
sections rather than bending a perforated plate. Fine mesh/optic detail stays
in source materials for the eventual normal bake.
"""
import math
from mathutils import Vector
from kit import model as G
from kit.vehicle import samples
from forms import nose_y,nose_corner,hood_z,lamp_surface,lamp_point,lamp_limits,fair
from detail_helpers import box,tube,print_quad

TOP=1.305
BOTTOM=.795
DEPTH=.080


def grille_outline(inset,steps):
    """Matched rounded trapezoid stations, with 70 mm face land."""
    slope=(.607-.548)/(TOP-BOTTOM)
    shift=inset*math.sqrt(1+slope*slope)
    w=.607-inset*slope-shift;bottom=.548+inset*slope-shift
    z0=BOTTOM+inset;z1=TOP-inset
    from body import rounded_polygon
    return rounded_polygon([(-bottom,z0),(bottom,z0),(w,z1),(-w,z1)], [.045]*4,steps)


def frame(b):
    outer=grille_outline(0,5 if b.high else 3)
    inner=grille_outline(.070,5 if b.high else 3)
    # Crown stations are essential on the long upper/lower lands. A single
    # polygon across the width would interpolate a flat chord over the nose.
    dense=[[],[]]
    for j in range(len(outer)):
        count=max(1,math.ceil(max(math.dist(path[j],path[(j+1)%len(path)]) for path in [outer,inner])/.10))
        for path,dst in zip([outer,inner],dense):
            a,c=path[j],path[(j+1)%len(path)]
            dst.extend(tuple(a[k]+(c[k]-a[k])*i/count for k in range(2)) for i in range(count))
    outer,inner=dense
    loops=[]
    for t,depth in [(0,.065),(0,.007),(.07,.001),(.28,-.003),(.76,-.003),(1,.006),(1,.080)]:
        loop=[]
        for a,c in zip(outer,inner):
            x,z=[a[k]+t*(c[k]-a[k]) for k in range(2)]
            loop.append((x,nose_y(x,z)+depth,z))
        loops.append(loop)
    mat=b.m['dark_chrome'] if b.detail else b.m['body']
    ob=G.smooth(G.ring_loft('Fascia shared frame',loops,mat),75)
    b.add(ob,category='nose')


def build_form(b):
    frame(b)
    for sign,side in [(-1,'L'),(1,'R')]:
        # Two stamped corner fields leave a real optical aperture. Both end
        # on the accepted fender boundary; no side section is resculpted.
        for name in ['lower','upper']:
            def cheek(u,v,name=name,sign=sign):
                lo,hi=lamp_limits(u)
                if name=='lower':z=.798+(lo-.002-.798)*v
                else:
                    top=1.305+(hood_z(.984,-2.499)-.0045-1.305)*fair((u-.70)/.30)
                    z=hi+.002+(top-hi-.002)*v
                # The lower pressing follows the grille's sloping edge, with
                # a covered mounting overlap, instead of leaving a 40 mm dark
                # slot beside a rectangular cheek.
                inner=.548+(z-BOTTOM)*(.607-.548)/(TOP-BOTTOM)-.004 if name=='lower' else .598
                x,y=nose_corner(u,z,inner=inner)
                return sign*x,y,z
            b.skin('Fascia body '+name+'_'+side,cheek,30,6,b.m['body'],(sign,-1,0),category='nose',
                   gauge=.0009,return_depth=.006,us=samples(30 if b.high else 15))
        def lens(u,v,sign=sign):
            x,y,z=lamp_surface(u,v);return sign*x,y,z
        b.skin('Headlamp envelope_'+str(sign),lens,36,6,b.m['lens'],(sign,-1,0),category='lamp_forms',
               gauge=.0026,return_depth=0,us=sorted(set(samples(36 if b.high else 18)+[.014,.028,.972,.986])))
    bumper_form(b)


def bumper_form(b):
    """250 mm press-formed beam, plate pocket and a separate textured valance."""
    # Continuous crown except for the license-plate pocket. The half contours
    # continue 180 mm around the corners toward the wheel openings.
    def surface(u,z):
        sign=1 if u>=.5 else -1
        x,y=nose_corner(abs(2*u-1),z,inner=0,bumper=True)
        return sign*x,y,z
    zs=[.540,.553,.565,.580,.610,.685,.744,.766,.780,.790] if b.high else [.540,.565,.580,.685,.766,.790]
    # Split only at the actual plate aperture, 346 x 180 mm.
    edge=.173/.950*.70
    for name,a,c in [('left',0,(1-edge)/2),('right',(1+edge)/2,1)]:
        sign=-1 if name=='left' else 1
        b.skin('Front bumper '+name,lambda u,z,a=a,c=c:surface(a+(c-a)*u,z),26,8,b.m['body'],(sign,-1,0),
               category='bumpers',gauge=.0025,return_depth=.025,vs=zs,us=samples(26 if b.high else 11))
    for name,zs0 in [('lower',[.540,.553,.565,.580]),('upper',[.764,.780,.790])]:
        b.skin('Front bumper '+name,lambda u,z:surface((1-edge)/2+edge*u,z),8,4,b.m['body'],(0,-1,0),
               category='bumpers',gauge=.0025,return_depth=.035,vs=zs0)
    # Pressed pocket floor and returns are behind the visible beam, not a
    # floating plate holder applied to its front.
    box(b,'Bumper plate pocket',(0,-2.875,.672),(.346,.028,.184),b.m['bumper'],'bumpers',radius=.010)
    def shelf(u,v):
        x,y,z=surface(u,.790)
        a=surface(u-.0001,.790);c=surface(u+.0001,.790)
        dx=c[0]-a[0];dy=c[1]-a[1];length=math.hypot(dx,dy)
        return x-.105*v*dy/length,y+.105*v*dx/length,z
    b.skin('Bumper upper return_F',shelf,48,3,b.m['body'],(0,0,1),category='bumpers',gauge=.0025,return_depth=0)
    # Mounting ears connect the cosmetic beam skin to the accepted crash beam.
    # Follow the curved skin at their front edge; a straight box would poke
    # through its crown. Each is a closed 8 mm plate, twelve game triangles.
    for sign in [-1,1]:
        def bracket(u,v,sign=sign):
            x=.390+.080*u
            _,front=nose_corner(.70*x/.950,.665,inner=0,bumper=True)
            return sign*x,front+.0015+(-2.797-front-.0015)*v,.665
        b.skin('Front bumper beam bracket_'+str(sign),bracket,2,2,b.m['frame'] if b.detail else b.m['bumper'],
               (0,0,1),category='bumpers',gauge=.008,return_depth=0,us=[0,1],vs=[0,1])
    # Broad intake and two recovery-hook slots, separated by molded webs.
    def valance(u,z):
        x,y,_=surface(u,.540)
        return x*.98,y+.025+(.540-z)*.25,z
    for name,a,c in [('left',0,.30),('right',.70,1),('web_L',.325,.37),('web_R',.63,.675)]:
        sign=-1 if name in ['left','web_L'] else 1
        b.skin('Lower valance '+name,lambda u,z,a=a,c=c:valance(a+(c-a)*u,z),16,3,b.m['bumper'],(sign,-1,0),
               category='bumpers',gauge=.003,return_depth=.018,vs=[.440,.452,.525,.535])
    for name,z0,z1 in [('lower',.440,.458),('upper',.520,.535)]:
        b.skin('Lower valance '+name,lambda u,v,z0=z0,z1=z1:valance(.30+.40*u,z0+(z1-z0)*v),24,2,b.m['bumper'],(0,-1,0),
               category='bumpers',gauge=.003,return_depth=.018)
    box(b,'Valance intake shadow',(0,-2.797,.489),(.685,.008,.080),b.m['frame'],'bumpers',radius=.002)
    for z in [.475,.499]:
        box(b,'Valance intake louver_'+str(z),(0,-2.829,z),(.668,.030,.008),b.m['plastic'],'bumpers',radius=.002)


def optic(b,name,profile,material,u,sign,segments=24):
    """Local optical axis follows the protective cover's plan normal."""
    p=Vector(lamp_surface(u,.5));a=Vector(lamp_surface(u-.001,.5));c=Vector(lamp_surface(u+.001,.5))
    tangent=(c-a).normalized();tangent.z=0;tangent.normalize();inward=Vector((-tangent.y,tangent.x,0))
    ob=G.lathe(name,profile,material,segments,axis='Y')
    for v in ob.data.vertices:
        q=p+tangent*v.co.x+inward*v.co.y+Vector((0,0,v.co.z));q.x*=sign;v.co=q
    if sign<0:
        for face in ob.data.polygons:face.flip()
    return b.add(ob,category='lamps')


def details(b):
    for sign,side in [(-1,'L'),(1,'R')]:
        def back(u,v,sign=sign):
            x,y,z=lamp_point(u,v,.082);return sign*x,y,z
        b.skin('Headlamp housing back_'+side,back,30,4,b.m['plastic'],(sign,-1,0),category='lamps',gauge=.002,return_depth=0)
        # Seal all four edges of the curving, tapering lens, with 3 mm gauge.
        uv=[(u,0) for u in samples(36 if b.high else 18)]+[(1,v) for v in samples(4)[1:]]
        uv += [(u,1) for u in reversed(samples(36 if b.high else 18)[:-1])]+[(0,v) for v in reversed(samples(4)[1:-1])]
        loops=[]
        for shrink,depth in [(0,.009),(0,.084),(.018,.084),(.018,.009)]:
            loop=[]
            for u,v in uv:
                u=u*(1-shrink*2)+shrink;v=v*(1-shrink*5)+shrink*2.5
                x,y,z=lamp_point(u,v,depth)
                loop.append((sign*x,y,z))
            loops.append(loop)
        b.add(G.ring_loft('Headlamp well walls_'+side,loops,b.m['plastic']),category='lamps')
        optic(b,'Headlamp reflector_'+side,[(.076,.014),(.076,.025),(.021,.056),(.020,.055),(.077,.014)],b.m['chrome'],.22,sign,32 if b.high else 20)
        optic(b,'Projector optic_'+side,[(.010,0),(.013,.037),(.019,.043),(.028,.040),(.031,0)],b.m['lens'],.22,sign,32 if b.high else 20)
        optic(b,'Projector emitter_'+side,[(.068,0),(.068,.018),(.072,.018),(.072,0)],b.m['headlight'],.22,sign,16)
        # A broad faceted reflector cup, recessed into the outer optical well.
        rings=[]
        for w,h,depth in [(.118,.070,.028),(.058,.030,.074),(.052,.025,.077),(.115,.067,.030)]:
            ring=[]
            for dx,dz in G.rounded_rectangle(w,h,.009,3 if b.high else 2):
                u=.55+dx/.49;x,y,z=lamp_point(u,.5,depth)
                ring.append((sign*x,y,z+dz))
            rings.append(ring)
        b.add(G.ring_loft('Headlamp lateral reflector_'+side,rings,b.m['chrome']),category='lamps')
        # Retain the accepted 16 mm guide and emission power, following the
        # new cover's outline instead of putting a rectangular guide in a box.
        signature=[(.04,.84),(.32,.84),(.65,.84),(.91,.79),(.96,.64),(.96,.30),(.88,.17),(.56,.16),(.18,.16),(.06,.24)]
        path=[]
        for a,c in zip(signature,signature[1:]):
            for t in samples(4 if b.high else 3)[:-1]:
                u,v=[a[k]+(c[k]-a[k])*t for k in range(2)];x,y,z=lamp_point(u,v,.018);path.append((sign*x,y,z))
        x,y,z=lamp_point(*signature[-1],.018);path.append((sign*x,y,z))
        tube(b,'Alder running signature_'+side,path,.008,b.m['drl'],'lamps',sides=6)
        x,y,z=lamp_point(.91,.50,.017)
        box(b,'Amber side marker_'+side,(sign*x,y,z),(.010,.026,.036),b.m['amber'],'lamps',radius=.003)
    # Four dark structural blades cross one full-height central opening. Fine
    # diamond relief behind them is the original generated normal-map input.
    for k,z in enumerate([.900,.990,1.080,1.170]):
        half=.553-(z-.795)*.14
        loops=[]
        for x in [-half,-half+.014,-.30,0,.30,half-.014,half]:
            y=nose_y(x,z)+.080
            loops.append([(x,y+dy,z+dz) for dy,dz in [(0,-.010),(0,.010),(.030,.008),(.030,-.008)]])
        b.add(G.loft('Alder grille lamella_'+str(k),loops,b.m['dark_chrome']),category='grille')
    for sign in [-1,1]:
        # Swept backing rails intersect all blade ends and the surround return.
        loops=[]
        for z in [.865,.900,.990,1.080,1.170,1.235]:
            x=sign*(.553-(z-.795)*.14)
            loops.append([(x+dx,nose_y(x,z)+dy,z) for dx,dy in [(-.016,.065),(.016,.065),(.016,.110),(-.016,.110)]])
        b.add(G.loft('Grille end mount_'+str(sign),loops,b.m['frame']),category='grille')
    # The closed cavity is bounded by the inner return, rather than two
    # disconnected fields separated by a lamp-sized web.
    contour=grille_outline(.069,5 if b.high else 3)
    inner=grille_outline(.071,5 if b.high else 3)
    loops=[[(x,nose_y(x,z)+d,z) for x,z in path] for path,d in [(contour,.078),(contour,.135),(inner,.135),(inner,.078)]]
    b.add(G.ring_loft('Grille cavity',loops,b.m['frame']),category='grille')
    back=G.profile('Grille cavity back',inner,.135,.137,b.m['frame'],axis='Y')
    for v in back.data.vertices:v.co.y+=nose_y(v.co.x,v.co.z)
    b.add(back,category='grille')
    # Slightly smaller field in front of the cavity's black back. A fan is
    # sufficient at this density; the small crown is smooth across the front.
    boundary=grille_outline(.072,5 if b.high else 3)
    vs=[(0,nose_y(0,1.05)+.124,1.05)]+[(x,nose_y(x,z)+.124,z) for x,z in boundary]
    ob=b.add(G.mesh('Alder grille field',vs,[(0,i+1,(i+1)%len(boundary)+1) for i in range(len(boundary))],b.m['grille']),category='grille')
    ob['allow_boundary']=True  # Original relief print over the solid cavity back.
    uv=ob.data.uv_layers.new(name='Original relief')
    for li,loop in enumerate(ob.data.loops):
        p=ob.matrix_world@ob.data.vertices[loop.vertex_index].co;uv.data[li].uv=((p.x+.54)/1.08,(p.z-.865)/.37)
    box(b,'Alder grille badge',(0,nose_y(0,1.080)+.057,1.080),(.205,.027,.052),b.m['plastic'],'grille',radius=.007)
    y=nose_y(0,1.080)+.042
    print_quad(b,'Alder front badge',[(-.095,y,1.062),(.095,y,1.062),(.095,y,1.098),(-.095,y,1.098)],b.m['badge'],'grille')
