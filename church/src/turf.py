"""Accepted garden July turf, clipped blades, traffic and mulched beds.

Read the garden's original albedo recipe and Ground relief. No other package
is modified. Whole-lot color fields ship as COLOR_0, not render-only nodes.
"""
import importlib.util,math,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('_church_garden_turf',ROOT/'community-garden/src/groundcover.py')
garden=importlib.util.module_from_spec(spec);spec.loader.exec_module(garden)
MODERN=False


def maps(out):garden.maps(ROOT,out)


def segment(x,y,a,b):
    dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)


def tint(x,y):
    base=garden.summer_tint(x,y,.15 if y< -18 else 0)
    # Congregants cut the corner between the sidewalk and entry approach.
    a,b=((-12,-39),(0,-22)) if MODERN else ((-13,-23),(-2.2,-17))
    traffic=math.exp(-(segment(x,y,a,b)/(.31+.05*math.sin(x*2)))**4)
    dry=.14+.18*math.sin(x*.19+y*.13)**2
    shade=.16*math.exp(-((x-21)**2+(y+21)**2)/22)
    return (base[0]*(.90+.20*traffic),base[1]*(.91-.49*traffic-dry*.18-shade),base[2]*(.90-.33*traffic-dry*.14-shade))


def beds(p):
    if p['style']=='aframe':return [(35.1,37.5,-8.8,15.1),(10.3,27.4,28.6,30.2),(-8.9,-7.8,-13,13)]
    return [(16.6,18.2,3.0,16.3),(-6.1,-2.3,-14.4,-13.1),(2.3,6.1,-14.4,-13.1)]


def details(p,parent,cuts,bounds):
    import geometry as G
    rng=random.Random(p['seed']+2947)
    m=G.Mesh('Mulched foundation planting beds',parent,actor_kind='site')
    for a,b,c,d in beds(p):
        # Ground's brown substrate under shrubs retains fine original grain.
        m.box(((a+b)/2,(c+d)/2,-.012),(b-a,d-c,.055),'timber',(.12,.13,.105))
    m.finish()
    a,b,c,d=bounds;blade=G.Mesh('Clipped summer sward edges',parent,actor_kind='vegetation',sheet=True)
    edges=[r for r in cuts if (r[1]-r[0])*(r[3]-r[2])<450]
    for j in range(3400):
        if j<2200:
            r=rng.choice(edges);side=rng.randrange(4);t=rng.random();off=rng.uniform(.018,.20)
            if side<2:x=r[side]+(-off if side==0 else off);y=r[2]+(r[3]-r[2])*t
            else:x=r[0]+(r[1]-r[0])*t;y=r[side]+(-off if side==2 else off)
        else:x=rng.uniform(a,b);y=rng.uniform(c,min(d,c+12))
        if not a<x<b or not c<y<d:continue
        if any(q[0]-.004<x<q[1]+.004 and q[2]-.004<y<q[3]+.004 for q in cuts):continue
        height=rng.uniform(.022,.052);width=rng.uniform(.003,.007);ang=rng.random()*math.tau
        dx=math.cos(ang)*width;dy=math.sin(ang)*width
        blade.geom([(x-dx,y-dy,-.009),(x+dx,y+dy,-.009),(x+dx*.3+.005,y+dy*.3,height)],[(0,1,2)],'lawn',color=(.92,1.0,.87))
    ob=blade.finish();ob['cause']='mower edges and clipped foreground sward; 22–52 mm; same July lawn set'


def imported_lawns():
    """Replace only local imported Ground lawn slots and repeat at 3.048m."""
    import bpy
    import geometry as G
    from mathutils import Vector
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not any(ma and ma.name.split('.')[0]=='Lawn' for ma in ob.data.materials):continue
        # Shared street mesh instances need their local color field evaluated
        # in world space; copy only this inexpensive terrain mesh.
        ob.data=ob.data.copy();uv=ob.data.uv_layers.active
        col=ob.data.color_attributes.get('Tint')
        for slot in ob.material_slots:
            if slot.material and slot.material.name.split('.')[0]=='Lawn':slot.material=G.MATS['lawn']
        if not col:col=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='CORNER')
        for face in ob.data.polygons:
            if ob.data.materials[face.material_index]!=G.MATS['lawn']:continue
            for li in face.loop_indices:
                vi=ob.data.loops[li].vertex_index;q=ob.matrix_world@ob.data.vertices[vi].co
                if abs(face.normal.z)>.8:uv.data[li].uv=(q.x/3.048,q.y/3.048)
                col.data[li if col.domain=='CORNER' else vi].color=(*tint(q.x,q.y),1)
