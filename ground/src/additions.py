"""Drive concrete, turf skins/edging, and fitted street castings.

All units are meters. `build_modules` receives the core modeling vocabulary so
there is one material registry and one set of UV/mesh conventions.
"""
import math,random
import bpy
import bmesh
import numpy as np
from mathutils import Vector
from dimensions import *
from textures import RECTS
from kit import model

b=None


def atlas_uv(ob,kind,extent=.3,axes=None):
    pad=2/2048
    uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='UVMap')
    points=[v.co for v in ob.data.vertices]
    limits=[(min(p[i] for p in points),max(p[i] for p in points)) for i in range(3)]
    for poly in ob.data.polygons:
        region='iron' if kind=='manhole' and (abs(poly.normal.z)<.7 or poly.normal.z<-.7) else kind
        u0,v0,u1,v1=RECTS[region]
        ax=axes or ((1,2) if abs(poly.normal.x)>.7 else (0,2) if abs(poly.normal.y)>.7 else (0,1))
        # Long cast faces run along the atlas's long V axis. Swapping them
        # avoids stretching a square sand grain into wood-like horizontal lines.
        if region=='iron' and axes is None:
            ax=(2,1) if abs(poly.normal.x)>.7 else (2,0) if abs(poly.normal.y)>.7 else (0,1)
        low=[limits[i][0] for i in ax];high=[limits[i][1] for i in ax]
        for li in poly.loop_indices:
            p=ob.data.vertices[ob.data.loops[li].vertex_index].co
            if region=='manhole':a,c=.5+p.x/extent,.5+p.y/extent
            else:
                a,c=[.05+.90*(p[i]-lo)/max(hi-lo,1e-8) for i,lo,hi in zip(ax,low,high)]
                # Two finish strips in the existing iron region: tire-abraded
                # upper faces and water-retaining vertical/underside faces.
                if region=='iron':a=a*.46+(0 if poly.normal.z>.7 else .54)
            uv.data[li].uv=(u0+pad+a*(u1-u0-2*pad),v0+pad+c*(v1-v0-2*pad))


def casting_box(name,rt,center,size,kind='iron',bevel=.0018):
    ob=model.box(name,center,size,b.MATS['GroundTrim'],radius=bevel,segments=1)
    model.apply(ob)
    # Bake locations into vertices; every service part retains a useful root.
    for v in ob.data.vertices:v.co+=ob.location
    ob.location=(0,0,0);ob.parent=rt;ob['surface_kind']='GroundTrim';ob['structural_casting']=True
    atlas_uv(ob,kind)
    return ob


def grass_edges(rt,paths,seed):
    rng=random.Random(seed);verts=[];faces=[];uvs=[]
    u0,v0,u1,v1=RECTS['grass'];cw=(u1-u0)/4;ch=(v1-v0)/2;pad=1.5/2048
    for path in paths:
        total=sum((Vector(c)-Vector(a)).length for a,c in zip(path,path[1:]))
        n=max(1,round(total/.135))
        points=[Vector(p) for p in path]
        lens=[0.]
        for a,c in zip(points,points[1:]):lens.append(lens[-1]+(c-a).length)
        for s in sorted(rng.uniform(.005,total-.005) for j in range(n)):
            idx=next((i for i in range(len(lens)-1) if lens[i]<=s<=lens[i+1]),len(lens)-2)
            t=(s-lens[idx])/(lens[idx+1]-lens[idx]);p=points[idx].lerp(points[idx+1],t)
            tangent=(points[idx+1]-points[idx]).normalized();out=Vector((-tangent.y,tangent.x,0))
            width=min(rng.uniform(.18,.27),2*min(s,total-s));height=rng.uniform(.032,.060)
            # Low, bent planes lean over concrete by a few cm; a second plane
            # turns across the first. Alpha holes retain individual blades.
            for axis in (tangent,(tangent*.30+out*.95).normalized()):
                bottom=p+out*rng.uniform(-.008,.007)-Vector((0,0,.012))
                top=bottom+Vector((0,0,height))+out*rng.uniform(.006,.016)
                start=len(verts)
                verts.extend([tuple(bottom-axis*width/2),tuple(bottom+axis*width/2),tuple(top+axis*width/2),tuple(top-axis*width/2)])
                cell=rng.randrange(4);row=rng.randrange(2)
                ua=u0+cell*cw+pad;ub=u0+(cell+1)*cw-pad;va=v0+row*ch+pad;vb=v0+(row+1)*ch-pad
                for f,uv in [((0,1,2),[(ua,va),(ub,va),(ub,vb)]),((0,2,3),[(ua,va),(ub,vb),(ua,vb)])]:
                    faces.append(tuple(start+i for i in f));uvs.append(uv)
    ob=b.mesh(rt.name+'_sod_blades',verts,faces,'GroundTrim',rt,uvs=uvs)
    ob.data.materials[0]=b.MATS['GroundFoliage']
    ob['organic_edging']=True
    return ob


