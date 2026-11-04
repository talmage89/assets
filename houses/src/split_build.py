"""Split-specific level construction on the accepted house components.

Shared roof envelopes/boxed cornices/drainage, masonry returns, sash systems,
door leaves, service assemblies and chimney are used without legacy changes.
"""
import copy
import json
import math
import bpy
from mathutils import Vector,Matrix
from build import Builder, Mesh, wall_sections, doors
from plan import clip, subtract, wall_frame
from cape_build import roofs, landing as cape_landing, service_mounts
from ranch_build import window, services, chimney, carport
from ranch_masonry import opening_masonry
from additions import portal
from kit import model as G


def veneer_top(plan, block, face):
    s=plan['spec']
    if s['cladding'][block.name][face]!='veneer':return None
    if s['wall_mix']=='all_brick':return block.plate-.03
    if block.stories==2:return plan['levels']['upper']-.254
    return block.plate-.03


class SplitMesh(Mesh):
    def box(self,p,s,role='Trim',color=None,r=.0015,xf=None):
        # Fine hidden/rear sash bevels never change the street silhouette.
        if self.props.get('component') in ('window','storm_window') and min(s)<.020:r=0
        return super().box(p,s,role,color,r,xf)
    def finish(self):
        ob=super().finish()
        if ob:
            # Exact roof clipping can leave sub-micrometer miters that
            # collapse in Blender float storage. Dissolve their edges into
            # neighboring faces before triangulation; never punch a hole.
            import bmesh
            bm=bmesh.new();bm.from_mesh(ob.data)
            bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
            bmesh.ops.triangulate(bm,faces=list(bm.faces))
            bm.verts.index_update();seen=set();duplicates=[]
            for face in bm.faces:
                key=tuple(sorted(v.index for v in face.verts))
                if key in seen:duplicates.append(face)
                else:seen.add(key)
            if duplicates:bmesh.ops.delete(bm,geom=duplicates,context='FACES_ONLY')
            bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
        return ob


class SplitBuilder(Builder):
    def __init__(self,plan):
        super().__init__(plan)
        self.door.location.z=plan['levels']['living']+.006
        self.frame_recess=0
    def mesh(self,name,part='Static',**props):return SplitMesh(self,name,part,**props)
    def frame(self,block,face):
        xf,n,length=super().frame(block,face)
        recess=self.frame_recess
        if not recess:return xf,n,length
        return lambda p:xf((p[0],p[1]-recess,p[2])),n,length


