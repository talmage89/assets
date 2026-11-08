"""Original visual river sections and county-bridge parameters, meters.

Not a hydraulic or structural design: dimensions are reference-informed art
choices. Flow follows +Y. Bridge station follows +X; water datum is Z=0.
"""
from dataclasses import dataclass, asdict
import math

FT = .3048


@dataclass(frozen=True)
class Plan:
    seed: int = 101
    kind: str = 'downtown'
    reach: float = 300
    width: float = 30.48
    spans: int = 3
    span: float = 18.288
    deck_width: float = 11.8872
    deck_z: float = 4.45
    pier: str = 'columns'
    bend: float = 7
    phase: float = .0
    riffle_y: float = 66
    bar_y: float = 43
    year: int = 1974

    @property
    def length(self): return self.spans*self.span

    def center(self, y):
        return self.bend*(math.sin(y/78+self.phase)-math.sin(self.phase))

    def tangent(self, y):
        dx = self.bend/78*math.cos(y/78+self.phase)
        length = math.hypot(dx, 1)
        return dx/length, 1/length

    def halfwidth(self, y):
        return self.width/2*(1+.065*math.sin(y/29+self.seed*.11))

    def water_z(self, y): return -.0006*y

    def bed(self, x, y):
        u=(x-self.center(y))/self.halfwidth(y); a=abs(u)
        riffle=math.exp(-((y-self.riffle_y)/9)**2)
        pool=math.exp(-((y-self.bar_y)/26)**2)
        depth=1.05-.68*riffle
        if a <= 1:
            z=-depth*(1-a**3)
            z-=1.25*pool*math.exp(-((u-.60)/.32)**2)
            # The inner point bar rises across the normal-flow contour.
            z+=1.08*pool*math.exp(-((u+.80)/.32)**2)
        else:
            steep=.18 if u>0 and pool>.3 else .46
            z=min(2.15,(a-1)/steep*2.15)
            z+=.08*math.sin(x*.62+y*.30)*min(1,(a-1)*4)
        if self.kind=='downtown' and x<0 and a>1.05: z=max(z,2.5)
        # Embankments under each road approach meet the abutment backwall.
        road_fill=max(0,1-max(0,abs(y)-7)/15)
        end_fill=max(0,min(1,(abs(x)-self.length/2+1)/6))
        z=max(z,2.1+(self.deck_z-2.1)*road_fill*end_fill) if a>1.12 else z
        return z+self.water_z(y)

    def water_edges(self, y):
        result=[]
        for side in (-1,1):
            lo=0.; hi=1.2
            for _ in range(32):
                mid=(lo+hi)/2
                z=self.bed(self.center(y)+side*self.halfwidth(y)*mid,y)-self.water_z(y)
                if z>0: hi=mid
                else: lo=mid
            result.append(self.center(y)+side*self.halfwidth(y)*(lo+hi)/2)
        return result

    def speed(self, x, y):
        depth=max(.02,self.water_z(y)-self.bed(x,y))
        return (.38+.65*math.exp(-((y-self.riffle_y)/11)**2))*min(1,depth/.35)

    def data(self): return asdict(self)


def generate(seed=101, **changes):
    rural=seed%2==0
    defaults=dict(seed=seed,kind='edge' if rural else 'downtown',width=36.576 if rural else 30.48,
                  spans=3 if not rural else 2,span=24.384 if rural else 18.288,
                  deck_width=11.8872 if not rural else 10.668,
                  pier='wall' if rural else 'columns',bend=15 if rural else 7,
                  phase=.35 if rural else 0,bar_y=40 if rural else 47,
                  riffle_y=74 if rural else 88,year=1968 if rural else 1974)
    defaults.update(changes)
    p=Plan(**defaults)
    if not 2<=p.spans<=4: raise ValueError('Bridge needs 2–4 spans')
    if not 12<=p.span<=27: raise ValueError('Type III visual span range: 12–27 m')
    if p.deck_width<10: raise ValueError('Two lanes and walks need at least 10 m')
    return p
