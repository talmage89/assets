"""Two rental building grammars on the shared house construction vocabulary."""
import math
import random
from geometry import Assembly,Mesh,label,finish_local
from components import panel_wall,window,door,sliding,balcony,stairs,meters,rail,oriented,STEEL,ALUM
from plans import FT,transform


def roof(a,name,w,d,eave,kind,upper_openings=(),base=0,endcaps=(True,True),gallery=False):
    m=a.mesh(name,component='roof');o=.30;ox=.30 if all(endcaps) else 0
    if kind=='mansard':
        bottom=eave-2.25;top=eave+.25
        # Mansard apron on four sides with cut-out inset window/dormer wells.
        for front in (-1,1):
            holes=[q for q in upper_openings if q['side']==front]
            xs=sorted({-w/2-ox,w/2+ox,*[q['x']+s*(q['w']/2+.12) for q in holes for s in (-1,1)]})
            zs=sorted({bottom,top,*[max(bottom,min(top,q['z']+s*(q['h']/2+.09))) for q in holes for s in (-1,1)]})
            def yy(z):return front*(d/2+.47-.80*(z-bottom)/(top-bottom))
            for x0,x1 in zip(xs,xs[1:]):
                for z0,z1 in zip(zs,zs[1:]):
                    x,z=(x0+x1)/2,(z0+z1)/2
                    if gallery and front<0 and -w/2+.85<x<w/2-.85:continue
                    if any(abs(x-q['x'])<q['w']/2+.12-1e-6 and abs(z-q['z'])<q['h']/2+.09-1e-6 for q in holes):continue
                    m.prism([(x0,yy(z0),z0),(x1,yy(z0),z0),(x1,yy(z1),z1),(x0,yy(z1),z1)],(0,-front,0),.065,'Shingles')
            for q in ([] if gallery and front<0 else holes):
                # Dormer cheeks have real depth to the vertical window jamb.
                zl=max(bottom,q['z']-q['h']/2-.09);zh=min(top,q['z']+q['h']/2+.09)
                for sx in (-1,1):
                    xx=q['x']+sx*(q['w']/2+.12)
                    m.prism([(xx,yy(zl),zl),(xx,front*(d/2+.03),zl),(xx,front*(d/2+.03),zh),(xx,yy(zh),zh)],(-sx,0,0),.025,'Trim')
            if not (gallery and front<0):m.box((0,yy(bottom),bottom),(w+.65,.075,.10),'Trim',r=.002)
        for sx in (-1,1):
            if not endcaps[0 if sx<0 else 1]:continue
            m.prism([(sx*(w/2+.30),-d/2-.47,bottom),(sx*(w/2+.30),d/2+.47,bottom),(sx*(w/2-.20),d/2-.33,top),(sx*(w/2-.20),-d/2+.33,top)],(-sx,0,0),.06,'Shingles')
        m.box((0,0,top-.015),(w-(.40 if all(endcaps) else 0),d-.66,.08),'Shingles',(.055,.053,.045),r=0)
        m.box((0,0,top+.04),(w-(.28 if all(endcaps) else 0),d-.54,.06),'Trim',(.30,.27,.21),r=.002)
    else:
        pitch=5/12;ridge=eave+pitch*d/2
        for sy in (-1,1):
            if kind!='cross_gable':m.prism([(-w/2-ox,sy*(d/2+o),eave-o*pitch),(w/2+ox,sy*(d/2+o),eave-o*pitch),(w/2+ox,0,ridge),(-w/2-ox,0,ridge)],(0,0,-1),.09,'Shingles')
            m.box((0,sy*(d/2+o),eave-.13),(w+.65,.10,.21),'Trim',r=.002)
            # Open trough with a low front lip, not a solid fascia masquerading as gutter.
            m.box((0,sy*(d/2+o+.035),eave-.23),(w+.65,.15,.025),'Trim',r=.002)
            m.box((0,sy*(d/2+o+.11),eave-.17),(w+.65,.025,.15),'Trim',r=.001)
        if kind=='cross_gable':
            from geometry import H
            Block=H.roof_faces.__globals__['Block']
            main=Block('Main',-w/2-ox,w/2+ox,-d/2-o,d/2+o,0,0,0,eave-o*5/12,'gable',5/12,'X',0)
            cross=Block('Front',-w*.41,w*.28,-d/2-o,.4,0,0,0,eave-.05,'gable',1.55/(w*.345),'Y',0)
            for q in H.roof_faces([main,cross]):
                aa,bb,cc=q['plane'];m.prism([(x,y,aa*x+bb*y+cc) for x,y in q['polygon']],(0,0,-1),.09,'Shingles')
        for sx in (-1,1):
            if not endcaps[0 if sx<0 else 1]:continue
            m.prism([(sx*w/2,-d/2,eave),(sx*w/2,d/2,eave),(sx*w/2,0,ridge)],(-sx,0,0),.16,'Siding')
            for sy in (-1,1):m.beam((sx*(w/2+ox),sy*(d/2+o),eave-.04),(sx*(w/2+ox),0,ridge+.06),.12,.16,'Trim',r=.002)
            # Attic louver sits in the gable plane.
            for j in range(7):m.box((sx*(w/2+.008),0,eave+.48+j*.055),(.035,.65,.024),'Trim',(.26,.26,.23),r=0)
        m.tube([(-w/2-.29,0,ridge+.035),(w/2+.29,0,ridge+.035)],.065,'Shingles',sides=6)
    # Drainage boots and believable grouped roof vents.
    for x in (-w*.27,w*.26):
        z=(eave+.33 if kind=='mansard' else eave+5/12*d*.25)
        m.box((x,d*.25,z),(.30,.30,.035),'Trim',(.12,.12,.105),r=.002)
        m.tube([(x,d*.25,z),(x,d*.25,z+.38)],.048,'Trim',(.19,.19,.17),sides=10)
    m.finish()
    g=a.mesh(name+'_downspouts',component='services')
    for xx in (-w/2+.10,w/2-.10):
        for sy in (-1,1):
            y=sy*(d/2+.03)
            g.tube([(xx,y+sy*.27,eave-.20),(xx,y+sy*.27,eave-.60),(xx,y,eave-.80),(xx,y,base+.25),(xx,y+sy*.30,base+.13)],.038,'Trim',a.colors['Trim'],sides=6)
            for zz in (base+.7,eave-.9):g.box((xx,y,zz),(.10,.10,.022),'Trim',r=0)
    g.finish()


