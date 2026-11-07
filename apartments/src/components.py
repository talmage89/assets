"""Visible construction: actual openings, sash, gauged decks, stairs and rails."""
import math
import random
from mathutils import Vector
from geometry import finish_local,label
DARK=(.032,.040,.035)
STEEL=(.045,.052,.046)
ALUM=(.29,.30,.28)


def oriented(m,origin,yaw):
    a=math.radians(yaw);c,s=math.cos(a),math.sin(a)
    m.v=[(origin[0]+x*c-y*s,origin[1]+x*s+y*c,origin[2]+z) for x,y,z in m.v]
    return m


def panel_wall(a,name,width,height,origin,yaw,openings,skin='mixed',band=2.7432,thick=.254,inset_upper=0,edge_insets=(0,0)):
    """Disjoint wall rectangles with true rough openings and gauged reveals."""
    if inset_upper:
        split=height-2.7432;shift=(edge_insets[0]-edge_insets[1])/2
        lo=[q for q in openings if q['z']-q['h']/2<split]
        hi=[dict(q,x=q['x']-shift,z=q['z']-split,w=q['w']+(.40 if q.get('kind')=='door' else 0)) for q in openings if q['z']+q['h']/2>split]
        panel_wall(a,name+'_lower',width,split,origin,yaw,lo,skin,band,thick)
        panel_wall(a,name+'_upper',width-sum(edge_insets),height-split,oriented_point((shift,inset_upper,split),origin,yaw),yaw,hi,'siding' if skin=='mixed' else skin,0,thick)
        cap=a.mesh(name+'_base_flashing',component='flashing')
        cap.box((0,(inset_upper+thick)/2,split-.0125),(width,inset_upper+thick,.025),'Trim',(.10,.095,.08),r=0)
        oriented(cap,origin,yaw).finish();return cap
    m=a.mesh(name,component='wall')
    xs=sorted({-width/2,width/2,*[max(-width/2,min(width/2,o['x']+side*o['w']/2)) for o in openings for side in (-1,1)]})
    zs=sorted({0,height,min(height,band),*[max(0,min(height,o['z']+side*o['h']/2)) for o in openings for side in (-1,1)]})
    # Coincident construction lines can differ by floating arithmetic.
    xs=sorted({round(v,6) for v in xs});zs=sorted({round(v,6) for v in zs})
    filled={}
    for i,(x0,x1) in enumerate(zip(xs,xs[1:])):
        for j,(z0,z1) in enumerate(zip(zs,zs[1:])):
            if min(x1-x0,z1-z0)<1e-6:continue
            x,z=(x0+x1)/2,(z0+z1)/2
            if any(abs(x-o['x'])<o['w']/2-1e-6 and abs(z-o['z'])<o['h']/2-1e-6 for o in openings):continue
            filled[i,j]='Veneer' if skin in ('brick','stone') or (skin=='mixed' and z<band) else 'Siding'
    # A connected gauged shell, not one closed box per grid rectangle. Only
    # rough openings and the wall perimeter receive returns; internal grid
    # boundaries carry no hidden duplicate faces. The same visible surfaces
    # retain their material courses and physical thickness.
    from geometry import ROLES
    indices={}
    def vertex(p):
        if p not in indices:
            indices[p]=len(m.v);m.v.append(p);m.col.append((*a.colors['Siding'],1))
        return indices[p]
    def face(points,role):m.f.append(tuple(vertex(p) for p in points));m.mat.append(ROLES.index(role))
    for (i,j),role in filled.items():
        x0,x1=xs[i:i+2];z0,z1=zs[j:j+2]
        front=[(x0,0,z0),(x1,0,z0),(x1,0,z1),(x0,0,z1)]
        back=[(x,y+thick,z) for x,y,z in front]
        face(front,role);face(list(reversed(back)),role)
        for edge,neighbor in ((0,(i,j-1)),(1,(i+1,j)),(2,(i,j+1)),(3,(i-1,j))):
            if neighbor in filled:continue
            nxt=(edge+1)%4;face([front[edge],back[edge],back[nxt],front[nxt]],role)
    oriented(m,origin,yaw).finish();return m


