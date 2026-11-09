"""Site-owned paving and paths with native landscape, fence and furniture."""
import math,random
import bpy
from mathutils import Vector
from geo import Assembly,ROOT,LOCAL,root
from library import place,clear
from services import flagpole,bollard,back_service


def ground(a,name,rect,kind='Lawn',z=0,slope=None):
    from kit.tiling import material,world_uv
    ma=bpy.data.materials.get('CivicGround_'+kind)
    if not ma:ma=material(kind,ROOT/'ground/textures/ship',tint=True);ma.name='CivicGround_'+kind
    l,r,f,k=rect;m=a.mesh(name,kind='Site'+kind)
    nx=max(1,min(40,math.ceil((r-l)/3.048)));ny=max(1,min(40,math.ceil((k-f)/3.048)))
    for j in range(ny):
        for i in range(nx):
            x=l+i*(r-l)/nx;xx=l+(i+1)*(r-l)/nx;y=f+j*(k-f)/ny;yy=f+(j+1)*(k-f)/ny
            pts=[(x,y,z),(xx,y,z),(xx,yy,z),(x,yy,z)]
            if slope:pts=[(u,v,slope(v)) for u,v,_ in pts]
            m.geom(pts,[(0,1,2,3)],'Concrete')
    ob=m.finish();ob.data.materials.clear();ob.data.materials.append(ma)
    for face in ob.data.polygons:face.material_index=0
    world_uv(ob,6.096 if kind=='Asphalt' else 3.048)
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
                for s in (-1,1):paint.box((x+s*(r-l)/n/2,y,.007),(.075,5.4864,.012),'Trim',(.67,.66,.57),r=0)
            else:
                x=l+3.1;y=f+(j+.5)*(k-f)/n;yaw=-90
                for s in (-1,1):paint.box((x,y+s*(k-f)/n/2,.007),(5.4864,.075,.012),'Trim',(.67,.66,.57),r=0)
            node=a.socket(lot['id']+f'_Stall_{row}_{j}',(x,y,.015),'parked_car');node.rotation_euler.z=math.radians(yaw)
            node['occupied']=((j*7+row*3+a.root.get('seed',0))%10)<8;node['police']=lot['id']=='Police';slots.append((x,y,yaw))
            if j%3!=1:decal(a,'EngineDrips_'+lot['id']+str(row)+'_'+str(j),(x,y+1.1,.004),(1.1,2.0),'oil',j+row*20)
    paint.finish()
    if lot['fenced']:
        fence=ROOT/'fences/chain-link/export/ChainLink.glb'
        for j in range(math.floor((r-l)/3.048)):
            x=l+(j+.5)*3.048
            for y in (f,k):
                if y==f and j==2:continue
                place(fence,'PoliceFence',(x,y,0),select='Chain_Section',parent=a.root)
                place(fence,'PoliceLinePost',(l+j*3.048,y,0),select='Chain_Line',parent=a.root)
        for x in (l,l+math.floor((r-l)/3.048)*3.048):
            for j in range(math.floor((k-f)/3.048)):
                place(fence,'PoliceFenceReturn',(x,f+(j+.5)*3.048,0),90,'Chain_Section',a.root)
                place(fence,'PoliceReturnPost',(x,f+j*3.048,0),90,'Chain_Line',a.root)
    return slots


def build_site(sp,building,off):
    a=Assembly('CivicSite_'+str(sp['seed']));a.root['seed']=sp['seed'];p=sp['building'];pos=sp['building_at'];building.root.parent=a.root;building.root.location=Vector(pos)+off
    l,r,f,k=sp['parcel'];w,d=p['width'],p['depth'];x,y,_=pos
    excluded=[(x-w/2,x+w/2,y-d/2,y+d/2)]+[lot['rect'] for lot in sp['lots']]+sp['walks']
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
    for lot in sp['lots']:ground(a,'Lot_'+lot['id'],lot['rect'],'Asphalt',-.003);parking(a,lot)
    for j,pole in enumerate(sp['flags']):flagpole(a,(*pole,0),'Flagpole_'+str(j))
    for j,(xx,yy) in enumerate(sp['trees']):place(ROOT/'trees/export'/('PinOak.glb' if j%3==0 else 'RedMaple.glb'),'SiteTree_'+str(j),(xx,yy,-.02),j*61,parent=a.root)
    for j in range(7):
        at=(x-w/2+1+j*2.3,y-d/2-1.2,0) if sp['kind']=='downtown' else (12.4,-4+j*1.1,0)
        place(ROOT/'shrubs/export/Shrubs.glb','FoundationBoxwood_'+str(j),at,j*47,'Boxwood',a.root)
    benches=[(x-7,-17,.145),(x+7,-17,.145)] if sp['kind']=='downtown' else [(12,-11,.145),(13.3,-7,.145)]
    for j,at in enumerate(benches):place(LOCAL/'build/context/furniture.glb','EntryBench_'+str(j),at,select='Bench',parent=a.root)
    place(LOCAL/'build/context/furniture.glb','BikeRack',(x+10,-15,.145) if sp['kind']=='downtown' else (12.3,-13,.145),select='BikeRack',parent=a.root)
    back_service(a,(34,31,0))
    from services import dumpster
    dumpster(a,(29,34,0))
    from services import public_details
    public_details(a,(12,-7,0) if sp['kind']=='arterial' else (11.5,-.5,.145),sp['kind']=='arterial')
    if sp['kind']=='arterial':place(LOCAL/'build/context/hydrant.glb','StreetHydrant',(-25,-31.5,0),parent=a.root)
    path(a,'StreetToEntry',[(x,-29,.145),(x,-15,.145),(x,-13,.145)])
    if sp['kind']=='downtown':path(a,'ParkingToAccessible',[(23,-2,.015),(20.4,-2,.145),(10.3,-2,.145),(10.3,-.2,.1524)])
    else:path(a,'ParkingToAccessible',[(17,-2,.015),(12,-2,.145),(7.5,-5,.1524)])
    if apron:
        for j in range(p['bays']):
            xx=x-w/2+.4572+(j+.5)*p['bay_width'];path(a,'ApparatusExit_'+str(j),[(xx,y,0),(xx,-27,.04),(xx,-39,0)],'drive',4.2672)
            for side in (-1,1):bollard(a,(xx+side*2.40,y-d/2-.4,0),'BayBollard')
        from wear import apron_wear
        apron_wear(a,sp)
    from delivery import counts
    veg=[o for o in a.root.children_recursive if o.type=='MESH' and any(k in o.name for k in ('SiteTree_','FoundationBoxwood_'))]
    sp['vegetation']=counts(veg);sp['static_site']=counts([o for o in a.root.children_recursive if o not in veg])
    clear();return a
