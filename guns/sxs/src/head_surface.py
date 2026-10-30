"""Machined exterior primitives joined by compact signed-distance blends.

Millimeters, visual game geometry only. A turned concave meridian on each
bore axis supplies the fence; the ground sides and rear roof are planes.
An inclined milled land carries the central rib-floor datum. No fitted
control net, photographic contour, or independent height controls occur here.
The zero set is resampled by head_mesh into the integral forging skin.
"""
import math
from functools import lru_cache
import numpy as np

FENCE_RADIUS = 13.35
SIDE_RADIUS = 6.0
BODY_TOP = 49.72
ROOF_SLOPE = .10
CENTER_TOP = 55.59
CENTER_BLEND = 1.5
OUTER_BLEND = 1.0
GRID_U_SAMPLES = 1281
SIDE_INTERSECTION_BLEND = .6


def smooth_min(a, b, radius):
    """C2 compact polynomial union of signed distance fields (negative inside).

    The support width is a single physical distance. Outside it the original
    primitive is exact; no local patches or freely placed height samples.
    """
    h = np.maximum(radius-np.abs(a-b), 0)/np.maximum(radius,1e-12)
    return np.minimum(a,b)-h*h*h*radius/6


def turned_radius(d):
    # One concave turned profile: its curvature decreases continuously from
    # the accepted front crown into a conical fall. It never flattens again
    # behind the crown, which would create the rejected rear cushion.
    b=2.0;k=.3
    root=np.sqrt(d*d+b*b)
    return FENCE_RADIUS-k*(root-b),-k*d/root,-k*b*b/root**3


def turned_distance(axial, radial):
    """Euclidean signed distance to a meridian of the turned exterior."""
    u=np.abs(axial);q=np.maximum(radial,1e-8);t=np.minimum(u,34.)
    for _ in range(10):
        r,dr,ddr=turned_radius(t)
        f=t-u+(r-q)*dr
        derivative=1+dr*dr+(r-q)*ddr
        t=np.clip(t-f/np.maximum(derivative,.1),0,35.)
    r,_,_=turned_radius(t)
    distance=np.hypot(t-u,r-q)
    surface,_,_=turned_radius(u)
    return distance*np.where(q>=surface,1.,-1.)


def raw_field(x,y,z):
    """One union of turned fences, milled roof, and inclined milled central land."""
    # R6 rolling-ball return between the constant-X ground sides and the
    # Z49.72 roof plane. The changing rear fall is one inclined plane.
    u=np.abs(x)-19.95
    v=(z-(BODY_TOP+ROOF_SLOPE*(y-115)))/math.sqrt(1+ROOF_SLOPE**2)+SIDE_RADIUS
    base=np.hypot(np.maximum(u,0),np.maximum(v,0))+np.minimum(np.maximum(u,v),0)-SIDE_RADIUS
    rear=(z-(46.4+.65*(y-85.2)))/math.sqrt(1+.65**2)
    base=-smooth_min(-base,-rear,2.0)
    # A milled central land, tangent to the rib floor at the front.
    # Its axis falls 0.32 mm per rearward mm. Holding the original rear
    # land at the front datum creates a raised ridge between lower fences.
    # A six-millimeter half-width flat and R2 shoulders stay buried in the
    # turned fences. A circular central cap would add two false troughs.
    u=np.abs(x)-6.0
    v=(z-(CENTER_TOP+.32*(y-115)))/math.sqrt(1+.32**2)+2.0
    land=np.hypot(np.maximum(u,0),np.maximum(v,0))+np.minimum(np.maximum(u,v),0)-2.0
    land_rear=(z-(46.4+.85*(y-85.2)))/math.sqrt(1+.85**2)
    land=-smooth_min(-land,-land_rear,3.0)
    result=land
    center_width=CENTER_BLEND
    for sign in (-1,1):
        # Continue the barrels' measured convergent axes behind the face.
        slope=sign*1.7/660.4;scale=math.sqrt(1+slope*slope)
        dx=x-sign*12.6;dy=y-115
        axial=(slope*dx-dy)/scale
        transverse=(dx+slope*dy)/scale
        distance=turned_distance(axial,np.hypot(transverse,z-44))
        result=smooth_min(result,distance,center_width)
    # The milling envelope retains the accepted overall width. The turned
    # front arcs are already within it; this clips only buried union excess.
    result=smooth_min(base,result,OUTER_BLEND)
    return result


