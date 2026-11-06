"""Original deterministic intersection configurations, in meters."""
from dataclasses import dataclass,asdict
import math
LANE=3.3528
HALF=1.5*LANE
FACE=HALF+.4572
BACK=FACE+.1524
CORE=FACE+4.572
CROSS=CORE+1.524
STOP=CROSS+2.4384
POLE_X=FACE+1.02
POLE_Y=CORE-1.00
GRADE=.1524
PAD_TOP=.15875
BUTTON_AXIS=1.0668+PAD_TOP-GRADE
PLATE_BOTTOM=.19685
PLATE_THICK=.0635
SHAFT_BASE=PLATE_BOTTOM+PLATE_THICK
POLE_TOP=PLATE_BOTTOM+7.62
SHAFT_R0=.4064/(2*math.cos(math.pi/12))
SHAFT_R1=.318262/(2*math.cos(math.pi/12))
ARM_Z=POLE_TOP-.9144
def xy(x,y,angle,z=0):
 c,s=math.cos(math.radians(angle)),math.sin(math.radians(angle))
 return (x*c-y*s,x*s+y*c,z)
@dataclass(frozen=True)
class Plan:
 seed:int
 town:str
 finish:str
 head:str
 visor:str
 border:bool
 left:str
 arm:float
 span:bool=False
 near:bool=False
 luminaire:bool=False
 cabinet:int=0
 illuminated:bool=False
 ped_mount:str='pedestal'
 def data(self):return asdict(self)
PLANS={
 201:Plan(201,'Aldervale','zinc','yellow','tunnel',True,'fya',10.9728,cabinet=0),
 202:Plan(202,'Cinderbrook','green','black','cap',False,'five',9.144,near=True,cabinet=1,illuminated=True,ped_mount='mast'),
 203:Plan(203,'Wrenfield','bronze','yellow','cap',False,'protected',7.62,luminaire=True,cabinet=2),
 204:Plan(204,'Morrow Glen','black','yellow','tunnel',False,'permissive',0,span=True,cabinet=3),
}
NAMES=[('Aldervale Rd','Juniper Mill Ln'),('Cinderbrook St','Oriole Hollow Dr'),('Wrenfield Ave','Hazel Run Ct'),('Morrow Glen Rd','Foxmeadow Ln')]
