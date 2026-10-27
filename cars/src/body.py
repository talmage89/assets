"""Returned outer sheet panels, cab glazing envelope and open pickup box."""
import math
from kit import model as G
from kit.vehicle import panel,samples
import pickup_spec as S
from forms import side_x,arch_floor,hood,roof,windshield,backlight,bilinear,smoothstep


def build(b):
    gap=S.PANEL_GAP
    hood_p=G.pivot('Hood',(0,S.HOOD_REAR,1.407),'X',(-62,0));hood_p.parent=b.root
    b.skin('Hood outer',hood,32,16,b.m['body'],(0,0,1),hood_p,'hood')
    b.skin('Roof crown',roof,32,18,b.m['body'],(0,0,1),category='cab')
    # Windshield and backlight are closed 4.8 mm form surfaces at this stage.
    b.skin('Windshield',windshield,24,12,b.m['glass'],(0,-1,1),category='glass',gauge=.0048,return_depth=0)
    b.skin('Rear glass',backlight,24,10,b.m['glass'],(0,1,0),category='glass',gauge=.0048,return_depth=0)
    for side,sign in [('L',-1),('R',1)]:
        # Fender top follows the hood edge with an actual 4.5 mm reveal.
        def fender(u,v):
            y=-2.585+(-1.345+2.585)*u
            low=arch_floor(y,S.FRONT_AXLE)
            high=1.248+.144*smoothstep((y-S.HOOD_FRONT)/(S.HOOD_REAR-S.HOOD_FRONT))
            z=low+(high-low)*v
            return sign*side_x(y,z),y,z
        b.skin('Front fender_'+side,fender,58,12,b.m['body'],(sign,0,0),category='fenders')
        def hood_gutter(u,v):
            xx,hy,zz=hood(1,v)
            fy=-2.585+(-1.345+2.585)*v
            fz=1.248+.144*smoothstep((fy-S.HOOD_FRONT)/(S.HOOD_REAR-S.HOOD_FRONT))
            edge=side_x(fy,fz)
            return sign*(xx+gap+(edge-xx-gap)*u),hy+(fy-hy)*u,zz+(fz-zz)*smoothstep(u)
        b.skin('Fender shoulder_'+side,hood_gutter,8,32,b.m['body'],(sign,0,1),category='fenders')
        # Four separate door outers with a shared curvature function on every seam.
        for end,ya,yb,tl,tr in [('F',S.DOOR_FRONT+gap/2,S.DOOR_SPLIT-gap/2,(-1.020,1.905),(-.05725,1.922)),
                              ('R',S.DOOR_SPLIT+gap/2,S.DOOR_REAR,( -.05275,1.922),(.800,1.907))]:
            pivot=G.pivot('Door_'+end+side,(sign*.944,ya,1.04),'Z',((-72,0) if sign==1 else (0,72)))
            pivot.parent=b.root;pivot['checkpoint_only']=True
            def door(u,v,ya=ya,yb=yb):
                y=ya+(yb-ya)*u;z=S.ROCKER+.013+(S.BELT-S.ROCKER-.013)*v
                return sign*side_x(y,z),y,z
            b.skin('Door skin_'+end+side,door,26,14,b.m['body'],(sign,0,0),pivot,'doors')
            # The visible stamped upper sash is a ring, with a genuine window opening.
            outer=[(ya,S.BELT),(yb,S.BELT),tr,tl]
            inner=[(ya+.069,S.BELT+.039),(yb-.046,S.BELT+.039),
                   (tr[0]-.041,tr[1]-.043),(tl[0]+.037,tl[1]-.046)]
            # Rounded stamp corners: same sample count on outer and inner loops,
            # without four independent strips or artificial miters in the sash.
            def loop(quad,r,inset=0):
                pts=[]
                for u,v in G.rounded_rectangle(1,1,r,8 if b.high else 5):
                    y,z=bilinear(quad,u+.5,v+.5)
                    pts.append((sign*(side_x(y,z)-inset),y,z))
                return pts
            outer_loop=loop(outer,.018);inner_loop=loop(inner,.070)
            outer_return=loop(outer,.018,.013);inner_return=loop(inner,.070,.013)
            sash=G.loft('Door sash_'+end+side,[outer_return,outer_loop,inner_loop,inner_return],b.m['body'],caps=False)
            sol=sash.modifiers.new('Sash closed sheet gauge','SOLIDIFY');sol.thickness=.0009;sol.offset=-1
            G.smooth(sash,35);b.add(sash,pivot,'doors')
            # A crowned closed glass fan, inset within the rounded window opening.
            glass_loop=loop(inner,.070,.007)
            x0=side_x(0,1.45);slope=(side_x(0,1.89)-x0)/.44
            glass_loop=[(sign*(x0+slope*(z-1.45)-.007),y,z) for _,y,z in glass_loop]
            cy=sum(p[1] for p in glass_loop)/len(glass_loop);cz=sum(p[2] for p in glass_loop)/len(glass_loop)
            verts=[(sign*(x0+slope*(cz-1.45)-.007),cy,cz)]+glass_loop
            n=len(glass_loop);faces=[(0,i+1,(i+1)%n+1) for i in range(n)]
            glass=G.mesh('Side glass_'+end+side,verts,faces,b.m['glass'])
            sol=glass.modifiers.new('Glass thickness','SOLIDIFY');sol.thickness=.0048;sol.offset=-1
            G.smooth(glass);b.add(glass,pivot,'glass')
        # Cab corners and A pillars: designed independently of any single manufacturer's shape.
        def a_pillar(u,v):
            x,y,z=windshield(1,v)
            sx=side_x(y+.011,z)
            return sign*(x+.009+(sx-x-.009)*u),y+.010*u,z
        b.skin('A pillar_'+side,a_pillar,5,20,b.m['body'],(sign,-1,0),category='cab')
        def c_pillar(u,v):
            z=S.ROCKER+(1.912-S.ROCKER)*v
            t=max(0,(z-S.BELT)/(1.912-S.BELT))
            front=.9265-.122*t
            rear=1.025-.039*min(1,(z-S.ROCKER)/(S.BELT-S.ROCKER))-.111*t
            y=front+(rear-front)*u
            return sign*side_x(y,z),y,z
        b.skin('Cab rear corner_'+side,c_pillar,5,24,b.m['body'],(sign,0,0),category='cab')
        # Roof rails bridge side sashes to the crowned roof edge.
        def rail(u,v):
            y=-1.035+1.910*v;xx,_,zz=roof(1,v)
            z=zz-.022*u;x=xx+(side_x(y,z)-xx)*u
            return sign*x,y,z
        b.skin('Roof rail_'+side,rail,5,32,b.m['body'],(sign,0,1),category='cab')
        def rocker(u,v):
            y=S.DOOR_FRONT+(S.DOOR_REAR-S.DOOR_FRONT)*u
            z=.532+.027*v
            return sign*(.933+.018*math.sin(v*math.pi/2)),y,z
        b.skin('Rocker return_'+side,rocker,32,4,b.m['body'],(sign,0,0),category='cab')
        def bed_side(u,v):
            y=S.BED_OUTER_FRONT+(2.844-S.BED_OUTER_FRONT)*u
            low=arch_floor(y,S.REAR_AXLE);z=low+(S.BED_TOP-low)*v
            return sign*side_x(y,z),y,z
        b.skin('Bed outer_'+side,bed_side,64,15,b.m['body'],(sign,0,0),category='bed')
        def bed_corner(u,v):
            z=S.ROCKER+(S.BED_TOP-S.ROCKER)*v
            x=.8625+(side_x(2.844,z)-.8625)*u
            return sign*x,2.847-.003*u,z
        b.skin('Bed rear corner_'+side,bed_corner,5,14,b.m['body'],(0,1,0),category='bed')
        # Rolled rail over the open double-wall box (not a solid block).
        def bed_rail(u,v):
            y=S.BED_OUTER_FRONT+(2.844-S.BED_OUTER_FRONT)*v
            outer=side_x(y,S.BED_TOP);x=.832+(outer-.832)*u
            return sign*x,y,S.BED_TOP+.007*math.sin(math.pi*u)
        b.skin('Bed rail_'+side,bed_rail,8,48,b.m['body'],(0,0,1),category='bed')
        def bed_inner(u,v):
            y=S.BED_FRONT+(S.BED_REAR-S.BED_FRONT)*u;z=S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v
            return sign*.832,y,z
        b.skin('Bed inner_'+side,bed_inner,24,6,b.m['bed'],(-sign,0,0),category='bed',return_depth=0)
        # Wheel tubs consume real bed-floor space; inner width 50.6 inches between tubs.
        tub=G.box('Bed wheelhouse_'+side,(sign*.744,S.REAR_AXLE,1.015),(.203,.99,.22),b.m['bed'],.09,5)
        b.add(tub,b.root,'bed')
        # Plain dark wheel-well envelopes establish the air volume behind the tires.
        for end,axle in [('F',S.FRONT_AXLE),('R',S.REAR_AXLE)]:
            def liner(u,v,axle=axle):
                a=math.pi*u;y=axle+.508*math.cos(a);z=S.ARCH_Z+.508*math.sin(a)
                return sign*(.653+.330*v),y,z
            b.skin('Wheelwell_'+end+side,liner,50,3,b.m['rubber'],(0,0,-1),category='liners',gauge=.002,return_depth=0)
            # Close the inboard liner: a side view must see a dark wheel well,
            # never the studio background through the tire-to-arch clearance.
            outline=[(axle-.508,.280),(axle+.508,.280)]
            outline += [(axle+.508*math.cos(math.pi*i/32),S.ARCH_Z+.508*math.sin(math.pi*i/32)) for i in range(33)]
            backing=G.profile('Wheelwell inboard_'+end+side,outline,sign*.649-.001,sign*.649+.001,b.m['rubber'],axis='X')
            b.add(backing,b.root,'liners')
            # Narrow stamped arch lip turns back into the liner opening.
            a0=math.asin((S.ROCKER-S.ARCH_Z)/S.ARCH_RADIUS)
            def lip(u,v,axle=axle):
                a=a0+(math.pi-2*a0)*u
                y=axle+S.ARCH_RADIUS*math.cos(a);z=S.ARCH_Z+S.ARCH_RADIUS*math.sin(a)
                return sign*(side_x(y,z)-.018*v),y,z
            b.skin('Arch return_'+end+side,lip,48,2,b.m['body'],(sign,0,-1),category='fenders' if end=='F' else 'bed',return_depth=0)
    # Firewall and rear cab wall are structural body volumes, not an interior proxy.
    b.skin('Cab rear lower',lambda u,v:((2*u-1)*.932,1.025-.049*v,S.ROCKER+(1.463-S.ROCKER)*v),24,10,b.m['body'],(0,1,0),category='cab')
    for name,quad in [('Rear upper',[(-.88,.873,1.902),(.88,.873,1.902),(.85,.885,1.936),(-.85,.885,1.936)]),
                      ('Cowl',[(-.938,-1.343,1.413),(.938,-1.343,1.413),(.903,-1.389,1.430),(-.903,-1.389,1.430)])]:
        b.skin(name,lambda u,v,q=quad:bilinear(q,u,v),24,3,b.m['body'],(0,0,1),category='cab')
    b.skin('Cab floor',lambda u,v:((2*u-1)*.92,-1.34+2.36*v,.565),20,16,b.m['rubber'],(0,0,1),category='cab',return_depth=0)
    b.skin('Pickup bed floor',lambda u,v:((2*u-1)*.832,S.BED_FRONT+S.BED_LENGTH*v,S.BED_FLOOR),20,24,b.m['bed'],(0,0,1),category='bed')
    b.skin('Pickup box front',lambda u,v:((2*u-1)*.832,S.BED_FRONT,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),24,8,b.m['bed'],(0,1,0),category='bed')
    # Tailgate is a crowned stamped panel with a separate lower hinge root.
    gate=G.pivot('Tailgate',(0,2.824,S.BED_FLOOR),'X',(-90,0));gate.parent=b.root
    def tailgate(u,v):
        x=(2*u-1)*.858;z=.843+(S.BED_TOP-.843)*v
        y=2.839+.008*(1-(2*u-1)**2)+.006*math.sin(math.pi*v)
        return x,y,z
    b.skin('Tailgate outer',tailgate,30,14,b.m['body'],(0,1,0),gate,'tailgate',return_depth=.035)
    b.skin('Tailgate inner',lambda u,v:((2*u-1)*.852,S.BED_REAR,S.BED_FLOOR+(S.BED_TOP-S.BED_FLOOR)*v),24,10,b.m['bed'],(0,-1,0),gate,'tailgate')
    # Nose at this checkpoint is deliberately unpierced; grille/lights wait for form approval.
    def nose(u,v):
        z=.774+(hood(u,0)[2]-.0045-.774)*v
        x=(2*u-1)*side_x(-2.585,z)
        y=-2.7895+.2045*abs(2*u-1)**4-.009*math.sin(math.pi*v)
        return x,y,z
    b.skin('Front fascia form',nose,32,16,b.m['body'],(0,-1,0),category='nose')
    # Swept bumper envelopes: rounded plan corners and real separate construction.
    for end,sgn in [('F',-1),('R',1)]:
        def bumper(u,v,sgn=sgn):
            x=(2*u-1)*.984;z=(.43 if sgn<0 else .595)+(.34 if sgn<0 else .235)*v
            y=sgn*(S.LENGTH/2-(.200 if sgn<0 else .060)*abs(2*u-1)**6-.017*(2*v-1)**2)
            return x,y,z
        b.skin('Bumper_'+end,bumper,40,8,b.m['bumper'],(0,sgn,0),category='bumpers',gauge=.0025,return_depth=.085)
        def bumper_top(u,v,sgn=sgn):
            x=(2*u-1)*.984
            outer=S.LENGTH/2-(.200 if sgn<0 else .060)*abs(2*u-1)**6-.017
            inner=2.780-.200*abs(2*u-1)**4 if sgn<0 else 2.817
            y=sgn*(outer+(inner-outer)*v)
            return x,y,.769 if sgn<0 else .829
        b.skin('Bumper upper return_'+end,bumper_top,32,3,b.m['bumper'],(0,0,1),category='bumpers',gauge=.0025,return_depth=0)
