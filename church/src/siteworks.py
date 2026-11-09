"""Two different town parcels; native streets, plants, cars and shared paving."""
import math,random
import geometry as G
from library import instance,car,clear
from hardware import sign


def slab(name,rect,z,role,parent,thick=.12):
    a,b,c,d=rect;thick=max(thick,z+.10);m=G.Mesh(name,parent,actor_kind='site',mulch='mulch' in name.lower());m.box(((a+b)/2,(c+d)/2,z-thick/2),(b-a,d-c,thick),role);return m.finish()


def paving(p,parent):
    import turf
    turf.MODERN=p['style']=='aframe'
    modern=p['style']=='aframe';cuts=[]
    def pad(name,rect,z=0,role='concrete'):
        cuts.append(rect);return slab(name,rect,z,role,parent)
    lot=(12,70,-36,-18) if modern else (-18,13,23,44)
    pad('Sealed parking lot',lot,.005,'asphalt')
    if modern:
        pad('Arterial driveway connection',(10.6908,13.7388,-39.38,-33),.005,'asphalt')
        pad('Canopy drop-off lane',(14,45,-18,-11),.005,'asphalt')
        pad('East lot connection',(40,50,-27,-11),.005,'asphalt')
        pad('Drop-off exit throat',(14,24,-27,-17),.005,'asphalt')
        pad('Canopy walk',(14,26.30,-12.2,-7.0),.1524)
        pad('Classroom arrival walk',(26.30,36,-12.2,-10.36),.1524)
        pad('Church entry plaza',(-4.2,10,-22,-14.5),.1524)
        pad('Street to entrance walk',(-1.0,1.0,-40,-22),0)
        m=G.Mesh('Accessible plaza approach',parent,actor_kind='site')
        m.prism([(-1,-23.9812,0),(1,-23.9812,0),(1,-22,.1524),(-1,-22,.1524)],(0,0,-.10),'concrete');m.finish()
        pad('Memorial garden walk',(9.0,25.8,-6.8,-4.5),0)
        pad('Memorial garden crosswalk',(13.2,15.1,-4.5,10.2),0)
        pad('Education route',(23.8,25.8,-7.0,16.5),.1524)
        pad('Accessible lot approach',(27.3,29.1,-23.65,-18),.009)
        from surfaces import paint_material
        paint_material();m=G.Mesh('Accessible canopy curb ramp',parent,actor_kind='site')
        m.prism([(27.3,-14.2,.005),(29.1,-14.2,.005),(29.1,-12.2,.1524),(27.3,-12.2,.1524)],(0,0,-.10),'concrete');m.finish()
        m=G.Mesh('Drop-off pedestrian crossing',parent,actor_kind='site',sheet=True)
        for j in range(6):
            yy=-18+j*.6;m.geom([(27.3,yy,.012),(29.1,yy,.012),(29.1,yy+.30,.012),(27.3,yy+.30,.012)],[(0,1,2,3)],'paint',uv=[[(.005,.755),(.12,.755),(.12,.995),(.005,.995)]])
        m.finish()
        p['dropoff_curve']=[(46.5,-29,.005),(46.5,-21,.005),(45,-16.5,.005),(40.5,-14.5,.005),(23,-14.5,.005),(18.5,-16,.005),(16.5,-20.5,.005),(18,-29,.005)]
    else:
        pad('Front approach',(-2.16,2.16,-23,-16.4),0)
        pad('Rear lot drive',(-21.3132,-15.2172,-22,44),.005,'asphalt')
        pad('Corner apron return',(-19.7892,-16.7412,-23.38,-22),.005)
        pad('Rear pedestrian way',(-14.4,17.7,19.1,21.2),0)
        pad('Accessible rear lot approach',(5.55,7.35,21.2,23),0)
        pad('Rear exit to lot walk',(-1.6,1.6,p['length']/2+1.8+4*.3302,19.1),0)
        pad('Parish hall door landing',(p['width']/2+3.3,p['width']/2+6.7,0,1.12),.1524)
        pad('Ramp to rear route',(17.7,19.7,0,21.2),0)
        pad('Ramp lower landing return',(p['width']/2+3.43,19.7,-1.8288,0),0)
        p['dropoff_curve']=[]
    p['paths']=[dict(name='Street_to_front',points=[(0,-40 if modern else -23,0),(0,-22 if modern else -17,0),(0,-p['length']/2-.40,p['floor'])]),dict(name='Lot_to_door',points=[(28.216,-20.9,.009),(28.216,-18,.009),(28.216,-14.2,.005),(28.216,-12.2,.1524),(30.6392,-12.2,.1524),(30.6392,-10.75,.1524)] if modern else [(6.4456,25.9,.005),(6.4456,20.1,0),(18.7,20.1,0),(18.7,-.9144,0),(9.1532,-.9144,0),(9.1532,-1.8288,0),(9.1532,-9.7536,.6096),(9.1532,-10.668,.6096),(6.9,-10.668,.6096)])]
    # Rectangular turf clipping includes construction footprints, so lawns
    # meet paving and foundations without grass polygons through the lot.
    w=p['width'];l=p['length'];cuts.append((-w/2,w/2,-l/2,l/2))
    if modern:cuts += [(w/2,w/2+21,l/2+1.9,l/2+14.1),(w/2+17.535,w/2+26.065,-10.2,16.8)]
    else:cuts.append((w/2,w/2+10,l/2-11.315,l/2+3.315))
    cuts+=turf.beds(p)
    if modern:
        islands=[(12,15.3,-36,-24),(32.3,35.1,-36,-31.0),(51.5,54.3,-36,-31.0),(67.6,70,-36,-18)]
        for r in islands:
            slab('Landscape island curb',r,.13,'concrete',parent)
            inner=(r[0]+.12,r[1]-.12,r[2]+.12,r[3]-.12)
            slab('Island mulch',inner,.14,'timber',parent,.04)
        cuts+=islands
    bounds=(-22.2,73,-39.4,47) if modern else (-22.2,30,-23.4,47)
    xs=sorted({bounds[0],bounds[1],*[max(bounds[0],min(bounds[1],q)) for r in cuts for q in r[:2]],*[x for x in range(math.ceil(bounds[0]),math.floor(bounds[1]),2)]})
    ys=sorted({bounds[2],bounds[3],*[max(bounds[2],min(bounds[3],q)) for r in cuts for q in r[2:]],*[y for y in range(math.ceil(bounds[2]),math.floor(bounds[3]),2)]})
    m=G.Mesh('Parcel turf',parent,actor_kind='site')
    for a,b in zip(xs,xs[1:]):
        for c,d in zip(ys,ys[1:]):
            x=(a+b)/2;y=(c+d)/2
            if any(r[0]<x<r[1] and r[2]<y<r[3] for r in cuts):continue
            m.geom([(a,c,-.008),(b,c,-.008),(b,d,-.008),(a,d,-.008)],[(0,1,2,3)],'lawn')
    m.finish();turf.details(p,parent,cuts,bounds);return lot


