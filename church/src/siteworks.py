"""Two different town parcels; native streets, plants, cars and shared paving."""
import math,random
import geometry as G
from library import instance,car,clear
from hardware import sign


def slab(name,rect,z,role,parent,thick=.12):
    a,b,c,d=rect;m=G.Mesh(name,parent,actor_kind='site');m.box(((a+b)/2,(c+d)/2,z-thick/2),(b-a,d-c,thick),role);return m.finish()


def paving(p,parent):
    modern=p['style']=='aframe';cuts=[]
    def pad(name,rect,z=0,role='concrete'):
        cuts.append(rect);return slab(name,rect,z,role,parent)
    lot=(12,57,-43,-22) if modern else (-18,13,23,44)
    pad('Sealed parking lot',lot,.005,'asphalt')
    if modern:
        pad('Canopy drop-off lane',(8.8,40,-18,-11),.005,'asphalt')
        pad('East lot connection',(40,47,-23,-11),.005,'asphalt')
        pad('Canopy walk',(7.5,36,-11,-7.0),.1524)
        pad('Church entry plaza',(-4.2,10,-22,-14.5),.1524)
        pad('Street to entrance walk',(-1.0,1.0,-40,-22),0)
        m=G.Mesh('Accessible plaza approach',parent,actor_kind='site')
        m.prism([(-1,-23.9812,0),(1,-23.9812,0),(1,-22,.1524),(-1,-22,.1524)],(0,0,-.10),'concrete');m.finish()
        pad('Memorial garden walk',(9.0,25.8,-6.8,-4.5),0)
        pad('Memorial garden crosswalk',(13.2,15.1,-4.5,10.2),0)
        pad('Education route',(25.8,28,-7.0,17.0),.1524)
        p['dropoff_curve']=[(45,-26,0),(43.5,-18,0),(32,-14.5,0),(16,-14.5,0),(9,-17,0),(10,-21,0),(18,-25,0)]
    else:
        pad('Front approach',(-2.16,2.16,-23,-16.4),0)
        pad('Rear lot drive',(-20.5,-14.4,-22,44),.005,'asphalt')
        pad('Rear pedestrian way',(-14.4,17.5,19.1,21.2),0)
        pad('Ramp to rear route',(8.12,10.12,3.0,21),0)
        p['dropoff_curve']=[]
    p['paths']=[dict(name='Street_to_front',points=[(0,-40 if modern else -23,0),(0,-22 if modern else -17,0),(0,-p['length']/2,p['floor'])]),dict(name='Lot_to_door',points=[(23,-22,0),(10,-20,.1524),(1,-15,.1524)] if modern else [(9,23,0),(9,20,0),(9,3,0),(9,-5,.6096)])]
    # Rectangular turf clipping includes construction footprints, so lawns
    # meet paving and foundations without grass polygons through the lot.
    w=p['width'];l=p['length'];cuts.append((-w/2,w/2,-l/2,l/2))
    if modern:cuts += [(w/2,w/2+21,l/2+1.9,l/2+14.1),(w/2+17.535,w/2+26.065,-10.2,16.8)]
    else:cuts.append((w/2,w/2+10,l/2-11.315,l/2+3.315))
    bounds=(-22.2,60,-39.4,47) if modern else (-22.2,30,-23.4,47)
    xs=sorted({bounds[0],bounds[1],*[max(bounds[0],min(bounds[1],q)) for r in cuts for q in r[:2]],*[x for x in range(math.ceil(bounds[0]),math.floor(bounds[1]),2)]})
    ys=sorted({bounds[2],bounds[3],*[max(bounds[2],min(bounds[3],q)) for r in cuts for q in r[2:]],*[y for y in range(math.ceil(bounds[2]),math.floor(bounds[3]),2)]})
    m=G.Mesh('Parcel turf',parent,actor_kind='site')
    for a,b in zip(xs,xs[1:]):
        for c,d in zip(ys,ys[1:]):
            x=(a+b)/2;y=(c+d)/2
            if any(r[0]<x<r[1] and r[2]<y<r[3] for r in cuts):continue
            m.geom([(a,c,-.008),(b,c,-.008),(b,d,-.008),(a,d,-.008)],[(0,1,2,3)],'lawn')
    m.finish();return lot


