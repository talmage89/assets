"""Section-station construction, original design. No image sampling.

Broad panels are ruled between near-planar sections. Features use explicit
piecewise-linear controls and short cubic tangent fillets, never additive
Gaussian/sine displacement. One section field is split into separate panels.
"""
import math
import pickup_spec as S


def blend(t):
    t=max(0,min(1,t));return t*t*(3-2*t)


def section(t, knots, radius=.003):
    """Linear control stations with C1 cubic tangent joins in a small support band.

    A radius here is the half-width along the independent coordinate. Straight
    regions stay exactly straight; curvature occurs only around authored bends.
    """
    def line(a,b,x):return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
    for i in range(1,len(knots)-1):
        a,b,c=knots[i-1:i+2];r=min(radius,(b[0]-a[0])*.35,(c[0]-b[0])*.35)
        if b[0]-r<t<b[0]+r:
            lo=b[0]-r;hi=b[0]+r;u=(t-lo)/(hi-lo)
            p=line(a,b,lo);q=line(b,c,hi)
            m=(b[1]-a[1])/(b[0]-a[0]);n=(c[1]-b[1])/(c[0]-b[0])
            return (2*u**3-3*u*u+1)*p+(u**3-2*u*u+u)*(hi-lo)*m+(-2*u**3+3*u*u)*q+(u**3-u*u)*(hi-lo)*n
    for a,b in zip(knots,knots[1:]):
        if t<=b[0]:return line(a,b,t)
    return line(knots[-2],knots[-1],t)


def shoulder_z(y):
    return 1.335-.075*max(0,min(1,(-y-1.40)/1.40))


def side_x(y,z,arch=False):
    h=shoulder_z(y)
    # The broad side is almost vertical, with a small lower tuck. A 3 mm
    # tangent fillet defines the pressed shoulder; there is no broad bulge.
    knots=[(.530,.966),(.590,.968),(.720,.974),(h-.025,.984),
           (h,.993),(h+.012,.979),(1.411,.964),(1.90,.834),(1.98,.818)]
    x=section(z,knots,.003)
    return x


def arch_floor(y,axle,radius=S.ARCH_RADIUS):
    d=abs(y-axle)
    return max(S.ROCKER,S.ARCH_Z+math.sqrt(max(0,radius**2-d*d))) if d<radius else S.ROCKER


def nose_y(x):
    a=abs(x)
    if a<=.850:return -2.840
    d=min(.140,a-.850)
    return -2.700-math.sqrt(max(0,.140**2-d*d))


def hood_z(x,y):
    v=(y-S.HOOD_FRONT)/(S.HOOD_REAR-S.HOOD_FRONT)
    base=1.275+.137*v
    # Raised center, crisp sides, a small crown on each planar stamping.
    rise=section(abs(x),[(0,.026),(.455,.026),(.510,.003),(.550,0),(.99,0)],.006)
    return base+rise


def hood(u,v):
    x=(2*u-1)*.900
    fy=nose_y(x)+.0045;y=fy+(S.HOOD_REAR-fy)*v
    return x,y,hood_z(x,y)


def roof(u,v):
    x=(2*u-1)*.835;a=abs(x)
    # Roof and its rolled shoulders are one surface, flush to the pillar tops.
    z=S.HEIGHT-.020*(x/.750)**2
    if a>.750:
        z-=.029*blend((a-.750)/.085)
    front=-.725+.022*(a/.835)**8
    rear=.980-.025*(a/.835)**8
    y=front+(rear-front)*v
    z-=.004*(2*v-1)**4*(1-(a/.835)**4)
    return x,y,z


def windshield(u,v):
    x=(2*u-1)*(.906*(1-v)+.802*v)
    y=-1.409*(1-v)-.706*v-.025*(1-(2*u-1)**2)
    z=1.433*(1-v)+1.893*v+.006*(1-(2*u-1)**2)
    return x,y,z


def backlight(u,v):
    x=(2*u-1)*(.875-.065*v)
    y=1.019-.064*v+.009*(1-(2*u-1)**2)
    return x,y,1.465+.426*v


def bilinear(corners,u,v):
    a,b,c,d=corners
    return tuple((1-u)*(1-v)*a[k]+u*(1-v)*b[k]+u*v*c[k]+(1-u)*v*d[k] for k in range(len(a)))