def turf_strip():
    rt=b.root('Lawn_Strip')
    def z(x,y):return CURB_HEIGHT-.007+.014*math.sin(math.pi*x/STRIP)
    ob=b.rectgrid('Lawn_strip_sward',np.linspace(0,STRIP,5),np.linspace(-BAY/2,BAY/2,9),z,'Lawn',rt,
        normal=lambda x,y:Vector((-.014*math.pi/STRIP*math.cos(math.pi*x/STRIP),0,1)).normalized())
    grass_edges(rt,[[(0,-BAY/2,z(0,0)),(0,BAY/2,z(0,0))],[(STRIP,BAY/2,z(STRIP,0)),(STRIP,-BAY/2,z(STRIP,0))]],441)
    b.socket(rt,'S',(0,-BAY/2,0));b.socket(rt,'N',(0,BAY/2,0));b.socket(rt,'Curb',(0,0,0));b.socket(rt,'Walk',(STRIP,0,0))
    return rt


def turf_yard(name='Lawn_Yard',depth=LENGTH,fringe=True,span=LENGTH,drive_edge=0):
    rt=b.root(name)
    def z(x,y):return YARD_GRADE-.005+.004*x
    b.rectgrid(name+'_sward',np.linspace(0,depth,5),np.linspace(-span/2,span/2,9),z,'Lawn',rt)
    paths=[[(0,-span/2,z(0,0)),(0,span/2,z(0,0))]] if fringe else []
    if drive_edge:
        path=[(x,drive_edge*span/2,z(x,0)) for x in np.linspace(0,depth,9)]
        paths.append(list(reversed(path)) if drive_edge<0 else path)
    if paths:grass_edges(rt,paths,901+drive_edge)
    for n,p in [('Walk',(0,0,0)),('Back',(depth,0,.004*depth)),('S',(0,-span/2,0)),('N',(0,span/2,0))]:b.socket(rt,n,p)
    return rt


def turf_corner(yard=False):
    rt=b.root('Lawn_CornerYard' if yard else 'Lawn_CornerStrip')
    ri=RADIUS-CURB-STRIP-PANEL if yard else RADIUS-CURB-STRIP
    ro=0 if yard else RADIUS-CURB
    verts=[];faces=[]
    if yard:
        verts=[(0,0,YARD_GRADE-.005+.004*ri)]
        for r in np.linspace(ri/4,ri,4):
            for theta in np.linspace(0,math.pi/2,49):
                x,y=-r*math.cos(theta),-r*math.sin(theta);a=-x/ri;t=1+y/ri
                h=t*t*(3-2*t);g=t+t*t-t*t*t
                verts.append((x,y,YARD_GRADE-.005+.004*ri*(g-a*h)))
        faces=[(0,i,i+1) for i in range(1,49)]
        for row in range(3):
            for j in range(48):
                a=1+row*49+j;c=a+49
                faces.extend([(a,c,c+1),(a,c+1,a+1)])
    else:
        for t in np.linspace(0,math.pi/2,49):
            for r in (ri,(ri+ro)/2,ro):verts.append((-r*math.cos(t),-r*math.sin(t),CURB_HEIGHT-.007+(.014 if ri<r<ro else 0)))
        for j in range(48):
            for i in range(2):
                a=j*3+i;faces.extend([(a,a+4,a+3),(a,a+1,a+4)])
    normals=[]
    for x,y,z in verts:
        if yard:
            a=-x/ri;t=1+y/ri;h=t*t*(3-2*t)
            normals.append(Vector((-.004*h,-.004*((1+2*t-3*t*t)-a*6*t*(1-t)),1)).normalized())
            continue
        r=math.hypot(x,y)
        dz=-.004 if yard else .014*math.pi/STRIP*math.cos(math.pi*(r-ri)/STRIP)
        normals.append(Vector((dz*(-x/r),dz*(-y/r),1)).normalized() if r>1e-7 else Vector((0,0,1)))
    ob=b.mesh(rt.name+'_sward',verts,faces,'Lawn',rt,normals=normals)
    paths=[]
    for r in ((ri,) if yard else (ri,ro)):
        paths.append([(-r*math.cos(t),-r*math.sin(t),YARD_GRADE-.005 if yard else CURB_HEIGHT-.007) for t in np.linspace(0,math.pi/2,49)])
    grass_edges(rt,paths,739 if yard else 991)
    anchor=ri if yard else ro
    b.socket(rt,'N',(-anchor,0,0));b.socket(rt,'E',(0,-anchor,0))
    return rt


