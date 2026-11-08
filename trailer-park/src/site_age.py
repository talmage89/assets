"""Service-history overlays using Ground's accepted maps, seeded per site."""
import math,random
from terrain import decal,mesh


def road(a,p,lib,material):
    trim=material(lib,'GroundTrim');r=random.Random(p['seed']+1371);old=p['kind']=='old'
    w,span=p['street_width'],p['span'];m=a.mesh('CrackSeals',component='street_age')
    def seal(points,width):
        for (x,y),(xx,yy) in zip(points,points[1:]):
            d=math.hypot(xx-x,yy-y);nx,ny=-(yy-y)/d*width,(xx-x)/d*width
            m.geom([(x+nx,y+ny,.0175),(x-nx,y-ny,.0175),(xx-nx,yy-ny,.0175),(xx+nx,yy+ny,.0175)],[(0,1,2,3)],'Trim',(.017,.018,.016))
    for lane in (-p['loop_x'],p['loop_x']):
        # Longitudinal fatigue seal; offset from the centerline oil drips.
        points=[(lane-.85+r.uniform(-.32,.32),-span/2+1+j*1.5) for j in range(math.floor((span-2)/1.5)+1)]
        seal(points,.018 if old else .012)
        for j in range(math.ceil(span/7)):
            y=-span/2+3+j*7+r.uniform(-1,1)
            branch=[(lane-.85,y),(lane+.25,y+.4),(lane+w/2-.10,y+1.0)]
            seal(branch,r.uniform(.012,.029) if old else r.uniform(.009,.019))
            if j%3!=1:
                decal(a.root,'Settled service-cut patch',(lane+r.uniform(-1.1,1.1),y+2),(r.uniform(.7,1.5),r.uniform(1.0,2.5)),trim,(.25,.25,.5,.5),r.uniform(-8,8),p['seed'],z=.019)
            decal(a.root,'Centerline traffic oil',(lane+r.uniform(-.3,.3),y-1.5),(r.uniform(.75,1.4),r.uniform(1.2,2.5)),trim,(.5,.5,.75,.75),r.uniform(-15,15),p['seed'],z=.020)
        for side in (-1,1):
            for j in range(math.ceil(span/3.3)):
                y=-span/2+(j+.5)*3.3
                decal(a.root,'Raveled asphalt shoulder',(lane+side*(w/2-.12),y),(.38,3.5),trim,(0,.5,.5,.75),0 if side>0 else 180,p['seed'],z=.0205)
                decal(a.root,'Washed shoulder gravel',(lane+side*(w/2+.12),y),(.42,3.4),trim,(.5,.25,1,.5),90*side,p['seed'],z=.006)
            # Dirt fingers cover the damaged edge, exposing an irregular
            # asphalt silhouette without widening the nominal lane.
            vs=[];fs=[]
            for j in range(math.ceil(span/.65)+1):
                y=-span/2+j*span/math.ceil(span/.65);depth=r.uniform(.03,.25) if old else r.uniform(.02,.13)
                vs.extend([(lane+side*(w/2-depth),y,.0165),(lane+side*(w/2+.32),y,.002)])
                if j:k=(j-1)*2;f=(k,k+2,k+3,k+1);fs.append(tuple(reversed(f)) if side>0 else f)
            earth=mesh(a.root,'Eroded shoulder dirt',vs,fs,material(lib,'Concrete'),.72)
            for c in earth.data.color_attributes.active_color.data:c.color=(.28,.23,.14,1)
    ob=m.finish()
    for poly in ob.data.polygons:
        if poly.normal.z<0:poly.flip()
    ob.data.update()


def pad(a,p,lib,material):
    trim=material(lib,'GroundTrim');r=random.Random(p['occupant_seed']+610);L,W=p['length'],p['width'];old=p['era']!='1996'
    # Wheel-loaded concrete has narrow actual fissures as well as old infills.
    n=10 if p.get('corner_apron') else 4 if old else 2
    for j in range(n):
        if p.get('corner_apron'):x,y=-L*.45+j*L*.09,-W/2-2.3+r.uniform(-1,1)
        else:x,y=L/2+r.uniform(.4,4.7),-1.1+r.uniform(-.65,.65)
        decal(a.root,'Concrete shrinkage and settlement',(x,y),(r.uniform(.65,1.4),r.uniform(1.3,2.6)),trim,(.5,0,.625,.25),r.uniform(-85,85),p['occupant_seed'],z=.018 if not p.get('corner_apron') else .006)
    if old:
        for j in range(2):
            x,y=(L*.15+j*2.7,-W/2-2.3) if p.get('corner_apron') else (L/2+1.2+j*1.7,-1+r.uniform(-.45,.45))
            decal(a.root,'Old concrete repair',(x,y),(r.uniform(.5,1.1),r.uniform(.7,1.3)),trim,(.25,.25,.5,.5),r.uniform(-8,8),p['occupant_seed'],z=.019 if not p.get('corner_apron') else .007)


def soil(a,p,lib,material):
    from ground_edges import edges
    r=random.Random(p['occupant_seed']+374);L,W=p['length'],p['width'];old=p['era']!='1996';paths=[]
    concrete=material(lib,'Concrete')
    # Roof rain/splash and lack of sun kill the sward beside skirting.
    # Separate narrow lobes, plus traffic-scuffed drive margins.
    for j in range(7 if old else 3):
        x=-L*.45+(j+.5)*L/(7 if old else 3);length=r.uniform(.7,2.0);y=-W/2-.08
        if p.get('corner_apron'):continue
        near=.04;far=r.uniform(.24,.65) if old else r.uniform(.18,.32)
        pts=[(x-length/2,y-near,.001),(x-length*.12,y-near,.001),(x+length/2,y-near,.001),
             (x+length*.40,y-far*.55,.001),(x+length*.12,y-far,.001),(x-length*.32,y-far*.78,.001)]
        ob=mesh(a.root,'Bare soil under skirt runoff',pts,[(0,5,4,3,2,1)],concrete,.65)
        for c in ob.data.color_attributes.active_color.data:c.color=(r.uniform(.24,.33),.23,.12,1)
        paths.append([(x-length*.32,y-far*.78,.001),(x+length*.12,y-far,.001),(x+length*.40,y-far*.55,.001)])
    for j in range(3 if old else 1):
        x=L/2+1+j*1.4;y=-2.72;length=r.uniform(.7,1.4)
        pts=[(x-length/2,y+.15,.001),(x+length/2,y+.15,.001),(x+length*.40,y-.15,.001),(x-length*.25,y-.32,.001)]
        ob=mesh(a.root,'Drive-edge worn soil',pts,[(0,3,2,1)],concrete,.72)
        for c in ob.data.color_attributes.active_color.data:c.color=(.33,.27,.16,1)
        paths.append([(x-length*.25,y-.32,.001),(x+length*.40,y-.15,.001)])
    if paths:edges(a.root,paths,p['occupant_seed']+922,lib)
