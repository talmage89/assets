"""Checkpoint policy, not a claim of delivery readiness."""
BUDGETS={'Pickup':70000}
BOUNDS={'Pickup':dict(size=(2.02946,5.89026,1.96088),tolerance=(.025,.002,.002))}
SHOTS={
 'front_three_quarter':dict(location=(8,-10,3.6),target=(0,-.10,.98),lens=57,aspect=1.6),
 'rear_three_quarter':dict(location=(-8,10,3.6),target=(0,.15,.96),lens=57,aspect=1.6,studio_yaw=180),
 'side':dict(location=(-12,0,1),target=(0,0,1),ortho=6.7,aspect=2.0),
 'front':dict(location=(0,-12,1),target=(0,0,1),ortho=3.0,aspect=1.0),
 'top':dict(location=(0,0,12),target=(0,0,0),ortho=6.7,aspect=1.2,roll=1.5707963267948966),
 'stripes_front':dict(location=(7.5,-9.5,4.6),target=(0,-.1,1),lens=57,aspect=1.6),
 'stripes_side':dict(location=(-10,-2.0,3.7),target=(0,0,1),lens=57,aspect=1.8),
}
STUDIO=dict(scale=3,light_center=(0,0,0),backdrop_half_width=12)
# The checkpoint does not certify motion; no swept-motion tests are declared yet.
MOTIONS=[]