def curb_cut_z(y):
    t=max(0,min(1,(abs(y)-BAY/2)/(LENGTH/2-BAY/2)));t=t*t*(3-2*t)
    return CURB_HEIGHT*(.17+.83*t)


def apron_z(x,y):
    return curb_cut_z(y)+(CURB_HEIGHT-curb_cut_z(y))*x/STRIP


def driveway_apron():
    rt=b.root('Driveway_Apron');verts=[];faces=[]
    # Fan-shaped wings meet the *actual* transition stations of the cut curb.
    ys=transition_stations(LENGTH,BAY)
    for x in (0,.6096,STRIP-.0254,STRIP-.0127,STRIP):
        half=BAY/2+(1-x/STRIP)*BAY/2
        for y0 in ys:
            y=y0/LENGTH*2*half
            z=apron_z(x,y)
            if x>=STRIP-.0127:z-=.005
            verts.append((x,y,z))
    w=len(ys)
    for i in range(4):
        for j in range(w-1):
            a=i*w+j;faces.extend([(a,a+w,a+w+1),(a,a+w+1,a+1)])
    def normal(x,y,z):
        e=.0001;dx=(CURB_HEIGHT-curb_cut_z(y))/STRIP
        dy=(apron_z(x,y+e)-apron_z(x,y-e))/(2*e)
        return Vector((-dx,-dy,1)).normalized()
    ob=b.mesh('Driveway_apron_pour',verts,faces,'Concrete',rt,normals=[normal(*p) for p in verts])
    ob['ramp_chart']=True
    b.world_uv(ob,CONCRETE_TILE,project=b.ramp_project)
    b.joint_floor(ob,lambda p:all(ob.data.vertices[i].co.x>=STRIP-.01271 for i in p.vertices))
    # Transverse sawn scores align with the walking route's existing 5 ft rhythm.
    for y in (-PANEL/2,PANEL/2):
        b.decal(rt,'Apron_score_'+str(y),[(x,yy,apron_z(x,yy)+.001) for x,yy in [(0,y-.0016),(STRIP-.0254,y-.0016),(STRIP-.0254,y+.0016),(0,y+.0016)]],'joint')
    b.socket(rt,'Curb',(0,0,0));b.socket(rt,'Walk',(STRIP,0,0))
    return rt


def driveway_wings():
    rt=b.root('Lawn_DriveWings')
    for side in (-1,1):
        verts=[];faces=[]
        for j,x in enumerate(np.linspace(0,STRIP,9)):
            edge=BAY/2+(1-x/STRIP)*BAY/2
            # First station is a single apex, avoiding degenerate triangles.
            if j==0:verts.append((0,side*LENGTH/2,CURB_HEIGHT-.007));continue
            for y in (edge,LENGTH/2):verts.append((x,side*y,apron_z(x,y)-.007+(.014*math.sin(math.pi*x/STRIP) if y==LENGTH/2 else 0)))
        f=(0,1,2);faces.append(f if side>0 else tuple(reversed(f)))
        for j in range(7):
            a=1+j*2
            fs=[(a,a+2,a+3),(a,a+3,a+1)]
            faces.extend(fs if side>0 else [tuple(reversed(f)) for f in fs])
        b.mesh('Turf_drive_wing_'+str(side),verts,faces,'Lawn',rt)
        grass_edges(rt,[[(x,side*(BAY/2+(1-x/STRIP)*BAY/2),apron_z(x,side*(BAY/2+(1-x/STRIP)*BAY/2))-.007) for x in np.linspace(0,STRIP,9)]],930+side)
    return rt


