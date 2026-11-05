"""Twenty maintained years, localized to traffic, wet joints and hand work.

The commercial family's accumulated deposits supply the shared swatches.
Wear moves with each physical leaf, and no overlay crosses a drainage hole.
"""
import math,random
import bpy
from geometry import *
from age import decal,ribbon
from strip_graphics import quad


def add(p,modules,ink,layout):
    rng=random.Random(p['seed']+8891);b=p['building'];causes=[]
    r=root('ServiceWear',kind='SitePaving');r['reusable_module']=True
    for i,s in enumerate(p['stalls']):
        x=(s['x0']+s['x1'])/2;y=(s['y0']+s['y1'])/2+s['facing']*.65
        # Many accumulated drops and a softer standing band, scaled to a
        # parked car, all retained in the original shared deposit artwork.
        decal('Stall engine accumulated oil',(x,y,.0035),rng.uniform(1.65,2.05),rng.uniform(3.4,4.1),'Oil'+str(i%4),r,rng.uniform(-8,8))
        causes.append(dict(cause='parked engine leaks',center=(x,y),row=s['row']))
    # Cars follow each double-loaded aisle, with two wheel paths in each
    # travel direction. Their centers are not painted as a black road stripe.
    for j,y in enumerate(p['aisle_centers']):
        left=p['rows'][j*2]['x0'];right=p['rows'][j*2]['x1']
        for lane in (-1,1):
            for wheel in (-1,1):
                pts=[(left+(right-left)*i/45,y+lane*1.45+wheel*.78+.08*math.sin(i*.31+j)) for i in range(46)]
                ob=ribbon('Drive aisle polished wheel contact',pts,.22,r,mat='White',z=.0037);ob['wear_cell']='Tire';ob['swept_wear']=True
    for dr in p['driveways']:
        x,y=dr['center'];east=dr['edge']=='east'
        for lane in (-1,1):
            pts=[]
            for i in range(16):
                t=i/15;u=lane*.79+1.7*t*t;v=1+t*8.0
                pts.append((x-v,y+u) if east else (x+u,y+v))
            ob=ribbon('Entry turning wheel contact',pts,.30,r,mat='White',z=.0038);ob['wear_cell']='Tire';ob['swept_wear']=True
    # Repairs follow a buried service run alongside the right circulation
    # drive. Sealant follows irregular cracks through the old wearing course.
    x=p['side_drive_centers'][1]-2.5;y0=-p['lot'][1]/2+5;y1=b['rear']
    ob=mesh('Repaired utility trench',[(x,y0,.002),(x+.68,y0,.002),(x+.68,y1,.002),(x,y1,.002)],[(0,1,2,3)],'Asphalt',r,False);ob['repair']=True
    for xx in (x,x+.68):ribbon('Sawcut trench seal',[(xx,y0),(xx,y1)],.034,r,mat='Black')
    for j in range(8):
        y=p['aisle_centers'][j%len(p['aisle_centers'])]+rng.uniform(-2.3,2.3);xx=rng.uniform(p['rows'][0]['x0'],p['rows'][0]['x1']-8)
        pts=[(xx+i*.8,y+.18*math.sin(i*.87+j)+rng.uniform(-.08,.08)) for i in range(11)]
        ribbon('Routed and sealed asphalt crack',pts,.025,r,mat='Black',z=.004)
        q=pts[5];ribbon('Sealant branch',[q,(q[0]+.27,q[1]+.52),(q[0]+1.3,q[1]+.79)],.021,r,mat='Black',z=.004)
    for j in range(11):
        s=p['stalls'][(j*17+p['seed'])%len(p['stalls'])];x=(s['x0']+s['x1'])/2;y=(s['y0']+s['y1'])/2
        ww=rng.uniform(1.2,2.2);hh=rng.uniform(1.0,2.5)
        ob=mesh('Repaired parking wearing course',[(x-ww/2,y-hh/2,.0023),(x+ww/2,y-hh/2+.08,.0023),(x+ww/2-.11,y+hh/2,.0023),(x-ww/2+.06,y+hh/2-.04,.0023)],[(0,1,2,3)],'Asphalt',r,False);ob['repair']=True
    for m in p['modules']:
        rt=modules[m['id']];w=m['width'];dx=-w*.23;rr=bpy.data.objects[m['id']+'_Rear']
        decal('Door footfall grime',(dx,-.65,.1536),3.3,.98,'WalkGrime',rt)
        decal('Walk traffic retained grit',(dx+.35,-.80,.1538),2.7,.65,'WalkTrack',rt)
        for i in range(14):
            gx=dx+rng.uniform(-.75,.75);gy=-rng.uniform(.18,1.95)
            if not m['wing'] and gy<-1.19 and any(a['x0']-.06<gx+m['origin'][0]<a['x1']+.06 for a in p['access']):continue
            decal('Threshold chewing gum',(gx,gy,.1534),rng.uniform(.025,.055),rng.uniform(.025,.050),'Gum',rt,rng.uniform(0,360))
        for i in range(max(1,math.ceil(w/2.4384))):
            x=-w/2+.20+i*2.4384;length=rng.uniform(.52,.85)
            ob=decal('Coping joint wash',(x,-.004,b['parapet']-.07-length/2),rng.uniform(.18,.31),length,'Grime',rt,vertical=True);ob['wear_flip']=rng.random()>.5
            ob=decal('Rear coping joint wash',(x,-.105,b['parapet']-.07-length/2),rng.uniform(.16,.26),length,'Grime',rr,vertical=True);ob['wear_flip']=rng.random()>.5
            if p['style']!='mansard':decal('Canopy seam retained runoff',(x,-p['walk']-.094,3.43),rng.uniform(.20,.38),.31,'Grime',rt,vertical=True)
        # Salts follow wet rough masonry at grade, with isolated stronger
        # deposits near piers and rain leaders instead of a uniform ring.
        for x in (-w/2+.18,w/2-.18):
            decal('Pier low damp salts',(x,-.234,.45),.26,.44,'Salt',rt,vertical=True)
        for xx,zz,ww,hh in ((w*.20,2.64,.50,.56),(-w*.28,3.65,.62,1.10)):
            decal('Rear fixture rain and soot stain',(xx,-.105,zz),ww,hh,'Grime',rr,vertical=True)
        for j in range(4):
            xx=-w/2+.65+j*w/4
            decal('Rear CMU splash dirt',(xx,-.105,.35),rng.uniform(.65,1.18),rng.uniform(.24,.48),'WalkGrime',rr,vertical=True)
        # Overhead utility run avoids the full service-door swing and has real clips.
        cylinder('Rear gas distribution main',(-w/2,-.28,2.53),(w/2,-.28,2.53),.022,'Metal',rr,8)
        for xx in (-w*.33,w*.33):box('Gas main wall clip',(xx,-.20,2.53),(.045,.17,.065),'Trim',rr,0)
        x=-w*.28
        decal('Rain leader splash salts',(x,-.105,.34),.68,.38,'Salt',rr,vertical=True)
        leaf=bpy.data.objects[m['id']+'_ServiceDoor']
        decal('Service door bottom corrosion',(.495,-.024,.10),.96,.19,'Rust',leaf,vertical=True)
        decal('Service kick abrasion',(.50,-.024,.38),.76,.40,'Scuff',leaf,vertical=True)
        if m['tenant']=='vacant':quad('Removed tenant letter ghost','Ghost','sign',0,-.004,4.38,w-.95,.82,rt,ink,layout)
        causes.append(dict(module=m['id'],cause='threshold gum/grit; coping and canopy joints; rain leader salts; wet steel-leaf bottom'))
    # Gates receive deposits at their lower folded hem and hinge feet.
    for ob in list(bpy.context.scene.objects):
        if not ob.get('pivot_axis') or 'Gate' not in ob.name:continue
        direction=1 if ob.name.endswith('-1') else -1
        for i in range(17):decal('Dumpster gate wet bottom corrosion',(direction*(.07+i*.111),-.0625,.14),.087,.20,'Rust',ob,vertical=True)
    p['weather_causes']=causes