def field(x,y,z):
    """Blend into the ground plane without rounding coincident side fields.

    An ordinary round maximum shrinks even two identical planes, leaving
    no zero set on the envelope. Its support must vanish as the two normals
    become parallel. The one 0.6 mm edge-blend scale is multiplied by their
    angular departure, continuously along the return.
    """
    x,y,z=np.broadcast_arrays(np.asarray(x),np.asarray(y),np.asarray(z))
    value=raw_field(x,y,z);side=np.abs(x)-25.95
    result=np.array(np.maximum(value,side),copy=True)
    # At these interior points the side is farther than the entire blend
    # support, so it cannot alter the zero set. Evaluate derivatives only
    # in the narrow envelope neighborhood; this is exact support culling.
    active=np.abs(x)>25.2
    if np.any(active):
        xx,yy,zz=x[active],y[active],z[active];v=value[active];e=.001
        gx=(raw_field(xx+e,yy,zz)-v)/e
        gz=(raw_field(xx,yy,zz+e)-v)/e
        cosine=np.clip(np.abs(gx)/np.maximum(np.hypot(gx,gz),1e-12),0,1)
        width=SIDE_INTERSECTION_BLEND*(1-cosine)
        result[active]=-smooth_min(-v,-side[active],width)
    return result


_GRID=None

def _grid():
    """Dense, deterministic resampling of the analytic zero set, not a cage.

    Cubic interpolation only evaluates the same SDF more cheaply for the
    lip and differential normals. Y spacing is 0.05 mm. X is uniform in transverse angle, so its samples
    resolve the vertical ground-side tangent instead of flattening it at a
    uniform-X interpolation boundary. No height smoothing or fit is applied.
    """
    global _GRID
    if _GRID is None:
        import time
        started=time.monotonic();print("Resampling analytic head field",flush=True)
        xs=25.95*np.sin(np.linspace(-math.pi/2,math.pi/2,GRID_U_SAMPLES));ys=np.arange(59.9,115.151,.05)
        x,y=np.meshgrid(xs,ys);lo=np.full(x.shape,25.);hi=np.full(x.shape,60.)
        # The side plane itself is vertical; evaluate its limiting roof from
        # 10 nm inside the envelope rather than bisecting an entire zero ray.
        x=np.clip(x,-25.95+1e-8,25.95-1e-8)
        for _ in range(28):
            z=(lo+hi)*.5;outside=field(x,y,z)>0
            hi=np.where(outside,z,hi);lo=np.where(outside,lo,z)
        _GRID=(lo+hi)*.5
        print("Head field sampled in",round(time.monotonic()-started,1),"seconds",flush=True)
    return _GRID


def _weights(t):
    return (-.5*t+t*t-.5*t**3,1-2.5*t*t+1.5*t**3,
            .5*t+2*t*t-1.5*t**3,-.5*t*t+.5*t**3)


@lru_cache(maxsize=400000)
def height(x,y):
    data=_grid();xx=(math.asin(max(-1,min(1,x/25.95)))+math.pi/2)*(GRID_U_SAMPLES-1)/math.pi;yy=(y-59.9)/.05
    i=math.floor(xx);j=math.floor(yy);wx=_weights(xx-i);wy=_weights(yy-j)
    return float(sum(wy[b]*sum(wx[a]*data[min(data.shape[0]-1,max(0,j+b-1)),min(data.shape[1]-1,max(0,i+a-1))] for a in range(4)) for b in range(4)))


def construction():
    return dict(method='zero set of compact C2 signed-distance union; remeshed in XY',
        fences='turned concave meridian about continued bore axes',
        fence_radius_mm=FENCE_RADIUS,profile_asymptotic_slope=.3,profile_scale_mm=2.0,
        side_return_mm=SIDE_RADIUS,rear_roof_slope=ROOF_SLOPE,central_land_flat_half_width_mm=6.0,central_land_edge_radius_mm=2.0,central_land_rearward_slope=.32,
        central_union_support_mm=CENTER_BLEND,outer_union_support_mm=OUTER_BLEND,
        side_intersection_support_mm=SIDE_INTERSECTION_BLEND,resampling_y_step_mm=.05,
        transverse_angle_samples=GRID_U_SAMPLES,maximum_x_step_mm=25.95*math.sin(math.pi/(GRID_U_SAMPLES-1)),
        free_height_controls=0)
