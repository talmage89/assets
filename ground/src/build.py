"""Parametric terrain skins; no buried caps or hidden interior end faces.

Library origins are at road center / curb flow line / sidewalk front center.
All sources and exports are scripted, and all shared-edge UVs use world XY.
"""
import argparse, json, math, sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from kit.tiling import material,world_uv,export
from dimensions import *
from textures import RECTS

MATS={}


def terrain_tint(p,kind):
    x,y,z=p
    # Exposure/traffic axes, continuous in world space and across module boundaries.
    exposure=.025*math.sin(x*.17+y*.037)+.016*math.sin(y*.41-x*.11)
    if kind=='Asphalt':
        distance=min(abs(x),abs(y))
        edge=math.exp(-((distance-ASPHALT_HALF)/.18)**2)
        # Broad mix / weather history; no painted tire tracks. Interpolated
        # vertex tint stays continuous across all world-aligned module ports.
        mix=.024*math.sin(x*.39+y*.16)*math.sin(y*.083-x*.07)
        t=.955+exposure+mix-.018*edge
    elif kind=='Lawn':
        t=.95+.035*math.sin(x*.14+y*.077)
    else:t=.985+exposure*.12
    t=max(0,min(1,t))
    return (t,t,t,1)


def mesh(name,verts,faces,kind,parent=None,uvs=None,normals=None):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.parent=parent
    ob.data.materials.append(MATS[kind]);ob['surface_kind']=kind
    if uvs is None:
        world_uv(ob,{'Asphalt':ASPHALT_TILE,'Concrete':CONCRETE_TILE,'Lawn':LAWN_TILE}.get(kind,CONCRETE_TILE))
    else:
        uv=me.uv_layers.new(name='UVMap')
        for poly,row in zip(me.polygons,uvs):
            for li,value in zip(poly.loop_indices,row):uv.data[li].uv=value
    if kind!='GroundTrim':
        colors=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT')
        for v in me.vertices:colors.data[v.index].color=terrain_tint(v.co,kind)
    if normals:
        for poly in me.polygons:poly.use_smooth=True
        me.normals_split_custom_set_from_vertices(normals)
    return ob


def joint_floor_uv(ob):
    uv=ob.data.uv_layers.active
    for poly in ob.data.polygons:
        if ob.data.materials[poly.material_index].name.startswith('GroundTrim'):
            for li in poly.loop_indices:
                p=ob.data.vertices[ob.data.loops[li].vertex_index].co
                uv.data[li].uv=(.6875+(p.x%1)*.05,.125+(p.y%1)*.0001)


def joint_floor(ob, select):
    ob.data.materials.append(MATS['GroundTrim']);uv=ob.data.uv_layers.active
    for poly in ob.data.polygons:
        if select(poly):
            poly.material_index=1
            for li in poly.loop_indices:
                p=ob.data.vertices[ob.data.loops[li].vertex_index].co
                uv.data[li].uv=(.6875+(p.x%1)*.05,.125+(p.y%1)*.0001)


def root(name):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob);ob['module']=name
    return ob


def socket(parent,name,loc):
    ob=bpy.data.objects.new(parent.name+'__'+name,None);bpy.context.collection.objects.link(ob);ob.parent=parent;ob.location=loc;ob['socket_kind']='terrain_snap'


def rectgrid(name,xs,ys,z,kind,parent,normal=None):
    verts=[(x,y,z(x,y)) for y in ys for x in xs];w=len(xs);faces=[]
    for j in range(len(ys)-1):
        for i in range(w-1):
            a=j*w+i;faces.extend([(a,a+1,a+w+1),(a,a+w+1,a+w)])
    ns=[normal(x,y) for y in ys for x in xs] if normal else None
    return mesh(name,verts,faces,kind,parent,normals=ns)


def roadnormal(x,y=0):
    return Vector((math.copysign(CROWN_SLOPE,x) if abs(x)>1e-7 else 0,0,1)).normalized()


