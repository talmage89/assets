"""Apartment site construction and immutable original-library landscaping."""
import math
import random
from geometry import Assembly,label
from buildings import garden_building
from components import rail,STEEL
from plans import FT,transform
from context import instance


def rectangle(m,x0,x1,y0,y1,z,role,col):
    if x1<x0:x0,x1=x1,x0
    if y1<y0:y0,y1=y1,y0
    nx=max(1,math.ceil((x1-x0)/1.25));ny=max(1,math.ceil((y1-y0)/1.25))
    # Shared vertices provide a continuous macro field; no patch edges or
    # independent tile tints. Fine mineral relief stays in the Ground maps.
    vs=[(x0+(x1-x0)*i/nx,y0+(y1-y0)*j/ny,z) for j in range(ny+1) for i in range(nx+1)]
    fs=[]
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1))
    m.geom(vs,fs,role,col)


def mailbox(a,p):
    m=a.mesh('Cluster_mailbox',component='site')
    x,y,z=p
    m.box((x,y,z+.06),(2.7,1.8,.12),'Concrete',r=.008)
    for sx in (-.58,.58):m.box((x+sx,y,z+.65),(.11,.13,1.15),'Trim',STEEL,r=.003)
    m.box((x,y,z+1.26),(1.66,.49,.89),'Trim',(.27,.30,.26),r=.015)
    for j in range(4):
        for i in range(4):
            xx=x+(i-1.5)*.40;zz=z+.95+j*.19
            m.box((xx,y-.253,zz),(.38,.018,.17),'Trim',(.35,.37,.32),r=.002)
            m.tube([(xx+.13,y-.268,zz),(xx+.13,y-.272,zz)],.010,'Trim',ALUM if False else (.15,.16,.14),sides=6)
    m.finish();label(a,'MAIL',(x,y-.28,z+1.75),.12)


def dumpster(a,p):
    x,y,z=p;m=a.mesh('Dumpster_enclosure',component='site')
    m.box((x,y,.08),(5.4,4.6,.16),'Concrete',r=.01)
    # Three original fence panels bound a service pad; front remains truck clear.
    for sx in (-1,1):instance('fence',a.root,'Dumpster_side_'+str(sx),(x+sx*2.45,y,0),90,select='Section_A')
    for i in (-1,1):instance('fence',a.root,'Dumpster_back_'+str(i),(x+i*1.2192,y+2.1,0),0,select='Section_A')
    for xx in (x-2.45,x,x+2.45):instance('fence',a.root,'Dumpster_post_'+str(xx),(xx,y+2.1,0),select='Post_Line')
    # Folded steel body with skids, fork pockets and two hinged molded lids.
    loops=[]
    for zz,w,d in ((.22,2.15,1.35),(1.45,2.35,1.55),(1.45,2.32,1.52),(.24,2.12,1.32)):
        loops.append([(x-w/2,y-d/2,zz),(x+w/2,y-d/2,zz),(x+w/2,y+d/2,zz),(x-w/2,y+d/2,zz)])
    # Skin is gauged; bottom and rim close it without a hidden solid box.
    from kit import model as G
    ob=G.ring_loft('Welded dumpster skin',loops,a.materials[4]);ob.parent=a.root
    attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for v in attr.data:v.color=(.055,.16,.105,1)
    for sx in (-1,1):
        m.box((x+sx*.72,y,.24),(.12,1.30,.16),'Trim',STEEL,r=.003)
        m.box((x+sx*1.2,y,.88),(.12,.72,.16),'Trim',(.055,.16,.105),r=.002)
        pivot=a.pivot('Dumpster_lid_'+str(sx),(x+sx*.59,y+.78,1.48));pivot['pivot_axis']='X';pivot['range_degrees']=(-95,0)
        mm=a.mesh('Dumpster_lid_'+str(sx),part=pivot.name,component='door_leaf')
        mm.box((x+sx*.59,y,1.50),(1.16,1.61,.055),'Trim',(.025,.031,.023),r=.016)
        from geometry import finish_local
        finish_local(mm)
    m.finish()


