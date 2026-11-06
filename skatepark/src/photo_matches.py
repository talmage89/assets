"""Camera evidence for period form comparisons; inferred unsurveyed anchors.

These are different original parks. Only named construction features enter
the fits; surrounding layouts are deliberately not photographic replicas.
Large residuals disclose how far a comparison can support a shape judgment.
"""
import math

def rim(t):
    phase=math.atan2(math.sin(t-math.pi/2),math.cos(t-math.pi/2));waist=1.60*math.exp(-(phase/.65)**2)
    return (-10.668+7.3152*math.cos(t)+.30*math.cos(2*t),5.1816*math.sin(t)*(1+.10*math.cos(t))-waist,0)
def anchor(p,uv):return dict(world=p,pixel=uv)
def normal(t):
    phase=math.atan2(math.sin(t-math.pi/2),math.cos(t-math.pi/2));w=1.60*math.exp(-(phase/.65)**2)
    dx=-7.3152*math.sin(t)-.60*math.sin(2*t);dy=5.1816*(math.cos(t)+.10*math.cos(2*t))+2*phase/.65**2*w
    length=math.hypot(dx,dy);return dy/length,-dx/length,0
def tile_bottom(t):
    h=1.6764+.4572*math.cos(t);theta=math.acos(1-h/2.4384);a=theta-.156/2.4384
    distance=2.4384*(math.sin(theta)-math.sin(a));p=rim(t);n=normal(t)
    return (p[0]-n[0]*distance,p[1]-n[1]*distance,-h+2.4384*(1-math.cos(a)))
def deck(t):
    p=rim(t);n=normal(t);return (p[0]+n[0]*.30,p[1]+n[1]*.30,0)

MATCHES={
 'alondra_bowl':dict(title='2012 kidney bowl / plan and section',photo='refs/alondra.jpg',crop=(120,320,986,653),
    location=(.543,-10.29865,3.86),target=(-.137,-9.6178,3.589),lens=38.65,lens_bounds_mm=(36,42),camera_height_m=(3.86,.5),
    # Contour correspondences were refined on this original rim with roll
    # constrained near vertical. They are inferred phases, not surveyed points.
    landmarks=[anchor(rim(t),uv) for t,uv in [(3.5554807,(222,406)),(1.88126525,(555,421)),(.06722843,(986,573)),(-1.01410311,(435,590)),(3.12466406,(295,367)),(-2.86505822,(259,454)),(.94895395,(850,480))]],
    exposure=-.2),
 'burnham_street':dict(title='2007 municipal hubba / steel-armored sloping ledge',photo='refs/20070329_Burnham_Park_Skatepark.JPG',crop=(1170,1110,1570,1270),
    isolate=['Stairs_5_3','StairReturnBank_3','SkatingFlatwork'],
    location=(18,-4,1.7),target=(14.8,0,.6),lens=80,lens_bounds_mm=(40,180),camera_height_m=(1.7,.3),
    landmarks=[anchor(p,uv) for p,uv in [((14.6304,-.762,.42),(1215,1199)),((15.0304,-.762,.42),(1270,1204)),((14.6304,.762,1.182),(1370,1134)),((15.0304,.762,1.182),(1440,1139)),((14.6304,1.762,1.182),(1480,1128)),((15.0304,1.762,1.182),(1540,1132)),((14.6304,-.762,0),(1215,1245)),((15.0304,-.762,0),(1270,1250))]],exposure=-.2),
 'memorial_coping':dict(title='2009 pool coping / projection and tile band',photo='refs/memorial.jpg',crop=(0,720,580,1220),
    location=(-13,-2,1.3),target=(-13,-5,0),lens=55,lens_bounds_mm=(24,100),camera_height_m=(1.3,.2),
    landmarks=[anchor(tuple(c+(.03175 if k==2 else 0) for k,c in enumerate(rim(t))),uv) for t,uv in [(-1.68,(8,836)),(-1.79,(175,855)),(-1.90,(365,897)),(-2.01,(560,955))]]+
       [anchor(tile_bottom(t),uv) for t,uv in [(-1.68,(8,887)),(-1.90,(365,957))]]+[dict(world=deck(-1.79),pixel=(175,820),weight=2)],exposure=-.2)
}

LIGHT={
 'alondra_bowl':dict(sun_direction=(-.35,.8,-1),sun_energy=3.8,sky_strength=.11,sky_saturation=.4),
 'burnham_street':dict(sun_direction=(-.5,.4,-1),sun_energy=1.3,sky_strength=.18,sky_saturation=.2,sun_angle_degrees=12),
 'memorial_coping':dict(sun_direction=(-.3,-.6,-1),sun_energy=1.2,sky_strength=.14,sky_saturation=.2,sun_angle_degrees=12),
}
# Neutral concrete ROIs avoid paint, people and foliage. Gains are comparison
# white-balance estimates, not an inversion of unknown photographic exposure.
NEUTRALS={'alondra_bowl':(160,330,210,350),'burnham_street':(1600,1150,1650,1180),'memorial_coping':(20,780,90,810)}
