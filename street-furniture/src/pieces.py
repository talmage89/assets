"""Original period street furniture, built as manufactured assemblies."""
import math,random
import bpy
from mathutils import Vector
import forms as F
from forms import box,cyl,tube,profile,loft,bolt,foot,frame,quad,glass
from kit import model as G

def bench(rt,offset=(0,0,0),prefix='Bench'):
    x0,y0,z0=offset
    # Formed 1/4 x 1-1/2 inch solid straps at 1 inch clear spacing.
    path=[(-.295,.442),(-.28,.455),(-.20,.456),(-.07,.439),(.07,.433),(.16,.451),(.205,.493),(.231,.57),(.258,.67),(.286,.76),(.30,.805)]
    for j in range(28):
        x=x0+(j-13.5)*.0635;poly=[(y+y0,z+z0) for y,z in path]+[(y+y0,z+z0-.00635) for y,z in reversed(path)]
        profile(prefix+' formed steel strap',poly,x-.01905,x+.01905,rt)
    for s in (-1,1):
        x=x0+s*.87
        for y in (-.23,.23):
            # Bent solid-bar end units have a broad foot, actual slant and knee.
            profile(prefix+' end leg',[(y+y0-.025,z0+.012),(y+y0+.025,z0+.012),(y*.68+y0+.024,z0+.435),(y*.68+y0-.024,z0+.435)],x-.0127,x+.0127,rt)
            foot(prefix+' foot',x,y+y0,rt,z=z0)
        tube(prefix+' seat cross member',[(x,y+y0,z+z0-.02) for y,z in path],.01667,rt,s=8)
    for x in (x0-.91,x0,x0+.91):
        # Arm is a curved flat casting, not thin round wire.
        pts=[(y0-.20,z0+.45),(y0-.20,z0+.58),(y0-.14,z0+.64),(y0+.05,z0+.65),(y0+.20,z0+.62),(y0+.231,z0+.57)]
        tube(prefix+' arm support',[(x,y,z) for y,z in pts],.016,rt,s=8)
    cyl(prefix+' rear tie',(x0-.88,y0+.13,z0+.40),(x0+.88,y0+.13,z0+.40),.01667,rt,'Paint',12)

def rack(rt,count=1):
    for j in range(count):
        y=(j-(count-1)/2)*.9144;r=.12;half=.358;z=.9144-.03016
        path=[(-half,y,.012),(-half,y,z-r)]
        path += [(-half+r+r*math.cos(math.pi-i*math.pi/12),y,z-r+r*math.sin(math.pi-i*math.pi/12)) for i in range(1,7)]
        path += [(half-r,y,z)]
        path += [(half-r+r*math.cos(math.pi/2-i*math.pi/12),y,z-r+r*math.sin(math.pi/2-i*math.pi/12)) for i in range(1,7)]
        path += [(half,y,.012)]
        tube('2-3/8 inch galvanized pipe U',path,.03016,rt,'Zinc',s=16)
        for x in (-half,half):
            cyl('Surface flange',(x,y,0),(x,y,.0127),.0762,rt,'Zinc',24)
            cyl('Pipe welded collar',(x,y,.012),(x,y,.023),.034,rt,'Zinc',16)
            for k in range(4):
                t=k*math.pi/2+math.pi/4;bolt('Rack expansion bolt',(x+.055*math.cos(t),y+.055*math.sin(t),.0127),rt,.00635)
            sock=G.pivot('Rack_flange_anchor',(x,y,0));sock.parent=rt;sock['socket_kind']='Four M12 anchors on 110mm circle'

