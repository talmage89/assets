"""Bounded postwar school grammar; no Blender dependency. Meters, -Y entry.

Original plans, informed by the sources in REFERENCE.md. Room dimensions are
clear dimensions; structural bays include their intervening partition gauge.
The three archetypes have different circulation graphs and site arrangements.
"""
import math
import random

FT=.3048
WALL=.3048
PART=.1524
BAY=30*FT+PART
DEPTH=32*FT
SEEDS=(101,102,103)


def school(seed=101,plan_type=None,bays=None):
    rng=random.Random(seed);typ=plan_type or ('finger','courtyard','compact')[(seed-101)%3]
    if typ not in ('finger','courtyard','compact'):raise ValueError(typ)
    n=bays or (3 if seed in SEEDS else rng.choice((3,4)))
    if n not in (3,4):raise ValueError('3 or 4 classroom bays per original finger')
    blocks=[]
    def block(name,rect,kind,era,roof=3.81,skin='brick',**kw):
        d=dict(id=name,rect=list(rect),kind=kind,era=era,roof=roof,skin=skin,openings=[],**kw);blocks.append(d);return d
    # Schools grow by whole classroom bays, not by stretching a facade.
    wing_w=DEPTH+8*FT+PART+2*WALL
    wing_d=n*30*FT+(n-1)*PART+2*WALL
    if typ=='finger':
        era=1956;name='CEDAR FORK';accent=(.065,.12,.17);wall=(.235,.082,.040)
        spine=block('Spine',(-36.5,38,-15,-11.3424),'corridor',era,3.55)
        for j,cx in enumerate((-30,-7,16)):
            b=block('Finger_'+chr(65+j),(cx-wing_w/2,cx+wing_w/2,-11.3424,-11.3424+wing_d),'single',era,3.81,replacement=j==2,bays=n,axis='Y',corridor=8*FT)
        end=-11.3424+wing_d
        block('Library',(-36.5,-8,-25,-15),'library',era,3.81)
        block('Office',(-8,14,-27,-15),'office',era,3.81)
        block('Multipurpose',(14,38,-33,-15),'gym',1963,7.3152)
        block('Kitchen',(38,47,-25,-15),'kitchen',1963,4.00,skin='cmu')
        block('Boiler',(38,47,-15,-7),'boiler',era,4.15,skin='cmu')
        add=block('Addition_1984',(-36.5,-36.5+3*BAY+2*WALL-PART,end,end+DEPTH+2*WALL),'classrow',1984,4.12,skin='cmu',bays=3,axis='X',replacement=True)
        entry=(3,-27);covered=[dict(rect=(-8,14,-30.0,-27),height=3.15),dict(rect=(-39,-36.477,-11.3424,end),height=2.95)]
        loop=dict(center=(0,-58),straight=28,radius=11.5,yaw=0)
        parent=dict(center=(-65,-31),straight=19,radius=9.5,yaw=90)
        parking=(56,86,-51,-26);blacktop=(13,43,37,57);play=(-62,-38,29,47);field=(52,65)
        portables=[(-56,15,0)]
    elif typ=='courtyard':
        era=1964;name='BRIAR COURT';accent=(.08,.19,.145);wall=(.29,.17,.073)
        block('Office',(-30,0,-28,-16),'office',era,3.66)
        block('Multipurpose',(0,24,-34,-16),'gym',era,6.7056)
        block('Kitchen',(24,34,-27,-16),'kitchen',era,3.96,skin='cmu')
        block('Boiler',(24,34,-16,-8),'boiler',era,4.12,skin='cmu')
        # Four classrooms around an eight-foot common link in each pod.
        pod_w=2*30*FT+PART+2*WALL;pod_d=2*DEPTH+8*FT+2*PART+2*WALL
        for j,x in enumerate((-36,3)):
            block('Cluster_'+chr(65+j),(x,x+pod_w,-8,-8+pod_d),'cluster',era,3.81,bays=2,axis='X',replacement=j==1,gable=True,corridor=8*FT)
        block('Addition_1988',(-27,-27+3*BAY+2*WALL-PART,23,23+DEPTH+2*WALL),'classrow',1988,4.15,skin='brick',bays=3,axis='X',replacement=True)
        pod_hall=-8+pod_d/2
        entry=(-15,-28);covered=[dict(rect=(-29,-1,-31,-28),height=3.08),dict(rect=(-17,-13,-16,23),height=2.92,wall_bearing_end=True),dict(rect=(-13,3,pod_hall-2,pod_hall+2),height=2.92),dict(rect=(-30,-13,19,23),height=2.92)]
        loop=dict(center=(-64,-25),straight=22,radius=12,yaw=90)
        parent=dict(center=(-3,-57),straight=22,radius=10.5,yaw=0)
        parking=(41,78,-65,-42);blacktop=(8,38,40,60);play=(45,69,9,27);field=(-40,58)
        portables=[(79,42,0)]
    else:
        era=1976;name='NORTH VALE';accent=(.095,.12,.07);wall=(.34,.25,.135)
        block('Media_Core',(-20,12,-13,6),'media',era,4.88,skin='cmu')
        block('South_Classrooms',(-2-(3*BAY+2*WALL-PART),-2,-13-DEPTH-2*WALL,-13),'classrow',era,4.12,bays=3,axis='X',replacement=True)
        block('Office',(-2,12,-13-DEPTH-2*WALL,-13),'office',era,4.12)
        block('West_Classrooms',(-20-DEPTH-2*WALL,-20,-13,-13+wing_d),'classrow',era,4.12,bays=n,axis='Y',replacement=True)
        block('North_Classrooms',(-20,-20+3*BAY+2*WALL-PART,6,6+DEPTH+2*WALL),'classrow',era,4.12,bays=3,axis='X',replacement=False)
        block('Multipurpose',(12,34,-31,-13),'gym',era,7.01,skin='brick',wall_color=(.18,.10,.05))
        block('Kitchen',(34,44,-23,-13),'kitchen',era,4.12,skin='cmu')
        block('Boiler',(34,44,-13,-5),'boiler',era,4.27,skin='cmu')
        block('Addition_1991',(-5,-5+3*BAY+2*WALL-PART,6+DEPTH+2*WALL,6+2*DEPTH+4*WALL),'classrow',1991,4.27,bays=3,axis='X',replacement=True)
        entry=(5,-13-DEPTH-2*WALL);covered=[dict(rect=(-2,12,-27.3632,-23.3632),height=3.20),dict(rect=(-30.3464,-2,-25.3632,-23.3632),height=3.15)]
        loop=dict(center=(65,-21),straight=22,radius=12,yaw=90)
        parent=dict(center=(-12,-57),straight=22,radius=10.5,yaw=0)
        parking=(-80,-47,-57,-30);blacktop=(-32,-2,35,55);play=(30,54,18,36);field=(43,63)
        portables=[]
    # Seeded local variation preserves each graph and real bay dimensions.
    if seed not in SEEDS:
        accent=tuple(v*rng.uniform(.88,1.12) for v in accent)
        wall=tuple(v*rng.uniform(.94,1.06) for v in wall)
        decade_shift=rng.choice((-2,0,2))
        era+=decade_shift
        for b in blocks:b['era']+=decade_shift
    x0=min(b['rect'][0] for b in blocks);x1=max(b['rect'][1] for b in blocks)
    y0=min(b['rect'][2] for b in blocks);y1=max(b['rect'][3] for b in blocks)
    cx,cy=(x0+x1)/2,(y0+y1)/2
    # Standalone building origin: center of its own footprint, on ground.
    for b in blocks:
        b['rect']=[b['rect'][0]-cx,b['rect'][1]-cx,b['rect'][2]-cy,b['rect'][3]-cy]
    for c in covered:c['rect']=[c['rect'][0]-cx,c['rect'][1]-cx,c['rect'][2]-cy,c['rect'][3]-cy]
    entry=(entry[0]-cx,entry[1]-cy)
    # Site fields stay in their independently designed ground-centered frame.
    p=dict(seed=seed,type=typ,name=name+' ELEMENTARY',era=era,period=2010,blocks=blocks,entry=entry,covered=covered,
           palette=dict(brick=wall,cmu=(.255,.245,.205),accent=accent),floor=.1524,wall=WALL,partition=PART,
           classroom_clear=(30*FT,32*FT),ceiling=10*FT,bay=BAY,lot=(210.,184.),
           bus=loop,parent=parent,parking=parking,blacktop=blacktop,playground=play,field=field,portables=portables,
           footprint=(-((x1-x0)/2),(x1-x0)/2,-((y1-y0)/2),(y1-y0)/2),
           stage='form / construction checkpoint; quick materials, no look-dev approval')
    populate_openings(p)
    for b in blocks:
        if not b['id'].startswith('Addition'):continue
        l,r,f,k=b['rect']
        for aa,bb in visible_intervals(b,'south',blocks):
            if bb-aa>1.8:p['covered'].append(dict(rect=(l+aa,l+bb,f-2.4384,f),height=3.15))
    validate(p);return p


