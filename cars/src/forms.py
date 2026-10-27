"""Original section surfaces in meters; photos never enter the evaluator.

Fair Hermite sections carry the crown. Arch opening, broad die draw and lip
all sample one side field; there is no attached annular flare patch. The cab
header is the tangent continuation of the windscreen into a rolled roof skin.
"""
import math
import pickup_spec as S


def blend(t):
    t=max(0,min(1,t));return t*t*(3-2*t)


def fair(t):
    t=max(0,min(1,t));return t*t*t*(10+t*(-15+6*t))


def hermite(x,stations):
    """Value and slope controls, with tangent extrapolation at the two ends."""
    if x<=stations[0][0]:
        a,v,m=stations[0];return v+(x-a)*m
    if x>=stations[-1][0]:
        a,v,m=stations[-1];return v+(x-a)*m
    for (a,p,m),(b,q,n) in zip(stations,stations[1:]):
        if x<=b:
            t=(x-a)/(b-a)
            return (2*t**3-3*t*t+1)*p+(t**3-2*t*t+t)*(b-a)*m+(-2*t**3+3*t*t)*q+(t**3-t*t)*(b-a)*n


def section(t,knots,radius=.003):
    slopes=[(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(knots,knots[1:])]
    for i in range(1,len(knots)-1):
        a,b,c=knots[i-1:i+2];r=min(radius,(b[0]-a[0])*.35,(c[0]-b[0])*.35)
        if b[0]-r<t<b[0]+r:
            return hermite(t,[(b[0]-r,b[1]-slopes[i-1]*r,slopes[i-1]),(b[0]+r,b[1]+slopes[i]*r,slopes[i])])
    for i,(a,b) in enumerate(zip(knots,knots[1:])):
        if t<=b[0]:return a[1]+slopes[i]*(t-a[0])
    return knots[-1][1]+slopes[-1]*(t-knots[-1][0])


def belt_z(y):return S.BELT-.036*fair((-y-.90)/.50)
def shoulder_z(y):return 1.332+.132*min(0,y+1.405)


def side_base(y,z):
    h=shoulder_z(y)
    if z>S.BELT:
        return .963-.26*(z-S.BELT)-.018*fair((y-.48)/.48)
    return hermite(z,[(.530,.935,.17),(.578,.943,.17),(.650,.956,.16),
        (.720,.967,.13),(.780,.973,.065),(.840,.977,.035),
        (1.000,.9815,0),(h-.065,.974,-.040),
        (h-.012,.985,.32),(h,.987,0),(h+.016,.979,-.30),
        (S.BELT,.963,-.26)])


ARCH_HALF=.505
ARCH_POWER=2.65
FLARE_DEPTH=.03580


def arch_floor(y,axle,radius=S.ARCH_RADIUS):
    t=abs((y-axle)/ARCH_HALF)
    z=S.ARCH_Z+radius*max(0,1-t**ARCH_POWER)**(1/ARCH_POWER)
    return max(S.ROCKER+.013,z)


def arch_point(t,axle):
    power=2/ARCH_POWER
    a0=math.asin(((S.ROCKER+.013-S.ARCH_Z)/S.ARCH_RADIUS)**(1/power))
    a=a0+(math.pi-2*a0)*t;c=math.cos(a)
    return axle+ARCH_HALF*math.copysign(abs(c)**power,c),S.ARCH_Z+S.ARCH_RADIUS*math.sin(a)**power


def side_x(y,z,arch=True):
    x=side_base(y,z)
    if arch:
        for axle in (S.FRONT_AXLE,S.REAR_AXLE):
            q=(abs((y-axle)/ARCH_HALF)**ARCH_POWER+abs((z-S.ARCH_Z)/S.ARCH_RADIUS)**ARCH_POWER)**(1/ARCH_POWER)
            # A 12 mm lip and broad, nearly ruled draw with tangent fillets
            # at the authored crease. No collapsed end of an annulus.
            t=min(1,max(-.05,(q-1)/.46))
            x+=FLARE_DEPTH*(1-t)**2
    return x


def nose_y(x,z=1.20):
    a=abs(x);r=.225
    corner=0 if a<=.760 else r-math.sqrt(max(0,r*r-(min(a,.984)-.760)**2))
    return -2.849+.10*(z-.830)+corner


def hood_z(x,y):
    t=(y-S.HOOD_FRONT)/(S.HOOD_REAR-S.HOOD_FRONT)
    base=1.181+.188*t+.008*t*(1-t)+.035*(1-fair((y-S.HOOD_FRONT)/.42))
    # Two broad raised planes with a crisp 6 mm die radius at the draw edges.
    rise=section(abs(x),[(0,.045),(.410,.042),(.520,.007),(.610,0),(.99,-.009)],.008)
    return base+rise+.004*(1-(x/.99)**2)


def hood(u,v):
    x=(2*u-1)*.900;fy=nose_y(x,hood_z(x,S.HOOD_FRONT))+.0045
    y=fy+(S.HOOD_REAR-fy)*v
    return x,y,hood_z(x,y)


def roof_center(y):
    return hermite(y,[(-.810,1.887,.76),(-.60,1.945,.045),(.03,S.HEIGHT,0),
                      (.62,1.926,-.09),(.82,1.909,-.12),(.970,1.873,-.38)])


def roof_roll_radius(y):return .090-.035*fair((y-.30)/.60)


def roof_width(y):
    drop=.012+roof_roll_radius(y)*.738
    return .963-.26*(roof_center(y)-drop-S.BELT)-.018*fair((y-.48)/.48)


def roof_height(x,y):
    w=roof_width(y);r=roof_roll_radius(y);start=w-r*.933333;theta0=math.atan(.024/start)
    a=abs(x)
    if a<=start:drop=.012*(a/start)**2
    else:
        sine=(a-start)/r+math.sin(theta0)
        # Tangent extrapolation only outside the authored patch for normal
        # finite differences. Within the skin the circle stays nonsingular.
        sine=max(-.9999,min(.9999,sine))
        drop=.012+r*(math.cos(theta0)-math.sqrt(1-sine*sine))
    return roof_center(y)-drop


def roof(u,v):
    s=2*u-1;front=-.810+.090*s**8;rear=.970-.070*s**8
    y=front+(rear-front)*v;x=s*roof_width(y)
    return x,y,roof_height(x,y)


def windshield(u,v):
    s=2*u-1;xt,yt,zt=roof((1+.935*s)/2,0)
    xb=s*.908;yb=-1.409-.018*(1-s*s);zb=1.399+.006*(1-s*s)
    # Shared boundary and near-tangent continuation into the header roll.
    return xb+(xt-xb)*v,yb+(yt-yb)*v,zb+(zt-zb)*v-.002


def backlight(u,v):
    s=2*u-1;x=s*(.872-.080*v)
    y=(1.024+.009*(1-s*s))*(1-v)+(.989-.065*s**8)*v
    z=1.457+.386*v+.005*(1-s*s)
    return x,y,z


def bilinear(corners,u,v):
    a,b,c,d=corners
    return tuple((1-u)*(1-v)*a[k]+u*(1-v)*b[k]+u*v*c[k]+(1-u)*v*d[k] for k in range(len(a)))


def lamp_surface(u,v):
    """Flush front-to-side lens seat, with the rear tangent on the fender."""
    z=.929+.274*v
    if u<=.70:
        x=.685+.257*u/.70;y=nose_y(x,z)+.004
    else:
        t=(u-.70)/.30;x0=.942;y0=nose_y(x0,z)+.004
        ye=-2.499;xe=side_x(ye,z)-.002
        e=1e-4;dxdy=(side_x(ye+e,z)-side_x(ye-e,z))/(2*e)
        dydx=(nose_y(x0+e,z)-nose_y(x0-e,z))/(2*e)
        p=(x0,y0);a=(x0+.030,y0+.030*dydx);c=(xe-.080*dxdy,ye-.080);d=(xe,ye)
        x,y=[(1-t)**3*p[k]+3*(1-t)**2*t*a[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in range(2)]
    return x,y,z