def stop(rt):
    cyl('Bus stop 2-3/8 inch post',(0,0,0),(0,0,3.05),.03016,rt,'Zinc',16)
    for key,z,w,h in [('transit',2.68,.4572,.6096),('routes',2.2479,.4572,.2286)]:
        box('Bus aluminum sign',(0,-.035,z),(w,.002032,h),rt,'White',.001)
        quad('Bus stop '+key,key,0,-.0361,z,w,h,rt)
        for zz in (z-h*.35,z+h*.35):bolt('Bus sign carriage bolt',(0,-.039,zz),rt,.006,(0,-1,0))
    frame('Schedule holder',0,-.054,1.52,.25,.44,rt,'Aluminum',.018,.05)
    box('Schedule backing',(0,-.03,1.52),(.25,.012,.44),rt,'Aluminum',0)
    quad('Timetable print','schedule',0,-.065,1.52,.214,.402,rt)
    glass('Schedule acrylic cover',(0,-.071,1.52),(.215,.002,.403),rt)
    for z in (1.38,1.67):
        cyl('Schedule strap around post',(0,0,z-.012),(0,0,z+.012),.034,rt,'Zinc',12)
        box('Schedule rear clamp',(0,-.02,z),(.04,.06,.025),rt,'Aluminum',0)

def shelter(rt,seed=11):
    rng=random.Random(seed);W,D=3.9624,1.524;H=2.30
    box('Shelter reinforced concrete slab',(0,0,.075),(4.2672,1.8288,.15),rt,'Concrete',.008)
    columns=[(-1.80,-.59),(1.80,-.59),(-1.80,.59),(-.60,.59),(.60,.59),(1.80,.59)]
    for x,y in columns:
        box('Extruded aluminum column',(x,y,.15+H/2),(.0635,.0635,H),rt,'Anodized',.002)
        box('Column bolted foot',(x,y,.16),(.16,.16,.02),rt,'Aluminum',.002)
        box('Column escutcheon',(x,y,.20),(.10,.10,.065),rt,'Anodized',.002)
        for sx in (-1,1):
            for sy in (-1,1):bolt('Shelter M12 hold-down',(x+sx*.058,y+sy*.058,.17),rt,.00635)
    # Narrower panes and a knee rail follow the in-use frame construction;
    # keeping panes replaceable explains each extrusion and gasket.
    for x in (-1.2,0,1.2):
        frame('Rear glazing frame',x,.59,1.31,1.14,1.91,rt,'Anodized',.028,.055)
        box('Rear intermediate glazing rail',(x,.59,1.08),(1.10,.055,.035),rt,'Anodized',.001)
        if not(seed==12 and x>.1):glass('Rear 3/8 inch safety glass',(x,.59,1.31),(1.084,.009525,1.854),rt)
        for z in (.39,2.22):box('Glazing channel gasket',(x,.561,z),(1.08,.008,.012),rt,'Rubber',0)
    for s in (-1,1):
        x=s*1.80;end=F.root('End glazing working frame');end.parent=rt;end.location=(x,0,0);end.rotation_euler.z=math.pi/2
        frame('End glazing frame',0,0,1.31,1.18,1.91,end,'Anodized',.028,.055)
        glass('End 3/8 inch safety glass',(0,0,1.31),(1.124,.009525,1.854),end)
        # End frame is construction, not a moving part. Rebase into module.
        for ob in list(end.children):ob.matrix_basis=end.matrix_basis@ob.matrix_basis;ob.parent=rt
        bpy.data.objects.remove(end,do_unlink=True)
    for y in (-.59,.59):box('Long roof perimeter extrusion',(0,y,2.47),(3.72,.09,.115),rt,'Anodized',.002)
    for x in (-1.80,-.90,0,.90,1.80):
        path=[(x,-.78+i*1.56/12,2.48+.24*math.sin(math.pi*i/12)) for i in range(13)]
        tube('Curved roof support rib',path,.022,rt,'Anodized',s=8)
    # Shallow original barrel canopy: a continuous 6mm sheet with closed rims.
    ys=[-.80+i*1.60/16 for i in range(17)]
    sec=[(y,2.49+.24*math.sin(math.pi*i/16)) for i,y in enumerate(ys)];poly=sec+[(y,z-.006) for y,z in reversed(sec)]
    profile('Bent aluminum canopy / real 6mm gauge',poly,-W/2,W/2,rt,'Aluminum')
    for y in (-.80,.80):box('Rain gutter / hem',(0,y,2.47),(W,.045,.05),rt,'Anodized',.002)
    # Original interchangeable double-sided poster in the right end's kiosk.
    ad=F.root('Ad kiosk local');ad.parent=rt;ad.location=(1.84,0,0);ad.rotation_euler.z=-math.pi/2
    box('Aluminum ad case',(0,0,1.34),(.96,.12,1.86),ad,'Anodized',.004)
    frame('Ad door gasket',0,-.068,1.34,.91,1.79,ad,'Rubber',.025,.025)
    quad('Swappable Rill River Park poster','advert',0,-.083,1.34,.85,1.72,ad)
    glass('Ad cover safety glazing',(0,-.085,1.34),(.86,.003,1.73),ad)
    for ob in list(ad.children):ob.matrix_basis=ad.matrix_basis@ob.matrix_basis;ob.parent=rt
    bpy.data.objects.remove(ad,do_unlink=True)
    bench(rt,(-.47,.22,.15),'Shelter bench')
    for x in (-.90,.90):
        box('Under-roof lighting case',(x,.12,2.48),(.64,.12,.055),rt,'Aluminum',.002)
        box('Lighting diffuser',(x,.12,2.45),(.58,.085,.007),rt,'Lamp',.001)
        sock=G.pivot('Shelter_LightSocket',(x,.12,2.44));sock.parent=rt;sock['socket_kind']='Downlight / 3000K / nominal 250 lumen'
    rt['seed']=seed;rt['panel_state']='rear right missing' if seed==12 else 'intact';rt['slab_top_m']=.15

