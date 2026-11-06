"""Sparse lived-in cues; all geometry and strings authored here."""
import math
from components import STEEL,ALUM


def add(a,w,d,base,fh,seed):
    m=a.mesh('Tenant_belongings',component='occupancy')
    # A locked bicycle leans beside the rear wall, a slack cable follows frame.
    x=-w*.38;y=d/2+.48;z=.34
    for dx in (-.52,.52):
        pts=[(x+dx+.32*math.cos(k*math.tau/20),y,z+.32*math.sin(k*math.tau/20)) for k in range(21)]
        m.tube(pts,.025,'Trim',(.020,.024,.019),sides=6)
        for k in range(8):
            t=k*math.tau/8;m.beam((x+dx,y,z),(x+dx+.30*math.cos(t),y,z+.30*math.sin(t)),.005,.005,'Trim',ALUM,r=0)
    for aa,bb in (((-.52,.34),(-.18,.79)),((-.18,.79),(.06,.34)),((.06,.34),(-.52,.34)),((-.18,.79),(.40,.76)),((.40,.76),(.06,.34)),((.40,.76),(.52,.34))):m.beam((x+aa[0],y,aa[1]),(x+bb[0],y,bb[1]),.027,.027,'Trim',(.17,.07,.035),r=.001)
    m.box((x-.17,y,.83),(.25,.16,.035),'Trim',(.025,.027,.021),r=.008)
    m.tube([(x-.16,y,.35),(x-.28,y-.04,.25),(x-.52,y-.03,.20),(x-.64,y+.07,.36),(x-.50,y+.14,.45)],.008,'Trim',STEEL,sides=6)
    # The bicycle's original 20 mm tire minimum rests on the low patio top.
    m.v=[(xx,yy,zz+base) for xx,yy,zz in m.v]
    grill_start=len(m.v)
    # Small kettle grill sits on three legs at a ground-floor patio.
    x=w*.27;y=-d/2-.85
    for t in (0,2.1,4.2):m.beam((x+.27*math.cos(t),y+.27*math.sin(t),0),(x+.16*math.cos(t),y+.16*math.sin(t),.54),.024,.024,'Trim',ALUM,r=.001)
    loops=[]
    for zz,rr in ((.43,.05),(.51,.22),(.65,.28),(.68,.28),(.80,.20),(.86,.035)):
        loops.append([(x+rr*math.cos(k*math.tau/16),y+rr*math.sin(k*math.tau/16),zz) for k in range(16)])
    from kit import model as G
    ob=G.loft('Patio kettle grill',loops,a.materials[4]);ob.parent=a.root;ob.location.z=base+.02
    attr=ob.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
    for v in attr.data:v.color=(.025,.036,.028,1)
    m.v=m.v[:grill_start]+[(xx,yy,zz+base+.02) for xx,yy,zz in m.v[grill_start:]]
    # A small bracketed dish on an end wall, not an unsupported satellite disk.
    x=w/2+.25;y=d*.25;z=base+fh+1.35
    m.beam((w/2,y,z-.3),(x+.20,y,z-.3),.04,.04,'Trim',ALUM,r=.001)
    m.beam((x+.20,y,z-.3),(x+.20,y,z),.04,.04,'Trim',ALUM,r=.001)
    center=(x+.21,y,z);verts=[center];rings=16
    for k in range(rings):
        t=k*math.tau/rings;verts.append((x+.30,y+.34*math.cos(t),z+.28*math.sin(t)))
    m.geom(verts,[(0,k+1,(k+1)%rings+1) for k in range(rings)],'Trim',(.46,.45,.40))
    # Left-up lights droop along the low patio eave; no imaginary taut cable.
    if seed%2==0:
        pts=[(-w*.3+k*.20,-d/2-.06,base+fh-.14-.035*math.sin(k*math.pi/5)) for k in range(22)]
        m.tube(pts,.003,'Trim',STEEL,sides=4)
        for k,p in enumerate(pts[::2]):m.box((p[0],p[1],p[2]-.018),(.012,.012,.028),'Trim',(.42,.22,.10) if k%2 else (.26,.34,.20),r=.002)
    m.finish()
