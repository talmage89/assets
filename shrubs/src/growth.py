"""Sheared shell supported by multi-stem wood, with uneven pruning and regrowth.

A dense outer skin is deliberate for sheared boxwood. Shallow sector lobes
encode successive shear bites; independent shoots grow past that surface.
The +Y low side is shaded/thinner. No mesh is inferred from photo pixels.
"""
import math,random
from mathutils import Vector
from settings import SEED,CARD_SIZE,HEIGHT

CENTER=Vector((0,0,.330))
RADII=Vector((.437,.421,.480))


def surface(direction):
    d=Vector(direction).normalized();az=math.atan2(d.y,d.x)
    lobe=1+.042*math.sin(5*az+.4)*(1-d.z*d.z)+.027*math.cos(3*az-4*d.z)+.018*math.sin(11*az+7*d.z)
    # Pruning leaves a broad lower skirt, not an ellipsoid's tapered foot.
    horizontal=(1-d.z*d.z)**(-.28) if d.z<0 else 1
    return CENTER+Vector((d.x*RADII.x*horizontal,d.y*RADII.y*horizontal,d.z*(RADII.z if d.z>=0 else .195)))*lobe


def generate(seed=SEED):
    rng=random.Random(seed);stems=[];sites=[]
    # Six basal stems plus a short old central stem, with staggered branches.
    for i in range(7):
        a=i*math.tau/7+.22
        base=Vector((math.cos(a)*.009,math.sin(a)*.009,0))
        end=Vector((math.cos(a)*.21,math.sin(a)*.21,.49+rng.uniform(-.07,.07)))
        pts=[base,base.lerp(end,.28)+Vector((0,0,.055)),base.lerp(end,.66),end]
        stems.append(dict(points=pts,radii=[.013,.011,.008,.004],sides=6,level=1,phase=rng.random(),parent=-1))
    for i in range(35):
        az=i*2.3999632297;z=-.57+(i+.5)/35*1.49
        d=Vector((math.sqrt(1-z*z)*math.cos(az),math.sqrt(1-z*z)*math.sin(az),z));tip=surface(d)
        parent=min(range(7),key=lambda j:(stems[j]['points'][-1]-tip).length)
        t=rng.uniform(.48,.92);pp=stems[parent]['points'];x=t*3;j=min(int(x),2);base=pp[j].lerp(pp[j+1],x-j)
        tip=CENTER+(tip-CENTER)*.82
        pts=[base,base.lerp(tip,.43)+Vector((0,0,.018)),tip]
        stems.append(dict(points=pts,radii=[.0050,.0035,.0012],sides=4,level=2,phase=stems[parent]['phase'],parent=parent))
    # Stratified directions avoid clumps of empty space. Interior copies give
    # genuine depth behind the clipped outer skin, not an opaque ball underneath.
    n=600
    for i in range(n):
        z=-.83+1.81*(i+.5)/n;az=i*2.3999632297+rng.uniform(-.09,.09)
        d=Vector((math.sqrt(1-z*z)*math.cos(az),math.sqrt(1-z*z)*math.sin(az),z))
        p=surface(d)
        shade=max(0,d.y)*max(0,(.45-p.z)/.3)
        if rng.random()<shade*.63:continue
        depth=rng.uniform(.004,.038) if i%6 else rng.uniform(.045,.085)
        p-=d*depth
        branch=min(range(7,len(stems)),key=lambda j:(stems[j]['points'][-1]-p).length)
        sites.append(dict(center=p,direction=d,branch=branch,new=False,old=p.z<.28 and d.y>-.2 and rng.random()<.62))
    # Unequal 5–15 cm new shoots beyond the last shear; whole branchlets show
    # their own axis. These are restrained accents, not a uniform spiky halo.
    for i in range(38):
        az=rng.random()*math.tau;z=rng.uniform(-.20,.99)
        d=Vector((math.sqrt(1-z*z)*math.cos(az),math.sqrt(1-z*z)*math.sin(az),z))
        p=surface(d);extension=rng.uniform(.05,.15)
        # New shoot card starts just inside shear line and follows outward/up.
        direction=(d+Vector((0,0,.65))).normalized();p+=direction*(extension*.44-.028)
        branch=min(range(7,len(stems)),key=lambda j:(stems[j]['points'][-1]-p).length)
        sites.append(dict(center=p,direction=direction,branch=branch,new=True,old=False,extension=extension))
    return stems,sites