def chain(rt,start,end,links=16):
    start,end=Vector(start),Vector(end)
    # Each open center link is swept wire; alternating planes, gentle slack.
    for j in range(links):
        t=(j+.5)/links;p=start.lerp(end,t);p.z-=.075*math.sin(math.pi*t)
        tangent=(end-start).normalized();u=tangent;v=Vector((0,1,0)) if j%2 else Vector((0,0,1));v=(v-u*v.dot(u)).normalized()
        points=[p+u*.019*math.cos(k*math.tau/8)+v*.010*math.sin(k*math.tau/8) for k in range(9)]
        tube('Welded security chain link',points,.0028,rt,'Zinc',s=4)

def newspaper(rt,kind=0,seed=None):
    w,d,H=((.48895,.434975,1.23825),(.46,.43,1.16),(.50,.45,1.28))[kind]
    seed=11+kind if seed is None else int(seed);edition=(seed-11)%3;finish=('Red','Blue','Cream')[edition]
    # Hollow brake-formed cabinet: 1.2mm shell, folded returns and real openings.
    low=.34;bodytop=.98 if kind!=2 else 1.02
    for x in (-w/2,w/2):
        if kind==2 and x>0:
            # A single cart-height impact deforms both sides of the real sheet,
            # fading before the welded folds. It is not a material noise dent.
            vs=[];fs=[];ny,nz=7,9
            for inner in (0,1):
                for j in range(nz):
                    zz=low+(bodytop-low)*j/(nz-1)
                    for k in range(ny):
                        yy=-d/2+d*k/(ny-1);dent=.012*math.exp(-((yy+.03)/.13)**2-((zz-.63)/.17)**2)*math.sin(math.pi*j/(nz-1))*math.sin(math.pi*k/(ny-1))
                        vs.append((x-inner*.0012-dent,yy,zz))
            N=ny*nz
            for inner in (0,1):
                for j in range(nz-1):
                    for k in range(ny-1):
                        v=inner*N+j*ny+k;f=(v,v+1,v+1+ny,v+ny);fs.append(f if inner==0 else tuple(reversed(f)))
            boundary=list(range(ny))+[j*ny+ny-1 for j in range(1,nz)]+[(nz-1)*ny+k for k in range(ny-2,-1,-1)]+[j*ny for j in range(nz-2,0,-1)]
            for u,v in zip(boundary,boundary[1:]+boundary[:1]):fs.append((u,u+N,v+N,v))
            F.own(G.smooth(G.mesh('Cart impact / 1.2mm cabinet side',vs,fs,F.M),45),rt,finish)
        else:box('News cabinet side wall',(x,0,(low+bodytop)/2),(.0012,d,bodytop-low),rt,finish,0)
    box('News back / returned seam',(0,d/2,(low+bodytop)/2),(w,.0012,bodytop-low),rt,finish,0)
    for z in (low,bodytop):box('News floor / roof skin',(0,0,z),(w,d,.0012),rt,finish,0)
    for y in (-d/2,d/2):box('News base hem',(0,y,low+.014),(w,.018,.028),rt,finish,0)
    if kind==1:
        box('Square pedestal',(0,.015,.18),(.16,.16,.32),rt,finish,.004);box('Pedestal plinth',(0,0,.018),(.40,.38,.036),rt,finish,.005)
        for x in (-.15,.15):
            for y in (-.14,.14):bolt('News plinth bolt',(x,y,.036),rt,.006)
    else:
        for x in (-w*.37,w*.37):
            for y in (-d*.34,d*.34):box('News welded foot',(x,y,.17),(.035,.035,.34),rt,finish,0)
        for x in (-w*.37,w*.37):box('News foot crossbar',(x,0,.015),(.055,d*.88,.03),rt,finish,.002)
    # Tall mechanical coin compartment on one side of the header.
    cx=w*.32;cw=.15
    box('Coin housing',(cx,-.005,(bodytop+H)/2),(cw,d*.83,H-bodytop),rt,finish,.009)
    coinlid=F.pivot('NewsCoinLid',(cx,d*.41,H-.006),rt,'X',(-105,0))
    box('Coin service cover',(0,-d*.41,.006),(cw+.006,d*.84,.012),coinlid,finish,.002)
    box('Coin slot bezel',(cx,-d*.425-.004,H-.075),(.095,.008,.055),rt,'Zinc',.004)
    box('Coin entry slot',(cx,-d*.425-.009,H-.075),(.029,.001,.003),rt,'Inside',0)
    bolt('Coin cabinet lock',(cx,-d*.425-.011,bodytop+.045),rt,.011,(0,-1,0))
    box('Coin return tray',(cx,-d*.425-.009,bodytop+.011),(.07,.027,.023),rt,'Zinc',.002)
    frame('News access opening',0,-d/2, (low+bodytop)/2,w,bodytop-low,rt,finish,.025,.022)
    hinge=F.pivot('NewsDoor',(0,-d/2-.014,low+.025),rt,'X',(0,75))
    dh=bodytop-low-.05;dw=w-.038
    frame('Returned newspaper door',0,0,dh/2,dw,dh,hinge,finish,.028,.020)
    glass('News door acrylic window',(0,.001,dh*.52),(dw-.056,.003,dh*.69),hinge)
    box('Door masthead panel',(0,0,dh-.062),(dw,.02,.124),hinge,finish,.001)
    quad('Fictional newspaper masthead','mast'+str(edition),0,-.011,dh-.064,dw-.018,.108,hinge)
    box('Door pull',(dw*.34,-.028,dh*.45),(.024,.035,.125),hinge,'Zinc',.006)
    cyl('Door pivot pin',(-dw/2,0,0),(dw/2,0,0),.005,hinge,'Zinc',10)
    for j in range(6):box('Folded paper in stack',(0,.015,low+.04+j*.005),(w-.10,d-.10,.004),rt,'Paper',0)
    quad('Display copy paper inside window','paper'+str(edition),-.025,-d/2+.032,(low+bodytop)/2,w-.12,(bodytop-low)*.71,rt)
    quad('Front low masthead','mast'+str(edition),-w*.16,-d/2-.002,low+.086,w*.55,.12,rt)
    cyl('Security anchor post',(w/2+.08,d/2+.095,0),(w/2+.08,d/2+.095,.69),.021,rt,'Zinc',8)
    chain(rt,(w/2-.01,d*.35,.55),(w/2+.08,d/2+.10,.59),8)

    if kind==2:
        tag=quad('Original F9 adhesive tag','tag',0,0,0,.16,.09,rt);tag.rotation_euler.z=math.pi/2;tag.location=(w/2+.001,-.03,.76)
    rt['seed']=seed;rt['paper_headline']=('RIVER WALK OPENS','LIBRARY ADDS HOURS','LOCAL FAIR RETURNS')[edition]

