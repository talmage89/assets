"""School construction: gauged masonry, sash pockets, bent roofs and leaves.

Fine mortar, normal-map fabrication and causal aging belong to the next
checkpoint. There are no decorative mesh bricks or modeled screw threads.
"""
import math,random,json
from geometry import Assembly,ROLES,orient,label
from plans import WALL,PART,BAY,FT,sides,world,visible_intervals,wall_sections

DARK=(.022,.027,.025)
ALUM=(.34,.36,.34)


def wall_panel(a,name,origin,yaw,width,z0,z1,openings,skin='Veneer',thick=WALL):
    """Connected front/back skin with returns only at boundaries/openings."""
    m=a.mesh(name,component='wall')
    xs=sorted({round(v,7) for v in [0,width,*[max(0,min(width,o['u']+s*o['w']/2)) for o in openings for s in (-1,1)]]})
    zs=sorted({round(v,7) for v in [z0,z1,*[max(z0,min(z1,o['z']+q*o['h'])) for o in openings for q in (0,1)]]})
    filled=set()
    for i,(l,r) in enumerate(zip(xs,xs[1:])):
        for j,(b,t) in enumerate(zip(zs,zs[1:])):
            u,z=(l+r)/2,(b+t)/2
            if not any(abs(u-o['u'])<o['w']/2-1e-6 and o['z']-1e-6<z<o['z']+o['h']+1e-6 for o in openings):filled.add((i,j))
    vertices={}
    def vertex(q):
        if q not in vertices:vertices[q]=len(m.v);m.v.append(q);m.col.append((*a.colors[skin],1))
        return vertices[q]
    def face(points):m.f.append(tuple(vertex(v) for v in points));m.mat.append(ROLES.index(skin))
    for i,j in sorted(filled):
        l,r=xs[i:i+2];b,t=zs[j:j+2]
        if min(r-l,t-b)<1e-6:continue
        f=[(l,0,b),(r,0,b),(r,0,t),(l,0,t)];back=[(x,y+thick,z) for x,y,z in f]
        face(f);face(back[::-1])
        for k,neighbor in enumerate(((i,j-1),(i+1,j),(i,j+1),(i-1,j))):
            if neighbor not in filled:face([f[k],back[k],back[(k+1)%4],f[(k+1)%4]])
    ob=orient(m,origin,yaw).finish()
    if ob:ob['wall_gauge_m']=thick;ob['openings']=json.dumps(openings)
    return ob


