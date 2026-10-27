"""Branch-first red maple: load-bearing axes, terminal masses, then branchlets.

No crown-volume rejection sampler. Each explicit scaffold ends in a 1–3 m
foliage mass, divided among secondary limbs and smaller fourth-order tufts.
The asymmetric growth controls describe one specimen; no reference pixels enter.
"""
from dataclasses import dataclass
import math,random
import numpy as np
from mathutils import Vector
from species import MAPLE

@dataclass
class Stem:
    points:list
    radii:list
    level:int
    parent:int
    attach:float
    phase:float
    sides:int
    load:int=0
    nominal_radius:float=0


def sample(stem,t):
    x=max(0,min(1,t))*(len(stem.points)-1);i=min(int(x),len(stem.points)-2)
    return stem.points[i].lerp(stem.points[i+1],x-i)


def direction(stem,t):
    return (sample(stem,min(1,t+.015))-sample(stem,max(0,t-.015))).normalized()


def arc(start,end,start_direction,end_direction,steps,rng):
    """A gently bending cubic, not independently jittered straight segments."""
    distance=(end-start).length
    a=start+start_direction.normalized()*distance*.38
    b=end-end_direction.normalized()*distance*.32
    return [(1-t)**3*start+3*(1-t)**2*t*a+3*(1-t)*t*t*b+t**3*end
            for t in [i/steps for i in range(steps+1)]]


def polar(az,r,z):
    a=math.radians(az);return Vector((math.cos(a)*r,math.sin(a)*r,z))


# azimuth, reach, center height, radial/tangential/vertical radii.
# Low limbs reach nearly horizontally, then droop. Different upper axes form
# separate upright tufts. These are branch destinations, not an envelope fill.



