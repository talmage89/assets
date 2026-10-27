from dimensions import *
TITLE='Aldervale / twenty-year residential street'
SHOTS={
'hero':dict(location=(1.0,-37,road_z(1.0)+1.7),target=(1.6,-24,.10),lens=28,aspect=1.6),
'streetside':dict(location=(7.05,-32,CURB_HEIGHT+(7.05-WALK_IN)*WALK_SLOPE+1.7),target=(.7,-16,.12),lens=28,aspect=1.6),
'block':dict(location=(42,-53,47),target=(0,-2,0),lens=43,aspect=1.4),
'repetition':dict(location=(0,0,95),target=(0,0,0),ortho=105,aspect=1.1),
'curb':dict(location=(2.9,-14.5,1.1),target=(4.02,-13.1,.045),lens=52,aspect=1.5),
'joint':dict(location=(7.3,-16.6,1.0),target=(6.8,-15.5448,.16),lens=52,aspect=1.5),
'ramp':dict(location=(2.4,-13.7,2.6),target=(5.45,-10.2108,.09),lens=43,aspect=1.5),
'drivecut':dict(location=(.2,19,2.7),target=(4.15,23.9268,.07),lens=40,aspect=1.5),
'driveway':dict(location=(.1,-28.5,3.7),target=(6.5,-23.9268,.15),lens=38,aspect=1.5),
'inlet':dict(location=(2.9,-14.8,.95),target=(3.98,-13.2588,.015),lens=48,aspect=1.5),
'manhole':dict(location=(-.2,-19.5,1.15),target=(-1.1,-17.8308,.06),lens=48,aspect=1.5),
'lawn':dict(location=(7.1,-19.6,.62),target=(6.15,-17.9,.16),lens=48,aspect=1.5),
'scale':dict(location=(14,-23,7),target=(4,-10,.65),lens=44,aspect=1.5,human=True),
'front':dict(location=(0,-105,40),target=(0,0,0),ortho=60,aspect=1.25),
'side':dict(location=(100,0,65),target=(0,0,0),ortho=98,aspect=1.25),
'back':dict(location=(0,105,40),target=(0,0,0),ortho=60,aspect=1.25),
}

SHOTS['dressed']=dict(SHOTS['hero'],dress=True)
SHOTS['tile_asphalt']=dict(location=(-24,0,25),target=(-24,0,0),ortho=18.288,aspect=1)
SHOTS['tile_concrete']=dict(location=(0,0,20),target=(0,0,0),ortho=9.144,aspect=1)
SHOTS['tile_lawn']=dict(location=(24,0,20),target=(24,0,0),ortho=9.144,aspect=1)
