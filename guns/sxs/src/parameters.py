"""Fictional visual asset envelope in mm. No working internal lockwork."""
from pathlib import Path
import hashlib
BREECH=115.0
MUZZLE=BREECH+660.4
BORE=44.0
SPACING=25.2
HINGE=(0,170,19)
OPEN=-42.0
LIFT=-10.0
EYE=(0,-123,67.0)
BUTT=-304.6
HEADS={'Root':(0,0,0),'Barrels':HINGE,'Forend':HINGE,'Extractor':(0,BREECH,BORE),
 'TopLever':(0,94,53),'Safety':(0,5,23),'Trigger':(2.6,64,4),
 'TriggerRear':(-2.6,31,4),'LockBolt':(0,130,13),
 **{name+side:(x,BREECH,BORE) for side,x in [('R',12.6),('L',-12.6)]
 for name in ('Live','Hull','InsertGuide','Insert')}}
PARENTS={'Forend':'Barrels','Extractor':'Barrels',
 **{name+side:'Extractor' for side in ('R','L') for name in ('Live','Hull','InsertGuide')},
 **{'Insert'+side:'InsertGuide'+side for side in ('R','L')}}
SOCKETS={'Socket_Muzzle':(0,MUZZLE,BORE),'Socket_Foregrip':(-18,270,12),
 'Socket_Butt':(0,BUTT,-43),'Socket_Eye':EYE,'Socket_Ejection':(0,BREECH,BORE),
 'Socket_MagWell':(0,BREECH,BORE),'Socket_Magazine':(0,BREECH,BORE),
 'Socket_SupportHand':(-18,270,12),'Socket_Shell':(12.6,BREECH,BORE),
 'Socket_ShellL':(-12.6,BREECH,BORE),
 'Socket_ChamberR':(12.6,BREECH,BORE),'Socket_ChamberL':(-12.6,BREECH,BORE),
 'Socket_MuzzleR':(10.9,MUZZLE,BORE),'Socket_MuzzleL':(-10.9,MUZZLE,BORE)}
RIDING={'Socket_SupportHand':'Forend','Socket_Shell':'InsertGuideR','Socket_ShellL':'InsertGuideL',
 'Socket_ChamberR':'Extractor','Socket_ChamberL':'Extractor',
 'Socket_MuzzleR':'Barrels','Socket_MuzzleL':'Barrels'}
def generator_digest():
 here=Path(__file__).parent;paths=[here/n for n in ('build.py','parameters.py','clips.py','interface.py')]
 paths += [here.parents[1]/'common'/n for n in ('shell12_visual.py','interface_v1_7.py')]
 h=hashlib.sha256()
 for p in paths:h.update(p.name.encode()+b'\0'+p.read_bytes())
 return h.hexdigest()