def window(a,name,p,w=1.524,h=1.2192,yaw=0,seed=1,replacement=False,slider=False,masonry=False,vinyl=False,reveal=0):
    rng=random.Random(seed);x,y,z=p
    m=a.mesh(name,component='window');frame=a.colors['Trim'] if replacement or vinyl else ALUM
    # Perimeter aluminum extrusion with a recessed glazing pocket and deep sill.
    for xx in (-w/2,w/2):m.box((xx,0,0),(.038,.10,h+.06),'Trim',frame,r=.001)
    for zz in (-h/2,h/2):m.box((0,0,zz),(w,.10,.035),'Trim',frame,r=.001)
    m.box((0,-.035,-h/2-.03),(w+.11,.18,.035),'Trim',frame,r=.001)
    m.box((0,-.013,0),(.035,.075,h),'Trim',frame,r=.001)
    if reveal:
        for sx in (-1,1):m.box((sx*(w/2+.05),reveal/2+.025,0),(.05,reveal,h+.08),'Trim',a.colors['Trim'],r=0)
        for sz in (-1,1):m.box((0,reveal/2+.025,sz*(h/2+.04)),(w+.15,reveal,.05),'Trim',a.colors['Trim'],r=0)
    # Four panes on replacement double-hungs, paired horizontal sliders originally.
    if replacement and not slider:m.box((0,-.022,.04),(w,.060,.030),'Trim',frame,r=.001)
    m.box((w*.25 if slider else 0,.026,0),(w*(.5 if slider else 1)-.052,.012,h-.045),'Glass',(.86,.88,.85),r=0)
    # Cheap room boxes sit behind the actual glazing rather than black stickers.
    m.box((0,.55,0),(w+.12,.055,h+.12),'Trim',(.026,.027,.025),r=0)
    curtain=rng.choice(((.40,.37,.28),(.57,.55,.47),(.22,.25,.26),(.43,.37,.31)))
    closed=rng.choice((.25,.55,.83))
    for side in (-1,1):
        for j in range(5):
            xx=side*(w*.5-w*closed*.24)+side*j*w*closed*.09
            ww=w*closed*.10;yl=.12+.022*math.sin(j*2);yr=.12+.022*math.sin((j+1)*2)
            # Thin folded fabric, with a slightly uneven hanging hem. Solid
            # rectangular curtain blocks wasted hidden faces inside the room.
            m.geom([(xx-ww/2,yl,-h/2+.04+.015*math.sin(j)),(xx+ww/2,yr,-h/2+.04+.015*math.sin(j+1)),
                    (xx+ww/2,yr,h/2-.04),(xx-ww/2,yl,h/2-.04)],[(0,1,2,3)],'Trim',curtain)
    # Slatted blinds differ by tenant; horizontal rails remain low-cost.
    if seed%3==0:
        for j in range(int(h/.032)):
            zz=h*.46-j*.032
            m.geom([(-w/2+.04,.085,zz),(w/2-.04,.085,zz),(w/2-.04,.098,zz-.025),(-w/2+.04,.098,zz-.025)],[(0,1,2,3)],'Trim',curtain)
    oriented(m,p,yaw).finish()
    if masonry:
        course=a.mesh(name+'_brick_courses',component='brick_courses')
        course.box((0,.004,h/2+.136),(w+.15,.11,.2032),'Veneer',r=0)
        course.box((0,-.025,-h/2-.068),(w+.15,.17,.0762),'Veneer',r=0)
        oriented(course,p,yaw).finish()
    return m


