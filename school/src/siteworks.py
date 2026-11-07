"""School-specific grounds plus immutable instances of the library families.

No playground equipment: only its fenced reservation, approach and socket.
The bus loop is a true swept-width stadium, with independent parent traffic.
"""
import math,json
from pathlib import Path
import bpy
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
    l,r,f,k=rect
    m.geom([(l,f,z),(r,f,z),(r,k,z),(l,k,z)],[(0,1,2,3)],role,color)


def stadium(s,radius=None):
    R=s['radius'] if radius is None else radius;half=s['straight'];pts=[]
    for cx,start in ((half,-math.pi/2),(-half,math.pi/2)):
        for i in range(25):
            a=start+i*math.pi/24;pt=world((cx+R*math.cos(a),R*math.sin(a),0),s['center'],s['yaw']);pts.append(pt[:2])
    return pts


def annulus(m,inner,outer,z,role,color=None,skip=None):
    n=len(inner);faces=[]
    for i in range(n):
        ids=(i,(i+1)%n,(i+1)%n+n,i+n)
        if skip and skip(tuple(sum((inner+outer)[k][axis] for k in ids)/4 for axis in (0,1))):continue
        faces.append(ids)
    m.geom([(x,y,z) for x,y in inner+outer],faces,role,color)


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


def loop(a,s,name,cuts):
    road=a.mesh(name+'_Asphalt',component='site',solid=False)
    inner=stadium(s,s['radius']-3.6576);outer=stadium(s,s['radius']+3.6576)
    annulus(road,inner,outer,.018,'Concrete');ground_finish(road.finish(),'Asphalt')
    curb=a.mesh(name+'_Curbs',component='site')
    sx=s['center'][0] if s['yaw'] else s['center'][0]+s['straight']
    sy=s['center'][1]-s['straight']-s['radius']-3.6576 if s['yaw'] else s['center'][1]-s['radius']-3.6576
    gateway=lambda pt:abs(pt[0]-sx)<4.05 and pt[1]<sy+2.8
    def walk_height(x,y,top=.1704):
        # The two walk ends descend into the vehicle crossing; an open cut in
        # a raised surface otherwise exposes a floating edge above the drive.
        ramp=min(1,max(0,(abs(x-sx)-4.05)/2.7432)) if y<sy+3 else 1
        return .018+(top-.018)*ramp
    # Ground's municipal section: 18in gutter, 6in back, 6in rise.
    for sign,rad in ((-1,s['radius']-3.6576),(1,s['radius']+3.6576)):
        stations=[(rad,.018),(rad+sign*.4572,.018),(rad+sign*.4826,.1704),(rad+sign*.6096,.1704)]
        loops=[[(x,y,walk_height(x,y,z)) for x,y in stadium(s,r)] for r,z in stations];n=len(loops[0]);v=[p for row in loops for p in row]
        curb.geom(v,[(q*n+i,q*n+(i+1)%n,(q+1)*n+(i+1)%n,(q+1)*n+i) for q in range(3) for i in range(n) if not gateway(((v[q*n+i][0]+v[q*n+(i+1)%n][0])/2,(v[q*n+i][1]+v[q*n+(i+1)%n][1])/2))],'Concrete')
    ground_finish(curb.finish(),'Concrete')
    walk=a.mesh(name+'_Walk',component='site',solid=False)
    wi,wo=stadium(s,s['radius']+4.2672),stadium(s,s['radius']+5.7912)
    annulus(walk,wi,wo,.1704,'Concrete',skip=gateway)
    walk.v=[(x,y,walk_height(x,y,z)) for x,y,z in walk.v]
    ground_finish(walk.finish(),'Concrete')
    # Two-meter verge rises to the walk instead of leaving an unsupported
    # black slot beneath its edge. This is landscape grading, not a black rim.
    verge=a.mesh(name+'_Graded_verge',component='site',solid=False)
    inn=stadium(s,s['radius']+5.7912);out=stadium(s,s['radius']+7.7912);nn=len(inn)
    verge.geom([(x,y,walk_height(x,y,.1704)) for x,y in inn]+[(x,y,-.004) for x,y in out],[(i,(i+1)%nn,(i+1)%nn+nn,i+nn) for i in range(nn) if not gateway(((inn[i][0]+out[(i+1)%nn][0])/2,(inn[i][1]+out[(i+1)%nn][1])/2))],'Siding')
    ground_finish(verge.finish(),'Siding');cuts.append(stadium(s,s['radius']+7.7912))
    # Restore the open lawn island; no hidden lawn sits beneath pavement.
    island=a.mesh(name+'_Island',component='site',solid=False)
    pts=stadium(s,s['radius']-4.2672);island.geom([(x,y,.165) for x,y in pts],[tuple(range(len(pts)))],'Siding');ground_finish(island.finish(),'Siding')
    return inner,outer


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
    for i in range(n):place(path,name+'_Bay_'+str(i),(start[0]+dx*(i+.5)/n,start[1]+dy*(i+.5)/n,0),yaw,'Chain_Section',a.root)
    for i in range(n+1):place(path,name+'_Post_'+str(i),(start[0]+dx*i/n,start[1]+dy*i/n,0),yaw,'Chain_Line',a.root)


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
    a.socket('Portable_'+str(index)+'_Ramp',world((w/2+.94,end-.762,bottom),(x,y),yaw),'portable_ramp',yaw)