def parking(p,parent,rect):
    from surfaces import paint_material
    paint_material();a,b,c,d=rect;modern=p['style']=='aframe';n=20 if modern else 10;start=a+2.5;pitch=2.7432
    m=G.Mesh('Parking stripes wheel stops and drains',parent,actor_kind='site');rng=random.Random(p['seed']+62)
    for row,y in enumerate((c+2.9,d-2.9)):
        for j in range(n):
            x=start+j*pitch
            if x+pitch/2>b-.7:continue
            if modern and (j==19 or (row==0 and j in (7,14))):continue
            if modern and row==1 and (x<24 or 40<x<50 or j==5):continue
            if not modern and row==0 and j==8:continue
            # Keep one generous access aisle at the pedestrian-route end.
            if j==0:
                continue
            for xx in (x-pitch/2,x+pitch/2):
                pts=[(xx-.045,y-2.72,.012),(xx+.045,y-2.72,.012),(xx+.045,y+2.72,.012),(xx-.045,y+2.72,.012)]
                m.geom(pts,[(0,1,2,3)],'paint',color=(.57,.55,.45),uv=[[(.005,.755),(.12,.755),(.12,.995),(.005,.995)]])
            yy=y+(2.1 if row else -2.1);m.box((x,yy,.075),(1.70,.17,.15),'concrete')
            occupied=((row,j) in ((0,3),(0,5),(0,10),(0,16),(1,4),(1,11),(1,17))) if modern else rng.random()<p['occupancy']
            accessible=(modern and row==1 and j==4) or (not modern and row==0 and j==9)
            stall=G.root(f'Stall_{row}_{j}',(x,y,.01),parent,socket_kind='parked_car',stall_width=pitch,stall_depth=5.4864,occupied=occupied,accessible=accessible)
            p['stalls'].append(dict(name=stall.name,center=[x,y,.01],yaw=180 if row else 0,occupied=occupied,accessible=accessible))
            if occupied:car(row*20+j,(x+rng.uniform(-.12,.12),y+rng.uniform(-.16,.16),.012),180 if row else 0)
            # Repeated cause, irregular occurrence: drips below engine/gearbox,
            # concentrated toward the stall head, never a road-wide noise wash.
            oy=y+(1.1 if row else -1.1)+rng.uniform(-.35,.35);ox=x+rng.uniform(-.22,.22)
            rx=rng.uniform(.18,.47);ry=rng.uniform(.30,.72)
            m.geom([(ox-rx,oy-ry,.014),(ox+rx,oy-ry,.014),(ox+rx,oy+ry,.014),(ox-rx,oy+ry,.014)],[(0,1,2,3)],'paint',color=(.65,.61,.54),uv=[[(.505,.505),(.745,.505),(.745,.745),(.505,.745)]])
    m.finish()