def sides(b):
    l,r,f,k=b['rect']
    return [('south',(l,f),0,r-l),('east',(r,f),90,k-f),('north',(r,k),180,r-l),('west',(l,k),270,k-f)]


def world(q,origin,yaw):
    a=math.radians(yaw);x,y,z=q
    return (origin[0]+x*math.cos(a)-y*math.sin(a),origin[1]+x*math.sin(a)+y*math.cos(a),z)


def visible_intervals(b,face,blocks):
    name,o,yaw,length=next(s for s in sides(b) if s[0]==face)
    cuts={0.,length}
    a=math.radians(yaw);tx,ty=round(math.cos(a)),round(math.sin(a))
    for other in blocks:
        for x in other['rect'][:2]:
            if tx:cuts.add((x-o[0])/tx)
        for y in other['rect'][2:]:
            if ty:cuts.add((y-o[1])/ty)
    cuts=sorted(round(v,7) for v in cuts if 0<=v<=length)
    out=[]
    for l,r in zip(cuts,cuts[1:]):
        x,y,_=world(((l+r)/2,-.01,0),o,yaw)
        occupied=any(q is not b and q['rect'][0]-.001<x<q['rect'][1]+.001 and q['rect'][2]-.001<y<q['rect'][3]+.001 for q in blocks)
        if not occupied and r-l>.01:
            if out and abs(out[-1][1]-l)<.00001:out[-1]=(out[-1][0],r)
            else:out.append((l,r))
    return out


