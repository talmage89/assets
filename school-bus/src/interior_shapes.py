"""Padded bench sections with rounded crowns; meter-scale original forms."""
import math
from kit import model as G

def padded_back(b,name,x,y,width=.970,z0=1.570,z1=2.335,barrier=False):
    rings=[];height=z1-z0
    # The 56 mm envelope retains the accepted clear back-to-back spacing.
    stations=[(0,.94,.080,.020),(.12,1,.085,.026),(.48,1,.105,.028),
              (.88,1,.122,.027),(.94,.985,.126,.025),(.978,.93,.128,.019),
              (.995,.85,.129,.008),(1,.82,.129,.002)]
    for t,scale,dy,depth in stations:
        if barrier:dy=0;depth*=1.70
        w=width*scale/2;ring=[]
        for side,values in [(-1,[-1,-.94,-.60,0,.60,.94,1]),(1,[1,.94,.60,0,-.60,-.94,-1])]:
            for u in values:
                ring.append((x+w*u,y+dy+side*depth*(1-.30*u*u),z0+t*height))
        rings.append(ring)
    ob=G.loft(name,rings,b.m['vinyl']);G.smooth(ob,65)
    return b.add(ob,category='interior')

def cushion(b,name,x,y):
    rings=[]
    for dy,scale in [(-.296,.84),(-.287,.96),(-.255,1),(-.08,1),(.115,.97),(.148,.83)]:
        ring=[]
        for k in range(16):
            t=math.tau*k/16;c,s=math.cos(t),math.sin(t)
            xx=.4953*scale*math.copysign(abs(c)**.42,c)
            zz=.064*math.copysign(abs(s)**.60,s)
            crown=.014*max(0,s)*(1-(xx/.4953)**2)
            ring.append((x+xx,y+dy,1.590+zz+crown))
        rings.append(ring)
    ob=G.loft(name,rings,b.m['vinyl']);G.smooth(ob,65)
    return b.add(ob,category='interior')

def front_welts(b,x,y):
    # Only the close entrance benches need silhouette-scale sewn welts.
    # All rows also carry fine seam relief in the source material.
    pts=[(x-.438,y+.110,1.70),(x-.468,y+.112,2.24),
         (x-.454,y+.114,2.29),(x-.415,y+.115,2.318),
         (x,y+.115,2.322),(x+.415,y+.115,2.318),
         (x+.454,y+.114,2.29),(x+.468,y+.112,2.24),(x+.438,y+.110,1.70)]
    b.tube('Bench sewn welt '+str(x)+str(y),pts,.0022,'vinyl',category='interior',sides=4)

def lining(b):
    # Thin light-gray inner panels cover the painted exterior's reverse faces.
    for sign in [-1,1]:
        intervals=[(-2.91,5.95)] if sign<0 else [(-3.88,-.065),(.625,5.95)]
        for j,(a,c) in enumerate(intervals):
            b.box('Interior lower wall '+str(sign)+str(j),(sign*1.187,(a+c)/2,1.504),
                  (.004,c-a,.613),'ceiling',category='interior',r=0)
            b.box('Interior rubber cove '+str(sign)+str(j),(sign*1.181,(a+c)/2,1.226),
                  (.010,c-a,.094),'floor',category='interior',r=.003)
        for i in range(13):
            yy=-2.40+i*.670
            if sign>0 and i==4:continue
            b.box('Interior window post '+str(sign)+str(i),(sign*1.182,yy-.335,2.245),
                  (.005,.043,.869),'ceiling',category='interior',r=0)
    b.box('Interior rear lower liner',(0,5.982,1.493),(.876,.003,.520),
          'ceiling',category='interior',r=0)
    for sign in [-1,1]:
        b.box('Interior rear corner liner '+str(sign),(sign*.854,5.982,1.495),(.672,.003,.606),
              'ceiling',category='interior',r=0)
    b.box('Interior firewall liner',(0,-3.872,1.320),(2.34,.004,1.020),
          'ceiling',category='interior',r=0)
    b.box('Entrance modesty lower panel',(-.689,-2.907,1.458),(.961,.016,.530),
          'ceiling',category='interior',r=.012)
    for x in [-1.04,-.34]:
        b.box('Barrier foot plate '+str(x),(x,-2.905,1.183),(.070,.080,.006),
              'frame',category='interior',r=0)
        b.tube('Barrier support '+str(x),[(x,-2.905,1.185),(x,-2.905,1.66),
               (x,-2.84,1.78),(x,-2.84,2.04)],.014,'frame',category='interior',sides=6)

def paint_reverse_faces(b,ob):
    """Paint the actual inside of closures and headers gray, on their pivots."""
    name=ob.name;direction=None
    if name.startswith(('Body post ','Last corner post ','Forward window bay closure ',
                        'Window header ','Window sill ','Driver window frame')):
        # The outer sheet stays yellow. The greenhouse channel's inner face
        # and perpendicular glass reveals belong to the gray cabin lining.
        sign=1 if sum((ob.matrix_world@v.co).x for v in ob.data.vertices)>0 else -1
        slot=len(ob.data.materials);ob.data.materials.append(b.m['ceiling'])
        normal=ob.matrix_world.to_3x3().inverted().transposed()
        for face in ob.data.polygons:
            if (normal@face.normal).normalized().x*sign<.7:face.material_index=slot
        return
    if name.startswith(('Rear emergency','Rear window jamb','Rear lower field','Rear upper field',
                        'Rear lower sill','Rear exit header','Rear roof cap')):direction=(0,-1,0)
    elif name.startswith(('Side emergency lower','Side emergency upper frame','Driver lower side')):direction=(-1,0,0)
    elif name in ['Windshield header closure','Front roof cap','Stepwell front wall']:direction=(0,1,0)
    elif name=='Stepwell rear wall':direction=(0,-1,0)
    elif name=='Front cap under-header':direction=(0,0,-1)
    if direction is None:return
    from mathutils import Vector
    slot=len(ob.data.materials);ob.data.materials.append(b.m['ceiling'])
    normal=ob.matrix_world.to_3x3().inverted().transposed();axis=Vector(direction)
    for face in ob.data.polygons:
        if (normal@face.normal).normalized().dot(axis)>.7:face.material_index=slot
