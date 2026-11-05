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
    d=math.sqrt(x*x+.002**2)-e;r=.018
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
    r=.012+.002*ease(-.30,.30,y);m=max(wall,top)
    return m+r*math.log(math.exp((wall-m)/r)+math.exp((top-m)/r))


def exact_loft(ob):
    """Evaluate the upper C2 die, instead of shipping subdivision-fit phase.

    The regular cage supplies the chart and the retained lower construction.
    Its finite subdivision approximation can be millimeters inside a tight
    die roll. Sample that die itself before any opening/panel is cut, so game,
    source, steel and optics use one actual surface and its own derivatives.
    """
    from mathutils import Vector
    import json
    maximum=0.;residual=0.;count=0
    for v in ob.data.vertices:
        original=v.co.copy()
        if original.z<=.70:continue
        p=original.copy();weight=ease(.70,.76,p.z)
        for _ in range(5):
            value=field(p)
            if abs(value)<2e-8:break
            h=.0001;x,y,z=p
            gradient=Vector(tuple((field((x+(h if k==0 else 0),y+(h if k==1 else 0),z+(h if k==2 else 0)))-
                field((x-(h if k==0 else 0),y-(h if k==1 else 0),z-(h if k==2 else 0))))/(2*h) for k in range(3)))
            p-=gradient*(value/gradient.length_squared)
        v.co=original.lerp(p,weight);maximum=max(maximum,(v.co-original).length);count+=1
        if original.z>=.76:residual=max(residual,abs(field(v.co)))
    ob.data.update()
    if residual>2e-6:raise ValueError(('Upper loft evaluation did not converge to its die',residual))
    ob['upper_exact_loft']=json.dumps(dict(vertices=count,maximum_subdivision_approximation_distance_m=maximum,maximum_die_residual_m=residual,lower_transition_z_m=[.70,.76],construction='C2 manufactured die evaluated before panel, glazing and lamp cuts'))
    print('S240_EXACT_UPPER_LOFT',count,'vertices; subdivision deviation',maximum,'residual',residual,flush=True)


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


def cut_hood(bm,names,parent):
    """Retain the accepted hood plan independently of the loft's cage columns."""
    import bmesh
    from mathutils import Vector
    width=Curve([(-1.90,.722),(-1.86,.725),(-1.512,.747),(-1.355,.769),
                 (-1.255,.832),(-1.152,.842),(-1.090,.838)])
    stations=[-1.90+(-1.090+1.90)*i/8 for i in range(9)]
    def candidates():
        return [f for f in bm.faces if names[f.material_index] in
                ['Hood','Front fender_L','Front fender_R','Greenhouse_L','Greenhouse_R']
                and -1.94<f.calc_center_median().y<-1.04 and f.calc_center_median().z>.72]
    def split(fs,point,normal):
        es={e for f in fs for e in f.edges};vs={v for f in fs for v in f.verts}
        bm.verts.index_update();bm.edges.index_update();bm.faces.index_update()
        bmesh.ops.bisect_plane(bm,geom=sorted(vs,key=lambda v:v.index)+sorted(es,key=lambda e:e.index)+sorted(fs,key=lambda f:f.index),
            dist=1e-8,plane_co=point,plane_no=normal,clear_inner=False,clear_outer=False)
    for y in stations:split(candidates(),(0,y,0),(0,1,0))
    for a,c in zip(stations,stations[1:]):
        slope=(width(c)-width(a))/(c-a)
        for sign in [-1,1]:
            split([f for f in candidates() if a-1e-7<f.calc_center_median().y<c+1e-7],
                  (sign*width(a),a,0),(sign,-slope,0))
    for f in candidates():
        p=f.calc_center_median()
        if stations[0]<p.y<stations[-1]:
            if abs(p.x)<width(p.y):f.material_index=names.index('Hood')
            elif names[f.material_index]=='Hood':f.material_index=names.index('Front fender_L' if p.x<0 else 'Front fender_R')
        elif p.y>=stations[-1] and names[f.material_index]=='Hood':
            f.material_index=names.index('Greenhouse_L' if p.x<0 else 'Greenhouse_R')
    for v in {v for f in candidates() for v in f.verts}:
        p=v.co
        if stations[0]-1e-6<=p.y<=stations[-1]+1e-6 and abs(abs(p.x)-width(p.y))<.0004:
            hit=parent.ray_cast(Vector((p.x,p.y,3)),Vector((0,0,-1)),4)[0]
            if hit is None:raise ValueError('Hood cut misses its parent stamping')
            v.co.z=hit.z
