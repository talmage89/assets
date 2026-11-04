"""Cape construction using shared solid skins, roof union, sash and services.

All parts are authored; the source checkpoint does not allocate delivery maps.
Dormer cheeks start on the actual parent slope, never at first-floor grade.
"""
import math
import json
import bpy
from mathutils import Vector
from build import Builder, Mesh, wall_sections, doors, exterior_edges
from plan import clip, subtract, roof_faces, roof_junctions, wall_frame
from cape_plan import roof_parts
from ranch_drain import drain
from ranch_build import window as picture_window, services as shared_services, chimney as shared_chimney
from additions import portal


class CapeMesh(Mesh):
    def box(self,p,s,role='Trim',color=None,r=.0015,xf=None):
        # Sub-40 mm sash/track/metal bevels belong in the later normal map.
        # Keep the casing/sill silhouette and shared construction dimensions.
        if self.builder.plan['spec']['siding'] not in ('cement','vinyl') and self.props.get('component') in ('window','storm_window') and min(s)<.040:r=0
        if (self.builder.plan['spec']['dormers']==3 and self.builder.plan['spec']['siding'] in ('wood','cedar') or self.builder.plan['spec']['siding']=='aluminum') and self.props.get('component')=='window' and role=='Trim' and self.props.get('opening') and json.loads(self.props['opening'])['face']!='front' and min(s)<.070:r=0
        if self.props.get('component')=='window' and abs(p[1]-.091)<1e-6 and abs(s[1]-.19)<1e-6 and abs(s[2]-.041)<1e-6:
            # Keep the supporting sill block below its sloping weather surface.
            # Its former flat top concealed that surface and the lifted film.
            p=(p[0],p[1],p[2]-.016)
        if self.props.get('component')=='window' and role=='Trim' and abs(p[1]+.28)<1e-6:
            # A real dark room behind the curtains, rather than a 290 mm box.
            p=(p[0],-1.15,p[2])
            color=(.008,.008,.007)
            for sign in (-1,1):
                super().box((p[0]+sign*(s[0]/2),-.66,p[2]),(.018,.96,s[2]),role,(.035,.033,.027),0,xf)
            # A few low furniture silhouettes interrupt the empty dark box.
            # Their top is about chair-back height above the first-floor datum.
            sill=p[2]-s[2]/2
            opening=json.loads(self.props['opening']);room=next(v for v in self.builder.plan['blocks'] if v.name==opening['block']);ground=room.floor
            super().box((p[0],-.66,ground-.012),(s[0]+.03,.98,.024),role,(.012,.011,.009),0,xf)
            super().box((p[0]+.16,-.66,sill+.20),(.22,.022,.22),role,(.025,.022,.018),0,xf)
            for sign in (-1,1):super().box((p[0]+.16+sign*.10,-.66,(ground+sill+.31)/2),(.025,.025,sill+.31-ground),role,(.018,.016,.013),0,xf)
            super().box((p[0]+.16,-.55,ground+.44),(.25,.30,.025),role,(.025,.022,.018),0,xf)
        return super().box(p,s,role,color,r,xf)


class CapeBuilder(Builder):
    def mesh(self,name,part='Static',**props):return CapeMesh(self,name,part,**props)


def foundation_top(block):
    """Exposed concrete datum, below the floor; garage remains a slab."""
    return min(.6096,block.floor-.0762) if block.floor>=.40 else max(.04,block.floor-.205)