def build_site(p,building):
    a=Assembly('Campus_'+str(p['seed']));building.root.parent=a.root;a.root['seed']=p['seed'];a.root['lot_m']=p['lot']
    cuts=[]
    bus_inner,bus_outer=loop(a,p['bus'],'Bus_loop',cuts);loop(a,p['parent'],'Parent_dropoff',cuts)
    # Entry plaza ties into the loop walk. No elevated unsupported platform.
    ex,ey=p['entry'];plaza=(ex-7,ex+7,ey-9,ey)
    m=a.mesh('Entry_plaza',component='site');m.box(((plaza[0]+plaza[1])/2,(plaza[2]+plaza[3])/2,.0762),(14,9,.1524),'Concrete',r=.004);ground_finish(m.finish(),'Concrete');cuts.append(rect_poly(plaza))
    # Front pedestrian connection from the closest loop side to the plaza.
    target=p['bus'] if p['type']=='finger' else p['parent'];rear=target['center'][1]+target['radius']+5.7912
    approach=(ex-1.524,ex+1.524,rear,ey-8.95)
    m=a.mesh('Entry_connection',component='site');m.box((ex,(approach[2]+approach[3])/2,.0852),(3.048,max(.01,approach[3]-approach[2]),.1704),'Concrete',r=.003);ground_finish(m.finish(),'Concrete');cuts.append(rect_poly(approach))
    # Staff lot: 9x18ft stalls, 24ft aisle, one reserved van bay/aisle.
    l,r,f,k=p['parking'];m=a.mesh('Staff_paving',component='site',solid=False);rectangle(m,p['parking'],.018);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(p['parking']))
    m=a.mesh('Staff_markings',component='site',solid=False)
    front_start=l+4.8768;front_count=max(1,int((r-front_start)/2.7432));back_count=max(1,int((r-l)/2.7432));p['staff_stalls']=1+front_count+back_count
    for i in range(front_count+1):line(m,[(front_start+i*2.7432,f),(front_start+i*2.7432,f+5.4864)],.10,(.53,.52,.46))
    for xx in (l,l+3.3528):line(m,[(xx,f),(xx,f+5.4864)],.10,(.53,.52,.46))
    for i in range(back_count+1):line(m,[(l+i*2.7432,k-5.4864),(l+i*2.7432,k)],.10,(.53,.52,.46))
    for j in range(6):line(m,[(l+3.3528+j*.20,f),(l+3.3528+j*.20+.35,f+5.4864)],.07,(.45,.45,.40))
    m.finish()
    # Drives connect all traffic areas to the site's front street. Paving
    # starts at the loop's end tangent and ends flush at the public street.
    drives=[]
    for s in (p['bus'],p['parent']):
        sx=s['center'][0] if s['yaw'] else s['center'][0]+s['straight']
        sy=s['center'][1]-s['straight']-s['radius']-3.6576 if s['yaw'] else s['center'][1]-s['radius']-3.6576
        drives.append((sx-3.6576,sx+3.6576,-87,sy+2.5))
    # A staff access joins its adjacent circulation lane rather than dead-ending.
    ay=(f+k)/2;drives.append((r,r+7.3152,-87,ay+3.6576));drives.append((r-1,r+7.3152,ay-3.6576,ay+3.6576))
    m=a.mesh('Access_drives',component='site',solid=False)
    for rect in drives:
        if rect[3]>rect[2]:rectangle(m,rect,.018);cuts.append(rect_poly(rect))
    ground_finish(m.finish(),'Asphalt')
    # Service yard at the kitchen's outside door. A straight side lane links
    # the public frontage without crossing the playground reservation.
    kitchen=next(b for b in p['blocks'] if b['kind']=='kitchen');kl,kr,kf,kk=kitchen['rect']
    offset=3 if p['type']=='compact' else 9.5
    yard=(kr,kr+offset+6.5,kf-2,kk+4);m=a.mesh('Service_yard',component='site',solid=False);rectangle(m,yard,.025);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(yard))
    service=(kr+offset,kr+offset+6,-87,kf-1.98);m=a.mesh('Service_drive',component='site',solid=False);rectangle(m,service,.019);ground_finish(m.finish(),'Asphalt');cuts.append(rect_poly(service))
    m=a.mesh('Service_dock',component='service');m.box((kr+1,kk-2,.18),(2,3,.36),'Concrete',r=.006)
    for yy in (kk-3.0,kk-1.0):m.box((kr+2.015,yy,.29),(.045,.25,.40),'Trim',DARK())
    # District dumpster enclosure, masonry sides, steel gates on true hinges.
    dx,dy=kr+7,kk+1
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
    m=a.mesh('Game_lines',component='site',solid=False);cx,cy=(l+r)/2,(f+k)/2
    court=(cx-12.8016,cx+12.8016,cy-7.62,cy+7.62)
    aa,bb,cc,dd=court;line(m,[(aa,cc),(bb,cc),(bb,dd),(aa,dd),(aa,cc)],.07)
    line(m,[(cx,cc),(cx,dd)],.07);line(m,[(cx+1.8*math.cos(t*math.tau/48),cy+1.8*math.sin(t*math.tau/48)) for t in range(49)],.065)
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
    # Flag, racks and modest foundation planting: library instances, not new
    # tree or shrub shapes. Two trees leave a useful triangle allowance.
    flagpole(a,(ex-8,ey-7))
    for j in range(2):place('build/context/furniture.glb','Bike_rack_'+str(j),(ex+8+j*1.0,ey-4,.1524),0,'BikeRack',a.root)
    place('build/context/furniture.glb','Entry_bench',(ex-4,ey-5,.1524),0,'Bench',a.root)
    tree_positions={'finger':((ex-26,ey-8),(ex+38,ey+5)), 'courtyard':((-45,-12),(37,5)), 'compact':((-43,-25),(36,8))}[p['type']]
    for j,(x,y) in enumerate(tree_positions):place(ROOT/'trees/export'/('RedMaple.glb' if j==0 else 'PinOak.glb'),'Mature_tree_'+str(j),(x,y,0),p['seed']*17+j*73,parent=a.root)
    for j in range(2):place('build/context/shrub.glb','Foundation_shrub_'+str(j),(ex-10-j*1.1,ey-1.2,0),j*43,parent=a.root)
    # Two cars are counted as placed geometry in the whole-site budget.
    for j in range(2):
        s=target;x=s['center'][0]+(-12 if j==0 else 3);y=s['center'][1]+s['radius']
        car=place('build/context/car.glb','Dropoff_car_'+str(j),(x,y,.020),90,parent=a.root)
        if j==1:
            paint=None
            for ob in car.children_recursive:
                if ob.type!='MESH':continue
                for slot in ob.material_slots:
                    if slot.material and 'paint' in slot.material.name.lower():
                        if paint is None:
                            paint=slot.material.copy();paint.name='School context blue hatch';paint.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.035,.085,.12,1)
                        slot.link='OBJECT';slot.material=paint
    for j,(x,y,yaw) in enumerate(p['portables']):portable(a,x,y,yaw,j)
    # One existing library pole serves the small staff lot. Period is 2010 for
    # this presentation, allowing the library's LED retrofit cobra head.
    l,r,f,k=p['parking'];place('build/context/light.glb','Staff_lot_light',(r+1.0,k-1.0,0),-90,parent=a.root)
    pedestrian_network(a,p,cuts)
    # All lawn is clipped around the actual building and site slabs.
    cuts += [rect_poly(b['rect']) for b in p['blocks']]+[rect_poly(c['rect']) for c in p['covered']]
    W,D=p['lot'];parts=[rect_poly((-W/2,W/2,-D/2,D/2))]
    for poly in cuts:
        constraints=convex_cuts(poly)
        parts=[q for piece in parts for q in H.subtract(piece,constraints)]
    turf=a.mesh('Site_lawn',component='site',solid=False)
    for poly in parts:
        if len(poly)>=3:turf.geom([(x,y,-.004) for x,y in poly],[tuple(range(len(poly)))],'Siding')
    ground_finish(turf.finish(),'Siding')
    # Public approach is library Ground road construction, on its native pitch.
    for j in range(34):place('build/context/ground.glb','Street_'+str(j),((j-16.5)*6.096,-89.7,0),90,'Road_Straight_A',a.root)
    for name,point in [('Bus_entry',(p['bus']['center'][0],-87,.02)),('Parent_entry',(p['parent']['center'][0],-87,.02)),('Service',(kr+6,kf,.02)),('Blacktop',(cx,cy,.025)),('Ballfield',(fx,fy,.01))]:a.socket(name,point,name.lower())
    # Stop / loading signs are school-specific fixtures absent from the library.
    for text,x,y in [('BUSES ONLY',p['bus']['center'][0],-80),('DROP OFF',ex-11,ey-9)]:
        m=a.mesh('Traffic_sign_'+text,component='sign');m.tube([(x,y,0),(x,y,2.4)],.0254,'Trim',ALUM(),sides=8);m.box((x,y,2.1),(.60,.04,.40),'Trim',(.56,.55,.46),r=.02);m.finish();label(a,text,(x,y-.025,2.06),.073,color=(.025,.032,.026))
    return a


