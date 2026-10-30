"""Machined exterior primitives joined by compact signed-distance blends.

Millimeters, visual game geometry only. A turned concave meridian on each
bore axis supplies the fence; the ground sides and rear roof are planes.
An inclined circular cylinder carries the central rib-floor land. No fitted
control net, photographic contour, or independent height controls occur here.
The zero set is resampled by head_mesh into the integral forging skin.
"""
import math
from functools import lru_cache
import numpy as np

FENCE_RADIUS = 13.35
SIDE_RADIUS = 6.0
BODY_TOP = 49.72
CENTER_TOP = 55.59
BLEND_RADIUS = 1.0


def smooth_min(a, b, radius):
    """C2 compact polynomial union of signed distance fields (negative inside).

    The support width is a single physical distance. Outside it the original
    primitive is exact; no local patches or freely placed height samples.
    """
    h = np.maximum(radius-np.abs(a-b), 0)/radius
    return np.minimum(a,b)-h*h*h*radius/6


def turned_radius(d):
    # One concave turned profile: its curvature decreases continuously from
    # the accepted front crown into a conical fall. It never flattens again
    # behind the crown, which would create the rejected rear cushion.
    b=12.8;k=.5
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


def field(x,y,z):
    """One union of turned fences, milled roof, and inclined circular central land."""
    # R6 rolling-ball return between the constant-X ground sides and the
    # Z49.72 roof plane. The changing rear fall is one inclined plane.
    u=np.abs(x)-19.95;v=z-(BODY_TOP-SIDE_RADIUS)
    base=np.hypot(np.maximum(u,0),np.maximum(v,0))+np.minimum(np.maximum(u,v),0)-SIDE_RADIUS
    rear=(z-(46.4+.65*(y-85.2)))/math.sqrt(1+.65**2)
    base=-smooth_min(-base,-rear,2.0)
    # A cylindrical filed land, tangent to the rib floor at the front.
    # Its axis falls 0.32 mm per rearward mm. Holding the original rear
    # land at the front datum creates a raised ridge between lower fences.
    # R16.46 meets the lower roof beside the accepted bore-axis stations.
    radius=16.46
    land=np.hypot(x,(z-(CENTER_TOP+.32*(y-115)))/math.sqrt(1+.32**2)+radius)-radius
    land_rear=(z-(46.4+.85*(y-85.2)))/math.sqrt(1+.85**2)
    land=-smooth_min(-land,-land_rear,3.0)
    result=smooth_min(base,land,BLEND_RADIUS)
    for sign in (-1,1):
        # Continue the barrels' measured convergent axes behind the face.
        axis=sign*(12.6+1.7*(115-y)/660.4)
        distance=turned_distance(115-y,np.hypot(x-axis,z-44))
        result=smooth_min(result,distance,BLEND_RADIUS)
    # The milling envelope retains the accepted overall width. The turned
    # front arcs are already within it; this clips only buried union excess.
    return np.maximum(result,np.abs(x)-25.95)


_GRID=None

def _grid():
    """Dense, deterministic resampling of the analytic zero set, not a cage.

    Cubic interpolation only evaluates the same SDF more cheaply for the
    lip and differential normals. Grid spacing is 0.05 mm, below the source
    tessellation; no smoothing or fit is applied to its heights.
    """
    global _GRID
    if _GRID is None:
        import time
        started=time.monotonic();print("Resampling analytic head field",flush=True)
        xs=np.arange(-26.05,26.051,.05);ys=np.arange(59.9,115.151,.05)
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
    data=_grid();xx=(x+26.05)/.05;yy=(y-59.9)/.05
    i=math.floor(xx);j=math.floor(yy);wx=_weights(xx-i);wy=_weights(yy-j)
    return float(sum(wy[b]*sum(wx[a]*data[min(data.shape[0]-1,max(0,j+b-1)),min(data.shape[1]-1,max(0,i+a-1))] for a in range(4)) for b in range(4)))


def construction():
    return dict(method='zero set of compact C2 signed-distance union; remeshed in XY',
        fences='turned concave meridian about continued bore axes',
        fence_radius_mm=FENCE_RADIUS,profile_asymptotic_slope=.5,profile_scale_mm=12.8,
        side_return_mm=SIDE_RADIUS,central_land_radius_mm=16.46,central_land_rearward_slope=.32,
        union_support_mm=BLEND_RADIUS,resampling_step_mm=.05,
        free_height_controls=0)
