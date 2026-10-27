"""Authored summer specimens; meters. References constrain ranges, not vertices."""
SEED=419
HEIGHT=.90
CARD_SIZE=.135
LEAF_LENGTH=(.015,.025)
LEAF_COLOR=(44,79,30)
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
