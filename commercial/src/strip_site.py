"""Strip parking, native commercial curb openings, walk and shared props."""
import hashlib
import math
import random
from pathlib import Path
import bpy
from geometry import *
from siteworks import flat,strip,curb_run
from ground_adapter import FLOW,CURB_TOP,STRIP,TRANSITION,cut_top,walk_z
from strip_plan import FT,transform
from strip_graphics import quad
from equipment import lightpole,dumpster_enclosure


def _south_street(p,parent):
    W,D=p['lot'];edge=-D/2;wing=5*FT
    stations={-W/2,W/2}
    for dr in p['driveways']:stations.update(dr['center'][0]+v for v in TRANSITION(dr['width']+2*wing,dr['width']))
    stations=sorted(stations)
    def top(u):return min((cut_top(u-dr['center'][0],dr['width']) for dr in p['driveways']),default=CURB_TOP)
    curb_run('Native public curb',[(u,edge-3.3528,top(u)) for u in stations],parent)
    for a,b in zip(stations,stations[1:]):
        mesh('Public sidewalk',[(a,edge-1.3716,walk_z(-1.3716)),(b,edge-1.3716,walk_z(-1.3716)),(b,edge+.1524,0),(a,edge+.1524,0)],[(0,1,2,3)],'Concrete',parent,False)
        if not any(abs((a+b)/2-dr['center'][0])<dr['width']/2+wing for dr in p['driveways']):
            flat('Public verge',(a,b,edge-3.2004,edge-1.3716),'Green',parent,CURB_TOP+.009)
    for u in [i*1.524-W/2 for i in range(round(W/1.524)+1)]:
        mesh('Public walk score',[(u-.002,edge-1.3716,walk_z(-1.3716)+.001),(u+.002,edge-1.3716,walk_z(-1.3716)+.001),(u+.002,edge+.1524,.001),(u-.002,edge+.1524,.001)],[(0,1,2,3)],'Trim',parent,False)
    for i,dr in enumerate(p['driveways']):
        dc=dr['center'][0];width=dr['width'];half=width/2;base=TRANSITION(width+2*wing,width)
        xs=(0,.6096,STRIP-.0254,STRIP-.0127,STRIP);verts=[];faces=[]
        for x in xs:
            t=x/STRIP;hh=half+wing*(1-t)
            for s in base:
                u=dc+s/(half+wing)*hh;z0=cut_top(u-dc,width);z=z0+(CURB_TOP-z0)*t
                verts.append((u,edge-3.2004+x,z))
        n=len(base)
        for j in range(len(xs)-1):
            for k in range(n-1):q=j*n+k;faces.append((q,q+1,q+1+n,q+n))
        mesh('Native commercial apron',verts,faces,'Concrete',parent,False)
        for side in (-1,1):
            vs=[]
            for x in xs:
                t=x/STRIP;inner=half+wing*(1-t)
                for u in (dc+side*inner,dc+side*(half+wing)):
                    z0=cut_top(u-dc,width);z=z0+(CURB_TOP-z0)*t+.002;vs.append((u,edge-3.2004+x,z))
            mesh('Apron turf wing',vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(4)],'Green',parent,False)
        for label,v,z in (('Drive',.1524,0),('GroundCurb',-3.3528,FLOW),('GroundApron',-3.2004,FLOW),('GroundWalk',-1.3716,FLOW)):
            socket(f"Socket_{label}_{dr.get('id',i+1)}",(dc,edge+v,z),parent,'ground_'+label.lower(),90)


def street(p,parent):
    south=[dict(dr,id=i+1) for i,dr in enumerate(p['driveways']) if dr['edge']=='south']
    _south_street({**p,'driveways':south},parent)
    if any(dr['edge']=='east' for dr in p['driveways']):
        W,D=p['lot'];east=[]
        for i,dr in enumerate(p['driveways']):
            if dr['edge']=='east':east.append(dict(dr,id=i+1,center=(dr['center'][1],-W/2)))
        rt=root('East public frontage',yaw=90,parent=parent)
        _south_street({**p,'lot':(D,W),'driveways':east},rt)


