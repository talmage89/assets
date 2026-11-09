"""Site-owned paving and paths with native landscape, fence and furniture."""
import math,random
import bpy
from mathutils import Vector
from geo import Assembly,ROOT,LOCAL,root
from library import place,clear
from services import bollard,back_service


def ground(a,name,rect,kind='Lawn',z=0,slope=None,grade=None):
    from kit.tiling import material,world_uv
    ma=bpy.data.materials.get('CivicGround_'+kind)
    if not ma:
        ma=material('GardenLawn' if kind=='Lawn' else kind,LOCAL/'textures/lawn' if kind=='Lawn' else ROOT/'ground/textures/ship',tint=True);ma.name='CivicGround_'+kind
    l,r,f,k=rect;m=a.mesh(name,kind='Site'+kind,authored_winding=True,allow_boundary=True)
    height=lambda u,v:grade(u,v) if grade else slope(v) if slope else z
    step=.85 if kind=='Lawn' and r-l<150 else 3.048
    nx=max(1,min(100,math.ceil((r-l)/step)));ny=max(1,min(100,math.ceil((k-f)/step)))
    for j in range(ny):
        for i in range(nx):
            x=l+i*(r-l)/nx;xx=l+(i+1)*(r-l)/nx;y=f+j*(k-f)/ny;yy=f+(j+1)*(k-f)/ny
            pts=[(u,v,height(u,v)) for u,v in ((x,y),(xx,y),(xx,yy),(x,yy))]
            m.geom(pts,[(0,1,2,3)],'Concrete')
    if kind=='Concrete' and (z>.02 or slope or grade):
        corners=[(u,v,height(u,v)) for u,v in ((l,f),(r,f),(r,k),(l,k))]
        for aa,bb in zip(corners,corners[1:]+corners[:1]):
            m.geom([aa,(aa[0],aa[1],-.035),(bb[0],bb[1],-.035),bb],[(0,1,2,3)],'Concrete')
    ob=m.finish();ob.data.materials.clear();ob.data.materials.append(ma)
    for face in ob.data.polygons:face.material_index=0
    world_uv(ob,6.096 if kind=='Asphalt' else 3.048)
    for face in ob.data.polygons:
        if abs(face.normal.z)>.5:continue
        axis=max(range(3),key=lambda k:abs(face.normal[k]));aa,bb=[(1,2),(0,2),(0,1)][axis]
        for li in face.loop_indices:
            q=ob.data.vertices[ob.data.loops[li].vertex_index].co;ob.data.uv_layers.active.data[li].uv=(q[aa]/3.048,q[bb]/3.048)
    c=ob.data.color_attributes['Tint']
    for li,loop in enumerate(ob.data.loops):
        q=ob.data.vertices[loop.vertex_index].co
        if kind=='Lawn':rgb=(.74,.78,.63);fac=.9+.1*math.sin(q.x*.34+q.y*.18)*math.sin(q.y*.63)
        elif kind=='Asphalt':rgb=(.72,.73,.72);fac=.97+.035*math.sin(q.x*.4+q.y*.25)
        else:rgb=(.91,.90,.86);fac=.965+.04*math.sin(math.floor(q.x/3.048)*2.1+math.floor(q.y/3.048)*3.8)
        c.data[li].color=(*(v*fac for v in rgb),1)
    return ob


def path(a,name,points,kind='walk',width=1.524):
    cv=bpy.data.curves.new(name,'CURVE');cv.dimensions='3D';sp=cv.splines.new('POLY');sp.points.add(len(points)-1)
    for cp,p in zip(sp.points,points):cp.co=(*p,1)
    ob=bpy.data.objects.new(a.root.name+'__Path_'+name,cv);bpy.context.collection.objects.link(ob);ob.parent=a.root
    ob['path_kind']=kind;ob['clear_width_m']=width;ob['points_m']=[v for p in points for v in p]
    return ob


