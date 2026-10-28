"""Original visual trigger blade, in mm; no working fire-control internals.

Muzzle is +Y. The exposed front is concave in side elevation and the toe
returns toward +Y. Width is a photo-class estimate (1/4 inch), not a
manufacturer's manufacturing dimension. Pivot and clip live in build/clips.
"""
import math
from mathutils import Vector
from geometry import M, MAT, HIGH, reg


def blade_mesh(name, subdivisions=1):
    # Concealed bearing neck joins the accepted pivot without moving its pin.
    neck=M.bezier((26.69,23),(33.5,25),(36,20),(34,16),6*subdivisions)
    bow=M.bezier((34,16),(27,7),(26,-1),(33,-5),16*subdivisions)
    path=neck+bow[1:]
    loops=[]
    for i,(y,z) in enumerate(path):
        tangent=(Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)])).normalized()
        normal=Vector((-tangent.y,tangent.x))
        # Flat parallel blade sides; rounded section edges and a shallow
        # transverse crown on the finger face, rather than a circular rod.
        depth=4.4 if i==0 else 3.2
        section=M.rounded_rectangle(6.35,depth,.42,2*subdivisions)
        loops.append([(x,y+(v+.20*(1-(x/3.175)**2)*max(0,v/(depth/2)))*normal.x,
                         z+(v+.20*(1-(x/3.175)**2)*max(0,v/(depth/2)))*normal.y)
                      for x,v in section])
    ob=M.loft(name,loops,MAT['steel'])
    # Ease only the toe's perimeter. A sawn-off rectangular end is conspicuous
    # in the underside macro; the class has a small machined edge radius.
    weight=ob.data.attributes.new('bevel_weight_edge','FLOAT','EDGE')
    start=len(ob.data.vertices)-len(loops[-1])
    for edge in ob.data.edges:
        weight.data[edge.index].value=float(all(i>=start for i in edge.vertices))
    bevel=ob.modifiers.new('Rounded blade toe','BEVEL');bevel.limit_method='WEIGHT'
    bevel.width=.32;bevel.segments=3;bevel.use_clamp_overlap=False
    M.apply(ob)
    return ob


def build():
    low=reg(blade_mesh('Trigger_Shoe'),'Trigger')
    # The blade already resolves its compound face and small toe radius.
    # Retain the same manufactured surface for baking: resampling the tiny
    # weighted toe bevel independently creates spurious projection ripples.
    # Procedural control-finish microdetail is still baked by lookdev.py.
    HIGH[low.name]=low.data.copy()
    return low


def packing_proxy():
    """Retain the accepted atlas pack for all OTHER parts, from scripts.

    This obsolete rod is never shipped or baked. Its old UV islands reserve
    precisely the same atlas footprint while the blade is unwrapped separately.
    """
    path=M.bezier((33,23),(39,14),(38,5),(32,-5),18)
    return reg(M.tube('Trigger packing proxy',[(0,y-6.31,z) for y,z in path],
                      2.2,MAT['steel'],sides=12),'Trigger')
