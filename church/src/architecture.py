"""Load-bearing masonry and timber building envelopes."""
import math
import geometry as G
from windows import bay,rose,ring,outline,window,crown
from hardware import doors,rail,bell,bearing


def buttress(parent,p,point,yaw=0):
    rt=G.root('Stepped buttress',point,parent,module_kind='Buttress');rt.rotation_euler.z=math.radians(yaw)
    m=G.Mesh('Brick stages and stone weatherings',rt,floor=p['floor'])
    for bottom,top,d in ((0,2.4,1.15),(2.4,5.5,.88),(5.5,p['eave']-.25,.59)):
        m.box((0,-d/2,(top+bottom)/2),(.62,d,top-bottom-.13),'brick')
        m.prism([(-.37,-d-.04,top-.13),(.37,-d-.04,top-.13),(.37,.04,top+.04),(-.37,.04,top+.04)],(0,0,-.14),'stone')
    m.box((0,-.56,.17),(.85,1.32,.34),'stone');m.finish();return rt


def roof(parent,p):
    rt=G.root('Nave roof',parent=parent,module_kind='Roof');w=p['width'];l=p['length'];e=p['eave'];ridge=p['ridge'];over=.61 if p['style']=='aframe' else .36
    for side in (-1,1):
        for i in range(p['bays']):
            m=G.Mesh('Roof panel '+str(side)+'_'+str(i),rt)
            y0=-l/2+i*p['bay']-(over if i==0 else 0);y1=-l/2+(i+1)*p['bay']+(over if i==p['bays']-1 else 0)
            xx=side*(w/2+over);zz=e-over*math.tan(math.radians(p['pitch']))
            m.prism([(0,y0,ridge),(xx,y0,zz),(xx,y1,zz),(0,y1,ridge)],(0,0,-.13),'shingle' if p['style'] in ('aframe','chapel') else 'slate')
            m.finish()
    m=G.Mesh('Roof ridge caps and rake edges',rt)
    m.beam((0,-l/2-over,ridge+.02),(0,l/2+over,ridge+.02),.16,.13,'copper')
    for yy in (-l/2-over,l/2+over):
        for s in (-1,1):m.beam((s*(w/2+over),yy,e-over*math.tan(math.radians(p['pitch']))),(0,yy,ridge),.14,.22,'timber' if p['style']=='aframe' else 'stone')
    m.finish();return rt


def pierced_gable(parent,p,y,back=False):
    w=p['width'];h=p['eave'];peak=p['ridge'];t=p['wall'];r=1.38;cz=h+.35
    m=G.Mesh('Front rose gable' if not back else 'Rear gable',parent,module_kind='Gable',floor=p['floor'])
    poly=[(-w/2,3.0),(w/2,3.0),(w/2,h),(0,peak),(-w/2,h)]
    angles=sorted(set([k*math.tau/64 for k in range(64)]+[math.atan2(z-cz,x)%math.tau for x,z in poly]))
    inner=[];outer=[]
    def cross(a,b):return a[0]*b[1]-a[1]*b[0]
    for a in angles:
        d=(math.cos(a),math.sin(a));hits=[]
        for aa,bb in zip(poly,poly[1:]+poly[:1]):
            q=(aa[0],aa[1]-cz);v=(bb[0]-aa[0],bb[1]-aa[1]);den=cross(d,v)
            if abs(den)<1e-10:continue
            lam=cross(q,v)/den;s=cross(q,d)/den
            if lam>0 and -1e-7<=s<=1+1e-7:hits.append(lam)
        rr=min(hits);outer.append((d[0]*rr,cz+d[1]*rr));inner.append((d[0]*r,cz+d[1]*r))
    ring(m,outer,inner,y,t,'brick')
    # Door gap below the rose-bearing wall; full depth returns at either side.
    for s in (-1,1):m.box((s*(w/2+1.12)/2,y+t/2,1.5),(w/2-1.12,t,3.0),'brick')
    m.finish();rose('Front rose' if not back else 'Rear rose',parent,(0,y-.06,cz),r)
    if not back:
        if p['tower']!='center':
            doors('Front doors',parent,(0,y-.12,p['floor']))
            portal(parent,p,y)
    else:doors('Rear exit',parent,(0,y+t+.12,p['floor']),180)