def walks(p,modules,parent):
    walk=p['walk'];front=p['building']['front']
    for m in p['modules']:
        rt=modules[m['id']];w=m['width'];cuts=[-w/2,w/2]
        if m.get('corner_walk_clip'):cuts.append(-w/2+walk)
        if not m['wing']:
            for a in p['access']:
                for q in (a['x0'],a['x1']):
                    xx=q-m['origin'][0]
                    if -w/2<xx<w/2:cuts.append(xx)
        cuts=sorted(set(cuts))
        for lo,hi in zip(cuts,cuts[1:]):
            if m.get('corner_walk_clip') and hi<=-w/2+walk+.001:continue
            mid=(lo+hi)/2+m['origin'][0]
            access=not m['wing'] and any(a['x0']<mid<a['x1'] for a in p['access'])
            if access:continue
            box('Bay covered walk',((lo+hi)/2,-walk/2,.0762),(hi-lo-.003,walk,.1524),'Concrete',rt,.002)
    for a in p['access']:
        x0,x1=a['x0'],a['x1'];y0=front-walk;y1=y0+a['ramp_run']
        mesh('Recessed accessible ramp',[(x0,y0,0),(x1,y0,0),(x1,y1,.1524),(x0,y1,.1524)],[(0,1,2,3)],'Concrete',parent,False)
        flat('Ramp level landing',(x0,x1,y1,front),'Concrete',parent,.1524)


def accessible_sign(p,s,parent,ink,layout):
    x=(s['x0']+s['x1'])/2;y=s['y1']-.22
    r=root('AccessibleSign',(x,y,0),kind='AccessibleSign',parent=parent)
    cylinder('Accessible post',(0,0,0),(0,0,2.25),.025,'Metal',r,10)
    panel('Accessible reserved panel',0,-.025,1.99,.37,.57,'White',r,.016)
    panel('ISA blue field',0,-.037,2.03,.30,.30,'Blue',r,.004)
    wheelchair_sign(r,0,-.044,2.01,.25)
    quad('Reserved parking text','RESERVED','sign',0,-.047,2.20,.32,.055,r,ink,layout)
    quad('Van text','VAN ACCESSIBLE','sign',0,-.047,1.77,.32,.045,r,ink,layout)