def parking(a,lot):
    from wear import decal
    l,r,f,k=lot['rect'];across=(r-l)>(k-f);n=lot['stalls'];rows=lot['rows'];slots=[]
    paint=a.mesh(lot['id']+'_ParkingPaint',kind='ParkingMarkings',trim_strip=5)
    for row in range(rows):
        for j in range(n):
            if across:
                x=l+(j+.5)*(r-l)/n;y=f+2.9 if row==0 else k-2.9;yaw=0 if row==0 else 180
                for s in ((-1,1) if j==0 else (1,)):decal(a,'ParkingPaint_'+lot['id']+f'_{row}_{j}_{s}',(x+s*(r-l)/n/2,y,0),(.075,5.4864),'paint',j+row*7)
            else:
                x=l+3.1;y=f+(j+.5)*(k-f)/n;yaw=-90
                for s in ((-1,1) if j==0 else (1,)):decal(a,'ParkingPaint_'+lot['id']+f'_{row}_{j}_{s}',(x,y+s*(k-f)/n/2,0),(5.4864,.075),'paint',j+row*7)
            node=a.socket(lot['id']+f'_Stall_{row}_{j}',(x,y,.015),'parked_car');node.rotation_euler.z=math.radians(yaw)
            reserved=(lot['id']=='Staff' and j==0) or (lot['id']=='Public' and j==1) or (lot['id']=='Police' and j==2) or j==lot.get('service_stall',-1)
            node.location.z=-.003;node['occupied']=((j*7+row*3+a.root.get('seed',0))%10)<8 and not reserved;node['police']=lot['id']=='Police';slots.append((x,y,yaw))
            if j%3!=1:decal(a,'EngineDrips_'+lot['id']+str(row)+'_'+str(j),(x,y+1.1,.004),(1.1,2.0),'oil',j+row*20)
    paint.finish()
    if lot['fenced']:
        fence=ROOT/'fences/chain-link/export/ChainLink.glb'
        def run(start,end,gap=None):
            aa,bb=Vector((*start,0)),Vector((*end,0));axis=(bb-aa).normalized();length=(bb-aa).length
            cuts=[0,length]+list(gap or ());cuts=sorted(set(cuts))
            for lo,hi in zip(cuts,cuts[1:]):
                if gap and lo>=gap[0] and hi<=gap[1]:continue
                count=math.ceil((hi-lo)/3.048)
                for j in range(count):
                    u=lo+j*(hi-lo)/count;span=(hi-lo)/count;mid=aa+axis*(u+span/2)
                    rt=place(fence,'PoliceFence',tuple(mid),math.degrees(math.atan2(axis.y,axis.x)),'Chain_Section',a.root);rt.scale.x=span/3.048
                    place(fence,'PolicePost',tuple(aa+axis*u),select='Chain_Line',parent=a.root)
                place(fence,'PoliceTerminal',tuple(aa+axis*hi),select='Chain_Terminal',parent=a.root)
        run((l,f),(r,f),(6.096,9.144));run((l,k),(r,k));run((l,f),(l,k))
        # The east opening reaches the rear maneuvering aisle, away from stalls.
        run((r,f),(r,k),(30-f,36-f))
    return slots


