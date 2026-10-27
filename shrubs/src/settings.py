"""Authored summer specimens; meters. References constrain ranges, not vertices."""
SEED=419
HEIGHT=.90
CARD_SIZE=.105
LEAF_LENGTH=(.015,.0205)
LEAF_COLOR=(52,100,45)
LEAF_RECTS=[(i*.25,j*.25,(i+1)*.25,(j+1)*.25) for j in range(2) for i in range(4)]
# Remaining half: future coarse hydrangea leaves/flower tiles; opaque stem strip.
WOOD_RECT=(.015,.59,.235,.985)
SHOTS={
 'three_quarter':dict(location=(1.65,-2.35,1.40),target=(0,0,.43),lens=55,aspect=1.25),
 'side':dict(location=(2.7,0,1.35),target=(0,0,.43),lens=55,aspect=1.25),
 'close_1m':dict(location=(.04,-1.266025403784,1.05),target=(.04,-.40,.55),lens=55,aspect=1.25),
 'scale':dict(location=(2.5,-4.5,2.40),target=(-.45,0,.87),lens=53,aspect=1.25,human=True),
 'base':dict(location=(.53,-1.12,.25),target=(0,0,.16),lens=57,aspect=1.25),
 'shaded_side':dict(location=(-1.8,1.9,1.30),target=(0,0,.42),lens=55,aspect=1.25),
 'structure':dict(location=(1.65,-2.35,1.40),target=(0,0,.43),lens=55,aspect=1.25,hide_leaves=True),
}

HYDRANGEA_SHOTS={
 'three_quarter':dict(location=(2.25,-3.05,1.85),target=(0,0,.57),lens=55,aspect=1.25),
 'side':dict(location=(3.65,0,1.80),target=(0,0,.58),lens=55,aspect=1.25),
 'close_1m':dict(location=(.16,-1.4960254,1.31),target=(.16,-.63,.81),lens=55,aspect=1.25),
 'scale':dict(location=(3.4,-5.5,2.85),target=(-.42,0,.91),lens=53,aspect=1.25,human=True),
 'base':dict(location=(.73,-1.45,.37),target=(0,0,.23),lens=52,aspect=1.25),
 'shaded_side':dict(location=(-2.3,2.8,1.80),target=(0,0,.59),lens=55,aspect=1.25),
 'structure':dict(location=(2.25,-3.05,1.85),target=(0,0,.57),lens=55,aspect=1.25,hide_leaves=True),
}

# Final views use the same daylight/camera as each accepted source hero.
for shots,height,distance in ((SHOTS,.43,2.7),(HYDRANGEA_SHOTS,.58,3.65)):
    shots['hero']=dict(shots['three_quarter'])
    shots['front']=dict(location=(0,-distance,height+.25),target=(0,0,height),lens=55,aspect=1.25)
    shots['back']=dict(location=(0,distance,height+.25),target=(0,0,height),lens=55,aspect=1.25)
    shots['top']=dict(location=(0,-.001,distance),target=(0,0,height),lens=48,aspect=1.25)
