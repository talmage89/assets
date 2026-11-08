"""Closed town settings from the native houses, Commercial, Ground and trees."""
import math,random
import bpy
from geometry import Library,ROOT


def context(plan):
    import importlib.util
    from pathlib import Path
    spec=importlib.util.spec_from_file_location('_town_terrain',Path(__file__).with_name('site.py'));S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
    lib=Library();W,D=plan['size'];old=plan['kind']=='old';rng=random.Random(plan['seed']+231)
    parent=bpy.data.objects.new('TownContext',None);bpy.context.collection.objects.link(parent)
    counts=dict(cars=0,vegetation=0,town_architecture=0,street=0);unique={k:set() for k in counts};placements=[]
    def count(rt,category,path=None):
        n=0;by_category={}
        for ob in rt.children_recursive:
            if ob.type!='MESH':continue
            ob.data.calc_loop_triangles();cost=len(ob.data.loop_triangles);n+=cost;kind=category
            if category=='town_architecture' and any(any(t in ma.name.lower() for t in ('shrubs','maple','oak','foliage','leaves')) for ma in ob.data.materials if ma):kind='vegetation'
            counts[kind]+=cost;unique[kind].add(ob.data);by_category[kind]=by_category.get(kind,0)+cost
        if path:placements.append(dict(kind=category,source=str(path),triangles=n,category_triangles=by_category,position=list(rt.location)))
        return rt
    def put(path,name,pos,yaw=0,select=None,scale=1,category='town_architecture'):
        rt=lib.place(ROOT/path,name,pos,yaw,select=select,scale=(scale,scale,scale));rt.parent=parent
        return count(rt,category,path)
    ground='ground/export/Ground.glb';turf=S.library_material(lib,'Lawn')
    # Distant flat land is entirely behind bounded backyards or a planted edge.
    for x0,x1,y0,y1 in ((-900,-W/2,-900,900),(W/2,900,-900,900),(-W/2,W/2,-900,-D/2),(-W/2,W/2,D/2,900)):
        S.ground_box(parent,'Continuing summer land',((x0+x1)/2,(y0+y1)/2,-.048),(x1-x0,y1-y0,.09),turf,3.048,(.96,.83,.49))
    def street(axis,c,lo,hi):
        for j in range(math.ceil((hi-lo)/6.096)):
            t=lo+(j+.5)*6.096;pos=(t,c,-.00635) if axis==0 else (c,t,-.00635)
            history=random.Random(plan['seed']+j*109+axis*157+round(c*100)).choice('AAAAABC')
            put(ground,'Public residential street',pos,90 if axis==0 else 0,'Road_Straight_'+history,category='street')
    street(0,-D/2-3.65,-260,260)
    if old:street(0,D/2+3.65,-260,260)
    for side in (-1,1):street(1,side*(W/2+42),-D/2-4,D/2+110)
    # Typical small ranch parcels, roughly 62–75ft frontage. Their rear yards
    # face the old park boundary, with a real fence, sheds and irregular trees.
    for side in (-1,1):
        for j in range(-4,5):
            y=(j+(.5 if old else 0))*22.0+rng.uniform(-1,1)
            # Reserve the cross-street corners. A full ranch envelope is
            # about 20m along this frontage, and must clear the road itself.
            if abs(y)>D/2-16:continue
            seed=(11,12,13,14,15,16)[(j+side)%6]
            put(f'houses/export/HearthfieldRanch-{seed}.gltf','Backyard ranch',(side*(W/2+21),y,0),90 if side>0 else -90)
            if old:
                put(f'houses/export/HearthfieldRanch-{(11,12,13,14,15,16)[(j+side+2)%6]}.gltf',
                    'Across-street ranch',(side*(W/2+63),y,0),-90 if side>0 else 90)
            if old:
                for k in range(8):put('fences/export/WoodPrivacy.glb','Backyard privacy line',(side*(W/2+1.0),y+(k-3.5)*2.4384,0),90,'Section_'+('AB'[k%2]))
                for k in range(9):put('fences/export/WoodPrivacy.glb','Backyard fence posts',(side*(W/2+1.0),y+(k-4)*2.4384,0),90,'Post_Line' if 0<k<8 else 'Post_End')
            if j%2==0:put('trees/export/PinOak.glb','Neighbor yard oak',(side*(W/2+9),y+6,0),j*47,scale=.85,category='vegetation')
    if old:
        for sy in (-1,1):
            for j in range(-5,6):
                if sy<0 and abs(j)>2:continue
                if any(abs(j*23+5-s*(W/2+42))<17 for s in (-1,1)):continue
                seed=(11,13,14,16)[j%4]
                put(f'houses/export/HearthfieldRanch-{seed}.gltf','Cross-street ranch',(j*23+5,sy*(D/2+23),0),180 if sy<0 else 0)
        road_south=D/2+3.65+3.6576
        # Native lots are 45.72m and 60.96m deep; their front throats meet
        # the 7.3152m public asphalt edge rather than stopping in the grass.
        put('commercial/export/CommercialGas-101.gltf','Neighborhood corner gas',(-W/2-33,-road_south-22.86,0),180)
        put('trailer-park/build/native/strip-201.glb','Entrance shops',(W/2+55,-road_south-30.48,0),180)
        # A second ordinary residential block closes the older aerial's
        # former empty field. Cross-street corners remain reserved parcels.
        street(0,D/2+70,-260,260)
        for offset,yaw in ((48,180),(92,0)):
            for j in range(-7,8):
                x=j*23+5
                if any(abs(x-s*(W/2+42))<17 for s in (-1,1)):continue
                seed=(11,12,13,14,15,16)[(j+int(offset))%6]
                put(f'houses/export/HearthfieldRanch-{seed}.gltf','Next town block',(x,D/2+offset,0),yaw)
    # A crop/field edge and multiple uneven tree ranks close the newer horizon.
    for j in range(-12,13):
        for rank in range(3):
            x=j*15+rng.uniform(-4,4)
            y=D/2+(11,35.5,110)[rank]+rng.uniform(-1.2,1.2) if old else D/2+10+rank*14+rng.uniform(-3,3)
            put('trees/export/'+('PinOak.glb' if (j+rank)%3 else 'RedMaple.glb'),'Distant tree line',(x,y,0),rng.uniform(0,360),scale=rng.uniform(.78,1.22),category='vegetation')
    cars=['cars/export/'+f for f in ('AlderC150.glb','AlderX220.glb','AlderH120.glb')]
    bpy.context.view_layer.update()
    markers=sorted([o for o in bpy.context.scene.objects if o.get('socket_kind') in ('car','tree','shrub') and not o.name.startswith('Library')],key=lambda o:o.name)
    for j,o in enumerate(markers):
        kind=o['socket_kind'];xf=o.matrix_world;pos=xf.translation;yaw=math.degrees(xf.to_euler().z)
        if kind=='car':
            if not o.get('occupied',True):continue
            rt=put(cars[int(o.get('vehicle_index',j%3))],'Resident car',pos,yaw,category='cars');lib.factory(rt,(3,4,0,1,2)[j%5])
        elif kind=='tree':
            put('trees/export/'+('PinOak.glb' if o.get('species')=='oak' else 'RedMaple.glb'),'Mature lot canopy' if old else 'Young lot tree',pos,j*47,scale=float(o.get('plant_scale',1)),category='vegetation')
        else:put('shrubs/export/Shrubs.glb','Resident planting',pos,j*31,'Hydrangea' if j%4==0 else 'Boxwood',.84,'vegetation')
    for j in range(-6,7):
        x=j*24+3;entries=(-plan['loop_x'],plan['loop_x']) if old else (0,)
        if any(abs(x-entry)<7 for entry in entries):continue
        # Shoulder parking on the actual 2% Ground crown; entrances stay clear.
        rt=put(cars[j%3],'Public street car',(x,-D/2-3.65+2.6,(3.6576-2.6)*.02),90,category='cars');lib.factory(rt,j)
    for side in (-1,1):
        for j in range(-6,7):put('trees/export/RedMaple.glb','Side canopy',(side*(W/2+49),j*19+5,0),j*53,scale=.93,category='vegetation')
    totals={key:sum(len(me.loop_triangles) for me in meshes) for key,meshes in unique.items()}
    lib.clear();return dict(triangles=counts,unique_triangles=totals,placements=placements,dependencies=lib.dependencies)
