"""Original shared body surface equations; never sampled from photographs."""
import math
import pickup_spec as S


def smoothstep(t):
    t=max(0,min(1,t));return t*t*(3-2*t)


def side_x(y,z):
    # Inward rocker, broad convex door crown, distinct but rounded shoulder.
    if z<=S.BELT:
        x=.949+.0434*math.sin(math.pi*(z-.530)/(S.BELT-.530))
    else:
        h=z-S.BELT
        x=.949-(.0434*math.pi/(S.BELT-.530))*h-.120*h*h
    # Wheel-arch stamping swells into the shoulder, dies out before the doors.
    for axle in [S.FRONT_AXLE,S.REAR_AXLE]:
        d=math.hypot(y-axle,(z-S.ARCH_Z)*1.03)
        x+=.025*math.exp(-((d-.535)/.125)**2)
    # A soft pressed waist and a lower scallop make a formed panel, not a slab.
    x+=.0035*math.exp(-((z-1.263)/.063)**2)
    x-=.008*math.exp(-((z-.759)/.096)**2)
    # Original gently swept front/rear plan corners.
    x-=.105*smoothstep((-y-2.53)/.29)
    x-=.042*smoothstep((y-2.57)/.25)
    return x


def arch_floor(y,axle):
    d=abs(y-axle)
    return max(S.ROCKER,S.ARCH_Z+math.sqrt(max(0,S.ARCH_RADIUS**2-d*d))) if d<S.ARCH_RADIUS else S.ROCKER


def hood(u,v):
    # Full-width parametric hood; rolled shoulders, shallow original central crown.
    x=(u*2-1)*(.856+.030*smoothstep(v))
    front_y=S.HOOD_FRONT+.2045*(x/.970)**4
    y=front_y+(S.HOOD_REAR-front_y)*v
    transverse=abs(u*2-1)
    z=1.270+.144*smoothstep(v)+.024*(1-transverse**2)
    z+=.019*math.exp(-((transverse-.43)/.13)**2)*math.sin(math.pi*(.08+.84*v))
    z-=.029*smoothstep((transverse-.91)/.09)
    return x,y,z


def roof(u,v):
    x=(u*2-1)*.858;y=-1.045+1.930*v
    z=S.HEIGHT-.035*(2*u-1)**4-.009*(2*v-1)**4
    return x,y,z


def windshield(u,v):
    x=(u*2-1)*(.903*(1-v)+.806*v)
    y=-1.389*(1-v)-1.013*v-.046*(1-(2*u-1)**2)*math.sin(math.pi*v)
    z=1.430*(1-v)+1.902*v+.014*(1-(2*u-1)**2)
    return x,y,z


def backlight(u,v):
    x=(2*u-1)*(.878-.069*v)
    y=.972-.100*v+.019*(1-(2*u-1)**2)
    z=1.470+.427*v
    return x,y,z


def bilinear(corners,u,v):
    a,b,c,d=corners
    return tuple((1-u)*(1-v)*a[k]+u*(1-v)*b[k]+u*v*c[k]+(1-u)*v*d[k] for k in range(len(a)))