def door(a,name,p,yaw=0,width=.9144,glass=False,number='',replaced=False,reveal=0):
    """Inward hinged leaf, origin at its vertical hinge; no wall behind leaf."""
    h=2.032
    frame=a.mesh(name+'_casing',component='entry')
    for side in (-1,1):frame.box((side*(width/2+.028),.03,h/2),(.055,.14,h+.06),'Trim',r=.002)
    frame.box((0,.03,h+.035),(width+.11,.14,.07),'Trim',r=.002)
    frame.box((0,-.025,.009),(width+.04,.16,.018),'Concrete',r=.001)
    if reveal:
        for sx in (-1,1):
            start=len(frame.v)
            frame.box((sx*(width/2+.06),.275,h/2),(.06,.55,h+.06),'Trim',r=0)
            # A splayed jamb clears the accepted inward 100 degree swing.
            for index in range(start,len(frame.v)):
                xx,yy,zz=frame.v[index];frame.v[index]=(xx+sx*.25*yy,yy,zz)
        frame.box((0,.275,h+.045),(width+.18,.55,.09),'Trim',r=0)
    frame.box((width/2+.18,-.075,1.78),(.13,.11,.25),'Trim',STEEL,r=.006)
    frame.box((width/2+.18,-.137,1.78),(.09,.017,.16),'Trim',(.66,.57,.35),r=.002)
    oriented(frame,p,yaw).finish()
    light=a.socket(name+'_Light',oriented_point((width/2+.18,-.24,1.78),p,yaw),'engine_light',yaw)
    light['light_kind']='entry';light['render_power_w']=65
    # Create pivot in building local coordinates and rebase moving mesh once.
    ang=math.radians(yaw);hinge=oriented_point((-width/2,.110,0),p,yaw)
    pivot=a.pivot(name,hinge,yaw=0)
    leaf=a.mesh(name+'_leaf',part=pivot.name,component='door_leaf')
    col=(.20,.22,.19) if replaced else a.colors.get('Door',(.10,.13,.11))
    leaf.box((0,.043,h/2+.012),(width-.012,.042,h-.036),'Trim',col,r=.002)
    for zz in (.56,1.44):
        leaf.box((0,.018,zz),(width-.20,.015,.62),'Trim',tuple(c*.85 for c in col),r=.006)
    for zz in (1.0,1.17):leaf.tube([ (width/2-.10,-.01,zz),(width/2-.10,-.025,zz)],.021,'Trim',(.22,.23,.21),sides=10)
    oriented(leaf,p,yaw);finish_local(leaf)
    if number:label(a,number,tuple(oriented_point((width/2+.18,-.15,1.48),p,yaw)),.082)
    return pivot


def oriented_point(p,origin,yaw):
    a=math.radians(yaw);x,y,z=p
    return (origin[0]+x*math.cos(a)-y*math.sin(a),origin[1]+x*math.sin(a)+y*math.cos(a),origin[2]+z)


def sliding(a,name,p,yaw=0,w=1.8288,h=2.032,seed=1):
    window(a,name+'_fixed',p,w,h,yaw,seed,slider=True)
    # Outer sash extrusion clears the fixed center stile by at least 12 mm.
    pivot=a.pivot(name+'_panel',p,slide=True);pivot.rotation_euler.z=math.radians(yaw)
    m=a.mesh(name+'_moving',part=pivot.name,component='slider')
    for xx in (-w*.5+.02,0):m.box((xx,-.085,0),(.030,.033,h-.04),'Trim',ALUM,r=.001)
    for zz in (-h/2+.02,h/2-.02):m.box((-w*.25,-.085,zz),(w*.5,.033,.030),'Trim',ALUM,r=.001)
    # Fixed window's glass is a visual room enclosure; moving sash carries its
    # own pane. Its closed track is offset, never coincident with the fixed glass.
    m.box((-w*.25,-.085,0),(w*.5-.035,.006,h-.065),'Glass',(.86,.88,.85),r=0)
    m.box((-.018,-.11,-.04),(.018,.028,.16),'Trim',DARK,r=.002)
    oriented(m,p,yaw);finish_local(m);pivot['range_m']=(0,w*.43)


def rail(m,a,b,height=1.0668,color=STEEL,balusters=True):
    a,b=Vector(a),Vector(b);length=(b-a).length
    for hh,w in ((.07,.025),(height-.015,.045)):
        m.beam(a+Vector((0,0,hh)),b+Vector((0,0,hh)),w,.028,'Trim',color,r=.001)
    count=math.ceil(length/.1016)
    if balusters:
        for i in range(count+1):
            q=a.lerp(b,i/count);m.beam(q+Vector((0,0,.07)),q+Vector((0,0,height-.035)),.0127,.0127,'Trim',color,r=0)
    for i in range(math.ceil(length/1.5)+1):
        q=a.lerp(b,i/max(1,math.ceil(length/1.5)));m.beam(q,q+Vector((0,0,height)),.038,.038,'Trim',color,r=.001)
        m.box(q+Vector((0,0,.008)),(.10,.10,.016),'Trim',color,r=0)