def glazing(a,b,o,index):
    u,z,w,h=o['u'],o['z']+.1524,o['w'],o['h'];origin=(*o['origin'],0)
    m=a.mesh(b['id']+'_Sash_'+str(index),component='sash')
    replacement=o.get('replacement',False);frame=ALUM if replacement else (.105,.115,.103)
    # 50 mm mullions, an inset pocket and 2 mm steel angle over the opening.
    for xx in (-w/2,w/2):m.box((u+xx,.085,z+h/2),(.050,.115,h+.05),'Trim',frame,r=.002)
    for zz in (z,z+h):m.box((u,.085,zz),(w,.115,.050),'Trim',frame,r=.002)
    panes=max(1,round(w/1.20));pitch=w/panes
    for i in range(1,panes):m.box((u-w/2+i*pitch,.084,z+h/2),(.043,.105,h-.05),'Trim',frame,r=.001)
    transom=.58 if b['era']<1970 else .46
    zz=z+h-transom
    m.box((u,.074,zz),(w,.12,.043),'Trim',frame,r=.001)
    for i in range(panes):
        x=u-w/2+(i+.5)*pitch
        for row,(lo,hi) in enumerate(((z+.026,zz-.0215),(zz+.0215,z+h-.026))):
            if b['kind']=='cluster' and row==0:
                m.box((x,.102,lo+.175),(pitch-.05,.022,.35),'Trim',(.46,.46,.40))
                m.box((x,.075,lo+.36),(pitch-.04,.08,.025),'Trim',frame)
                lo+=.375
            if o.get('infill') and (row==1 or i in (0,panes-1)):
                m.box((x,.109,(lo+hi)/2),(pitch-.05,.025,hi-lo),'Trim',(.36,.36,.285),r=0)
            else:
                # Gauged glass leaves reflections and a room beyond; geometry
                # is simple at this gate but never an opaque blue rectangle.
                m.box((x,.109,(lo+hi)/2),(pitch-.05,.006,hi-lo),'Glass',(.80,.86,.83),r=0)
            if row==0 and i%2==0:
                m.box((x,.052,lo+.16),(.10,.025,.018),'Trim',frame,r=.001)
                m.box((x,.11,lo+.15),(pitch-.10,.027,.018),'Trim',frame,r=0)
    # Steel lintel and precast sill project beyond actual rough opening.
    m.box((u,-.025,z+h+.07),(w+.20,.06,.052),'Trim',(.12,.13,.115),r=0)
    m.prism([(u-w/2-.10,-.145,z-.04),(u+w/2+.10,-.145,z-.04),(u+w/2+.10,.20,z-.015),(u-w/2-.10,.20,z-.015)],(0,0,-1),.065,'Concrete',(.34,.34,.30))
    # Interior reveals expose the separate 4in brick / cavity / block build-up.
    for xx in (-w/2-.025,w/2+.025):m.box((u+xx,.225,z+h/2),(.045,.16,h+.05),'Concrete',(.42,.42,.35),r=0)
    # A recessed room end, floor/ceiling returns and selectively lowered blinds
    # give different window responses without final material randomness.
    depth=1.45
    m.box((u,depth,z+h/2),(w+.15,.08,h+.20),'Concrete',(.105,.115,.095),r=0)
    for sz in (z-.04,z+h+.06):m.box((u,(depth+.28)/2,sz),(w+.12,depth-.28,.04),'Concrete',(.31,.30,.25),r=0)
    rng=random.Random(index+b['era']*17)
    if index%3==1:
        closed=rng.choice((.24,.45,.71))
        for j in range(int(h*closed/.045)):
            zh=z+h-.06-j*.045
            m.geom([(u-w/2+.04,.26,zh),(u+w/2-.04,.26,zh),(u+w/2-.04,.28,zh-.032),(u-w/2+.04,.28,zh-.032)],[(0,1,2,3)],'Trim',(.43,.42,.34))
    orient(m,origin,o['yaw']).finish()