def driveway_slab():
    rt=b.root('Driveway_Slab')
    xs=(0,.006,.012,.024,BAY-.024,BAY-.012,BAY-.006,BAY)
    ys=(-BAY/2,-BAY/2+.012,BAY/2-.012,BAY/2)
    def z(x,y):
        edge=min(x,BAY-x)
        border=min(y+BAY/2,BAY/2-y)
        return YARD_GRADE+.004*x-(.005 if edge<.007 else .0015 if edge<.025 or border<.0121 else 0)
    ob=b.rectgrid('Driveway_slab_pour',xs,ys,z,'Concrete',rt)
    b.joint_floor(ob,lambda p:all(min(ob.data.vertices[i].co.x,BAY-ob.data.vertices[i].co.x)<.007 for i in p.vertices))
    # This panel spans exactly three meters between some joint vertices;
    # modulo-one lookup would collapse their UVs onto the same texel column.
    uv=ob.data.uv_layers.active
    for p in ob.data.polygons:
        if p.material_index!=1:continue
        for li in p.loop_indices:
            v=ob.data.vertices[ob.data.loops[li].vertex_index].co
            uv.data[li].uv=(.6875+v.x*.01,.125+v.y*.01)
    for y in (-.80,.80):
        b.decal(rt,'Drive_tire_polish_'+str(y),[(x,yy,z(x,yy)+.002) for x,yy in [(.03,y-.18),(BAY-.03,y-.18),(BAY-.03,y+.18),(.03,y+.18)]],'scuff')
    b.socket(rt,'Street',(0,0,0));b.socket(rt,'Back',(BAY,0,.004*BAY));return rt


def patch_radius(t):
    """Ray intersection with one shared 64-edge resurfacing cut polygon."""
    step=math.tau/64;k=math.floor(t/step);a=k*step;c=a+step
    def p(theta):
        r=MANHOLE_PATCH/2+.009*math.sin(theta*7+.4)+.006*math.sin(theta*13)
        return np.array((r*math.cos(theta),r*math.sin(theta)))
    u=p(a);v=p(c)-u;d=np.array((math.cos(t),math.sin(t)))
    return float((u[0]*v[1]-u[1]*v[0])/(d[0]*v[1]-d[1]*v[0]))


def road_manhole():
    rt=b.root('Road_Straight_Manhole');cx=1.1
    boundary=[(x,y) for y in (-LENGTH/2,LENGTH/2) for x in np.linspace(-ASPHALT_HALF,ASPHALT_HALF,9)]
    boundary += [(x,y) for x in (-ASPHALT_HALF,ASPHALT_HALF) for y in np.linspace(-LENGTH/2,LENGTH/2,5)]
    angles=sorted(set([round(math.atan2(y,x-cx)%math.tau,10) for x,y in boundary]+[round(i*math.tau/64,10) for i in range(64)]))
    verts=[];faces=[]
    for t in angles:
        dx,dy=math.cos(t),math.sin(t)
        length=min(((ASPHALT_HALF-cx)/dx if dx>1e-10 else (-ASPHALT_HALF-cx)/dx if dx< -1e-10 else 1e6),LENGTH/2/abs(dy) if abs(dy)>1e-10 else 1e6)
        for r in (patch_radius(t),length):verts.append((cx+r*dx,r*dy,0))
    # Clip triangles at the crown before evaluating their height. No facet can
    # shortcut the crown; outer samples retain the core road's port geometry.
    def clipped(poly,positive):
        result=[]
        for a,c in zip(poly,poly[1:]+poly[:1]):
            inside=a[0]>=-1e-9 if positive else a[0]<=1e-9
            other=c[0]>=-1e-9 if positive else c[0]<=1e-9
            if inside:result.append(a)
            if inside!=other:
                f=-a[0]/(c[0]-a[0]);result.append((0,a[1]+f*(c[1]-a[1]),0))
        return result
    out=[]
    for i in range(len(angles)):
        a=i*2;c=((i+1)%len(angles))*2
        for ix in ((a,a+1,c+1),(a,c+1,c)):
            poly=[verts[j] for j in ix]
            for positive in (True,False):
                p=clipped(poly,positive)
                for j in range(1,len(p)-1):
                    pts=[p[0],p[j],p[j+1]]
                    if abs((pts[1][0]-pts[0][0])*(pts[2][1]-pts[0][1])-(pts[2][0]-pts[0][0])*(pts[1][1]-pts[0][1]))<1e-8:continue
                    start=len(out);out.extend([(x,y,b.road_z(x)) for x,y,z in pts]);faces.append((start,start+1,start+2))
    # The core's port shading interpolates from its center vertex to the first
    # 914.4 mm station. Match that authored interpolation at added edge samples.
    def portnormal(x):return Vector((math.copysign(CROWN_SLOPE,x)*min(1,abs(x)/(ASPHALT_HALF/4)),0,1)).normalized()
    b.mesh('Road_manhole_opening',out,faces,'Asphalt',rt,normals=[portnormal(x) for x,y,z in out])
    for side,y in [('S',-LENGTH/2),('N',LENGTH/2)]:b.socket(rt,side,(0,y,0))
    for side,x in [('W',-ASPHALT_HALF),('E',ASPHALT_HALF)]:b.socket(rt,side,(x,0,ROAD_EDGE))
    b.socket(rt,'Cover',(cx,0,b.road_z(cx)))
    return rt


