"""Original visual asset dimensions, millimeters; no functional internals.

The family's held frame is +Y muzzle, +Z up, +X right, grip origin.
Published envelopes constrain this fictional design, not manufacturing fits.
"""
import math
import hashlib
from pathlib import Path
def generator_digest():
 here=Path(__file__).parent
 paths=[here/n for n in ('build.py','parameters.py','clips.py','interface.py')]
 paths.append(here.parents[1]/'common/magnum357.py')
 h=hashlib.sha256()
 for p in paths:h.update(p.name.encode()+b'\0'+p.read_bytes())
 return h.hexdigest()
CY=48.2
PITCH=12.8
BORE=CY+PITCH
REAR=38.0
FRONT=82.2
GAP=.20
BREECH=FRONT+GAP
MUZZLE=BREECH+101.6
RADIUS=19.7
FLUTE_RADIUS=7.1
FLUTE_START=REAR+10
FLUTE_END=FRONT-1.5
def flute_axis(i):
 t=math.pi/2+math.pi/6+i*math.tau/6
 return round(25*math.cos(t),6),round(CY+25*math.sin(t),6)
CRANE=(-8,85,20)
OPEN=-80
EYE=(0,-622,83)
def chamber(i):
 t=math.pi/2+i*math.tau/6
 return (round(PITCH*math.cos(t),6),REAR,round(CY+PITCH*math.sin(t),6))
HEADS={'Root':(0,0,0),'Crane':CRANE,'Cylinder':(0,REAR,CY),
 'Extractor':(0,REAR,CY),'Trigger':(0,31,23),'Hammer':(0,10,48),
 'CylinderStop':(4.7,37,24),'Latch':(-9,23,53),'LatchPin':(0,33,CY),
 'LoaderGuide':(0,REAR,CY),'LoaderBody':(0,REAR,CY),'LoaderRelease':(0,20,CY),
 'RoundGuide':chamber(0),'InsertRound':chamber(0),
 **{'Live'+str(i):chamber(i) for i in range(6)},
 **{'Case'+str(i):chamber(i) for i in range(6)},
 **{'LoaderRound'+str(i):chamber(i) for i in range(6)}}
PARENTS={'Cylinder':'Crane','Extractor':'Cylinder','LatchPin':'Root',
 'LoaderGuide':'Crane','LoaderBody':'LoaderGuide','LoaderRelease':'LoaderGuide','RoundGuide':'Crane','InsertRound':'RoundGuide',
 **{'Live'+str(i):'Cylinder' for i in range(6)},
 **{'Case'+str(i):'Cylinder' for i in range(6)},
 **{'LoaderRound'+str(i):'LoaderGuide' for i in range(6)}}
SOCKETS={'Socket_Muzzle':(0,MUZZLE,BORE),'Socket_Foregrip':(-14,0,0),
 'Socket_Butt':(0,-21,-22),'Socket_Eye':EYE,
 'Socket_Ejection':(0,REAR,CY),'Socket_MagWell':(0,REAR,CY),
 'Socket_Magazine':(0,REAR,CY),'Socket_Cylinder':(0,REAR,CY),
 'Socket_Speedloader':(0,REAR,CY),'Socket_Round':chamber(0)}
RIDING={'Socket_Cylinder':'Cylinder','Socket_Speedloader':'LoaderGuide','Socket_Round':'RoundGuide'}