def collection(rt):
    w,d,H=.879475,.635,1.330325;floor=.385;shoulder=H-d/2
    for x in (-w*.39,w*.39):
        for y in (-d*.34,d*.34):
            # Exposed angle-stock legs, not isolated cylinders.
            profile('Collection box angle leg',[(x-.020,y-.020),(x+.020,y-.020),(x+.020,y-.014),(x-.014,y-.014),(x-.014,y+.020),(x-.020,y+.020)],.006,floor+.07,rt,'Blue','Z')
            foot('Collection leg foot',x,y,rt,.10,.085)
    sec=[(-d/2,floor),(-d/2,shoulder)]+[(d/2*math.cos(math.pi-i*math.pi/16),shoulder+d/2*math.sin(math.pi-i*math.pi/16)) for i in range(1,17)]+[(d/2,floor)]
    for s in (-1,1):profile('Pressed rounded collection side',sec,s*w/2-.00095,s*w/2+.00095,rt,'Blue')
    path=[(d/2*math.cos(math.pi-i*math.pi/20),shoulder+d/2*math.sin(math.pi-i*math.pi/20)) for i in range(21)]
    roof=path+[(y*.994,z-.0019) for y,z in reversed(path)];G.smooth(profile('Rolled collection roof skin',roof,-w/2,w/2,rt,'Blue'),60)
    box('Collection back skin',(0,d/2,(floor+shoulder)/2),(w,.0019,shoulder-floor),rt,'Blue',0)
    box('Collection interior floor',(0,0,floor),(w,d,.0019),rt,'Blue',0)
    frame('Collection lower service opening',0,-d/2,(floor+.925)/2,w,.925-floor,rt,'Blue',.025,.026)
    door=F.pivot('CollectionServiceDoor',(-w/2+.025,-d/2-.004,floor+.025),rt,'Z',(-105,0))
    box('Returned service door',(w/2-.025,0,(.925-floor-.05)/2),(w-.05,.022,.925-floor-.05),door,'Blue',.005)
    quad('Generic town post envelope','mail',w/2-.025,-.0115,(.925-floor-.05)/2,w-.16,.33,door)
    bolt('Collection door lock',(w-.09,-.016,.15),door,.013,(0,-1,0))
    # Open mail throat behind a pull-down curved chute.
    box('Mail throat cavity',(0,-d/2+.055,.975),(w-.10,.10,.15),rt,'Inside',0)
    for s in (-1,1):box('Fixed chute shoulder',(s*w*.45,-d/2,.996),(w*.10,.0019,.15),rt,'Blue',0)
    chute=F.pivot('CollectionPullDownChute',(0,-d/2,.925),rt,'X',(0,50))
    profile('Pull-down formed chute',[(-.012,0),(-.021,.14),(.035,.20),(.065,.195),(.065,.187),(.045,.188),(-.012,.136),(-.006,.006)],-w*.40,w*.40,chute,'Blue')
    tube('Collection chute handle',[(-.12,-.025,.13),(-.12,-.062,.13),(.12,-.062,.13),(.12,-.025,.13)],.009,chute,'Zinc',s=8)
    quad('Collection schedule','collection',0,-.023,.065,.22,.09,chute)