def site(p,modules,ink,layout):
    W,D=p['lot'];r=root('SitePaving',kind='SitePaving');r['reusable_module']=True
    # Terrain skins are split around actual islands and building. There is no
    # buried full rectangular asphalt sheet under the architecture or planting.
    excludes=[tuple(isl['bounds']) for isl in p['islands']]
    b=p['building'];excludes.append((b['left'],b['left']+b['width'],b['front'],b['rear']))
    if p['elbow']:
        inner=p['elbow']['bounds'][0];excludes.append((inner,inner+b['depth'],b['front']-2*p['modules'][0]['width'],b['front']))
    # Property edge beds occupy the last four feet, except street entries.
    east=next((dr for dr in p['driveways'] if dr['edge']=='east'),None)
    excludes.extend([(-W/2,-W/2+4*FT,-D/2,D/2),(W/2-4*FT,W/2,-D/2,D/2),(-W/2,W/2,D/2-4*FT,D/2)])
    if east:
        excludes.remove((W/2-4*FT,W/2,-D/2,D/2))
        ey=east['center'][1];half=east['width']/2+5*FT
        excludes.extend([(W/2-4*FT,W/2,-D/2,ey-half),(W/2-4*FT,W/2,ey+half,D/2)])
    xs=sorted({-W/2,W/2,*[q for e in excludes for q in e[:2]]});ys=sorted({-D/2,D/2,*[q for e in excludes for q in e[2:]]})
    for x0,x1 in zip(xs,xs[1:]):
        for y0,y1 in zip(ys,ys[1:]):
            if not any(a<(x0+x1)/2<c and d<(y0+y1)/2<e for a,c,d,e in excludes):flat('Lot asphalt',(x0,x1,y0,y1),'Asphalt',r)
    for bounds in ((-W/2,-W/2+4*FT,-D/2,D/2),(W/2-4*FT,W/2,-D/2,D/2),(-W/2+4*FT,W/2-4*FT,D/2-4*FT,D/2)):
        if east and bounds[0]>0:
            ey=east['center'][1];half=east['width']/2+5*FT
            for aa,bb in ((bounds[2],ey-half),(ey+half,bounds[3])):flat('Perimeter planted verge',(bounds[0],bounds[1],aa,bb),'Green',r,.009)
        else:flat('Perimeter planted verge',bounds,'Green',r,.009)
    for x in (-W/2+4*FT,W/2-4*FT):
        spans=[(-D/2,D/2)]
        if east and x>0:spans=[(-D/2,ey-half),(ey+half,D/2)]
        for aa,bb in spans:box('Private perimeter curb',(x,(aa+bb)/2,.06),(.14,bb-aa,.12),'Concrete',r,.004)
    box('Private rear curb',(0,D/2-4*FT,.06),(W-8*FT,.14,.12),'Concrete',r,.004)
    paint=set()
    for s in p['stalls']:
        for x in (s['x0'],s['x1']):paint.add((round(x,6),s['y0'],s['y1']))
        cy=s['y1']-.65 if s['facing']>0 else s['y0']+.65
        box('Concrete wheel stop',((s['x0']+s['x1'])/2,cy,.065),(1.65,.17,.13),'Concrete',r,.022)
        if s['accessible']:accessible_sign(p,s,r,ink,layout)
    for x,y0,y1 in sorted(paint):strip('Faded parking stripe',(x,y0),(x,y1),.10,'White',r)
    for a in p['access']:
        for x in (a['x0'],a['x1']):strip('Access stall boundary',(x,a['y0']),(x,a['y1']),.10,'White',r)
        for yy in [a['y0']+.25+j*.48 for j in range(11)]:strip('Access aisle hatching',(a['x0']+.06,yy),(a['x1']-.06,yy+.38),.07,'White',r)
    # Dispersed center-row islands break up the large field. Native low shrubs
    # are instanced after consolidation, never replaced with faceted spheres.
    for i,isl in enumerate(p['islands']):
        x0,x1,y0,y1=isl['bounds'];w=x1-x0;d=y1-y0
        rounded_slab('Island concrete curb',((x0+x1)/2,(y0+y1)/2,0),w,d,.1524,.37,'Concrete',r)
        flat('Island bark bed',(x0+.14,x1-.14,y0+.14,y1-.14),'Soil',r,.156)
        rng=random.Random(p['seed']*101+i)
        verts=[];faces=[]
        for j in range(45):
            x=rng.uniform(x0+.19,x1-.19);y=rng.uniform(y0+.19,y1-.19);a=rng.uniform(0,math.tau)
            le=rng.uniform(.06,.15);wi=rng.uniform(.015,.035);z=rng.uniform(.157,.176);n=len(verts)
            verts.extend([(x+dx*math.cos(a)-dy*math.sin(a),y+dx*math.sin(a)+dy*math.cos(a),z+dz) for dx,dy,dz in ((-le/2,-wi/2,0),(le/2,-wi/3,.003),(le/2,wi/2,0),(-le/2,wi/3,.004))]);faces.append((n,n+1,n+2,n+3))
        mesh('Original loose bark chips',verts,faces,'Soil',r,False)
    walks(p,modules,r);street(p,r)
    for i,isl in enumerate(p['islands']):
        if i%2:continue
        x0,x1,y0,y1=isl['bounds'];lightpole('LotPole_'+str(i),((x0+x1)/2,(y0+y1)/2,.155))
    # Service yard sits in the buffer between the left end and the side drive,
    # with its gates opening into a clear apron, not across the rear drive.
    enclosure=dumpster_enclosure((b['left']-2.75,b['rear']-3.1,0));enclosure.name='StripDumpsterEnclosure';enclosure['reusable_module']=True
    for ob in enclosure.children_recursive:
        if ob.get('pivot_axis'):ob.name='Strip_'+ob.name
    return r


