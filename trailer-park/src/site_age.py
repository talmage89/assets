"""Service-history overlays using Ground's accepted maps, seeded per site."""
import math,random
from terrain import decal,mesh


def road(a,p,lib,material):
    from soil_finish import material as soil_material
    trim=material(lib,'GroundTrim');r=random.Random(p['seed']+1371);old=p['kind']=='old'
    w,span=p['street_width'],p['span'];m=a.mesh('CrackSeals',component='street_age')
    seal_rng=random.Random(p['seed']+18171)
    def seal(points,width):
        smooth=[]
        for j in range(len(points)-1):
            a0,a1,a2,a3=points[max(0,j-1)],points[j],points[j+1],points[min(len(points)-1,j+2)]
            for k in range(7):
                t=k/7;smooth.append(tuple(.5*(2*a1[axis]+(-a0[axis]+a2[axis])*t+(2*a0[axis]-5*a1[axis]+4*a2[axis]-a3[axis])*t*t+(-a0[axis]+3*a1[axis]-3*a2[axis]+a3[axis])*t**3) for axis in (0,1)))
        smooth.append(points[-1]);vs=[];fs=[];colors=[]
        for j,(x,y) in enumerate(smooth):
            before=smooth[max(0,j-1)];after=smooth[min(len(smooth)-1,j+1)];dx,dy=after[0]-before[0],after[1]-before[1];d=math.hypot(dx,dy)
            # 2–4in overband, applicator wander, irregular squeeze-out and
            # cooler tar at the margins. Each edge has independent width.
            wobble=seal_rng.uniform(-.016,.016);x+=-dy/d*wobble;y+=dx/d*wobble
            half=width*seal_rng.uniform(.72,1.28);nx,ny=-dy/d*half,dx/d*half
            asym=seal_rng.uniform(.70,1.30)
            vs.extend([(x+nx,y+ny,.017),(x,y,.019),(x-nx*asym,y-ny*asym,.017)])
            colors.extend([(.009,.009,.008,1),(.004,.004,.004,1),(.009,.009,.008,1)])
            if j:
                k=(j-1)*3;fs.extend([(k,k+3,k+4,k+1),(k+1,k+4,k+5,k+2)])
        m.geom(vs,fs,'Trim');m.col[-len(colors):]=colors
    for lane in (-p['loop_x'],p['loop_x']):
        # Longitudinal fatigue seal; offset from the centerline oil drips.
        points=[(lane-.85+r.uniform(-.32,.32),-span/2+1+j*1.5) for j in range(math.floor((span-2)/1.5)+1)]
        for start in range(0,len(points)-3,7):
            if r.random()<(.92 if old else .68):seal(points[start:min(start+r.randint(5,8),len(points))],.039 if old else .030)
        for j in range(math.ceil(span/7)):
            y=-span/2+3+j*7+r.uniform(-2.4,2.4)
            branch=[(lane-.85,y),(lane+.25,y+.4),(lane+w/2-.10,y+1.0)]
            if old or r.random()<.58:seal(branch,r.uniform(.030,.045) if old else r.uniform(.026,.037))
            # Branches leave the principal fatigue crack, with short unfilled
            # ends; own RNG leaves accepted oil and service patch placements.
            if seal_rng.random()<.72:
                bx,by=branch[1];sign=seal_rng.choice((-1,1))
                seal([(bx,by),(bx+sign*.35,by+.42),(bx+sign*.72,by+.64)],.030)
            if j%3!=1:
                decal(a.root,'Settled service-cut patch',(lane+r.uniform(-1.1,1.1),y+2),(r.uniform(.7,1.5),r.uniform(1.0,2.5)),trim,(.25,.25,.5,.5),r.uniform(-8,8),p['seed'],z=.019)
            variant=r.randrange(3);rect=(.5+variant/12,.5,.5+(variant+1)/12,.75)
            decal(a.root,'Centerline traffic oil',(lane+r.uniform(-.45,.45),y-1.5),(r.uniform(.35,.75),r.uniform(.55,1.3)),trim,rect,r.uniform(-35,35),p['seed'],z=.020)
        for side in (-1,1):
            if old:
                # Connected irregular cells near loaded, unsupported margins.
                for station in range(math.ceil(span/8)):
                    cy=-span/2+3+station*8;cx=lane+side*(w/2-.45)
                    for cell in range(5):
                        yy=cy+cell*.24;dx=seal_rng.uniform(-.10,.10)
                        seal([(cx-.20+dx,yy),(cx+.02,yy+.07),(cx+.20+dx,yy+.29)],.004)
                        seal([(cx+.02,yy+.07),(cx-.05,yy+.28)],.003)
            for j in range(math.ceil(span/3.3)):
                y=-span/2+(j+.5)*3.3
                decal(a.root,'Raveled asphalt shoulder',(lane+side*(w/2-.12),y),(.38,3.5),trim,(0,.5,.5,.75),0 if side>0 else 180,p['seed'],z=.0205)
                decal(a.root,'Washed shoulder gravel',(lane+side*(w/2+.12),y),(.42,3.4),trim,(.5,.25,1,.5),90*side,p['seed'],z=.006)
            # Dirt fingers cover the damaged edge, exposing an irregular
            # asphalt silhouette without widening the nominal lane.
            vs=[];fs=[];opacity=[]
            for j in range(math.ceil(span/.65)+1):
                y=-span/2+j*span/math.ceil(span/.65);depth=r.uniform(.03,.25) if old else r.uniform(.02,.13)
                outer=r.uniform(.15,.48);amount=0 if j%17 in (0,1,2) else .70+.25*math.sin(j*.63)**2
                from terrain import sward_height
                xs=[lane+side*q for q in (w/2-depth,w/2-.012,w/2+outer*.45,w/2+outer)]
                vs.extend([(xs[0],y,.0165),(xs[1],y,.0165),(xs[2],y,sward_height(xs[2],y)+.004),(xs[3],y,sward_height(xs[3],y)+.004)])
                opacity.extend([0,amount,amount*.65,0])
                if j:
                    k=(j-1)*4
                    for column in range(3):
                        f=(k+column,k+column+4,k+column+5,k+column+1);fs.append(tuple(reversed(f)) if side>0 else f)
            earth=mesh(a.root,'Eroded shoulder dirt',vs,fs,soil_material(material(lib,'Concrete')),.72)
            for c,alpha in zip(earth.data.color_attributes.active_color.data,opacity):c.color=(.28,.23,.14,alpha)
    ob=m.finish()
    for poly in ob.data.polygons:
        if poly.normal.z<0:poly.flip()
    ob.data.update()


