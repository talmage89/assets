"""Fit native car envelopes using transformed vertices, including deck bank."""
import math
import numpy as np
from mathutils import Vector,Quaternion


def vertices(root):
    inverse=root.matrix_world.inverted()
    return np.asarray([tuple(inverse@ob.matrix_world@v.co) for ob in root.children_recursive if ob.type=='MESH' for v in ob.data.vertices])


def lateral(points,space,normal,angle,jitter):
    # A 100mm stripe has a 50mm half-width. Reserve 10mm inside that painted
    # envelope and check the actual transformed body/mirrors, not nominal spec.
    half=space['width']/2+.040
    tilt=Vector((0,0,1)).rotation_difference(normal)
    for _ in range(12):
        q=tilt@Quaternion((0,0,1),math.radians(space['yaw']+angle))
        x=points@np.asarray(q.to_matrix(),dtype=float)[0,:]
        lo=-half-float(x.min());hi=half-float(x.max())
        if lo<=hi:
            return min(hi,max(lo,jitter)),angle
        angle*=.5
    raise ValueError(('Native car cannot fit the actual stalled envelope',space['id'],float(x.min()),float(x.max()),half))