def carport(a,stalls):
    for i in range(0,min(16,len(stalls)),4):
        group=stalls[i:i+4];x=sum(q['x'] for q in group)/len(group);y=group[0]['y'];width=len(group)*9*FT
        m=a.mesh('Carport_'+str(i),component='carport')
        for sx in (-1,1):
            for sy in (-1,1):m.box((x+sx*(width/2-.23),y+sy*2.05,1.35),(.10,.10,2.70),'Trim',STEEL,r=.002)
        for sx in (-1,1):m.beam((x+sx*(width/2-.23),y-2.60,2.75),(x+sx*(width/2-.23),y+2.60,2.94),.10,.17,'Trim',r=.001)
        m.prism([(x-width/2,y-2.9,2.75),(x+width/2,y-2.9,2.75),(x+width/2,y+2.9,2.96),(x-width/2,y+2.9,2.96)],(0,0,-1),.045,'Trim',(.39,.38,.31))
        for j in range(round(width/.30)):m.beam((x-width/2+j*.30,y-2.9,2.78),(x-width/2+j*.30,y+2.9,2.99),.018,.016,'Trim',(.30,.30,.26),r=0)
        m.finish()


def amenity(a,kind,p):
    x,y,z=p;m=a.mesh('Amenity_'+kind,component='site')
    if kind=='pool':
        for sy in (-1,1):m.box((x,y+sy*4,.08),(14,2,.16),'Concrete',r=.01)
        for sx in (-1,1):m.box((x+sx*6,y,.08),(2,6,.16),'Concrete',r=.01)
        # A real open pool bowl; water stays below the coping, no floating slab.
        m.box((x,y,-1.1),(10.2,6.2,.18),'Concrete',(.40,.55,.55),r=0)
        for sx in (-1,1):m.box((x+sx*5.0,y,-.50),(.20,6.2,1.2),'Concrete',(.40,.55,.55),r=.01)
        for sy in (-1,1):m.box((x,y+sy*3.,-.5),(10.0,.20,1.2),'Concrete',(.40,.55,.55),r=.01)
        rectangle(m,x-4.9,x+4.9,y-2.9,y+2.9,-.09,'Glass',(.12,.33,.34))
        rail(m,(x-6.6,y-4.6,.16),(x+6.6,y-4.6,.16),1.22)
        # Pool access opens away from the water onto its connected site walk.
        for lo,hi in ((-6.6,-.74),(.74,6.6)):
            rail(m,(x+lo,y+4.6,.16),(x+hi,y+4.6,.16),1.22)
        hinge=a.pivot('Pool_gate',(x-.64,y+4.6,.16));hinge['range_degrees']=(0,100)
        gate=a.mesh('Pool_gate_leaf',part=hinge.name,component='gate')
        for zz in (.23,1.365):gate.beam((x-.64,y+4.6,zz),(x+.64,y+4.6,zz),.035,.028,'Trim',STEEL,r=.001)
        for dx in (-.64,.64):gate.beam((x+dx,y+4.6,.23),(x+dx,y+4.6,1.38),.035,.028,'Trim',STEEL,r=.001)
        for j in range(1,13):
            xx=x-.64+j*1.28/13;gate.beam((xx,y+4.6,.23),(xx,y+4.6,1.365),.0127,.0127,'Trim',STEEL,r=0)
        from geometry import finish_local
        finish_local(gate)
        for zz in (.42,1.15):m.box((x-.69,y+4.6,zz),(.10,.035,.045),'Trim',STEEL,r=.002)
        m.box((x+.70,y+4.6,1.30),(.08,.045,.07),'Trim',STEEL,r=.002)
        for sx in (-1,1):rail(m,(x+sx*6.6,y-4.6,.16),(x+sx*6.6,y+4.6,.16),1.22)
    elif kind=='playground':
        rectangle(m,x-6,x+6,y-4,y+4,.01,'Siding',(.16,.115,.065))
        for sx in (-1,1):
            m.beam((x+sx*2.1,y-1.3,0),(x+sx*2.1,y,2.6),.065,.065,'Trim',(.20,.10,.035))
            m.beam((x+sx*2.1,y+1.3,0),(x+sx*2.1,y,2.6),.065,.065,'Trim',(.20,.10,.035))
        m.beam((x-2.2,y,2.6),(x+2.2,y,2.6),.075,.075,'Trim',(.20,.10,.035))
        for dx in (-.9,.9):
            for sx in (-1,1):m.tube([(x+dx+sx*.20,y,2.60),(x+dx+sx*.20,y+.05,1.4),(x+dx+sx*.20,y,.52)],.007,'Trim',STEEL,sides=6)
            m.box((x+dx,y,.50),(.52,.23,.04),'Trim',(.018,.027,.023),r=.008)
    m.finish()


