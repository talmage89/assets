"""One regular Catmull–Clark limit cage for the action's upper forging.

All dimensions below are original, measured visual-asset constraints in mm.
The cage has no fence patches, return masks or unions. Its regular interior
is the tensor-product cubic B-spline limit of quad subdivision. Extended
support rows keep the evaluated region clear of boundary rules; repeated
outer X controls turn the roof vertically into the ground side planes.
"""
from functools import lru_cache
import math
import numpy as np

# More support loops are needed at the circular front and R6 side than in
# the broad rear face. These coordinates are controls, not mesh samples.
_half = [0, 2.5, 4.5, 6.5, 8.5, 10.5, 12.6, 14.5, 16.5, 18.5,
         20.5, 22.5, 24, 25.1, 25.7, 25.95, 25.95, 25.95]
X = np.array([-v for v in _half[:0:-1]] + _half)
Y = np.array([60, 65, 70, 77, 83, 88, 92, 95, 98, 101, 104, 107,
              109, 111, 113, 115, 117, 119], dtype=float)

def basis(u, n):
    i = min(n-3, max(1, int(math.floor(u)))); t = u-i
    b = np.zeros(n)
    b[i-1:i+3] = [(1-t)**3/6, (3*t**3-6*t*t+4)/6,
                  (-3*t**3+3*t*t+3*t+1)/6, t**3/6]
    return b

@lru_cache(maxsize=200000)
def coordinate_basis(value, axis):
    controls = X if axis == 0 else Y; lo = 1.; hi = float(len(controls)-2)
    for _ in range(38):
        mid = (lo+hi)*.5
        if basis(mid, len(controls)) @ controls < value: lo = mid
        else: hi = mid
    return basis((lo+hi)*.5, len(controls))

def _pchip(x, xp, yp):
    """Monotone station interpolation, used only to place the initial cage."""
    xp = np.asarray(xp); yp = np.asarray(yp); h = np.diff(xp); d = np.diff(yp)/h
    m = np.zeros(len(xp)); m[0] = d[0]; m[-1] = d[-1]
    for i in range(1, len(xp)-1):
        if d[i-1]*d[i] > 0:
            w1 = 2*h[i]+h[i-1]; w2 = h[i]+2*h[i-1]
            m[i] = (w1+w2)/(w1/d[i-1]+w2/d[i])
    i = min(len(h)-1, max(0, int(np.searchsorted(xp, x)-1))); t = (x-xp[i])/h[i]
    return ((2*t**3-3*t*t+1)*yp[i]+(t**3-2*t*t+t)*h[i]*m[i]
            +(-2*t**3+3*t*t)*yp[i+1]+(t**3-t*t)*h[i]*m[i+1])

_SX = np.array([0, 4, 8, 10, 12.6, 16, 19.95, 23, 25.95])
_SY = np.array([65, 70, 80, 85, 88, 91, 94, 95.5, 98, 101, 104, 107])
# Height above the R6 side drop, before recess subtraction. The center is
# filled broadly into the fences instead of a narrow raised strip with two
# thresholded returns. The outside stays level until the shorter outer roll.
_STATIONS = np.array([
 [43.72]*9, [44.32]*9, [45.52]*9, [46.12]*9,
 [48.6,48.5,48.3,48.2,48.0,47.9,47.8,47.8,47.8],
 [51.8,51.7,51.1,50.2,49.3,49.1,49.1,49.1,49.1],
 [54.8,54.4,52.5,51.0,49.65,49.72,49.72,49.72,49.72],
 [55.3,54.9,53.4,51.9,49.75,49.72,49.72,49.72,49.72],
 [55.59,55.3,54.1,52.8,51.0,50.0,49.72,49.72,49.72],
 [55.59,55.5,54.9,54.1,53.0,51.5,49.9,49.72,49.72],
 [55.59,55.59,55.4,55.3,55.0,53.5,51.0,49.85,49.72],
 [55.59,55.67,55.88,56.0,56.037,55.65,54.0,50.96,49.72],
])