def manhole():
    rt=b.root('Manhole');angles=sorted(set([round(i*math.tau/64,10) for i in range(64)]))
    def ring(name,rows,kind,cover=False):
        vs=[];fs=[]
        for i,t in enumerate(angles):
            for r,z in rows(t):vs.append((r*math.cos(t),r*math.sin(t),z-r*math.cos(t)*CROWN_SLOPE))
        n=len(rows(0))
        for i in range(len(angles)):
            for j in range(n-1):
                a=i*n+j;c=((i+1)%len(angles))*n+j
                fs.extend([(a,a+1,c+1),(a,c+1,c)])
        ob=b.mesh(name,vs,fs,kind,rt)
        if kind=='GroundTrim':atlas_uv(ob,'iron')
        return ob
    patch=ring('Manhole_asphalt_patch',lambda t:[(MANHOLE_FRAME/2+.003,0),(patch_radius(t),0)],'Asphalt')
    patch['tint_scale']=.77
    ring('Manhole_cast_frame',lambda t:[(.291,-.0371),(MANHOLE_COVER/2+.0016,-.0371),(MANHOLE_COVER/2+.0016,-.001),(MANHOLE_COVER/2+.0036,.0015),(MANHOLE_FRAME/2-.0015,.0015),(MANHOLE_FRAME/2+.003,0)],'GroundTrim')
    # Full 38.1 mm lid gauge and underside: they become visible during a
    # service lift. A real frame seat supports the underside at rest.
    verts=[(0,0,.001)];faces=[]
    for r,z in ((MANHOLE_COVER/2-.002,.001),(MANHOLE_COVER/2,-.001),(MANHOLE_COVER/2,-.0371)):
        for t in angles:verts.append((r*math.cos(t),r*math.sin(t),z-r*math.cos(t)*CROWN_SLOPE))
    for i in range(len(angles)):
        j=(i+1)%len(angles);faces.append((0,1+i,1+j))
        for k in range(2):
            a=1+k*len(angles)+i;c=1+k*len(angles)+j
            faces.extend([(a,a+len(angles),c+len(angles)),(a,c+len(angles),c)])
    underside=len(verts);verts.append((0,0,-.0371))
    for i in range(len(angles)):
        j=(i+1)%len(angles);faces.append((underside,1+2*len(angles)+j,1+2*len(angles)+i))
    lid=b.mesh('Manhole_Cover',verts,faces,'GroundTrim',rt);atlas_uv(lid,'manhole',MANHOLE_COVER)
    lid['service_lift_axis']='Z';lid['nominal_cast_thickness_m']=.0381
    # Sparse 24 mm cast grip lands earn geometry: at grazing view their 3 mm
    # relief casts real shadows. Micro pitting and lettering stay in the map.
    vs=[];fs=[]
    for ix in range(-4,5):
        for iy in range(-4,5):
            x,y=ix*.070,iy*.070
            if math.hypot(x,y)>.269 or abs(y)<.075 and abs(x)<.20:continue
            start=len(vs)
            for half,z in ((.012,.001),(.010,.004)):
                for dx,dy in ((-1,-1),(1,-1),(1,1),(-1,1)):
                    xx,yy=x+dx*half,y+dy*half
                    vs.append((xx,yy,z-xx*CROWN_SLOPE))
            for face in ((4,5,6),(4,6,7),(0,1,5),(0,5,4),(1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)):
                fs.append(tuple(start+i for i in face))
    pads=b.mesh('Manhole_grip_lands',vs,fs,'GroundTrim',rt);atlas_uv(pads,'manhole',MANHOLE_COVER)
    bpy.ops.object.select_all(action='DESELECT');lid.select_set(True);pads.select_set(True);bpy.context.view_layer.objects.active=lid;bpy.ops.object.join()
    # Frame and patch are one static mesh; the service lid remains separate.
    static=[o for o in rt.children_recursive if o.type=='MESH' and o!=lid]
    bpy.ops.object.select_all(action='DESELECT')
    for ob in static:ob.select_set(True)
    bpy.context.view_layer.objects.active=patch;bpy.ops.object.join()
    b.socket(rt,'Surface',(0,0,0));b.socket(rt,'Patch_E',(patch_radius(0),0,-patch_radius(0)*CROWN_SLOPE));return rt


