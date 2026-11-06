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
    stain_sites=[]
    for i,s in enumerate(p['stalls']):
        x=(s['x0']+s['x1'])/2;y=(s['y0']+s['y1'])/2+s['facing']*.65
        # Preserve the accepted RNG sequence for all subsequent rear wear.
        width=rng.uniform(1.65,2.05);length=rng.uniform(3.4,4.1);angle=math.radians(rng.uniform(-8,8))
        strength=.50+.50*((i*73+p['seed']*19)%101)/100
        stain_sites.append((x,y,width/2,length/2,math.cos(angle),math.sin(angle),strength))
        causes.append(dict(cause='absorbed parked-engine oil in wearing-course COLOR_0',center=(x,y),row=s['row']))
    # Absorbed floor deposits belong to the actual asphalt surface. Separate
    # alpha films reflected the sky at a walking eye and turned dark oil pale.
    # Preserve entry-turn causes as field samples, with no floating ribbon mesh.
    entry_paths=[]
    for dr in p['driveways']:
        x,y=dr['center'];east=dr['edge']=='east'
        for lane in (-1,1):
            for i in range(16):
                t=i/15;u=lane*.79+1.7*t*t;v=1+t*8.0
                entry_paths.append((x-v,y+u) if east else (x+v,y-u) if dr['edge']=='west' else (x+u,y+v))
    p['pavement_entry_paths']=entry_paths;p['pavement_stain_sites']=stain_sites
    # Repairs follow a buried service run alongside the right circulation
    # drive. Sealant follows irregular cracks through the old wearing course.
    x=p['side_drive_centers'][1]-2.5;y0=-p['lot'][1]/2+5;y1=b['rear']
    ob=mesh('Repaired utility trench',[(x,y0,.002),(x+.68,y0,.002),(x+.68,y1,.002),(x,y1,.002)],[(0,1,2,3)],'Asphalt',r,False);ob['repair']=True
    for xx in (x,x+.68):
        seal=ribbon('Sawcut trench seal',[(xx,y0),(xx,y1)],.055,r,mat='Black');seal['asphalt_seal']=True
    for j in range(8):
        y=p['aisle_centers'][j%len(p['aisle_centers'])]+rng.uniform(-2.3,2.3);xx=rng.uniform(p['rows'][0]['x0'],p['rows'][0]['x1']-8)
        if j<2:y=p['aisle_centers'][0]+1.6-j*.3;xx=p['rows'][0]['x0']+7+j*13
        pts=[(xx+i*.8,y+.18*math.sin(i*.87+j)+rng.uniform(-.08,.08)) for i in range(11)]
        seal=ribbon('Routed and sealed asphalt crack',pts,.055,r,mat='Black',z=.004);seal['asphalt_seal']=True
        q=pts[5];seal=ribbon('Sealant branch',[q,(q[0]+.27,q[1]+.52),(q[0]+1.3,q[1]+.79)],.045,r,mat='Black',z=.004);seal['asphalt_seal']=True
    for j in range(11):
        s=p['stalls'][(j*17+p['seed'])%len(p['stalls'])];x=(s['x0']+s['x1'])/2;y=(s['y0']+s['y1'])/2
        ww=rng.uniform(1.2,2.2);hh=rng.uniform(1.0,2.5)
        if j<2:
            # Exposed aisle utility repairs remain visible beyond parked cars.
            x=p['rows'][0]['x0']+9+j*13;y=p['aisle_centers'][0]+.6-j*.9;ww=2.3;hh=3.8
        ob=mesh('Repaired parking wearing course',[(x-ww/2,y-hh/2,.0023),(x+ww/2,y-hh/2+.08,.0023),(x+ww/2-.11,y+hh/2,.0023),(x-ww/2+.06,y+hh/2-.04,.0023)],[(0,1,2,3)],'Asphalt',r,False);ob['repair']=True
    for m in p['modules']:
        rt=modules[m['id']];w=m['width'];dx=-w*.23;rr=bpy.data.objects[m['id']+'_Rear']
        foot=decal('Door footfall grime',(dx,-.65,.1536),4.5,1.60,'WalkGrime',rt)
        track=decal('Walk traffic retained grit',(dx+.35,-.95,.1538),2.7,1.10,'WalkTrack',rt)
        # The level walk ends 1.2192 m from the glazing at access ramps.
        # Deposit quads stop on that surface, rather than bridging its slope.
        for mark in (foot,track):
            for v in mark.data.vertices:v.co.y=max(v.co.y,-1.18-mark.location.y)
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
