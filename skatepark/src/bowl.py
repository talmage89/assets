"""Sixteen snap sectors, a graded floor and a fitted deck surround.

Kidney boundary is an original analytic plan. Normal-offset circular sections
have 8ft radii with 4ft/7ft ends and a sloping waterfall between them. Block
coping and 6-inch tile band are construction geometry at this form gate.
"""
import math
import bmesh
from geometry import *
R=2.4384
SEGMENTS=320
BANDS=32
SECTORS=16
BX=9.144
BY=7.3152
SHAPE='kidney'

from contour import rim_xy,normal_xy

def rim(t):return Vector((*rim_xy(t,SHAPE),0))
def outward(t):return Vector((*normal_xy(t,SHAPE),0))
def depth(t):
    if SHAPE=='clover':
        # Put the shallow/deep sections in actual pockets, rather than making
        # the clover's waist its shallowest station. Control stations are on
        # the construction sampling grid; the three pockets ease into one another.
        t=t%math.tau;nodes=[(0,2.1336),(math.pi*.75,1.2192),(math.pi*1.25,1.6764),(math.tau,2.1336)]
        for (a,z0),(b,z1) in zip(nodes,nodes[1:]):
            if t<=b:return z0+(z1-z0)*(.5-.5*math.cos(math.pi*(t-a)/(b-a)))
    return 1.6764+.4572*math.cos(t)
def station(t,u):
    h=depth(t);theta=math.acos(1-h/R);a=theta*u;run=R*math.sin(theta)
    p=rim(t)-outward(t)*(run-R*math.sin(a));p.z=-h+R*(1-math.cos(a));return p

def surface_normal(fn,t,u):
    dt=fn(t+.001,u)-fn(t-.001,u);du=fn(t,u+.001)-fn(t,u-.001)
    n=du.cross(dt).normalized()
    return n if n.z>=0 else -n

def skin(n,verts,faces,rt,normals=None):
    ob=mesh(n,verts,faces,rt,smooth=True)
    bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update()
    bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<0]);bm.to_mesh(ob.data);bm.free();ob.data.update()
    if normals:ob.data.normals_split_custom_set_from_vertices(normals)
    return ob

def rimrect(t):
    p=rim(t);s=min(BX/max(abs(p.x),1e-8),BY/max(abs(p.y),1e-8));return p*s

