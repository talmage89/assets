"""Lot-by-lot community assembly on Ground's existing material vocabulary."""
import math,random,json
from pathlib import Path
import bpy
from mathutils import Vector
from geometry import Assembly,Library,Instances,native,place,label,ROOT
from homes import build as make_home
import addons as A
from kit import model as G
from kit.tiling import world_uv


def library_material(lib,prefix):
    objects=lib.load(ROOT/'ground/export/Ground.glb')
    return next(m for o in objects if o.type=='MESH' for m in o.data.materials if m.name.startswith(prefix))


def ground_box(parent,name,p,size,mat,coverage,tint=(1,1,1)):
    ob=G.box(name,p,size,mat,0);ob.parent=parent;world_uv(ob,coverage)
    uv=ob.data.uv_layers.active
    for poly in ob.data.polygons:
        if abs(poly.normal.z)>.5:continue
        axes=sorted(range(3),key=lambda k:abs(poly.normal[k]))[:2]
        for li in poly.loop_indices:
            v=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]]/coverage,v[axes[1]]/coverage)
    # Ground's tint is authored as linear multiplier; preserve its PBR images.
    names={n.layer_name or 'Color' for n in mat.node_tree.nodes if n.type=='VERTEX_COLOR'}
    for name in names:
        attr=ob.data.color_attributes.new(name=name,type='FLOAT_COLOR',domain='POINT');ob.data.color_attributes.active_color=attr
        for v in attr.data:v.color=(*tint,1)
    ob['reused_surface']='ground';return ob


def road(parent,p,lib):
    asphalt=library_material(lib,'Asphalt');a=Assembly('PrivateStreet');a.root.parent=parent
    w=p['street_width'];span=p['span'];old=p['kind']=='old';xx=p['loop_x']
    tint=(.48,.47,.44) if old else (.43,.43,.41)
    radius=5.0
    ranges=[(x,0,w,span+20) for x in (-xx,xx)] if old else [(-xx,0,w,span),(xx,0,w,span),(0,-span/2-5,2*xx-2*radius,w),(0,span/2+5,2*xx-2*radius,w),(0,-span/2-9,w,8)]
    from site_age import road_tone
    for i,(x,y,sx,sy) in enumerate(ranges):
        ob=ground_box(a.root,'Private asphalt '+str(i),(x,y,-.035),(sx,sy,.10),asphalt,6.096,tint)
        road_tone(ob,tint,p['seed']+i)
    from terrain import road_edge
    road_edge(a.root,p,asphalt,tint)
    from site_age import road as age_road
    age_road(a,p,lib,library_material)
    if not old:
        top=span/2+5
        for cx,cy,start in ((xx-radius,-top+radius,270),(xx-radius,top-radius,0),(-xx+radius,top-radius,90),(-xx+radius,-top+radius,180)):
            vs=[]
            for i in range(13):
                t=math.radians(start+i*90/12)
                vs.extend([(cx+r*math.cos(t),cy+r*math.sin(t),.015) for r in (radius-w/2,radius+w/2)])
            fs=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(12)]
            mesh=bpy.data.meshes.new('Private circular return');mesh.from_pydata(vs,[],fs);mesh.materials.append(asphalt);mesh.update()
            ob=bpy.data.objects.new('Private circular return',mesh);bpy.context.collection.objects.link(ob);ob.parent=a.root;world_uv(ob,6.096)
            for name in {n.layer_name or 'Color' for n in asphalt.node_tree.nodes if n.type=='VERTEX_COLOR'}:
                attr=mesh.color_attributes.new(name=name,type='FLOAT_COLOR',domain='POINT');mesh.color_attributes.active_color=attr
                for v in attr.data:v.color=(*tint,1)
    for k,path in enumerate(p['roads']):
        closed=math.dist(path[0],path[-1])<1e-7
        for j,point in enumerate(path):
            next_index=j+1 if j+1<len(path) else (1 if closed else -1)
            q=path[next_index] if next_index>=0 else [point[i]+point[i]-path[j-1][i] for i in range(3)]
            yaw=math.degrees(math.atan2(q[0]-point[0],-(q[1]-point[1])))
            extras=dict(next_index=next_index,path_id=k,speed_mph=10,width_m=w,closed_path=closed)
            if not old and k==1 and next_index==-1:extras.update(connects_path=0,join_segment=len(p['roads'][0])-2,join_fraction=.5)
            a.socket(f'DrivePath_{k}_{j}',[point[0],point[1],.015],'drive_path',yaw=yaw,**extras)
    m=a.mesh('BumpsSigns',component='traffic')
    for x,y in [(x,y) for x in (-xx,xx) for y in (-span*.23,span*.28)]:
        # 3.7 m wide, 0.3 m travel depth bolt-down rubber speed bump.
        sections=[(-.18,.016),(-.13,.055),(-.06,.088),(.06,.088),(.13,.055),(.18,.016)]
        for (y0,z0),(y1,z1) in zip(sections,sections[1:]):
            m.prism([(x-w*.43,y+y0,z0),(x+w*.43,y+y0,z0),(x+w*.43,y+y1,z1),(x-w*.43,y+y1,z1)],(0,0,-1),.018,'Trim',(.055,.05,.025))
        wear=random.Random(p['seed']+round((x+y)*100))
        for j in range(9):
            # Paint survives beside the tire tracks, with chipped gaps.
            for k in range(5):
                if wear.random()<(.40 if old else .22):continue
                m.box((x-w*.40+j*w*.1,y+(k-2)*.05,.087),(w*.045*wear.uniform(.55,1),.038,.009),'Trim',(.36,.25,.035))
        m.box((x+w/2+.55,y-.8,1.02),(.06,.05,2.04),'Trim',(.25,.28,.26))
        m.box((x+w/2+.55,y-.82,1.85),(.47,.035,.60),'Trim',(.62,.57,.37),r=.007)
        label(a,'10',(x+w/2+.55,y-.843,1.86),.23,(.025,.03,.025))
        label(a,'SLOW',(x+w/2+.55,y-.843,1.69),.095,(.025,.03,.025))
    m.finish();return a