def portal(parent,p,y):
    """Three rebated archivolts, jointed stones and a recessed tympanum."""
    f=p['floor'];rt=G.root('Gothic entry portal',(0,y,f),parent,module_kind='Portal')
    kind='round' if p['style']=='romanesque' else 'pointed';m=G.Mesh('Portal archivolts and hood',rt)
    for k in range(3):
        r=1.13+k*.13;stem=2.18
        ring(m,outline(r+.12,stem,kind,bottom=0),outline(r,stem,kind,bottom=0),-.25-k*.10,.13,'stone')
    outer=outline(1.66,2.18,kind,bottom=0);inner=outline(1.60,2.18,kind,bottom=0)
    ring(m,outer,inner,-.60,.10,'stone')
    for s in (-1,1):
        m.box((s*1.50,-.39,1.08),(.30,.36,2.16),'stone');m.box((s*1.50,-.42,.15),(.48,.44,.30),'stone')
        m.box((s*1.50,-.43,2.13),(.44,.42,.15),'stone')
    # Dark timber tympanum seats behind the archivolts above the square leaves.
    poly=[(-1.11,-.20,2.18),(1.11,-.20,2.18),*[(1.11-2.22*i/20,-.20,2.18+crown(1.11-2.22*i/20,1.11,kind)) for i in range(21)]]
    m.prism(poly,(0,.08,0),'timber',(.19,.15,.12))
    m.box((0,-.32,3.04),(.075,.06,.70),'bronze');m.box((0,-.32,3.14),(.40,.06,.075),'bronze')
    # Bed and radial joints terminate at the actual arch profile.
    for i in range(1,20):
        x=-1.57+3.14*i/20;z=2.18+crown(x,1.57,kind)
        m.tube([(x,-.615,z-.05),(x*1.055,-.615,z+.11)],.006,'iron',4)
    m.finish()


