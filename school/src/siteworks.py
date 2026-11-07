"""School-specific grounds plus immutable instances of the library families.

No playground equipment: only its fenced reservation, approach and socket.
Open loading drives, curb-side walks and independent parent traffic replace the former stadium loops.
"""
import math,json
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
from geometry import Assembly,orient,label,H
from plans import world,FT
ROOT=Path(__file__).resolve().parents[2]
CACHE={}


def chain(ob):
    out=[]
    while ob:out.append(ob);ob=ob.parent
    return out


def library(path):
    path=Path(path).resolve()
    if path in CACHE:return CACHE[path]
    before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=str(path))
    obs=sorted(set(bpy.context.scene.objects)-before,key=lambda o:o.name);roots=[o for o in obs if o.parent not in obs]
    if path.name=='chain.glb':
        # Keep the library's exact native diamond charts. Repeated run pipes
        # do not need six modeled wire ties per ten-foot bay at site distance.
        source=next(o for o in obs if o.type=='MESH' and any(q.name=='Chain_Section' for q in chain(o)))
        rt=bpy.data.objects.new('School_ChainFabric',None);bpy.context.collection.objects.link(rt)
        cp=source.copy();cp.data=source.data.copy();bpy.context.collection.objects.link(cp);cp.parent=rt;cp.matrix_basis=Matrix.Identity(4)
        bm=bmesh.new();bm.from_mesh(cp.data)
        delete=[f for f in bm.faces if source.data.materials[f.material_index].name!='ChainLink']
        bmesh.ops.delete(bm,geom=delete,context='FACES');bm.to_mesh(cp.data);bm.free();cp.name='Native chain fabric / run LOD'
        obs += [rt,cp];roots.append(rt)
    for o in obs:o.hide_render=True;o.hide_set(True);o['library_template']=True
    CACHE[path]=(obs,roots);return obs,roots


def place(path,name,p=(0,0,0),yaw=0,select=None,parent=None):
    obs,roots=library(path)
    if select:
        candidates=[o for o in obs if o.name.split('.')[0]==select]
        if not candidates:raise ValueError((path,select,[o.name for o in roots]))
        rt=candidates[0];chosen=[o for o in obs if rt in chain(o)];base=rt.matrix_world.inverted()
    else:
        chosen=list(obs);base=Matrix.Identity(4)
    rt=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(rt);rt.parent=parent
    srcpath=Path(path);srcpath=srcpath.relative_to(ROOT) if srcpath.is_absolute() else srcpath
    rt.location=p;rt.rotation_euler.z=math.radians(yaw);rt['library_source']=str(srcpath);rt['static_root']=True
    copies={o:o.copy() for o in chosen}
    for src,cp in copies.items():
        bpy.context.collection.objects.link(cp);cp.name=name+'__'+src.name;cp.parent=copies.get(src.parent,rt)
        cp.matrix_basis=src.matrix_basis.copy() if src.parent in copies else base@src.matrix_world
        cp.hide_render=False;cp.hide_set(False);cp.pop('library_template',None)
        cp['site_instance']=name
    return rt


def clear_templates():
    for obs,roots in CACHE.values():
        for ob in obs:
            if ob.name in bpy.data.objects:bpy.data.objects.remove(ob,do_unlink=True)
    CACHE.clear()


def rectangle(m,rect,z,role='Concrete',color=None):
    m.props['authored_winding']=True
    l,r,f,k=rect
    pts=[(l,f,z),(r,f,z),(r,k,z),(l,k,z)]
    m.geom(pts,[(0,1,2,3)],role,color)
    if z>.011:
        for j in range(4):
            aa,bb=pts[j],pts[(j+1)%4]
            m.geom([aa,bb,(bb[0],bb[1],-.025),(aa[0],aa[1],-.025)],[(3,2,1,0)],role,color)


def entry_height(p,y):
    return p['floor']+(.1704-p['floor'])*min(1,max(0,(p['entry'][1]-y)/(p['entry'][1]-p['bus_curb'][0][1])))


def grounded_slab(m,points,depth=.18,role='Concrete'):
    # Gauged sides meet buried fill. The invisible buried bottom is omitted.
    start=len(m.f);m.prism(points,(0,0,-1),depth,role)
    if len(m.f)>start+1:m.f.pop(start+1);m.mat.pop(start+1)


def stadium(s,radius=None):
    R=s['radius'] if radius is None else radius;half=s['straight'];pts=[]
    for cx,start in ((half,-math.pi/2),(-half,math.pi/2)):
        for i in range(25):
            a=start+i*math.pi/24;pt=world((cx+R*math.cos(a),R*math.sin(a),0),s['center'],s['yaw']);pts.append(pt[:2])
    return pts


def convex_cuts(poly):
    # CCW polygon interior is the left halfspace of every edge.
    return [(a[1]-b[1],b[0]-a[0],a[0]*b[1]-b[0]*a[1]) for a,b in zip(poly,poly[1:]+poly[:1])]


def ground_material(role):
    from kit.tiling import material
    # Let Blender 5.2 create the complete settings interface before the kit's
    # compatible occlusion-only fallback would be needed in an empty scene.
    from io_scene_gltf2.blender.imp.pbrMetallicRoughness import get_settings_group
    get_settings_group()
    prefix={'Asphalt':'Asphalt','Concrete':'Concrete','Siding':'Lawn'}[role]
    name='SchoolGround_'+prefix
    ma=bpy.data.materials.get(name)
    if ma is None:ma=material(prefix,ROOT/'ground/textures/ship',tint=True);ma.name=name
    return ma


def ground_finish(ob,role):
    from kit.tiling import world_uv
    if not ob:return
    # These are exposed ground skins, with buried bottoms deliberately absent.
    # Independent route ribbons must face up on both sides of a centerline.
    bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<-.01])
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    ma=ground_material(role);ob.data.materials.clear();ob.data.materials.append(ma)
    for f in ob.data.polygons:f.material_index=0
    world_uv(ob,6.096 if role=='Asphalt' else 3.048)
    uv=ob.data.uv_layers.active
    for f in ob.data.polygons:
        if abs(f.normal.z)>.5:continue
        axes=sorted(range(3),key=lambda k:abs(f.normal[k]))[:2];axes.sort()
        for li in f.loop_indices:
            v=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
            uv.data[li].uv=(v[axes[0]]/3.048,v[axes[1]]/3.048)
    attr=ob.data.color_attributes.get('Tint')
    if attr:
        for row in attr.data:row.color=(.48,.48,.47,1) if role=='Asphalt' else (.85,.85,.83,1) if role=='Concrete' else (.62,.68,.58,1)


def round_route(points,radius=10.5):
    """Open driveway centerline with straight tangents and eased bends."""
    pts=[Vector((*q,0)) for q in points];out=[pts[0]]
    for a,b,c in zip(pts,pts[1:],pts[2:]):
        incoming=(b-a).normalized();outgoing=(c-b).normalized()
        angle=math.acos(max(-1,min(1,incoming.dot(outgoing))))
        # A quadratic's minimum radius at its midpoint is d*cos²(h)/sin(h).
        # Trim to the requested physical radius, bounded by adjacent runs.
        half=angle/2;wanted=radius*math.sin(half)/max(.05,math.cos(half)**2)
        d=min(wanted,(b-a).length*.45,(c-b).length*.45)
        if d<.001:out.append(b);continue
        u=b+(a-b).normalized()*d;v=b+(c-b).normalized()*d
        out.append(u)
        for i in range(1,9):
            t=i/8;out.append((1-t)**2*u+2*t*(1-t)*b+t*t*v)
    out.append(pts[-1]);return out