def balcony(a,name,x,y,z,w=3.3,depth=1.524,sign=-1,seed=0,support_base=0,recessed=False):
    m=a.mesh(name,component='balcony');outer=y+sign*depth;cy=(y+outer)/2
    m.box((x,cy,z-.10),(w,depth,.20),'Concrete',r=.006)
    # Steel posts and beams bear at the slab edges; no floating decks.
    if z>1:
        if not recessed:
            for sx in (-1,1):m.box((x+sx*(w/2-.13),outer-sign*.10,(z-.20+support_base)/2),(.10,.10,z-.20-support_base),'Trim',STEEL,r=.002)
        rail(m,(x-w/2+.04,outer-sign*.04,z),(x+w/2-.04,outer-sign*.04,z))
        if not recessed:
            for sx in (-1,1):rail(m,(x+sx*(w/2-.04),y,z),(x+sx*(w/2-.04),outer,z))
    # Cause-located runoff at slab drips, represented by inset-colored hems.
    for j in range(4):m.box((x-w*.35+j*w*.23,outer+sign*.003,z-.13),(.075,.004,.11),'Concrete',(.18,.185,.16),r=0)
    if seed%3==0:
        # A rental patio chair: 25 mm bent tube, sagged fabric seat.
        for sx in (-.22,.22):
            m.tube([(x+sx,cy-.25,z),(x+sx,cy+.22,z+.45),(x+sx,cy+.28,z+.83)],.0125,'Trim',ALUM,sides=6)
        for sx in (-.22,.22):m.tube([(x+sx,cy+.25,z),(x+sx,cy-.22,z+.45)],.0125,'Trim',ALUM,sides=6)
        m.box((x,cy,z+.40),(.44,.43,.025),'Trim',(.17,.20,.15),r=.008)
        m.box((x,cy+.25,z+.65),(.44,.03,.35),'Trim',(.17,.20,.15),r=.01)
    if seed%4==1:
        m.tube([(x+w*.27,cy,z),(x+w*.27,cy,z+.24)],.16,'Trim',(.21,.105,.055),sides=10)
        for j in range(6):
            t=j*math.tau/6;m.beam((x+w*.27,cy,z+.22),(x+w*.27+.12*math.cos(t),cy+.12*math.sin(t),z+.55),.025,.02,'Trim',(.10,.17,.055),r=0)
    if z>1 and seed%4==0:
        gx=x+w*.25;gy=cy
        for t in (0,2.1,4.2):m.beam((gx+.22*math.cos(t),gy+.22*math.sin(t),z),(gx+.13*math.cos(t),gy+.13*math.sin(t),z+.48),.023,.023,'Trim',ALUM,r=0)
        for lo,hi,r0,r1 in ((.43,.55,.04,.24),(.55,.65,.24,.24),(.65,.78,.24,.03)):
            vs=[(gx+rr*math.cos(k*math.tau/12),gy+rr*math.sin(k*math.tau/12),z+zz) for zz,rr in ((lo,r0),(hi,r1)) for k in range(12)]
            m.geom(vs,[(k,(k+1)%12,(k+1)%12+12,k+12) for k in range(12)],'Trim',(.022,.031,.026))
        m.box((gx,gy,z+.81),(.16,.05,.035),'Trim',(.04,.045,.035),r=.003)
    if z>1 and seed%5==2:
        # Bicycle leans along the inside of the guard; real 32 mm tires,
        # narrow steel tubing and spokes, rather than a painted silhouette.
        by=outer-sign*.20;bx=x-.10;bz=z+.34
        for dx in (-.5,.5):
            m.tube([(bx+dx+.32*math.cos(k*math.tau/16),by,bz+.32*math.sin(k*math.tau/16)) for k in range(17)],.016,'Trim',(.018,.021,.018),sides=5)
        for aa,bb in (((-.5,0),(-.2,.43)),((-.2,.43),(.05,0)),((.05,0),(-.5,0)),((-.2,.43),(.39,.40)),((.39,.40),(.05,0)),((.39,.40),(.5,0))):
            m.beam((bx+aa[0],by,bz+aa[1]),(bx+bb[0],by,bz+bb[1]),.026,.026,'Trim',(.12,.045,.025),r=0)
        m.box((bx-.18,by,bz+.46),(.23,.13,.035),'Trim',(.025,.027,.02),r=0)
    m.finish()


