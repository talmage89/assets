"""Visible service construction, routed drains, gear and supported accessories."""
import math
from geo import orient,text


def equipment(a,p):
    x,y,z=p;m=a.mesh('RoofMechanical',kind='HVAC',trim_strip=7)
    m.box((x,y,z+.18),(2.20,1.65,.36),'Trim',(.21,.23,.21))
    m.box((x,y,z+.70),(2.05,1.48,.75),'Trim',(.48,.49,.43))
    m.box((x,y,z+1.10),(2.16,1.57,.12),'Trim',(.43,.44,.40))
    for xx in (x-.53,x+.53):
        m.tube([(xx,y,z+1.15),(xx,y,z+1.23)],.40,'Trim',(.08,.09,.08),sides=24)
        for j in range(7):m.box((xx,y+(j-3)*.105,z+1.24),(.76,.014,.015),'Trim',(.28,.29,.27),r=0)
    m.finish()


def drains(a,rect,top):
    l,r,f,k=rect;m=a.mesh('Drainage',kind='ScupperDownspout',trim_strip=2)
    for x,y in ((l+.38,f-.08),(r-.38,k+.08)):
        m.box((x,y,top-.12),(.26,.23,.20),'Trim',(.24,.25,.21))
        pts=[(x,y,top-.10),(x,y,top-.45),(x,y-.12,top-.65),(x,y-.12,.30),(x,y-.40,.17)]
        m.tube(pts,.058,'Trim',(.24,.25,.21),sides=8)
        for z in (.7,2.7,4.7,6.7):
            if z<top:m.box((x,y-.10,z),(.17,.15,.035),'Trim',(.32,.34,.30))
        m.box((x,y-.52,.07),(.40,.75,.12),'Concrete',(.32,.32,.28))
    m.finish()


def gear(a,name,p):
    x,y,z=p;m=a.mesh(name,kind='TurnoutGearRack',trim_strip=2)
    for xx in (x-.31,x+.31):
        m.tube([(xx,y,z),(xx,y,z+2.05)],.018,'Trim',(.30,.32,.30),sides=8)
        for zz in (.15,1.8,2.05):m.tube([(xx,y-.30,z+zz),(xx,y+.25,z+zz)],.014,'Trim',sides=6)
    for zz in (.15,1.8,2.05):m.tube([(x-.31,y,z+zz),(x+.31,y,z+zz)],.018,'Trim',sides=8)
    # Hanging coat has an elliptical body, sagging hem and separate drooping sleeves.
    vs=[];levels=[(.55,.22,.14),(.61,.24,.15),(1.05,.23,.15),(1.45,.24,.16),(1.60,.16,.13)]
    n=12
    for zz,rx,ry in levels:
        for j in range(n):
            t=j*math.tau/n;fold=.012*math.cos(t*5+zz*2)
            vs.append((x+(rx+fold)*math.cos(t),y+(ry+fold)*math.sin(t)-.07,z+zz+.015*math.sin(t*3)))
    fs=[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]
    fs += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(levels)-1) for i in range(n)]
    m.geom(vs,fs,'Trim',(.25,.20,.11))
    for s in (-1,1):
        m.tube([(x+s*.19,y-.07,z+1.47),(x+s*.30,y-.08,z+1.28),(x+s*.34,y-.12,z+1.0)],.080,'Trim',(.25,.20,.11),sides=10)
        m.box((x+s*.115,y-.08,z+.30),(.13,.28,.42),'Trim',(.030,.033,.026))
    for zz in (.69,1.18):m.tube([(x-.20,y-.18,z+zz),(x+.20,y-.18,z+zz)],.024,'Trim',(.65,.64,.23),sides=6)
    m.tube([(x,y,z+1.84),(x,y,z+1.97)],.18,'Trim',(.59,.43,.020),sides=16)
    m.tube([(x,y,z+1.96),(x,y,z+2.09)],.14,'Trim',(.59,.43,.020),sides=16)
    m.finish()


def bollard(a,p,name='Bollard'):
    m=a.mesh(name,kind='Bollard',trim_strip=5,weather=True)
    x,y,z=p;m.tube([(x,y,z),(x,y,z+1.0)],.0825,'Trim',(.64,.38,.020),sides=12)
    m.tube([(x,y,z+.90),(x,y,z+.98)],.086,'Trim',(.24,.24,.17),sides=12);return m.finish()