def door(a,b,o,index,glass=False,base=.1524):
    u,w=o['u'],o['w'];h=2.10;origin=(*o['origin'],0);yaw=o['yaw']
    pair=o['type'] in ('entry','double');entry=o['type']=='entry';rough=w
    # Entry opening includes sidelight/transom bays. Door pair stays 2 x 3ft.
    door_w=.9144 if pair else min(1.1176,w-.1524)
    center=u
    m=a.mesh(b['id']+'_DoorFrame_'+str(index),component='frame')
    for s in (-1,1):m.box((u+s*(rough/2-.027),.04,base+o['h']/2),(.054,.18,o['h']),'Trim',r=.002)
    m.box((u,.04,base+o['h']-.03),(rough,.18,.06),'Trim',r=.002)
    m.box((u,-.012,base+.007),(rough,.20,.014),'Trim',ALUM,r=.001)
    if entry:
        for s in (-1,1):
            xx=u+s*(door_w+.062);m.box((xx,.04,base+h/2),(.055,.16,h),'Trim',ALUM,r=.001)
            sw=rough/2-door_w-.08
            m.box((xx+s*(sw/2+.035),.08,base+h/2),(sw,.008,h-.08),'Glass',(.81,.87,.84))
        m.box((u,.04,base+h+.060),(rough,.15,.055),'Trim',ALUM,r=.001)
        m.box((u,.08,base+h+(o['h']-h)/2),(rough-.10,.008,o['h']-h-.08),'Glass',(.81,.87,.84))
    elif pair:
        m.box((u,.04,base+h/2),(.045,.16,h),'Trim',r=.001)
    # A close-coupled wall pack and alarm beside every external assembly.
    m.box((u+rough/2+.22,-.09,base+2.24),(.18,.19,.29),'Trim',DARK,r=.008)
    m.box((u+rough/2+.22,-.192,base+2.20),(.14,.012,.15),'Concrete',(.57,.55,.43),r=.002)
    m.box((u-rough/2-.13,-.026,base+1.52),(.11,.035,.13),'Trim',(.34,.035,.021),r=.003)
    orient(m,origin,yaw).finish()
    leaves=2 if pair else 1
    for j in range(leaves):
        sign=1 if j==0 else -1
        x0=u-door_w-.030 if pair and j==0 else u+door_w+.030 if pair else u-door_w/2
        hinge=world((x0,-.045,base),o['origin'],yaw)
        pivot=a.pivot(b['id']+'_Door_'+str(index)+'_'+str(j),hinge,limits=(-90,0) if sign==1 else (0,90))
        pivot['face_yaw_degrees']=yaw;pivot['leaf_width_m']=door_w;pivot['opening_kind']=o['type']
        leaf=a.mesh(pivot.name+'_Leaf',part=pivot.name,component='door')
        cx=x0+sign*(door_w/2+.004);col=a.colors['Trim']
        if entry or glass:
            # Separate stiles/rails around a real light opening.
            for sx in (-1,1):leaf.box((cx+sx*(door_w/2-.055),-.004,h/2),(.11,.045,h),'Trim',ALUM,r=.002)
            for zz,hh in ((.13,.26),(h-.055,.11)):
                leaf.box((cx,-.004,zz),(door_w-.22,.045,hh),'Trim',ALUM,r=.002)
            leaf.box((cx,.002,(h+.26-.11)/2),(door_w-.22,.008,h-.37),'Glass',(.80,.86,.83))
        else:
            # Vision lite is cut out of a 1-3/4in steel leaf.
            lite_w=.18;lite_h=.46;lite_z=1.57
            for sx in (-1,1):leaf.box((cx+sx*(door_w+lite_w)/4,-.004,h/2),((door_w-lite_w)/2,.04445,h),'Trim',col,r=.0015)
            for lo,hi in ((0,lite_z-lite_h/2),(lite_z+lite_h/2,h)):
                leaf.box((cx,-.004,(lo+hi)/2),(lite_w,.04445,hi-lo),'Trim',col,r=0)
            for sx in (-1,1):leaf.box((cx+sx*(lite_w/2+.013),-.03,lite_z),(.026,.016,lite_h+.05),'Trim',ALUM,r=.001)
            for sz in (-1,1):leaf.box((cx,-.03,lite_z+sz*(lite_h/2+.013)),(lite_w,.016,.026),'Trim',ALUM,r=.001)
            leaf.box((cx,.003,lite_z),(lite_w,.006,lite_h),'Glass',(.72,.80,.76))
        leaf.box((cx,-.03,.17),(door_w-.10,.006,.29),'Trim',ALUM,r=.001)
        # Exterior pull, inside panic bar with two solid stand-offs, 3 hinges,
        # overhead closer and actual paired elbow arms.
        handle=cx+sign*(door_w/2-.14)
        leaf.tube([(handle,-.035,.93),(handle,-.085,.96),(handle,-.085,1.20),(handle,-.035,1.23)],.010,'Trim',ALUM,sides=8)
        for sx in (-1,1):leaf.box((cx+sx*(door_w/2-.14),.042,1.01),(.075,.07,.07),'Trim',ALUM,r=.003)
        leaf.box((cx,.082,1.01),(door_w-.24,.045,.055),'Trim',ALUM,r=.006)
        leaf.box((cx,.045,h-.13),(.28,.08,.065),'Trim',ALUM,r=.003)
        leaf.beam((cx,.09,h-.09),(cx+.13,.14,h-.06),.018,.012,'Trim',ALUM,r=0)
        leaf.beam((cx+.13,.14,h-.06),(cx+.32,.07,h-.04),.018,.012,'Trim',ALUM,r=0)
        leaf.v=[(x,y,z+base+.018) for x,y,z in leaf.v]
        orient(leaf,origin,yaw).finish()
        # Cylindrical knuckles stay fixed on the jamb axis. Their intended
        # attachment penetrates the jamb; it is not leaf/casing interference.
        hinges=a.mesh(b['id']+'_DoorHinges_'+str(index)+'_'+str(j),component='hinge')
        for zh in (.22,1.04,1.88):hinges.tube([(x0,-.045,base+.018+zh-.045),(x0,-.045,base+.018+zh+.045)],.0125,'Trim',ALUM,sides=8)
        orient(hinges,origin,yaw).finish()
    if o.get('label') and not entry:
        p=world((u,-.021,base+o['h']+.16),o['origin'],yaw)
        label(a,o['label'],p,.105,yaw=yaw)


