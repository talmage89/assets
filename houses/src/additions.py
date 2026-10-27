"""Rear circulation, a reserved stairwell, shallow foyer and gas-fireplace chase."""
import math
from mathutils import Vector
from kit import model as G


def portal(b,o):
    block=next(v for v in b.plan['blocks'] if v.name==o['block'])
    xf,n,length=b.frame(block,o['face']);u,z,w,h=[o[k] for k in ('u','z','w','h')]
    fixed=b.mesh(o['id']+'_Frame',component='secondary_door_frame')
    for s in (-1,1):fixed.box((u+s*(w/2+.045),.043,z+h/2),(.09,.07,h+.1),xf=xf)
    fixed.box((u,.043,z+h+.045),(w+.18,.07,.09),xf=xf)
    fixed.box((u,-.025,z-.008),(w,.28,.016),color=(.25,.26,.24),r=.001,xf=xf)
    if o['kind']=='patio':
        pivot=G.pivot('PatioDoor',xf((u-w/4,.028,z)));pivot.parent=b.root
        pivot['slide_axis']='X';pivot['range_m']=[0,w/2-.0762]
        b.moving['PatioDoor']=pivot
        for side,part,v in ((-1,'PatioDoor',.028),(1,'Static',-.020)):
            me=b.mesh('Patio_Slider' if side<0 else 'Patio_Fixed',part,component='patio_door')
            cx=u+side*w/4;pw=w/2-.027
            for s in (-1,1):me.box((cx+s*(pw/2-.026),v,z+h/2),(.052,.030,h-.014),xf=xf)
            for zz in (z+.038,z+h-.038):me.box((cx,v,zz),(pw-.10,.030,.062),xf=xf)
            me.box((cx,v-.019,z+h/2),(pw-.10,.004,h-.13),'Glass',b.colors['Glass'],0,xf)
            if side<0:
                me.box((cx+pw/2-.08,v+.028,z+.98),(.035,.025,.14),color=(.18,.19,.17),r=.006,xf=xf)
            me.finish()
        # A softly folded sheer at one side leaves the sliding opening legible.
        for i in range(10):
            fixed.box((u+w*.36+(i-4.5)*.021,-.17-.009*math.cos(i*1.5),z+h/2),(.023,.018,h-.10),color=(.43,.40,.33),r=.005,xf=xf)
        fixed.box((u,-.42,z+h/2),(w-.06,.012,h-.04),color=(.065,.061,.049),r=0,xf=xf)
    else:
        p=xf((u-w/2+.004,-.153,z+.006));pivot=G.pivot('ServiceDoor',p,'Z',(-100,0) if n[0]<0 else (0,100));pivot.parent=b.root
        b.moving['ServiceDoor']=pivot
        me=b.mesh('ServiceDoor_Leaf','ServiceDoor',component='service_door')
        me.box((u,-.128,z+h/2),(w-.008,.044,h-.012),r=.002,xf=xf)
        for zz in (z+.57,z+1.48):
            me.box((u,-.102,zz),(w-.20,.014,.64),color=tuple(c*.88 for c in b.colors['Trim']),r=.007,xf=xf)
        me.tube([xf((u+w*.34,-.104,z+1.0)),xf((u+w*.34,-.065,z+1.0))],.022,color=(.22,.23,.21))
        me.finish()
        step=b.mesh('GarageService_Step',component='service_step')
        step.box(xf((u,.34,.05)),(1.08,.65,.10) if abs(n[1])>.5 else (.65,1.08,.10),'Concrete',r=.005)
        step.finish()
    fixed.finish()


