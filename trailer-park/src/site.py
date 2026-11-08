"""Lot-by-lot community assembly on Ground's existing material vocabulary."""
import math,random,json
from pathlib import Path
import bpy
from mathutils import Vector
from geometry import Assembly,Library,native,place,label,ROOT
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
    radius=7.0
    ranges=[(0,0,w,span+42)] if old else [(-xx,0,w,span+18-2*radius),(xx,0,w,span+18-2*radius),(0,-span/2-9,2*xx-2*radius,w),(0,span/2+9,2*xx-2*radius,w),(0,-span/2-15,w,12)]
    for i,(x,y,sx,sy) in enumerate(ranges):ground_box(a.root,'Private asphalt '+str(i),(x,y,-.035),(sx,sy,.10),asphalt,6.096)
    if not old:
        top=span/2+9
        for cx,cy,start in ((xx-radius,-top+radius,270),(xx-radius,top-radius,0),(-xx+radius,top-radius,90),(-xx+radius,-top+radius,180)):
            vs=[]
            for i in range(13):
                t=math.radians(start+i*90/12)
                vs.extend([(cx+r*math.cos(t),cy+r*math.sin(t),.015) for r in (radius-w/2,radius+w/2)])
            fs=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(12)]
            mesh=bpy.data.meshes.new('Private circular return');mesh.from_pydata(vs,[],fs);mesh.materials.append(asphalt);mesh.update()
            ob=bpy.data.objects.new('Private circular return',mesh);bpy.context.collection.objects.link(ob);ob.parent=a.root;world_uv(ob,6.096)
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
    for x,y in ([(0,-span*.23),(0,span*.28)] if old else [(-xx,0),(xx,0)]):
        # 3.7 m wide, 0.3 m travel depth bolt-down rubber speed bump.
        sections=[(-.18,.016),(-.13,.055),(-.06,.088),(.06,.088),(.13,.055),(.18,.016)]
        for (y0,z0),(y1,z1) in zip(sections,sections[1:]):
            m.prism([(x-w*.43,y+y0,z0),(x+w*.43,y+y0,z0),(x+w*.43,y+y1,z1),(x-w*.43,y+y1,z1)],(0,0,-1),.018,'Trim',(.055,.05,.025))
        for j in range(9):m.box((x-w*.40+j*w*.1,y,.087),(w*.045,.27,.009),'Trim',(.52,.35,.025))
        m.box((x+w/2+.55,y-.8,1.02),(.06,.05,2.04),'Trim',(.25,.28,.26))
        m.box((x+w/2+.55,y-.82,1.85),(.47,.035,.60),'Trim',(.62,.57,.37),r=.007)
        label(a,'10',(x+w/2+.55,y-.843,1.86),.23,(.025,.03,.025))
        label(a,'SLOW',(x+w/2+.55,y-.843,1.69),.095,(.025,.03,.025))
    m.finish();return a


