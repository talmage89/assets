"""Original tilting fiberglass mold, with a supported subdivision cage.

The crown, shoulder and fender share one cage. A transverse wheelhouse cut
and finite laminate gauge follow subdivision. No photographic contour enters it.
"""
import math
from functools import lru_cache
import numpy as np
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from kit import model as G
from kit.vehicle import panel
import spec as S

# Evenly spaced fairing stations between the two boundary support loops.
# The old cage changed both its shoulder height and its transverse blend in
# the last four stations: two overlapping eases made a dent in each fender.
def fair_station(y):
    t=max(0,min(1,(y+5.94)/1.953))
    nose=max(0,1-(y+5.94)/.52);nose=nose*nose
    width=1.202-.132*nose-.024*t*t
    top=1.480+.566*t-.160*t*t
    gap=.335+.065*math.sin(math.pi*t)
    bottom=.700+.110*nose+.100*t**8
    return (y,width,top,top-gap,bottom)

STATIONS=[(-5.964,1.045,1.455,1.125,.830)]+[
    fair_station(y) for y in [-5.938,-5.66,-5.38,-5.10,-4.82,-4.54,-4.26,-4.015,-3.987]]

def section(row):
    y,w,top,shoulder,bottom=row
    half=[(0,top+.012),(.28,top+.005),(.56,top-.016),(.72,top-.054),
          (.79,top-.121),(.85,shoulder+.055),(.955,shoulder+.036),
          (w-.045,shoulder-.020),(w,shoulder-.079),(w,bottom+.030),
          (w-.006,bottom)]
    # At the cowl the shoulder rises into the crown using a single fair ease.
    t=max(0,min(1,(y+4.58)/.593));t=t*t*t*(10-15*t+6*t*t)
    offsets=[.012,.008,.005,.002,-.001,-.003,-.005,-.007,-.011]
    half=[(x,z*(1-t)+(top+offsets[i])*t) if i<9 else (x,z) for i,(x,z) in enumerate(half)]
    return [(-x,y,z) for x,z in reversed(half[1:])]+[(x,y,z) for x,z in half]

def optical_bow(ob,skin_y,reference_y):
    """Conform cassette layers to the mold, keeping their authored depth."""
    # attach() has just rebased box vertices into the bus root. Flush its
    # identity transform before bending: a stale box-location matrix applies
    # the center twice and pushes the small bulbs/signals into the bucket back.
    bpy.context.view_layer.update()
    world=ob.matrix_world.copy();inverse=world.inverted()
    for vertex in ob.data.vertices:
        p=world@vertex.co;p.y+=skin_y(p.x,p.z)+.008-reference_y
        vertex.co=inverse@p
    ob.data.update()
    return ob

