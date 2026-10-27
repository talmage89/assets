"""Pin oak specimen: 25-year street tree; finished summer surface controls.

Dimensions are authored within the brief, not inferred from unmeasured photos.
The accepted maple namespace is inherited only for shared atlas/delivery policy.
"""
from maple import *
ASSET='PinOak'
ARCHITECTURE='excurrent'
SEED=19463
HEIGHT=16.70
HEIGHT_REFERENCE=16.70
DBH=.45
CROWN_WIDTH=10.1
CROWN_BASE=2.5
CROWN_CENTER=(0,0,9.6)
FORK_HEIGHT=0
CARD_COUNT=7140
LOWER_EXTRA_CARDS=420
CARD_SIZE=.78
NORMAL_BEND=.42
MASS_NORMAL_BLEND=.48
NORMAL_MASS_BLEND_UPPER=.28
MASS_INTERLOCK=.08
INNER_BRANCHLET_SHARE=.28
MIN_CARD_HEIGHT=2.95
MIN_INNER_HEIGHT=3.10
PLACEHOLDER=False
LEAF_ALTERNATE=True
LEAF_COLOR=(77,105,48)
LEAF_LENGTH=(.08,.13)
PETIOLE_COLOR=(95,91,47)
TWIG_COLOR=(77,65,43)
ROOT_REACH=(.38,.43)
ROOT_FLARE_HEIGHT=.42
ROOT_FLARE_RATIO=1.24
# Legacy placeholder outline controls; finished blades are in oak_leaves.py.
LEAF_PROFILE_3=((0,0),(-.16,.05),(-.40,.23),(-.31,.29),(-.08,.30),(-.08,.36),
                (-.48,.56),(-.39,.62),(-.10,.56),(-.07,.62),(-.27,.85),(-.16,.83),(0,1))
LEAF_PROFILE_5=LEAF_PROFILE_3
BARK_NAME='Pin oak / shallow gray-brown ridges'
BARK=dict(old_transition=(9.,2.5),ridge_width_m=(.02,.05),plate_length_m=(.10,.40),
          grain_frequency=185,relief_m=.0034,ridge_breakup=.85,field_circumference=1.414,field_height=5.5,
          roughness=.86,specular=.06,young=(.115,.092,.058),mature=(.095,.075,.043),
          fissure=(.030,.017,.007),flake=(.170,.120,.064),dead=(.060,.055,.045))

# Irregular internodes, branch-length envelope and true ramification.
LATERALS=dict(count=40,base_z=4.25,top_z=15.65,
              reach_profile=((4.25,3.0),(5.3,3.9),(6.5,4.55),(7.2,5.05),
                             (9.3,4.65),(10.5,3.65),(12.,2.35),(13.36,1.5),(14.5,.85),(15.65,.35)),
              lower_zone=7.10,upper_zone=11.8)
DEAD_PINS=dict(count=22,base_z=1.8,top_z=5.25,exposed_length=(.18,.34),radius=(.005,.008))
MIN_WOOD_RADIUS=.0055
DEAD_WOOD_RADIUS=.0015
WOOD_RESOLUTION={2:(7,5),3:(3,4)}
LEAF_NODES=(12,13)
LEAF_SHADER=dict(name='Pin oak glossy summer foliage',specular=.18,normal_strength=.85,back_multiplier=(1.40,1.45,1.20,1),back_saturation=.78,transmission=.32)
APEX_CARD_HEADROOM=.32

# A light-space cap on local branch growth, authored from the round-2 brief.
# It trims sparse outliers; it is never sampled as a foliage volume.
CROWN_RADII=((2.95,3.10),(4.2,4.10),(5.5,4.90),(6.6,5.15),(7.8,4.85),
             (9.7,4.50),(11.1,3.95),(12.6,3.25),(13.8,2.55),(15.,1.55),(15.9,.65),(16.38,.08))

BARK_UV_CUTS=(.4,.8,2.,4.,6.,8.,10.,12.,14.,16.)
CARD_SCALE=(.99,1.015)

ROOT_LOBES=.24