def shell(b):
    s=b.plan['spec'];lv=b.plan['levels']
    for block in b.plan['blocks']:
        if block.name=='Garage' and s['garage']['kind']=='carport':continue
        for face in ('front','back','left','right'):
            xf,n,length=b.frame(block,face)
            wall=b.mesh(block.name+'_'+face+'_Wall',component='wall',block=block.name,face=face)
            foundation=b.mesh(block.name+'_'+face+'_Foundation',component='foundation',block=block.name,face=face)
            cap=b.mesh(block.name+'_'+face+'_VeneerCap',component='veneer_cap',block=block.name,face=face)
            top=veneer_top(b.plan,block,face)
            base_top=block.floor-.0762 if block.stories==1 and block.name!='Garage' else block.floor-.025
            recess=s['wing']['overhang'] if block.stories==2 and face=='front' and s['kind']=='side' else 0
            for poly,adj in wall_sections(b,block,face):
                if not adj:
                    lo=min(p[0] for p in poly);hi=max(p[0] for p in poly)
                    if block.stories==2:poly=[(u,base_top if abs(z-.02)<1e-6 else z) for u,z in poly]
                    poly=clip(poly,0,1,-base_top)
                    bottom=min(-.18,block.floor-.18)
                    foundation.prism([xf((lo,-.024-recess,bottom)),xf((hi,-.024-recess,bottom)),xf((hi,-.024-recess,base_top)),xf((lo,-.024-recess,base_top))],(-n[0],-n[1],0),.18,'Concrete')
                parts=[poly]
                for o in b.openings:
                    if o['block']!=block.name or o['face']!=face:continue
                    cuts=[(1,0,-o['u']+o['w']/2),(-1,0,o['u']+o['w']/2),(0,1,-o['z']),(0,-1,o['z']+o['h'])]
                    parts=[p for v in parts for p in subtract(v,cuts)]
                # A real floor/belly band separates the recessed lower wall
                # from the projecting upper facade; no doubled coplanar boxes.
                split=lv['upper']-.254 if block.stories==2 else None
                for poly in parts:
                    fields=[('Veneer',clip(poly,0,-1,top)),('Siding',clip(poly,0,1,-top))] if top is not None else [('Siding',poly)]
                    for role,piece in fields:
                        if not piece:continue
                        regions=[(piece,0)]
                        if split is not None:regions=[(clip(piece,0,-1,split),recess),(clip(piece,0,1,-split),0)]
                        for part,inset in regions:
                            if part:wall.prism([xf((u,(.072 if role=='Veneer' else .012)-inset,z)) for u,z in part],(-n[0],-n[1],0),.165,role)
                        if role=='Veneer':
                            for a,c in zip(piece,piece[1:]+piece[:1]):
                                if abs(a[1]-top)<1e-6 and abs(c[1]-top)<1e-6:
                                    lo,hi=sorted((a[0],c[0]));depth=.072-recess
                                    cap.prism([xf((lo,depth-.02,top+.035)),xf((hi,depth-.02,top+.035)),xf((hi,depth+.09,top+.010)),xf((lo,depth+.09,top+.010))],(0,0,-1),.028,'Veneer')
                if not adj and split is not None and recess:
                    lo=min(v[0] for v in poly) if poly else 0;hi=max(v[0] for v in poly) if poly else 0
            wall.finish();foundation.finish();cap.finish()
            trim=b.mesh(block.name+'_'+face+'_Trim',component='corner_posts',block=block.name,face=face)
            # Trim starts at the actual cladding edge above concrete/veneer.
            low=top+.04 if top is not None else base_top+.02
            for u in (.035,length-.035):
                p=xf((u,0,0));height=block.height(p.x,p.y)-.151-low
                if height>.02 and not any(v is not block and v.contains(*(xf((u,.02,0))[:2]),.015) for v in b.plan['blocks']):
                    trim.box((u,.036,low+height/2),(.07,.045,height),r=.001,xf=xf)
            # A frieze follows the true gable or bearing line.
            from build import exterior_edges
            for poly,adj in wall_sections(b,block,face):
                lo=min(v[0] for v in poly);hi=max(v[0] for v in poly)
                a=xf((lo,.032,0));c=xf((hi,.032,0));a.z=block.height(a.x,a.y)-.195;c.z=block.height(c.x,c.y)-.195
                if (a-c).length>.03:trim.beam(a,c,.072,.024,r=0)
            if recess:
                trim.box((length/2,-recess/2+.012,lv['upper']-.205),(length,recess+.025,.089),r=.001,xf=xf)
                # Closed soffit under the cantilever, bedded into both walls.
                trim.box((length/2,-recess/2+.014,lv['upper']-.26),(length,recess+.04,.015),r=0,xf=xf)
            trim.finish()
            if s['siding'] in ('battens','grooved') and s['wall_mix']!='all_brick':
                bat=b.mesh(block.name+'_'+face+'_Battens',component='battens',block=block.name,face=face)
                for j in range(1,math.ceil(length/.3048)):
                    u=j*.3048;point=xf((u,0,0));hi=block.height(point.x,point.y)-.15
                    low=top+.05 if top is not None else base_top+.02
                    segments=[[(u-.019,low),(u+.019,low),(u+.019,hi),(u-.019,hi)]]
                    for o in b.openings:
                        if (o['block'],o['face'])==(block.name,face):
                            segments=[p for v in segments for p in subtract(v,[(1,0,-o['u']+o['w']/2+.10),(-1,0,o['u']+o['w']/2+.10),(0,1,-o['z']+.10),(0,-1,o['z']+o['h']+.13)])]
                    for piece in segments:
                        if piece:bat.prism([xf((x,.026,z)) for x,z in piece],(-n[0],-n[1],0),.025,'Siding')
                bat.finish()