def open_drive(a,points,name,cuts,width=7.3152,openings=()):
    points=[list(q) for q in points]
    for q in (points[0],points[-1]):
        if abs(q[1]+89.7)<.1:q[1]+=3.6576
        elif abs(q[0]-108)<.1:q[0]-=3.6576
    pts=round_route(points,10.5 if name.startswith('Bus') else 5.5);left=[];right=[]
    for j,q in enumerate(pts):
        t=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized();n=Vector((-t.y,t.x,0))
        left.append(q+n*width/2);right.append(q-n*width/2)
    m=a.mesh(name+'_paving',component='site',solid=False)
    for j in range(len(pts)-1):
        poly=[tuple(v[:2]) for v in (right[j],right[j+1],left[j+1],left[j])]
        m.geom([(x,y,.018) for x,y in poly],[(0,1,2,3)],'Concrete');cuts.append(poly)
    paving=m.finish();segment=paving.data.attributes.new('RouteSegment','INT','FACE')
    segment.data.foreach_set('value',list(range(len(pts)-1)));ground_finish(paving,'Asphalt')
    curb=a.mesh(name+'_curb_gutter',component='site',solid=False,authored_winding=True)
    segments=[];face_kinds=[]
    for side in (-1,1):
        edge=right if side<0 else left
        included=[not any(l<((edge[j]+edge[j+1])/2).x<r and f<((edge[j]+edge[j+1])/2).y<k for l,r,f,k in openings) for j in range(len(pts)-1)]
        for j in range(len(pts)-1):
            if not included[j]:continue
            first_face=len(curb.f)
            # Street intersections/aprons taper from grade without closing the
            # roadway. The first/last four meters remain flush.
            verts=[]
            for k in (j,j+1):
                tangent=(pts[min(k+1,len(pts)-1)]-pts[max(0,k-1)]).normalized();n=Vector((-tangent.y,tangent.x,0))*side
                end=min((pts[k]-pts[0]).length,(pts[k]-pts[-1]).length)
                z=.018+.1524*min(1,end/4)
                verts += [(edge[k].x,edge[k].y,.018),tuple((edge[k]+n*.4572)[:2])+(z,),tuple((edge[k]+n*.6096)[:2])+(z,)]
            faces=[(0,3,4,1),(1,4,5,2)]
            curb.geom(verts,[q if side>0 else tuple(reversed(q)) for q in faces],'Concrete')
            # The curb's back is a real vertical face down to soil. The old
            # two-face ribbon left a 174 mm open slit all along its outer edge.
            curb.geom([verts[2],verts[5],(verts[5][0],verts[5][1],-.025),(verts[2][0],verts[2][1],-.025)],[(0,1,2,3) if side>0 else (3,2,1,0)],'Concrete')
            for at,sign,exposed in ((0,-1,j==0 or not included[j-1]),(3,1,j==len(pts)-2 or not included[j+1])):
                if not exposed:continue
                aa,bb,cc=verts[at:at+3]
                cap=[aa,bb,cc,(cc[0],cc[1],-.025),(aa[0],aa[1],-.025)]
                normal=sum((Vector(u).cross(Vector(v)) for u,v in zip(cap,cap[1:]+cap[:1])),Vector())
                outward=(pts[j+1]-pts[j])*sign
                ids=tuple(range(5))
                curb.geom(cap,[ids if normal.dot(outward)>0 else tuple(reversed(ids))],'Concrete')
            poly=[tuple(v[:2]) for v in (edge[j],edge[j+1])]
            # Turf cut accounts for the actual curb/gutter footprint.
            nn=(edge[j]-pts[j]).normalized()*.6096;mm=(edge[j+1]-pts[j+1]).normalized()*.6096
            q=[poly[0],poly[1],tuple((edge[j+1]+mm)[:2]),tuple((edge[j]+nn)[:2])]
            if sum(x*yy-xx*y for (x,y),(xx,yy) in zip(q,q[1:]+q[:1]))<0:q.reverse()
            cuts.append(q)
            segments.extend([j]*(len(curb.f)-first_face))
            face_kinds.extend([0,0,1]+[2]*(len(curb.f)-first_face-3))
    curb_ob=curb.finish();segment=curb_ob.data.attributes.new('RouteSegment','INT','FACE')
    segment.data.foreach_set('value',segments)
    kind=curb_ob.data.attributes.new('CurbFaceKind','INT','FACE');kind.data.foreach_set('value',face_kinds)
    ground_finish(curb_ob,'Concrete')
    return pts


def line(m,points,width=.075,color=(.48,.46,.35),role='Trim',z=.031):
    for a,b in zip(points,points[1:]):
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
        if length<1e-6:continue
        nx,ny=-dy/length*width/2,dx/length*width/2
        m.geom([(a[0]+nx,a[1]+ny,z),(a[0]-nx,a[1]-ny,z),(b[0]-nx,b[1]-ny,z),(b[0]+nx,b[1]+ny,z)],[(0,1,2,3)],role,color)


def hoop(a,x,y,sy):
    m=a.mesh('Basketball_'+str(x)+'_'+str(y),component='hoop')
    # 4in schedule pipe, braced gooseneck, 6x3.5ft steel backboard, 18in ring.
    m.tube([(x,y,0),(x,y,3.15),(x,y+sy*.55,3.55),(x,y+sy*1.10,3.55)],.05715,'Trim',(.22,.24,.20),sides=10)
    m.box((x,y+sy*1.12,3.45),(1.8288,.06,1.0668),'Trim',(.59,.59,.53),r=.008)
    m.box((x,y+sy*1.15,3.07),(.50,.10,.035),'Trim',(.31,.07,.025))
    m.tube([(x+.2286*math.cos(j*math.tau/24),y+sy*(1.15+.2286)+.2286*math.sin(j*math.tau/24),3.048) for j in range(25)],.010,'Trim',(.31,.07,.025),sides=6)
    for j in range(12):
        ang=j*math.tau/12
        m.tube([(x+.218*math.cos(ang),y+sy*(1.15+.2286)+.218*math.sin(ang),3.038),(x+.115*math.cos(ang+.12),y+sy*(1.15+.2286)+.115*math.sin(ang+.12),2.68)],.0024,'Trim',(.49,.49,.43),sides=4)
    # Construction above uses local +Y as its backboard normal. The court's
    # long axis is X: rotate the complete original hoop, not only its pole.
    m.v=[(x+(yy-y),y-(xx-x),zz) for xx,yy,zz in m.v]
    m.finish()


def fence_run(a,start,end,name,height=1.8288):
    dx,dy=end[0]-start[0],end[1]-start[1];length=math.hypot(dx,dy);yaw=math.degrees(math.atan2(dy,dx));n=max(1,round(length/3.048));pitch=length/n
    path=Path('build/context/chain.glb')
    # Native fabric diamonds remain their true size. Custom-length runs use
    # native bays; end points are deliberately designed on the 10ft grid.
    assert abs(pitch-3.048)<.002,(name,pitch)
    for i in range(n):place(path,name+'_Bay_'+str(i),(start[0]+dx*(i+.5)/n,start[1]+dy*(i+.5)/n,0),yaw,'School_ChainFabric',a.root)
    m=a.mesh(name+'_Run_pipes',component='fence')
    m.tube([(*start,1.78),(*end,1.78)],.0211,'Trim',ALUM(),sides=8)
    m.tube([(*start,.095),(*end,.095)],.002,'Trim',ALUM(),sides=4)
    for i in range(n+1):
        x,y=start[0]+dx*i/n,start[1]+dy*i/n
        m.tube([(x,y,.018),(x,y,1.86)],.0302,'Trim',ALUM(),sides=8)
        m.tube([(x,y,1.85),(x,y,1.88)],.034,'Trim',ALUM(),sides=8)
    m.finish()


