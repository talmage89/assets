"""X220 framing in the unchanged C150 gallery studio."""
import math
from suv_lookdev import SHOTS

VIEWS={
 'hero':dict(location=(6.7,-8.4,2.80),target=(0,-.08,.86),lens=65,aspect=1.6,studio_yaw=-35),
 'rear':dict(location=(-6.7,8.4,2.80),target=(0,.12,.88),lens=65,aspect=1.6,studio_yaw=145),
 'front':dict(location=(0,-12,.92),target=(0,0,.92),ortho=2.65,aspect=1.2,studio_yaw=-35),
 'side':dict(location=(12,0,.92),target=(0,0,.92),ortho=5.25,aspect=2.0,studio_yaw=-25,exposure=-2.8),
 'back':dict(location=(0,12,.92),target=(0,0,.92),ortho=2.65,aspect=1.2,studio_yaw=145),
 'top':dict(location=(0,0,12),target=(0,0,0),ortho=5.25,aspect=1.25,roll=math.pi/2,studio_yaw=-35),
 'face':dict(SHOTS['face'],studio_yaw=-35,paint='Graphite'),
 'lamp':dict(SHOTS['lamp_unlit'],studio_yaw=-35,paint='Graphite'),
 'quarter':dict(SHOTS['rear_quarter'],studio_yaw=145,paint='Graphite'),
 'wheel':dict(SHOTS['wheel'],studio_yaw=-50),
 'cargo':dict(SHOTS['cargo_open'],studio_yaw=145),
 'opened':dict(SHOTS['opened'],studio_yaw=-35),
 'lamps_lit':dict(SHOTS['lamp_lit'],studio_yaw=-35,paint='Graphite'),
 'scale':dict(location=(7.7,-9.5,2.90),target=(.45,-.10,.92),lens=53,aspect=1.6,studio_yaw=-35,human=True,human_offset=(2.2,-.7,0)),
}