def lot(p,record,lib,parent,instances):
    spec=record['home'];seed=spec['occupant_seed'];a=Assembly(f'Lot_{record["number"]:02}');L,W=spec['length'],spec['width']
    spec=dict(spec,site_yaw=record['yaw'],lot_kind=p['kind'],corner_apron=p['kind']=='old' and record['number']==1);hn=a.root.name+'_Home'
    h=instances.get(('home',spec['variant_id'],record['yaw']),hn,lambda:make_home(spec,hn));place(h,parent=a.root)
    h['home_spec']=json.dumps(spec,sort_keys=True)
    label(a,str(record['number']),(-L*.035+.69,-W/2-.092,2.30),.11,spec['accent'])
    def part(key,suffix,factory,pos,yaw=0):
        name=a.root.name+'_'+suffix;rt=instances.get(key,name,lambda:factory(name))
        return place(rt,pos,yaw,parent=a.root)
    cp_x=L/2-2.9
    if spec['carport']:
        cp=instances.get(('carport',spec['awning_sag'],spec['era']=='1996',spec['upkeep']),a.root.name+'_Carport',lambda:A.carport(a.root.name+'_Carport',sag=spec['awning_sag'],context=spec))
        place(cp,(cp_x,-W/2-1.82,0),parent=a.root)
        marker=next(o for o in cp.children if o.get('socket_kind')=='car')
        marker.name=a.root.name+'__CarportCar';marker['vehicle_index']=(seed+1)%3
        marker['paint_index']=(seed+2)%5;marker['occupied']=seed%5!=0
    if spec['room']:
        room_variant=(seed+2)%3
        part(('room',room_variant),'AddedRoom',lambda n:A.room(n,seed=room_variant),(-L*.32,-W/2-1.20,0))
    if spec['propane']:part('propane','Propane',A.propane,(L*.13,W/2+.55,0))
    part(('ac',spec['ac']),'AC',lambda n:A.conditioner(n,spec['ac']),
         (L*.12,W/2+.17,1.80) if spec['ac']=='window' else (-L*.24,W/2+.73,0),180 if spec['ac']=='window' else 0)
    utility_y=3.25 if p['kind']=='old' else W/2+.55
    part('utility','Utility',A.utility,(-L/2-1.0,utility_y,0))
    connections=a.mesh('ServiceConnections',component='service_connections')
    for offset,radius,color in ((.10,.020,(.19,.21,.18)),(.36,.016,(.27,.29,.25)),(.85,.051,(.47,.46,.38))):
        x=-L/2-1+offset;y=utility_y+.05
        connections.tube([(x,y,.08),(x+.10,y,.03),(x+.30,y-.05,-.08),(x+.75,W/2-.25,-.08),(x+.75,W/2-.25,.48)],radius,'Trim',color,8)
    connections.finish()
    if spec['dish']:part('dish','Dish',A.dish,(L*.32,W/2+.10,1.42),180)
    part(('pots',seed%6),'PotsToy',lambda n:A.dressing(n,seed%6),(-L*.035,-W/2-2.75,0))
    from lot_dressing import add
    add(a,spec,seed)
    if spec['tarp']:
        m=a.mesh('BlueTarp',component='tarp');vs=[];fs=[]
        for j in range(7):
            for i in range(9):
                x=-L*.32+(i/8-.5)*3.0;y=(j/6-.5)*W*.80
                roof=spec['eave']+.10+.13*(1-(y/(W/2+.12))**2)
                z=roof+.006+.026*math.sin(i*2.6+j*.8)**2
                vs.append((x,y,z))
        for j in range(6):
            for i in range(8):k=j*9+i;fs.append((k,k+1,k+10,k+9))
        m.geom(vs,fs,'Trim',(.015,.085,.24));m.finish()
    # Existing household assets retain their own geometry, pivots and atlases.
    for path,name,pos,yaw,select in [
        ('trailer-park/build/native/shed.gltf','Shed',(-L/2-(2.5 if p['kind']=='old' else 1.9),1.6 if p['kind']=='old' else 2.3,0),90 if p['kind']=='old' else 0,None),
        ('trash-cart/export/TrashCart.glb','Cart',(L*.15,-W/2-.7,0) if spec['corner_apron'] else (L/2+.8,-W/2-.5,.015),90,None),
        ('mailbox/export/Mailbox.glb','Mailbox',(L/2+3.2,1.7,.015),-90,None),
        ('patio-set/export/PatioSet.glb','LawnChair',(-L*.035+.75,-W/2-1.05,spec['floor']-.025),0,'Chair'),
    ]:
        if name=='Shed' and (seed%3==0 or p['kind']=='new' and L>18.5):continue
        rt=native(lib,path,a.root.name+'_'+name,pos,yaw,select,parent=a.root)
    if seed%3==1:native(lib,'gas-grill/export/GasGrill.glb',a.root.name+'_Grill',(-L*.035+2.9,-W/2-1.8,0),180,parent=a.root)
    # Short property edge: native 4 ft chain-link with a working native gate.
    if seed%3==0:
        path='fences/chain-link/export/ChainLink.glb'
        for j in range(2):native(lib,path,a.root.name+'_Fence'+str(j),(-L/2+.5+j*3.048,-W/2-3.55,0),0,'Chain_Section',a.root)
        for j in range(3):native(lib,path,a.root.name+'_Post'+str(j),(-L/2-1.024+j*3.048,-W/2-3.55,0),0,'Chain_Terminal' if j in (0,2) else 'Chain_Line',a.root)
        native(lib,path,a.root.name+'_Gate',(-L/2+5.60,-W/2-3.55,0),0,'Chain_GateBay',a.root)
    a.socket('Car',(-L*.31,-7.20,0) if spec['corner_apron'] else (L/2+3.1,-1.1,.015),'car',yaw=90,vehicle_index=2 if spec['corner_apron'] else seed%3,paint_index=seed%5)
    a.socket('Mailbox',(L/2+3.2,1.7,0),'mailbox')
    # Real paving between uncurbed private lane and the home end.
    concrete=library_material(lib,'Concrete');gravel=seed%3==0 and not spec['corner_apron']
    mat=concrete if not gravel else library_material(lib,'Asphalt')
    # Partition the union at the carport pad rather than laying coplanar
    # slabs on top of one another. The approach meets the actual lane edge.
    cp_rect=(cp_x-3.45,cp_x+3.45,-W/2-3.595,-W/2-.045)
    xs=[L/2,L/2+5.42];ys=[-8.30 if spec['corner_apron'] else -2.55,.40]
    if spec['carport']:
        xs=sorted(set(xs+[v for v in cp_rect[:2] if xs[0]<v<xs[-1]]))
        ys=sorted(set(ys+[v for v in cp_rect[2:] if ys[0]<v<ys[-1]]))
    for x0,x1 in zip(xs,xs[1:]):
        for y0,y1 in zip(ys,ys[1:]):
            if spec['carport'] and cp_rect[0]<(x0+x1)/2<cp_rect[1] and cp_rect[2]<(y0+y1)/2<cp_rect[3]:continue
            ground_box(a.root,'Lot drive apron',((x0+x1)/2,(y0+y1)/2,-.015),(x1-x0,y1-y0,.06),mat,3.048 if not gravel else 1.5,(.80,.77,.67) if gravel else (.90,.89,.84))
    if spec['corner_apron']:
        ground_box(a.root,'Aged corner-lot hardstanding',(-.15,(-8.30-W/2-.02)/2,-.025),(L+.30,8.30-W/2-.02,.05),concrete,3.048,(.88,.85,.76))
    if spec['carport']:ground_box(a.root,'Carport pad',(cp_x,-W/2-1.82,-.015),(6.9,3.55,.06),concrete,3.048,(.86,.85,.79))
    for y in (-1.85,-.45):ground_box(a.root,'Unpaved driveway throat',(L/2+5.758,y,-.018),(.676,.48,.045),concrete,1.5,(.47,.40,.25))
    # A narrow resident-made walk connects the parking approach to the stairs.
    x0=-L*.035-spec['deck_width']/2+.475;x1=L/2+1.2;wy=-W/2-3.0
    if not spec['corner_apron']:
        if p['kind']=='old' and seed%3==0:
            from terrain import worn_walk
            worn_walk(a.root,spec,x0,x1,wy,concrete)
        else:
            ground_box(a.root,'Resident walk',((x0+x1)/2,wy,-.008),(x1-x0,.80,.045),concrete,3.048,(.78,.77,.70))
            ground_box(a.root,'Resident walk return',(x1,(wy-2.7)/2,-.008),(.80,-2.7-wy,.045),concrete,3.048,(.78,.77,.70))
    from ground_edges import edges
    paths=[[(L/2,-2.55,.005),(L/2+5.4,-2.55,.005)],[(L/2+5.4,.40,.005),(L/2,.40,.005)],[(x0,wy-.44,.005),(x1,wy-.44,.005)]]
    if spec['corner_apron']:paths=[[(-L/2-.3,-8.30,.002),(L/2+5.4,-8.30,.002)],[(-L/2-.3,-W/2-.10,.002),(L/2,-W/2-.10,.002)]]
    edges(a.root,paths,seed+314,lib)
    from terrain import pavement
    pavement(a,spec,lib,library_material)
    from site_age import pad as age_pad
    age_pad(a,spec,lib,library_material)
    from site_age import soil
    soil(a,spec,lib,library_material,record)
    from traffic import selection
    for marker in a.root.children_recursive:
        if marker.get('socket_kind')!='car':continue
        model,color=selection(p['seed'],record['number'],int('Carport' in marker.name),round(p['span']/p['lot_frontage']))
        if spec['corner_apron']:model=2
        marker['vehicle_index']=model;marker['factory_color']=color;marker['occupant_seed']=seed
    # Sparse pad dressing is geometry now; oil and causal weather remain look-dev.
    place(a.root,record['origin'],record['yaw'],parent);a.root['lot_record']=json.dumps(record,sort_keys=True)
    return a