def pylon(p,ink,layout):
    r=root('PylonSign',(*p['sign_center'],0),kind='PylonSign');r['reusable_module']=True
    # Capped masonry plinth, twin posts with flanges, a service cabinet and
    # separately replaceable tenant panels on both actual street-facing sides.
    box('Sign footing',(0,0,.16),(4.0,1.02,.32),'Concrete',r,.035,2)
    box('Pylon masonry base',(0,0,.58),(3.72,.84,.70),'Wall',r,.008)
    box('Pylon base cap',(0,0,.97),(3.86,.96,.09),'Concrete',r,.009)
    for x in (-1.35,1.35):
        box('Pylon steel post',(x,0,3.87),(.21,.21,5.78),'Trim',r,.008)
        box('Pylon base flange',(x,0,1.045),(.38,.38,.055),'Metal',r,.005)
        for dx in (-.13,.13):
            for dy in (-.13,.13):cylinder('Pylon anchor',(x+dx,dy,1.07),(x+dx,dy,1.115),.022,'Metal',r,8)
    box('Pylon cabinet',(0,0,4.27),(3.50,.40,5.68),'Trim',r,.035,2)
    occupants=list(dict.fromkeys(m['tenant'] for m in p['modules']))
    for side in (-1,1):
        face=root('Pylon face',(0,-side*.228,0),0 if side>0 else 180,parent=r)
        frame('Center sign extruded rim',0,0,6.42,3.51,1.05,'Metal',face,.045,.065)
        quad('Center name',p['center_name'],'sign',0,-.041,6.42,3.37,.91,face,ink,layout)
        for j,key in enumerate(occupants):
            z=5.57-j*.475
            panel('Tenant sign substrate',0,-.016,z,3.32,.445,'Trim' if layout[key]['style']=='channel' else 'White',face,.028)
            frame('Tenant panel extrusion',0,-.022,z,3.39,.465,'Metal',face,.022,.046)
            quad('Pylon tenant panel',key,'sign',0,-.051,z,3.28,.405,face,ink,layout)
            for x in (-1.62,1.62):cylinder('Panel screw',(x,-.054,z),(x,-.061,z),.009,'Metal',face,8)
    return r


def plant(p,world):
    source=Path('../shrubs/export/Shrubs.glb');before=set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=str(source.resolve()));added=set(bpy.context.scene.objects)-before
    stock=sorted((o for o in added if o.type=='MESH' and o.name.startswith('Boxwood')),key=lambda o:o.name)
    assert len(stock)==2
    if p.get('look'):
        mask=next(m for o in stock for m in o.data.materials if m.surface_render_method=='DITHERED')
        for o in stock:o.data.materials.clear();o.data.materials.append(mask)
    data=[(o.data,o.matrix_world.copy()) for o in stock]
    for o in added:bpy.data.objects.remove(o,do_unlink=True)
    r=root('Landscape',kind='Landscape',parent=world);r['reusable_module']=True
    rng=random.Random(p['seed']+7700);count=0
    for isl in p['islands']:
        x0,x1,y0,y1=isl['bounds']
        for t in (.20,.48,.79):
            x=(x0+x1)/2+rng.uniform(-.20,.20);y=y0+t*(y1-y0)
            rt=root(f'StripBoxwood_{count}',(x,y,.16),rng.uniform(0,360),parent=r)
            rt.scale=(.85,.85,.85)
            for j,(mesh,xf) in enumerate(data):
                ob=bpy.data.objects.new(f'StripBoxwood_{count}_{j}',mesh);bpy.context.collection.objects.link(ob);ob.parent=rt;ob.matrix_basis=xf
            count+=1
    return dict(source='shrubs/export/Shrubs.glb',sha256=hashlib.sha256(source.read_bytes()).hexdigest(),instances=count,unique_meshes=2,reused_gpu_mib=16)