def bay(b,o):
    """Three planar glazed facets and a supported seat, 16 inches projection."""
    block=next(v for v in b.plan['blocks'] if v.name==o['block']);xf,n,_=b.frame(block,o['face']);u,z,w,h=(o[k] for k in ('u','z','w','h'))
    depth=.4064;center=w*.58;side=(w-center)/2;angle=math.atan2(depth,side);slant=math.hypot(side,depth)
    frame=b.frame
    for j,(cx,d,ww,ang) in enumerate(((u-w/2+side/2,depth/2,slant,-angle),(u,depth,center,0),(u+w/2-side/2,depth/2,slant,angle))):
        # Each sash is made by the common window assembler in its local plane.
        def facet(bl,fa,cx=cx,d=d,ang=ang):
            def transform(p):
                du=p[0]-u;return xf((cx+math.cos(ang)*du+math.sin(ang)*p[1],d-math.sin(ang)*du+math.cos(ang)*p[1],p[2]))
            return transform,n,block.width
        b.frame=facet
        local={**o,'id':o['id']+f'_Bay_{j}','u':u,'w':ww,'style':'picture' if j==1 else 'hung','shutters':False}
        # Avoid the picture subdivision on the central fixed light.
        local['style']='fixed' if j==1 else 'hung'
        window(b,local)
    b.frame=frame
    me=b.mesh(o['id']+'_BaySeat',component='bay',block=block.name)
    footprint=[(u-w/2,0),(u-center/2,depth),(u+center/2,depth),(u+w/2,0)]
    for zz in (z-.08,z+h+.06):me.prism([xf((x,v,zz)) for x,v in footprint],(0,0,-1),.045)
    # Knee brackets carry the seat; no floating glass bay.
    for x in (u-center*.35,u+center*.35):me.beam(xf((x,.018,z-.52)),xf((x,depth-.04,z-.10)),.065,r=.001)
    me.finish()


def wells(b):
    for o in b.openings:
        if not o.get('well'):continue
        block=next(v for v in b.plan['blocks'] if v.name==o['block']);xf,n,_=b.frame(block,o['face']);u=o['u']
        me=b.mesh(o['id']+'_Well',component='window_well',opening_id=o['id'],allow_boundary=True)
        vs=[]
        for j in range(33):
            a=math.pi*j/32
            for z in (-.22,.12):
                d=.56*math.sin(a)+.012;xx=u+(o['w']/2+.20)*math.cos(a)
                vs.append(xf((xx,d,z)))
        me.geom(vs,[(2*j,2*j+1,2*j+3,2*j+2) for j in range(32)],color=(.25,.26,.24))
        me.prism([xf((u-o['w']/2-.18,0,-.22)),xf((u+o['w']/2+.18,0,-.22)),xf((u+o['w']/2+.18,.50,-.22)),xf((u-o['w']/2-.18,.50,-.22))],(0,0,-1),.02,'Concrete')
        me.finish()


def driveway(b):
    d=b.plan['driveway'];x=d['x'];w=d['width'];back=d['back'];front=d['front'];end=d['back_z']-.01
    me=b.mesh('Driveway',component='driveway')
    # Level apron followed by a continuously graded drive; no buried door.
    stations=[(front,d['front_z']), (back-1.25,end), (back+.035,end)]
    for (y,z),(yy,zz) in zip(stations,stations[1:]):
        me.prism([(x-w/2,y,z),(x+w/2,y,z),(x+w/2,yy,zz),(x-w/2,yy,zz)],(0,0,-1),.10,'Concrete')
    me.finish()
    if end<-.1:
        walls=b.mesh('Driveway_RetainingCheeks',component='retaining',allow_boundary=False)
        for side in (-1,1):
            xx=x+side*(w/2+.09)
            walls.prism([(xx,front,.025),(xx,back+.10,.025),(xx,back+.10,end-.12)],(side,0,0),.16,'Concrete')
        walls.finish()