def louver(a,b,o,index):
    m=a.mesh(b['id']+'_Louver_'+str(index),component='louver');u,z,w,h=o['u'],o['z']+.1524,o['w'],o['h']
    m.box((u,.20,z+h/2),(w,.04,h),'Trim',DARK)
    for s in (-1,1):
        m.box((u+s*w/2,0,z+h/2),(.055,.10,h+.08),'Trim',ALUM,r=.001)
        m.box((u,0,z+h/2+s*h/2),(w,.10,.055),'Trim',ALUM,r=.001)
    for j in range(int(h/.085)):
        zz=z+.045+j*.085;m.prism([(u-w/2+.035,-.045,zz-.02),(u+w/2-.035,-.045,zz-.02),(u+w/2-.035,.05,zz+.02),(u-w/2+.035,.05,zz+.02)],(0,0,-1),.0015,'Trim',ALUM)
    orient(m,(*o['origin'],0),o['yaw']).finish()


def roof(a,b,p):
    l,r,f,k=b['rect'];z=b['roof'];m=a.mesh(b['id']+'_Roof',component='roof')
    if b.get('gable'):
        # Low-slope roof above each classroom pod, exposed deep fascia.
        mid=(f+k)/2;rise=(k-f)/2/12
        for yy in (f-.65,k+.65):
            m.prism([(l-.65,yy,z),(r+.65,yy,z),(r+.65,mid,z+rise),(l-.65,mid,z+rise)],(0,0,-1),.16,'Shingles')
            for x in (l-.65,r+.65):m.prism([(x,yy,z-.20),(x,mid,z+rise-.20),(x,mid,z+rise),(x,yy,z)],(1,0,0),.045,'Trim',(.18,.19,.145))
            m.box(((l+r)/2,yy,z-.12),(r-l+1.30,.05,.25),'Trim',(.18,.19,.145))
        m.box(((l+r)/2,mid,z+rise+.015),(r-l+1.3,.18,.035),'Trim',ALUM)
        # Solid triangular end infill below the pitched roof.
        for x in (l,r):m.prism([(x,f,z-.01),(x,k,z-.01),(x,mid,z+rise-.16)],(1 if x==l else -1,0,0),WALL,'Veneer')
    else:
        m.box(((l+r)/2,(f+k)/2,z-.08),(r-l,k-f,.16),'Shingles')
        # Coping profile has a folded outside drip, horizontal cap, inside leg.
        for face,o,yaw,length in sides(b):
            for aa,bb,z0,neighbor in wall_sections(b,face,p['blocks']):
                cap=a.mesh(b['id']+'_Coping_'+face+'_'+str(aa),component='coping')
                cap.box(((aa+bb)/2,.11,z+.17),(bb-aa,.32,.035),'Trim',(.27,.28,.245),r=.001)
                cap.box(((aa+bb)/2,-.04,z+.10),(bb-aa,.025,.17),'Trim',(.27,.28,.245),r=.001)
                cap.box(((aa+bb)/2,.25,z+.105),(bb-aa,.025,.14),'Trim',(.27,.28,.245))
                cap.box(((aa+bb)/2,.105,z+.025),(bb-aa,.255,.255),'Veneer' if b['skin']=='brick' else 'Siding')
                for j in range(1,math.ceil((bb-aa)/3.048)):
                    cap.box((aa+j*3.048,.11,z+.191),(.018,.33,.005),'Trim',(.15,.16,.14))
                orient(cap,(*o,0),yaw).finish()
                # Scupper box, open mouth and downspout kept clear of openings.
                if bb-aa>5 and face in ('north','east','west') and neighbor is None:
                    u=aa+.48;dr=a.mesh(b['id']+'_Drain_'+face,component='drainage')
                    dr.box((u,-.072,z-.10),(.22,.03,.13),'Trim',DARK)
                    for sx in (-1,1):dr.box((u+sx*.13,-.18,z-.19),(.025,.25,.20),'Trim',ALUM)
                    dr.box((u,-.18,z-.28),(.26,.25,.025),'Trim',ALUM)
                    dr.tube([(u,-.19,z-.24),(u,-.22,z-.43),(u,-.14,.33),(u,-.40,.18)],.048,'Trim',ALUM,sides=6)
                    for zh in (.6,2.2):dr.box((u,-.15,zh),(.15,.07,.035),'Trim',(.14,.15,.13))
                    dr.box((u,-.46,.085),(.28,.65,.07),'Concrete',r=.008)
                    orient(dr,(*o,0),yaw).finish()
    # Equipment rests on actual raised curbs, with intake/exhaust and conduit.
    if b['kind'] not in ('corridor','boiler'):
        count=2 if max(r-l,k-f)>22 else 1
        for j in range(count):
            x=l+(j+1)*(r-l)/(count+1);y=(f+k)/2+.8;zz=z+(k-f)/2/12 if b.get('gable') else z
            m.box((x,y,zz+.12),(1.65,2.3,.24),'Trim',(.16,.17,.145))
            m.box((x,y,zz+.61),(1.55,2.2,.78),'Trim',(.35,.36,.32),r=.014)
            m.box((x,y,zz+1.02),(1.63,2.27,.055),'Trim',(.27,.28,.25),r=.005)
            for sx in (-1,1):
                for q in range(9):m.box((x+sx*.78,y-.86+q*.20,zz+.59),(.012,.065,.56),'Trim',DARK)
            for sx in (-.37,.37):
                m.tube([(x+sx,y,zz+1.051),(x+sx,y,zz+1.061)],.25,'Trim',DARK,sides=16)
                for q in range(3):
                    ang=q*math.tau/3;m.beam((x+sx,y,zz+1.065),(x+sx+.22*math.cos(ang),y+.22*math.sin(ang),zz+1.065),.035,.018,'Trim',ALUM,r=0)
            m.tube([(x+.5,y+1.1,zz+.24),(x+.5,y+1.6,zz+.10),(x+.5,y+2.2,zz+.10)],.015,'Trim',ALUM,sides=6)
    if b['kind']=='boiler':
        x,y=(l+r)/2,(f+k)/2
        m.box((x,y,z+1.8),(1.05,1.05,3.60),'Veneer')
        m.box((x,y,z+3.64),(1.20,1.20,.14),'Concrete')
        m.box((x,y,z+3.73),(.78,.78,.07),'Trim',DARK)
        m.box((x,y,z+4.03),(1.05,1.05,.055),'Trim',ALUM)
        for sx in (-1,1):m.box((x+sx*.42,y,z+3.9),(.03,.03,.25),'Trim',ALUM)
    if b['kind']=='media':
        x,y=(l+r)/2,(f+k)/2
        m.box((x,y,z+.40),(8.0,3.8,.8),'Siding')
        for sy in (-1,1):
            m.box((x,y+sy*1.906,z+.45),(7.7,.008,.50),'Glass',(.70,.78,.74))
            for dx in range(-3,4):m.box((x+dx,y+sy*1.93,z+.45),(.04,.05,.56),'Trim',ALUM)
        m.box((x,y,z+.86),(8.45,4.25,.12),'Trim',(.16,.17,.135))
    m.finish()