def road_tone(ob,tint,seed):
    """Wheel lanes retain binder; exposed loose margins oxidize lighter."""
    import bmesh
    bm=bmesh.new();bm.from_mesh(ob.data)
    lo=min(v.co.y for v in bm.verts);hi=max(v.co.y for v in bm.verts);half=max(abs(v.co.x) for v in bm.verts)
    if hi-lo<10:bm.free();return
    for axis,values in ((1,[lo+j*(hi-lo)/math.ceil((hi-lo)/.65) for j in range(1,math.ceil((hi-lo)/.65))]),(0,[-half*.70,-half*.45,0,half*.45,half*.70])):
        for value in values:
            co=[0,0,0];n=[0,0,0];co[axis]=value;n[axis]=1
            bmesh.ops.bisect_plane(bm,geom=[*bm.verts,*bm.edges,*bm.faces],plane_co=co,plane_no=n,dist=1e-6)
    # Recede the actual asphalt edge between isolated intact stations. Width
    # remains the nominal maximum; the boundary is physically broken.
    for v in bm.verts:
        if abs(v.co.x)>half-.0001 and lo+.01<v.co.y<hi-.01:
            t=v.co.y
            inset=.02+.12*(.5+.5*math.sin(t*5.71+seed))*math.sin(t*2.19+seed*.3)**2
            v.co.x-=math.copysign(inset,v.co.x)
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    for attr in ob.data.color_attributes:
        if attr.domain!='POINT':continue
        for row,v in zip(attr.data,ob.data.vertices):
            x,y=v.co.x,v.co.y;track=math.exp(-((abs(x)-half*.48)/.43)**2)
            factor=1+.16*(abs(x)/half)**3-.08*track+.035*math.sin(y*.17+seed)
            row.color=(*(c*factor for c in tint),1)


