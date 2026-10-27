"""Surface comparisons, not a survey of the photographed municipalities.

Warning is compared to one nominal 24-in-deep half of the photographed panel.
Width is a 5-ft assumption; neither this photo nor the Ohio street is a scale
certificate. Municipal drawings, rather than image fits, set delivered dimensions.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from dimensions import *
MATCHES={
'warning_material':dict(title='Used curb ramp / concrete, flow line and tactile finish',
    photo='refs/ramp.jpg',crop=(1200,800,3300,2300),location=(2.3,-13,2.5),target=(4.7,-10.3,0),lens=35,
    landmarks=[
        dict(world=(BACK,-CORE-PANEL-PANEL/2,.002),pixel=(1670,1314)),
        dict(world=(BACK,-CORE-PANEL+PANEL/2,.002),pixel=(2187,1099)),
        dict(world=(BACK+.6096,-CORE-PANEL+PANEL/2,.0528),pixel=(2490,1236)),
        dict(world=(BACK+.6096,-CORE-PANEL-PANEL/2,.0528),pixel=(1940,1475)),
    ]),
'road_material':dict(title='Quiet local street / oxidized asphalt and sparse repairs',
    photo='refs/arlington.jpg',crop=(0,1750,3883,2912),location=(0,-30,1.7),target=(0,-10,0),lens=35,
    landmarks=[
        dict(world=(-ASPHALT_HALF,-24.5,ROAD_EDGE),pixel=(300,2400)),
        dict(world=(ASPHALT_HALF,-24.5,ROAD_EDGE),pixel=(3400,2400)),
        dict(world=(-ASPHALT_HALF,-11.5,ROAD_EDGE),pixel=(1300,2080)),
        dict(world=(ASPHALT_HALF,-11.5,ROAD_EDGE),pixel=(2480,2080)),
    ]),
}

# The photographed grate is a broader municipal casting than this family's
# narrow-pan adaptation. Compare iron/patina/grass and show residuals honestly;
# these fits never define the physical module sizes.
MATCHES['inlet_material']=dict(title='Used combination inlet / oxide, depressed pan and grass edge',
    photo='refs/curb-inlet.jpg',crop=(90,540,760,1120),location=(2,-16,1.8),target=(3.95,-13.25,0),lens=48,
    landmarks=[
        dict(world=(FACE-.405,-13.2588+.45,-.024),pixel=(154,703)),
        dict(world=(FACE-.020,-13.2588+.45,-.024),pixel=(425,720)),
        dict(world=(FACE-.020,-13.2588-.45,-.024),pixel=(610,937)),
        dict(world=(FACE-.405,-13.2588-.45,-.024),pixel=(234,929)),
    ])
MATCHES['manhole_material']=dict(title='Used cast cover / grip lands and dirt at the frame',
    photo='refs/manhole-grid.jpg',crop=(800,500,4650,3500),location=(-1.1,-17.8308,1.3),target=(-1.1,-17.8308,0),lens=42,
    landmarks=[
        dict(world=(-1.1-MANHOLE_COVER/2,-17.8308,road_z(1.1)),pixel=(1630,2050)),
        dict(world=(-1.1+MANHOLE_COVER/2,-17.8308,road_z(1.1)),pixel=(4380,2050)),
        dict(world=(-1.1,-17.8308+MANHOLE_COVER/2,road_z(1.1)),pixel=(2910,690)),
        dict(world=(-1.1,-17.8308-MANHOLE_COVER/2,road_z(1.1)),pixel=(3030,3430)),
    ])

# Revised dark used casting: general fit/finish only; photographed pan is wider.
MATCHES['inlet_material'].update(
    title='Used dark combination inlet / charcoal iron and worn bar tops',
    photo='refs/used-inlet-dark.jpg',crop=(0,0,1240,960),
    landmarks=[
        dict(world=(FACE-.405,-13.2588+.45,-.0254),pixel=(31,399)),
        dict(world=(FACE-.020,-13.2588+.45,-.0254),pixel=(416,161)),
        dict(world=(FACE-.020,-13.2588-.45,-.0254),pixel=(944,486)),
        dict(world=(FACE-.405,-13.2588-.45,-.0254),pixel=(584,941)),
    ])

# Wheel-polished dark lands with retained sediment between them; heavily
# weathered specimen, used to judge material response rather than its pattern.
MATCHES['manhole_material'].update(
    title='Used traffic casting / dark polished lands and rusty retained edges',
    photo='refs/manhole.jpg',crop=(0,0,2012,2012),
    landmarks=[
        dict(world=(-1.1-MANHOLE_COVER/2,-17.8308,road_z(1.1)),pixel=(63,1006)),
        dict(world=(-1.1+MANHOLE_COVER/2,-17.8308,road_z(1.1)),pixel=(1930,1006)),
        dict(world=(-1.1,-17.8308+MANHOLE_COVER/2,road_z(1.1)),pixel=(1006,75)),
        dict(world=(-1.1,-17.8308-MANHOLE_COVER/2,road_z(1.1)),pixel=(1006,1905)),
    ])