def common(p,lib,parent):
    old=p['kind']=='old';span=p['span'];a=Assembly('CommonFacilities');a.root.parent=parent
    base=-span/2-5;first=-span/2+p['lot_frontage']/2
    # Buildings use the same construction grammar, converted into an office /
    # laundry program by signs and independent entrances; no new house system.
    from plans import home
    spec=home(p['seed']+71,'1972' if old else '1996',width_ft=12 if old else 24,length_ft=52)
    office=make_home(spec,'Office' if old else 'Clubhouse');place(office.root,(0 if old else -14,base+2 if old else first+1.15,0),0,a.root)
    label(office,'OFFICE' if old else 'CLUBHOUSE',(0,-spec['width']/2-.06,2.49),.19,spec['accent'])
    # Newer clubhouse occupies the loop's center; an independently placed
    # laundry at the north end leaves the central common lawn open.
    ls=home(p['seed']+81,'1984',width_ft=14,length_ft=52);ls['carport']=False
    laund=make_home(ls,'Laundry');place(laund.root,(0 if old else -14,span/2+3 if old else span/2-p['lot_frontage']/2,0),180 if old else 0,a.root)
    label(laund,'LAUNDRY',(0,-ls['width']/2-.04,2.55),.21,ls['accent'])
    sg=A.sign('EntranceSign',p['name'].upper());place(sg.root,(-p['loop_x']+6 if old else 8,base-2,0),0,a.root)
    for j in range(5):a.socket('EntrancePlant_'+str(j),(-p['loop_x']+4+j*1.2 if old else 8+j,base-1.3,0),'shrub')
    m=a.mesh('ClusterMail',component='cluster_mail')
    mx,my=(14,base+3) if old else (-24,first-4)
    m.box((mx,my,.04),(3.5,2.0,.08),'Concrete')
    for dx in (-.5,.5):m.box((mx+dx,my,.65),(.10,.10,1.2),'Trim',(.24,.25,.22))
    m.box((mx,my,1.26),(1.62,.44,.78),'Trim',(.29,.30,.26),r=.012)
    for row in range(3):
        for col in range(4):
            xx=mx+(col-1.5)*.39;zz=1.02+row*.235
            m.box((xx,my-.235,zz),(.372,.020,.215),'Trim',(.48,.48,.41),r=.003)
            m.box((xx+.13,my-.25,zz-.05),(.024,.008,.018),'Trim',(.08,.09,.07))
    m.finish();a.socket('MailUser',(mx,my-1,0),'occupant')
    # Dumpster and service enclosure, with open gates supplied by native fence.
    dx,dy=(24,base+1) if old else (-22,span/2-2)
    m=a.mesh('Dumpster',component='dumpster')
    m.box((dx,dy,.73),(2.12,1.62,1.35),'Trim',(.045,.12,.095),r=.025)
    m.box((dx,dy,1.44),(2.2,1.70,.10),'Trim',(.035,.04,.033),r=.009)
    for sx in (-1,1):m.box((dx+sx*1.10,dy,.90),(.13,.82,.16),'Trim',(.065,.10,.075))
    m.finish()
    for j in range(2):native(lib,'fences/export/WoodPrivacy.glb','DumpsterRear'+str(j),(dx+(j-.5)*2.4384,dy+1.3,0),0,'Section_A',a.root)
    for j in range(3):native(lib,'fences/export/WoodPrivacy.glb','DumpsterPostRear'+str(j),(dx+(j-1)*2.4384,dy+1.3,0),0,'Post_Line' if j==1 else 'Post_Corner',a.root)
    for sign in (-1,1):
        native(lib,'fences/export/WoodPrivacy.glb','DumpsterSide'+str(sign),(dx+sign*2.4384,dy+.0808,0),90,'Section_B',a.root)
        native(lib,'fences/export/WoodPrivacy.glb','DumpsterFrontPost'+str(sign),(dx+sign*2.4384,dy-1.1384,0),90,'Post_End',a.root)
    if not old:
        # Native dated playground pieces plus conservative 2H swing envelopes.
        native(lib,'trailer-park/build/native/playground.gltf','CommonPlayground',(13,first,0),0,parent=a.root)
        concrete=library_material(lib,'Concrete')
        ground_box(a.root,'Playground containment',(13,first,-.01),(18,12,.06),concrete,3.048,(.66,.53,.36))
        a.socket('PlayUseMin',(4,first-6,0),'play_use_zone');a.socket('PlayUseMax',(22,first+6,0),'play_use_zone')
        # Common routes, visitor parking and a planted gathering edge give the
        # loop's center a reason to exist rather than leaving an empty island.
        for x,y,w,d in ((0,first-7.2,56,1.22),(-14,span/2-9,28,1.22)):
            ground_box(a.root,'Common walk',(x,y,-.008),(w,d,.045),concrete,3.048,(.86,.85,.79))
        asphalt=library_material(lib,'Asphalt');ground_box(a.root,'Visitor parking',(-8,span/2-8,-.015),(12,5.6,.060),asphalt,6.096)
        pm=a.mesh('VisitorMarkings',component='parking')
        for j in range(5):pm.box((-13.5+j*2.743,span/2-8,.021),(.085,5.5,.006),'Trim',(.46,.45,.36))
        pm.finish()
        for j in (0,2,3):a.socket('VisitorCar_'+str(j),(-12.2+j*2.743,span/2-8,.015),'car',vehicle_index=j%3,paint_index=j+3)
        for j in range(3):a.socket('CommonTree_'+str(j),(4+j*8,first+6,0),'tree',species='maple',plant_scale=.64)
        for j in range(7):a.socket('CommonShrub_'+str(j),(-22+j*2.3,first+3+(j%2)*.55,0),'shrub')
    return a