def shell(b):
    main=b.plan['blocks'][0]
    for block in b.plan['blocks']:
        if block.name=='Breezeway':continue
        dorm=block.name.startswith('Dormer') or block.name=='RearShed'
        for face in ('front','back','left','right'):
            xf,n,length=b.frame(block,face)
            me=b.mesh(block.name+'_'+face+'_Wall',component='wall',block=block.name,face=face)
            base=b.mesh(block.name+'_'+face+'_Foundation',component='foundation',block=block.name,face=face)
            foundation_intervals=[]
            for poly,adjoining in wall_sections(b,block,face):
                if dorm:
                    # Exact planar intersections form the cheek's wedge.
                    origin,t,_,_=wall_frame(block,face)
                    pieces=[]
                    for plane in main.planes():
                        a=plane[0]*t[0]+plane[1]*t[1];c=plane[0]*origin[0]+plane[1]*origin[1]+plane[2]-.012
                        piece=clip(poly,-a,1,-c)
                        # Retain only this parent plane's active domain.
                        for q in main.planes():
                            piece=clip(piece,(q[0]-plane[0])*t[0]+(q[1]-plane[1])*t[1],0,(q[0]-plane[0])*origin[0]+(q[1]-plane[1])*origin[1]+q[2]-plane[2])
                        if piece:pieces.append(piece)
                else:pieces=[poly]
                for opening in [o for o in b.openings if o['block']==block.name and o['face']==face]:
                    o=opening;cuts=[(1,0,-o['u']+o['w']/2),(-1,0,o['u']+o['w']/2),(0,1,-o['z']),(0,-1,o['z']+o['h'])]
                    pieces=[p for v in pieces for p in subtract(v,cuts)]
                if not dorm:pieces=[q for p in pieces if (q:=clip(p,0,1,-foundation_top(block)))]
                for part in pieces:me.prism([xf((u,.012,z)) for u,z in part],(-n[0],-n[1],0),.165,'Siding')
                if not adjoining and not dorm:
                    foundation_intervals.append((min(v[0] for v in poly),max(v[0] for v in poly)))
            # Several clipped roof/wall sections can share a ground interval.
            # Build their union once, rather than overlapping foundation solids.
            merged=[]
            for lo,hi in sorted(foundation_intervals):
                if merged and lo<=merged[-1][1]+1e-6:merged[-1]=(merged[-1][0],max(hi,merged[-1][1]))
                else:merged.append((lo,hi))
            for lo,hi in merged:
                top=foundation_top(block);pieces=[[(lo,0),(hi,0),(hi,top),(lo,top)]]
                for u,z,w,h in basement_holes(b,block,face):
                    pieces=[p for v in pieces for p in subtract(v,[(1,0,-u+w/2),(-1,0,u+w/2),(0,1,-z),(0,-1,z+h)])]
                for p in pieces:base.prism([xf((u,-.024,z)) for u,z in p],(-n[0],-n[1],0),.18,'Concrete')
                base.box(((lo+hi)/2,-.016,top-min(.044,top)/2),(hi-lo,.024,min(.044,top)),'Concrete',r=.001,xf=xf)
            me.finish();base.finish()
        trim=b.mesh(block.name+'_Corners',component='corner_posts',block=block.name)
        for x in (block.x0,block.x1):
            for y in (block.y0,block.y1):
                if any(v is not block and v.name not in ('RearShed',) and not v.name.startswith('Dormer') and not (block.name.startswith('Dormer') and v.name=='Main') and v.contains(x,y,.001) for v in b.plan['blocks']):continue
                bottom=main.height(x,y)-.01 if dorm else foundation_top(block)+.012;top=block.height(x,y)-.145
                if top-bottom<.05:continue
                sx=-1 if x==block.x0 else 1;sy=-1 if y==block.y0 else 1
                trim.box((x+sx*.020,y-sy*.034,(bottom+top)/2),(.032,.089,top-bottom),r=0 if block.name.startswith('Dormer') else .001)
                trim.box((x-sx*.034,y+sy*.020,(bottom+top)/2),(.089,.032,top-bottom),r=0 if block.name.startswith('Dormer') else .001)
        trim.finish()
        if not dorm:
            # Sloped water table bridges the siding/foundation at the real floor.
            water=b.mesh(block.name+'_WaterTable',component='water_table',block=block.name)
            for face in ('front','back','left','right'):
                xf,n,length=b.frame(block,face);z=foundation_top(block)
                for poly,adj in wall_sections(b,block,face):
                    if adj:continue
                    lo=min(v[0] for v in poly);hi=max(v[0] for v in poly)
                    water.prism([xf((lo,.04,z+.045)),xf((hi,.04,z+.045)),xf((hi,.08,z+.018)),xf((lo,.08,z+.018))],(0,0,-1),.035)
            water.finish()