def sector(k,pool=True):
    rt=root('Bowl_Sector_%02d'%k);start=k*math.tau/SECTORS;end=(k+1)*math.tau/SECTORS;N=SEGMENTS//SECTORS
    ts=[start+(end-start)*i/N for i in range(N+1)]
    v=[station(t,j/BANDS) for j in range(BANDS+1) for t in ts];f=[]
    for j in range(BANDS):
        for i in range(N):
            a=j*(N+1)+i;f.append((a,a+1,a+N+2,a+N+1))
    normals=[surface_normal(station,t,j/BANDS) for j in range(BANDS+1) for t in ts]
    ob=skin('8ft circular shotcrete section',v,f,rt,normals);ob['role']='bowl_transition'
    # Unfold every riding band by measured chainage. Adjacent sectors share
    # the same phase; projection-axis changes cannot leave a diagonal UV seam.
    chainages=[]
    for j in range(BANDS+1):
        row=[0.];last=station(0,j/BANDS)
        for q in range(1,SEGMENTS+1):
            p=station(q*math.tau/SEGMENTS,j/BANDS);row.append(row[-1]+(p-last).length);last=p
        chainages.append(row)
    uv=ob.data.uv_layers.active
    for face in ob.data.polygons:
        for li in face.loop_indices:
            index=ob.data.loops[li].vertex_index;j,i=divmod(index,N+1);t=ts[i]
            theta=math.acos(1-depth(t)/R)
            uv.data[li].uv=(chainages[j][k*N+i]/3.048,R*theta*j/BANDS/3.048)
    # Fill ring from coping to rectangular deck border, with intentional pour seams.
    v=[];f=[]
    for j in range(5):
        for t in ts:
            p=rim(t).lerp(rimrect(t),j/4);p.z=0;v.append(p)
    for j in range(4):
        for i in range(N):
            a=j*(N+1)+i;f.append((a,a+1,a+N+2,a+N+1))
    skin('Deck around actual bowl opening',v,f,rt,[(0,0,1)]*len(v))
    # Angular stations need not land exactly on a rectangular border corner.
    # Close the small chord cut at each edge change with its actual corner.
    for ta,tb in zip(ts,ts[1:]):
        a,b=rimrect(ta),rimrect(tb)
        ax=abs(abs(a.x)-BX)<1e-7;bx=abs(abs(b.x)-BX)<1e-7
        if ax==bx:continue
        c=Vector((math.copysign(BX,a.x+b.x),math.copysign(BY,a.y+b.y),0))
        z=(b-a).cross(c-a).z
        if abs(z)>1e-10:mesh('Deck corner closes to the actual rectangular paving cut',[a,b,c],[(0,1,2) if z>0 else (2,1,0)],rt)
    if pool:
        # Bullnose cast blocks, 3mm mortar seams, 11 inch wide by 2.5 inch high.
        profile=[(.285,-.03175),(.012,-.03175)]+[(.012-.03175*math.sin(j*math.pi/8),-.03175*math.cos(j*math.pi/8)) for j in range(1,9)]+[(.285,.03175)]
        for i in range(4):
            a=start+(end-start)*i/4+.00025;b=start+(end-start)*(i+1)/4-.00025;verts=[]
            for t in [a+(b-a)*j/5 for j in range(6)]:
                p=rim(t);n=outward(t)
                verts += [p+n*x+Vector((0,0,z)) for x,z in profile]
            L=len(profile);faces=[tuple(reversed(range(L))),tuple(range(5*L,6*L))]
            faces += [(q*L+j,q*L+(j+1)%L,(q+1)*L+(j+1)%L,(q+1)*L+j) for q in range(5) for j in range(L)]
            block=mesh('Cast bullnose coping block / square radial end planes',verts,faces,rt,'Coping',True)
            # End faces are genuinely planar, normal to the lip tangent. Do not
            # smooth a cut cap into the rounded nose: it bends the visible joint.
            for face in block.data.polygons:
                if len(face.vertices)>4:face.use_smooth=False
            block['coping_profile_vertices']=L
            # Mortar has a concrete value, recessed 2mm from the block top.
            t=start+(end-start)*i/4;p=rim(t);n=outward(t);tangent=Vector((-n.y,n.x,0))
            mesh('Radial 3mm mortar joint',[p+n*x+tangent*s+Vector((0,0,.02975)) for x,s in ((.01,-.0015),(.285,-.0015),(.285,.0015),(.01,.0015))],[(0,1,2,3)],rt,'Grout')
        # Tile follows the riding surface, not a vertical cylindrical wall.
        # Three 52mm courses, each split into individually grouted tiles.
        for row in range(3):
            for i in range(N):
                for sub in range(2):
                    a=ts[i]+(ts[i+1]-ts[i])*(sub/2+.007)
                    b=ts[i]+(ts[i+1]-ts[i])*((sub+1)/2-.007)
                    points=[]
                    for t,d in ((a,(row+1)*.052+.002),(b,(row+1)*.052+.002),(b,row*.052+.005),(a,row*.052+.005)):
                        theta=math.acos(1-depth(t)/R);u=1-d/(R*theta)
                        p=station(t,u);p-=outward(t)*.0015;points.append(p)
                    tile=mesh('Blue ceramic waterline tile',points,[(3,2,1,0)],rt,'Tile')
                    tile['tile_wear_index']=(k*N+i)*2+sub+row*SEGMENTS*2
                    tile['missing_tile']=(tile['tile_wear_index']%173==11 or (k in (10,11,12) and row==1 and i==5 and sub==0))
    else:
        tube('2-3/8 inch bowl steel coping',[rim(t)-outward(t)*.0206+Vector((0,0,-.0206)) for t in ts],.0301625,rt,s=16)
    socket(rt,'Seam_A',rim(start),kind='bowl_sector');socket(rt,'Seam_B',rim(end),kind='bowl_sector')
    return describe(rt,[BX*2,BY*2],transition_radius_m=R,section_angles_degrees=[math.degrees(start),math.degrees(end)],shallow_m=1.2192,deep_m=2.1336)