def lot(p,record,lib,parent):
    spec=record['home'];seed=spec['seed'];a=Assembly(f'Lot_{record["number"]:02}');L,W=spec['length'],spec['width']
    h=make_home(spec,f'Lot_{record["number"]:02}_Home');h.root.parent=a.root
    d=A.deck(a.root.name+'_Deck',spec['deck_width'],height=spec['floor']-.025,seed=seed)
    place(d.root,(-L*.035,-W/2-1.11,0),parent=a.root)
    back=A.deck(a.root.name+'_BackSteps',1.22,1.0,spec['floor']-.025,seed+1)
    place(back.root,(L*.26,W/2+.55,0),180,parent=a.root)
    if spec['carport']:
        cp=A.carport(a.root.name+'_Carport',sag=spec['awning_sag']);place(cp.root,(L/2-3.4,-W/2-1.82,0),parent=a.root)
    if spec['room']:place(A.room(a.root.name+'_AddedRoom').root,(-L*.32,-W/2-1.20,0),parent=a.root)
    if spec['propane']:place(A.propane(a.root.name+'_Propane').root,(L*.13,W/2+.55,0),parent=a.root)
    ac=A.conditioner(a.root.name+'_AC',spec['ac'])
    place(ac.root,(L*.12,W/2+.17,1.80) if spec['ac']=='window' else (-L*.13,W/2+.73,0),180 if spec['ac']=='window' else 0,parent=a.root)
    place(A.utility(a.root.name+'_Utility').root,(-L/2-1.0,W/2+.55,0),parent=a.root)
    connections=a.mesh('ServiceConnections',component='service_connections')
    for offset,radius,color in ((.10,.020,(.19,.21,.18)),(.36,.016,(.27,.29,.25)),(.85,.051,(.47,.46,.38))):
        x=-L/2-1+offset;y=W/2+.60
        connections.tube([(x,y,.08),(x+.10,y,.03),(x+.30,y-.05,-.08),(x+.75,W/2-.25,-.08),(x+.75,W/2-.25,.48)],radius,'Trim',color,8)
    connections.finish()
    if spec['dish']:place(A.dish(a.root.name+'_Dish').root,(L*.32,W/2+.10,1.42),180,parent=a.root)
    place(A.dressing(a.root.name+'_PotsToy',seed).root,(-L*.035,-W/2-2.75,0),parent=a.root)
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
        ('trailer-park/build/native/shed.gltf','Shed',(-L/2+1.7,W/2+1.60,0),90,None),
        ('trash-cart/export/TrashCart.glb','Cart',(L/2+.8,-W/2-.5,.015),90,None),
        ('mailbox/export/Mailbox.glb','Mailbox',(L/2+3.2,1.7,.015),-90,None),
        ('patio-set/export/PatioSet.glb','LawnChair',(-L*.035+.75,-W/2-1.05,spec['floor']-.025),0,'Chair'),
    ]:
        if name=='Shed' and seed%3==0:continue
        rt=native(lib,path,a.root.name+'_'+name,pos,yaw,select,parent=a.root)
    if seed%3==1:native(lib,'gas-grill/export/GasGrill.glb',a.root.name+'_Grill',(-L*.035+2.9,-W/2-1.8,0),180,parent=a.root)
    # Short property edge: native 4 ft chain-link with a working native gate.
    if seed%3==0:
        path='fences/chain-link/export/ChainLink.glb'
        for j in range(2):native(lib,path,a.root.name+'_Fence'+str(j),(-L/2+.5+j*3.048,-W/2-3.55,0),0,'Chain_Section',a.root)
        for j in range(3):native(lib,path,a.root.name+'_Post'+str(j),(-L/2-1.024+j*3.048,-W/2-3.55,0),0,'Chain_Terminal' if j in (0,2) else 'Chain_Line',a.root)
        native(lib,path,a.root.name+'_Gate',(-L/2+5.60,-W/2-3.55,0),0,'Chain_GateBay',a.root)
    a.socket('Car',(L/2+3.1,-1.1,.015),'car',yaw=90,vehicle_index=2 if p['kind']=='old' and record['number']==1 else seed%3,paint_index=seed%5)
    a.socket('CarportCar',(L/2-3.2,-W/2-1.8,.015),'car',yaw=90,vehicle_index=(seed+1)%3,paint_index=(seed+2)%5)
    a.socket('Mailbox',(L/2+3.2,1.7,0),'mailbox')
    # Real paving between uncurbed private lane and the home end.
    concrete=library_material(lib,'Concrete');gravel=seed%3==0
    mat=concrete if not gravel else library_material(lib,'Asphalt')
    ground_box(a.root,'Lot drive apron',(L/2+3.0,-.6,-.015),(6.0,5.6,.06),mat,3.048 if not gravel else 1.5,(.80,.77,.67) if gravel else (.90,.89,.84))
    if spec['carport']:ground_box(a.root,'Carport pad',(L/2-3.4,-W/2-1.82,-.015),(6.9,3.55,.06),concrete,3.048,(.86,.85,.79))
    # A narrow resident-made walk connects the parking approach to the stairs.
    x0=-L*.035-spec['deck_width']/2+.475;x1=L/2+1.2;wy=-W/2-3.0
    ground_box(a.root,'Resident walk',((x0+x1)/2,wy,-.008),(x1-x0,.80,.045),concrete,3.048,(.78,.77,.70))
    ground_box(a.root,'Resident walk return',(x1,(wy-2.7)/2,-.008),(.80,-2.7-wy,.045),concrete,3.048,(.78,.77,.70))
    from ground_edges import edges
    edges(a.root,[[(L/2,-3.4,.005),(L/2+6.0,-3.4,.005)],[(L/2+6.0,2.2,.005),(L/2,2.2,.005)],
                  [(x0,wy-.44,.005),(x1,wy-.44,.005)]],seed+314,lib)
    # Sparse pad dressing is geometry now; oil and causal weather remain look-dev.
    place(a.root,record['origin'],record['yaw'],parent);a.root['lot_record']=json.dumps(record,sort_keys=True)
    return a