def basement_holes(b,block,face):
    if block.name!='Main':return []
    if b.plan['spec']['foundation']=='crawlspace':
        return [(block.width*f,.13,.40,.18) for f in (.15,.85)] if face in ('front','back') else []
    length=block.width if face=='back' else block.depth;top=foundation_top(block)
    if top<.18:return []
    # Keep the exposed wells in the rear quarters, clear of chimney and additions.
    if face!='back':return []
    return [(length*f,.075,.70,min(.30,top-.12)) for f in (.10,.90)]


def basement(b):
    m=b.plan['blocks'][0]
    for face in ('front','back'):
        xf,n,length=b.frame(m,face)
        for i,(u,z,w,h) in enumerate(basement_holes(b,m,face)):
            if b.plan['spec']['foundation']=='crawlspace':
                me=b.mesh('CrawlVent_'+face+str(i),component='crawl_vent',allow_boundary=True)
                me.box((u,-.055,z+h/2),(w-.025,.012,h-.025),color=(.012,.015,.011),r=0,xf=xf)
                for sign in (-1,1):me.box((u+sign*(w/2-.014),-.010,z+h/2),(.028,.045,h+.04),color=(.14,.16,.13),r=0,xf=xf)
                for zz in (z-.008,z+h+.008):me.box((u,-.010,zz),(w+.02,.045,.024),color=(.14,.16,.13),r=0,xf=xf)
                for k in range(5):me.box((u,.008,z+.018+k*(h-.036)/4),(w-.04,.024,.011),color=(.18,.20,.16),r=0,xf=xf)
                me.finish();continue
            me=b.mesh('BasementWindow_'+str(i),component='basement_window')
            for sign in (-1,1):me.box((u+sign*(w/2-.018),-.035,z+h/2),(.036,.055,h),r=.001,xf=xf)
            for zz in (z+.018,z+h-.018):me.box((u,-.035,zz),(w,.055,.036),r=.001,xf=xf)
            me.box((u,-.064,z+h/2),(w-.07,.004,h-.07),'Glass',(1,1,1),0,xf)
            me.box((u,-.16,z+h/2),(w-.07,.012,h-.07),color=(.008,.009,.007),r=0,xf=xf)
            # Open corrugated galvanized well; a half-ellipse attached to wall.
            vs=[]
            for j in range(21):
                a=math.pi*j/20;xx=u+.48*math.cos(a);dep=.015+.42*math.sin(a)
                for zz in (0,.12):vs.append(xf((xx,dep,zz)))
            me.geom(vs,[(j*2,j*2+1,(j+1)*2+1,(j+1)*2) for j in range(20)],color=(.24,.25,.23))
            me.finish()