def settlement(parent,rect,seed):
    rng=random.Random(seed+207);a,b,c,d=rect;m=G.Mesh('Lot settlement cracks',parent,actor_kind='site',sheet=True)
    for i in range(9):
        x=rng.uniform(a+1,b-1);y=rng.uniform(c+1,d-2);w=rng.uniform(.08,.18);length=rng.uniform(1.4,3.5)
        m.geom([(x-w,y,.013),(x+w,y,.013),(x+w,y+length,.013),(x-w,y+length,.013)],[(0,1,2,3)],'paint',uv=[[(.502,.005),(.623,.005),(.623,.245),(.502,.245)]])
    m.finish()


def streets(parent,modern):
    path=G.ROOT/'ground/export/Ground.glb';z=-.16764
    # Ground's junction and exact crown/curb/walk mating grid are retained.
    cx=-30;cy=-47 if modern else -31
    instance(path,'Corner intersection',(cx,cy,z),kind='Road_Intersection',actor='site')
    for k in range(4):
        a=k*math.pi/2;c,s=math.cos(a),math.sin(a)
        pt=(cx+(c-s)*8.6868,cy+(s+c)*8.6868,z)
        for kind in ('Curb_Corner','Sidewalk_Corner','Lawn_CornerStrip'):
            instance(path,kind+'_'+str(k),pt,k*90,kind=kind,actor='site')
    for arm,count in ((0,17),(1,11),(2,10),(3,10)):
        a=arm*math.pi/2;c,s=math.cos(a),math.sin(a)
        def xy(x,y):return (cx+c*x-s*y,cy+s*x+c*y,z)
        for i in range(count):
            station=8.6868+(i+.5)*6.096
            instance(path,'Town road '+str(arm)+'_'+str(i),xy(0,station),arm*90,kind='Road_Straight_B' if i==5 else 'Road_Straight_A',actor='site')
            for side in (-1,1):
                yaw=arm*90+(180 if side<0 else 0)
                for j in range(2):
                    yy=8.6868+i*6.096+(j+.5)*3.048
                    # A driveway aperture spans both curb modules.
                    drive=arm==3 and side==-1 and i==(5 if modern else 0)
                    if drive:
                        if j:continue
                        yy=station
                    kind='Curb_DrivewayCut' if drive else 'Curb_Straight'
                    instance(path,'Town curb',xy(side*4.1148,yy),yaw,kind=kind,actor='site')
                    if drive:instance(path,'Drive apron',xy(side*4.2672,yy),yaw,kind='Driveway_Apron',actor='site')
                    else:instance(path,'Verge sod with dense edges',xy(side*4.2672,yy),yaw,kind='Lawn_Strip',actor='site')
                for j in range(4):
                    yy=8.6868+i*6.096+(j+.5)*1.524
                    instance(path,'Jointed public sidewalk',xy(side*6.096,yy),yaw,kind='Sidewalk_A',actor='site')
    return cx,cy


