"""Church grammar assembly, additions, entrances and service construction."""
import math
import geometry as G
from architecture import roof,buttress,pierced_gable,tower
from windows import bay
from hardware import doors,rail


def wing(parent,name,point,size,modern=True):
    rt=G.root(name,point,parent,module_kind='EducationWing' if modern else 'ParishHall');w,l,h=size;t=.3048
    m=G.Mesh('Wing foundation roof and ends',rt,floor=.1524,patch=True)
    m.box((0,0,.15),(w+.12,l+.12,.30),'concrete')
    m.box((0,l/2,h/2),(w,t,h),'brick',(.98,1.05,1.14))
    for s in (-1,1):m.box((s*(w/2+1.12)/2,-l/2,h/2),(w/2-1.12,t,h),'brick',(.98,1.05,1.14))
    m.box((0,-l/2,(h+2.5)/2),(2.24,t,h-2.5),'brick',(.98,1.05,1.14))
    m.box((0,0,h+.04),(w+.35,l+.35,.17),'asphalt')
    for x in (-w/2-.11,w/2+.11):m.box((x,0,h+.20),(.19,l+.5,.17),'stone')
    for y in (-l/2-.11,l/2+.11):m.box((0,y,h+.20),(w+.5,.19,.17),'stone')
    m.finish()
    count=max(2,round(l/3.6576));pitch=l/count
    for side in (-1,1):
        for i in range(count):
            rr=G.root(name+' classroom bay '+str(side)+'_'+str(i),(side*w/2,-l/2+(i+.5)*pitch,0),rt,module_kind='ClassroomBay');rr.rotation_euler.z=side*math.pi/2
            m=G.Mesh('Pierced classroom wall',rr,patch=i==2,floor=.1524)
            for s in (-1,1):m.box((s*(pitch/2+1.25)/2,0,h/2),(pitch/2-1.25,t,h),'brick',(.98,1.05,1.14))
            m.box((0,0,.55),(2.5,t,1.1),'brick',(.98,1.05,1.14));m.box((0,0,(h+2.65)/2),(2.5,t,h-2.65),'brick',(.98,1.05,1.14))
            for z in (1.1,2.65):m.box((0,-.18,z),(2.64,.13,.10),'stone')
            for x in (-1.23,0,1.23):m.box((x,-.03,1.87),(.06,.10,1.50),'iron')
            m.box((0,-.04,2.10),(2.50,.08,.045),'iron');m.panel(0,.01,1.87,2.46,1.47,'glass')
            m.box((0,.21,1.87),(2.5,.05,1.50),'black');m.finish()
    doors(name+' exit',rt,(0,-l/2-.2,.1524),modern=True)
    return rt


def entrance(parent,p):
    y=p['tower_xy'][1]-4.57/2 if p['tower']=='center' else -p['length']/2;f=p['floor'];m=G.Mesh('Entrance landing and measured steps',parent,module_kind='Steps')
    m.box((0,y-1.17,f/2),(4.3,2.34,f),'stone')
    count=round(f/.1524)
    for i in range(count):
        z=(count-i)*.1524;yy=y-2.34-(i+.5)*.3302
        m.box((0,yy,z/2),(4.30,.3302,z),'stone')
    m.finish()
    for s in (-1,1):rail('Front stair rail',parent,(s*1.98,y-2.55,f),(s*1.98,y-2.34-count*.3302,.1524),True)
    # Side retrofit: top landing at the entry, run parallel to nave, generous
    # landing at grade. It connects to side doorway, independently of stairs.
    x=p['width']/2+2.6;start=-p['length']/2+.5*p['bay']+.9144;end=start+p['ramp']['run'];w=1.66
    rt=G.root('1996 accessible ramp',(x,start,0),parent,module_kind='Ramp')
    m=G.Mesh('Retrofit ramp and edge curbs',rt)
    m.prism([(-w/2,0,.6096),(-w/2,p['ramp']['run'],0),(-w/2,p['ramp']['run'],-.16),(-w/2,0,-.16)],(w,0,0),'concrete')
    m.box((0,-.9144,.2248),(w,1.8288,.7696),'concrete');m.box((0,p['ramp']['run']+.9144,-.08),(w,1.8288,.16),'concrete')
    for s in (-1,1):
        m.beam((s*w/2,0,.66),(s*w/2,p['ramp']['run'],.05),.075,.10,'concrete')
    # New concrete bridge meets a proper door aperture on the later hall.
    m.box((-1.7,-.9144,.5296),(1.9,1.8288,.16),'concrete');m.finish()
    for s in (-1,1):rail('Ramp handrail',rt,(s*.795,0,.6096),(s*.795,p['ramp']['run'],0),True)
    return rt