def flagpole(a,p,name):
    x,y,z=p;m=a.mesh(name,kind='Flagpole',trim_strip=2,weather=True)
    m.box((x,y,.06),(.48,.48,.12),'Concrete',(.32,.31,.27))
    m.tube([(x,y,z),(x,y,z+9.1)],.044,'Trim',(.48,.49,.46),sides=16)
    m.tube([(x-.04,y,1.3),(x-.04,y,8.9)],.004,'Trim',(.32,.30,.24),sides=4)
    m.tube([(x+.04,y,1.3),(x+.04,y,8.9)],.004,'Trim',(.32,.30,.24),sides=4)
    m.finish();a.pivot(name+'_Flag',(x,y,8.8),axis='Z',limits=(-180,180))
    f=a.mesh(name+'_Cloth',part=name+'_Flag',kind='Flag',trim_strip=4)
    vs=[];nx,ny=10,6
    for j in range(ny+1):
        for i in range(nx+1):
            u=i/nx;v=j/ny;vs.append((x+u*1.5,y+.14*math.sin(u*8-v*3)*u,8.8-v*.85-.15*u*u))
    fs=[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)]
    f.geom(vs,fs,'Trim',(.08,.15,.21));f.finish()


def back_service(a,p):
    x,y,z=p;m=a.mesh('RearServiceEquipment',kind='GeneratorMeterBank',trim_strip=7)
    m.box((x,y,.08),(3.4,2.1,.16),'Concrete',(.34,.34,.30))
    m.box((x,y,.78),(2.7,1.4,1.4),'Trim',(.25,.29,.23))
    m.box((x,y,1.52),(2.85,1.52,.13),'Trim',(.29,.32,.26))
    for j in range(4):
        xx=x-1+j*.65;m.box((xx,y+2,1.2),(.35,.22,.55),'Trim',(.43,.45,.41))
        m.tube([(xx,y+1.86,1.22),(xx,y+1.82,1.22)],.105,'Glass',sides=12)
        m.tube([(xx,y+2,.05),(xx,y+2,.94)],.022,'Trim',sides=8)
    m.finish()


def dumpster(a,p):
    x,y,z=p;m=a.mesh('DumpsterEnclosure',kind='ServiceEnclosure',brick_strip=1,weather=True)
    for xx in (x-2,x+2):m.box((xx,y+1,1.0),(.20,3.2,2),'Veneer',r=0)
    m.box((x,y+2.5,1),(4.2,.20,2),'Veneer',r=0)
    for xx in (x-2,x+2):m.box((xx,y+1,2.05),(.30,3.3,.10),'Concrete')
    m.box((x,y+2.5,2.05),(4.2,.30,.10),'Concrete');m.finish()
    m=a.mesh('DumpsterContainer',kind='Dumpster',trim_strip=5)
    m.box((x,y+.8,.75),(2.25,1.4,1.30),'Trim',(.035,.095,.07))
    for xx in (x-.92,x+.92):
        m.box((xx,y+.80,1.12),(.25,1.47,.19),'Trim',(.035,.085,.06))
        m.box((xx,y+.8,.12),(.18,1.1,.20),'Trim',(.040,.045,.038))
    m.finish();a.pivot('DumpsterLid',(x,y+1.5,1.45),axis='X',limits=(0,105))
    m=a.mesh('DumpsterLidMesh',part='DumpsterLid',kind='DumpsterLid',trim_strip=1)
    m.box((x,y+.8,1.48),(2.35,1.50,.075),'Trim',(.035,.040,.032));m.finish()
    for j in range(2):
        a.pivot('EnclosureGate_'+str(j),(x-2+4*j,y-.60,0),axis='Z',limits=(0,105))
        m=a.mesh('EnclosureGateMesh_'+str(j),part='EnclosureGate_'+str(j),kind='EnclosureGate',trim_strip=0)
        for t in range(13):m.box((x-1+j*2+(t-6)*.14,y-.60,1),(.13,.065,1.90),'Trim',(.16,.13,.085),r=.002)
        m.finish()