def flagpole(a,p):
    x,y=p;m=a.mesh('Flagpole',component='flagpole')
    m.box((x,y,.09),(.65,.65,.18),'Concrete',r=.02)
    # True tapered aluminum tube, flash collar, cleat, pulley and slack halyard.
    for z0,z1,r0,r1 in ((.18,4.0,.075,.054),(4.,8.2,.054,.031)):
        verts=[]
        for z,r in ((z0,r0),(z1,r1)):
            verts.extend((x+r*math.cos(i*math.tau/12),y+r*math.sin(i*math.tau/12),z) for i in range(12))
        m.geom(verts,[(i,(i+1)%12,(i+1)%12+12,i+12) for i in range(12)],'Trim',(.38,.40,.37))
    m.tube([(x,y,.19),(x,y,.26)],.10,'Trim',ALUM(),sides=16)
    m.tube([(x-.07,y,7.95),(x-.10,y,4.0),(x-.08,y,1.2),(x-.15,y,1.05),(x-.22,y,1.20),(x-.11,y,4.0),(x-.07,y,7.95)],.003,'Trim',(.49,.47,.39),sides=5)
    m.box((x-.085,y,1.18),(.035,.12,.025),'Trim',ALUM(),r=.003)
    m.finish()
    pivot=a.pivot('Flag_on_halyard',(x-.07,y,7.95),axis='Z',limits=(-60,60));pivot['motion_kind']='flag yaw; halyard lowering via socket'
    pivot['slide_axis']='Z';pivot['range_m']=(-6.2,0)
    fl=a.mesh('Fictional_district_flag',part=pivot.name,component='flag',solid=False)
    # Authored resting cloth: 1.83 x 1.22m, gravity sag between winded folds.
    nx,ny=20,12;verts=[]
    for j in range(ny+1):
        for i in range(nx+1):
            u,v=i/nx,j/ny;verts.append((x-.07-u*1.83,y+.10*math.sin(u*11-v*2)*u,7.90-v*1.22-.21*u*u+.07*math.sin(u*8+v*3)*u))
    for j in range(ny):
        for i in range(nx):
            ids=(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i)
            fl.geom([verts[k] for k in ids],[(0,1,2,3)],'Trim',(.14,.22,.28) if j<8 else (.51,.47,.29))
    fl.finish();a.socket('Flag_halyard',(x-.07,y,7.95),'halyard')


def ALUM():return (.34,.36,.34)


def portable(a,x,y,yaw,index):
    from buildings import wall_panel,door,glazing
    m=a.mesh('Portable_'+str(index),component='portable');w,d=7.3152,9.7536
    # Raised transportable, skirt joints, metal panel edges and low gable.
    m.box((0,0,.35),(w,d,.70),'Trim',(.16,.15,.12))
    for face,org,angle,width in [('S',(-w/2,-d/2),0,w),('N',(w/2,d/2),180,w),('E',(w/2,-d/2),90,d),('W',(-w/2,d/2),270,d)]:
        openings=[dict(u=width/2+sgn*1.75,w=1.55,z=1.58,h=1.10) for sgn in (-1,1)] if face in ('S','N') else [dict(u=.95,w=1.0668,z=.70,h=2.1844)] if face=='E' else []
        pos=world((*org,0),(x,y),yaw);wall_panel(a,'Portable_'+str(index)+'_'+face,pos,yaw+angle,width,.70,3.40,openings,'Siding',.10)
        for j,o in enumerate(openings):
            definition=dict(o,origin=pos[:2],yaw=yaw+angle,type='door' if face=='E' else 'window')
            b=dict(id='Portable_'+str(index),era=1994,kind='portable')
            if face=='E':door(a,b,definition,j,base=.70)
            else:
                definition['z']-=.1524;glazing(a,b,definition,j)
    for sy in (-1,1):m.prism([(-w/2-.25,sy*(d/2+.25),3.42),(w/2+.25,sy*(d/2+.25),3.42),(w/2+.25,0,3.82),(-w/2-.25,0,3.82)],(0,0,-1),.12,'Shingles')
    for xx in range(-3,4):m.box((xx,-d/2-.061,2.05),(.016,.025,2.67),'Trim',(.23,.22,.17))
    # Landing / ramp at 1:12, both landings, toe curbs and 36in handrails.
    top=.70;bottom=.1524;run=12*(top-bottom);start=-d/2-1.75;end=start-run
    m.box((w/2+.94,-d/2+.025,top/2),(1.88,3.55,top),'Concrete')
    m.box((w/2+.94,end-.762,bottom/2),(1.88,1.524,bottom),'Concrete')
    # The lower landing stays at the school walk datum; a separate gentle
    # approach meets actual site grade, avoiding a six-inch step at its end.
    q=[(w/2,end-1.524,bottom),(w/2+1.88,end-1.524,bottom),(w/2+1.88,end-1.524-2.7432,.018),(w/2,end-1.524-2.7432,.018)]
    m.geom(q+[(xx,yy,-.004) for xx,yy,zz in q],[(0,1,2,3)]+[(j,(j+1)%4,(j+1)%4+4,j+4) for j in range(4)],'Concrete')
    for xx in (w/2,w/2+1.88):
        m.beam((xx,start,top),(xx,end,bottom),.08,.12,'Trim',ALUM(),r=0)
        m.tube([(xx,start+.305,top+.9144),(xx,start,top+.9144),(xx,end,bottom+.9144),(xx,end-.305,bottom+.9144)],.021,'Trim',ALUM(),sides=8)
        for j in range(9):
            yy=start-j*run/8;z=top-j*(top-bottom)/8
            m.tube([(xx,yy,z),(xx,yy,z+.91)],.018,'Trim',ALUM(),sides=6)
            if j in (2,4,6):
                m.box((xx,yy,(z-.10)/2),(.075,.075,z-.10),'Trim',ALUM())
                m.box((xx,yy,.025),(.24,.24,.05),'Concrete')
    m.prism([(w/2,start,top),(w/2+1.88,start,top),(w/2+1.88,end,bottom),(w/2,end,bottom)],(0,0,-1),.10,'Concrete')
    # The high landing has a guard on its open outer side. The doorway side
    # remains clear; source door component retains its physical outer hinge.
    for yy in (-d/2+1.8,start):
        m.tube([(w/2+1.88,yy,top),(w/2+1.88,yy,top+1.0668)],.022,'Trim',ALUM(),sides=6)
    m.tube([(w/2+1.88,start,top+1.0668),(w/2+1.88,-d/2+1.8,top+1.0668)],.022,'Trim',ALUM(),sides=6)
    for j in range(35):
        yy=start+j*3.55/34;m.tube([(w/2+1.88,yy,top+.08),(w/2+1.88,yy,top+1.03)],.008,'Trim',ALUM(),sides=4)
    orient(m,(x,y,0),yaw).finish()
    a.socket('Portable_'+str(index)+'_Ramp',world((w/2+.94,end-1.524-2.7432,.018),(x,y),yaw),'portable_ramp',yaw)


