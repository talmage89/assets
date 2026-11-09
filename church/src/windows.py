"""True masonry apertures, voussoirs, storm frames and vented art glass."""
import math
import geometry as G


def crown(x,r,kind):
    return math.sqrt(max(0,r*r-x*x)) if kind=='round' else math.sqrt(max(0,4*r*r-(abs(x)+r)**2))


def outline(r,stem,kind='pointed',n=16,bottom=0):
    return [(-r,bottom),(r,bottom),*[(r-2*r*i/n,stem+crown(r-2*r*i/n,r,kind)) for i in range(n+1)]]


def ring(m,outer,inner,y,depth,role='stone'):
    for i in range(len(outer)):
        j=(i+1)%len(outer);poly=[(outer[i][0],y,outer[i][1]),(outer[j][0],y,outer[j][1]),(inner[j][0],y,inner[j][1]),(inner[i][0],y,inner[i][1])]
        m.prism(poly,(0,depth,0),role)


def window(name,parent,width=1.7,stem=2.8,sill=2.5,kind='pointed',point=(0,0,0),yaw=0,storm=True):
    rt=G.root(name,point,parent,module_kind='Window',opening_width=width)
    r=width/2;outer=outline(r+.12,stem,kind,bottom=-.12);inner=outline(r,stem,kind)
    m=G.Mesh('Cast surrounds',rt);ring(m,outer,inner,-.34,.28)
    # Sloping stone sill overhangs reveal; underside lip is a separate molding.
    m.prism([(-r-.18,-.46,-.15),(r+.18,-.46,-.15),(r+.18,-.05,-.08),(-r-.18,-.05,-.08)],(0,0,-.12),'stone');m.finish()
    m=G.Mesh('Window frame and tracery',rt)
    ring(m,outline(r-.015,stem-.015,kind,bottom=.015),outline(r-.07,stem-.03,kind,bottom=.07),-.16,.065,'iron')
    m.box((0,-.145,stem*.48),(.05,.06,stem-.09),'iron')
    for z in (.78,1.6,2.4):
        if z<stem:m.box((0,-.15,z),(width-.12,.04,.027),'iron')
    # Paired lancet tracery carries only the silhouette. Fine leading is map detail.
    for s in (-1,1):
        rr=(r-.1)/2;cx=s*(rr+.025)
        pts=[(cx-rr+2*rr*i/12,-.17,stem-.15+crown(-rr+2*rr*i/12,rr,kind)) for i in range(13)]
        m.tube(pts,.022,'stone',6)
    m.finish()
    m=G.Mesh('Stained glass',rt,sheet=True)
    poly=outline(r-.075,stem-.035,kind,bottom=.075)
    h=max(z for x,z in poly);uv=[[(.004+(x/r/2+.5)*.492,.004+z/h*.492) for x,z in poly]]
    m.geom([(x,-.10,z) for x,z in poly],[tuple(range(len(poly)))],'stained',uv=uv);m.finish()
    if storm:
        m=G.Mesh('1990s protective glazing',rt,sheet=True)
        # Outside protective sheet held off art glass; 20mm breathing slots
        # remain at sill/head. The tinted polymer is deliberately not emissive.
        poly=outline(r-.045,stem-.03,kind,bottom=.035)
        m.geom([(x,-.245,z) for x,z in poly],[tuple(range(len(poly)))],'glass');m.finish()
        m=G.Mesh('Storm bars vents and screws',rt)
        ring(m,outline(r,stem,kind,bottom=0),outline(r-.035,stem-.025,kind,bottom=.035),-.275,.035,'iron')
        for z in (stem*.42,stem*.82):m.box((0,-.269,z),(width,.035,.024),'iron')
        for x in (-r+.065,r-.065):
            for z in (.15,stem/2,stem):m.tube([(x,-.285,z),(x,-.268,z)],.007,'bronze',6)
        m.finish()
    rt.location.z+=sill;rt.rotation_euler.z=math.radians(yaw)
    return rt


def bay(name,parent,p,point,yaw,kind=None):
    kind=kind or ('round' if p['style']=='romanesque' else 'pointed')
    rt=G.root(name,point,parent,module_kind='WallBay');rt.rotation_euler.z=math.radians(yaw)
    w=p['bay'];t=p['wall'];h=p['eave'];r=.60 if p['style']=='chapel' else .70;stem=1.55 if p['style']=='chapel' else 3.10;sill=1.35 if p['style']=='chapel' else 2.30
    if p.get('raised_window'):
        # A later hall closes the lower light, retaining the original head.
        sill=4.75;stem=.65
    m=G.Mesh('Masonry pierced bay',rt,floor=p['floor'],drips=[-r,r],drip_z=sill,patch=name.endswith('2'))
    for x in (-1,1):m.box((x*(w/2+r)/2,0,h/2),((w/2-r),t,h),'brick')
    m.box((0,0,sill/2),(2*r,t,sill),'brick')
    xs=[-r+2*r*i/16 for i in range(17)]
    for a,b in zip(xs,xs[1:]):
        za=sill+stem+crown(a,r,kind);zb=sill+stem+crown(b,r,kind)
        m.prism([(a,-t/2,za),(b,-t/2,zb),(b,-t/2,h),(a,-t/2,h)],(0,t,0),'brick')
    m.box((0,-t/2-.04,.37),(w,.08,.32),'stone');m.box((0,-t/2-.045,h-.14),(w,.10,.18),'stone')
    m.finish();window('Lancet',rt,r*2,stem,sill,kind,point=(0,.105,0))
    return rt


def rose(name,parent,point,r=1.45):
    rt=G.root(name,point,parent,module_kind='Rose');m=G.Mesh('Rose masonry and mullions',rt)
    for a,b in ((r,r+.20),(r-.12,r)):
        outer=[(b*math.sin(k*math.tau/48),b*math.cos(k*math.tau/48)) for k in range(48)]
        inner=[(a*math.sin(k*math.tau/48),a*math.cos(k*math.tau/48)) for k in range(48)]
        ring(m,outer,inner,-.2,.28)
    for k in range(12):
        a=k*math.tau/12;m.beam((.28*math.sin(a),-.24,.28*math.cos(a)),((r-.1)*math.sin(a),-.24,(r-.1)*math.cos(a)),.062,.11,'stone')
    m.finish();m=G.Mesh('Rose art glass',rt,sheet=True)
    pts=[((r-.08)*math.sin(k*math.tau/48),-.03,(r-.08)*math.cos(k*math.tau/48)) for k in range(48)]
    m.geom(pts,[tuple(range(48))],'stained',uv=[[(.75+x/(r*4),.75+z/(r*4)) for x,y,z in pts]]);m.finish()
    return rt