def rear_landing(b):
    m=b.plan['blocks'][0];x=m.x0+m.width*.56;y=m.y1;w=4.2672
    kind=b.plan['spec']['rear_landing'];me=b.mesh('Rear_'+kind.title(),component='rear_landing')
    if kind=='patio':
        me.box((x,y+1.55,.0508),(w,3.10,.1016),'Concrete',r=.007)
        me.box((x,y+.47,.2908),(2.24,.94,.3784),'Concrete',r=.005)
        for i in range(2):
            top=.48-(i+1)*(.3784/3);yy=y+.94+(i+.5)*.3048
            me.box((x,yy,(top+.1016)/2),(1.65,.3048,top-.1016),'Concrete',r=.004)
    else:
        depth=2.4384;wood=(.24,.22,.18)
        for j in range(18):me.box((x,y+(j+.5)*depth/18,.468),(w-.002,depth/18-.004,.024),'Trim',wood,.001)
        for xx in (x-w/2+.07,x+w/2-.07):
            me.box((xx,y+depth/2,.37),(.14,depth,.172),'Trim',wood,.002)
            for yy in (y+.15,y+depth-.15):me.box((xx,yy,.16),(.089,.089,.32),'Trim',wood,.002)
        for i in range(2):
            top=.32-i*.16;yy=y+depth+(i+.5)*.3048
            me.box((x,yy,top-.019),(1.22,.3048,.038),'Trim',wood,.002)
            for xx in (x-.48,x+.48):me.box((xx,yy,(top-.038)/2),(.065,.20,top-.038),'Trim',wood,.001)
        # Under-30-inch deck: two open rails read as a modest owner addition.
        for sign in (-1,1):
            xx=x+sign*(w/2-.06)
            for yy in (y+.12,y+depth-.1):me.box((xx,yy,.94),(.089,.089,.92),'Trim',wood,.002)
            for zz in (.90,1.37):me.box((xx,y+depth/2,zz),(.064,depth-.2,.064),'Trim',wood,.002)
    me.finish()


def foyer(b):
    m=b.plan['blocks'][0];x=b.plan['door_x'];y=m.y0
    me=b.mesh('Shallow_Foyer',component='foyer');cream=(.43,.40,.34)
    me.box((x,y+1.02,.496),(2.25,1.98,.024),'Trim',(.22,.15,.09),r=0)
    for xx in (x-1.125,x+1.125):me.box((xx,y+1.02,1.82),(.09,2.04,2.63),'Trim',cream,r=0)
    me.box((x,y+2.0,1.82),(2.25,.09,2.63),'Trim',cream,r=0)
    me.box((x,y+1.0,3.13),(2.25,2.04,.08),'Trim',cream,r=0)
    for xx in (x-1.07,x+1.07):me.box((xx,y+1.02,.56),(.025,1.94,.10),r=.001)
    me.finish()


def chase(b):
    if not b.plan['spec']['fireplace']:return
    m=b.plan['blocks'][0];face='left' if b.plan['spec']['garage']['side']=='right' else 'right'
    xf,n,l=b.frame(m,face);u=l*.48;me=b.mesh('GasFireplace_Chase',component='fireplace')
    # Direct-vent, single-story chase: no new main-roof penetration.
    me.box((u,.23,.15),(1.2192,.46,.30),'Concrete',r=.003,xf=xf)
    me.box((u,.24,1.62),(1.2192,.48,2.64),'Siding',r=.002,xf=xf)
    me.prism([xf((u-.66,-.01,3.04)),xf((u+.66,-.01,3.04)),xf((u+.66,.55,2.96)),xf((u-.66,.55,2.96))],(0,0,-1),.025,'Trim',(.21,.23,.21))
    me.box((u,.495,1.82),(.24,.05,.24),'Trim',(.12,.14,.13),.005,xf)
    me.box((u,.54,1.83),(.18,.045,.13),'Trim',(.26,.28,.26),.003,xf)
    me.finish()


def gable_vent(b):
    g=b.plan['blocks'][1];xf,n,l=b.frame(g,'front');z=g.eave+g.pitch*g.width*.30
    me=b.mesh('Garage_OctagonalVent',component='gable_vent');vs=[]
    for radius,v in ((.255,.035),(.205,.052)):
        vs += [xf((l/2+radius*math.cos(a),v,z+radius*math.sin(a))) for a in [math.pi/8+i*math.pi/4 for i in range(8)]]
    me.geom(vs,[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)])
    me.geom(vs[8:],[tuple(range(8))],'Trim',(.17,.19,.17))
    for j in range(-3,4):
        zz=j*.045;ww=2*math.sqrt(max(0,.19**2-zz**2))
        me.box((l/2,.058,z+zz),(ww,.025,.017),r=.001,xf=xf)
    me.finish()


def build_additions(b):
    for o in b.openings:
        if o['kind'] in ('patio','service'):portal(b,o)
    rear_landing(b);foyer(b);chase(b);gable_vent(b)