def build_site(p,building):
    a=Assembly('Campus_'+str(p['seed']));building.root.parent=a.root;a.root['seed']=p['seed'];a.root['lot_m']=p['lot']
    cuts=[]
    open_drive(a,p['bus_route'],'Bus_loading_lane',cuts)
    open_drive(a,p['parent_route'],'Parent_one_way',cuts,openings=[p['parking'],*p['parking_aprons']])
    ex,ey=p['entry']
    # Loading curb and sheltered entrance share one continuous paved forecourt.
    # No lawn strip between a waiting child and the bus step.
    c0,c1=p['bus_curb'];plaza=(min(c0[0],ex-7),max(c1[0],ex+7),c0[1],ey)
    m=a.mesh('Entry_plaza',component='site',solid=False)
    parts=[rect_poly(plaza)]
    for b in p['blocks']:
        parts=[q for poly in parts for q in H.subtract(poly,convex_cuts(rect_poly(b['rect'])))]
    for x,y,radius in p['tree_wells']:
        hole=[(x+radius*math.cos(j*math.tau/16),y+radius*math.sin(j*math.tau/16)) for j in range(16)]
        parts=[q for poly in parts for q in H.subtract(poly,convex_cuts(hole))]
        mulch=a.mesh('Entry_tree_well',component='site',solid=False,trim_cell=10)
        mulch.geom([(xx,yy,.003) for xx,yy in hole],[tuple(range(16))],'Trim',(.050,.028,.012));mulch.finish();cuts.append(hole)
    for poly in parts:grounded_slab(m,[(x,y,entry_height(p,y)) for x,y in poly]);cuts.append(poly)
    ground_finish(m.finish(),'Concrete')
    joints=a.mesh('Entry_plaza_pour_joints',component='site',solid=False,trim_cell=4)
    for station in range(math.floor(plaza[0]/1.524),math.ceil(plaza[1]/1.524)):
        x=station*1.524
        for poly in parts:
            q=H.clip(H.clip(poly,1,0,-x+.005),-1,0,x+.005)
            if len(q)>=3:joints.geom([(xx,yy,entry_height(p,yy)+.0007) for xx,yy in q],[tuple(range(len(q)))],'Trim',(.12,.12,.105))
    joints.finish()
    if p['type']=='finger':
        rect=(-45.3424,-41.73,-8.5,19.8);m=a.mesh('Parent_curb_walk',component='site',solid=False)
        grounded_slab(m,[(x,y,p['floor']+(.1704-p['floor'])*(rect[1]-x)/(rect[1]-rect[0])) for x,y in rect_poly(rect)]);ground_finish(m.finish(),'Concrete');cuts.append(rect_poly(rect))
    if p['type']!='finger':
        (x0,y0),(x1,y1)=p['parent_curb'];rect=(x0,x1,y0,y0+1.524)
        m=a.mesh('Parent_loading_walk',component='site',solid=False);grounded_slab(m,[(x,y,.1704) for x,y in rect_poly(rect)]);ground_finish(m.finish(),'Concrete');cuts.append(rect_poly(rect))
    # Bus sockets reserve empty 11m loading positions; no invented bus mesh.
    for j in range(p['bus_bays']):
        total=p['bus_bays']*11+(p['bus_bays']-1)
        x=c0[0]+((c1[0]-c0[0])-total)/2+5.5+j*12;y=c0[1]-1.55
        a.socket('Bus_loading_'+str(j),(x,y,.018),'school_bus_11m',-90)
    text=floor_text(a,'BUS ONLY',(c0[0]+c1[0])/2,c0[1]-3.9,.55,(.31,.29,.20));text.rotation_euler.z=math.pi/2
    sx,sy=p['bus_route'][-1]
    if abs(sy+89.7)<1:
        text=floor_text(a,'STOP',sx,-80,.60,(.37,.36,.30));text.rotation_euler.z=math.pi
    # A reinstated underground-service trench crosses the loading pavement.
    # Its dark wearing course and iron inspection lid explain the straight
    # patch; this is not random dirt painted over the whole road.
    rx=c0[0]+4;ry=c0[1]
    patch=a.mesh('Loading_utility_reinstatement',component='site',solid=False)
    patch.geom([(rx-.46,ry-7.10,.027),(rx+.57,ry-7.01,.027),(rx+.44,ry-.12,.027),(rx-.51,ry-.18,.027)],[(0,1,2,3)],'Concrete')
    ob=patch.finish();ground_finish(ob,'Asphalt')
    for row in ob.data.color_attributes['Tint'].data:row.color=(.29,.29,.28,1)
    cover=a.mesh('Service_inspection_lid',component='site')
    cover.tube([(rx,ry-1,.028),(rx,ry-1,.044)],.18,'Trim',(.065,.068,.062),sides=16)
    for dx in (-.06,.06):cover.box((rx+dx,ry-1,.045),(.028,.075,.008),'Trim',(.022,.024,.021))
    cover.finish()
    if p['type']=='compact':a.socket('Bus_queue',(76,-75,.018),'school_bus_11m_waiting',180)
    a.socket('Bus_entry',(*p['bus_route'][0],.018),'bus_entry')
    a.socket('Parent_entry',(*p['parent_route'][0],.018),'parent_entry')
    # Staff lot: 9x18ft stalls, 24ft aisle, one reserved van bay/aisle.
    l,r,f,k=p['parking'];m=a.mesh('Staff_paving',component='site',solid=False);rectangle(m,p['parking'],.018);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(p['parking']))
    m=a.mesh('Staff_markings',component='site',solid=False)
    front_start=l+4.8768;front_count=max(1,int((r-front_start)/2.7432));back_count=max(1,int((r-l)/2.7432));p['staff_stalls']=1+front_count+back_count
    for i in range(front_count+1):line(m,[(front_start+i*2.7432,f),(front_start+i*2.7432,f+5.4864)],.10,(.53,.52,.46))
    for xx in (l,l+3.3528):line(m,[(xx,f),(xx,f+5.4864)],.10,(.53,.52,.46))
    for i in range(back_count+1):line(m,[(l+i*2.7432,k-5.4864),(l+i*2.7432,k)],.10,(.53,.52,.46))
    for j in range(6):line(m,[(l+3.3528+j*.20,f),(l+3.3528+j*.20+.35,f+5.4864)],.07,(.45,.45,.40))
    m.finish()
    for rect in p['parking_aprons']:
        m=a.mesh('Staff_driveway_apron',component='site',solid=False);rectangle(m,rect,.018);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(rect))
    # Staff parking joins the independent parent route; its curb is the
    # second unloading frontage rather than a duplicate bus stadium.
    # Service yard at the kitchen's outside door. A straight side lane links
    # the public frontage without crossing the playground reservation.
    kitchen=next(b for b in p['blocks'] if b['kind']=='kitchen');kl,kr,kf,kk=kitchen['rect']
    offset=7
    side=-1 if p['type']=='courtyard' else 1
    base=kl if side<0 else kr
    outward=lambda d:base+side*d
    yard=(min(base,outward(offset+6.5)),max(base,outward(offset+6.5)),kf-2,kk+4)
    m=a.mesh('Service_yard',component='site',solid=False);rectangle(m,yard,.025);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(yard))
    service=(min(outward(offset),outward(offset+6)),max(outward(offset),outward(offset+6)),-52,kf-1.98)
    m=a.mesh('Service_drive',component='site',solid=False);rectangle(m,service,.019);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(service))
    m=a.mesh('Service_dock',component='service');m.box((outward(1),kk-2,.18),(2,3,.36),'Concrete',r=.006)
    for yy in (kk-3.0,kk-1.0):m.box((outward(2.015),yy,.29),(.045,.25,.40),'Trim',DARK())
    dx,dy=outward(7),kk+1
    for sx in (-1,1):m.box((dx+sx*2.0,dy,1.0),(.20,3.4,2.0),'Siding')
    m.box((dx,dy+1.7,1.0),(4.2,.20,2.0),'Siding')
    m.box((dx,dy,.74),(2.7,1.45,1.48),'Trim',(.075,.13,.09),r=.04)
    m.box((dx,dy,1.52),(2.80,1.52,.14),'Trim',DARK(),r=.015)
    m.finish()
    for sx in (-1,1):
        pv=a.pivot('Dumpster_gate_'+str(sx),(dx+sx*2,dy-1.7,0),limits=(-110,0) if sx<0 else (0,110))
        m=a.mesh('Gate_leaf',part=pv.name,component='gate')
        for z in (.15,1.8):m.box((dx+sx*1,dy-1.7,z),(1.98,.065,.065),'Trim',r=.003)
        for j in range(15):m.box((dx+sx*(.07+j*.13),dy-1.7,.98),(.115,.04,1.6),'Trim',r=.002)
        m.finish()
    # A marked asphalt court / four square / hopscotch, with two hoops.
    l,r,f,k=p['blacktop'];m=a.mesh('Blacktop',component='site',solid=False);rectangle(m,p['blacktop'],.025);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(p['blacktop']))
    if p['type']=='finger':
        # An L apron touches the original fingers and later cross wing. Clip
        # its notch at actual walls; grass does not divide the exit from play.
        parts=[rect_poly((-18.7,29,19.84,30.2))]
        for b in p['blocks']:parts=[q for poly in parts for q in H.subtract(poly,convex_cuts(rect_poly(b['rect'])))]
        m=a.mesh('Blacktop_classroom_apron',component='site',solid=False)
        for q in parts:m.geom([(x,y,.025) for x,y in q],[tuple(range(len(q)))],'Concrete');cuts.append(q)
        ground_finish(m.finish(),'Asphalt')
    m=a.mesh('Game_lines',component='site',solid=False);cx,cy=(l+r)/2,(f+k)/2
    court_x=l+16;court=(court_x-12.8016,court_x+12.8016,cy-7.62,cy+7.62)
    aa,bb,cc,dd=court;line(m,[(aa,cc),(bb,cc),(bb,dd),(aa,dd),(aa,cc)],.07)
    line(m,[(court_x,cc),(court_x,dd)],.07);line(m,[(court_x+1.8*math.cos(t*math.tau/48),cy+1.8*math.sin(t*math.tau/48)) for t in range(49)],.065)
    for xx,sign in ((aa,1),(bb,-1)):
        line(m,[(xx,cy-1.8),(xx+sign*4.57,cy-1.8),(xx+sign*4.57,cy+1.8),(xx,cy+1.8)],.065)
        hoop(a,xx-sign*1.25,cy,sign)
    # Four-square court occupies its own rear-side apron, with finite lines.
    line(m,[(l+.6,f+.6),(l+3.6,f+.6),(l+3.6,f+3.6),(l+.6,f+3.6),(l+.6,f+.6)],.06)
    line(m,[(l+2.1,f+.6),(l+2.1,f+3.6)],.06);line(m,[(l+.6,f+2.1),(l+3.6,f+2.1)],.06);m.finish()
    # Playground reservation on the native fence pitch, gate gap at its entry.
    pl,pr,pf,pk=p['playground'];pr=pl+7*3.048;pk=pf+5*3.048;p['playground']=(pl,pr,pf,pk)
    for n,start,end in [('Rear',(pl,pk),(pr,pk)),('Left',(pl,pf),(pl,pk)),('Right',(pr,pf),(pr,pk)),('FrontA',(pl,pf),(pl+3*3.048,pf)),('FrontB',(pl+4*3.048,pf),(pr,pf))]:fence_run(a,start,end,'Playground_'+n)
    place('build/context/chain.glb','Playground_gate',(pl+3.5*3.048,pf,0),0,'Chain_GateBay',a.root)
    for sign in (-1,1):place('build/context/chain.glb','Gate_infill_'+str(sign),(pl+3.5*3.048+sign*(1.069975/2+(3.048-1.069975)/4),pf,0),0,'Chain_InfillShort',a.root)
    a.socket('Playground',((pl+pr)/2,(pf+pk)/2,0),'playground_clear_reservation')
    a.root['playground_reservation_m']=(pr-pl,pk-pf)
    m=a.mesh('Playground_base',component='site',solid=False);rectangle(m,(pl,pr,pf,pk),.013,'Concrete',(.19,.15,.088));m.finish();cuts.append(rect_poly((pl,pr,pf,pk)))
    # Ballfield: native chain fabric backstop wings, 60ft base paths in dirt.
    fx,fy=p['field'];m=a.mesh('Ballfield',component='field',solid=False)
    pts=[(fx,fy)]+[(fx+24*math.cos(math.radians(t)),fy+24*math.sin(math.radians(t))) for t in range(0,91,3)]
    m.geom([(x,y,.010) for x,y in pts],[tuple(range(len(pts)))],'Concrete',(.23,.17,.09));m.finish();cuts.append(pts)
    field=a.mesh('Field_markings',component='field',solid=False)
    line(field,[(fx,fy),(fx+24,fy)],.055,(.48,.47,.38),z=.013);line(field,[(fx,fy),(fx,fy+24)],.055,(.48,.47,.38),z=.013)
    for x,y in ((fx+18.288,fy),(fx,fy+18.288),(fx+18.288,fy+18.288)):field.box((x,y,.025),(.38,.38,.04),'Trim',(.50,.49,.42),r=.018)
    # Tall upper backstop fabric uses stacked native panels at municipal pitch.
    for n,s,e in [('BackA',(fx-3.048,fy-3.048),(fx+3.048,fy-3.048)),('BackB',(fx-3.048,fy-3.048),(fx-3.048,fy+3.048))]:
        fence_run(a,s,e,n)
        for j in range(2):
            pos=(s[0]+(e[0]-s[0])*(j+.5)/2,s[1]+(e[1]-s[1])*(j+.5)/2,1.8288)
            place('build/context/chain.glb',n+'_Upper_'+str(j),pos,0 if e[0]!=s[0] else 90,'Chain_Section',a.root)
        for j in range(3):
            x=s[0]+(e[0]-s[0])*j/2;y=s[1]+(e[1]-s[1])*j/2
            field.tube([(x,y,0),(x,y,3.70)],.0302,'Trim',ALUM(),sides=8)
    field.finish()
    # Native mature species and foundation shrubs, with a different planted
    # rhythm on each parcel. More native trees continue in presentation context.
    flagpole(a,(ex-8,ey-4.3))
    for j in range(3):place('build/context/furniture.glb','Bike_rack_'+str(j),(ex+8+j*1.05,ey-2,.1704),0,'BikeRack',a.root)
    place('build/context/furniture.glb','Entry_bench',(ex-4,ey-2,.1704),0,'Bench',a.root)
    for j,(x,y) in enumerate(p['trees'][:5]):place(ROOT/'trees/export'/('RedMaple.glb' if j%2==0 else 'PinOak.glb'),'Mature_tree_'+str(j),(x,y,0),p['seed']*17+j*73,parent=a.root)
    for j,(x,y) in enumerate(p['shrubs'][:4]):place('build/context/shrub.glb','Foundation_shrub_'+str(j),(x,y,0),j*43,parent=a.root)
    planting_beds(a,p,cuts)
    for j,(x,y,yaw) in enumerate(p['portables']):portable(a,x,y,yaw,j)
    # One existing library pole serves the small staff lot. Period is 2010 for
    # this presentation, allowing the library's LED retrofit cobra head.
    l,r,f,k=p['parking'];place('build/context/light.glb','Staff_lot_light',(r+1.0,k-1.0,0),-90,parent=a.root)
    pedestrian_network(a,p,cuts)
    amenities(a,p,cuts)
    streets(a,p,cuts)
    # All lawn is clipped around the actual building and site slabs.
    cuts += [rect_poly(b['rect']) for b in p['blocks']]+[rect_poly(c['rect']) for c in p['covered']]
    W,D=p['lot'];parts=[rect_poly((-W/2,W/2,-D/2,D/2))]
    for poly in cuts:
        constraints=convex_cuts(poly)
        xl,xh=min(v[0] for v in poly),max(v[0] for v in poly);yl,yh=min(v[1] for v in poly),max(v[1] for v in poly)
        result=[]
        for piece in parts:
            if max(v[0] for v in piece)<=xl+1e-7 or min(v[0] for v in piece)>=xh-1e-7 or max(v[1] for v in piece)<=yl+1e-7 or min(v[1] for v in piece)>=yh-1e-7:result.append(piece)
            else:result.extend(H.subtract(piece,constraints))
        parts=result
    desire_paths(a,p,parts)
    turf=a.mesh('Site_lawn',component='site',solid=False)
    for poly in parts:
        if len(poly)<3:continue
        # Coarse color stations follow shade, roots and shortcut traffic.
        # They do not allocate a campus-sized texture or extra plant meshes.
        for ix in range(math.floor(min(x for x,y in poly)/10),math.ceil(max(x for x,y in poly)/10)):
            for iy in range(math.floor(min(y for x,y in poly)/10),math.ceil(max(y for x,y in poly)/10)):
                q=poly
                for aa,bb,cc in convex_cuts(rect_poly((ix*10,(ix+1)*10,iy*10,(iy+1)*10))):q=H.clip(q,aa,bb,cc)
                if len(q)>=3:turf.geom([(x,y,-.004) for x,y in q],[tuple(range(len(q)))],'Siding')
    ob=turf.finish();ground_finish(ob,'Siding')
    for i,v in enumerate(ob.data.vertices):
        x,y=v.co[:2];dry=0.
        for tx,ty in p['trees'][:5]:dry+=.28*math.exp(-((x-tx)**2+(y-ty)**2)/20)
        varied=.94+.05*math.sin(x*.18+math.sin(y*.16))+.025*math.sin(y*.73+x*.31)
        ob.data.color_attributes['Tint'].data[i].color=(.62*varied*(1+.22*dry),.68*varied*(1-.18*dry),.58*varied*(1-.22*dry),1)
    # Public frontage has real driveway openings. Its continuous road remains
    # library geometry, while curb/walk omissions follow each apron footprint.
    for name,point in [('Service',(kr+6,kf,.02)),('Blacktop',(cx,cy,.025)),('Ballfield',(fx,fy,.01))]:a.socket(name,point,name.lower())
    # Stop / loading signs are school-specific fixtures absent from the library.
    for text,x,y in [('BUSES ONLY',p['bus_route'][0][0]-4,p['bus_route'][0][1]+10),('DROP OFF',p['parent_route'][0][0]+4,p['parent_route'][0][1]+10)]:
        m=a.mesh('Traffic_sign_'+text,component='sign');m.tube([(x,y,0),(x,y,2.4)],.0254,'Trim',ALUM(),sides=8);m.box((x,y,2.1),(.60,.04,.40),'Trim',(.56,.55,.46),r=.02);m.finish();label(a,text,(x,y-.025,2.06),.073,color=(.025,.032,.026))
    return a