def services(a,w,d,base,count,seed,meters_count=None):
    meters(a,'Meter_bank',(w/2+.02,0,base),meters_count or count,yaw=90)
    m=a.mesh('Mechanical_services',component='services')
    for j in range(count):
        x=-w/2-.78;y=(j-(count-1)/2)*1.08
        m.box((x,y,.06),(1.05,.94,.12),'Concrete',r=.006)
        m.box((x,y,.43),(.73,.70,.74),'Trim',(.30,.31,.27),r=.025)
        for z in (.20,.32,.44,.56,.68):m.box((x,y-.355,z),(.65,.008,.019),'Trim',(.12,.14,.12),r=0)
        m.tube([(x,y,.81),(x,y,.83)],.26,'Trim',(.10,.115,.10),sides=16)
        # Refrigerant pair follows pad/wall and is strapped; no taut air wire.
        m.tube([(x+.37,y,.30),(x+.45,y,.18),(-w/2-.10,y,.18),(-w/2-.05,y,base+.60)],.028,'Trim',(.025,.03,.025),sides=6)
    m.finish()


def garden_module(p,parent,name,loc=(0,0,0),yaw=0,materials=None):
    c=p['color'];a=Assembly(name,dict(Siding=c['siding'],Veneer=c['brick'],Trim=c['trim'],Door=c['door']),parent,loc,yaw,materials)
    w,d,base,fh=p['width'],p['depth'],p['base'],p['floor_height'];core=p['core_width'];floors=p['floors']
    eave=base+floors*fh;upper=[];flights=[];wall_ac_count=0
    m=a.mesh('Foundation_and_floor_diaphagms',component='foundation')
    m.box((0,0,base-.10),(w,d,.20),'Concrete',r=.002)
    if base>0:m.box((0,0,base/2),(w,d,base),'Concrete',(.28,.27,.235),r=0)
    # Floor plates in unit zones only: common stairwell stays physically open.
    for f in range(1,floors):
        z=base+f*fh
        if p['access']=='breezeway':m.box((0,0,z-.13),(w,d,.254),'Concrete',r=0)
        else:
            for sx in (-1,1):m.box((sx*(core/4+w/4),0,z-.127),((w-core)/2,d,.254),'Concrete',r=0)
            # A 1.4 m bypass on the right connects both pairs of unit doors.
            m.box((core/2-.70,0,z-.127),(1.4,d,.254),'Concrete',r=0)
            m.box((0,-1.85,z-.127),(core,1.2192,.254),'Concrete',r=0)
            for lo,hi in ((-d/2,-1.24),(2.30,d/2)):
                m.box((-.70,(lo+hi)/2,z-.127),(core-1.4,hi-lo,.254),'Concrete',r=0)
    m.finish()
    unitwidth=p['unit_width']
    for sy in (-1,1):
        openings=[]
        for f in range(floors):
            z=base+f*fh
            if p['access']=='breezeway':
                centers=[-w/2+(j+.5)*unitwidth for j in range(4)]
            else:centers=[-(core/2+unitwidth/2),core/2+unitwidth/2]
            for j,x in enumerate(centers):
                sid=f'{f+1}{j+1 if sy<0 else j+3:02d}';number=f'{(f+1)*100+(j+1 if p["access"]=="breezeway" or sy<0 else j+3)}'
                front=p['access']=='breezeway' and sy<0
                # Breezeway entry and kitchen window; opposite living slider.
                if front:
                    q=dict(x=x-unitwidth*.28,w=.9652,h=2.09,z=z+1.045-base,kind='door');openings.append(q)
                    door(a,'Unit_'+number,(q['x'],-d/2-.014,z+.02),number=number,replaced=(f+j+p['seed'])%5==0)
                    wx=x+unitwidth*.22
                    openings.append(dict(x=wx,w=1.27,h=1.08,z=z+1.53-base,kind='window'))
                    window(a,'Kitchen_'+number,(wx,-d/2-.025,z+1.53),1.27,1.08,seed=p['seed']+f*7+j)
                else:
                    bx=x-unitwidth*.22;wx=x+unitwidth*.25;sw=1.8288
                    openings.extend([dict(x=bx,w=sw+.05,h=2.10,z=z+1.05-base,kind='slider'),dict(x=wx,w=1.5748,h=1.27,z=z+1.50-base,kind='window')])
                    pos=(bx,sy*(d/2+.025),z+1.016)
                    sliding(a,'Patio_'+number,pos,0 if sy<0 else 180,seed=p['seed']+f*9+j)
                    window(a,'Bedroom_'+number,(wx,sy*(d/2+.025),z+1.50),1.524,1.2192,0 if sy<0 else 180,seed=p['seed']+f*3+j,replacement=(j+f+p['seed'])%4==0)
                    if z>=0:balcony(a,'Balcony_'+number,bx,sy*d/2,z+.02,w=3.35,sign=sy,seed=p['seed']+f*4+j,support_base=(base+(f-1)*fh+.02 if f>1 else 0))
                    idx=f*4+j+(0 if p['access']=='breezeway' or sy<0 else 2)
                    if idx%3==0:
                        wall_ac_count+=1
                        ac=a.mesh('Through_wall_AC_'+number,component='air_conditioner')
                        ac.box((wx,sy*(d/2+.15),z+.65),(.70,.34,.44),'Trim',(.33,.32,.27),r=.008)
                        for jj in range(8):ac.box((wx,sy*(d/2+.326),z+.48+jj*.045),(.63,.014,.012),'Trim',(.11,.12,.10),r=0)
                        ac.finish()
                        openings.append(dict(x=wx,w=.72,h=.46,z=z+.65-base,kind='ac'))
            if p['access']!='breezeway':
                if p['access']=='enclosed':
                    openings.append(dict(x=0,w=1.27,h=2.14 if f==0 else 1.80,z=(1.07 if f==0 else f*fh+1.45),kind='hall'))
                    if f==0:
                        door(a,'Hall_entry_'+str(sy),(0,sy*(d/2+.025),max(.02,base)),0 if sy<0 else 180,width=1.2192,number='A')
                    else:window(a,'Hall_window_'+str(sy)+str(f),(0,sy*(d/2+.025),base+f*fh+1.45),1.22,1.75,0 if sy<0 else 180,seed=1)
                else:openings.append(dict(x=0,w=core-.20,h=fh-.18,z=f*fh+fh/2,kind='open_hall'))
        upper.extend(dict(x=q['x'],w=q['w'],h=q['h'],z=q['z']+base,side=sy) for q in openings if q['z']>(floors-1)*fh and q['kind']!='ac')
        # Back facade coordinates reverse X under its 180 degree rotation.
        os=[dict(q,x=q['x'] if sy<0 else -q['x']) for q in openings]
        panel_wall(a,'Facade_'+str(sy),w,floors*fh,(0,sy*d/2,base),0 if sy<0 else 180,os,p['skin'])
    # End-wall bedrooms and service bank, not blank slabs.
    for sx in (-1,1):
        os=[]
        for f in range(floors):
            for j,yy in enumerate((-d*.29,d*.29)):
                os.append(dict(x=yy,w=1.27,h=1.27,z=f*fh+1.50))
                window(a,f'End_{sx}_{f}_{j}',(sx*(w/2+.025),yy,base+f*fh+1.50),1.22,1.2192,90 if sx>0 else -90,seed=p['seed']+j+f)
        panel_wall(a,'End_wall_'+str(sx),d,floors*fh,(sx*w/2,0,base),90 if sx>0 else -90,os,p['skin'])
    if p['access']=='breezeway':
        # Continuous front access gallery with two separated exit stairs.
        m=a.mesh('Gallery',component='gallery')
        for f in range(floors):
            z=base+f*fh
            m.box((0,-d/2-.88,z-.09),(w,1.76,.18),'Concrete',r=.005)
            if f:
                # Exit stair landings interrupt the gallery guard, as built.
                left=-w/2+.90-width if False else -w/2+.90-.5588
                right=w/2-2.10-.5588
                for l,r in ((-w/2,left),(left+2.4352,right),(right+2.4352,w/2)):
                    if r-l>.05:rail(m,(l,-d/2-1.73,z),(r,-d/2-1.73,z))
        for xx in [(-w/2)+j*unitwidth for j in range(5)]:m.box((xx,-d/2-1.64,(base+(floors-1)*fh)/2),(.10,.10,base+(floors-1)*fh),'Trim',STEEL,r=.001)
        m.finish()
        for sx in (-1,1):
            flights+=stairs(a,'Exterior_stair_'+str(sx),(sx*(w/2-1.5)-.6,-d/2-3.10,base),fh,floors,reverse=True)
    else:
        flights=stairs(a,'Core_stairs',(-1.65,-1.10,base),fh,floors)
        # Lateral unit entrances open into the full-depth common hall.
        for sx in (-1,1):
            os=[]
            for f in range(floors):
                for j,yy in enumerate((-2.7432,2.7432)):
                    os.append(dict(x=yy,w=.9652,h=2.10,z=f*fh+1.05))
                    door(a,f'Unit_{sx}_{f}_{j}',(sx*core/2,yy,base+f*fh+.02),-90 if sx>0 else 90,number=str((f+1)*100+j*2+(1 if sx<0 else 2)))
            panel_wall(a,'Core_fire_separation_'+str(sx),d,floors*fh,(sx*core/2,0,base),90 if sx>0 else -90,os,'siding',thick=.1524)

    a.socket('Front_walk',(0,-d/2-(1.76 if p['access']=='breezeway' else .30),0));a.socket('Rear_walk',(0,d/2+.3,0),yaw=180)
    roof(a,'Roof',w,d,eave,p['roof'],upper,base,gallery=p['access']=='breezeway')
    services(a,w,d,base,p['units_per_module']-wall_ac_count,p['seed'],p['units_per_module'])
    from occupancy import add
    add(a,w,d,base,fh,p['seed'])
    # Partly sunken units get real areaways outside low sliding doors.
    if base<0:
        m=a.mesh('Sunken_areaways',component='foundation')
        for sx in (-1,1):
            for sy in (-1,1):
                x=sx*(core/2+unitwidth*.28);y=sy*(d/2+1)
                m.box((x,y,base-.06),(3.8,2.0,.12),'Concrete',r=0)
                for xx in (x-1.9,x+1.9):m.box((xx,y,base/2),(.15,2.1,-base+.10),'Concrete',r=.002)
                m.box((x,sy*(d/2+2),base/2),(3.8,.15,-base+.1),'Concrete',r=.002)
        m.finish()
    a.root['units']=p['units_per_module'];a.root['era']=p['era'];a.root['access']=p['access']
    a.root['footprint_m']=[w,d];a.root['floor_height_m']=fh
    a.root['stair_flights']=__import__('json').dumps(flights)
    return a


