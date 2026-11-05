"""H120 camera framing in the family's unchanged gallery lighting."""
from hatch_views import SHOTS
FINAL_VIEWS={
 'hero':dict(location=(5.9,-7.5,2.25),target=(0,-.10,.74),lens=65,aspect=1.6,studio_yaw=-35),
 'rear':dict(location=(-5.9,7.5,2.25),target=(0,.12,.74),lens=65,aspect=1.6,studio_yaw=145),
 'front':dict(location=(0,-10,.78),target=(0,0,.78),ortho=2.55,aspect=1.25,studio_yaw=-35),
 'side':dict(SHOTS['side'],exposure=-2.8),
 'back':dict(SHOTS['rear']),
 'top':dict(SHOTS['top'],roll=1.5707963267948966),
 'face':dict(SHOTS['face']),
 'lamp':dict(SHOTS['lamp_unlit']),
 'wheel':dict(SHOTS['wheel']),
 'rear_quarter':dict(SHOTS['rear_quarter']),
 'gate':dict(location=(.90,4.15,1.16),target=(0,2.13,.86),lens=85,aspect=1.5,studio_yaw=145,paint='Graphite'),
 'plate':dict(SHOTS['plate_detail']),
 'cargo':dict(SHOTS['cargo'],parts={'Liftgate':dict(axis='X',angle=82)}),
 'scale':dict(location=(6.8,-8.0,2.5),target=(.45,-.10,.75),lens=52,aspect=1.6,studio_yaw=-35,human=True,human_offset=(2.35,-.65,0)),
}
