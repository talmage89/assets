"""Blender-independent unequal-height catenaries and adaptive wire meshes.

Sag is the vertical distance below the endpoint chord at horizontal midspan.
No reference image, sampled asset or numerical library is required.
"""
import math


def sag_from_tension(start,end,mass_kg_m,horizontal_tension_n,gravity=9.80665):
    """Exact mid-chord sag for H / distributed self weight (a = H / w).

    H is the horizontal tension component, not breaking strength or total
    endpoint tension. Mass is the whole supported cable assembly per metre.
    Temperature, ice, wind and elastic state must be supplied by a real solver
    as an appropriate tension/weight case; this function does not invent them.
    """
    if mass_kg_m<=0 or horizontal_tension_n<=0:raise ValueError('Positive mass and horizontal tension required')
    length=math.hypot(end[0]-start[0],end[1]-start[1])
    if length<.05:raise ValueError('Need a horizontal span >= .05 m')
    a=horizontal_tension_n/(mass_kg_m*gravity)
    h=length/(2*a);k=math.asinh((end[2]-start[2])/(2*a*math.sinh(h)))
    return a*math.cosh(k)*(2*math.sinh(h/2)**2)


def catenary(start, end, sag):
    p, q = tuple(start), tuple(end)
    length = math.hypot(q[0]-p[0], q[1]-p[1])
    if length < .05 or sag <= 0 or sag > length*.4:
        raise ValueError('Need a horizontal span >= .05 m and 0 < sag <= .4 span')
    rise = q[2]-p[2]
    # For a given a, unequal supports shift the low point by asinh(dz / S).
    def parameters(a):
        h=length/(2*a)
        k=math.asinh(rise/(2*a*math.sinh(h)))
        return length/2-a*k, h, k
    def mid_sag(a):
        _,h,k=parameters(a)
        return a*math.cosh(k)*(2*math.sinh(h/2)**2)
    lo,hi=length/20,length*length/max(sag,.00001)*2
    for _ in range(90):
        a=(lo+hi)/2
        if mid_sag(a)>sag:lo=a
        else:hi=a
    a=(lo+hi)/2;x0,_,_=parameters(a)
    def point(t):
        x=t*length
        # Difference-of-cosh identity avoids cancellation on shallow spans.
        dz=2*a*math.sinh(x/(2*a))*math.sinh((x-2*x0)/(2*a))
        return (p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1]),p[2]+dz)
    low=max(0,min(1,x0/length))
    return dict(point=point,a=a,low_t=low,minimum_z=point(low)[2],horizontal_m=length,
                arc_m=a*(math.sinh((length-x0)/a)-math.sinh(-x0/a)),sag_m=sag)


def sample(start,end,sag,tolerance=.008,max_step=4.):
    if tolerance<=0 or max_step<=0:raise ValueError('Positive sampling tolerances required')
    # Uniform catenary stations avoid the old power-of-two oversampling. Each
    # interval is independently screened at three interior positions, then
    # refined below if necessary. The API and 8 mm / 4 m guarantees stay put.
    curve=catenary(start,end,sag);point=curve['point'];out=[(0.,point(0))]
    def split(t0,p0,t1,p1):
        tm=(t0+t1)/2;pm=point(tm)
        error=max(math.dist(point(t0+(t1-t0)*f),tuple(x+(y-x)*f for x,y in zip(p0,p1))) for f in (.25,.5,.75))
        if error>tolerance or math.dist(p0,p1)>max_step:
            split(t0,p0,tm,pm);split(tm,pm,t1,p1)
        else:out.append((t1,p1))
    count=max(1,math.ceil(curve['arc_m']/max_step),math.ceil(math.sqrt(sag/tolerance)))
    for i in range(count):split(i/count,point(i/count),(i+1)/count,point((i+1)/count))
    return [p for _,p in out],{k:v for k,v in curve.items() if k!='point'}


def screen_width(diameter,depth,height_px=1080,vertical_fov=50,minimum_px=.85):
    """Coverage-preserving far-wire policy, widths in metres and pixels."""
    metres_per_pixel=2*depth*math.tan(math.radians(vertical_fov)/2)/height_px
    actual=diameter/metres_per_pixel
    width=max(actual,minimum_px)
    return dict(actual_px=actual,width_px=width,coverage=min(1,actual/width),
                width_m=width*metres_per_pixel)


if __name__=='__main__':
    import argparse,json
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--start',nargs=3,type=float,required=True)
    p.add_argument('--end',nargs=3,type=float,required=True)
    p.add_argument('--sag',type=float,required=True)
    p.add_argument('--tolerance',type=float,default=.008)
    p.add_argument('--out',required=True)
    a=p.parse_args();points,report=sample(a.start,a.end,a.sag,a.tolerance)
    from pathlib import Path
    output=Path(a.out);output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(dict(points=points,**report),indent=2))