def covered_walk(a,c,index):
    l,r,f,k=c['rect'];z=c['height'];m=a.mesh('Covered_walk_'+str(index),component='covered_walk')
    # Galvanized folded steel deck, fascia, longitudinal channels and joists.
    m.box(((l+r)/2,(f+k)/2,z+.15),(r-l,k-f,.30),'Trim',(.17,.19,.16),r=.005)
    m.box(((l+r)/2,(f+k)/2,z-.018),(r-l-.08,k-f-.08,.035),'Concrete',(.40,.40,.34))
    along_x=r-l>k-f;length=r-l if along_x else k-f
    steps=max(1,math.ceil(length/4.5));narrow=(k-f if along_x else r-l)
    for j in range(steps+1):
        if along_x:x=l+j*(r-l)/steps;y=f+.18
        else:x=l+.18;y=f+j*(k-f)/steps
        if c.get('wall_bearing_end') and j==steps:
            # This link terminates against the later addition's masonry above
            # its door. A wall seat carries the end instead of blocking the
            # doorway with an unsupported choice of column station.
            m.box((x,y,z-.07),(.24,.18,.14),'Trim',ALUM)
            m.beam((l+.10,y,z-.10),(r-.1,y,z-.10),.06,.14,'Trim',r=0)
            continue
        m.box((x,y,.1524+(z-.1524)/2),(.1016,.1016,z-.1524),'Trim',r=.003)
        m.box((x,y,.1674),(.23,.23,.030),'Trim',(.17,.18,.14),r=.002)
        m.box((x,y,z-.035),(.18,.18,.07),'Trim',ALUM,r=.001)
        for sx in (-1,1):
            for sy in (-1,1):m.tube([(x+sx*.077,y+sy*.077,.184),(x+sx*.077,y+sy*.077,.205)],.009,'Trim',ALUM,sides=6)
        if along_x:m.beam((x,f+.10,z-.10),(x,k-.1,z-.10),.06,.14,'Trim',r=0)
        else:m.beam((l+.10,y,z-.10),(r-.1,y,z-.10),.06,.14,'Trim',r=0)
    # Roof columns land on the continuous concrete walk, not floating in turf.
    m.box(((l+r)/2,(f+k)/2,.0762),(r-l+.30,k-f+.30,.1524),'Concrete',r=.004)
    m.finish()


