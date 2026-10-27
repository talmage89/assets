"""Final GLB camera/pose recipes; changing presentation never repacks the atlas."""
from config import LOOKDEV_SHOTS

FINAL_VIEWS={
 'hero':dict(LOOKDEV_SHOTS['front_three_quarter'],lens=65),
 'front':dict(location=(0,-12,1.10),target=(0,0,1.10),ortho=3.05,aspect=1.20,studio_yaw=-35),
 'side':dict(LOOKDEV_SHOTS['side']),
 'back':dict(location=(0,12,1.10),target=(0,0,1.10),ortho=3.05,aspect=1.20,studio_yaw=145),
 'top':dict(location=(0,0,12),target=(0,0,0),ortho=6.65,aspect=1.25,roll=1.5707963267948966,studio_yaw=-35),
 'front_detail':dict(LOOKDEV_SHOTS['front_detail']),
 'wheel_detail':dict(LOOKDEV_SHOTS['wheel_detail']),
 'interior':dict(location=(2.90,-.45,1.95),target=(.20,-.55,1.18),lens=48,aspect=1.45,studio_yaw=-35,paint='Graphite',parts={'Door_FR':dict(axis='Z',angle=-68)},exposure=-1.2),
 'scale':dict(location=(9,-11,3.3),target=(.35,-.1,1.00),lens=53,aspect=1.6,studio_yaw=-35,human=True,human_offset=(2.60,-1.0,0)),
 'lamps_lit':dict(LOOKDEV_SHOTS['lamps_lit']),
}