def common(p,lib,parent):
    old=p['kind']=='old';span=p['span'];a=Assembly('CommonFacilities');a.root.parent=parent
    base=-span/2-13
    # Buildings use the same construction grammar, converted into an office /
    # laundry program by signs and independent entrances; no new house system.
    from plans import home
    spec=home(p['seed']+71,'1972' if old else '1996',width_ft=12 if old else 24,length_ft=52)
    office=make_home(spec,'Office' if old else 'Clubhouse');place(office.root,(-17 if old else 0,base+3 if old else -19,0),0,a.root)
    label(office,'OFFICE' if old else 'CLUBHOUSE',(0,-spec['width']/2-.06,2.49),.19,spec['accent'])
    d=A.deck('OfficeDeck',3.048);place(d.root,(-spec['length']*.035,-spec['width']/2-1.11,0),parent=office.root)
    # Newer clubhouse occupies the loop's center; an independently placed
    # laundry at the north end leaves the central common lawn open.
    ls=home(p['seed']+81,'1984',width_ft=14,length_ft=52);ls['carport']=False
    laund=make_home(ls,'Laundry');place(laund.root,(18 if old else 0,span/2+11 if old else span/2-12,0),0,a.root)
    label(laund,'LAUNDRY',(0,-ls['width']/2-.04,2.55),.21,ls['accent'])
    ld=A.deck('LaundrySteps',3.048);place(ld.root,(-ls['length']*.035,-ls['width']/2-1.11,0),parent=laund.root)
    sg=A.sign('EntranceSign',p['name'].upper());place(sg.root,(7 if old else 8,base-3,0),0,a.root)
    for j in range(5):a.socket('EntrancePlant_'+str(j),(5+j*1.2,base-2.3,0),'shrub')
    m=a.mesh('ClusterMail',component='cluster_mail')
    mx,my=(14,base+3) if old else (6,-7)
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
    dx,dy=(27,base+1) if old else (8,span/2+4)
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
        native(lib,'trailer-park/build/native/playground.gltf','CommonPlayground',(-4,9,0),0,parent=a.root)
        concrete=library_material(lib,'Concrete')
        ground_box(a.root,'Playground containment',(-2,9,-.01),(18,12,.06),concrete,3.048,(.66,.53,.36))
        a.socket('PlayUseMin',(-11,3,0),'play_use_zone');a.socket('PlayUseMax',(7,15,0),'play_use_zone')
        # Common routes, visitor parking and a planted gathering edge give the
        # loop's center a reason to exist rather than leaving an empty island.
        for x,y,w,d in ((-7,-26.8,15.7,1.22),(-7,16,15.7,1.22),(-11.5,7,1.22,35)):
            ground_box(a.root,'Common walk',(x,y,-.008),(w,d,.045),concrete,3.048,(.86,.85,.79))
        asphalt=library_material(lib,'Asphalt');ground_box(a.root,'Visitor parking',(8,-35,-.015),(13.5,12.2,.060),asphalt,6.096)
        pm=a.mesh('VisitorMarkings',component='parking')
        for j in range(5):pm.box((6.5,-40.5+j*2.743,.021),(5.5,.085,.006),'Trim',(.46,.45,.36))
        pm.finish()
        for j in (0,2,3):a.socket('VisitorCar_'+str(j),(6.2,-39.15+j*2.743,.015),'car',yaw=90,vehicle_index=j%3,paint_index=j+3)
        for j,(x,y) in enumerate([(-11,-8),(-9,17),(11,20),(-3,22),(7,-13)]):a.socket('CommonTree_'+str(j),(x,y,0),'tree',species='maple',plant_scale=.64)
        for j in range(7):a.socket('CommonShrub_'+str(j),(-8+j*2.3,18.5+(j%2)*.55,0),'shrub')
    return a


def build(p):
    a=Assembly('Park_'+str(p['seed']));a.root['park_plan']=json.dumps(p,sort_keys=True);lib=Library()
    turf=library_material(lib,'Lawn');W,D=p['size']
    ground_box(a.root,'Community ground',(0,0,-.07),(W,D,.14),turf,3.048,(.87,.86,.74))
    road(a.root,p,lib)
    for row in p['lots']:lot(p,row,lib,a.root)
    common(p,lib,a.root)
    # Native poles carry supported luminaires; overhead conductors sag between
    # native neutral sockets. Newer lots reserve buried drops at pedestals.
    poles=[]
    rows=len([r for r in p['lots'] if r['side']==-1]);boundaries=(0,round(rows/3),round(rows*2/3),rows)
    for j in range(4):
        y=-p['span']/2+boundaries[j]*p['lot_frontage']
        pole=native(lib,'trailer-park/build/native/utility.gltf','ParkPole_'+str(j),(5.5 if p['kind']=='old' else -p['loop_x']-4.7,y,0),0,parent=a.root);poles.append(pole)
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
        a.socket('Tree_'+str(j),(xx+row['side']*8+rng.uniform(-1.2,1.2),yy+rng.uniform(1.4,4.2),0),'tree',species='oak' if j%3==0 else 'maple',plant_scale=rng.uniform(.92,1.12) if old else rng.uniform(.44,.64))
        if j%2==0:a.socket('Shrub_'+str(j),(row['origin'][0]+row['side']*4,yy-3,0),'shrub')
    a.socket('TownEntry',(0,-D/2,.015),'street_connection',yaw=180)
    if p['kind']=='old':a.socket('TownExit',(0,D/2,.015),'street_connection')
    lib.clear();return a
