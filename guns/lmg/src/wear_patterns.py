"""Original located handling scars; no photograph enters these fields."""
import random

def scratches(n,p,x,y,z,nz):
    # Gear dragged diagonally along the cover. Each groove has finite ends;
    # millimeter spacing survives the canonical atlas at player distance.
    rng=random.Random(56027);strokes=[]
    for i in range(24):
        start=rng.uniform(-.035,.205);length=rng.uniform(.003,.028)
        x0=rng.uniform(-.024,.024);slope=rng.uniform(-.45,.45)
        d=n.math('ABSOLUTE',n.math('SUBTRACT',x,n.add(x0,n.mul(n.math('SUBTRACT',y,start),slope))))
        width=rng.uniform(.000124,.00036)
        ends=n.mul(n.ramp(y,start,start+.002),n.ramp(y,start+length,start+length-.002))
        strokes.append(n.mul(n.ramp(d,width*1.5,width*.35),ends))
    return n.mul(n.maximum(*strokes),n.ramp(nz,.65,.93),n.ramp(z,.137,.142))

def stock_scuffs(n,p,x,y,z,nx):
    """Short gear/vest drags on the stock's exposed bearing faces."""
    rng=random.Random(56028);sides=[]
    for side in (-1,1):
        strokes=[]
        for i in range(64):
            cy,cz=((- .267,.073),(-.218,.045),(-.181,.087))[i%3]
            start=rng.gauss(cy,.020);z0=rng.gauss(cz,.012)
            length=rng.uniform(.006,.014);slope=rng.uniform(-.95,.95)
            d=n.math('ABSOLUTE',n.math('SUBTRACT',z,n.add(z0,n.mul(n.math('SUBTRACT',y,start),slope))))
            width=rng.uniform(.00018,.00036)
            ends=n.mul(n.ramp(y,start,start+.0015),n.ramp(y,start+length,start+length-.0015))
            strokes.append(n.mul(n.ramp(d,width*1.5,width*.30),ends))
        sides.append(n.mul(n.maximum(*strokes),n.ramp(n.mul(nx,side),.72,.95)))
    broken=n.ramp(n.noise(n.vec('MULTIPLY',p,(260,110,330)),1,2),.30,.60)
    return n.mul(n.maximum(*sides),broken)