def _design(x, y):
    x = abs(x)
    r6 = 6*(1-math.sqrt(max(0, 1-(max(0, x-19.95)/6)**2)))
    if y < 107:
        heights = [_pchip(y, _SY, _STATIONS[:, i]) for i in range(len(_SX))]
        return _pchip(x, _SX, heights)-r6
    d = 115-y; r = 13.35*math.sqrt(max(0, 1-(d/18.5)**2)); bx = 12.6+1.7*d/660.4
    # The front's outer arc is fixed by the accepted bore relation. Inside
    # the crowns the single cage fills the space, without two separate domes.
    if x < bx:
        t = x/bx
        return 55.59+(44+r-55.59)*(2*t*t-t**4)
    dx = x-bx
    arc = 44+math.sqrt(max(0, r*r-dx*dx))
    # Only initialization near the outer upright tangent; the final form is
    # the one solved control net, with no min/max blend in its evaluation.
    return max(49.72-r6, arc if dx < r else 0)

_Z = None
def control_heights():
    global _Z
    if _Z is not None: return _Z
    rows = []; values = []
    def add(x, y, z, weight=1):
        rows.append(np.outer(coordinate_basis(y, 1), coordinate_basis(x, 0)).ravel()*weight)
        values.append(z*weight)
    # Original station table places the broad surface; it is deliberately
    # approximate. Exact constraints below take precedence over these.
    for y in np.arange(66, 117.01, 1.5):
        for x in np.linspace(-25.95, 25.95, 63): add(float(x), float(y), _design(x,y), .025)
    # Outward front arcs, their actual axes, and the level central fill.
    for y in np.arange(107.5, 115.01, .5):
        d = 115-y; r = 13.35*math.sqrt(1-(d/18.5)**2); bx = 12.6+1.7*d/660.4
        for side in (-1,1):
            for angle in np.arange(35, 100.1, 5):
                a = math.radians(angle); add(side*(bx+r*math.cos(a)), float(y), 44+r*math.sin(a), 500)
    for y in np.arange(100.5, 116.01, .5):
        for x in (-1., 0., 1.): add(x, float(y), 55.59, 1000)
    # R6 side-return section and the three accepted photographic drops.
    for x in np.linspace(19.95,25.95,31):
        z = 49.72-6+math.sqrt(max(0,36-(x-19.95)**2))
        for side in (-1,1): add(side*float(x),95.2,z,200)
    for side in (-1,1): add(side*12.6,95.5,49.72,200)
    # Accepted longitudinal profile stations constrain the broad return;
    # no zero-height thresholds or separately fitted transverse returns.
    for side in (-1,1):
        for y,z in [(96.5,49.72),(98,49.83),(100,50.73),(102,52.46),(104,54.33),(107,56.037)]:
            add(side*12.6,y,z,200)
        for y in (91,91.5,92,92.5,93,93.5,94):
            add(side*10,y,49.72-6.5+math.sqrt(6.5**2-(94-y)**2),800)
        for y in (96,98,100,102):
            for x in (20.5,22,23,24,25,25.7,25.95):
                add(side*x,y,49.72-6+math.sqrt(max(0,36-(x-19.95)**2)),2)
        for y in (96,98,100,102,103):
            add(side*23,y,49.72-6+math.sqrt(36-(23-19.95)**2),100)
    add(0,85.2,46.4,20)
    # The subdivision cage's discrete third differences penalize extra
    # inflections. Unlike return-by-return fitting this solves all rows and
    # both transverse halves together, sharing every interior control.
    ny, nx = len(Y), len(X)
    for j in range(ny):
        for i in range(nx-3):
            row = np.zeros((ny,nx)); row[j,i:i+4] = [-1,3,-3,1]
            rows.append(row.ravel()*2); values.append(0)
    for i in range(nx):
        for j in range(ny-3):
            row = np.zeros((ny,nx)); row[j:j+4,i] = [-1,3,-3,1]
            rows.append(row.ravel()*2); values.append(0)
    # Curvature variation is measured in physical millimeters too. The
    # support loops have unequal spacing; parameter-space differences alone
    # otherwise leave broad but visible changes in the reflected band width.
    def derivatives(value,axis):
        e=.15; f=lambda d:coordinate_basis(float(value+d),axis)
        return ((f(e)-f(-e))/(2*e),(f(e)-2*f(0)+f(-e))/e**2,
                (f(2*e)-2*f(e)+2*f(-e)-f(-2*e))/(2*e**3))
    for y in np.arange(87,114.5,1.3):
        by=coordinate_basis(float(y),1);dy,dyy,dyyy=derivatives(y,1)
        for x in np.arange(.5,20,1.3):
            bx=coordinate_basis(float(x),0);dx,dxx,dxxx=derivatives(x,0)
            for row in (np.outer(by,dxxx),np.outer(dy,dxx)*math.sqrt(3),
                        np.outer(dyy,dx)*math.sqrt(3),np.outer(dyyy,bx)):
                rows.append(row.ravel()*25);values.append(0)
    # Solve only the symmetric half of the net. Linear monotonicity
    # constraints remove unintended secondary humps/dents rather than merely
    # making their derivatives continuous. The central transverse gradient
    # reverses once as the crowns rise above the 55.59 center datum.
    def symmetric_rows(a):
        a=a.reshape(-1,ny,nx); mid=nx//2
        return (a[:,:,mid:]+np.pad(a[:,:,:mid][:,:,::-1],((0,0),(0,0),(1,0)))).reshape(len(a),-1)
    a=symmetric_rows(np.array(rows)); b=np.array(values); constraints=[]
    def gradient(x,y,axis,sign=1):
        e=.04
        if axis==0:
            row=np.outer(coordinate_basis(y,1),(coordinate_basis(x+e,0)-coordinate_basis(x-e,0))/(2*e))
        else:
            row=np.outer((coordinate_basis(y+e,1)-coordinate_basis(y-e,1))/(2*e),coordinate_basis(x,0))
        constraints.append(row.ravel()*sign)
    for y in np.arange(86,115,.6):
        for x in np.arange(.5,25.6,1): gradient(float(x),float(y),1)
    for y in np.arange(88,115.01,.8):
        for x in np.arange(.5,25.6,.65):
            if x>=12.7 or y<=105.8: gradient(float(x),float(y),0,-1)
            elif y>=107: gradient(float(x),float(y),0,1)
    g=symmetric_rows(np.array(constraints))
    # ADMM for this small convex least-squares problem. Nonnegative physical
    # derivatives are the only inequalities; measured heights/radii remain
    # the same observations used above. No image is an input to this solve.
    rho=20000.; h=a.T@a+rho*(g.T@g)+np.eye(a.shape[1])*1e-8
    inverse=np.linalg.inv(h); rhs=a.T@b
    c=np.linalg.lstsq(a,b,rcond=1e-10)[0]; z=np.maximum(g@c,0); u=np.zeros_like(z)
    for iteration in range(350):
        c=inverse@(rhs+rho*(g.T@(z-u)))
        q=g@c; previous=z; z=np.maximum(q+u,0); u+=q-z
        if iteration>50 and np.max(abs(q-z))<.00002 and np.max(abs(z-previous))<.00002: break
    right=c.reshape(ny,nx//2+1)
    _Z=np.c_[right[:,1:][:,::-1],right]
    return _Z

@lru_cache(maxsize=200000)
def height(x, y):
    return float(coordinate_basis(y,1) @ control_heights() @ coordinate_basis(x,0))

def cage():
    z = control_heights(); nx = len(X); ny = len(Y)
    vertices = [(float(x),float(y),float(z[j,i])) for j,y in enumerate(Y) for i,x in enumerate(X)]
    faces = [(j*nx+i,j*nx+i+1,(j+1)*nx+i+1,(j+1)*nx+i) for j in range(ny-1) for i in range(nx-1)]
    return vertices, faces
