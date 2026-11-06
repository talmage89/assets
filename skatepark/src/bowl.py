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

def rim(t):
    phase=math.atan2(math.sin(t-math.pi/2),math.cos(t-math.pi/2))
    waist=1.60*math.exp(-(phase/.65)**2)
    return Vector((7.3152*math.cos(t)+.30*math.cos(2*t),5.1816*math.sin(t)*(1+.10*math.cos(t))-waist,0))
def outward(t):
    phase=math.atan2(math.sin(t-math.pi/2),math.cos(t-math.pi/2));waist=1.60*math.exp(-(phase/.65)**2)
    dx=-7.3152*math.sin(t)-.60*math.sin(2*t)
    dy=5.1816*(math.cos(t)+.10*math.cos(2*t))+2*phase/(.65**2)*waist
    return Vector((dy,-dx,0)).normalized()
def depth(t):return 1.6764+.4572*math.cos(t)
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
    # Fill ring from coping to rectangular deck border, with intentional pour seams.
    v=[];f=[]
    for j in range(5):
        for t in ts:
            p=rim(t).lerp(rimrect(t),j/4);p.z=0;v.append(p)
    for j in range(4):
        for i in range(N):
            a=j*(N+1)+i;f.append((a,a+1,a+N+2,a+N+1))
    skin('Deck around actual bowl opening',v,f,rt,[(0,0,1)]*len(v))
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
            mesh('Cast bullnose coping block',verts,faces,rt,'Coping',True)
        # Tile follows the riding surface, not a vertical cylindrical wall.
        # Three rows; 51mm squares, one grouted channel mesh beneath.
        for row in range(3):
            for i in range(N):
                for sub in range(2):
                    a=ts[i]+(ts[i+1]-ts[i])*(sub/2+.007)
                    b=ts[i]+(ts[i+1]-ts[i])*((sub+1)/2-.007)
                    points=[]
                    for t,d in ((a,(row+1)*.052+.002),(b,(row+1)*.052+.002),(b,row*.052+.005),(a,row*.052+.005)):
                        theta=math.acos(1-depth(t)/R);u=1-d/(R*theta)
                        p=station(t,u);p-=outward(t)*.0015;points.append(p)
                    mesh('Blue ceramic waterline tile',points,[(0,1,2,3)],rt,'Tile')
    else:
        tube('2-3/8 inch bowl steel coping',[rim(t)-outward(t)*.0206+Vector((0,0,-.0206)) for t in ts],.0301625,rt,s=16)
    socket(rt,'Seam_A',rim(start),kind='bowl_sector');socket(rt,'Seam_B',rim(end),kind='bowl_sector')
    return describe(rt,[BX*2,BY*2],transition_radius_m=R,section_angles_degrees=[math.degrees(start),math.degrees(end)],shallow_m=1.2192,deep_m=2.1336)

def floor():
    rt=root('Bowl_Floor');v=[];f=[];N=SEGMENTS
    # Surface interpolates the bottom tangent ring through a broad waterfall.
    center=Vector((4.0,0,-2.1336))
    def point(t,u):
            edge=station(t,0);direction=edge-center
            scale=min(.15/max(abs(direction.x),1e-9),.15/max(abs(direction.y),1e-9))
            inner=center+direction*scale
            p=inner.lerp(edge,u);s=u*u*(3-2*u);p.z=inner.z*(1-s)+edge.z*s-.009*(1-u*u);return p
    normals=[]
    for j in range(9):
        for i in range(N):
            t=i*math.tau/N;u=j/8;v.append(point(t,u));normals.append(surface_normal(point,t,u))
    for j in range(8):
        for i in range(N):
            a=j*N+i;b=j*N+(i+1)%N;f.append((a,b,b+N,a+N))
    floors=[rt]+[root('Bowl_Floor_'+str(i)) for i in range(1,4)]
    for k,owner in enumerate(floors):
        selected=[face for face in f if int((face[0]%N)/(N/4))==k]
        ids=sorted({i for face in selected for i in face});remap={old:i for i,old in enumerate(ids)}
        ob=skin('Waterfall floor with drainage fall',[v[i] for i in ids],[tuple(remap[i] for i in face) for face in selected],owner,[normals[i] for i in ids]);ob['role']='bowl_floor'
    # Deep-end drain is on the graded surface, with slot voids and rim frame.
    z=-2.1426
    box('Drain sediment sump',(4,0,z-.07),(.30,.30,.12),rt,'Black',0)
    for x in (3.845,4.155):box('Drain grate frame',(x,0,z-.004),(.01,.32,.012),rt,'Steel',0)
    for y in (-.155,.155):box('Drain grate frame',(4,y,z-.004),(.30,.01,.012),rt,'Steel',0)
    for k in range(11):box('Drain actual slotted bar',(3.86+k*.028,0,z-.003),(.009,.30,.012),rt,'Steel',.001)
    socket(rt,'Drain',(4,0,z),kind='drain')
    for owner in floors:describe(owner,[11.0,4.4],shallow_m=1.2192,deep_m=2.1336)
    return floors

def build(pool=True):return [sector(k,pool) for k in range(SECTORS)]+floor()