def garden_building(p,name='Garden',parent=None,loc=(0,0,0),yaw=0,materials=None):
    b=Assembly(name,parent=parent,loc=loc,yaw=yaw,materials=materials);b.root['building_kind']='garden';b.root['unit_count']=p['units']
    for j,q in enumerate(p['modules']):garden_module(p,b.root,name+'_Wing'+str(j+1),q['origin'],q['yaw'],b.materials)
    if len(p['modules'])>1:
        # A covered, open circulation link joins separate fire compartments.
        # It is intentionally a low canopy, below both independent wing roofs.
        m=b.mesh('Covered_wing_link',component='link');x=p['width']/2+.762-p['module_recenter_m'][0];y=p['depth']*.18-p['module_recenter_m'][1]
        m.box((x,y,.0762),(1.524,2.4384,.1524),'Concrete',r=.003)
        m.box((x,y,2.62),(1.80,2.70,.12),'Shingles',r=.003)
        for sx in (-1,1):
            for sy in (-1,1):m.box((x+sx*.67,y+sy*1.12,1.30),(.089,.089,2.60),'Trim',r=.002)
        m.finish();b.socket('Wing_link',(x,y,0),'walk')
    b.root['footprint_polygons_m']=__import__('json').dumps(p['footprint_polygons'])
    for j,poly in enumerate(p['footprint_polygons']):
        for k,point in enumerate(poly):b.socket(f'Footprint_{j}_{k}',point,'footprint_corner')
    b.socket('Footprint_origin',(0,0,0),'footprint');return b