def build_site(sp,building,off):
    a=Assembly('CivicSite_'+str(sp['seed']));a.root['seed']=sp['seed'];p=sp['building'];pos=sp['building_at'];building.root.parent=a.root;building.root.location=Vector(pos)+off
    l,r,f,k=sp['parcel'];w,d=p['width'],p['depth'];x,y,_=pos
    excluded=[(x-w/2,x+w/2,y-d/2,y+d/2)]+[lot['rect'] for lot in sp['lots']]+sp['walks']+[q['rect'] for q in sp['ramps']]+sp['drives']+sp['service_pads']
    from turf import beds
    excluded+=beds(a,sp)
    apron=None
    if sp['kind']=='arterial':
        apron=(x-w/2-.5,x-w/2+p['bayblock']+.5,-32,y-d/2);excluded.append(apron)
        ground(a,'ApparatusApron',apron,'Concrete',slope=lambda q:.1524*(q+32)/(y-d/2+32))
    # Exact rectangle partition: lawn never overlaps the active hardscape.
    xs=sorted({l,r,*[max(l,min(r,v)) for q in excluded for v in q[:2]]});ys=sorted({f,k,*[max(f,min(k,v)) for q in excluded for v in q[2:]]})
    for aa,bb in zip(xs,xs[1:]):
        for cc,dd in zip(ys,ys[1:]):
            mid=((aa+bb)/2,(cc+dd)/2)
            if any(q[0]<mid[0]<q[1] and q[2]<mid[1]<q[3] for q in excluded):continue
            ground(a,'MunicipalLawn',(aa,bb,cc,dd),'Lawn',-.012)
    for j,q in enumerate(sp['walks']):ground(a,'Walk_'+str(j),q,'Concrete',.145)
    for j,q in enumerate(sp['ramps']):
        aa,bb,_,_=q['rect'];ground(a,'AccessibleRamp_'+str(j),q['rect'],'Concrete',grade=lambda u,v,l=aa,r=bb:q['high']+(q['low']-q['high'])*(u-l)/(r-l))
    for lot in sp['lots']:ground(a,'Lot_'+lot['id'],lot['rect'],'Asphalt',-.003);parking(a,lot)
    for j,q in enumerate(sp['drives']):ground(a,'VehicleConnection_'+str(j),q,'Asphalt',-.003)
    for j,q in enumerate(sp['service_pads']):ground(a,'RearServicePad_'+str(j),q,'Concrete',-.003)
    from flags import pole as flag
    for j,pole in enumerate(sp['flags']):
        flag(a,(*pole,0),'Flagpole_'+str(j),national=j==0)
        from aging import rust
        rust(a,(*pole,.122),'FlagpoleFootRust_'+str(j))
    for j,(xx,yy) in enumerate(sp['trees']):place(ROOT/'trees/export'/('PinOak.glb' if j%3==0 else 'RedMaple.glb'),'SiteTree_'+str(j),(xx,yy,-.02),j*61,parent=a.root)
    for j in range(7):
        at=([(-19.4,-9.9,-.012),(-17.2,-9.9,-.012),(-15,-9.9,-.012),(-12.8,-9.9,-.012),(1.2,-9.9,-.012),(3.4,-9.9,-.012),(5.6,-9.9,-.012)][j]) if sp['kind']=='downtown' else (14.0,-4+j*1.1,-.012)
        place(ROOT/'shrubs/export/Shrubs.glb','FoundationBoxwood_'+str(j),at,j*47,'Boxwood',a.root)
    benches=[(x-7,-17,.145),(x+7,-17,.145)] if sp['kind']=='downtown' else [(11.8,-10.3,.145),(13.2,-12.5,.145)]
    for j,at in enumerate(benches):place(LOCAL/'build/context/furniture.glb','EntryBench_'+str(j),at,select='Bench',parent=a.root)
    place(LOCAL/'build/context/furniture.glb','BikeRack',(x+10,-15,.145) if sp['kind']=='downtown' else (13.3,-8.5,.145),select='BikeRack',parent=a.root)
    back_service(a,sp['generator'])
    from services import dumpster
    dumpster(a,sp['dumpster'])
    from services import public_details
    public_details(a,(12,-7,.145) if sp['kind']=='arterial' else (11.5,-.5,.145),sp['kind']=='arterial',sp['road_y']+sp['road_width']/2+.6)
    if sp['kind']=='arterial':place(LOCAL/'build/context/hydrant.glb','StreetHydrant',(-25,-30.7,-.012),parent=a.root)
    if sp['kind']=='downtown':
        # Follow a stair lane beside the center handrail to the real leaf.
        count=round(p['floor']/.1524);lane=x+.50;front=y-d/2-3.45
        treads=[(lane,front-(count-j-.5)*.3302,(j+1)*.1524) for j in range(count)]
        path(a,'StreetToEntry',[(lane,-29,.145),(lane,-14.3,.145)]+treads+[(lane,y-d/2-.12,p['floor'])])
        path(a,'ParkingToAccessible',[(23,-2,.015),(20.4,-2,.145),(10.3,-2,.145),(10.3,-.2,.1524)])
        path(a,'PoliceLotToDoor',[(-13.3,25,.015),(-13.3,22.10,.015),(-13.3,21.9,.145),(-13.3,20.73,.1524)])
        path(a,'PublicAndPoliceDrive',[(33,-35,-.03),(33,-6,-.003),(33,33,-.003),(9,33,-.003),(-10,33,-.003)],'drive',6)
        path(a,'ServiceAccess',[(33,22.45,-.003),(17.5,22.45,-.003),(17.5,23.7,-.003)],'drive',3.7)
    else:
        entry=x-w/2+p['bayblock']+p['office']/2
        path(a,'StreetToEntry',[(entry,-32,.145),(entry,-7,.145),(entry,y-d/2-.12,.1524)])
        path(a,'ParkingToAccessible',[(17,-2,.015),(12.8,-2,.145),(12,-2,.145),(12,-7,.145),(entry,-7,.145),(entry,y-d/2-.12,.1524)])
        path(a,'StaffLotDrive',[(32,-41,-.03),(32,-2,-.003),(32,17,-.003)],'drive',8)
        path(a,'ServiceAccess',[(29,20,-.003),(29,30,-.003),(29,33.3,-.003)],'drive',4)
    if apron:
        for j in range(p['bays']):
            xx=x-w/2+.4572+(j+.5)*p['bay_width'];path(a,'ApparatusExit_'+str(j),[(xx,y,0),(xx,-27,.04),(xx,-39,0)],'drive',4.2672)
            for side in (-1,1):bollard(a,(xx+side*2.40,y-d/2-.4,0),'BayBollard')
        from wear import apron_wear
        apron_wear(a,sp)
    from turf import finish as finish_turf
    finish_turf(a,sp,excluded)
    from delivery import counts
    veg=[o for o in a.root.children_recursive if o.type=='MESH' and any(k in o.name for k in ('SiteTree_','FoundationBoxwood_'))]
    sp['vegetation']=counts(veg);sp['static_site']=counts([o for o in a.root.children_recursive if o not in veg])
    clear();return a