def generate(seed,species=MAPLE):
    rng=random.Random(seed);stems=[];cards=[];assignments={};masses=[];card_masses=[];card_tufts=[]
    def add(points,level,parent,attach,phase,sides):
        ix=len(stems);stems.append(Stem(points,[],level,parent,attach,phase,sides));return ix
    if species.ARCHITECTURE=='excurrent':
        from oak_growth import generate as oak_generate
        return oak_generate(rng,species)
    else:
        zs=[0,.07,.16,.30,.60,1.,1.35,1.8,2.05,2.25,2.45,2.66]
        points=[Vector((.018*math.sin(z*1.6),.012*(math.cos(z*2)-1),z)) for z in zs]
        points[0]=Vector((0,0,0));points[1]=Vector((0,0,.07))
        bole=add(points,0,-1,0,rng.random(),24)
        # Five low, rounded buttresses end below grade within half a meter.
        for j in range(species.ROOT_COUNT):
            v=polar(j*360/species.ROOT_COUNT+rng.uniform(-12,12),1,0);length=rng.uniform(*species.ROOT_REACH)
            ps=[v*.09+Vector((0,0,.36)),v*.19+Vector((0,0,.20)),v*length*.72+Vector((0,0,.035)),v*length+Vector((0,0,-.12))]
            ix=add(ps,-1,0,0,rng.random(),10);stems[ix].radii=[.125,.10,.065,.030]
        leaders=[]
        for j,az in enumerate(species.LEADER_AZIMUTHS):
            fork_z=species.LEADER_FORK_Z[j]
            attach=min(range(2001),key=lambda k:abs(sample(stems[0],k/2000).z-fork_z))/2000
            start=sample(stems[0],attach);out=polar(az,1,0)
            end=polar(az,species.LEADER_REACH[j],species.LEADER_TOP[j])
            ps=arc(start,end,out*.66+Vector((0,0,.75)),out*.15+Vector((0,0,1)),24,rng)
            leaders.append(add(ps,1,0,attach,rng.random(),16))
        terminals=[]
        # Grow every order before sampling its terminal foliage.
        for j,layout in enumerate(species.MASS_LAYOUT):
            leader=leaders[j]
            for k,(az,reach,z,rx,ry,rz) in enumerate(layout):
                width_scale=species.CROWN_WIDTH/10.8
                reach*=1.10*width_scale;rx*=1.20*width_scale;ry*=1.20*width_scale
                if z>9.6:rx*=species.UPPER_MASS_BREADTH;ry*=species.UPPER_MASS_BREADTH
                elif z>6.5:rx*=1.12;ry*=1.12
                center=polar(az,reach,z);out=polar(az,1,0);side=Vector((-out.y,out.x,0))
                t=min(.98,max(.08,(z-3.15)/6.1));start=sample(stems[leader],t)
                end=center-out*.24
                initial=direction(stems[leader],t)*.35+out*.95
                # Basal scaffold arches outward then turns gently down at the tip.
                final=out*.95+Vector((0,0,-.45 if k==0 else .45))
                scaffold=add(arc(start,end,initial,final,18,rng),2,leader,t,stems[leader].phase,12)
                mass_id=len(masses)
                masses.append(dict(center=list(center),radii=[rx,ry,rz],scaffold=scaffold,leader=leader,azimuth=az,subclumps=[]))
                # Six irregular subclumps, paired on three secondary limbs; each
                # subclump has two fine fourth-order forks in the alpha branchlets.
                for q in range(6):
                    angle=q*math.tau/6+rng.uniform(-.35,.35)
                    displacement=out*math.cos(angle)*rx*.56+side*math.sin(angle)*ry*.61
                    displacement.z=rz*([-.45,.12,.48,-.20,.34,-.05][q]+rng.uniform(-.12,.12))
                    tuft=center+displacement
                    if k==0:tuft.z=max(tuft.z,2.35)
                    tuft_r=Vector((rx*rng.uniform(.40,.55),ry*rng.uniform(.43,.57),rz*rng.uniform(.48,.64)))
                    t2=[.40,.55,.68,.79,.90,1.][q];p2=sample(stems[scaffold],t2)
                    axis=(tuft-p2).normalized()
                    if q%2==0:
                        secondary=add(arc(p2,tuft,direction(stems[scaffold],t2)*.55+axis*.7,axis,5,rng),3,scaffold,t2,stems[leader].phase,5)
                    sub=dict(center=list(tuft),radii=list(tuft_r),secondary=secondary,terminals=[])
                    masses[-1]['subclumps'].append(sub)
                    for fork in range(2):
                        t3=.66 if fork==0 else 1.;p3=sample(stems[secondary],t3)
                        tip=tuft+side*(.25 if fork==0 else -.25)+out*.08+Vector((0,0,.18 if fork==0 else -.05))
                        axis=(tip-p3).normalized()
                        terminal=add(arc(p3,tip,direction(stems[secondary],t3)*.6+axis*.5,axis,6,rng),4,secondary,t3,stems[leader].phase,7)
                        terminals.append(terminal);sub['terminals'].append(terminal);assignments[terminal]=[]
    # Allocate a fixed card budget by supported mass volume. No global oval.
    volumes=np.array([np.prod(m['radii']) for m in masses]);groups_total=species.CARD_COUNT//3
    counts=np.floor(volumes/volumes.sum()*groups_total).astype(int)
    for i in np.argsort(-(volumes/volumes.sum()*groups_total-counts))[:groups_total-counts.sum()]:counts[i]+=1
    for mi,(mass,count) in enumerate(zip(masses,counts)):
        az=math.radians(mass['azimuth']);out=Vector((math.cos(az),math.sin(az),0));side=Vector((-out.y,out.x,0))
        for g in range(int(count)):
            qi=g%6;sub=mass['subclumps'][qi];c=Vector(sub['center']);r=Vector(sub['radii'])
            # Overlapping smaller clusters give a scalloped limb-sized mass.
            # The solid core is denser than its fringes, so recesses show shaded
            # foliage rather than a regular pattern of holes through the tree.
            d=Vector((rng.gauss(0,1),rng.gauss(0,1),rng.gauss(0,.95))).normalized()
            rho=rng.random()**.42
            if rng.random()<.46:
                c=Vector(mass['center']);r=Vector(mass['radii'])*.68
                if g%4==0:
                    c=c.lerp(sample(stems[mass['scaffold']],.72),.65)
                    r=Vector(mass['radii'])*.52
            if rng.random()<species.MASS_INTERLOCK:
                # Part of this scaffold's leafy growth overlaps the adjacent
                # supported mass. Recesses become half-depth, not sky tunnels.
                outer=[m for m in masses if m is not mass and math.hypot(*m['center'][:2])>2.15
                       and 1.2<abs(m['center'][2]-mass['center'][2])<3.6]
                adjacent=min(outer or [m for m in masses if m is not mass],
                             key=lambda m:(Vector(m['center'])-Vector(mass['center'])).length)
                c=Vector(mass['center']).lerp(Vector(adjacent['center']),rng.uniform(.32,.62))
                r=Vector(mass['radii'])*.72
            elif rng.random()<species.INNER_BRANCHLET_SHARE:
                c=Vector(mass['center']).lerp(sample(stems[mass['scaffold']],.60),.70)
                r=Vector(mass['radii'])*.56
            p=c+out*d.x*r.x*rho+side*d.y*r.y*rho+Vector((0,0,d.z*r.z*rho))
            # Lowest peripheral blade support ~1.9–2 m, central walk clearance.
            p.z=max(species.MIN_CARD_HEIGHT,p.z)
            if math.hypot(p.x,p.y)<1.1:p.z=max(species.MIN_INNER_HEIGHT,p.z)
            owners=sub['terminals']
            owner=owners[(g//6)%2]
            for companion in range(3):
                idx=len(cards);cards.append(p+Vector((rng.uniform(-.04,.04),rng.uniform(-.04,.04),rng.uniform(-.035,.035))))
                assignments[owner].append(idx);card_masses.append(mi);card_tufts.append(qi)
    # A detached branchlet-sized island is more conspicuous than individual
    # leaf tips. Pull only sparse outliers toward their nearest branchlet in
    # the same supported mass, retaining the mass's large-scale notches.
    for mi in (range(len(masses)) if species.ARCHITECTURE=='decurrent' else []):
        indices=[i for i in range(0,len(cards),3) if card_masses[i]==mi]
        for _ in range(3):
            q=np.array([cards[i] for i in indices]);d=np.linalg.norm(q[:,None]-q[None,:],axis=2)
            np.fill_diagonal(d,np.inf);nearest=d.argmin(axis=1)
            for j,index in enumerate(indices):
                distance=d[j,nearest[j]]
                if distance>.36:
                    shift=Vector(q[nearest[j]]-q[j])*min(.7,(distance-.30)/distance)
                    for k in range(3):cards[index+k]+=shift
    children={i:[] for i in range(len(stems))}
    for i,s in enumerate(stems):
        if s.parent>=0 and s.level>=1:children[s.parent].append(i)
    for i in reversed(range(len(stems))):
        s=stems[i]
        if s.level<0:continue
        s.load=sum(stems[c].load for c in children[i]) if children[i] else len(assignments.get(i,[]))
    unit=(.159*species.DBH/.36)**2/species.CARD_COUNT
    for i,s in enumerate(stems):
        if s.level<0:continue
        s.nominal_radius=math.sqrt(unit*s.load)
        if s.level==0:
            s.radii=[r*species.DBH/.36 for r in [.18,.18,.18,.18,.18,.183,.18,.173,.168,.154,.128,.092]]
            for j,p in enumerate(s.points):
                t=max(0,1-p.z/species.ROOT_FLARE_HEIGHT)
                s.radii[j]+=(species.DBH*.5*(species.ROOT_FLARE_RATIO-1))*t*t*(3-2*t)
            continue
        radii=[]
        for j in range(len(s.points)):
            t=j/(len(s.points)-1)
            if children[i]:
                load=sum(stems[ci].load*max(0,min(1,(stems[ci].attach-t)/.18+.5)) for ci in children[i])
                r=math.sqrt(unit*max(load,s.load*.05))
            else:r=s.nominal_radius*(1-.49*t)
            # >2 cm wood only. Collar broadening dies away smoothly.
            r=r*(1+.23*math.exp(-t*22))
            radii.append(r)
        s.radii=radii
    # The specimen layout is expressed around a 12.1 m crown/card envelope.
    # Height scales axes/mass placement; blade dimensions stay in real meters.
    height_scale=species.HEIGHT/species.HEIGHT_REFERENCE
    for stem in stems:
        for point in stem.points:point.z*=height_scale
    for point in cards:point.z*=height_scale
    for mass in masses:
        mass['center'][2]*=height_scale;mass['radii'][2]*=height_scale
        for sub in mass['subclumps']:
            sub['center'][2]*=height_scale;sub['radii'][2]*=height_scale
    # Return explicit mass ownership as part of the reproducible growth graph.
    return stems,terminals,cards,assignments,masses,card_masses,card_tufts