def intersection_z(x,y):
    d=math.hypot(CORE-abs(x),CORE-abs(y))-(RADIUS+GUTTER)
    return ROAD_EDGE+min(ASPHALT_HALF,max(0,d))*CROWN_SLOPE


def intersection_normal(x,y):
    dx,dy=CORE-abs(x),CORE-abs(y);r=math.hypot(dx,dy)
    if r-(RADIUS+GUTTER)>=ASPHALT_HALF-1e-7:return Vector((0,0,1))
    nx=(math.copysign(1,x) if abs(x)>1e-7 else 0)*dx/r*CROWN_SLOPE
    ny=(math.copysign(1,y) if abs(y)>1e-7 else 0)*dy/r*CROWN_SLOPE
    return Vector((nx,ny,1)).normalized()


def curb_project(ob,v,p):
    # Unfold the rounded vertical profile along its local radial direction.
    # World coordinates retain phase; a corner's tangent ends equal the straight.
    direction=Vector((-v.x,-v.y,0)).normalized() if ob.get('curb_curved') else Vector((1,0,0))
    return p+ob.matrix_world.to_3x3()@(direction*v.z)


def inlet_return_uv(ob):
    """Unfold chamber ends along Y; the curb's longitudinal faces use X."""
    if not ob.get('inlet_returns'):return
    uv=ob.data.uv_layers.active
    for poly in ob.data.polygons:
        if abs(poly.normal.y)<.9 or ob.data.materials[poly.material_index].name!='Concrete':continue
        for li in poly.loop_indices:
            v=ob.data.vertices[ob.data.loops[li].vertex_index].co
            p=ob.matrix_world@v+ob.matrix_world.to_3x3()@Vector((0,v.z,0))
            uv.data[li].uv=(p.x/CONCRETE_TILE,p.y/CONCRETE_TILE)


def ramp_project(ob,v,p):
    factor=max(0,1-v.x/STRIP)
    return p+ob.matrix_world.to_3x3()@Vector((v.z*factor,0,0))


def decal(parent,name,points,kind,rect=None):
    r=RECTS[kind] if rect is None else rect;u0,v0,u1,v1=r
    return mesh(name,points,[(0,1,2),(0,2,3)],'GroundTrim',parent,
        uvs=[[(u0,v0),(u1,v0),(u1,v1)],[(u0,v0),(u1,v1),(u0,v1)]])


def road_card(parent,name,x0,x1,y0,y1,kind,z=lambda x,y:road_z(x),rect=None):
    # Vertices must share crown break subdivisions for the card never to cut below asphalt.
    xs=sorted(set([x0,x1]+[x for x in (-ASPHALT_HALF/2,0,ASPHALT_HALF/2) if x0<x<x1]))
    rows=[y0,y1];verts=[(x,y,z(x,y)+{'polish':.002,'oil':.004,'seal':.003,'patch':.008,'paint':.003}.get(kind,DECAL_OFFSET)) for y in rows for x in xs];faces=[];uvs=[]
    r=RECTS[kind] if rect is None else rect;u0,v0,u1,v1=r
    for i in range(len(xs)-1):
        w=len(xs);a=i;faces.extend([(a,a+1,a+w+1),(a,a+w+1,a+w)])
    def uv(p):return (u0+(p[0]-x0)/(x1-x0)*(u1-u0),v0+(p[1]-y0)/(y1-y0)*(v1-v0))
    for f in faces:uvs.append([uv(verts[v]) for v in f])
    return mesh(name,verts,faces,'GroundTrim',parent,uvs=uvs)