def pad(a,p,lib,material):
    trim=material(lib,'GroundTrim');r=random.Random(p['occupant_seed']+610);L,W=p['length'],p['width'];old=p['era']!='1996'
    # Wheel-loaded concrete has narrow actual fissures as well as old infills.
    n=10 if p.get('corner_apron') else 4 if old else 2
    for j in range(n):
        if p.get('corner_apron'):x,y=-L*.45+j*L*.09,-6.9+r.uniform(-.35,.35)
        else:x,y=L/2+r.uniform(.4,4.7),-1.1+r.uniform(-.65,.65)
        decal(a.root,'Concrete shrinkage and settlement',(x,y),(r.uniform(.65,1.4),r.uniform(1.3,2.6)),trim,(.5,0,.625,.25),r.uniform(-85,85),p['occupant_seed'],z=.018 if not p.get('corner_apron') else .006)
    if old:
        for j in range(2):
            x,y=(L*.08+j*2.7,-6.7-j*.32) if p.get('corner_apron') else (L/2+1.2+j*1.7,-1+r.uniform(-.45,.45))
            decal(a.root,'Old concrete repair',(x,y),(r.uniform(.9,1.5),r.uniform(1.1,1.6)),trim,(.25,.25,.5,.5),r.uniform(-8,8),p['occupant_seed'],z=.019 if not p.get('corner_apron') else .007)


def soil(a,p,lib,material,record):
    from ground_edges import edges
    from terrain import sward_height
    from soil_finish import material as soil_material,patch
    r=random.Random(p['occupant_seed']+374);L,W=p['length'],p['width'];old=p['era']!='1996';paths=[]
    concrete=soil_material(material(lib,'Concrete'))
    angle=math.radians(record['yaw']);cs,sn=math.cos(angle),math.sin(angle)
    def grade(x,y):
        xx=record['origin'][0]+cs*x-sn*y;yy=record['origin'][1]+sn*x+cs*y
        return sward_height(xx,yy)+.0015
    def ground(ob):
        for v in ob.data.vertices:v.co.z=grade(v.co.x,v.co.y)
        ob.data.update()
    # Roof rain/splash and lack of sun kill the sward beside skirting.
    # Separate narrow lobes, plus traffic-scuffed drive margins.
    for j in range(7 if old else 3):
        x=-L*.45+(j+.5)*L/(7 if old else 3);length=r.uniform(.7,2.0);y=-W/2-.08
        if p.get('corner_apron'):continue
        near=.04;far=r.uniform(.24,.65) if old else r.uniform(.18,.32)
        pts=[(x-length/2,y-near,.001),(x-length*.12,y-near,.001),(x+length/2,y-near,.001),
             (x+length*.40,y-far*.55,.001),(x+length*.12,y-far,.001),(x-length*.32,y-far*.78,.001)]
        ob=patch(a.root,'Bare soil under skirt runoff',list(reversed(pts)),concrete,(r.uniform(.24,.33),.23,.12),.65)
        ground(ob)
        paths.append([(x-length*.32,y-far*.78,.001),(x+length*.12,y-far,.001),(x+length*.40,y-far*.55,.001)])
    for j in range(3 if old else 1):
        x=L/2+1+j*1.4;y=-2.72;length=r.uniform(.7,1.4)
        pts=[(x-length/2,y+.22,.001),(x+length/2,y+.22,.001),(x+length*.40,y-.48,.001),(x-length*.25,y-.72,.001)]
        ob=patch(a.root,'Drive-edge worn soil',list(reversed(pts)),concrete,(.33,.27,.16),.72)
        ground(ob)
        paths.append([(x-length*.25,y-.72,.001),(x+length*.40,y-.48,.001)])
    if p['upkeep']!='kept' or p['occupant_seed']%4==0:
        # Turning toward the mailbox compacts the unpaved side of the drive.
        x=L/2+2.2;y=1.2;length=r.uniform(1.0,2.0) if old else .85
        pts=[(x-length*.6,y-.65,.001),(x+length*.4,y-.52,.001),(x+length*.6,y-.10,.001),
             (x+length*.38,y+.55,.001),(x-length*.25,y+.65,.001),(x-length*.62,y+.08,.001)]
        ob=patch(a.root,'Dry compacted mailbox approach',pts,concrete,(r.uniform(.42,.58),.38,.19),.7);ground(ob)
        paths.append([pts[3],pts[4],pts[5]])
    paths=[[(x,y,grade(x,y)) for x,y,z in path] for path in paths]
    if paths:edges(a.root,paths,p['occupant_seed']+922,lib)