def sculpt(b):
    rings=[section(r) for r in STATIONS];n=len(rings[0]);vs=[p for r in rings for p in r]
    fs=[(j*n+i,j*n+i+1,(j+1)*n+i+1,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n-1)]
    # Front shell annulus: support rings hold a recessed, rounded grille mouth.
    # Its count matches the outside contour, and the shell is welded at the nose.
    outer=[(x,z) for x,_,z in rings[0]]
    center=1.125
    def aperture(x,z):
        dx,dz=x,z-center
        scale=(abs(dx/.625)**4+abs(dz/.277)**4)**.25
        return dx/max(scale,1e-8),center+dz/max(scale,1e-8)
    inner=[aperture(x,z) for x,z in outer]
    # Closing lower edge belongs only to the nose, leaving engine bay open below.
    outer.append((0,.830));inner.append((0,center-.277))
    vs.append((0,STATIONS[0][0],.830));prev=list(range(n))+[len(vs)-1]
    for amount,depth in [(.10,-.004),(.90,.001),(1,.010),(1,.055),(1,.078)]:
        ids=[]
        for (ox,oz),(ix,iz) in zip(outer,inner):
            x=ox+(ix-ox)*amount;z=oz+(iz-oz)*amount
            ids.append(len(vs));vs.append((x,-5.964+depth+.055*(x/1.1)**2,z))
        fs.extend((prev[i],prev[(i+1)%len(ids)],ids[(i+1)%len(ids)],ids[i]) for i in range(len(ids)))
        prev=ids
    ob=G.mesh('Compound hood shell',vs,fs,b.m['yellow']);b.add(ob)
    sub=ob.modifiers.new('Fiberglass compound subdivision','SUBSURF');sub.levels=1;sub.render_levels=1
    high=ob.copy();high.data=ob.data.copy();bpy.context.collection.objects.link(high)
    high.name='Dense front mold';del high['asset_set'];high['bake_only']=True
    high.modifiers[0].levels=3;high.modifiers[0].render_levels=3
    # Keep an independently generated dense mold for selected-to-active normals.
    # It is saved separately, never joined into or exported with the game mesh.
    ob['mold_source']='Ten longitudinal fairing stations, single cowl ease; dense level-3 mold'
    for mold in [ob,high]:
        G.apply(mold)
        wall=mold.modifiers.new('Six millimeter fiberglass laminate','SOLIDIFY');wall.thickness=.006;wall.offset=-1
        G.apply(mold)
        for sign in [-1,1]:
            cut=G.cylinder('Wheelhouse mold tool',(sign*.76,S.FRONT_AXLE,S.HUB),(sign*1.50,S.FRONT_AXLE,S.HUB),.692,None,96)
            G.boolean(mold,cut)
        G.smooth(mold,50)
    # Thin black wheelhouse liners sit inside the laminate lip, with a real
    # radial/axial return. They preserve the steering tire's swept envelope.
    for sign in [-1,1]:
        loops=[];start=math.asin((.720-S.HUB)/.705)
        for i in range(37):
            t=start+(math.pi-2*start)*i/36
            loops.append([(sign*xx,S.FRONT_AXLE+rr*math.cos(t),S.HUB+rr*math.sin(t))
                          for xx,rr in [(.790,.705),(1.170,.705),(1.170,.709),(.790,.709)]])
        liner=G.loft('Front wheelhouse liner '+str(sign),loops,b.m['black'])
        G.smooth(liner,35);b.add(liner)
    # Narrow recessed mouth, actual return walls and a radiator behind the web.
    contour=G.rounded_rectangle(1.20,.505,.080,6)
    rings=[[(x,-5.895+d+.055*(x/1.1)**2,1.125+z) for x,z in contour] for d in [0,.012,.076]]
    b.add(G.ring_loft('Seated grille molding',rings,b.m['black']))
    b.box('Grille radiator bed',(0,-5.788,1.125),(1.205,.020,.512),'black',r=.070)
    # A restrained horizontal open grille has depth; original eight paired slots.
    for j in range(7):
        z=.925+j*.064
        points=[(x,-5.857+.055*(x/1.1)**2,z) for x in [-.565,-.35,0,.35,.565]]
        b.tube('Recessed grille cross web '+str(j),points,.008,'frame',sides=6)
    for x in [-.40,-.20,0,.20,.40]:
        b.box('Grille vertical web '+str(x),(x,-5.831,1.117),(.008,.025,.427),'black',r=.002)
    # Locate the real game mold before routing either lamp. The upper outside
    # corners sweep back into the fender; a constant-Y trim ring floats there.
    bpy.context.view_layer.update();ob.data.calc_loop_triangles()
    skin=BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],
        [tuple(t.vertices) for t in ob.data.loop_triangles],all_triangles=True)
    high.data.calc_loop_triangles()
    optical_mold=BVHTree.FromPolygons([high.matrix_world@v.co for v in high.data.vertices],
        [tuple(t.vertices) for t in high.data.loop_triangles],all_triangles=True)
    def measured_y(x,z):
        hit=optical_mold.ray_cast(Vector((x,-6.5,z)),Vector((0,1,0)),3)[0]
        if hit is None:raise ValueError('Optical surface misses the dense mold')
        return hit.y
    # Fair optical die over the actual molding, inside its frontal land. The
    # glass needs C2 curvature, rather than every triangle of the projection.
    samples=[(u,v) for u in np.linspace(-1,1,7) for v in np.linspace(-1,1,7)]
    design=np.array([[u**i*v**j for i in range(3) for j in range(3)] for u,v in samples])
    heights=np.array([measured_y(.840+.180*u,1.000+.150*v) for u,v in samples])
    coefficients=np.linalg.lstsq(design,heights,rcond=None)[0]
    @lru_cache(maxsize=20000)
    def front_y(x,z):
        u=(abs(x)-.840)/.180;v=(z-1.000)/.150
        return float(sum(c*u**i*v**j for c,(i,j) in zip(coefficients,[(i,j) for i in range(3) for j in range(3)])))
    # Each lamp is a bonded cassette inside a real cut in the common molding.
    for sign in [-1,1]:
        x=sign*.840;z=1.040
        # The cover seats 8 mm behind the surrounding nose, sweeping rearward
        # toward the wheel. A yellow laminate reveal encloses the thin gasket.
        face_y=front_y(x,z)+.008
        def warp(part):return optical_bow(part,front_y,face_y)
        # The dense source is the smooth mold before these routed cassette
        # openings. Their narrow laminate returns use exact game normals;
        # projecting the original mold onto those perpendicular walls is wrong.
        # Route only the nose wall. Extending this tool behind the cassette
        # pierced the swept fender roof, leaving two small top-view holes.
        # The routed aperture follows the same curved die as the cover. A
        # planar cutter stopped short beneath the swept upper outside corner.
        aperture=G.rounded_rectangle(.355,.275,.036,6)
        cut=G.loft('Optical pocket tool',[
            [(x+xx,-6.30,1.000+zz) for xx,zz in aperture],
            [(x+xx,front_y(x+xx,1.000+zz)+.150,1.000+zz) for xx,zz in aperture]],None)
        G.boolean(ob,cut)
        # A lapped, molded yellow return hides the cassette wall: the housing
        # is behind the fender skin, with only its thin seal exposed.
        contours=[(.365,.285,.040,0),(.349,.273,.033,.35),(.335,.260,.028,1)]
        reveal=[]
        for w,h,r,blend in contours:
            ring=[]
            for xx,zz in G.rounded_rectangle(w,h,r,4):
                px,pz=x+xx,1.000+zz
                hit=skin.ray_cast(Vector((px,-6.5,pz)),Vector((0,1,0)),3)[0]
                if hit is None:raise ValueError('Optical surround misses the actual mold')
                cassette=front_y(px,pz)+.018
                ring.append((px,hit.y+.001+(cassette-hit.y)*blend,pz))
            reveal.append(ring)
        flange=G.ring_loft('Headlamp molded reveal '+str(sign),reveal,b.m['yellow'])
        # Set smoothing boundaries on the actual triangles of this small,
        # twisted return, rather than on non-planar quads before tessellation.
        tri=flange.modifiers.new('Mold return triangles','TRIANGULATE');tri.quad_method='BEAUTY'
        G.apply(flange);G.smooth(flange,35);b.add(flange)
        bucket=b.box('Headlamp closed bucket '+str(sign),(x,face_y+.050,1.000),(.334,.104,.264),'black',r=.027)
        G.boolean(bucket,G.box('Optical bucket interior',(x,face_y+.020,1.000),(.324,.160,.244),None,.022,4))
        warp(bucket)
        for dx in [-.082,.082]:
            contour=G.rounded_rectangle(.130,.110,.023,4)
            rings=[[(x+dx+xx*scale,face_y+depth,z+zz*scale) for xx,zz in contour]
                   for scale,depth in [(1,.020),(.72,.040),(.21,.070)]]
            reflector=G.loft('Headlamp formed reflector '+str(sign)+str(dx),rings,b.m.get('reflector',b.m['aluminum']),caps=False)
            wall=reflector.modifiers.new('Reflector gauge','SOLIDIFY');wall.thickness=.001
            G.smooth(reflector,65);b.add(reflector,category='lamps');warp(reflector)
            warp(b.box('Lamp front lowbeam '+str(sign)+str(dx),(x+dx,face_y+.068,z),(.038,.005,.034),'headlight',category='lamps',r=.010))
        def cover(u,v,x=x,z=z):
            xx=x+(u-.5)*.320;zz=z+(v-.5)*.170
            return xx,front_y(xx,zz)+.008-.0015*math.sin(math.pi*u)*math.sin(math.pi*v),zz
        obc=panel('Glass sealed headlamp cover '+str(sign),cover,[i/8 for i in range(9)],[i/6 for i in range(7)],b.m.get('lens',b.m['windshield']),(0,-1,0),gauge=.0024,return_depth=0)
        b.add(obc,category='glass')
        bezel=[(x+xx,front_y(x+xx,z+zz)+.008,z+zz) for xx,zz in G.rounded_rectangle(.336,.189,.025,6)]
        b.tube('Bonded headlamp bezel '+str(sign),bezel+[bezel[0]],.004,'black',sides=6)
        warp(b.box('Front amber signal '+str(sign),(x,face_y+.014,.906),(.225,.010,.046),'amber',category='lamps',r=.017))
        # Backed parting line follows the full curved cowl, rather than a plate.
        b.box('Hood rubber latch '+str(sign),(sign*1.175,-4.11,1.31),(.032,.058,.138),'black',r=.008)
    gasket=G.loft('Hood cowl parting line',
        [[(x,yy,z) for x,_,z in section(STATIONS[-1])] for yy in [-3.985,-3.964]],
        b.m['black'],caps=False,closed=False)
    gauge=gasket.modifiers.new('Cowl gasket gauge','SOLIDIFY');gauge.thickness=.002
    b.add(gasket)
    high['normal_scope']='Subdivided fiberglass mold; routed optical returns retain exact game normals'
    high.hide_render=True
    return ob