def floor():
    """Constrained triangulation of the actual concave toe contour.

    A clamped cubic radial-basis surface respects the boundary heights and
    bottom tangents. A fan from the deep drain folds across a kidney waist;
    this floor has an independently constrained polygon and an actual hole.
    """
    import numpy as np
    from mathutils.geometry import delaunay_2d_cdt
    rt=root('Bowl_Floor');N=SEGMENTS
    boundary=[station(i*math.tau/N,0) for i in range(N)]
    collar=[p-outward(i*math.tau/N)*.035 for i,p in enumerate(boundary)]
    constraints=boundary+collar+[Vector((x,y,-2.1426)) for x,y in ((3.85,-.15),(4.15,-.15),(4.15,.15),(3.85,.15))]
    xy=np.array([[p.x,p.y] for p in constraints]);zz=np.array([p.z for p in constraints])
    # Cubic polyharmonic interpolation, including an affine null space.
    d=np.linalg.norm(xy[:,None,:]-xy[None,:,:],axis=2);K=d**3
    P=np.c_[np.ones(len(xy)),xy];A=np.block([[K+np.eye(len(K))*1e-7,P],[P.T,np.zeros((3,3))]])
    weights=np.linalg.solve(A,np.r_[zz,[0,0,0]])
    def height(points):
        q=np.asarray(points);dist=np.linalg.norm(q[:,None,:]-xy[None,:,:],axis=2)
        fitted=(dist**3)@weights[:-3]+np.c_[np.ones(len(q)),q]@weights[-3:]
        # Interpolation must not leave a low pocket beside the drain. A
        # shallow 0.4% minimum apron rises from the actual square opening;
        # it stays below all accepted transition/toe boundary stations.
        apron=-2.1426+.004*np.maximum.reduce([np.abs(q[:,0]-4)-.15,np.abs(q[:,1])-.15,np.zeros(len(q))])
        return np.maximum(fitted,apron)
    def inside(x,y):
        hit=False
        for a,b in zip(boundary,boundary[1:]+boundary[:1]):
            if (a.y>y)!=(b.y>y) and x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x:hit=not hit
        return hit
    points=[Vector((p.x,p.y)) for p in constraints]
    for x in np.arange(min(p.x for p in boundary)+.2,max(p.x for p in boundary),.24):
        for y in np.arange(min(p.y for p in boundary)+.2,max(p.y for p in boundary),.24):
            if inside(x,y) and not (3.82<x<4.18 and -.18<y<.18):points.append(Vector((float(x),float(y))))
    edges=[(i,(i+1)%N) for i in range(N)]+[(2*N+i,2*N+(i+1)%4) for i in range(4)]
    verts,edges,faces,*_=delaunay_2d_cdt(points,edges,[list(range(N))],1,1e-6)
    coords=np.array([list(p) for p in verts]);z=height(coords)
    eps=.001;gx=(height(coords+[eps,0])-height(coords-[eps,0]))/(2*eps);gy=(height(coords+[0,eps])-height(coords-[0,eps]))/(2*eps)
    normals=[Vector((-float(x),-float(y),1)).normalized() for x,y in zip(gx,gy)]
    v=[(float(p[0]),float(p[1]),float(h)) for p,h in zip(coords,z)]
    floors=[rt]+[root('Bowl_Floor_'+str(i)) for i in range(1,4)]
    buckets=[[] for _ in floors]
    for face in faces:
        cx=sum(v[i][0] for i in face)/len(face);cy=sum(v[i][1] for i in face)/len(face)
        if 3.85<cx<4.15 and -.15<cy<.15:continue
        bucket=(int(cx>0)+2*int(cy>0));buckets[bucket].append(tuple(face))
    for k,owner in enumerate(floors):
        selected=buckets[k];ids=sorted({i for f in selected for i in f});remap={old:i for i,old in enumerate(ids)}
        ob=skin('Clamped concave basin floor',[v[i] for i in ids],[tuple(remap[i] for i in f) for f in selected],owner,[normals[i] for i in ids]);ob['role']='bowl_floor'
    # Deep-end drain is on the graded surface, with slot voids and rim frame.
    z=-2.1426
    box('Drain sediment sump',(4,0,z-.07),(.30,.30,.12),rt,'Black',0)
    for x in (3.845,4.155):box('Drain grate frame',(x,0,z-.004),(.01,.32,.012),rt,'Steel',0)
    for y in (-.155,.155):box('Drain grate frame',(4,y,z-.004),(.30,.01,.012),rt,'Steel',0)
    for k in range(11):box('Drain actual slotted bar',(3.86+k*.028,0,z-.003),(.009,.30,.012),rt,'Steel',.001)
    socket(rt,'Drain',(4,0,z),kind='drain')
    for owner in floors:describe(owner,[11.0,4.4],shallow_m=1.2192,deep_m=2.1336)
    return floors

def build(pool=True):
    global SHAPE
    SHAPE='kidney' if pool else 'clover'
    roots=[sector(k,pool) for k in range(SECTORS)]+floor()
    for rt in roots:rt['bowl_plan']=SHAPE
    return roots
