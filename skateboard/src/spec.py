"""Original medium street mold, SI meters; published baselines in REFERENCE.md."""
from dataclasses import dataclass, asdict
import math
INCH=.0254
@dataclass
class Spec:
    seed:int=0
    state:str='season'
    width:float=.2032
    length:float=.815975
    wheelbase:float=.365125 # INNER mounting rows, not axle spacing
    nose:float=.174625
    tail:float=.168275
    pitch_x:float=.041275
    pitch_y:float=.053975
    thickness:float=.0105
    concave:float=.00762
    nose_angle:float=18.0
    tail_angle:float=18.0
    truck_height:float=.055
    wheel_diameter:float=.054
    wheel_width:float=.032
    contact_width:float=.015
    riser:float=0
    lean_limit:float=12
    @property
    def plate_y(self):return (self.wheelbase+self.pitch_y)/2
    @property
    def axle_y(self):return self.plate_y+.015
    @property
    def axle_z(self):return self.wheel_diameter/2
    @property
    def underside(self):return self.axle_z+self.truck_height+self.riser
    @property
    def nose_end(self):return -self.wheelbase/2-self.pitch_y-self.nose
    @property
    def tail_end(self):return self.wheelbase/2+self.pitch_y+self.tail
    @property
    def axle_width(self):return self.width
    @property
    def hanger_width(self):return self.width-.0662
    def dict(self):return asdict(self)
def spec(seed=0,state='season'):
    # Geometric variations first; age surface effects deliberately wait for look-dev.
    rows=[(8,32.125,14.375,6.875,6.625),(7.75,31.75,14,6.875,6.625),
          (8.25,32,14.25,7,6.5),(8.5,32.25,14.5,6.875,6.625)]
    w,l,wb,n,t=rows[seed%4]
    return Spec(seed=seed,state=state,width=w*INCH,length=l*INCH,wheelbase=wb*INCH,
                nose=n*INCH,tail=t*INCH,concave=.00762*(w/8)**2,
                wheel_diameter=(54,51,53,56)[seed%4]/1000,
                riser=.003175 if seed%4==3 else 0)
def halfwidth(s,y):
    # Elliptical end caps join nearly parallel, very gently waisted rails.
    end=s.nose_end if y<0 else s.tail_end
    cap=.124 if y<0 else .112
    t=max(0,(abs(y)-(abs(end)-cap))/cap)
    return s.width/2*math.sqrt(max(0,1-t*t))*(1-.014*(1-min(1,abs(y)/.26))**2)
def kick(s,y):
    start=s.plate_y+.040
    t=max(0,abs(y)-start);blend=.043
    angle=math.radians(s.nose_angle if y<0 else s.tail_angle)
    slope=math.tan(angle)
    return slope*(t*t/(2*blend) if t<blend else t-blend/2)
def height(s,x,y):
    # Concave is cylindrical/parabolic through stance, eases on the kicks.
    fade=1-.65*min(1,max(0,(abs(y)-.25)/.12))
    return s.underside+kick(s,y)+s.concave*(x/(s.width/2))**2*fade