def DARK():return (.023,.028,.024)


def planting_beds(a,p,cuts):
    """Maintained foundation beds, low clipped evergreens and a marquee bed.

    Small shrubs use original leaf cards with the library's alpha material;
    fine leaves remain in that map. Native mature trees remain intact.
    """
    import random
    rng=random.Random(p['seed']+491)
    src,_=library('build/context/shrub.glb')
    ma=next(ma for ob in src if ob.type=='MESH' for ma in ob.data.materials if ma and 'Shrubs' in ma.name)
    foliage=a.mesh('Low_foundation_planting',component='site',solid=False)
    beds=list(p['beds'])
    sx=p['bus_route'][0][0]+12 if p['type']!='courtyard' else 96;sy=-79 if p['type']!='courtyard' else -70
    beds.append((sx-3.8,sx+3.8,sy-1.9,sy+1.5))
    mulch=a.mesh('Maintained_planting_beds',component='site',solid=False,trim_cell=10)
    for j,(l,r,f,k) in enumerate(beds):
        poly=[(l+.45,f),(r-.45,f),(r,f+.45),(r,k-.3),(r-.4,k),(l+.3,k),(l,k-.3),(l,f+.4)]
        mulch.geom([(x,y,.002) for x,y in poly],[tuple(range(len(poly)))],'Trim',(.065,.035,.014));cuts.append(poly)
        count=max(2,round((r-l)/1.6))
        for q in range(count):
            x=l+.75+(r-l-1.5)*(q/max(1,count-1));y=(f+k)/2+rng.uniform(-.12,.12)
            if j==len(beds)-1:y=f+.45
            height=rng.uniform(.42,.68);rad=rng.uniform(.40,.58)
            for n in range(45):
                theta=rng.uniform(0,math.tau);h=rng.uniform(.1,.95);rr=rad*math.sqrt(max(0,1-h*h))
                xx=x+rr*math.cos(theta);yy=y+rr*math.sin(theta);zz=.07+h*height
                ang=rng.uniform(0,math.tau);w=.14;dx,dy=math.cos(ang)*w,math.sin(ang)*w
                foliage.geom([(xx-dx,yy-dy,zz-.13),(xx+dx,yy+dy,zz-.13),(xx+dx,yy+dy,zz+.13),(xx-dx,yy-dy,zz+.13)],[(0,1,2,3)],'Trim')
    mulch.finish();ob=foliage.finish();ob.data.materials.clear();ob.data.materials.append(ma)
    uv=ob.data.uv_layers.active
    for j,face in enumerate(ob.data.polygons):
        face.material_index=0
        u=(j%4)*.25;v=((j//4)%2)*.25
        for li,co in zip(face.loop_indices,((u,v),(u+.25,v),(u+.25,v+.25),(u,v+.25))):uv.data[li].uv=co
    # This material ignores Tint; the exporter removes COLOR_0 for it.
    ob['school_pbr']=True
def rect_poly(r):
    l,rr,f,k=r;return [(l,f),(rr,f),(rr,k),(l,k)]


def pedestrian_network(a,p,cuts):
    """Exterior paths connect actual doors, court, gate, field and portable."""
    m=a.mesh('School_walk_network',component='site',solid=False)
    def walk_rect(rect,z=.018):
        if min(rect[1]-rect[0],rect[3]-rect[2])<.001:return
        # Clip at building footprints: outdoor circulation never slices through
        # a classroom and no hidden green/paving duplicates ship underneath it.
        parts=[rect_poly(rect)]
        for b in p['blocks']:parts=[q for poly in parts for q in H.subtract(poly,convex_cuts(rect_poly(b['rect'])))]
        pl,pr,pf,pk=p['playground'];fx,fy=p['field']
        obstacles=[p['blacktop'],(pl,pr,pf,pk),(fx,fx+24,fy,fy+24)]
        obstacles += [(x-3.66,x+3.66,y-4.88,y+4.88) for x,y,yaw in p['portables']]
        for rect in obstacles:parts=[q for poly in parts for q in H.subtract(poly,convex_cuts(rect_poly(rect)))]
        for poly in parts:
            points=[(x,y,z(x,y) if callable(z) else z) for x,y in poly]
            if max(q[2] for q in points)>.03:grounded_slab(m,points)
            else:m.geom(points,[tuple(range(len(poly)))],'Concrete')
            cuts.append(poly)
    def path(points,width=1.524,z=.018):
        for (x,y),(xx,yy) in zip(points,points[1:]):
            walk_rect((min(x,xx)-width/2,max(x,xx)+width/2,min(y,yy)-width/2,max(y,yy)+width/2),z)
    def slope(points):
        lower=[(xx,yy,-.004) for xx,yy,zz in points]
        m.geom(points+lower,[(0,1,2,3)]+[(j,(j+1)%4,(j+1)%4+4,j+4) for j in range(4)],'Concrete')
        poly=[pt[:2] for pt in points]
        area=sum(x*yy-xx*y for (x,y),(xx,yy) in zip(poly,poly[1:]+poly[:1]))
        cuts.append(poly if area>0 else poly[::-1])
    # Outside door approaches descend to the general site grade at <1:20.
    endpoints=[]
    for b in p['blocks']:
        for o in b['openings']:
            if o['type'] not in ('door','double','entry'):continue
            u=o['u'];point=world((u,0,0),o['origin'],o['yaw']);normal=world((0,-1,0),(0,0),o['yaw'])
            endpoint=(point[0]+normal[0]*2.7432,point[1]+normal[1]*2.7432)
            under_cover=any(c['rect'][0]-.1<endpoint[0]<c['rect'][1]+.1 and c['rect'][2]-.1<endpoint[1]<c['rect'][3]+.1 for c in p['covered'])
            if not under_cover:
                half=max(1.0,o['w']/2+.30)
                points=[world((u-half,0,.1524),o['origin'],o['yaw']),world((u+half,0,.1524),o['origin'],o['yaw']),world((u+half,-2.7432,.018),o['origin'],o['yaw']),world((u-half,-2.7432,.018),o['origin'],o['yaw'])]
                slope(points)
            endpoints.append((o['face'],endpoint,b['kind']))
    pl,pr,pf,pk=p['playground'];gx=pl+3.5*3.048;wrap=pl-1.524 if gx<0 else pr+1.524
    rear=p['footprint'][3]+2.4384;cl,cr,cf,ck=p['blacktop'];court=(cl+cr)/2
    fx,fy=p['field']
    left=min(wrap,court,p['footprint'][0]-2,fx-4.5 if p['type']=='courtyard' else p['footprint'][0]-2);right=max(wrap,court,p['footprint'][1]+2)
    path([(left,rear),(right,rear)],2.4384)
    for face,end,kind in endpoints:
        if end[1]>0 and kind in ('single','cluster','classrow'):
            if face in ('east','west','north'):path([end,(end[0],rear)],1.524)
    path([(court,rear),(court,cf+.03)],2.4384)
    path([(wrap,rear),(wrap,pf-2.7432),(gx,pf-2.7432),(gx,pf+.02)],1.524)
    if p['type']=='courtyard':path([(fx-4.5,rear),(fx-4.5,fy)],1.524)
    else:
        field_row=max(fy-4.5,pk+1.524,ck+1.524)
        path([(wrap,rear),(wrap,field_row),(fx-4.5,field_row),(fx-4.5,fy)],1.524)
    for x,y,yaw in p['portables']:
        # Lower ramp landing meets a route which passes outside the entire
        # portable body and its guard, instead of following beneath the ramp.
        end=world((7.3152/2+.94,-9.7536/2-1.75-6.5712-1.524-2.7432,0),(x,y),yaw)
        join=x+7.3152/2+1.88+1.524 if x<0 else wrap
        path([(end[0],end[1]),(join,end[1]),(join,rear)],1.524)
    if p['type']=='finger':
        def level(x,y):
            parent=p['floor']+(.1704-p['floor'])*min(1,max(0,(-41.73-x)/3.6124))
            t=min(1,max(0,(-8.5-y)/18));return parent*(1-t)+entry_height(p,y)*t
        path([(-42.8,-8.5),(-42.8,-26.5),(-40,-26.5)],1.524,level)
    elif p['type']=='courtyard':
        ym=.4196;yy=p['entry'][1];start=yy+3.048
        slope([(55,ym-.762,.1704),(55,ym+.762,.1704),(51.952,ym+.762,.018),(51.952,ym-.762,.018)])
        path([(51.952,ym),(48,ym),(48,-11),(23,-11),(23,start)],1.524)
        slope([(22.238,start,.018),(23.762,start,.018),(23.762,yy,p['floor']),(22.238,yy,p['floor'])])
    elif p['type']=='compact':
        ym=-4.5804;c=p['covered'][1];edge=c['rect'][0]-.15;start=edge-3.048;row=(c['rect'][2]+c['rect'][3])/2+.10
        slope([(-56,ym-.762,.1704),(-52.952,ym-.762,.018),(-52.952,ym+.762,.018),(-56,ym+.762,.1704)])
        path([(-52.952,ym),(start,ym),(start,row)],1.524)
        slope([(start,row-.762,.018),(edge,row-.762,p['floor']),(edge,row+.762,p['floor']),(start,row+.762,.018)])
    # Front exits meet the public entry via a route ahead of the longest mass.
    ex,ey=p['entry'];front=p['footprint'][2]-3.6
    for face,end,kind in endpoints:
        if face=='south' and kind=='gym':path([end,(end[0],front),(ex,front),(ex,ey-8.9)],1.524)
        if face=='north' and kind=='gym':
            if p['type']=='compact':
                addition=next(b for b in p['blocks'] if b['id'].startswith('Addition'))
                lane=addition['rect'][1]+2.4384;path([end,(lane,end[1]),(lane,rear)],1.524)
            elif p['type']=='courtyard':
                edge=p['covered'][1]['rect'][1]+.15;start=edge+2.7432;y=end[1]
                path([end,(start,y)],1.524)
                slope([(start,y-.762,.018),(start,y+.762,.018),(edge,y+.762,.1524),(edge,y-.762,.1524)])
    ground_finish(m.finish(),'Concrete')


def streets(a,p,cuts):
    """Native crowned street, 6in curb/gutter and tapered driveway aprons."""
    for row in p['streets']:
        horizontal=row['axis']=='X';at=row['at'];length=210 if horizontal else 184
        cuts.append(rect_poly((-105,105,at-8.096,at+8.096) if horizontal else (at-8.096,at+8.096,-92,92)))
        for i in range(-round(length/12.192),round(length/12.192)+1):
            v=i*6.096
            place('build/context/ground.glb','Public_road_'+str(at)+'_'+str(i),(v,at,.01165) if horizontal else (at,v,.01165),90 if horizontal else 0,'Road_Straight_A',a.root)
        ends=[q for key in ('bus_route','parent_route') for q in (p[key][0],p[key][-1]) if abs(q[1 if horizontal else 0]-at)<1]
        openings=[q[0 if horizontal else 1] for q in ends]
        def point(v,d,z):return (v,at+d,z) if horizontal else (at+d,v,z)
        for sign in (-1,1):
            near=sign==(1 if horizontal else -1)
            def top(v):
                distance=min((abs(v-q) for q in openings),default=1e6)
                return .019+.1514*min(1,max(0,(distance-3.6576)/2.14)) if near else .1704
            c=a.mesh('Frontage_curb_'+str(at)+'_'+str(sign),component='site',solid=False)
            walk=a.mesh('Public_walk_'+str(at)+'_'+str(sign),component='site',solid=False)
            verge=a.mesh('Frontage_verge_'+str(at)+'_'+str(sign),component='site',solid=False)
            for i in range(-int(length/2),int(length/2)):
                verts=[]
                for v in (i,i+1):
                    for d,z in ((3.6576,.018),(4.1148,.018),(4.1402,top(v)),(4.2672,top(v))):verts.append(point(v,sign*d,z))
                c.geom(verts,[(j,j+1,j+5,j+4) for j in range(3)],'Concrete')
                walk.geom([point(i,sign*4.2672,top(i)),point(i+1,sign*4.2672,top(i+1)),point(i+1,sign*6.096,top(i+1)),point(i,sign*6.096,top(i))],[(0,1,2,3)],'Concrete')
                verge.geom([point(i,sign*6.096,top(i)),point(i+1,sign*6.096,top(i+1)),point(i+1,sign*8.096,-.004),point(i,sign*8.096,-.004)],[(0,1,2,3)],'Siding')
            ground_finish(c.finish(),'Concrete');ground_finish(walk.finish(),'Concrete');ground_finish(verge.finish(),'Siding')


def floor_text(a,text,x,y,size=.35,color=(.42,.39,.25)):
    ob=label(a,text,(x,y,.034),size,color);ob.rotation_euler=(0,0,0);return ob


def amenities(a,p,cuts):
    import random
    rng=random.Random(p['seed']+991);l,r,f,k=p['blacktop'];cx,cy=(l+r)/2,(f+k)/2
    # A mixed elementary yard: basketball, four-square, hopscotch, a states
    # map, oval run and tetherball. None is a soccer goal-area marking.
    m=a.mesh('Yard_games',component='site',solid=False)
    for j in range(3):
        x=l+3+j*5.4;y=k-6
        line(m,[(x,y),(x+4.5,y),(x+4.5,y+4.5),(x,y+4.5),(x,y)],.065,(.38,.38,.30),z=.032)
        line(m,[(x+2.25,y),(x+2.25,y+4.5)],.065,z=.032);line(m,[(x,y+2.25),(x+4.5,y+2.25)],.065,z=.032)
        for q in range(4):floor_text(a,str(q+1),x+.9+(q%2)*2.25,y+.7+(q//2)*2.25,.34)
    x=l+2;y=f+6
    for j in range(8):
        w=1.4 if j in (2,4,6) else .70;xx=x+(.35 if j in (1,5) else 0)
        line(m,[(xx,y+j*.70),(xx+w,y+j*.70),(xx+w,y+(j+1)*.70),(xx,y+(j+1)*.70),(xx,y+j*.70)],.055,(.50,.44,.24),z=.032)
        if w>1:line(m,[(xx+.7,y+j*.7),(xx+.7,y+(j+1)*.7)],.055,z=.032)
    # The running oval occupies the perimeter of the asphalt yard, leaving
    # the basketball keys and free-play games inside it.
    s=dict(center=(cx,cy),straight=(r-l-(k-f))/2,radius=(k-f)/2-1.5,yaw=0)
    for offset in (0,.85):
        pts=stadium(s,s['radius']-offset);line(m,pts+[pts[0]],.06,(.32,.31,.235),z=.032)
    m.finish()
    for j in range(3):
        x=r-3-j*4;y=k-6;tt=a.mesh('Tetherball_'+str(j),component='tetherball')
        tt.tube([(x,y,.025),(x,y,3.05)],.0254,'Trim',(.28,.30,.28),sides=8)
        # Rope hangs under gravity with a real slack bend beside the pole.
        tt.tube([(x,y,3.03),(x+.08,y+.12,2.52),(x+.10,y+.14,1.90)],.004,'Trim',(.42,.39,.29),sides=4)
        for zz,rad in ((1.88,.085),(1.78,.13),(1.68,.085)):
            tt.tube([(x+.10,y+.14,zz-.04),(x+.10,y+.14,zz+.04)],rad,'Trim',(.48,.25,.025),sides=10)
        tt.finish()
    states_map(a,r-15,f+3)
    # Street-side monument and maintained changeable-letter marquee. Fictional.
    sx=p['bus_route'][0][0]+12 if p['type']!='courtyard' else 96;sy=-79 if p['type']!='courtyard' else -70
    m=a.mesh('School_marquee',component='sign')
    m.box((sx,sy,.42),(4.6,1.1,.84),'Veneer')
    m.box((sx,sy,1.55),(4.25,.25,1.52),'Trim',p['palette']['accent'],r=.016)
    m.box((sx,sy-.14,1.25),(3.94,.035,.67),'Concrete',(.46,.45,.39),r=.002)
    for z in (1.04,1.24,1.44):m.box((sx,sy-.164,z),(3.94,.012,.012),'Trim',(.21,.22,.19))
    m.finish();label(a,p['name'],(sx,sy-.17,1.91),.15,color=(.56,.55,.47));label(a,'FAMILY NIGHT   THURS 6 PM',(sx,sy-.171,1.26),.13,color=(.017,.025,.019));label(a,'RILL COUNTY   EST '+str(p['era']),(sx,sy-.17,.65),.12)
    # Rear yard boundary on the native ten-foot grid, with the field beyond.
    for name,s,e in [('North',(-91.44,82.296),(91.44,82.296)),('East',(91.44,15.24),(91.44,82.296))]:fence_run(a,s,e,'Yard_'+name)
    # Place asphalt repairs where services cross/turn, with irregular cutbacks
    # and crack seal along failed seams. Shared Ground map, no new image set.
    repair=a.mesh('Asphalt_repairs',component='site',solid=False)
    for j in range(7):
        x=l+6+rng.random()*(r-l-12);y=f+3+rng.random()*(k-f-6);w=rng.uniform(.7,2.3);h=rng.uniform(.4,1.2)
        q=[(x-w,y-h,.028),(x+w*.7,y-h*.8,.028),(x+w,y+h,.028),(x-w*.85,y+h*.9,.028)]
        repair.geom(q,[(0,1,2,3)],'Concrete',(.34,.34,.33))
    ob=repair.finish();ground_finish(ob,'Asphalt')
    attr=ob.data.color_attributes['Tint']
    for v in attr.data:v.color=(.28,.28,.27,1)
    seams=a.mesh('Crack_seal',component='site',solid=False)
    for j in range(9):
        x=l+2+rng.random()*(r-l-4);y=f+2+rng.random()*(k-f-4)
        line(seams,[(x+i*.8,y+math.sin(i*1.7+j)*.16) for i in range(5)],rng.uniform(.025,.055),(.017,.020,.018),z=.030)
    seams.finish()


def states_map(a,x,y):
    """Original simplified geographic schoolyard map; no traced reference data.

    The western rectilinear survey and irregular eastern borders are an
    illustrative playground graphic, not a geographic survey or GIS dataset.
    """
    outline=[(0,3.8),(.7,5.2),(2,5.1),(3.1,5.5),(6.4,5.3),(7.4,5.65),(8.2,5.2),(9.4,5.1),(10.2,5.8),(10.4,5),(9.7,4.6),(9.4,3.7),(8.6,3.2),(8.4,2.4),(7.8,1.9),(8.5,.3),(8,.15),(7.3,1.6),(6.6,1.9),(5.8,1.6),(4.9,1.8),(4.4,.9),(3.8,1.6),(3.6,2.2),(2.5,2.2),(1.9,2.7),(.8,2.7),(.7,3.2),(0,3.8)]
    m=a.mesh('States_map',component='site',solid=False)
    line(m,[(x+xx,y+yy) for xx,yy in outline],.08,(.47,.42,.24),z=.033)
    borders=[[(.6,4.4),(2,4.3),(2,5.1)],[(2,4.3),(2.3,3.7),(3.1,3.7),(3.1,5.5)],[(3.1,4.8),(4.4,4.8),(4.4,5.4)],[(3.1,4.1),(4.4,4.1),(4.4,4.8)],[(3.1,3.4),(4.4,3.4),(4.4,4.1)],[(2.3,3.7),(2.5,2.2)],[(3.1,3.7),(3.1,2.2)],[(3.1,2.9),(4.4,2.9),(4.4,3.4)],[(4.4,5.4),(4.4,1.8)],[(4.4,4.8),(5.5,4.8),(5.5,5.4)],[(4.4,4.1),(5.6,4.1),(5.5,4.8)],[(4.4,3.4),(5.6,3.4),(5.6,4.1)],[(4.4,2.9),(5.6,2.9),(5.6,3.4)],[(4.4,2.4),(5.6,2.4),(5.6,2.9)],[(5.6,1.7),(5.6,4.8),(6.2,4.9),(6.2,5.3)],[(5.6,4.1),(6.4,4.1),(6.4,4.9)],[(5.6,3.4),(6.5,3.4),(6.4,4.1)],[(5.6,2.9),(6.6,2.9),(6.5,3.4)],[(5.6,2.4),(6.6,2.4),(6.6,2.9)],[(6.4,4.1),(7,4.1),(7,5.3)],[(7,4.1),(7.6,4.3),(7.8,5.1)],[(6.5,3.4),(7.5,3.4),(7.6,4.3)],[(6.6,2.9),(8,2.9),(8.4,3.4),(7.5,3.4)],[(6.6,2.4),(7.3,2.4),(7.3,1.6)],[(7.3,2.4),(8.4,2.4)],[(7.5,3.4),(8.4,3.9),(9.1,4.0)],[(7.6,4.3),(8.7,4.5),(9.4,4.3)],[(8.7,4.5),(8.7,5.2)],[(9.1,4.0),(9.2,4.8),(9.7,4.6)],[(9.2,4.8),(9.6,5.2)],[(9.6,5.2),(9.8,5.6)]]
    for pts in borders:line(m,[(x+xx,y+yy) for xx,yy in pts],.045,(.31,.37,.29),z=.033)
    m.finish();floor_text(a,'U S A',x+3,y-.6,.50,(.40,.35,.18))


def desire_paths(a,p,lawn):
    """Narrow soil exposures where a shortcut cuts the maintained turf."""
    def inside(q,poly):return all(aa*q[0]+bb*q[1]+cc>=-1e-6 for aa,bb,cc in convex_cuts(poly))
    routes={'finger':[((-34,-51),(-17,-34)),((39,27),(45,36))],
            'courtyard':[((-54,-61),(-32,-40)),((-36,30),(-44,40))],
            'compact':[((-42,-52),(-30,-33)),((17,30),(45,25))]}[p['type']]
    m=a.mesh('Childrens_desire_paths',component='site',solid=False,trim_cell=10)
    for route in routes:
        start,end=map(lambda q:Vector((*q,0)),route);tangent=(end-start).normalized();normal=Vector((-tangent.y,tangent.x,0))
        n=round((end-start).length/.65)
        for j in range(n):
            for side in (-1,1):
                pts=[];cols=[]
                for k,d in ((j,0),(j,side),(j+1,side),(j+1,0)):
                    t=k/n;center=start.lerp(end,t);width=.33+.08*math.sin(t*26+p['seed']);q=center+normal*d*width
                    pts.append((q.x,q.y,-.002));cols.append((.085,.080,.035) if d else (.105,.068,.029))
                if not all(any(inside(q,poly) for poly in lawn) for q in pts):continue
                begin=len(m.col);m.geom(pts,[(0,1,2,3)],'Trim');m.col[begin:]=[(*c,1) for c in cols]
    m.finish()