def townhouse(p,name='Townhouses',parent=None,materials=None):
    c=p['color'];a=Assembly(name,dict(Siding=c['siding'],Veneer=c['brick'],Trim=c['trim'],Door=c['door']),parent=parent,materials=materials)
    a.root['building_kind']='row';a.root['unit_count']=p['count'];w,d,fh=p['width'],p['depth'],p['floor_height']
    for u in p['units']:
        i=u['index'];x,y,z=u['x'],u['y'],p['base']+u['z'];num=str(110+i*2)
        unit=Assembly(name+'_Unit'+str(i+1),a.colors,parent=a.root,loc=(x,y,u['z']),materials=a.materials)
        base=p['base'];h=2*fh;openings=[];upper=[]
        plinth=unit.mesh('Foundation',component='foundation')
        plinth.box((0,0,(base-u['z'])/2),(w,d,base+u['z']),'Concrete',(.26,.25,.22),r=.002)
        plinth.finish()
        dx=w*.29 if p['garage'] else -w*.29;wx=-w*.14 if p['garage'] else w*.14
        openings.append(dict(x=dx,w=.9652,h=2.10,z=1.05))
        if p['garage']:openings.append(dict(x=-w*.16,w=2.54,h=2.16,z=1.08))
        else:openings.append(dict(x=wx,w=2.1844,h=1.37,z=1.48))
        for xx in (-w*.26,w*.22):
            openings.append(dict(x=xx,w=1.27,h=1.37,z=fh+1.43))
            window(unit,f'Upper_{i}_{xx}',(xx,-d/2-.03,base+fh+1.43),1.22,1.32,seed=p['seed']+i,replacement=u['window_replaced'])
            upper.append(dict(x=xx,w=1.27,h=1.37,z=base+fh+1.43,side=-1))
        panel_wall(unit,'Front',w,h,(0,-d/2,base),0,openings,'brick' if p['skin']=='brick' else 'mixed' if p['skin']=='stone' else 'siding',band=.85 if p['skin']=='stone' else fh)
        door(unit,'Entry',(dx,-d/2-.025,base+.02),number=num,replaced=u['door_replaced'])
        if p['garage']:
            group=unit.root.name+'_Garage';hpanel=2.11/4
            for j in range(4):
                top=(-w*.16,-d/2+.55,base+(j+1)*hpanel)
                pivot=unit.pivot('Garage_panel_'+str(j+1),top)
                del pivot['pivot_axis'];del pivot['range_degrees']
                pivot['motion_kind']='sectional_track';pivot['garage_group']=group;pivot['section']=j+1
                pivot['section_height_m']=hpanel;pivot['track_radius_m']=.20;pivot['closed_top_m']=top
                m=unit.mesh('Garage_panel_mesh_'+str(j+1),part=pivot.name,component='garage_panel')
                # Reduced joint noses clear adjacent sections on the curved
                # guide; a full rectangular slab binds as the hinges fold.
                cy=-d/2+.55;lo=top[2]-hpanel;hi=top[2];xx=-w*.16-1.25
                profile=[(cy-.020,lo+.035),(cy-.003,lo+.005),(cy+.003,lo+.005),(cy+.020,lo+.035),
                         (cy+.020,hi-.035),(cy+.003,hi-.005),(cy-.003,hi-.005),(cy-.020,hi-.035)]
                m.prism([(xx,yy,zz) for yy,zz in profile],(1,0,0),2.50,'Trim',(.55,.55,.50))
                for xx in (-w*.16-.78,-w*.16,-w*.16+.78):m.box((xx,-d/2+.527,top[2]-hpanel/2),(.70,.012,.39),'Trim',(.49,.49,.45),r=.004)
                finish_local(m)
            m=unit.mesh('Garage_tracks_and_reveals',component='garage_frame')
            # Deep return jambs leave the curved guide entirely behind framing.
            for sx in (-1,1):
                xx=-w*.16+sx*1.285
                m.box((xx,-d/2+.35,base+1.08),(.035,.40,2.16),'Trim',r=.001)
                pts=[]
                from garage_motion import track
                for jj in range(40):
                    q=track(jj*4.5/39,2.11,.20);pts.append((xx,-d/2+.55+q.y,base+q.z))
                m.tube(pts,.012,'Trim',ALUM,sides=6)
                for yy in (-d/2+1.0,-d/2+2.7):m.box((xx,yy,base+2.53),(.025,.025,.30),'Trim',ALUM,r=0)
            m.box((0,0,base+fh-.127),(w,d,.254),'Concrete',(.25,.25,.23),r=0)
            m.finish()
        else:window(unit,'Living',(wx,-d/2-.025,base+1.48),2.1344,1.32,seed=p['seed']+i*3,replacement=u['window_replaced'])
        # Rear living slider and kitchen; upper two bedrooms.
        rear=[dict(x=-w*.20,w=1.89,h=2.10,z=1.05),dict(x=w*.29,w=1.02,h=1.10,z=1.55)]
        for xx in (-w*.26,w*.22):rear.append(dict(x=xx,w=1.27,h=1.37,z=fh+1.43))
        panel_wall(unit,'Rear',w,h,(0,d/2,base),180,[dict(q,x=-q['x']) for q in rear],'siding')
        sliding(unit,'Rear_slider',(-w*.20,d/2+.025,base+1.016),180,seed=p['seed']+i)
        for j,q in enumerate(rear[1:]):window(unit,'Rear_window_'+str(j),(q['x'],d/2+.025,base+q['z']),q['w']-.05,q['h']-.05,180,seed=i+j*3)
        # Stepped units expose actual narrow wall returns; interior party-wall
        # portions are skipped, with only the end units carrying full side walls.
        for sx in (-1,1):
            neighbor=i+sx
            if neighbor<0 or neighbor>=p['count']:panel_wall(unit,'Side_'+str(sx),d,h,(sx*w/2,0,base),90 if sx>0 else -90,[],'siding')
            else:
                other=p['units'][neighbor];off=other['y']-y
                if abs(off)>.001:
                    # Only uncovered front/rear strips, never a hidden full plate.
                    yy=-d/2+off/2 if off>0 else d/2+off/2
                    mm=unit.mesh('Exposed_party_return_'+str(sx),component='wall');mm.box((sx*w/2,yy,base+h/2),(.20,abs(off),h),'Siding',r=0);mm.finish()
        roof(unit,'Roof',w,d,base+h,p['roof'],upper,-u['z'],(i==0,i==p['count']-1))
        if p['roof']=='cross_gable':
            m=unit.mesh('Front_gable',component='roof');ridge=base+h+1.50
            m.prism([(-w*.41,-d/2-.18,base+h-.03),(w*.28,-d/2-.18,base+h-.03),(-w*.065,-d/2-.18,ridge)],(0,1,0),.13,'Siding')
            m.finish()
        if p['parapet'] and i<p['count']-1:
            m=unit.mesh('Raised_firewall',component='firewall');m.box((w/2,0,base+h+.36),(.20,d,.72),'Veneer',r=.001);m.box((w/2,0,base+h+.745),(.28,d+.10,.05),'Concrete',r=.001);m.finish()
        # Two/three riser stoops and rear patio, plus route/party-wall sockets.
        m=unit.mesh('Stoop_and_patio',component='site')
        total=base+u['z'];n=math.ceil(total/.1778)
        for j in range(n):
            height=total*(n-j)/n
            m.box((dx,-d/2-.47-j*.28,-u['z']+height/2),(1.35,1.10+j*.56,height),'Concrete',r=.003)
        for sx in (-1,1):rail(m,(dx+sx*.62,-d/2-.12,base),(dx+sx*.62,-d/2-1.12,.03),height=.9144,balusters=False)
        m.box((0,d/2+1.55,.055-u['z']),(w-.20,3.10,.11),'Concrete',r=.005)
        m.finish();balcony(unit,'Patio_contents',-w*.12,d/2,.15-u['z'],w=2.8,sign=1,seed=p['seed']+i)
        meters(unit,'Unit_meter',(-w*.42,-d/2-.12,-u['z']),1)
        m=unit.mesh('Mailbox_and_cart',component='services');m.box((dx-.67,-d/2-.16,1.18),(.27,.18,.34),'Trim',STEEL,r=.008)
        # Wheeled molded cart set on its wheels beside each door.
        cx=-w*.42;cy=-d/2-.65
        m.box((cx,cy,.48),(.47,.52,.75),'Trim',(.055,.09,.065),r=.035);m.box((cx,cy,.88),(.51,.57,.065),'Trim',(.035,.055,.04),r=.025)
        for sx in (-1,1):m.tube([(cx+sx*.22,cy+.18,.12),(cx+sx*.27,cy+.18,.12)],.10,'Trim',(.018,.02,.016),sides=10)
        m.v=[(xx,yy,zz-u['z']) for xx,yy,zz in m.v];m.finish()
        for sx in (-1,1):
            unit.socket('Party_wall_'+str(sx),(sx*w/2,0,0),'party_wall')
            for sy in (-1,1):unit.socket(f'Party_wall_{sx}_end_{sy}',(sx*w/2,sy*d/2,0),'party_wall_endpoint')
        unit.socket('Front_walk',(dx,-d/2-1.45,0));unit.socket('Rear_patio',(0,d/2+3.1,0),'patio')
    return a
