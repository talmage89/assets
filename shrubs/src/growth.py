"""Low-branched sheared Buxus: dome, fine sprig tufts, shaded skirt."""
import math,random
from mathutils import Vector
from settings import SEED

CENTER=Vector((0,0,.34))
BASAL_COUNT=24


def surface(direction):
    d=Vector(direction).normalized();az=math.atan2(d.y,d.x);t=(d.z+1)*.5
    # A clipped dome is broadest at the skirt, not halfway up an ellipsoid.
    lobe=1+.035*math.sin(5*az+.4)+.018*math.cos(9*az-5*t)
    radius=.462*math.sqrt(max(0,1-t**1.70))*lobe
    return Vector((radius*math.cos(az),radius*.96*math.sin(az),.125+.655*t+.012*math.sin(4*az)*math.sin(math.pi*t)))


def generate(seed=SEED):
    rng=random.Random(seed);stems=[];sites=[]
    for i in range(BASAL_COUNT):
        az=i*math.tau/BASAL_COUNT+.19;reach=rng.uniform(.20,.32);height=rng.uniform(.36,.65)
        base=Vector((math.cos(az)*rng.uniform(.025,.065),math.sin(az)*rng.uniform(.025,.065),0))
        end=Vector((math.cos(az)*reach,math.sin(az)*reach,height))
        pts=[base,base.lerp(end,.32)+Vector((0,0,.025)),end]
        radius=rng.uniform(.0035,.0053)
        stems.append(dict(points=pts,radii=[radius,radius*.7,.0015],sides=4,level=1,phase=rng.random(),parent=-1))
    for i in range(32):
        parent=i%BASAL_COUNT;pp=stems[parent]['points'];t=rng.uniform(.08,.27)
        base=pp[0].lerp(pp[1],t*2);az=math.atan2(pp[-1].y,pp[-1].x)+rng.choice((-1,1))*rng.uniform(.25,.65)
        tip=Vector((math.cos(az)*rng.uniform(.29,.41),math.sin(az)*rng.uniform(.29,.41),rng.uniform(.19,.55)))
        pts=[base,base.lerp(tip,.53)+Vector((0,0,.018)),tip]
        stems.append(dict(points=pts,radii=[.0028,.0018,.0008],sides=3,level=2,phase=stems[parent]['phase'],parent=parent))
    for i in range(635):
        dz=-.995+1.99*(i+.5)/635;az=i*2.3999632297+rng.uniform(-.065,.065)
        d=Vector((math.sqrt(1-dz*dz)*math.cos(az),math.sqrt(1-dz*dz)*math.sin(az),dz));p=surface(d)
        t=(dz+1)*.5;outward=Vector((math.cos(az),math.sin(az),.16+1.1*t)).normalized()
        shade=max(0,math.sin(az))*max(0,(.30-p.z)/.19)
        if rng.random()<shade*.40:continue
        p-=outward*rng.uniform(.0,.032)
        branch=min(range(len(stems)),key=lambda j:(stems[j]['points'][-1]-p).length)
        sites.append(dict(center=p,direction=outward,branch=branch,new=False,old=p.z<.25 and p.y>0 and rng.random()<.52))
    # Slight interior leaf depth screens twig gaps while preserving cavities.
    for i in range(135):
        az=rng.random()*math.tau;p=Vector((math.cos(az)*.33,math.sin(az)*.33,rng.uniform(.14,.42)))
        sites.append(dict(center=p,direction=(p-CENTER).normalized(),branch=i%len(stems),new=False,old=False))
    for i in range(32):
        az=rng.random()*math.tau;dz=rng.uniform(-.75,.95)
        d=Vector((math.sqrt(1-dz*dz)*math.cos(az),math.sqrt(1-dz*dz)*math.sin(az),dz));p=surface(d)
        direction=Vector((math.cos(az)*.45,math.sin(az)*.45,.95)).normalized();extension=rng.uniform(.05,.11)
        p+=direction*(extension-.032)
        sites.append(dict(center=p,direction=direction,branch=i%len(stems),new=True,old=False,extension=extension))
    return stems,sites
