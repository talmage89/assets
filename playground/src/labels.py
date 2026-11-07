"""Fictional identification print on a curved metal post plate; same metal set."""
import math
from kit import model as G
import geometry as F
from uv_finish import METAL,rect_uv

def build(parent,plan):
    rt=F.root('Meadowworks identification');rt.parent=parent
    x0=-.6096;y0=-.6096;vs=[]
    for j in range(2):
        for i in range(9):
            x=-.052+i*.104/8;y=-math.sqrt(.0645**2-x*x)
            vs.append((x0+x,y0+y,1.04+j*.052))
    ob=F.own(G.mesh('Meadowworks fictional maker plate',vs,[(i,i+1,i+10,i+9) for i in range(8)],F.M['Frame']),rt,(1,1,1,1))
    uv=ob.data.uv_layers.active
    for face in ob.data.polygons:
        for li in face.loop_indices:
            p=ob.data.vertices[ob.data.loops[li].vertex_index].co
            rect_uv(uv.data[li],METAL['Label'],(p.x-x0+.052)/.104,(p.z-1.04)/.052)
    F.finish(rt)