def meter_head(rt,x,z,expired=False,name='Meter'):
    # Rounded die-cast compound housing: independent sections vary in both
    # width and depth. No extruded silhouette with a bevel pretending to be a casting.
    stations=[(0,.035,.039),(.012,.055,.052),(.04,.068,.058),(.10,.076,.064),(.17,.074,.069),(.215,.080,.075),(.27,.098,.080),(.34,.107,.080),(.39,.107,.079),(.43,.100,.074),(.455,.083,.062),(.473,.055,.044),(.480,.012,.016)]
    loops=[[(x+rx*math.cos(t*math.tau/32),ry*math.sin(t*math.tau/32),z+zz) for t in range(32)] for zz,rx,ry in stations]
    shell=G.loft(name+' die-cast support cage',loops,F.M,True)
    sub=shell.modifiers.new('Compound cast support cage','SUBSURF');sub.levels=2;G.apply(shell)
    window=[(-.084,-.052),(.084,-.052),(.084,-.022)]+[(.084*math.cos(i*math.pi/12),-.022+.084*math.sin(i*math.pi/12)) for i in range(1,13)]
    cutter=G.profile('Arched cast window seat',window,-.14,-.012,F.M,axis='Y');cutter.location=(x,0,z+.385);G.boolean(shell,cutter);G.apply(shell)
    cutter=G.profile('Straight-die vault mouth',G.rounded_rectangle(.116,.173,.0505,6),-.14,.03,F.M,axis='Y');cutter.location=(x,0,z+.10);G.boolean(shell,cutter);G.apply(shell)
    # Remeshing the smooth cage/cuts removes the pinched Boolean shoulder fans.
    bpy.ops.object.select_all(action='DESELECT');shell.select_set(True);bpy.context.view_layer.objects.active=shell
    shell.data.remesh_voxel_size=.0015;bpy.ops.object.voxel_remesh()
    sm=shell.modifiers.new('Cast fillet relaxation','SMOOTH');sm.factor=.72;sm.iterations=4;G.apply(shell)
    shell.data.calc_loop_triangles();source_count=len(shell.data.loop_triangles)
    if F.QUALITY=='game':
        dec=shell.modifiers.new('Budgeted cast skin','DECIMATE');dec.ratio=700/source_count;G.apply(shell)
    shell.name=name+' compound die-cast body';F.own(G.smooth(shell,180),rt,'Aluminum')
    shell['cast_source_triangles']=source_count;shell['construction']='Subdivision support cage, die openings, smooth voxel union; high projected to low'
    backing=profile(name+' instrument well',window,-.018,-.014,rt,'Inside','Y');backing.location=(x,0,z+.385)
    quad(name+' minutes dial','meter',x,-.021,z+.382,.170,.095,rt)
    if expired:quad(name+' expired flag','expired',x,-.024,z+.360,.145,.026,rt)
    else:
        o=box(name+' clock hand',(x+.013,-.026,z+.38),(.004,.003,.046),rt,'Red',.001);o.rotation_euler.y=-.5
    # Domed glazing has a rolled perimeter and compound crown; independent of
    # the housing and its retaining bezel. Two rings avoid a pointed fan.
    n=len(window);vertices=[]
    for scale,yy in ((1,-.078),(.45,-.091)):
        vertices += [(x+u*scale,yy,z+.385+v*scale) for u,v in window]
    faces=[]
    for j in range(1):
        for i in range(n):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    faces.append(tuple(range(n,2*n)))
    F.own(G.smooth(G.mesh(name+' separate domed lens',vertices,faces,F.GLASS),180),rt,'White')
    # A die-cast retaining bezel seats the real dome and covers the cut edge.
    # Its inner/outer lips are explicit; this is not a painted outline.
    loops=[]
    for scale,yy in ((1.065,-.073),(1.065,-.080),(1.0,-.080),(1.0,-.073)):
        loops.append([(x+u*scale,yy,z+.385+v*scale) for u,v in window])
    bezel=G.ring_loft(name+' window retaining bezel',loops,F.M)
    import bmesh
    bm=bmesh.new();bm.from_mesh(bezel.data);bm.faces.ensure_lookup_table();bmesh.ops.delete(bm,geom=list(bm.faces)[-n:],context='FACES');bm.to_mesh(bezel.data);bm.free()
    F.own(G.smooth(bezel,50),rt,'Zinc')
    # Coin-vault door is hinged at the housing's side, with a clearance seam.
    door=F.pivot(name+'CoinDoor',(x-.058,-.065,z+.025),rt,'Z',(-95,0))
    leaf=profile(name+' rounded coin vault door',G.rounded_rectangle(.111,.168,.048,5),-.008,.006,door,'Aluminum','Y');leaf.location=(.058,0,.075)
    box(name+' vault recess',(x,-.029,z+.10),(.10,.008,.16),rt,'Inside',.014,2)
    bolt(name+' vault lock',(.088,-.010,.083),door,.010,(0,-1,0))
    box(name+' coin bezel',(x+.027,-.083,z+.231),(.060,.017,.035),rt,'Zinc',.005)
    box(name+' coin slot',(x+.027,-.092,z+.231),(.028,.001,.003),rt,'Inside',0)
    cyl(name+' winding knob stem',(x-.03,-.08,z+.205),(x-.03,-.108,z+.205),.009,rt,'Zinc',10)
    box(name+' winding grip',(x-.03,-.12,z+.205),(.066,.018,.016),rt,'Zinc',.005)
    cyl(name+' post collar',(x,0,z-.06),(x,0,z+.018),.036,rt,'Aluminum',16)

