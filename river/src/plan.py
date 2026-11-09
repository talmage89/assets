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

    @property
    def outside(self):
        return 1 if self.bend*math.sin(self.bar_y/78+self.phase)>=0 else -1

    def center(self, y):
        # A second, broad bend gives the downtown reach an actual turn while
        # retaining its accepted width, crossing stations and bend parameter.
        t=max(0,min(1,(y+30)/90));local=1+.95*t*t*(3-2*t) if self.kind=='downtown' else 1
        return local*self.bend*(math.sin(y/78+self.phase)-math.sin(self.phase))

    def tangent(self, y):
        delta=.01;dx=(self.center(y+delta)-self.center(y-delta))/(2*delta)
        length = math.hypot(dx, 1)
        return dx/length, 1/length

    def halfwidth(self, y):
        return self.width/2*(1+.065*math.sin(y/29+self.seed*.11))

    def water_z(self, y): return -.0006*y

    def road_z(self,x):
        t=max(0,min(1,(abs(x)-145)/85));t=t*t*(3-2*t)
        grade=3.775 if self.kind=='downtown' else 2.225
        return self.deck_z+(grade-self.deck_z)*t

    def bed(self, x, y):
        u=(x-self.center(y))/self.halfwidth(y); a=abs(u)
        riffle=math.exp(-((y-self.riffle_y)/5.5)**2)
        pool=math.exp(-((y-self.bar_y)/26)**2)
        depth=1.05-.86*riffle
        if a <= 1:
            z=-depth*(1-a**3)
            z-=1.25*pool*math.exp(-((u*self.outside-.60)/.32)**2)
            # The inner point bar rises across the normal-flow contour.
            z+=1.08*pool*math.exp(-((u*self.outside+.80)/.32)**2)
        else:
            cut=u*self.outside>0 and pool>.22
            # Retreat/scallop the outside bank; slump toes occur below the
            # near-vertical soil face rather than along an even ramp.
            retreat=(.020*math.sin(y*.83)+.025*math.sin(y*.29)) * pool if cut else 0
            bank=a-1-retreat
            steep=.105 if cut else .46
            z=min(2.15,max(0,bank)/steep*2.15)
            if cut:
                z+=.24*math.exp(-((bank-.028)/.025)**2)*( .55+.45*math.sin(y*.71))
                z-=.26*pool*math.exp(-((bank-.14)/.09)**2)*( .5+.5*math.sin(y*.57))
            z+=.10*math.sin(x*.62+y*.30)*min(1,max(0,bank)*4)
        if self.kind=='downtown' and a>1:
            # Main Street is a raised terrace. The floodable low riverwalk
            # passes under the girders with >2.3m headroom.
            edge_distance=abs(x-self.center(y))-self.halfwidth(y)
            if edge_distance>=4.45:z=max(z,3.7)
            elif edge_distance>.75:z=.50
            else:z=min(z,.50)
        # Embankments under each road approach meet the abutment backwall.
        road_fill=max(0,1-max(0,abs(y)-7)/15)
        end_fill=max(0,min(1,(abs(x)-self.length/2-.90)/.12))
        wing=self.deck_width/2+math.tan(math.radians(30))*max(0,min(5.5,abs(x)-self.length/2-.8))
        if abs(y)>wing+.3:
            # Outside the retaining walls the approach fill has a sloping
            # toe, rather than extending the backwall's vertical soil face.
            end_fill=max(0,min(1,(abs(x)-self.length/2-.90)/6))
        fill_top=self.road_z(x)-.075-.02*min(abs(y),3.3528)
        if abs(y)>3.3528:fill_top=self.road_z(x)-.06
        if abs(y)<self.deck_width/2+4 and abs(x)<self.length/2+.90:
            cap=1.05
            if self.kind=='downtown':
                edge_distance=abs(x-self.center(y))-self.halfwidth(y)
                # Keep the low riverwalk clear, then armor a 2H:1V bank
                # up toward the abutment seat instead of a broad flat void.
                cap=.50+min(.65,max(0,edge_distance-4.45)*.5)
            blend=max(0,min(1,(abs(y)-self.deck_width/2)/4))
            cap+=(3.70-cap if self.kind=='downtown' else 2.15-cap)*blend
            z=min(z,cap)
        if a>1.12 and end_fill>0:z=max(z,2.1+(fill_top-2.1)*road_fill*end_fill)
        if self.kind=='edge' and abs(x)>self.length/2+9:
            ditch=math.exp(-((abs(y)-9.4)/1.85)**2)
            z-=.70*ditch
        if self.kind=='edge' and abs(y+36)<=2.05:
            launch_edge=self.center(-36)-self.halfwidth(-36)
            t=(x-(launch_edge-18))/18.8
            if 0<=t<=1:z=min(z,2.10-2.22*t-.08)
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
        run=.43/(.65+depth*.48)
        return (run+.75*math.exp(-((y-self.riffle_y)/7)**2))*min(1,depth/.20)

    def flow(self,x,y):
        tx,ty=self.tangent(y);speed=self.speed(x,y);vx,vy=tx*speed,ty*speed
        # Sheltered, curling wakes. This is analytic game data, not CFD.
        for j in range(1,self.spans):
            dx=x-(-self.length/2+j*self.span);dy=y-(self.deck_width/2+2.2)
            wake=math.exp(-(dx/1.5)**2-(dy/3)**2)
            vx=vx*(1-.50*wake)-dy/3*.12*wake
            vy=vy*(1-.50*wake)+dx/1.5*.12*wake
        return vx,max(.03,vy)

    def data(self): return asdict(self)


def generate(seed=101, **changes):
    rural=seed%2==0
    defaults=dict(seed=seed,kind='edge' if rural else 'downtown',width=36.576 if rural else 30.48,
                  spans=3 if not rural else 2,span=24.384 if rural else 18.288,
                  deck_width=11.8872 if not rural else 10.668,
                  pier='wall' if rural else 'columns',bend=15 if rural else -7,
                  phase=.35 if rural else 0,bar_y=40 if rural else 47,
                  riffle_y=74 if rural else 88,year=1968 if rural else 1974)
    defaults.update(changes)
    p=Plan(**defaults)
    if not 2<=p.spans<=4: raise ValueError('Bridge needs 2–4 spans')
    if not 12<=p.span<=27: raise ValueError('Type III visual span range: 12–27 m')
    if not 10<=p.deck_width<=14: raise ValueError('Five-girder two-lane deck width range: 10–14 m')
    if p.length<p.width+6:raise ValueError('Span layout needs the channel width plus two abutment banks')
    if p.pier not in ('columns','wall'):raise ValueError('Pier must be columns or wall')
    return p