def stairs(a,name,p,floor_height,levels,steel=True,width=1.1176,reverse=False):
    """Two closed-riser flights, 8 risers each; landings leave an open stairwell."""
    rise=floor_height/16;going=.2794;n=8;run=7*going;landing=1.2192;flights=[]
    for f in range(levels-1):
        m=a.mesh(f'{name}_{f}',component='stairs');base=f*floor_height
        for leg in range(2):
            xx=p[0]+leg*(width+.20);z0=p[2]+base+leg*floor_height/2
            def point(i):return (xx,p[1]+(i*going if leg==0 else run-i*going),z0+i*rise)
            for j in range(8):
                y=p[1]+(j*going if leg==0 else run-j*going);top=z0+(j+1)*rise
                # Concrete-filled steel pans: horizontal pan and closed riser.
                m.box((xx,y,top-.027),(width,going+.024,.054),'Concrete',r=.002)
                front=y-going/2 if leg==0 else y+going/2
                m.box((xx,front,top-rise/2),(width,.013,rise),'Trim',STEEL,r=0)
            for sx in (-1,1):
                x=xx+sx*(width/2+.035)
                aa=(x,p[1]-.12 if leg==0 else p[1]+run+.12,z0-.10)
                bb=(x,p[1]+run+.12 if leg==0 else p[1]-.12,z0+floor_height/2-.10)
                m.beam(aa,bb,.065,.18,'Trim',STEEL,r=.002)
                # Sloped guard with graspable handrail at 914 mm, 38 mm diameter.
                a0=Vector((x,aa[1],z0+rise));b0=Vector((x,bb[1],z0+floor_height/2))
                rail(m,a0,b0,height=1.0668)
                m.tube([a0+Vector((0,0,.9144)),b0+Vector((0,0,.9144))],.01905,'Trim',STEEL,sides=8)
            flights.append(dict(name=m.name,first=(xx,p[1] if leg==0 else p[1]+run,z0+rise),last=(xx,p[1]+run if leg==0 else p[1],z0+floor_height/2),tread=.2794,risers=8,width=width))
        # Half-level landing beyond both flights; top landing in front.
        m.box((p[0]+(width+.20)/2,p[1]+run+landing/2+.14,p[2]+base+floor_height/2-.07),(2*width+.20,landing,.14),'Concrete',r=.003)
        m.box((p[0]+(width+.20)/2,p[1]-landing/2-.14,p[2]+base+floor_height-.07),(2*width+.20,landing,.14),'Concrete',r=.003)
        landing_guards=[(p[1]+run+landing+.14,p[2]+base+floor_height/2)]
        if not reverse:landing_guards.append((p[1]-landing-.14,p[2]+base+floor_height))
        for yy,zz in landing_guards:
            rail(m,(p[0]-width/2,yy,zz),(p[0]+1.5*width+.20,yy,zz))
        # Bearing columns and landing edge beams extend to real ground.
        for xx in (p[0]-width/2-.03,p[0]+1.5*width+.23):
            m.box((xx,p[1]+run+landing*.65,(p[2]+base+floor_height/2)/2),(.09,.09,p[2]+base+floor_height/2),'Trim',STEEL,r=.002)
        if reverse:
            if f==0:m.box((p[0]+(width+.20)/2,p[1]-.38,p[2]/2),(2.55,.80,p[2]),'Concrete',r=.002)
            m.v=[(x,2*p[1]-y,z) for x,y,z in m.v]
        m.finish()
    if reverse:
        for row in flights:
            for key in ('first','last'):
                x,y,z=row[key];row[key]=(x,2*p[1]-y,z)
    return flights


def meters(a,name,p,count=12,yaw=0):
    m=a.mesh(name,component='meters')
    for j in range(count):
        x=(j%6-2.5)*.33;z=.95+(j//6)*.57
        m.box((x,0,z),(.25,.15,.38),'Trim',(.28,.29,.26),r=.008)
        m.tube([(x,-.09,z+.05),(x,-.15,z+.05)],.087,'Trim',ALUM,sides=12)
        m.tube([(x,-.155,z+.05),(x,-.159,z+.05)],.066,'Glass',(.63,.68,.64),sides=12)
        m.tube([(x,.045,z+.19),(x,.045,2.25)],.012,'Trim',ALUM,sides=6)
    m.box((0,.04,2.3),(2.07,.11,.18),'Trim',(.28,.29,.26),r=.003)
    m.tube([(-1.16,.035,.02),(-1.16,.035,2.30),(0,.035,2.30)],.035,'Trim',ALUM,sides=10)
    oriented(m,p,yaw).finish()