def wall_sections(b,face,blocks,floor=.1524):
    """Exposed vertical intervals, including a tall wall over a low neighbor."""
    name,o,yaw,length=next(s for s in sides(b) if s[0]==face);cuts={0.,length}
    a=math.radians(yaw);tx,ty=round(math.cos(a)),round(math.sin(a))
    for q in blocks:
        if tx:cuts.update((v-o[0])/tx for v in q['rect'][:2])
        if ty:cuts.update((v-o[1])/ty for v in q['rect'][2:])
    cuts=sorted({round(v,7) for v in cuts if 0<=v<=length});out=[]
    for l,r in zip(cuts,cuts[1:]):
        x,y,_=world(((l+r)/2,-.01,0),o,yaw)
        neighbor=next((q for q in blocks if q is not b and q['rect'][0]-.001<x<q['rect'][1]+.001 and q['rect'][2]-.001<y<q['rect'][3]+.001),None)
        z0=max(floor,neighbor['roof']-.18) if neighbor else floor
        if r-l>.01 and b['roof']-.17>z0+.01:
            if out and abs(out[-1][1]-l)<.00001 and abs(out[-1][2]-z0)<.00001 and out[-1][3] is neighbor:out[-1]=(out[-1][0],r,z0,neighbor)
            else:out.append((l,r,z0,neighbor))
    return out


