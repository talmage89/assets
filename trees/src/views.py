"""Outdoor checkpoint cameras. Full-tree cameras are at human eye height."""
SHOTS={
 'daylight':dict(location=(16,-24,1.70),target=(0,0,6.1),lens=47,aspect=1),
 'crown_up':dict(location=(.75,-3.8,1.70),target=(0,0,6.0),lens=23,aspect=1),
 'scale':dict(location=(16,-24,1.70),target=(0,0,6.1),lens=47,aspect=1,human=True),
 'structure':dict(location=(16,-24,1.70),target=(0,0,6.1),lens=47,aspect=1,hide_leaves=True),
 'unions':dict(location=(1.6,-2.7,1.7),target=(0,0,2.7),lens=53,aspect=1.2,hide_leaves=True),
 'unions_reverse':dict(location=(-2.1,2.8,1.70),target=(0,0,2.75),lens=49,aspect=1.2,hide_leaves=True),
 'unions_upper':dict(location=(3.8,-5.5,1.70),target=(.15,0,4.9),lens=44,aspect=1.2,hide_leaves=True),
 'unions_upper_reverse':dict(location=(-4.6,5.5,1.70),target=(0,0,4.9),lens=44,aspect=1.2,hide_leaves=True),
 'dripline':dict(location=(3.8,-2.4,1.70),target=(.4,0,4.0),lens=22,aspect=1.2),
 'root_flare':dict(location=(1.1,-1.7,1.70),target=(0,0,.18),lens=55,aspect=1.2,hide_leaves=True),
 'silhouette':dict(location=(-15,-25,1.70),target=(0,0,6.1),lens=47,aspect=1,silhouette=True),
}

# Final presentation; the calibrated photo cameras above remain independent.
SHOTS.update({
 'hero':dict(location=(13.5,-21,1.70),target=(0,0,6.05),lens=52,aspect=1),
 'front':dict(location=(0,-26,6.2),target=(0,0,6.2),lens=47,aspect=1),
 'side':dict(location=(26,0,6.2),target=(0,0,6.2),lens=47,aspect=1),
 'back':dict(location=(0,26,6.2),target=(0,0,6.2),lens=47,aspect=1),
 'top':dict(location=(0,-.01,27),target=(0,0,4.5),lens=47,aspect=1),
 'bark':dict(location=(.85,-1.25,1.35),target=(0,0,.95),lens=56,aspect=1.2),
 'bark_2m':dict(location=(1.10,-1.67,1.70),target=(0,0,1.35),lens=40,aspect=1.2),
})

SHOTS['branchlet']=dict(location=(2.4831,-3.7335,2.9880),target=(1.7591,-3.1656,2.7518),lens=42,aspect=1.2)