def town(p,parent):
    modern=p['style']=='aframe';cx,cy=streets(parent,modern)
    from neighborhood import build
    build(p)
    # Native foliage, at varied orientations and credible setbacks. Shrub roots
    # are selected from the single delivered two-species library.
    plants=[(-18,-17),(20,-17),(-20,17),(23,39),(49,26),(58,-4),(33.7,-33),(52.9,-33)] if modern else [(-18,-25),(21,-25),(-25,8),(26,35),(-42,46),(43,48)]
    for i,(x,y) in enumerate(plants):
        instance(G.ROOT/('trees/export/PinOak.glb' if i%3==0 else 'trees/export/RedMaple.glb'),'Established street tree '+str(i),(x,y,0),i*53,.70 if modern else .61,actor='vegetation')
    for i in range(12 if modern else 7):
        point=(36.2,-7+i*1.65,0) if modern else (17.1,4+i*1.65,0)
        instance(G.ROOT/'shrubs/export/Shrubs.glb','Foundation shrub '+str(i),point,i*37,.75 if not modern else .87,kind='Hydrangea' if i%4==0 else 'Boxwood',actor='vegetation')
    for i,(x,y) in enumerate(((-22,-40),(14,-27),(69,-24)) if modern else ((-25,-22),(22,-25),(-25,20))):
        instance(G.ROOT/'street-light/export/StreetLight.glb','Street light '+str(i),(x,y,0),0,actor='site')
    instance(G.ROOT/'street-signs/export/StreetSigns.glb','Corner street names',(cx+5,cy+6,0),actor='site')
    if not modern:
        for i,(x,y,yaw) in enumerate(((-12,-28,90),(-4,-28,90),(8,-28,90),(20,-28,90),(33,-28,90),(45,-28,90),(-27,-8,0),(-27,4,0),(-27,16,0),(-27,28,0))):car(80+i,(x,y,-.13),yaw)
    # A distant district plane closes the horizon below all authored surfaces.
    slab('Distant town ground',(-600,600,-600,600),-.18,'lawn',parent,.02)
    from turf import imported_lawns
    __import__('bpy').context.view_layer.update();imported_lawns()


def site(p,church):
    rt=G.root('ChurchSite_'+str(p['seed']),seed=p['seed']);church.parent=rt;church.location=p['placement_offset']
    lot=paving(p,rt);parking(p,rt,lot);settlement(rt,lot,p['seed']);town(p,rt)
    marquee=sign(rt,(7,-37.5,0) if p['style']=='aframe' else (17,-22,0),p['name'],['CEDAR & BELL' if p['style']=='aframe' else 'GRACE CORNER','WORSHIP 10:30','ALL WELCOME']);marquee['actor_kind']='site'
    # Accessible walk paths and drive curves ship as empty-node point lists.
    for row in p['paths']:G.root(row['name'],parent=rt,socket_kind='walk_path',points=row['points'])
    if p['dropoff_curve']:G.root('Dropoff route',parent=rt,socket_kind='drive_curve',points=p['dropoff_curve'],interpolation='CATMULL_ROM',lane_width_m=7.0)
    for ob in list(__import__('bpy').context.scene.objects):
        if ob!=rt and ob.parent is None and not ob.name.startswith('Template_'):ob.parent=rt
    clear();return rt
