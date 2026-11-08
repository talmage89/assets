"""Meters, +Y station axis. Original 2012 maintained freeway configurations.

The scene seed changes the *civil plan*, not just dressings. Alignment samples
are also the single source for road, rail, terrain and driving-path placement.
"""
import math
from dataclasses import dataclass, asdict

FT=.3048
LANE=12*FT
RIGHT=10*FT
LEFT=4*FT
LINE=.5*FT
JOINT=15*FT
DASH=10*FT
CYCLE=40*FT
BRIDGE_Z=7.35

@dataclass(frozen=True)
class Plan:
    seed:int
    kind:str
    town:str
    length:float
    median:float
    radius:float
    grade:float
    bank:float
    pavement:str
    terminal:float=78.

    def center(self,s):
        x=0 if self.radius==0 else self.radius*(1-math.cos(s/self.radius))
        y=s if self.radius==0 else self.radius*math.sin(s/self.radius)
        return (x,y,self.grade)

    def frame(self,s):
        a=0 if self.radius==0 else s/self.radius
        return (math.cos(a),-math.sin(a)),(math.sin(a),math.cos(a))

    def xyz(self,s,u,z=0):
        c=self.center(s);n,_=self.frame(s)
        # Crown breaks at the center of the median. Superelevation is constant
        # through this circular-curve excerpt; transition modules are separate.
        h= - .02*max(0,abs(u)-self.median/2) if self.bank==0 else u*self.bank
        return (c[0]+n[0]*u,c[1]+n[1]*u,c[2]+h+z)

    def lane(self,side,index):
        return side*(self.median/2+LEFT+(index+.5)*LANE)

    @property
    def edge(self):return self.median/2+LEFT+2*LANE+RIGHT

    def data(self):return asdict(self)

def plan(seed):
    if seed==101:return Plan(seed,'diamond','Alder Junction',1600.,8*FT,0,0,0,'Concrete')
    if seed==202:return Plan(seed,'soundwall','Cedar Hollow',1000.,30*FT,1400.,1.4,-.04,'Asphalt')
    # Unpublished seeds remain deterministic and select both plans.
    return Plan(seed,'soundwall' if seed%2==0 else 'diamond','Lark Township',
                1000. if seed%2==0 else 1600.,(30 if seed%2==0 else 8)*FT,
                (1200.+seed%5*100) if seed%2==0 else 0.,1.4 if seed%2==0 else 0.,
                -.04 if seed%2==0 else 0.,'Asphalt' if seed%2==0 else 'Concrete',72.+seed%4*6)

def ramp_points(p,side,entry=False,n=96):
    """Opposing half-diamonds; northbound is east of the median.

    264 m station extent plus explicit 366 m parallel speed-change lanes
    and 91.44 m tapers. Stops are at the arterial's edge.
    """
    start=side*(16 if entry else -280)
    end=side*(280 if entry else -16)
    low_u=p.edge-RIGHT+LANE/2
    u0=p.terminal if entry else low_u
    u1=low_u if entry else p.terminal
    rows=[]
    for i in range(n+1):
        t=i/n;q=t*t*(3-2*t)
        u=side*(u0+(u1-u0)*q)
        s=start+(end-start)*t
        # Flat grade at both ends; maximum gradient is measured by check.py.
        # Hold the freeway grade through the first 10% at the gore. The
        # vertical ramp curve starts beyond that shared pavement throat.
        travel=1-t if entry else t
        v=max(0,min(1,(travel-.10)/.90));v=v*v*(3-2*v)
        # Until the vertical curve starts, follow the mainline crossfall plane
        # as the branch moves laterally. This prevents a lip in the shared throat.
        z=-.02*(abs(u)-p.median/2)+(BRIDGE_Z+.02*(p.terminal-p.median/2))*v
        rows.append((u,s,z))
    return rows

def path_curvature(points):
    result=[]
    for a,b,c in zip(points,points[1:],points[2:]):
        ab=math.dist(a[:2],b[:2]);bc=math.dist(b[:2],c[:2]);ac=math.dist(a[:2],c[:2])
        cross=abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
        if cross>1e-10:result.append(ab*bc*ac/(2*cross))
    return min(result) if result else None