def services(parent,p):
    w=p['width'];l=p['length'];h=p['eave'];over=.61 if p['style']=='aframe' else .36
    edge_h=h-over*math.tan(math.radians(p['pitch']));m=G.Mesh('Rainwater goods and splash blocks',parent,module_kind='Drainage')
    for s in (-1,1):
        xx=s*(w/2+over+.04)
        # Open U trough, hemmed outside lip, outlet and supported offset pipe.
        m.box((xx,0,edge_h-.17),(.18,l+.5,.035),'copper')
        for sx in (-.09,.09):m.box((xx+sx,0,edge_h-.10),(.025,l+.5,.15),'copper')
        for yy in (-l/2+.4,l/2-.4):
            xp=s*(w/2+.10);pts=[(xx,yy,edge_h-.17),(xx,yy,edge_h-.54),(xp,yy,edge_h-.76),(xp,yy,.32),(xp+s*.2,yy,.16)]
            m.tube(pts,.058,'copper',10)
            for z in (1.0,3.5,6.3):
                if z<edge_h-.6:m.box((xp,yy,z),(.13,.15,.045),'iron')
            m.box((xp+s*.12,yy,.05),(.64,.40,.10),'concrete')
    m.finish();m=G.Mesh('Rear meters conduit and condensers',parent,module_kind='Services')
    face=l/2+(.125 if p['style']=='aframe' else 0);yy=face+.10
    for j in range(3):
        x=-3+j*.7;m.box((x,yy,1.25),(.40,.20,.63),'stone',(.7,.75,.74));m.tube([(x,yy,-.04),(x,yy,1.0)],.022,'iron',8)
        m.tube([(x,yy+.11,1.30),(x,yy+.18,1.30)],.115,'glass',16)
        m.box((x,yy+.107,1.30),(.17,.006,.17),'black')
        for z in (.30,.75):m.box((x,face+.05,z),(.08,.11,.035),'iron')
    for x in (-3.2,3.3):
        m.box((x,yy+1,.13),(1.5,1.2,.26),'concrete');m.box((x,yy+1,.78),(1.22,.95,1.06),'stone',(.65,.7,.69))
        for i in range(13):m.box((x-.54+i*.09,yy+.51,.78),(.022,.035,.90),'iron')
        m.tube([(x+.58,yy+1,.36),(x+.88,yy+1,.30),(x+.88,face-.05,.30)],.032,'iron',8)
    m.finish()


def rear_steps(parent,p):
    y=p['length']/2;f=p['floor'];count=round(f/.1524)
    rt=G.root('Rear exit landing',parent=parent,module_kind='RearSteps')
    m=G.Mesh('Rear exit filled landing and treads',rt)
    m.box((0,y+.90,(f-.12)/2),(3.20,1.80,f+.12),'concrete')
    for i in range(count):
        z=(count-i)*.1524;m.box((0,y+1.8+(i+.5)*.3302,(z-.12)/2),(3.20,.3302,z+.12),'concrete')
    m.finish()
    if count>1:
        for s in (-1,1):rail('Rear stair rail',rt,(s*1.45,y+1.6,f),(s*1.45,y+1.8+count*.3302,.1524),True)


def build(p):
    G.STYLE=p['style'];G.PLAN=p
    rt=G.root('Church_'+str(p['seed']),asset_set='Church',static_root=True,seed=p['seed'],style=p['style'])
    w=p['width'];l=p['length'];modern=p['style']=='aframe'
    if modern:
        for i in range(p['bays']+1):
            y=-l/2+i*p['bay'];m=G.Mesh('Laminated bent '+str(i),rt,module_kind='Bent')
            foot=(p['ridge']-.70-.15)/math.tan(math.radians(p['pitch']))
            for s in (-1,1):
                m.beam((s*foot,y,.15),(0,y,p['ridge']-.70),.62,.24,'timber')
                m.box((s*foot,y,.22),(.70,.76,.44),'stone')
            # Miter the bent against the actual roof underside at the ridge;
            # a square beam end otherwise pokes through the sloping covering.
            m.v=[(x,yy,min(z,p['ridge']-abs(x)*math.tan(math.radians(p['pitch']))-.13)) for x,yy,z in m.v]
            m.finish()
        for s in (-1,1):
            m=G.Mesh('Low brick sidewall '+str(s),rt,module_kind='LowWall',floor=.1524);m.box((s*(w-p['wall'])/2,0,p['eave']/2),(p['wall'],l,p['eave']),'brick',(.87,1.02,1.12));m.finish()
        from modern import glazed_end
        glazed_end(rt,p,-l/2);glazed_end(rt,p,l/2,True)
    else:
        for s in (-1,1):
            for i in range(p['bays']):
                point=(s*(w-p['wall'])/2,-l/2+(i+.5)*p['bay'],0)
                if s==1 and i==0:
                    from details import side_exit
                    side_exit(rt,p,point)
                else:
                    raised=s==1 and i>=p['bays']-3 and 'hall' in p['wings'] and p['style']!='chapel'
                    bay('Nave bay '+str(s)+'_'+str(i),rt,dict(p,raised_window=raised),point,s*90)
            if p['style']!='chapel':
                for i in range(p['bays']+1):buttress(rt,p,(s*w/2,-l/2+i*p['bay'],0),s*90)
        pierced_gable(rt,p,-l/2);pierced_gable(rt,p,l/2-p['wall'],True)
    roof(rt,p);tower(rt,p);services(rt,p);rear_steps(rt,p)
    if not modern:entrance(rt,p)
    from modern import additions
    additions(rt,p)
    from details import fittings
    fittings(rt,p)
    from weather import repairs
    repairs(rt,p)
    from maintenance import add as history
    history(rt,p)
    import bpy
    bpy.context.view_layer.update()
    points=[ob.matrix_world@v.co for ob in rt.children_recursive if ob.type=='MESH' for v in ob.data.vertices]
    center=[(min(q[k] for q in points)+max(q[k] for q in points))/2 for k in (0,1)]
    wrapper=G.root(rt.name+'_Footprint',asset_set='Church',static_root=True,seed=p['seed'],style=p['style'],nave_offset=[-center[0],-center[1],0])
    rt.parent=wrapper;rt.location=(-center[0],-center[1],0);p['placement_offset']=[*center,0]
    return wrapper