def road(name,variant):
    rt=root(name)
    rectgrid(name+'_asphalt',np.linspace(-ASPHALT_HALF,ASPHALT_HALF,9),np.linspace(-LENGTH/2,LENGTH/2,5),lambda x,y:road_z(x),'Asphalt',rt,roadnormal)
    for side in (-1,1):
        lo,hi=((-ASPHALT_HALF+.001,-ASPHALT_HALF+.181) if side<0 else (ASPHALT_HALF-.181,ASPHALT_HALF-.001))
        ob=road_card(rt,name+'_edge_ravel_'+str(side),lo,hi,-LENGTH/2,LENGTH/2,'ravel')
        if side<0:
            u0,v0,u1,v1=RECTS['ravel']
            for value in ob.data.uv_layers.active.data:value.uv.x=u0+u1-value.uv.x
    if variant==1:
        road_card(rt,name+'_sealed_transverse',-2.8,1.5,-.105,.105,'seal')
    if variant==2:
        road_card(rt,name+'_utility_patch',-2.9,-1.2,-2.5,-.6,'patch')
    for side,y in [('S',-LENGTH/2),('N',LENGTH/2)]:socket(rt,side,(0,y,0))
    for side,x in [('W',-ASPHALT_HALF),('E',ASPHALT_HALF)]:socket(rt,side,(x,0,ROAD_EDGE))
    rt['size_m']=[2*ASPHALT_HALF,LENGTH,road_z(0)]
    return rt


