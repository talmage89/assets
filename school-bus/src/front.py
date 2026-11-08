"""Original tilting fiberglass mold, with a supported subdivision cage.

The crown, shoulder and fender share one cage. A transverse wheelhouse cut
and finite laminate gauge follow subdivision. No photographic contour enters it.
"""
import math
import bpy
from kit import model as G
from kit.vehicle import panel
import spec as S

# y, width, center crown, fender shoulder, lower edge. Closely spaced first
# and last stations support the nose rollover and the actual cowl parting line.
STATIONS=[(-5.964,1.045,1.455,1.125,.830),(-5.938,1.070,1.479,1.145,.810),
 (-5.84,1.112,1.510,1.185,.770),(-5.67,1.166,1.554,1.232,.725),
 (-5.44,1.192,1.610,1.284,.700),(-5.20,1.202,1.667,1.314,.700),
 (-4.953,1.202,1.720,1.328,.700),(-4.70,1.197,1.773,1.353,.700),
 (-4.45,1.187,1.822,1.425,.700),(-4.23,1.177,1.857,1.555,.720),
 (-4.075,1.177,1.878,1.734,.770),(-4.015,1.178,1.885,1.805,.800),
 (-3.987,1.178,1.886,1.822,.800)]

def section(row):
    y,w,top,shoulder,bottom=row
    half=[(0,top+.012),(.32,top+.008),(.59,top-.015),(.72,top-.054),
          (.79,top-.121),(.85,shoulder+.055),(.955,shoulder+.036),
          (w-.045,shoulder-.020),(w,shoulder-.079),(w,bottom+.030),
          (w-.006,bottom)]
    t=max(0,min(1,(y+4.45)/.435));t=t*t*(3-2*t)
    # The fender shoulder merges into the nearly level windshield sill.
    # A rising shoulder must not cross the falling crown and make a trough.
    offsets=[.012,.008,.005,.002,-.001,-.003,-.005,-.007,-.011]
    half=[(x,z*(1-t)+(top+offsets[i])*t) if i<9 else (x,z) for i,(x,z) in enumerate(half)]
    return [(-x,y,z) for x,z in reversed(half[1:])]+[(x,y,z) for x,z in half]

def optical_bow(ob,center_x):
    """Seat every cassette layer behind the same bowed cover mold."""
    world=ob.matrix_world.copy();inverse=world.inverted()
    for vertex in ob.data.vertices:
        p=world@vertex.co;p.y+=.055*((p.x/1.1)**2-(center_x/1.1)**2)
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
    ob['mold_source']='Supported cage, Catmull-Clark; high source uses three levels'
    for mold in [ob,high]:
        G.apply(mold)
        wall=mold.modifiers.new('Six millimeter fiberglass laminate','SOLIDIFY');wall.thickness=.006;wall.offset=-1
        G.apply(mold)
        for sign in [-1,1]:
            cut=G.cylinder('Wheelhouse mold tool',(sign*.76,S.FRONT_AXLE,S.HUB),(sign*1.50,S.FRONT_AXLE,S.HUB),.692,None,96)
            G.boolean(mold,cut)
        G.smooth(mold,50)
    high.hide_render=True
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
    # Each lamp is a bonded cassette inside a real cut in the common molding.
    for sign in [-1,1]:
        x=sign*.882;z=1.070;face_y=-5.940+.055*(x/1.1)**2
        for mold in [ob,high]:
            cut=G.box('Optical pocket tool',(x,-5.88,1.035),(.395,.38,.305),None,.040,5)
            G.boolean(mold,cut)
        bucket=b.box('Headlamp closed bucket '+str(sign),(x,face_y+.050,1.035),(.400,.104,.314),'black',r=.035)
        G.boolean(bucket,G.box('Optical bucket interior',(x,face_y+.020,1.035),(.378,.160,.292),None,.028,4))
        optical_bow(bucket,x)
        for dx in [-.092,.092]:
            contour=G.rounded_rectangle(.146,.125,.023,4)
            rings=[[(x+dx+xx*scale,face_y+depth,z+zz*scale) for xx,zz in contour]
                   for scale,depth in [(1,.008),(.72,.035),(.21,.065)]]
            reflector=G.loft('Headlamp formed reflector '+str(sign)+str(dx),rings,b.m.get('reflector',b.m['aluminum']),caps=False)
            wall=reflector.modifiers.new('Reflector gauge','SOLIDIFY');wall.thickness=.001
            G.smooth(reflector,65);b.add(reflector,category='lamps');optical_bow(reflector,x)
            optical_bow(b.box('Lamp front lowbeam '+str(sign)+str(dx),(x+dx,face_y+.063,z),(.044,.005,.038),'headlight',category='lamps',r=.010),x)
        def cover(u,v,x=x,z=z):
            xx=x+(u-.5)*.360;zz=z+(v-.5)*.192
            return xx,-5.940+.055*(xx/1.1)**2-.003*math.sin(math.pi*u)*math.sin(math.pi*v),zz
        obc=panel('Glass sealed headlamp cover '+str(sign),cover,[0,.10,.25,.5,.75,.9,1],[0,.2,.5,.8,1],b.m.get('lens',b.m['windshield']),(0,-1,0),gauge=.0024,return_depth=0)
        b.add(obc,category='glass')
        bezel=[(x+xx,-5.940+.055*((x+xx)/1.1)**2,z+zz) for xx,zz in G.rounded_rectangle(.376,.211,.025,4)]
        b.tube('Bonded headlamp bezel '+str(sign),bezel+[bezel[0]],.008,'black',sides=6)
        optical_bow(b.box('Front amber signal '+str(sign),(x,face_y+.004,.915),(.245,.010,.054),'amber',category='lamps',r=.017),x)
        # Backed parting line follows the full curved cowl, rather than a plate.
        b.box('Hood rubber latch '+str(sign),(sign*1.175,-4.11,1.31),(.032,.058,.138),'black',r=.008)
    gasket=G.loft('Hood cowl parting line',
        [[(x,yy,z) for x,_,z in section(STATIONS[-1])] for yy in [-3.985,-3.964]],
        b.m['black'],caps=False,closed=False)
    gauge=gasket.modifiers.new('Cowl gasket gauge','SOLIDIFY');gauge.thickness=.002
    b.add(gasket)
    return ob
