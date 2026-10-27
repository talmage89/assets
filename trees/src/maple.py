"""Decurrent red-maple family controls; all dimensions are meters."""
SEED=8241
HEIGHT=12.40
DBH=.36
CROWN_WIDTH=9.95
CROWN_BASE=1.90
CROWN_CENTER=(0,0,(HEIGHT+CROWN_BASE)/2)
FORK_HEIGHT=2.65
CARD_SIZE=.66
CARD_COUNT=7800
NORMAL_BEND=.90
LEAF_RECTS=tuple(((i%4)/4+.002,(i//4)/4+.002,(i%4+1)/4-.002,(i//4+1)/4-.002) for i in range(8))
BARK_RECT=(.01,.51,.99,.99)
BARK_UV_CUTS=(.8,2.0)

# Species surface and construction controls. No reference pixels are inputs.
MASS_INTERLOCK=.36
UPPER_MASS_BREADTH=1.42
INNER_BRANCHLET_SHARE=.17
ROOT_FLARE_HEIGHT=.72
ROOT_FLARE_RATIO=1.60
LEAF_COLOR=(71,99,53)
LEAF_LENGTH=(.066,.094)
PETIOLE_COLOR=(142,47,38)
TWIG_COLOR=(91,54,42)

MASS_NORMAL_BLEND=.60

BARK=dict(old_transition=(3.7,2.4),ridge_width_m=(.022,.040),plate_length_m=(.10,.30),grain_frequency=210,relief_m=.0030,
          field_circumference=1.13,field_height=4.2,young=(.012,.010,.0065),mature=(.0035,.0022,.00115),
          fissure=(.00045,.00032,.00018),flake=(.0085,.0057,.0032))
LEAF_PROFILE_3=((0,0),(-.20,.015),(-.34,.10),(-.44,.25),(-.40,.38),
                (-.54,.64),(-.32,.62),(-.23,.57),(-.21,.78),(0,1))
LEAF_PROFILE_5=((0,0),(-.20,.015),(-.34,.10),(-.49,.28),(-.34,.32),
                (-.40,.40),(-.54,.64),(-.32,.62),(-.23,.57),(-.21,.78),(0,1))
LEADER_AZIMUTHS=(-49,43,139,224)
LEADER_FORK_Z=(2.14,2.30,2.49,2.66)
LEADER_REACH=(1.52,1.63,1.60,1.45)
LEADER_TOP=(7.70,8.00,7.40,7.90)
ROOT_COUNT=5
ROOT_REACH=(.33,.43)

# This specimen’s scaffold destinations; algorithms stay in growth.py.
MASS_LAYOUT=[
 [( -73,3.20,3.03,1.58,1.45,1.25),(-23,3.35,5.45,1.50,1.40,1.36),(-55,2.60,8.35,1.45,1.40,1.58),(-24,1.75,10.85,1.12,1.05,1.22),( -5,1.10,4.65,1.50,1.40,1.60),(-57,1.65,9.65,1.26,1.28,1.42)],
 [(  12,3.25,4.05,1.58,1.45,1.50),( 67,3.25,6.05,1.50,1.45,1.35),( 32,2.45,8.75,1.32,1.28,1.38),( 62,1.85,11.05,1.05, .96,1.08),(65,1.65,7.20,1.40,1.38,1.50)],
 [( 119,3.25,3.45,1.65,1.48,1.45),(165,3.40,5.75,1.48,1.45,1.40),(124,2.65,8.20,1.40,1.35,1.30),(157,1.75,10.40,1.02,1.03,1.30),(148,1.05,6.65,1.32,1.25,1.40),(140,1.60,9.50,1.25,1.28,1.45)],
 [( 212,3.15,3.80,1.55,1.50,1.55),(252,3.30,6.10,1.52,1.43,1.35),(207,2.50,8.60,1.38,1.30,1.28),(239,1.60,10.85, .98,1.02,1.22),(235,1.05,7.80,1.40,1.35,1.45),(225,1.45,5.25,1.45,1.38,1.50)],
]

ASSET="RedMaple"
ARCHITECTURE="decurrent"
PLACEHOLDER=False
HEIGHT_REFERENCE=12.10
MIN_CARD_HEIGHT=2.22
MIN_INNER_HEIGHT=2.55
LEAF_ALTERNATE=False
BARK_NAME="Maple bark / dark gray-brown flaky ridges"

LEAF_NODES=(4,5)

LEAF_SHADER={}
