"""Original located handling scars; no photograph enters these fields."""
import random

def scratches(n,p,x,y,z,nz):
    # Gear dragged diagonally along the cover. Each groove has finite ends;
    # millimeter spacing survives the canonical atlas at player distance.
    rng=random.Random(56027);strokes=[]
    for i in range(34):
        start=rng.uniform(-.035,.205);length=rng.uniform(.008,.044)
        x0=rng.uniform(-.024,.024);slope=rng.uniform(-.45,.45)
        d=n.math('ABSOLUTE',n.math('SUBTRACT',x,n.add(x0,n.mul(n.math('SUBTRACT',y,start),slope))))
        width=rng.uniform(.00025,.00065)
        ends=n.mul(n.ramp(y,start,start+.002),n.ramp(y,start+length,start+length-.002))
        strokes.append(n.mul(n.ramp(d,width*1.5,width*.35),ends))
    return n.mul(n.maximum(*strokes),n.ramp(nz,.65,.93),n.ramp(z,.137,.142))
