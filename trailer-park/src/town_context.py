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
        n=0
        for ob in rt.children_recursive:
            if ob.type=='MESH':ob.data.calc_loop_triangles();n+=len(ob.data.loop_triangles);unique[category].add(ob.data)
        counts[category]+=n
        if path:placements.append(dict(kind=category,source=str(path),triangles=n,position=list(rt.location)))
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
            put(ground,'Public residential street',pos,90 if axis==0 else 0,'Road_Straight_'+('ABC'[j%3]),category='street')
    street(0,-D/2-4.15,-260,260)
    if old:street(0,D/2+4.15,-260,260)
    for side in (-1,1):street(1,side*(W/2+42),-D/2-4,D/2+110)
    # Typical small ranch parcels, roughly 62–75ft frontage. Their rear yards
    # face the old park boundary, with a real fence, sheds and irregular trees.
    for side in (-1,1):
        for j in range(-4,5):
            y=j*22.0+rng.uniform(-1,1)
            if abs(y)>D/2+12:continue
            seed=(11,12,13,14,15,16)[(j+side)%6]
            put(f'houses/export/HearthfieldRanch-{seed}.gltf','Backyard ranch',(side*(W/2+21),y,0),90 if side>0 else -90)
            if old:
                for k in range(8):put('fences/export/WoodPrivacy.glb','Backyard privacy line',(side*(W/2+1.0),y+(k-3.5)*2.4384,0),90,'Section_'+('AB'[k%2]))
            if j%2==0:put('trees/export/PinOak.glb','Neighbor yard oak',(side*(W/2+9),y+6,0),j*47,scale=.85,category='vegetation')
    if old:
        for sy in (-1,1):
            for j in range(-5,6):
                if sy<0 and abs(j)>2:continue
                seed=(11,13,14,16)[j%4]
                put(f'houses/export/HearthfieldRanch-{seed}.gltf','Cross-street ranch',(j*23+5,sy*(D/2+23),0),180 if sy<0 else 0)
        put('commercial/export/CommercialGas-101.gltf','Neighborhood corner gas',(-W/2-33,-D/2-34,0),180)
        put('trailer-park/build/native/strip-201.glb','Entrance shops',(W/2+55,-D/2-46,0),180)
    # A crop/field edge and multiple uneven tree ranks close the newer horizon.
    for j in range(-12,13):
        for rank in range(2 if old else 3):
            x=j*15+rng.uniform(-4,4);y=D/2+10+rank*14+rng.uniform(-3,3)
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
        rt=put(cars[j%3],'Public street car',(j*24+3,-D/2-14,0),90,category='cars');lib.factory(rt,j)
    for side in (-1,1):
        for j in range(-6,7):put('trees/export/RedMaple.glb','Side canopy',(side*(W/2+49),j*19+5,0),j*53,scale=.93,category='vegetation')
    totals={key:sum(len(me.loop_triangles) for me in meshes) for key,meshes in unique.items()}
    lib.clear();return dict(triangles=counts,unique_triangles=totals,placements=placements,dependencies=lib.dependencies)