def build_school(p,parent=None):
    a=Assembly('School_'+str(p['seed']),dict(Veneer=p['palette']['brick'],Siding=p['palette']['cmu'],Trim=p['palette']['accent']),parent)
    a.root['seed']=p['seed'];a.root['plan_type']=p['type'];a.root['stage']=p['stage'];a.root['footprint_m']=p['footprint']
    for b in p['blocks']:
        original_brick=a.colors['Veneer']
        if b.get('wall_color'):a.colors['Veneer']=b['wall_color']
        l,r,f,k=b['rect'];base=p['floor'];skin='Veneer' if b['skin']=='brick' else 'Siding'
        for face,o,yaw,length in sides(b):
            holes=[dict(q,z=q['z']+base) for q in b['openings'] if q['face']==face]
            for aa,bb,z0,neighbor in wall_sections(b,face,p['blocks']):
                origin=world((aa,0,0),o,yaw)
                openings=[dict(q,u=q['u']-aa) for q in holes if aa<q['u']<bb]
                ob=wall_panel(a,b['id']+'_'+face,origin,yaw,bb-aa,z0,b['roof']-.17,openings,skin)
                if ob:ob['block_id']=b['id'];ob['era']=b['era']
                # Vertical control joints and the exposed roof deck edge follow
                # construction bays, independent from material tiling repetition.
                m=a.mesh(b['id']+'_'+face+'_Joints',component='joints')
                if neighbor:
                    m.box(((aa+bb)/2,-.025,z0+.23),(bb-aa,.045,.22),'Trim',(.23,.24,.21))
                for j in range(1,math.ceil((bb-aa)/BAY)):
                    x=aa+j*BAY
                    if any(abs(x-q['u'])<q['w']/2+.05 for q in holes):continue
                    m.box((x,-.001,(base+b['roof']-.17)/2),(.012,.009,b['roof']-.17-base),'Trim',(.09,.09,.071))
                if b['kind']=='gym':
                    for j in range(1,math.ceil((bb-aa)/4.5)):
                        x=aa+j*4.5
                        if any(abs(x-q['u'])<q['w']/2+.20 for q in holes):continue
                        m.box((x,-.045,(base+b['roof']-.3)/2),(.20,.12,b['roof']-.3-base),skin,r=.004)
                orient(m,(*o,0),yaw).finish()
        for i,o in enumerate(b['openings']):
            if o['type']=='window':glazing(a,b,o,i)
            elif o['type']=='louver':louver(a,b,o,i)
            else:door(a,b,o,i,glass=o['type']=='entry')
        m=a.mesh(b['id']+'_Slab',component='floor')
        m.box(((l+r)/2,(f+k)/2,base/2),(r-l,k-f,base),'Concrete',(.25,.25,.21))
        # Interior partitions at real classroom module boundaries. They stop
        # at the ceiling; the exterior roof is the actual upper closure.
        ceiling=base+p['ceiling']
        if b['rooms']:
            partitions=set()
            for j,(x0,x1,y0,y1) in enumerate(b['rooms']):
                m.geom([(x0,y0,ceiling),(x1,y0,ceiling),(x1,y1,ceiling),(x0,y1,ceiling)],[(3,2,1,0)],'Concrete',(.46,.46,.40))
                entries=[('west',(x0,y0),90,y1-y0,(x0-PART,x0,y0,y1),abs(x0-(l+WALL))<.002),
                         ('east',(x1,y1),270,y1-y0,(x1,x1+PART,y0,y1),abs(x1-(r-WALL))<.002),
                         ('south',(x1,y0),180,x1-x0,(x0,x1,y0-PART,y0),abs(y0-(f+WALL))<.002),
                         ('north',(x0,y1),0,x1-x0,(x0,x1,y1,y1+PART),abs(y1-(k-WALL))<.002)]
                for face,org,yaw,length,bounds,exterior in entries:
                    interface=False
                    if exterior:
                        _,oo,side_yaw,side_length=next(v for v in sides(b) if v[0]==face)
                        xx,yy=(x0+x1)/2,(y0+y1)/2;ang=math.radians(side_yaw)
                        u=(xx-oo[0])*math.cos(ang)+(yy-oo[1])*math.sin(ang)
                        interface=not any(lo-.001<u<hi+.001 for lo,hi in visible_intervals(b,face,p['blocks']))
                        if not interface:continue
                    key=tuple(round(v,5) for v in bounds)
                    if key in partitions:continue
                    partitions.add(key)
                    access=(interface or b['kind']=='single' and face=='east' or b['kind']=='cluster' and (face=='north' if y0<f+(k-f)/2 else face=='south') or b['kind']=='classrow' and face==('north' if b['axis']=='X' else 'east'))
                    openings=[dict(u=length-.95,w=.9652,z=base,h=2.1336)] if access else []
                    wall_panel(a,b['id']+'_Room_'+str(j)+'_'+face,org,yaw,length,base,ceiling,openings,'Concrete',PART)
        m.finish();roof(a,b,p);a.colors['Veneer']=original_brick
    for i,c in enumerate(p['covered']):covered_walk(a,c,i)
    x,y=p['entry'];canopy=p['covered'][0];cl,cr,cf,ck=canopy['rect']
    label(a,p['name'],((cl+cr)/2,cf-.025,canopy['height']+.045),.24,color=(.65,.66,.61))
    label(a,'RILL COUNTY PUBLIC SCHOOLS',(x+3.2,y-.055,2.65),.10,color=(.52,.54,.49))
    for name,pt,kind in [('Entry',(x,y-.20,.1524),'entry'),('Walk',(x,y-3.15,.1524),'walk'),('Footprint',(0,0,0),'footprint')]:a.socket(name,pt,kind)
    for b in p['blocks']:
        b['geometry_window_count']=sum(o['type']=='window' for o in b['openings'])
    return a