def intersection():
    rt=root('Road_Intersection')
    rectgrid('Intersection_center',np.linspace(-ASPHALT_HALF,ASPHALT_HALF,9),np.linspace(-ASPHALT_HALF,ASPHALT_HALF,9),intersection_z,'Asphalt',rt,intersection_normal)
    # Arms, with identical port tessellation and normals to the straight module.
    for yaw in range(4):
        ang=yaw*math.pi/2;cs,sn=math.cos(ang),math.sin(ang)
        verts=[];faces=[]
        for y in np.linspace(ASPHALT_HALF,CORE,7):
            for x in np.linspace(-ASPHALT_HALF,ASPHALT_HALF,9):
                xx,yy=x*cs-y*sn,x*sn+y*cs;verts.append((xx,yy,intersection_z(xx,yy)))
        for j in range(6):
            for i in range(8):
                a=j*9+i;faces.extend([(a,a+1,a+10),(a,a+10,a+9)])
        mesh('Intersection_arm_'+str(yaw),verts,faces,'Asphalt',rt,normals=[intersection_normal(x,y) for x,y,z in verts])
    # Four convex roadway wedges outside the swept curb return.
    for yaw in range(4):
        ang=yaw*math.pi/2;cs,sn=math.cos(ang),math.sin(ang)
        verts=[(ASPHALT_HALF,ASPHALT_HALF,intersection_z(ASPHALT_HALF,ASPHALT_HALF))];faces=[]
        # Radial strips retain all seven shared arm-edge samples. No T-junction
        # can bridge a different crown height between the wedge and the arm.
        for level in range(1,7):
            f=level/6
            for t in np.linspace(0,math.pi/2,25):
                bx=CORE-(RADIUS+GUTTER)*math.cos(t);by=CORE-(RADIUS+GUTTER)*math.sin(t)
                x=ASPHALT_HALF+(bx-ASPHALT_HALF)*f;y=ASPHALT_HALF+(by-ASPHALT_HALF)*f
                verts.append((x,y,intersection_z(x,y)))
        for i in range(24):faces.append((0,2+i,1+i))
        for level in range(5):
            start=1+level*25
            for i in range(24):
                a=start+i;faces.extend([(a,a+26,a+25),(a,a+1,a+26)])
        vv=[]
        for x,y,z in verts:
            xx,yy=x*cs-y*sn,x*sn+y*cs;vv.append((xx,yy,z))
        mesh('Intersection_wedge_'+str(yaw),vv,faces,'Asphalt',rt,normals=[intersection_normal(x,y) for x,y,z in vv])
    # Edge fretting around returns follows the actual game mesh, not an
    # analytic height that could cut through its triangulated crown.
    from mathutils.bvhtree import BVHTree
    points=[];triangles=[]
    for ob in rt.children_recursive:
        if ob.type!='MESH':continue
        ob.data.calc_loop_triangles();start=len(points);points.extend([v.co.copy() for v in ob.data.vertices])
        triangles.extend([tuple(start+i for i in t.vertices) for t in ob.data.loop_triangles])
    bvh=BVHTree.FromPolygons(points,triangles,all_triangles=True)
    for k in range(4):
        angle=k*math.pi/2;c,s=math.cos(angle),math.sin(angle);verts=[];faces=[];uvs=[]
        for j,t in enumerate(np.linspace(math.pi/2,0,25)):
            for r in (RADIUS+GUTTER+.181,RADIUS+GUTTER+.001):
                x,y=CORE-r*math.cos(t),CORE-r*math.sin(t);xx,yy=x*c-y*s,x*s+y*c
                xx=max(-CORE+.00001,min(CORE-.00001,xx));yy=max(-CORE+.00001,min(CORE-.00001,yy))
                hit,normal,_,_=bvh.ray_cast(Vector((xx,yy,1)),Vector((0,0,-1)))
                if hit is None:raise RuntimeError(f'Unfitted intersection ravel {k} {t} {xx} {yy}')
                verts.append(tuple(hit+Vector((0,0,DECAL_OFFSET))))
        u0,v0,u1,v1=RECTS['ravel']
        for j in range(24):
            a=j*2
            for f in ((a,a+1,a+3),(a,a+3,a+2)):
                faces.append(f);uvs.append([(u0+(v%2)*(u1-u0),v0+(v//2)/24*(v1-v0)) for v in f])
        mesh('Intersection_edge_ravel_'+str(k),verts,faces,'GroundTrim',rt,uvs=uvs)
    for side,loc in [('N',(0,CORE,0)),('E',(CORE,0,0)),('S',(0,-CORE,0)),('W',(-CORE,0,0))]:socket(rt,side,loc)
    rt['size_m']=[2*CORE,2*CORE,road_z(0)]
    return rt


# Open buried underside/end faces. Keep the municipal pan/envelope, with the
# lead's crisp barrier curb: 13 mm tool radii and a 1:12 battered planar face.
PROFILE=[(-GUTTER,ROAD_EDGE),(-.15,.002),(-.0254,0),(-.013,0)]
PROFILE_NORMALS=[(.014,1),(.015,1),(.008,1),(0,1)]
radius=.013;face_angle=math.atan(1/12)
for t in (-math.pi/3,-math.pi/6,-face_angle):
    PROFILE.append((-.013+radius*math.cos(t),radius+radius*math.sin(t)))
    PROFILE_NORMALS.append((-math.cos(t),-math.sin(t)))
bottom_q,bottom_z=PROFILE[-1]
cz=CURB_HEIGHT-radius;front_z=cz+radius*math.sin(face_angle)
cx=bottom_q+(front_z-bottom_z)/12+radius*math.cos(face_angle)
for t in np.linspace(math.pi-face_angle,math.pi/2,4):
    PROFILE.append((cx+radius*math.cos(t),cz+radius*math.sin(t)))
    PROFILE_NORMALS.append((math.cos(t),math.sin(t)))
PROFILE.append((CURB,CURB_HEIGHT));PROFILE_NORMALS.append((0,1))


def curb(name,cut=False,ramp=False,corner=False):
    rt=root(name);verts=[];faces=[]
    joint_angles=[math.pi/6,math.pi/3]
    joint_half=.0015875/RADIUS
    if corner:
        stations=sorted(set(list(np.linspace(0,math.pi/2,25))+[t+d for t in joint_angles for d in (-.006/RADIUS,-joint_half,joint_half,.006/RADIUS)]))
    else:
        length=LENGTH if cut else BAY
        stations=sorted(set(np.linspace(-length/2,length/2,25).tolist()+[-PANEL/2,PANEL/2,-.006,-.0015875,0,.0015875,.006]))
    if cut or ramp:stations=transition_stations(LENGTH if cut else BAY,BAY if cut else PANEL)
    if not corner and not cut and not ramp:
        stations=[-BAY/2,-.006,-.0015875,.0015875,.006,BAY/2]
    def depress(s):
        if not cut and not ramp:return 1.
        width=BAY if cut else PANEL; length=LENGTH if cut else BAY
        t=max(0,min(1,(abs(s)-width/2)/((length-width)/2)))
        t=t*t*(3-2*t)
        return .17+.83*t if cut else t
    for s in stations:
        depression=depress(s)
        for q,z in PROFILE:
            zz=z
            if q>=-.01:zz=z*depression
            # Control joint at the center; geometry carries the groove, not a decal shadow.
            if not corner and not cut and not ramp and abs(s)<=.0016:zz-=.006*max(0,min(1,(q+GUTTER)/.04))
            if corner and min(abs(s-t) for t in joint_angles)<=joint_half+1e-9:
                zz-=.006*max(0,min(1,(q+GUTTER)/.04))
            if corner:
                rr=RADIUS-q
                # Extra joint stations stay ON the original 24-segment road edge.
                step=math.pi/48;j=min(23,int(s/step));f=(s-j*step)/step
                x=-rr*((1-f)*math.cos(j*step)+f*math.cos((j+1)*step))
                y=-rr*((1-f)*math.sin(j*step)+f*math.sin((j+1)*step))
                verts.append((x,y,zz))
            else:verts.append((q,s,zz))
    count=len(PROFILE)
    for j in range(len(stations)-1):
        for i in range(count-1):
            a=j*count+i
            # Along +Y then across +X yields +Z.
            faces.extend([(a,a+1+count,a+1),(a,a+count,a+1+count)] if corner else [(a,a+1,a+1+count),(a,a+1+count,a+count)])
    ob=mesh(name+'_concrete',verts,faces,'Concrete',rt)
    if corner:
        def select(poly):
            station=poly.index//(2*(len(PROFILE)-1))
            return any(abs(stations[station]-t)<=joint_half+1e-9 and abs(stations[station+1]-t)<=joint_half+1e-9 for t in joint_angles)
        joint_floor(ob,select)
    elif not cut and not ramp:
        joint_floor(ob,lambda p:all(abs(verts[i][1])<=.0016 for i in p.vertices))
    ob['curb_chart']=True;ob['curb_curved']=corner
    world_uv(ob,CONCRETE_TILE,project=curb_project)
    joint_floor_uv(ob)
    # Smooth only the real rounded profile; same analytic strip normals at each station.
    ns=[]
    for j,s in enumerate(stations):
        for i,(q,z) in enumerate(PROFILE):
            nx,nz=PROFILE_NORMALS[i]
            nx*=depress(s) if q>=-.01 else 1
            ds=z*(depress(s+.00001)-depress(s-.00001))/.00002 if q>=-.01 else 0
            n=Vector((nx,-nz*ds,nz)).normalized()
            if corner:
                # Local across-profile +q points toward the center of the corner circle.
                n=Vector((n.x*math.cos(s),n.x*math.sin(s),n.z))
            ns.append(n)
    for p in ob.data.polygons:p.use_smooth=True
    ob.data.normals_split_custom_set_from_vertices(ns)
    if corner:
        socket(rt,'N',(-RADIUS,0,0));socket(rt,'E',(0,-RADIUS,0))
    else:
        socket(rt,'S',(0,-(LENGTH if cut else BAY)/2,0));socket(rt,'N',(0,(LENGTH if cut else BAY)/2,0))
        if ramp:socket(rt,'Back',(CURB,0,0))
    return rt


def walk_z(x):return CURB_HEIGHT+x*WALK_SLOPE


def sidewalk(name,variant=0):
    rt=root(name)
    # Half-panels at each end allow seamless module cuts through a panel. Grooves
    # fall on centers, exactly 5 ft apart after instancing.
    ys=sorted(set([-PANEL/2,-.012,-.005,-.0015875,.0015875,.005,.012,PANEL/2]))
    def z(x,y):
        g=.006 if abs(y)<=.0016 else .002 if abs(y)<=.005 else 0
        border=.002*(max(0,1-x/.012)+max(0,1-(PANEL-x)/.012))
        return walk_z(x)-g-border
    def normal(x,y):
        slope=WALK_SLOPE+(.002/.012 if x==0 else -.002/.012 if x==PANEL else 0)
        return Vector((-slope,0,1)).normalized()
    slab=rectgrid(name+'_slab',[0,.012,PANEL-.012,PANEL],ys,z,'Concrete',rt,normal)
    joint_floor(slab,lambda p:all(abs(slab.data.vertices[i].co.y)<=.0016 for i in p.vertices))
    if variant:
        p=[(.2,-.5),(.43,-.28),(.36,-.09),(.62,-.02)]
        for i,((x0,y0),(x1,y1)) in enumerate(zip(p,p[1:])):
            width=.025
            decal(rt,name+'_shrinkage_'+str(i),[(x0-width,y0,z(x0-width,y0)+DECAL_OFFSET*2),(x0+width,y0,z(x0+width,y0)+DECAL_OFFSET*2),(x1+width,y1,z(x1+width,y1)+DECAL_OFFSET*2),(x1-width,y1,z(x1-width,y1)+DECAL_OFFSET*2)],'crack')
    socket(rt,'S',(0,-PANEL/2,0));socket(rt,'N',(0,PANEL/2,0));return rt


def sidewalk_corner():
    rt=root('Sidewalk_Corner');ri=RADIUS-CURB-STRIP;ro=ri-PANEL
    verts=[];faces=[];radii=[ro,ro+.012,ri-.012,ri]
    thetas=sorted(set(list(np.linspace(0,math.pi/2,49))+[t+d for t in (math.pi/6,math.pi/3) for d in (-.006/ri,-.0015875/ri,.0015875/ri,.006/ri)]))
    for theta in thetas:
        for r in radii:
            off=ri-r;border=.002 if r in (ro,ri) else 0
            depth=.006 if min(abs(theta-t) for t in (math.pi/6,math.pi/3))<=.0015875/ri+1e-9 else 0
            verts.append((-r*math.cos(theta),-r*math.sin(theta),walk_z(off)-border-depth))
    for j in range(len(thetas)-1):
        for i in range(3):
            a=j*4+i;faces.extend([(a,a+5,a+4),(a,a+1,a+5)])
    ob=mesh('Sidewalk_corner_slab',verts,faces,'Concrete',rt)
    joint_floor(ob,lambda p: all(min(abs(math.atan2(-verts[i][1],-verts[i][0])-t) for t in (math.pi/6,math.pi/3))<=.0015875/ri+1e-8 for i in p.vertices))
    # Radius/angular normals independent of tessellation, including both end seams.
    normals=[]
    for theta in thetas:
        for i,r in enumerate(radii):
            slope=WALK_SLOPE+(-.002/.012 if i==0 else .002/.012 if i==3 else 0)
            normals.append(Vector((-math.cos(theta)*slope,-math.sin(theta)*slope,1)).normalized())
    for p in ob.data.polygons:p.use_smooth=True
    ob.data.normals_split_custom_set_from_vertices(normals)
    socket(rt,'N',(-ri,0,0));socket(rt,'E',(0,-ri,0));return rt


def sidewalk_ramp():
    rt=root('Sidewalk_Ramp')
    # x=0 is the curb back; x=STRIP is the sidewalk front. Full 5 ft landing remains.
    xs=[0,.6096,STRIP,STRIP+.012,STRIP+PANEL-.012,STRIP+PANEL]
    ys=transition_stations(BAY,PANEL)
    def z(x,y):
        if x>=STRIP:
            xx=x-STRIP
            border=.002*(max(0,1-xx/.012)+max(0,1-(PANEL-xx)/.012))
            return walk_z(xx)-border
        full=CURB_HEIGHT*x/STRIP
        flare=max(0,min(1,(abs(y)-PANEL/2)/(PANEL/2)));flare=flare*flare*(3-2*flare)
        return full+(CURB_HEIGHT-full)*flare
    def normal(x,y):
        if x>=STRIP:
            xx=x-STRIP;slope=WALK_SLOPE+(.002/.012 if abs(xx)<1e-6 else -.002/.012 if abs(xx-PANEL)<1e-6 else 0)
            return Vector((-slope,0,1)).normalized()
        e=.00001;dx=(z(x+e,y)-z(x-e,y))/(2*e);dy=(z(x,y+e)-z(x,y-e))/(2*e)
        return Vector((-dx,-dy,1)).normalized()
    slab=rectgrid('Ramp_and_landing',xs,ys,z,'Concrete',rt,normal)
    slab['ramp_chart']=True
    world_uv(slab,CONCRETE_TILE,project=ramp_project)
    points=[(0,-PANEL/2,z(0,-PANEL/2)+DECAL_OFFSET),(.6096,-PANEL/2,z(.6096,-PANEL/2)+DECAL_OFFSET),(.6096,PANEL/2,z(.6096,PANEL/2)+DECAL_OFFSET),(0,PANEL/2,z(0,PANEL/2)+DECAL_OFFSET)]
    # Rotate panel UVs: its 25 domes run across ramp width, 10 in travel direction.
    u0,v0,u1,v1=RECTS['warning']
    pad=1/2048;u0+=pad;v0+=pad;u1-=pad;v1-=pad
    uv=[[(u0,v0),(u0,v1),(u1,v1)],[(u0,v0),(u1,v1),(u1,v0)]]
    mesh('Detectable_warning',points,[(0,1,2),(0,2,3)],'GroundTrim',rt,uvs=uv)
    socket(rt,'S',(STRIP,-BAY/2,0));socket(rt,'N',(STRIP,BAY/2,0));socket(rt,'Curb',(0,0,0));return rt


def trims():
    rt=root('Markings_Crossing')
    # Perpendicular 5 ft crosswalk band centered on both ramp axes. A 12-inch
    # stop bar lies 4 ft before the nearest edge, only on the approach lane.
    y0=-.9144;y1=.9144
    def paint_rect(index):
        u0,v0,u1,v1=RECTS['paint'];w=(u1-u0)/4;pad=1/2048
        return (u0+index*w+pad,v0+pad,u0+(index+1)*w-pad,v1-pad)
    for i,x in enumerate(np.arange(-ASPHALT_HALF+.22,ASPHALT_HALF-.3,.9144)):
        index=(0,1,2,0,3,2,1,0)[i%8]
        road_card(rt,'Crosswalk_bar_'+str(i),float(x),float(min(x+.4572,ASPHALT_HALF)),y0,y1,'paint',rect=paint_rect(index))
    xs=(-ASPHALT_HALF,-2.95,-2.3,-1.3,-.65,0)
    for i,(a,b) in enumerate(zip(xs,xs[1:])):
        road_card(rt,'Stop_bar_'+str(i),a,b,.9144+1.2192,.9144+1.2192+.3048,'paint',rect=paint_rect((0,1,0,2,0)[i]))
    socket(rt,'Ramp_axis',(0,0,0));return rt


def consolidate(rt):
    meshes=[o for o in rt.children_recursive if o.type=='MESH']
    if len(meshes)<2:return
    base=next((o for o in meshes if o.get('surface_kind')!='GroundTrim'),meshes[0])
    bpy.ops.object.select_all(action='DESELECT')
    for ob in meshes:ob.select_set(True)
    bpy.context.view_layer.objects.active=base;bpy.ops.object.join()


def opaque_castings(roots):
    """Solid atlas regions must not enter a viewer's transparent draw queue."""
    for rt in roots:
        for ob in rt.children_recursive:
            if ob.type!='MESH':continue
            uv=ob.data.uv_layers.active
            selected=[]
            for poly in ob.data.polygons:
                if ob.data.materials[poly.material_index].name!='GroundTrim':continue
                coords=[uv.data[i].uv for i in poly.loop_indices]
                for region in ('iron','manhole'):
                    u0,v0,u1,v1=RECTS[region]
                    if all(u0-1e-6<=p.x<=u1+1e-6 and v0-1e-6<=p.y<=v1+1e-6 for p in coords):
                        selected.append(poly);break
            if selected:
                slot=len(ob.data.materials);ob.data.materials.append(MATS['GroundIron'])
                for poly in selected:poly.material_index=slot


def main():
    p=argparse.ArgumentParser();p.add_argument('--textures',type=Path,default=Path('textures/ship'));p.add_argument('--out',type=Path,default=Path('export/Ground.glb'));a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for name in ('Asphalt','Concrete','Lawn','GroundTrim'):MATS[name]=material(name,a.textures,alpha=name=='GroundTrim',tint=name!='GroundTrim')
    # One additional alpha state shares the same three atlas images. Grass
    # uses standard glTF MASK; fractional paint/sediment keeps BLEND.
    foliage=MATS['GroundTrim'].copy();foliage.name='GroundFoliage';foliage.use_backface_culling=False
    nt=foliage.node_tree;bs=nt.nodes.get('Principled BSDF')
    alpha=next(n for n in nt.nodes if n.type=='TEX_IMAGE' and 'BaseColor' in n.image.name)
    clip=nt.nodes.new('ShaderNodeMath');clip.operation='GREATER_THAN';clip.inputs[1].default_value=.30
    nt.links.new(alpha.outputs['Alpha'],clip.inputs[0]);nt.links.new(clip.outputs[0],bs.inputs['Alpha'])
    MATS['GroundFoliage']=foliage
    iron=MATS['GroundTrim'].copy();iron.name='GroundIron'
    bs=iron.node_tree.nodes.get('Principled BSDF')
    for link in list(bs.inputs['Alpha'].links):iron.node_tree.links.remove(link)
    bs.inputs['Alpha'].default_value=1
    MATS['GroundIron']=iron
    roots=[road('Road_Straight_A',0),road('Road_Straight_B',1),road('Road_Straight_C',2),intersection(),curb('Curb_Straight'),curb('Curb_Corner',corner=True),curb('Curb_DrivewayCut',cut=True),curb('Curb_Ramp',ramp=True),sidewalk('Sidewalk_A'),sidewalk('Sidewalk_B',1),sidewalk_corner(),sidewalk_ramp(),trims()]
    from additions import build_modules
    roots+=build_modules(sys.modules[__name__])
    for rt in roots:
        if rt.name not in ('Road_Intersection','Manhole','Curb_StormInlet'):consolidate(rt)
    opaque_castings(roots)
    # Preserve editable source shaders/meshes before inspection layout moves roots.
    bpy.ops.wm.save_as_mainfile(filepath=str(Path('build/source.blend').resolve()))
    report={}
    for i,rt in enumerate(roots):
        tris=sum(len(ob.data.loop_triangles) for ob in rt.children_recursive if ob.type=='MESH')
        # loop_triangles may be lazily empty until evaluated.
        tris=0
        for ob in rt.children_recursive:
            if ob.type=='MESH':ob.data.calc_loop_triangles();tris+=len(ob.data.loop_triangles)
        report[rt.name]=dict(triangles=tris,sockets={c.name.split('__')[-1]:list(c.location) for c in rt.children if c.type=='EMPTY'})
        rt.location=(i%4*22,i//4*22,0)
    export(a.out)
    Path('build/modules.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':main()
