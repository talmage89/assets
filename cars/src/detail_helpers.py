"""Small authored assembly helpers, all coordinates in the vehicle rest frame."""
import math
import bpy
from mathutils import Vector
from kit import model as G


def pivot(b,name,position,parent=None,axis='Z',limits=(0,90)):
    ob=G.pivot(name,position,axis,limits);bpy.context.view_layer.update();world=ob.matrix_world.copy()
    ob.parent=parent or b.root;ob.matrix_world=world
    return ob


def box(b,name,center,size,material,category='trim',parent=None,radius=.003):
    return b.add(G.box(name,center,size,material,radius,3 if b.high else 1),parent,category)


def tube(b,name,points,radius,material,category='trim',parent=None,sides=8):
    return b.add(G.tube(name,points,radius,material,sides if not b.high else max(sides,12)),parent,category)


def loop(b,name,center,a,baxis,radii,section,material,category='trim',parent=None,segments=24,sides=6):
    a=Vector(a).normalized();baxis=Vector(baxis).normalized();normal=a.cross(baxis).normalized();c=Vector(center)
    loops=[]
    for i in range(segments):
        t=math.tau*i/segments;radial=(a*math.cos(t)+baxis*math.sin(t)).normalized()
        p=c+a*(radii[0]*math.cos(t))+baxis*(radii[1]*math.sin(t))
        loops.append([p+section*(radial*math.cos(k*math.tau/sides)+normal*math.sin(k*math.tau/sides)) for k in range(sides)])
    return b.add(G.smooth(G.ring_loft(name,loops,material)),parent,category)


def print_quad(b,name,corners,material,category='trim',parent=None):
    ob=G.plane_uv(name,corners,material)
    return b.add(ob,parent,category)