def tower(parent,p):
    if p['tower']=='none':return
    xx,yy=p['tower_xy'];modern=p['tower']=='freestanding';w=3.30 if modern else 4.57
    rt=G.root('Campanile' if modern else 'Masonry tower',(xx,yy,0),parent,module_kind='Tower')
    if modern:
        m=G.Mesh('Steel bell frame',rt)
        for x in (-w/2,w/2):
            for y in (-.72,.72):
                m.box((x,y,6.5),(.18,.18,13),'iron');m.box((x,y,.16),(.54,.54,.32),'concrete')
        for z in (4.3,8.5,12.8):
            for y in (-.72,.72):m.beam((-w/2,y,z-3.9),(w/2,y,z),.06,.06,'iron')
        m.box((0,0,11.35),(w,.26,.22),'iron');m.box((0,0,13.0),(w+.36,1.9,.15),'stone')
        for x in (-.75,.75):bearing(m,x,10.45,True)
        m.finish();bell(rt,(0,0,10.45));height=13
    else:
        # Hollow tower shaft, separate corner piers, actual belfry openings.
        m=G.Mesh('Tower shaft',rt,floor=p['floor']);shaft=12.95
        for k in range(4):
            face=G.root('Tower aperture face '+str(k),(0,0,0),rt);face.rotation_euler.z=k*math.pi/2
            mm=G.Mesh('Pierced tower shaft '+str(k),face,floor=p['floor'])
            rr=.44;stem=1.20;sill=7.3;doorway=p['tower']=='center' and k in (0,2);kind='round' if p['style']=='romanesque' else 'pointed'
            for s in (-1,1):
                if doorway:
                    mm.box((s*(w/2+1.12)/2,-w/2+.23,1.5),(w/2-1.12,.46,3),'brick')
                    mm.box((s*(w/2+rr)/2,-w/2+.23,(shaft+3)/2),(w/2-rr,.46,shaft-3),'brick')
                else:mm.box((s*(w/2+rr)/2,-w/2+.23,shaft/2),(w/2-rr,.46,shaft),'brick')
            mm.box((0,-w/2+.23,(sill+(3 if doorway else 0))/2),(rr*2,.46,sill-(3 if doorway else 0)),'brick')
            xs=[-rr+2*rr*i/12 for i in range(13)]
            for a,b in zip(xs,xs[1:]):
                aa=sill+stem+crown(a,rr,kind);bb=sill+stem+crown(b,rr,kind)
                mm.prism([(a,-w/2,aa),(b,-w/2,bb),(b,-w/2,shaft),(a,-w/2,shaft)],(0,.46,0),'brick')
            mm.finish();window('Tower lancet',face,rr*2,stem,sill,kind,point=(0,-w/2+.26,0),storm=False)
        for z in (.28,5.0,12.85,17.35):m.box((0,0,z),(w+.18,w+.18,.22),'stone')
        m.finish()
        for k in range(4):
            side=G.root('Belfry side '+str(k),parent=rt,module_kind='BelfryBay');side.rotation_euler.z=k*math.pi/2
            m=G.Mesh('Belfry piers and arch',side)
            for s in (-1,1):m.box((s*(w/2-.40),-w/2+.23,15.15),(.80,.46,4.45),'brick')
            r=1.28;stem=2.45;inner=outline(r,stem,'round',bottom=0);outer=outline(r+.21,stem,'round',bottom=-.15)
            ring(m,[(x,z+13) for x,z in outer],[(x,z+13) for x,z in inner],-w/2-.04,.36,'stone')
            m.box((0,-w/2+.23,17.15),(w-.8,.46,.40),'brick')
            for i in range(13):
                z=13.25+i*.235;hw=min(r-.05,math.sqrt(max(0,r*r-max(0,z-15.45)**2)))
                m.prism([(-hw,-w/2-.02,z),(hw,-w/2-.02,z),(hw,-w/2+.24,z+.11),(-hw,-w/2+.24,z+.11)],(0,0,-.035),'iron')
            m.finish()
        m=G.Mesh('Bell beams and bearings',rt)
        for x in (-.75,.75):
            m.box((x,0,15.30),(.18,w-.2,.24),'timber');bearing(m,x,15.53)
        m.finish();bell(rt,(0,0,15.53));height=17.65
        if p['tower']=='center':
            doors('Tower front doors',rt,(0,-w/2-.12,p['floor']));portal(rt,p,-w/2)
            m=G.Mesh('Tower passage floor and neck',rt)
            m.box((0,0,p['floor']-.10),(w-.6,w+.65,.20),'stone')
            for s in (-1,1):m.box((s*1.24,w/2+.16,1.5),(.24,.40,3.0),'brick')
            m.box((0,w/2+.16,3.10),(2.72,.40,.20),'stone');m.finish()
    cap=G.Mesh('Tower top',rt)
    if p['top']=='spire':
        rings=[]
        for z,r in ((height,w*.75),(height+.65,w*.67),(height+9.1,.04)):
            rings.append([(r*math.cos(k*math.tau/8+math.pi/8),r*math.sin(k*math.tau/8+math.pi/8),z) for k in range(8)])
        cap.loft(rings,'slate');height+=9.2
    elif p['top']=='belfry':
        for s in (-1,1):
            for k in range(5):
                x=-w/2+k*w/4;cap.box((x,s*w/2,height+.45),(.46,.48,.9),'stone');cap.box((s*w/2,x,height+.45),(.48,.46,.9),'stone')
    cap.box((0,0,height+.95),(.10,.10,2.30),'iron');cap.box((0,0,height+1.55),(1.1,.10,.10),'iron');cap.finish()
    return rt