def populate_openings(p):
    for b in p['blocks']:
        l,r,f,k=b['rect'];kind=b['kind'];era=b['era'];b['rooms']=[]
        for face,o,yaw,length in sides(b):
            for aa,bb in visible_intervals(b,face,p['blocks']):
                span=bb-aa
                def opening(u,w,z,h,typ='window',**kw):
                    if aa+.20<u-w/2 and u+w/2<bb-.20:
                        b['openings'].append(dict(face=face,u=u,w=w,z=z,h=h,type=typ,yaw=yaw,origin=o,**kw))
                if kind in ('single','classrow','cluster'):
                    along=(b.get('axis')=='Y' and face in ('east','west') or b.get('axis')=='X' and face in ('south','north'))
                    if kind=='cluster':along=face in ('south','north')
                    if kind=='single' and face=='east':
                        # Exterior corridor gets high, smaller glazing.
                        for i in range(b['bays']):opening(WALL+(i+.5)*BAY,2.4,1.55,1.15)
                    elif along:
                        n=b['bays'];pitch=BAY
                        for j in range(n):
                            u=WALL+j*pitch+15*FT;w=7.15
                            if era>=1970 and p['type']=='compact':w=4.85
                            if b['id'].startswith('Addition') and face=='south':
                                opening(u+.60,6.60,1.17,1.67,replacement=True)
                                opening(WALL+j*pitch+.50,1.0668,0,2.1844,'door',label='CLASSROOM')
                            elif kind=='cluster':opening(u,8.60,.32,2.70,replacement=b.get('replacement',False))
                            else:opening(u,w,.92 if era<1970 else 1.17,2.10 if era<1970 else 1.67,replacement=b.get('replacement',False),infill=j==1 and era<1970 and b.get('replacement',False))
                    elif span>5:
                        opening((aa+bb)/2,1.0668,0,2.1844,'door',label='EXIT')
                        if span>10:opening(aa+2.3,2.0,1.05,1.85)
                elif kind=='gym':
                    if p['type']=='compact' and face=='south':continue
                    count=max(1,int(span/4.5))
                    for j in range(count):opening(aa+(j+.5)*span/count,2.3,b['roof']-1.55,.90)
                    if face in ('south','north') and span>9:opening((aa+bb)/2,2.0828,0,2.1844,'double',label='GYM')
                elif kind=='office':
                    if face=='south':
                        ex=p['entry'][0]-o[0];opening(ex,3.8,0,2.85,'entry',label='MAIN OFFICE')
                        for u in (aa+3.5,bb-3.5):
                            if abs(u-ex)>4.5:opening(u,4.1,.8,2.16,replacement=True)
                    elif span>6:opening((aa+bb)/2,min(5,span-2),.92,2.0,replacement=True)
                elif kind in ('library','media'):
                    n=max(1,int(span/8))
                    for j in range(n):opening(aa+(j+.5)*span/n,min(5.5,span/n-1),1.1,1.85)
                elif kind in ('kitchen','boiler'):
                    if face=='east':
                        opening((aa+bb)/2,1.2184,0,2.1844,'door',label='SERVICE')
                    elif span>4:opening((aa+bb)/2,1.5,1.2,1.2,'louver')
                elif kind=='corridor' and span>4:
                    opening((aa+bb)/2,min(2.2,span-1),1.1,1.6)
        if kind in ('single','classrow','cluster'):
            # Room reservations are exact clear rectangles, later checked on
            # source surfaces independently of export serialization.
            if kind=='single':
                for j in range(b['bays']):b['rooms'].append([l+WALL,l+WALL+DEPTH,f+WALL+j*BAY,f+WALL+j*BAY+30*FT])
            elif kind=='cluster':
                for x in (l+WALL,l+WALL+BAY):
                    for y in (f+WALL,k-WALL-DEPTH):b['rooms'].append([x,x+30*FT,y,y+DEPTH])
            elif b['axis']=='X':
                for j in range(b['bays']):b['rooms'].append([l+WALL+j*BAY,l+WALL+j*BAY+30*FT,f+WALL,min(k-WALL,f+WALL+DEPTH)])
            else:
                for j in range(b['bays']):b['rooms'].append([l+WALL,min(r-WALL,l+WALL+DEPTH),f+WALL+j*BAY,f+WALL+j*BAY+30*FT])


def validate(p):
    assert len({b['id'] for b in p['blocks']})==len(p['blocks'])
    for i,b in enumerate(p['blocks']):
        l,r,f,k=b['rect'];assert l<r and f<k
        for q in p['blocks'][i+1:]:
            a,c,d,e=q['rect'];assert min(r,c)-max(l,a)<.001 or min(k,e)-max(f,d)<.001,('Overlapping volumes',b['id'],q['id'])
        for o in b['openings']:assert o['z']+o['h']+.13<b['roof']
    assert sum(o['type']=='entry' for b in p['blocks'] for o in b['openings'])==1,'Missing main entrance'
    return p
