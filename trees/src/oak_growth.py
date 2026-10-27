"""Pin oak ramification: irregular axes, secondary masses, then twig cards.

Uses the shared family growth primitives. No photo coordinates enter growth.
All dimensions below are meters; fine live laterals remain in branchlet cards.
"""
import math
import numpy as np
from mathutils import Vector
from growth import Stem,arc,sample,direction,polar


def interpolate(rows,z):
    for (a,x),(b,y) in zip(rows,rows[1:]):
        if z<=b:return x+(y-x)*max(0,(z-a)/(b-a))
    return rows[-1][1]


def generate(rng,species):
    stems=[];masses=[];terminals=[];assignments={};cards=[];card_masses=[];card_tufts=[]
    def add(ps,rs,level,parent,attach,phase,sides=5,kind='live'):
        i=len(stems);s=Stem(ps,rs,level,parent,attach,phase,sides)
        s.kind=kind;s.nominal_radius=rs[0] if rs else 0;stems.append(s);return i
    zs=[0,.07,.18,.38,.8,1.35,2.3]+[3.+j*.5 for j in range(28)]+[species.HEIGHT]
    ps=[Vector((.045*math.sin(z*.45)*z/species.HEIGHT,.035*(math.cos(z*.52)-1),z)) for z in zs];ps[0]=Vector((0,0,0))
    rs=[species.DBH*.5*(1-.96*(z/species.HEIGHT)**1.30)+(.012*math.exp(-((z-15.3)/1.2)**2) if z>=12 else 0) for z in zs]
    for j,z in enumerate(zs):
        t=max(0,1-z/species.ROOT_FLARE_HEIGHT);rs[j]+=species.DBH*.5*(species.ROOT_FLARE_RATIO-1)*t*t*(3-2*t)
    add(ps,rs,0,-1,0,rng.random(),20)
    for j in range(species.ROOT_COUNT):
        v=polar(j*360/species.ROOT_COUNT+rng.uniform(-14,14),1,0);reach=rng.uniform(*species.ROOT_REACH)
        add([v*.09+Vector((0,0,.35)),v*.21+Vector((0,0,.14)),v*reach*.78+Vector((0,0,.03)),v*reach+Vector((0,0,-.10))],[.10,.075,.040,.018],-1,0,0,rng.random(),10)
    def attachment(z):
        for j,(a,b) in enumerate(zip(stems[0].points,stems[0].points[1:])):
            if a.z<=z<=b.z:return (j+(z-a.z)/(b.z-a.z))/(len(stems[0].points)-1)
        return 1.
    pins=species.DEAD_PINS
    for j in range(pins['count']):
        z=rng.uniform(pins['base_z'],pins['top_z']);t=attachment(z);a=sample(stems[0],t);az=rng.uniform(0,360);out=polar(az,1,0)
        radius=interpolate(list(zip(zs,rs)),z);length=rng.uniform(*pins['exposed_length']);slope=rng.uniform(-.55,-.25)
        end=a+out*(radius+length)+Vector((0,0,(radius+length)*slope))
        ps=arc(a,end,out+Vector((0,0,-.12)),out+Vector((0,0,-.85)),6,rng)
        r=rng.uniform(*pins['radius']);i=add(ps,[r*(1-.76*k/6) for k in range(7)],3,0,t,rng.random(),4,'dead')
        # Short grayer forks, not a row of straight rods. Only dead pins spend
        # millimeter geometry; the large live lateral population lives in cards.
        for q in range(1+(j%3==0)):
            at=rng.uniform(.64,.85);a2=sample(stems[i],at);side=polar(az+rng.choice([-60,65]),1,0)
            b=a2+side*rng.uniform(.055,.11)+Vector((0,0,-rng.uniform(.025,.065)))
            ps2=arc(a2,b,direction(stems[i],at),side+Vector((0,0,-.6)),3,rng)
            add(ps2,[.0025,.0022,.0018,.0016],3,i,at,stems[i].phase,3,'dead')
    limbs=species.LATERALS
    # Random positive internodes normalized to the chosen height range: no
    # whorls, golden-angle spiral or repeated vertical intervals.
    gaps=[rng.uniform(.12,.48) for _ in range(limbs['count']-1)]
    heights=[limbs['base_z']]
    for gap in gaps:heights.append(heights[-1]+gap/sum(gaps)*(limbs['top_z']-limbs['base_z']))
    azimuths=[]
    for z in heights:
        candidates=[rng.uniform(0,360) for _ in range(24)]
        def crowding(az):
            return sum(math.exp(-(((az-old+180)%360-180)/35)**2)*math.exp(-(z-h)/2.2)
                       for h,old in azimuths[-8:])
        az=min(candidates,key=crowding);azimuths.append((z,az))
    for j,(z,az) in enumerate(azimuths):
        out=polar(az,1,0);side=Vector((-out.y,out.x,0));phase=rng.random();t=attachment(z);a=sample(stems[0],t)
        reach=interpolate(limbs['reach_profile'],z)*rng.uniform(.97,1.025)
        if z<limbs['lower_zone']:
            initial=rng.uniform(-22,-12);final=rng.uniform(-43,-30)
            end_z=max(2.75,z-reach*rng.uniform(.32,.43))
        elif z<limbs['upper_zone']:
            initial=rng.uniform(-8,12);final=rng.uniform(-8,20)
            # The outward shoots turn upward progressively through the shoulder.
            # A step from level endpoints to ascending endpoints made an empty
            # collar below the upper crown despite correct exit angles.
            shoulder=max(0,min(1,(z-8.4)/(limbs['upper_zone']-8.4)))
            initial-=shoulder*5
            end_z=z+reach*math.tan(math.radians(rng.uniform(-12,7)+shoulder*35))
        else:
            initial=rng.uniform(38,46);final=rng.uniform(33,48)
            end_z=min(species.HEIGHT-.65,z+reach*math.tan(math.radians(rng.uniform(33,45))))
        b=a+out*reach+side*(rng.uniform(-.30,.30)*min(1,reach/2));b.z=end_z
        def tangent(degrees):return out*math.cos(math.radians(degrees))+Vector((0,0,math.sin(math.radians(degrees))))
        ps=arc(a,b,tangent(initial),tangent(final),24,rng)
        # Independent gentle lateral bow, zero at both ends; not jagged jitter.
        bow=rng.uniform(-.25,.25)*min(1,reach/2)
        for k,p in enumerate(ps):
            u=k/24;p+=side*math.sin(math.pi*u)*bow
            if z<limbs['lower_zone']:
                # Continuous sweep: departure is shallow, then the whole limb
                # bends progressively down, including its middle third.
                drop=z-end_z;start_drop=reach*math.tan(math.radians(-initial))*.78
                p.z=z-start_drop*u-(drop-start_drop)*u*u
            if limbs['lower_zone']<=z<limbs['upper_zone']:p.z+=.32*math.sin(math.pi*u)**2
        r=.030+.026*min(1,reach/4.9)
        rs2=[r*(1-.90*k/24)**.82*(1+.055*math.exp(-k/2)) for k in range(25)]
        primary=add(ps,rs2,2,0,t,phase,5)
        nsec=rng.choice([2,3,3,4]) if reach>1.2 else 2
        for q in range(nsec):
            at=.35+.34*q/max(1,nsec-1)+rng.uniform(-.035,.035);start=sample(stems[primary],at)
            # Real fork: secondaries spread sideways and turn with their parent,
            # rather than continuing as three short parallel brushes at its tip.
            sign=-1 if q%2==0 else 1
            spread=sign*rng.uniform(.80,1.40)*min(1,reach/2.2)
            distal=min(.98,at+rng.uniform(.48,.62));dest=sample(stems[primary],distal)
            dest+=side*spread+out*rng.uniform(-.12,.18)
            dest.z+=rng.uniform(-.28,.38) if z<9 else rng.uniform(.30,.90) if z<11.8 else rng.uniform(-.75,-.10)
            axis=(dest-start).normalized();initial_axis=(direction(stems[primary],at)*.55+axis*.65).normalized()
            ps3=arc(start,dest,initial_axis,axis+Vector((0,0,-.15 if z<7 else .22)),12,rng)
            radius=min(.025,r*(.48-.08*at))
            rs3=[radius*(1-.87*k/12)**.85*(1+.10*math.exp(-k/2)) for k in range(13)]
            secondary=add(ps3,rs3,3,primary,at,phase,4)
            center=sample(stems[secondary],.60)
            # One 1–3 m leaf-bearing mass PER secondary. Taller, interlocking
            # shoulders above the low-tier region prevent the fir ladder gaps.
            length=(dest-start).length
            rx=max(.48,min(1.35,length*.62+.26));ry=.63 if z<7 else 1.10;rz=.55 if z<7 else 1.35 if z<12 else 1.15
            mi=len(masses);m=dict(center=list(center),radii=[rx,ry,rz],scaffold=primary,secondary=secondary,leader=0,azimuth=az,subclumps=[])
            masses.append(m)
            for qi in range(6):
                at2=.22+qi*.15;a4=sample(stems[secondary],at2)
                lateral_dir=(out*.35+side*(-.65 if qi%2 else .65)+Vector((0,0,.10 if z<9 else .30))).normalized()
                tip=a4+lateral_dir*rng.uniform(.22,.50)
                ti=add(arc(a4,tip,direction(stems[secondary],at2),lateral_dir,4,rng),[.003,.0025,.002,.0015,.001],4,secondary,at2,phase,4)
                terminals.append(ti);assignments[ti]=[]
                m['subclumps'].append(dict(center=list(tip),radii=[rx*.45,ry*.65,rz*.65],secondary=secondary,terminals=[ti,ti]))
    # The actual leader carries six short shoots, overlapping the ascending
    # upper limbs. Spread its leaves vertically instead of making a separate
    # opaque top pompon. Fine shoots are represented by alpha branchlet cards.
    m=dict(center=[0,0,15.25],radii=[.5,.5,1.1],scaffold=0,secondary=0,leader=0,azimuth=0,apex=True,subclumps=[])
    masses.append(m)
    for qi,z in enumerate([13.8,14.3,14.8,15.3,15.8,16.28]):
        at=attachment(z);a=sample(stems[0],at);az=rng.uniform(0,360);out=polar(az,1,0)
        reach=(16.55-z)*.28;tip=a+out*reach+Vector((0,0,.12))
        ti=add(arc(a,tip,out+Vector((0,0,.7)),out+Vector((0,0,.8)),4,rng),[.004,.003,.002,.0015,.001],4,0,at,stems[0].phase,4)
        terminals.append(ti);assignments[ti]=[]
        m['subclumps'].append(dict(center=list(tip),radii=[.3,.3,.45],secondary=0,terminals=[ti,ti]))
    # Allocate a finite budget; a denser continuous upper crown, with the low
    # boughs retaining windows. Cardinal shoots remain attached to secondary axes.
    weights=np.array([np.prod(m['radii'])*(6.0 if stems[m['scaffold']].points[0].z<7.1 and not m.get('apex') else 1.05 if m['center'][2]>8 else 1.35) for m in masses]);weights[-1]=2.2
    extra=species.LOWER_EXTRA_CARDS//3
    count=species.CARD_COUNT//3-extra;counts=np.floor(weights/weights.sum()*count).astype(int)
    for i in np.argsort(-(weights/weights.sum()*count-counts))[:count-counts.sum()]:counts[i]+=1
    # Spend the triangles reclaimed from hidden secondary rings on low lateral
    # sprays specifically. The accepted upper allocation stays unchanged.
    low=np.array([weights[i] if not m.get('apex') and stems[m['scaffold']].points[0].z<7.1 else 0 for i,m in enumerate(masses)])
    bonus=np.floor(low/low.sum()*extra).astype(int)
    for i in np.argsort(-(low/low.sum()*extra-bonus))[:extra-bonus.sum()]:bonus[i]+=1
    counts+=bonus
    # A separate stream changes only leafy growth; accepted wood stays fixed.
    import random
    foliage_rng=random.Random(species.SEED+491)
    for mi,(m,count) in enumerate(zip(masses,counts)):
        az=math.radians(m['azimuth']);out=Vector((math.cos(az),math.sin(az),0));side=Vector((-out.y,out.x,0));secondary=stems[m['secondary']]
        for g in range(int(count)):
            qi=g%6;sub=m['subclumps'][qi]
            if m.get('apex'):
                p=Vector(sub['center'])+Vector((rng.gauss(0,.16),rng.gauss(0,.16),rng.uniform(-.30,.14)))
            else:
                # Continuous leaves start on the proximal short laterals too;
                # distal-only weighting leaves an empty ring below the apex.
                upper=stems[m['scaffold']].points[0].z>=7.1
                along=.05+.95*(rng.betavariate(.75,1.4) if upper else rng.betavariate(1.15,1.25))
                p=sample(secondary,along)
                p+=side*rng.gauss(0,m['radii'][1]*.75)+out*rng.gauss(0,m['radii'][0]*.37)
                p.z+=math.tanh(rng.gauss(0,1))*m['radii'][2]*.82
                if p.z>15.4:
                    limit=max(.14,(16.55-p.z)*.65)
                    r=math.hypot(p.x,p.y)
                    if r>limit:p.x*=limit/r;p.y*=limit/r
            if not m.get('apex'):
                primary=stems[m['scaffold']];root_z=primary.points[0].z
                if 5.5<=root_z<9.5 and g<3:
                    # Retain the leaf-bearing outer secondary extensions when
                    # inner growth is reallocated. These support crown breadth.
                    p=sample(secondary,foliage_rng.uniform(.85,1.0))+side*foliage_rng.gauss(0,.38)
                    p.z+=foliage_rng.uniform(-.20,.35)
                elif root_z<7.1 and g%4<2:
                    # Leaf-bearing short laterals screen the inner two thirds
                    # of low boughs too. Keep the remaining outer sprays so the
                    # skirt stays ragged, rather than adding a foliage shell.
                    t=foliage_rng.uniform(.04,.32) if g%4==0 else foliage_rng.uniform(.25,.82)
                    p=sample(primary,t)+side*foliage_rng.gauss(0,.65)
                    p.z+=foliage_rng.uniform(-.85,.60)-.20*t
                elif 7.1<=root_z<10.2 and g%2==0:
                    p=sample(primary,foliage_rng.uniform(.06,.82))+side*foliage_rng.gauss(0,.75)
                    p.z+=foliage_rng.uniform(-.85,.65)
                elif 10.2<=root_z<14 and g%3==0:
                    # Inner live shoots originate on the primary before its
                    # secondary fork. Screen the middle bole without a filler shell.
                    t=foliage_rng.uniform(.06,.25)
                    p=sample(primary,t)+side*foliage_rng.uniform(-.42,.42)
                    p.z+=foliage_rng.uniform(-.38,.68)
                elif root_z<12 and g%5==4:
                    p=sample(primary,foliage_rng.uniform(.78,1.0))+side*foliage_rng.gauss(0,.25)
                    p.z+=foliage_rng.uniform(-.45,.28)
                elif root_z<7.1:
                    # Drooping lateral sprays: extension and drop are correlated.
                    along2=foliage_rng.uniform(.03,.85)
                    p=sample(secondary,along2)+side*foliage_rng.gauss(0,.60)+out*foliage_rng.gauss(0,.18)
                    p.z+=foliage_rng.uniform(-.35,.20)-.45*along2
            p.z=max(species.MIN_CARD_HEIGHT,min(species.HEIGHT-species.APEX_CARD_HEADROOM,p.z))
            radius=math.hypot(p.x,p.y);limit=interpolate(species.CROWN_RADII,p.z)
            if radius>limit:
                p.x*=limit/radius;p.y*=limit/radius
            if math.hypot(p.x,p.y)<1:p.z=max(species.MIN_INNER_HEIGHT,p.z)
            ti=sub['terminals'][0]
            for companion in range(3):
                i=len(cards);cards.append(p+Vector((rng.uniform(-.025,.025),rng.uniform(-.025,.025),rng.uniform(-.025,.025))))
                assignments[ti].append(i);card_masses.append(mi);card_tufts.append(qi)
    children={i:[] for i in range(len(stems))}
    for i,s in enumerate(stems):
        if s.parent>=0:children[s.parent].append(i)
    for i in reversed(range(len(stems))):
        s=stems[i];s.load=len(assignments.get(i,[]))+sum(stems[c].load for c in children[i])
    return stems,terminals,cards,assignments,masses,card_masses,card_tufts