def roofs(b):
    blocks=roof_parts(b.plan);faces=roof_faces(blocks)
    # Exact union is shared with the accepted two house types.
    for i,row in enumerate(faces):
        p=row['plane'];me=b.mesh(f"{row['block']}_Roof_{i}",component='roof',block=row['block'])
        me.prism([(x,y,p[0]*x+p[1]*y+p[2]) for x,y in row['polygon']],(0,0,-1),.14,'Shingles');me.finish()
    for block in blocks:
        trim=b.mesh(block.name+'_RoofEdges',component='eave_rake_soffit',block=block.name)
        gutters=b.mesh(block.name+'_Drainage',component='drainage',block=block.name)
        for index,(pts,n) in enumerate(exterior_edges(block,faces)):
            a,c=map(Vector,pts);normal=Vector((*n,0));level=abs(a.z-c.z)<.005
            trim.prism([a+Vector((0,0,-.018)),c+Vector((0,0,-.018)),c+Vector((0,0,-.151)),a+Vector((0,0,-.151))],normal,.019)
            inner=[Vector((max(block.x0,min(block.x1,p.x)),max(block.y0,min(block.y1,p.y)),p.z-.14)) for p in (a,c)]
            trim.prism([a+Vector((0,0,-.14)),c+Vector((0,0,-.14)),inner[1],inner[0]],(0,0,-1),.009)
            trim.beam(a+normal*.01+Vector((0,0,-.013)),c+normal*.01+Vector((0,0,-.013)),.014,.014,color=(.40,.41,.37),r=0)
            trim.beam(a+Vector((0,0,.003)),c+Vector((0,0,.003)),.024,.012,'Shingles',r=0)
            # Dormer eaves discharge onto the parent roof, with a drip edge;
            # pipes on the house/additions use the existing rounded K system.
            if level and block.name in ('Main','Wing','Garage'):
                drain(b,gutters,a,c,n,block,index)
                # Concealed steel hangers at 3 ft centers, fixed to the fascia.
                axis=0 if abs(c.x-a.x)>abs(c.y-a.y) else 1
                lo,hi=sorted((a[axis],c[axis]))
                for k in range(math.ceil(lo/.9144),math.ceil(hi/.9144)):
                    t=(k*.9144-a[axis])/(c[axis]-a[axis]);q=a.lerp(c,t)
                    gutters.beam(q-normal*.02+Vector((0,0,-.025)),q+normal*.12+Vector((0,0,-.038)),.016,.003,color=(.24,.25,.22),r=0)
            if b.plan['spec']['returns'] and block.name=='Main' and not level:
                low=min((a,c),key=lambda p:p.z)
                # Short boxed cornice return, supported against the gable.
                end=low+Vector((0,.31 if low.y<block.cy else -.31,0))
                trim.beam(low+Vector((0,0,-.12)),end+Vector((0,0,-.12)),.085,.07,r=.001)
        trim.finish();gutters.finish()
    for i,row in enumerate(roof_junctions(blocks)):
        a,c=map(Vector,row['points']);side=(c-a).cross(Vector((0,0,1))).normalized()
        me=b.mesh('RoofJunction_'+str(i),component=row['kind'])
        if row['kind']=='ridge':
            vs=[]
            for p in (a,c):vs.extend((p-side*.11+Vector((0,0,-.05)),p+Vector((0,0,.035)),p+side*.11+Vector((0,0,-.05))))
            me.geom(vs,[(0,3,4,1),(1,4,5,2)],'Shingles')
        else:
            # Both halves bed onto their own slopes, rather than a level strip
            # bridging a steep valley and penetrating the shingles.
            owners=[v for v in blocks if v.name in row['blocks']]
            for sign in (-1,1):
                vs=[]
                for p in (a,c):
                    q=p+side*.065*sign;z=max(v.height(q.x,q.y) for v in owners)
                    vs.extend((p+Vector((0,0,.007)),Vector((q.x,q.y,z+.007))))
                me.prism([vs[0],vs[2],vs[3],vs[1]],(0,0,-1),.002,color=(.18,.19,.17))
        me.finish()
    # Dormer cheeks receive stepped metal, each top edge set into the siding.
    main=blocks[0]
    for block in b.plan['blocks']:
        if not (block.name.startswith('Dormer') or block.name=='RearShed'):continue
        me=b.mesh(block.name+'_StepFlashing',component='flashing',block=block.name)
        for x in (block.x0,block.x1):
            y0=block.y0;y1=min(block.y1,main.y0+(block.eave-.14-main.eave)/main.pitch) if block.name.startswith('Dormer') else block.y1
            count=max(1,math.ceil((y1-y0)/.18))
            for j in range(count):
                ya=y0+(y1-y0)*j/count;yb=y0+(y1-y0)*(j+1)/count+.025
                za=main.height(x,ya);zb=main.height(x,yb);top=max(za,zb)+.09
                me.prism([(x,ya,za+.004),(x,yb,zb+.004),(x,yb,top),(x,ya,top)],(1 if x==block.x0 else -1,0,0),.002,color=(.26,.27,.24))
        me.finish()
    vents=b.mesh('Plumbing_RoofVents',component='roof_vent')
    # One boot beside, never through, the rear shed cheeks.
    x=main.x0+.26;y=main.cy+.60;z=main.height(x,y)
    vents.prism([(xx,yy,main.height(xx,yy)+.006) for xx,yy in [(x-.12,y-.18),(x+.12,y-.18),(x+.12,y+.18),(x-.12,y+.18)]],(0,0,-1),.005,color=(.10,.105,.095))
    vents.tube([(x,y,z),(x,y,z+.40)],.038,color=(.075,.078,.071),sides=10,closed=False);vents.finish()


