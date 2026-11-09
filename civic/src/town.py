"""Native town closes every camera; cars are separate presentation actors."""
import math,random,json,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from geo import ROOT,LOCAL,Assembly
from library import place,clear
from plans import site
from sites import ground


def context(seed):
    from actors import finish,CACHE as AC
    AC.clear()
    sp=site(seed);a=Assembly('TownPresentation');a.root['presentation_only']=True
    ground(a,'ContinuingTownGround',(-650,650,-650,650),'Lawn',-.055)
    ry=sp['road_y'];rw=sp['road_width'];l,r,ff,k=sp['parcel']
    ground(a,'PublicArterial',(-650,650,ry-rw/2,ry+rw/2),'Asphalt',-.03)
    from wear import decal
    for j in range(-65,66):
        for side in (-1,1):decal(a,'DoubleYellowCenter',(j*3.048,ry+side*.105,-.026),(3.048,.1016),'paint',j,color=(1,.64,.025))
    for side in (-1,1):
        yy=ry+side*(rw/2+1.524)
        crossings=sorted(sp['vehicle_crossings']+([(-20.4,-1.3)] if seed==202 else [])) if side>0 else []
        spans=[];last=-240
        for aa,bb in crossings:spans.append((last,aa));last=bb
        spans.append((last,240))
        for aa,bb in spans:ground(a,'PublicSidewalk',(aa,bb,yy-.762,yy+.762),'Concrete',.145)
        for aa,bb in crossings:ground(a,'LoweredVehicleCrossing',(aa,bb,ry+rw/2-.05,yy+.762),'Concrete',-.015)
    # Native crowned road, curb and sidewalk cross streets bound actual blocks.
    for xx in (-48,48):
        ground(a,'CrossStreet',(xx-4.2,xx+4.2,-200,220),'Asphalt',-.028)
        for side in (-1,1):ground(a,'CrossSidewalk',(xx+side*6-.762,xx+side*6+.762,-200,220),'Concrete',.145)
    place(ROOT/'street-signs/export/StreetSigns.glb','NativeCornerStreetSign',(-43,ry+rw/2+2.7,.145),180,parent=a.root)
    # At street scale preserve native dropped curb/driveway and corner shapes.
    for j in range(-36,37):
        x=j*3.048
        for side in (-1,1):
            crossings=sp['vehicle_crossings']+([(-20.4,-1.3)] if seed==202 else [])
            if side>0 and any(x+1.524>aa and x-1.524<bb for aa,bb in crossings):continue
            yy=ry+side*rw/2
            place(ROOT/'ground/export/Ground.glb','StreetCurb',(x,yy,-.012),90 if side<0 else -90,'Curb_Straight',a.root)
    town=LOCAL/'textures/shared/downtown/build/blocks/midwest/block.glb'
    if seed==101:
        for j,(pos,yaw) in enumerate([((-52,2,0),90),((55,4,0),-90),((-8,60,0),0),((-4,-62,0),180),((-8,110,0),0),((104,10,0),-90)]):
            place(town,'NeighboringDowntownBlock_'+str(j),pos,yaw,parent=a.root)
    else:
        for j in range(-4,5):
            place(LOCAL/'build/context/house.glb','AcrossStreetRanch_'+str(j),(j*23,-63,-.01),180,parent=a.root)
            place(LOCAL/'build/context/house.glb','RearRanch_'+str(j),(j*24,57,-.01),0,parent=a.root)
        place(town,'ArterialShops',(72,-3,0),-90,parent=a.root)
    # Delivered oak/maple and boxwood only; street and distant rows close above views.
    for j in range(-9,10):
        for yy in (-52,52):
            if abs(j)<2 and yy<0:continue
            place(ROOT/'trees/export'/('PinOak.glb' if j%3==0 else 'RedMaple.glb'),'TownTree_'+str(j)+'_'+str(yy),(j*23,yy+(j%3)*2,-.04),j*37,parent=a.root)
    poles=[]
    for j in range(-4,5):
        if not any(aa-1<j*32<bb+1 for aa,bb in sp['vehicle_crossings']):place(ROOT/'street-light/export/StreetLight.glb','StreetLight_'+str(j),(j*32,ry+rw/2+2.7,.145),0,parent=a.root)
        poles.append(place(LOCAL/'build/context/utility.glb','UtilityPole_'+str(j),(j*40,ry-rw/2-3,0),90,'Tangent',a.root))
    # These native pole roots expose their attachment sockets; conductors sag
    # between them at true centimeter gauge, rather than straight proxy lines.
    m=a.mesh('OverheadConductors',kind='NativeUtilitySpan',trim_strip=2)
    bpy.context.view_layer.update()
    for left,right in zip(poles,poles[1:]):
        def pins(rt):return sorted([o for o in rt.children_recursive if 'Socket_Primary_' in o.name],key=lambda o:o.name)
        assert len(pins(left))==len(pins(right))==3
        for pa,pb in zip(pins(left),pins(right)):
            start,end=pa.matrix_world.translation,pb.matrix_world.translation
            pts=[tuple(start.lerp(end,t)-Vector((0,0,1.1*4*t*(1-t)))) for t in [i/16 for i in range(17)]]
            m.tube(pts,float(pa.get('diameter_m',.0101))/2,'Trim',(.009,.010,.008),sides=4)
    m.finish()
    # Occupancy follows every exported stall socket; cars are native deliveries,
    # separate from civic/site budgets, with linked meshes and preserved maps.
    actors=[]
    for node in list(bpy.context.scene.objects):
        if node.get('socket_kind')!='parked_car' or not node.get('occupied'):continue
        bpy.context.view_layer.update();p=node.matrix_world.translation
        car=place(ROOT/'cars/export/AlderS240.glb','ParkedPoliceCar' if node.get('police') else 'ParkedStaffCar',tuple(p),math.degrees(node.matrix_world.to_euler().z),parent=a.root)
        finish(car,'Carbon' if node.get('police') else ['Porcelain','Graphite','Atlantic','Aluminum'][len(actors)%4],bool(node.get('police')));actors.append(car)
    parked=len(actors)
    # On-street weekday parking and two passing cars, clear of the apron.
    for j in range(-5,6):
        if seed==202 and -24<j*8<0:continue
        if abs(j*8-24)<6:continue
        car=place(ROOT/'cars/export'/('AlderC150.glb' if j%4==0 else 'AlderS240.glb'),'OnStreetCar_'+str(j),(j*8,ry-rw/2+1.2,-.015),90,parent=a.root)
        finish(car,['Porcelain','Atlantic','Graphite','Aluminum'][j%4]);actors.append(car)
    from delivery import counts
    label=f'cars-{seed}' if parked else f'cars-context-{seed}'
    receipt=Path('build',label+'.json');recipe=hashlib.sha256(b''.join(p.read_bytes() for p in sorted((LOCAL/'src').glob('*.py')))+repr([(rt.name,tuple(rt.location),tuple(rt.rotation_euler)) for rt in actors]).encode()).hexdigest()
    previous=json.loads(receipt.read_text()) if receipt.exists() else {}
    if previous.get('recipe_sha256')!=recipe:
        metrics=counts([o for rt in actors for o in rt.children_recursive]);metrics.update(actors=len(actors),parked_stall_actors=parked,on_street_actors=len(actors)-parked,recipe_sha256=recipe);receipt.write_text(json.dumps(metrics,indent=2)+'\n')
    clear();return a