def inlet():
    rt=b.root('Curb_StormInlet');verts=[];faces=[]
    stations=sorted(set([-BAY/2,-1.15,-.82,-.70,-.56,-.50,-.45,.45,.50,.56,.70,.82,1.15,BAY/2]))
    profile=list(b.PROFILE)
    # A station at the frame's outer lip makes the pan meet its top exactly.
    outer_z=float(np.interp(-.405,[p[0] for p in profile],[p[1] for p in profile]))
    profile.insert(1,(-.405,outer_z));count=len(profile)
    for y in stations:
        t=max(0,min(1,(abs(y)-.45)/(.70)));t=t*t*(3-2*t)
        fall=.0254*(1-t)
        for x,z in profile:
            # Keep the road/pan boundary intact; deepen only the flow line.
            f=max(0,min(1,(x+GUTTER)/.18)) if x<0 else 0
            target=float(np.interp(x,[-GUTTER,-.405,-.020],[ROAD_EDGE,-.0254,-.0254])) if x<-.020 else z-.0254*f
            verts.append((x,y,z+(target-z)*(1-t)))
    for j in range(len(stations)-1):
        for i in range(count-1):
            x0,x1=profile[i][0],profile[i+1][0]
            # Remove the grate footprint and the curb throat, including its
            # solid front. The cast box replaces this skin rather than hides it.
            if abs(stations[j])<=.45001 and abs(stations[j+1])<=.45001:continue
            a=j*count+i;faces.extend([(a,a+1,a+1+count),(a,a+1+count,a+count)])
    ob=b.mesh('Inlet_depressed_gutter',verts,faces,'Concrete',rt)
    ob['curb_chart']=True;ob['curb_curved']=False
    ns=[]
    for y in stations:
        normals=list(b.PROFILE_NORMALS);normals.insert(1,(.014,1))
        for nx,nz in normals:ns.append(Vector((nx,0,nz)).normalized())
    for p in ob.data.polygons:p.use_smooth=True
    ob.data.normals_split_custom_set_from_vertices(ns)
    # The grate/frame share the depressed flow-line elevation. Transverse
    # cast bars are 25 mm wide; 25 clear slots are 9.6 mm wide, across
    # gutter flow / bicycle travel. No long wheel-trapping longitudinal slots.
    z=-.0254
    b.rectgrid('Inlet_outer_pan',[-GUTTER,-.405],[-.45,.45],lambda x,y:ROAD_EDGE+(z-ROAD_EDGE)*(x+GUTTER)/(GUTTER-.405),'Concrete',rt)
    xs=[-.400,-.375,-.050,-.025]
    gap=(.840-24*.025)/25
    ys=[-.445,-.420]
    for i in range(25):
        ys.append(ys[-1]+gap)
        if i<24:ys.append(ys[-1]+.025)
    ys.append(.445)
    vs=[];fs=[];index={}
    def vertex(i,j,k):
        key=(i,j,k)
        if key not in index:
            index[key]=len(vs);vs.append((xs[i],ys[j],z-k*.035))
        return index[key]
    cells={(i,j) for i in range(3) for j in range(len(ys)-1)
           if i!=1 or j==0 or j==len(ys)-2 or j%2==0}
    for i,j in sorted(cells):
        for k in (0,1):
            q=[vertex(i,j,k),vertex(i+1,j,k),vertex(i+1,j+1,k),vertex(i,j+1,k)]
            fs.append(q if k==0 else list(reversed(q)))
        for di,dj,ends in [(-1,0,((i,j+1),(i,j))), (1,0,((i+1,j),(i+1,j+1))),
                           (0,-1,((i,j),(i+1,j))), (0,1,((i+1,j+1),(i,j+1)))]:
            if (i+di,j+dj) in cells:continue
            (a,c),(d,e)=ends
            fs.append([vertex(a,c,0),vertex(a,c,1),vertex(d,e,1),vertex(d,e,0)])
    grate=b.mesh('Inlet_grate_casting',vs,fs,'GroundTrim',rt)
    # Dissolve coplanar grid seams before a small foundry edge radius; bars
    # and perimeter are one connected casting, without welded intersections.
    bm=bmesh.new();bm.from_mesh(grate.data)
    bmesh.ops.dissolve_limit(bm,angle_limit=.001,verts=list(bm.verts),edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(grate.data);bm.free()
    model.bevel(grate,.0012,1);model.apply(grate);grate.data.update()
    grate['structural_casting']=True;atlas_uv(grate,'iron')
    service=bpy.data.objects.new('Inlet_Grate',None);bpy.context.collection.objects.link(service)
    service.location=(-.2125,0,z);service['service_lift_axis']='Z';service['service_lift_m']=.35
    for v in grate.data.vertices:v.co-=service.location
    grate.parent=service
    # The curb box is an 18 mm returned casting, occupying the curb's exact
    # battered / rounded section. Its cap ends at the curb back, never in sod.
    # Face-plate lower edge is at 70 mm, with the throat open underneath.
    face_z=.070
    front=b.bottom_q+(face_z-b.bottom_z)/12
    section=[(front,face_z)]+[(x,h) for x,h in profile if h>face_z]
    section += [(CURB,CURB_HEIGHT-.018),(.032,CURB_HEIGHT-.018),(front+.018,face_z)]
    # Sweep the full curb section only at the end cheeks and the returned
    # plate between them. No coincident caps or hidden overlapping solids.
    cheek=[(-.020,z)]+[(x,h) for x,h in profile if x>=b.bottom_q]+[(CURB,z)]
    inner_cheek=[(-.020,z)]+[(x,h) for x,h in profile if x>=b.bottom_q and h<face_z]
    inner_cheek += [(front,face_z),(front+.018,face_z),(.032,CURB_HEIGHT-.018),(CURB,CURB_HEIGHT-.018),(CURB,z)]
    def sweep(points,lo,hi,caps=()):
        n=len(points);vs=[(x,y,h) for y in (lo,hi) for x,h in points]
        fs=[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        if 0 in caps:fs.append(tuple(reversed(range(n))))
        if 1 in caps:fs.append(tuple(range(n,2*n)))
        ob=model.mesh('Inlet_curb_box',vs,fs,b.MATS['GroundTrim']);ob.parent=rt
        ob['surface_kind']='GroundTrim';ob['structural_casting']=True;atlas_uv(ob,'iron')
    sweep(section,-.40,.40)
    sweep(cheek,-.45,-.40,(0,));sweep(cheek,.40,.45,(1,))
    # Only the exposed lower parts of the inner cheek need caps.
    for y in (-.40,.40):
        vs=[(x,y,h) for x,h in inner_cheek]
        ob=model.mesh('Inlet_inner_cheek',vs,[tuple(range(len(vs)))],b.MATS['GroundTrim'])
        ob.parent=rt;ob['surface_kind']='GroundTrim';ob['structural_casting']=True;atlas_uv(ob,'iron')
    # Cast perimeter seat: top supports the 35 mm grate gauge. Its webs
    # return into the chamber walls; only the removable plate moves.
    vs=[];fs=[]
    outer=[(-.405,-.45),(-.020,-.45),(-.020,.45),(-.405,.45)]
    inner=[(-.388,-.429),(-.037,-.429),(-.037,.429),(-.388,.429)]
    for level in (z-.035,z-.055):
        for ring in (outer,inner):vs.extend((x,y,level) for x,y in ring)
    for i in range(4):
        j=(i+1)%4
        for quad in ((i,j,4+j,4+i),(8+i,12+i,12+j,8+j),(i,8+i,8+j,j),(4+i,4+j,12+j,12+i)):
            a,c,d,e=quad;fs.extend([(a,c,d),(a,d,e)])
    seat=b.mesh('Inlet_grate_frame_seat',vs,fs,'GroundTrim',rt)
    atlas_uv(seat,'iron');seat['structural_casting']=True
    # Narrow upper rim is flush with the pan and removable bar tops.
    for center,size in [((-.4025,0,z-.009),(.005,.90,.018)),
                        ((-.0225,0,z-.009),(.005,.90,.018)),
                        ((-.2125,-.4475,z-.009),(.375,.005,.018)),
                        ((-.2125,.4475,z-.009),(.375,.005,.018))]:
        casting_box('Inlet_flush_frame',rt,center,size,bevel=.0007)
    # Dark interior is a shallow concrete catch basin, visible through slots.
    floor=b.rectgrid('Inlet_basin_floor',[-.405,.145],[-.45,.45],lambda x,y:-.30,'Concrete',rt)
    floor['tint_scale']=.22
    for x in (-.405,.145):
        top=z-.055 if x<0 else CURB_HEIGHT-.010
        fs=[(0,1,2),(0,2,3)]
        if x>0:fs=[tuple(reversed(f)) for f in fs]
        ob=b.mesh('Inlet_basin_wall_'+str(x),[(x,-.45,-.3),(x,.45,-.3),(x,.45,top),(x,-.45,top)],fs,'GroundTrim',rt)
        atlas_uv(ob,'iron');ob['structural_casting']=True
    # The chamber's end returns are visible through the outer slot rows.
    # Leaving these open exposes the lawn/walk beyond the depressed pan.
    for y in (-.45,.45):
        # Concrete chamber walls stop below the iron cheeks/seat, rather
        # than duplicating the cast end surface at the same position.
        vs=[(-GUTTER,y,ROAD_EDGE),(-.405,y,z),(-.405,y,z-.055),
            (CURB,y,z-.055),(CURB,y,-.30),(-.405,y,-.30)]
        fs=[(0,5,1),(2,5,4),(2,4,3)]
        if y<0:fs=[tuple(reversed(f)) for f in fs]
        b.mesh('Inlet_basin_end_'+str(y),vs,fs,'Concrete',rt)
    # Fictional shallow cast lettering on the hood's horizontal top.
    p=[(.036,-.32,CURB_HEIGHT+.0003),(.146,-.32,CURB_HEIGHT+.0003),(.146,.32,CURB_HEIGHT+.0003),(.036,.32,CURB_HEIGHT+.0003)]
    label=b.decal(rt,'Inlet_foundry',p,'foundry')
    u0,v0,u1,v1=RECTS['foundry'];coords=((u0,v0),(u0,v1),(u1,v1),(u1,v0))
    for poly in label.data.polygons:
        for li in poly.loop_indices:label.data.uv_layers.active.data[li].uv=coords[label.data.loops[li].vertex_index]
    # Join fixed concrete and cast box surfaces, preserving the removable
    # grate as the only separate service mesh. The temporary pivot is outside
    # this root during consolidation, then returned to its real mating frame.
    b.consolidate(rt);service.parent=rt
    body=next(o for o in rt.children if o.type=='MESH')
    body.name='Inlet_depressed_gutter';body['surface_kind']='Concrete'
    body['tint_scale']=1.
    body['curb_chart']=True;body['curb_curved']=False
    body['inlet_returns']=True
    b.world_uv(body,CONCRETE_TILE,project=b.curb_project,material_filter=lambda m:m.name=='Concrete')
    b.inlet_return_uv(body)
    b.socket(rt,'S',(0,-BAY/2,0));b.socket(rt,'N',(0,BAY/2,0));b.socket(rt,'Curb',(0,0,0))
    rt['nominal_throat_m']=[.8,.0954];return rt


def build_modules(api):
    global b
    b=api
    narrow=RADIUS-CURB-STRIP-PANEL
    return [driveway_apron(),driveway_slab(),turf_strip(),turf_yard(),turf_yard('Lawn_Field',fringe=False),
            turf_yard('Lawn_YardNarrow',narrow,True),turf_yard('Lawn_FieldNarrow',narrow,False),
            turf_yard('Lawn_DriveSide_N',span=PANEL,drive_edge=-1),turf_yard('Lawn_DriveSide_S',span=PANEL,drive_edge=1),
            turf_corner(),turf_corner(True),driveway_wings(),inlet(),road_manhole(),manhole()]
