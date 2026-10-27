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
    # Eight-degree upper face with a continuous 125 mm plan crown. Only the
    # nose and hood/fender leading boundaries use this; side fields stay fixed.
    return -2.849+math.tan(math.radians(8))*(z-.795)+.125*(abs(x)/.984)**2.6


def hood_front_y(x):
    return nose_y(x,1.305)+.0045


def hood_z(x,y):
    # Straight shut line above the fascia. The center pressing blends in aft
    # of that line instead of continuing forward as a raised beak.
    # Preserve the accepted hood field aft of the nose/fender joint. Only the
    # leading strip is reclosed to the deeper front crown.
    a=abs(x);r=.360
    corner=0 if a<=.780 else r-math.sqrt(max(0,r*r-(min(a,.984)-.780)**2))
    fy=-2.849+.10*(1.305-.830)+corner+.008
    t=(y-fy)/(S.HOOD_REAR-fy)
    base=1.3095+(1.369-1.3095)*t+.008*t*(1-t)
    rise=section(abs(x),[(0,.045),(.410,.042),(.520,.007),(.610,0),(.99,-.009)],.008)
    result=base+(rise+.004*(1-(x/.99)**2))*fair((y-fy)/.30)
    if y< -2.499:
        nf=hood_front_y(x);nt=(nf-fy)/(S.HOOD_REAR-fy)
        at_front=1.3095+(1.369-1.3095)*nt+.008*nt*(1-nt)+(rise+.004*(1-(x/.99)**2))*fair((nf-fy)/.30)
        result+=(1.3095-at_front)*(1-fair((y-nf)/max(.035,-2.499-nf)))
    return result


def hood(u,v):
    x=(2*u-1)*.900;fy=hood_front_y(x);y=fy+(S.HOOD_REAR-.035-fy)*v
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
    """Low optical cover continuing around the fender corner, never a box."""
    bottom,top=lamp_limits(u)
    r=.012;d=min(u,1-u)*.420
    cut=0 if d>=r else r-math.sqrt(max(0,r*r-(r-d)**2))
    z=bottom+cut+(top-bottom-2*cut)*v
    x,y=nose_corner(u,z)
    return x,y+.003,z


def lamp_limits(u):
    taper=fair((u-.58)/.42)
    return 1.095+.040*taper,1.249-.032*taper


def nose_corner(u,z,inner=.598,bumper=False):
    """Front crown into a tangent side return; ends at the existing fender."""
    def fy(x):
        if not bumper:return nose_y(x,z)
        depth=section(z,[(.540,.035),(.548,.023),(.565,.004),(.580,0),(.665,.006),(.755,.020),(.784,.023),(.788,.026),(.790,.031)],.002)
        return -S.LENGTH/2+.0004+.125*(abs(x)/.984)**2.6+depth
    if u<=.70:
        x=inner+(.950-inner)*u/.70
        return x,fy(x)
    t=(u-.70)/.30;end=-2.499;side=side_x(end,z)
    ps=[(.950,fy(.950)),(.990,fy(.950)+.015),(side,end-.080),(side,end)]
    return tuple((1-t)**3*ps[0][k]+3*(1-t)**2*t*ps[1][k]+3*(1-t)*t*t*ps[2][k]+t**3*ps[3][k] for k in range(2))


def lamp_point(u,v,depth=0):
    """Offset into the optical well along its actual plan normal."""
    x,y,z=lamp_surface(u,v)
    # Offset around the plan curve at a fixed height. Including the rounded
    # aperture's vertical edge derivative would twist the well's inboard cap.
    a=nose_corner(u-.0001,z);c=nose_corner(u+.0001,z)
    dx=c[0]-a[0];dy=c[1]-a[1];length=math.hypot(dx,dy)
    return x-depth*dy/length,y+depth*dx/length,z