def parking(p,parent,rect):
    from surfaces import paint_material
    paint_material();a,b,c,d=rect;modern=p['style']=='aframe';n=14 if modern else 10;start=a+2.5;pitch=2.7432
    m=G.Mesh('Parking stripes wheel stops and drains',parent,actor_kind='site');rng=random.Random(p['seed']+62)
    for row,y in enumerate((c+2.9,d-2.9)):
        for j in range(n):
            x=start+j*pitch
            if x+pitch/2>b-.7:continue
            # Keep one generous access aisle at the pedestrian-route end.
            if j==0:
                continue
            for xx in (x-pitch/2,x+pitch/2):
                pts=[(xx-.045,y-2.72,.012),(xx+.045,y-2.72,.012),(xx+.045,y+2.72,.012),(xx-.045,y+2.72,.012)]
                m.geom(pts,[(0,1,2,3)],'paint',uv=[[(.005,.755),(.12,.755),(.12,.995),(.005,.995)]])
            yy=y+(2.1 if row else -2.1);m.box((x,yy,.075),(1.70,.17,.15),'concrete')
            occupied=rng.random()<p['occupancy'];stall=G.root(f'Stall_{row}_{j}',(x,y,.01),parent,socket_kind='parked_car',stall_width=pitch,stall_depth=5.4864,occupied=occupied)
            p['stalls'].append(dict(name=stall.name,center=[x,y,.01],yaw=0 if row else 180,occupied=occupied))
            if occupied:car(row*20+j,(x+rng.uniform(-.12,.12),y+rng.uniform(-.16,.16),.012),0 if row else 180)
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
                    drive=arm==3 and side==1 and i==(5 if modern else 3)
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
    # Locally reduced distant hosts retain their library maps. Their canonical
    # deliveries are neither rewritten nor counted as this church's geometry.
    ranch=G.ROOT/'houses/export/HearthfieldRanch-11.gltf';cape=G.ROOT/'houses/export/HearthfieldCape-34.gltf'
    if modern:
        points=[(-12,53,0),(15,55,0),(44,54,0),(76,9,0),(-50,-18,90),(-50,12,90),(-7,-69,180),(25,-68,180),(55,-70,180)]
        for i,(x,y,yaw) in enumerate(points):instance(ranch if i%2 else cape,'Arterial neighbor '+str(i),(x,y,0),yaw,actor='town')
    else:
        host=G.ROOT/'church/build/hosts/downtown-opposite.glb'
        for i,x in enumerate((-20,-10,0,10,20,30,40)):
            instance(host,'One block from Main Street '+str(i),(x,56,0),actor='town')
        for i,y in enumerate((-12,15,42)):instance(ranch,'Side street house '+str(i),(-51,y,0),90,actor='town')
        for i,x in enumerate((-10,18,44)):instance(cape,'Across corner house '+str(i),(x,-54,0),180,actor='town')
    # Native foliage, at varied orientations and credible setbacks. Shrub roots
    # are selected from the single delivered two-species library.
    plants=[(-18,-17),(20,-17),(-20,17),(23,39),(49,26),(58,-4),(-48,35),(-45,-13)] if modern else [(-18,-20),(21,-20),(-21,8),(26,27),(-42,46),(43,48)]
    for i,(x,y) in enumerate(plants):
        instance(G.ROOT/('trees/export/PinOak.glb' if i%3==0 else 'trees/export/RedMaple.glb'),'Established street tree '+str(i),(x,y,0),i*53,.70 if modern else .61,actor='vegetation')
    for i in range(12 if modern else 7):
        point=(29.5,-7+i*1.65,0) if modern else (18,4+i*1.65,0)
        instance(G.ROOT/'shrubs/export/Shrubs.glb','Foundation shrub '+str(i),point,i*37,.87,kind='Hydrangea' if i%4==0 else 'Boxwood',actor='vegetation')
    for i,(x,y) in enumerate(((-22,-21),(22,-21),(49,-23)) if modern else ((-22,-22),(22,-22),(-22,20))):
        instance(G.ROOT/'street-light/export/StreetLight.glb','Street light '+str(i),(x,y,0),0,actor='site')
    instance(G.ROOT/'street-signs/export/StreetSigns.glb','Corner street names',(cx+5,cy+6,0),actor='site')
    if not modern:
        for i,(x,y,yaw) in enumerate(((8,-28.0,90),(20,-28.0,90),(-27,1,0),(-27,13,0))):car(80+i,(x,y,-.13),yaw)
    # A distant district plane closes the horizon below all authored surfaces.
    slab('Distant town ground',(-600,600,-600,600),-.18,'lawn',parent,.02)


def site(p,church):
    rt=G.root('ChurchSite_'+str(p['seed']),seed=p['seed']);church.parent=rt;church.location=p['placement_offset']
    lot=paving(p,rt);parking(p,rt,lot);settlement(rt,lot,p['seed']);town(p,rt)
    sign(rt,(17,-40 if p['style']=='aframe' else -22,0),p['name'],['CEDAR & BELL' if p['style']=='aframe' else 'GRACE CORNER','WORSHIP 10:30','ALL WELCOME'])
    # Accessible walk paths and drive curves ship as empty-node point lists.
    for row in p['paths']:G.root(row['name'],parent=rt,socket_kind='walk_path',points=row['points'])
    if p['dropoff_curve']:G.root('Dropoff route',parent=rt,socket_kind='drive_curve',points=p['dropoff_curve'])
    for ob in list(__import__('bpy').context.scene.objects):
        if ob!=rt and ob.parent is None and not ob.name.startswith('Template_'):ob.parent=rt
    clear();return rt