def DARK():return (.023,.028,.024)
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
        for poly in parts:
            m.geom([(x,y,z) for x,y in poly],[tuple(range(len(poly)))],'Concrete');cuts.append(poly)
    def path(points,width=1.524):
        for (x,y),(xx,yy) in zip(points,points[1:]):
            walk_rect((min(x,xx)-width/2,max(x,xx)+width/2,min(y,yy)-width/2,max(y,yy)+width/2))
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
                lower=[(xx,yy,-.004) for xx,yy,zz in points]
                m.geom(points+lower,[(0,1,2,3)]+[(j,(j+1)%4,(j+1)%4+4,j+4) for j in range(4)],'Concrete')
                cuts.append([pt[:2] for pt in points][::-1])
            endpoints.append((o['face'],endpoint,b['kind']))
    pl,pr,pf,pk=p['playground'];gx=pl+3.5*3.048;wrap=pl-1.524 if gx<0 else pr+1.524
    rear=p['footprint'][3]+2.4384;cl,cr,cf,ck=p['blacktop'];court=(cl+cr)/2
    left=min(wrap,court,p['footprint'][0]-2);right=max(wrap,court,p['footprint'][1]+2)
    path([(left,rear),(right,rear)],2.4384)
    for face,end,kind in endpoints:
        if end[1]>0 and kind in ('single','cluster','classrow'):
            if face in ('east','west','north'):path([end,(end[0],rear)],1.524)
    path([(court,rear),(court,cf+.03)],2.4384)
    path([(wrap,rear),(wrap,pf-2.7432),(gx,pf-2.7432),(gx,pf+.02)],1.524)
    fx,fy=p['field'];path([(wrap,rear),(wrap,fy-4.5),(fx-4.5,fy-4.5),(fx-4.5,fy)],1.524)
    for x,y,yaw in p['portables']:
        # Lower ramp landing meets a route which passes outside the entire
        # portable body and its guard, instead of following beneath the ramp.
        end=world((7.3152/2+.94,-9.7536/2-1.75-6.5712-.762,0),(x,y),yaw)
        path([(end[0],end[1]),(wrap,end[1]),(wrap,rear)],1.524)
    # Front exits meet the public entry via a route ahead of the longest mass.
    ex,ey=p['entry'];front=p['footprint'][2]-3.6
    for face,end,kind in endpoints:
        if face=='south' and kind=='gym':path([end,(end[0],front),(ex,front),(ex,ey-8.9)],1.524)
    ground_finish(m.finish(),'Concrete')