def sectional(b,ob,o):
    """Retain the shared stamped panels as four moving rigid sections."""
    import bmesh
    block=next(v for v in b.plan['blocks'] if v.name==o['block']);xf,_,_=b.frame(block,o['face'])
    h=o['h']/4
    for row in range(4):
        bm=bmesh.new();bm.from_mesh(ob.data)
        # The original low-cost section construction keeps each section's
        # faces within its Z band, including its bead and recessed islands.
        discard=[f for f in bm.faces if min(3,max(0,int((f.calc_center_median().z-o['z'])/h)))!=row]
        bmesh.ops.delete(bm,geom=discard,context='FACES')
        loose=[v for v in bm.verts if not v.link_faces]
        if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
        me=bpy.data.meshes.new(f'GaragePanel{row+1}');bm.to_mesh(me);bm.free()
        for mat in ob.data.materials:me.materials.append(mat)
        # Sectional leaves run behind the masonry/frame, not within its
        # thickness. A 180 mm recess clears the solid header on lift.
        me.transform(Matrix.Translation((0,.18,0)))
        if b.plan['seed']%6==0 and row==0:
            # A shallow parking impact in an old lower steel section. The
            # stamped profile survives; no isolated damage box or decal.
            center=xf((o['u']+.30,-.201,o['z']+.30))
            for v in me.vertices:
                weight=math.exp(-((v.co.x-center.x)/.36)**2-((v.co.z-center.z)/.20)**2)
                v.co.y+=.012*weight
        name=f'GaragePanel{row+1}';pivot=G.pivot(name,xf((o['u'],-.225,o['z']+(row+1)*h)))
        pivot.parent=b.root;pivot['motion_kind']='sectional_track';pivot['section']=row+1
        pivot['section_height_m']=h;pivot['travel_m']=o['h']+.55;pivot['track_radius_m']=.20
        pivot['pivot_axis']='X';pivot['range_degrees']=[-90,0]
        pivot['closed_top_m']=list(pivot.location);b.moving[name]=pivot
        part=bpy.data.objects.new(name+'_Leaf',me);bpy.context.collection.objects.link(part)
        part.parent=pivot;bpy.context.view_layer.update();me.transform(pivot.matrix_world.inverted())
        for key,value in ob.items():part[key]=value
        part['part']=name;part['component']='garage_panel';part['export_part']=name
        part['block']=block.name
        b.objects.append(part)
    # The guides and hanger brackets are fixed to real jambs / ceiling.
    track=b.mesh('Garage_Tracks',component='garage_track',block=block.name,allow_boundary=True)
    for side in (-1,1):
        x=o['u']+side*(o['w']/2+.05)
        for sign in (-1,1):
            points=[xf((x+sign*.016,-.260,o['z']+.04)),xf((x+sign*.016,-.260,o['z']+o['h']+.06))]
            points += [xf((x+sign*.016,-.260-.20*(1-math.cos(t)),o['z']+o['h']+.06+.20*math.sin(t))) for t in [k*math.pi/24 for k in range(1,13)]]
            points.append(xf((x+sign*.016,-.260-o['h']-.40,o['z']+o['h']+.26)))
            for a,c in zip(points,points[1:]):track.beam(a,c,.010,.020,color=(.25,.26,.25),r=0)
    track.finish();b.objects.remove(ob);bpy.data.objects.remove(ob,do_unlink=True)


def foyer(b):
    """Shallow entry room and genuine short flights, visible through the door.

    These are room backings, not a complete interior or a permit plan.
    """
    p=b.plan;m=p['blocks'][0];lv=p['levels'];x=p['door_x'];floor=lv['living']
    room=b.mesh('Entry_Foyer',component='foyer');cream=(.32,.30,.255)
    room.box((x,m.y0+.58,floor-.025),(1.94,1.42,.05),color=(.13,.085,.045),r=0)
    # Reveal walls leave clear circulation into the split stair hall.
    for sign in (-1,1):room.box((x+sign*.98,m.y0+1.6,floor+1.12),(.06,2.5,2.24),color=cream,r=0)
    room.box((x,m.y0+3.0,floor+1.3),(2.0,.06,3.0),color=cream,r=0)
    room.box((x,m.y0+1.5,floor+2.38),(2.0,2.8,.04),color=cream,r=0)
    for j,flight in enumerate(p['stairs']):
        xx=x+(-.48 if j else .48);nr=flight['risers'];step=flight['riser_m'];tread=flight['tread_m']
        for k in range(nr-1):
            zz=floor+(k+1)*step if j==0 else floor-(k+1)*step
            yy=m.y0+1.3+(k+.5)*tread
            room.box((xx,yy,zz-.018),(.87,tread+.020,.036),color=(.16,.115,.070),r=.001)
            rz=zz-step/2 if j==0 else zz+step/2
            room.box((xx,yy-tread/2,rz),(.87,.019,step),color=(.30,.28,.23),r=0)
        a=(xx-.43,m.y0+1.28,floor-.12);end=(xx-.43,m.y0+1.3+(nr-1)*tread,flight['to_z']-.12 if j==0 else flight['from_z']-.12)
        room.beam(a,end,.045,.19,color=(.16,.115,.07),r=0)
    room.finish()


