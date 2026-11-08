"""Silt/gravel reach, asymmetric banks, sorted bar and water with flow data."""
import math
import random
import bpy
from mathutils import Vector
import geometry as G


def stone(b,x,y,z,r,rng,role='bank'):
    # Low-silhouette angular riprap, individual seating determined by terrain.
    n=7;phase=rng.random()*6.28;sx=rng.uniform(.8,1.3);sy=rng.uniform(.7,1.2)
    base=[(x+sx*r*math.cos(i*math.tau/n+phase),y+sy*r*math.sin(i*math.tau/n+phase),z-r*.22) for i in range(n)]
    top=[(x+sx*r*.7*math.cos(i*math.tau/n+phase),y+sy*r*.7*math.sin(i*math.tau/n+phase),z+r*rng.uniform(.32,.72)) for i in range(n)]
    v=rng.uniform(.60,1.05);b.loft([base,top],role,(v,v,v*.96,1))


def terrain(p,parent):
    rt=G.root('RiverReach',parent=parent)
    b=G.Batch('BedBanksFloodplain',rt,'reach')
    us=[-8,-6,-4,-3,-2.3,-1.8,-1.5,-1.3,-1.15,-1.08,-1,-.94,-.87,-.78,-.66,-.5,-.3,0,.3,.5,.66,.78,.87,.94,1,1.05,1.10,1.16,1.25,1.4,1.7,2.3,3,4,6,8]
    ys=[-p.reach/2+i*2 for i in range(round(p.reach/2)+1)]
    for y0,y1 in zip(ys,ys[1:]):
        for u0,u1 in zip(us,us[1:]):
            vs=[]
            for u,y in ((u0,y0),(u1,y0),(u1,y1),(u0,y1)):
                x=p.center(y)+u*p.halfwidth(y);vs.append((x,y,p.bed(x,y)))
            z=sum(v[2] for v in vs)/4;u=(u0+u1)/2;y=(y0+y1)/2
            role='grass' if abs(u)>1.16 and z>1.1 else 'bank'
            # Broad caused wetness: submerged bed, low wet bank, upper dry soil.
            wet=.48 if z<.12 else .67 if z<.60 else .85
            if role=='grass':
                v=.61+.13*math.sin(y*.067+u*1.7)+.07*math.sin(y*.31-u*.9)
                color=(v*.91,v,v*.72,1)
            else:color=(wet,wet*.98,wet*.90,1)
            b.geom(vs,[(0,1,2,3)],role,color,smooth=True)
    b.finish()
    rng=random.Random(p.seed);rocks=G.Batch('BarCobbleAndScourRiprap',rt,'reach')
    for i in range(1150):
        y=rng.uniform(p.bar_y-26,p.bar_y+27);x=p.center(y)+p.halfwidth(y)*rng.uniform(-1.04,-.49)
        z=p.bed(x,y)
        if z>p.water_z(y)-.32:stone(rocks,x,y,z,rng.uniform(.035,.14),rng)
    # Armored, keyed slope and toe at both abutments and each pier.
    for side in (-1,1):
        for i in range(460):
            x=side*rng.uniform(p.width*.40,p.length/2+3.0);y=rng.uniform(-9,9)
            z=p.bed(x,y);stone(rocks,x,y,z+.04,rng.uniform(.16,.39),rng)
    for j in range(1,p.spans):
        xx=-p.length/2+j*p.span
        for i in range(170):
            x=xx+rng.uniform(-2.0,2.0);y=rng.uniform(-p.deck_width*.48,p.deck_width*.48)
            z=p.bed(x,y);stone(rocks,x,y,z+.06,rng.uniform(.15,.33),rng)
    rocks.finish()
    # Cutbank roots and flood debris are dead wood, not new tree species.
    debris=G.Batch('CutbankExposedRootsAndDrift',rt,'reach')
    for j in range(18):
        y=p.bar_y-20+j*2.3;x=p.center(y)+p.halfwidth(y)*1.11;z=p.bed(x,y)
        for k in range(3):
            debris.tube([(x+.3,y,z+.15),(x-.10,y+.2,z-.2),(x-.45-k*.10,y+.2+k*.23,z-.9)],.018/(k+1),'wood',5)
    for j in range(1,p.spans):
        xx=-p.length/2+j*p.span
        debris.tube([(xx-.9,-p.deck_width/2-1.4,.17),(xx+.1,-p.deck_width/2-.35,.12),(xx+.8,-p.deck_width/2+.3,.19)],.13,'wood',9)
        for k in range(8):debris.tube([(xx-.8+k*.19,-p.deck_width/2-.5,.12),(xx-1+k*.17,-p.deck_width/2-1.3,.23)],.025,'wood',5)
    debris.finish()
    G.path('FlowCenterline',[(p.center(y),y,p.water_z(y)) for y in ys],rt,'flow',flow_direction='+Y',nominal_speed_m_s=.38)
    return rt


def water(p,parent):
    b=G.Batch('WaterSurface',parent,'water');ny=240;nx=20
    rows=[]
    for i in range(ny+1):
        y=-p.reach/2+i*p.reach/ny;l,r=p.water_edges(y)
        rows.append([(l+(r-l)*j/nx,y,p.water_z(y)+.006*math.sin(j*.9+y*.7)*math.exp(-((y-p.riffle_y)/10)**2)) for j in range(nx+1)])
    vs=[v for row in rows for v in row]
    fs=[(i*(nx+1)+j,i*(nx+1)+j+1,(i+1)*(nx+1)+j+1,(i+1)*(nx+1)+j) for i in range(ny) for j in range(nx)]
    b.geom(vs,fs,'water',smooth=True);ob=b.finish()
    flow=ob.data.attributes.new('Flow',type='FLOAT_VECTOR',domain='POINT')
    for v,a in zip(ob.data.vertices,flow.data):
        tx,ty=p.tangent(v.co.y);speed=p.speed(v.co.x,v.co.y);a.vector=(tx*speed,ty*speed,max(0,p.water_z(v.co.y)-p.bed(v.co.x,v.co.y)))
    # A real closed bottom/edge shell makes absorption scale with actual depth.
    volume=G.Batch('WaterVolumeClosure',parent,'water')
    for row in (rows[0],rows[-1]):
        for a,c in zip(row,row[1:]):volume.geom([a,c,(c[0],c[1],p.bed(c[0],c[1])-.02),(a[0],a[1],p.bed(a[0],a[1])-.02)],[(0,1,2,3)],'water')
    for side in (0,-1):
        for a,c in zip(rows,rows[1:]):
            a,c=a[side],c[side];volume.geom([a,c,(c[0],c[1],p.bed(c[0],c[1])-.02),(a[0],a[1],p.bed(a[0],a[1])-.02)],[(0,1,2,3)],'water')
    floor=[(x,y,p.bed(x,y)-.02) for x,y,z in vs];volume.geom(floor,[tuple(reversed(f)) for f in fs],'water',smooth=True)
    volume.finish()
    foam=G.Batch('RiffleBrokenFoam',parent,'water');rng=random.Random(p.seed+31)
    for j in range(160):
        y=rng.gauss(p.riffle_y,3.5);l,r=p.water_edges(y);x=rng.uniform(l+.7,r-.7)
        length=rng.uniform(.07,.5);w=rng.uniform(.008,.028)
        foam.geom([(x-length/2,y,p.water_z(y)+.013),(x+length/2,y+.06,p.water_z(y)+.013),(x+length*.30,y+.06+w,p.water_z(y)+.014),(x-length*.4,y+w,p.water_z(y)+.014)],[(0,1,2,3)],'foam')
    foam.finish()
