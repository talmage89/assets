"""Section-built stamped pickup shell, split at real panel reveals.

Near-planar ruled patches share one cross-section field. Tight shoulder support
bands are sampled explicitly; arch flares are bounded to their formed lip.
"""
import math
from kit import model as G
from kit.vehicle import samples
import pickup_spec as S
from forms import blend,section,side_x,arch_floor,shoulder_z,hood,hood_z,nose_y,roof,windshield,backlight,bilinear


def build(b):
    gap=S.PANEL_GAP
    arch_us=[(1-math.cos(math.pi*i/48))/2 for i in range(49)]
    hood_p=G.pivot('Hood',(0,S.HOOD_REAR,1.420),'X',(-62,0));hood_p.parent=b.root
    # Explicit transverse supports around the center rise: the large fields stay planar.
    hx=sorted(set([0,.25,.45,.455-.006,.455,.455+.006,.510-.006,.510,.510+.006,.550-.006,.550,.550+.006,.75,.90]))
    hu=sorted(set([.5+x/1.8 for x in hx]+[.5-x/1.8 for x in hx]))
    b.skin('Hood outer',hood,32,12,b.m['body'],(0,0,1),hood_p,'hood',us=hu)
    b.skin('Roof crown',roof,32,20,b.m['body'],(0,0,1),category='cab',return_depth=.006)
    b.skin('Windshield',windshield,20,8,b.m['glass'],(0,-1,1),category='glass',gauge=.0048,return_depth=0)
    b.skin('Windshield header',lambda u,v:tuple(a+(c-a)*v for a,c in zip(windshield(u,1),roof(u,0))),24,4,b.m['body'],(0,-1,1),category='cab',return_depth=.008)
    b.skin('Rear glass',backlight,18,8,b.m['glass'],(0,1,0),category='glass',gauge=.0048,return_depth=0)

    def side_panel(name,ya,yb,cap,sign,parent,category,axle=None):
        def lower(u,v):
            y=ya+(yb-ya)*u
            low=arch_floor(y,axle,S.ARCH_RADIUS+.067) if axle is not None else S.ROCKER+.013
            high=shoulder_z(y)-.027;z=low+(high-low)*v
            return sign*side_x(y,z,False),y,z
        lower_us=samples(6)
        if axle is not None:
            radius=S.ARCH_RADIUS+.067;a0=math.asin((S.ROCKER-S.ARCH_Z)/radius)
            ys=[axle+radius*math.cos(a0+(math.pi-2*a0)*u) for u in arch_us]
            lower_us=sorted(set([0,1]+[(y-ya)/(yb-ya) for y in ys if ya<y<yb]))
        b.skin(name,lower,70 if axle is not None else 6,18,b.m['body'],(sign,0,0),parent,category,
               us=lower_us,vs=[0,.025,.09,.22,.45,.72,1],return_depth=0 if axle is not None else .012)
        # Fixed section heights around the character line, shared across panels.
        # A separate upper quad strip prevents a variable arch grid from moving it.
        knots=[-.027,-.008,-.003,0,.003,.009,.012,.015]
        def upper(u,v):
            y=ya+(yb-ya)*u;h=shoulder_z(y);top=cap(y)
            z=h+v if v<=.015 else h+.015+(top-h-.015)*(v-.015)/(.10-.015)
            return sign*side_x(y,z),y,z
        b.skin(name+' shoulder',upper,8,12,b.m['body'],(sign,0,0),parent,category,vs=knots+[.035,.065,.10],return_depth=.008)

    for side,sign in [('L',-1),('R',1)]:
        yfront=nose_y(.984)
        fend_end=S.DOOR_FRONT-gap/2
        side_panel('Front fender_'+side,yfront,fend_end,lambda y:hood_z(.984,y),sign,b.root,'fenders',S.FRONT_AXLE)
        def fender_top(u,v):
            x=.9045+(.984-.9045)*u
            fy=nose_y(x);y=fy+(S.HOOD_REAR-fy)*v
            return sign*x,y,hood_z(x,y)
        b.skin('Fender shoulder_'+side,fender_top,8,30,b.m['body'],(0,0,1),category='fenders',return_depth=.008)
        for end,ya,yb,tl,tr in [('F',S.DOOR_FRONT+gap/2,S.DOOR_SPLIT-gap/2,(-.703,1.907),(-.05725,1.907)),
                              ('R',S.DOOR_SPLIT+gap/2,S.DOOR_REAR,(-.05275,1.907),(.865,1.907))]:
            pivot=G.pivot('Door_'+end+side,(sign*.944,ya,1.04),'Z',((-72,0) if sign==1 else (0,72)))
            pivot.parent=b.root;pivot['checkpoint_only']=True
            side_panel('Door skin_'+end+side,ya,yb,lambda y:S.BELT,sign,pivot,'doors')
            outer=[(ya,S.BELT),(yb,S.BELT),tr,tl]
            inner=[(ya+.057,S.BELT+.035),(yb-.038,S.BELT+.035),
                   (tr[0]-.036,tr[1]-.035),(tl[0]+.035,tl[1]-.035)]
            def loop(quad,r,inset=0):
                return [(sign*(side_x(y,z,False)-inset),y,z)
                        for u,v in G.rounded_rectangle(1,1,r,8 if b.high else 5)
                        for y,z in [bilinear(quad,u+.5,v+.5)]]
            sash=G.loft('Door sash_'+end+side,[loop(outer,.020,.009),loop(outer,.020),loop(inner,.055),loop(inner,.055,.009)],b.m['body'],caps=False)
            sol=sash.modifiers.new('Sash gauge','SOLIDIFY');sol.thickness=.0009;sol.offset=-1
            G.smooth(sash,35);b.add(sash,pivot,'doors')
            perimeter=loop(inner,.055,.006)
            # Plane through the side-glass section; preserve true tumblehome.
            x0=side_x(0,1.45,False);slope=(side_x(0,1.88,False)-x0)/.43
            perimeter=[(sign*(x0+slope*(z-1.45)-.006),y,z) for _,y,z in perimeter]
            cy=sum(q[1] for q in perimeter)/len(perimeter);cz=sum(q[2] for q in perimeter)/len(perimeter)
            verts=[(sign*(x0+slope*(cz-1.45)-.006),cy,cz)]+perimeter;n=len(perimeter)
            gl=G.mesh('Side glass_'+end+side,verts,[(0,i+1,(i+1)%n+1) for i in range(n)],b.m['glass'])
            sol=gl.modifiers.new('Glass thickness','SOLIDIFY');sol.thickness=.0048;sol.offset=-1
            b.add(gl,pivot,'glass')
        def pillar_a(u,v):
            x,y,z=windshield(1,v)
            outer_y=(S.DOOR_FRONT)*(1-v)+(-.703)*v
            outer_z=S.BELT*(1-v)+1.907*v
            return sign*(x+(side_x(outer_y,outer_z,False)-x)*u),y+(outer_y-y)*u,z+(outer_z-z)*u
        b.skin('A pillar_'+side,pillar_a,5,24,b.m['body'],(sign,-1,0),category='cab',return_depth=.009)
        def pillar_c(u,v):
            z=S.ROCKER+(1.907-S.ROCKER)*v;t=max(0,(z-S.BELT)/(1.907-S.BELT))
            front=.9265-.057*t;rear=1.025-.068*t
            y=front+(rear-front)*u
            return sign*side_x(y,z,False),y,z
        b.skin('Cab rear corner_'+side,pillar_c,5,24,b.m['body'],(sign,0,0),category='cab')
        def rocker(u,v):
            y=S.DOOR_FRONT+(S.DOOR_REAR-S.DOOR_FRONT)*u;z=.538+.026*v
            return sign*(.932+.021*v),y,z
        b.skin('Rocker return_'+side,rocker,24,3,b.m['body'],(sign,0,0),category='cab')
        # Mirrors are coarse silhouette volumes, without glass/hardware detail.
        stem=G.box('Mirror support_'+side,(sign*1.036,-1.16,1.415),(.230,.125,.065),b.m['rubber'],.015,3)
        b.add(stem,b.root,'mirrors')
        mirror=G.box('Mirror envelope_'+side,(sign*1.13936,-1.19,1.505),(.180,.230,.180),b.m['bumper'],.024,4)
        b.add(mirror,b.root,'mirrors');mirror['bounds_exclude']=True;stem['bounds_exclude']=True
        side_panel('Bed outer_'+side,S.BED_OUTER_FRONT,2.844,lambda y:S.BED_TOP,sign,b.root,'bed',S.REAR_AXLE)
        def rail(u,v):
            y=S.BED_OUTER_FRONT+(2.844-S.BED_OUTER_FRONT)*v
            return sign*(.832+(.958-.832)*u),y,S.BED_TOP+.003
        b.skin('Bed rail_'+side,rail,6,32,b.m['body'],(0,0,1),category='bed',gauge=.0012,return_depth=.016)
        b.skin('Bed inner_'+side,lambda u,v:(sign*.832,S.BED_FRONT+S.BED_LENGTH*u,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),18,5,b.m['bed'],(-sign,0,0),category='bed',return_depth=0)
        tub=G.box('Bed wheelhouse_'+side,(sign*.744,S.REAR_AXLE,1.015),(.203,.99,.22),b.m['bed'],.065,4);b.add(tub,b.root,'bed')
        def bed_corner(u,v):
            z=.841+(S.BED_TOP-.841)*v
            return sign*(.863+(.984-.863)*u),2.847,z
        b.skin('Bed rear corner_'+side,bed_corner,6,10,b.m['body'],(0,1,0),category='bed')
        # Vertical taillamp form volumes locate the rear corners; no optics yet.
        lamp=G.box('Taillamp envelope_'+side,(sign*.922,2.850,1.182),(.122,.034,.395),b.m['glass'],.012,3)
        b.add(lamp,b.root,'lamp_forms')
        for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            # Structured annular quad cage: a planar lip and short, fair ramp to
            # the side. Radial supports replace the old displaced rectangular grid.
            ri=S.ARCH_RADIUS;ro=ri+.067
            radial=[ri,ri+.008,ri+.012,ri+.020,ri+.032,ri+.045,ri+.057,ri+.063,ro]
            def flare(u,r,axle=axle):
                a0=math.asin((S.ROCKER-S.ARCH_Z)/r);a=a0+(math.pi-2*a0)*u
                y=axle+r*math.cos(a);z=S.ARCH_Z+r*math.sin(a)
                base=side_x(y,z,False)
                t=max(0,min(1,(r-ri-.012)/.055))
                weight=t**3*(10-15*t+6*t*t)
                strength=blend((z-S.ROCKER)/.155)
                x=base+(1-weight)*strength*(S.WIDTH/2-base)
                return sign*x,y,z
            b.skin('Arch flare_'+end+side,flare,48,8,b.m['body'],(sign,0,0),category='fenders' if end=='F' else 'bed',us=arch_us,vs=radial,return_depth=0)
            # Interior liner stays inside the opening and ends at the rocker,
            # with no vertical black plate protruding below the body silhouette.
            a0=math.asin((S.ROCKER+.015-S.ARCH_Z)/.478)
            def liner(u,v,axle=axle):
                a=a0+(math.pi-2*a0)*u
                return sign*(.650+.325*v),axle+.478*math.cos(a),S.ARCH_Z+.478*math.sin(a)
            b.skin('Wheelwell_'+end+side,liner,48,3,b.m['rubber'],(0,0,-1),category='liners',gauge=.002,return_depth=0)
            outline=[(axle+.478*math.cos(a0),S.ROCKER+.015)]
            outline += [(axle+.478*math.cos(a0+(math.pi-2*a0)*i/32),S.ARCH_Z+.478*math.sin(a0+(math.pi-2*a0)*i/32)) for i in range(1,33)]
            backing=G.profile('Wheelwell inboard_'+end+side,outline,sign*.649-.001,sign*.649+.001,b.m['rubber'],axis='X');b.add(backing,b.root,'liners')
            lip0=math.asin((S.ROCKER-S.ARCH_Z)/S.ARCH_RADIUS)
            def lip(u,v,axle=axle):
                a=lip0+(math.pi-2*lip0)*u;y=axle+S.ARCH_RADIUS*math.cos(a);z=S.ARCH_Z+S.ARCH_RADIUS*math.sin(a)
                base=side_x(y,z,False);x=base+blend((z-S.ROCKER)/.155)*(S.WIDTH/2-base)
                return sign*(x-.016*v),y,z
            b.skin('Arch return_'+end+side,lip,48,2,b.m['body'],(sign,0,-1),category='fenders' if end=='F' else 'bed',us=arch_us,return_depth=0)
    b.skin('Cab rear lower',lambda u,v:((2*u-1)*.932,1.025,S.ROCKER+(1.458-S.ROCKER)*v),18,7,b.m['body'],(0,1,0),category='cab')
    b.skin('Rear upper',lambda u,v:tuple(a+(c-a)*v for a,c in zip(backlight(u,1),roof(u,1))),24,4,b.m['body'],(0,1,0),category='cab')
    b.skin('Cowl',lambda u,v:((2*u-1)*.91,S.HOOD_REAR+.0045+.018*v,1.414+.019*v),18,3,b.m['body'],(0,0,1),category='cab')
    b.skin('Cab floor',lambda u,v:((2*u-1)*.92,S.DOOR_FRONT+(1.025-S.DOOR_FRONT)*v,.565),18,10,b.m['rubber'],(0,0,1),category='cab',return_depth=0)
    b.skin('Pickup bed floor',lambda u,v:((2*u-1)*.832,S.BED_FRONT+S.BED_LENGTH*v,S.BED_FLOOR),18,20,b.m['bed'],(0,0,1),category='bed')
    b.skin('Pickup box front',lambda u,v:((2*u-1)*.832,S.BED_FRONT,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),18,6,b.m['bed'],(0,1,0),category='bed')
    gate=G.pivot('Tailgate',(0,2.824,S.BED_FLOOR),'X',(-90,0));gate.parent=b.root
    b.skin('Tailgate outer',lambda u,v:((2*u-1)*.858,2.847,.841+(S.BED_TOP-.841)*v),24,10,b.m['body'],(0,1,0),gate,'tailgate')
    b.skin('Tailgate inner',lambda u,v:((2*u-1)*.852,S.BED_REAR,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),18,7,b.m['bed'],(0,-1,0),gate,'tailgate')
    b.skin('Tailgate top lip',lambda u,v:((2*u-1)*.858,S.BED_REAR+(2.847-S.BED_REAR)*v,S.BED_TOP+.003),24,3,b.m['body'],(0,0,1),gate,'tailgate',gauge=.0012,return_depth=.015)
    # Front frame around the broad grille and independent headlamp volumes.
    def front_patch(name,x0,x1,zlo,zhi,mat):
        def fn(u,v):
            x=x0+(x1-x0)*u;y=nose_y(x);hi=hood_z(x,y)-.0045 if zhi is None else zhi
            return x,y,zlo+(hi-zlo)*v
        b.skin(name,fn,6 if x1-x0<.4 else 18,4,mat,(0,-1,0),category='nose',return_depth=.014)
    front_patch('Nose brow',-.984,.984,1.245,None,b.m['body'])
    front_patch('Lower fascia',-.984,.984,.797,.836,b.m['body'])
    for side in [-1,1]:
        lo,hi=sorted([side*.60,side*.984]);front_patch('Lower fascia wing_'+str(side),lo,hi,.8405,.967,b.m['body'])
    for sign in [-1,1]:
        lo,hi=sorted([sign*.60,sign*.632]);front_patch('Nose lamp bridge_'+str(sign),lo,hi,.967,1.245,b.m['body'])
        lo,hi=sorted([sign*.924,sign*.984]);front_patch('Nose outer corner_'+str(sign),lo,hi,.967,1.245,b.m['body'])
        lo,hi=sorted([sign*.632,sign*.924]);front_patch('Headlamp lower seat_'+str(sign),lo,hi,.8405,.967,b.m['body'])
        b.skin('Headlamp envelope_'+str(sign),lambda u,v,s=sign:(s*(.6365+.283*u),nose_y(s*(.6365+.283*u))+.006, .9715+.269*v),12,5,b.m['wheel'],(0,-1,0),category='lamp_forms',gauge=.003,return_depth=.010)
    grille=G.box('Grille envelope',(0,-2.829,1.0405),(1.191,.028,.400),b.m['rubber'],.012,3);b.add(grille,b.root,'nose')
    # Front bumper: thin formed swept beam immediately below the fascia, with
    # a supporting upper return and a tapered lower valance; rear is a step tray.
    for end,sgn in [('F',-1),('R',1)]:
        z0,z1=(.565,.792) if sgn<0 else (.590,.832)
        wrap=.180 if sgn<0 else .110
        def bumper(u,v,sgn=sgn,z0=z0,z1=z1,wrap=wrap):
            x=(2*u-1)*.984
            y=sgn*(S.LENGTH/2-wrap*max(0,(abs(x)-.825)/.159)**2-.006*(2*v-1)**2)
            return x,y,z0+(z1-z0)*v
        b.skin('Bumper_'+end,bumper,36,6,b.m['bumper'],(0,sgn,0),category='bumpers',gauge=.0025,return_depth=.055)
        def shelf(u,v,sgn=sgn,z1=z1,wrap=wrap):
            x=(2*u-1)*.984;outer=S.LENGTH/2-wrap*max(0,(abs(x)-.825)/.159)**2-.006
            inner=-nose_y(x)+.007 if sgn<0 else 2.815
            return x,sgn*(outer+(inner-outer)*v),z1
        b.skin('Bumper upper return_'+end,shelf,30,3,b.m['bumper'],(0,0,1),category='bumpers',gauge=.0025,return_depth=0)
    def valance(u,v):
        x=(2*u-1)*(.956-.020*v)
        y=-2.927+.173*max(0,(abs(x)-.825)/.159)**2+.032*v
        return x,y,.565-.110*v
    b.skin('Lower valance',valance,32,4,b.m['rubber'],(0,-1,0),category='bumpers',gauge=.003,return_depth=.030)