def roof_wall_flashing(b):
    if b.plan['spec']['kind']!='side':return
    main,wing=b.plan['blocks'][:2];right=wing.cx>main.cx;x=main.x1 if right else main.x0
    inward=-1 if right else 1;y0=max(main.y0,wing.y0);y1=min(main.y1,wing.y1)
    me=b.mesh('LivingRoof_WingStepFlashing',component='flashing',block='Main',allow_boundary=True)
    count=math.ceil((y1-y0)/.15)
    for j in range(count):
        a=y0+(y1-y0)*j/count;c=min(y1,y0+(y1-y0)*(j+1)/count+.025)
        if wing.height(x,(a+c)/2)<main.height(x,(a+c)/2)+.17:continue
        apron=[(xx,yy,main.height(xx,yy)+.008) for xx,yy in ((x+inward*.006,a),(x+inward*.16,a),(x+inward*.16,c),(x+inward*.006,c))]
        me.prism(apron,(0,0,-1),.002,color=(.19,.195,.18))
        za=main.height(x,a);zc=main.height(x,c);top=max(za,zc)+.14
        me.prism([(x+inward*.014,a,za+.007),(x+inward*.014,c,zc+.007),(x+inward*.014,c,top),(x+inward*.014,a,top)],(-inward,0,0),.002,color=(.21,.22,.20))
    me.finish()


def build(plan):
    b=SplitBuilder(plan);shell(b)
    all_openings=b.openings[:]
    for o in all_openings:
        b.openings=[o];b.frame_recess=o.get('recess',0)
        if o['kind']=='window':
            if o['style']=='bay':bay(b,o)
            else:window(b,o)
        elif o['kind']=='service':portal(b,o)
        else:doors(b)
        opening_masonry(b)
        if o['kind']=='garage':
            ob=next(v for v in b.objects if v.get('component')=='garage_door')
            sectional(b,ob,o)
    b.openings=all_openings;b.frame_recess=0
    roofs(b);roof_wall_flashing(b)
    oldfloor=plan['blocks'][0].floor;oldhood=plan['spec']['hood']
    plan['blocks'][0].floor=plan['levels']['living']
    if plan['porch'] is None:plan['spec']['hood']='none'
    cape_landing(b)
    plan['spec']['hood']=oldhood;plan['blocks'][0].floor=oldfloor
    # Rear landing is at the actual kitchen level, including raised foyer.
    oldfloor=plan['blocks'][0].floor
    rear=next(o for o in b.openings if o['kind']=='service')
    plan['blocks'][0].floor=rear['z'];cape_landing(b,True);plan['blocks'][0].floor=oldfloor
    generic=bpy.data.objects.get('GarageService_Step')
    if generic:b.objects.remove(generic);bpy.data.objects.remove(generic,do_unlink=True)
    if 'ServiceDoor' in b.moving:b.moving['ServiceDoor']['range_degrees']=[-100,0]
    original=b.plan;main=plan['blocks'][0]
    # Shared service positions use the living wing, never the buried garage.
    service_main=copy.copy(main);service_main.floor=plan['levels']['living']
    b.plan={**plan,'blocks':[service_main,service_main]};services(b);service_mounts(b);b.plan=original
    if plan['spec']['garage']['kind']=='carport':
        garage=next(v for v in plan['blocks'] if v.name=='Garage')
        b.plan={**plan,'blocks':[main,garage]};carport(b);b.plan=original
    # The reused chimney's outer-end choice follows the two-story wing.
    b.plan={**plan,'spec':{**plan['spec'],'garage':{**plan['spec']['garage'],'side':plan['spec']['wing']['side']}}}
    chimney(b);b.plan=original
    rail=b.mesh('Entry_IronRail',component='entry_rail')
    if plan['spec']['rail']:
        top=plan['levels']['living']-.010;yy=main.y0-.94;x=plan['door_x']+.77
        for y,z in ((yy,top),(yy-.65,max(.06,top-.36))):
            rail.box((x,y,z+.44),(.025,.025,.88),color=(.026,.029,.023),r=.001)
        rail.beam((x,yy,top+.88),(x,yy-.65,max(.06,top-.36)+.88),.032,.025,color=(.026,.029,.023),r=.001)
    rail.finish();wells(b);driveway(b);foyer(b)
    bpy.context.view_layer.update();return b