def meter(rt,twin=False,seed=11):
    cyl('Meter pipe post',(0,0,0),(0,0,1.075),.03016,rt,'Zinc',16)
    cyl('Meter post base collar',(0,0,0),(0,0,.07),.041,rt,'Zinc',16)
    if twin:
        box('Twin die-cast yoke',(0,0,1.06),(.285,.065,.065),rt,'Aluminum',.015,2)
        for j,x in enumerate((-.137,.137)):meter_head(rt,x,1.075,expired=(seed+j)%2==0,name='Twin'+str(j))
    else:meter_head(rt,0,1.04,expired=seed%2==1)
    rt['seed']=seed;rt['flag_state']='expired' if seed%2 else 'paid'

def receptacle(rt,recycle=False):
    R=.332;z0=.10;z1=.85;n=32
    for j in range(n):
        t=j*math.tau/n;x,y=R*math.cos(t),R*math.sin(t)
        o=box('Vertical steel receptacle slat',(x,y,(z0+z1)/2),(.0381,.00635,z1-z0),rt,'Paint',0);o.rotation_euler.z=t-math.pi/2
    for z in (.14,.78,.84):
        F.own(G.lathe('Rolled welded retaining hoop',[(z-.016,R-.014),(z+.016,R-.014),(z+.016,R-.004),(z-.016,R-.004)],F.M,32,closed=True),rt,'Paint')
    F.own(G.lathe('Black polyethylene liner',[(.12,0),(.12,.29),(.80,.30),(.80,.294),(.126,.284),(.126,0)],F.M,32),rt,'Inside')
    lid=F.pivot('RecyclingLid' if recycle else 'LitterLid',(0,.31,.86),rt,'X',(-100,0))
    profilepts=[(.0,.337),(.014,.35),(.045,.345),(.076,.31),(.094,.24),(.100,.155),(.094,.15),(.090,.236),(.071,.304),(.040,.339),(.014,.344),(.006,.333)]
    # Ring lathe preserves the actual depositing hole and sheet thickness.
    ob=F.own(G.lathe('Spun steel lid / open center',[(z+.0,r) for z,r in profilepts],F.M,48,closed=True),lid,'Blue' if recycle else 'Black');ob.location=(0,-.31,0)
    for t in (math.pi/6,math.pi*5/6,math.pi*3/2):
        x,y=.29*math.cos(t),.29*math.sin(t);foot('Receptacle anchored foot',x,y,rt,.10,.085)
        box('Receptacle riser',(x,y,.06),(.025,.025,.10),rt,'Paint',0)
    # Small plaque is mechanically fixed to welded side tabs.
    box('Receptacle curved plaque backing',(0,-.342,.57),(.25,.010,.145),rt,'Blue' if recycle else 'Paint',.008)
    quad('Recycling / litter instruction','recycle' if recycle else 'litter',0,-.348,.57,.23,.125,rt)
    for x in (-.11,.11):bolt('Plaque rivet',(x,-.35,.57),rt,.003,(0,-1,0))