def landing(b,rear=False):
    m=b.plan['blocks'][0];s=b.plan['spec'];floor=m.floor;top=floor-.010
    opening=next(o for o in b.openings if o['kind']=='service') if rear else None
    x=m.x0+opening['u'] if rear else b.plan['door_x'];y=m.y1 if rear else m.y0;direction=1 if rear else -1
    me=b.mesh('Rear_Stoop' if rear else 'Porch_Concrete',component='rear_landing' if rear else 'porch_steps')
    width=1.45 if rear else 1.75;depth=1.02
    me.box((x,y+direction*(depth/2+.025),top/2),(width,depth+.05,top),'Concrete',r=.004)
    count=math.ceil(top/.19);riser=top/count
    for j in range(count-1):
        z=top-(j+1)*riser;yy=y+direction*(depth+(j+.5)*.28)
        me.box((x,yy,z/2),(width-.18,.285,z),'Concrete',r=.003)
    me.finish()
    if not rear and s['hood']!='none':
        p=b.plan['porch'];me=b.mesh('Porch_Supports',component='porch_structure')
        beam_z=p.eave-.22
        me.box((p.cx,p.y0+.16,beam_z),(p.width-.10,.10,.14),r=.001)
        if s['hood']=='portico':
            for xx in (p.x0+.13,p.x1-.13):me.box((xx,p.y0+.16,(top+beam_z-.07)/2),(.089,.089,beam_z-.07-top),r=.002)
        else:
            for xx in (p.x0+.13,p.x1-.13):
                me.beam((xx,m.y0-.04,beam_z-.46),(xx,p.y0+.16,beam_z-.075),.048,.048,r=.001)
                me.box((xx,m.y0-.035,beam_z-.22),(.065,.07,.60),r=.001)
        # Painted-board front pediment and a supported underside ceiling.
        me.prism([(p.x0,p.y0-.012,p.eave-.14),(p.x1,p.y0-.012,p.eave-.14),(p.cx,p.y0-.012,p.height(p.cx,p.y0)-.14)],(0,1,0),.018)
        me.box((p.cx,p.cy,beam_z+.05),(p.width-.12,p.depth,.018),r=0)
        me.box((p.cx,p.y0+.015,p.eave-.19),(p.width,.060,.10),r=.001)
        me.finish()


def build(plan):
    b=CapeBuilder(plan);shell(b)
    # Picture units reuse the accepted ranch assembly. Other windows keep the
    # colonial sash/trim, with optional original grille divisions.
    pictures=[o for o in b.openings if o.get('style')=='picture']
    for o in pictures:b.openings.remove(o)
    doors(b)
    for o in pictures:
        o['system']='vinyl';picture_window(b,o);b.openings.append(o)
    for o in b.openings:
        if o['kind']=='service':portal(b,o)
    # Its generic low garage step is replaced by the Cape's real rear stoop.
    step=bpy.data.objects.get('GarageService_Step')
    if step:
        b.objects.remove(step);bpy.data.objects.remove(step,do_unlink=True)
    if 'ServiceDoor' in b.moving:b.moving['ServiceDoor']['range_degrees']=[-100,0]
    roofs(b);landing(b);landing(b,True);basement(b)
    storms(b);breezeway(b)
    # Existing service assemblies are constructed in a shallow copied view of
    # this plan. Real walls/openings/sockets stay in the original Cape plan.
    original=b.plan
    dummy=plan['blocks'][0]
    b.plan={**plan,'blocks':[dummy,dummy],'spec':{**plan['spec'],'aerial':None}}
    shared_services(b)
    service_mounts(b)
    # The broad ranch shaft is reused with a Cape-specific location/size view.
    b.plan=original
    chimney(b)
    bpy.context.view_layer.update();return b


def storms(b):
    if not b.plan['spec']['storms']:return
    for o in b.openings:
        if o['kind']!='window' or o.get('style')=='picture':continue
        block=next(v for v in b.plan['blocks'] if v.name==o['block']);xf,n,l=b.frame(block,o['face']);u,z,w,h=(o[k] for k in ('u','z','w','h'))
        me=b.mesh(o['id']+'_Storm',component='storm_window',window_system='aluminum')
        c=(.28,.29,.26)
        for sign in (-1,1):me.box((u+sign*(w/2-.012),.070,z+h/2),(.024,.024,h),color=c,r=.001,xf=xf)
        for zz in (z+.012,z+h/2,z+h-.012):me.box((u,.070,zz),(w-.024,.024,.024),color=c,r=.001,xf=xf)
        for j in range(2):me.box((u,.058,z+(j+.5)*h/2),(w-.05,.003,h/2-.035),'Glass',(1,1,1),0,xf)
        for sign in (-1,1):me.tube([xf((u+sign*(w/2-.012),.081,z+h-.012)),xf((u+sign*(w/2-.012),.084,z+h-.012))],.0025,color=(.21,.22,.20),sides=6)
        me.finish()