def build(p):
    a=Assembly('Park_'+str(p['seed']));a.root['park_plan']=json.dumps(p,sort_keys=True);lib=Library()
    from kit import tiling
    turf=tiling.material('GardenLawn','textures/ship',tint=True);turf.name='ManufacturedSummerTurf';W,D=p['size']
    # Reuse the native blades and their physical UV scale. Stronger grazing
    # relief survives the wide exported view without an extra texture or mesh.
    for node in turf.node_tree.nodes:
        if node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=1.3
    from terrain import turf as summer_turf
    summer_turf(a.root,p,turf)
    road(a.root,p,lib);instances=Instances()
    for row in p['lots']:lot(p,row,lib,a.root,instances)
    common(p,lib,a.root)
    # Native poles carry supported luminaires; overhead conductors sag between
    # native neutral sockets. Newer lots reserve buried drops at pedestals.
    poles=[]
    rows=round(p['span']/p['lot_frontage']);boundaries=(0,round(rows/3),round(rows*2/3),rows)
    for j in range(4):
        y=-p['span']/2+boundaries[j]*p['lot_frontage']
        pole=native(lib,'trailer-park/build/native/utility.gltf','ParkPole_'+str(j),(-p['loop_x']+5.5,y,0),0,parent=a.root);poles.append(pole)
    bpy.context.view_layer.update();m=a.mesh('OverheadConductors',component='conductors')
    for left,right in zip(poles,poles[1:]):
        for suffix in ('Neutral','Service','CommDrop'):
            aa=next((o for o in left.children_recursive if o.name.split('.') [0].endswith('_'+suffix)),None)
            bb=next((o for o in right.children_recursive if o.name.split('.') [0].endswith('_'+suffix)),None)
            if aa and bb:
                p0,p1=aa.matrix_world.translation,bb.matrix_world.translation
                m.tube([p0.lerp(p1,t)-Vector((0,0,.45*4*t*(1-t))) for t in [k/18 for k in range(19)]],.006,'Trim',(.025,.03,.024),6)
    m.finish()
    rng=random.Random(p['seed']+740)
    for j,row in enumerate(p['lots']):
        if row.get('central'):continue
        xx,yy,*_=row['lot'];old=p['kind']=='old'
        # Mature crowns are staggered at rear/side yards; newer planted trees
        # are the same native species scaled once, with explicit age inference.
        if (old and j%3!=1) or (not old and j%2==0):
            tx=rng.uniform(-.7,.7)
            if old and row['yaw']==180:
                h=row['home'];u=-h['length']*.32+2.05 if h['room'] else -h['length']*.22
                # At the end row the rear-yard tree clears the room and
                # porch, rather than growing immediately through their roof.
                if j==len(p['lots'])-1:u=-h['length']*.74
                tx=row['origin'][0]-u+rng.uniform(-.05,.05)
            else:tx=row['origin'][0]+tx*(1 if row['yaw']==0 else -1)
            if old and j==5:tx=row['origin'][0]-4.0
            a.socket('Tree_'+str(j),(tx,yy+p['lot_frontage']/2-.4,0),'tree',species='oak' if j%3==0 else 'maple',plant_scale=rng.uniform(.92,1.12) if old else rng.uniform(.44,.64))
        if j%2==0:a.socket('Shrub_'+str(j),(row['origin'][0]+row['side']*4,yy-3,0),'shrub')
    for i,x in enumerate((-p['loop_x'],p['loop_x']) if p['kind']=='old' else (0,)):
        a.socket('TownEntry_'+str(i),(x,-D/2,.015),'street_connection',yaw=180)
        if p['kind']=='old':a.socket('TownExit_'+str(i),(x,D/2,.015),'street_connection')
    # Ship the crown variation with each planting socket so a game obtains
    # the same species/scale/rotation as the reviewed presentation.
    import hashlib
    for marker in a.root.children_recursive:
        if marker.get('socket_kind')!='tree':continue
        seed=int.from_bytes(hashlib.sha256((str(p['seed'])+marker.name).encode()).digest()[:4],'little')&0x7fffffff;tr=random.Random(seed)
        marker.rotation_euler.z=tr.uniform(0,math.tau);marker['plant_seed']=seed
        marker['plant_scale']*=tr.uniform(.88,1.12)
        marker['plant_aspect']=[tr.uniform(.85,1.12),tr.uniform(.85,1.12)]
    from sward import add as lawn_clumps
    lawn_clumps(a.root,p,lib)
    lib.clear();return a
