"""A new C2 longitudinal loft for the S240 roof, sail and deck stamping.

The old canopy combined station peaks, a Gaussian header displacement, a rear
lift, and a protected/unprotected fit boundary. Those independent corrections
survive subdivision as waves. This die has one sagittal curve, one crown curve
and one roof-rail curve. Its sections are evaluated before any part is cut.
Dimensions are authored in meters; no photograph or saved mesh is read.
"""
import math
import numpy as np
from functools import lru_cache
from bisect import bisect_right


class Curve:
    """Natural cubic through sparse construction stations, continuous in C2."""
    def __init__(self, stations):
        self.x=np.array([p[0] for p in stations]);self.y=np.array([p[1] for p in stations])
        h=np.diff(self.x);a=np.eye(len(h)+1);b=np.zeros(len(h)+1)
        for i in range(1,len(h)):
            a[i,i-1:i+2]=(h[i-1],2*(h[i-1]+h[i]),h[i])
            b[i]=6*((self.y[i+1]-self.y[i])/h[i]-(self.y[i]-self.y[i-1])/h[i-1])
        self.m=np.linalg.solve(a,b).tolist();self.x=self.x.tolist();self.y=self.y.tolist()

    def __call__(self,x):
        i=max(0,min(len(self.x)-2,bisect_right(self.x,x)-1))
        h=self.x[i+1]-self.x[i];a=(self.x[i+1]-x)/h;b=(x-self.x[i])/h
        return float(a*self.y[i]+b*self.y[i+1]+((a*a*a-a)*self.m[i]+(b*b*b-b)*self.m[i+1])*h*h/6)


spine=Curve([(-1.30,.932),(-1.08,.971),(-.49,1.281),(-.27,1.378),
             (.05,1.435),(.36,1.450),(.69,1.428),(1.26,1.288),
             (1.76,1.130),(1.99,1.080),(2.16,1.084),(2.36,1.111),(2.50,1.096)])
# Roof-rail tangent stations preserve the accepted shoulder and 22-degree
# upper door draw. The earlier narrow experimental rail intersected the wall
# below its shoulder at the front door, changing the accepted section.
rail=Curve([(-1.30,.87),(-1.03,.88),(-.65,.834),(-.47,.792),(-.30,.758),
            (.05,.731),(.36,.729),(.69,.742),(1.04,.800),
            (1.40,.878),(1.74,.916),(2.50,.92)])
crown=Curve([(-1.30,.045),(-1.08,.035),(-.65,.040),(-.3,.045),(.7,.045),(1.3,.068),(1.7,.090),(1.99,.065),(2.5,.065)])


def ease(a,b,x):
    t=max(0.,min(1.,(x-a)/(b-a)));return t*t*t*(10+t*(-15+6*t))


@lru_cache(maxsize=65536)
def section_parameters(y):return spine(y),rail(y),crown(y)


def height(x,y):
    from sedan_body import hood_height,deck_height
    # Positive-part fillet, a measured roof-rail draw rather than a hard
    # hinge between an almost flat roof and a straight extruded side profile.
    h,e,c=section_parameters(y)
    # One gentle optical crown through the windshield package; join it to
    # the hood and roof outside the physical opening, without an S bend.
    t=y+1.0773;wind=.971+.530*t-.009*t*t
    weight=ease(-1.15,-1.07,y)*(1-ease(-.33,-.24,y))
    h=h*(1-weight)+wind*weight
    d=abs(x)-e;r=.018
    roll=.5*(d+math.sqrt(d*d+r*r))
    z=h-c*x*x-2.25*roll
    if y<-.97:
        w=ease(-1.30,-.97,y);z=hood_height(x,y)*(1-w)+z*w
    if y>1.99:
        w=ease(1.99,2.16,y);z=z*(1-w)+deck_height(x,y)*w
    return z


def field(p):
    from sedan_body import section_field
    x,y,z=p;wall=section_field(p,wall_only=True);top=z-height(x,y)
    r=.012 if y<0 else .014;m=max(wall,top)
    return m+r*math.log(math.exp((wall-m)/r)+math.exp((top-m)/r))


def section(y,w,belt,top):
    """Fresh ordered radial loft section above the retained shoulder draw.

    No former upper control row is reused: transverse stations progress by
    angle around the die. All share the same physical Y, so no header/sail
    displacement can double a row back across its neighbor.
    """
    from mathutils import Vector
    from sedan_body import body_section,crease_rows,longitudinal,shoulder_height
    lower=crease_rows(body_section(y,w,belt,top),False)
    physical=longitudinal(y)
    # Retain the accepted A-rake/header package, expressed as section spacing,
    # rather than the old height-dependent displacement through each section.
    yy=physical-.106*math.exp(-((y+.14)/.25)**2)
    h,e,_=section_parameters(yy);center=Vector((0,yy,.60))
    belt_z=max(min(belt,h-.045),lower[10][2]+.008)
    lo,hi=0.,1.1
    for _ in range(30):
        x=(lo+hi)/2
        if field((x,yy,belt_z))>0:hi=x
        else:lo=x
    end_angle=math.atan2((lo+hi)/2,belt_z-.60)
    roof_x=max(.58,min(.84,e-.005));lo,hi=.60,1.70
    for _ in range(30):
        z=(lo+hi)/2
        if field((roof_x,yy,z))>0:hi=z
        else:lo=z
    edge_angle=min(math.atan2(roof_x,(lo+hi)/2-.60),end_angle*.93)
    angles=[0,edge_angle*.30,edge_angle*.56,edge_angle*.72,edge_angle*.86,edge_angle,
            edge_angle+(end_angle-edge_angle)*.17,edge_angle+(end_angle-edge_angle)*.55,
            edge_angle+(end_angle-edge_angle)*.90,end_angle]
    upper=[]
    for a in angles:
        d=Vector((math.sin(a),0,math.cos(a)));lo,hi=0.,1.8
        for _ in range(30):
            t=(lo+hi)/2
            if field(center+d*t)>0:hi=t
            else:lo=t
        upper.append(tuple(center+d*((lo+hi)/2)))
    return upper+lower[10:]