def breezeway(b):
    bridge=next((v for v in b.plan['blocks'] if v.name=='Breezeway'),None)
    if not bridge:return
    me=b.mesh('Breezeway_Structure',component='breezeway',block=bridge.name)
    me.box((bridge.cx,bridge.cy,.0508),(bridge.width,bridge.depth,.1016),'Concrete',r=.003)
    for x in (bridge.x0+.07,bridge.x1-.07):
        for y in (bridge.y0+.06,bridge.y1-.06):me.box((x,y,(bridge.eave-.19+.1016)/2),(.089,.089,bridge.eave-.19-.1016),r=.001)
    for y in (bridge.y0+.06,bridge.y1-.06):me.box((bridge.cx,y,bridge.eave-.23),(bridge.width,.10,.18),r=.001)
    me.finish()
    # The open connector has an actual back screen, not a solid anonymous box.
    back=b.mesh('Breezeway_BackWall',component='breezeway_back',block=bridge.name)
    back.box((bridge.cx,bridge.y1-.045,.55),(bridge.width-.16,.065,.90),'Siding',r=.001)
    for zz in (1.04,bridge.eave-.33):back.box((bridge.cx,bridge.y1-.04,zz),(bridge.width-.12,.065,.070),r=.001)
    # 19 x 38 mm lattice strips, 160 mm centers, clipped to a framed opening.
    lo,hi=bridge.x0+.09,bridge.x1-.09;z0,z1=1.08,bridge.eave-.37
    for slope in (-1,1):
        for k in range(-18,20):
            intercept=z0+k*.16
            ts=[(x,intercept+slope*(x-lo)) for x in (lo,hi)]
            for zz in (z0,z1):ts.append((lo+(zz-intercept)/slope,zz))
            pts=sorted({(round(x,8),round(z,8)) for x,z in ts if lo-1e-7<=x<=hi+1e-7 and z0-1e-7<=z<=z1+1e-7})
            if len(pts)==2:back.beam((pts[0][0],bridge.y1-.02-slope*.011,pts[0][1]),(pts[1][0],bridge.y1-.02-slope*.011,pts[1][1]),.025,.019,color=(.25,.245,.21),r=0)
    back.finish()


def chimney(b):
    # Shared crown, liners, cap and roof-conforming apron/counterflashing.
    # Relocate the authored ranch broad-shaft construction to the clear end.
    if not b.plan['spec']['chimney']:return
    main=b.plan['blocks'][0];original=b.plan;spec=b.plan['spec'];side=spec['garage']['side']
    # Choose opposite the wing/breezeway; never run a shaft through an addition.
    occupied={('left' if v.cx<main.cx else 'right') for v in b.plan['blocks'] if v.name in ('Wing','Breezeway')}
    target='right' if 'left' in occupied else 'left'
    b.plan={**original,'spec':{**spec,'chimney_offset':0.,'chimney_position':.74,'garage':{**spec['garage'],'side':'left' if target=='right' else 'right'}}}
    shared_chimney(b);b.plan=original


def service_mounts(b):
    m=b.plan['blocks'][0];xf,n,l=b.frame(m,'back')
    me=b.mesh('Cape_ServiceMounts',component='services')
    # Stand-off meter lugs bed into the wall; piping keeps its accepted route.
    for dx in (-.10,.10):
        for zz in (1.07,1.43):me.box((l*.29+dx,.044,zz),(.035,.066,.06),color=(.25,.27,.24),r=.001,xf=xf)
    me.box((l*.65,.041,.59),(.12,.060,.10),color=(.25,.27,.24),r=.001,xf=xf)
    x=m.x0+l*.64
    for xx,zz,rr in ((x-.45,.50,.04),(x-.36,.45,.023)):
        me.tube([(xx,m.y1+.012,zz),(xx,m.y1+.095,zz)],rr,color=(.23,.24,.20),sides=8)
    me.finish()