def make_complex(p):
    a=Assembly('Complex_'+str(p['seed']));a.root['site_kind']='complex';W,D=p['lot'];rng=random.Random(p['seed']+91);wear_rng=random.Random(p['seed']+1921)
    for b in p['buildings']:garden_building(p['building'],b['id'],a.root,b['origin'],b['yaw'],a.materials)
    ground=a.mesh('Private_paving',component='site')
    # Ground library road construction and curbs carry the site; stalls are
    # private additions with the same measured nine-by-eighteen-foot grammar.
    instance('ground',a.root,'Parking_road',(0,0,-.172),90,select='Road_Straight_A',scale=(1,(W-8)/6.096,1))
    for sy in (-1,1):
        rectangle(ground,-W/2+4,W/2-4,sy*4.05,sy*9.54,.0,'Shingles',(.070,.073,.069)) if sy>0 else rectangle(ground,-W/2+4,W/2-4,-9.54,-4.05,0,'Shingles',(.070,.073,.069))
        # Curb top and path meet without buried lawn or duplicate walk panels.
        instance('ground',a.root,'Parking_curb_'+str(sy),(0,sy*9.54,-.008),90 if sy<0 else 270,select='Curb_Straight',scale=(1,(W-8)/3.048,1))
        ground.box((0,sy*10.42,.065),(W-8,1.524,.13),'Concrete',r=.002)
    for j,s in enumerate(p['stalls']):
        x,y=s['x'],s['y'];sy=1 if y>0 else -1
        # Thin paint has no visible side wall. Missing chips follow the wheel
        # crossings, with long retained runs beside the parked vehicle.
        for sx in (-1,1):
            xx=x+sx*4.5*FT
            for k in range(7):
                lo=y-9*FT+k*18*FT/7;hi=lo+18*FT/7
                gap=.03+(.17 if k in (0,1,5) else .015)*wear_rng.random()
                if (j*7+k*3+int(sx))%31==0:continue
                ground.geom([(xx-.043,lo+gap,.001),(xx+.043,lo+gap*.7,.001),(xx+.043,hi-.035,.001),(xx-.043,hi-.055,.001)],[(0,1,2,3)],'Trim',(.52,.51,.40))
        ground.box((x,y+sy*2.18,.09),(1.72,.15,.17),'Concrete',(.33,.32,.285),r=.016)
        rng.random()  # Preserve the deterministic placement sequence.
    # Utility patches and routed seals stay in the wearing course and share
    # the asphalt material/metric charts; no glossy alpha film or new maps.
    for j,(xx,yy,ww,dd) in enumerate(((-W*.28,6.7,2.1,3.8),(W*.21,-6.2,2.7,2.9),(-W*.12,-5.7,1.6,2.4))):
        ground.geom([(xx-ww/2,yy-dd/2,.002),(xx+ww/2,yy-dd/2+.18,.002),(xx+ww/2-.12,yy+dd/2,.002),(xx-ww/2+.15,yy+dd/2-.08,.002)],[(0,1,2,3)],'Shingles',(.047,.049,.047))
    for j in range(12):
        xx=-W/2+12+j*(W-24)/12;yy=wear_rng.choice((-1,1))*wear_rng.uniform(4.5,8.8)
        pts=[(xx+.11*k+.18*math.sin(k*1.7+j),yy+(k-3)*.35,.003) for k in range(7)]
        for q,r in zip(pts,pts[1:]):
            dx,dy=r[0]-q[0],r[1]-q[1];ll=math.hypot(dx,dy);ox,oy=-dy/ll*.022,dx/ll*.022
            ground.geom([(q[0]+ox,q[1]+oy,q[2]),(q[0]-ox,q[1]-oy,q[2]),(r[0]-ox,r[1]-oy,r[2]),(r[0]+ox,r[1]+oy,r[2])],[(0,1,2,3)],'Shingles',(.020,.022,.021))
    # Main walk branches terminate on actual building walk sockets.
    for b in p['buildings']:
        for module in p['building']['modules']:
            local=transform((0,-p['building']['depth']/2-1.5,0),module['origin'],module['yaw'])
            q=transform(local,b['origin'],b['yaw']);sy=1 if q[1]>0 else -1;end=sy*11.18
            ground.box((q[0],(q[1]+end)/2,.065),(1.524,abs(q[1]-end)+.10,.13),'Concrete',r=.002)
    # Two curbed planted end islands and a real drive to the parcel edge.
    ground.box((-W/2+4,-D/4,-.025),(7.32,D/2,.10),'Shingles',(.070,.073,.069),r=0)
    for sx in (-1,1):
        xx=sx*(W/2-6)
        for sy in (-1,1):
            yy=sy*6.7932
            ground.box((xx,yy,.06),(3.30,5.48,.12),'Concrete',(.29,.28,.24),r=.12)
            ground.box((xx,yy,.123),(3.0,5.18,.015),'Siding',(.075,.12,.035),r=0)
            instance('shrub',a.root,'Island_shrub_'+str(sx)+str(sy),(xx,yy,.13),sx*31+sy*12)
    if p['amenity']!='none':
        ax=W/2-12;ay=-D/2+11+(4.6 if p['amenity']=='pool' else 4)
        ground.box((ax,(ay-11.18)/2,.065),(1.524,-11.18-ay,.13),'Concrete',r=.002)
    # Disjoint native lawn regions omit buildings, slabs, walks and the pool.
    # This keeps turf out of sunken bowls and avoids whole-site buried faces.
    excluded=[(-W/2,W/2,-11.2,11.2),(-W/2,-W/2+8,-D/2,0)]
    for bb in p['buildings']:
        for module in p['building']['modules']:
            w0,d0=p['building']['width'],p['building']['depth']
            corners=[transform(transform((xx,yy,0),module['origin'],module['yaw']),bb['origin'],bb['yaw']) for xx in (-w0/2-1.5,w0/2+.4) for yy in (-d0/2-1.8,d0/2+1.8)]
            excluded.append((min(q[0] for q in corners),max(q[0] for q in corners),min(q[1] for q in corners),max(q[1] for q in corners)))
            q=transform(transform((0,-d0/2-1.5,0),module['origin'],module['yaw']),bb['origin'],bb['yaw']);end=11.2 if q[1]>0 else -11.2
            excluded.append((q[0]-.77,q[0]+.77,min(q[1],end),max(q[1],end)))
    if p['amenity']=='pool':excluded.append((W/2-19,W/2-5,-D/2+6,-D/2+16))
    if p['amenity']!='none':excluded.append((W/2-12-.77,W/2-12+.77,-D/2+15,-11.18))
    excluded.append((W/2-11,W/2-5,D/2-10,D/2-4))
    xs=sorted({-W/2,W/2,*[max(-W/2,min(W/2,q)) for e in excluded for q in e[:2]]})
    ys=sorted({-D/2,D/2,*[max(-D/2,min(D/2,q)) for e in excluded for q in e[2:]]})
    for xi,(x0,x1) in enumerate(zip(xs,xs[1:])):
        for yi,(y0,y1) in enumerate(zip(ys,ys[1:])):
            x,y=(x0+x1)/2,(y0+y1)/2
            if min(x1-x0,y1-y0)<.02 or any(l<x<r and b<y<t for l,r,b,t in excluded):continue
            rectangle(ground,x0,x1,y0,y1,-.008,'Siding',(.075,.115,.035))
    ground.finish()
    # Keep occupancy selective and leave sight lines to construction details.
    used=rng.sample(p['stalls'],min(16,len(p['stalls'])//3))
    for j,s in enumerate(used):
        rt=instance('car',a.root,'Parked_'+str(j),(s['x'],s['y'],0),s['yaw']+(180 if j%4==0 else 0))
        # A few colors are a source material control, no new vehicle shapes.
    trees=[(-W/2+5,-D*.35),(W/2-6,D*.30),(-W/2+6,D*.30),(W/2-7,-D*.34),(-8,D/2-5),(18,D/2-6)]
    for j,(x,y) in enumerate(trees):instance('tree',a.root,'Mature_maple_'+str(j),(x,y,0),j*67)
    for b in p['buildings']:
        for j in range(9):
            x=(j-4)*1.35
            if abs(x)<1.4:continue
            local=transform((x,-p['building']['depth']/2-1.85,0),p['building']['modules'][0]['origin'],p['building']['modules'][0]['yaw'])
            q=transform(local,b['origin'],b['yaw'])
            instance('shrub',a.root,b['id']+'_Foundation_shrub_'+str(j),q,j*43)
    mailbox(a,(-W/2+9,15,0));dumpster(a,(W/2-8,D/2-7,0))
    if p['carports']:carport(a,[s for s in p['stalls'] if s['y']>0][5:17])
    if p['amenity']!='none':amenity(a,p['amenity'],(W/2-12,-D/2+11,0))
    m=a.mesh('Entrance_sign',component='site')
    for sx in (-1,1):m.box((-W/2+10+sx*1.45,-D/2+4,.72),(.20,.20,1.44),'Trim',(.18,.19,.14),r=.004)
    m.box((-W/2+10,-D/2+4,1.35),(3.6,.16,1.05),'Trim',(.09,.13,.09),r=.012);m.finish()
    label(a,p['name'],(-W/2+10,-D/2+4.091,1.43),.24);label(a,'APARTMENTS',(-W/2+10,-D/2+4.091,1.05),.13)
    return a


def row_site(p,a):
    width=p['count']*p['width']+12;d=p['depth'];m=a.mesh('Row_site',component='site')
    # Reserve the public street for the presentation's native Ground road.
    # Turf must not cover its real crown; the row ships its private grounds.
    road=-d/2-11.2
    for lo,hi in ((-d/2-17,road-4.13),(road+4.13,d/2+10)):
        rectangle(m,-width/2,width/2,lo,hi,-.01,'Siding',(.075,.115,.035))
    m.box((0,-d/2-6.3,.065),(width,1.524,.13),'Concrete',r=.002)
    for u in p['units']:
        x,y=u['x'],u['y'];dx=p['width']*.29 if p['garage'] else -p['width']*.29
        m.box((x+dx,-d/2-3+y/2,.066),(1.22,5+y,.13),'Concrete',r=.002)
        if p['garage']:
            xx=x-p['width']*.16;front=-d/2-7.6;back=-d/2+y-1;top=p['base']+u['z']
            m.prism([(xx-1.4,front,.03),(xx+1.4,front,.03),(xx+1.4,back,top),(xx-1.4,back,top)],(0,0,-1),.09,'Concrete')
        # Library privacy fences partition patios. Posts at true bay endpoints.
        if u['index']<p['count']-1:
            xx=x+p['width']/2
            instance('fence',a.root,'Rear_divider_'+str(u['index']),(xx,d/2+y+1.2192,0),90,select='Section_A')
            for yy in (d/2+y,d/2+y+2.4384):instance('fence',a.root,'Divider_post_'+str(xx)+'_'+str(yy),(xx,yy,0),select='Post_End')
        for sx in (-1,1):instance('shrub',a.root,'Row_shrub_'+str(u['index'])+str(sx),(x+sx*p['width']*.30,-d/2-1.7+y,0),u['index']*33)
    m.finish()
    for j,x in enumerate((-width/2+3,width/2-3)):
        instance('tree',a.root,'Row_maple_'+str(j),(x,d/2+6,0),j*70)
    if p['garage']:
        for i in (1,4):
            u=p['units'][i];slope=(p['base']+u['z']-.03)/(6.6+u['y']);zz=.03+slope*(7.6-3.25)
            rt=instance('car',a.root,'Driveway_vehicle_'+str(i),(u['x']-p['width']*.16,-d/2-3.25,zz),0)
            rt.rotation_euler.x=math.atan(slope)
    mailbox(a,(-width/2+2,-d/2-4,0))
